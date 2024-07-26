from common import *

import numpy as np
from typing import *

def main(input_grid):
    output_grid = np.copy(input_grid)
    color = input_grid[input_grid != Color.BLACK][0]

    # Coordinates of the central part of the grid
    center_x, center_y = input_grid.shape[0] // 2, input_grid.shape[1] // 2

    for distance in range(1, max(input_grid.shape)):
        # Draw line in all four directions
        for dx, dy in [(-distance, 0), (distance, 0), (0, -distance), (0, distance)]:
            if 0 <= center_x + dx < input_grid.shape[0] and 0 <= center_y + dy < input_grid.shape[1]:
                output_grid[center_x + dx, center_y + dy] = color

        # Continue the process until lines reach the boundaries of the grid
        if (center_x - distance < 0 or center_x + distance >= input_grid.shape[0] or
            center_y - distance < 0 or center_y + distance >= input_grid.shape[1]):
            break

    return output_grid

def generate_input():
    # Create a 15x15 grid
    input_grid = np.full((15, 15), Color.BLACK)

    # Choose a random color for the central pixel
    color = np.random.choice(Color.NOT_BLACK)

    # Place the central pixel
    center_x, center_y = input_grid.shape[0] // 2, input_grid.shape[1] // 2
    input_grid[center_x, center_y] = color

    return input_grid