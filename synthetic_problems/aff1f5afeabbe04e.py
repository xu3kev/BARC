from common import *

import numpy as np
from typing import *


def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the connected components in the input grid
    components = find_connected_components(input_grid, connectivity=8, monochromatic=True)

    # Initialize the output grid
    output_grid = np.zeros_like(input_grid)

    for component in components:
        # Find the boundary of the component
        boundary = object_boundary(component)
        
        # Find the interior of the component
        interior = object_interior(component)

        # For the boundary, flip the color to the second in a predefined list
        for (x, y) in np.argwhere(boundary):
            output_grid[x, y] = Color.RED  # Set to RED as the new boundary color
        
        # Copy the non-boundary interior to the output
        for (x, y) in np.argwhere(interior):
            if not boundary[x, y]:
                output_grid[x, y] = component[x, y]
    
    return output_grid


def generate_input() -> np.ndarray:
    # Define the grid size
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    
    # Generate a large object with random color
    color = np.random.choice(Color.NOT_BLACK)
    large_object = random_sprite(n // 2, m // 2, density=0.8, color_palette=[color])

    # Ensure the object is contiguous
    while not is_contiguous(large_object, connectivity=8):
        large_object = random_sprite(n // 2, m // 2, density=0.8, color_palette=[color])

    # Create an empty grid with padding to fit the object
    input_grid = np.zeros((n, m), dtype=int)
    
    # randomly place the large object without touching borders
    x, y = random_free_location_for_object(input_grid, large_object, padding=2)
    blit(input_grid, large_object, x, y)

    return input_grid