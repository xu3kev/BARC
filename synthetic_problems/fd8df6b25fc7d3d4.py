from common import *

import numpy as np
from typing import *

# concepts:
# connectivity, topology, boolean logical operations

# description:
# The input grid contains three types of objects: red squares (2x2), blue circles (3x3), and yellow pixels.
# The yellow pixels form paths that may connect the red squares and blue circles.
# To produce the output:
# 1. If all red squares are connected by yellow paths, color the entire grid red.
# 2. If all blue circles are connected by yellow paths, color the entire grid blue.
# 3. If condition 1 and 2 are both true, perform a logical XOR operation:
#    color pixels red where either red squares or blue circles are connected, but not both.
# 4. If neither condition 1 nor 2 is true, output a black grid.

def main(input_grid):
    output_grid = np.zeros_like(input_grid)
    
    # Find connected components
    components = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=False)
    
    red_connected = False
    blue_connected = False
    
    for component in components:
        red_squares = np.all(component[input_grid == Color.RED] == Color.RED)
        blue_circles = np.all(component[input_grid == Color.BLUE] == Color.BLUE)
        
        if red_squares and np.sum(component == Color.RED) == np.sum(input_grid == Color.RED):
            red_connected = True
        
        if blue_circles and np.sum(component == Color.BLUE) == np.sum(input_grid == Color.BLUE):
            blue_connected = True
    
    if red_connected and blue_connected:
        # XOR operation
        red_component = np.zeros_like(input_grid, dtype=bool)
        blue_component = np.zeros_like(input_grid, dtype=bool)
        
        for component in components:
            if np.any(component == Color.RED):
                red_component |= (component != Color.BLACK)
            if np.any(component == Color.BLUE):
                blue_component |= (component != Color.BLACK)
        
        output_grid[red_component ^ blue_component] = Color.RED
    elif red_connected:
        output_grid[:] = Color.RED
    elif blue_connected:
        output_grid[:] = Color.BLUE
    # else: output remains black

    return output_grid

def generate_input():
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)
    
    red_square = np.full((2, 2), Color.RED)
    blue_circle = random_sprite(3, 3, color_palette=[Color.BLUE], symmetry='radial')
    
    # Place red squares
    for _ in range(np.random.randint(2, 4)):
        x, y = random_free_location_for_sprite(grid, red_square, padding=1)
        blit_sprite(grid, red_square, x, y)
    
    # Place blue circles
    for _ in range(np.random.randint(2, 4)):
        x, y = random_free_location_for_sprite(grid, blue_circle, padding=1)
        blit_sprite(grid, blue_circle, x, y)
    
    # Add yellow paths
    for _ in range(n * m // 4):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        if grid[x, y] == Color.BLACK:
            grid[x, y] = Color.YELLOW
    
    return grid