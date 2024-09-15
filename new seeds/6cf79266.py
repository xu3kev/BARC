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
        detect_sqaure = True
        for dx in range(3):
            for dy in range(3):
                if grid[posx + dx][posy + dy] != square_color:
                    detect_sqaure = False
        return detect_sqaure
    
    # Detect the 3x3 black square with specific color in the random color pattern.
    for x, column in enumerate(input_grid):
        for y, item in enumerate(column):
            if_detect_square = detect_square(square_len=3, grid=output_grid, posx=x, posy=y, square_color=Color.BLACK)
            if if_detect_square:
                # Replace the 3x3 black square with the blue square.
                output_grid = blit_sprite(grid=output_grid, sprite=blue_square, x=x, y=y)
    return output_grid

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = 20, 20
    grid = np.zeros((n, m), dtype=int)

    # Get the random scatter color pixels on the grid.
    avaliable_colors = [c for c in Color.NOT_BLACK if c != Color.BLUE]
    background_color = np.random.choice(avaliable_colors)

    # Randomly scatter color pixels on the grid.
    def random_scatter_point_on_grid(grid, color, density):
        n, m = grid.shape
        colored = 0
        # Randomly scatter density of color pixels on the grid.
        while colored < density * n * m:
            x = np.random.randint(0, n)
            y = np.random.randint(0, m)
            if grid[x, y] == Color.BLACK:
                grid[x, y] = color
                colored += 1
        return grid
    
    # Generate random color pixels on the grid.
    grid = random_scatter_point_on_grid(grid=grid, color=background_color, density=0.7)

    # Randomly generate the number of black squares.
    square_num = np.random.randint(1, 4)

    # Generate the black squares on the grid.
    for _ in range(square_num):
        square = random_sprite(n=3, m=3, color_palette=[Color.BLACK], density=1.0, background=background_color)
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
