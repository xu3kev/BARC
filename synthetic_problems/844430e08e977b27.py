from common import *

import numpy as np
import random
from typing import *


def main(input_grid: np.ndarray) -> np.ndarray:
    # Decompose the grid into non-overlapping color regions
    decomposition = detect_objects(input_grid, background=Color.BLACK, colors=Color.NOT_BLACK,
                                   allowed_dimensions=[(2, 2), (3, 1), (1, 3), (1, 1)])

    output_grid = np.full(input_grid.shape, Color.BLACK)

    # Helper function to surround an object with a specific color
    def surround_object(grid, x, y, w, h, border_color):
        for i in range(x-1, x+w+1):
            for j in range(y-1, y+h+1):
                if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
                    if not (x <= i < x+w and y <= j < y+h):
                        grid[i, j] = border_color

    color_cycle = [Color.TEAL, Color.RED, Color.BLUE]
    for obj in decomposition:
        x, y, w, h = bounding_box(obj, background=Color.BLACK)
        sprite = crop(obj, background=Color.BLACK)

        # Determine the new color based on the dimension
        if w == 2 and h == 2:
            new_color = Color.TEAL
        elif (w == 3 and h == 1) or (w == 1 and h == 3):
            new_color = Color.RED
        elif w == 1 and h == 1:
            new_color = Color.BLUE
        else:
            assert 0, "Invalid object found"
        
        # Color change for the sprite
        sprite[sprite != Color.BLACK] = new_color

        # Determine the border color
        new_color_idx = color_cycle.index(new_color)
        border_color = color_cycle[(new_color_idx + 1) % len(color_cycle)]

        # Copy the sprite back into the output grid
        blit_sprite(output_grid, sprite, x, y, background=Color.BLACK)

        # Surround the object with the border color
        surround_object(output_grid, x, y, w, h, border_color)

    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    n_objects = np.random.randint(5, 10)

    for _ in range(n_objects):
        # Randomly choose a color and dimensions
        color = random.choice(Color.NOT_BLACK)
        dimensions = random.choice([(2, 2), (3, 1), (1, 3), (1, 1)])
        w, h = dimensions
        sprite = np.full((w, h), color)

        # place it randomly on the grid, assuming we can find a spot
        try:
            x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK)
        except:
            continue

        blit_sprite(grid, sprite, x, y, background=Color.BLACK)

    return grid