import random

class MazeGenerator:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]  # 1 for wall, 0 for path
        self.seed = seed

    def generate_maze(self):
        if self.seed is not None:
            random.seed(self.seed)  # Seed the random generator for reproducibility

        # Step 1: Carve a guaranteed path from start (0, 0) to end (width-1, height-1)
        self._carve_direct_path()

        # Step 2: Apply randomized DFS to create additional paths
        self._carve_path(0, 0)

        # Ensure start and end cells are open
        self.maze[0][0] = 0  # Start cell (top-left) is open
        self.maze[self.height - 1][self.width - 1] = 0  # End cell (bottom-right) is open

        return self.maze

    def _carve_direct_path(self):
        """Carve a direct path from (0, 0) to (width-1, height-1)."""
        x, y = 0, 0
        while x < self.width - 1:
            self.maze[y][x] = 0  # Carve path to the right
            x += 1
        while y < self.height - 1:
            self.maze[y][x] = 0  # Carve path down
            y += 1

    def _carve_path(self, x, y):
        """Randomly carve paths using DFS."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)  # Shuffle directions deterministically if a seed is set
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == 1:
                self.maze[y + dy][x + dx] = 0
                self.maze[ny][nx] = 0
                self._carve_path(nx, ny)


