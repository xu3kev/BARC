from common import *

import numpy as np
from typing import *


# concepts:
# rectangular cells, color guide, pixel manipulation

# description:
# In the input you will see grey horizontal and vertical bars that divide the grid into nine 3x3 rectangular regions. Each region contains a random pattern of colored pixels.
# To make the output, locate the region that has the color pattern that forms a cross (one horizontal and one vertical line intersecting in the middle). 
# Reflect this region about the center and color all the other regions using this reflected pattern.

def main(input_grid: np.ndarray) -> np.ndarray:
    
    # Extracting divider color
    divider_colors = [ input_grid[x,y] for x in range(input_grid.shape[0]) for y in range(input_grid.shape[1])
                      if np.all(input_grid[x,:] == input_grid[x,0]) or np.all(input_grid[:,y] == input_grid[0,y]) ]
    assert len(set(divider_colors)) == 1, "There should be exactly one divider color"
    divider_color = divider_colors[0]
      
    regions = find_connected_components(input_grid, background=divider_color, monochromatic=False)
    locations = []
    
    for region in regions:
        x, y, w, h = bounding_box(region, background=divider_color)
        locations.append((x, y, region))
        
    grid_of_regions = []
    for x, y, region in locations:
        num_left_of_region = len({other_x for other_x, other_y, other_region in locations if other_x < x})
        num_above_region = len({other_y for other_x, other_y, other_region in locations if other_y < y})
        grid_of_regions.append((num_left_of_region, num_above_region, region))
    
    # Find the region with the cross pattern
    cross_pattern = np.array([
        [False, True, False],
        [True,  True, True],
        [False, True, False]
    ])
    
    special_region = None
    for region in regions:
        region_cropped = crop(region, background=divider_color)
        check_pattern = (region_cropped != divider_color) & (region_cropped != Color.BLACK)
        if np.array_equal(check_pattern, cross_pattern):
            assert special_region is None, "More than one special region found"
            special_region = region_cropped
    
    # Reflect the special region about its center
    reflected_pattern = np.rot90(special_region, 2)
        
    # Create the output grid
    output_grid = np.zeros_like(input_grid)
    output_grid[input_grid == divider_color] = divider_color  # Retain the dividers
    
    # Fill regions with reflected pattern and place dividers back
    for x, y, region in grid_of_regions:
        output_grid[region != divider_color] = reflected_pattern[x, y]
        
    return output_grid

def generate_input() -> np.ndarray:
    
    divider_color = Color.GRAY

    # make the dividers, which comprise horizontal/vertical bars creating 3x3 cells, with 3 cells in each direction
    cell_size = 3
    n_cells = 3
    divider_size = 1
    n_dividers = n_cells - 1
    distance_between_cells = cell_size + divider_size
    m = cell_size*n_cells + divider_size*n_dividers
    grid = np.full((m, m), Color.BLACK)
    for i in range(n_dividers):
        # horizontal dividers
        grid[cell_size + i*(cell_size + divider_size), :] = divider_color
        # vertical dividers
        grid[:, cell_size + i*(cell_size + divider_size)] = divider_color
    
    # Choose one cell to have the cross pattern
    cross_cell_x, cross_cell_y = np.random.randint(3), np.random.randint(3)
    
    # Generate the cross pattern in the chosen cell
    cross_x_start, cross_y_start = cross_cell_x * distance_between_cells, cross_cell_y * distance_between_cells
    grid[cross_x_start:cross_x_start + cell_size, cross_y_start + 1] = Color.BLUE
    grid[cross_x_start + 1, cross_y_start:cross_y_start + cell_size] = Color.BLUE
    
    for x in range(3):
        for y in range(3):
            if x == cross_cell_x and y == cross_cell_y:
                continue
            
            n_colors = np.random.randint(4, 6)

            # Extract view of the cell
            cell = grid[x*distance_between_cells : x*distance_between_cells + cell_size,
                        y*distance_between_cells : y*distance_between_cells + cell_size]

            while np.sum(cell != Color.BLACK) < n_colors:
                cell_x, cell_y = np.random.randint(cell_size), np.random.randint(cell_size)
                cell[cell_x, cell_y] = np.random.choice([color for color in Color.ALL_COLORS if color != Color.BLACK and color != divider_color])

    return grid