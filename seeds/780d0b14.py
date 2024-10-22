from common import *

import numpy as np
from typing import *

# concepts:
# downscaling, rectangular partitions

# description:
# In the input you will see a grid consisting of a chessboard pattern (rectangular partitions) of different colors.
# Each rectangular partition region is incompletely scattered with a color. Regions are separated by black lines, going all the way top-bottom/left-right. 
# To make the output, make a grid with one color pixel for each colored rectangular region of the input.

def main(input_grid):
    # Plan:
    # 1. Partition the input into rectangular regions by finding all horizontal and vertical black lines
    # 2. For each region, find the color of the region
    # 3. Use one pixel to represent the original region and create the output grid

    # 1. Input parsing
    # Get the shape of the input grid
    width, height = input_grid.shape
    background = Color.BLACK
    # Find all horizontal and vertical lines
    vertical_lines = [ x for x in range(width) if np.all(input_grid[x, :] == background) ]
    horizontal_lines = [ y for y in range(height) if np.all(input_grid[:, y] == background) ]
    
    # Start from (0, 0)
    vertical_lines = [0] + vertical_lines
    horizontal_lines = [0] + horizontal_lines

    # Deduplicate successive lines
    vertical_lines = [x for i, x in enumerate(vertical_lines) if i == 0 or x != vertical_lines[i - 1]]
    horizontal_lines = [y for i, y in enumerate(horizontal_lines) if i == 0 or y != horizontal_lines[i - 1]]

    # use one pixel to represent the original region and create the output grid
    output_width, output_height = len(vertical_lines), len(horizontal_lines)
    output_grid = np.full((output_width, output_height), background) 

    # Initialize the output grid
    for i in range(len(vertical_lines)):
        for j in range(len(horizontal_lines)):
            # Get the region of the color
            x1 = vertical_lines[i]
            x2 = vertical_lines[i + 1] if i + 1 < len(vertical_lines) else width
            y1 = horizontal_lines[j]
            y2 = horizontal_lines[j + 1] if j + 1 < len(horizontal_lines) else height

            # Get the original region
            region = input_grid[x1:x2, y1:y2]
            # Get the color of the region
            color = object_colors(region, background=Color.BLACK)[0]
            # Use one pixel to represent the original region
            output_grid[i, j] = color

    return output_grid

def generate_input():
    # Randomly generate the grid size
    width, height = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.full((width, height), Color.BLACK)

    # Randomly select the grid separation
    n_region_horizontal, n_region_vertical = np.random.randint(2, 5), np.random.randint(2, 5)
    horizontal_region_boundaries = randomly_spaced_indices(max_len=width, n_indices=n_region_horizontal - 1, border_size=1, padding=2)
    vertical_region_boundaries = randomly_spaced_indices(max_len=height, n_indices=n_region_vertical - 1, border_size=1, padding=2)

    # Randomly select the colors to put in each region/partition
    colors = np.random.choice(Color.NOT_BLACK, (n_region_horizontal, n_region_vertical), replace=True)

    # Assign the colors to each partition
    # Big (X,Y) indexes the partition coordinates, not the canvas coordinates, which are little (x,y)
    for X in range(n_region_horizontal):
        for Y in range(n_region_vertical):
            # Get the region on the canvas
            # Note that the final region goes all the way to the width/height
            x1 = 0 if X == 0 else horizontal_region_boundaries[X-1]
            x2 = horizontal_region_boundaries[X] if X < len(horizontal_region_boundaries) else width
            y1 = 0 if Y == 0 else vertical_region_boundaries[Y-1]
            y2 = vertical_region_boundaries[Y] if Y < len(vertical_region_boundaries) else height

            # Each region is incomplete scattered color
            sprite = np.full((x2 - x1, y2 - y1), Color.BLACK)
            randomly_scatter_points(sprite, color=colors[X, Y], density=0.8)

            # Place the pattern in the grid
            blit_sprite(grid, sprite, x=x1, y=y1, background=Color.BLACK)

    # Draw black lines to separate the colors
    # First draw vertical lines
    for x in horizontal_region_boundaries:
        draw_line(grid=grid, x=x, y=0, direction=(0, 1), color=Color.BLACK)
        # equivalently: grid[x, :] = Color.BLACK

    # Then draw horizontal lines
    for y in vertical_region_boundaries:
        draw_line(grid=grid, x=0, y=y, direction=(1, 0), color=Color.BLACK)
        # equivalently: grid[:, y] = Color.BLACK

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
