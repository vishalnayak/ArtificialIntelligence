__author__ = 'vishal'
import sys
import timeit
import heapq


# Setting the recursion limit to increase the capabillity of the program to go to deeper levels
sys.setrecursionlimit(1000000)

# A list used as stack for holding fringe elements of iterative deepening search algorithm
stack = []

# A list to be supplied to a priority queue implementation to hold the fringe elements of the A* algorithm
pq = []

# Var to hold the size of one node. This is used to calculate the total memory usage of the algorithm.
sizeOfNode = 0

# Var for bookkeeping the number of nodes expanded
num_of_nodes_expanded = 0

# Var to hold the max size of the stack reached
num_of_fringe_nodes = 0

# Data structure to hold information of each node. Holds the snapshot of the state and the depth of the node
# in the search tree
class Node(object):
    # Node holding the state and depth information
    def __init__(self, depth, state):
        self.state = state
        self.parent = None
        self.depth = depth

    def __str__(self):
        return str(self.depth) + ' ' + str(self.state)


# Copies the contents of one state to another.
def copy_state(state_from, state_to):
    for i in range(7):
        for j in range(7):
            state_to[i][j] = state_from[i][j]


# Finds out all the successor states of the node passed and puts them into the fringe.
def expand_ids_node(node):
    global num_of_fringe_nodes
    """
    Expanding the node and adding the successor states to the fringe.
    For each valid location which does not contain the peg, the successor states are tried to be searched on all 4 directions.
    """
    cur_state = node.state
    count = 0
    for i in range(7):
        for j in range(7):
            if j > 1 and cur_state[i][j] == '0' and cur_state[i][j - 1] == '1' and cur_state[i][j - 2] == '1':
                # Move possible: Left to Right
                # print 'Left to Right: ' + str(i) + ' ' + str(j)
                new_state = [['0' for x in range(7)] for x in range(7)]
                copy_state(cur_state, new_state)
                new_state[i][j] = '1'
                new_state[i][j - 1] = '0'
                new_state[i][j - 2] = '0'
                new_node = Node(node.depth + 1, new_state)
                new_node.parent = node
                stack.append(new_node)
                num_of_fringe_nodes += 1
                count += 1

            if j < 5 and cur_state[i][j] == '0' and cur_state[i][j + 1] == '1' and cur_state[i][j + 2] == '1':
                # print 'Right to Left: ' + str(i) + ' ' + str(j)
                # Move possible: Right to Left
                new_state = [['0' for x in range(7)] for x in range(7)]
                copy_state(cur_state, new_state)
                new_state[i][j] = '1'
                new_state[i][j + 1] = '0'
                new_state[i][j + 2] = '0'
                new_node = Node(node.depth + 1, new_state)
                new_node.parent = node
                stack.append(new_node)
                num_of_fringe_nodes += 1
                count += 1

            if i > 1 and cur_state[i][j] == '0' and cur_state[i - 1][j] == '1' and cur_state[i - 2][j] == '1':
                # print 'Up to Down: ' + str(i) + ' ' + str(j)
                # Move possible: Up to Down
                new_state = [['0' for x in range(7)] for x in range(7)]
                copy_state(cur_state, new_state)
                new_state[i][j] = '1'
                new_state[i - 1][j] = '0'
                new_state[i - 2][j] = '0'
                new_node = Node(node.depth + 1, new_state)
                new_node.parent = node
                stack.append(new_node)
                num_of_fringe_nodes += 1
                count += 1

            if i < 5 and cur_state[i][j] == '0' and cur_state[i + 1][j] == '1' and cur_state[i + 2][j] == '1':
                # print 'Down to Up: ' + str(i) + ' ' + str(j)
                # Move possible: Down to Up
                new_state = [['0' for x in range(7)] for x in range(7)]
                copy_state(cur_state, new_state)
                new_state[i][j] = '1'
                new_state[i + 1][j] = '0'
                new_state[i + 2][j] = '0'
                new_node = Node(node.depth + 1, new_state)
                new_node.parent = node
                stack.append(new_node)
                num_of_fringe_nodes += 1
                count += 1


def is_goal(state):
    """
    The goal check. The goal state is identified by checking if the board is left with only one peg.
    """
    count = 0
    for i in range(7):
        for j in range(7):
            if '1' == state[i][j]:
                count += 1
    if 1 == count:
        return True
    else:
        return False


def recursive_dls(node, limit):
    """
    Iterative deepenning uses this method to check the node if it is containing the goal state.
    If yes, it returns it. If not, it recursively tries to search the goal state by expanding the current node.
    Also, the depth of the iteration is also controlled in this method.
    """
    global num_of_nodes_expanded
    global stack
    cutoff_occured = False
    if is_goal(node.state):
        return 'solution', node
    elif node.depth == limit:
        # print 'cutoff from ' + str(limit)
        return 'cutoff', None
    else:
        # expansion of node is done here
        expand_ids_node(node)
        num_of_nodes_expanded += 1
        if [] != stack:
            successor = stack.pop()
        else:
            successor = None
        while successor is not None:
            (result, ret_node) = recursive_dls(successor, limit)
            if result == 'cutoff':
                cutoff_occured = True
            elif result != 'fail':
                return result, ret_node
            if [] != stack:
                successor = stack.pop()
            else:
                successor = None
    if cutoff_occured:
        return 'cutoff', None
    else:
        return 'fail', None


def depth_limited_search(init_state, limit):
    """
    This method initiates the depth first search for the goal. But, it stops the search at the level specified by limit.
    """
    global sizeOfNode
    init_node = Node(0, init_state)
    # size of one node is captured here. After the object is fully populated.
    sizeOfNode = sys.getsizeof(init_node)
    result, node = recursive_dls(init_node, limit)
    return result, node


def iterative_deepening_search(init_state):
    """
    This method initiates the DFS by setting the depth limit incrementally
    """
    for i in range(20):
        result, node = depth_limited_search(init_state, i)
        if result == 'solution':
            return node


def print_solution(goal):
    """
    Prints the solution given the goal state.
    Traverses backwards using the parent pointer to reach the root
    """
    print 'Goal:'
    while goal.parent is not None:
        for i in range(7):
            for j in range(7):
                print goal.state[i][j],
            print '\n'
        print '~' * 50
        goal = goal.parent


def print_state(state):
    """
    Prints the state.
    """
    for i in range(7):
        for j in range(7):
            print state[i][j],
        print '\n'
    print '~' * 50


def main():
    """
    Reads the contents of input.txt, which contains the start state and populates
    the init_state. init_state is then passed to appropriate algorithms for solving it.
    """
    f = open('input.txt', 'r')
    i = 0
    j = 0
    init_state = [['0' for x in range(7)] for x in range(7)]
    for line in f:
        if 7 == i: continue
        j = 0
        for x in line:
            if 7 == j: continue
            init_state[i][j] = x
            j += 1
        i += 1

    print_state(init_state)

    # Iterative Deepening Search algorithm starts here.
    ids(init_state)

    # A* algorithm with heuristic-1 starts here.
    astar(init_state, 1)

    # A* algorithm with heuristic-2 starts here.
    astar(init_state, 2)


def print_stats(goal, time_taken):
    """
    Prints the statistics of the algorithm which was run before invoking this method.
    The details of the usage are updated into the global variables by the algorithm.
    Those variables are used to print the usage statistics here.
    """
    global num_of_nodes_expanded
    global sizeOfNode
    global pq
    global stack
    global num_of_fringe_nodes
    if goal is not None:
        import platform

        print 'Able to reach goal. Platform: ' + platform.system() + ' ' + platform.release()
        print 'Number of nodes expanded = ' + str(num_of_nodes_expanded)
        print 'Memory required by solution (in Bytes): (SizeOfNode=%d) * (NumOfNodesExpanded=%d) = %d' % (
            sizeOfNode, num_of_nodes_expanded, sizeOfNode * num_of_nodes_expanded)
        print 'Maximum fringe size reached (in Bytes): (SizeOfNode=%d) * (FringeTransit=%d) = %d' % (
            sizeOfNode, num_of_fringe_nodes, sizeOfNode * num_of_fringe_nodes)
        print 'Running Time = ' + str(time_taken) + ' seconds.'
        print '~' * 50
        # print_solution(goal)
    else:
        print 'Not able to reach goal'

    """
    Resetting all the variables here so that the algorithm which runs next should start afresh.
    This is not the right place for this logic. Placing it here is just for mere convenience.
    """
    num_of_nodes_expanded = 0
    sizeOfNode = 0
    num_of_fringe_nodes = 0
    # while 0 != len(pq):
    # heapq.heappop(pq)
    pq = []
    stack = []
    import gc

    gc.collect()


def ids(state):
    """
    Invoking IDS here. Time taken is cached and the stats are printed accordingly
    """
    start_time = timeit.default_timer()
    goal = iterative_deepening_search(state)
    time_taken = timeit.default_timer() - start_time
    print 'Method: Iterative Deepening Search using DFS'
    print_stats(goal, time_taken)


def astar(state, heuristic):
    """
    A* algorithm is invoked here. Time taken is cached and the stats are printed accordingly.
    """
    start_time = timeit.default_timer()
    result, node = astar_search_heuristic(state, heuristic)
    time_taken = timeit.default_timer() - start_time
    goal = None
    if 'solution' == result:
        goal = node
    print 'Method: A* with Heuristic %d' % heuristic
    print_stats(goal, time_taken)


def astar_search_heuristic(init_state, heuristic):
    """
    A* algorithm recursive procedure is invoked here.
    """
    global sizeOfNode
    init_node = Node(0, init_state)
    sizeOfNode = sys.getsizeof(init_node)
    result, node = recursive_astar_heuristic(init_node, heuristic)
    return result, node


def recursive_astar_heuristic(node, heuristic):
    """
    Recursive procedure which expands the node, picks the node with the least f(n) value.
    Note that there is no 'cutoff' logic for A*, unlike IDS.
    """
    global num_of_nodes_expanded
    global pq
    if is_goal(node.state):
        return 'solution', node
    else:
        # expansion of node is done here
        expand_astar_node_heuristic(node, heuristic)
        num_of_nodes_expanded += 1
        if 0 != len(pq):
            entry = heapq.heappop(pq)
            successor = entry[entry.keys()[0]]
        else:
            successor = None
        while successor is not None:
            (result, ret_node) = recursive_astar_heuristic(successor, heuristic)
            if result != 'fail':
                return result, ret_node
            if 0 != len(pq):
                entry = heapq.heappop(pq)
                successor = entry[entry.keys()[0]]
            else:
                successor = None
    return 'fail', None


def expand_astar_node_heuristic(node, heuristic):
    """
    Expanding the node and adding the successor states to the fringe.
    For each valid location which does not contain the peg, the successor states are tried to be searched on all 4 directions.
    The priority queue's cost function is f(n), sum of g(n) and h(n).
    g(n) is the depth of the node and h(n) is provided by the heuristic method, based on the heuristic parameter passed.
    """
    global num_of_fringe_nodes
    cur_state = node.state
    count = 0
    for i in range(7):
        for j in range(7):
            if j > 1 and cur_state[i][j] == '0' and cur_state[i][j - 1] == '1' and cur_state[i][j - 2] == '1':
                # print 'Left to Right: ' + str(i) + ' ' + str(j)
                # Move possible: Left to Right
                new_state = [['0' for x in range(7)] for x in range(7)]
                copy_state(cur_state, new_state)
                new_state[i][j] = '1'
                new_state[i][j - 1] = '0'
                new_state[i][j - 2] = '0'
                new_node = Node(node.depth + 1, new_state)
                new_node.parent = node
                g_n = new_node.depth
                h_n = get_heuristic_value(heuristic, node)
                """
                Pushing the node to the fringe using both g(n) and h(n)
                """
                heapq.heappush(pq, {g_n + h_n: new_node})
                num_of_fringe_nodes += 1
                count += 1

            if j < 5 and cur_state[i][j] == '0' and cur_state[i][j + 1] == '1' and cur_state[i][j + 2] == '1':
                # print 'Right to Left: ' + str(i) + ' ' + str(j)
                # Move possible: Right to Left
                new_state = [['0' for x in range(7)] for x in range(7)]
                copy_state(cur_state, new_state)
                new_state[i][j] = '1'
                new_state[i][j + 1] = '0'
                new_state[i][j + 2] = '0'
                new_node = Node(node.depth + 1, new_state)
                new_node.parent = node
                g_n = new_node.depth
                h_n = get_heuristic_value(heuristic, node)
                """
                Pushing the node to the fringe using both g(n) and h(n)
                """
                heapq.heappush(pq, {g_n + h_n: new_node})
                num_of_fringe_nodes += 1
                count += 1

            if i > 1 and cur_state[i][j] == '0' and cur_state[i - 1][j] == '1' and cur_state[i - 2][j] == '1':
                # print 'Up to Down: ' + str(i) + ' ' + str(j)
                # Move possible: Up to Down
                new_state = [['0' for x in range(7)] for x in range(7)]
                copy_state(cur_state, new_state)
                new_state[i][j] = '1'
                new_state[i - 1][j] = '0'
                new_state[i - 2][j] = '0'
                new_node = Node(node.depth + 1, new_state)
                new_node.parent = node
                g_n = new_node.depth
                h_n = get_heuristic_value(heuristic, node)
                """
                Pushing the node to the fringe using both g(n) and h(n)
                """
                heapq.heappush(pq, {g_n + h_n: new_node})
                num_of_fringe_nodes += 1
                count += 1

            if i < 5 and cur_state[i][j] == '0' and cur_state[i + 1][j] == '1' and cur_state[i + 2][j] == '1':
                # print 'Down to Up: ' + str(i) + ' ' + str(j)
                # Move possible: Down to Up
                new_state = [['0' for x in range(7)] for x in range(7)]
                copy_state(cur_state, new_state)
                new_state[i][j] = '1'
                new_state[i + 1][j] = '0'
                new_state[i + 2][j] = '0'
                new_node = Node(node.depth + 1, new_state)
                new_node.parent = node
                g_n = new_node.depth
                h_n = get_heuristic_value(heuristic, node)
                """
                Pushing the node to the fringe using both g(n) and h(n)
                """
                heapq.heappush(pq, {g_n + h_n: new_node})
                num_of_fringe_nodes += 1
                count += 1


def get_heuristic_value(heuristic, node):
    """
    This method calculates the h(n) value for the A* algorithm.
    Heuristic-1 h1(n): A state with maximum possible successors is chosen with higher priority.
     This is because, more the number of states more moves are possible.
     More moves means that more pegs will be removed from the state, nearing to the goal faster.
    Heuristic-2 h2(n): A state with less sparse pegs is chosen with higher priority.
     A sparse peg is the one which has no moves, either because it is in the border of the board and/or
     it has no neighbors.
    h2(n) > h1(n)
    Both h1(n) and h2(n) are admissible heuristics.
    """
    if 1 == heuristic:
        return number_of_valid_moves(node)
    elif 2 == heuristic:
        return number_of_pegs(node) - number_of_sparse_pegs(node)
    else:
        return 0


def number_of_pegs(node):
    """
    Calculates the number of pegs present in the node's state.
    """
    state = node.state
    count = 0
    for i in range(7):
        for j in range(7):
            if '1' == state[i][j]:
                count += 1
    return count


def number_of_valid_moves(node):
    """
    This is the method which calculates the Heuristic-1.
    The value determined is essentially the number of successor states that can be reached from the current state.
    """
    cur_state = node.state
    count = 0
    move = False
    for i in range(7):
        for j in range(7):
            if (j > 1 and cur_state[i][j] == '1' and cur_state[i][j - 1] == '1' and cur_state[i][j - 2] == '0') \
                    or (j < 5 and cur_state[i][j] == '1' and cur_state[i][j + 1] == '1' and cur_state[i][j + 2] == '0') \
                    or (i > 1 and cur_state[i][j] == '1' and cur_state[i - 1][j] == '1' and cur_state[i - 2][j] == '0') \
                    or (i < 5 and cur_state[i][j] == '1' and cur_state[i + 1][j] == '1' and cur_state[i + 2][j] == '0'):
                move = True
            if move:
                count += 1
            move = False
    return count


def number_of_sparse_pegs(node):
    """
    This method calculates the Heuristic-2.
    The sparse peg is the one which cannot move in all 4 directions.
    This method finds out the number of sparse pegs present in the node's state.
    """
    s = node.state
    sparse = 0
    for i in range(7):
        for j in range(7):
            # print 'checking: %d:%d' % (i,j)
            if s[i][j] == '1' and (i - 1 < 0 or '0' == s[i - 1][j]) and (j - 1 < 0 or '0' == s[i][j - 1]) and (
                                i + 1 > 5 or '0' == s[i + 1][j]) and (j + 1 > 5 or '0' == s[i][j + 1]):
                sparse += 1
                # print 'sparse: %d:%d' % (i,j)
    return sparse


def number_of_children(node):
    """"
    This method is not used in the code.
    """
    cur_state = node.state
    count = 0
    for i in range(7):
        for j in range(7):
            if j > 1 and cur_state[i][j] == '0' and cur_state[i][j - 1] == '1' and cur_state[i][j - 2] == '1':
                count += 1
            if j < 5 and cur_state[i][j] == '0' and cur_state[i][j + 1] == '1' and cur_state[i][j + 2] == '1':
                count += 1
            if i > 1 and cur_state[i][j] == '0' and cur_state[i - 1][j] == '1' and cur_state[i - 2][j] == '1':
                count += 1
            if i < 5 and cur_state[i][j] == '0' and cur_state[i + 1][j] == '1' and cur_state[i + 2][j] == '1':
                count += 1
    return count


if __name__ == '__main__':
    main()
