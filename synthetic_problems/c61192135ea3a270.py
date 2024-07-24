from common import *

import numpy as np
from typing import *

def main(input_grid: np.ndarray) -> np.ndarray:
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    
    # Separate blue squares, red squares, and dots
    blue_squares = [obj for obj in objects if np.all(obj == Color.BLUE)]
    red_squares = [obj for obj in objects if np.all(obj == Color.RED) and obj.shape == (2, 2)]
    dots = [obj for obj in objects if (obj.shape == (1, 1)) and (np.any(obj == Color.RED) or np.any(obj == Color.BLUE))]

    slide_count = 0
    output_grid = np.copy(input_grid)

    for blue_square in blue_squares:
        for red_square in red_squares:
            while True:
                new_red_square = translate(red_square, x=0, y=1, background=Color.BLACK)
                if contact(object1=new_red_square, object2=blue_square) or np.any(new_red_square == background):
                    break
                blit_object(output_grid, new_red_square, background=Color.BLACK)
                slide_count += 1

    # Count the slides and display vertically on the right edge of the grid
    n = output_grid.shape[0]
    output_grid[-slide_count:, -1] = Color.RED

    return output_grid


def generate_input() -> np.ndarray:
    n = m = 9
    grid = np.zeros((n, m), dtype=int)

    blue_square = np.full((2, 2), Color.BLUE, dtype=int)
    for _ in range(np.random.randint(2, 6)):
        x, y = random_free_location_for_sprite(grid, blue_square)
        if not contact(object1=grid, object2=blue_square, x2=x, y2=y): 
            blit_sprite(grid, blue_square, x, y)
    
    red_square = np.full((2, 2), Color.RED, dtype=int)
    for _ in range(np.random.randint(2, 6)):
        x, y = random_free_location_for_sprite(grid, red_square)
        if not contact(object1=grid, object2=red_square, x2=x, y2=y): 
            blit_sprite(grid, red_square, x, y)
        
    blue_pixel = np.full((1, 1), Color.BLUE, dtype=int)
    for _ in range(np.random.randint(4)):
        x, y = random_free_location_for_sprite(grid, blue_pixel)
        blit_sprite(grid, blue_pixel, x, y)

    red_pixel = np.full((1, 1), Color.RED, dtype=int)
    for _ in range(np.random.randint(4)):
        x, y = random_free_location_for_sprite(grid, red_pixel)
        blit_sprite(grid, red_pixel, x, y)

    return grid