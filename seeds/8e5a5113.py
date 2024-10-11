from common import *

import numpy as np
from typing import *

# concepts:
# rotate, position

# description:
# In the input you will see a grid with 3 squares separated by lines, the first square is the template square
# with a pattern. The other 2 squares are black squares.
# To make the output, rotate the template square 90 degree clockwise and place it in the first black squares.
# Rotate the template square 180 degree clockwise and place it in the second black square.

def main(input_grid):
    # Get all the squares in the input grid
    line_color = Color.GRAY
    squares = find_connected_components(grid=input_grid, connectivity=4, background=line_color, monochromatic=False)

    # Crop all the squares out and get their positions
    cropped_squares = []
    for square in squares:
        x, y, n, m = bounding_box(grid=square, background=line_color)
        cropped_square = crop(grid=square, background=line_color)
        cropped_squares.append({'x': x, 'y': y, 'n': n, 'm': m, 'square': cropped_square})
    
    # Sort the cropped squares by x position
    cropped_squares = sorted(cropped_squares, key=lambda x: x['x'])

    # Get the template square, which is the first square in the sorted list
    template_square = cropped_squares[0]['square']

    # Get the black squares, which are the rest of the squares in the sorted list
    black_squares = cropped_squares[1:]
    output_grid = input_grid.copy()

    # Place the rotated template square in the output grid
    for cnt, black_square in enumerate(black_squares):
        # Rotate the template square 90 degree by pos times
        pos = cnt + 1
        rotated_template_square = np.rot90(template_square, k=pos)

        # Place the rotated template square in the black square
        x, y = black_square['x'], black_square['y']
        output_grid = blit_sprite(grid=output_grid, sprite=rotated_template_square, x=x, y=y)
    
    return output_grid

def generate_input():
    # Create a grid with 3 squares separated by lines
    square_num = 3
    square_size = np.random.randint(3, 6)
    line_num = square_num - 1
    n, m = 3 * square_size + line_num, square_size
    grid = np.zeros((n, m), dtype=int)

    # Draw lines
    line_color = Color.GRAY
    for x in range(square_size, n, square_size + 1):
        grid = draw_line(grid=grid, x=x, y=0, direction=(0, 1), color=line_color)

    # Draw one square pattern
    pattern_color_num = 3
    remain_color = [color for color in Color.NOT_BLACK if color != line_color]
    square_colors = np.random.choice(remain_color, pattern_color_num, replace=False)  
    square_pattern = random_sprite(n=square_size, m=square_size, color_palette=square_colors, density=1.0)

    # Place the template pattern in the first black square on the grid
    x, y = 0, 0
    grid = blit_sprite(grid=grid, sprite=square_pattern, x=x, y=y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
