from common import *

import numpy as np
from typing import *

# concepts:
# alignment, objects, growing, patterns

# description:
# In the input, you will see three different colored shapes (red, blue, and yellow) on a black background. 
# Each shape is the same, but they appear at different sizes and vertical positions.
# The output should show the shapes aligned vertically at their centers, and each shape should grow or shrink 
# to match the size of the largest shape while maintaining its aspect ratio.

def main(input_grid):
    # Find the three colored shapes
    colors = [Color.RED, Color.BLUE, Color.YELLOW]
    shapes = []
    for color in colors:
        shape = np.where(input_grid == color)
        shapes.append(shape)

    # Calculate the size and center of each shape
    shape_info = []
    for shape in shapes:
        min_x, max_x = np.min(shape[1]), np.max(shape[1])
        min_y, max_y = np.min(shape[0]), np.max(shape[0])
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2
        shape_info.append((width, height, center_x, center_y))

    # Find the largest shape
    max_width = max(info[0] for info in shape_info)
    max_height = max(info[1] for info in shape_info)

    # Calculate the vertical center of the output grid
    output_center_y = input_grid.shape[0] // 2

    # Create the output grid
    output_grid = np.full_like(input_grid, Color.BLACK)

    # Process each shape
    for i, (shape, color) in enumerate(zip(shapes, colors)):
        width, height, _, _ = shape_info[i]
        
        # Calculate scaling factors
        scale_x = max_width / width
        scale_y = max_height / height
        scale = min(scale_x, scale_y)  # Use the smaller scale to maintain aspect ratio

        # Create a new array for the resized shape
        new_width = int(width * scale)
        new_height = int(height * scale)
        new_shape = np.zeros((new_height, new_width), dtype=bool)

        # Resize the shape
        for y in range(new_height):
            for x in range(new_width):
                orig_y = int(y / scale)
                orig_x = int(x / scale)
                if (orig_y, orig_x) in zip(shape[0] - np.min(shape[0]), shape[1] - np.min(shape[1])):
                    new_shape[y, x] = True

        # Calculate the position to place the resized shape
        start_y = output_center_y - new_height // 2
        start_x = i * (input_grid.shape[1] // 3) + (input_grid.shape[1] // 6) - new_width // 2

        # Place the resized shape in the output grid
        output_grid[start_y:start_y+new_height, start_x:start_x+new_width][new_shape] = color

    return output_grid

def generate_input():
    # Create a random sprite
    w, h = np.random.randint(2, 5), np.random.randint(2, 5)
    sprite = random_sprite(w, h)

    # Define colors and scaling factors
    colors = [Color.RED, Color.BLUE, Color.YELLOW]
    scales = [np.random.uniform(0.5, 2) for _ in range(3)]

    # Calculate the required grid size
    max_scaled_size = max(int(max(w, h) * max(scales)), 10)
    grid_width = max_scaled_size * 4  # Ensure enough space for all shapes
    grid_height = max_scaled_size * 2  # Ensure enough vertical space

    # Create the input grid
    input_grid = np.full((grid_height, grid_width), Color.BLACK, dtype=int)

    for i, (color, scale) in enumerate(zip(colors, scales)):
        # Scale the sprite
        scaled_w, scaled_h = int(w * scale), int(h * scale)
        scaled_sprite = np.zeros((scaled_h, scaled_w), dtype=bool)
        for y in range(scaled_h):
            for x in range(scaled_w):
                orig_y, orig_x = int(y / scale), int(x / scale)
                if orig_y < h and orig_x < w and sprite[orig_y, orig_x] != Color.BLACK:
                    scaled_sprite[y, x] = True

        # Color the scaled sprite
        colored_sprite = np.full((scaled_h, scaled_w), Color.BLACK, dtype=int)
        colored_sprite[scaled_sprite] = color

        # Place the colored sprite in a random vertical position
        x = i * (grid_width // 3) + (grid_width // 6) - scaled_w // 2
        y = np.random.randint(0, grid_height - scaled_h)
        input_grid[y:y+scaled_h, x:x+scaled_w] = colored_sprite

    return input_grid