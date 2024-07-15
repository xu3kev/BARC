from common import *

import numpy as np
from typing import *

# concepts:
# counting, resizing

# description:
# In the input, you will see a grid with a row of colored blocks on the bottom and the right. 
# There is also a square in the top left that is not touching the other colors.
# To make the output:
# 1. count the number of colors that aren't black
# 2. enlarge every pixel in the input by a factor of the number of colors
# 3. add diagonal red lines coming out of the corners of the square in the top left portion of the grid

def main(input_grid):
    # count the number of colors that aren't black
    num_colors = len(set(input_grid.flatten())) - 1

    # magnify the pixels in input grid onto the output grid
    output_grid = np.repeat(np.repeat(input_grid, num_colors, axis=0), num_colors, axis=1)

    # find the square in the output grid
    objects = find_connected_components(output_grid, connectivity=8, monochromatic=False)
    for obj in objects:
        # the square is the only object not in the bottom right corner
        if obj[-1,-1] == Color.BLACK:
            square = obj
            break
    
    # find the bounding box of the square
    x, y, w, h = bounding_box(square)

    # draw the diagonal red lines
    draw_line(output_grid, x - 1, y - 1, length=None, color=Color.RED, direction=(-1,-1), stop_at_color=Color.NOT_BLACK)
    draw_line(output_grid, x + w, y + h, length=None, color=Color.RED, direction=(1,1), stop_at_color=Color.NOT_BLACK)
    draw_line(output_grid, x - 1, y + h, length=None, color=Color.RED, direction=(-1,1), stop_at_color=Color.NOT_BLACK)
    draw_line(output_grid, x + w, y - 1, length=None, color=Color.RED, direction=(1,-1), stop_at_color=Color.NOT_BLACK)

    return output_grid

def generate_input():
    # make a 5x5 black grid for the background
    n = m = 5
    grid = np.zeros((n,m), dtype=int)

    # pick the colors for the bottom and right of the grid
    colors = list(Color.NOT_BLACK)

    # construct a random sequence of colors for the bottom and right of the grid
    # don't repeat a color in the sequence
    sequence = []
    while len(sequence) < 5:
        # select a color
        color = np.random.choice(colors)
        # remove the color from the array of remaining colors
        colors = np.delete(colors, np.where(colors == color))
        length = np.random.randint(1, 6 - len(sequence))
        sequence.extend([color] * length)

    # put the same sequence on the bottom and right of the grid
    grid[-1, :] = sequence
    grid[:, -1] = sequence

    # pick the color of the square
    square_color = np.random.choice(list(Color.NOT_BLACK))
    
    # make the square
    square_sprite = random_sprite(2, 2, density=1, color_palette=[square_color])

    # put the square on the grid so it doesn't touch the bottom or right
    x, y = random_free_location_for_sprite(grid, square_sprite, padding=1)
    blit_sprite(grid, square_sprite, x, y)
    
    return grid




# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
