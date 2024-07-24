from common import *
import numpy as np
from typing import *
import random

# concepts:
# rectangular cells, color guide, pixel manipulation

# description:
# In the input, you will see blue horizontal and vertical bars that divide the grid into nine rectangular regions.
# Each region contains a colorful matrix.
# To make the output:
# 1. Identify the region with a cross pattern of identical colors.
# 2. Use the cross pattern colors to perform a mirroring operation on each other region's colors horizontally across the center.

def main(input_grid):
    # Determine the color of the dividers (which should be consistent)
    divider_color = None
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if np.all(input_grid[x,:]==input_grid[x,0]) or np.all(input_grid[:,y]==input_grid[0,y]):
                divider_color = input_grid[x, y]
                break
        if divider_color is not None:
            break

    # Find connected components, treating the divider color as the background
    regions = find_connected_components(input_grid, background=divider_color, monochromatic=False)
    
    # Identify the region with the cross pattern
    cross_pattern_region = None
    for region in regions:
        if is_cross_pattern(region):
            cross_pattern_region = region
            break
    
    # Extract the cross pattern colors
    cross_pattern_colors = extract_cross_pattern_colors(cross_pattern_region)
    
    # Create the output grid
    output_grid = np.copy(input_grid)
    
    for region in regions:
        if not is_cross_pattern(region):
            x, y, w, h = bounding_box(region, background=divider_color)
            mirrored_region = horizontal_mirror(region, cross_pattern_colors)
            blit_object(output_grid, mirrored_region, background=divider_color)

    return output_grid

def is_cross_pattern(region):
    # Determines if the region follows a cross pattern with identical colors
    hs, vs = region.shape[0]//2, region.shape[1]//2
    center_color = region[hs, vs]
    return (
        all(region[i, vs] == center_color for i in range(region.shape[0])) and
        all(region[hs, j] == center_color for j in range(region.shape[1]))
    )

def extract_cross_pattern_colors(region):
    # Simply return the colors from the cross pattern
    hs, vs = region.shape[0]//2, region.shape[1]//2
    colors = {
        'center': region[hs, vs]
    }
    return colors

def horizontal_mirror(region, colors):
    mirrored_region = np.copy(region)
    rows, cols = region.shape
    hs = rows // 2
    
    for r in range(rows):
        for c in range(cols):
            mirrored_region[r, c] = region[r, cols - c - 1]
    
    return mirrored_region


def generate_input():
    divider_color = Color.GREY
    n_cells = 3
    cell_size = 4
    divider_size = 1
    n_dividers = n_cells - 1

    m = cell_size * n_cells + divider_size * n_dividers
    grid = np.full((m, m), Color.BLACK)
    
    for i in range(n_dividers):
        grid[cell_size + i * (cell_size + divider_size), :] = divider_color
        grid[:, cell_size + i * (cell_size + divider_size)] = divider_color

    special_cell_x, special_cell_y = np.random.randint(3), np.random.randint(3)
    for x in range(3):
        for y in range(3):
            cell = grid[
                x * (cell_size + divider_size) : x * (cell_size + divider_size) + cell_size,
                y * (cell_size + divider_size) : y * (cell_size + divider_size) + cell_size
            ]

            if x == special_cell_x and y == special_cell_y:
                # Special cross pattern cell
                for i in range(cell.shape[0]//2):
                    cell[i, cell.shape[1]//2] = Color.GREEN
                    cell[cell.shape[0]//2, i] = Color.GREEN
            else:
                # Randomly color other cells
                for _ in range(np.random.randint(3, cell.size)):
                    rx, ry = np.random.randint(cell_size), np.random.randint(cell_size)
                    cell[rx, ry] = random.choice(list(Color.NOT_BLACK))

    return grid