#!/bin/zsh

mkdir -p exp5
python -u run_search.py -s 6785 -n 1000 -k 7 -t 250 -d 0.999 -p -f '1-DA_solution.jpg' | tee exp5/run_1.txt
python -u run_search.py -s 4819 -n 1000 -k 7 -t 250 -d 0.999 -p -f '2-DA_solution.jpg' | tee exp5/run_2.txt
python -u run_search.py -s 8147 -n 1000 -k 7 -t 250 -d 0.999 -p -f '3-DA_solution.jpg' | tee exp5/run_3.txt
