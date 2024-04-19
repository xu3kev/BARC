import numpy as np
from typing import *
black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

def main(input_grid: np.ndarray) -> np.ndarray:
    outleft = np.zeros((3, 3), dtype=int)
    outright = np.zeros((3, 3), dtype=int)
    outleft = extract_left_grid(input_grid)
    outright = extract_right_grid(input_grid)
    out = np.zeros((3, 3), dtype=int)
    out = samepixels(outleft, outright)
    return out

# the first three columns of the grid form a new 3*3 grid
def extract_left_grid(grid: np.ndarray) -> np.ndarray:
    return grid[:, :3]

# the fifth, sixth and seventh columns of the grid form a new 3*3 grid
def extract_right_grid(grid: np.ndarray) -> np.ndarray:
    return grid[:, 4:7]

def samepixels(outleft, outright):
    out = np.zeros((3, 3), dtype=int)
    for i in range(0, outleft.shape[0]):
        for j in range(0, outleft.shape[1]):
            if both_equal(a=outleft[i][j], b=outright[i][j], color=blue):
                out = set_to_red(out, x=i, y=j)
    return out

# a and b are both equal to color
def both_equal(a: int, b: int, color: int) -> bool:
    return a == b == color

# The value of row x and column y of this grid becomes red
def set_to_red(grid: np.ndarray, x: int, y: int) -> np.ndarray:
    grid[x][y] = red
    return grid

# make 2 3x3 grid of black and blue, and put them side by side with a gray 3x1 division in the middle
def generate_input() -> np.ndarray:
    # create a 3x3 grid of black (0)
    grid1 = np.zeros((3, 3), dtype=int)
    # sparsely populate it with blue (1)
    for i in range(3):
        for j in range(3):
            if np.random.random() < 0.2:
                grid1[i][j] = blue

    # create a 3x3 grid of black (0)
    grid2 = np.zeros((3, 3), dtype=int)
    # sparsely populate it with blue (1)
    for i in range(3):
        for j in range(3):
            if np.random.random() < 0.2:
                grid2[i][j] = blue
    
    # create a 3x1 grid of gray (5)
    grid3 = np.zeros((3, 1), dtype=int)
    for i in range(3):
        grid3[i][0] = grey

    # concatenate the three grids
    grid = np.concatenate((grid1, grid3, grid2), axis=1)
    return grid

if __name__ == '__main__':
    input_grid = generate_input()
    print(input_grid)
    print(main(input_grid))
