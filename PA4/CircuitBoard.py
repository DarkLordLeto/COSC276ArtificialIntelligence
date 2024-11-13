from collections import deque

class BoardCSP:
    def __init__(self, boardWidth, boardHeight, components, useAC3 = False):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.components = components
        self.assignment = {}
        self.useAC3 = useAC3
        self.variables = list(components.keys())
        self.constraints = self.generate_constraints()
        self.domains = self.generate_domains()
        
    def generate_constraints(self):
        constraints = {}
        for i in range(len(self.variables)):
            for j in range(i + 1, len(self.variables)):
                constraints[(self.variables[i], self.variables[j])] = 'non_overlap'
        return constraints
    
    def generate_domains(self):
        domains = {}
        for component, (width, height) in self.components.items():
            domains[component] = []
            for x in range(self.boardWidth - width + 1):
                for y in range(self.boardHeight - height + 1):
                    domains[component].append((x, y))
        return domains
    
    def non_overlap(self, component1, postion1, component2, postion2):
        x1, y1 = postion1
        x2, y2 = postion2
        w1, h1 = self.components[component1]
        w2, h2 = self.components[component2]
        return not (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)
    
    def is_consistent(self, component, position):
        for (c1, c2), constraint in self.constraints.items():
            if constraint == 'non_overlap' and component in (c1, c2):
                other = c2 if c1 == component else c1
                if other in self.assignment and not self.non_overlap(component, position, other, self.assignment[other]):
                    return False
        return True
    
    def ac3(self):
        queue = deque([(var1, var2) for (var1, var2) in self.constraints])
        while queue:
            xi, xj = queue.popleft()
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for (var1, var2) in self.constraints:
                    if var1 == xi and var2 != xj:
                        queue.append((var2, var1))
                    elif var2 == xi and var1 != xj:
                        queue.append((var1, var2))
        return True
    
    def revise(self, xi, xj):
        revised = False
        for value1 in self.domains[xi][:]:
            if not any(value1 != value2 for value2 in self.domains[xj]):
                self.domains[xi].remove(value1)
                revised = True
        return revised
    
    def backtrack(self):
        if len(self.assignment) == len(self.variables):
            return self.assignment
        
        if self.useAC3:
            if not self.ac3():
                return None
            
        var = self.select_unassigned_variable()
        for value in self.domains[var]:
            if self.is_consistent(var, value):
                self.assignment[var] = value

                original_domains = self.domains.copy()
                self.domains[var] = [value]

                result = self.backtrack()
                if result is not None:
                    return result
                
                self.domains = original_domains
                del self.assignment[var]
        return None
    
    def select_unassigned_variable(self):
        for var in self.variables:
            if var not in self.assignment:
                return var
        return None
    
    def display(self):
        board = [[' ' for _ in range(self.boardWidth)] for _ in range(self.boardHeight)]
        for component, (x, y) in self.assignment.items():
            w, h = self.components[component]
            for i in range(h):
                for j in range(w):
                    board[y + i][x + j] = component
        for row in reversed(board):
            print(' '.join(row))

board_width = 10
board_height = 3
components = {
    'a': (3, 2),  # component 'a' is 3x2
    'b': (5, 2),  # component 'b' is 5x1
    'c': (2, 3),  # component 'c' is 2x3
    'e': (7, 1)   # component 'e' is 7x1
}

# Create the CSP instance for the circuit board problem
csp = BoardCSP(board_width, board_height, components, useAC3=True)

# Solve the CSP
solution = csp.backtrack()

# Display the solution
if solution:
    print("Solution found:")
    csp.display()
else:
    print("No solution found.")