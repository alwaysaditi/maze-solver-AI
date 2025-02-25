from maze_generator import MazeGenerator
from search_algorithms import MazeSolver
from gui import MazeGUI
import tkinter as tk
from tkinter import messagebox
import time
from maze_generator import MazeGenerator
#from mdp import MDPSolver
from gui import MazeGUI
from tkinter import PhotoImage
from stats import bfs_results
from stats import dfs_results
from stats import astar_results
import openpyxl
from openpyxl import Workbook
from value_iter import measure_performance_value
from policy_iter import measure_performance_policy

# Step 1: Generate a deterministic maze using a fixed seed
seed = 42  # Any number can be used as a seed
sizes = range(5, 16)  # Maze sizes from 5x5 to 15x15

choice = int(input("Enter the choice of algorithm to execute. \n 0 for BFS \n 1 for DFS \n 2 for Astar\n 3 for Value Iteration \n 4 for Policy Iteration"))

if choice ==0:
    for size in sizes:
        maze_generator = MazeGenerator(size,size, seed=seed)  # Generate a maze of any size with the seed
        maze = maze_generator.generate_maze()

        # Step 2: Solve the maze using BFS, DFS, or A*
        solver = MazeSolver(maze)
        solver_steps = solver.bfs() 
        gui = MazeGUI(maze, solver_steps)
        gui.run() 
    
elif choice ==1:
    for size in sizes:
        maze_generator = MazeGenerator(size,size, seed=seed)  # Generate a maze of any size with the seed
        maze = maze_generator.generate_maze()

        # Step 2: Solve the maze using BFS, DFS, or A*
        solver = MazeSolver(maze)
        solver_steps = solver.dfs()
        gui = MazeGUI(maze, solver_steps)
        gui.run()
    
elif choice ==2:
    for size in sizes:
        maze_generator = MazeGenerator(size,size, seed=seed)  # Generate a maze of any size with the seed
        maze = maze_generator.generate_maze()

        # Step 2: Solve the maze using BFS, DFS, or A*
        solver = MazeSolver(maze)
        solver_steps = solver.a_star()
        gui = MazeGUI(maze, solver_steps)
        gui.run()
        
elif choice == 3:
    measure_performance_value()
    
    
elif choice == 4:
    measure_performance_policy()
     
    

    
    # Step 3: Display the step-by-step solution in the GUI
    



def append_to_excel(filename, algo_name, results):
    try:
        # Load existing workbook or create a new one if not found
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active
    except FileNotFoundError:
        wb = Workbook()
        sheet = wb.active
    #these are the headers for the files
        sheet.append(["Algo Name", "Maze Size", "Memory Used (KB)", "Time Taken (s)", "Path Cost"])

    # Append results with increasing maze size (5 to 15)
    maze_size = 5  # Start from size 5
    for result in results:
        sheet.append([algo_name, maze_size,
                      result["BFS memory used" if algo_name == "BFS" else 
                             "DFS memory used" if algo_name == "DFS" else 
                             "Astar memory used"], 
                      result["BFS time taken" if algo_name == "BFS" else 
                             "DFS time taken" if algo_name == "DFS" else 
                             "Astar time taken"], 
                      result["BFS Path Cost" if algo_name == "BFS" else 
                             "DFS Path Cost" if algo_name == "DFS" else 
                             "Astar Path Cost"]])
        maze_size += 1  # Increase maze size

    
    # Save the file
    wb.save(filename)
    print(f"Data appended to {filename} successfully!")

if choice==0:
    append_to_excel("search_algorithms_metrics.xlsx", "BFS", bfs_results)
elif choice == 1:
    append_to_excel("search_algorithms_metrics.xlsx", "DFS", dfs_results)
elif choice==2:
    append_to_excel("search_algorithms_metrics.xlsx", "Astar", astar_results)

root = tk.Tk()
root.withdraw()  # Hide the main tkinter window



