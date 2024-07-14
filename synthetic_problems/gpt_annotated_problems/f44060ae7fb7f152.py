from common import *

import numpy as np
from typing import *

# concepts:
# patterns, growing, objects, color guide, connectivity

# description:
# In the input, you will see a 30x30 grid with several rectangular objects of different colors. Each object contains one or more special pixels of a different color (the "seed" pixels). There is also a small "growth pattern" object somewhere on the grid.
# For each rectangular object:
# 1. Find all seed pixels within it
# 2. For each seed pixel, grow the pattern outward in all directions, stopping at the edges of the rectangle
# 3. If two growing patterns from different seeds meet, they stop growing at that point
# The output should show all rectangles with their grown patterns inside.

def main(input_grid):
    # Get grid size
    n, m = input_grid.shape

    # Determine background color (most common color)
    background_color = np.bincount(input_grid.flatten()).argmax()

    # Find all objects (rectangles and the growth pattern)
    objects = find_connected_components(input_grid, background=background_color, connectivity=4, monochromatic=False)

    # Sort objects by size, the smallest one is the growth pattern
    sorted_objects = sorted(objects, key=lambda x: np.count_nonzero(x != background_color))
    growth_pattern = crop(sorted_objects[0], background=background_color)
    rectangles = sorted_objects[1:]

    # Prepare output grid
    output_grid = np.full_like(input_grid, background_color)

    # Process each rectangle
    for rectangle in rectangles:
        # Crop the rectangle while preserving its position
        rec_x, rec_y, w, h = bounding_box(rectangle, background=background_color)
        cropped_rectangle = crop(rectangle, background=background_color)

        # Find the rectangle color and seed color
        colors, counts = np.unique(cropped_rectangle, return_counts=True)
        rectangle_color = colors[np.argmax(counts)]
        seed_color = colors[counts != np.max(counts)]

        # Create a mask for the grown pattern
        growth_mask = np.zeros_like(cropped_rectangle, dtype=bool)

        # Find all seed pixels
        seed_pixels = np.argwhere(cropped_rectangle == seed_color)

        # Grow pattern from each seed
        for seed in seed_pixels:
            current_growth = np.zeros_like(cropped_rectangle, dtype=bool)
            current_growth[tuple(seed)] = True

            while True:
                new_growth = np.zeros_like(current_growth)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    shifted = np.roll(current_growth, (dx, dy), axis=(0, 1))
                    new_growth |= shifted & (cropped_rectangle == rectangle_color) & ~growth_mask

                if not np.any(new_growth):
                    break

                current_growth = new_growth
                growth_mask |= current_growth

        # Apply growth pattern to the rectangle
        for x, y in np.argwhere(growth_mask):
            pattern_x, pattern_y = x % growth_pattern.shape[0], y % growth_pattern.shape[1]
            if growth_pattern[pattern_x, pattern_y] != background_color:
                cropped_rectangle[x, y] = growth_pattern[pattern_x, pattern_y]

        # Add processed rectangle back to output grid
        blit_sprite(output_grid, cropped_rectangle, rec_x, rec_y, background=background_color)

    return output_grid

def generate_input():
    # Create empty 30x30 grid
    n, m = 30, 30
    grid = np.full((n, m), Color.BLACK)

    # Generate growth pattern
    growth_pattern = random_sprite(np.random.randint(3, 5), np.random.randint(3, 5), 
                                   density=0.7, color_palette=Color.NOT_BLACK)

    # Place growth pattern on grid
    gp_x, gp_y = random_free_location_for_sprite(grid, growth_pattern)
    blit_sprite(grid, growth_pattern, gp_x, gp_y)

    # Generate 3-5 rectangles
    for _ in range(np.random.randint(3, 6)):
        # Random rectangle size
        rect_w, rect_h = np.random.randint(5, 15), np.random.randint(5, 15)
        
        # Random colors for rectangle and seeds
        rect_color = np.random.choice(list(Color.NOT_BLACK))
        seed_color = np.random.choice([c for c in Color.NOT_BLACK if c != rect_color])

        # Create rectangle
        rectangle = np.full((rect_w, rect_h), rect_color)

        # Add 1-3 seed pixels
        for _ in range(np.random.randint(1, 4)):
            seed_x, seed_y = np.random.randint(rect_w), np.random.randint(rect_h)
            rectangle[seed_x, seed_y] = seed_color

        # Place rectangle on grid
        rect_x, rect_y = random_free_location_for_sprite(grid, rectangle, padding=1)
        blit_sprite(grid, rectangle, rect_x, rect_y)

    return grid