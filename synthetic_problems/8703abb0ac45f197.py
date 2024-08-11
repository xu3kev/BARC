from common import *

import numpy as np
from typing import *

# concepts:
# flood fill, connectivity, objects, color

# description:
# In the input grid, there are several disconnected black regions within a larger grid with random colored pixels.
# To make the output, identify each black region and replace it with the color of the largest connected component that is touching it from any side.


def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # Find all distinct colored regions except for black
    colored_regions = find_connected_components(input_grid, connectivity=4, background=Color.BLACK, monochromatic=True)

    # Identify all black regions
    black_regions = find_connected_components(input_grid, connectivity=4, background=Color.BLACK, monochromatic=False)

    # Process each black region
    for black_region in black_regions:
        black_bb = bounding_box(black_region)
        touching_colors = []

        for region in colored_regions:
            region_bb = bounding_box(region)
            is_touching = (
                (region_bb[0] < black_bb[0] + black_bb[2] and region_bb[0] + region_bb[2] > black_bb[0]) or
                (region_bb[1] < black_bb[1] + black_bb[3] and region_bb[1] + region_bb[3] > black_bb[1])
            )
            if is_touching:
                touching_colors.append(np.count_nonzero(region != 0))

        if touching_colors:
            max_count_idx = np.argmax(touching_colors)
            dominant_color = np.unique(region)[0]

            x, y = np.where(black_region != Color.BLACK)
            if x.size > 0 and y.size > 0:
                flood_fill(output_grid, x[0], y[0], dominant_color)

    return output_grid


def generate_input():
    width, height = np.random.randint(10, 15), np.random.randint(10, 15)
    input_grid = np.zeros((width, height), dtype=int)

    # Select random palette colors excluding black
    colors = list(Color.NOT_BLACK)

    # Fill the grid with a random distribution of colors
    for i in range(width):
        for j in range(height):
            if random.random() < 0.2:
                input_grid[i, j] = Color.BLACK
            else:
                input_grid[i, j] = random.choice(colors)

    # Add random black regions
    num_black_regions = np.random.randint(1, 4)
    for _ in range(num_black_regions):
        region_w, region_h = np.random.randint(1, 4), np.random.randint(1, 4)
        region_x, region_y = np.random.randint(0, width - region_w), np.random.randint(0, height - region_h)
        input_grid[region_x:region_x + region_w, region_y:region_y + region_h] = Color.BLACK

    return input_grid