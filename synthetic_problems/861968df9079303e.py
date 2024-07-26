from common import *

import numpy as np
from typing import *

# concepts:
# pattern recognition, lines, grid manipulation, symmetry

# description:
# In the input, you will see several colored plus ('+') and L-shaped seed patterns on a black background.
# To make the output, symmetrically extend each pattern horizontally and vertically until reaching the edges of the grid.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # Find the bounding boxes of all the '+' and 'L' shaped seeds
    seeds = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=False)
    
    # Get the colors of the components
    for seed in seeds:
        bounding = bounding_box(seed, background=Color.BLACK)
        x, y, w, h = bounding

        # Get seed color
        color = input_grid[x, y]
        
        # Extend '+' shapes
        if w == 3 and h == 3:
            # Draw vertical lines
            for i in range(x - x, output_grid.shape[0]):
                draw_line(output_grid, x, y, length=None, color=color, direction=(1, 0))
                draw_line(output_grid, x, y, length=None, color=color, direction=(-1, 0))
            # Draw horizontal lines
            for j in range(y - y, output_grid.shape[1]):
                draw_line(output_grid, x, y, length=None, color=color, direction=(0, 1))
                draw_line(output_grid, x, y, length=None, color=color, direction=(0, -1))
        
        # Extend 'L' shapes
        elif (w == 2 and h == 3) or (w == 3 and h == 2):
            if w == 2:
                # Draw vertical line
                draw_line(output_grid, x, y, length=None, color=color, direction=(1, 0))
                draw_line(output_grid, x, y, length=None, color=color, direction=(-1, 0))
                # Draw horizontal section
                y_b = y + 1 if input_grid[x, y + 1] == color else y - 1
                draw_line(output_grid, x, y_b, length=None, color=color, direction=(0, 1))
                draw_line(output_grid, x, y_b, length=None, color=color, direction=(0, -1))
            else:
                # Draw horizontal line
                draw_line(output_grid, x, y, length=None, color=color, direction=(0, 1))
                draw_line(output_grid, x, y, length=None, color=color, direction=(0, -1))
                # Draw vertical section
                x_b = x + 1 if input_grid[x + 1, y] == color else x - 1
                draw_line(output_grid, x_b, y, length=None, color=color, direction=(1, 0))
                draw_line(output_grid, x_b, y, length=None, color=color, direction=(-1, 0))
    return output_grid


def generate_input():
    n, m = np.random.randint(10, 20, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Colors to be chosen randomly
    possible_colors = list(Color.NOT_BLACK)
    
    # Number of seed patterns
    num_seeds = np.random.randint(2, 5)
    
    for _ in range(num_seeds):
        seed_type = np.random.choice(["plus", "L"])
        color = np.random.choice(possible_colors)
        
        if seed_type == "plus":
            seed_pattern = np.array([[0, color, 0],
                                     [color, color, color],
                                     [0, color, 0]])
        else:
            # Randomly choose between L-shaped patterns
            if np.random.rand() > 0.5:
                seed_pattern = np.array([[color, 0],
                                         [color, 0],
                                         [color, color]])
            else:
                seed_pattern = np.array([[0, color],
                                         [0, color],
                                         [color, color]])

        # Find a free location for the sprite
        try:
            x, y = random_free_location_for_sprite(grid, seed_pattern, padding=1, border_size=1)
            blit_sprite(grid, seed_pattern, x, y, background=Color.BLACK)
        except:
            continue # If no place is found, just skip it and try the next one

    return grid