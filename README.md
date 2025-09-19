# Wilson's Algorithm Maze Generator & Solver

A real-time maze generation and solving visualization using Wilson's Algorithm and multiple AI search algorithms. Features fullscreen visualization, interactive controls, and configurable maze properties.

## Features

### Maze Generation
- **Wilson's Algorithm**: Generates uniform random mazes with guaranteed connectivity
- **Real-time visualization**: Watch the maze being built step by step
- **Multiple solution modes**: Toggle between single-path and multi-path mazes
- **Configurable dimensions**: Adjustable maze width and height

### AI Search Algorithms
Four search algorithms solve the same maze simultaneously:
- **Depth-First Search (DFS)**: Stack-based exploration
- **Breadth-First Search (BFS)**: Queue-based shortest path
- **Greedy Best-First Search**: Heuristic-guided exploration
- **A* Search**: Optimal pathfinding with Manhattan distance heuristic

### Visualization
- **Fullscreen interface**: Immersive fullscreen experience
- **2x2 grid layout**: Compare all four algorithms side by side
- **Dynamic scaling**: Automatically adjusts to screen resolution
- **Real-time statistics**: Shows explored nodes and solution length
- **Color-coded visualization**: Different colors for walls, paths, explored areas, and solutions

## Files Structure

```
maze_solver/
├── main.py              # Entry point and program documentation
├── maze_generator.py    # Wilson's Algorithm implementation
├── maze_solver.py       # Search algorithms and maze data structures
├── visualizer.py        # Pygame visualization and UI management
└── README.md           # This file
```

## Configuration

Edit these variables in `visualizer.py`:

```python
MAZE_WIDTH = 41           # Maze width (odd numbers recommended)
MAZE_HEIGHT = 31          # Maze height (odd numbers recommended)  
MULTIPLE_SOLUTIONS = False # True for multi-path mazes, False for single solution
FPS = 30                  # Frame rate for smooth animation
```

## Controls

### Menu Screen
- **G** - Generate new maze
- **Q** - Quit application

### After Generation
- **S** - Start solving with all algorithms
- **G** - Generate another maze
- **Q** - Quit application

### During Solving
- **G** - Generate new maze
- **Q** - Quit application

## How to Run

### Requirements
- Python 3.7+
- Pygame library

### Installation
```bash
# Install pygame if not already installed
pip install pygame

# Run the program
python main.py
```

### Usage Flow
1. Start application → Main menu appears
2. Press **G** → Watch Wilson's Algorithm generate maze
3. Press **S** → Watch all four algorithms solve simultaneously
4. Press **G** anytime → Generate new maze to test different scenarios

## Technical Details

### Wilson's Algorithm
- Generates uniform spanning trees (perfect mazes)
- Uses loop-erased random walks
- Guarantees exactly one path between any two points (when `MULTIPLE_SOLUTIONS = False`)
- Includes connectivity verification to prevent unsolvable mazes

### Search Algorithm Comparison
- **DFS**: May not find shortest path, memory efficient
- **BFS**: Guarantees shortest path in unweighted graphs
- **Greedy**: Fast but not guaranteed optimal
- **A***: Optimal pathfinding with admissible heuristic

### Multiple Solutions Mode
When `MULTIPLE_SOLUTIONS = True`:
- Removes ~12.5% of walls to create cycles
- Enables testing whether algorithms find optimal solutions
- Useful for comparing algorithm efficiency with multiple valid paths

## Learning Objectives

This project demonstrates:
- Advanced maze generation algorithms
- Search algorithm implementation and comparison
- Real-time algorithm visualization
- State management and user interface design
- Performance analysis of different search strategies

## Customization

- Modify maze dimensions for different difficulty levels
- Toggle between single/multiple solution modes to test algorithm optimality
- Adjust frame rate for different visualization speeds
- Experiment with different heuristics in the A* implementation
