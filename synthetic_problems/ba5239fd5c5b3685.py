from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, repetition, object manipulation

# description:
# In the input grid, there are objects of various colors. Each object will be rotated iteratively around the grid center.
# At each rotation iteration, if there is any collision between rotated parts of an object, the resultant color of the collision will be the new color.
# Colors are mixed at collision points (but not combinatorially; should be simple, e.g., always choose a particular color).

def mix_colors(color1, color2):
    # Define a deterministic way to mix colors
    if color1 == color2:
        return color1
    return Color.ORANGE if Color.ORANGE in [color1, color2] else color1  # Example: mixed color priority for simplicity.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros_like(input_grid)
    sym = detect_rotational_symmetry(input_grid)
    
    if not sym:
        return input_grid
    
    for x, y in np.argwhere(input_grid != Color.BLACK):
        center_x, center_y = int(sym.center_x), int(sym.center_y)
        n_iters = 4  # Rotate 90 degrees for 4 iterations.
        init_color = input_grid[x, y]
        
        for i in range(1, n_iters):
            new_x, new_y = sym.apply(x, y, iters=i)
            if output_grid[new_x, new_y] == Color.BLACK:
                output_grid[new_x, new_y] = init_color
            else:
                output_grid[new_x, new_y] = mix_colors(output_grid[new_x, new_y], init_color)

    return output_grid

def generate_input() -> np.ndarray:
    n, m = 10, 10
    input_grid = np.zeros((n, m), dtype=int)
    
    # Define some simple objects
    obj_colors = random.sample(list(Color.NOT_BLACK), 3)
    obj_positions = [(3, 3), (7, 2), (4, 8)]
    
    for color, pos in zip(obj_colors, obj_positions):
        obj_grid = random_sprite(2, 2, color_palette=[color])
        blit(input_grid, obj_grid, pos[0], pos[1])
    
    return input_grid