from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, mirror

# description:
# In the input you will see two objects on each outer side of two red frames.
# To make the output, you need to mirror the two objects by flipping them over the symmetry of the red frames, making them inside the red frames. Each object flips over the frame closest to it.

def main(input_grid):
    # Extract the framework
    frame_color = Color.RED
    object_color = Color.GRAY 
    background = Color.BLACK

    # Create an empty grid
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    # parse the input
    objects = find_connected_components(grid=input_grid, connectivity=8, monochromatic=True, background=background)
    frames = [ obj for obj in objects if frame_color in object_colors(obj, background=background) ]
    mirrored_objects = [ obj for obj in objects if object_color in object_colors(obj, background=background) ]

    # determine if we are doing horizontal or vertical mirroring
    # if all the objects have the same X coordinate, we are doing vertical mirroring
    # if all the objects have the same Y coordinate, we are doing horizontal mirroring
    x_positions = [ object_position(obj, background=background, anchor="center")[0] for obj in objects ]
    y_positions = [ object_position(obj, background=background, anchor="center")[1] for obj in objects ]
    if all(x == x_positions[0] for x in x_positions): orientation = "vertical"
    elif all(y == y_positions[0] for y in y_positions): orientation = "horizontal"
    else: raise ValueError(f"The objects are not aligned in a single axis")

    # Flip each other object over its closest frame
    for mirrored_object in mirrored_objects:
        # Find the closest frame
        def distance_between_objects(obj1, obj2):
            x1, y1 = object_position(obj1, background=background, anchor="center")
            x2, y2 = object_position(obj2, background=background, anchor="center")
            return (x1 - x2)**2 + (y1 - y2)**2        
        closest_frame = min(frames, key=lambda frame: distance_between_objects(frame, mirrored_object))

        # Build a symmetry object for flipping over the closest frame
        frame_x, frame_y = object_position(closest_frame, background=background, anchor="center")
        this_x, this_y = object_position(mirrored_object, background=background, anchor="center")
        # Make it one pixel past the middle of frame
        frame_y += 0.5 if this_y > frame_y else -0.5
        frame_x += 0.5 if this_x > frame_x else -0.5
        symmetry = MirrorSymmetry(mirror_x=frame_x if orientation == "horizontal" else None,
                                  mirror_y=frame_y if orientation == "vertical" else None)
        
        # Flip the object over the symmetry
        for x, y in np.argwhere(mirrored_object != background):
            x2, y2 = symmetry.apply(x, y)
            output_grid[x2, y2] = mirrored_object[x, y]
        
        # Draw the frame
        output_grid = blit_object(output_grid, closest_frame)

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
    frame_sprite = np.zeros((frame_length, frame_width), dtype=int)
    # horizontal bar and two vertical pixels
    frame_sprite[:, 0] = frame_color
    frame_sprite[0, 1] = frame_color
    frame_sprite[-1, 1] = frame_color

    # Select the interval for two half frameworks that form one entire framework
    frame_interval = np.random.randint(4, 6)
    
    # Calculate the sizes of two things that we are going to mirror within framwork
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
    whole_frame = blit_sprite(whole_frame, frame_sprite, x=0, y=pattern_width_with_padding)
    # Place the upper pattern
    whole_frame = blit_sprite(whole_frame, pattern_1, x=1, y=0)
    # Place the lower pattern
    whole_frame = blit_sprite(whole_frame, pattern_2, x=1, y=frame_width * 2 + frame_interval + pattern_width_with_padding + 1)
    # Place the lower half of the frame
    whole_frame = blit_sprite(whole_frame, np.fliplr(frame_sprite), x=0, y=frame_width + frame_interval + pattern_width_with_padding)

    # place the frame in the background
    x, y = random_free_location_for_sprite(grid=grid, sprite=whole_frame)
    grid = blit_sprite(grid=grid, sprite=whole_frame, x=x, y=y)

    # Randomly rotate the grid so that we get both vertical and horizontal arrangements
    if np.random.rand() < 0.5:
        grid = np.rot90(grid)
    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
