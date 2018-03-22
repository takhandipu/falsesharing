from collections import namedtuple
from datetime import datetime
import csv
import math
import time
import os

import tensorflow.python.platform
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer('batch_size', 128,
                            """Batch size.""")
tf.app.flags.DEFINE_integer('num_batches', 1,
                            """Number of batches to run.""")
tf.app.flags.DEFINE_boolean('forward_only', True,
                            """Only run the forward pass.""")
tf.app.flags.DEFINE_boolean('forward_backward_only', False,
                            """Only run the forward-forward pass.""")
tf.app.flags.DEFINE_string('data_format', 'NHWC',
                           """The data format for Convnet operations.
                           Can be either NHWC or NCHW.
                           """)
tf.app.flags.DEFINE_string('csv_file', 'conv.csv',
                           """File to output timing information to in csv
                           format. If not file is passed in, csv file will
                           not be cteated.
                           """)

parameters = []
conv_counter = 1

TimingEntry = namedtuple(
    'TimingEntry', ['info_string', 'timestamp', 'num_batches', 'mean', 'sd'])

def _conv(inpOp, nIn, nOut, kH, kW, dH, dW, padType):
    global conv_counter
    global parameters
    name = 'conv' + str(conv_counter)
    conv_counter += 1
    with tf.name_scope(name) as scope:
        kernel = tf.Variable(tf.truncated_normal([kH, kW, nIn, nOut],
                                                 dtype=tf.float16,
                                                 stddev=1e-1), name='weights')
        if FLAGS.data_format == 'NCHW':
          strides = [1, 1, dH, dW]
        else:
          strides = [1, dH, dW, 1]
        conv = tf.nn.conv2d(inpOp, kernel, strides, padding=padType,
                            data_format=FLAGS.data_format)
        biases = tf.Variable(tf.constant(0.0, shape=[nOut], dtype=tf.float16),
                             trainable=True, name='biases')
        bias = tf.reshape(tf.nn.bias_add(conv, biases,
                                         data_format=FLAGS.data_format),
                          conv.get_shape())
        # conv1 = tf.nn.relu(bias, name=scope)
        parameters += [kernel, biases]
        return bias

def inference(images):
    conv1 = _conv (images, 3, 64, 11, 11, 4, 4, 'VALID')
    return conv1

def time_tensorflow_run(session, target, info_string):
  num_steps_burn_in = 0
  total_duration = 0.0
  total_duration_squared = 0.0
  if not isinstance(target, list):
    target = [target]
  target_op = tf.group(*target)
  for i in range(FLAGS.num_batches + num_steps_burn_in):
    start_time = time.time()
    _ = session.run(target_op)
    duration = time.time() - start_time
    if i >= num_steps_burn_in:
      if not i % 10:
        print ('%s: step %d, duration = %.3f' %
               (datetime.now(), i - num_steps_burn_in, duration))
      total_duration += duration
      total_duration_squared += duration * duration
  mn = total_duration / FLAGS.num_batches
  vr = total_duration_squared / FLAGS.num_batches - mn * mn
  sd = math.sqrt(vr)
  print ('%s: %s across %d steps, %.3f +/- %.3f sec / batch' %
         (datetime.now(), info_string, FLAGS.num_batches, mn, sd))
  return TimingEntry(info_string, datetime.now(), FLAGS.num_batches, mn, sd)  

def store_data_in_csv(timing_entries):
  with open(FLAGS.csv_file, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for timing_entry in timing_entries:
      writer.writerow(
          [timing_entry.info_string, timing_entry.timestamp,
           timing_entry.num_batches, timing_entry.mean, timing_entry.sd])

def run_benchmark():
  global parameters
  timing_entries = []
  with tf.Graph().as_default():
    # Generate some dummy images.
    image_size = 224
    # Note that our padding definition is slightly different the cuda-convnet.
    # In order to force the model to start with the same activations sizes,
    # we add 3 to the image_size and employ VALID padding above.
    if FLAGS.data_format == 'NCHW':
      image_shape = [FLAGS.batch_size, 3, image_size + 3, image_size + 3]
    else:
      image_shape = [FLAGS.batch_size, image_size + 3, image_size + 3, 3]
    images = tf.Variable(tf.random_normal(image_shape,
                                          dtype=tf.float16,
                                          stddev=1e-1))

    labels = tf.Variable(tf.ones([FLAGS.batch_size],
                                 dtype=tf.int32))

    # Build a Graph that computes the logits predictions from the
    # inference model.
    last_layer = inference(images)

    # Build an initialization operation.
    init = tf.global_variables_initializer()

    # Start running operations on the Graph.
    session_conf = tf.ConfigProto(intra_op_parallelism_threads=16,inter_op_parallelism_threads=16)
    sess = tf.Session(config=session_conf)
    sess.run(init)

    run_forward = True
    run_forward_backward = True
    if FLAGS.forward_only and FLAGS.forward_backward_only:
      raise ValueError("Cannot specify --forward_only and "
                       "--forward_backward_only at the same time.")
    if FLAGS.forward_only:
      run_forward_backward = False
    elif FLAGS.forward_backward_only:
      run_forward = False

    if run_forward:
      # Run the forward benchmark.
      timing_entries.append(time_tensorflow_run(sess, last_layer, "Forward"))

    if run_forward_backward:
      # Add a simple objective so we can calculate the backward pass.
      objective = loss(last_layer, labels)
      # Compute the gradient with respect to all the parameters.
      grad = tf.gradients(objective, parameters)
      # Run the backward benchmark.
      timing_entries.append(time_tensorflow_run(sess, grad, "Forward-backward"))

  if FLAGS.csv_file:
    store_data_in_csv(timing_entries)


def main(_):
  run_benchmark()


if __name__ == '__main__':
  tf.app.run()
