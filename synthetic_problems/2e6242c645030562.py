import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, symmetry

# description:
# In the input, you will see two blue radial bitmasks separated by a vertical grey bar.
# To make the output, detect the region which has symmetrical pattern in both bitmaps.
# Color this overlapping symmetrical region with teal.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the grey vertical bar to split the grid into two parts
    for x_bar in range(input_grid.shape[0]):
        if np.all(input_grid[x_bar, :] == Color.GREY):
            break

    left_mask = input_grid[:x_bar, :]
    right_mask = input_grid[x_bar+1:, :]

    # Detect symmetry in the left and right masks
    left_sym = detect_rotational_symmetry(left_mask, ignore_colors=[Color.BLACK])
    right_sym = detect_rotational_symmetry(right_mask, ignore_colors=[Color.BLACK])
    
    # Initialize the output grid
    output_grid = np.zeros_like(left_mask)

    # Determine the overlapping symmetrical region
    left_blues = np.argwhere(left_mask == Color.BLUE)
    right_blues = np.argwhere(right_mask == Color.BLUE)

    for x, y in left_blues:
        # Rotate the pixel to check symmetry
        rotated_x, rotated_y = left_sym.apply(x, y, iters=1)
        if right_mask[rotated_x, rotated_y] == Color.BLUE:
            output_grid[x, y] = Color.TEAL
            output_grid[rotated_x, rotated_y] = Color.TEAL

    return np.concatenate((output_grid, np.full((1, output_grid.shape[1]), Color.GREY), output_grid), axis=0)

def generate_input() -> np.ndarray:
    # Create pair of radial symmetric blue bitmasks
    width, height = np.random.randint(10, 20, size=2)

    sprite_size = min(width, height) // 2

    grid1 = random_sprite(sprite_size, sprite_size, symmetry='radial', color_palette=[Color.BLUE], density=0.2)
    grid2 = random_sprite(sprite_size, sprite_size, symmetry='radial', color_palette=[Color.BLUE], density=0.2)

    # Create a vertical grey bar to separate the grids
    bar = np.full((1, sprite_size), Color.GREY)

    # Align grids with the vertical bar
    grid = np.concatenate((grid1, bar, grid2), axis=0)

    final_grid = np.zeros((width, grid.shape[1]), dtype=int)
    start_x = (width - grid.shape[0]) // 2
    final_grid[start_x:start_x+grid.shape[0], :] = grid

    return final_grid