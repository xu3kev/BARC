from common import *

import numpy as np
from typing import *

# concepts:
# alignment, copy to object border

# description:
# In the input you will see a teal object on a black background, several color pixels are placed on the border of black background.
# To make the output grid, you should copy the color pixels to the border of the teal object either vertically or horizontally.

def main(input_grid):
    # Detects the rectangle in the input grid that are of the color TEAL,
    teal_objects = detect_objects(grid=input_grid, colors=[Color.TEAL], monochromatic=True, connectivity=4)
    
    # There should only be one rectangle of the color TEAL has been detected in the grid.
    assert len(teal_objects) == 1
    teal_object = teal_objects[0]
    
    # Get the size and coordinates of the TEAL rectangle.
    x_grid, y_grid, width, height = bounding_box(teal_object)

    # color pixels are NOT black and NOT TEAL.
    color_except_teal = [c for c in Color.NOT_BLACK if c != Color.TEAL]
    
    # Detects all other color pixels in the grid 
    find_pixels = detect_objects(grid=input_grid, colors=color_except_teal, monochromatic=True, connectivity=4)

    # Copy the color pixels to the border of the teal object either vertically or horizontally.
    for pixel_grid in find_pixels:
        # Get the coordinates of the color pixel.
        x, y, _, _ = bounding_box(pixel_grid)
        
        # If the pixel is on the top row, move it to the top of the TEAL bounding box.
        if x == 0:
            input_grid[x_grid, y] = input_grid[x, y]
        # If the pixel is on the bottom row, move it to the bottom of the TEAL bounding box.
        elif x == input_grid.shape[0] - 1:
            input_grid[x_grid + width - 1, y] = input_grid[x, y]
        # If the pixel is on the leftmost column, move it to the left of the TEAL bounding box.
        elif y == 0:
            input_grid[x, y_grid] = input_grid[x, y]
        # If the pixel is on the rightmost column, move it to the right of the TEAL bounding box.
        elif y == input_grid.shape[1] - 1:
            input_grid[x, y_grid + height - 1] = input_grid[x, y]
    
    return input_grid


def generate_input():
    # Initialize a 10x10 grid representing a black background.
    n = m = 10
    grid = np.zeros((n, m), dtype=int)
    
    # Randomly determine the width and height of the TEAL rectangle between 2 and 5.
    width, height = np.random.randint(2, 6), np.random.randint(2, 6)
    
    # Randomly choose the position (x_grid, y_grid) where the TEAL sprite will be placed
    # within the grid, ensuring the sprite fits inside the grid's boundaries.
    x_grid, y_grid = np.random.randint(2, n - width - 1), np.random.randint(2, m - height - 1)
    
    # Generate the TEAL rectangle
    sprite = np.full((width, height), Color.TEAL)
    
    # Blit the sprite into the main grid at the randomly chosen location.
    blit_sprite(grid, sprite, x_grid, y_grid)

    # Initialize an empty list to hold the available positions, which are edges of the sprite), for placing non-TEAL color pixels.
    available_position = []
    
    # Add the top and bottom row positions along the width of the sprite to the available positions list.
    for i in range(width):
        available_position.append((i + x_grid, 0))         # Top row
        available_position.append((i + x_grid, n-1))       # Bottom row
    
    # Add the left and right column positions along the height of the sprite to the available positions list.
    for i in range(1, height - 1):
        available_position.append((n-1, i + y_grid))       # Right column
        available_position.append((0, i + y_grid))         # Left column

    # Randomly determine the number of positions to fill with colors, between one-third and two-thirds of the available positions.
    color_num = np.random.randint(len(available_position) // 3, len(available_position) * 2 // 3 + 1)
    
    # Limit the number of colors to at most 8 to ensure the density of color pixels is reasonable.
    density = min(color_num, 8)
    
    # Randomly select `density` positions from the available positions list.
    random_position = random.sample(available_position, density)
    
    # Generate a list of color pixels with different colors except TEAL.
    color_except_teal = [c for c in Color.NOT_BLACK if c != Color.TEAL]
    random_color = random.sample(color_except_teal, density)

    # Assign the color pixels to the boarder of the main grid.
    for cnt, (x, y) in enumerate(random_position):
        grid[x, y] = random_color[cnt]

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
