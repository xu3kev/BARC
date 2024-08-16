from common import *

import numpy as np
from typing import *

# concepts:
# patterns, pixel manipulation, objects, connecting same color

# description:
# In the input grid, you will see a small multicolor object and several large colored rectangles.
# To make the output:
# 1. Identify and remove the small multicolor object from the grid.
# 2. Place a copy of the small object inside each rectangle.
# 3. Extend the multicolor object until it touches the edges of the rectangle with the corresponding colors.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Identify the background color
    background_color = np.argmax(np.bincount(input_grid.flatten()))

    # Step 1: Find and remove the small multicolor object
    input_grid[input_grid == background_color] = Color.BLACK
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)
    smallest_object = min(objects, key=lambda x: np.count_nonzero(x))
    input_grid[smallest_object != Color.BLACK] = Color.BLACK
    small_object_sprite = crop(smallest_object)

    # Step 2: Identify the large colored rectangles
    output_grid = np.copy(input_grid)
    rectangles = find_connected_components(input_grid, background=Color.BLACK, connectivity=8)
    for rectangle in rectangles:
        if np.count_nonzero(rectangle) < (min(input_grid.shape) // 2) ** 2:
            continue

        # Find the bounding box of the rectangle
        x, y, w, h = bounding_box(rectangle, background=Color.BLACK)

        # Step 3: Place the small object inside the rectangle
        center_x, center_y = x + w // 2, y + h // 2
        blit_sprite(output_grid, small_object_sprite, center_x - small_object_sprite.shape[0] // 2, center_y - small_object_sprite.shape[1] // 2, background=Color.BLACK)

        # Extend the small object to the edges of the rectangle
        for i in range(small_object_sprite.shape[0]):
            for j in range(small_object_sprite.shape[1]):
                if small_object_sprite[i, j] != Color.BLACK:
                    extend_color(output_grid, x, y, w, h, center_x - small_object_sprite.shape[0] // 2 + i, center_y - small_object_sprite.shape[1] // 2 + j)

    output_grid[output_grid == Color.BLACK] = background_color
    return output_grid

def extend_color(grid, x, y, w, h, obj_x, obj_y):
    color = grid[obj_x, obj_y]
    draw_line(grid, obj_x, y, length=(obj_y - y + 1), color=color, direction=(0, -1), stop_at_color=[Color.BLACK])
    draw_line(grid, obj_x, y + h - 1, length=(y + h - obj_y), color=color, direction=(0, 1), stop_at_color=[Color.BLACK])
    draw_line(grid, x, obj_y, length=(obj_x - x + 1), color=color, direction=(-1, 0), stop_at_color=[Color.BLACK])
    draw_line(grid, x + w - 1, obj_y, length=(x + w - obj_x), color=color, direction=(1, 0), stop_at_color=[Color.BLACK])

def generate_input() -> np.ndarray:
    # Set up the grid size and background color
    n, m = np.random.randint(18, 24), np.random.randint(18, 24)
    grid = np.full((n, m), Color.BLACK)

    # Choose colors for the rectangles and the small object
    background_color = random.choice(Color.NOT_BLACK)
    rectangle_color = random.choice([color for color in Color.NOT_BLACK if color != background_color])
    small_object_colors = [color for color in Color.NOT_BLACK if color != background_color and color != rectangle_color]

    # Create and place the small multicolor object
    small_object = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), color_palette=small_object_colors)
    small_object = crop(small_object)
    small_object_pos_x, small_object_pos_y = random_free_location_for_sprite(grid, small_object, padding=1)
    blit_sprite(grid, small_object, small_object_pos_x, small_object_pos_y, background=Color.BLACK)

    # Create and place large colored rectangles with some random color pixels inside them
    num_rectangles = random.randint(1, 3)
    for _ in range(num_rectangles):
        rect_width, rect_height = random.randint(n//3, 2*n//3), random.randint(m//3, 2*m//3)
        rectangle = np.full((rect_width, rect_height), rectangle_color)
        for _ in range(random.randint(2, 4)):
            rx, ry = random.randint(1, rect_width-2), random.randint(1, rect_height-2)
            rectangle[rx, ry] = random.choice(small_object_colors)
        rect_x, rect_y = random_free_location_for_sprite(grid, rectangle, padding=1)
        blit_sprite(grid, rectangle, rect_x, rect_y)

    # Change back the background color
    grid[grid == Color.BLACK] = background_color
    return grid