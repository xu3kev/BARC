from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, repetition, patterns

# description:
# In the input you will see an 7x7 grid with a staircase-like diagonal pattern of colored pixels.
# Each staircase consists of multiple right-angled steps of various colors leading upwards and to the right.
# To generate the output, repeat each colored staircase pattern throughout the grid.
# Make sure to repeat it in every direction (both vertically and horizontally).
# Ensure the colors and lengths of stairs are preserved, and the repetitions form a coherent pattern filling the output grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros((7, 7), dtype=int)

    # Loop over the input to detect colored pixels in a staircase pattern
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i][j] != Color.BLACK:
                c = input_grid[i][j]

                # Detected the starting point of a staircase, repeat the steps in the pattern
                lengths = detect_staircase_length(input_grid, i, j, c)

                # Apply repeated staircases in every direction
                for distance in range(0, output_grid.shape[0]*2, 3):
                    draw_staircase(output_grid, i-distance, j, c, lengths)
                    draw_staircase(output_grid, i+distance, j, c, lengths)
                    draw_staircase(output_grid, i, j-distance, c, lengths)
                    draw_staircase(output_grid, i, j+distance, c, lengths)
    
    return output_grid

def detect_staircase_length(grid: np.ndarray, x: int, y: int, c: str) -> List[int]:
    # Determine the length of each step in a staircase
    lengths = []
    while x < grid.shape[0] and y < grid.shape[1] and grid[x][y] == c:
        length = 1
        while x + length < grid.shape[0] and y + length < grid.shape[1] and grid[x + length][y + length] == c:
            length += 1
        lengths.append(length)
        x += length
        y += length
    return lengths

def draw_staircase(grid: np.ndarray, x: int, y: int, c: str, lengths: List[int]):
    # Draw the staircase pattern based on the detected lengths
    for length in lengths:
        draw_line(grid, x, y, length=length, color=c, direction=(1, 1))
        draw_line(grid, x + length - 1, y + length - 1, length=length, color=c, direction=(1, 0))
        x += length
        y += length

def generate_input() -> np.ndarray:
    # Create a 7x7 grid of black (0)
    grid = np.zeros((7, 7), dtype=int)

    # Pick 3 random distinct colors
    c1, c2, c3 = np.random.choice(list(Color.NOT_BLACK), 3, replace=False)

    # Put down the staircase patterns
    place_staircase(grid, c1)
    place_staircase(grid, c2)
    place_staircase(grid, c3)

    return grid

def place_staircase(grid: np.ndarray, color: str):
    # Create staircase pattern with random positions and lengths
    stair_length = np.random.randint(2, 4)
    x_start = np.random.randint(0, grid.shape[0] - stair_length)
    y_start = np.random.randint(0, grid.shape[1] - stair_length)
    
    for step in range(stair_length):
        grid[x_start + step][y_start + step] = color
        if step < stair_length - 1:
            grid[x_start + step + 1][y_start + step] = color
            grid[x_start + step][y_start + step + 1] = color
  
    # Ensure the desktop contains no orphan blocks 
    if np.any(main(grid) == Color.BLACK):
        place_staircase(grid, color)

    return grid