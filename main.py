# main.py

from visualizer import Visualizer

def main():
    """
    Wilson's Algorithm Maze Generator and Solver
    
    This program:
    1. Shows a menu to generate mazes using Wilson's Algorithm (visualized)
    2. Allows manual control over when to start solving
    3. Solves the same maze using 4 different algorithms simultaneously:
       - Depth-First Search (DFS)
       - Breadth-First Search (BFS) 
       - Greedy Best-First Search
       - A* Search
    
    Configuration:
    - To change maze size, edit MAZE_WIDTH and MAZE_HEIGHT in visualizer.py
    - Toggle multiple solutions using M key in the menu
    - Odd numbers work best for maze dimensions (ensures proper maze structure)
    
    Controls:
    - Menu: G to generate maze, M to toggle solutions, Q to quit
    - After generation: S to start solving, G for new maze, Q to quit
    - During/After solving: R to return to menu, Q to quit
    
    Features:
    - Real-time Wilson's algorithm visualization
    - All four algorithms displayed in a 2x2 grid
    - Fullscreen interface with automatic scaling
    - Statistics display for each algorithm
    - Guaranteed maze connectivity (no unsolvable mazes)
    - Optional multiple solution paths for algorithm comparison
    """
    
    print("="*60)
    print("WILSON'S ALGORITHM MAZE GENERATOR AND SOLVER")
    print("="*60)
    print("Starting fullscreen interface...")
    print("Controls:")
    print("  Menu: G = Generate maze, M = Toggle solutions, Q = Quit")
    print("  After generation: S = Solve, G = New maze, Q = Quit")
    print("  During/After solving: R = Return to menu, Q = Quit")
    print("="*60)
    
    visualizer = Visualizer()
    visualizer.run()
    
    print("Program completed. Thank you for using the maze solver!")

if __name__ == "__main__":
    main()