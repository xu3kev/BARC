from common import *

import numpy as np
from typing import *

# concepts:
# symmetry detection, occlusion

# description:
# In the input you will see a translationally symmetric pattern that has been partially occluded by a black rectangle
# The output should be what the black rectangle should be in order to make it perfectly symmetric.
# In other words, the output should be the missing part of the pattern, and it should be the same dimensions as the black rectangle.

def main(input_grid):
    # Plan:
    # 1. Find the black rectangle
    # 2. Find the symmetry
    # 3. Fill in the missing part
    # 4. Extract the part that you filled in, which is the final output

    # Find the black rectangle and save where it is
    # Do this first because we will need to know where it was after we fill it in
    occlusion_color = Color.BLACK
    black_rectangle_mask = (input_grid == occlusion_color)

    # Find the symmetry. Notice that black is not the background, but instead is the occlusion color. In fact there is no well-defined background color.
    symmetries = detect_translational_symmetry(input_grid, ignore_colors=[occlusion_color], background=None)

    # Fill in the missing part
    for occluded_x, occluded_y in np.argwhere(black_rectangle_mask):
        for symmetric_x, symmetric_y in orbit(input_grid, occluded_x, occluded_y, symmetries):
            if input_grid[symmetric_x, symmetric_y] != occlusion_color:
                input_grid[occluded_x, occluded_y] = input_grid[symmetric_x, symmetric_y]
                break
    
    # Extract the region that we filled in, ultimately as a 2D sprite
    # first, get just the part of the final image which corresponds to what used to be included
    filled_in_region = np.full_like(input_grid, occlusion_color)
    filled_in_region[black_rectangle_mask] = input_grid[black_rectangle_mask]
    # then, crop it to obtain the sprite
    filled_in_region = crop(filled_in_region, background=occlusion_color)

    return filled_in_region
    


def generate_input():
    # Plan:
    # 1. Make a random sprite
    # 2. Tile it to make a symmetric pattern
    # 3. Occlude it with a black rectangle

    # Make a random sprite
    w, h = np.random.randint(2, 5, size=(2))
    sprite = random_sprite(w, h, color_palette=Color.NOT_BLACK, density=1)

    # Tile it to make a symmetric pattern
    horizontal_repetitions, vertical_repetitions = np.random.randint(2, 5, size=(2))
    pattern = np.tile(sprite, (horizontal_repetitions, vertical_repetitions))

    # Occlude it with a randomly placed black rectangle
    w_occluder, h_occluder = np.random.randint(2, 5, size=(2))
    x_occluder, y_occluder = np.random.randint(0, pattern.shape[0] - w_occluder + 1), np.random.randint(0, pattern.shape[1] - h_occluder + 1)
    black_rectangle_sprite = np.full((w_occluder, h_occluder), Color.BLACK)
    blit_sprite(pattern, black_rectangle_sprite, x_occluder, y_occluder, background=None)

    return pattern
    



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
