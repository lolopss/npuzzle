import sys
import math

class Puzzle:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
        self.flat = tuple(num for row in grid for num in row) # Flatten the 2D grid into a 1D tuple for easy indexing
        self.zero_pos = self.flat.index(0)

    def __hash__(self):
        return hash(self.flat)

    def __eq__(self, other):
        return isinstance(other, Puzzle) and self.flat == other.flat
        
    def manhattan(self, goal):
        if self.size != goal.size:
            raise ValueError("Puzzle sizes do not match", self.size, goal.size)

        print(f"Self flat: {self.flat}")
        print(f"Goal flat: {goal.flat}")
        # Create a dictionary mapping each value in the goal puzzle to its (row, column) position
        goal_positions = {val: divmod(i, self.size) for i, val in enumerate(goal.flat)}
        dist = 0

        for i, val in enumerate(self.flat):
            print(i, val)
            if val == 0:
                continue  # Skip the empty space
            if val not in goal_positions:
                raise ValueError(f"Value {val} not found in goal puzzle")
            x1, y1 = divmod(i, self.size)
            x2, y2 = goal_positions[val]
            dist += abs(x1 - x2) + abs(y1 - y2)

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
    
def create_goal(size):
    return Puzzle([[size * i + j + 1 for j in range(size)] for i in range(size)] + [[0]])

def is_solvable(puzzle):
    flat = puzzle.flat
    inversions = sum(
        1 for i in range(len(flat)) for j in range(i + 1, len(flat))
        if flat[i] and flat[j] and flat[i] > flat[j]
    )

    if puzzle.size % 2 == 1:
        return inversions % 2 == 0
    else:
        row_from_bottom = puzzle.size - (puzzle.zero_pos // puzzle.size) # From bottom when pair
        return (inversions + row_from_bottom) % 2 == 1

import heapq

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def solve_puzzle(initial, goal):
    open_set = []
    heapq.heappush(open_set, (0, initial))

    came_from = {}
    print(initial.flat)
    g_score = {initial.flat: 0}
    print(g_score)
    print("oui ", initial.manhattan(goal))

    f_score = {initial.flat: initial.manhattan(goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current.flat == goal.flat:
            return reconstruct_path(came_from, current)

        for neighbor in current.get_neighbors():
            neighbor_flat = tuple(neighbor.flat)  # Ensure neighbor.flat is a tuple
            tentative_g_score = g_score[current.flat] + 1
            if neighbor_flat not in g_score or tentative_g_score < g_score[neighbor_flat]:
                came_from[neighbor_flat] = current
                g_score[neighbor_flat] = tentative_g_score
                f_score[neighbor_flat] = tentative_g_score + neighbor.manhattan(goal)
                heapq.heappush(open_set, (f_score[neighbor_flat], neighbor))

    return None  # No solution found

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
                if not line.isdigit():
                    raise ValueError(f"Invalid size value: {line}")
                size = int(line)  # First valid line is the size of the puzzle (n)
                continue
            try:
                row = list(map(int, line.split()))
            except ValueError:
                raise ValueError(f"Non-numerical value found in row: {line}")
            if len(row) != size:
                raise ValueError("Row length does not match the puzzle size")
            puzzle.append(row)

        if len(puzzle) != size:
            raise ValueError("Number of rows does not match the puzzle size")

        # Validate puzzle numbers
        valid_numbers = set(range(size * size))
        flat_puzzle = [num for row in puzzle for num in row]
        if set(flat_puzzle) != valid_numbers:
            raise ValueError(f"Invalid puzzle numbers. Expected numbers: {valid_numbers}, Found: {set(flat_puzzle)}")

        print("Parsed puzzle:")
        for row in puzzle:
            print(row)
        initial_puzzle = Puzzle(puzzle)
        goal = create_goal(size)
        if not is_solvable(initial_puzzle):
            raise ValueError("The puzzle is not solvable")
        solution = solve_puzzle(initial_puzzle, goal)
        if solution:
            print("Solution found:")
            for step in solution:
                for row in step.grid:
                    print(row)
                print()
        else:
            print("No solution exists")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__" :
    main()