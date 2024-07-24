from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, direction, lines, magnetism

# description:
# In the input, you will see a black grid with teal pixels scattered along one edge and red pixels scattered along an edge perpendicular to the teal one.
# Teal pixels will flow symmetrically from the edge they are on to the opposite edge, forming lines. Whenever there is a red pixel in the same column or row as the flow of teal pixels, it will push the teal pixelâs flow one pixel away from the red pixel.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)
    
    # figure out the direction of teal flow and the push direction based on the positions of red pixels
    edges_with_red = [0, -1]  # Top and bottom edges
    vertical_push_dir = [(0, 1), (0, -1)]  # Pushing to left or right when facing top or bottom row
    
    if Color.RED in output_grid[0, :]:
        push_dir = (0, 1)  # Teal will be pushed left to right
        teal_flow_dir = (1, 0)  # Teal flows from top to bottom
        red_edge = 0
    elif Color.RED in output_grid[-1, :]:
        push_dir = (0, -1)  # Teal will be pushed right to left
        teal_flow_dir = (-1, 0)  # Teal flows from bottom to top
        red_edge = -1
    elif Color.RED in output_grid[:, 0]:
        push_dir = (1, 0)  # Teal will be pushed top to bottom
        teal_flow_dir = (0, 1)  # Teal flows horizontally from left to right
        red_edge = 0
    else:
        push_dir = (-1, 0)  # Teal will be pushed bottom to top
        teal_flow_dir = (0, -1)  # Teal flows horizontally from right to left
        red_edge = -1

    # Get the teal pixels' coordinates
    teal_coords = list(zip(*np.where(input_grid == Color.TEAL)))
    red_coords = list(zip(*np.where(input_grid == Color.RED)))

    # Create flow paths for teal pixels considering the direction and symmetry
    for x, y in teal_coords:
        while 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
            if ((x, red_edge) in red_coords) or ((red_edge, y) in red_coords):
                x += push_dir[0]
                y += push_dir[1]
                if not (0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]):
                    break
            output_grid[x, y] = Color.TEAL
            x += teal_flow_dir[0]
            y += teal_flow_dir[1]
    
    return output_grid


def generate_input():
    # Generate a black grid with the dimensions between 10 and 20 inclusive
    width, height = np.random.randint(10, 20, size=2)
    grid = np.full((width, height), Color.BLACK)

    # Decide which end or side will have teal pixels
    edges = ['top', 'bottom', 'left', 'right']
    teal_edge = np.random.choice(edges)
    red_edge = 'top'
    
    if teal_edge == 'top':
        teal_pixels = np.random.choice(range(1, width-1), np.random.randint(2, 5), replace=False)
        grid[teal_pixels, 0] = Color.TEAL
        red_edge = np.random.choice(['left', 'right'])
        if red_edge == 'left':
            red_pixels = np.random.choice(range(1, height-1), np.random.randint(2, 5), replace=False)
            grid[0, red_pixels] = Color.RED
        else:
            red_pixels = np.random.choice(sum(range(1, width-1)), np.random.randint(2, 5), replace=False)
            grid[-1, red_pixels] = Color.RED
            
    elif teal_edge == 'bottom':
        teal_pixels = np.random.choice(range(1, width-1), np.random.randint(2, 5), replace=False)
        grid[teal_pixels, -1] = Color.TEAL
        red_edge = np.random.choice(['left', 'right'])
        if red_edge == 'left':
            red_pixels = np.random.choice(range(1, height-1), np.random.randint(2, 5), replace=False)
            grid[0, red_pixels] = Color.RED
        else:
            red_pixels = np.random.choice(sum(range(1, width-1)), np.random.randint(2, 5), replace=False)
            grid[-1, red_pixels] = Color.RED

    elif teal_edge == 'left':
        teal_pixels = np.random.choice(range(1, height-1), np.random.randint(2, 5), replace=False)
        grid[0, teal_pixels] = Color.TEAL
        red_edge = np.random.choice(['top', 'bottom'])
        if red_edge == 'top':
            red_pixels = np.random.choice(range(1, width-1), np.random.randint(2, 5), replace=False)
            grid[red_pixels, 0] = Color.RED
        else:
            red_pixels = np.random.choice(sum(range(1, width-1)), np.random.randint(2, 5), replace=False)
            grid[red_pixels, -1] = Color.RED

    else:  # teal_edge == 'right'
        teal_pixels = np.random.choice(range(1, height-1), np.random.randint(2, 5), replace=False)
        grid[-1, teal_pixels] = Color.TEAL
        red_edge = np.random.choice(['top', 'bottom'])
        if red_edge == 'top':
            red_pixels = np.random.choice(range(1, width-1), np.random.randint(2, 5), replace=False)
            grid[red_pixels, 0] = Color.RED
        else:
            red_pixels = np.random.choice(sum(range(1, width-1)), np.random.randint(2, 5), replace=False)
            grid[red_pixels, -1] = Color.RED

    return grid