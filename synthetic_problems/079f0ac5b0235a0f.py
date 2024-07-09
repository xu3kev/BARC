from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, sprites, color mapping

# description:
# The input contains a rotationally symmetric sprite made of blue pixels on a black background.
# 1. Detect the center of rotational symmetry.
# 2. For each blue pixel, calculate its distance from the center.
# 3. Map each blue pixel to a new color based on its distance from the center:
#    - Closest 25% of pixels: Red
#    - Next 25% of pixels: Green
#    - Next 25% of pixels: Yellow
#    - Farthest 25% of pixels: Pink
# The output should maintain rotational symmetry but with the new color mapping.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    # Detect rotational symmetry
    sym = detect_rotational_symmetry(input_grid, ignore_colors=[Color.BLACK])
    center_x, center_y = sym.center_x, sym.center_y
    
    # Find all blue pixels
    blue_pixels = np.argwhere(input_grid == Color.BLUE)
    
    # Calculate distances from center
    distances = np.sqrt((blue_pixels[:, 0] - center_x)**2 + (blue_pixels[:, 1] - center_y)**2)
    
    # Sort pixels by distance
    sorted_indices = np.argsort(distances)
    num_pixels = len(blue_pixels)
    
    # Define color mapping based on quartiles
    color_map = [
        (Color.RED, int(0.25 * num_pixels)),
        (Color.GREEN, int(0.5 * num_pixels)),
        (Color.YELLOW, int(0.75 * num_pixels)),
        (Color.PINK, num_pixels)
    ]
    
    # Apply color mapping
    current_index = 0
    for color, threshold in color_map:
        while current_index < threshold:
            x, y = blue_pixels[sorted_indices[current_index]]
            output_grid[x, y] = color
            current_index += 1
    
    return output_grid

def generate_input() -> np.ndarray:
    # Create a black grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.zeros((n, m), dtype=int)
    
    # Generate a rotationally symmetric blue sprite
    sprite_size = np.random.randint(10, min(n, m) - 2)
    sprite = random_sprite(sprite_size, sprite_size, symmetry='radial', color_palette=[Color.BLUE], density=0.3)
    
    # Place the sprite at a random location
    x, y = random_free_location_for_sprite(grid, sprite, border_size=1)
    blit_sprite(grid, sprite, x, y)
    
    return grid