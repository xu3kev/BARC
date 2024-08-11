from common import *

import numpy as np
from typing import *

# concepts:
# direction, directional growth, connectivity

# description:
# In the input, you will see several colored pixels scattered across a black background.
# The goal is to grow lines from each of the colored pixels in 4 cardinal directions (up, down, left, right).
# If the lines hit another colored pixel or the edge of the grid, they should stop.
# Lines should be drawn in the color of the starting pixel.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the positions of all colored pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    
    # directions correspond to (dy, dx): up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for x, y in colored_pixels:
        color = input_grid[x, y]
        
        for direction in directions:
            dx, dy = direction
            nx, ny = x + dx, y + dy
            while 0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1]:
                if input_grid[nx, ny] != Color.BLACK:
                    break
                output_grid[nx, ny] = color
                nx += dx
                ny += dy

    return output_grid

def generate_input():
    # create a grid with dimensions between 6 and 10
    n, m = np.random.randint(6, 11), np.random.randint(6, 11)
    grid = np.zeros((n, m), dtype=int)

    # place a random number of colored pixels, we'll make sure they are at least 4 and less than 7
    num_pixels = np.random.randint(4, 7)
    colors = list(Color.NOT_BLACK)
    
    for _ in range(num_pixels):
        color = np.random.choice(colors)
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = color

    return grid

# Example of running the functions
if __name__ == '__main__':
    generated_input = generate_input()
    print("Input Grid:")
    print(generated_input)
    output_grid = main(generated_input)
    print("Output Grid:")
    print(output_grid)