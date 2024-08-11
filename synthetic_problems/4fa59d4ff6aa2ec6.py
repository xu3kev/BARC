from common import *

import numpy as np
from typing import *


# concepts:
# objects, magnetism, lines, direction

# description:
# In the input grid, you will see a grid with teal pixels scattered along one edge, and blue pixels elsewhere in the grid. 
# The teal pixels flow in a specific direction (down, up, left, or right), but if they encounter a blue pixel, they will split perpendicular to the direction of the flow.

def main(input_grid):
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Determine the flow direction based on where the teal pixels are (left, right, top, or bottom edge)
    flow_direction = None
    if Color.TEAL in input_grid[0, :]:
        flow_direction = 'down'
    elif Color.TEAL in input_grid[-1, :]:
        flow_direction = 'up'
    elif Color.TEAL in input_grid[:, 0]:
        flow_direction = 'right'
    elif Color.TEAL in input_grid[:, -1]:
        flow_direction = 'left'

    # Vectors for each possible flow direction
    direction_vectors = {
        'down': (1, 0),
        'up': (-1, 0),
        'right': (0, 1),
        'left': (0, -1)
    }

    dx, dy = direction_vectors[flow_direction]

    # Find coordinates of teal and blue pixels
    teal_coords = np.argwhere(input_grid == Color.TEAL)
    blue_coords = set(zip(*np.where(input_grid == Color.BLUE)))

    # Process each teal pixel's flow
    for x, y in teal_coords:
        while 0 <= x < height and 0 <= y < width:
            if (x, y) in blue_coords:
                # Split direction when encountering a blue pixel
                if flow_direction in ['down', 'up']:
                    dx, dy = 0, 1 if (x, y)[1] % 2 == 0 else -1
                else:
                    dx, dy = 1 if (x, y)[0] % 2 == 0 else -1, 0

            if x >= height or y >= width or x < 0 or y < 0:
                break  # stop if going out of bounds

            output_grid[x, y] = Color.TEAL
            x += dx
            y += dy

    return output_grid


def generate_input():
    # Create the base empty grid
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # Select flow direction
    flow_direction = np.random.choice(['down', 'up', 'right', 'left'])

    # Set the teal edge based on the direction
    if flow_direction == 'down':
        grid[0, np.random.choice(range(m), np.random.randint(2, m // 2), replace=False)] = Color.TEAL
    elif flow_direction == 'up':
        grid[-1, np.random.choice(range(m), np.random.randint(2, m // 2), replace=False)] = Color.TEAL
    elif flow_direction == 'right':
        grid[np.random.choice(range(n), np.random.randint(2, n // 2), replace=False), 0] = Color.TEAL
    else:
        grid[np.random.choice(range(n), np.random.randint(2, n // 2), replace=False), -1] = Color.TEAL

    # Randomly place blue pixels as barriers
    for _ in range(np.random.randint(3, 8)):
        grid[np.random.randint(0, n), np.random.randint(0, m)] = Color.BLUE

    return grid