from common import *

import numpy as np
from typing import *

# concepts:
# proximity, symmetry detection, horizontal/vertical bars

# description:
# In the input, there are two lines on the edge of the canvas (either horizontal or vertical), and there are various colored pixels randomly placed between these lines.
# Change the color of each pixel to match the color of its symmetric counterpart relative to the center of the grid. If the symmetric counterpart is black, the pixel should remain unchanged.


def main(input_grid: np.ndarray) -> np.ndarray:
    # Output grid is initially the same as the input grid
    output_grid = np.copy(input_grid)
    
    n, m = input_grid.shape

    center_x, center_y = n // 2, m // 2
    
    for x in range(n):
        for y in range(m):
            if input_grid[x, y] != Color.BLACK:
                # Calculate symmetric position
                sym_x, sym_y = 2 * center_x - x, 2 * center_y - y
                
                if 0 <= sym_x < n and 0 <= sym_y < m:
                    sym_color = input_grid[sym_x, sym_y]
                    
                    if sym_color != Color.BLACK:
                        output_grid[x, y] = sym_color
    
    return output_grid


def generate_input() -> np.ndarray:
    # Make a random grid with initial size roughly between 10x10 and 20x20
    n, m = random.randint(10, 20), random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # Randomly sprinkle colors in the inner section of the grid
    num_pixels = random.randint(5, 20)
    for _ in range(num_pixels):
        x, y = random.randint(1, n - 2), random.randint(1, m - 2)
        grid[x, y] = random.choice(list(Color.NOT_BLACK))
    
    # Decide on a pair of colors for the horizontal or vertical lines
    line_colors = random.sample(list(Color.NOT_BLACK), 2)
    
    # Flip a coin to decide whether it is horizontal or vertical
    is_horizontal = random.choice([True, False])
    
    if is_horizontal:
        grid[:, 0] = line_colors[0]
        grid[:, -1] = line_colors[1]
    else:
        grid[0, :] = line_colors[0]
        grid[-1, :] = line_colors[1]
    
    return grid