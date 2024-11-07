# You write this:
from SensorlessProblem import SensorlessProblem
from astar_search import astar_search
from Maze import Maze

def blind_heuristic( belief_state):
    return len(belief_state) #use length of possible state as heuristic


def test_blind_robot(maze_filename):
    # Load the maze
    maze = Maze(maze_filename)
    
    # Create the SensorlessProblem instance
    problem = SensorlessProblem(maze)
    
    # Run A* search
    solution = astar_search(problem, blind_heuristic)
    
    # Check the result
    if solution.path:
        print(f"Solution found in {len(solution.path)} steps.")
        for step in solution.path:
            print(step)
        # Animate the path
        problem.animate_path(solution.path)
    else:
        print("No solution found.")

if __name__ == "__main__":
    # Test the blind robot problem on a maze
    test_blind_robot("maze3.maz")
    test_blind_robot("maze_test_case_6.maz")
    test_blind_robot("maze_test_case_7.maz")