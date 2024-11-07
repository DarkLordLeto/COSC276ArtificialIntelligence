from SearchSolution import SearchSolution
from heapq import heappush, heappop
#my implementation of A* search refers to the sudo code in https://www.geeksforgeeks.org/a-search-algorithm/
class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        # you write this part
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost#initiallize each varible from input

        self.ttlCst = parent.ttlCst + transition_cost if parent else transition_cost #calculate total cumulative cost

    def priority(self):
        # you write this part
        return self.ttlCst + self.heuristic 

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    while pqueue:
        current = heappop(pqueue) #get least piority
        currentState = current.state
        solution.nodes_visited += 1#update visted

        if search_problem.reachedGoal(current.state): #check if reached goal
            solution.path = backchain(current)
            solution.cost = current.ttlCst
            return solution
        
        for successor, transition_cost in search_problem.get_successors(currentState):
            updatedCost = current.ttlCst + transition_cost

            # If the successor is unvisited or has a lower cost, update it
            if successor not in visited_cost or updatedCost < visited_cost[successor]:
                visited_cost[successor] = updatedCost
                heuristic = heuristic_fn(successor)
                successor_node = AstarNode(successor, heuristic, current, transition_cost)
                heappush(pqueue, successor_node)

    # If no solution is found
    return solution


    # you write the rest:
