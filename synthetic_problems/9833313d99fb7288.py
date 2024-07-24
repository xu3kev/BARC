from common import *

import numpy as np
from typing import *

# concepts:
# topology, color mapping

# description:
# The input is a grid with various enclosed regions of different colors on a black background.
# The task for the user is to find these enclosed regions and change their colors based on the following mapping:
# BLUE -> RED, GREEN -> YELLOW, MAROON -> ORANGE, TEAL -> PINK

color_map = {
    Color.BLUE: Color.RED,
    Color.GREEN: Color.YELLOW,
    Color.MAROON: Color.ORANGE,
    Color.TEAL: Color.PINK
}

def main(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = input_grid.copy()

    # Find all colored components in the grid
    components = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=True)

    for component in components:
        # Get the color of the current component
        component_color = next(iter(set(component.flatten()) - {Color.BLACK}))

        if component_color in color_map:
            # Map the current color to the target color
            target_color = color_map[component_color]

            # Get the bounding box of the component
            x, y, w, h = bounding_box(component, background=Color.BLACK)

            # Replace the color within the bounding box
            for i in range(x, x + w):
                for j in range(y, y + h):
                    if input_grid[i, j] == component_color:
                        output_grid[i, j] = target_color

    return output_grid

def generate_input():
    # Generate a grid of arbitrary size within given limits
    n = np.random.randint(10, 20)
    m = np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)

    # Predefined palette of colors (must match the keys of the color_map)
    palette = [Color.BLUE, Color.GREEN, Color.MAROON, Color.TEAL]

    # Generate some random colored sprites, then hollow out their interior to form enclosed areas
    for _ in range(np.random.randint(1, 5)):
        p_color = np.random.choice(palette)
        sprite_width = np.random.randint(4, 8)
        sprite_height = np.random.randint(4, 8)
        sprite = random_sprite(sprite_width, sprite_height, density=1, color_palette=[p_color], connectivity=8)
        
        # Optional hollowing to ensure closed regions
        interior_mask = object_interior(sprite, background=Color.BLACK)
        boundary_mask = object_boundary(sprite, background=Color.BLACK)
        hollowed_area = interior_mask & ~boundary_mask
        sprite[hollowed_area] = Color.BLACK

        # Find a random free location to place the sprite
        try:
            x, y = random_free_location_for_sprite(grid, sprite, border_size=1)
        except:
            continue

        blit_sprite(grid, sprite, x, y, background=Color.BLACK)

    return grid