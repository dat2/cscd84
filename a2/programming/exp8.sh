#!/bin/zsh

mkdir -p exp8
python -u run_search.py -s -289 -n 1250 -k 7 -p -f 'LS_restaraunts.jpg' | tee exp8/run_1.txt
