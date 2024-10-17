from common import *

import numpy as np
from typing import *

# concepts:
# downscaling

# description:
# In the input you will see one grid with chessboard pattern separated by several lines.
# Each separated region is a square of same size.
# Some square regions are have same color on the four corners, and some are not.
# To make the output, you need to find the minimum regular squares with same color on the four corners,
# The black square regions with same color on the four corners should be filled with the color in the output.
# Each square region should be represented by one pixel in the output grid.

def main(input_grid):
    # Detect the objects
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    
    # The line color is the color that appear most 
    objects = sorted(objects, key=lambda x: np.sum(x != Color.BLACK), reverse=True)
    line_color = object_colors(objects[0])[0]

    # Detect the pixels that form the square
    pixels = [obj for obj in objects if object_colors(obj) != [line_color]]
    x_position = [object_position(obj)[0] for obj in pixels]
    y_position = [object_position(obj)[1] for obj in pixels]

    # Find the region of the pattern
    x_min, x_max = min(x_position), max(x_position)
    y_min, y_max = min(y_position), max(y_position)
    pattern_region = input_grid[x_min:x_max+1, y_min:y_max+1]

    # Figure out the size of black square
    squares = find_connected_components(pattern_region, background=line_color, connectivity=4, monochromatic=True)
    squares = [square for square in squares if object_colors(square, background=line_color) == [Color.BLACK]]
    square_len = crop(squares[0], background=line_color).shape[0]

    # Calculate the size of the output grid, should be the same size as using one pixel to represent a square in the region
    w, h = (x_max - x_min) // (square_len + 1), (y_max - y_min) // (square_len + 1)
    output_grid = np.full((w, h), Color.BLACK)

    # Check the representing color for each square in the output grid
    for x, y in np.ndindex(w, h):
        # Calculate the relative position of the square in the pattern region
        rela_x = x * (square_len + 1)
        rela_y = y * (square_len + 1)

        # Check if the four corners on the square are in same color different from the line color
        # If so, fill the square with the color
        cur_pixel_color = pattern_region[rela_x, rela_y]
        if (cur_pixel_color != line_color and
            pattern_region[rela_x + square_len + 1, rela_y] == cur_pixel_color and
            pattern_region[rela_x, rela_y + square_len + 1] == cur_pixel_color and
            pattern_region[rela_x + square_len + 1, rela_y + square_len + 1] == cur_pixel_color):
            output_grid[x, y] = cur_pixel_color
    
    return output_grid
            
def generate_input():
    # Randomly set square size and square number for each row
    # Make sure the grid size is smaller than 30
    square_size = np.random.randint(2, 4)
    square_num = np.random.randint(6, 30 // (square_size + 1))

    # Calculate the grid size
    n = square_size * square_num + square_num - 1
    m = n
    grid = np.full((n, m), Color.BLACK)

    # Randomly set the color of the squares and lines
    color_number = 3
    colors = np.random.choice(Color.NOT_BLACK, color_number, replace=False)
    line_color = colors[0]
    square_colors = colors[1:]

    # Draw lines to separate the squares
    # First draw the vertical lines
    for i in range(square_size, n, square_size + 1):
        draw_line(grid=grid, x=i, y=0, direction=(0, 1), color=line_color)
    # Then draw the horizontal lines
    for j in range(square_size, m, square_size + 1):
        draw_line(grid=grid, x=0, y=j, direction=(1, 0), color=line_color)

    # Generate the pattern of the square, each color should not touch other colors
    while(True):
        # Initialize the 3x3 background
        pattern = np.full((3, 3), Color.BLACK)

        # Generate the first pattern with one color
        n1, m1 = np.random.randint(1, 4), np.random.randint(1, 4)
        object1 = random_sprite(n=n1, m=m1, color_palette=[square_colors[0]], background=Color.BLACK, connectivity=8)
        x, y = random_free_location_for_sprite(grid=pattern, sprite=object1, background=Color.BLACK, padding=1, padding_connectivity=8)
        blit_sprite(pattern, object1, x=x, y=y, background=Color.BLACK)
        
        # Generate the second pattern with another color
        n2, m2 = np.random.randint(1, 4), np.random.randint(1, 4)
        object2 = random_sprite(n=n2, m=m2, color_palette=[square_colors[1]], background=Color.BLACK, connectivity=8)
        try:
            # Ensure the two patterns do not touch each other
            x, y = random_free_location_for_sprite(grid=pattern, sprite=object2, background=Color.BLACK, padding=1, padding_connectivity=8)
            blit_sprite(pattern, object2, x=x, y=y, background=Color.BLACK)
            break
        except:
            continue

    # Randomly choose a 3x3 square to be the target square
    x_square = np.random.randint(1, square_num - 3)
    y_square = np.random.randint(1, square_num - 3)
    

    # Draw the target square 
    for x, y in np.ndindex(3, 3):
        rela_x = (x_square + x) * (square_size + 1) - 1
        rela_y = (y_square + y) * (square_size + 1) - 1
        # Color the four corners with the color of the pattern
        if pattern[x, y] != Color.BLACK:
            color = pattern[x, y]
            grid[rela_x, rela_y] = color
            grid[rela_x, rela_y + square_size + 1] = color
            grid[rela_x + square_size + 1, rela_y] = color
            grid[rela_x + square_size + 1, rela_y + square_size + 1] = color
        
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
