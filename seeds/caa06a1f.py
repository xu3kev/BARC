from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, symmetry detection, non-black background

# description:
# In the input you will see a a translationally symmetric pattern that does not extend to cover the entire canvas. The background is not black.
# To make the output, continue the symmetric pattern until it covers the entire canvas, but shift everything right by one pixel.
 
def main(input_grid):
    # Plan:
    # 1. Find the background color
    # 2. Find the repeated translation, which is a symmetry
    # 3. Extend the pattern by computing the orbit of each pixel in the pattern

    # Find the background color which is the most common color along the border of the canvas
    pixels_on_border = np.concatenate([input_grid[0, :], input_grid[-1, :], input_grid[:, 0], input_grid[:, -1]])
    background = max(set(pixels_on_border), key=list(pixels_on_border).count)
    
    # Find the repeated translation, which is a symmetry
    symmetries = detect_translational_symmetry(input_grid, ignore_colors=[], background=background)
    assert len(symmetries) > 0, "No translational symmetry found"

    # because we are going to shift everything right by one pixel, we make an output grid which is one pixel wider
    # at the end, we will just remove the leftmost pixels
    width, height = input_grid.shape
    output_grid = np.full((width+1, height), Color.BLACK)
    
    # Copy all of the input pixels to the output, INCLUDING their symmetric copies (i.e. their orbit)
    for x, y in np.argwhere(input_grid != background):
        # Compute the orbit into the output grid
        for x2, y2 in orbit(output_grid, x, y, symmetries):
            output_grid[x2, y2] = input_grid[x, y]
    
    # Shift everything right by one pixel by removing the leftmost pixels
    output_grid = output_grid[1:, :]

    return output_grid


def generate_input():

    background_color = random.choice(Color.NOT_BLACK)
    # Make a random large canvas
    grid = np.full((np.random.randint(15, 30), np.random.randint(15, 30)), background_color)

    # Make the basic sprite
    w, h = random.randint(2, 4), random.randint(2, 4)
    sprite = np.random.choice([color for color in Color.ALL_COLORS if color != background_color], (w, h))

    # Tile it a few times, starting from the upper left hand corner
    max_x = random.randint(w+1, grid.shape[0])
    max_y = random.randint(h+1, grid.shape[1])
    for x in range(0, max_x, w):
        for y in range(0, max_y, h):
            blit_sprite(grid, sprite, x, y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)