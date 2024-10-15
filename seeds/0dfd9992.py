from common import *

import numpy as np
from typing import *

# concepts:
# occlusion, translational symmetry

# description:
# In the input you will see a translationally symmetric pattern randomly occluded by black pixels.
# To make the output, remove the occluding black pixels to reveal the translationally symmetric pattern.

def main(input_grid):
    # Plan:
    # 1. Find the translational symmetries
    # 2. Reconstruct the sprite by ignoring the black pixels and exploiting the symmetry

    w, h = input_grid.shape

    # Identify the translational symmetries. Note that there is no background color for this problem.
    translations = detect_translational_symmetry(input_grid, ignore_colors=[Color.BLACK], background=None)
    assert len(translations) > 0, "No translational symmetry found"

    # Reconstruct the occluded black pixels by replacing them with colors found in the orbit of the symmetries
    output_grid = np.copy(input_grid)
    for x in range(w):
        for y in range(h):
            if output_grid[x, y] == Color.BLACK:
                # Use the translational symmetry to fill in the occluded pixels
                # to do this we compute the ORBIT of the current pixel under the translations
                # and take the most common non-black color in the orbit

                # Compute the orbit into the output
                orbit_pixels = orbit(output_grid, x, y, translations)
                orbit_colors = {input_grid[transformed_x, transformed_y]
                                for transformed_x, transformed_y in orbit_pixels}
                
                # occluded by black, so whatever color it is, black doesn't count
                orbit_colors = orbit_colors - {Color.BLACK}

                # Copy the color
                assert len(orbit_colors) == 1, "Ambiguity: multiple colors in the orbit"
                output_grid[x, y] = orbit_colors.pop()
    
    return output_grid

def generate_input():
    # Make a random large canvas
    grid = np.full((np.random.randint(15, 30), np.random.randint(15, 30)), Color.BLACK)

    # Make the basic sprite
    w, h = random.randint(3, 8), random.randint(3, 8)
    sprite = random_sprite(w, h, density=1, color_palette=Color.NOT_BLACK)

    # Place the sprite in the upper left corner of the canvas, then compute the orbit under the symmetry group
    blit_sprite(grid, sprite, x=0, y=0)
    symmetries = [TranslationalSymmetry(w, 0), TranslationalSymmetry(0, h)]
    for x, y in np.argwhere(sprite != Color.BLACK):
        for x2, y2 in orbit(grid, x, y, symmetries):
            grid[x2, y2] = sprite[x, y]
    # You could have also done this:
    # for x in range(0, grid.shape[0], w):
    #     for y in range(0, grid.shape[1], h):
    #         blit_sprite(grid, sprite, x, y)
    
    # Create random occluders
    n_occluders = random.randint(1, 5)
    for _ in range(n_occluders):
        x, y = random.randint(0, grid.shape[0]), random.randint(0, grid.shape[1])
        w, h = random.randint(3, 7), random.randint(3, 7)
        grid[x:x+w+1, y:y+h+1] = Color.BLACK

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
