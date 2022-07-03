#!/bin/bash

n=20
rate=u200000

# # i: 做 i 組 data
# for i in $(seq 1 1 10)
# do
#   for m in $(seq 20 10 80)
#   do
#     total=`expr $n + $m`
#     dir="sc2/data_$i"
#     mkdir -p ./MAC_address/$dir
#     python3 make_MAC.py -n $total > ./MAC_address/$dir/MAC_address_$total
#     python3 make_topofile.py -n $total
#     cd ../../utils
#     python3 set_param.py -n $n -m $m -r $rate -d ./testing/$dir
#     cd ../exercises/syn_flood_cuckoo/
#     make
#     make clean
#   done
# done

# i: 做 i 組 data
for i in $(seq 1 1 10)
do
  dir="sc2/data_$i"
  mkdir -p ./analysis/$dir
  mkdir -p ./plot_dataset/bloom/$dir
  mkdir -p ./plot_dataset/cuckoo2/$dir
  python3 method.py -n $n -r $rate -e 900 -s 300 -sc 2 -d $dir
done

# cd plot_dataset/
# for i in $(seq 1 1 10)
# do
#   dir="sc2/data_$i"
#   mkdir -p ./pic/$dir
#   python3 plot.py -n $n -r $rate -sc 2 -d $dir
# done
