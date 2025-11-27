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
from pacman import GameState
from evaluator import computeMinDistanceToFoodAndCapsule, computeMinDistanceToUnscaredGhost

from typing import Tuple


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # return successorGameState.getScore()

        return betterEvaluationFunction(successorGameState)


def scoreEvaluationFunction(currentGameState: GameState):
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
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        _, action = self._getMinimaxInfo(gameState, self.depth, self.index)
        return action

    def _getMinimaxInfo(self, gameState: GameState, more_levels: int, agentIndex: int) -> Tuple[float, str]:
        """
        Helper function to get the minimax info for a given game state
        Return a tuple of (score, action)
        1. If the game state is a terminal state (win/lose), return the score
        2. If more_levels == 0, return the evaluation function value
        3. Otherwise, for each legal action, get the successor state and
           recursively call _getMinimaxValue on the successor state with
            updated more_levels and agentIndex; if agentIndex == 0, it's a max node,
            otherwise it's a min node.
        """
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore(), Directions.STOP
        if more_levels == 0:
            return self.evaluationFunction(gameState), Directions.STOP
        
        legal_actions = gameState.getLegalActions(agentIndex)
        successors = []
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            next_agent_index = (agentIndex + 1) % gameState.getNumAgents()
            next_more_levels = more_levels - 1 if next_agent_index == 0 else more_levels
            succ_score, _ = self._getMinimaxInfo(successor_state, next_more_levels, next_agent_index)
            successors.append((succ_score, action))

        if agentIndex == 0:
            return max(successors, key=lambda x: x[0])
        else:
            return min(successors, key=lambda x: x[0])


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = float("-inf")
        beta = float("inf")
        _, action = self._getMinimaxInfo(gameState, alpha, beta, self.depth, self.index)
        return action

    def _getMinimaxInfo(self, gameState: GameState, alpha: float, beta: float, more_levels: int, agentIndex: int) -> Tuple[float, str]:
        """
        Helper function to get the minimax info for a given game state
        It is accelerated with alpha-beta pruning.
        Return a tuple of (score, action)
        1. If the game state is a terminal state (win/lose), return the score
        2. If more_levels == 0, return the evaluation function value
        3. Otherwise, for each legal action, get the successor state and
           recursively call _getMinimaxValue on the successor state with
           updated more_levels and agentIndex; if agentIndex == 0, it's a max node,
           otherwise it's a min node.
        """
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore(), Directions.STOP
        if more_levels == 0:
            return self.evaluationFunction(gameState), Directions.STOP
        
        if agentIndex == 0:
            v = float("-inf")
        else:
            v = float("inf")
        best_action = Directions.STOP

        legal_actions = gameState.getLegalActions(agentIndex)
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            next_agent_index = (agentIndex + 1) % gameState.getNumAgents()
            next_more_levels = more_levels - 1 if next_agent_index == 0 else more_levels
            succ_score, _ = self._getMinimaxInfo(successor_state, alpha, beta, next_more_levels, next_agent_index)
        
            if agentIndex == 0:
                v = max(v, succ_score)
                if v > beta:
                    return v, best_action
                if v > alpha:
                    alpha = v
                    best_action = action
            else:
                v = min(v, succ_score)
                if v < alpha:
                    return v, best_action
                if v < beta:
                    beta = v
                    best_action = action

        return v, best_action

            

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        _, action = self._getExpectimaxInfo(gameState, self.depth, self.index)
        return action

    def _getExpectimaxInfo(self, gameState: GameState, more_levels: int, agentIndex: int) -> Tuple[float, str]:
        """
        Helper function to get the expectimax info for a given game state
        Return a tuple of (score, action)
        1. If the game state is a terminal state (win/lose), return the score
        2. If more_levels == 0, return the evaluation function value
        3. Otherwise, for each legal action, get the successor state and
           recursively call _getExpectimaxInfo on the successor state with
            updated more_levels and agentIndex; if agentIndex == 0, it's a max node,
            otherwise it's a expect node.
        """
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore(), Directions.STOP
        if more_levels == 0:
            return self.evaluationFunction(gameState), Directions.STOP
        
        legal_actions = gameState.getLegalActions(agentIndex)
        successors = []
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            next_agent_index = (agentIndex + 1) % gameState.getNumAgents()
            next_more_levels = more_levels - 1 if next_agent_index == 0 else more_levels
            succ_score, _ = self._getExpectimaxInfo(successor_state, next_more_levels, next_agent_index)
            successors.append((succ_score, action))

        if agentIndex == 0:
            return max(successors, key=lambda x: x[0])
        else: # return STOP for action since it's not used
            return sum([s[0] for s in successors])/len(successors), Directions.STOP

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    totalScore = 0
    # add score already present in the successor state
    totalScore += currentGameState.getScore()
    # encourage eating capsules, the less remaining the better
    totalScore -= len(currentGameState.getCapsules()) * 20
    # encourage moving towards the closet food or capsule
    minFoodDist = computeMinDistanceToFoodAndCapsule(currentGameState)
    totalScore += 10 / 2 / (minFoodDist + 1)
    # discourage getting too close to unscared ghosts
    if computeMinDistanceToUnscaredGhost(currentGameState) == 1:
        totalScore -= 500 / 2
    return totalScore

# Abbreviation
better = betterEvaluationFunction
