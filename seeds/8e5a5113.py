from common import *

import numpy as np
from typing import *

# concepts:
# rotate, position

# description:
# In the input you will see a grid with 3 regions separated by grey horizontal lines. The leftmost region contains a multicolored sprite and the others are empty (black)
# To make the output, rotate the leftmost region 90 degree clockwise and place it in the first empty region, then rotate it a further 90 degrees and put it in the second empty region, etc.

def main(input_grid):
    # Get all the regions separated by the divider in the input grid
    divider_color = Color.GRAY
    regions = find_connected_components(input_grid, connectivity=4, background=divider_color, monochromatic=False)

    # Sort the region by x position so that we can get the leftmost, middle, and rightmost regions
    regions.sort(key=lambda region: object_position(region, background=divider_color)[0])

    # We are going to draw on top of the input
    output_grid = input_grid.copy()

    # Get the leftmost region which contains the multicolored sprite
    leftmost_region = regions[0]
    template_sprite = crop(grid=leftmost_region, background=divider_color)

    empty_regions = regions[1:]

    for empty_region in empty_regions:
        # Rotate the template sprite 90 degree clockwise
        template_sprite = np.rot90(template_sprite)

        # Place the rotated template sprite in the empty region
        x, y = object_position(empty_region, background=divider_color)
        blit_sprite(output_grid, sprite=template_sprite, x=x, y=y)
    
    return output_grid

def generate_input():
    # Create a grid with some regions separated by vertical grey lines
    # This is generalized so that there can be various numbers of regions
    n_regions = random.choice([2, 3, 4, 5])
    region_size = np.random.randint(3, 6)
    n_dividers = n_regions - 1
    width, height = n_regions * region_size + n_dividers, region_size
    grid = np.full((width, height), Color.BLACK)

    # Draw lines for the dividers
    line_color = Color.GRAY
    for x in range(region_size, width, region_size + 1):
        draw_line(grid, x=x, y=0, direction=(0, 1), color=line_color)

    # Draw one template
    possible_colors = [color for color in Color.NOT_BLACK if color != line_color]
    template_sprite = random_sprite(region_size, region_size, color_palette=possible_colors, density=1.0)

    # Place the template pattern in the first black region
    x, y = 0, 0
    blit_sprite(grid, sprite=template_sprite, x=x, y=y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
