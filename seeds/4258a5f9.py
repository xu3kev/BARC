import numpy as np
from typing import *
black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

# high level description of the main function:
# take in a np grid of integers, where each integer represents a color
# detect the gray color (5)
# then surround it with blue (1) in a 3x3 grid around it

def exists_grey_square(grid: List[List[int]]) -> bool:
    """
    Checks if there exists a square in the grid which color is grey.
    
    Args:
    - grid: a 2D list of integers representing the grid
    
    Returns:
    - a boolean value indicating whether there exists a grey square in the grid
    """
    for row in grid:
        for square in row:
            if square == grey:
                return True
    return False

def main(input_grid):
    output_grid = [[0 for i in range(9)] for j in range(9)]
    for i in range(len(input_grid)):
        for j in range(len(input_grid[i])):
            if input_grid[i][j] == 5:
                output_grid[i][j] = input_grid[i][j]
            elif exists_grey_square(input_grid[max(i - 1, 0):min(i + 2, 9), max(0, j - 1):min(j + 2, 9)]):
                output_grid[i][j] = 1
            else:
                output_grid[i][j] = input_grid[i][j]
    return output_grid


# high level description of the input generator to the main function:
# create a 9x9 grid of black (0) and then sparsely populate it with gray (5)
def generate_input():
    # create a 9x9 grid of black (0)
    grid = [[0 for i in range(9)] for j in range(9)]
    # sparsely populate it with gray (5)
    for i in range(9):
        for j in range(9):
            if np.random.random() < 0.05:
                grid[i][j] = 5
    return np.array(grid)

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    input_grid = generate_input()
    print(input_grid)
    print(main(input_grid))