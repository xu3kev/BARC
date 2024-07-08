from common import *

import numpy as np
from typing import *

# concepts:
# patterns, positioning, copying

# description:
# In the input you will see a pattern of pixels in the top left corner of the grid, the top right corner of the grid, the bottom left corner of the grid, and the bottom right corner of the grid. All the pixels are the same color, and the patterns are in square regions.
# To make the output, copy the pattern in each corner of the input to the corresponding corner of the output. The output grid is one pixel larger in each dimension than the maximum pattern side length.

def main(input_grid):
    # get the patterns from the input
    objects = find_connected_components(input_grid, connectivity=8)

    # find the bounding box of each pattern
    bounding_boxes = [bounding_box(obj) for obj in objects]

    # figure out how big the output grid should be (the pattern is a square and the output should be one pixel larger in each dimension)
    n = m = max([max(pattern[2], pattern[3]) for pattern in bounding_boxes]) + 1

    # make the output grid
    output_grid = np.full((n, m), Color.BLACK)

    # copy the patterns to the output grid
    for obj, (x, y, _, _) in zip(objects, bounding_boxes):
        # adjust the position of the pattern in the output grid if necessary
        if x >= n - 1:
            x = x - input_grid.shape[0] + n
        if y >= m - 1:
            y = y - input_grid.shape[1] + m
        # crop the pattern to remove any extra rows or columns of black pixels
        sprite = crop(obj)
        # copy the pattern to the output grid
        blit_sprite(output_grid, sprite, x=x, y=y, background=Color.BLACK)
    
    return output_grid
    

def generate_input():
    # make a random sized grid with black background
    n = np.random.randint(5, 8)
    m = np.random.randint(5, 8)
    grid = np.zeros((n, m), dtype=int)

    # select a color for the patterns
    color = np.random.choice(list(Color.NOT_BLACK))

    # select a size for the patterns so that there will be space between the patterns after they are in their corners
    size = np.random.randint(2, (min(n, m) + 1) // 2)


    # make a random pattern in the top left corner of the specified size
    grid[:size, :size] = [[np.random.choice([color, Color.BLACK]) for _ in range(size)] for _ in range(size)]

    # make a random pattern in the top right corner of the specified size
    grid[:size, -size:] = [[np.random.choice([color, Color.BLACK]) for _ in range(size)] for _ in range(size)]

    # make a random pattern in the bottom left corner of the specified size
    grid[-size:, :size] = [[np.random.choice([color, Color.BLACK]) for _ in range(size)] for _ in range(size)]

    # make a random pattern in the bottom right corner of the specified size
    grid[-size:, -size:] = [[np.random.choice([color, Color.BLACK]) for _ in range(size)] for _ in range(size)]

    # Check that at least one of the patterns is not all black
    # If they are all black, try again
    if np.all(grid == Color.BLACK):
        return generate_input()

    return grid




# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)