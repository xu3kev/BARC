from common import *

import numpy as np
from typing import *

# concepts:
# objects, flood fill, connectivity, color, borders

# description:
# In the input, you will see a black grid with a blue line that starts from a random point on the left side of the grid and moves in a random walk until it reaches any other border of the grid.
# To make the output:
# 1. Find all enclosed regions created by the blue line.
# 2. For each region, count the number of border pixels it touches (top, bottom, left, or right of the grid).
# 3. Color the regions based on their border count:
#    - 0 borders: Leave black
#    - 1 border: Color red
#    - 2 borders: Color green
#    - 3 borders: Color yellow
#    - 4 borders: Color orange (this should be rare or impossible in most cases)

def main(input_grid):
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find enclosed regions
    regions = find_connected_components(input_grid, connectivity=4, background=Color.BLUE)

    for region in regions:
        # Count border pixels
        left_border = np.any(region[:, 0] == Color.BLACK)
        right_border = np.any(region[:, -1] == Color.BLACK)
        top_border = np.any(region[0, :] == Color.BLACK)
        bottom_border = np.any(region[-1, :] == Color.BLACK)
        
        border_count = sum([left_border, right_border, top_border, bottom_border])

        # Determine color based on border count
        if border_count == 1:
            fill_color = Color.RED
        elif border_count == 2:
            fill_color = Color.GREEN
        elif border_count == 3:
            fill_color = Color.YELLOW
        elif border_count == 4:
            fill_color = Color.ORANGE
        else:
            fill_color = Color.BLACK  # Keep it black if it doesn't touch any border

        # Fill the region with the determined color
        if fill_color != Color.BLACK:
            x, y = np.where(region == Color.BLACK)
            flood_fill(output_grid, x[0], y[0], fill_color)

    return output_grid

def generate_input():
    # Create a black grid with random dimensions
    height = np.random.randint(8, 15)
    width = np.random.randint(15, 25)
    grid = np.zeros((height, width), dtype=int)

    # Choose a random starting point on the left border
    start_y = np.random.randint(height)
    x, y = 0, start_y

    # Perform random walk until reaching another border
    while 0 < x < width - 1 and 0 < y < height - 1:
        grid[y, x] = Color.BLUE
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0)])
        x += dx
        y += dy

    # Ensure the last pixel is also blue
    grid[y, x] = Color.BLUE

    return grid