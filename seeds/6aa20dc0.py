from common import *

import numpy as np
from typing import *

# concepts:
# puzzle pieces, rotation, rescaling

# description:
# In the input you will see a non-black background, a small multicolored object, and fragments of that object rescaled and rotated scattered around.
# To make the output, isolate the small multicolored object and then rescale/rotate/translate to cover the fragments as much as possible, matching color whenever the fragment has that color.

def main(input_grid):
    # Plan:
    # 1. Detect the object, separating the small multicolored puzzle piece from its fragments
    # 2. Rescale/rotate/translate the small object
    # 3. Find the transformation covering as much of the fragments as possible, matching colors whenever they overlap
    # 4. Copy the resulting transformation to the output grid; delete the fragments from the input
    # 5. Repeat until all the fragments are gone

    # 1. object detection
    # because the background is not black, set it to be the most common color
    background = max(Color.NOT_BLACK, key=lambda color: np.sum(input_grid == color))
    # detect the objects and figure out which is the template puzzle piece, which is going to be the one with the largest variety of colors
    objects = find_connected_components(input_grid, connectivity=8, background=background, monochromatic=False)
    template_object = max(objects, key=lambda obj: len(object_colors(obj, background=background)))
    template_sprite = crop(template_object, background=background)

    output_grid = np.full_like(input_grid, background)

    # 2. rescale/rotate/translate the small object to cover as much of the fragments as possible, matching colors whenever they overlap
    rescaled_and_rotated = [ np.rot90(scale_sprite(template_sprite, scale), k=rot)
                            for scale in [1, 2, 3, 4]
                            for rot in range(4) ]
    # A placement solution is a tuple of (x, y, sprite) where x, y is the top-left corner of the rotated/scaled sprite
    possible_solutions = [ (x, y, sprite)
                          for sprite in rescaled_and_rotated
                          for x in range(output_grid.shape[0] - sprite.shape[0])
                          for y in range(output_grid.shape[1] - sprite.shape[1]) ]
    
    # Keep on looping until we are out of things to copy to the output
    while np.any(input_grid != background):

        def score_solution(x, y, sprite):
            # The score is -inf if the placement violates non-background colors
            # Otherwise it is the number of pixels that match in color between the sprite and the input
            test_canvas = np.full_like(input_grid, background)
            blit_sprite(test_canvas, sprite, x, y)

            if np.any( (test_canvas != background) & (input_grid != background) & (test_canvas != input_grid) ):
                return float("-inf")
            
            return np.sum( (test_canvas == input_grid) & (input_grid != background) )
        
        # Remove -inf solutions, and zero solutions
        possible_solutions = [ solution for solution in possible_solutions if score_solution(*solution) > 0 ]
        
        best_x, best_y, best_sprite = max(possible_solutions, key=lambda solution: score_solution(*solution))

        # 4. Copy the resulting transformation to the output grid; delete the fragments from the input
        # Copy output
        blit_sprite(output_grid, best_sprite, best_x, best_y)
        # Delete from input
        for dx, dy in np.argwhere(best_sprite != background):
            input_grid[best_x + dx, best_y + dy] = background
        
        # 5. Repeat until all the fragments are gone
    
    return output_grid


def generate_input():
    # Create a template puzzle piece, and then put down some randomly transformed+occluded versions of it on a non-black background

    background = random.choice(Color.NOT_BLACK)
    width, height = np.random.randint(10, 30), np.random.randint(10, 30)
    grid = np.full((width, height), background)

    template_puzzle_piece = random_sprite([2,3,4], [2,3,4], connectivity=8, color_palette=Color.NOT_BLACK, background=background)
    x, y = random_free_location_for_sprite(grid, template_puzzle_piece, background=background)
    blit_sprite(grid, template_puzzle_piece, x, y, background=background)

    n_fragments = np.random.randint(1, 3)
    for _ in range(n_fragments):
        fragment = template_puzzle_piece.copy()
        # randomly occlude w/ background squares
        fragment[np.random.rand(*fragment.shape) < 0.3] = background
        # randomly rotate and scale
        fragment = np.rot90(fragment, k=np.random.randint(0, 4))
        fragment = scale_sprite(fragment, np.random.randint(1, 3+1))
        x, y = random_free_location_for_sprite(grid, fragment, background=background, padding=2, border_size=2)
        blit_sprite(grid, fragment, x, y, background=background)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
