from common import *

import numpy as np
from typing import *

# concepts:
# color, falling, cropping

# description:
# In the input, you should see colored pixels and solid color blocks acting as obstacles.
# To create the output, make each pixel fall downward until it hits an obstacle or the bottom.
# Crop the resulting grid to the smallest bounding box that contains all non-background pixels.

def main(input_grid):
    output_grid = np.copy(input_grid)

    width, height = output_grid.shape

    # Find the color of the background, which is the most common color
    background_color = np.argmax(np.bincount(output_grid.flatten()))

    # Now make all the other colors fall down
    for x in range(width):
        for y in range(height-2, -1, -1):
            if output_grid[x, y] != background_color:
                # Make it fall to the bottom or until it hits an obstacle
                for k in range(y+1, height):
                    if output_grid[x, k] != background_color: 
                        output_grid[x, k-1] = output_grid[x, y]
                        if k-1 != y:
                            output_grid[x, y] = background_color
                        break
                else:
                    output_grid[x, height-1] = output_grid[x, y]
                    output_grid[x, y] = background_color

    return crop(output_grid, background=background_color)


def generate_input():
    width, height = 10, 10
    input_grid = np.zeros((width, height), dtype=int)

    # Add some solid color blocks acting as obstacles
    num_obstacles = random.choice([5, 10, 15])
    for _ in range(num_obstacles):
        x = random.randint(0, width-1)
        y = random.randint(5, height-1)  # ensuring obstacles are closer to the bottom
        input_grid[x, y] = random.choice(Color.NOT_BLACK)

    # Add colored pixels in random positions above obstacles
    num_pixels = random.choice([5, 10, 15, 20])
    for _ in range(num_pixels):
        while True:
            x = random.randint(0, width-1)
            y = random.randint(0, height-6)  # placed above possible obstacles
            if input_grid[x, y] == 0:
                input_grid[x, y] = random.choice(Color.NOT_BLACK)
                break

    return input_grid