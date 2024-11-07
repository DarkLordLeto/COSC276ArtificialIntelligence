from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze):
        
        #Initializes the SensorlessProblem for a blind robot, add all floor tile to possible loc at the start
        
        self.maze = maze #any floor tile the robot can be at the start state
        self.start_state = set()
        for x in range(maze.width):
            for y in range(maze.height):
                if maze.is_floor(x, y):
                    self.start_state.add((x, y))
        self.start_state = tuple(self.start_state)

    def __str__(self):
        string =  "Blind robot problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def reachedGoal(self, belief_state):#when there's only one state possible, the blind robot reached goal state as said in the write up
        return len(belief_state) == 1
    
    def updateState(self, belief_state, action):
        newState = set() #update movements according to action
        for (x, y) in belief_state:
            if action == 'north':
                new_x, new_y = x, y + 1
            elif action == 'south':
                new_x, new_y = x, y - 1
            elif action == 'east':
                new_x, new_y = x + 1, y
            elif action == 'west':
                new_x, new_y = x - 1, y

            # Check if the new position is a valid floor position
            if self.maze.is_floor(new_x, new_y):
                newState.add((new_x, new_y))
            else:
                # If the move is blocked by a wall, the robot stays in place, so do not update to new pos
                newState.add((x, y))

        return tuple(newState)
    
    def get_successors(self, belief_state):
        #get possible successors for the four movement
        actions = ['north', 'south', 'east', 'west']
        successors = []
        
        for action in actions:
            new_belief_state = self.updateState(belief_state, action)
            move_cost = 1  # Each action has a cost of 1
            successors.append((new_belief_state, move_cost))
        
        return successors
    
    '''def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))'''
    def animate_path(self, path): #the provided animate function has a int and tuple conflict problem so I rewrite this with a renderHelper function
   
        belief_state = self.start_state

        for state in path:
            print(f"Belief state: {list(belief_state)}")
            belief_state = state
            sleep(1)  # Simulate animation with a delay
            print(self.renderHelper(belief_state))

    
    def renderHelper(self, belief_state):
        render = []
        for y in range(self.maze.height - 1, -1, -1):
            row = ""
            for x in range(self.maze.width):
                # Check if the current (x, y) is in the belief state (possible positions)
                if (x, y) in belief_state:
                    row += "R"  # R represents the possible robot locations
                else:
                    row += self.maze.map[self.maze.index(x, y)]
            render.append(row)
        return "\n".join(render)

## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
    test_maze6 = Maze("maze_test_case_6.maz")
    test_problem = SensorlessProblem(test_maze6)
    test_maze7 = Maze("maze_test_case_7.maz")
    test_problem = SensorlessProblem(test_maze7)
