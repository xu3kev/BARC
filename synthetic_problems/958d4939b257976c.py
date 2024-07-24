from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, direction, intersection, pixel manipulation

# description:
# In the input grid, you will see black and a mix of colored pixels along the edges of the grid. There will be pink pixels on one edge and teal pixels on the opposite edge.
# To make the output grid, move the pink pixels towards the teal ones and the teal pixels towards the pink ones. When the paths of pink and teal pixels intersect, replace the intersecting pixel with a yellow pixel.

def main(input_grid):
    # Copy the input grid to output grid
    output_grid = np.copy(input_grid)
    
    # Find the coordinates of the pink and teal pixels
    pink_coords = np.argwhere(input_grid == Color.PINK)
    teal_coords = np.argwhere(input_grid == Color.TEAL)

    # Figure out the directions of movement
    if len(pink_coords) == 0 or len(teal_coords) == 0:
        return output_grid
    
    # Determine directions based on initial positions
    move_direction = None
    if np.all(pink_coords[:, 0] == 0): # pink on the top
        move_direction = (1, 0) # move down
    elif np.all(pink_coords[:, 0] == input_grid.shape[0] - 1): # pink on the bottom
        move_direction = (-1, 0) # move up
    elif np.all(pink_coords[:, 1] == 0): # pink on the left
        move_direction = (0, 1) # move right
    elif np.all(pink_coords[:, 1] == input_grid.shape[1] - 1): # pink on the right
        move_direction = (0, -1) # move left

    if move_direction is None:
        return output_grid
    
    inverse_direction = (-move_direction[0], -move_direction[1])

    # Move the pink pixels
    for (x, y) in pink_coords:
        while 0 <= x < input_grid.shape[0] and 0 <= y < input_grid.shape[1]:
            output_grid[x, y] = Color.PINK
            if output_grid[x + move_direction[0], y + move_direction[1]] == Color.TEAL:
                output_grid[x + move_direction[0], y + move_direction[1]] = Color.YELLOW
                break
            x += move_direction[0]
            y += move_direction[1]
    
    # Move the teal pixels
    for (x, y) in teal_coords:
        while 0 <= x < input_grid.shape[0] and 0 <= y < input_grid.shape[1]:
            if output_grid[x, y] == Color.PINK and output_grid[x + inverse_direction[0], y + inverse_direction[1]] == Color.PINK:
                output_grid[x, y] = Color.YELLOW
            else:
                output_grid[x, y] = Color.TEAL
            x += inverse_direction[0]
            y += inverse_direction[1]

    return output_grid


def generate_input():
    # Make a random-sized grid of black background
    n = np.random.randint(10, 20)
    m = np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    
    # Place pink pixels on one random edge
    pink_edge = np.random.choice(['top', 'bottom', 'left', 'right'])
    if pink_edge in ['top', 'bottom']:
        pink_x = 0 if pink_edge == 'top' else n - 1
        pink_y_choices = np.random.choice(range(1, m - 1), np.random.randint(2, m//2), replace=False)
        for py in pink_y_choices:
            grid[pink_x, py] = Color.PINK
    else:
        pink_y = 0 if pink_edge == 'left' else m - 1
        pink_x_choices = np.random.choice(range(1, n - 1), np.random.randint(2, n // 2), replace=False)
        for px in pink_x_choices:
            grid[px, pink_y] = Color.PINK

    # Place teal pixels on the opposite edge
    teal_edge = {'top': 'bottom', 'bottom': 'top', 'left': 'right', 'right': 'left'}[pink_edge]
    if teal_edge in ['top', 'bottom']:
        teal_x = 0 if teal_edge == 'top' else n - 1
        teal_y_choices = np.random.choice(range(1, m - 1), np.random.randint(2, m // 2), replace=False)
        for ty in teal_y_choices:
            grid[teal_x, ty] = Color.TEAL
    else:
        teal_y = 0 if teal_edge == 'left' else m - 1
        teal_x_choices = np.random.choice(range(1, n - 1), np.random.randint(2, n // 2), replace=False)
        for tx in teal_x_choices:
            grid[tx, teal_y] = Color.TEAL

    return grid