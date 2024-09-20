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
    gray_rectangle = detect_objects(grid=input_grid, colors=[Color.GRAY], monochromatic=True, connectivity=4)[0]
    output_grid = crop(grid=gray_rectangle)

    # Get the color lines in the input grid
    objects = detect_objects(grid=input_grid, monochromatic=False, connectivity=8)
    lines = []
    for obj in objects:
        # Get the position and size of the color line
        x_pos, y_pos, x_len, y_len = bounding_box(grid=obj)
        color = obj[x_pos, y_pos]
        if color != Color.GRAY:
            lines.append({'x': x_pos, 'y': y_pos, 'color': color, 'x_len': x_len, 'y_len': y_len})
    
    # Check if the stripes are horizontal or vertical
    is_horizontal = all(line['y_len'] == 1 for line in lines)

    # Sort the color lines by their position
    if is_horizontal:
        lines = sorted(lines, key=lambda x: x['y'])
    else:
        lines = sorted(lines, key=lambda x: x['x'])
    
    # Get the direction of the stripes
    direction = (1, 0) if is_horizontal else (0, 1)

    # Find the colors lines in the input grid in order
    colors_in_square = [c['color'] for i, c in enumerate(lines) if i == 0 or c['color'] != lines[i - 1]['color']]

    # Fill the gray square with the colors of the stripes in the order and direction they appear
    for i in range(len(output_grid)):
        # Draw horizontal line
        if is_horizontal:
            draw_line(grid=output_grid, x=0, y=i, direction=direction, color=colors_in_square[i])
        # Draw vertical line
        else:
            draw_line(grid=output_grid, x=i, y=0, direction=direction, color=colors_in_square[i])
            
    return output_grid

def generate_input():
    # Initialize the grid, make sure the length and width are not too different
    n, m = np.random.randint(9, 24), np.random.randint(9, 24)
    while n > 1.5 * m or m > 1.5 * n:
        n, m = np.random.randint(9, 24), np.random.randint(9, 24)
    grid = np.zeros((n, m), dtype=int)

    # Set stripe's interval
    STRIPE_INTERVAL = 3

    # Randomly choose the starting position of the stripe
    start_from = np.random.randint(0, STRIPE_INTERVAL)

    # Calculate the number of horizontal stripes given the start position, direction and interval
    num_lines = (m - start_from + STRIPE_INTERVAL - 1) // STRIPE_INTERVAL
    
    # Randomly choose the colors of the stripes, each stripe has a different color
    avaliable_colors = [c for c in Color.NOT_BLACK if c != Color.GRAY]
    colors = random.sample(avaliable_colors, num_lines)

    # Draw horizontal stripes with different colors
    for i in range(num_lines):
        x, y = 0, i * STRIPE_INTERVAL + start_from
        draw_line(grid=grid, x=x, y=y, direction=(1, 0), color=colors[i])

    # Draw the gray square and its black border, the length of the square is the same as the number of the stripes
    square_x, square_y = np.random.randint(0, n - (num_lines + 1)), np.random.randint(0, m - (num_lines + 1))
    black_border = np.full((num_lines + 2, num_lines + 2), Color.BLACK)
    gray_object = np.full((num_lines, num_lines), Color.GRAY)
    grid = blit_sprite(grid, black_border, square_x, square_y, background=Color.GRAY)
    grid = blit_sprite(grid, gray_object, square_x + 1, square_y + 1)

    # Randomly rotate the grid
    grid = np.rot90(grid, 1) if np.random.choice([True, False]) else grid

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
