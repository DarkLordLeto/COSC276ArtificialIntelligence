from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations #initialize two variables based on input
        self.start_state = (0,) + tuple(self.maze.robotloc) #robot turn& inital Pos
        self.num_robots = len(goal_locations) // 2

    def __str__(self):
        string =  "Mazeworld problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))
    
    def reachedGoal(self, state): #check if reached goal
        robot_positions = state[1:]  # get pos only
        return robot_positions == self.goal_locations
    
    def manhattan_heuristic(self, state):
        ttlDst = 0
        #state = node.sdade
        positions = state[1:]  # get pos only
        goalPos = self.goal_locations
        robotNum = self.num_robots
        for i in range(robotNum):
            x = positions[2 * i]
            y = positions[2 * i + 1]
            goal_x = goalPos[2 * i]
            goal_y = goalPos[2 * i + 1]
            ttlDst += abs(x - goal_x) + abs(y - goal_y)
    # Since robots move in turns, divide by the number of robots to get a lower-bound estimate
        return ttlDst / robotNum
    
    #check statelegal, integrated into get successor 
    '''def stateLegal(self, state): #check if state is legal 
        turn = state[0]
        positions = state[1:]
        robotNum = self.num_robots

        for i in range(robotNum): #check if robot on map
            x = positions[2 * i]
            y = positions[2 * i + 1]
            if not self.maze.is_floor(x, y):
                return False

        #positions = set()#check if two robot collde into each other
        for i in range(robotNum):
            pos = positions[2 * i], positions[2 * i + 1]
            if pos in positions:
                return False
            positions.append(pos)

        return True'''
    
    def get_successors(self, state):
        successors = []
        turn = state[0]  # The current robot's turn
        robot_positions = state[1:]  # Extract positions of robots
        num_robots = self.num_robots

        # Get the current robot's position
        robot_x = robot_positions[2 * turn]
        robot_y = robot_positions[2 * turn + 1]

        # List of possible movement directions (Stay, North, East, South, West)
        moves = [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]  # (dx, dy)

        for dx, dy in moves:
            new_x = robot_x + dx
            new_y = robot_y + dy

            # **Check if the new position is within bounds and not a wall**
            if self.maze.is_floor(new_x, new_y):
            # **Check for collisions with other robots**
                collision = False
                for i in range(num_robots):
                    if i != turn:
                        other_x = robot_positions[2 * i]
                        other_y = robot_positions[2 * i + 1]
                        if (new_x, new_y) == (other_x, other_y):
                            collision = True
                            break
                if collision:
                    continue  # Skip this move due to collision

            # Create the new state by updating the current robot's position
                new_positions = list(robot_positions)
                new_positions[2 * turn] = new_x
                new_positions[2 * turn + 1] = new_y

            # Next robot's turn (wrap around to robot 0 after the last robot)
                next_turn = (turn + 1) % num_robots
                new_state = (next_turn,) + tuple(new_positions)

            # Movement cost: 1 if the robot moves, 0 if it stays
                move_cost = 1 if (dx != 0 or dy != 0) else 0

            # Add this new state as a valid successor
                successors.append((new_state, move_cost))

        return successors





## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
