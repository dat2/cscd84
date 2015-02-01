#!/bin/zsh

mkdir -p exp1
./run_search.py -s 289 -n 1240 -k 9 > exp1/run_1.txt &
./run_search.py -s 289 -n 1245 -k 9 > exp1/run_2.txt &
./run_search.py -s 289 -n 1250 -k 9 > exp1/run_3.txt &
./run_search.py -s 289 -n 1255 -k 9 > exp1/run_4.txt &
./run_search.py -s 289 -n 1260 -k 9 > exp1/run_5.txt &
