from common import *

import numpy as np
from typing import *

# concepts:
# pixel manipulation, growing, color, objects

# description:
# In the input, you will see several colored squares of different sizes (1x1, 2x2, or 3x3) on a black background.
# To make the output, transform each square as follows:
# - For 1x1 squares: Grow the square into a 3x3 cross, with the original color in the center and arms.
# - For 2x2 squares: Grow the square into a 4x4 diamond shape, with the original color forming the diamond.
# - For 3x3 squares: Grow the square into a 5x5 square with rounded corners (i.e., a 3x3 square with 1-pixel protrusions on each side).
# If growing causes overlap between shapes, the later shape (in reading order) takes precedence.

def main(input_grid):
    output_grid = np.full_like(input_grid, Color.BLACK)
    objects = find_connected_components(input_grid, background=Color.BLACK)
    
    for obj in objects:
        x, y, w, h = bounding_box(obj)
        color = obj[obj != Color.BLACK][0]
        
        if w == 1 and h == 1:  # 1x1 square
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 or dy == 0:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < output_grid.shape[0] and 0 <= ny < output_grid.shape[1]:
                            output_grid[nx, ny] = color
        
        elif w == 2 and h == 2:  # 2x2 square
            for dx in [-1, 0, 1, 2]:
                for dy in [-1, 0, 1, 2]:
                    if abs(dx - 0.5) + abs(dy - 0.5) <= 1.5:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < output_grid.shape[0] and 0 <= ny < output_grid.shape[1]:
                            output_grid[nx, ny] = color
        
        elif w == 3 and h == 3:  # 3x3 square
            for dx in [-1, 0, 1, 2, 3]:
                for dy in [-1, 0, 1, 2, 3]:
                    if max(abs(dx - 1), abs(dy - 1)) <= 1 or (dx in [0, 2] and dy == 1) or (dy in [0, 2] and dx == 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < output_grid.shape[0] and 0 <= ny < output_grid.shape[1]:
                            output_grid[nx, ny] = color
    
    return output_grid

def generate_input():
    grid = np.zeros((20, 20), dtype=int)
    
    for _ in range(random.randint(3, 6)):
        size = random.choice([1, 2, 3])
        color = random.choice(list(Color.NOT_BLACK))
        sprite = np.full((size, size), color)
        
        try:
            x, y = random_free_location_for_sprite(grid, sprite, padding=1)
            blit_sprite(grid, sprite, x, y)
        except:
            pass
    
    return grid