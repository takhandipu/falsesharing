class Model(object):
  """Base model configuration for CNN benchmarks."""

  def __init__(self,
               model,
               image_size,
               batch_size,
               learning_rate,
               layer_counts=None,
               fp16_loss_scale=128):
    self.model = model
    self.image_size = image_size
    self.batch_size = batch_size
    self.default_batch_size = batch_size
    self.learning_rate = learning_rate
    self.layer_counts = layer_counts
    # TODO(reedwm) Set custom loss scales for each model instead of using the
    # default of 128.
    self.fp16_loss_scale = fp16_loss_scale

  def get_model(self):
    return self.model

  def get_image_size(self):
    return self.image_size

  def get_batch_size(self):
    return self.batch_size

  def set_batch_size(self, batch_size):
    self.batch_size = batch_size

  def get_default_batch_size(self):
    return self.default_batch_size

  def get_layer_counts(self):
    return self.layer_counts

  def get_fp16_loss_scale(self):
    return self.fp16_loss_scale

  def get_learning_rate(self, global_step, batch_size):
    del global_step
    del batch_size
    return self.learning_rate

  def add_inference(self, unused_cnn):
    raise ValueError('Must be implemented in derived classes')
