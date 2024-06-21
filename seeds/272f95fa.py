from common import *

import numpy as np
from typing import *


# concepts:
# filling, intersection, horizontal/vertical bars

# description:
# In the input you will see a grid with two horizontal and two vertical teal bars with a black background.
# For each partitioned section in the grid, fill in the top, left, bottom, right, and middle sections with red, yellow, blue, green, and pink, respectively. Ignore the corner sections.

def main(input_grid):
    # first get the grid size
    n, m = input_grid.shape

    # before we can find the partitions, we need to recolor them to not be black, such as grey, so we can find the connected components
    input_grid[input_grid == Color.BLACK] = Color.GREY

    # find the connected components in the grid with teal as the background color, giving us the partitions
    partitions = find_connected_components(input_grid, background=Color.TEAL, connectivity=4, monochromatic=True)
    
    # for each partition, if it is one of the top, left, bottom, right, or middle sections, fill it with the appropriate color, otherwise recolor it to black
    for partition in partitions:
        # get the bounding box of the partition and set the max x and y values
        min_x, min_y, width, height = bounding_box(partition)
        max_x = min_x + width - 1
        max_y = min_y + height - 1

        # if the partition is in the top row and not touching either edge of the grid, fill that section with red
        if min_y == 0 and min_x > 0 and max_x < n - 1:
            flood_fill(input_grid, min_x, min_y, Color.RED)
        # else, if the partition is on the bottom row and not touching either edge of the grid, fill that section with blue
        elif max_y == m - 1 and min_x > 0 and max_x < n - 1:
            flood_fill(input_grid, min_x, min_y, Color.BLUE)
        # else, if it is in the middle row, then we need to check if it is touching the left, right, or neither edge of the grid
        elif min_y > 0 and max_y < m - 1:
            # if the partition is touching the left edge of the grid, fill it with yellow
            if min_x == 0:
                flood_fill(input_grid, min_x, min_y, Color.YELLOW)
            # else, if the partition is touching the right edge of the grid, fill it with green
            elif max_x == n - 1:
                flood_fill(input_grid, min_x, min_y, Color.GREEN)
            # otherwise, fill the partition with pink
            else:
                flood_fill(input_grid, min_x, min_y, Color.PINK)
        # else, the partition is not one of the sections we need to fill, so recolor it to black
        else:
            flood_fill(input_grid, min_x, min_y, Color.BLACK)
        
    return input_grid


def generate_input():
    # first create a grid with a black background somewhere between 12x12 and 20x20
    n = random.randint(12, 20)
    m = random.randint(12, 20)
    grid = np.full((n, m), Color.BLACK)

    # now we need to add the two horizontal/vertical teal bars spanning the grid, making sure they are not touching the edges of the grid and have at least one empty row/column between them
    # both bars can be somewhere between row 1 and row m - 2/column 1 and column n - 2, however, the second bar must be at least 2 rows/columns away from the first bar
    bar1_y = random.randint(1, m - 2)
    bar2_y = random.choice([y for y in range(1, m - 2) if abs(y - bar1_y) >= 2])
    bar1_x = random.randint(1, n - 2)
    bar2_x = random.choice([x for x in range(1, n - 2) if abs(x - bar1_x) >= 2])

    # now that we have the positions of the bars, we can draw them on the grid
    draw_line(grid, 0, bar1_y, length=None, color=Color.TEAL, direction=(1, 0))
    draw_line(grid, bar1_x, 0, length=None, color=Color.TEAL, direction=(0, 1))
    draw_line(grid, 0, bar2_y, length=None, color=Color.TEAL, direction=(1, 0))
    draw_line(grid, bar2_x, 0, length=None, color=Color.TEAL, direction=(0, 1))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)