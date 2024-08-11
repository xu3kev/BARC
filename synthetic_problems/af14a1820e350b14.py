from common import *

import numpy as np
from typing import *

# concepts:
# decomposition, borders, color change

# description:
# In the input you will see a grid with non-overlapping colored regions composed of 2x2 squares and 1x3/3x1 rectangles.
# To make the output, detect these regions and then:
# 1. Change the color of 2x2 squares to teal and the 1x3/3x1 rectangles to red.
# 2. Add a one-pixel-wide border around each shape. The border should be yellow.

def main(input_grid: np.ndarray) -> np.ndarray:

    # Detect objects (regions) using a custom predicate, considering shapes only without overlap.
    regions = detect_objects(input_grid, background=Color.BLACK,
                             allowed_dimensions=[(2, 2), (3, 1), (1, 3)], predicate=lambda obj: not np.any(obj == Color.BLACK))

    output_grid = np.full(input_grid.shape, Color.BLACK)
    
    for region in regions:
        x, y, w, h = bounding_box(region, background=Color.BLACK)
        sprite = crop(region, background=Color.BLACK)

        # Change color based on shape
        if w == 2 and h == 2:
            inner_color = Color.TEAL
        elif (w == 3 and h == 1) or (w == 1 and h == 3):
            inner_color = Color.RED
        else:
            continue  # Ignore invalid shapes

        sprite[sprite != Color.BLACK] = inner_color
        
        # Compute the extended sprite with a border
        bordered_sprite = np.full((w + 2, h + 2), Color.BLACK)
        bordered_sprite[1:-1, 1:-1] = sprite
        bordered_sprite[0, :] = bordered_sprite[-1, :] = bordered_sprite[:, 0] = bordered_sprite[:, -1] = Color.YELLOW
        
        blit_sprite(output_grid, bordered_sprite, x-1, y-1, background=Color.BLACK)

    return output_grid

def generate_input():
    # Define the grid size
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    n_objects = np.random.randint(4, 8)
    shapes = [(2, 2), (3, 1), (1, 3)]
    
    for _ in range(n_objects):
        # Create a randomly colored rectangle
        color = random.choice(Color.NOT_BLACK)
        w, h = random.choice(shapes)
        sprite = np.full((w, h), color)
        
        # Place the rectangle randomly on the grid
        try:
            x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK)
        except:
            continue

        blit_sprite(grid, sprite, x, y, background=Color.BLACK)

    return grid