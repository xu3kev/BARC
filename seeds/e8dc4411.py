from common import *

import numpy as np
from typing import *

# concepts:
# repeated translation, indicator pixels, non-black background

# description:
# In the input you will see a non-black background with a black object and an indicator pixel touching it of a different color.
# To make the output, repeatedly translate the black object in the direction of the indicator pixel and make the color of these repeated translations match the indicator.

def main(input_grid):
    # Plan:
    # 1. Parse the input into the black object and the indicator pixel(s)
    # 2. Determine the direction of translation
    # 3. Put down recolored versions of the black object

    # 1. Parse the input
    # background is most common color
    background = max(Color.ALL_COLORS, key=lambda color: np.sum(input_grid == color))
    # REMEMBER: pass background to everything that needs it, because it isn't by default BLACK
    objects = find_connected_components(input_grid, connectivity=8, background=background, monochromatic=True)
    # indicators are single pixels
    indicator_objects = [ obj for obj in objects if crop(obj, background=background).shape == (1,1) ]
    # other objects are bigger than (1,1)
    template_objects = [ obj for obj in objects if crop(obj, background=background).shape != (1,1) ]

    # We draw on top of the output, so copy it
    output_grid = input_grid.copy()

    # Iterate over every template and indicator which are in contact
    for template_obj in template_objects:
        template_sprite = crop(template_obj, background=background)
        for indicator_obj in indicator_objects:
            if not contact(object1=template_obj, object2=indicator_obj, background=background, connectivity=8): continue

            # 2. Determine the direction of translation
            indicator_x, indicator_y = object_position(indicator_obj, background=background, anchor="center")
            template_x, template_y = object_position(template_obj, background=background, anchor="center")

            dx, dy = np.sign(indicator_x - template_x), np.sign(indicator_y - template_y)
            # Figure out the stride the translation, which is as far as we can go while still covering the indicator pixel
            possible_strides = [ stride for stride in range(1, max(output_grid.shape))
                                if collision(object1=indicator_obj, object2=template_obj, x2=stride*dx, y2=stride*dy, background=background) ]
            stride = max(possible_strides)

            # 3. Put down recolored versions of the black object as much as we can until we fall out of the canvas
            # Prepare a new version of the sprite
            new_color = object_colors(indicator_obj, background=background)[0]
            recolored_template_sprite = template_sprite.copy()
            recolored_template_sprite[recolored_template_sprite != background] = new_color

            # Put down the recolored sprite at every stride
            for i in range(1, 10):
                old_x, old_y = object_position(template_obj, background=background, anchor="upper left")
                new_x, new_y = old_x + i*dx*stride, old_y + i*dy*stride
                blit_sprite(output_grid, recolored_template_sprite, new_x, new_y, background=background)
    
    return output_grid

def generate_input():
    # Make a grid with a grey horizontal rectangle stretching all the way through the middle, and some scattered points around it
    # Then randomly rotate to get a variety of orientations

    background_color, indicator_color = np.random.choice(Color.ALL_COLORS, size=2, replace=False)
    template_color = Color.BLACK

    width, height = np.random.randint(10, 25), np.random.randint(10, 25)
    grid = np.full((width, height), background_color)

    template_sprite = random_sprite(range(3,6), range(3,6), color_palette=[template_color], background=background_color)

    # place the template sprite randomly in the grid
    x, y = random_free_location_for_sprite(grid, template_sprite, background=background_color)
    blit_sprite(grid, template_sprite, x, y, background=background_color)

    # figure out a direction/stride that works
    indicator_sprite = np.full((1,1), indicator_color)
    dx, dy = 1, 1 # randomly rotate at the end to get a variety of orientations
    possible_strides = [ stride for stride in range(1, max(grid.shape))
                        if contact(object1=grid, object2=indicator_sprite, x2=x+stride*dx, y2=y+stride*dy, background=background_color) ]
    stride = max(possible_strides)

    # Put down the indicator pixel
    blit_sprite(grid, indicator_sprite, x+stride*dx, y+stride*dy, background=background_color)
    
    # random rotation to get a variety of orientations
    grid = np.rot90(grid, np.random.randint(0, 4))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
