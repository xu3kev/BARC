from common import *

import numpy as np
from typing import *

# concepts:
# denoising, topology

# description:
# In the input you will see a black background with large rectangles of the same color, and random "noise" pixels added at random locations, in the same color as the rectangles.
# To make the output, remove the noise pixels, leaving only the big rectangles.

def main(input_grid):
    # Plan:
    # 1. Find the neighbors of each pixel
    # 2. If its neighbors are mostly colored (>=2 neighbors), it's part of a rectangle
    # 3. Otherwise, it's noise, so delete it

    output_grid = np.copy(input_grid)

    for x, y in np.argwhere(input_grid != Color.BLACK):
        # Turn this single pixel into an object, and get its neighbors
        obj = np.full(input_grid.shape, Color.BLACK)
        obj[x, y] = input_grid[x, y]
        neighbors_mask = object_neighbors(obj, connectivity=4, background=Color.BLACK)

        # If the object has at least 2 colored neighbors, then it is part of a rectangle. Otherwise, it is noise, so delete it.
        colors_of_neighbors = input_grid[neighbors_mask]
        if np.sum(colors_of_neighbors != Color.BLACK) >= 2:
            # has at least 2 colored neighbors, so it's part of a rectangle
            pass
        else:
            # doesn't have at least 2 colored neighbors, so delete it
            output_grid[x, y] = Color.BLACK

    return output_grid


def generate_input():
    w, h = np.random.randint(10, 25, size=2)
    grid = np.full((w, h), Color.BLACK)

    color = np.random.choice(Color.NOT_BLACK)
    n_rectangles = np.random.randint(2, 4)

    for _ in range(n_rectangles):
        rw, rh = np.random.randint(3, 2*w//3), np.random.randint(3, 2*h//3)
        sprite = np.full((rw, rh), color) # Can also do: random_sprite(rw, rh, color_palette=[rectangle_color], density=1)
        x, y = random_free_location_for_sprite(grid, sprite)
        blit_sprite(grid, sprite, x, y)
    
    n_noise_pixels = np.random.randint(8, 16)
    for _ in range(n_noise_pixels):
        x, y = np.random.randint(w), np.random.randint(h)
        grid[x, y] = color
    
    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
