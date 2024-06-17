from common import *

import numpy as np
from typing import *

# concepts:
# objects, color, alignment, scaling

# description:
# In the input you will see a large object that represents a pattern using only one color and a square object with many colors.
# To make the output, make the pattern of the large object with the colors of the small object. The pattern should be scaled to fit the smaller object and aligned to the top left corner of the smaller object.

def main(input_grid):
    # find all the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    # figure out which object is the pattern and which object is the multi-colored square
    pattern = square = None
    for obj in objects:
        # if the object has only one color and black, it is the pattern. Otherwise, it is the multi-colored square.
        if len(set(obj.flatten())) == 2:
            pattern = obj
        else:
            square = obj
    
    # cut out the bounding box of the square
    x, y, width, height = bounding_box(square)
    square = square[x:x+width, y:y+height]

    # cut out the bounding box of the pattern
    x2, y2, width2, height2 = bounding_box(pattern)
    # make sure the pattern is square
    if width2 != height2:
        width2 = height2 = max(width2, height2)
    pattern = pattern[x2:x2+width2, y2:y2+height2]

    # figure out how much bigger the pattern is than the square
    scale = width2 // width

    # scale down the pattern to fit the square
    scaled_pattern = np.zeros_like(square) 
    for i in range(width):
        for j in range(height):
            scaled_pattern[i,j] = pattern[i * scale, j * scale]
    
    # if the pixel is in the pattern, keep the color from the square otherwise make it black in the output grid
    output_grid = np.where(scaled_pattern, square, Color.BLACK)

    return output_grid


def generate_input():
    # decide how big the multi-colored square will be
    size = np.random.randint(3, 5)

    # make the multi-colored square with all colors except black
    square = random_sprite(size, size, 1, "not_symmetric", Color.NOT_BLACK)
    
    # make sure the square has more than one color, if not then try again
    if len(set(square.flatten())) == 1:
        return generate_input()

    # make a random pattern that is the same size as the multi-colored square but only uses one color 
    color = np.random.choice(list(Color.NOT_BLACK))
    pattern = random_sprite(size, size, .7, "not_symmetric", [color], 8)

    # check that pattern is continuous, if not then try again
    if not is_contiguous(pattern, connectivity=8):
        return generate_input()

    # decide how much to scale up the pattern
    scale = np.random.randint(2, 6)

    # scale up the pattern
    pattern = np.repeat(np.repeat(pattern, scale, axis=0), scale, axis=1)

    # make a grid large enough to fit both the pattern and the multi-colored square without touching
    n = m = (size * scale) + (2 * size) + np.random.randint(2, 5)
    grid = np.zeros((n, m), dtype=int)

    # put the pattern on the grid randomly
    x, y = np.random.randint(0, n - size * scale), np.random.randint(0, m - size * scale)
    blit(grid, pattern, x, y)

    # put the multi-colored square on the grid randomly but not touching the pattern
    x2, y2 = random_free_location_for_object(grid, square)
    # make sure the multi-colored square is not touching the pattern, if it is then keep looking for a place to put it
    while contact(object1=grid, object2=square, x2=x2, y2=y2, connectivity=8):
        x2, y2 = random_free_location_for_object(grid, square)
    blit(grid, square, x2, y2)

    return grid






# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)