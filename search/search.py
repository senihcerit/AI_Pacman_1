# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    print "------------------ DFS ------------------"
    #We can use Stack Data Structure for Depth First Search. Because We have to keep parent class of childs(if we dont find goal state in our depth state, we have to go back and go to other childs)
    my_stack = util.Stack() #Our stack name is my_stack.
    visited_states = [] #We keep visited states
    path = [] #We keep minimum way to goal from start state
    start_state = problem.getStartState() #Name of the start state is start_state. And we define start state with .getStartState

    if problem.isGoalState(start_state): #if start state is also goal state we dont need to search anything
        return path #if goal state is start state we return empty path
    else: #unless start state is goal state
        item = (start_state, path) #item is our start state in the path
        my_stack.push(item) #and we put this item into the our stack.

        while(my_stack.isEmpty() != True): #until there is no item in our stack - dont quit from loop
            current_pos, path = my_stack.pop() #current_pos is current position. we keep the position where we are. and we pop(delete) top item from our stack
            if problem.isGoalState(current_pos): #if we reach to goal state (if our position is the goal state)
                return path #if goal state is current position we return path
            visited_states.append(current_pos) #we are adding current position to visited states
            new_successors = problem.getSuccessors(current_pos) #and we keep successors of the our current position state as new_successors

            if new_successors: #if we have new successors
                for successor in new_successors: #for every successor in new_successors we enter to loop
                    if successor[0] not in visited_states: #if first successor has not been visited
                        new_path = path + [successor[1]] #our new path is addition of the our path and second successor
                        item = (successor[0], new_path) #item is our first successor in new path
                        my_stack.push(item) #we adding item to our stack
                        print "New Path:", new_path #printing new path as solution

def breadthFirstSearch(problem):
    print "------------------ BFS ------------------"
    #We can use Queue data structure for Breadth First Search. Because queue has first in first out methodology. and our breadth fs is same as this methodology
    my_queue = util.Queue() #Our queue name is my_queue
    visited_states = [] #We keep visited states
    path = [] #We keep minimum way to goal from start state
    start_state = problem.getStartState() #Name of the start state is start_state. And we define start state with .getStartState

    if problem.isGoalState(start_state): #if start state is also goal state we dont need to search anything
        return path #if goal state is start state we return empty path
    else: #unless start state is goal state
        item = (start_state, path) #item is our start state in the path
        my_queue.push(item) #and we put this item into the our queue

        while(my_queue.isEmpty() != True): #until there is no item in our queue - dont quit from loop
            current_pos, path = my_queue.pop() #current_pos is current position. we keep the position where we are. and we pop(delete) top item from our queue
            if problem.isGoalState(current_pos): #if we reach to goal state (if our position is the goal state)
                return path #if goal state is current position we return path
            visited_states.append(current_pos) #we are adding current position to visited states
            new_successors = problem.getSuccessors(current_pos) #and we keep successors of the our current position state as new_successors
            current_queue = (state[0] for state in my_queue.list) #we create a new queue from first index of each states in our queue as current_queue

            #DONT FOCUS ON THIS
            #print "---------------------------"
            #for state in my_queue.list:
            #    print state[0]
            #print "---------------------------"

            if new_successors: #if we have new successors
                for successor in new_successors: #for every successor in new_successors we enter to loop
                    if (successor[0] not in visited_states) and (successor[0] not in current_queue): #if first successor has not been visited and it is not in the current_queue
                        new_path = path + [successor[1]] #our new path is addition of the our path and second successor
                        item = (successor[0], new_path)  #item is our first successor in new path
                        my_queue.push(item) #we adding item to our queue
                        print "New Path:", new_path #printing new path as solution

def uniformCostSearch(problem):
    print "------------------ UniformCost ------------------"
    #We can use Priority Queue data structure for uniform Cost Search. Because in the uniform cost search, we choose new state according to the minimum cost and it can be applied with priority queue
    my_pqueue = util.PriorityQueue() #Our priority queue's name is my_pqueue
    visited_states = [] #We keep visited states
    path = [] #We keep minimum way to goal from start state
    start_state = problem.getStartState() #Name of the start state is start_state. And we define start state with .getStartState
    priorty = 0 # our priority is 0 now

    if problem.isGoalState(start_state): #if start state is also goal state we dont need to search anything
        return path #if goal state is start state we return empty path
    else: #unless start state is goal state
        item = (start_state, path) #item is our start state in the path
        my_pqueue.push(item, priorty) #and we put this item into the our priority queue

        while(my_pqueue.isEmpty() != True): #until there is no item in our priority queue - dont quit from loop
            current_pos, path = my_pqueue.pop() #current_pos is current position. we keep the position where we are. and we pop(delete) top item from our priority queue
            if problem.isGoalState(current_pos): #if we reach to goal state (if our position is the goal state)
                return path #if goal state is current position we return path
            visited_states.append(current_pos) #we are adding current position to visited states
            new_successors = problem.getSuccessors(current_pos) #and we keep successors of the our current position state as new_successors
            current_queue = (state[2][0] for state in my_pqueue.heap) #we create a new queue from [2][0] index of each states in our queue as current_queue (we know PriorityQueue is using heap)
            #according to priority, it gives us to past
            #print "---------------------------"
            #for state in my_pqueue.heap:
            #    print state[2][0]
            #print "---------------------------"
            # tryings for see DONT FOCUS ON THIS
            if new_successors: #if we have new successors
                for successor in new_successors: #for every successor in new_successors we enter to loop
                    if successor[0] not in visited_states:  #if first successor has not been visited and it is not in the visited_states
                        if successor[0] not in current_queue: #if first successor has not been visited and it is not in the current_queue
                            new_path = path + [successor[1]] #our new path is addition of the our path and second successor
                            priorty = problem.getCostOfActions(new_path) #our new priorty is actions cost for new path
                            item = (successor[0], new_path) #item is our first successor in new path
                            my_pqueue.push(item, priorty) #we adding item to our priority queue
                        else: #unless successor [0] not in current queue
                            for state in my_pqueue.heap: #we use loop for states in the heap of the priorty queue
                                if state[2][0] == successor[0]: #if first successor is equal to state[2][0]
                                    old_priorty = problem.getCostOfActions(state[2][1]) #old priorty is equal to actions cost of the state [2][1]
                            new_priorty = problem.getCostOfActions(path + [successor[1]]) #our new priority is actions cost of the addition path and second successor

                            if old_priorty > new_priorty: #if old priorty is bigger than old
                                new_path = path + [successor[1]] #our new path is the addition of path and second successor
                                item = (successor[0], new_path) #item is our first successor in new path
                                my_pqueue.update(item, new_priorty) #we are updating our priority queue with item and new priority
                        print "New Path:", new_path #printing new path as solution

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
"""
def manhattanHeuristic(state, problem):
    return problem.manhattanDistance(state[0], problem.goal)
"""

def aStarSearch(problem, heuristic=nullHeuristic):
    print "------------------ aStar ------------------"
    # We use priorty queue for a star algorithm. Because we are adding to cost and hueristic costs. and it looks like uniform cost.
    print heuristic #we call heuristic
    my_pqueue = util.PriorityQueue() #our priority queue's name is my_pqueue
    visited_states = [] #We keep visited states
    path = [] #We keep minimum way to goal from start state
    start_state = problem.getStartState() #Name of the start state is start_state. And we define start state with .getStartState
    priorty = 0 #our priority is 0 now

    if problem.isGoalState(start_state): #if start state is also goal state we dont need to search anything
        return path #if goal state is start state we return empty path
    else: #unless start state is goal state
        item = (start_state, path) #item is our start state in the path
        my_pqueue.push(item, priorty) #and we put this item into the our priority queue

        while(my_pqueue.isEmpty() != True): #until there is no item in our priority queue - dont quit from loop
            current_pos, path = my_pqueue.pop() #current_pos is current position. we keep the position where we are. and we pop(delete) top item from our priority queue
            if current_pos in visited_states: #if current position is in the visited states
                continue #we can continue
            if problem.isGoalState(current_pos): #if we reach to goal state (if our position is the goal state)
                return path #if goal state is current position we return path

            visited_states.append(current_pos) #we are adding current position to visited states
            new_successors = problem.getSuccessors(current_pos) #and we keep successors of the our current position state as new_successors

            if new_successors: #if we have new successors
                for successor in new_successors: #for every successor in new_successors we enter to loop
                    if successor[0] not in visited_states: #if first successor has not been visited and it is not in the visited_states
                        new_path = path + [successor[1]] #our new path is addition second successor to our path
                        new_priorty = problem.getCostOfActions(path + [successor[1]]) + heuristic(successor[0], problem=problem) #our new priority is ADDITION OF actions cost of the second accessors to path and heuristic valuee of the first successor
                        item = (successor[0], new_path)  #item is our first successor in new path
                        my_pqueue.push(item, new_priorty) #we adding item to our priority queue with new priority
                        print "New Path:", new_path #printing new path as solution

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
