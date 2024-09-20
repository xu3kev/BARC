from common import *

import numpy as np
from typing import *

# concepts:
# pattern recognition, rotation, color correspondence, pattern reconstruction

# description:
# In the input you will see one or two color pattern with a red or green pixel as an indicator
# and a set of red and green pixels. 
# To make the output, you should reconstruct the pattern with the red and green pixels 
# indicates the pattern's position. If the indicator is red, the pattern should be flipped by x-axis before reconstructing.

def main(input_grid):
    # Detect the continuous object in the input grid
    objects = detect_objects(grid=input_grid, monochromatic=False, connectivity=8)
    pixels = []
    original_pattern = []

    # Find out the original pattern and the pixel indicator for reconstruction
    for obj in objects:
        cropped_obj = crop(grid=obj, background=Color.BLACK)
        if cropped_obj.shape == (1,1):
            pixels.append(obj)
        else:
            original_pattern.append(cropped_obj)
    output_grid = input_grid.copy()

    for pattern in original_pattern:
        # If the indicator color is red, flip the pattern by x-axis
        if np.any(pattern == Color.RED):
            indicator_color = Color.RED
            pattern = np.flipud(pattern)
        else:
            indicator_color = Color.GREEN
        
        # Find the relative position of the indicator pixel in the pattern
        rela_x, rela_y = np.where(pattern == indicator_color)
        rela_x, rela_y = rela_x[0], rela_y[0]

        for pixel in pixels:
            color_pixel = Color.RED if np.any(pixel == Color.RED) else Color.GREEN

            # Find the position of the indicator pixel in the input grid
            if color_pixel == indicator_color:
                x, y = np.where(pixel == color_pixel)
                x, y = x[0], y[0]
                x -= rela_x
                y -= rela_y

                # Place the pattern in correct position using the indicator pixel, finish the reconstruction
                output_grid = blit_sprite(x=x, y=y, grid=output_grid, sprite=pattern, background=Color.BLACK)
    return output_grid

def generate_input():
    # Initialize the grid
    n, m = 13, 13
    grid = np.zeros((n, m), dtype=int)

    # The indicator color is red or green, the pattern color is blue, yellow or teal
    number_object = np.random.randint(1, 3)
    indicator_color = [Color.RED, Color.GREEN]
    available_color = [Color.BLUE, Color.YELLOW, Color.TEAL]

    # mask color: dummy color used to indicate where we aren't allowed to put something
    # these mask color pixel wil be occupied in the output, when that's computed
    # after making the input, we scrub the mask color (change it to black)
    mask_color = mask_color

    # Randomly shuffle the indicator color and available color
    random.shuffle(indicator_color)
    random.shuffle(available_color)


    # There are 1 or 2 object pattern need to be reconstructed
    for i in range(number_object):
        # Generate the object pattern need to be reconstructed, use mask_color to represent the object pattern
        object_pattern = random_sprite(n=3, m=3, color_palette=[mask_color], density=0.5, symmetry="not_symmetric")

        # There are 1 or 2 object pattern need to be reconstructed
        num_sample = np.random.randint(1, 3)

        # Place the indicator in the object pattern
        position_x, position_y = np.random.randint(0, 3), np.random.randint(0, 3)
        while object_pattern[position_x, position_y] != mask_color:
            position_x, position_y = np.random.randint(0, 3), np.random.randint(0, 3)

        # Randomly place the object pattern in the grid
        for _ in range(num_sample):
            object_pattern[position_x, position_y] = indicator_color[i]
            x, y = random_free_location_for_sprite(grid=grid, sprite=object_pattern, padding=1, padding_connectivity=8)
            grid = blit_sprite(x=x, y=y, grid=grid, sprite=object_pattern, background=Color.BLACK)
        
        # Replace the gray color with the available color as the original pattern for reconstruction
        showed_pattern = object_pattern.copy()
        showed_pattern[showed_pattern == mask_color] = available_color[i]

        # If the indicator color is red, flip the pattern by x-axis
        if indicator_color[i] == Color.RED:
            showed_pattern = np.flipud(showed_pattern)
        
        # Place the original pattern in the grid
        x, y = random_free_location_for_sprite(grid=grid, sprite=showed_pattern, padding=1, padding_connectivity=8)
        grid = blit_sprite(x=x, y=y, grid=grid, sprite=showed_pattern, background=Color.BLACK)
    
    grid[grid == mask_color] = Color.BLACK

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
