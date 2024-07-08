from common import *

import numpy as np
from typing import *

# concepts:
# repulsion, sliding objects, direction

# description:
# In the input, you will see randomly positioned colored squares (size 2x2). They will be repelling each other.
# The goal is to move each square away from the center of the grid.
# If two squares would overlap during the move, they push each other further away till they stop overlapping.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # Detect all squares
    squares = detect_objects(input_grid, allowed_dimensions=[(2, 2)], colors=Color.NOT_BLACK, can_overlap=False)
    center_x, center_y = np.array(input_grid.shape) // 2

    for square in squares:
        # Get the bounding box and center of the square
        x, y, w, h = bounding_box(square)
        square_center_x, square_center_y = x + w // 2, y + h // 2
        
        # Determine the direction to move: vector from the grid center to the square center
        dx, dy = np.sign([square_center_x - center_x, square_center_y - center_y])
        
        # Initial position
        pos_x, pos_y = x, y
        
        while True:
            # Translate the square
            translated_square = translate(square, dx, dy)
            translated_x, translated_y = x + dx, y + dy
            
            # Check if the translated square has left the grid or overlaps any other object
            if (translated_x < 0 or translated_x + w > input_grid.shape[0] or
                translated_y < 0 or translated_y + h > input_grid.shape[1] or
                any(collision(object1=translated_square, object2=s, background=Color.BLACK) for s in squares if not np.array_equal(s, square))):
                break

            pos_x, pos_y = translated_x, translated_y
            dx += np.sign(dx)
            dy += np.sign(dy)
        
        # Place the square at the new position
        blit(output_grid, square, pos_x, pos_y, background=Color.BLACK)
    
    return output_grid

def generate_input():
    # Make a black grid first as background, roughly 10x10 to 16x16 size.
    n, m = np.random.randint(10, 16, size=2)
    grid = np.full((n, m), Color.BLACK)

    # Define the number of squares and their colors
    num_squares = np.random.randint(2, 6)
    colors = random.sample(list(Color.NOT_BLACK), num_squares)

    for color in colors:
        # Create a 2x2 square of the chosen color
        square = np.full((2, 2), color)
        
        # Randomly position the square on the grid
        x, y = random_free_location_for_object(grid, square, background=Color.BLACK, padding=1)
        blit(grid, square, x, y, background=Color.BLACK)

    return grid