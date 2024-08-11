from common import *

import numpy as np
from typing import *

# concepts:
# horizontal/vertical bars, surrounding

# description:
# In the input, you will see a grid with colored pixels sprinkled on it. Each colored pixel will be expanded into a cross shape 
# by adding a horizontal and a vertical bar originating from the pixel. At intersections where bars meet, the grid will use the color of the pixel at that position.
# Any pixel that is surrounded (i.e., it has non-black pixels in all four cardinal directions: left, right, up, down) will turn black.

def main(input_grid: np.ndarray) -> np.ndarray:
    n, m = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    
    # Expand each pixel into a cross shape
    for x in range(n):
        for y in range(m):
            if input_grid[x, y] != Color.BLACK:
                output_grid[:, y] = input_grid[x, y]  # Vertical bar
                output_grid[x, :] = input_grid[x, y]  # Horizontal bar

    # Handle the surrounding rule
    for x in range(1, n-1):
        for y in range(1, m-1):
            if (output_grid[x-1, y] != Color.BLACK and
                output_grid[x+1, y] != Color.BLACK and
                output_grid[x, y-1] != Color.BLACK and
                output_grid[x, y+1] != Color.BLACK):
                output_grid[x, y] = Color.BLACK

    return output_grid


def generate_input() -> np.ndarray:
    # make a black grid of random size
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)

    # sprinkle some random-not-black pixels
    num_pixels = np.random.randint(1, min(n, m))
    for _ in range(num_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        color = random.choice(list(Color.NOT_BLACK))
        grid[x, y] = color

    return grid