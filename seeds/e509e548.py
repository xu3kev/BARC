from common import *

import numpy as np
from typing import *

# concepts:
# topology, counting

# description:
# In the input you will see a grid with several green objects with different number of bends.
# To make the output, color the objects with one bend with blue, two bends with pink, three bends with red.

def main(input_grid):
    # Create a copy of the input grid to avoid modifying the original
    output_grid = np.copy(input_grid)

    # Find all the green objects in the grid
    object_color = Color.GREEN
    background = Color.BLACK
    objects = find_connected_components(input_grid, monochromatic=True, connectivity=4, background=background)
    for obj in objects:
        # Get the bounding box of the sprite and crop the sprite
        x, y, w, h = bounding_box(obj, background=background)
        sprite = crop(obj, background=Color.BLACK)
        mask = sprite != background

        # Determine how many bends the mask has
        # Do this by building an L-shaped mask, and seeing how many times it appears in the sprite
        bend_mask = np.array([[1, 1], [1, 0]])
        rotated_bend_masks = [bend_mask, np.rot90(bend_mask), np.rot90(bend_mask, 2), np.rot90(bend_mask, 3)]

        from scipy.ndimage import correlate
        
        n_bends = sum( np.sum( correlate(mask*1, filter*1, mode='constant', cval=0) == np.sum(filter*1) ) for filter in rotated_bend_masks )

        # find the new color based on bends
        new_color = {1: Color.BLUE, 2: Color.PINK, 3: Color.RED}[n_bends]
        # color the sprite with the new color
        sprite[sprite == object_color] = new_color
        blit_sprite(output_grid, sprite=sprite, x=x, y=y)

    return output_grid

def generate_input():
    # Generate grid of size n x m
    n, m = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.zeros((n, m), dtype=int)

    # The objects color is green
    object_color = Color.GREEN

    # keep track of what bends we've already created, so that we end up with at least one of each bend
    bends_we_have = set()

    for _ in range(random.randint(3, 6)):
        # Randomly generate sprite with one to three bends
        w, h = np.random.randint(3, 6), np.random.randint(3, 6)

        # Generate sprite with the object color
        sprite = random_sprite(w, h, color_palette=[object_color], symmetry="not_symmetric", density=0.3)

        # calculate how many bends it has and make sure that the number of bends are 1-3
        mask = sprite != Color.BLACK
        bend_mask = np.array([[1, 1], [1, 0]])
        rotated_bend_masks = [bend_mask, np.rot90(bend_mask), np.rot90(bend_mask, 2), np.rot90(bend_mask, 3)]
        from scipy.ndimage import correlate
        n_bends = sum( np.sum( correlate(mask*1, filter*1, mode='constant', cval=0) == np.sum(filter*1) ) for filter in rotated_bend_masks )
        if n_bends not in [1, 2, 3]: continue

        # keep track of what bends we've already created
        bends_we_have.add(n_bends)

        # Randomly place the sprite on the grid
        x, y = random_free_location_for_sprite(grid=grid, sprite=sprite, padding=1, padding_connectivity=8)

        blit_sprite(grid, sprite, x=x, y=y)

    # The input grid should have at least one object one type of bend as example.
    if len(bends_we_have) < 3:
        return generate_input()
    
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
