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
    squares = find_connected_components(grid=output_grid, background=line_color, monochromatic=False, connectivity=4)

    # Get all squares' bounding box and cropped pattern
    cropped_squares  = []
    for obj in squares:
        x, y, width, height = bounding_box(grid=obj, background=line_color)
        square = crop(grid=obj, background=line_color)
        cropped_squares.append({'x': x, 'y': y, 'len': width, 'pattern': square})

    # Sort the squares by their position
    cropped_squares = sorted(cropped_squares, key=lambda x: (x['x'], x['y']))

    # The top-left square contains the original pattern
    template_pattern = cropped_squares[0]['pattern']
    other_patterns = cropped_squares[1:]

    # Fill the missing pattern compared to template square with line color
    for square in other_patterns:
        x, y = square['x'], square['y']
        square_pattern = square['pattern']

        # Fill the missing pattern compared to template square with line color
        for i, j in np.argwhere(template_pattern != Color.BLACK):
            if template_pattern[i, j] != square_pattern[i, j]:
                square_pattern[i, j] = line_color

        # Place the reconstructed pattern on the output grid
        output_grid = blit_sprite(grid=output_grid, sprite=square_pattern, x=x, y=y)

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
    template_sprite = random_sprite(n=pattern_len, m=pattern_len, color_palette=[pattern_color], connectivity=8, density=0.5)

    # Fill the top-left square with the original pattern
    # Fill the other regions with corrupted versions that have pixels randomly set to black
    for i in range(0, n, square_len + 1):
        for j in range(0, m, square_len + 1):
            # are we the top-left region?
            if i == 0 and j == 0:
                blit_sprite(grid, template_sprite, i + 1, j + 1)
                continue

            # otherwise: Create a corrupted version of the pattern; randomly set some pixels to black
            corrupted_sprite = template_sprite.copy()
            for x, y in np.argwhere(corrupted_sprite != Color.BLACK):
                if random.choice([0, 1]) == 0:
                    corrupted_sprite[x, y] = Color.BLACK
            # Place the sprite on the grid, remain a black border around the sprite
            blit_sprite(grid, corrupted_sprite, i + 1, j + 1)  
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
