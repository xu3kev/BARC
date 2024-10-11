from common import *

import numpy as np
from typing import *

# concepts:
# attraction, magnetism

# description:
# In the input you will individual pixels are the sides of a grid. Each pixel is in a matching pair, which is a different color, but on the opposite side of the grid.
# To make the output, make each pixel copy its color toward its matching pair until they meet in the middle. Turn the middle point grey.

def main(input_grid):
    # Plan:
    # 1. Detect the pixels
    # 2. Associate each pixel with its matching pair
    # 3. Make them attract/march toward each other until they meet in the middle, leaving a trail of their own color

    # 1. Find the location of the pixels
    pixel_objects = find_connected_components(input_grid, connectivity=4, background=Color.BLACK)
    assert len(pixel_objects) % 2 == 0, "There should be an even number of pixels"

    # we're going to draw on top of the input grid
    output_grid = input_grid.copy()

    for obj in pixel_objects:
        # 2. Associate each pixel with its matching pair
        # Find the matching position, which is either the opposite x or the opposite y
        x, y = object_position(obj, background=Color.BLACK, anchor='center')
        if x in [0, input_grid.shape[0] - 1]:
            opposite_x = input_grid.shape[0] - 1 - x
            opposite_y = y
        else:
            opposite_x = x
            opposite_y = input_grid.shape[1] - 1 - y

        # get the unit vector pointing from one to the other
        dx, dy = np.sign([opposite_x - x, opposite_y - y], dtype=int)

        color = input_grid[x, y]
        other_color = input_grid[opposite_x, opposite_y]

        # 3. Make them attract/march toward each other until they meet in the middle (grey when they touch), leaving a trail of their own color
        while (x, y) != (opposite_x, opposite_y):
            # Draw a trail of color
            if output_grid[x, y] == Color.BLACK:
                output_grid[x, y] = color
            if output_grid[opposite_x, opposite_y] == Color.BLACK:
                output_grid[opposite_x, opposite_y] = other_color
            x += dx
            y += dy
            opposite_x -= dx
            opposite_y -= dy

            # Make sure we haven't fallen out of bounds
            if not (0 <= x < input_grid.shape[0] and 0 <= y < input_grid.shape[1] and 0 <= opposite_x < input_grid.shape[0] and 0 <= opposite_y < input_grid.shape[1]):
                break
        # when they meet, turn the middle point grey
        output_grid[x, y] = Color.GREY
    
    return output_grid
        



def generate_input():
    # We are going to generate a grid with pairs that go top-bottom, but then randomly rotate to get the other orientations

    # Generate the grid with random size, but odd height so that there is a unique middle point
    width, height = np.random.randint(5, 25), np.random.randint(10, 30)
    # Makes sure it's odd
    if height%2 != 1:
        return generate_input()
        
    grid = np.full((width, height), Color.BLACK)
    
    n_pairs = np.random.randint(3, 6+1)
    for pair_index in range(n_pairs):
        # Pick a random top-bottom position for the first pixel, which has to be on the border but not in the corners
        top_bottom_locations = [ (x, 0) for x in range(1, width-1) ] + [ (x, height-1) for x in range(1, width-1) ]
        x, y = random.choice(top_bottom_locations)
        color = random.choice([ color for color in Color.NOT_BLACK if color != Color.GREY ])
        # Make sure it is not already occupied
        if grid[x, y] != Color.BLACK: continue
        grid[x, y] = color

        # Find the opposite position
        if x in [0, width - 1]:
            opposite_x = width - 1 - x
            opposite_y = y
        else:
            opposite_x = x
            opposite_y = height - 1 - y
        other_color = random.choice([ other_color for other_color in Color.NOT_BLACK if other_color != color and other_color != Color.GREY ])
        grid[opposite_x, opposite_y] = other_color

    # random rotation
    grid = np.rot90(grid, np.random.randint(0, 4))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
