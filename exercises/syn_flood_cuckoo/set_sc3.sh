#!/bin/bash

n=20
rate=4

for m in $(seq 20 10 80)
do
  echo $m
  cd ../../utils
  python3 set_param.py -n $n -m $m -r $rate
  cd ../exercises/syn_flood_cuckoo/
  python3 make_topofile.py -n `expr $n + $m`
  make
  make clean
done

python3 method.py -n $n -r $rate -e 900 -s 300 -sc 3

cd plot_dataset/
python3 plot.py -sc 3
