# This is the script that implements the different search algorithms
# that you will try with the mouse.
#
# The algorithms you are responsible for are:
#
# BFS
# DFS
# A* search
# A* search with cat heuristic
#
# Read the comments at the head of each function carefully and be
# sure to return exactly what is requested. Also, be sure to
# update the Maze[][] array. Read below for details.
#
# All work you do here is individual.
#
# Global data you will have access to (note each of these *MUST*
# be prefixed with 'AI_global_data.', e.g. 'AI_global_data.Ncats'
#
# ****** DATA WHICH YOU CAN ACCESS BUT YOU ARE NOT ALLOWED TO MODIFY:
# 'Ncats'    -> An integer holding the numebr of cats in the game
# 'Ncheese'  -> An integer holding the number of cheese chunks
# 'Mouse'    -> A single entry list with mouse coordinates [x,y]
# 'Cats'     -> An Ncats x 2 list with cat coordinates [x,y]
# 'Cheese'   -> An Ncheese x 2 list with cheese locations [x,y]
# 'msx','msy'-> Maximum size of the maze along x and y respectively,
#               this is fixed at 32 for both directions. DO NOT
#               CHANGE. You only need this for indexing into A[][]
# 'A[][]'    -> An adjacency list encoding the maze connectivity.
#               The size of A[][] is (AI_global_data.msx*msy) x 4, that is, it
#               contains one row for each location in the maze,
#               and for each row, it specifies 4 possible edges
#               to the top, right, bottom, and left neighbours
#               respectively.
#               Example: Say your mouse is at location [2,3], and
#                        you want to check where it can move to.
#                        The data for this location is stored at
#                        A[2+(3*AI_global_data.msx)][0] : Link to grid location [2,2]
#                        A[2+(3*AI_global_data.msx)][1] : Link to grid location [3,3]
#                        A[2+(3*AI_global_data.msx)][2] : Link to grid location [2,4]
#                        A[2+(3*AI_global_data.msx)][3] : Link to grid location [1,3]
#                        If the link is 1, the locations are connected,
#                        if the link is 0 there is a wall in between.
#
# ******* DATA WHICH YOU CAN ACCESS AND MODIFY
# 'Maze[][]' -> An array of size msx x msy (32 x 32) you will use
#               to record the order in which each location in the
#               maze is 'discovered' during search. i.e., if
#               Maze[i][j]=k then location [i][j] was the kth
#               location explored by your search function.
# 'P[][]'    -> An array of size msx x msy (32 x 32) you can use for
#               storing any node-related temporary data you may need
#               during search.
# 'MousePath' -> You will use this list to return a path from the
#                mouse to the cheese. It will be used by the search
#                core to update the mouse position at each turn.
#                Be sure to store information in the order requested,
#                and make sure each [x,y] location pair contains
#                only valid locations.
#
# 'junkpile'  -> An empty list. You can use this list to insert any data your
#                code may need to keep track of between calls. Do not add just because
#                you can! use only sparingly and only where needed. Your TA will look
#                for excessive/unnecessary usage of this global list.
#
# Let me stresst this point:
# You *CAN NOT MODIFY* anything other than 'MousePath', 'P', 'Maze', and 'junkpile' in the global
# data described above. Changing anything else will cause your program to give results that
# disagree with our automatic testing and you'll get zero.
#
# Starter code: F.J.E. Aug. 8, 2012, updated Jan. 2014
#

from math import *

# Import global data
import AI_global_data
import numpy as np

from operator import itemgetter
from math import log

# Function definitions

def checkForCats(x,y):
  # A little helper function to tell you if there is a cat at [x,y].
  # Returns 1 if there is a cat, 0 otherwise.
  for i in range(AI_global_data.Ncats):
    if (AI_global_data.Cats[i][0] == x and AI_global_data.Cats[i][1] == y):
      return 1

  return 0

def checkForCheese(x,y):
  # A little helper function to tell you if there is cheese at [x,y].
  # Returns 1 if there is cheese, 0 otherwise.
  for i in range(AI_global_data.Ncheese):
    if (AI_global_data.Cheese[i][0] == x and AI_global_data.Cheese[i][1] == y):
      return 1

  return 0

def calculateIndex(x, y):
  return x + AI_global_data.msx * y;

def getMouseCoords():
  return tuple(AI_global_data.Mouse[0])

def adjacentCoordinates(x,y):
  return [ (x, y-1), (x+1, y), (x, y+1), (x-1,y) ]

# returns [ (index in adj array, coords) ]
def nonBlockedWalls(x,y):
  return filter(
    lambda (idx, _): int(AI_global_data.A[calculateIndex(x,y)][idx]) == 1,
    # lazy way to do this
    enumerate( adjacentCoordinates(x,y) )
  )

# returns the opposite direction of the given direction, useful for reverse parent
# direction
def opposite(idx):
  if idx == 3:
    return 1
  elif idx == 2:
    return 0
  elif idx == 1:
    return 3
  else:
    return 2

def manhattan(x1,y1,x2,y2):
  return (abs(x1 - x2) + abs(y1 - y2))

def Astar_cost(x,y):
  # Use this function to compute the heuristic cost estimate for
  # location [x,y] given the locations of cheese. This function
  # *MUST NOT* use cat locations in computing the cost.

  ###############################################################
  ## TO DO: Implement the heuristic cost computation.
  ##        Your function must implement an admissible heuristic!
  ###############################################################

  return min(
    map ( lambda (cx, cy): manhattan(x,y,cx,cy), AI_global_data.Cheese )
  )

def Astar_cost_nokitty(x,y):
  # Use this function to compute the heuristic cost estimate for
  # location [x,y] given the locations of cheese. This function
  # *CAN* use cat locations in computing the cost.

  ###############################################################
  ## TO DO: Implement the heuristic cost computation.
  ##        Your function must implement an admissible heuristic!
  ###############################################################

  cheeses = map ( lambda (cx, cy): manhattan(x,y,cx,cy), AI_global_data.Cheese )
  cats =  map ( lambda (cx, cy): manhattan(x,y,cx,cy), AI_global_data.Cats )

  # prevent the ai from crashing if the red cheese disappears and it is the last
  # cheese
  try:
    cheese_cost = min(cheeses)
  except:
    cheese_cost = 0

  # prevent the ai from crashing if there are no cats
  try:
    closest_cat = min(cats)

    # get the number of cats that are within 6 manhattan distance of the node
    cluster_radius = 6
    number_of_cats_nearby = len(
      filter( lambda x: x <= cluster_radius, cats)
    )

    # lower values for fear factor cause the scaling variable to grow less,
    # causing the mouse to be more brave
    fear_factor = 7

    # closest cost increases if you have a single cat nearby
    # closest cost also increases if you have many cats nearby
    closest_cost = 2 ** ( number_of_cats_nearby + fear_factor - closest_cat )

    cat_cost = closest_cost
  except:
    cat_cost = 0

  # if the cheese is right beside you, then cat cost is nothing
  # this makes the mouse much more attracted to the cheese
  if any(map(lambda (x,y): checkForCheese(x,y) and not checkForCats(x,y), adjacentCoordinates(x,y))):
    cat_cost = 0

  return cheese_cost + cat_cost

def BFS():
  # Breadth-first search

  ###################################################################
  ## TO DO: Implement BFS here starting at the mouse's location
  ##        and ending at the cheese location. Be sure to update
  ##        the Maze[][] array to indicate in which order maze
  ##        locations were expanded while looking for a path to
  ##        the cheese.
  ##
  ## Notes:
  ##        - This is *NOT A RECURSIVE* function. Do not attempt
  ##          to turn it into a recursion - you will blow the
  ##          stack easily.
  ##        - If a path is found, return 1, and update
  ##          AI_global_data.MousePath to contain the path
  ##          from *END TO START*, that is, the first entry
  ##          in the list will be the cheese location, and
  ##          the last entry will be the mouse location.
  ##          The function will return 1 in this case.
  ##        - If no path is found, set AI_global_data.MousePath
  ##          to be an empty list, and return 0. The mouse
  ##          will wait at its current location for cats to move
  ##          away from possible paths to the cheese.
  ##        - Add any local data you need.
  ##        - Be careful to expand each location only once!
  ##        - Given a current location [x,y], its neighbours
  ##          *MUST* be expanded in the following order:
  ##          top, right, bottom, left.
  ##      - Mouse can't go through cats. If your search
  ##          reaches a location with a cat, it must backtrack.
  ##        - If multiple cheese exist, return the path to the
  ##          first cheese found
  ###################################################################

  # initialize
  search_order = -1

  queue = []
  queue.append( getMouseCoords() )

  # visited mask
  visited = np.zeros( (AI_global_data.msx, AI_global_data.msy) )

  (x, y) = getMouseCoords()
  visited[x][y] = 1

  while queue:
    # dequeue
    (x,y) = queue.pop(0)

    # if there's cheese there, we found it
    if checkForCheese(x,y):
      break

    # update the last search_order parameter
    search_order = search_order + 1
    AI_global_data.Maze[x][y] = search_order

    # find all that do not have cats, and have not been visited
    neighbours = filter(
      # don't even expand nodes that have a cat on them
      lambda (_,(xi,yi)): not visited[xi][yi] and not checkForCats(xi,yi),
      nonBlockedWalls(x,y) # don't go through walls
    )

    # set the node visited, point back to the parent
    for (dir, (xa,ya)) in neighbours:
      visited[xa][ya] = 1
      # dir is the direction from (x,y) -> (xa,ya)
      # opposite returns the dir from (xa,ya) -> (x,y)
      # this tells us later how to travel back from the cheese
      AI_global_data.P[xa][ya] = opposite(dir)

    # add the walkable coordinates back to the list
    queue.extend( map( lambda (_, coords): coords, neighbours) )

  # rebuild the path backwards from the direction data we set earlier
  path = [ (x,y) ]
  while (x,y) != getMouseCoords():
    (x,y) = adjacentCoordinates(x,y) [ int(AI_global_data.P[x][y]) ]
    path.append( (x, y) )

  # need this check since we set path to contain cheeseCoords
  if len(path) >= 1:
    AI_global_data.MousePath = path
    return 1

  return 0  # No path found

def DFS(DFS_stack,cnt):
  # Depth-first search

  ###################################################################
  ## TO DO: Implement DFS here starting at the mouse's location
  ##        and ending at the cheese location. Be sure to update
  ##        the Maze[][] array to indicate in which order maze
  ##        locations were expanded while looking for a path to
  ##        the cheese.
  ##
  ## Notes:
  ##        - This is a *RECURSIVE* function, do not try to turn
  ##          it into an iterative one. DFS is an ideal candidate
  ##          for recursion. There are several ways to build the
  ##          mouse path once you find the cheese, but one way is
  ##          to get the path directly from the recursion sequence.
  ##        - Except for the recursive nature of DFS, the same
  ##          conditions apply as for BFS above.
  ##        - For a given node, its children will also be expanded
  ##          in order top,right,bottom,left.
  ###################################################################

  # base case
  if cnt == 0:
    mouse = getMouseCoords()
    DFS_stack.append( mouse )

    AI_global_data.MousePath = []
    return DFS(DFS_stack, cnt + 1)
  # recursive case
  else:
    (x,y) = DFS_stack.pop()
    # P is the visited mask here
    AI_global_data.P[x][y] = 1

    # if we are at the cheese, return 1 to end the recursion
    if checkForCheese(x,y):
      AI_global_data.MousePath.append( (x,y) )
      return 1

    # for visualizations
    AI_global_data.Maze[x][y] = cnt

    neighbours = filter(
      # don't even expand nodes that have a cat on them, or already visited
      lambda (_,(xi,yi)): not checkForCats(xi,yi) and not AI_global_data.P[xi][yi],
      nonBlockedWalls(x,y) # don't go through walls
    )

    for (dir, (xa,ya)) in neighbours:
      DFS_stack.append( (xa, ya) )
      cnt = cnt + 1
      if DFS(DFS_stack, cnt):
        AI_global_data.MousePath.append( (xa, ya) )
        return 1

    return 0  # No path found

def Astar():
  # A* search

  ###################################################################
  ## TO DO: Implement A* search as discussed in lecture. Note that
  ##        I am not giving you the heuristic cost function. You
  ##        are responsible for coming up with an *admissible*
  ##        heuristic (justify your choice and explain why it is
  ##        admissible in your report).
  ##
  ## Notes:
  ##        - Same conditions apply as for BFS and DFS.
  ##        - This is *NOT* a recursive function.
  ##        - Expansion order given by cost estimate. Be sure to
  ##          compute the cost for each location correctly! and note
  ##          it is *NOT* only the heuristic cost.
  ##        - If multiple cheese exist, you need to account for that
  ##          somehow in the heuristic cost function. Explain in
  ##          the report how you handle this.
  ###################################################################

  # initialize
  search_order = -1

  closed = np.zeros( (AI_global_data.msx, AI_global_data.msy) )
  g_cost = np.zeros( (AI_global_data.msx, AI_global_data.msy) )

  (x, y) = getMouseCoords()
  g_cost[x][y] = 0
  closed[x][y] = 1
  f_cost = g_cost[x][y] + Astar_cost(x,y)

  # dictionary is easier than simple list
  openset = { f_cost: [ (x,y) ] }

  while openset:
    # if the dictionary has no nodes left, next throws an error
    # so we just catch it and say there's no path
    try:
      key = next(key for key in sorted(openset.keys()) if openset[key])
    except:
      return 0

    # since the dictionary keeps the same cost on the list
    x,y = openset[key].pop(0)

    # if we are at the goal, reconstruct the path
    if checkForCheese(x,y):
      break

    # add to the closed set
    closed[x][y] = 1

    search_order = search_order + 1
    AI_global_data.Maze[x][y] = search_order

    neighbours = filter(
      lambda (_, (xi,yi)): not closed[xi][yi] and not checkForCats(xi,yi),
      nonBlockedWalls(x,y)
    )

    # A* algorithm
    for (dir, (xa,ya)) in neighbours:
      new_cost = g_cost[x][y] + 1
      f_cost = g_cost[xa][ya] + Astar_cost(xa, ya)
      if f_cost not in openset:
        openset[f_cost] = []

      if (xa,ya) not in openset[f_cost] or new_cost < g_cost[xa][ya]:
        openset[f_cost].append( (xa, ya) )
        AI_global_data.P[xa][ya] = opposite(dir)

  # reconstruct the path
  path = [ (x,y) ]
  while (x,y) != getMouseCoords():
    # get the parent
    (x,y) = adjacentCoordinates(x,y) [ int(AI_global_data.P[x][y]) ]
    path.append( (x, y) )

  if len(path) >= 1:
    # set the path accordingly
    AI_global_data.MousePath = path
    return 1

  return 0  # No path found

def Astar_nokitty():
  # A* search with cat-dependent heuristic

  ###################################################################
  ## TO DO: This is an improved version of A* that not only
  ##        uses cheese locations in the heuristic cost function,
  ##        but also tries to account for cat locations. Your
  ##        heuristic should be such that the mouse avoids as
  ##        far as possible going too near any cats while at the
  ##        same time finding efficiently a path to the cheese.
  ##
  ##        Explain your heuristic cost function, how the cheese
  ##        and cat locations influence the cost, and whether it
  ##        is admissible or not.
  ##
  ## Notes:
  ##        - Same conditions apply as for BFS and DFS and Astar.
  ###################################################################

  search_order = -1

  closed = np.zeros( (AI_global_data.msx, AI_global_data.msy) )
  g_cost = np.zeros( (AI_global_data.msx, AI_global_data.msy) )

  (x, y) = getMouseCoords()
  g_cost[x][y] = 0
  closed[x][y] = 1
  f_cost = g_cost[x][y] + Astar_cost_nokitty(x,y)

  openset = { f_cost: [ (x,y) ] }

  while openset:
    try:
      key = next(key for key in sorted(openset.keys()) if openset[key])
    except:
      return 0
    x,y = openset[key].pop(0)

    # if we are at the goal, reconstruct the path
    if checkForCheese(x,y):
      break

    # add to the closed set
    closed[x][y] = 1

    search_order = search_order + 1
    AI_global_data.Maze[x][y] = search_order

    neighbours = filter(
      lambda (_, (xi,yi)): not closed[xi][yi],
      nonBlockedWalls(x,y)
    )

    for (dir, (xa,ya)) in neighbours:

      new_cost = g_cost[x][y] + 1
      f_cost = g_cost[xa][ya] + Astar_cost_nokitty(xa, ya)
      if f_cost not in openset:
        openset[f_cost] = []

      if (xa,ya) not in openset[f_cost] or new_cost < g_cost[xa][ya]:
        openset[f_cost].append( (xa, ya) )
        AI_global_data.P[xa][ya] = opposite(dir)

  # reconstruct the path
  path = [ (x,y) ]
  while (x,y) != getMouseCoords():
    (x,y) = adjacentCoordinates(x,y) [ int(AI_global_data.P[x][y]) ]
    path.append( (x, y) )

  if len(path) >= 1:
    # set the path accordingly
    AI_global_data.MousePath = path
    return 1

  return 0  # No path found
