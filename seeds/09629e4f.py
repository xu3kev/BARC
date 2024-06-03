from common import *

import numpy as np
from typing import *

black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

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
            cell = input_grid[4*x:4*(x+1)-1, 4*y:4*(y+1)-1]
            if np.sum(cell != black) == 4:
                assert special_cell is None, "More than one special cell found"
                special_cell = cell

    output_grid = np.zeros_like(input_grid)

    # create grey horizontal and vertical bars, making 9 empty cells that we will later fill in with the special cell's colors as a guide
    # 3x3 cells, so 2 horizontal/vertical dividers
    for i in range(2): 
        output_grid[3*(i+1)+i, :] = grey
        output_grid[:, 3*(i+1)+i] = grey

    # fill in the cells with the special cell's colors
    for x in range(3):
        for y in range(3):
            cell = output_grid[4*x:4*(x+1)-1, 4*y:4*(y+1)-1]
            cell[:,:] = special_cell[x, y]

    return output_grid



def generate_input() -> np.ndarray:
    
    divider_color = grey

    # make the dividers, which comprise horizontal/vertical bars creating 3x3 cells, with 3 cells in each direction
    grid = np.zeros((3*3+2, 3*3+2), dtype=int)
    for i in range(2):
        # horizontal dividers
        grid[3*(i+1)+i, :] = divider_color
        # vertical dividers
        grid[:, 3*(i+1)+i] = divider_color
    
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
            # the last -1 is to exclude the divider
            cell = grid[4*x:4*(x+1)-1, 4*y:4*(y+1)-1]

            # color the cell by picking random positions and random colors until we have enough colored pixels
            while np.sum(cell!=black) < n_colors:
                # pick a random spot to color
                x_, y_ = np.random.randint(3), np.random.randint(3)
                cell[x_, y_] = random.choice([color for color in range(10) if color != black and color != divider_color])

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)