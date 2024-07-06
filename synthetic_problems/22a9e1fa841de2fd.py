from common import *

import numpy as np
from typing import *

# concepts:
# rotational symmetry, tiling

# description:
# In the input, you will see a grid with a central tile. You are to rotate this tile around the center of the grid and fill in the missing tiles symmetrically to complete the grid. If the input tile extends beyond the grid, it should be cropped.

def main(input_grid):
    # Find the center of the grid
    center_x, center_y = input_grid.shape[0] // 2, input_grid.shape[1] // 2
    
    # Crop the central tile using a bounding box
    central_tile = input_grid[center_x-1:center_x+2, center_y-1:center_y+2]
    
    # Initialize the output grid
    output_grid = input_grid.copy()
    
    # Rotate the central tile 90, 180, 270 degrees and fill symmetrically
    for i in range(1, 4):
        rotated_tile = np.rot90(central_tile, k=i)
        x_shift = center_x + (i % 2) * central_tile.shape[0] * (-1 if i > 2 else 1)
        y_shift = center_y + ((i+1) % 2) * central_tile.shape[1] * (-1 if i > 1 else 1)
        
        # Adjust for boundary conditions
        for x in range(central_tile.shape[0]):
            for y in range(central_tile.shape[1]):
                if 0 <= x + x_shift < output_grid.shape[0] and 0 <= y + y_shift < output_grid.shape[1]:
                    output_grid[x + x_shift, y + y_shift] = rotated_tile[x, y]
    
    return output_grid


def generate_input():
    # Pick random tile pattern
    tile_color = np.random.choice(Color.NOT_BLACK)
    tile_background = np.random.choice([color for color in Color.NOT_BLACK if color != tile_color])
    
    # Create a 3x3 tile
    central_tile = np.full((3, 3), tile_background, dtype=int)
    for _ in range(5):
        central_tile[np.random.randint(0, 3), np.random.randint(0, 3)] = tile_color
    
    # Place the tile in the center of a larger grid
    grid_size = 7
    input_grid = np.full((grid_size, grid_size), Color.BLACK, dtype=int)
    input_grid[grid_size//2 - 1:grid_size//2 + 2, grid_size//2 - 1:grid_size//2 + 2] = central_tile
    
    return input_grid

# Testing the functions
if __name__ == '__main__':
    grid_in = generate_input()
    print("Input Grid:")
    print(grid_in)
    grid_out = main(grid_in)
    print("Output Grid:")
    print(grid_out)