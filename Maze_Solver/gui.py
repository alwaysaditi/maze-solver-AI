import pygame
import time

class MazeGUI:
    def __init__(self, maze, solver_steps):
        self.maze = maze
        self.solver_steps = solver_steps  # The steps (generator) from the BFS/DFS solver
        self.cell_size = 20
        self.screen = pygame.display.set_mode((len(maze[0]) * self.cell_size, len(maze) * self.cell_size))

    def draw_maze(self):
        self.screen.fill((255, 255, 255))  # White background
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = (0, 0, 0) if cell == 1 else (255, 255, 255)  # Black walls, white paths
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

   
    def draw_step(self, pos, is_solution=False):
        if isinstance(pos, tuple) and len(pos) == 2:
            # Proceed if pos is a valid tuple of (x, y)
            x, y = pos
            color = (0, 255, 0) if is_solution else (0, 0, 255)  # Green for solution, Blue for exploration
            pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        else:
            print(f"Invalid step format: {pos}")  # For debugging purposes


    def run(self):
        running = True
        clock = pygame.time.Clock()

        # Draw the maze initially
        self.draw_maze()
        pygame.display.update()

        for step in self.solver_steps:
            self.draw_step(step, is_solution=(step == (len(self.maze[0])-1, len(self.maze)-1)))  # Solution path is green
            pygame.display.update()

            # Add delay to slow down the visualization
            time.sleep(0.1)  # Sleep for 100ms between each step

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return

        pygame.quit()
