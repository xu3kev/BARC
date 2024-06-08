from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, flood fill, connecting same color

# description:
# In the input you will see horizontal and vertical bars that divide the grid into rectangular cells
# To make the output, find any pair of rectangular cells that are in the same row and column and have the same color, then color all the rectangular cells between them with that color

def main(input_grid: np.ndarray) -> np.ndarray:

    # find the color of the horizontal and vertical bars that divide the rectangular cells
    # this is the color of any line that extends all the way horizontally or vertically
    jail_color = None
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            color = input_grid[i][j]
            if np.all(input_grid[i, :] == color) or np.all(input_grid[:, j] == color):
                jail_color = color
                break
    
    assert jail_color is not None, "No jail color found"

    output_grid = input_grid.copy()

    # color all the cells between the same color pixels
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            color = input_grid[x][y]
            if color == jail_color or color == Color.BLACK:
                continue

            # check if there is a cell with the same color in the same X value
            for y2 in range(y+1, input_grid.shape[1]):
                if input_grid[x][y2] == color:
                    for y3 in range(y+1, y2):
                        if input_grid[x][y3] == Color.BLACK:
                            output_grid[x][y3] = color
                    break

            # check if there is a cell with the same color in the same Y value
            for x2 in range(x+1, input_grid.shape[0]):
                if input_grid[x2][y] == color:
                    for x3 in range(x+1, x2):
                        if input_grid[x3][y] == Color.BLACK:
                            output_grid[x3][y] = color
                    break
                
    return output_grid

def generate_input() -> np.ndarray:

    grid_size = 32
    cell_size = 2

    # First create the array of rectangular cells, each of which is separated by horizontal and vertical bars dividing cells

    # pick a non-black color for the divider
    divider_color = random.choice(Color.NOT_BLACK)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    r_offset_x, r_offset_y = np.random.randint(0, cell_size), np.random.randint(0, cell_size)

    # make horizontal bars with cell_size gaps, but +1 because we need to include the divider, which is one pixel wide
    for x in range(r_offset_x, grid_size, cell_size+1):
        grid[x, :] = divider_color
    # make vertical bars with cell_size gaps
    for y in range(r_offset_y, grid_size, cell_size+1):
        grid[:, y] = divider_color

    # Second we will color some of the cells with a random color

    # random number of cells to color
    number_to_color = np.random.randint(1, 4)
    for _ in range(number_to_color):
        # pick what we're going to color the inside of the cell, which needs to be a different color from the divider
        other_color = np.random.choice([c for c in Color.ALL_COLORS if c != divider_color and c != Color.BLACK])

        # get all coords of black cells
        black_coords = np.argwhere(grid == Color.BLACK)
        # pick a random black cell
        x, y = random.choice(black_coords)
        flood_fill(grid, x, y, other_color)

        # sometimes skip coloring the other side of the divider
        if random.random() <= 0.2:
            continue 

        # flip a coin to decide if horizontal or vertical
        h_or_v = random.random() < 0.5
        if h_or_v:
            # horizontal
            # get all the black cells in the same row
            black_coords = np.argwhere(grid[x, :] == Color.BLACK)
            # pick a random black cell
            other_y = random.choice(black_coords)
            flood_fill(grid, x, other_y, other_color)
        else:
            # vertical
            # get all the black cells in the same column
            black_coords = np.argwhere(grid[:, y] == Color.BLACK)
            # pick a random black cell
            other_x = random.choice(black_coords)
            flood_fill(grid, other_x, y, other_color)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)