from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, counting

# description:
# In the input you will see monochromatic rectangles arranged into an array.
# To make the output, find the most common color of the 2x1 rectangles, second most common color, etc.
# Then, make the output a vertical stripe colored with the second common color, then the third most common color, etc., starting at the top, and skipping the most common color.

def main(input_grid):
    # Plan:
    # 1. Extract the objects, arranged into the array
    # 2. Count the colors
    # 3. Sort the colors by count
    # 4. Create the output grid, remembering to skip the most common color

    background = Color.BLACK
    
    objects = find_connected_components(input_grid, monochromatic=True, connectivity=4, background=background)
    possible_x_values = [ object_position(obj, background=background, anchor="upper left")[0] for obj in objects ]
    possible_y_values = [ object_position(obj, background=background, anchor="upper left")[1] for obj in objects ]
    object_array = [ [ next(obj for obj in objects if (x, y) == object_position(obj, background=background, anchor="upper left") )
                      for y in sorted(set(possible_y_values)) ]
                    for x in sorted(set(possible_x_values)) ]

    # Extract and count the colors
    object_colors = [ obj[obj!=background][0] for obj in objects ]
    color_counts = { color: sum(1 for object_color in object_colors if object_color == color) for color in set(object_colors) }

    sorted_colors = list(sorted(color_counts, key=lambda color: color_counts[color], reverse=True))
    # skip the most common color
    sorted_colors = sorted_colors[1:]

    # the output is a vertical stripe containing one pixel per color
    output_grid = np.full((1, len(sorted_colors)), background)
    for y, color in enumerate(sorted_colors):
        output_grid[0, y] = color

    return output_grid




def generate_input():
    # Plan:
    # 1. randomly pick size and possible colors for the rectangles
    # 2. randomly pick how far apart the rectangle should be when they are arranged in an array
    # 3. create the array of rectangles, randomly choosing colors
    # 5. double check that no two colors have the exact same count

    rectangle_dimensions = np.random.randint(1, 4, size=(2))
    number_of_distinct_colors = np.random.randint(3, 6)
    rectangle_colors = np.random.choice(Color.NOT_BLACK, size=(number_of_distinct_colors), replace=False)

    rectangle_spacing = np.random.randint(1, 4, size=(2))
    grid_dimensions = np.random.randint(10, 30, size=(2))

    grid = np.full(grid_dimensions, Color.BLACK)

    possible_x_values = np.arange(rectangle_spacing[0], grid_dimensions[0] - rectangle_dimensions[0], rectangle_spacing[0] + rectangle_dimensions[0])
    possible_y_values = np.arange(rectangle_spacing[1], grid_dimensions[1] - rectangle_dimensions[1], rectangle_spacing[1] + rectangle_dimensions[1])
    for x in possible_x_values:
        for y in possible_y_values:
            color = np.random.choice(rectangle_colors)
            sprite = random_sprite(rectangle_dimensions[0], rectangle_dimensions[1], density=1, color_palette=[color])
            blit_sprite(grid, sprite, x, y)

    # doublecheck that no pair of colors have the same count
    for color1 in rectangle_colors:
        for color2 in rectangle_colors:
            if color1 == color2:
                continue
            count1 = sum(1 for color in grid.flatten() if color == color1)
            count2 = sum(1 for color in grid.flatten() if color == color2)
            assert count1 != count2
    
    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
