from common import *

import numpy as np
from typing import *

# concepts:
# downscaling, mirror, horizontal/vertical bars

# description:
# In the input you will see horizontal and vertical bars separating different regions/cells/partitions with each cell containing different colors, like a chessboard.
# Each separated region has a single color.
# To make the output, make a grid with one colored pixel for each region of the chessboard.
# Finally mirror along the x-axis.

def main(input_grid):
    # Find the color of horizontal and vertical bars that separate the different regions/cells/partitions
    line_candidates = find_connected_components(grid=input_grid, connectivity=4, monochromatic=True, background=Color.BLACK)
    line_candidates = sorted(line_candidates, key=lambda x: crop(x).shape[0] * crop(x).shape[1], reverse=True)

    # The grid lines spread across the whole grid
    line_grid = line_candidates[0]
    line_color = object_colors(line_grid)[0]

    # Extract all the squares separated by the grid lines
    squares = find_connected_components(grid=input_grid, connectivity=4, monochromatic=True, background=line_color)

    # Sort the squares by their position
    squares = sorted(squares, key=lambda x: object_position(obj=x, background=line_color)[0])
    squares = sorted(squares, key=lambda x: object_position(obj=x, background=line_color)[1])

    # Get the size of the output chessboard
    w = np.unique([object_position(obj=x, background=line_color)[0] for x in squares]).shape[0]
    h = np.unique([object_position(obj=x, background=line_color)[1] for x in squares]).shape[0]

    # Create the output grid
    # Use one pixel to represent the original region
    output_grid = np.full((w, h), Color.BLACK)
    for i, square in enumerate(squares):
        cur_color = object_colors(obj=square, background=line_color)[0]
        output_grid[i % w, i // w] = cur_color

    # Mirror the output grid by x-axis
    output_grid = np.flip(output_grid, axis=0)

    return output_grid

def generate_input():
    # Randomly choose the pattern size
    w, h = np.random.randint(3, 6), np.random.randint(3, 6)
    pattern = np.full((w, h), Color.BLACK)

    # Randomly choose the color size
    num_color = np.random.randint(1, 4)
    colors = np.random.choice(Color.NOT_BLACK, num_color + 1, replace=False)
    pattern_colors = colors[1:]
    line_color = colors[0]

    # Randomly color the pattern
    for x, y in np.ndindex(w, h):
        # Randomly determine if the cell should be colored
        if_color = np.random.choice([True, False])
        if if_color:
            # Randomly choose the color
            pattern[x, y] = np.random.choice(pattern_colors)
    
    # Randomly choose the scale factor and scale the pattern
    scale_factor = np.random.randint(3, 6)
    scaled_pattern = scale_sprite(pattern, scale_factor)
    
    # Draw lines to separate the colors
    interval = scale_factor
    # First draw vertical lines
    for i in range(0, w * scale_factor, interval):
        draw_line(grid=scaled_pattern, x=i, y=0, direction=(0, 1), color=line_color)
    # Then draw horizontal lines
    for j in range(0, h * scale_factor, interval):
        draw_line(grid=scaled_pattern, x=0, y=j, direction=(1, 0), color=line_color)
    
    # Get rid of the border
    grid = scaled_pattern[1:, 1:]

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
