from common import *

import numpy as np
from typing import *

# concepts:
# symmetry detection, counting

# description:
# In the input, there will be multiple colored pixels arranged in shapes that are symmetric across the vertical axis.
# The output should align each shape to the leftmost column of the output grid with each shape aligned at the top,
# and the length of the output grid will be the count of shapes.

def main(input_grid):
    # Detect vertical symmetry axes
    shapes = []
    visited = set()

    # Detect shapes by finding unique pixels and leveraging the symmetry
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] != Color.BLACK and (x, y) not in visited:
                # Identify the shape
                pixels = []
                stack = [(x, y)]

                while stack:
                    px, py = stack.pop()
                    if (px, py) not in visited and input_grid[px, py] != Color.BLACK:
                        visited.add((px, py))
                        pixels.append((px, py))
                        # Add neighbors
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = px + dx, py + dy
                            if 0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1] and (nx, ny) not in visited:
                                stack.append((nx, ny))

                shapes.append(pixels)

    # Create the output grid
    output_height = 10 * len(shapes)
    output_width = 10  # Arbitrary width to have enough space for shapes
    output_grid = np.full((output_height, output_width), Color.BLACK, dtype=int)

    # Align each shape with the leftmost column
    current_y = 0
    for shape_pixels in shapes:
        shape = np.full((len(shape_pixels), len(shape_pixels)), Color.BLACK, dtype=int)
        offset_x = min(px for px, py in shape_pixels)
        offset_y = min(py for px, py in shape_pixels)

        for px, py in shape_pixels:
            shape[px - offset_x, py - offset_y] = input_grid[px, py]

        sprite = crop(shape)
        new_y = current_y
        x, y = 0, new_y
        blit_sprite(output_grid, sprite, x, y)
        current_y += sprite.shape[0]

    return output_grid

def generate_input():
    # Initialize a large grid
    grid_size = 20
    grid = np.full((grid_size, grid_size), Color.BLACK, dtype=int)

    # Place multiple random symmetric sprites
    num_shapes = np.random.randint(2, 5)
    shape_size = np.random.randint(3, 6)
    
    for _ in range(num_shapes):
        color = np.random.choice(Color.NOT_BLACK)
        sprite = random_sprite(shape_size, shape_size, symmetry="vertical", color_palette=[color])
        
        x, y = random_free_location_for_sprite(grid, sprite)
        
        # Ensure the sprite supports vertical symmetry
        blit_sprite(grid, sprite, x, y)
    
    return grid