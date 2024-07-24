from common import *

import numpy as np
from typing import *

# concepts:
# patterns, masking, objects, color guide, connectivity, expanding

# description:
# In the input you will see 30x30 grid with multiple squares of different sizes.
# Inside each square, there will be at least one pixel of a random color that is not black.
# Your task is to identify the unique colors and expand each of these colored pixels vertically and horizontally 
# until it reaches the boundary of the square while staying within the square. Return the resulting grid.

def main(input_grid):
    # Copy the input to an output grid
    output_grid = np.copy(input_grid)
    
    # Find all objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    
    # Filter objects larger than 1x1 (to ensure they are squares)
    squares = [crop(obj, background=Color.BLACK) for obj in objects if obj.shape[0] > 1 and obj.shape[1] > 1]
    
    for square in squares:
        # Get the bounding box of the square
        x, y, width, height = bounding_box(square)
        
        # Identify the unique colors inside the square excluding the background color
        colors, counts = np.unique(square[square != Color.BLACK], return_counts=True)
        
        # Expand each unique color horizontally and vertically within the square until they hit the boundary
        for color in colors:
            coords = np.argwhere(square == color)
            for xx, yy in coords:
                # Expand vertically
                for i in range(xx, width):
                    if square[i, yy] == Color.BLACK:
                        square[i, yy] = color
                    else:
                        break
                for i in range(xx, -1, -1):
                    if square[i, yy] == Color.BLACK:
                        square[i, yy] = color
                    else:
                        break
                
                # Expand horizontally
                for j in range(yy, height):
                    if square[xx, j] == Color.BLACK:
                        square[xx, j] = color
                    else:
                        break
                for j in range(yy, -1, -1):
                    if square[xx, j] == Color.BLACK:
                        square[xx, j] = color
                    else:
                        break
        
        # Blit the modified square back to the output grid
        blit_sprite(output_grid, square, x, y, background=Color.BLACK)
    
    return output_grid


def generate_input():
    # Create an empty 30x30 grid
    input_grid = np.full((30, 30), Color.BLACK, dtype=int)

    num_squares = np.random.randint(3, 6)

    for _ in range(num_squares):
        # Define square size and position
        width = height = np.random.randint(5, 11)
        square = np.full((width, height), Color.BLACK, dtype=int)
        
        # Place at least one colored pixel within the square
        num_colored_pixels = np.random.randint(1, 4)
        for _ in range(num_colored_pixels):
            color = np.random.choice(list(Color.NOT_BLACK))
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            square[x, y] = color
        
        # Find a free position in the input grid to place the square
        x, y = random_free_location_for_sprite(input_grid, square, border_size=1)
        blit_sprite(input_grid, square, x, y, background=Color.BLACK)
    
    return input_grid