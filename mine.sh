sudo ../../linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user python benchmark_alexnet.py
sudo ../../linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > alex.txt
mv perf.data alex.perf.data
sudo ../../linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user python benchmark_googlenet.py
sudo ../../linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > google.txt
mv perf.data google.perf.data
sudo ../../linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user python benchmark_vgg.py
sudo ../../linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > vgg.txt
mv perf.data vgg.perf.data
