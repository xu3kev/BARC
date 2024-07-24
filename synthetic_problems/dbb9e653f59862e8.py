from common import *

import numpy as np
from typing import *

def main(input_grid: np.ndarray) -> np.ndarray:
    # Extracting objects from the grid
    objects = detect_objects(input_grid, monochromatic=True, connectivity=8, background=Color.BLACK)
    
    # Separate the rectangle from the symmetric object
    sym_object = None
    rectangle = None
    for obj in objects:
        obj_cropped = crop(obj, background=Color.BLACK)
        if obj_cropped.shape[0] * obj_cropped.shape[1] == np.sum(obj != Color.BLACK):
            # A fully filled object is the rectangle
            rectangle = obj
        else:
            # The remaining object is our symmetric object
            sym_object = obj
    
    if sym_object is None or rectangle is None:
        raise ValueError("Input grid does not contain the required objects")

    rectangle_color = np.unique(crop(rectangle))[0]
    
    # Removing the rectangle from the grid
    rectangle_mask = rectangle != Color.BLACK
    working_grid = input_grid.copy()
    working_grid[rectangle_mask] = Color.BLACK

    # Detect symmetry regarding the object ignoring the rectangle
    mirrors = detect_mirror_symmetry(working_grid, ignore_colors=[rectangle_color])
    
    # Apply symmetry to fill the missing parts
    output_grid = working_grid.copy()
    for x, y in np.argwhere(working_grid == sym_object[sym_object != Color.BLACK][0]):
        for mirror in mirrors:
            nx, ny = mirror.apply(x, y)
            if working_grid[nx, ny] == Color.BLACK:
                output_grid[nx, ny] = working_grid[x, y]
    
    return output_grid

def generate_input() -> np.ndarray:
    # Create a grid
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    obj_color, rect_color = random.sample(list(Color.NOT_BLACK), 2)
    
    # Create a symmetric object
    sprite_w, sprite_h = np.random.randint(5, n-2), np.random.randint(5, m-2)
    sprite = random_sprite(sprite_w, sprite_h, density=0.5, symmetry='horizontal', color_palette=[obj_color])
    spr_x, spr_y = random_free_location_for_sprite(grid, sprite, border_size=1, padding=1)

    blit_sprite(grid, sprite, spr_x, spr_y)

    # Create the rectangle
    rect_w, rect_h = np.random.randint(2, 5), np.random.randint(2, 5)
    rect = np.full((rect_w, rect_h), rect_color)

    # Place the rectangle over or near the symmetric object ensuring overlap
    while True:
        rect_x, rect_y = np.random.randint(0, n - rect_w), np.random.randint(0, m - rect_h)
        if collision(object1=grid, object2=rect, x2=rect_x, y2=rect_y, background=Color.BLACK):
            break
    blit_sprite(grid, rect, rect_x, rect_y, background=Color.BLACK)

    return grid

# Sample run of the functions