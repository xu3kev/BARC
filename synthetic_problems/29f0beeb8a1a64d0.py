from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, direction, color guide, symmetry

# description:
# In the input, you will see a black grid with two colored pixels on opposite corners: one blue and one red.
# There will also be several yellow pixels scattered throughout the grid.
# To make the output, imagine the blue and red pixels as magnets attracting the yellow pixels.
# Move each yellow pixel towards the closest colored corner (blue or red) until it reaches that corner.
# If a yellow pixel is equidistant from both corners, it should split into two pixels, one moving towards each corner.
# The path of each yellow pixel should be marked with a trail of green pixels.

def main(input_grid):
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the positions of blue and red pixels
    blue_pos = np.argwhere(input_grid == Color.BLUE)[0]
    red_pos = np.argwhere(input_grid == Color.RED)[0]

    # Find all yellow pixels
    yellow_pixels = np.argwhere(input_grid == Color.YELLOW)

    for y, x in yellow_pixels:
        # Calculate distances to blue and red corners
        dist_to_blue = np.abs(y - blue_pos[0]) + np.abs(x - blue_pos[1])
        dist_to_red = np.abs(y - red_pos[0]) + np.abs(x - red_pos[1])

        if dist_to_blue == dist_to_red:
            # Split the pixel and move towards both corners
            move_pixel(output_grid, y, x, blue_pos[0], blue_pos[1])
            move_pixel(output_grid, y, x, red_pos[0], red_pos[1])
        elif dist_to_blue < dist_to_red:
            move_pixel(output_grid, y, x, blue_pos[0], blue_pos[1])
        else:
            move_pixel(output_grid, y, x, red_pos[0], red_pos[1])

    return output_grid

def move_pixel(grid, start_y, start_x, end_y, end_x):
    y, x = start_y, start_x
    while (y, x) != (end_y, end_x):
        if y < end_y:
            y += 1
        elif y > end_y:
            y -= 1
        elif x < end_x:
            x += 1
        elif x > end_x:
            x -= 1
        
        if grid[y, x] == Color.BLACK:
            grid[y, x] = Color.GREEN

def generate_input():
    # Create a black grid
    size = np.random.randint(8, 15)
    grid = np.full((size, size), Color.BLACK)

    # Place blue and red pixels in opposite corners
    corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
    blue_corner = random.choice(corners)
    red_corner = corners[(corners.index(blue_corner) + 2) % 4]

    grid[blue_corner] = Color.BLUE
    grid[red_corner] = Color.RED

    # Scatter yellow pixels
    num_yellow = np.random.randint(3, 8)
    for _ in range(num_yellow):
        while True:
            y, x = np.random.randint(0, size), np.random.randint(0, size)
            if grid[y, x] == Color.BLACK:
                grid[y, x] = Color.YELLOW
                break

    return grid