import heapq
import time
import tracemalloc
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start = (0, 0)
        self.end = (len(maze) - 1, len(maze[0]) - 1)

    def a_star(self, heuristic_type):
        tracemalloc.start()
        start_time = time.time()
        open_list = []
        heapq.heappush(open_list, (0, self.start))
        g_costs = {self.start: 0}
        path = {}
        visited = set()

        while open_list:
            current = heapq.heappop(open_list)[1]
            if current == self.end:
                path_cost = g_costs[self.end]
                end_time = time.time()
                memory_used = tracemalloc.get_traced_memory()[1] / 1024
                tracemalloc.stop()
                return path_cost, end_time - start_time, memory_used

            visited.add(current)
            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    tentative_g = g_costs[current] + 1
                    heuristic_value = self._heuristic(neighbor, heuristic_type)
                    if tentative_g < g_costs.get(neighbor, float('inf')):
                        g_costs[neighbor] = tentative_g
                        f_cost = tentative_g + heuristic_value
                        heapq.heappush(open_list, (f_cost, neighbor))
                        path[neighbor] = current
        return float('inf'), float('inf'), float('inf')  # If no path found

    def _get_neighbors(self, pos):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x < len(self.maze[0]) and 0 <= y < len(self.maze) and self.maze[y][x] == 0:
                neighbors.append((x, y))
        return neighbors

    def _heuristic(self, pos, heuristic_type):
        if heuristic_type == "manhattan":
            return abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1])
        elif heuristic_type == "euclidean":
            return np.sqrt((pos[0] - self.end[0])**2 + (pos[1] - self.end[1])**2)


def generate_random_maze(size, seed=42):
    np.random.seed(seed)
    maze = np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])
    maze[0][0] = 0  # Start
    maze[size-1][size-1] = 0  # End
    return maze


def evaluate_heuristics():
    sizes = range(5, 16)
    results = {"size": [], "heuristic": [], "path_length": [], "time": [], "memory": []}
    
    for size in sizes:
        maze = generate_random_maze(size)
        solver = MazeSolver(maze)
        
        for heuristic in ["manhattan", "euclidean"]:
            path_length, time_taken, memory_used = solver.a_star(heuristic)
            results["size"].append(size)
            results["heuristic"].append(heuristic)
            results["path_length"].append(path_length)
            results["time"].append(time_taken)
            results["memory"].append(memory_used)
    
    return results


def plot_results_separately(results):
    sns.set(style="whitegrid")
    metrics = ["path_length", "time", "memory"]
    titles = ["Path Length Comparison", "Execution Time Comparison", "Memory Usage Comparison", "Heuristic Comparison"]
    ylabels = ["Path Length", "Time (s)", "Memory (KB)", "Heuristic Value"]
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)
    
    for i, metric in enumerate(metrics):
        plt.figure(figsize=(8, 5))
        sns.lineplot(x=results["size"], y=results[metric], hue=results["heuristic"], marker="o")
        plt.title(titles[i])
        plt.xlabel("Maze Size")
        plt.ylabel(ylabels[i])
        plt.legend(title="Heuristic")
        plt.savefig(os.path.join(plot_dir, f"{metric}_comparison.png"))
        plt.show()
    
   
    plt.figure(figsize=(8, 5))
    heuristic_values = {"size": [], "manhattan": [], "euclidean": []}
    for size in range(5, 16):
        solver = MazeSolver(generate_random_maze(size))
        heuristic_values["size"].append(size)
        heuristic_values["manhattan"].append(solver._heuristic(solver.start, "manhattan"))
        heuristic_values["euclidean"].append(solver._heuristic(solver.start, "euclidean"))
    
    sns.lineplot(x=heuristic_values["size"], y=heuristic_values["manhattan"], label="Manhattan", marker="o")
    sns.lineplot(x=heuristic_values["size"], y=heuristic_values["euclidean"], label="Euclidean", marker="s")
    plt.title("Heuristic Value Comparison")
    plt.xlabel("Maze Size")
    plt.ylabel("Heuristic Value")
    plt.legend(title="Heuristic Type")
    plt.savefig(os.path.join(plot_dir, "heuristic_comparison.png"))
    plt.show()

results = evaluate_heuristics()
plot_results_separately(results)
