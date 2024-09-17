from common import *

import numpy as np
from typing import *

# concepts:
# pattern recognition, if symmetry

# description:
# In the input you will see a 3x3 grid with red pixels scattered randomly.
# To make the output grid, you should recognize if the input grid has mirror symmetry along the y-axis.
# If the input grid has mirror symmetry along the y-axis, output a 1x1 grid with a blue pixel.
# Otherwise, output a 1x1 grid with an orange pixel.

def main(input_grid):
    # Find the possible symmetry of the input grid.
    best_symmetry = detect_mirror_symmetry(grid=input_grid)

    # Check if the symmetry is along the y-axis.
    if_symmetry = False
    for symmetry in best_symmetry:
        if symmetry.mirror_y is not None:
            if_symmetry = True
            break
    
    # Output a 1x1 grid with a blue pixel if the input grid has mirror symmetry along the y-axis.
    if if_symmetry:
        output_grid = np.array([[Color.BLUE]])
    else:
        output_grid = np.array([[Color.ORANGE]])
    
    return output_grid

def generate_input():
    n, m = 3, 3
    grid = np.zeros((n, m), dtype=int)

    num_pixel = np.random.randint(2, 8)
        # Randomly scatter color pixels on the grid.
    
    # Randomly generate a 3x3 grid with symmetric pattern or not.
    if_symmetry = np.random.choice([True, False])
    symmetry_type = "horizontal" if if_symmetry else "not_symmetric"
    grid = random_sprite(n=3, m=3, density=num_pixel // 9, color_palette=[Color.RED], symmetry=symmetry_type)

    # Randomly scatter color pixels on the grid.
    def random_scatter_point_on_grid(grid, color, density):
        n, m = grid.shape
        colored = 0
        # Randomly scatter density of color pixels on the grid.
        while colored < density * n * m:
            x = np.random.randint(0, n)
            y = np.random.randint(0, m)
            grid[x, y] = color
            colored += 1
        return grid
    
    # If the pattern is not symmetric, scatter some black pixels on the grid to make it not symmetric.
    if not if_symmetry:
        grid = random_scatter_point_on_grid(grid, Color.BLACK, 0.4)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
