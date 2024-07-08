from common import *

import numpy as np
from typing import *

# concepts:
# objects, alignment, sliding objects, color guide

# description:
# In the input grid, you will see a black grid with several 2x2 colored squares randomly placed in it. Each 2x2 square contains a single color.
# To make the output, create a 6x6 grid. Align each 2x2 square from the input in a pattern
# where the squares are positioned diagonally in the output grid.

def main(input_grid):
    # Plan:
    # 1. Extract the 2x2 colored squares from the input grid
    # 2. Create the output grid
    # 3. Arrange the 2x2 squares diagonally in the output grid
    
    # step 1: extract the 2x2 colored squares from the input grid
    square_size = (2, 2)
    square_objects = detect_objects(input_grid, background=Color.BLACK, 
                                    allowed_dimensions=[square_size],
                                    predicate=lambda sprite: np.any(sprite != Color.BLACK) and np.all(sprite != Color.BLACK))
    square_sprites = [crop(obj, background=Color.BLACK) for obj in square_objects]

    # step 2: create the output grid, which is all black
    output_grid = np.full((6, 6), Color.BLACK, dtype=int)

    # step 3: arrange the 2x2 squares diagonally in the output grid
    for i, square in enumerate(square_sprites):
        x, y = i * 2, i * 2  # positioning squares diagonally
        blit_sprite(output_grid, square, x, y)

    return output_grid

def generate_input():
    # create a black grid with size ranging from 10x10 to 15x15
    n = np.random.randint(10, 16)
    m = np.random.randint(10, 16)
    input_grid = np.full((n, m), Color.BLACK, dtype=int)

    n_objects = 3  # ensure we can place 3 squares diagonally in the 6x6 output grid

    for _ in range(n_objects):
        # make a colored 2x2 square
        color = np.random.choice(list(Color.NOT_BLACK))
        square = np.full((2, 2), color, dtype=int)

        # place it randomly on the grid, assuming we can find a spot
        try:
            x, y = random_free_location_for_sprite(input_grid, square, background=Color.BLACK)
        except:
            continue

        blit_sprite(input_grid, square, x, y, background=Color.BLACK)

    return input_grid