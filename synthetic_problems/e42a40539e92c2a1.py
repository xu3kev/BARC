from common import *
import numpy as np
from typing import *

# concepts:
# cropping, reflection, pixel manipulation

# description:
# In the input you will see a shape of a certain color placed on a black background in a 10x10 grid.
# To make the output, first crop the grid to the bounding box around the shape, then reflect the shape across the horizontal axis,
# and finally, concatenate the original cropped shape with the reflected shape vertically.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Crop the input grid to the bounding box around the non-black pixels
    cropped_grid = crop(input_grid, background=Color.BLACK)
    
    # Reflect the cropped grid across the horizontal axis
    reflected_grid = cropped_grid[::-1, :]
    
    # Concatenate the original cropped grid and the reflected grid vertically
    output_grid = np.vstack((cropped_grid, reflected_grid))
    
    return output_grid

def generate_input() -> np.ndarray:
    # Create a 10x10 grid with black background
    grid = np.full((10, 10), Color.BLACK, dtype=int)
    
    # Create a random shape with random size in the range [2, 6] x [2, 6]
    shape_height = np.random.randint(2, 7)
    shape_width = np.random.randint(2, 7)
    shape = random_sprite(shape_height, shape_width, density=1, color_palette=[np.random.choice(Color.NOT_BLACK)])
    
    # Place the shape at a random position in the grid
    x, y = random_free_location_for_sprite(grid, shape, border_size=1)
    blit_sprite(grid, shape, x, y)

    return grid