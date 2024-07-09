from common import *

import numpy as np
from typing import *

# concepts:
# decomposition, symmetry detection, color change

# description:
# In the input, you will see grey-colored regions on a medium-sized black canvas. These regions are comprised of 3x3 squares and 2x4/4x2 rectangles, but this might be hard to see because regions might be touching.
# To make the output:
# 1. Decompose the input into 3x3 squares and 2x4/4x2 rectangles
# 2. For 3x3 squares:
#    - If the square has rotational symmetry, color it teal
#    - If it has only vertical or horizontal symmetry, color it red
#    - If it has no symmetry, color it blue
# 3. For 2x4/4x2 rectangles:
#    - If the rectangle has vertical or horizontal symmetry, color it orange
#    - If it has no symmetry, color it pink

def main(input_grid: np.ndarray) -> np.ndarray:
    # Decompose the grid into non-overlapping grey regions
    decomposition = detect_objects(input_grid, background=Color.BLACK, colors=[Color.GREY],
                                   allowed_dimensions=[(3, 3), (2, 4), (4, 2)],
                                   predicate=lambda sprite: np.all(sprite == Color.GREY))

    output_grid = np.full(input_grid.shape, Color.BLACK)

    for obj in decomposition:
        x, y, w, h = bounding_box(obj, background=Color.BLACK)
        sprite = crop(obj, background=Color.BLACK)

        if w == 3 and h == 3:
            # Check for symmetry in 3x3 squares
            rot_sym = detect_rotational_symmetry(sprite, ignore_colors=[Color.BLACK])
            if rot_sym:
                new_color = Color.TEAL
            else:
                # Check for vertical and horizontal symmetry
                vert_sym = np.all(sprite[:, 0] == sprite[:, 2])
                horz_sym = np.all(sprite[0, :] == sprite[2, :])
                if vert_sym or horz_sym:
                    new_color = Color.RED
                else:
                    new_color = Color.BLUE
        elif (w == 2 and h == 4) or (w == 4 and h == 2):
            # Check for symmetry in 2x4/4x2 rectangles
            if w == 2:
                sym = np.all(sprite[:, 0:2] == sprite[:, 2:4])
            else:
                sym = np.all(sprite[0:2, :] == sprite[2:4, :])
            new_color = Color.ORANGE if sym else Color.PINK
        else:
            assert 0, "Invalid object found"

        sprite[sprite == Color.GREY] = new_color
        blit_sprite(output_grid, sprite, x, y, background=Color.BLACK)

    return output_grid

def generate_input():
    n, m = np.random.randint(15, 20), np.random.randint(15, 20)
    grid = np.zeros((n, m), dtype=int)

    n_objects = np.random.randint(5, 9)

    for _ in range(n_objects):
        # Make a gray rectangle sprite
        color = Color.GREY
        w, h = random.choice([(3, 3), (2, 4), (4, 2)])
        sprite = np.full((w, h), color)

        # For 3x3 squares, randomly add symmetry
        if w == 3 and h == 3:
            symmetry = random.choice(['none', 'vertical', 'horizontal', 'rotational'])
            if symmetry == 'vertical':
                sprite[:, 1] = random.choice(list(Color.NOT_BLACK))
            elif symmetry == 'horizontal':
                sprite[1, :] = random.choice(list(Color.NOT_BLACK))
            elif symmetry == 'rotational':
                sprite[1, 1] = random.choice(list(Color.NOT_BLACK))
                sprite[0, 0] = sprite[2, 2] = random.choice(list(Color.NOT_BLACK))
                sprite[0, 2] = sprite[2, 0] = random.choice(list(Color.NOT_BLACK))
        
        # For 2x4/4x2 rectangles, randomly add symmetry
        elif w == 2 or h == 2:
            symmetry = random.choice(['none', 'symmetrical'])
            if symmetry == 'symmetrical':
                if w == 2:
                    sprite[:, 0:2] = np.random.choice(list(Color.NOT_BLACK), size=(2, 2))
                    sprite[:, 2:4] = sprite[:, 0:2]
                else:
                    sprite[0:2, :] = np.random.choice(list(Color.NOT_BLACK), size=(2, 4))
                    sprite[2:4, :] = sprite[0:2, :]

        # Reset all non-black pixels to grey
        sprite[sprite != Color.BLACK] = Color.GREY

        # Place it randomly on the grid, assuming we can find a spot
        try:
            x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK)
        except:
            continue

        blit_sprite(grid, sprite, x, y, background=Color.BLACK)

    return grid