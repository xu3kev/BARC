from common import *

import numpy as np
from typing import *

# concepts:
# rectangle detection, background shape detection

# description:
# In the input you will see a grid with scattered one color pixels
# To make the output grid, you should detect the 3x3 black square in the random color pattern
# and replace it with a 3x3 blue square

def main(input_grid):
    output_grid = input_grid.copy()
    # Generate the blue square sprite.
    blue_square = random_sprite(n=3, m=3, color_palette=[Color.BLUE], density=1.0)

    # Detect the 3x3 black square with specific color in the random color pattern.
    def detect_square(square_len, grid, posx, posy, square_color):
        width = len(grid)
        height = len(grid[0])
        if posx > width - square_len or posy > height -square_len:
            return False
        else:
            detect_sqaure = True
            for dx in range(3):
                for dy in range(3):
                    if grid[posx + dx][posy + dy] != square_color:
                        detect_sqaure = False
        return detect_sqaure
    
    # Detect the 3x3 black square with specific color in the random color pattern.
    for x, column in enumerate(input_grid):
        for y, item in enumerate(column):
            # Detect the black square with square length with black color from position x,y.
            square_len=3
            width = len(output_grid)
            height = len(output_grid[0])
            # If the current position does not enough space for the square, skip it.
            if x > width - square_len or y > height -square_len:
                detect_sqaure = False
            else:
                # Check if the there is a square with color black and length of square_len.
                detect_sqaure = True
                for dx in range(square_len):
                    for dy in range(square_len):
                        if output_grid[x + dx][y + dy] != Color.BLACK:
                            detect_sqaure = False
            if detect_sqaure:
                # Replace the black square with the blue square.
                output_grid = blit_sprite(grid=output_grid, sprite=blue_square, x=x, y=y)
    return output_grid

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = 20, 20
    grid = np.zeros((n, m), dtype=int)

    # Get the random scatter color pixels on the grid.
    avaliable_colors = [c for c in Color.NOT_BLACK if c != Color.BLUE]
    background_color = np.random.choice(avaliable_colors)
    
    # Generate random color pixels on the grid.
    colored = 0
    density = 0.7
    # Randomly scatter density of color pixels on the grid.
    while colored < density * n * m:
        x = np.random.randint(0, n)
        y = np.random.randint(0, m)
        if grid[x, y] == Color.BLACK:
            grid[x, y] = background_color
            colored += 1

    # Randomly generate the number of black squares.
    square_num = np.random.randint(1, 4)

    # Generate the black squares on the grid.
    square_len = 3
    for _ in range(square_num):
        square = random_sprite(n=square_len, m=square_len, color_palette=[Color.BLACK], density=1.0, background=background_color)
        try:
            # Get the random free location for the black square.
            x, y = random_free_location_for_sprite(grid=grid, sprite=square, background=background_color)
        except:
            continue
        # Blit the black square on the grid.
        grid = blit_sprite(grid=grid, sprite=square, x=x, y=y, background=background_color)
     
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
