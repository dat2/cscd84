#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(prog='runner.py', description='CSCD84 runner')
parser.add_argument('-u', '--units', type=int, required=True)
parser.add_argument('-f', '--function', type=int, required=True)
parser.add_argument('-r', '--rate', type=float, required=True)
parser.add_argument('-s', '--seed', type=int, required=True)
parser.add_argument('-t', '--threshold', type=float, required=True)
args = parser.parse_args()

def functionLabel(f):
  if f == 0:
    return 'logistic'
  else:
    return 'hyperbolic tangent'

print 'seed:', args.seed
print 'hidden layer units:', args.units
print 'activation function type:', functionLabel(args.function)
print 'learning rate:', args.rate
print 'learning threshold', args.threshold

from NeuralNets_core_GL import *
NeuralNets_init(args.units,args.function,args.rate,args.seed)
NeuralNets_train(args.threshold)
