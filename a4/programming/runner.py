#!/usr/bin/python
import argparse

def getMazeSize(arg):
  if arg == 0:
    return '4x4'
  elif arg == 1:
    return '8x8'
  elif arg == 2:
    return '16x16'
  elif arg == 3:
    return '32x32'

parser = argparse.ArgumentParser(prog='runner.py', description='CSCD84 runner')
parser.add_argument('-s', '--seed', type=int, required=True)
parser.add_argument('-m', '--maze-size', type=int, required=True)
parser.add_argument('-k', '--num-cats', type=int, required=True)
parser.add_argument('-c', '--num-cheese', type=int, required=True)

parser.add_argument('--train', action='store_true')
parser.add_argument('-n', '--num-trials', type=int)
parser.add_argument('-r', '--num-rounds', type=int)

parser.add_argument('--play-game', action='store_true')
args = parser.parse_args()

print 'seed:', args.seed
print 'maze size:', getMazeSize(args.maze_size)
print 'num cats:', args.num_cats
print 'num cheese:', args.num_cheese

from QLearn_core_GL import *
initGame(args.seed, args.maze_size, args.num_cats, args.num_cheese)
if args.train:
  doQLearn(args.num_trials,args.num_rounds)
if args.play_game:
  doGame()
