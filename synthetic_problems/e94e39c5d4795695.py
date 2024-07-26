from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, patterns, repetition, color change

# description:
# In the input, you will see a grid containing a pattern consisting of a sequence of identical shapes placed in a 2x2 grid pattern.
# Each shape in one quadrant will have one unique color. The remaining sections in all shapes will be black.
# Your task is to identify the unique color in each quadrant of the 2x2 grid, then generate an output that is a 2x2 tiling of those colors in their respective quadrants.

def main(input_grid):
    n, m = input_grid.shape
    assert n % 2 == 0 and m % 2 == 0, "Input grid dimensions should be even."
    
    # Get the size of each quadrant
    quad_size = (n // 2, m // 2)
    
    quadrant_colors = []
    for i in range(2):
        for j in range(2):
            # Extract the section corresponding to the current quadrant
            quadrant = input_grid[i*quad_size[0]: (i+1)*quad_size[0], j*quad_size[1]: (j+1)*quad_size[1]]
            
            # Identify the unique non-black color in this quadrant
            unique_colors = set(quadrant.flatten()) - {Color.BLACK}
            assert len(unique_colors) == 1, f"Unexpected number of unique colors in quadrant {i},{j}, found {len(unique_colors)}"
            quadrant_color = unique_colors.pop()
            
            quadrant_colors.append(quadrant_color)
    
    color_mapping = [
        [quadrant_colors[0], quadrant_colors[1]],
        [quadrant_colors[2], quadrant_colors[3]]
    ]
    
    # Create the output grid
    output_grid = np.zeros_like(input_grid)
    
    # Fill in the output grid with the identified colors in the proper 2x2 tiling pattern
    for i in range(2):
        for j in range(2):
            output_grid[i*quad_size[0]: (i+1)*quad_size[0], j*quad_size[1]: (j+1)*quad_size[1]] = color_mapping[i][j]
    
    return output_grid


def generate_input():
    n, m = 12, 12 # You can vary n and m for different sizes, just ensure they are multiples of 2
    
    grid = np.zeros((n, m), dtype=int)
    
    # Define unique colors for the quadrants
    colors = random.sample(Color.NOT_BLACK, 4)
    
    for i in range(2):
        for j in range(2):
            quadrant_color = colors[i * 2 + j]
            
            # Adding a random pattern (e.g., a random rotated 'L' shape) in each quadrant
            l_pattern = random.choice([["*", ".", "*", "*"], ["*", "*", ".", "."], [".", "*", "*", "*"], ["*", "*", "*", "."]])
            l_grid = np.array(l_pattern).reshape(2, 2)
            l_grid[l_grid == "*"] = quadrant_color
            l_grid[l_grid == "."] = Color.BLACK
            
            start_x, start_y = i * (n // 2), j * (m // 2)
            
            for dx in range(2):
                for dy in range(2):
                    grid[start_x + dx, start_y + dy] = l_grid[dx, dy]
    
    return grid