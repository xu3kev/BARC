from common import *

import numpy as np
from typing import *

# concepts:
# holes, objects, distracters, topology, puzzle piece

# description:
# In the input you will see multiple grey rectangular objects, each with a black hole inside of it. There are also monochromatic objects somewhere exactly the same shape as each hole, and random other distracter objects (distracters all the same color). 
# To make the output, check to see if each non-distracter object perfectly fits inside the black hole inside of a gray object, like it is a puzzle piece. If it does, place it inside the black hole. If it doesn't, leave it where it is.

def main(input_grid):
    # Plan:
    # 1. Parse the input into objects, sprites, and black holes inside the grey objects
    # 2. Identify color of distracter objects.
    # 3. Turn each object into a sprite
    # 4. Check if each sprite can be moved into a black hole, and if so, move it there
    
    # Parse, separating greys from other objects
    grey_input = input_grid.copy()
    grey_input[input_grid != Color.GREY] = Color.BLACK
    grey_objects = find_connected_components(grey_input, background=Color.BLACK, connectivity=4, monochromatic=True)

    # extracting a mask for the black region is tricky, because black is also the color of the background
    # get the black region inside the object by getting the interior mask, then just the black pixels
    interior_black_regions = [ object_interior(obj, background=Color.BLACK) & (obj == Color.BLACK)
                               for obj in grey_objects ]

    not_grey_input = input_grid.copy()
    not_grey_input[input_grid == Color.GREY] = Color.BLACK
    not_grey_objects = find_connected_components(not_grey_input, background=Color.BLACK, connectivity=4, monochromatic=True)

    # Get the sprites
    not_grey_sprites = [ crop(obj, background=Color.BLACK) for obj in not_grey_objects ]

    # Get the color of the distracter objects
    # This is the most common color of the non-grey objects
    color_of_each_object = [ np.unique(obj[obj!=Color.BLACK])[0] for obj in not_grey_objects ]
    distracter_color = max(set(color_of_each_object), key=color_of_each_object.count)
    
    # Check if each sprite perfectly fits in a black hole/black interior region
    # do this by checking if it has the same shape as a black interior region
    # if it does, place it there
    output_grid = np.copy(input_grid)
    for sprite, obj, color in zip(not_grey_sprites, not_grey_objects, color_of_each_object):
        # Try to find a perfect fit (if it is not the distracter color)
        if color == distracter_color:
            continue
        
        for interior_obj_mask in interior_black_regions:
            # check the sprite masks are the same, meaning that they have the same shape
            # to convert a sprite to a mask you check if it is not background (black)
            sprite_mask = sprite != Color.BLACK
            # to convert an object to a spright you crop it
            interior_sprite_mask = crop(interior_obj_mask, background=Color.BLACK)
            perfect_fit = np.array_equal(sprite_mask, interior_sprite_mask)

            if perfect_fit:
                # remove the object from its original location
                object_mask = obj != Color.BLACK
                output_grid[object_mask] = Color.BLACK

                # place the sprite in the black hole by blitting it
                interior_x, interior_y, interior_width, interior_height = bounding_box(interior_obj_mask)
                blit_sprite(output_grid, sprite, interior_x, interior_y, background=Color.BLACK)
                break

    return output_grid            
    
    


def generate_input():
    n, m = np.random.randint(10, 25, size=2)
    input_grid = np.full((n, m), Color.BLACK)

    distracter_color = np.random.choice(Color.NOT_BLACK)

    n_grey_objects = np.random.randint(1, 3)
    for k in range(n_grey_objects):
        grey_width, grey_height = np.random.randint(5, 8, size=2)
        grey_sprite = np.full((grey_width, grey_height), Color.GREY)

        # make a black hole in the grey object
        # the black hole should be a sprite whole primary color is black, and whose background color is grey
        # it should be smaller than the grey object
        hole_width, hole_height = np.random.randint(1, grey_width-2), np.random.randint(1, grey_height-2)
        hole_sprite = random_sprite(hole_width, hole_height, color_palette=[Color.BLACK], background=Color.GREY, symmetry="not_symmetric")
        hole_x, hole_y = random_free_location_for_sprite(grey_sprite, hole_sprite, border_size=1, background=Color.GREY)
        blit_sprite(grey_sprite, hole_sprite, hole_x, hole_y, background=Color.GREY)

        # place the grey object in the input grid
        x, y = random_free_location_for_sprite(input_grid, grey_sprite, padding=1, border_size=1)
        blit_sprite(input_grid, grey_sprite, x, y, background=Color.BLACK)

        # each hole has a corresponding colored object somewhere on the grid waiting for it with the same shape as the whole
        # this is going to have the perfect fit, so it needs to have the same mask as the hole but a different color (but not the special colors of gray or the distracter)
        color = np.random.choice([c for c in Color.NOT_BLACK if c != Color.GREY and c != distracter_color])
        object_sprite = np.full((hole_width, hole_height), Color.BLACK)
        object_sprite[hole_sprite == Color.BLACK] = color

        # place the object sprite in the input grid
        x, y = random_free_location_for_sprite(input_grid, object_sprite, padding=1, border_size=1)
        blit_sprite(input_grid, object_sprite, x, y, background=Color.BLACK)

    # place small distracter objects
    n_distracter_objects = np.random.randint(5, 10)
    for k in range(n_distracter_objects):
        distracter_width, distracter_height = np.random.randint(1, 3, size=2)
        distracter_sprite = random_sprite(distracter_width, distracter_height, color_palette=[distracter_color], background=Color.BLACK)
        x, y = random_free_location_for_sprite(input_grid, distracter_sprite, padding=1)
        blit_sprite(input_grid, distracter_sprite, x, y, background=Color.BLACK)

    return input_grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
