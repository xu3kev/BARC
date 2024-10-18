from common import *

import numpy as np
from typing import *

# concepts:
# growing, connecting

# description:
# In the input you will see two pixels of different colors aligned horizontally or vertically.
# To make the output, you need to connect the two pixels with two lines and a hollow rectangle of size 4x5 in the middle.
# Half of the rectangle is colored with the color of the one side's pixel, and the other half with the color of the other side's pixel.

def main(input_grid):
    # Plan:
    # 1. Parse the input
    # 2. Canonicalize the input: because it could be horizontal or vertical, rotate to make horizontal (we will rotate back at the end)
    # 3. Prepare a 4x5 rectangle sprite whose left half is left_color and right half is right_color
    # 4. Place the rectangle in the middle of the two pixels
    # 5. Draw lines to connect the original two pixels with the rectangle
    # 6. Rotate the grid back if it was not originally horizontal

    # 1. Input parsing
    # Extract the two pixels from the input grid
    pixels = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # 2. Canonicalize the input: Ensure that the two pixels are horizontally aligned
    # Check if the two pixels are horizontally aligned
    was_originally_horizontal = object_position(pixels[0])[1] == object_position(pixels[1])[1]
    
    # If the two pixels are not horizontally aligned, rotate the grid for easier processing
    if not was_originally_horizontal:
        input_grid = np.rot90(input_grid)
        pixels = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    
    # we draw on top of the input
    output_grid = input_grid.copy()

    # Prepare for what follows: extract properties of the input here
    # Sort the two horizontally-aligned pixels by their position, from left to right
    pixels = sorted(pixels, key=lambda x: object_position(x)[0])
    # Get the position of the two pixels
    left_pos = object_position(pixels[0])
    right_pos = object_position(pixels[1])
    left_color = object_colors(pixels[0])[0]
    right_color = object_colors(pixels[1])[0]
    
    # 3. Prepare hollow 4x5 rectangle sprite whose left half is left_color and right half is right_color
    rectangle_width, rectangle_height = 4, 5
    rectangle_sprite = np.full((rectangle_width, rectangle_height), Color.BLACK)
    rectangle_sprite[0, :] = left_color
    rectangle_sprite[-1, :] = right_color
    rectangle_sprite[:rectangle_width//2, 0] = left_color
    rectangle_sprite[rectangle_width//2:, 0] = right_color
    rectangle_sprite[:rectangle_width//2, -1] = left_color
    rectangle_sprite[rectangle_width//2:, -1] = right_color

    # 4. Place the rectangle in the middle of the two pixels
    middle_x = (left_pos[0] + right_pos[0] + 1) // 2
    middle_y = left_pos[1]
    blit_sprite(output_grid, sprite=rectangle_sprite, x=middle_x - rectangle_width // 2, y=middle_y - rectangle_height // 2)

    # 5. Draw lines that connect the original two pixels with the rectangle
    draw_line(grid=output_grid, x=left_pos[0]+1, y=left_pos[1], direction=(1, 0), color=left_color, stop_at_color=Color.NOT_BLACK)
    draw_line(grid=output_grid, x=right_pos[0]-1, y=right_pos[1], direction=(-1, 0), color=right_color, stop_at_color=Color.NOT_BLACK)

    # 6. If the grid is not horizontal, rotate it back
    if not was_originally_horizontal:
        output_grid = np.rot90(output_grid, k=-1)

    return output_grid

def generate_input():
    # Generate a random background grid
    # Make sure the grid's width is greater than its height
    width, height = random.randint(15, 20), random.randint(10, 15)
    grid = np.zeros((width, height), dtype=int)

    # Get the color of two pixels
    colors = np.random.choice(Color.NOT_BLACK, 2, replace=False)
    color1, color2 = colors

    # Place the two pixels on the grid horizontally (randomly rotate at the end to get a variety of orientations)
    x1 = np.random.randint(0, width)
    x2 = np.random.randint(0, width)
    y = np.random.randint(0, height)

    # Ensure there is enough horizontal distance to place the 4x5 rectangle
    distance = abs(x2 - x1)
    rectangle_width, rectangle_height = 4, 5
    if distance < rectangle_width+1: return generate_input()

    # Ensure the remaining distance is odd, so that we can split the pixel colors in half between them
    if (distance - rectangle_width) % 2 != 1: return generate_input()

    # Ensure there is enough vertical space to place the rectangle
    if y < rectangle_height // 2 or y + rectangle_height // 2 >= height: return generate_input()    

    # Place the two pixels on the grid
    grid[x1, y] = color1
    grid[x2, y] = color2

    # Randomly rotate the whole grid
    if np.random.rand() < 0.5:
        grid = np.rot90(grid)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
