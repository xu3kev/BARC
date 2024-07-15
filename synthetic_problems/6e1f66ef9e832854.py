from common import *

import numpy as np
from typing import *

# concepts:
# sliding objects, infinite ray, color guide

# description:
# In the input grid, you will see a T-shaped object of one color in a black grid, with pixels of another color scattered around the grid.
# To produce the output grid, for each colored pixel, draw a line in the direction away from the nearest point of the T-shape.
# The line should extend until it reaches the edge of the grid or hits another line.
# The color of each line should match the color of its originating pixel.

def main(input_grid):
    # 1. Find the T-shaped object
    # 2. Get the color of the T-shape and the scattered pixels
    # 3. For each scattered pixel, find the nearest point on the T-shape
    # 4. Draw a line from the pixel in the opposite direction of the nearest T-shape point

    # Find the T-shape (largest object)
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)
    t_shape = max(objects, key=lambda o: np.count_nonzero(o))

    # Get colors
    t_color = t_shape[t_shape != Color.BLACK][0]
    colors = set(np.unique(input_grid)) - {Color.BLACK, t_color}
    assert len(colors) == 1
    pixel_color = list(colors)[0]

    output_grid = np.full_like(input_grid, Color.BLACK)
    
    # Find T-shape coordinates
    t_coords = np.argwhere(t_shape == t_color)

    # Process each colored pixel
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] != pixel_color:
                continue

            # Find nearest point on T-shape
            distances = np.sqrt(np.sum((t_coords - [x, y])**2, axis=1))
            nearest_t_point = t_coords[np.argmin(distances)]

            # Calculate direction away from T-shape
            dx, dy = x - nearest_t_point[0], y - nearest_t_point[1]
            length = np.sqrt(dx**2 + dy**2)
            dx, dy = int(round(dx/length)), int(round(dy/length))

            # Draw line
            draw_line(output_grid, x, y, length=None, color=pixel_color, direction=(dx, dy), stop_at_color=[pixel_color])

    # Add T-shape to output
    output_grid[t_shape == t_color] = t_color

    return output_grid

def generate_input():
    # Create a 20x20 black grid
    input_grid = np.full((20, 20), Color.BLACK)

    # Choose colors for T-shape and pixels
    t_color, pixel_color = np.random.choice(Color.NOT_BLACK, 2, replace=False)

    # Create T-shape
    t_shape = np.full((7, 5), Color.BLACK)
    t_shape[0:3, :] = t_color
    t_shape[3:, 2] = t_color

    # Place T-shape at a random location
    x, y = np.random.randint(0, 20 - 7), np.random.randint(0, 20 - 5)
    blit_sprite(input_grid, t_shape, x=x, y=y)

    # Generate 5-15 pixels at random unfilled spots
    n_pixels = np.random.randint(5, 16)
    x_choices, y_choices = np.where(input_grid == Color.BLACK)
    location_choices = list(zip(x_choices, y_choices))
    pixel_locations = random.sample(location_choices, n_pixels)
    for x, y in pixel_locations:
        input_grid[x, y] = pixel_color

    return input_grid