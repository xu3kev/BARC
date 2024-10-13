from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, reflection

# description:
# In the input you will see a small monochromatic pattern with reflectional symmetry (horizontal and vertical), as well as another monochromatic object in one of its quadrants.
# To make the output, reflect the other object across the axes of reflectional symmetry of the small pattern.

def main(input_grid):
    # Plan:
    # 1. Detect the pair of objects and divide them by whether or not they are already symmetric
    # 2. Reflect the non-symmetric object across the axes of symmetry of the symmetric object

    # 1. Object detection and setup
    objects = find_connected_components(input_grid, connectivity=8, background=Color.BLACK)
    assert len(objects) == 2

    # Find the object that is symmetric
    symmetric_object = None
    for obj in objects:
        # Detect all symmetry
        # There is no occlusion so and don't ignore any colors
        # But we know the background is black
        symmetries = detect_mirror_symmetry(obj, ignore_colors=[], background=Color.BLACK)

        # actually finds three symmetries: horizontal, vertical, and diagonal mirroring
        if len(symmetries) >= 2:
            symmetric_object = obj
            break
    assert symmetric_object is not None, "There should be a symmetric object"

    # Find the object that is not symmetric
    non_symmetric_object = next(obj for obj in objects if obj is not symmetric_object)

    # 2. Reflect the non-symmetric object across the axes of symmetry of the symmetric object
    output_grid = input_grid.copy()

    for x, y in np.argwhere(non_symmetric_object != Color.BLACK):
        original_color = non_symmetric_object[x, y]
        for transformed_x, transformed_y in orbit(output_grid, x, y, symmetries=symmetries):
            output_grid[transformed_x, transformed_y] = original_color
    
    return output_grid
        



def generate_input():
    
    grid = np.full((random.choice(range(15, 30+1)), random.choice(range(15, 30+1))), Color.BLACK)

    # We are going to generate a grid with a symmetric pattern and a non-symmetric object in one of its quadrants
    
    # Generate the symmetric pattern
    symmetric_sprite = random_sprite(range(3, 6), range(3, 6),
                                     color_palette=[random.choice(Color.NOT_BLACK)], connectivity=8, 
                                     symmetry="mirror")    

    # Generate the non-symmetric object
    non_symmetric_sprite = random_sprite(range(7,10), range(7,10),
                                         color_palette=[random.choice(Color.NOT_BLACK)], connectivity=8, 
                                         symmetry="not_symmetric")
    
    # Randomly place the small symmetric object with enough padding so that the non symmetric one can go in one of its quadrants
    x_symmetric, y_symmetric = random_free_location_for_sprite(grid, symmetric_sprite, border_size=max(non_symmetric_sprite.shape))
    blit_sprite(grid, symmetric_sprite, x_symmetric, y_symmetric)

    # Put the other sprite in the lower right quadrant, and then randomly rotate at the end to get a variety of possible placements
    x_non_symmetric = x_symmetric + symmetric_sprite.shape[0] + 1
    y_non_symmetric = y_symmetric + symmetric_sprite.shape[1] + 1
    blit_sprite(grid, non_symmetric_sprite, x_non_symmetric, y_non_symmetric)

    # random rotation
    grid = np.rot90(grid, np.random.randint(0, 4))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
