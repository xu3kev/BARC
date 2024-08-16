from common import *

import numpy as np
from typing import *

# concepts:
# decomposition, symmetry detection, growing

# description:
# In the input you will see a grid with small, randomly placed 'L'-shaped patterns composed of different colors.
# The goal is to identify symmetrical pairs of opposing 'L' shapes that together form a square, then expand them to form a larger symmetrical pattern of concentric squares.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = input_grid.copy()

    # Detect all L-shaped patterns in the grid
    objects = detect_objects(input_grid, background=Color.BLACK, monochromatic=True, allowed_dimensions=[(2,2)])

    # Decompose detected objects into symmetrical pairs
    for obj in objects:
        x, y, w, h = bounding_box(obj)
        sprite = crop(obj)
        
        # Detect L-shape by its unique pixel placements if not occluded completely
        if (sprite[0, 0] != Color.BLACK and sprite[1, 0] != Color.BLACK and sprite[1, 1] != Color.BLACK) or \
           (sprite[0, 0] != Color.BLACK and sprite[0, 1] != Color.BLACK and sprite[1, 1] != Color.BLACK):
            color = sprite[sprite != Color.BLACK][0]
            
            # Determine symmetry and grow into larger pattern
            check_x, check_y = x - 1, y - 1
            if check_x >= 0 and check_y >= 0 and input_grid[check_x: check_x + 3, check_y: check_y + 3].all() == Color.BLACK:
                draw_line(output_grid, check_x, check_y, length=3, color=color, direction=(1,0), stop_at_color=[])
                draw_line(output_grid, check_x, check_y, length=3, color=color, direction=(0,1), stop_at_color=[])
                draw_line(output_grid, check_x + 2, check_y, length=3, color=color, direction=(0,1), stop_at_color=[])
                draw_line(output_grid, check_x, check_y+2, length=3, color=color, direction=(1,0), stop_at_color=[])
                
    return output_grid

def generate_input():
    # Create a grid within a set size range
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # Randomly place 'L'-shaped sprites on the grid
    num_sprites = np.random.randint(4, 8)
    for _ in range(num_sprites):
        color = np.random.choice(Color.NOT_BLACK)
        sprite = np.array([
            [color, Color.BLACK],
            [color, color]
        ] if np.random.random() < 0.5 else [
            [color, color],
            [Color.BLACK, color]
        ])

        x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK)
        blit_sprite(grid, sprite, x, y)

    return grid