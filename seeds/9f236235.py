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
    # Plan:
    # 1. Determine the color of the separator between the regions
    # 2. Extract all the regions separated by the separator color
    # 3. Find the region positions and their possible X/Y positions
    # 4. Create the output grid so that one pixel represents the original region, preserving X/Y ordering
    # 5. Mirror the output grid by x-axis

    # 1. Find the color of horizontal and vertical bars that separate the different regions/cells/partitions
    # One way of doing this is to find the connected component which stretches all the way horizontally and vertically over the input
    separator_candidates = [ possible_separator
                            for possible_separator in find_connected_components(grid=input_grid, connectivity=4, monochromatic=True, background=Color.BLACK)
                            if crop(possible_separator).shape == input_grid.shape ]
    assert len(separator_candidates) == 1, "There should be exactly 1 separator partitioning the input"
    separator = separator_candidates[0]
    separator_color = object_colors(separator, background=Color.BLACK)[0]

    # 2. Extract all the regions separated by the separator color
    regions = find_connected_components(grid=input_grid, connectivity=4, monochromatic=True, background=separator_color)

    # 3. Find the region positions
    x_positions = { object_position(obj, background=separator_color)[0] for obj in regions }
    y_positions = { object_position(obj, background=separator_color)[1] for obj in regions }

    # 4. Create the output grid, each region becomes a single pixel

    # Get the size of the output
    width = len(x_positions)
    height = len(y_positions)    

    # Create the output grid
    # Use one pixel to represent the original region
    output_grid = np.full((width, height), Color.BLACK)
    for output_x, input_x in enumerate(sorted(x_positions)):
        for output_y, input_y in enumerate(sorted(y_positions)):
            for region in regions:
                if object_position(region, background=separator_color) == (input_x, input_y):
                    output_grid[output_x, output_y] = object_colors(region, background=separator_color)[0]
                    break

    # 5. Mirror the output grid by x-axis
    output_grid = np.flip(output_grid, axis=0)

    return output_grid

def generate_input():
    # Randomly choose the number of regions that are going to form the output canvas
    w, h = np.random.randint(3, 6), np.random.randint(3, 6)
    # Keep track of the color of each region
    region_colors = np.full((w, h), Color.BLACK)

    # Randomly choose the colors. the separator gets a special color and colored regions get a color randomly selected from other_colors
    num_other_colors = np.random.randint(1, 4)
    separator_color, *other_colors = np.random.choice(Color.NOT_BLACK, num_other_colors + 1, replace=False)

    # Randomly color the regions
    for x, y in np.ndindex(w, h):
        # Randomly determine if the cell should be colored
        if np.random.choice([True, False]):
            # Randomly choose the color
            region_colors[x, y] = np.random.choice(other_colors)
    
    # Randomly choose the scale factor and scale the regions so that they are bigger than just a single pixel
    scale_factor = np.random.randint(3, 6)
    grid = scale_sprite(region_colors, scale_factor)
    
    # Draw horizontal/vertical lines to separate the colors
    interval = scale_factor
    # First draw vertical lines
    for x in range(interval, w * scale_factor, interval):
        draw_line(grid, x=x, y=0, direction=(0, 1), color=separator_color)
    # Then draw horizontal lines
    for y in range(interval, h * scale_factor, interval):
        draw_line(grid, x=0, y=y, direction=(1, 0), color=separator_color)
    
    # drop the extra pixels
    grid = grid[1:,1:]

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
