import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for plots if it doesn't exist
plot_dir = "plots"
os.makedirs(plot_dir, exist_ok=True)

# File paths
value_iteration_file = "csv_results/value_iteration_performance.xlsx"
policy_iteration_file = "csv_results/policy_iteration_performance.xlsx"
search_algorithms_file = "csv_results/search_algorithms_metrics.xlsx"

# Load Excel files
value_iteration_df = pd.read_excel(value_iteration_file, sheet_name="value_iteration_performance", engine="openpyxl")
policy_iteration_df = pd.read_excel(policy_iteration_file, sheet_name="policy_iteration_performance", engine="openpyxl")
search_algorithms_df = pd.read_excel(search_algorithms_file, sheet_name="Sheet", engine="openpyxl")

# Merge data for comparison
comparison_df = pd.merge(value_iteration_df, policy_iteration_df, on="Maze Size", suffixes=("_Value", "_Policy"))

# Select best algorithms for comparison
mdp_best_algo = value_iteration_df  # Best MDP algorithm: Value Iteration
search_best_algo = search_algorithms_df[search_algorithms_df["Algo Name"] == "Astar"]  # Best Search Algorithm: A*

# Set Seaborn style
sns.set(style="whitegrid")

def plot_best_comparison(x, y_mdp, y_search, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(mdp_best_algo[x], mdp_best_algo[y_mdp], marker='o', label='Value Iteration')
    plt.plot(search_best_algo[x], search_best_algo[y_search], marker='s', label='A* Search')
    plt.xlabel("Maze Size")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(os.path.join(plot_dir, filename))
    plt.show()

# Execution time comparison
plot_best_comparison("Maze Size", "Execution Time (s)", "Time Taken (s)", "Execution Time (s)", "MDP vs Search Execution Time", "mdp_vs_search_execution_time.png")

# Memory usage comparison
plot_best_comparison("Maze Size", "Memory Used (KB)", "Memory Used (KB)", "Memory Usage (KB)", "MDP vs Search Memory Usage", "mdp_vs_search_memory_usage.png")

# Path length comparison
plot_best_comparison("Maze Size", "Path Length", "Path Cost", "Path Length", "MDP vs Search Path Length", "mdp_vs_search_path_length.png")

# Execution time of Search Algorithms
plt.figure(figsize=(10, 6))
sns.lineplot(data=search_algorithms_df, x="Maze Size", y="Time Taken (s)", hue="Algo Name", marker='o')
plt.xlabel("Maze Size")
plt.ylabel("Execution Time (s)")
plt.title("Search Algorithm Execution Time Comparison")
plt.legend(title="Algorithm")
plt.savefig(os.path.join(plot_dir, "search_algorithm_execution_time.png"))
plt.show()

# Path length of Search Algorithms
plt.figure(figsize=(10, 6))
markers = {"BFS": "o", "DFS": "s", "Astar": "D"}  # Define marker for each algorithm
sns.lineplot(data=search_algorithms_df, x="Maze Size", y="Path Cost", hue="Algo Name", 
             style="Algo Name", markers=markers, dashes=False)
plt.xlabel("Maze Size")
plt.ylabel("Path Length")
plt.title("Search Algorithm Path Length Comparison")
plt.legend(title="Algorithm")
plt.savefig(os.path.join(plot_dir, "search_algorithm_path_length.png"))
plt.show()

# Memory usage of Search Algorithms
plt.figure(figsize=(10, 6))
sns.lineplot(data=search_algorithms_df, x="Maze Size", y="Memory Used (KB)", hue="Algo Name", marker='o')
plt.xlabel("Maze Size")
plt.ylabel("Memory Used (KB)")
plt.title("Search Algorithm Memory Usage Comparison")
plt.legend(title="Algorithm")
plt.savefig(os.path.join(plot_dir, "search_algorithm_memory_usage.png"))
plt.show()


def plot_mdp_comparison(x, y_value, y_policy, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(comparison_df[x], comparison_df[y_value], marker='o', label='Value Iteration')
    plt.plot(comparison_df[x], comparison_df[y_policy], marker='s', label='Policy Iteration')
    plt.xlabel("Maze Size")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(os.path.join(plot_dir, filename))
    plt.show()

# Execution time comparison between MDP algorithms
plot_mdp_comparison("Maze Size", "Execution Time (s)_Value", "Execution Time (s)_Policy", "Execution Time (s)", "Value vs Policy Execution Time", "value_vs_policy_execution_time.png")

# Memory usage comparison between MDP algorithms
plot_mdp_comparison("Maze Size", "Memory Used (KB)_Value", "Memory Used (KB)_Policy", "Memory Usage (KB)", "Value vs Policy Memory Usage", "value_vs_policy_memory_usage.png")

# Path length comparison between MDP algorithms
plot_mdp_comparison("Maze Size", "Path Length_Value", "Path Length_Policy", "Path Length", "Value vs Policy Path Length", "value_vs_policy_path_length.png")
