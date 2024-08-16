import numpy as np
from typing import *
from common import *

# concepts:
# symmetry detection, shape mirroring

# description:
# In the input grid, you will find a randomly positioned non-symmetrical 2D shape on the left half of the grid. 
# The task is to detect the boundaries of the shape and mirror it horizontally over a central vertical axis, placing the mirrored version on the right side of the grid.
# The output grid should show the shape in its original position on the left and its mirrored version on the right.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the bounding box of the non-background pixels on the left half of the grid
    n, m = input_grid.shape
    left_half = input_grid[:, :m//2]
    bbox = bounding_box(left_half, background=Color.BLACK)
    
    x, y, w, h = bbox
    # Extract the original shape
    shape = input_grid[x:x+w, y:y+h].copy()

    # Create the mirrored shape
    mirrored_shape = np.fliplr(shape)

    # Place the original shape back on the output grid
    output_grid = np.full_like(input_grid, Color.BLACK)
    output_grid[x:x+w, y:y+h] = shape
    
    # Place the mirrored shape on the right side of the grid
    mirrored_y = m - y - h
    output_grid[x:x+w, mirrored_y:mirrored_y+h] = mirrored_shape
    
    return output_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    
    # Generate a random shape with random colors on the left half of the grid
    shape_width, shape_height = np.random.randint(2, m//2), np.random.randint(2, n//2)
    shape = random_sprite(shape_width, shape_height, color_palette=Color.NOT_BLACK, symmetry='not_symmetric')
    
    # Place the shape on the left half of the grid
    x, y = np.random.randint(0, n - shape_height), np.random.randint(0, m//2 - shape_width)
    blit(grid, shape, x, y, background=Color.BLACK)
    
    return grid