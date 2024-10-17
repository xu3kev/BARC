from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation

# description:
# In the input you will see a grid with some rectangles. Each rectangle is three pixels tall and has a single color.
# To make the output, you should draw a pattern in each rectangle.
# The pattern is created by turning the inner pixel of the rectangle to black alternatingly.

def main(input_grid):
    # Output grid is the same size as the input grid
    output_grid = np.zeros_like(input_grid)

    # Extract the rectangles from the input grid
    rectangles = find_connected_components(input_grid, monochromatic=True)

    # Draw pattern in the rectangle, which is turn the inner pixel to black alternatingly
    for rectangle in rectangles:
        x, y, w, h = bounding_box(rectangle)
        rectangle = crop(rectangle)
        # The rectangles are all three pixels tall, so the inner part is the second row
        for i in range(1, w, 2):
            rectangle[i, 1] = Color.BLACK
        output_grid = blit(output_grid, rectangle, x, y)

    return output_grid

def generate_input():
    # Generate the background grid
    n, m = np.random.randint(20, 30), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose the number of rectangles on the grid
    rectangle_number = np.random.randint(1, 4)
    # Randomly choose colors for the rectangles
    colors = np.random.choice(Color.NOT_BLACK, rectangle_number, replace=False)

    for color in colors:
        # Randomly choose the width of the rectangle, should not be too short and should be odd
        w, h = np.random.randint(2, 6) * 2 + 1, 3
        rectangle = np.full((w, h), color)

        # Randomly choose the position of the rectangle
        try:
            x, y = random_free_location_for_sprite(grid, rectangle, padding=1, padding_connectivity=8)
        except:
            # If there is no free location for the rectangle, retry
            return generate_input()
        blit(grid, rectangle, x, y)

    return grid
# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
