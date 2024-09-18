from common import *
import numpy as np
from typing import *

# concepts:
# pattern reconstruction

# description:
# In the input you will see 9 squares seperated by 4 lines. The top-left square contains the original pattern.
# Each square contains either a small portion of pattern or remains empty.
# To make the output, you should detect the pattern on the top-left square and fill each square 

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create a copy of the input grid to avoid modifying the original
    output_grid = np.copy(input_grid)  

    # Detect the color of the lines
    for x, row in enumerate(output_grid):
        # Find the line
        all_equal = np.unique(row).size == 1
        if all_equal:
            line_color = row[0]
            break
    
    # Get all the squares seperated by lines in the grid
    squares = detect_objects(grid=output_grid, background=line_color, monochromatic=False, connectivity=4)
    cropped_square  = []
    for obj in squares:
        square = crop(grid=obj, background=line_color)
        cropped_square.append(square)
    
    # Get the length of the square and the length of the grid
    sqare_len = cropped_square[0].shape[0]
    grid_len = output_grid.shape[0]     

    # Iterate over each square within the grid
    for i in range(0, grid_len, sqare_len + 1):
        for j in range(0, grid_len, sqare_len + 1):
            # Check each cell within the pattern of the current square
            for x in range(0, sqare_len):
                for y in range(0, sqare_len):
                    # If the cell is the missing part of the top-left pattern, fill it with the line color
                    if output_grid[i + x, j + y] != output_grid[x, y]:  
                        output_grid[i + x, j + y] = line_color 
    return output_grid

def generate_input() -> np.ndarray:
    # Define the base cofiguration of the grid seperated by chessboard lines
    # Randomly select the size of the squares, create a 3x3 grid of squares
    square_len = np.random.choice([5, 7, 9])
    pattern_len = square_len - 2
    square_num = 3

    # Size of the grid is grid length plus line length
    n, m = square_len * square_num + square_num - 1, square_len * square_num + square_num - 1
    grid = np.zeros((n, m), dtype=int)

    # Select two colors for the lines and the pattern
    colors = Color.NOT_BLACK.copy()
    line_color = random.choice(colors)  
    colors.remove(line_color)
    pattern_color = random.choice(colors) 

    # Fill specific rows and columns with the line color
    for i in range(square_len, n, square_len + 1):
        draw_line(grid=grid, x=i, y=0, color=line_color, direction=(0, 1))
        draw_line(grid=grid, x=0, y=i, color=line_color, direction=(1, 0))

    # Create the pattern in the top-left square with the pattern color
    sprite = random_sprite(n=pattern_len, m=pattern_len, color_palette=[pattern_color], connectivity=8, density=0.5)

    # Fill the top-left square with the origianl pattern
    # Fill the left squares with parts of the pattern
    for i in range(0, n, square_len + 1):
        for j in range(0, m, square_len + 1):
            sprite_ = sprite.copy()
            for x in range(0, pattern_len):
                for y in range(0, pattern_len):
                    # Randomly set cells to black if they are not in the top-left corner
                    if (i != 0 or j != 0) and random.choice([0, 1]) == 0:
                        sprite_[x, y] = Color.BLACK
            # Place the sprite on the grid, remain a black border around the sprite
            blit(grid, sprite_, i + 1, j + 1)  
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
