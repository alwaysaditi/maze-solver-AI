import heapq
import time
import tracemalloc
from stats import bfs_results
from stats import dfs_results
from stats import astar_results
class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start = (0, 0)
        self.end = (len(maze) - 1, len(maze[0]) - 1)

    def bfs(self):
        tracemalloc.start() 
        start_time = time.time()
        queue = [self.start] #BFS uses a queue data structure to keep track of all nodes at the current level
        visited = set()
        visited.add(self.start) #this is to prevent visiting the same nodes repeatedly, initially the start node is added to the visited set
        path = {} #this stores the path from the start node to the goal node.
        path_cost = 0  

        while queue:
            current = queue.pop(0)
            yield current  # this helps in visualisation (we are showing each step on the Maze in GUI)

            if current == self.end:
                path_cost = len(list(self._retrace_path(path))) - 1  # Path length (excluding start node)
                end_time = time.time()
                current_memory, peak_memory = tracemalloc.get_traced_memory() #current memory returns the memory currently allocated to the program, peak memory is the maximum memory at any point in execution
                memory_used= peak_memory / 1024 #the value returned is in bytes so we divide by 1024 to convert to KB
                tracemalloc.stop()
                
             
                  
              
                stats = { #appending result for each individual maze size
                "BFS memory used": memory_used,
                "BFS time taken": end_time - start_time,
                "BFS Path Cost": path_cost
            }
            
                bfs_results.append(stats)  # Append to global list
                yield from self._retrace_path(path)
                return True
            
               
             
               

            for neighbor in self._get_neighbors(current): #for each neighbour of the current node we add it to the queue if not already explored and also mark it visited
                if neighbor not in visited:
                    visited.add(neighbor)
                    path[neighbor] = current
                    queue.append(neighbor)
        return False

    def dfs(self):
        tracemalloc.start() 
        start_time = time.time()
        stack = [self.start]
        visited = set()
        visited.add(self.start)
        path = {}
        path_cost = 0  # Track the cost (number of steps)

        while stack:
            current = stack.pop()  # this removes the last element by default behaving as LIFO
            yield current  

            if current == self.end:
                #print("found solution!")
                path_cost = len(list(self._retrace_path(path))) - 1  # Path length (excluding start node)
                end_time = time.time()
                current_memory, peak_memory = tracemalloc.get_traced_memory()
                memory_used= peak_memory / 1024
                tracemalloc.stop()
                
         

                stats = {
                "DFS memory used": memory_used,
                "DFS time taken": end_time - start_time,
                "DFS Path Cost": path_cost
            }
            
                dfs_results.append(stats)  # Append to global list
               
                yield from self._retrace_path(path)  #this helps to visualise the entire cost once solved.
                return True

            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path[neighbor] = current  # this stores the parent of neighbour (which is current node)
                    stack.append(neighbor)
        return False

    def a_star(self):
        tracemalloc.start() 
        start_time = time.time()
        open_list = []
        #in astar algorithm, we explore nodes by priority, that is node with the lowest cost is explored first. this can be implemented 
        #with the help of a heap data structure. heap automatically prioritises the nodes with the lowest f-cost to be explored first/
        heapq.heappush(open_list, (0, self.start))
        g_costs = {self.start: 0}
        
        path = {}
        visited = set()
        path_cost = 0  # Track the cost (number of steps)

        while open_list:
            current = heapq.heappop(open_list)[1]
            yield current  # Yield the current position to show the step

            if current == self.end:
                path_cost = g_costs[self.end]  # g_cost stores the shortest known cost to reach each node. if we have reached the end, then we print the shortest cost to reach the end node.
                end_time = time.time()
                current_memory, peak_memory = tracemalloc.get_traced_memory()
                memory_used= peak_memory / 1024
                tracemalloc.stop()
                
            

                
                stats = {
                "Astar memory used": memory_used,
                "Astar time taken": end_time - start_time,
                "Astar Path Cost": path_cost
            }
            
                astar_results.append(stats)  # Append to global list
               
                yield from self._retrace_path(path)  # Yield the entire path once solved
                return True

            visited.add(current)

            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    tentative_g = g_costs[current] + 1 #since all edges have an equal weight, we consider g cost to reach a node as it's parent's g cost+1
                    if tentative_g < g_costs.get(neighbor, float('inf')): #if the route cost found to a node through the current node as parent is lesser than the route cost found through any other parent, we update the g cost
                        g_costs[neighbor] = tentative_g
                        f_cost = tentative_g + self._heuristic(neighbor) #heuristic returns the manhattan distance
                        heapq.heappush(open_list, (f_cost, neighbor))
                        path[neighbor] = current
        return False

    def _get_neighbors(self, pos): #for any node in our maze movement is permitted to only one of the four directions (LEFT, DOWN, RIGHT, UP). This function returns the neighbours for any node
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x < len(self.maze[0]) and 0 <= y < len(self.maze) and self.maze[y][x] == 0:
                neighbors.append((x, y))
        return neighbors

    def _heuristic(self, pos):  # Manhattan distance heuristic for A*
        return abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1])

    def _retrace_path(self, path):
        current = self.end
        solution = [current]
        while current != self.start:
            current = path[current]
            solution.append(current)
        solution.reverse()
        for step in solution:
            yield step  # Yield each step of the final solution
