from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, mirror

# description:
# In the input you will see two patterns on each outer side of two frames.
# To make the output, you need mirror two patterns by the symmetry of the framework, make them inside the framework.

def main(input_grid):
    # Extract the framework
    frame_color = Color.RED
    object_color = Color.GRAY 

    # Create an empty grid
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    # Get two frame that form the framework
    frames = find_connected_components(grid=input_grid, connectivity=4)
    frames = [frame for frame in frames if np.any(frame == frame_color)]

    # Get two objects that outside the framework
    objects = find_connected_components(grid=input_grid, connectivity=8, monochromatic=True)
    objects = [obj for obj in objects if np.any(obj == object_color)]
    
    object_list = []
    framework = []
    for frame in frames:
        # Get the frame and its position
        x, y, w, h = bounding_box(grid=frame)
        cropped_frame = crop(grid=frame)
        framework.append({"x": x, "y": y, "w": w, "h": h, "frame": cropped_frame})
        # Place the frame in the output grid
        output_grid = blit_sprite(grid=output_grid, sprite=cropped_frame, x=x, y=y)

    for obj in objects:
        # Get the object and its position
        x, y, w, h = bounding_box(grid=obj)
        cropped_obj = crop(grid=obj)
        object_list.append({"x": x, "y": y, "w": w, "h": h, "obj": cropped_obj})

    # Sort the framework by position
    framework = sorted(framework, key=lambda x: x["x"])
    framework = sorted(framework, key=lambda x: x["y"])    

    # Check if the framework is horizontal or vertical
    if_horizontal = framework[0]["w"] > framework[0]["h"]

    if if_horizontal:
        # Sort the objects by position
        object_list = sorted(object_list, key=lambda x: x["y"])

        # Get the two outer patterns
        pattern_part1 = object_list[0]['obj']
        pattern_part2 = object_list[1]['obj']

        # Mirror the two inner patterns according to each frame's line
        pattern_part1 = np.fliplr(pattern_part1)
        pattern_part2 = np.fliplr(pattern_part2)

        # Place the two outside patterns in the framework
        output_grid = blit_sprite(grid=output_grid, sprite=pattern_part1, x=object_list[0]['x'], y=framework[0]['y'] + 2)
        output_grid = blit_sprite(grid=output_grid, sprite=pattern_part2, x=object_list[1]['x'], y=framework[1]['y'] - object_list[1]['h'])
    else:
        # Sort the objects by position
        object_list = sorted(object_list, key=lambda x: x["x"])

        # Get the two outer patterns
        pattern_part1 = object_list[0]['obj']
        pattern_part2 = object_list[1]['obj']

        # Mirror the two inner patterns according to each frame's line
        pattern_part1 = np.flipud(pattern_part1)
        pattern_part2 = np.flipud(pattern_part2)

        print(framework)
        print(object_list)
       # Place the two outside patterns in the framework
        output_grid = blit_sprite(grid=output_grid, sprite=pattern_part1, x=framework[0]['x'] + 2, y=object_list[0]['y'])
        output_grid = blit_sprite(grid=output_grid, sprite=pattern_part2, x=framework[1]['x'] - object_list[1]['w'], y=object_list[1]['y'])

    return output_grid

def generate_input():
    # Create a 2D background
    n, m = np.random.randint(15, 30), np.random.randint(15, 30)
    grid = np.zeros((n, m), dtype=int)

    # Get a framework for pattern
    frame_length = np.random.randint(5, 10)
    frame_width = 2
    frame_color = Color.RED

    # Draw a half of the framework
    frame = np.zeros((frame_length, frame_width), dtype=int)
    frame = draw_line(grid=frame, x=0, y=0, direction=(1, 0), color=frame_color)
    frame[0][1] = frame_color
    frame[-1][1] = frame_color

    # Select the interval for two half frameworks that form one entire framework
    frame_interval = np.random.randint(4, 6)
    
    # Calculate the sizes of two patterns in framwork
    pattern_color = Color.GRAY
    pattern_length = frame_length - 2
    pattern_width = frame_interval // 2
    pattern_width_with_padding = frame_interval // 2 + 1

    # Generate two patterns out the framwork
    pattern_1 = random_sprite(n=pattern_length, m=pattern_width, color_palette=[pattern_color])
    pattern_2 = random_sprite(n=pattern_length, m=pattern_width, color_palette=[pattern_color])

    # place the pattern in the frame
    whole_frame = np.zeros((frame_length, frame_width * 2 + frame_interval + pattern_width_with_padding * 2), dtype=int)
    # Place the upper half of the frame
    whole_frame = blit_sprite(grid=whole_frame, sprite=frame, x=0, y=pattern_width_with_padding)
    # Place the upper pattern
    whole_frame = blit_sprite(grid=whole_frame, sprite=pattern_1, x=1, y=0)
    # Place the lower pattern
    whole_frame = blit_sprite(grid=whole_frame, sprite=pattern_2, x=1, y=frame_width * 2 + frame_interval + pattern_width_with_padding + 1)
    # Place the lower half of the frame
    whole_frame = blit_sprite(grid=whole_frame, sprite=np.fliplr(frame), x=0, y=frame_width + frame_interval + pattern_width_with_padding)

    # place the frame in the background
    x, y = random_free_location_for_sprite(grid=grid, sprite=whole_frame)
    grid = blit_sprite(grid=grid, sprite=whole_frame, x=x, y=y)

    # Randomly rotate the grid
    if np.random.rand() < 0.5:
        grid = np.rot90(grid)
    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
