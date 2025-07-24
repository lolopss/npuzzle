import sys
import math

class Puzzle:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
        self.flat = tuple(num for row in grid for num in row) # Flatten the 2D grid into a 1D tuple for easy indexing
        self.zero_pos = self.flat.index(0)
        
    def manhattan(self, goal):
        dist = 0
        for i, val in enumerate(self.flat):
            if val == 0:
                continue
            x1, y1 = divmod(i, self.size) # Current position of the tile | (divmod returns : i // size, i %% size, so row and collumn)
            goal_i = goal.flat.index(val) # Find the tile's position in the goal state
            x2, y2 = divmod(goal_i, self.size) # Goal position of the tile
            dist += abs(x1 - x2) + abs(y1 - y2) # Total dist (horizontal + vertical)
        return dist

    def get_neighbors(self):
        neighbors = []
        x, y = divmod(self.zero_pos, self.size)
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                new_flat = list(self.flat)
                new_i = new_x * self.size + new_y
                new_flat[self.zero_pos], new_flat[new_i] = new_flat[new_i], new_flat[self.zero_pos]
                new_grid = [new_flat[i:i+self.size] for i in range(0, len(new_flat), self.size)]
                neighbors.append(Puzzle(new_grid))
        return neighbors
    


def main():
    try:
        arg = sys.argv
        if (len(arg) == 2):
            file = sys.argv[1]
            if not file.endswith(".txt"):
                raise ValueError("The file must have a .txt extension")
        else:
            raise ValueError("Missing an argument (.txt file)")
        
        with open(file, 'r') as f:
            lines = f.readlines()

        puzzle = []
        size = None

        for line in lines:
            line = line.split('#')[0].strip()  # Remove comments and whitespace
            if not line:
                continue  # Skip empty lines
            if size is None:
                size = int(line)  # First valid line is the size of the puzzle
                continue
            row = list(map(int, line.split()))
            if len(row) != size:
                raise ValueError("Row length does not match the puzzle size")
            puzzle.append(row)

        if len(puzzle) != size:
            raise ValueError("Number of rows does not match the puzzle size")

        print("Parsed puzzle:")
        for row in puzzle:
            print(row)
        initial_puzzle = Puzzle(puzzle)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__" :
    main()