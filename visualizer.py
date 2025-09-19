# visualizer.py

import pygame
from maze_generator import MazeGenerator
from maze_solver import Maze, StackFrontier, QueueFrontier, GreedyBestFirstFrontier, AStarFrontier

# Maze configuration
MAZE_WIDTH = 41
MAZE_HEIGHT = 31
MARGIN = 10
FPS = 30

# UI States
STATE_MENU = "menu"
STATE_GENERATING = "generating"  
STATE_READY_TO_SOLVE = "ready_to_solve"
STATE_SOLVING = "solving"
STATE_SOLVED = "solved"

# Colors
WALL_COLOR = (40, 40, 40)
START_COLOR = (255, 0, 0)
GOAL_COLOR = (0, 171, 28)
EXPLORED_COLOR = (212, 97, 85)
SOLUTION_COLOR = (220, 235, 113)
EMPTY_COLOR = (237, 240, 252)
GENERATION_COLOR = (100, 100, 255)
WALK_COLOR = (255, 255, 0)

class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h

        # Dynamic cell size and quadrant dimensions
        self.quadrant_width = self.screen_width // 2 - 2 * MARGIN
        self.quadrant_height = (self.screen_height - 60) // 2 - 2 * MARGIN
        self.cell_size = min(self.quadrant_width // MAZE_WIDTH, self.quadrant_height // MAZE_HEIGHT)

        # Dynamic fonts
        title_font_size = max(16, self.screen_width // 80)
        stats_font_size = max(12, self.screen_width // 100)
        menu_font_size = max(24, self.screen_width // 60)
        self.title_font = pygame.font.SysFont("Arial", title_font_size, bold=True)
        self.stats_font = pygame.font.SysFont("Arial", stats_font_size, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", menu_font_size, bold=True)

        self.clock = pygame.time.Clock()
        self.mazes = [Maze() for _ in range(4)]
        self.titles = ["DFS", "BFS", "Greedy Best-First", "A* Search"]
        self.generators = None
        
        # State management
        self.state = STATE_MENU
        self.maze_data = None
        self.multiple_solutions = False  # Toggle-able setting
        self.all_solved = False  # Track if all algorithms are done

    def draw_menu(self):
        """Draw the main menu screen"""
        self.screen.fill((0, 0, 0))
        
        # Title
        title_text = self.menu_font.render("Wilson's Algorithm Maze Generator & Solver", True, (255, 255, 255))
        title_x = (self.screen_width - title_text.get_width()) // 2
        self.screen.blit(title_text, (title_x, self.screen_height // 4))
        
        # Configuration display
        config_lines = [
            f"Maze Size: {MAZE_WIDTH} x {MAZE_HEIGHT}",
            f"Multiple Solutions: {'Enabled' if self.multiple_solutions else 'Disabled (Single Solution)'}",
            "",
            "Controls:",
            "G - Generate New Maze",
            "M - Toggle Multiple Solutions",
            "Q - Quit",
            "During/After solving:",
            "R - Return to Menu"
        ]
        
        y_offset = self.screen_height // 2 - 150
        for line in config_lines:
            if line:
                color = (200, 200, 200)
                if line.startswith(("G -", "M -", "S -", "R -", "Q -")):
                    color = (255, 255, 100)
                elif "Multiple Solutions:" in line:
                    color = (0, 255, 0) if self.multiple_solutions else (255, 100, 100)
                
                text = self.title_font.render(line, True, color)
                text_x = (self.screen_width - text.get_width()) // 2
                self.screen.blit(text, (text_x, y_offset))
            y_offset += 30

    def draw_solved_screen(self):
        """Draw the screen when all algorithms have finished"""
        self.screen.fill((0, 0, 0))
        
        # Show completed maze with all solutions
        for i, (maze, gen, title) in enumerate(zip(self.mazes, self.generators, self.titles)):
            col = i % 2
            row = i // 2

            maze_pixel_width = maze.width * self.cell_size
            maze_pixel_height = maze.height * self.cell_size

            offset_x = col * self.screen_width // 2 + (self.quadrant_width - maze_pixel_width) // 2
            offset_y = row * self.screen_height // 2 + (self.quadrant_height - maze_pixel_height) // 2

            self.draw_maze_solving(maze, offset_x, offset_y, title)

        # Completion message
        complete_text = self.menu_font.render("All Algorithms Completed!", True, (0, 255, 0))
        complete_x = (self.screen_width - complete_text.get_width()) // 2
        self.screen.blit(complete_text, (complete_x, self.screen_height - 120))
        
        # Mode display
        mode_text = f"Mode: {'Multiple Solutions' if self.multiple_solutions else 'Single Solution'}"
        mode_surface = self.title_font.render(mode_text, True, (255, 255, 0))
        mode_x = (self.screen_width - mode_surface.get_width()) // 2
        self.screen.blit(mode_surface, (mode_x, self.screen_height - 90))
        
        # Instructions
        controls_text1 = self.title_font.render("Press R to return to menu", True, (255, 255, 255))
        controls_text2 = self.title_font.render("Press Q to quit", True, (255, 255, 255))
        controls_x = (self.screen_width - controls_text1.get_width()) // 2
        self.screen.blit(controls_text1, (controls_x, self.screen_height - 60))
        self.screen.blit(controls_text2, (controls_x, self.screen_height - 30))

    def draw_ready_screen(self):
        """Draw the ready to solve screen"""
        self.screen.fill((0, 0, 0))
        
        # Show the generated maze in center
        if self.maze_data:
            maze_width = len(self.maze_data[0]) * self.cell_size
            maze_height = len(self.maze_data) * self.cell_size
            offset_x = (self.screen_width - maze_width) // 2
            offset_y = (self.screen_height - maze_height) // 2 - 50
            
            for i in range(len(self.maze_data)):
                for j in range(len(self.maze_data[0])):
                    self.draw_generation_cell(self.maze_data, i, j, offset_x, offset_y, "complete", None)
        
        # Instructions
        ready_text = self.menu_font.render("Maze Generation Complete!", True, (0, 255, 0))
        ready_x = (self.screen_width - ready_text.get_width()) // 2
        self.screen.blit(ready_text, (ready_x, self.screen_height - 150))
        
        controls_text = self.title_font.render("Press S to start solving, G to generate new maze, Q to quit", True, (255, 255, 255))
        controls_x = (self.screen_width - controls_text.get_width()) // 2
        self.screen.blit(controls_text, (controls_x, self.screen_height - 100))

    def draw_generation_cell(self, maze_data, row, col, offset_x, offset_y, status, extra_data):
        x = offset_x + col * self.cell_size
        y = offset_y + row * self.cell_size
        cell = maze_data[row][col]

        if cell == '#':
            color = WALL_COLOR
        elif cell == 'A':
            color = START_COLOR
        elif cell == 'B':
            color = GOAL_COLOR
        elif cell == ' ':
            color = WALK_COLOR if status == "walking" and extra_data and (row, col) in extra_data else EMPTY_COLOR
        else:
            color = WALL_COLOR

        pygame.draw.rect(self.screen, color, (x, y, self.cell_size - 1, self.cell_size - 1))

    def draw_solving_cell(self, maze, row, col, offset_x, offset_y):
        x = offset_x + col * self.cell_size
        y = offset_y + row * self.cell_size

        if maze.walls[row][col]:
            color = WALL_COLOR
        elif (row, col) == maze.start:
            color = START_COLOR
        elif (row, col) == maze.goal:
            color = GOAL_COLOR
        elif maze.solution and (row, col) in maze.solution[1]:
            color = SOLUTION_COLOR
        elif (row, col) in maze.explored:
            color = EXPLORED_COLOR
        else:
            color = EMPTY_COLOR

        pygame.draw.rect(self.screen, color, (x, y, self.cell_size - 1, self.cell_size - 1))

    def draw_maze_generation(self, maze_data, status, extra_data):
        maze_width = len(maze_data[0]) * self.cell_size
        maze_height = len(maze_data) * self.cell_size
        offset_x = (self.screen_width - maze_width) // 2
        offset_y = (self.screen_height - maze_height) // 2

        for i in range(len(maze_data)):
            for j in range(len(maze_data[0])):
                self.draw_generation_cell(maze_data, i, j, offset_x, offset_y, status, extra_data)

        status_text = f"Generating maze using Wilson's Algorithm... Status: {status}"
        text = self.title_font.render(status_text, True, (255, 255, 255))
        text_x = (self.screen_width - text.get_width()) // 2
        self.screen.blit(text, (text_x, 20))

        inst_text = self.stats_font.render("Press Q to quit during generation", True, (200, 200, 200))
        inst_x = (self.screen_width - inst_text.get_width()) // 2
        self.screen.blit(inst_text, (inst_x, 50))

    def draw_maze_solving(self, maze, offset_x, offset_y, title):
        for i in range(maze.height):
            for j in range(maze.width):
                self.draw_solving_cell(maze, i, j, offset_x, offset_y)

        title_text = self.title_font.render(title, True, (255, 255, 255))
        stats = f"Explored: {len(maze.explored)}, Solution: {len(maze.solution[1])}" if maze.solution else f"Explored: {len(maze.explored)}"
        stats_text = self.stats_font.render(stats, True, (200, 200, 200))

        self.screen.blit(title_text, (offset_x + 5, offset_y + maze.height * self.cell_size + 5))
        self.screen.blit(stats_text, (offset_x + 5, offset_y + maze.height * self.cell_size + 25))

    def generate_maze(self):
        generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT, self.multiple_solutions)
        gen = generator.wilson_algorithm_generator()

        for maze_data, status, extra_data in gen:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            self.draw_maze_generation(maze_data, status, extra_data)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    return None

            pygame.display.flip()

        return generator.maze

    def initialize_mazes(self, maze_data):
        for maze in self.mazes:
            maze._init_from_data(maze_data)

        frontiers = [
            StackFrontier(),
            QueueFrontier(),
            GreedyBestFirstFrontier(self.mazes[2].goal),
            AStarFrontier(self.mazes[3].goal)
        ]

        self.generators = [maze.solve_generator(frontier) for maze, frontier in zip(self.mazes, frontiers)]

    def run(self):
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_m:
                        # Toggle multiple solutions (only in menu)
                        if self.state == STATE_MENU:
                            self.multiple_solutions = not self.multiple_solutions
                            print(f"Multiple solutions: {'Enabled' if self.multiple_solutions else 'Disabled'}")
                    elif event.key == pygame.K_g:
                        if self.state in [STATE_MENU, STATE_READY_TO_SOLVE]:
                            self.state = STATE_GENERATING
                            print("Starting maze generation...")
                            self.maze_data = self.generate_maze()
                            if self.maze_data:
                                self.state = STATE_READY_TO_SOLVE
                                print("Maze generation complete! Press S to solve or G for new maze.")
                            else:
                                self.state = STATE_MENU
                    elif event.key == pygame.K_s:
                        if self.state == STATE_READY_TO_SOLVE and self.maze_data:
                            print("Starting solving phase...")
                            self.initialize_mazes(self.maze_data)
                            self.state = STATE_SOLVING
                            self.all_solved = False
                    elif event.key == pygame.K_r:
                        # Return to menu (from solved state or during solving)
                        if self.state in [STATE_SOLVING, STATE_SOLVED]:
                            self.state = STATE_MENU
                            self.maze_data = None
                            self.all_solved = False
                            print("Returned to main menu")
            
            # Draw based on current state
            if self.state == STATE_MENU:
                self.draw_menu()
            elif self.state == STATE_READY_TO_SOLVE:
                self.draw_ready_screen()
            elif self.state == STATE_SOLVING:
                self.screen.fill((0, 0, 0))
                
                solved_count = 0
                
                for i, (maze, gen, title) in enumerate(zip(self.mazes, self.generators, self.titles)):
                    col = i % 2
                    row = i // 2

                    maze_pixel_width = maze.width * self.cell_size
                    maze_pixel_height = maze.height * self.cell_size

                    offset_x = col * self.screen_width // 2 + (self.quadrant_width - maze_pixel_width) // 2
                    offset_y = row * self.screen_height // 2 + (self.quadrant_height - maze_pixel_height) // 2

                    try:
                        status, state = next(gen)
                        if status == "exploring":
                            maze.explored.add(state)
                    except StopIteration:
                        solved_count += 1

                    self.draw_maze_solving(maze, offset_x, offset_y, title)

                # Check if all algorithms are done
                if solved_count == 4 and not self.all_solved:
                    self.all_solved = True
                    self.state = STATE_SOLVED
                    print("All algorithms completed! Press R to return to menu.")

                # Instructions for solving phase
                mode_text = f"Mode: {'Multiple Solutions' if self.multiple_solutions else 'Single Solution'}"
                mode_surface = self.stats_font.render(mode_text, True, (255, 255, 0))
                self.screen.blit(mode_surface, (10, 10))
                
                inst_text = self.stats_font.render("Press R to return to menu, Q to quit", True, (200, 200, 200))
                self.screen.blit(inst_text, (10, 35))
            
            elif self.state == STATE_SOLVED:
                self.draw_solved_screen()
            
            # Note: STATE_GENERATING is handled by the generate_maze method
            
            pygame.display.flip()

        pygame.quit()