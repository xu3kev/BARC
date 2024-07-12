from common import *

import numpy as np
from typing import *

# concepts:
# color guide, lines, connectivity, objects

# description:
# In the input, there are multiple colored shapes (objects) and a single floating line of colored pixels acting as a guideline.
# The output requires drawing lines from the centroid of each shape to the closest pixel of the guideline, with lines of the same color as the guideline pixel it connects to.
# Ensure that lines do not intersect with any other objects.

def main(input_grid):
    # Copy input to output grid
    output_grid = np.copy(input_grid)

    # Identify all objects in the grid
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)

    # Identify guideline pixels
    guideline_pixels = [(x,y) for x, y in np.argwhere(output_grid != Color.BLACK) 
                        if all(output_grid[tx,ty] == output_grid[x,y] for tx, ty in np.ndindex(output_grid.shape) if (tx, ty) != (x, y) 
                        and abs(tx - x) <= 1 and abs(ty - y) <= 1)]

    for obj in objects:
        # Get the centroid of the object
        bounding_x, bounding_y, w, h = bounding_box(obj)
        centroid_x = bounding_x + w // 2
        centroid_y = bounding_y + h // 2
        
        # Find the closest guide pixel
        closest_pixel = None
        closest_distance = float('inf')
        for px, py in guideline_pixels:
            distance = abs(px - centroid_x) ** 2 + abs(py - centroid_y) ** 2
            if distance < closest_distance:
                closest_pixel = (px, py)
                closest_distance = distance
        
        if closest_pixel:
            draw_line(output_grid, centroid_x, centroid_y, length=None, color=output_grid[closest_pixel], direction=(closest_pixel[0] - centroid_x, closest_pixel[1] - centroid_y))

    return output_grid


def generate_input():
    n, m = np.random.randint(15, 20), np.random.randint(15, 20)
    grid = np.zeros((n, m), dtype=int)

    # Create several objects on grid
    num_objects = np.random.randint(3, 6)
    for _ in range(num_objects):
        w, h = np.random.randint(2, 5), np.random.randint(2, 5)
        color = np.random.choice(list(Color.NOT_BLACK))
        sprite = random_sprite(w, h, density=0.7, color_palette=[color])
        x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK)
        blit_sprite(grid, sprite, x, y)

    # Create a horizontal or vertical guideline on the grid
    if np.random.choice([True, False]):
        # Horizontal line
        y = np.random.randint(1, n - 1)
        for x in range(5, m - 5):
            grid[y, x] = np.random.choice(list(Color.NOT_BLACK))
    else:
        # Vertical line
        x = np.random.randint(1, m - 1)
        for y in range(5, n - 5):
            grid[y, x] = np.random.choice(list(Color.NOT_BLACK))

    return grid