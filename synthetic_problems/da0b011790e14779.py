from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, reflection, rotation, objects

# description:
# In the input, you will see a sprite repeated in a 2x2 grid pattern. Each repetition might be rotated by 0, 90, 180, or 270 degrees.
# To make the output, extract the original sprite and reflect it vertically (top to bottom).

def main(input_grid):
    # Find the size of the sprite (half of the input grid size)
    sprite_size = input_grid.shape[0] // 2

    # Extract the four quadrants
    quadrants = [
        input_grid[:sprite_size, :sprite_size],
        input_grid[:sprite_size, sprite_size:],
        input_grid[sprite_size:, :sprite_size],
        input_grid[sprite_size:, sprite_size:]
    ]

    # Find the original sprite (the one that wasn't rotated)
    original_sprite = None
    for q in quadrants:
        if all(np.array_equal(q, np.rot90(other, k)) for other, k in zip(quadrants, range(4))):
            original_sprite = q
            break

    assert original_sprite is not None, "No valid original sprite found"

    # Reflect the original sprite vertically
    return np.flipud(original_sprite)

def generate_input():
    # Create the sprite to be duplicated; pick a trio of random colors
    n = random.randint(3, 8)
    sprite = random_sprite(n, n, color_palette=random.sample(list(Color.NOT_BLACK), 3))
    
    # Create a 2x2 grid of the sprite with random rotations
    grid = np.zeros((2*n, 2*n), dtype=int)
    for i in range(2):
        for j in range(2):
            rotated_sprite = np.rot90(sprite, k=random.randint(0, 3))
            blit_sprite(grid, rotated_sprite, x=i*n, y=j*n)

    return grid