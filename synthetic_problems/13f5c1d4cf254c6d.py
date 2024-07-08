from common import *

import numpy as np
from typing import *

# concepts:
# objects, rotational symmetry, spatial analysis, color matching

# description:
# In the input grid, you will find different groups of colored pixels distributed across the grid. 
# Each group represents an object. Among these groups, some objects may exhibit rotational symmetry. 
# Identify these symmetric objects, and fill the interior of the largest symmetric object with the most prevalent color within that object. 
# Return the resulting grid as the output.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Extract objects from the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    max_size = 0
    largest_object = None
    most_prevalent_color = None

    for obj in objects:
        # Detect rotational symmetry of the object
        symmetry = detect_rotational_symmetry(obj, ignore_colors=[Color.BLACK])
        if symmetry:
            # Calculate the internal area of the object
            interior = object_interior(obj, background=Color.BLACK)
            size = np.sum(interior)

            if size > max_size:
                max_size = size
                largest_object = obj
                # Determine the most prevalent color within the object
                colors, counts = np.unique(obj[obj != Color.BLACK], return_counts=True)
                most_prevalent_color = colors[np.argmax(counts)]

    if largest_object is not None:
        # Fill the interior of the largest symmetric object with the most prevalent color
        interior = object_interior(largest_object, background=Color.BLACK)
        largest_object[interior] = most_prevalent_color

        # Find the bounding box of the largest object
        x, y, width, height = bounding_box(largest_object)
        output_grid = input_grid.copy()
        output_grid[x:x+width, y:y+height] = largest_object[x:x+width, y:y+height]

        return output_grid

    return input_grid

def generate_input() -> np.ndarray:
    # Generate a grid with random objects
    grid_size = random.randint(10, 20)
    grid = np.zeros((grid_size, grid_size), dtype=int)

    # Create random objects with potential rotational symmetry
    num_objects = random.randint(3, 5)
    for _ in range(num_objects):
        color_palette = list(Color.NOT_BLACK)
        np.random.shuffle(color_palette)
        color = color_palette[0]

        # Randomly create either symmetric or non-symmetric objects
        choice = random.choice(["symmetric", "non_symmetric"])
        if choice == "symmetric":
            obj = random_sprite(grid_size // 2, grid_size // 2, color_palette=[color], symmetry='radial', connectivity=8)
        else:
            obj = random_sprite(grid_size // 2, grid_size // 2, color_palette=[color], symmetry='not_symmetric', connectivity=8)

        try:
            x, y = random_free_location_for_object(grid, obj, border_size=1, padding=1)
        except:
            continue
        
        blit(grid, obj, x, y, background=Color.BLACK)

    return grid