#!/bin/zsh

mkdir -p exp6
python -u run_search.py -s 289 -n 1000 -k 7 -p -f 'LS_solution.jpg' | tee exp6/run_1.txt
