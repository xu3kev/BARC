from common import *

import numpy as np
from typing import *

# concepts:
# symmetry detection, boolean indicator

# description:
# In the input you will see a 3x3 grid with red pixels scattered randomly.
# To make the output grid, you should recognize if the input grid has mirror symmetry along the x-axis.
# If the input grid has mirror symmetry along the x-axis, output a 1x1 grid with a blue pixel.
# Otherwise, output a 1x1 grid with an orange pixel.

def main(input_grid):
    # Check if the input grid has mirror symmetry along the middle x-axis.
    width, height = input_grid.shape
    middle_x = width // 2
    
    # If the input grid has mirror symmetry along the middle x-axis, output a blue pixel.
    # Otherwise, output an orange pixel.
    if np.all(input_grid[0: middle_x] == input_grid[middle_x + 1:][::-1]):
        output_grid = np.full((1,1), Color.BLUE)
    else:
        output_grid = np.full((1,1), Color.ORANGE)
    
    return output_grid

def generate_input():
    width, height = 3, 3
    grid = np.zeros((width, height), dtype=int)
    
    # Randomly generate a 3x3 grid with symmetric pattern or not.
    has_y_axis_symmetry = np.random.choice([True, False])
    symmetry_type = "horizontal" if has_y_axis_symmetry else "not_symmetric"
    density = random.choice([0.3, 0.4, 0.5, 0.6])
    grid = random_sprite(n=3, m=3, density=density, color_palette=[Color.RED], symmetry=symmetry_type)
    
    # If the pattern is not symmetric, scatter some black pixels on the grid to make it not symmetric.
    if not has_y_axis_symmetry:
        # Randomly 40% colored pixels on the grid
        target_density = 0.4
        target_number_of_pixels = int(target_density * height * width)
        for i in range(target_number_of_pixels):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            grid[x, y] = Color.BLACK

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
