from collections import deque

class CSP:
    def __init__(self, variables, domains, constraints, useMRV = False, useDegree = False, useLCV = False, useAC3 = False):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.assigment = {}
        self.useMRV = useMRV
        self.useDegree = useDegree
        self.useLCV = useLCV
        self.useAC3 = useAC3

    def is_consistent(self, var, value):
        '''for neighbour, constraint in self.constraints.items():
            if var in neighbour:
                other = neighbour[1] if neighbour[0] == var else neighbour[0]
                if other in self.assigment and self.assigment[other] == value:
                    return False
        return True'''
        for (v1, v2), _ in self.constraints.items():
            if var in (v1, v2):
                neighbour = v2 if v1 == var else v1
                if neighbour in self.assigment and self.assigment[neighbour] == value:
                    return False
        return True
    
    def degree(self, var):
        count = 0
        for (v1, v2) in self.constraints:
            if var in (v1, v2):
                neighbour = v2 if v1 == var else v1
                if neighbour not in self.assigment:
                    count += 1
        return count
    
    def select_unassigned_variable(self):
        '''for var in self.variables:
            if var not in self.assigment:
                return var
        return None'''
        unassigned = [var for var in self.variables if var not in self.assigment]
        if self.useMRV:
            unassigned.sort(key=lambda var: len([value for value in self.domains[var] if self.is_consistent(var, value)]))

        if self.useDegree:
            unassigned.sort(key=lambda var: -self.degree(var))

        return unassigned[0] if unassigned else None
    
    def count_conflicts(self, var, value):
        count = 0
        for (v1, v2), constraint in self.constraints.items():
            if var in (v1, v2):
                other = v2 if v1 == var else v1
                if other not in self.assigment:
                    count += sum([1 for value2 in self.domains[other] if value2 != value])
        return count
    
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
    
    def order_values(self, var):
        if not self.useLCV:
            return self.domains[var]
        
        return sorted(self.domains[var], key=lambda value: self.count_conflicts(var, value))
    
    def backtrack(self):
        if len(self.assigment) == len(self.variables):
            return self.assigment
        
        if self.useAC3:
            if not self.ac3():
                return None
            
        var = self.select_unassigned_variable()
        for value in self.domains[var]:
            if self.is_consistent(var, value):
                self.assigment[var] = value

                original_domains = self.domains.copy()
                self.domains[var] = [value]

                result = self.backtrack()
                if result is not None:
                    return result
                
                self.domains = original_domains
                del self.assigment[var]
        return None

#this following part is test code based on the map coloring problem in textbook
variables = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
domain = {var: ['red', 'green', 'blue'] for var in variables}
constraints = {
    ('WA', 'SA'): 'WA != SA',
    ('WA', 'NT'): 'WA != NT',
    ('NT', 'SA'): 'NT != SA',
    ('NT', 'Q'): 'NT != Q',
    ('Q', 'SA'): 'Q != SA',
    ('Q', 'NSW'): 'Q != NSW',
    ('NSW', 'SA'): 'NSW != SA',
    ('NSW', 'V'): 'NSW != V',
    ('V', 'SA'): 'V != SA'
}

# Create the CSP instance
csp = CSP(variables, domain, constraints, useMRV=False, useDegree=False, useLCV=False, useAC3=False)

# Solve the CSP
solution = csp.backtrack()
print("Solution:", solution)