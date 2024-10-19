from common import *
import numpy as np
from typing import *

# concepts:
# counting, dividers, filling

# description:
# In the input you will see grey horizontal and vertical bars that divide rectangular regions. Each rectangular region is black with some colored pixels added.
# To make the output, fill the rectangular region with the most colored pixels. Fill it with is color. Fill the other rectangular regions with black.   

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create a copy of the input grid to avoid modifying the original
    output_grid = np.copy(input_grid)  

    # Get all the rectangular regions seperated by horizontal and vertical dividers
    # The dividers are colored grey, but more generally their color is just whatever color stretches all the way horizontally or vertically
    for x in range(input_grid.shape[0]):
        if np.all(input_grid[x, :] == input_grid[x, 0]):
            divider_color = input_grid[x, 0]
            break
    # For this problem you could also do: divider_color = Color.GRAY
    regions = find_connected_components(grid=output_grid, background=divider_color, monochromatic=False, connectivity=4)

    # Find the region with the most colored pixels inside of it
    num_colored_pixels = [ np.sum((region != divider_color) & (region != Color.BLACK)) for region in regions ]
    max_colored_pixels = max(num_colored_pixels)

    # Fill the region with the most colored pixels with its color
    # Fill the other regions with black
    for region_obj in regions:
        # Figure out if it is one of the max colored regions to determine what the target color is that we are going to fill with
        num_colored_pixels_in_this_region = np.sum((region_obj != divider_color) & (region_obj != Color.BLACK))
        if num_colored_pixels_in_this_region == max_colored_pixels:
            colors = [ color for color in object_colors(region_obj, background=divider_color) if color != Color.BLACK ]
            assert len(colors) == 1, "Each region should have only one color"
            target_color = colors[0]
        else:
            target_color = Color.BLACK

        # Fill the region with the target color
        output_grid[region_obj != divider_color] = target_color

    return output_grid

def generate_input() -> np.ndarray:
    # Define the base cofiguration of the grid seperated by chessboard lines
    # Randomly select the size of the squares, create a 3x3 grid of squares
    region_len = np.random.choice([4, 5, 7])
    interior_len = region_len - 2
    region_num = 3

    # Size of the grid is grid length plus line length
    n, m = region_len * region_num + region_num - 1, region_len * region_num + region_num - 1
    grid = np.zeros((n, m), dtype=int)

    # Select two distinct colors for the lines and the pattern
    divider_color, interior_color = np.random.choice(Color.NOT_BLACK, 2, replace=False) 

    # Fill rows and columns with the divider color
    for i in range(region_len, n, region_len + 1):
        draw_line(grid=grid, x=i, y=0, color=divider_color, direction=(0, 1))
        draw_line(grid=grid, x=0, y=i, color=divider_color, direction=(1, 0))

    # Add different density of pixels to each square
    for x in range(0, n, region_len + 1):
        for y in range(0, m, region_len + 1):
            # Randomly select the density of the square
            square_background = np.zeros((interior_len, interior_len), dtype=int)
            density = np.random.randint(1, interior_len * interior_len) / (interior_len * interior_len)

            # Randomly scatter the color in the square
            square_background = randomly_scatter_points(square_background, color=interior_color, density=density)
            blit_sprite(grid, square_background, x, y)
        
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)