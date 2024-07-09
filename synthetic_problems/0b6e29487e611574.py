from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, symmetry detection, colors, rotational symmetry

# description:
# In the input, you will see a grid with a pattern of colored pixels that repeats both horizontally and vertically.
# To create the output:
# 1. Detect the translational symmetry in both directions.
# 2. Expand the grid to be 9x9, repeating the pattern as needed.
# 3. Apply a 90-degree clockwise rotation to the entire expanded grid.
# 4. For each color in the rotated grid, replace it with the next color in the sequence: 
#    RED -> GREEN -> BLUE -> YELLOW -> ORANGE -> PINK -> RED (cycle repeats)

def main(input_grid):
    # Detect translational symmetries
    symmetries = detect_translational_symmetry(input_grid, ignore_colors=[])
    assert len(symmetries) > 0, "No translational symmetry found"

    # Create 9x9 output grid
    output_grid = np.full((9, 9), Color.BLACK)

    # Expand the pattern to fill the 9x9 grid
    for x, y in np.argwhere(input_grid != Color.BLACK):
        for x2, y2 in orbit(output_grid, x, y, symmetries):
            output_grid[x2, y2] = input_grid[x, y]

    # Rotate the grid 90 degrees clockwise
    output_grid = np.rot90(output_grid, k=-1)

    # Define the color cycle
    color_cycle = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.ORANGE, Color.PINK]

    # Replace colors
    for i, color in enumerate(color_cycle):
        next_color = color_cycle[(i + 1) % len(color_cycle)]
        output_grid[output_grid == color] = next_color

    return output_grid

def generate_input():
    # Create a small pattern with random colors
    pattern_size = (np.random.randint(2, 4), np.random.randint(2, 4))
    color_palette = np.random.choice([Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.ORANGE, Color.PINK], size=3, replace=False)
    pattern = random_sprite(pattern_size[0], pattern_size[1], symmetry="not_symmetric", color_palette=color_palette, density=0.7, connectivity=8)

    # Create a larger grid by tiling the pattern
    grid_size = (np.random.randint(4, 7), np.random.randint(4, 7))
    input_grid = np.tile(pattern, (grid_size[0] // pattern_size[0] + 1, grid_size[1] // pattern_size[1] + 1))
    input_grid = input_grid[:grid_size[0], :grid_size[1]]

    return input_grid