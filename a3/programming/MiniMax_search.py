# This is the script that implements MiniMax search.
#
# You are responsible for implementing:
#
#	MiniMax_search()
#	MiniMax_utility()
#
# Read the comments at the head of each function carefully and be
# sure to return exactly what is requested. Also, be sure to
# update the Maze[][] array as required. Read below for details.
#
# All work you do here is individual.
#
# Starter code by: F.J.E. Jan. 15, 2013. Time to Dine!
# Updated Jan. 2014.
#
# Global data you will have access to (note each of these *MUST*
# be prefixed with 'MiniMax_global_data.', e.g. 'MiniMax_global_data.Ncats'
#
# 'Ncats'    -> An integer holding the numebr of cats in the game
# 'Ncheese'  -> An integer holding the number of cheese chunks
# 'msx','msy'-> Maximum size of the maze along x and y respectively,
#               this is fixed at 32 for both directions. DO NOT
#               CHANGE. You only need this for indexing into A[][]
# 'Maze[][]' -> An array of size msx x msy (32 x 32) you will use
#               to record the order in which each location in the
#               maze is 'discovered' during search. i.e., if
#               Maze[i][j]=k then location [i][j] was the kth
#               location explored by your search function
# 'A[][]'    -> An adjacency list encoding the maze connectivity.
#               The size of A[][] is (MiniMax_global_data.msx*msy) x 4, that is, it
#               contains one row for each location in the maze,
#               and for each row, it specifies 4 possible edges
#               to the top, right, bottom, and left neighbours
#               respectively.
#               Example: Say your mouse is at location [2,3], and
#                        you want to check where it can move to.
#                        The data for this location is stored at
#                        A[2+(3*MiniMax_global_data.msx)][0] : Link to grid location [2,2]
#                        A[2+(3*MiniMax_global_data.msx)][1] : Link to grid location [3,3]
#                        A[2+(3*MiniMax_global_data.msx)][2] : Link to grid location [2,4]
#                        A[2+(3*MiniMax_global_data.msx)][3] : Link to grid location [1,3]
#                        If the link is 1, the locations are connected,
#                        if the link is 0 there is a wall in between.
# 'GameState[]' -> This is a list containing the concatenated Mouse and Cat
#		   coordinates.
#
#		   In this list, information is stored as follows:
#			GameState[0] 			 -> Mouse coordinates
#			GameState[1] to GameState[Ncats] -> Coordinates of cats
#                       GameState[Ncats+1] to end 	 -> Coordinates of cheese
#
#		   NOTE: the length of the GameState can change as cheese gets
#                  eaten, but there is always the same number of cats.
#
# You *CAN NOT MODIFY* anything other than 'Maze' in the global data
# described above. Doing so will cause your program to give results that
# disagree with our automatic testing and you'll get zero.

from math import *
from random import choice

# Import global data
import MiniMax_global_data

debug=0

# Function definitions
def checkForCats(GameState):
  # A little helper function to tell you if the Mouse got eaten.
  # Returns 1 if toast, 0 otherwise.
  for i in range(MiniMax_global_data.Ncats):
   if (GameState[i+1]==GameState[0]):
    return 1

  return 0

def checkForCheese(GameState):
  # A little helper function to tell you if the Mouse got the cheese.
  # Returns 1 if lunch, 0 otherwise.
  for i in range(MiniMax_global_data.Ncheese):
   if (GameState[i+1+MiniMax_global_data.Ncats]==GameState[0]):
    return 1

  return 0

def MiniMax_utility(GameState, agent_id, depth,alpha,beta):
  ############################################################
  # Use this function to compute the utility at location [x,y]
  # given the location of all agents and cheese pieces.
  #
  # Inputs:
  #
  # GameState, agent_id, depth - see the
  #            MiniMax_search() function.
  #
  # alpha,beta - These are *NOT* used by the utility function,
  #              but the utility function will need to pass
  #              them on to MiniMax_search().
  #
  #              Note that alpha and beta are not used by
  #              MiniMax_search() unless alpha/beta pruning
  #              is specified (search type = 2)
  #
  #
  # Note:      This utility function
  #            must return a numerical value when
  #            depth>=MiniMax_global_data.search_END,
  #            or when the Mouse has hit either a
  #            cat, a cheese, or a dead-end.
  #
  # Returns: A utility value for moving to (x,y)
  #          A partial sequence of *GAME STATES*. If this is
  #          a terminal node, then simply return the input
  #          game state with its utility value. Otherwise,
  #          return the partial game state list and utility
  #          score returned by a call to MiniMax_search()
  ###########################################################

  ###########################################################
  ##
  ## DO NOT CHANGE any code outside the indicated parts of
  ##  this file!
  ##
  ## But note you must understand what the code provided here
  ##  is doing in order to answer questions in the report
  ##
  ###########################################################
  global debug    # Set this to 1 above to print out debug data

  if (agent_id>=1+MiniMax_global_data.Ncats):
  	print "MiniMax_utility(): Invalid agent_id: ",agent_id," using ",agent_id % (MiniMax_global_data.Ncats+1)
        agent_id = agent_id % (MiniMax_global_data.Ncats+1)
  if (len(GameState)!=MiniMax_global_data.Ncats+MiniMax_global_data.Ncheese+1):
        print "MiniMax_utility(): GameState() is broken!? lengh= ",len(GameState),", shoule be ",MiniMax_global_data.Ncats+MiniMax_global_data.Ncheese+1, "\n"
        print "Wrong length, check your search code.\n"
        return [[],0]

  utility=0
  x,y=GameState[0]	# Utilities are computed w.r.t. position of the mouse

  # If the node is *NOT* a terminal node, call MiniMax once again to keep searching
  if not (depth>MiniMax_global_data.search_END or checkForCats(GameState) or checkForCheese(GameState)):
	[pl,utility]=MiniMax_search(GameState,agent_id+1,depth+1,alpha,beta)
	# MiniMax_search() will return a state [-1,-1] and utility=0 if the node below is
        # a dead-end. In which case we still have to evaluate the utility function
 	if (pl!=[-1,-1] and utility !=0):
		return [pl,utility]

  # This *IS* a terminal node (one of the conditions above is true, or the node is a dead-end with
  # no successors. Either way, evaluate the utility function here and return this node
  pl=[]
  pl.append(GameState)	# The returned partial list of game states will only contain
			# the current state (there's nothing below in the search tree!)
			# DO NOT modify pl[] in the code below

  ###############################################################
  ## TO DO: Complete this function. It computes the utility
  ##        value for the current state (including the locations of
  ##        mouse, cats, and cheese). In general, if this is
  ##        a 'good' state for the mouse the utility should be
  ##        positive, if the state is 'bad' utility should be
  ##        negative.
  ##
  ##        Things you may want to consider:
  ##
  ##        - Position of cats relative to mouse
  ##        - Position of cheese relative to mouse
  ##        - Relative advantage of eating a cheese vs.
  ##          getting eaten.
  ##
  ##          ***************************************************
  ##          ** Document carefully and extensively your utility
  ##          ** function in the REPORT.txt file, explain how
  ##          ** you came up with it, and why it is a good
  ##          ** utility function from the point of view of the
  ##          ** mouse.
  ##          ** We want to see a carefully thought-out utility
  ##          ** computation here
  ##          ** NOTE: The utility is computed from the point of
  ##          **       view of the mouse, so it should use the
  ##          **       mouse location in some way.
  ##          ***************************************************
  ##
  ###############################################################

	# Add all your code in this space
  mouse = (x,y)
  cats = get_cats(GameState)
  cheeses = get_cheese(GameState)

  # some constants
  SCALE = 10
  MAX_DIST = manhattan( (0, 0), ( MiniMax_global_data.msx, MiniMax_global_data.msy ) )
  NEAR_RADIUS = 8
  # become more afraid if there are more cats than mice
  FEAR_FACTOR = 30

  # feature 1:
  # distance to cheese
  dist_to_cheeses = [ manhattan(mouse, cheese) for cheese in cheeses ]

  # feature 2:
  # distance to cats
  dist_to_cats = [ manhattan(mouse, cat) for cat in cats ]

  # feature 3
  # number of cats near to the mouse position
  num_cats_nearby = len( filter( lambda x : x < NEAR_RADIUS, dist_to_cats ) )

  # scale higher as you get closer to the cheese
  # because max - (min) > max - (second_min)
  # however, nearby cats are really scary
  utility = SCALE * (MAX_DIST - min(dist_to_cheeses) - FEAR_FACTOR * num_cats_nearby)

  # utility is really high if the cheese is there
  if(checkForCheese(GameState)):
    utility = 3000
  # utility is really low if the cat is there
  elif(checkForCats(GameState)):
    utility = -3000

  return [pl,utility]	# Of course, by now your utility should be non-zero

def MiniMax_search(GameState, agent_id, depth, alpha, beta):
  ###############################################################
  ##
  ## MiniMax search - It takes a GameState (could be a hpothetical
  ##                  state somewhere down the search tree). It
  ##                  evaluates each potential move by the agent
  ##                  specified by agent_id, and returns either
  ##                  the MIN or MAX of possible actions depending
  ##                  on the agent.
  ## Inputs:
  ##
  ## GameState - Lists the position of the mouse, cats, and cheese
  ##             in that order.
  ##             This function MUST NOT access the global game state
  ##             in MiniMax_global_data.GameState[]
  ## agent_id  - Identifies the agent whose turn it is to move.
  ##             If it is the mouse's turn, then agent_id=0 and this
  ##             is a MAX node. Otherwise, it is a cat's turn and
  ##             this is a MIN node.
  ## depth     - Current search depth. MiniMax_global_data.search_END
  ##             specifies the maximum allowed search depth. This
  ##             is set when the user calls doSearch(). The user provides
  ##             the maximum number of turns that agents can search,
  ##             and the maximum search depth is set to
  ##             max_levels*(1+Ncats)
  ## alpha/beta - Current bounds on utility passed on by the parent of
  ##              this node. Used to do alpha/beta pruning when
  ##              search type = 2 (otherwise ignore them!)
  ##
  ## Returns:
  ##
  ## utility     - A utility value for the selected at this node
  ##
  ## pl          - A partial list of *GAME STATES* ending at at the
  ##               winning terminal node.
  ##               This is key. MiniMax searches in DFS order, but
  ##               must explore all possible paths of the specified
  ##               length and then decide which one to take.
  ##               In order to keep track of the paths, we build this
  ##               list of game states back to front.
  ##               Completely searched paths are returned back up
  ##               to the parent who then appends their own game state
  ##               to pass on to the grandparent, and so on.
  ##
  ##               There is a loop inside this function that computes
  ##               the minimax utility of all successors of this node,
  ##               each call will result in some utility value and
  ##               a partial list of game states. This function will
  ##               select the winning utility, take the associated
  ##               partial list of game states, append this node's
  ##               state (at the head of the list!) and return.
  ##
  ##               Notice that if the successor list is empty, this
  ##               function returns pl=[-1,-1], and utility=0
  ##               (when does this happen?)
  ##
  ###############################################################
  global debug

  agent_id=agent_id % (MiniMax_global_data.Ncats+1)
  MiniMax_global_data.t_cnt+=1

  if debug:
	  print "MiniMax search called for agent ",agent_id, "\n", "Mouse: ",GameState[0],", Cat:",GameState[1]

  # Get current coordinates of this agent and build list of successors
  # Successors are only added if the game state they create has not
  # already been expanded (even if it is still under evaluation)
  x,y=GameState[agent_id]
  successors=[]
  utilities=[]

  if (MiniMax_global_data.A[x+(y*MiniMax_global_data.msx)][3]==1):
   GameState_t=list(GameState)
   GameState_t[agent_id]=[x-1,y]
   successors.append([x-1,y])
  if (MiniMax_global_data.A[x+(y*MiniMax_global_data.msx)][1]==1):
   GameState_t=list(GameState)
   GameState_t[agent_id]=[x+1,y]
   successors.append([x+1,y])
  if (MiniMax_global_data.A[x+(y*MiniMax_global_data.msx)][0]==1):
   GameState_t=list(GameState)
   GameState_t[agent_id]=[x,y-1]
   successors.append([x,y-1])
  if (MiniMax_global_data.A[x+(y*MiniMax_global_data.msx)][2]==1):
   GameState_t=list(GameState)
   GameState_t[agent_id]=[x,y+1]
   successors.append([x,y+1])

  if (len(successors)==0):
  	# All configurations for this agent have been explored. Stay put
	return [[-1,-1],0]

  if debug:
  	print "Sucessor nodes at depth: ",depth," :",successors

  #pl=[]			## COMMENT OUT ONCE YOU START TO IMPLEMENT
  #pl.append(GameState)  ## THE MINIMAX CODE
  #return [pl,0]         ## IN THE SPACE BELOW. THIS IS A DUMMY

  ############################################################################
  ##
  ## TO DO: Implement the MiniMax search in the space below. Steps that you
  ##        need to do:
  ##
  ##        Evaluate each successor of this node (already stored as coordinates
  ##        of cells the current agent could visit within the successors[]
  ##        list created above.
  ##
  ##        This means creating a temporary game state, where the agent has
  ##        in fact moved to the successor's specified location. Then
  ##        evaluating the utility at that location.
  ##
  ##        Store the utilities of all successors of this node. Store the
  ##        partial lists of states returned for these successors (so you can
  ##        choose one of these paths)
  ##
  ##        NOTE: if a successor returns a partial list [-1,-1] and a
  ##              utility=0, DO NOT inser it into the list of utilities
  ##              or the list with partial paths!
  ##
  ##        NOTE (2): Your lists of utilities and partial paths should NEVER
  ##                  be empty if you implement this function and the utility
  ##                  function properly. (Why is that?)
  ##
  ##        Select the winning successor (utility and partial state list)
  ##        depending on whether this is a MAX node (mouse's turn, agent_id=0)
  ##        or a MIN node (cat's turn, agent_id>0)
  ##
  ##        Once you have completed the standard MiniMax method (and only
  ##        when you have already verified it works properly!) add
  ##        alpha/beta pruning to optimize search.
  ##
  ##        Note that alpha/beta pruning *IS ONLY ACTIVE IF*
  ##
  ##          MiniMax_global_data.SearchType=2
  ##
  ##        Otherwise, use standard MiniMax search!
  ##
  ############################################################################
  utilities=[]		# Use this to record utilities for successors
  pls=[]		# Use this to record partial paths returned by successors
  opt_idx=0		# Use this to record the *INDEX* of the winning successor


	# Add all your code in this space
  for suc in successors:
    GameState_t = list(GameState)
    GameState_t[agent_id] = suc

    partial,utility = MiniMax_utility(GameState_t, agent_id, depth, alpha, beta)

    if partial != [-1,-1] and utility != 0:
      pls.append(partial)
      utilities.append(utility)

      # prune
      if MiniMax_global_data.SearchType == 2:
        # if the player is the mouse
        # update alpha
        if agent_id == 0:
          alpha = max(alpha, utility)

        # else update beta if the player is the adversary
        else:
          beta = min(beta, utility)

        # if alpha >= beta, then we prune
        # as said in class
        if alpha >= beta:
          break

  u_min = min(utilities)
  u_max = max(utilities)

  # agent_id > 0 means its a cat, so they are minimizing
  # agent_id == 0 means its a mouse, so they are maximizing
  min_max = u_min if agent_id else u_max
  opt_idx = choice([ i for i, u in enumerate(utilities) if u == min_max])

  ################################################################
  ##
  ## DO NOT CHANGE code below this point.
  ##
  ################################################################
  # Update the maze array with the utility for this location.
  if (agent_id>=0):
  	MiniMax_global_data.Maze[GameState[agent_id][0],GameState[agent_id][1]]=utilities[opt_idx];

  # Insert this node and the selected partial path into the path returned by this call, and return
  # it along with the utility value.
  pl=[]
  if (pls[opt_idx]!=[-1,-1]):
  	pl=list(pls[opt_idx])
  	pl.reverse()
  pl.append(GameState)
  pl.reverse()

  if (agent_id==0 and depth==0 and debug):
  	print "Agent: ",agent_id,", at ",GameState[agent_id], "depth=",depth, ", Mouse at:",GameState[0]
  	print "Successors: "
  	print successors
  	print "Utilities: "
  	print utilities
  	print "Chosen: ",opt_idx, "with utility ",utilities[opt_idx],", move:",successors[opt_idx]

  return [pl,utilities[opt_idx]]

def get_cats(GameState):
  return GameState[1:1+MiniMax_global_data.Ncats]

def get_cheese(GameState):
  return GameState[1+MiniMax_global_data.Ncats:]

def avg(l):
  return sum(l) / len(l)

def manhattan( (x,y), (x2,y2) ):
  return abs( x - x2 ) + abs( y - y2 )
