from common import *

import numpy as np
from typing import *

# concepts:
# patterns, growing, colors as indicators, repeating patterns

# description:
# In the input, you will see a colored square (the "seed") surrounded by a ring of pixels of a different color (the "soil").
# To make the output, grow the seed in all eight directions (including diagonals) until it reaches the edge of the grid or another growing seed.
# If two growing seeds meet, they stop growing at that point.
# The soil ring disappears in the output, replaced by the growing seed or empty space.

def main(input_grid):
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Find all seeds and their soil
    seeds = []
    for y in range(1, height-1):
        for x in range(1, width-1):
            if input_grid[y, x] != Color.BLACK:
                if all(input_grid[y+dy, x+dx] != input_grid[y, x] for dy, dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]):
                    seeds.append((y, x, input_grid[y, x]))
                    
    # Remove soil
    for y, x, color in seeds:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if input_grid[y+dy, x+dx] != color and input_grid[y+dy, x+dx] != Color.BLACK:
                    output_grid[y+dy, x+dx] = Color.BLACK
    
    # Grow seeds
    while seeds:
        new_seeds = []
        for y, x, color in seeds:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < height and 0 <= nx < width and output_grid[ny, nx] == Color.BLACK:
                        output_grid[ny, nx] = color
                        new_seeds.append((ny, nx, color))
        seeds = new_seeds
    
    return output_grid

def generate_input():
    size = np.random.randint(10, 20)
    grid = np.zeros((size, size), dtype=int)
    
    num_seeds = np.random.randint(2, 5)
    colors = np.random.choice(list(Color.NOT_BLACK), size=num_seeds*2, replace=False)
    
    for i in range(num_seeds):
        seed_color = colors[i*2]
        soil_color = colors[i*2+1]
        
        x = np.random.randint(1, size-2)
        y = np.random.randint(1, size-2)
        
        grid[y, x] = seed_color
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy != 0 or dx != 0:
                    grid[y+dy, x+dx] = soil_color
    
    return grid