from common import *

import numpy as np
from typing import *

# concepts:
# color stripe, fill the square in order

# description:
# In the input you will see several vertical or horizontal stripes of different colors and a gray square with length equal the number of the stripes.
# To make the output, fill the gray square with the colors of the stripes in the order and direction they appear.

def main(input_grid):
    # Find the gray square in the input grid and get its position and size
    find_grid = detect_objects(grid=input_grid, colors=[Color.GRAY], monochromatic=True, connectivity=4)
    assert len(find_grid) == 1
    pos_x, pos_y, square_len, square_len = bounding_box(find_grid[0])

    # Get the color lines in the input grid
    objects = detect_objects(grid=input_grid, monochromatic=False, connectivity=8)
    lines = []
    x_len_cur, y_len_cur = -1, -1
    if_horizonal = True
    for obj in objects:
        # Get the position and size of the color line
        x_pos, y_pos, x_len, y_len = bounding_box(grid=obj)
        color = obj[x_pos, y_pos]
        if color != Color.GRAY:
            lines.append({'x': x_pos, 'y': y_pos, 'color': color})
            x_len_cur = x_len if x_len_cur == -1 else x_len_cur
            y_len_cur = y_len if y_len_cur == -1 else y_len_cur
            # If the line is horizonal, it's height should always be 1
            if_horizonal = y_len == y_len_cur and if_horizonal

    # Sort the color lines by their position
    if if_horizonal:
        lines = sorted(lines, key=lambda x: x['y'])
    else:
        lines = sorted(lines, key=lambda x: x['x'])
    
    # Get the direction of the stripes
    direction = (1, 0) if if_horizonal else (0, 1)

    # Find the colors lines in the input grid in order
    colors_in_square = [c['color'] for i, c in enumerate(lines) if i == 0 or c['color'] != lines[i - 1]['color']]

    # Draw line on the grid same size of the gray square
    output_grid = np.zeros((square_len, square_len), dtype=int)

    # Fill the gray square with the colors of the stripes in the order and direction they appear
    for i in range(square_len):
        if if_horizonal:
            draw_line(grid=output_grid, x=0, y=i, direction=direction, color=colors_in_square[i])
        else:
            draw_line(grid=output_grid, x=i, y=0, direction=direction, color=colors_in_square[i])
            
    return output_grid

def generate_input():
    # Set stripe's interval
    STRIPE_INTERVAL = 3

    # Initialize the grid, make sure the length and width are not too different
    n, m = np.random.randint(9, 24), np.random.randint(9, 24)
    while n > 1.5 * m or m > 1.5 * n:
        n, m = np.random.randint(9, 24), np.random.randint(9, 24)
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose the starting position of the stripe
    start_from = np.random.randint(0, STRIPE_INTERVAL)

    # Randomly choose the direction of the stripe
    if_horizonal = np.random.choice([True, False])
    direction = (1, 0) if if_horizonal else (0, 1)

    # Calculate the number of stripes given the start position, direction and interval
    num_lines = (m - start_from + STRIPE_INTERVAL - 1) // STRIPE_INTERVAL if if_horizonal else (n - start_from + STRIPE_INTERVAL - 1) // STRIPE_INTERVAL
    
    # Randomly choose the colors of the stripes, each stripe has a different color
    avaliable_colors = [c for c in Color.NOT_BLACK if c != Color.GRAY]
    colors = random.sample(avaliable_colors, num_lines)

    # Draw the stripes
    for i in range(num_lines):
        if if_horizonal:
            x, y = 0, i * STRIPE_INTERVAL + start_from
        else:
            x, y = i * STRIPE_INTERVAL + start_from, 0
        draw_line(grid=grid, x=x, y=y, direction=direction, color=colors[i])

    # Draw the gray square and its black border, the length of the square is the same as the number of the stripes
    square_x, square_y = np.random.randint(0, n - (num_lines + 1)), np.random.randint(0, m - (num_lines + 1))
    black_border = np.zeros((num_lines + 2, num_lines + 2), dtype=int)
    grid = blit_sprite(grid, black_border, square_x, square_y, background=Color.GRAY)
    gray_object = random_sprite(n=num_lines, m=num_lines, color_palette=[Color.GRAY], density=1.0)
    grid = blit_sprite(grid, gray_object, square_x + 1, square_y + 1)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
