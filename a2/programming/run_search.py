#!/usr/bin/python

import argparse
import sys

parser = argparse.ArgumentParser(prog='run_search.py', description='Run the CSCD84 tests')
parser.add_argument('-s', '--seed', type=int, required=True)
parser.add_argument('-n', type=int, required=True)
parser.add_argument('-k', type=int, required=True)
parser.add_argument('-t', '--initial-temperature', type=int, default=0)
parser.add_argument('-d', '--decay-factor', type=float, default=0)
parser.add_argument('-p', '--screen-shot', action='store_true')
parser.add_argument('-f', '--filename', default='')
args = parser.parse_args(sys.argv[1:])

print 'seed', args.seed
print 'N', args.n
print 'K', args.k
print 'Temperature', args.initial_temperature
print 'Decay Factor', args.decay_factor

import Kmedians_core_GL
Kmedians_core_GL.initKmedians(args.seed, args.n, args.k, args.screen_shot, args.filename)
Kmedians_core_GL.Kmedians(args.initial_temperature, args.decay_factor)
