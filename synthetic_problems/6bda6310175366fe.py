from common import *
import numpy as np

# concepts:
# lines, counting

# description:
# In the input, you will see a grid with one or more vertical green lines extending from the top to the bottom of the grid.
# To make the output, count the number of vertical green lines and create an output grid of size 1xN where N is the count of green lines, filling this row with green pixels.

def main(input_grid):
    n, m = input_grid.shape
    green_line_count = 0

    # Count the number of vertical green lines
    for x in range(m):
        if np.all(input_grid[:, x] == Color.GREEN):
            green_line_count += 1

    # Create the output grid of size 1xN where N is the green line count
    output_grid = np.zeros((1, green_line_count), dtype=int)
    output_grid[:, :] = Color.GREEN

    return output_grid

def generate_input():
    # Make a random grid size between 5 and 10 for width (number of columns) and fixed height of 5
    n = 5
    m = np.random.randint(5, 11)
    grid = np.zeros((n, m), dtype=int)

    # Randomly decide on the number of green vertical lines (between 1 and the total number of columns)
    num_green_lines = np.random.randint(1, m + 1)
    green_columns = np.random.choice(m, num_green_lines, replace=False)

    # Draw vertical green lines at the chosen columns
    for col in green_columns:
        draw_line(grid, 0, col, length=n, color=Color.GREEN, direction=(1, 0))

    return grid