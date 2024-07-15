from common import *

import numpy as np
from typing import *

# concepts:
# objects, color guide, growing, patterns, intersection

# description:
# In the input, you will see a 30x30 grid with several rectangular objects of different colors. 
# Each rectangle contains one or more pixels of a different color (the "seed" pixels).
# Outside these rectangles, there's a small 3x3 "growth pattern" sprite.
# To create the output:
# 1. For each seed pixel, apply the growth pattern centered on that pixel.
# 2. Then, grow the pattern outwards in all directions within its rectangle, stopping at the rectangle's edges.
# 3. If growths from different seed pixels intersect, color the intersection points red.
# The growth should not extend outside the rectangles or affect the background.

def main(input_grid):
    n, m = input_grid.shape
    background_color = np.bincount(input_grid.flatten()).argmax()
    output_grid = np.full_like(input_grid, background_color)

    # Find all objects
    objects = find_connected_components(input_grid, background=background_color, connectivity=4, monochromatic=False)

    # Sort objects by size, the smallest one is the growth pattern
    sorted_objects = sorted(objects, key=lambda x: np.count_nonzero(x != background_color))
    growth_pattern = crop(sorted_objects[0], background=background_color)
    rectangles = sorted_objects[1:]

    for rectangle in rectangles:
        # Crop the rectangle and find its position
        rec_x, rec_y, w, h = bounding_box(rectangle, background=background_color)
        cropped_rectangle = crop(rectangle, background=background_color)

        # Find the main color and seed color of the rectangle
        colors, counts = np.unique(cropped_rectangle, return_counts=True)
        rectangle_color = colors[counts.argmax()]
        seed_color = colors[counts.argmin()]

        # Create a growth mask
        growth_mask = np.zeros_like(cropped_rectangle, dtype=bool)

        # For each seed pixel, apply and grow the pattern
        for x, y in np.argwhere(cropped_rectangle == seed_color):
            # Apply initial growth pattern
            pattern_mask = np.zeros_like(cropped_rectangle, dtype=bool)
            blit_sprite(pattern_mask, growth_pattern, x - 1, y - 1, background=False)
            growth_mask |= pattern_mask

            # Grow the pattern
            while True:
                new_growth = np.zeros_like(growth_mask)
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    shifted = np.roll(growth_mask, (dx, dy), axis=(0, 1))
                    new_growth |= shifted & (cropped_rectangle == rectangle_color)
                if np.array_equal(new_growth, growth_mask):
                    break
                growth_mask = new_growth

        # Apply growth to the rectangle
        cropped_rectangle[growth_mask] = seed_color

        # Find intersections and color them red
        seed_positions = np.argwhere(cropped_rectangle == seed_color)
        if len(seed_positions) > 1:
            for x, y in seed_positions:
                if np.sum(cropped_rectangle[max(0, x-1):x+2, max(0, y-1):y+2] == seed_color) > 5:
                    cropped_rectangle[x, y] = Color.RED

        # Add the modified rectangle back to the output grid
        blit_sprite(output_grid, cropped_rectangle, rec_x, rec_y, background=background_color)

    return output_grid

def generate_input():
    n = m = 30
    grid = np.full((n, m), Color.BLACK)

    # Generate growth pattern
    growth_pattern = random_sprite(3, 3, density=0.7, symmetry='radial', color_palette=[Color.GREY])

    # Place growth pattern
    x, y = np.random.randint(0, n-3), np.random.randint(0, m-3)
    blit_sprite(grid, growth_pattern, x, y)

    # Generate 3-5 rectangles
    for _ in range(np.random.randint(3, 6)):
        width, height = np.random.randint(5, 15), np.random.randint(5, 15)
        rectangle_color = np.random.choice([Color.BLUE, Color.GREEN, Color.YELLOW, Color.PINK])
        seed_color = np.random.choice([Color.RED, Color.ORANGE, Color.TEAL, Color.MAROON])
        
        rectangle = np.full((height, width), rectangle_color)
        
        # Add 1-3 seed pixels
        for _ in range(np.random.randint(1, 4)):
            seed_x, seed_y = np.random.randint(0, height), np.random.randint(0, width)
            rectangle[seed_x, seed_y] = seed_color

        # Place rectangle
        rx, ry = random_free_location_for_sprite(grid, rectangle, padding=1)
        blit_sprite(grid, rectangle, rx, ry)

    return grid