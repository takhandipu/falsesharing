gcc -Wall -D_LINUX_ -O3 -o no_false no_false.c -lm -lpthread -lrt
gcc -Wall -D_LINUX_ -O3 -o false false.c -lm -lpthread -lrt
../../pmu-tools/ocperf.py stat -r 100 -e mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_l3_miss_retired.remote_hitm ./false key_file_500MB.txt 2>> stat.txt
../../pmu-tools/ocperf.py stat -r 100 -e mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_l3_miss_retired.remote_hitm ./no_false key_file_500MB.txt 2>> stat.txt
