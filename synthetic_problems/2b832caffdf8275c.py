from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, surrounding, flood fill, connecting same color

# description:
# In the input, you will have rectangular cells divided by bars (in a specific divider color). 
# Inside some cells there are squares of different colors. 
# The output should have each square surrounded by a border of its own color.

def main(input_grid: np.ndarray) -> np.ndarray:

    # find the color of the horizontal and vertical bars that divide the rectangular cells
    # this is the color of any line that extends all the way horizontally or vertically
    divider_color = None
    for i in range(input_grid.shape[0]):
        if np.all(input_grid[i, :] == input_grid[i, 0]):
            divider_color = input_grid[i, 0]
            break
    if not divider_color:
        for j in range(input_grid.shape[1]):
            if np.all(input_grid[:, j] == input_grid[0, j]):
                divider_color = input_grid[0, j]
                break

    assert divider_color, "No divider color found"

    output_grid = input_grid.copy()

    # Go through each cell. If a cell includes a square, surround it with a border of the same color.
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            color = input_grid[x][y]
            if color != Color.BLACK and color != divider_color:
                expand_color_border(output_grid, x, y, color, divider_color)

    return output_grid


def expand_color_border(grid: np.ndarray, x: int, y: int, color: int, divider_color: int):
    rows, cols = grid.shape
    for i in range(max(0, x-1), min(rows, x+2)):
        for j in range(max(0, y-1), min(cols, y+2)):
            if grid[i, j] == divider_color or (i == x and j == y):
                continue
            if grid[i, j] == Color.BLACK:
                grid[i, j] = color


def generate_input() -> np.ndarray:
    grid_size = 32
    cell_size = 5

    # Create the array of rectangular cells with specific dividers.
    divider_color = random.choice(Color.NOT_BLACK)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    r_offset_x, r_offset_y = np.random.randint(0, cell_size), np.random.randint(0, cell_size)

    for x in range(r_offset_x, grid_size, cell_size + 1):
        grid[x, :] = divider_color
    for y in range(r_offset_y, grid_size, cell_size + 1):
        grid[:, y] = divider_color

    # Color random squares within those cells with different color than divider.
    number_to_color = np.random.randint(1, 6)
    for _ in range(number_to_color):
        square_color = np.random.choice([c for c in Color.ALL_COLORS if c != divider_color and c != Color.BLACK])
        
        black_coords = np.argwhere((grid == Color.BLACK) | (grid == divider_color))
        chosen_loc = random.choice(black_coords)
        x, y = chosen_loc[0], chosen_loc[1]
        
        # Ensure chosen location is surrounded by divider in a proper cell
        if grid[x, y] == Color.BLACK and (y-x) % (cell_size+1) == 0:
            grid[x, y] = square_color

    return grid