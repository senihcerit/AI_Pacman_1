# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py) - thanks
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "**************************************************************************************************************"

        currentFood = currentGameState.getFood(); # we are getting food from current game state and we will called as currentFood
        score = 0  # our score's initialize value is zero
        scoresArray = [2000, -200, 100, 10.0, 1.0] # these are our scores. we put them into array.

        for ghostState in newGhostStates: # for any ghost in the newGhostStates
          decisive = 1 # our decisive value is zero
          position = ghostState.getPosition() # we are taking ghost's position
          distance = manhattanDistance(newPos , position) # and we are calculating manhattanDistance btw newPos and position

          if(distance<=1): # if our manhattanDistance is less than 1
            if(ghostState.scaredTimer==0): # this scared time is time which our ghost is not eating us
              score = score + scoresArray[1] # our new score is old score minus 200
            else: # normal condition
              score = score + scoresArray[0] # our new score is old score plus 2000
              decisive = -1 # our decisive value is -1

        for capsule in currentGameState.getCapsules(): # for any capsule in the currentGameState

          distance = manhattanDistance(newPos , capsule) # we are calculating manhattanDistance btw newPos and capsule
          if(distance==0): score = score + scoresArray[2] # if the manhattanDistance is zero, our score is addition of the old score and 100
          else:            score = score + (scoresArray[3]/distance) # if our manhattanDistance is not zero, our score is addition of the old score and (10/distance)

        for x in xrange(currentFood.width): # for any x in the xrange. current food's width is used
          for y in xrange(currentFood.height): # for any y in the yrange. current food's height is used
            if(currentFood[x][y]):
              distance = manhattanDistance(newPos , (x,y)) # we are calculating manhattanDistance btr newPos and (x,y)
              if(distance==0): score = score + scoresArray[2] # if our manhattanDistance is zero, our score is addition of the 100 and old score
              else:            score = score + (scoresArray[4]/(distance*distance)) # if our manhattanDistance is not zero, our score is addition of the  old score and (1 over square of the distance)


        print(score) # BUNU KAPATMAYI UNUTMA---------------------
        return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)




class MinimaxAgent(MultiAgentSearchAgent):
    """
      QUESTION 2
    """
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        "**************************************************************************************************************"
        depth = self.depth * 2 # this is our depth for tree
        maxim = True # our maximizing value is true
        agent = 0 # our agent is zero
        minimaxResult = self.minimax(gameState, depth, agent, maxim)[1] # and we use minimaxResult for minimax algorithm

        return minimaxResult
        util.raiseNotDefined()

    def minimax(self, gameState, depth, agent = 0, maximizing = True): #this is our minimax algorithm

        if gameState.isWin() or gameState.isLose() or depth == 0 : # if our state is win or lose, and if our depth is equal to zero
            eFunc = self.evaluationFunction(gameState) # we are using eFunc for hold evaluationFunction
            direction = Directions.STOP # and we set direction as NO. STOP
            return eFunc , direction # returns efunc and direction

        actions = gameState.getLegalActions(agent) # this is our Legal Actions into actions

        if (maximizing == True):
            scores = [self.minimax(gameState.generateSuccessor(agent, action), depth - 1, 1, False)[0] for action in actions] # we can call minimax algorithm as a score
            maxScore = max(scores) # our best score is max(score)
            bestIndices = [i for i in range(len(scores)) if scores[i] == maxScore] # this is our best indices calculation
            action = actions[random.choice(bestIndices)] # our choice for action is using indice in the best indices randomly
            return maxScore, action
        else:
            scores = [] # we initialize our scores array as space
            if agent == gameState.getNumAgents() - 1: # this is for the last ghost
                scores = [self.minimax(gameState.generateSuccessor(agent, action), depth - 1, 0, True)[0] for action in actions] # we are calling minimax algorithm for set to score
            else:
                scores = [self.minimax(gameState.generateSuccessor(agent, action), depth, agent + 1, False)[0] for action in actions] # we are calling again with different depth, agent and maximizing value
            maxScore = min(scores) # this is our best score
            bestIndices = [i for i in range(len(scores)) if scores[i] == maxScore] # we are calculating our best indices
            action = actions[random.choice(bestIndices)] # we are choosing our action from best indices
            return maxScore, action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      QUESTION 3


      YOU SHOULD DO IT WITH THE PSEUDO CODE IN THE ASSIGNMENT 2

    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE *********************************************************************************************"
        depth = self.depth * 2 # this is our depth of the tree
        minusInfinity = -1e10000 # this is for max value algorithm
        plusInfinity = 1e10000 # this is for min value algorithm
        agent = 0 # our agents initializevalue is zero
        maximizing = True
        minimaxResult = self.minimax(gameState, depth, minusInfinity , plusInfinity , agent, maximizing)[1] # we are calling our function of Minimax
        return minimaxResult
        util.raiseNotDefined()

    def minimax(self, gameState, depth, alpha, beta, agent = 0, maximizing = True):
        if gameState.isWin() or gameState.isLose() or depth == 0: # if state is win or lose, if our depth is zero
            eFunc = self.evaluationFunction(gameState) # this is eFunc. it is evaluationFunction for state
            direction = Directions.STOP # we stop our state
            return eFunc, direction
        actions = gameState.getLegalActions(agent) # we use action from legal actions
        if maximizing:
            bestScore = -1e10000 # initialize v= minus infinity
            bestActions = [] # we initialize array with no arg
            for action in actions: # for any action
                value = gameState.generateSuccessor(agent, action)
                depthValue = depth - 1 # our depth is old depth minus 1
                agentValue = 1 # our agent value is one
                maximValue = False
                score = self.minimax(value , depthValue , alpha, beta, agentValue, maximValue)[0]
                if alpha >= score : alpha = alpha # this is our compairing score and alpha
                else: alpha = score # we found max value
                if score > bestScore: # if our score is bigger than best value
                    bestScore = score # our new best value is our score
                    bestActions = [action]
                elif score == bestScore: # if it equals to best score we added our action to bestActions
                    bestActions.append(action)
                if bestScore > beta: break
            action = random.choice(bestActions)
            return bestScore, action
        else:
            bestScore = 1e10000 # initialize v= plus infinity
            bestActions = [] # we initialize our array of the best action
            if agent == gameState.getNumAgents() - 1: # it is for last ghhost
                for action in actions: # for each action
                    value = gameState.generateSuccessor(agent, action)
                    depthValue = depth - 1 # our depth is old depth minus 1
                    agentValue = 0 # our agent value is zero
                    maximValue = True
                    score = self.minimax(value, depthValue, alpha, beta, agentValue, maximValue)[0]
                    if beta >= score : beta = score # this is compairing beta and score
                    else: beta = beta # we found our minimum value
                    if score < bestScore: # if our score is less than min value
                        bestScore = score # new minimum score is our score
                        bestActions = [action]
                    elif score == bestScore:
                        bestActions.append(action) # we adding our action to best Action
                    if alpha > bestScore: break
            else:
                for action in actions:
                    score = self.minimax(gameState.generateSuccessor(agent, action), depth, alpha, beta, agent + 1, False)[0]
                    if beta >= score : beta = score # we are compairing beta and score
                    else: beta = beta #we found our beta
                    if score < bestScore:
                        bestScore = score # we calculated in the if condition same explainings..
                        bestActions = [action]
                    elif score == bestScore:
                        bestActions.append(action) # we are adding this action to best actions
                    if alpha > bestScore: break # pruning
            choice =  random.choice(bestActions) # our choice is from best actions randompl
            return bestScore, choice

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      QUESTION 4 - BONUS
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE *********************************************************************************************"
        # i did not do bonus question
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <Teacher please care about 5th question answer. It is not working but i tried to solve a lot.
      If you give partial points, i will be happy. Thanks>





      numbers = [10000, 1000, 10, 1e100, -1]
      evaluationNumber = 0 # this is evaluation Number
      pacmanPosition = currentGameState.getPacmanPosition() # we are taking position of the pacman
      foodPositions = currentGameState.getFood().asList() # we are taking list of the food positions
      minimumDistance = numbers[0] # our minimum distance is 10000
      setMinimumDistance = False # our boolean value of the set min distance is false
      for fPosition in foodPositions: # for each food position in the array of the food positions
          foodDistance = manhattanDistance(fPosition , pacmanPosition) # we are calculatng manhattanDistance btw positions of the food and pacman
          if foodDistance < minimumDistance: # if distance of the food is less than minimum distance
              minimumDistance = foodDistance # our new minimum distance is food distance
              setMinimumDistance = True # we changed our minimum distance thats why boolean value is true
          if setMinimumDistance: # we changed our vboolean value and it will be enter this block
            evaluationNumber = evaluationNumber + minimumDistance # our elevation number will be changed. new elevation number is addition of old elevation number and minimum distance(food distance)
            evaluationNumber = evaluationNumber + (numbers[1]*currentGameState.getNumFood()) # new elevation number is addition of the old elevation number and (1000 * number of food)
            evaluationNumber = evaluationNumber + (numbers[2]*len(currentGameState.getCapsules())) # new elevation number is addition of the old elevation number and (10 * length of the capsules array)
          ghostPositions = currentGameState.getGhostPositions() #we are taking ghost positions array
          for gPosition in ghostPositions: # for all position in the array
              gDistance = manhattanDistance(pacmanPosition, gPosition) #distance of the ghost is calculated with manhattan distance algorith (between pacman position and ghost position)
          if gDistance < 2: # if our ghost distance is less than 2
            evaluationNumber = numbers[3] # our elevation number is infitinity
          evaluationNumber = evaluationNumber -  (numbers[2]*currentGameState.getScore()) # our elevation number is old elevation number minus (1000 * score )
          return evaluationNumber*(numbers[4])

    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
