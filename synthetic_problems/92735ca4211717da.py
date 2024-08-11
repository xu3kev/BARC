from common import *

import numpy as np
from typing import *

# concepts:
# occlusion, counting, translational symmetry

# description:
# In the input grid, there is a translationally symmetric pattern and an occluding rectangular region of black pixels.
# Count the number of colored pixels from the pattern inside the occluded region and replace each black pixel with a color representing the count: 1=Green, 2=Red, 3=Blue, etc.

def main(input_grid):
    # Identify the translational symmetries
    translations = detect_translational_symmetry(input_grid, ignore_colors=[Color.BLACK])
    assert len(translations) > 0, "No translational symmetry found"

    w, h = input_grid.shape
    output_grid = np.copy(input_grid)

    # Find the occluded region
    occluders = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    occluder = max(occluders, key=lambda o: np.count_nonzero(o))

    # Find the bounding box of the occluded region
    min_x, min_y = np.min(occluder.nonzero(), axis=1)
    max_x, max_y = np.max(occluder.nonzero(), axis=1)

    # Count the number of colored pixels inside the occluded region
    pixel_count = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if input_grid[x, y] != Color.BLACK:
                pixel_count += 1

    # Set the color based on the number of counted pixels
    if pixel_count == 1:
        fill_color = Color.GREEN
    elif pixel_count == 2:
        fill_color = Color.RED
    elif pixel_count == 3:
        fill_color = Color.BLUE
    else:
        fill_color = Color.GREY

    # Replace each black pixel in the occluded region with the fill color
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if input_grid[x, y] == Color.BLACK:
                output_grid[x, y] = fill_color

    return output_grid 

def generate_input():
    # Create a random canvas size between 15x15 and 20x20
    grid = np.full((np.random.randint(15, 21), np.random.randint(15, 21)), Color.BLACK)

    # Make the basic repeating pattern (sprite)
    w, h = random.randint(3, 5), random.randint(3, 5)
    pattern = random_sprite(w, h, density=1, color_palette=Color.NOT_BLACK)

    # Place the sprite in the canvas repeated in a grid
    for x in range(0, grid.shape[0], w):
        for y in range(0, grid.shape[1], h):
            blit_sprite(grid, pattern, x, y)

    # Create one large occluding (black) rectangle in the grid
    x, y = random.randint(0, grid.shape[0] - w), random.randint(0, grid.shape[1] - h)
    occluder_width, occluder_height = random.randint(w, grid.shape[0] - x), random.randint(h, grid.shape[1] - y)
    grid[x:x + occluder_width, y:y + occluder_height] = Color.BLACK

    return grid