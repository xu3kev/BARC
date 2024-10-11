from common import *

import numpy as np
from typing import *

# concepts:
# puzzle pieces, rescaling

# description:
# In the input you will see a small multicolored object, and a big region bordered by 4 yellow pixels in the corners. The big region contains some colored things.
# To make the output, rescale and translate the small multicolored object so that it is in the big region and matches as much as possible the colors of the things in the big region.
# The output should be just the big region with its 4 yellow pixels (plus the rescaled and translated thing).

def main(input_grid):
    # Plan:
    # 1. Detect the little object, yellow pixels, and big region
    # 2. Rescale and translate the little object to cover as much of the big region as possible, matching colors whenever they overlap

    # 1. Detect little object, yellow pixels, and big region
    objects = find_connected_components(input_grid, connectivity=4, background=Color.BLACK, monochromatic=False)
    yellow_pixel_objects = [ obj for obj in objects if set(object_colors(obj, background=Color.BLACK)) == {Color.YELLOW} and crop(obj).shape == (1, 1) ]
    assert len(yellow_pixel_objects) == 4, "There should be exactly 4 yellow pixels"

    # Find the region indicated by the 4 yellow pixels
    yellow_pixel_min_x, yellow_pixel_max_x, yellow_pixel_min_y, yellow_pixel_max_y = \
        min([ object_position(obj, anchor="center")[0] for obj in yellow_pixel_objects ]), \
        max([ object_position(obj, anchor="center")[0] for obj in yellow_pixel_objects ]), \
        min([ object_position(obj, anchor="center")[1] for obj in yellow_pixel_objects ]), \
        max([ object_position(obj, anchor="center")[1] for obj in yellow_pixel_objects ])
    
    # The little object is what is outside that region
    little_objects = [ obj for obj in objects
                      if object_position(obj, anchor="center")[0] < yellow_pixel_min_x or object_position(obj, anchor="center")[0] > yellow_pixel_max_x or object_position(obj, anchor="center")[1] < yellow_pixel_min_y or object_position(obj, anchor="center")[1] > yellow_pixel_max_y ]
    assert len(little_objects) == 1, "There should be exactly one little object"
    little_object = little_objects[0]

    # The output grid is going to be the region delimited by the yellow pixels
    output_grid = input_grid[yellow_pixel_min_x:yellow_pixel_max_x+1, yellow_pixel_min_y:yellow_pixel_max_y+1]

    # The big region has some colored pixels that we are going to try and match with
    # Extract the content of big region as tuples (x, y, color)
    big_region_pixels = [ (x, y, output_grid[x, y])
                         for x in range(output_grid.shape[0]) for y in range(output_grid.shape[1])
                         if output_grid[x, y] != Color.BLACK and output_grid[x, y] != Color.YELLOW ]

    # 2. Rescale and translate the little object to cover as much of the big region as possible, matching colors whenever they overlap
    little_sprite = crop(little_object, background=Color.BLACK)
    scaled_sprites = [ scale_sprite(little_sprite, factor) for factor in [1, 2, 3, 4, 5, 6] ]
    # A placement solution is a tuple of (x, y, scaled_sprite) where x, y is the top-left corner of the scaled sprite
    possible_solutions = [ (x, y, scaled_sprite) for scaled_sprite in scaled_sprites
                          for x in range(output_grid.shape[0] - scaled_sprite.shape[0])
                          for y in range(output_grid.shape[0] - scaled_sprite.shape[1]) ]
    
    # Filter placement solutions to only those where the colors of the big region match the colors of the scaled+translated sprite
    def valid_solution(x, y, scaled_sprite):
        # Make a canvas to try putting down the scaled sprite
        test_canvas = np.full_like(output_grid, Color.BLACK)
        blit_sprite(test_canvas, scaled_sprite, x, y)
        # Check if every big region color is also in the test canvas
        test_colors = [ (x, y, test_canvas[x, y]) for x in range(output_grid.shape[0]) for y in range(output_grid.shape[1]) if test_canvas[x, y] != Color.BLACK ]
        return all( (x, y, color) in test_colors for x, y, color in big_region_pixels )        
    
    possible_solutions = [ solution for solution in possible_solutions if valid_solution(*solution) ]
    if len(possible_solutions) == 0:
        assert False, "No solution found for the little object"
    
    # Pick the first solution and blit the sprite into the output grid
    x, y, scaled_sprite = list(possible_solutions)[0]
    blit_sprite(output_grid, scaled_sprite, x, y)

    return output_grid

def generate_input():
    # Create a little object and then rescale it to make a big version.
    # Cover up some parts of the big version with black pixels, and put yellow markers in the corners.
    # Finally figure out how to put everything on a big canvas

    little_sprite = random_sprite([2,3,4], [2,3,4], connectivity=4, color_palette=[color for color in Color.NOT_BLACK if color != Color.YELLOW], background=Color.BLACK)
    scaling_factor = np.random.randint(2, 4+1)
    big_sprite = scale_sprite(little_sprite, scaling_factor)

    # Cover up some parts of the big sprite with black pixels
    for _ in range(np.random.randint(1, 3)):
        x0, y0 = np.random.randint(0, big_sprite.shape[0]), np.random.randint(0, big_sprite.shape[1])
        x1, y1 = np.random.randint(x0, big_sprite.shape[0]), np.random.randint(y0, big_sprite.shape[1])
        big_sprite[x0:x1+1, y0:y1+1] = Color.BLACK

    # Create a big-ish canvas
    width, height = np.random.randint(big_sprite.shape[0]+7, 30), np.random.randint(big_sprite.shape[1]+7, 30)
    grid = np.full((width, height), Color.BLACK)
    
    # Put the big sprite in the canvas
    x, y = random_free_location_for_sprite(grid, big_sprite, background=Color.BLACK)
    blit_sprite(grid, big_sprite, x, y)

    # Put yellow markers in the corners
    grid[x-1, y-1] = Color.YELLOW
    grid[x-1, y+big_sprite.shape[1]] = Color.YELLOW
    grid[x+big_sprite.shape[0], y-1] = Color.YELLOW
    grid[x+big_sprite.shape[0], y+big_sprite.shape[1]] = Color.YELLOW
    
    # Find a spot for the little sprite
    x, y = random_free_location_for_sprite(grid, little_sprite, background=Color.BLACK)
    blit_sprite(grid, little_sprite, x, y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
