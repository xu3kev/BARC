from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, symmetry detection, pattern extension, color change, objects

# description:
# In the input, you will see a grid consisting of a single colored sprite that is repeatedly translated horizontally, forming a line of the same sprite.
# To create the output, find the repeated translational symmetry in the input. Extend the pattern by copying the sprite to the left and right, symmetrically, within a new grid with extended width. Finally, change the color of the original sprite pattern to a new color.

def main(input_grid):
    # Detect translational symmetry in the input grid
    symmetries = detect_translational_symmetry(input_grid, ignore_colors=[Color.BLACK])
    assert len(symmetries) > 0, "No translational symmetry found"

    # Determine the dimensions of the input grid
    input_height, input_width = input_grid.shape
    
    # Create the output grid with extended width (double the input width)
    output_width = input_width * 2
    output_grid = np.full((input_height, output_width), Color.BLACK)
    
    # Copy the input pattern and extend the pattern horizontally
    for x, y in np.argwhere(input_grid != Color.BLACK):
        # Compute the orbit in the input grid
        for x2, y2 in orbit(input_grid, x, y, symmetries):
            output_grid[x][y2 % output_width] = input_grid[x, y]

    # Change the color of the extended pattern to a new color
    new_color = Color.RED
    original_color = input_grid[input_grid != Color.BLACK][0]  # Assuming all non-background pixels are the same color
    output_grid[output_grid == original_color] = new_color

    return output_grid

def generate_input():
    # Create a random sized grid with a horizontal pattern
    input_height = np.random.randint(5, 8)
    input_width = np.random.randint(10, 15)
    grid = np.full((input_height, input_width), Color.BLACK)
    
    # Select a random color for the pattern
    color = np.random.choice(list(Color.NOT_BLACK))
    
    # Create a random sprite pattern of a random length
    sprite_length = np.random.randint(2, input_width // 2)
    sprite = random_sprite(input_height, sprite_length, color_palette=[color], density=0.7)
    
    # Place the sprite in a horizontal line within the grid
    horizontal_repeat_frequency = np.random.randint(1, sprite_length)
    for i in range(0, input_width, sprite_length + horizontal_repeat_frequency):
        grid[:, i:i+sprite_length] = sprite[:, :min(sprite_length, input_width - i)]
    
    return grid