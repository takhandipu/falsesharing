sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user ./serial
sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > serial.txt
mv perf.data serial.perf.data
sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user ./false
sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > false.txt
mv perf.data false.perf.data
sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user ./no_false
sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > no_false.txt
mv perf.data no_false.perf.data
