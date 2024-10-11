from common import *

import numpy as np
from typing import *

# concepts:
# same/different, color change, containment

# description:
# In the input you will see some monochromatic objects. Some of them will be contained by a grey box, and some of them will not.
# To make the output, take each shape contained inside a grey box, and find any other shapes with the same shape (but a different color), and change their color to match the color of the shape inside the grey box.

def main(input_grid):
    # Plan:
    # 1. Extract the objects and separate them according to if they are grey or not
    # 2. Determine if each non-grey shape is contained by a grey shape
    # 3. Check to see which objects (among grey contained shapes) have another object which has the same shape (not contained by grey)
    # 4. Do the color change when you find these matching objects

    # 1. Extract the objects, separating them by if they are grey or not
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=True)
    grey_objects = [ obj for obj in objects if Color.GREY in object_colors(obj, background=Color.BLACK) ]
    non_grey_objects = [ obj for obj in objects if Color.GREY not in object_colors(obj, background=Color.BLACK) ]

    # 2. Determine if each non-grey shape is contained by a grey shape
    # Divide the non-grey objects into two groups: those contained by grey, and those not contained by grey
    # Make a helper function for checking of one object is contained by another
    def object_contains_another_object(inside_object, outside_object):
        # Using bounding boxes:
        # inside_x, inside_y, inside_width, inside_height = bounding_box(inside_object)
        # outside_x, outside_y, outside_width, outside_height = bounding_box(outside_object)
        # return inside_x >= outside_x and inside_y >= outside_y and inside_x + inside_width <= outside_x + outside_width and inside_y + inside_height <= outside_y + outside_height
        # Using topology+masks:
        inside_object_mask = inside_object != Color.BLACK
        outside_interior_mask = object_interior(outside_object, background=Color.BLACK)
        return np.all(outside_interior_mask >= inside_object_mask)
    objects_contained_by_grey = [ non_grey for non_grey in non_grey_objects
                                  if any( object_contains_another_object(non_grey, grey) for grey in grey_objects ) ]
    objects_not_contained_by_gray = [ non_grey for non_grey in non_grey_objects
                                     if not any( object_contains_another_object(non_grey, grey) for grey in grey_objects ) ]
    
    # 3. Check to see which objects (among grey contained shapes) have another object which has the same shape (not contained by grey)
    output_grid = input_grid.copy()

    # Helper function to check if two objects have the same shape
    def objects_have_same_shape(obj1, obj2):
        mask1 = crop(obj1, background=Color.BLACK) != Color.BLACK
        mask2 = crop(obj2, background=Color.BLACK) != Color.BLACK
        return np.array_equal(mask1, mask2)
    
    for grey_contained in objects_contained_by_grey:
        for non_grey in objects_not_contained_by_gray:
            if objects_have_same_shape(grey_contained, non_grey):
                # 4. Do the color change
                target_color = object_colors(grey_contained, background=Color.BLACK)[0]
                non_grey_mask = non_grey != Color.BLACK
                output_grid[non_grey_mask] = target_color

    return output_grid

def generate_input():
    # Make some sprites
    # One of those sprites is going to be contained by a grey box, and occur more than once (but in different colors)
    # The other sprites are not going to be contained by the grey box, and might occur multiple times anyway

    width, height = random.choice(range(17, 30+1)), random.choice(range(17, 30+1))
    grid = np.full((width, height), Color.BLACK)

    possible_sprite_dimensions = [1,2,3,4]
    contained_color = random.choice([ color for color in Color.NOT_BLACK if color != Color.GREY ])
    contained_sprite = random_sprite(possible_sprite_dimensions, possible_sprite_dimensions,
                                     color_palette=[contained_color])

    # put down the contained sprite at a random spot, and then put a gray box around it
    x, y = random_free_location_for_sprite(grid, contained_sprite, background=Color.BLACK, border_size=2, padding=2)
    blit_sprite(grid, contained_sprite, x, y)
    contained_w, contained_h = contained_sprite.shape

    # make the gray box (outline of a rectangle)
    grey_box = np.full((contained_w+4, contained_h+4), Color.GREY)
    grey_box[1:-1, 1:-1] = Color.BLACK
    blit_sprite(grid, grey_box, x-2, y-2)

    # put down some other sprites which are the same shape as the contained sprite, but in different colors
    n_duplicate_sprites = np.random.randint(1, 3)
    for _ in range(n_duplicate_sprites):
        duplicate_sprite = contained_sprite.copy()
        duplicate_sprite[duplicate_sprite != Color.BLACK] = random.choice([ color for color in Color.NOT_BLACK if color != Color.GREY and color != contained_color ])
        x, y = random_free_location_for_sprite(grid, duplicate_sprite, background=Color.BLACK, border_size=1, padding=1)
        blit_sprite(grid, duplicate_sprite, x, y)
    
    # put down some other sprites which are not the same shape as the contained sprite, which might be duplicated occasionally
    n_non_contained_sprites = np.random.randint(1, 3)
    for _ in range(n_non_contained_sprites):
        sprite_color = random.choice([ color for color in Color.NOT_BLACK if color != Color.GREY ])
        sprite = random_sprite(possible_sprite_dimensions, possible_sprite_dimensions,
                               color_palette=[sprite_color])
        x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK, border_size=1, padding=1)
        blit_sprite(grid, sprite, x, y)

        # Maybe duplicate?
        if np.random.rand() < 0.5:
            x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK, border_size=1, padding=1)
            blit_sprite(grid, sprite, x, y)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
