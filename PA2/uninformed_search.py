
from collections import deque
from SearchSolution import SearchSolution
from MazeworldProblem import MazeworldProblem

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        # you write this part
        self.state = state
        self.parent = parent

# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions

def backChain(node, solution):
    path = []
    while node: #reversly add each node's parents to list
        path.append(node.state)
        
        node = node.parent
    path.reverse()# reverse list to get parent to child order
    solution.path = path
    return solution

def bfs_search(search_problem):
    sol = SearchSolution(search_problem, "BFS") #followed format of dfs start
    start = SearchNode(search_problem.start_state)

    visit = deque([start]) #initialize visiting list
    visited = set([start])
    sol.nodes_visited += 1
    while visit:
        node = visit.popleft() #visit front of deque and add child nodes to the list
        successors = search_problem.get_successors(node.state)
        for successor in successors:
            if successor in visited:
                continue
            sol.nodes_visited += 1
            visited.add(successor)
            child = SearchNode(successor, node)
            if search_problem.reachedGoal(successor):
                return backChain(child, sol)
            visit.append(child)
    

    return sol

# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

def checkPath(node, state):
    while node: #uses a logic similar to backChain to check if a path contains a node
        if node.state == state:
            return True
        node = node.parent
    return False

def checkDepth(node):
    d = 0
    while node: #uses a logic similar to backChain to check if a path contains a node
        d += 1
        node = node.parent
    return d

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None: 
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
    
    if checkDepth(node) >= depth_limit:
        return solution
    
    solution.nodes_visited += 1 # the nodes_visted is correctly updated in recurrse since search_problem is the same instance
    if search_problem.reachedGoal(node.state):
        return backChain(node, solution)
    
    successors = search_problem.get_successors(node.state) #if searched a whole path and do not reach goal, move to the next successor's path
    for successor in successors:
        child = SearchNode(successor, node)
        
        if checkPath(node, successor): #check if path contains child
            continue
        else:
            rst = dfs_search(search_problem, depth_limit, child, solution)# recurrsivly deepen the search, not that depth limit needs to be specified as placeholder, else solution and child will not update correctly 
            if len(rst.path) >0:
                return rst
    
    return solution

    # you write this part



def ids_search(search_problem, depth_limit=100):
    solution = SearchSolution(search_problem, "IDS")
    start = SearchNode(search_problem.start_state)
    max_depth = 0
    while max_depth < depth_limit: #iteratively increase depth limit
        #print(max_depth)
        result = dfs_search(search_problem, max_depth, start, solution)#initialize dfs using start node and IDS solution
        if len(result.path)>0:
            return result
        max_depth += 1
    return solution
    # you write this part
