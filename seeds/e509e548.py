from common import *

import numpy as np
from typing import *

# concepts:
# count bends, color

# description:
# In the input you will see a grid with several green objects with different number of bends.
# To make the output, color the objects with one bend with blue, two bends with pink, three bends with red.

def main(input_grid):
    # Create a copy of the input grid to avoid modifying the original
    output_grid = np.copy(input_grid)

    # Find all the green objects in the grid
    object_color = Color.GREEN
    sprites = find_connected_components(grid=input_grid, background=Color.BLACK, monochromatic=True, connectivity=4)
    for sprite in sprites:
        # Get the bounding box of the sprite and crop the sprite
        obj_x, obj_y, w, h = bounding_box(grid=sprite, background=Color.BLACK)
        sprite = crop(grid=sprite, background=Color.BLACK)

        # Determine how many bends the sprite has
        bend_number = 0
        bend = np.array([[Color.BLACK, object_color], 
                        [object_color, object_color]])
        
        # Iterate over all the pixels in the sprite
        for x, y in np.ndindex(w, h):
            # Check if current position is a bend
            current_pattern = sprite[x:x+2, y:y+2]
            if np.array_equal(current_pattern, bend):
                bend_number += 1
            elif np.array_equal(current_pattern, np.rot90(bend, k=1)):
                bend_number += 1
            elif np.array_equal(current_pattern, np.rot90(bend, k=2)):
                bend_number += 1
            elif np.array_equal(current_pattern, np.rot90(bend, k=3)):
                bend_number += 1

        # If bend number is 1, color the sprite with blue
        if bend_number == 1:
            sprite[sprite == object_color] = Color.BLUE
        # If bend number is 2, color the sprite with pink
        elif bend_number == 2:
            sprite[sprite == object_color] = Color.PINK
        # If bend number is 3, color the sprite with red
        elif bend_number == 3:
            sprite[sprite == object_color] = Color.RED

        output_grid = blit_sprite(grid=output_grid, sprite=sprite, x=obj_x, y=obj_y)
    return output_grid

def generate_input():
    # Generate grid of size n x m
    n, m = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.zeros((n, m), dtype=int)

    # The objects color is green
    object_color = Color.GREEN
    one_bend, two_bends, three_bends = 0, 0, 0
    while True:
        # Randomly generate sprite with one to three bends
        w, h = np.random.randint(3, 6), np.random.randint(3, 6)

        # Generate sprite with the object color
        # If the sprite cannot be generated, regenerate the sprite
        try:
            sprite = random_sprite(n=w, m=h, color_palette=[object_color])
        except:
            continue

        # Determine how many bends the sprite has
        bend_number = 0
        bend = np.array([[Color.BLACK, object_color], 
                        [object_color, object_color]])

        # Iterate over all the pixels in the sprite
        for x, y in np.ndindex(w, h):
            # Check if current position is a bend
            current_pattern = sprite[x:x+2, y:y+2]
            if np.array_equal(current_pattern, bend):
                bend_number += 1
            elif np.array_equal(current_pattern, np.rot90(bend, k=1)):
                bend_number += 1
            elif np.array_equal(current_pattern, np.rot90(bend, k=2)):
                bend_number += 1
            elif np.array_equal(current_pattern, np.rot90(bend, k=3)):
                bend_number += 1

        # If the sprite does not have any bends or has more than three bends, regenerate the sprite
        if bend_number == 0 or bend_number > 3:
            continue

        # Randomly place the sprite on the grid
        try:
            x, y = random_free_location_for_sprite(grid=grid, sprite=sprite, padding=1, padding_connectivity=8)

        # If there is no free location for the sprite, break the loop
        except:
            break

        if bend_number == 1:
            one_bend += 1
        elif bend_number == 2:
            two_bends += 1
        elif bend_number == 3:
            three_bends += 1

        grid = blit_sprite(grid=grid, sprite=sprite, x=x, y=y)

    # The input grid should have at least one object one type of bend as example.
    if one_bend == 0 or two_bends == 0 or three_bends == 0:
        return generate_input()
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
