from common import *

import numpy as np
from typing import *

# concepts:
# attraction, objects, non-black background

# description:
# In the input you will see a non-black background with a colored rectangle and some colored pixels sprinkled randomly.
# To make the output, draw a horizontal or vertical line connecting each colored pixel to the rectangle (whenever possible: the rectangle and pixel have to be lined up). Color the line the same as the pixel.

def main(input_grid):
    # Plan:
    # 1. Find the background color
    # 2. Extract objects, separating the pixels from the rectangle
    # 3. For each pixel, draw a line to the rectangle

    # The background is the most common color
    background = np.bincount(input_grid.flatten()).argmax()

    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True, background=background)
    # The rectangle is the largest object
    rectangle_object = max(objects, key=lambda obj: np.sum(obj != background))
    # The pixels are the rest
    pixel_objects = [obj for obj in objects if obj is not rectangle_object]

    for pixel_object in pixel_objects:
        for x, y in np.argwhere(pixel_object != background):
            pixel_color = pixel_object[x, y]

            # Check if the pixel is on a horizontal or vertical line with the rectangle
            # Do this by trying to move the pixel up/down/left/right by different amounts until there is contact
            # After finding contact, double check that going one step further would lead to overlap (collision) to avoid glancing contact
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]: # up, right, down, left
                for distance in range(max(input_grid.shape)):
                    translated_pixel = translate(pixel_object, distance * dx, distance * dy, background=background)
                    if contact(object1=translated_pixel, object2=rectangle_object, background=background) and \
                        collision(object1=translate(pixel_object, (distance + 1) * dx, (distance + 1) * dy, background=background), object2=rectangle_object, background=background):
                        # Draw the line
                        end_x, end_y = x + distance * dx, y + distance * dy
                        draw_line(input_grid, x, y, end_x=end_x, end_y=end_y, color=pixel_color)
                        break
    
    return input_grid
                


def generate_input():
    # Plan:
    # 1. Pick different colors for the background, rectangle, and pixels
    # 2. Randomly place the rectangle
    # 3. Randomly place the pixels
    # 4. Check that at least one pixel will make a line to the rectangle

    background_color, rectangle_color, pixel_color = np.random.choice(Color.NOT_BLACK, size=3, replace=False)
    width, height = np.random.randint(7, 20, size=2)

    input_grid = np.full((width, height), fill_value=background_color)

    rectangle_width, rectangle_height = np.random.randint(2, width//2), np.random.randint(2, height//2)
    rectangle_sprite = random_sprite(rectangle_width, rectangle_height, color_palette=[rectangle_color], density=1)
    rectangle_x, rectangle_y = random_free_location_for_sprite(input_grid, rectangle_sprite, background=background_color, padding=1, border_size=1)
    blit_sprite(input_grid, rectangle_sprite, x=rectangle_x, y=rectangle_y, background=background_color)

    n_pixels = np.random.randint(2, 8)
    for _ in range(n_pixels):
        pixel_sprite = random_sprite(1, 1, color_palette=[pixel_color], density=1)
        pixel_x, pixel_y = random_free_location_for_sprite(input_grid, pixel_sprite, background=background_color, padding=1, border_size=1)
        blit_sprite(input_grid, pixel_sprite, x=pixel_x, y=pixel_y, background=background_color)
    
    # Check that at least one pixel shares an X or Y coordinate with the rectangle
    rectangle_coordinates = np.argwhere(input_grid == rectangle_color)
    pixel_coordinates = np.argwhere(input_grid == pixel_color)
    rectangle_xs, rectangle_ys = set(rectangle_coordinates[:, 0]), set(rectangle_coordinates[:, 1])
    pixel_xs, pixel_ys = set(pixel_coordinates[:, 0]), set(pixel_coordinates[:, 1])
    if not (rectangle_xs & pixel_xs) and not (rectangle_ys & pixel_ys):
        return generate_input()
    
    return input_grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
