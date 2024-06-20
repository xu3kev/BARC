from common import *

import numpy as np
from typing import *

# concepts:
# Identifying area separated by lines.

# description:
# In the input, you will be given a square grid with some non-consecutive horizontal and vertical lines.
# In the output, you want to identify the number of areas separated by these lines and put them into a grid.
# For example, if the grid is horizontally separated into n areas and vertically separated into m areas, then output
# a nxm grid.


def main(input_grid):
    line_color = Color.BLACK
    background = Color.BLACK
    col_not_line = np.zeros(input_grid.shape[1], dtype=int)
    row_not_line = np.zeros(input_grid.shape[0], dtype=int)
    # Find line color and background color
    for x in range(input_grid.shape[0]):
        # Check if every element in the column is the same
        if np.all(input_grid[x, :] == input_grid[x, 0]):
            line_color = input_grid[x, 0]
        else:
            col_not_line = input_grid[x, :]
        # If we found both, break
        if line_color != Color.BLACK and not np.all(col_not_line == 0):
            break

    # Finds a not line row
    for y in range(input_grid.shape[1]):
        if not np.all(input_grid[:, y] == input_grid[0, y]):
            row_not_line = input_grid[:, y]
            break

    # Count the number of areas separated by the vertical lines by looking at a not line row.
    n_areas_vertical = 0
    prev = False
    for x in range(row_not_line.shape[0]):
        if row_not_line[x] != line_color:
            background = row_not_line[x]
            if not prev:
                n_areas_vertical += 1
            prev = True
        else:
            prev = False

    # Count number of area separated by the horizontal lines by looking at a not line column.
    n_areas_horizontal = 0

    prev = False
    for x in range(col_not_line.shape[0]):
        if col_not_line[x] != line_color:
            if not prev:
                n_areas_horizontal += 1
            prev = True
        else:
            prev = False

    # Create output grid
    output_grid = np.full((n_areas_vertical, n_areas_horizontal), background, dtype=int)

    return output_grid


def generate_input():
    # Picking background and line colors
    [background, lines] = random.sample(list(Color.NOT_BLACK), k=2)
    # Creating the background grid
    n = random.randint(11, 21)
    grid = np.full((n, n), background, dtype=int)

    # Creating a line sprite
    vertical_line_sprite = np.zeros((1, n - 2), dtype=int)
    draw_line(vertical_line_sprite, 0, 0, n - 2, lines, (0, 1))
    horizontal_line_sprite = np.zeros((n - 2, 1), dtype=int)
    draw_line(horizontal_line_sprite, 0, 0, n - 2, lines, (1, 0))

    # Picking how many lines to have in each dimension
    line_n, line_m = random.randint(0, n // 3), random.randint(0, n // 3)
    vertical_line_grid = grid.copy()

    for i in range(line_n):
        x, y = random_free_location_for_object(
            vertical_line_grid,
            vertical_line_sprite,
            background=background,
            border_size=1,
        )
        blit(vertical_line_grid, vertical_line_sprite, x, y)

    # Draw horizontal lines
    for i in range(line_m):
        x, y = random_free_location_for_object(
            grid, horizontal_line_sprite, background=background, border_size=1
        )
        blit(grid, horizontal_line_sprite, x, y)

    show_colored_grid(grid)
    show_colored_grid(vertical_line_grid)
    # Combine the two line grids
    blit(grid, vertical_line_grid, background=background)
    show_colored_grid(grid)
    """
    # Draw vertical lines (except endpoints)
    possible_index = np.arange(1, n - 1, 1)
    for i in range(line_n):
        draw_ind = random.choice(list(possible_index))
        draw_line(grid, draw_ind, 0, n, lines, (0, 1))
        possible_index = possible_index[
            (possible_index != draw_ind)
            & (possible_index != draw_ind + 1)
            & (possible_index != draw_ind - 1)
        ]
    
    # Draw horizontal lines (except endpoints)
    possible_index = np.arange(1, n - 1, 1)
    for i in range(line_m):
        draw_ind = random.choice(list(possible_index))
        draw_line(grid, 0, draw_ind, n, lines, (1, 0))
        possible_index = possible_index[
            (possible_index != draw_ind)
            & (possible_index != draw_ind + 1)
            & (possible_index != draw_ind - 1)
        ]
    """
    return grid[1:-1, 1:-1]


# ============= remove below this point for prompting =============
if __name__ == "__main__":
    visualize(generate_input, main)
