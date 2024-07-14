from common import *

import numpy as np
from typing import *

# concepts:
# counting, incrementing, colors as indicators, repeating patterns

# description:
# In the input, you will see a single row with pixels of various colors.
# To make the output:
# 1. Take the input row as the first row of the output
# 2. For each subsequent row:
#    - If the pixel above is black, copy it
#    - If the pixel above is colored, change it to the next color in the sequence:
#      BLUE -> RED -> GREEN -> YELLOW -> GREY -> PINK -> ORANGE -> TEAL -> MAROON -> BLUE
# 3. Repeat until the number of rows equals the number of non-black pixels in the original input row

def main(input_grid):
    # Define the color sequence
    color_sequence = [Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW, Color.GREY, 
                      Color.PINK, Color.ORANGE, Color.TEAL, Color.MAROON]
    
    # Count non-black pixels in the input row
    non_black_count = np.sum(input_grid != Color.BLACK)
    
    # Create the output grid
    output_grid = np.zeros((non_black_count, input_grid.shape[1]), dtype=object)
    output_grid[0] = input_grid[0]  # Copy the input row as the first row
    
    # Fill in the subsequent rows
    for row in range(1, non_black_count):
        for col in range(input_grid.shape[1]):
            if output_grid[row-1, col] == Color.BLACK:
                output_grid[row, col] = Color.BLACK
            else:
                current_color_index = color_sequence.index(output_grid[row-1, col])
                next_color_index = (current_color_index + 1) % len(color_sequence)
                output_grid[row, col] = color_sequence[next_color_index]
    
    return output_grid

def generate_input():
    # Decide the length of the row
    length = np.random.randint(5, 15)
    
    # Create a row with random colors (including black)
    color_options = list(Color.ALL_COLORS)
    row = np.array([np.random.choice(color_options) for _ in range(length)])
    
    # Ensure there's at least one non-black pixel
    if np.all(row == Color.BLACK):
        row[np.random.randint(length)] = np.random.choice(list(Color.NOT_BLACK))
    
    # Make this row the entire grid
    grid = row.reshape(1, -1)
    
    return grid