from common import *

import numpy as np
from typing import *

# concepts:
# mirror symmetry, non-black background, indicator pixels

# description:
# In the input you will see an object with some red pixels attached to it on one side.
# To make the output, mirror the object to cover the red pixels. Then change the background to green.
 
def main(input_grid):
    # Plan:
    # 1. Find the main object and the red pixels
    # 2. Calculate the axis over which to mirror depending on which side the red pixels are on
    # 3. Do the mirroring
    # 4. Change background to green
    
    # 1. Input parsing
    background = Color.BLACK
    objects = find_connected_components(input_grid, connectivity=8, background=background, monochromatic=True)
    assert len(objects) == 2, "There should be exactly two objects"

    # Find the main object
    main_object = next(obj for obj in objects if Color.RED not in object_colors(obj, background=background))
    # Find the red pixels
    red_pixels = next(obj for obj in objects if Color.RED in object_colors(obj, background=background))

    # 2. Axis calculation

    # Figure out what side of the object the red pixels are on
    x1, y1 = object_position(main_object, anchor="upper left")
    x2, y2 = object_position(main_object, anchor="lower right")
    # on the right?
    if collision(object1=translate(main_object, x=1, y=0), object2=red_pixels):
        # the +/- 0.5 is to clobber the red pixels, otherwise we'd reflect over them and leave them be, which would also be a reasonable thing to do
        symmetry = MirrorSymmetry(mirror_x=x2+0.5, mirror_y=None)
    # on the left?
    elif collision(object1=translate(main_object, x=-1, y=0), object2=red_pixels):
        symmetry = MirrorSymmetry(mirror_x=x1-0.5, mirror_y=None)
    # on the top?
    elif collision(object1=translate(main_object, x=0, y=-1), object2=red_pixels):
        symmetry = MirrorSymmetry(mirror_x=None, mirror_y=y1-0.5)
    # on the bottom?
    elif collision(object1=translate(main_object, x=0, y=1), object2=red_pixels):
        symmetry = MirrorSymmetry(mirror_x=None, mirror_y=y2+0.5)
    else:
        assert False, "Red pixels are not on any side of the main object"
    
    # 3. Mirror the main object
    output_grid = np.full_like(input_grid, background)
    blit_object(output_grid, main_object)
    for x, y in np.argwhere(main_object != background):
        for x2, y2 in orbit(output_grid, x, y, symmetries=[symmetry]):
            if 0 <= x2 < output_grid.shape[0] and 0 <= y2 < output_grid.shape[1]:
                output_grid[x2, y2] = main_object[x, y]
    
    # 4. Change the background to green
    output_grid[output_grid == background] = Color.GREEN

    return output_grid

def generate_input():
    # Make an empty black grid of random size, and then put a non-red object somewhere. Put some red pixels on one side.
    background = Color.BLACK
    grid = np.full((random.randint(10, 25), random.randint(10, 25)), background)

    object_color = random.choice([ color for color in Color.NOT_BLACK if color != Color.RED ])
    sprite = random_sprite(random.randint(3, 6), random.randint(3, 6), color_palette=[object_color])

    # Put red on the right side. We will randomly rotate at the end to get a variety of orientations.
    # But make sure that there are some pixels on the right side.
    assert np.any(sprite[-1, :] == object_color), "The object must have some pixels on the right side"
    for x, y in np.argwhere(sprite == object_color):
        if x == sprite.shape[0]-1:
            sprite[x, y] = Color.RED

    # placed randomly but a little bit far away from the border
    x, y = random_free_location_for_sprite(grid, sprite, border_size=6)
    blit_sprite(grid, sprite, x, y)

    # randomly rotate
    grid = np.rot90(grid, random.randint(0, 4))

    return grid

    

    

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)