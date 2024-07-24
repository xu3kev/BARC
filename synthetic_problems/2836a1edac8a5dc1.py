from common import *

import numpy as np
from typing import *
from collections import Counter

# concepts:
# growing, pixel manipulation, patterns

# description:
# In the input, you will see some number of colored crosses, each of which is 3 pixels tall, 3 pixels wide, and has a single pixel in the center that is a different color.
# Make the output by growing each cross by 1 pixel in north/south/east/west directions and replacing the center pixel with the resulting diagonals from the grown part.
# If the grown crosses overlap, blend the overlapping colors.

def blend_colors(colors):
    # Blending function: Just return the most common color in case of blending
    return Counter(colors).most_common(1)[0][0]

def main(input_grid):
    output_grid = np.copy(input_grid)
    crosses = find_connected_components(input_grid, background=Color.BLACK, monochromatic=False)
    
    colors_dict = {}
    
    for cross in crosses:
        x, y, w, h = bounding_box(cross)
        center_x, center_y = x + w // 2, y + h // 2

        center_color = cross[center_x, center_y]
        cross_color = cross[cross != Color.BLACK][0]

        for output_x in range(x - 1, x + w + 1):
            for output_y in range(y - 1, y + h + 1):
                if output_x < 0 or output_y < 0 or output_x >= input_grid.shape[0] or output_y >= input_grid.shape[1]:
                    continue

                if output_x == center_x or output_y == center_y:
                    if (output_x, output_y) not in colors_dict:
                        colors_dict[(output_x, output_y)] = []
                    colors_dict[(output_x, output_y)].append(cross_color)
                
                if (output_x - center_x) == (output_y - center_y) or (output_x - center_x) == (center_y - output_y):
                    if (output_x, output_y) not in colors_dict:
                        colors_dict[(output_x, output_y)] = []
                    colors_dict[(output_x, output_y)].append(center_color)
    
    for (output_x, output_y), colors in colors_dict.items():
        output_grid[output_x, output_y] = blend_colors(colors)

    return output_grid

def generate_input():
    input_grid = np.zeros((20, 20), dtype=int)

    for _ in range(3):
        cross = np.zeros((3, 3), dtype=int)
        cross_color, center_color = random.sample(list(Color.NOT_BLACK), 2)
        cross[1, :] = cross_color
        cross[:, 1] = cross_color
        cross[1, 1] = center_color

        x, y = random_free_location_for_sprite(input_grid, cross)
        blit_sprite(input_grid, cross, x, y)

    return input_grid