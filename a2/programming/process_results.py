#!/usr/bin/python

import argparse
import sys
import glob

parser = argparse.ArgumentParser(prog='process_results.py', description='Get the results')
parser.add_argument('-d', '--directory', required=True)
parser.add_argument('-s', '--seed', action='store_true')
parser.add_argument('-r', '--range', action='store_true')
parser.add_argument('-a', '--all-costs', action='store_true')
parser.add_argument('-t', '--temperature', action='store_true')
parser.add_argument('-df', '--decay-factor', action='store_true')
args = parser.parse_args(sys.argv[1:])

def average(l):
    return sum(l) / len(l)

runs = glob.glob(args.directory + '/run_*.txt')
initial_costs = []
final_costs = []
initial_temperatures = []
decay_factors = []
seeds = []
for run in runs:
    with open(run, 'r') as f:
        lines = list(f)

        seeds += [int((lines[0].strip())[len('seed '):])]
        initial_temperatures += [float((lines[3].strip())[len('Temperature '):])]
        decay_factors += [float((lines[4].strip())[len('Decay Factor '):])]
        initial_costs += [float(lines[11].strip())]
        final_costs += [float((lines[-1].strip())[len('final cost: '):])]

if args.seed:
    print 'Seeds ', seeds

print 'Average initial cost:', average(initial_costs)
print 'Average final cost:', average(final_costs)

if args.temperature:
    print 'Temperatures with their final costs:', zip(initial_temperatures, final_costs)

if args.decay_factor:
    print 'Decay factor with their final costs:', zip(decay_factors, final_costs)

if args.range:
    print 'Range of final costs:', min(final_costs), max(final_costs)

if args.all_costs:
    print 'All initial costs:', initial_costs
    print 'All final costs:', final_costs
