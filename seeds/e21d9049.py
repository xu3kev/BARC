from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation, expand

# description:
# In the input you will see a grid with a cross pattern, each line's pixel has alternating colors.
# To make the output, you should expand the cross to the right, left, top, and bottom follow the color 
# of the cross's original color sequence.

def main(input_grid):
    # Create output grid
    output_grid = input_grid.copy()
    n, m = input_grid.shape

    # Extract the pattern
    pattern = find_connected_components(input_grid, monochromatic=False)[0]

    # Detect the row and column that contain lines
    cropped_pattern = crop(pattern)
    for x in range(cropped_pattern.shape[0]):
        if np.all(cropped_pattern[x, :] != Color.BLACK):
            break
    for y in range(cropped_pattern.shape[1]):
        if np.all(cropped_pattern[:, y] != Color.BLACK):
            break
    vertical_line = np.array([cropped_pattern[x, :]])
    horizontal_line = np.array([cropped_pattern[:, y]]).T
    
    x_pattern, y_pattern = object_position(pattern)

    # STEP 1: expand the horizontal line to the right and left
    x_start, y_start, len_line = x_pattern, y_pattern + y, cropped_pattern.shape[0]
    for i in range(x_start, n, len_line):
        blit_sprite(output_grid, horizontal_line, x=i, y=y_start)
    for i in range(x_start, -(len_line), -len_line):
        blit_sprite(output_grid, horizontal_line, x=i, y=y_start)
    
    # STEP 2: expand the vertical line to the top and bottom
    x_start, y_start, len_line = x_pattern + x, y_pattern, cropped_pattern.shape[1]
    for i in range(y_start, m, len_line):
        blit_sprite(output_grid, vertical_line, x=x_start, y=i)
    for i in range(y_start, -(len_line), -len_line):
        blit_sprite(output_grid, vertical_line, x=x_start, y=i)
        
    return output_grid

def generate_input():
    # Generate the background grid
    n, m = np.random.randint(20, 30, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose the number of colors
    num_colors = np.random.randint(2, 5)
    colors = np.random.choice(Color.NOT_BLACK, size=num_colors, replace=False)

    # Generate a line with these colors in sequence
    line = np.zeros((num_colors, 1), dtype=int)
    for i in range(num_colors):
        line[i, 0] = colors[i]

    # form a cross pattern randomly
    cross_points = random.randint(0, num_colors - 1)
    pattern = np.zeros((num_colors, num_colors), dtype=int)
    line_t = np.transpose(line)
    blit_sprite(pattern, line, x=0, y=cross_points)
    blit_sprite(pattern, line_t, x=cross_points, y=0)

    # Randomly rotate the pattern
    pattern = np.rot90(pattern, k=np.random.randint(4))

    # Randomly place the pattern on the grid
    x, y = random_free_location_for_sprite(grid=grid, sprite=pattern)
    blit_sprite(grid, pattern, x=x, y=y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
