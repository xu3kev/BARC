import numpy as np
from typing import *
from common import *

# concepts:
# symmetry, color, connected components, sorting

# description:
# In the input you will see several objects of varying shapes and sizes. Each object is a single color or a combination of colors.
# One of these objects is symmetric (vertically, horizontally, diagonally, or radially) and contains multiple colors.
# The goal is to find this colorful symmetric object and return it.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the objects (connected components) in the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    # Crop out the objects to isolate them
    isolated_objects = [crop(obj) for obj in objects]

    # Function to check if an object is symmetric
    def is_symmetric(obj):
        if np.array_equal(obj, np.rot90(obj, 1)) or \
           np.array_equal(obj, np.fliplr(obj)) or \
           np.array_equal(obj, np.flipud(obj)) or \
           np.array_equal(obj, obj.T):
            return True
        return False

    # Find the symmetric objects and their color counts
    symmetric_objects = []
    for obj in isolated_objects:
        if is_symmetric(obj):
            num_colors = len(np.unique(obj[obj != Color.BLACK]))
            symmetric_objects.append((obj, num_colors))

    # Find the symmetric object with the maximum number of colors
    if not symmetric_objects:
        return np.array([])  # Return an empty array if no symmetric objects found

    max_color_object = max(symmetric_objects, key=lambda x: x[1])[0]

    return max_color_object

def generate_input() -> np.ndarray:
    # Make a black 10x10 grid as the background
    grid = np.zeros((10, 10), dtype=int)

    # Add the symmetric colorful sprite:
    colors = np.random.choice(list(Color.NOT_BLACK), size=4, replace=False).tolist()

    # Choose the symmetry and size of the sprite
    symmetry = np.random.choice(['vertical', 'horizontal', 'diagonal', 'radial'])
    side_length = np.random.randint(2, 5)
    
    symmetric_sprite = random_sprite(side_length, side_length, symmetry=symmetry, color_palette=colors, connectivity=8)

    # Place the sprite randomly on the grid
    x, y = random_free_location_for_sprite(grid, symmetric_sprite, padding=1)
    blit_sprite(grid, symmetric_sprite, x=x, y=y)

    # Add some non-symmetric sprites:
    for _ in range(np.random.randint(3, 6)):
        # Choose a color of the sprite
        color = np.random.choice(Color.NOT_BLACK)

        # Choose the side length of the sprite
        side_length = np.random.randint(2, 5)

        non_symmetric_sprite = random_sprite(side_length, side_length, symmetry="not_symmetric", color_palette=[color], connectivity=8)

        # Place the sprite randomly on the grid if there is space
        try:
            x, y = random_free_location_for_sprite(grid, non_symmetric_sprite, padding=1)
            blit_sprite(grid, non_symmetric_sprite, x=x, y=y)
        except:
            pass

    return grid