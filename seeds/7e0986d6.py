from common import *

import numpy as np
from typing import *

# concepts:
# denoising, topology

# description:
# In the input you will see a black background with large rectangles of the same color, and random "noise" pixels added at random locations sometimes on the rectangles and sometimes not.
# To make the output, remove the noise pixels to reveal the rectangles.

def main(input_grid):
    # Plan:
    # 1. Extract and classify the objects (rectangles, noise pixels)
    # 2. If a noise pixel is significantly touching a rectangle (it has at least 2 neighbors that are part of the rectangle), then the noise reveals the rectangle color
    # 3. Otherwise, the noise reveals the background, so delete the noise pixel

    objects = find_connected_components(input_grid, monochromatic=True, connectivity=4, background=Color.BLACK)
    rectangle_size_threshold = 4
    noisy_objects = [ obj for obj in objects if np.sum(obj != Color.BLACK) < rectangle_size_threshold ]
    rectangle_objects = [ obj for obj in objects if np.sum(obj != Color.BLACK) >= rectangle_size_threshold ]

    output_grid = np.copy(input_grid)
    for noise_object in noisy_objects:
        noise_object_mask = noise_object != Color.BLACK
        noise_neighbors_mask = object_neighbors(noise_object, connectivity=4, background=Color.BLACK)

        for rectangle_object in rectangle_objects:
            # Check if the noise object has at least 2 neighbors that are part of this rectangle
            rectangle_object_mask = rectangle_object != Color.BLACK
            if np.sum(noise_neighbors_mask & rectangle_object_mask) >= 2:
                rectangle_color = np.argmax(np.bincount(rectangle_object[rectangle_object_mask]))
                output_grid[noise_object_mask] = rectangle_color
                break
        else:
            # Delete this noise object
            output_grid[noise_object_mask] = Color.BLACK

    return output_grid


def generate_input():
    w, h = np.random.randint(10, 25, size=2)
    grid = np.full((w, h), Color.BLACK)

    rectangle_color, noise_color = np.random.choice(Color.NOT_BLACK, size=2, replace=False)
    n_rectangles = np.random.randint(2, 4)

    for _ in range(n_rectangles):
        rw, rh = np.random.randint(3, 2*w//3), np.random.randint(3, 2*h//3)
        sprite = np.full((rw, rh), rectangle_color) # Can also do: random_sprite(rw, rh, color_palette=[rectangle_color], density=1)
        x, y = random_free_location_for_sprite(grid, sprite)
        blit_sprite(grid, sprite, x, y)
    
    n_noise_pixels = np.random.randint(8, 16)
    for _ in range(n_noise_pixels):
        x, y = np.random.randint(w), np.random.randint(h)
        grid[x, y] = noise_color
    
    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
