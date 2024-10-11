from common import *

import numpy as np
from typing import *

# concepts:
# Fulfill, surrounding

# description:
# In the input you will see several yellow pixels, each four yellow pixels form a rectangle shape.
# To make the output, fill the inner rectangle with red color.

def main(input_grid):
    # Detect the area of the rectangle by finding the four surrounding yellow pixels
    surrounding_color = Color.YELLOW
    rectangle_color = Color.RED

    n, m = input_grid.shape
    output_grid = np.copy(input_grid) 

    for x, y in np.ndindex(n, m):
        if input_grid[x, y] == surrounding_color:
            # Get all the rectangles grid start from this point
            rectangles = []
            for dx, dy in np.ndindex(n - x, m - y):
                rectangles.append(input_grid[x:x + dx + 1, y:y + dy + 1])
            
            # Check if one rectangle is surrounded by four yellow pixels
            # Also check if the pixels have enough space to draw the inner rectangle
            for rectangle in rectangles:
                if ((rectangle.shape)[0] > 2 and (rectangle.shape)[1] > 2 and
                    rectangle[0, 0] ==  surrounding_color and
                    rectangle[0, -1] == surrounding_color and
                    rectangle[-1, 0] == surrounding_color and
                    rectangle[-1, -1] == surrounding_color):
                    # Find the inner rectangle need to be colored
                    bound_width, bound_height = rectangle.shape
                    rec_width, rec_height = bound_width - 2, bound_height - 2

                    # Place the inner rectangle with red color
                    filled_rectangle = np.ones((rec_width, rec_height), dtype=int) * rectangle_color
                    output_grid = blit_sprite(grid=output_grid, sprite=filled_rectangle, x=x + 1, y=y + 1)

    return output_grid

def generate_input():
    # Create the background grid
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    rectangle_num = np.random.randint(1, 4)

    # Draw rectangles on the grid
    rectangle_color = Color.RED
    surrounding_color = Color.YELLOW

    for _ in range(rectangle_num):
        rectangle_len = np.random.randint(1, 5)
        rectangle_width = np.random.randint(1, 5)
        
        # Draw the rectangle with rectangle color
        rectangle = np.ones((rectangle_len, rectangle_width), dtype=int) * rectangle_color
        try:
            x, y = random_free_location_for_sprite(grid=grid, sprite=rectangle, padding=2, padding_connectivity=8, border_size=1)
        except:
            continue

        grid = blit_sprite(grid=grid, sprite=rectangle, x=x, y=y)

        # Place four surrounding colors around the rectangle
        grid[x-1, y-1] = surrounding_color
        grid[x-1, y+rectangle_width] = surrounding_color
        grid[x+rectangle_len, y-1] = surrounding_color
        grid[x+rectangle_len, y+rectangle_width] = surrounding_color

    # Remove the inner rectangle color, only keep the surrounding color
    grid[grid == rectangle_color] = Color.BLACK
    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
