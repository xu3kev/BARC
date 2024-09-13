from common import *

import numpy as np
from typing import *

# concepts:
# color correspondence, object splitting

# description:
# In the input you will see a 9x9 grid with a 6x6 green sprite and a 2x2 sprite with 4 different colors,
# separated by two teal lines.
# To make the output grid, you should separate the 6x6 green sprite into 4 3x3 sprites and color them 
# with the 4 different colors in the 2x2 sprite, with the same relative position.

def main(input_grid):
    # Find out the intersect point of two teal lines that separate the 6x6 green sprite and the 2x2 sprite.
    for x, row in enumerate(input_grid):
        find_block = False
        for y, item in enumerate(row):
            if x > 0 and x < len(input_grid) and y > 0 and y < len(row) and item == Color.TEAL:
                directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                find_block = True
                for dx, dy in directions:
                    if input_grid[x + dx, y + dy] != Color.TEAL:
                        find_block = False
                        break
                # Find the intersect point of two teal lines.
                if find_block:
                    selected_pos = (x, y)
                    break
        if find_block:
            break
    # Find the position of the 2x2 sprite and the 6x6 green sprite according to the intersect point.
    if selected_pos[0]  == 2:
        x_green = selected_pos[0] + 1
        x_board = 0
    else:
        x_green = 0
        x_board = selected_pos[0] + 1
    
    if selected_pos[1]  == 2:
        y_green = selected_pos[1] + 1
        y_board = 0
    else:
        y_green = 0
        y_board = selected_pos[1] + 1

    # Get the 4 different colors in the 2x2 sprite.
    color_board = np.array([input_grid[x_board, y_board], input_grid[x_board + 1, y_board], input_grid[x_board, y_board + 1], input_grid[x_board + 1, y_board + 1]])
    output_grid = input_grid.copy()

    # Seperate the 6x6 green sprite into 4 3x3 sprites.
    # Color the 6x6 green sprite with the 4 different colors in the 2x2 sprite.
    output_grid[x_green: x_green + 3, y_green: y_green + 3][output_grid[x_green: x_green + 3, y_green: y_green + 3] == Color.GREEN] = color_board[0]
    output_grid[x_green + 3: x_green + 6, y_green: y_green + 3][output_grid[x_green + 3: x_green + 6, y_green: y_green + 3] == Color.GREEN] = color_board[1]
    output_grid[x_green: x_green + 3, y_green + 3: y_green + 6][output_grid[x_green: x_green + 3, y_green + 3: y_green + 6] == Color.GREEN] = color_board[2]
    output_grid[x_green + 3: x_green + 6, y_green + 3: y_green + 6][output_grid[x_green + 3: x_green + 6, y_green + 3: y_green + 6] == Color.GREEN] = color_board[3]
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
    color_board = np.array([[four_colors[0], four_colors[1]], [four_colors[2], four_colors[3]]])

    # Get one random position for the intersect point of two teal lines that 
    # separate the 6x6 green sprite and the 2x2 sprite.
    four_pos = [(2, 2), (2, 6), (6, 2), (6, 6)]
    selected_pos = random.choice(four_pos)

    # Get the position of the 2x2 sprite and the 6x6 green sprite according to the intersect point.
    if selected_pos[0]  == 2:
        x_green = selected_pos[0] + 1
        x_board = 0
    else:
        x_green = 0
        x_board = selected_pos[0] + 1
    
    if selected_pos[1]  == 2:
        y_green = selected_pos[1] + 1
        y_board = 0
    else:
        y_green = 0
        y_board = selected_pos[1] + 1

    # Place the 6x6 green sprite and the 2x2 sprite on the input grid.
    grid = blit_sprite(grid=grid, sprite=green_pattern, x=x_green, y=y_green, background=Color.BLACK)
    grid = blit_sprite(grid=grid, sprite=color_board, x=x_board, y=y_board, background=Color.BLACK)

    # Place two teal lines that separate the 6x6 green sprite and the 2x2 sprite.
    draw_line(grid=grid, color=Color.TEAL, x=selected_pos[0], y=0, direction=(0, 1))
    draw_line(grid=grid, color=Color.TEAL, x=0, y=selected_pos[1], direction=(1, 0))
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
