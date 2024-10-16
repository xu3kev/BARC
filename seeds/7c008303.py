from common import *

import numpy as np
from typing import *

# concepts:
# color correspondence, object splitting

# description:
# In the input you will see a 9x9 grid with a 6x6 green sprite and a 2x2 sprite with 4 different colors separated by two teal lines.
# To make the output grid, you should separate the 6x6 green sprite into 4 3x3 sub-sprites and color them 
# with the 4 different colors in the 2x2 sprite, with the same relative position.

def main(input_grid):
    # Detect four parts seperated by two intersected teal lines.
    sub_grids = find_connected_components(grid=input_grid, connectivity=4, monochromatic=False, background=Color.TEAL)

    # Find the green pattern and square with four colors as a coloring guidance.
    for sub_grid in sub_grids:
        cropped_sub_grid = crop(grid=sub_grid, background=Color.TEAL)

        # If this part is the color guide, then store the color guide.
        if np.all(cropped_sub_grid != Color.BLACK) and np.all(cropped_sub_grid != Color.GREEN):
            color_guide = cropped_sub_grid

        # If this part is the green pattern, then store the green pattern.s
        elif np.any(cropped_sub_grid == Color.GREEN):
            green_pattern = cropped_sub_grid
    
    # Caculate the size of four sub-sprites on green pattern to be colored.
    width_green, height_green = green_pattern.shape
    width_green_half, height_green_half = width_green // 2, height_green // 2
    
    # Color each sub-sprite on the green pattern follow the color guide: with the color in same relative position.
    green_pattern[0: width_green_half, 0: height_green_half][green_pattern[0: width_green_half, 0: height_green_half] == Color.GREEN] = color_guide[0, 0]
    green_pattern[width_green_half: width_green, 0: height_green_half][green_pattern[width_green_half: width_green, 0: height_green_half] == Color.GREEN] = color_guide[1, 0]
    green_pattern[0: width_green_half, height_green_half: height_green][green_pattern[0: width_green_half, height_green_half: height_green] == Color.GREEN] = color_guide[0, 1]
    green_pattern[width_green_half: width_green, height_green_half: height_green][green_pattern[width_green_half: width_green, height_green_half: height_green] == Color.GREEN] = color_guide[1, 1]

    output_grid = green_pattern
    return output_grid

def generate_input():
    # Initialize the 9x9 grid with black color.
    n, m = 9, 9
    grid = np.zeros((n, m), dtype=int)

    # Get available colors for the 2x2 sprite.
    available_colors = [c for c in Color.NOT_BLACK if c != Color.GREEN and c != Color.TEAL]

    # Generate the 6x6 green sprite with random pattern.
    green_pattern = random_sprite(n=6, m=6, color_palette=[Color.GREEN], density=0.3)

    # Get four different colors for the 2x2 sprite.
    four_colors = random.sample(available_colors, 4)
    color_guide = np.array([[four_colors[0], four_colors[1]], [four_colors[2], four_colors[3]]])

    x_green, y_green = 3, 3
    x_board, y_board = 0, 0

    # Place the 6x6 green sprite and the 2x2 sprite on the input grid.
    grid = blit_sprite(grid=grid, sprite=green_pattern, x=x_green, y=y_green, background=Color.BLACK)
    grid = blit_sprite(grid=grid, sprite=color_guide, x=x_board, y=y_board, background=Color.BLACK)

    # Place two teal lines that separate the 6x6 green sprite and the 2x2 sprite.
    draw_line(grid=grid, color=Color.TEAL, x=x_board + 2, y=0, direction=(0, 1))
    draw_line(grid=grid, color=Color.TEAL, x=0, y=y_board + 2, direction=(1, 0))

    # Randomly rotate the input grid.
    grid = np.rot90(grid, np.random.randint(0, 4))
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
