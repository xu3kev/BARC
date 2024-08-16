from common import *

import numpy as np
from typing import *

# concepts:
# objects, holes, topology, puzzle piece, rotation

# description:
# In the input, you will see multiple colored rectangular objects, each with a black hole inside of it. There are also grey objects somewhere on the grid that are exactly the same shape as each hole, but they might be rotated.
# To make the output, check to see if each grey object perfectly fits inside the black hole of a colored object when rotated 0, 90, 180, or 270 degrees. If it does, place it inside the black hole in the correct orientation. If it doesn't fit anywhere, leave it where it is.

def main(input_grid):
    # Plan:
    # 1. Parse the input into colored objects with holes, and grey objects
    # 2. Turn each object into a sprite
    # 3. For each grey sprite, check if it can be rotated and placed into a black hole
    # 4. If it can, remove it from its original position and place it in the hole
    
    # Parse, separating colored objects from grey objects
    colored_input = input_grid.copy()
    colored_input[input_grid == Color.GREY] = Color.BLACK
    colored_objects = find_connected_components(colored_input, background=Color.BLACK, connectivity=4, monochromatic=False)

    grey_input = input_grid.copy()
    grey_input[input_grid != Color.GREY] = Color.BLACK
    grey_objects = find_connected_components(grey_input, background=Color.BLACK, connectivity=4, monochromatic=True)

    # Extract black holes from colored objects
    holes = []
    for obj in colored_objects:
        interior = object_interior(obj, background=Color.BLACK)
        hole = interior & (obj == Color.BLACK)
        holes.append(hole)

    # Get the sprites
    grey_sprites = [crop(obj, background=Color.BLACK) for obj in grey_objects]
    hole_sprites = [crop(hole, background=Color.BLACK) for hole in holes]

    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Check if each grey sprite can be rotated and placed into a black hole
    for grey_sprite, grey_obj in zip(grey_sprites, grey_objects):
        placed = False
        for hole_sprite, colored_obj in zip(hole_sprites, colored_objects):
            for k in range(4):  # Try all 4 rotations
                rotated_grey = np.rot90(grey_sprite, k)
                if np.array_equal(rotated_grey.shape, hole_sprite.shape) and np.all(rotated_grey[hole_sprite] == Color.GREY):
                    # Remove grey object from its original position
                    output_grid[grey_obj == Color.GREY] = Color.BLACK
                    
                    # Place rotated grey sprite in the hole
                    hole_x, hole_y, _, _ = bounding_box(colored_obj & (input_grid == Color.BLACK))
                    blit_sprite(output_grid, rotated_grey, hole_x, hole_y, background=Color.BLACK)
                    
                    placed = True
                    break
            if placed:
                break

    return output_grid

def generate_input():
    n, m = np.random.randint(15, 30, size=2)
    input_grid = np.full((n, m), Color.BLACK)

    n_colored_objects = np.random.randint(2, 4)
    for _ in range(n_colored_objects):
        width, height = np.random.randint(5, 8, size=2)
        color = np.random.choice([c for c in Color.NOT_BLACK if c != Color.GREY])
        colored_sprite = np.full((width, height), color)

        # Make a black hole in the colored object
        hole_width, hole_height = np.random.randint(2, width-1), np.random.randint(2, height-1)
        hole_sprite = random_sprite(hole_width, hole_height, color_palette=[Color.BLACK], background=color, symmetry="not_symmetric")
        hole_x, hole_y = random_free_location_for_sprite(colored_sprite, hole_sprite, border_size=1, background=color)
        blit_sprite(colored_sprite, hole_sprite, hole_x, hole_y, background=color)

        # Place the colored object in the input grid
        x, y = random_free_location_for_sprite(input_grid, colored_sprite, padding=1, border_size=1)
        blit_sprite(input_grid, colored_sprite, x, y, background=Color.BLACK)

        # Create a corresponding grey object with the same shape as the hole
        grey_sprite = np.full((hole_width, hole_height), Color.BLACK)
        grey_sprite[hole_sprite == Color.BLACK] = Color.GREY

        # Randomly rotate the grey sprite
        grey_sprite = np.rot90(grey_sprite, np.random.randint(4))

        # Place the grey object in the input grid
        x, y = random_free_location_for_sprite(input_grid, grey_sprite, padding=1, border_size=1)
        blit_sprite(input_grid, grey_sprite, x, y, background=Color.BLACK)

    return input_grid