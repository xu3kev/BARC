from common import *

import numpy as np
from typing import *

# concepts:
# patterns, incrementing, repetition, lines

# description:
# In the input, you will see a grid with several small vertical bars of random lengths made up of different colors.
# To make the output, have each bar grow one pixel taller in each iteration while maintaining its original color until the bar hits the top or bottom of the grid.
# Repeat this pattern until there is no more space on the grid.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # Iterating maximum possible times to ensure all bars reach the grid border
    for _ in range(input_grid.shape[0]):
        new_growth = []
        for x in range(input_grid.shape[0]):
            for y in range(input_grid.shape[1]):
                if input_grid[x, y] != Color.BLACK:
                    color = input_grid[x, y]
                    
                    # Grow upwards
                    if x > 0 and output_grid[x - 1, y] == Color.BLACK:
                        new_growth.append((x - 1, y, color))
                    
                    # Grow downwards
                    if x < input_grid.shape[0] - 1 and output_grid[x + 1, y] == Color.BLACK:
                        new_growth.append((x + 1, y, color))
        
        if not new_growth:
            break
        
        for x, y, color in new_growth:
            output_grid[x, y] = color

    return output_grid

def generate_input():
    n = np.random.randint(5, 10)  # Number of rows
    m = np.random.randint(10, 15) # Number of columns
    grid = np.zeros((n, m), dtype=int)

    num_bars = np.random.randint(3, 6)  # Number of vertical bars
    
    for _ in range(num_bars):
        start_y = np.random.randint(0, m)
        start_x = np.random.randint(0, n)
        bar_length = np.random.randint(1, n//2 + 1)
        color = random.choice(Color.NOT_BLACK)

        for i in range(bar_length):
            if start_x + i < n:
                grid[start_x + i, start_y] = color

    return grid