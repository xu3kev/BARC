from common import *

import numpy as np
from typing import *

# concepts:
# symmetry detection, occlusion

# description:
# In the input you will see an object that is almost rotationally symmetric, except that some of it has been removed (covered in black pixels)
# To make the output fill in the missing parts of the object to make it rotationally symmetric


def main(input_grid):
    # Plan:
    # 1. Find the center of rotation
    # 2. Rotate each colored pixel (4 times, rotating around the center of rotation) and fill in any missing pixels
    output_grid = input_grid.copy()

    # Find the center of rotation
    rotate_center_x, rotate_center_y = detect_rotational_symmetry(input_grid, ignore_color=Color.BLACK)

    # Find the coloured pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)

    # Do the rotations and fill in the missing colors
    for x, y in colored_pixels:
        # Get the color, which is going to be copied to the rotated positions
        color = input_grid[x, y]
        
        # Loop over all rotations, going 90 degrees each time (so four times)
        for i in range(4):
            # Calculate rotated coordinate
            # IMPORTANT! Cast to int to avoid floats
            rotated_x, rotated_y = y + int(rotate_center_x - rotate_center_y), -x + int(rotate_center_y + rotate_center_x)

            # Fill in the missing pixel
            if output_grid[rotated_x, rotated_y] == Color.BLACK:
                output_grid[rotated_x, rotated_y] = color
            else:
                assert output_grid[rotated_x, rotated_y] == color, "The object is not rotationally symmetric"
            
            # Update the pixel to be its rotation
            x, y = rotated_x, rotated_y

    return output_grid


def generate_input():
    # Initialize 10x10 grid
    grid = np.zeros((10, 10), dtype=int)

    # Create 5x5 sprite
    sprite = random_sprite(
        5, 5, density=0.3, symmetry="radial", color_palette=list(Color.NOT_BLACK)
    )

    # Randomly remove pixels from sprite
    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            if random.random() < 0.2:
                sprite[i, j] = Color.BLACK

    # Place sprite randomly onto the grid
    x, y = random_free_location_for_object(grid, sprite)
    blit(grid, sprite, x, y)

    return grid


# ============= remove below this point for prompting =============

if __name__ == "__main__":
    visualize(generate_input, main)
