from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, mirror

# description:
# In the input you will see two patterns close by two frames.
# To make the output, you need to split the inner pattern into two parts by the symmetry of the framework. 
# Then, mirror the two parts according to each frame's line and place them in the output grid.

def main(input_grid):
    # Extract the framework
    frame_color = Color.RED

    # Create an empty grid
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    # Get two frame that form the framework
    frames = find_connected_components(grid=input_grid, connectivity=4)
    frames = [frame for frame in frames if np.any(frame == frame_color)]
    framework = []
    for frame in frames:
        # Get the frame and its position
        x, y, w, h = bounding_box(grid=frame)
        cropped_frame = crop(grid=frame)
        framework.append({"x": x, "y": y, "w": w, "h": h, "frame": cropped_frame})
        # Place the frame in the output grid
        output_grid = blit_sprite(grid=output_grid, sprite=cropped_frame, x=x, y=y)

    # Sort the framework by position
    framework = sorted(framework, key=lambda x: x["x"])
    framework = sorted(framework, key=lambda x: x["y"])

    # Get the inner pattern
    x_whole, y_whole, w_whole, h_whole = bounding_box(grid=input_grid)
    inner_pattern = input_grid[x_whole + 1 : x_whole + w_whole - 1, y_whole + 1 : y_whole + h_whole - 1]

    # Check if the framework is horizontal or vertical
    if_horizontal = framework[0]["w"] > framework[0]["h"]

    if if_horizontal:
        # Split the inner pattern into two parts by the symmetry of the framework
        pattern_len = inner_pattern.shape[1] // 2
        pattern_part1 = inner_pattern[:, : pattern_len]
        pattern_part2 = inner_pattern[:, pattern_len:]

        # Mirror the two inner patterns according to each frame's line
        pattern_part1 = np.fliplr(pattern_part1)
        pattern_part2 = np.fliplr(pattern_part2)

        # Place the two inner patterns in the output grid
        output_grid = blit_sprite(grid=output_grid, sprite=pattern_part1, x=framework[0]['x'] + 1, y=framework[0]['y'] - pattern_len)
        output_grid = blit_sprite(grid=output_grid, sprite=pattern_part2, x=framework[1]['x'] + 1, y=framework[1]['y'] + 2)
    else:
        # Split the inner pattern into two parts by the symmetry of the framework
        pattern_len = inner_pattern.shape[0] // 2
        pattern_part1 = inner_pattern[: pattern_len, :]
        pattern_part2 = inner_pattern[pattern_len:, :]

        # Mirror the two inner patterns according to each frame's line
        pattern_part1 = np.flipud(pattern_part1)
        pattern_part2 = np.flipud(pattern_part2)

        # Place the two inner patterns in the output grid
        output_grid = blit_sprite(grid=output_grid, sprite=pattern_part1, x=framework[0]['x'] - pattern_len, y=framework[0]['y'] + 1)
        output_grid = blit_sprite(grid=output_grid, sprite=pattern_part2, x=framework[1]['x'] + 2, y=framework[1]['y'] + 1)

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
    frame_interval = 4
    
    # Calculate the sizes of two patterns in framwork
    pattern_color = Color.GRAY
    pattern_interval = 1
    pattern_length = frame_length - 2
    pattern_width_1 = frame_interval // 2
    pattern_width_2 = frame_interval - pattern_width_1 - pattern_interval

    # Generate two patterns in framwork
    pattern_1 = random_sprite(n=pattern_length, m=pattern_width_1, color_palette=[pattern_color])
    pattern_2 = random_sprite(n=pattern_length, m=pattern_width_2, color_palette=[pattern_color])

    # place the pattern in the frame
    whole_frame = np.zeros((frame_length, frame_width * 2 + frame_interval), dtype=int)
    # Place the upper half of the frame
    whole_frame = blit_sprite(grid=whole_frame, sprite=frame, x=0, y=0)
    # Place the upper pattern
    whole_frame = blit_sprite(grid=whole_frame, sprite=pattern_1, x=1, y=frame_width)
    # Place the lower pattern
    whole_frame = blit_sprite(grid=whole_frame, sprite=pattern_2, x=1, y=frame_width + pattern_width_1 + pattern_interval)
    # Place the lower half of the frame
    whole_frame = blit_sprite(grid=whole_frame, sprite=np.fliplr(frame), x=0, y=frame_width + pattern_width_1 + pattern_interval + pattern_width_2)

    # place the frame in the background
    x, y = random_free_location_for_sprite(grid=grid, sprite=whole_frame)
    grid = blit_sprite(grid=grid, sprite=whole_frame, x=x, y=y)

    # Randomly rotate the grid
    grid = np.rot90(grid, k=np.random.randint(4))

    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
