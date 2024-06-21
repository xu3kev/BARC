from common import *

import numpy as np
from typing import *

# concepts:
# color mapping

# description:
# The input is a grid where each column is of the same color. 
# To make the output, change each color according to the following mapping:
# green -> yellow, blue -> gray, red -> pink, teal -> maroon, yellow -> green, gray -> blue, pink -> red, maroon -> teal

def main(input_grid):
    # Initialize output grid
    output_grid = input_grid.copy()

    # Performs color mapping
    output_grid = np.vectorize(lambda color: color_map.get(color, color))(output_grid)

    return output_grid
    
# Constructing the color map
color_map = {Color.GREEN : Color.YELLOW, 
             Color.BLUE : Color.GRAY, 
             Color.RED : Color.PINK,
             Color.TEAL : Color.MAROON,
             Color.YELLOW : Color.GREEN, 
             Color.GRAY : Color.BLUE, 
             Color.PINK : Color.RED,
             Color.MAROON : Color.TEAL             
            }


def generate_input():
    grid = np.full((3, 3), Color.BLACK)
    for x in range(grid.shape[0]):
        grid[x, :] = random.choice(list(color_map.keys()))
    return grid
# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)