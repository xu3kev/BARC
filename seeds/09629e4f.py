from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, color guide

# description:
# In the input you will see grey horizontal and vertical bars that divide the grid into nine 3x3 rectangular regions, each of which contains 4-5 colored pixels
# To make the output, find the region that has exactly 4 colored pixels, and use its colors as a guide to fill in all the other cells

def main(input_grid: np.ndarray) -> np.ndarray:

    # First identify 

    # Trick for decomposing inputs divided into rectangular regions by horizontal/vertical bars:
    # Treat the bar color as the background, and break the input up into connected components with that background color

    # The divider color is the color of the horizontal and vertical bars
    divider_colors = [ input_grid[x,y] for x in range(input_grid.shape[0]) for y in range(input_grid.shape[1])
                     if np.all(input_grid[x,:] == input_grid[x,0]) or np.all(input_grid[:,y] == input_grid[0,y]) ]
    assert len(set(divider_colors)) == 1, "There should be exactly one divider color"
    divider_color = divider_colors[0] # background=divider_color

    # Find multicolored regions, which are divided by divider_color, so we treat that as background, because it separates objects
    # Within each region there can be multiple colors
    regions = find_connected_components(input_grid, background=divider_color, monochromatic=False)
    # Tag the regions with their location within the 2D grid of (divided) regions
    # First get the bounding-box locations...
    locations = []
    for region in regions:
        x, y, w, h = bounding_box(region, background=divider_color)
        locations.append((x, y, region))
    # ...then re-index them so that (x, y) is the coordinate within the grid of rectangular regions
    grid_of_regions = []
    for x, y, region in locations:
        num_left_of_region = len({other_x for other_x, other_y, other_region in locations if other_x < x})
        num_above_region = len({other_y for other_x, other_y, other_region in locations if other_y < y})
        grid_of_regions.append((num_left_of_region, num_above_region, region))

    # Find the region with exactly 4 colors
    special_region = None
    for region in regions:
        not_divider_and_not_black = (region != divider_color) & (region != Color.BLACK)
        if np.sum(not_divider_and_not_black) == 4:
            assert special_region is None, "More than one special region found"
            special_region = region
    
    # Convert to a sprite
    special_sprite = crop(special_region, background=divider_color)
    
    # Create the output grid
    output_grid = np.zeros_like(input_grid)

    # Put the dividers back in
    output_grid[input_grid == divider_color] = divider_color

    # Fill in the cells with the special colors
    for x, y, region in grid_of_regions:
        output_grid[region != divider_color] = special_sprite[x, y]

    return output_grid



def generate_input() -> np.ndarray:
    
    divider_color = Color.GRAY

    # make the dividers, which comprise horizontal/vertical bars creating 3x3 cells, with 3 cells in each direction
    cell_size = 3
    n_cells = 3
    divider_size = 1 # the divider is a single pixel
    n_dividers = n_cells - 1
    distance_between_cells = cell_size + divider_size
    m = cell_size*n_cells + divider_size*n_dividers
    grid = np.full((m, m), Color.BLACK)
    for i in range(n_dividers):
        # horizontal dividers
        grid[cell_size + i*(cell_size + divider_size), :] = divider_color
        # vertical dividers
        grid[:, cell_size + i*(cell_size + divider_size)] = divider_color
    
    # pick one of the cells to have exactly 4 colors (the others will have 5)
    special_cell_x, special_cell_y = np.random.randint(3), np.random.randint(3)

    for x in range(3):
        for y in range(3):
            if x == special_cell_x and y == special_cell_y:
                n_colors = 4
            else:
                n_colors = 5

            # extract view of the cell
            # each of the cells is 3x3, but there is a divider in between them, so they are actually 4x4 apart
            cell = grid[x*distance_between_cells : x*distance_between_cells + cell_size,
                        y*distance_between_cells : y*distance_between_cells + cell_size]

            # color the cell by picking random positions and random colors until we have enough colored pixels
            while np.sum(cell!=Color.BLACK) < n_colors:
                # pick a random spot to color
                cell_x, cell_y = np.random.randint(cell_size), np.random.randint(cell_size)
                cell[cell_x, cell_y] = random.choice([color for color in Color.ALL_COLORS if color != Color.BLACK and color != divider_color])

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)