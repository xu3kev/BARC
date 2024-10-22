from common import *

import numpy as np
from typing import *

# concepts:
# downscaling

# description:
# In the input you will see horizontal and vertical bars/dividers of a particular color that define rectangular regions, with some of the single-pixel vertices colored differently.
# Some rectangular regions are have same color on the four vertices, and some are not.
# To make the output, find the regions colored differently on all vertices and produce a single output pixel of that color in the corresponding part of the output.
# Ignore regions which just have the color of the horizontal and vertical bars at their vertices.

def main(input_grid):
    # Plan:
    # 1. Parse the input into  dividers, regions, and vertices
    # 2. Extract the regions colored differently from the divider on all vertices
    # 3. Produce the output grid by representing each region with a single pixel of the color of its vertices, as long as its color is not the divider

    # 1. Parse the input
    # Detect the objects
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    
    # The divider color is the most frequent non-background color, and the background is black
    divider_color = max(Color.NOT_BLACK, key=lambda color: np.sum(input_grid == color))

    # Detect the single pixels that form the vertices of the regions
    pixels = [ obj for obj in objects if object_colors(obj) != [divider_color] ]
    x_positions = [object_position(obj)[0] for obj in pixels]
    y_positions = [object_position(obj)[1] for obj in pixels]

    # Ignore regions that are not part of those special pixels
    x_min, x_max = min(x_positions), max(x_positions)
    y_min, y_max = min(y_positions), max(y_positions)
    input_grid = input_grid[x_min:x_max+1, y_min:y_max+1]

    # Extract just the black regions delimited by the divider color
    regions = find_connected_components(input_grid, background=divider_color, connectivity=4, monochromatic=True)
    regions = [region for region in regions if object_colors(region, background=divider_color) == [Color.BLACK]]

    # 2. Analyze vertices, which live on the diagonal corners of the regions, to find the color of the regions
    # Determine their colors by the colors of their vertices, so we are going to have to look at the corners
    def diagonal_corners(obj, background):
        x, y, w, h = bounding_box(obj, background)
        return [(x-1, y-1), (x + w, y-1), (x-1, y + h), (x + w, y + h)]
    
    region_colors = []
    for region in regions:
        vertex_colors = { input_grid[x, y] for x, y in diagonal_corners(region, background=divider_color) }
        vertex_colors = set(vertex_colors)
        if len(vertex_colors) == 1 and vertex_colors != {divider_color}:
            region_colors.append(vertex_colors.pop())
        else:
            region_colors.append(Color.BLACK)

    # 3. Produce the output grid, representing each big region as a single pixel
    
    # Find the number distinct X/Y positions of the regions, which tells us the size of the output
    x_positions = sorted({object_position(region, background=divider_color)[0] for region in regions})
    y_positions = sorted({object_position(region, background=divider_color)[1] for region in regions})

    # Make the output
    output_grid = np.full((len(x_positions), len(y_positions)), Color.BLACK)

    for region, color in zip(regions, region_colors):
        x, y = object_position(region, background=divider_color)
        output_grid[x_positions.index(x), y_positions.index(y)] = color
    
    return output_grid
            
def generate_input():
    # We are going to generate square regions
    # Randomly set square size and square number for each row
    # Make sure the grid size is smaller than 30
    square_size = np.random.randint(2, 4)
    square_num = np.random.randint(6, 30 // (square_size + 1))

    # Calculate the grid size
    width = square_size * square_num + square_num - 1
    height = width
    grid = np.full((width, height), Color.BLACK)

    # Randomly set the color of the squares and lines
    n_colors = 4
    divider_color, *other_colors = np.random.choice(Color.NOT_BLACK, n_colors, replace=False)

    # Draw horizontal/vertical lines to separate the square regions
    # First draw the vertical lines
    for x in range(square_size, width, square_size + 1):
        draw_line(grid=grid, x=x, y=0, direction=(0, 1), color=divider_color)
    # Then draw the horizontal lines
    for y in range(square_size, height, square_size + 1):
        draw_line(grid=grid, x=0, y=y, direction=(1, 0), color=divider_color)
    
    # Split the grid into black regions
    regions = find_connected_components(grid=grid, background=divider_color, connectivity=4, monochromatic=True)
    regions = [region for region in regions if object_colors(region, background=divider_color) == [Color.BLACK]]

    # Repeatedly pick random regions and try coloring their vertices with a random color
    # Remember that we can't recolor a vertex that is already colored differently from the divider
    # Vertices are at diagonal corners, so define helper for this
    def diagonal_corners(obj, background):
        x, y, w, h = bounding_box(obj, background)
        return [(x-1, y-1), (x + w, y-1), (x-1, y + h), (x + w, y + h)]
    # check to make sure that we only consider regions whose corners are in the canvas
    regions = [region for region in regions
               if all(0 <= x < width and 0 <= y < height for x, y in diagonal_corners(region, background=divider_color))]
    for _ in range(6):
        region = random.choice(regions)
        vertex_colors = { grid[x, y] for x, y in diagonal_corners(region, background=divider_color) }
        # Pick the color, remembering that we can't recolor a vertex that is already colored differently from the divider
        vertex_colors = vertex_colors - {divider_color}
        if len(vertex_colors) == 0:
            new_color = np.random.choice(other_colors)
        elif len(vertex_colors) == 1:
            new_color = vertex_colors.pop()
        elif len(vertex_colors) > 1:
            continue

        # Color the vertices
        for x, y in diagonal_corners(region, background=divider_color):
            grid[x, y] = new_color
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
