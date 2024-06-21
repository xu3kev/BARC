from common import *

import numpy as np
from typing import *

# concepts:
# Making sprite symmetric, detecting sprite

# description:
# In the input you will see a grid. Within it, there is a smaller nxn grid (n odd) that contains 4 parts that are
# mostly radially symmetric to its center, except for some pixels. Some corresponding parts of these pixels are missing in other quadrants.
# The output would find the not symmetric pixels and recover its corresponding parts such that the inner grid has radial symmetry.


def main(input_grid):
    output_grid = input_grid.copy()

    # Finds sprite
    center_of_rotation = detect_rotational_symmetry(
        input_grid, ignore_color=Color.BLACK
    )
    x, y, w, h = bounding_box(input_grid, background=Color.BLACK)
    # Finds the maximum edge
    dist_to_center = max(
        center_of_rotation[0] - x,
        x + w - center_of_rotation[0] - 1,
        center_of_rotation[1] - y,
        y + h - center_of_rotation[1] - 1,
    )

    x, y = (
        center_of_rotation[0] - dist_to_center,
        center_of_rotation[1] - dist_to_center,
    )
    sprite = input_grid[
        x : (center_of_rotation[0] + dist_to_center + 1),
        y : (center_of_rotation[1] + dist_to_center + 1),
    ]
    show_colored_grid(sprite)
    # Find the different regions of the sprite
    center_x, center_y = sprite.shape[0] // 2 + 1, sprite.shape[1] // 2 + 1
    upper_left = sprite[0:center_x, 0:center_y]
    upper_right = sprite[center_x - 1 :, 0:center_y]
    lower_left = sprite[0:center_x, center_y - 1 :]
    lower_right = sprite[center_x - 1 :, center_y - 1 :]
    # Stores the amount of rotation needed and the regions
    regions = [(upper_left, 0), (upper_right, 3), (lower_left, 1), (lower_right, 2)]

    # Make each region have matching pixels from other regions
    for i in range(len(regions)):
        region_i = np.rot90(regions[i][0], regions[i][1])
        for j in range(i + 1, len(regions)):
            region_j = np.rot90(regions[j][0].copy(), regions[j][1])
            # Compare regions and add missing pixels
            for r0 in range(region_i.shape[0]):
                for r1 in range(region_i.shape[1]):
                    if (
                        region_i[r0, r1] != region_j[r0, r1]
                        and region_j[r0, r1] == Color.BLACK
                    ):
                        region_j[r0, r1] = region_i[r0, r1]
                    elif (
                        region_i[r0, r1] != region_j[r0, r1]
                        and region_i[r0, r1] == Color.BLACK
                    ):
                        region_i[r0, r1] = region_j[r0, r1]

        regions[i] = (np.rot90(region_i, -regions[i][1]), regions[i][1])
        regions[j] = (np.rot90(region_j, -regions[j][1]), regions[j][1])

    # Create output sprite by combining quadrants
    output_sprite = np.zeros((sprite.shape[0], sprite.shape[1]), dtype=int)
    blit(output_sprite, regions[0][0], 0, 0)
    blit(output_sprite, regions[1][0], center_x - 1, 0)
    blit(output_sprite, regions[2][0], 0, center_y - 1)
    blit(output_sprite, regions[3][0], center_x - 1, center_y - 1)

    # Place the output sprite back to the output grid
    blit(output_grid, output_sprite, x, y)

    return output_grid


def generate_input():
    # Initialize 10x10 grid
    grid = np.zeros((10, 10), dtype=int)

    # Create 5x5 sprite
    sprite = random_sprite(
        5, 5, density=0.4, symmetry="radial", color_palette=list(Color.NOT_BLACK)
    )

    # Randomly remove pixels from sprite
    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            if random.random() < 0.2:
                sprite[i, j] = Color.BLACK

    # Place sprite randomly onto the grid
    x, y = random_free_location_for_object(grid, sprite)
    blit(grid, sprite, x, y)

    return grid


# ============= remove below this point for prompting =============

if __name__ == "__main__":
    visualize(generate_input, main)
