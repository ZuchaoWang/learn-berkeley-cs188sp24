from typing import Tuple
from game import Directions
from game import Actions
from game import Grid
import search

class AnyPosSearchProblem(search.SearchProblem):
    """
    A search problem for finding a path to any of the listed positions.
    The positions can be of foods, or of ghosts.
    """

    def __init__(self, startPos: Tuple[int,int], endPoses: Grid, walls: Grid, costFn = lambda x: 1):
        self.startPos = startPos
        self.endPoses = endPoses
        self.walls = walls
        self.costFn = costFn

    def getStartState(self):
        return self.startPos

    def isGoalState(self, state: Tuple[int, int]):
        x,y = state
        return self.endPoses[x][y]
    
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        return successors
    
    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost


def computeMinDistanceToFoodAndCapsule(gameState) -> int:
    """
    Computes the minimum distance from startPos to any food or capsule in the gameState.
    Returns 0 if there is no food or capsule.
    """
    foodAndCapsule = gameState.getFood().copy()
    for capsule in gameState.getCapsules():
        foodAndCapsule[int(capsule[0])][int(capsule[1])] = True

    if foodAndCapsule.count() == 0:
        return 0
    
    startPos = gameState.getPacmanPosition()
    walls = gameState.getWalls()
    problem = AnyPosSearchProblem(startPos, foodAndCapsule, walls)
    path = search.bfs(problem)

    return problem.getCostOfActions(path)


def computeMinDistanceToUnscaredGhost(gameState) -> int:
    """
    Computes the minimum distance from startPos to any ghost in the gameState.
    Returns 999999 if there is no ghost.
    """
    ghostStates = gameState.getGhostStates()
    walls = gameState.getWalls()
    ghostPositionsGrid = Grid(walls.width, walls.height, False)
    for ghostState in ghostStates:
        pos = ghostState.getPosition()
        scaredTimer = ghostState.scaredTimer
        if scaredTimer <= 1: # either unscared or about to be unscared
            ghostPositionsGrid[int(pos[0])][int(pos[1])] = True

    if ghostPositionsGrid.count() == 0:
        return 999999

    startPos = gameState.getPacmanPosition()
    problem = AnyPosSearchProblem(startPos, ghostPositionsGrid, walls)
    path = search.bfs(problem)

    return problem.getCostOfActions(path)