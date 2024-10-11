from common import *
import numpy as np
from typing import *

# concepts:
# counting, color

# description:
# In the input you will see a grid with several squares separated by lines of the same color.
# Each square has several pixels of the same color.
# To make the output, fill the square with the most colored pixels with its color,
# fill the other squares with black.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create a copy of the input grid to avoid modifying the original
    output_grid = np.copy(input_grid)  

    # Get all the squares seperated by lines in the grid
    line_color = Color.GRAY
    squares = find_connected_components(grid=output_grid, background=line_color, monochromatic=False, connectivity=4)

    # Get all squares' bounding box and cropped pattern
    cropped_squares  = []
    max_num_pixels = 0
    for obj in squares:
        x, y, width, height = bounding_box(grid=obj, background=line_color)
        square = crop(grid=obj, background=line_color)
        cropped_squares.append({'x': x, 'y': y, 'len': width, 'pattern': square, 'num_pixels': np.sum(square != Color.BLACK)})
        max_num_pixels = max(max_num_pixels, np.sum(square != Color.BLACK))
    # Sort the squares by their position
    cropped_squares = sorted(cropped_squares, key=lambda x: (x['x'], x['y']))

    # Calculate colored pixels' number in each square
    # Fill the square with most colored pixels with its color
    # Fill the other squares with black
    for square in cropped_squares:
        x, y = square['x'], square['y']
        square_pattern = square['pattern']

        if square['num_pixels'] == max_num_pixels:
            # Fill the square with the color of the pattern
            square_color = np.unique(square_pattern)[1]
            filled_square = np.full_like(square_pattern, fill_value=square_color)    
            output_grid = blit_sprite(grid=output_grid, sprite=filled_square, x=x, y=y, background=line_color)
        else:
            # Fill the square with black
            black_square = np.full_like(square_pattern, fill_value=Color.BLACK)
            output_grid = blit_sprite(grid=output_grid, sprite=black_square, x=x, y=y, background=line_color)

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
    line_color = Color.GRAY 
    colors.remove(line_color)
    pattern_color = random.choice(colors) 

    # Fill specific rows and columns with the line color
    for i in range(square_len, n, square_len + 1):
        draw_line(grid=grid, x=i, y=0, color=line_color, direction=(0, 1))
        draw_line(grid=grid, x=0, y=i, color=line_color, direction=(1, 0))


    # Add different density of pixels to each square
    for i in range(0, n, square_len + 1):
        for j in range(0, m, square_len + 1):
            # Randomly select the density of the square
            square_background = np.zeros((square_len, square_len), dtype=int)
            density = np.random.randint(1, pattern_len * pattern_len) / (pattern_len * pattern_len)

            # Randomly scatter the color in the square
            square_background = random_scatter_points(grid=square_background, color=pattern_color, density=density)
            grid = blit_sprite(grid=grid, sprite=square_background, x=i, y=j)
        
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)