from common import *

import numpy as np
from typing import *

# concepts:
# color mapping, rotational symmetry

# description:
# The input is a grid with a rotationally symmetric pattern of colored pixels.
# To make the output, apply the following color mapping:
# 1. Find the center of rotational symmetry.
# 2. For each pixel, calculate its distance from the center.
# 3. If the distance is even, shift the color one step forward in the sequence:
#    red -> blue -> green -> yellow -> orange -> pink -> teal -> red
# 4. If the distance is odd, shift the color one step backward in the sequence.
# 5. Black pixels remain black and are not part of the sequence.

def main(input_grid):
    # Initialize output grid
    output_grid = input_grid.copy()

    # Define color sequence
    color_sequence = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, 
                      Color.ORANGE, Color.PINK, Color.TEAL]

    # Find center of rotational symmetry
    h, w = input_grid.shape
    center_y, center_x = h // 2, w // 2

    # Apply color mapping
    for y in range(h):
        for x in range(w):
            if input_grid[y, x] != Color.BLACK:
                # Calculate distance from center
                distance = int(np.sqrt((y - center_y)**2 + (x - center_x)**2))
                
                # Find current color index in sequence
                current_index = color_sequence.index(input_grid[y, x])
                
                # Shift color based on distance
                if distance % 2 == 0:
                    new_index = (current_index + 1) % len(color_sequence)
                else:
                    new_index = (current_index - 1) % len(color_sequence)
                
                # Apply new color
                output_grid[y, x] = color_sequence[new_index]

    return output_grid

def generate_input():
    # Generate a square grid
    size = random.randint(7, 15)
    grid = np.full((size, size), Color.BLACK)

    # Define color sequence
    color_sequence = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, 
                      Color.ORANGE, Color.PINK, Color.TEAL]

    # Create a rotationally symmetric pattern
    center = size // 2
    max_radius = min(center, size - center - 1)
    
    for r in range(max_radius + 1):
        color = random.choice(color_sequence)
        for angle in range(0, 360, 45):  # 8-fold symmetry
            x = int(center + r * np.cos(np.radians(angle)))
            y = int(center + r * np.sin(np.radians(angle)))
            grid[y, x] = color

    return grid