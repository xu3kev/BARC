from common import *

import numpy as np
from typing import *

# concepts:
# object detection, color change

# description:
# In the input you will see a grid with a red pattern
# To make the output grid, you should find out the single isolated red object with size of 1x1 and change it to blue.

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

    # Randomly scatter color pixels on the grid.
    def random_scatter_point_on_grid(grid, color, density):
        n, m = grid.shape
        colored = 0
        # Randomly scatter density of color pixels on the grid.
        while colored < density * n * m:
            x = np.random.randint(0, n)
            y = np.random.randint(0, m)
            if grid[x, y] == Color.BLACK:
                grid[x, y] = color
                colored += 1
        return grid
    
    # Randomly scatter color pixels on the grid.
    grid = random_scatter_point_on_grid(grid, Color.RED, 0.5)

    # Ensure there is at least one 1x1 single isolated red object in the grid.
    random_x, random_y = np.random.randint(0, n), np.random.randint(0, m)
    grid[random_x, random_y] = Color.RED
    if random_x > 0:
        grid[random_x - 1, random_y] = Color.BLACK 
    if random_x < n - 1:
        grid[random_x + 1, random_y] = Color.BLACK
    if random_y > 0:
        grid[random_x, random_y - 1] = Color.BLACK
    if random_y < m - 1:
        grid[random_x, random_y + 1] = Color.BLACK

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
