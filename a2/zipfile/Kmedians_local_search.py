###########################################################
#
# CSC D84 - A2 - Local search for K-medians problem
#
# In this script you will implement two methods for
# solving the K-medians problem:
#
# 1) Simple local search
#
# 2) Local search with deterministic annealing
#
# Your code will be called by Kmedians_core_GL to
# solve particular instances of the problem, so you
# should not add any tester functions here.
#
# You have access to the following global data (all
# prefixed by 'Kmedians_global_data.' )
#
# all_points      - List of [x,y] point coordinates
# current_medians - List of [x,y] with current medians
# N               - Number of points
# K               - Number of medians
# Temperature     - Temperature for deterministic annealing
# Decay           - Decay factor for deterministic annealing
#
# Use the global 'current_cost' function to return the cost
# of a potential solution, e.g.
#
#   Kmedians_global_data.current_cost(guess)
#   will return the cost of 'guess' where guess is
#       a lst of tuples containing a potential solution
#
# Sorry, that's bad style, but I claim poetic license!
#
# Do not add any additional global data.
#
# Updated by: F.J.E. Jan. 2014
##########################################################

import Kmedians_global_data
import random
import math
import numpy as np

def try_new_medians():
    p_i = random.randint(0, Kmedians_global_data.N-1)
    m_i = random.randint(0, Kmedians_global_data.K-1)

    px,py = Kmedians_global_data.all_points[p_i]
    mx,my = Kmedians_global_data.current_medians[m_i]

    rand_point = np.array( (px, py) )
    rand_median = np.array( (mx, my) )

    if np.linalg.norm(rand_point - rand_median) > 250:
        return

    medians = list(Kmedians_global_data.current_medians)
    medians[m_i] = Kmedians_global_data.all_points[p_i]

    return medians

def local_search():
    # This function carries out a local search to improve
    # the current guess. You can only examine *ONE* possible
    # update to the current solution per call. That is, at
    # most one of the current medians should change from
    # call to call. Note that this procedure is greedy
    # and will only update the current solution if its
    # new guess yields a better cost

    #####################################################
    # NEIGHBOURHOOD DEFINITION:
    # At each step, one of the current guesses for your
    # median locations can be swaped for another
    # point as long as the distance between the current
    # guess and the point is less than 250 units
    # (this is Euclidean distance of course)
    # This means that you CAN NOT SWAP with just any
    # point! Make sure your updates consider this
    # simple neighbourhood structure.
    #
    # If the proposed swap is more than 250 units away,
    # do not perform the sawp! just return from this
    # function with the same guess you started with.
    ######################################################

    ####################################################
    ##
    ## TO DO: Complete this function to perform simple
    ##        local search for better solutions to the
    ##        K-medians problem.
    ##
    ##        Make sure your code updates the global
    ##        'current_medians' list!
    ####################################################

    medians = try_new_medians()
    if not medians:
        return

    med_cost = Kmedians_global_data.current_cost(medians)
    cur_cost = Kmedians_global_data.current_cost(Kmedians_global_data.current_medians)

    if med_cost < cur_cost:
        Kmedians_global_data.current_medians = medians
        print med_cost
    return

def deterministic_annealing():
    # This function carries out a local search using the
    # deterministic annealing method as discussed in lecture.
    # The 'temperature' is set by the initKmedians function.
    # Each call to this function will try a new solution
    # and accept it under the conditions specified by the
    # deterministic annealing method.

    # temperature as T=T*D, where D<1.0 is a decay factor that
    # controls how quickly the temperature decreases.
    # Both the temperature and decay factor are global
    # variables.

    # Each call to this function can examine only *ONE*
    # guess at the solution.

    ####################################################
    # THE SAME NEIGHBOURHOOD DEFINITION APPLIES AS FOR
    # LOCAL SEARCH ABOVE
    ####################################################

    ####################################################
    ##
    ## TO DO: Complete this function to perform
    ##        local search with deterministic annealing.
    ##
    ##        Make sure your code updates the global
    ##        'current_medians' list!
    ####################################################

    T = Kmedians_global_data.Temperature = Kmedians_global_data.Temperature * Kmedians_global_data.Decay

    medians = try_new_medians()
    if not medians:
        return

    med_cost = Kmedians_global_data.current_cost(medians)
    cur_cost = Kmedians_global_data.current_cost(Kmedians_global_data.current_medians)
    delta_t = abs(med_cost - cur_cost)

    probability = math.exp (-delta_t / T)

    r = random.random()

    if med_cost > cur_cost:
        if r < probability:
            Kmedians_global_data.current_medians = medians
    else:
        Kmedians_global_data.current_medians = medians

    print med_cost

    return