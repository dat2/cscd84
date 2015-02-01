#!/bin/zsh

mkdir -p exp7
python -u run_search.py -s -1859 -n 1250 -k 7 -t 250 -d 0.999 -p -f '1-DA_restaraunts.jpg' | tee exp7/run_1.txt
python -u run_search.py -s -4278 -n 1250 -k 7 -t 250 -d 0.999 -p -f '2-DA_restaraunts.jpg' | tee exp7/run_2.txt
python -u run_search.py -s -5172 -n 1250 -k 7 -t 250 -d 0.999 -p -f '3-DA_restaraunts.jpg' | tee exp7/run_3.txt
