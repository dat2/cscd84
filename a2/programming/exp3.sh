#!/bin/zsh

mkdir -p exp3
./run_search.py -s 289 -n 1250 -k 9 -t 250 -d 0.999 > exp3/run_1.txt &
./run_search.py -s 289 -n 1250 -k 9 -t 100 -d 0.999 > exp3/run_2.txt &
./run_search.py -s 289 -n 1250 -k 9 -t 50 -d 0.999 > exp3/run_3.txt &
