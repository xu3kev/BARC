from common import *
import numpy as np
from typing import *

# concepts:
# pattern construction, color sequence

# description:
# In the input you will see a grid with one square with a different color indicates its border.
# To make the output, you should expand the square into a larger shape, the length is the same as the inner square's side length, 
# and swap the colors between the inner and outer layers.

def main(input_grid: np.ndarray) -> np.ndarray:
    grid = np.copy(input_grid)
    n = len(grid)
    flag = np.zeros((n, n), dtype=int)

    for i in range(0, n):
        for j in range(0, n):
            if flag[i, j] == 1:
                continue
            # Find the square and determine its size
            if grid[i, j] != Color.BLACK:
                if grid[i + 3, j + 3] != Color.BLACK:
                    ty = 2  # 2x2 square
                else:
                    ty = 1  # 1x1 square
                # Mark the area of the square to avoid processing it again
                for x in range(0, ty * 3 + 2):
                    for y in range(0, ty * 3 + 2):
                        flag[i - ty + x, j - ty + y] = 1
                
                c0 = grid[i, j]  # Color of the outer layer
                c1 = grid[i + 1, j + 1]  # Color of the inner layer
                
                # Change colors
                for x in range(0, ty + 2):
                    for y in range(0, ty + 2):
                        grid[i + x, j + y] = c1  # Set outer layer to inner color
                for x in range(0, ty):
                    for y in range(0, ty):
                        grid[i + 1 + x, j + 1 + y] = c0  # Set inner layer to outer color
                
                # Fill the extended areas around the square
                for x in range(0, ty + 2):
                    for y in range(1, ty + 1):
                        grid[i - y, j + x] = c0
                        grid[i + x, j - y] = c0
                        grid[i + ty + 1 + y, j + x] = c0
                        grid[i + x, j + ty + 1 + y] = c0

    return grid

def generate_input() -> np.ndarray:
    n = random.randint(24, 30)  # Size of the grid
    grid = np.zeros((n, n), dtype=int)
    flag = np.copy(grid)

    # Randomly place one or two squares
    t = random.randint(1, 2)
    while t > 0:
        t = t - 1
        ty = random.randint(1, 2)  # Size of the square (1x1 or 2x2)

        # Create the square and its inner part
        sprite = np.zeros((ty + 2, ty + 2), dtype=int)
        inner = np.zeros((ty, ty), dtype=int)
        flag_ = np.zeros((ty * 3 + 2, ty * 3 + 2), dtype=int)
        sprite.fill(random.choice(Color.NOT_BLACK))
        inner.fill(random.choice(Color.NOT_BLACK))
        flag_.fill(1)
        blit_sprite(sprite, inner, 1, 1)  # Create the square with inner color
        
        while True:
            # Randomly select a position to place the square
            row, col = random.randint(0, n - (ty * 3 + 2)), random.randint(0, n - (ty * 3 + 2))
            sub_matrix = flag[row:row + ty * 3 + 2, col:col + ty * 3 + 2]
            if np.all(sub_matrix == 0):  # Ensure no overlap
                blit_sprite(flag, flag_, row, col)
                blit_sprite(grid, sprite, row + ty, col + ty)
                break
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
