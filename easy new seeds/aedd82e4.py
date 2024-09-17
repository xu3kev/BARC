from common import *

import numpy as np
from typing import *

# concepts:
# object detection, color change

# description:
# In the input you will see a grid with a red pattern
# To make the output grid, you should find out any single isolated red objects with size of 1x1 and change them to blue.

def main(input_grid):
    # Detect all the red objects in the grid, ignoring objects of other colors
    red_objects = detect_objects(grid=input_grid, colors=[Color.RED], monochromatic=True, connectivity=4)

    # Convert 1x1 objects (isolated pixels) into blue
    output_grid = input_grid.copy()
    for object in red_objects:
        x, y, length, width = bounding_box(object, background=Color.BLACK)
        # Find out the single isolated red object with size of 1x1 and change it to blue.
        if length == 1 and width == 1:
            output_grid[x, y] = Color.BLUE

    return output_grid

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = np.random.randint(3, 6), np.random.randint(3, 6)
    grid = np.zeros((n, m), dtype=int)

    colored = 0
    # Randomly scatter density of red pixels on the grid.
    density = 0.4
    while colored < density * n * m:
        x = np.random.randint(0, n)
        y = np.random.randint(0, m)
        if grid[x, y] == Color.BLACK:
            grid[x, y] = Color.RED
            colored += 1

    # Ensure there is at least one 1x1 single isolated red object in the grid.
    red_objects = detect_objects(grid=grid, colors=[Color.RED], monochromatic=True, connectivity=4)
    if not any(np.sum(object != Color.BLACK) == 1 for object in red_objects):
        return generate_input()
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
