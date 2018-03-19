../pmu-tools/ocperf.py stat -r 100 -e mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_l3_miss_retired.remote_hitm python benchmark_alexnet.py 2>> stat_16.txt
../pmu-tools/ocperf.py stat -r 100 -e mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_l3_miss_retired.remote_hitm python benchmark_googlenet.py 2>> stat_16.txt
../pmu-tools/ocperf.py stat -r 100 -e mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_l3_miss_retired.remote_hitm python benchmark_vgg.py 2>> stat_16.txt
