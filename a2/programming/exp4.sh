#!/bin/zsh

mkdir -p exp4
./run_search.py -s 289 -n 1250 -k 9 -t 250 -d 0.999 > exp4/run_1.txt &
./run_search.py -s 289 -n 1250 -k 9 -t 250 -d 0.99 > exp4/run_2.txt &
./run_search.py -s 289 -n 1250 -k 9 -t 250 -d 0.9 > exp4/run_3.txt &
