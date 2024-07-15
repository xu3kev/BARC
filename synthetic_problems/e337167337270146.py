from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, occlusion, growing

# description:
# In the input grid, there is a left-right symmetric monochromatic object occluded by a colored rectangle.
# The goal is to remove the colored rectangle and extend the symmetric object's leftmost and rightmost points to the left and right edges of the grid respectively, maintaining its symmetry.

def main(input_grid):
    # Plan:
    # 1. Detect the symmetric object and the occluding rectangle.
    # 2. Remove the rectangle.
    # 3. Extend the object's left and right extremities horizontally to the edges of the grid while maintaining its symmetry.

    background_color = Color.BLACK

    # Detect objects in the input grid
    objects = detect_objects(input_grid, monochromatic=True, connectivity=8, background=background_color)
    cropped_objects = [crop(obj, background=background_color) for obj in objects]

    # Identify the occluding rectangle
    for obj, cropped in zip(objects, cropped_objects):
        if np.count_nonzero(cropped) == cropped.size:
            rectangle = obj
            break
    
    # Find the color of the rectangle (it's a single color block)
    rectangle_color = np.unique(crop(rectangle))[0]

    # Remove the rectangle from the grid
    output_grid = input_grid.copy()
    rectangle_mask = rectangle != background_color
    output_grid[rectangle_mask] = background_color

    # Detect the main object after rectangle removal
    objects_after_removal = detect_objects(output_grid, monochromatic=True, connectivity=8, background=background_color)
    for obj in objects_after_removal:
        if np.any(obj != background_color):
            symmetric_object = obj
            break

    # Extend the object horizontally maintaining its symmetry
    symmetric_x, symmetric_y, symmetric_w, symmetric_h = bounding_box(symmetric_object)
    for i in range(symmetric_y, symmetric_y + symmetric_h):
        left_extreme = symmetric_x
        right_extreme = symmetric_x + symmetric_w - 1
        while left_extreme > 0:
            left_extreme -= 1
            output_grid[left_extreme, i] = output_grid[symmetric_x, i]
        while right_extreme < output_grid.shape[1] - 1:
            right_extreme += 1
            output_grid[right_extreme, i] = output_grid[symmetric_x + symmetric_w - 1, i]

    return output_grid

def generate_input():
    # Generate a grid of random size
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    object_color, rectangle_color = random.sample(list(Color.NOT_BLACK), 2)

    # Create a symmetric object
    symmetric_object = random_sprite(
        np.random.randint(4, n-2), np.random.randint(2, m//2),
        symmetry="horizontal", color_palette=[object_color]
    )

    # Place the symmetric object in the grid
    object_x, object_y = random_free_location_for_sprite(grid, symmetric_object, border_size=1)
    blit_sprite(grid, symmetric_object, x=object_x, y=object_y)

    # Create the occluding rectangle
    rectangle = np.full((np.random.randint(2, 5), np.random.randint(2, 5)), rectangle_color)

    # Find an occlusion location that overlaps with the object
    while True:
        rectangle_x, rectangle_y = np.random.randint(0, n - rectangle.shape[0]), np.random.randint(0, m - rectangle.shape[1])
        if collision(object1=grid, object2=rectangle, x2=rectangle_x, y2=rectangle_y, background=Color.BLACK):
            break
    blit_sprite(grid, rectangle, x=rectangle_x, y=rectangle_y, background=Color.BLACK)

    return grid