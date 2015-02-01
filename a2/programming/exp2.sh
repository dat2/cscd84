#!/bin/zsh

mkdir -p exp2
./run_search.py -s 123 -n 1250 -k 9 > exp2/run_1.txt &
./run_search.py -s 723 -n 1250 -k 9 > exp2/run_2.txt &
./run_search.py -s 7456 -n 1250 -k 9 > exp2/run_3.txt &
./run_search.py -s 6725 -n 1250 -k 9 > exp2/run_4.txt &
./run_search.py -s 9158 -n 1250 -k 9 > exp2/run_5.txt &
