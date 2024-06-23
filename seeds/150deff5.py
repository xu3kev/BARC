from common import *

import numpy as np
from typing import *

# concepts:
# decomposition, color change

# description:
# In the input you will see grey-colored regions on a medium sized black canvas. These regions are comprised of 2x2 squares and 1x3/3x1 rectangles, but this might be hard to see because regions might be touching.
# To make the output, decompose the input into 2x2 squares and 1x3/3x1 rectangles, and color them as follows:
# 1. Color teal the 2x2 squares
# 2. Color red the 1x3/3x1 rectangles

def main(input_grid: np.ndarray) -> np.ndarray:

    # Decompose the grid into non-overlapping grey regions
    # We need a custom predicate because otherwise the regions are also allowed to include background pixels, and we want it all grey
    decomposition = detect_objects(input_grid, background=Color.BLACK, colors=[Color.GREY],
                                   allowed_dimensions=[(2, 2), (3, 1), (1, 3)], # 2x2 squares and 1x3/3x1 rectangles
                                   predicate=lambda sprite: np.all(sprite == Color.GREY))

    output_grid = np.full(input_grid.shape, Color.BLACK)

    for obj in decomposition:
        # Color change based on dimensions: 2x2 -> teal, 1x3/3x1 -> red
        w, h = crop(obj, background=Color.BLACK).shape
        if w == 2 and h == 2:
            obj[obj == Color.GREY] = Color.TEAL
        elif (w == 3 and h == 1) or (w == 1 and h == 3):
            obj[obj == Color.GREY] = Color.RED
        else:
            assert 0, "Invalid object found"
        
        # Copy the object back into the output grid
        blit(output_grid, obj, background=Color.BLACK)

    return output_grid



def generate_input():
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    n_objects = np.random.randint(4, 8)

    for _ in range(n_objects):
        # Make a gray rectangle sprite
        color = Color.GREY
        w, h = random.choice([(2, 2), (3, 1), (1, 3)])
        sprite = np.full((w, h), color)

        # place it randomly on the grid, assuming we can find a spot
        try:
            x, y = random_free_location_for_object(grid, sprite, background=Color.BLACK)
        except:
            continue

        blit(grid, sprite, x, y, background=Color.BLACK)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)