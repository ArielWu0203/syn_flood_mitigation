#!/bin/bash
n=20
m=20

for rate in '4' '1' 'u200000' 'u100000' 'u66667' 'u50000'
do
  cd ../../utils
  python3 set_param.py -n $n -m $m -r $rate
  cd ../exercises/syn_flood_cuckoo/
  python3 make_MAC.py
  python3 make_topofile.py -n `expr $n + $m`
  make
  make clean
done

for rate in '4' '1' 'u200000' 'u100000' 'u66667' 'u50000'
do
  python3 method.py -n $n -m $m -r $rate -e 900 -sc 1
done

cd bloom_plot/
python3 decide_threshold.py
