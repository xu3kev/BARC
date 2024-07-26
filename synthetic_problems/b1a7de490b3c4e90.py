from common import *

import numpy as np
from typing import *

# concepts:
# cropping, collision detection

# description:
# In the input you will see several small colored shapes scattered across a black background.
# Create an output grid by cropping each individual shape and arranging the cropped shapes into a single row.
# Each shape in the output should be separated horizontally by one black pixel.


def main(input_grid: np.ndarray) -> np.ndarray:
    # Find all the colored shapes
    shapes = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=False)
    
    # Crop each shape separately
    cropped_shapes = [crop(shape, background=Color.BLACK) for shape in shapes]
    
    # Find maximum height for the output grid
    max_height = max(shape.shape[0] for shape in cropped_shapes)
    total_width = sum(shape.shape[1] for shape in cropped_shapes) + len(cropped_shapes) - 1
    
    # Prepare the output grid
    output_grid = np.zeros((max_height, total_width), dtype=int)
    
    # Arrange the cropped shapes in a single row
    current_x = 0
    for shape in cropped_shapes:
        blit_sprite(output_grid, shape, x=0, y=current_x, background=Color.BLACK)
        current_x += shape.shape[1] + 1  # Move current_x to the next position with a gap of 1 black pixel
    
    return output_grid


def generate_input() -> np.ndarray:
    # Create a randomly sized grid
    n = np.random.randint(15, 20)
    m = np.random.randint(15, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # Add a few small random shapes
    for _ in range(np.random.randint(3, 6)):
        w = np.random.randint(2, 5)
        h = np.random.randint(2, 5)
        sprite = random_sprite(w, h, color_palette=[np.random.choice(Color.NOT_BLACK)])
        
        x, y = random_free_location_for_sprite(grid, sprite)
        blit_sprite(grid, sprite, x, y)
    
    return grid