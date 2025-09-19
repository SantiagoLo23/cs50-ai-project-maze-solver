# maze_generator.py

import random
from collections import deque

class MazeGenerator:
    def __init__(self, width, height, multiple_solutions=False):
        # Ensure odd dimensions for proper maze structure
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.multiple_solutions = multiple_solutions
        self.maze = None

    def wilson_algorithm_generator(self):
        """Generator that yields maze states during Wilson's algorithm execution"""
        maze = [['#' for _ in range(self.width)] for _ in range(self.height)]
        in_maze = set()
        start_cell = (1, 1)
        maze[start_cell[0]][start_cell[1]] = ' '
        in_maze.add(start_cell)
        yield maze, "initial", start_cell

        all_cells = [(r, c) for r in range(1, self.height, 2)
                     for c in range(1, self.width, 2)]
        remaining_cells = [cell for cell in all_cells if cell not in in_maze]

        while remaining_cells:
            current = random.choice(remaining_cells)
            path = [current]
            yield maze, "walk_start", current

            steps = 0
            max_steps = 1000

            while current not in in_maze and steps < max_steps:
                steps += 1
                neighbors = []
                for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                    nr, nc = current[0] + dr, current[1] + dc
                    if 1 <= nr < self.height - 1 and 1 <= nc < self.width - 1:
                        neighbors.append((nr, nc))

                if not neighbors:
                    break

                next_cell = random.choice(neighbors)
                if next_cell in path:
                    loop_start = path.index(next_cell)
                    path = path[:loop_start + 1]
                else:
                    path.append(next_cell)

                current = next_cell
                yield maze, "walking", path.copy()

            # Connect the entire path to the existing maze
            for i in range(len(path)):
                r, c = path[i]
                maze[r][c] = ' '
                in_maze.add((r, c))
                
                # Connect to next cell in path
                if i < len(path) - 1:
                    r1, c1 = path[i]
                    r2, c2 = path[i + 1]
                    wall_r = (r1 + r2) // 2
                    wall_c = (c1 + c2) // 2
                    maze[wall_r][wall_c] = ' '
                
                yield maze, "adding_path", (r, c)

            remaining_cells = [cell for cell in all_cells if cell not in in_maze]
            yield maze, "path_complete", None

        # Add start
        maze[1][1] = 'A'

        # Safe goal placement with connectivity verification
        goal_placed = self.place_connected_goal(maze)
        
        if not goal_placed:
            # Fallback: place goal at furthest reachable point from start
            furthest_cell = self.find_furthest_cell(maze, (1, 1))
            if furthest_cell and furthest_cell != (1, 1):
                maze[furthest_cell[0]][furthest_cell[1]] = 'B'

        # Add multiple solutions if requested
        if self.multiple_solutions:
            self.add_multiple_paths(maze)

        self.maze = maze
        yield maze, "complete", None
    
    def place_connected_goal(self, maze):
        """Place goal ensuring it's connected to start using BFS verification"""
        start_pos = (1, 1)
        
        # Get all reachable positions from start
        reachable = self.get_reachable_positions(maze, start_pos)
        
        # Try to place goal in bottom-right area first
        for r in range(self.height - 2, 0, -2):
            for c in range(self.width - 2, 0, -2):
                if (r, c) in reachable and (r, c) != start_pos:
                    maze[r][c] = 'B'
                    return True
        
        # Try any reachable position
        for r in range(self.height - 2, 0, -1):
            for c in range(self.width - 2, 0, -1):
                if (r, c) in reachable and (r, c) != start_pos:
                    maze[r][c] = 'B'
                    return True
        
        return False

    def get_reachable_positions(self, maze, start):
        """Get all positions reachable from start using BFS"""
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < self.height and 0 <= nc < self.width and 
                    (nr, nc) not in visited and maze[nr][nc] != '#'):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        return visited

    def find_furthest_cell(self, maze, start):
        """Find the cell furthest from start using BFS"""
        visited = set()
        queue = deque([(start, 0)])  # (position, distance)
        visited.add(start)
        furthest_cell = start
        max_distance = 0
        
        while queue:
            (r, c), distance = queue.popleft()
            
            if distance > max_distance:
                max_distance = distance
                furthest_cell = (r, c)
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < self.height and 0 <= nc < self.width and 
                    (nr, nc) not in visited and maze[nr][nc] != '#'):
                    visited.add((nr, nc))
                    queue.append(((nr, nc), distance + 1))
        
        return furthest_cell

    def add_multiple_paths(self, maze):
        """Add additional connections to create multiple solution paths"""
        # Find some walls between open spaces and randomly remove some
        walls_to_remove = []
        
        for r in range(2, self.height - 1, 2):
            for c in range(1, self.width - 1, 2):
                # Horizontal wall
                if (maze[r-1][c] == ' ' and maze[r+1][c] == ' ' and 
                    maze[r][c] == '#'):
                    walls_to_remove.append((r, c))
        
        for r in range(1, self.height - 1, 2):
            for c in range(2, self.width - 1, 2):
                # Vertical wall  
                if (maze[r][c-1] == ' ' and maze[r][c+1] == ' ' and 
                    maze[r][c] == '#'):
                    walls_to_remove.append((r, c))
        
        # Remove 10-20% of possible walls to create cycles
        num_to_remove = len(walls_to_remove) // 8  # Remove about 12.5%
        if num_to_remove > 0:
            walls_to_remove = random.sample(walls_to_remove, num_to_remove)
            for r, c in walls_to_remove:
                maze[r][c] = ' '