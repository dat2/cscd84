# CSC D84 - Winter 2014 - Assignment 4 - Q Learning
#
# This file is where you will implement the QLearning updates
# and the action selection process for the Mouse.
#
# Functions you have to write
#       Qlearn()
#       reward()
#       decideAction()
#       and their counterparts for feature based Q Learning
#       (look for the 'TO DO' sections below)
#
# Read the comments at the head of each function carefully and be
# sure to implement exactly what is requested.
#
# All work you do here is individual.
#
# Starter code: F.J.E. Jan. 30, 2013, updated Feb. 2014
#
# Global data you will have access to (note each of these *MUST*
# be prefixed with 'QLearn_global_data.', e.g. 'QLearn_global_data.Ncats'
#
# 'Mouse'    -> A single entry list with mouse coordinates [x,y]
# 'Cats'     -> An single entry list with cat coordinates [x,y]
# 'Cheese'   -> An single entry list with cheese locations [x,y]
# 'msx','msy'-> Maximum size of the maze along x and y respectively,
#               this is set by QLearn_core_GL. DO NOT
#               CHANGE. You only need this for indexing into A[][]
# 'A[][]'    -> An adjacency list encoding the maze connectivity.
#               The size of A[][] is (msx*msy) x 4, that is, it
#               contains one row for each location in the maze,
#               and for each row, it specifies 4 possible edges
#               to the top, right, bottom, and left neighbours
#               respectively.
#               Example: Say your mouse is at location [2,3], and
#                        you want to check where it can move to.
#                        The data for this location is stored at
#                        A[2+(3*QLearn_global_data.msx)][0] : Link to grid location [2,2]
#                        A[2+(3*QLearn_global_data.msx)][1] : Link to grid location [3,3]
#                        A[2+(3*QLearn_global_data.msx)][2] : Link to grid location [2,4]
#                        A[2+(3*QLearn_global_data.msx)][3] : Link to grid location [1,3]
#                        If the link is 1, the locations are connected,
#                        if the link is 0 there is a wall in between.
#
# 'Qtable[][]'  An array of size [(msx*msy)^3][4] with one row per state, and
#               4 columns corresponding to the 4 possible mouse moves.
# 'Qweights[]'  A list where you will store feature weights for feature-based Q Learning
# 'alpha'       The Q-learning learning rate
# 'lamb'        The Q-learning discount constant for future rewards
# mapCr, mapCg, mapCb  -  Arrays of size [msx]x[msy] where you can store any data you want
#                         displayed on the maze squares as a colour (r,g,b)!. Data is
#                         autoscaled, just make sure you understand what you are doing.
#                         * This only has an effect for feature based Q Learning
#
# YOU ARE NOT ALLOWED TO MODIFY ANY GLOBAL DATA EXCEPT FOR 'Qtable', 'Qweights',
#  'alpha' (though I would leave it alone), and the colour arrays mapCx.
#
# This is the only place where you need to update anything at all.
#

from math import *
from numpy import *

# Import global data
import QLearn_global_data

# Hack to keep around some static data

class MyStatic(object):
    # You can add to this object any data you need to keep around for feature based Q Learning.
    # You can access and modify this data by, for example, doing
    # print MyStatic.init
    #
    # or
    #
    # MyStatic.init=10
    #
    # Do not add data just because you can! you will have to justify what you are using here
    init=-1

# Function definitions
def QLearn(s,a,r,s_new):
    ####################################################################
    # This function implements the Q-learning update rule. It updates an
    # entry in the Qtable given the experience tuple <s,a,r,s_new>
    # as discussed in lecture.
    #
    # Return values: NONE
    ####################################################################

    ####################################################################
    ## TO DO:
    ##       Implement this function to carry out the Qtable updates
    ##       This is a 1-line function! (it's a long line)
    ####################################################################

    # split into a few lines for readability
    old = QLearn_global_data.Qtable[s][a]
    alpha = QLearn_global_data.alpha
    lamb = QLearn_global_data.lamb

    QLearn_global_data.Qtable[s][a] = old + alpha * (r + lamb * max(QLearn_global_data.Qtable[s_new]) - old)

    return

def reward():
    ####################################################################
    # This function computes and returns a reward value for the
    # CURRENT GAME CONFIGURATION (i.e. for the current Mouse, Cat,
    # and Cheese location). It is called by the code in QLearn_core_GL
    # during training to determine the reward associated with a given
    # state.
    #
    # The function can be as simple or as complicated as you like,
    # but it should give positive rewards for configurations that
    # are favorable to the mouse, and negative rewards for configurations
    # that favour the cat.
    #
    # Be careful! the reward function will have a STRONG impact on the
    # ability of your mouse to learn!
    ####################################################################

    ####################################################################
    ## TO DO:
    ##      Implement the reward function. It must return a real-valued
    ##      scalar reward appropriate for the current game configuration.
    ##
    ##      Document this function carefully in the REPORT.TXT
    ####################################################################

    return 0        # Replace with your computed reward

def decideAction(s):
    ####################################################################
    # This function is called by QLearn_core_GL once the training is
    # complete. It is used to playt the actual game against the
    # cat. The function should choose for the given input state 's'
    # the optimal action that is *ALLOWABLE*.
    #
    # This means, the optimal action that does not involve crossing a
    # wall. You must somehow use the Qtable and the A[][] adjacency
    # list to determine where the mouse should go.
    ####################################################################

    ####################################################################
    ## TO DO:
    ##      Implement this function to enable the mouse to choose an
    ##      optimal action for any given state 's'
    ##
    ##      The function MUST RETURN the *INDEX* of the optimal move
    ##      as follows:
    ##                      idx=0 -> Mouse moves up
    ##                      idx=1 -> Mouse moves right
    ##                      idx=2 -> Mouse moves down
    ##                      idx=3 -> Mouse moves left
    ####################################################################

    return 0        # Replace this with your return value!

############################################################################
#
# Here begin the functions for feature-based Q Learning. Do not work on
# these until you have completed standard Q Learning above!
#
############################################################################

def evaluateFeatures(mousep, catp, cheesep):
    ####################################################################
    # This function is called by the QLearning core to evaluate features
    # for a given game configuration.
    #
    # The function *MUST* return a list with a fixed number of features
    # which will be used to learn the weights of the overall reward
    # function as discussed in lecture. During play (once training is
    # complete) these features will determine how the mouse plays.
    #
    # This function will receive a list with the mouse position,
    #   a list with cat position(s),
    #   a list with cheese position(s)
    #
    # Global variables Ncheese and Ncats tell you how many of each.
    #
    # You are free to add as many features as you want. But:
    #
    # - You *must* document here with comments, and also in your report,
    #   what each feature does and how it is computed
    #
    # - Consider runtime. If a feature takes long to compute but
    #   doesn't help the mouse get smarter, don't use it!
    #
    # - We will evaluate mouse smartness competitively (again!) so be
    #   sure to spend some time coming up with clever features!
    #
    # - You're free to use search and path finding to help with your
    #   feature selection. But everything you use must eventually
    #   be turned into a single value within your features list.
    #
    # - For this function, you can the maze adjacency matrix A. But you
    #   are not allowed to change it. You are also not allowed to
    #   change the positions of the agents.
    #
    # - The weights to be trained are stored in the global variable
    #   QLearn_global_data.Qweights; which is a list of the same
    #   length as your feature list.
    #
    # - Your features should be in the range [-1,1] to avoid issues
    #   with weights becoming too large. Also, make sure your reward
    #   function returns small numbers. If your weights are growing
    #   like mad, try reducing the reward range, feature range, or
    #   setting a smaller learning factor alpha.
    #
    ###################################################################

    ###################################################################
    #
    #  TO DO:
    #         Implement your feature computations and return the
    #         list of the current features given the positions of
    #         the agents, and the maze
    ###################################################################

    feature_list=[]         # Add as many features as you need!

    return feature_list

def evaluateQsa(feature_list):
    ####################################################################
    #
    # This function returns the current value for Q(s,a). The input,
    # the feature_list, contains the features evaluated after the
    # mouse has taken a specific action 'a' from state 's'. Note that
    # this function doesn't care what 'a' or 's' are, it just returns
    # the result of performing the linear combination of features
    # given the current weight.
    #
    # Either the QLearning training code, or the code that decides on
    # mouse actions must figure out how to compute the appropriate
    # feature_list.
    ####################################################################

    ####################################################################
    #
    # TO DO: Complete this function and return the value for Q(s,a)
    #
    ####################################################################

    return 0        # Replace with your own code

def maxQsa_prime(mousep,catp,cheesep):
    ####################################################################
    #
    # This function computes and returns the index and value of the
    # best possible action starting at the configuration given by the
    # input mousep, catp, and cheesep.
    #
    # In other words, it must try every possible action (that is allowed
    # given the maze!) and return the action with highest value given
    # the current weights for the QLearning expected reward function.
    #
    # The return value should be a 2-entry list with [idx,val]. idx
    # must be in [0,3] where each value has the same meaning as in
    # the 'decideAction' function above. 'val' is a real-valued
    # expected reward given that the mouse takes action 'idx' from
    # the current config.
    ####################################################################

    ####################################################################
    #
    # TO DO: Complete this function.
    #
    ####################################################################

    return [0,0]      # Replace with your code

def QLearn_features(a,r):
    ####################################################################
    #
    # This function carries out the QLearning update for the feature-
    # based method. It evaluates the utility Q(s,a) given the specified
    # action a (in [0,3]) and determines the weight updates for each
    # of the weights associated to your features.
    #
    # The immediate reward obtained by the mouse is provided in 'r'
    #
    # Returns NONE
    ####################################################################

    # Make local copies of the current config. Do not mess with the globals!
    mousep=list(QLearn_global_data.Mouse)
    catp=list(QLearn_global_data.Cats)
    cheesep=list(QLearn_global_data.Cheese)

    # First time through this code we need to initialize the weights
    # Requires a working 'evaluateFeatures' function!
    if (len(QLearn_global_data.Qweights)==0):
            dummy_features=evaluateFeatures(mousep,catp,cheesep)
            for i in range(len(dummy_features)):
                    QLearn_global_data.Qweights.append(0.0);

    ####################################################################
    #
    # TO DO: Carry out the QLearning weight update!
    #  remember:  By the time you get here, the mouse has already moved
    #             (i.e. you are already at state s'). However, if you
    #             compute your features right now, and evaluate Q, you
    #             will obtain Q(s,a), which is the expected utility of
    #             carrying out action a from s. Don't get confused!
    #
    ####################################################################

    return

def decideAction_features(mousep, catp, cheesep):
    ####################################################################
    #
    # This function is used to decide which action to take from the
    # specified configuration given the current weights of the features
    # in the QLearning method.
    #
    # Returns the index 'idx' of the optimal action. idx is in [0,3] as
    # described in 'decideAction' above
    ####################################################################

    ####################################################################
    #
    # TO DO: Complete this function.
    #
    ####################################################################

    return 0        # Replace with your own code

