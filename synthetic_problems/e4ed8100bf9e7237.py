from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, reflection, lines, color change, objects

# description:
# In the input, you will see objects of various shapes and colors scattered around on a black grid. Each object has a specific type of symmetry (horizontal, vertical, or diagonal).
# To make the output, reflect each object based on its symmetry type and then draw connecting lines between the new positions of the objects.

def main(input_grid):

    # extract the objects
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)

    # prepare a blank output grid
    output_grid = np.zeros_like(input_grid)

    reflected_objects = []

    for obj in objects:
        # identify the symmetry type (this is encoded in the top-left 2x2 grid of the object)
        obj_cropped = crop(obj)
        x, y, w, h = bounding_box(obj_cropped)

        top_left_2x2 = obj_cropped[:2, :2]

        if top_left_2x2[0, 0] == top_left_2x2[1, 0]:  # vertical symmetry
            symmetry_type = 'vertical'
        elif top_left_2x2[0, 0] == top_left_2x2[0, 1]:  # horizontal symmetry
            symmetry_type = 'horizontal'
        else:  # diagonal
            symmetry_type = 'diagonal'

        if symmetry_type == 'vertical':
            reflected_object = np.fliplr(obj_cropped)
        elif symmetry_type == 'horizontal':
            reflected_object = np.flipud(obj_cropped)
        else:  # diagonal reflection
            reflected_object = np.rot90(obj_cropped, 2)

        # save the reflected object for later
        reflected_objects.append(reflected_object)

        # place the reflected object into output grid at the same location as the original
        blit_object(output_grid, reflected_object, background=Color.BLACK)

    # Draw lines between the reflected objects (centers) in yellow
    for i in range(len(reflected_objects) - 1):
        ref_obj1 = reflected_objects[i]
        ref_obj2 = reflected_objects[i + 1]

        # find the centers of the reflected objects
        x1, y1, w1, h1 = bounding_box(ref_obj1)
        x2, y2, w2, h2 = bounding_box(ref_obj2)
        
        center_x1, center_y1 = x1 + w1 // 2, y1 + h1 // 2
        center_x2, center_y2 = x2 + w2 // 2, y2 + h2 // 2

        # draw the lines using the centers
        draw_line(output_grid, center_x1, center_y1, length=None, color=Color.YELLOW, direction=(np.sign(center_x2 - center_x1), 0), stop_at_color=[Color.BLACK])
        draw_line(output_grid, center_x2, y1, length=None, color=Color.YELLOW, direction=(0, np.sign(center_y2 - center_y1)), stop_at_color=[Color.BLACK])

    return output_grid


def generate_input():
    # make a black grid for the background
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    num_objects = np.random.randint(3, 6)

    for _ in range(num_objects):
        # create a random sprite with symmetry
        symmetry_type = np.random.choice(['horizontal', 'vertical', 'diagonal'])
        sprite_color = np.random.choice(list(Color.NOT_BLACK))
        sprite = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), color_palette=[sprite_color])

        # encode the symmetry in the top-left 2x2 grid of the sprite
        if symmetry_type == 'vertical':
            sprite[0, 0] = sprite[0, 1]
            sprite[1, 0] = sprite[1, 1]
        elif symmetry_type == 'horizontal':
            sprite[0, 0] = sprite[1, 0]
            sprite[0, 1] = sprite[1, 1]
        else:  # diagonal
            sprite[0, 0] = sprite[1, 1]
            sprite[0, 1] = sprite[1, 0]

        # place the sprite on the grid
        x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK, padding=1)
        blit_sprite(grid, sprite, x, y)

    return grid