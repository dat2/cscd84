#!/usr/bin/python

import argparse
import sys

parser = argparse.ArgumentParser(prog='run_search.py', description='Run the CSCD84 tests')
parser.add_argument('-s', '--seed', type=int, required=True)
parser.add_argument('-n', '--num-cats', type=int, required=True)
parser.add_argument('-c', '--num-cheese', type=int, required=True)
parser.add_argument('-t', '--search-type', type=int, required=True)
parser.add_argument('-l', '--lookahead', type=int, required=True)
args = parser.parse_args(sys.argv[1:])

print 'seed', args.seed
print 'num cats:', args.num_cats
print 'num cheese:', args.num_cheese
print 'search type:', args.search_type
print 'turns to lookahead:', args.lookahead

import MiniMax_core_GL
MiniMax_core_GL.initGame(args.seed, args.num_cats, args.num_cheese)
MiniMax_core_GL.doSearch(args.search_type,args.lookahead)
