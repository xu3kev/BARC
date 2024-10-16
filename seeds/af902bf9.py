from common import *

import numpy as np
from typing import *

# concepts:
# filling, surrounding

# description:
# In the input you will see several yellow pixels arranged in groups of 4 so that each group outlines a rectangular shape.
# To make the output, fill the corresponding inner rectangular regions with red.

def main(input_grid):
    # Detect the rectangular regions by finding groups of four surrounding yellow pixels
    surrounding_color = Color.YELLOW
    rectangle_color = Color.RED
    
    output_grid = np.copy(input_grid) 

    # loop over all the yellows...
    for x, y in np.argwhere(input_grid == surrounding_color):
        # ...and find the other matching yellows forming a rectangle: (x, y), (x, y'), (x', y), (x', y')
        for other_x, other_y in np.argwhere(input_grid == surrounding_color):
            if input_grid[x, other_y] == surrounding_color and input_grid[other_x, y] == surrounding_color:
                # fill the rectangle with red
                output_grid[x+1:other_x, y+1:other_y] = rectangle_color

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
        rectangle_sprite = np.full((rectangle_len, rectangle_width), rectangle_color)
        try:
            x, y = random_free_location_for_sprite(grid, rectangle_sprite, padding=2, padding_connectivity=8, border_size=1)
        except:
            continue

        blit_sprite(grid, rectangle_sprite, x=x, y=y)

        # Place four surrounding colors around the rectangle right outside its corners
        min_x, min_y, max_x, max_y = x, y, x+rectangle_len, y+rectangle_width
        grid[min_x-1, min_y-1] = surrounding_color
        grid[min_x-1, max_y] = surrounding_color
        grid[max_x, y-1] = surrounding_color
        grid[max_x, max_y] = surrounding_color

    # Remove the inner rectangle color, only keep the surrounding color
    grid[grid == rectangle_color] = Color.BLACK
    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
