from common import *

import numpy as np
from typing import *

# concepts:
# objects, color guide, masking, rotation

# description:
# In the input, you will see a large square monochromatic object and a smaller square with many colors.
# To make the output, rotate the large square by 90 degrees clockwise and use it to create a binary mask for the smaller square.
# Apply the mask to the small square and return the resulting masked object.

def main(input_grid: np.ndarray) -> np.ndarray:
    # find all the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    # figure out which object is the pattern and which one is the multi-colored square
    pattern = square = None
    for obj in objects:
        # if the object has only one color and black, it is the pattern. Otherwise, it is the multi-colored square.
        if len(set(obj.flatten())) == 2:
            pattern = obj
        else:
            square = obj

    # crop out the bounding box of the pattern and the square
    pattern = crop(pattern)
    square = crop(square)

    # rotate the pattern 90 degrees clockwise
    rotated_pattern = np.rot90(pattern, k=-1)

    # shape of the smaller square
    square_shape = square.shape

    # resize the rotated pattern to the same shape as the square
    resized_pattern = np.zeros_like(square)
    pattern_shape = rotated_pattern.shape
    scale_x, scale_y = square_shape[0] / pattern_shape[0], square_shape[1] / pattern_shape[1]

    for x in range(square_shape[0]):
        for y in range(square_shape[1]):
            px, py = int(x / scale_x), int(y / scale_y)
            resized_pattern[x, y] = rotated_pattern[px, py]

    # if the pixel in the resized pattern is not black, keep the color from the square, otherwise make it black in the output
    output_grid = np.where(resized_pattern != Color.BLACK, square, Color.BLACK)

    return output_grid

def generate_input():
    # size of the small multi-colored square
    size = np.random.randint(3, 5)

    # create the multi-colored square with random colors (non-black)
    square = random_sprite(size, size, density=1, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)

    # ensure the square contains more than one color
    if len(set(square.flatten())) == 1:
        return generate_input()

    # create a monochromatic pattern
    color = np.random.choice(list(Color.NOT_BLACK))
    pattern = random_sprite(size, size, density=0.7, symmetry="not_symmetric", color_palette=[color], connectivity=8)

    # ensure that the pattern is contiguous
    if not is_contiguous(pattern, connectivity=8):
        return generate_input()

    # scale the pattern up by a random factor
    scale_factor = np.random.randint(2, 6)
    pattern_large = np.repeat(np.repeat(pattern, scale_factor, axis=0), scale_factor, axis=1)

    # create a grid large enough to fit both the large pattern and the multi-colored square without touching each other
    n = (size * scale_factor) + (2 * size) + np.random.randint(2, 5)
    grid = np.zeros((n, n), dtype=int)

    # randomly place the large pattern on the grid
    x, y = np.random.randint(0, n - size * scale_factor), np.random.randint(0, n - size * scale_factor)
    blit_sprite(grid, pattern_large, x=x, y=y)

    # find a random place for the multi-colored square, ensuring it doesn't touch the pattern
    x2, y2 = random_free_location_for_sprite(grid, square)
    while contact(object1=grid, object2=square, x2=x2, y2=y2, connectivity=8):
        x2, y2 = random_free_location_for_sprite(grid, square)
    
    blit_sprite(grid, square, x=x2, y=y2)

    return grid