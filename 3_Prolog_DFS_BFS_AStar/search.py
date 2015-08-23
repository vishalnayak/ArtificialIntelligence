# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    print problem.walls
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    print 'This is DFS'
    from searchAgents import direction_list
    from spade import pyxf
    import os
    """
    Building the XSB PROLOG query
    """
    myXsb = pyxf.xsb("/home/vishal/Downloads/xsb/XSB/bin/xsb")
    myXsb.load(os.getcwd() + '/maze.P')
    myXsb.load(os.getcwd() + '/dfs.P')
    q_result = myXsb.query("dfs(start,X)")
    result =  q_result[0]['X']
    result = result[1:]
    result = result[:-1]
    result = result.split(',')
    result.reverse()
    result = result[1:]
    result_list = list()
    result_list.append(direction_list[('start', result[0])])
    """
    Converting the list of actions returned by prolog into appropriate directions to be returned
    """
    for x in range(len(result) - 1):
        result_list.append(direction_list[(result[x], result[x + 1])])
    return result_list


def breadthFirstSearch(problem):
    print 'This is BFS!'
    if problem.problemType is 'Position':
        from searchAgents import direction_list
        from spade import pyxf
        import os
        """
        Building the XSB PROLOG query
        """
        myXsb = pyxf.xsb("/home/vishal/Downloads/xsb/XSB/bin/xsb")
        myXsb.load(os.getcwd() + '/maze.P')
        myXsb.load(os.getcwd() + '/bfs.P')
        q_result = myXsb.query("bfs(start,X)")
        result =  q_result[0]['X']
        result = result[1:]
        result = result[:-1]
        result = result.split(',')
        result.reverse()
        result = result[1:]
        result_list = list()
        result_list.append(direction_list[('start', result[0])])
        """
        Converting the list of actions returned by prolog into appropriate directions to be returned
        """
        for x in range(len(result) - 1):
            result_list.append(direction_list[(result[x], result[x + 1])])
        return result_list
    elif problem.problemType is 'Corners':
        from searchAgents import direction_list
        from spade import pyxf
        import os
        merged_result = []

        """
        Building the XSB PROLOG query
        """
        myXsb = pyxf.xsb("/home/vishal/Downloads/xsb/XSB/bin/xsb")
        myXsb.load(os.getcwd() + '/maze.P')
        myXsb.load(os.getcwd() + '/bfs.P')
        myXsb.load(os.getcwd() + '/corner4.P')
        q_result = myXsb.query("bfs(start,X)")
        result =  q_result[0]['X']
        result = result[1:]
        result = result[:-1]
        result = result.split(',')
        merged_result.extend(result[1:])

        """
        Building the XSB PROLOG query
        """
        myXsb = pyxf.xsb("/home/vishal/Downloads/xsb/XSB/bin/xsb")
        myXsb.load(os.getcwd() + '/maze.P')
        myXsb.load(os.getcwd() + '/bfs.P')
        myXsb.load(os.getcwd() + '/corner3.P')
        q_result = myXsb.query("bfs("+str(result[0])+",X)")
        result =  q_result[0]['X']
        result = result[1:]
        result = result[:-1]
        result = result.split(',')

        temp = result[1:]
        temp.extend(merged_result)
        merged_result = temp

        """
        Building the XSB PROLOG query
        """
        myXsb = pyxf.xsb("/home/vishal/Downloads/xsb/XSB/bin/xsb")
        myXsb.load(os.getcwd() + '/maze.P')
        myXsb.load(os.getcwd() + '/bfs.P')
        myXsb.load(os.getcwd() + '/corner2.P')
        q_result = myXsb.query("bfs("+str(result[0])+",X)")
        result =  q_result[0]['X']
        result = result[1:]
        result = result[:-1]
        result = result.split(',')
        
        temp = result[1:]
        temp.extend(merged_result)
        merged_result = temp

        """
        Building the XSB PROLOG query
        """
        myXsb = pyxf.xsb("/home/vishal/Downloads/xsb/XSB/bin/xsb")
        myXsb.load(os.getcwd() + '/maze.P')
        myXsb.load(os.getcwd() + '/bfs.P')
        myXsb.load(os.getcwd() + '/corner1.P')
        q_result = myXsb.query("bfs("+str(result[0])+",X)")
        result =  q_result[0]['X']
        result = result[1:]
        result = result[:-1]
        result = result.split(',')

        temp = result
        temp.extend(merged_result)
        merged_result = temp

        result = merged_result
        result.reverse()
        result = result[1:]
        result_list = list()
        result_list.append(direction_list[('start', result[0])])
        """
        Converting the list of actions returned by prolog into appropriate directions to be returned
        """
        for x in range(len(result) - 1):
            result_list.append(direction_list[(result[x], result[x + 1])])
        return result_list

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    print 'This is A*!'
    from game import Directions
    """
    A separate file consisting of heuristic values based on argument is populated for future use by the query.
    """
    f = open('astar_heuristic.P', 'w')
    sx, sy = problem.startState
    start = sx + (problem.walls.width - 2) * (problem.walls.height- 2 - sy)
    gx, gy = problem.goal
    goal = gx + (problem.walls.width - 2) * (problem.walls.height - 2 - gy)
    for x in range(problem.walls.width):
        for y in range(problem.walls.height):
            """
            Avoiding the boundary frames
            """
            if x != 0 and y != 0 and x != problem.walls.width - 1 and y != problem.walls.height - 1:
                if problem.walls[x][y] is False:
                    curr = x + (problem.walls.width - 2) * (problem.walls.height - 2 - y)
                    if curr == goal:
                        u = 'finish'
                    elif curr == start:
                        u = 'start'
                    else:
                        u = 'c' + str(curr)
                    v = ''
                    temp = 0
                    """
                    Processing the left of the node
                    """
                    if problem.walls[x - 1][y] is False:
                        temp = x - 1 + (problem.walls.width - 2) * (problem.walls.height - 2 - y)
                        if temp == goal:
                            v = 'finish'
                        elif temp == start:
                            v = 'start'
                        else:
                            v = 'c' + str(temp)
                        """
                        Adding the manhattan heuristic value to the clause file.
                        """
                        man_d = heuristic((x-1,y),problem,{})
                        f.write('manhattan_distance_heuristic(' + v + ',' + str(man_d) + ').\n')
                    """
                    Processing the right of the node
                    """
                    if problem.walls[x + 1][y] is False:
                        temp = x + 1 + (problem.walls.width - 2) * (problem.walls.height - 2 - y)
                        if temp == goal:
                            v = 'finish'
                        elif temp == start:
                            v = 'start'
                        else:
                            v = 'c' + str(temp)
                        """
                        Adding the manhattan heuristic value to the clause file.
                        """
                        man_d = heuristic((x+1,y),problem,{})
                        f.write('manhattan_distance_heuristic(' + v + ',' + str(man_d) + ').\n')
                    """
                    Processing left of the node
                    """
                    if problem.walls[x][y - 1] is False:
                        temp = x + (problem.walls.width - 2) * (problem.walls.height - 2 - (y - 1))
                        if temp == goal:
                            v = 'finish'
                        elif temp == start:
                            v = 'start'
                        else:
                            v = 'c' + str(temp)
                        """
                        Adding the manhattan heuristic value to the clause file.
                        """
                        man_d = heuristic((x,y-1),problem,{})
                        f.write('manhattan_distance_heuristic(' + v + ',' + str(man_d) + ').\n')
                    """
                    Processing right of the node
                    """
                    if problem.walls[x][y + 1] is False:
                        temp = x + (problem.walls.width - 2) * (problem.walls.height - 2 - (y + 1))
                        if temp == goal:
                            v = 'finish'
                        elif temp == start:
                            v = 'start'
                        else:
                            v = 'c' + str(temp)
                        """
                        Adding the manhattan heuristic value to the clause file.
                        """
                        man_d = heuristic((x,y+1),problem,{})
                        f.write('manhattan_distance_heuristic(' + v + ',' + str(man_d) + ').\n')

    f.close()
    from searchAgents import direction_list
    from spade import pyxf
    import os
    """
    Building the XSB PROLOG Query
    """
    myXsb = pyxf.xsb("/home/vishal/Downloads/xsb/XSB/bin/xsb")
    myXsb.load(os.getcwd() + '/maze.P')
    myXsb.load(os.getcwd() + '/astar.P')
    myXsb.load(os.getcwd() + '/astar_heuristic.P')
    q_result = myXsb.query("astar(start,X)")
    result =  q_result[0]['X']
    result = result[1:]
    result = result[:-1]
    result = result.split(',')
    result = result[1:]
    result_list = list()
    result_list.append(direction_list[('start', result[0])])
    """
    Converting the list of actions returned by prolog into appropriate directions to be returned
    """
    for x in range(len(result) - 1):
        result_list.append(direction_list[(result[x], result[x + 1])])
    return result_list


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
