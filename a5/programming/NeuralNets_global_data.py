import math
import numpy
import pickle
N_out = 10
N_in = 65
N_hidden = 0
alpha = 0
sig_type = 0
Err_Thresh = 0
W_ih = []
W_ho = []
W_io = []
f = open('TrainTestData.pickle', 'r')
(trainDigits, trainLabels, TD, TL,) = pickle.load(f)
f.close()

