##################################################################
# CSC D84 - Non-deterministic programming example
#
# Let us try to move a set of N tigers and M people across a river
#
# Your task is to use the functions provided by this starter file.
#
# ** You can only modify the function called 'SearchForPlan'
# ** Do not touch any other part of the starter code, as we
# ** may replace and swap components for testing. Your solution
# ** must not depend on details of how the calls provided to
# ** you are implemented.
#
# Now, go move some tigers across the river!
#
# Starter: F.J.E. Dec. 2014
###################################################################
from random import *        # I apologize, but not too much
import sys

class chalupa:
    """
    This is a small boat - typically found floating in Xochimilco
    It can also be a tasty form of street food. Take your pick.
    """
    def __init__(self):
        self.side=0     # Boat always starts on the left river bank
        self.contents=list()    # and is empty

def initialize_game(N,M,Left):
    """
    Sets up the initial creatures list
    All creatures always start on the left river bank
    """
    for i in range(N):
        Left.append('T')
    for i in range(M):
        Left.append('P')
    print "Initial creatures list: ", Left_Side

def reset_game(Left,Right,Boat,Backup):
    """
    Reset lists to initial configuration - needed during search for command sequence
    evaluation. YOU WILL NOT call this function within SearchForPlan()
    """
    while len(Left)>0:
        Left.pop()
    for i in range(len(Backup)):
        Left.append(Backup[i])
    while len(Right)>0:
        Right.pop()
    while len(Boat.contents)>0:
        Boat.contents.pop()
    Boat.side=0

def load_type(t,Left,Right,Boat):
    """
    Loads an entity of type t in ['T' 'P'] onto the boat. If there
    is no such entity left on the corresponding side of the river
    it does nothing.
    Assumes there is space in the boat for at least one item, else
    does nothing.
    """

    if len(Boat.contents)>1:
        return 0

    if Boat.side==0:
        Active_List=Left
    else:
        Active_List=Right

    try:
        x=Active_List.index(t)
        Boat.contents.append(Active_List.pop(x))
        return 1
    except ValueError:
        # None left on this side
        return 0

def unload_type(t,Left,Right,Boat):
    """
    Unload a creature of the specified type onto the current side
    of the river
    If no such creature is on the boat does nothing
    """

    if len(Boat.contents)==0:
        return 0

    if Boat.side==0:
        Active_List=Left
    else:
        Active_List=Right

    try:
        x=Boat.contents.index(t)
        Active_List.append(Boat.contents.pop(x))
        return 1
    except ValueError:
        # No such creature left
        return 0

def swap_type(t,Left,Right,Boat):
    """
    Swap one creature between the boat and the riverside. In this case 't' is the type
    of creature on the Boat that will be swapped out.
    """

    if len(Boat.contents)==0:
        return 0

    if t=='P':
        tt='T'
    else:
        tt='P'

    try:
        x=Boat.contents.index(t)
    except ValueError:
        # No such creature left on Boat
        return 0

    if Boat.side==0:
        Active_List=Left
    else:
        Active_List=Right

    try:
        y=Active_List.index(tt)
    except ValueError:
        # No such creature left on river bank
        return 0

    # Swap!
    Active_List[y]=t
    Boat.contents[x]=tt
    return 1

def cross(Boat):
    """
    Takes the Boat across the river
    Boat must have at least one person (Tigers can't drive boats,
        just ask Pi)
    """

    try:
        x=Boat.contents.index('P')
        if (Boat.side==0):
            Boat.side=1
        else:
            Boat.side=0
        return 1
    except ValueError:
        # No people in the boat
        return 0

def numP(where):
    """
    Return the number of people within the list 'where'
    """
    pp=0
    for i in range(len(where)):
        if where[i]=='P':
            pp=pp+1

    return pp

def numT(where):
    """
    Return the number of tigers within the list 'where'
    """
    tt=0
    for i in range(len(where)):
        if where[i]=='T':
            tt=tt+1

    return tt

def check_state(Left,Right,Boat):
    """
    Verifies the current configuration to ensure no people are
    being lunched on.
    Returns: -1 if the current config. causes people to be eaten
         0 if the current config is safe
         1 if the current config is a solution
    """

    if numT(Left)>numP(Left) and numP(Left)>0:
        return -1

    if numT(Right)>numP(Right) and numP(Right)>0:
        return -1

    if numT(Right)-numP(Right)>2:       # Unsolvable!
        return -1

    if len(Left)==0 and len(Boat.contents)==0:
        print "Found a solution!"
        print Left,"****",Boat.contents,"****",Right
        return 1
    else:
        return 0

def SearchForPlan(some_plan,Left,Right,Boat,Backup):
    """
    Generate a sequence of program actions to solve the transportation problem
    Starts with an empty plan, progressively adds commands from the following
    choices:
        * load_type(t)     (append to plan [load_type, t])
        * cross()      (append to plan [cross, []])
        * unload_type(t)   (append to plan [unload_type, t])
        * swap_type(t)     (append to plan [swap, t])

    In the commands above, t can be either 'T' or 'P' and your search code can
    add commands in any order.

    Once you have created a new plan, execute the plan by calling RunPlan(plan)

    You will receive a return value of:
        -1  if your plan leads to a configuration where people are eaten.
            In this case you must backtrack (up to you how much) and
            keep searching
        0   The current plan results in a safe configuration, you can keep
            adding commands to it
        1   A solution has been found! you're done
    """

    ##############################################################################
    ## TO DO:
    ##   Add your search code below. Mind the following constraints:
    ##    You are not to use graph search to come up with your plan (i.e. you
    ##      are not allowed to solve the problem in order to solve the problem!)
    ##    You are not allowed to call commands directly. All actions must be
    ##      part of the plan you are searching for
    ##    You are not allowed to hardcode the solution for a given N and M
    ##  (yes, I know you can solve the problem in your head. So can I. We
    ##   are studying how non-deterministic-programming works. So work
    ##   with it and learn!)
    ##    You are not allowed to change or update the contents of:
    ##      Left_Side
    ##      Right_Side
    ##      Boat
    ##      creatures
    ##      tries
    ##    The simplest plan generation method will find a solution - given enough
    ##  time. But you should aim for a smarter search process that does not
    ##  require a ridiculous amount of search.
    ##
    ##    You can choose to use recursion, or not. As you please. But explain your
    ##  choice in the report.
    ###############################################################################

    some_plan.append([cross, []])
#       If you need to see what your code is doing, you should print the plan!
    print "DEBUG: ***** "
    print "Current plan:"
    print some_plan

    # Below is an example of how to run input plan
    x=RunPlan(some_plan,Left,Right,Boat,Backup)
    print x
#   if x!=0:
#       # Failed or succeeded - do something about it
#   else:
#       # Safe configuration - do something different about it

    return 1  # You will need to change this of course - somehow.

def RunPlan(some_plan,Left,Right,Boat,Backup):
    """
    Execute the current command sequence - on a clean game state

    If the command sequence does not cause an unsafe configuration, this function will
    return:
        0   -   If the game state is not a solution
        1   -   If the game state is a solution
    Otherwise the function returns -1
    """
    global tries

    reset_game(Left,Right,Boat,Backup)

    tries=tries+1

    if len(some_plan)==0:       # Initial empty plan
        return 0

    for i in range(len(some_plan)):
        if (some_plan[i][0]==cross):
            y=some_plan[i][0](Boat)
        else:
            y=some_plan[i][0](some_plan[i][1],Left,Right,Boat)
        x=check_state(Left,Right,Boat)
        if x==-1 or y==0:
            return -1   # Results in an unsafe configuration

        if x==1:
            print "Solution found!, total tries=",tries," plan length=",len(some_plan)
            return 1
    return 0

if __name__=="__main__":

    Left_Side=list()
    Right_Side=list()
    Left_Backup=list()
    tries=0
    Boat=chalupa()

    initialize_game(1,1,Left_Side)  # <-- Your solution should work with 3 tigers, 3 people!
    Left_Backup=list(Left_Side) # <-- I could re-initialize, but why not just make a copy?

    plan=list() # Here! I'm giving you an empty plan! Am I Not Merciful?
            # (if you don't get that, you haven't seen Gladiator)

    # Call your search code to build the solution to this problem
    SearchForPlan(plan,Left_Side,Right_Side,Boat,Left_Backup)

    # We have a solution! let's run it and see how it works
    reset_game(Left_Side,Right_Side,Boat,Left_Backup)
    print "Left Side        Boat            Right Side"
    for i in range(len(plan)):
        if plan[i][0]==cross:
            print "Crossing!"
            plan[i][0](Boat)
        else:
            plan[i][0](plan[i][1],Left_Side,Right_Side,Boat)
        if Boat.side==0:
            print Left_Side,"   ",Boat.contents,"           ",Right_Side
        else:
            print Left_Side,"           ",Boat.contents,"   ",Right_Side

    print "Done!"

