#!/bin/bash

m=20
rate=4

# i: 做 i 組 data
for i in $(seq 1 1 10)
do
  for n in $(seq 20 10 80)
  do
    total=`expr $n + $m`
    dir="sc6/data_$i"
    mkdir -p ./MAC_address/$dir
    python3 make_MAC.py -n $total > ./MAC_address/$dir/MAC_address_$total
    python3 make_topofile.py -n $total
    cd ../../utils
    python3 set_param.py -n $n -m $m -r $rate -d ./testing/$dir
    cd ../exercises/syn_flood_cuckoo/
    make
    make clean
  done
done

# for i in $(seq 1 1 10)
# do
#   dir="sc5/data_$i"
#   mkdir -p ./analysis/$dir
#   mkdir -p ./plot_dataset/bloom/$dir
#   mkdir -p ./plot_dataset/cuckoo2/$dir
#   python3 method.py -n $n -r $rate -e 900 -s 300 -sc 5 -d $dir
# done

# for test_3 (檢測沒有 decreasing 的情況)
# for i in $(seq 1 1 10)
# do
#   dir="sc5/data_$i"
#   mkdir -p ./analysis/$dir
#   mkdir -p ./plot_dataset/bloom/$dir
#   mkdir -p ./plot_dataset/cuckoo2/$dir
#   python3 method.py -n $n -r $rate -e 900 -s 300 -sc 51 -d $dir
# done

# cd plot_dataset/
# for i in $(seq 1 1 10)
# do
#   dir="sc5/data_$i"
#   mkdir -p ./pic/$dir
#   python3 plot.py -n $n -r $rate -sc 5 -d $dir
# done

# for i in $(seq 1 1 10)
# do
#   dir="sc5/data_$i"
#   mkdir -p ./pic/$dir
#   python3 plot.py -n $n -r $rate -sc 51 -d $dir
# done

