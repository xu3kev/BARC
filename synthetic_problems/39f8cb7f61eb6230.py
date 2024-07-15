from common import *

import numpy as np
from typing import *

# concepts:
# patterns, positioning, copying, color guide, rotation

# description:
# In the input, you will see four square patterns of pixels, one in each corner of the grid. Each pattern is made up of two colors: a background color and a foreground color. The background color is the same for all patterns, but the foreground color may vary.
# To create the output:
# 1. Determine the size of the output grid by adding 2 to the size of the largest pattern.
# 2. Copy each pattern to the corresponding corner of the output grid.
# 3. Rotate each pattern 90 degrees clockwise.
# 4. Change the foreground color of each pattern to match the foreground color of the pattern that was originally in the clockwise-next corner.

def main(input_grid):
    # Find the patterns
    background_color = input_grid[0, 0]  # Assuming the background color is in the top-left corner
    objects = find_connected_components(input_grid, background=background_color, connectivity=8, monochromatic=False)

    # Find the bounding box of each pattern
    bounding_boxes = [bounding_box(obj) for obj in objects]

    # Determine the size of the output grid
    pattern_size = max([max(bb[2], bb[3]) for bb in bounding_boxes])
    output_size = pattern_size + 2

    # Create the output grid
    output_grid = np.full((output_size, output_size), background_color)

    # Process each pattern
    corner_positions = [(0, 0), (0, output_size - pattern_size), (output_size - pattern_size, 0), (output_size - pattern_size, output_size - pattern_size)]
    foreground_colors = []

    for obj, (x, y, w, h) in zip(objects, bounding_boxes):
        # Determine the corner of the pattern
        if x < input_grid.shape[0] // 2:
            if y < input_grid.shape[1] // 2:
                corner = 0  # Top-left
            else:
                corner = 1  # Top-right
        else:
            if y < input_grid.shape[1] // 2:
                corner = 2  # Bottom-left
            else:
                corner = 3  # Bottom-right

        # Crop and rotate the pattern
        pattern = crop(obj, background=background_color)
        rotated_pattern = np.rot90(pattern, k=-1)  # Rotate 90 degrees clockwise

        # Find the foreground color
        foreground_color = next(color for color in np.unique(pattern) if color != background_color)
        foreground_colors.append(foreground_color)

        # Copy the rotated pattern to the output grid
        blit_sprite(output_grid, rotated_pattern, x=corner_positions[corner][0], y=corner_positions[corner][1], background=background_color)

    # Change the foreground colors
    for i, (x, y) in enumerate(corner_positions):
        next_color = foreground_colors[(i + 1) % 4]
        mask = (output_grid[x:x+pattern_size, y:y+pattern_size] != background_color)
        output_grid[x:x+pattern_size, y:y+pattern_size][mask] = next_color

    return output_grid

def generate_input():
    # Generate a random sized grid with a random background color
    n = np.random.randint(8, 12)
    m = np.random.randint(8, 12)
    background_color = np.random.choice(list(Color.ALL_COLORS))
    grid = np.full((n, m), background_color)

    # Select four different colors for the patterns (excluding the background color)
    pattern_colors = np.random.choice([c for c in Color.ALL_COLORS if c != background_color], size=4, replace=False)

    # Generate patterns for each corner
    pattern_size = np.random.randint(3, min(n, m) // 2)
    corners = [(0, 0), (0, m - pattern_size), (n - pattern_size, 0), (n - pattern_size, m - pattern_size)]

    for (x, y), color in zip(corners, pattern_colors):
        pattern = np.random.choice([background_color, color], size=(pattern_size, pattern_size))
        grid[x:x+pattern_size, y:y+pattern_size] = pattern

    return grid