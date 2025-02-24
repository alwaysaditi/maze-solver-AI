import numpy as np
import pygame
import time
import tracemalloc
import csv
from value_iter import MazeSolverGUI  

class PolicyIterationSolver:
    def __init__(self, maze, rewards=None, discount_factor=0.9, threshold=1e-4, move_prob=0.8):
        self.maze = np.array(maze)
        self.rows, self.cols = self.maze.shape
        self.discount_factor = discount_factor
        self.threshold = threshold
        self.move_prob = move_prob  # Probability of moving in the intended direction
        
        self.rewards = rewards if rewards else self._initialize_rewards()
        self.values = np.zeros((self.rows, self.cols))
        self.policy = np.full((self.rows, self.cols), 'R')  # Default to 'R'
        
        self.directions = {
            'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)
        }

        self.side_moves = {
            'U': ['L', 'R'], 'D': ['L', 'R'],
            'L': ['U', 'D'], 'R': ['U', 'D']
        }

    def _initialize_rewards(self):
        rewards = np.full((self.rows, self.cols), -0.1) 
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

    def policy_evaluation(self): #this function calculates the values of all cells based on a current policy.
        while True:
            delta = 0
            new_values = np.copy(self.values)
            
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.maze[row, col] == 1: #we don't evaluate the policy for cells that represent walls
                        continue
                    
                    action = self.policy[row, col] #get the current policy for that cell
                    if action in self.directions:
                        nr, nc = row + self.directions[action][0], col + self.directions[action][1] #these lines of code update the value of a cell based on the current policy
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            new_values[row, col] = self.rewards[row, col] + self.discount_factor * self.values[nr, nc]
                    
                    delta = max(delta, abs(new_values[row, col] - self.values[row, col]))
            
            self.values = new_values
            if delta < self.threshold: #this is the convergence check
                break

    def policy_improvement(self):
        policy_stable = True # Assume the policy is stable unless changes occur
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row, col] == 1:
                    continue
                
                best_action = None #Initializing best_action = None to track the best move.
                best_value = float('-inf') #Set best_value to -∞, so any valid move will be better
                possible_moves = self._get_possible_moves(row, col) #getting the possible moves for any position
                
                for action, (nr, nc) in possible_moves.items(): #Loop through each possible move. and get the expected value using bellman equation which indicates how good is a move.
                    value = self.rewards[row, col] + self.discount_factor * self.values[nr, nc]
                    
                    # Add probability of moving to left or right of the intended move
                    side_actions = self.side_moves[action]  # Get left and right moves
                    side_prob = (1 - self.move_prob) / 2  # Probability split for side moves
                    
                    for side_action in side_actions:
                        if side_action in possible_moves:
                            sr, sc = possible_moves[side_action]
                            value += side_prob * (self.rewards[sr, sc] + self.discount_factor * self.values[sr, sc])
                        else:
                            value += side_prob * (self.rewards[row, col] + self.discount_factor * self.values[row, col])
                    
                    if value > best_value:
                        best_value = value
                        best_action = action
                
                if best_action and best_action != self.policy[row, col]:
                    policy_stable = False  # Policy has changed, so it's not stable
                self.policy[row, col] = best_action # Update policy with best action
        
        return policy_stable
    
    def policy_iteration(self): #this function counts one iteration as a complete execution of policy evaluation and policy improvement
        iterations = 0
        while True:
            iterations += 1
            self.policy_evaluation()
            if self.policy_improvement():
                break
        return iterations

    def get_optimal_path(self):
        path = [(0, 0)]
        row, col = 0, 0
        
        while (row, col) != (self.rows-1, self.cols-1):
            action = self.policy[row, col]
            if action is None:
                break
            row, col = row + self.directions[action][0], col + self.directions[action][1]
            path.append((row, col))
        
        return path

# Main execution for measuring performance
from maze_generator import MazeGenerator
def measure_performance_policy():
    maze_sizes = [5,6,7,8,9,10,11,12,13,14, 15] 
    results = []
    
    for size in maze_sizes:
        generator = MazeGenerator(size, size, seed=42)
        maze = generator.generate_maze()
        
        solver = PolicyIterationSolver(maze)
        
        # Measure execution time and memory usage with tracemalloc
        tracemalloc.start()  # Start tracing memory
        
        start_time = time.time()
        
        iterations = solver.policy_iteration()  # Run policy iteration
        
        # Measure memory usage after policy iteration
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()  # Stop tracing memory
        
        end_time = time.time()
        
        # Convert memory to kilobytes
        memory_used = peak / 1024  # Convert to KB
        
        path = solver.get_optimal_path()
        path_length = len(path)
        
        execution_time = end_time - start_time
       
        results.append([size, execution_time, iterations, path_length, memory_used])
        
     
        gui = MazeSolverGUI(maze, path)
        gui.run()
    
    # Write results to CSV
    with open('policy_iteration_performance.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Maze Size', 'Execution Time (s)', 'Iterations', 'Path Length', 'Memory Used (KB)'])
        writer.writerows(results)


if __name__ == "__main__":
    measure_performance_policy()
