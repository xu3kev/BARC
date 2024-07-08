from common import *

import numpy as np
from typing import *

# concepts:
# triangle, infinite ray, color guide

# description:
# In the input you will see a pyramid with a flat base (possibly rotated), with a single special pixel inside of it that is a different color. The special pixel is centered in the base of the pyramid, opposite the tip of the pyramid.
# To make the output, draw a line starting from the tip of the pyramid and extending outward infinitely (away from the pyramid). The color of the line is the color of the special pixel.

def main(input_grid):
    # Plan:
    # 1. Find the special pixel and the pyramid
    # 2. Find the tip of the pyramid, and which way it is pointing
    # 3. Draw a line outward from the tip of the pyramid in the correct direction (away from the pyramid)

    # 1. Find the special pixel and the triangle, and extract the color of the special pixel
    objects = find_connected_components(input_grid, monochromatic=True, connectivity=8)
    for obj in objects:
        if np.count_nonzero(obj) == 1:
            special_pixel = obj
        else:
            pyramid = obj
    special_pixel_color = next(iter(set(special_pixel.flatten()) - {Color.BLACK}))

    # 2. Find the tip of the pyramid, and which way it is pointing
    # To do this, remember that the special pixel is opposite the tip of the pyramid (and centered on the base)
    # Compute the vector from the special pixel to the centre of the pyramid, and go in that direction to find the tip
    # Computing vector: Difference of center positions
    special_x, special_y, special_w, special_h = bounding_box(special_pixel)
    pyramid_x, pyramid_y, pyramid_w, pyramid_h = bounding_box(pyramid)
    special_center_x, special_center_y = special_x + special_w / 2, special_y + special_h / 2
    pyramid_center_x, pyramid_center_y = pyramid_x + pyramid_w / 2, pyramid_y + pyramid_h / 2
    dx, dy = np.sign([pyramid_center_x - special_center_x, pyramid_center_y - special_center_y])
    # make sure everything grid is ints
    dx, dy = int(dx), int(dy)
    # Move along the vector until we reach the end of the tip, at which point we are on the background (Color.BLACK)
    tip_x, tip_y = special_x, special_y
    while input_grid[tip_x, tip_y] != Color.BLACK:
        tip_x += dx
        tip_y += dy
    
    # 3. Draw a line outward from the tip of the pyramid in the correct direction (away from the pyramid)
    # The line is the same color as the special pixel
    output_grid = np.copy(input_grid)
    draw_line(output_grid, tip_x, tip_y, length=None, direction=(dx, dy), color=special_pixel_color)

    return output_grid

def generate_input():
    # Make the pyramid by concatenating (horizontally) together two lower-diagonal matrices
    pyramid_color = random.choice(Color.NOT_BLACK)
    pyramid_height = np.random.randint(2, 6)
    pyramid_width = 2 * pyramid_height - 1
    pyramid = np.concatenate([np.tri(pyramid_height)[:, ::-1], # left half
                              np.tri(pyramid_height).T[1:]], # right half
                              axis=0) # horizontal (along X axis)
    pyramid[pyramid != 0] = pyramid_color

    # Make the special pixel
    special_pixel_color = random.choice([ color for color in Color.NOT_BLACK if color != pyramid_color ])
    special_y = pyramid_height - 1
    special_x = pyramid_width // 2
    pyramid[special_x, special_y] = special_pixel_color

    # Randomly rotate the pyramid
    rotated_pyramid = np.rot90(pyramid, np.random.randint(4))

    # Make the output grid, ensuring it is large enough to contain the rotated pyramid
    width, height = np.random.randint(rotated_pyramid.shape[0]+2, 20), np.random.randint(rotated_pyramid.shape[1]+2, 20)
    output_grid = np.full((width, height), Color.BLACK)

    # Place the pyramid in the output grid
    x, y = random_free_location_for_sprite(output_grid, rotated_pyramid, border_size=1)
    blit_sprite(output_grid, rotated_pyramid, x, y, background=Color.BLACK)

    return output_grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
