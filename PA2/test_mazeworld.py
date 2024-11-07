from MazeworldProblem import MazeworldProblem
from Maze import Maze
import random

from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0



# Test problems

test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# this should do a bit better:
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

# Your additional tests here:
#note that for this part I used Chatgpt to give me maze design ideas and also format to store output
def generate_random_maze(width, height, wall_prob=0.2):
    maze_lines = []
    for y in range(height):
        line = ''
        for x in range(width):
            if random.random() < wall_prob:
                line += '#'
            else:
                line += '.'
        maze_lines.append(line)
    return maze_lines

def write_maze_to_file(filename, maze_lines, robot_positions):
    with open(filename, 'w') as f:
        # Write the maze lines
        for line in maze_lines:
            f.write(line + '\n')
        # Write robot positions
        for robot in robot_positions:
            f.write(f'\\robot {robot[0]} {robot[1]}\n')

def test_case_1(): #test smallest maze
    maze_lines = [
        '. . . . .',
        '. # . . .',
        '. # # . .',
        '. . . . .',
        '. . . . .'
    ]
    # Replace spaces with no spaces
    maze_lines = [line.replace(' ', '') for line in maze_lines]
    robot_positions = [(0, 0)]  # A at (0, 0)
    goal_positions = (4, 4)     # Goal at (4, 4)
    filename = 'maze_test_case_1.maz'
    write_maze_to_file(filename, maze_lines, robot_positions)
    return filename, goal_positions

def test_case_2(): #test increase in maze size
    maze_lines = [
        '. . . . . . . . . .',
        '. . . . . # . . . .',
        '. . . . # # . . . .',
        '. . . # # # . . . .',
        '. . # # # # . . . .',
        '. . # # # # . . . .',
        '. . . . . . . . . .',
        '. . . . . . . . . .',
        '. . . . . . . . . .',
        '. . . . . . . . . .'
    ]
    maze_lines = [line.replace(' ', '') for line in maze_lines]
    robot_positions = [(0, 0), (1, 0)]  # A at (0, 0), B at (1, 0)
    goal_positions = (9, 9, 8, 9)       # A to (9, 9), B to (8, 9)
    filename = 'maze_test_case_2.maz'
    write_maze_to_file(filename, maze_lines, robot_positions)
    return filename, goal_positions

def test_case_3(): #test random maze function
    width, height = 20, 20
    wall_prob = 0.7  # Increase wall probability for complexity, this might generate invalid maze or take extremely long running time
    maze_lines = generate_random_maze(width, height, wall_prob)
    robot_positions = [(0, 0), (1, 0), (2, 0)]  # A at (0,0), B at (1,0), C at (2,0)
    goal_positions = (9, 9, 8, 9, 7, 9)   # Goals for A, B, C
    filename = 'maze_test_case_3.maz'
    write_maze_to_file(filename, maze_lines, robot_positions)
    return filename, goal_positions

def test_case_4(): #test largest maze
    width, height = 40, 40
    wall_prob = 0.2
    maze_lines = generate_random_maze(width, height, wall_prob)
    robot_positions = [(0, 0)]   # A at (0, 0)
    goal_positions = (39, 39)    # Goal at (39, 39)
    filename = 'maze_test_case_4.maz'
    write_maze_to_file(filename, maze_lines, robot_positions)
    return filename, goal_positions

def test_case_5(): #in a limited space maze and A and B need to Switch Place
    maze_lines = [
        '. . # # #',
        '. . # # #',
        '. . # # #',
        '. . # # #',
        '. . # # #'
    ]
    maze_lines = [line.replace(' ', '') for line in maze_lines]
    robot_positions = [(0, 1), (1, 1)]  # A at (0,1), B at (1,1)
    goal_positions = (1, 1, 0, 1)       # A to (1,1), B to (0,1)
    filename = 'maze_test_case_5.maz'
    write_maze_to_file(filename, maze_lines, robot_positions)
    return filename, goal_positions

def run_test_case(test_case_function, test_case_number):
    filename, goal_positions = test_case_function()
    maze = Maze(filename)
    problem = MazeworldProblem(maze, goal_positions)
    heuristic_fn = lambda state: problem.manhattan_heuristic(state)
    solution = astar_search(problem, heuristic_fn)
    
    # Save output to a file
    output_filename = f'test_case_{test_case_number}_output.txt'
    with open(output_filename, 'w') as f:
        f.write(f'--- Test Case {test_case_number} ---\n')
        f.write(str(solution) + '\n')
        if solution.path:
            f.write('Path:\n')
            for state in solution.path:
                f.write(str(state) + '\n')
        else:
            f.write('No path found.\n')
    print(f'Test Case {test_case_number} completed. Output saved to {output_filename}')

if __name__ == "__main__":
    test_cases = [
        (test_case_1, 1),
        (test_case_2, 2),
        (test_case_3, 3),
        (test_case_4, 4),
        (test_case_5, 5)
    ]
    
    for test_case_func, test_case_number in test_cases:
        run_test_case(test_case_func, test_case_number)
