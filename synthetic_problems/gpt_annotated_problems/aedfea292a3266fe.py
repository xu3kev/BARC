from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, color guide, pixel manipulation

# description:
# In the input, you will see grey horizontal and vertical bars that divide the grid into nine 3x3 rectangular regions. 
# Each region contains 3-5 colored pixels.
# To make the output:
# 1. Find the region with exactly 5 colored pixels. This is the "guide" region.
# 2. For each other region:
#    a. Count the number of colored pixels (N) in that region.
#    b. Copy the N most common colors from the guide region to this region.
#    c. Place these colors in the region, starting from the top-left and moving right then down.
# 3. The grey dividers should remain unchanged in the output.

def main(input_grid: np.ndarray) -> np.ndarray:
    divider_color = Color.GRAY

    # Find regions
    regions = find_connected_components(input_grid, background=divider_color, monochromatic=False)

    # Find the guide region (the one with exactly 5 colored pixels)
    guide_region = None
    for region in regions:
        colored_pixels = np.sum((region != divider_color) & (region != Color.BLACK))
        if colored_pixels == 5:
            guide_region = region
            break
    
    assert guide_region is not None, "No guide region found"

    # Get color frequencies in the guide region
    guide_colors = [color for color in guide_region.flatten() if color not in [Color.BLACK, divider_color]]
    color_freq = {}
    for color in guide_colors:
        color_freq[color] = color_freq.get(color, 0) + 1
    sorted_colors = sorted(color_freq.items(), key=lambda x: x[1], reverse=True)

    # Create output grid
    output_grid = np.full_like(input_grid, Color.BLACK)

    # Copy dividers
    output_grid[input_grid == divider_color] = divider_color

    # Process each region
    for region in regions:
        if np.array_equal(region, guide_region):
            output_grid[region != divider_color] = guide_region[region != divider_color]
        else:
            colored_pixels = np.sum((region != divider_color) & (region != Color.BLACK))
            colors_to_use = [color for color, _ in sorted_colors[:colored_pixels]]
            
            # Place colors in the region
            region_mask = (region != divider_color) & (region != Color.BLACK)
            flat_indices = np.where(region_mask.flatten())[0]
            for i, index in enumerate(flat_indices):
                x, y = np.unravel_index(index, region.shape)
                output_grid[np.where(region == region[x, y])] = colors_to_use[i]

    return output_grid

def generate_input() -> np.ndarray:
    divider_color = Color.GRAY

    # Create grid with dividers
    cell_size = 3
    n_cells = 3
    divider_size = 1
    n_dividers = n_cells - 1
    distance_between_cells = cell_size + divider_size
    m = cell_size * n_cells + divider_size * n_dividers
    grid = np.full((m, m), Color.BLACK)

    # Add dividers
    for i in range(n_dividers):
        grid[cell_size + i * (cell_size + divider_size), :] = divider_color
        grid[:, cell_size + i * (cell_size + divider_size)] = divider_color

    # Pick one cell to have exactly 5 colors (the guide cell)
    guide_cell_x, guide_cell_y = np.random.randint(3), np.random.randint(3)

    for x in range(3):
        for y in range(3):
            if x == guide_cell_x and y == guide_cell_y:
                n_colors = 5
            else:
                n_colors = np.random.randint(3, 6)  # 3 to 5 colors

            cell = grid[x*distance_between_cells : x*distance_between_cells + cell_size,
                        y*distance_between_cells : y*distance_between_cells + cell_size]

            while np.sum(cell != Color.BLACK) < n_colors:
                cell_x, cell_y = np.random.randint(cell_size), np.random.randint(cell_size)
                cell[cell_x, cell_y] = random.choice([color for color in Color.ALL_COLORS if color != Color.BLACK and color != divider_color])

    return grid