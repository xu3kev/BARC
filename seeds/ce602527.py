from common import *

import numpy as np
from typing import *

# concepts:
# scaling, shape matching, non-black background

# description:
# In the input you should see three objects, two of which are the same shape but different sizes and colors. The third object is a different shape.
# To make the output, you need to find the two objects that are the same shape but different sizes and colors.
# Return the smaller object in the same shape.

def main(input_grid):
    # Plan:
    # 1. Find the background color
    # 2. Extract objects by color
    # 3. Define a helper function to check if two objects are the same shape but different color/scale, remembering that the bigger one might be partially out of the canvas
    # 4. Iterate all candidate objects and check if they are the same shape but different color/scale
    # 5. Return what we find

    # Determine the background color, which is the most common color in the grid
    colors = np.unique(input_grid)
    background = colors[np.argmax([np.sum(input_grid == c) for c in colors])]
    object_colors = [c for c in colors if c != background]

    # Extract the objects, each of which is a different color.
    # This means we can split the canvas by color, instead of using connected components.
    objects = []
    for color in object_colors:
        object = np.copy(input_grid)
        object[input_grid != color] = background
        objects.append(object)
    
    # Define a helper function for checking if two objects are different color/scale but same shape
    # This has to handle the case where the bigger object is partially outside the grid
    def same_shape_different_color_different_scale(obj1, obj2):
        # obj1 is the smaller object
        if np.sum(obj1 != background) > np.sum(obj2 != background): return False

        mask1 = crop(obj1, background=background) != background
        mask2 = crop(obj2, background=background) != background

        # Loop through all possible scale factors
        for scale_factor in range(2, 4):
            scaled_mask1 = scale_sprite(mask1, scale_factor)
            # loop over all possible places that we might put mask2, which starts anywhere in the scaled_mask1
            # note that we are only doing this because there can be objects that fall outside of the canvas
            # otherwise we would just compare the two masks directly
            for dx, dy in np.ndindex(scaled_mask1.shape):
                if np.array_equal(scaled_mask1[dx : dx + mask2.shape[0], dy : dy + mask2.shape[1]], mask2):
                    return True
        return False
    
    output_grid_candidates = []
    # Iterate all candidate objects
    for obj in objects:
        other_objects = [o for o in objects if o is not obj]
        if any( same_shape_different_color_different_scale(obj, other_obj) for other_obj in other_objects ):
            output_grid_candidates.append(obj)

    # Check if the generated input grid is valid
    assert len(output_grid_candidates) == 1, f"Should only have one output grid candidate, have {len(output_grid_candidates)}"

    output_grid = crop(output_grid_candidates[0], background=background)

    return output_grid

def generate_input():
    # get color for background and three objects
    background, small_color, big_color, other_color = np.random.choice(Color.NOT_BLACK, 4, replace=False)

    # Create background grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.full((n, m), background)

    # Create two different sprites
    n1, m1 = np.random.randint(3, 6), np.random.randint(3, 6)
    n2, m2 = np.random.randint(3, 6), np.random.randint(3, 6)

    sprite_small = random_sprite(n=n1, m=m1, color_palette=[small_color], background=background, connectivity=8)
    sprite_other = random_sprite(n=n2, m=m2, color_palette=[other_color], background=background, connectivity=8)

    # Scale the small sprite to the big sprite
    scale_factor = np.random.randint(2, 4)
    sprite_big = scale_sprite(sprite_small, scale_factor)
    # change its color
    sprite_big[sprite_big == small_color] = big_color

    # Place the big sprite on the grid
    # The sprite can be partially outside the grid
    # Ensure the sprite is not too outside the grid
    padding = 4
    x, y = np.random.randint(padding, n - padding), np.random.randint(padding, m - padding)
    blit_sprite(grid=grid, sprite=sprite_big, x=x, y=y, background=background)

    try:
        # Place the small sprite on the grid
        x, y = random_free_location_for_sprite(grid=grid, sprite=sprite_small, background=background)
        blit_sprite(grid=grid, sprite=sprite_small, x=x, y=y, background=background)

        # Place the other sprite on the grid
        x, y = random_free_location_for_sprite(grid=grid, sprite=sprite_other, background=background)
        blit_sprite(grid=grid, sprite=sprite_other, x=x, y=y, background=background)

        # Check if the generated grid is valid
        main(grid)
    except:
        return generate_input()

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
