import numpy as np
import time
import tracemalloc
import csv
import pygame
from maze_generator import MazeGenerator 

class ValueIterationSolver:
    #this function initializes all our parameters for running the value iteration algorithm for a particular instance.
    def __init__(self, maze, rewards=None, discount_factor=0.9, threshold=1e-4, move_prob=0.8):
        self.maze = np.array(maze)
        self.rows, self.cols = self.maze.shape
        self.discount_factor = discount_factor
        self.threshold = threshold
        self.move_prob = move_prob
        
        self.rewards = rewards if rewards else self._initialize_rewards()
        self.values = np.zeros((self.rows, self.cols))
        self.policy = np.full((self.rows, self.cols), None)
        
        self.directions = { #four possible permitted directions: left, down, right, up
            'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)
        }
        
        self.side_moves = { #this has been done to introduce stochasticity. for any potential direction of movement, the movement can drift left or right of the intended direction with a small probability.
            'U': ['L', 'R'], 'D': ['L', 'R'],
            'L': ['U', 'D'], 'R': ['U', 'D']
        }

    def _initialize_rewards(self): #this function initializes the rewards for the value iteration instance
        rewards = np.full((self.rows, self.cols), -0.1) #living reward is -0.1 to discourage the agent from lingering in the maze for long
        rewards[self.maze == 1] = -100  # Walls have high negative reward
        rewards[self.rows-1, self.cols-1] = 100  # Goal has high positive reward
        return rewards

    def _get_possible_moves(self, row, col):
        moves = {}
        for action, (dr, dc) in self.directions.items():
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.maze[nr, nc] != 1:
                moves[action] = (nr, nc)
        return moves

    def value_iteration(self):
        iterations = 0
        while True:
            delta = 0
            new_values = np.copy(self.values)  # To update values in parallel
            iterations += 1
            
            for row in range(self.rows): #we update the value of each cell (or state)
                for col in range(self.cols):
                    if (row, col) == (self.rows-1, self.cols-1) or self.maze[row, col] == 1: #if the cell is a goal or wall we skip updating it's value
                        continue  
                    
                    best_value = float('-inf')
                    best_action = None
                    
                    possible_moves = self._get_possible_moves(row, col)
                    
                    for action, (nr, nc) in possible_moves.items():
                        value = self.move_prob * (self.rewards[nr, nc] + self.discount_factor * self.values[nr, nc]) #this update is performed according to bellman equation
                        
                        side_actions = self.side_moves[action]  # Get left and right moves
                        side_prob = (1 - self.move_prob) / 2  # Probability split
                        
                        for side_action in side_actions: #adding up the porbability for the intended move along with the probability for the side moves.
                            if side_action in possible_moves:
                                sr, sc = possible_moves[side_action]
                                value += side_prob * (self.rewards[sr, sc] + self.discount_factor * self.values[sr, sc])
                            else:
                                value += side_prob * (self.rewards[row, col] + self.discount_factor * self.values[row, col])
                        
                        if value > best_value: #updating the value of a state if a better value is found
                            best_value = value
                            best_action = action
                    
                    new_values[row, col] = best_value
                    self.policy[row, col] = best_action
                    
                    delta = max(delta, abs(self.values[row, col] - best_value))

            self.values = new_values  # Update values in one go
            
            if delta < self.threshold:  # checking for convergence
                break
        
        return iterations
    
    def get_optimal_path(self): #after the optimal values have been found for all states, this prints the path considering the optimal values
        path = []
        row, col = 0, 0
        path.append((0,0))
      
        while (row, col) != (self.rows-1, self.cols-1):
            action = self.policy[row, col]
            
            if action is None:
                break
            nr, nc = row + self.directions[action][0], col + self.directions[action][1]
            if self.maze[nr, nc] == 1:
                break
            row, col = nr, nc
            path.append((row, col))
        
        return path

class MazeSolverGUI:
    def __init__(self, maze, path):
        pygame.init()
        self.maze = maze
        self.path = path
        self.cell_size = 20
        self.screen = pygame.display.set_mode((len(maze[0]) * self.cell_size, len(maze) * self.cell_size))
        
    def draw_maze(self):
        self.screen.fill((255, 255, 255))
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = (0, 0, 0) if cell == 1 else (255, 255, 255)
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
    
    def draw_solution(self):
        for y, x in self.path: 
            pygame.draw.rect(self.screen, (0, 0, 255), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
            pygame.display.update()
            time.sleep(0.1)
    
    def run(self):
        self.draw_maze()
        pygame.display.update()
        self.draw_solution()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

# Main execution
def measure_performance_value():
    maze_sizes = [5,6,7,8,9,10,11,12,13,14, 15]  # executing for mazes of sizes 5 to 15
    results = []
    
    for size in maze_sizes:
        generator = MazeGenerator(size, size, seed=42)
        maze = generator.generate_maze()
        
        solver = ValueIterationSolver(maze)
        
      
        tracemalloc.start()  # Start tracing memory
        
        start_time = time.time()
        
        iterations = solver.value_iteration()  # Run value iteration
        
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()  # Stop tracing memory
        
        end_time = time.time()
        
        memory_used = peak / 1024  # Convert to KB
        
        path = solver.get_optimal_path()
        path_length = len(path)
        
        execution_time = end_time - start_time
        
        # Store results in a list
        results.append([size, execution_time, iterations, path_length, memory_used])
        
        # Display the GUI for solving the maze
        gui = MazeSolverGUI(maze, path)
        gui.run()
    
    # Write results to CSV
    with open('value_iteration_performance_setting1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Maze Size', 'Execution Time (s)', 'Iterations', 'Path Length', 'Memory Used (KB)'])
        writer.writerows(results)


if __name__ == "__main__":
    measure_performance_value()
