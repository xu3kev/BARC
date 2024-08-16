from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, color guide, growing, surrounding

# description:
# In the input you will see grey horizontal and vertical bars that divide the grid into nine 3x3 rectangular regions.
# Each region contains 1-3 colored pixels.
# To make the output:
# 1. Find the region with exactly 1 colored pixel. This is the "seed" region.
# 2. For each other region:
#    a. If it has 2 colored pixels, grow those pixels outward until they touch or hit a wall.
#    b. If it has 3 colored pixels, surround each colored pixel with a 3x3 square of its color.
# 3. Finally, fill the seed region with copies of itself, rotated 90 degrees each time, to fill the 3x3 space.

def main(input_grid: np.ndarray) -> np.ndarray:
    divider_color = Color.GRAY
    
    # Find the regions
    regions = find_connected_components(input_grid, background=divider_color, monochromatic=False)
    
    # Create the output grid
    output_grid = np.zeros_like(input_grid)
    output_grid[input_grid == divider_color] = divider_color

    # Find the seed region (the one with exactly 1 colored pixel)
    seed_region = None
    for region in regions:
        colored_pixels = np.sum((region != divider_color) & (region != Color.BLACK))
        if colored_pixels == 1:
            seed_region = region
            break
    
    # Process each region
    for region in regions:
        x, y, w, h = bounding_box(region, background=divider_color)
        colored_pixels = np.sum((region != divider_color) & (region != Color.BLACK))
        
        if region is seed_region:
            # Fill seed region with rotated copies
            seed_color = region[(region != divider_color) & (region != Color.BLACK)][0]
            seed_pattern = np.full((3, 3), Color.BLACK)
            seed_pattern[1, 1] = seed_color
            for i in range(3):
                for j in range(3):
                    rotated = np.rot90(seed_pattern, k=(i+j)%4)
                    output_grid[x+i:x+i+3, y+j:y+j+3] = np.where(
                        (output_grid[x+i:x+i+3, y+j:y+j+3] == Color.BLACK) & (rotated != Color.BLACK),
                        rotated,
                        output_grid[x+i:x+i+3, y+j:y+j+3]
                    )
        elif colored_pixels == 2:
            # Grow pixels outward
            for i in range(w):
                for j in range(h):
                    if region[i, j] not in [Color.BLACK, divider_color]:
                        color = region[i, j]
                        draw_line(output_grid, x+i, y+j, None, color, (0, 1), [divider_color, color])
                        draw_line(output_grid, x+i, y+j, None, color, (0, -1), [divider_color, color])
                        draw_line(output_grid, x+i, y+j, None, color, (1, 0), [divider_color, color])
                        draw_line(output_grid, x+i, y+j, None, color, (-1, 0), [divider_color, color])
        elif colored_pixels == 3:
            # Surround each colored pixel with a 3x3 square
            for i in range(w):
                for j in range(h):
                    if region[i, j] not in [Color.BLACK, divider_color]:
                        color = region[i, j]
                        for di in range(-1, 2):
                            for dj in range(-1, 2):
                                if 0 <= x+i+di < output_grid.shape[0] and 0 <= y+j+dj < output_grid.shape[1]:
                                    if output_grid[x+i+di, y+j+dj] == Color.BLACK:
                                        output_grid[x+i+di, y+j+dj] = color

    return output_grid

def generate_input() -> np.ndarray:
    divider_color = Color.GRAY

    # Create the grid with dividers
    cell_size = 3
    n_cells = 3
    divider_size = 1
    n_dividers = n_cells - 1
    distance_between_cells = cell_size + divider_size
    m = cell_size*n_cells + divider_size*n_dividers
    grid = np.full((m, m), Color.BLACK)
    for i in range(n_dividers):
        grid[cell_size + i*(cell_size + divider_size), :] = divider_color
        grid[:, cell_size + i*(cell_size + divider_size)] = divider_color
    
    # Choose a random cell to be the seed (1 colored pixel)
    seed_x, seed_y = np.random.randint(3), np.random.randint(3)

    for x in range(3):
        for y in range(3):
            if x == seed_x and y == seed_y:
                n_colors = 1
            else:
                n_colors = np.random.randint(2, 4)  # 2 or 3 colors

            cell = grid[x*distance_between_cells : x*distance_between_cells + cell_size,
                        y*distance_between_cells : y*distance_between_cells + cell_size]

            positions = [(i, j) for i in range(cell_size) for j in range(cell_size)]
            np.random.shuffle(positions)
            
            for _ in range(n_colors):
                i, j = positions.pop()
                cell[i, j] = random.choice([color for color in Color.ALL_COLORS if color != Color.BLACK and color != divider_color])

    return grid