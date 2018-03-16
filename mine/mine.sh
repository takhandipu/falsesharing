# sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user ./serial
# sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > serial.txt
# mv perf.data serial.perf.data
# sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user ./false
# sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > false.txt
# mv perf.data false.perf.data
# sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c record -F 15000 -a --all-user ./no_false
# sudo ../../tmpGits/linux-4.15.10/tools/perf/perf c2c report -NN -c pid,iaddr --full-symbols --stdio > no_false.txt
# mv perf.data no_false.perf.data
# ../../pmu-tools/ocperf.py stat -r 100 -e mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_l3_miss_retired.remote_hitm ./serial 2>> stat.txt
../../pmu-tools/ocperf.py stat -r 100 -e mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_l3_miss_retired.remote_hitm ./false 2>> stat.txt
../../pmu-tools/ocperf.py stat -r 100 -e mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_l3_miss_retired.remote_hitm ./no_false 2>> stat.txt
