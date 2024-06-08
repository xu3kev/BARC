from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, color guide

# description:
# In the input you will see grey horizontal and vertical bars that divide the grid into nine 3x3 rectangular cells, each of which contains 4-5 colored pixels
# To make the output, find the cell that has exactly 4 colored pixels, and use its colors as a guide to fill in all the other cells

def main(input_grid: np.ndarray) -> np.ndarray:

    # find the cell with exactly 4 colors
    special_cell = None
    for x in range(3):
        for y in range(3):
            cell_size = 3
            distance_between_cells = cell_size + 1
            cell = input_grid[distance_between_cells*x : distance_between_cells*x + cell_size,
                              distance_between_cells*y : distance_between_cells*y + cell_size]
            if np.sum(cell != Color.BLACK) == 4:
                assert special_cell is None, "More than one special cell found"
                special_cell = cell

    output_grid = np.zeros_like(input_grid)

    # create grey horizontal and vertical bars, making 9 empty cells that we will later fill in with the special cell's colors as a guide
    # 3x3 cells, so 2 horizontal/vertical dividers
    for i in range(2): 
        output_grid[cell_size + i*distance_between_cells, :] = Color.GREY
        output_grid[:, cell_size + i*distance_between_cells] = Color.GREY

    # fill in the cells with the special cell's colors
    for x in range(3):
        for y in range(3):
            cell = output_grid[distance_between_cells*x : distance_between_cells*x + cell_size,
                               distance_between_cells*y : distance_between_cells*y + cell_size]
            cell[:,:] = special_cell[x, y]

    return output_grid



def generate_input() -> np.ndarray:
    
    divider_color = Color.GRAY

    # make the dividers, which comprise horizontal/vertical bars creating 3x3 cells, with 3 cells in each direction
    cell_size = 3
    n_cells = 3
    divider_size = 1 # the divider is a single pixel
    n_dividers = n_cells - 1
    distance_between_cells = cell_size + divider_size
    grid = np.zeros((cell_size*n_cells + divider_size*n_dividers), dtype=int)
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