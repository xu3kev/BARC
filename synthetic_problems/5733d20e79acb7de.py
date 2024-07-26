from common import *

import numpy as np
from typing import *

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros((10, 10), dtype=int) # create a blank 10x10 grid
    
    # extract the 2x2 objects from the input
    objects = detect_objects(input_grid, background=Color.BLACK, allowed_dimensions=[(2, 2)], monochromatic=False)

    for obj in objects:
        color = obj[0,0] # assuming all 2x2 objects are monochromatic
        x, y = np.argwhere(input_grid == color)[0]
        
        # slide each object to the bottom-right corner of a 2x2 cell
        new_obj = np.zeros((2, 2), dtype=int)
        new_obj[1, 1] = color
        new_obj[1, 0] = color
        new_obj[0, 1] = color
        new_obj[0, 0] = color

        # find location for new 2x2 object
        cell_x, cell_y = x//2, y//2
        start_x, start_y = (2 * cell_x)+5, (2 * cell_y)+5

        blit_sprite(output_grid, new_obj, start_x, start_y)

    return output_grid




def generate_input() -> np.ndarray:
    grid = np.zeros((5, 5), dtype=int)
    color_palette = list(Color.NOT_BLACK)

    num_objects = np.random.randint(3, 5)

    for _ in range(num_objects):
        color = np.random.choice(color_palette)
        x, y = np.random.choice(range(0, 4)), np.random.choice(range(0, 4))
        object_2x2 = np.array([[color, color], [color, color]])
        blit_sprite(grid, object_2x2, x, y)
    
    return grid