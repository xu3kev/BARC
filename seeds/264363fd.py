from common import *

import numpy as np
from typing import *


# concepts:
# patterns, growing, horizontal/vertical bars

# description:
# In the input you will see a 30x30 grid with at least two rectangles, each with at least one special pixel of a different color, and a crosshair-type pattern outside these rectangles.
# For each of these special pixels, apply the crosshair pattern and extend the points inside the rectangle that special pixel is in, until it reaches the edge.

def main(input_grid):
    # first get the grid size
    n, m = input_grid.shape

    # figure out background color by assuming it is the most common color
    background_color = np.bincount(input_grid.flatten()).argmax()

    # with this background color, find the polychromatic objects
    objects = find_connected_components(input_grid, background=background_color, connectivity=8, monochromatic=False)

    # sort the objects by their size in terms of area, the crosshair is the smallest object
    sorted_objects = sorted(objects, key=lambda x: np.count_nonzero(x != background_color))
    crosshair_object = sorted_objects[0]
    rectangles = sorted_objects[1:]

    # now find the crosshair sprite coordinates
    crosshair_sprite = crop(crosshair_object, background=background_color)
    width, height = crosshair_sprite.shape
    
    # if the crosshair is wider than it is tall, it extends horizontally, vertically if taller, both if square
    horizontal = True
    vertical = True
    if width > height:
        vertical = False
        point_color = crosshair_sprite[0, height // 2]
    elif height > width:
        horizontal = False
        point_color = crosshair_sprite[width // 2, 0]
    else:
        point_color = crosshair_sprite[width // 2, 0]

    # now we prepare the output grid
    output_grid = np.full_like(input_grid, background_color)

    # for each rectangle, crop it to just the rectangle, find the special pixel, extend the crosshair pattern from it, then add it back to the grid
    for rectangle in rectangles:
        # crop the rectangle to just the rectangle, while preserving its position in the grid
        rec_x, rec_y, w, h = bounding_box(rectangle, background=background_color)
        cropped_rectangle = crop(rectangle, background=background_color)

        # find the special color, it is the least common color in the rectangle
        colors, counts = np.unique(cropped_rectangle, return_counts=True)
        # colors are sorted by their frequency, so choose least common as the special color
        special_color = colors[-1]
        rectangle_color = colors[-2]

        # for each special pixel, extend the crosshair pattern
        for x, y in np.argwhere(cropped_rectangle == special_color):
            # first color the special pixel with the crosshair sprite centered on it
            cropped_rectangle = blit_sprite(cropped_rectangle, crosshair_sprite, x - width // 2, y - height // 2, background=background_color)

            # then extend the points in the crosshair pattern until they reach the edge of the rectangle
            if horizontal:
                for x0 in range(w):
                    if cropped_rectangle[x0, y] == rectangle_color:
                        cropped_rectangle[x0, y] = point_color
            if vertical:
                for y0 in range(h):
                    if cropped_rectangle[x, y0] == rectangle_color:
                        cropped_rectangle[x, y0] = point_color
        
        # add the rectangle back to the grid
        blit_sprite(output_grid, cropped_rectangle, rec_x, rec_y, background=background_color)

    return output_grid


def generate_input():
    # not complete

    return None

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)