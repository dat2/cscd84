#!/usr/bin/python

from __future__ import division

import argparse
import sys
import glob

parser = argparse.ArgumentParser(prog='process_results.py', description='Get the results')
parser.add_argument('old', type=float)
parser.add_argument('new', type=float)
args = parser.parse_args(sys.argv[1:])

print "{0:.00f}%".format( ((args.new - args.old) / args.old) * 100 )
