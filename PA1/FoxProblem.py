class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.totalChicken = start_state[0]#num of chicken and fox
        self.totalFox = start_state[1]
        self.boat = start_state[2]
        self.goal_state = (0, 0, 0)
        self.current_state = start_state #current state, actually not used since state update is in each search

        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    def reachedGoal(self, state):
        if state == self.goal_state:
            return True
        return False
    
    def stateLegal(self, state):
        c, f, b = state
        if not (0 <= c <= self.totalChicken and 0 <= f <= self.totalFox):
            return False #test if state is legal, ie have right number of chicken and fox, fox dont eat chicken on either bank
        if (c > 0 and c < f) or (self.totalChicken - c > 0 and self.totalChicken - c < self.totalFox - f):
            return False
        return True
    # get successor states for the given state

    def get_successors(self, state):
        successors = []
        actions = [(1,0),(2,0),(0,1),(0,2),(1,1)] #actions, num of chicken removed from bank
        c,f,b = state
        for cm, fm in actions:
            if b == 1:
                nc = c - cm
                nf = f - fm
                nb = 0
            else:
                nc = c + cm
                nf = f + fm
                nb = 1

            ns = (nc, nf, nb)
            if self.stateLegal(ns):
                successors.append(ns)
        return successors
        

        # you write this part. I also had a helper function
        #  that tested if states were safe before adding to successor list

    # I also had a goal test method. You should write one.

    def __str__(self):
        string =  "Chickens and foxes problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
