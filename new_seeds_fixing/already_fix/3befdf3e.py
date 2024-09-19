from common import *
import numpy as np
from typing import *

# concepts:
# growing, color change

# description:
# In the input you will see square(s) with a single pixel border around them in a different color.
# To make the output, swap the color between the square and the border, 
# and then put rectangles on the edges of the border whose width is the same as the length of the inner square, 
# and whose color is the same as the border in the input image.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Get the output grid with the same size as the input grid.
    output_grid = np.copy(input_grid)

    # Detect the square pattern in the input grid.
    entire_square = find_connected_components(grid=input_grid, connectivity=4, monochromatic=False)
    for each_square in entire_square:
        # Detect the inner and outer squares in the pattern.
        object_square = find_connected_components(grid=each_square, connectivity=4, monochromatic=True)

        # Split the square pattern into inner and outer squares.
        split_objects = []
        for obj in object_square:
            x, y, width, height = bounding_box(grid=obj)
            shape = crop(grid=obj)
            color = obj[x, y]
            split_objects.append({'x': x, 'y': y, 'len': width, 'color': color, 'shape': shape})

        # Get the outer and inner square by comparing their size.
        if split_objects[0]['len'] > split_objects[1]['len']:
            outer_square = split_objects[0]
            inner_square = split_objects[1]
        else:
            outer_square = split_objects[1]
            inner_square = split_objects[0]
        
        # Swap the color between the inner and outer squares.
        outer_square_pattern, inner_square_pattern = outer_square['shape'], inner_square['shape']
        outer_square_pattern[outer_square_pattern == outer_square['color']] = inner_square['color']
        inner_square_pattern[inner_square_pattern == inner_square['color']] = outer_square['color']

        # Draw the inner and outer squares after swaping on the output grid.
        output_grid = blit_sprite(grid=output_grid, sprite=outer_square_pattern, x=outer_square['x'], y=outer_square['y'])
        output_grid = blit_sprite(grid=output_grid, sprite=inner_square_pattern, x=inner_square['x'], y=inner_square['y'])

        # Draw the rectangle as growing from outer square, the width is the same as the length of the inner square.
        # The rectangle is the same color as the original outer square.
        rectangle_width, rectangle_height = outer_square['len'], inner_square['len']  
        
        # Create the rectangle pattern for the edges of the outer square.
        rectangle_up_down = np.full((rectangle_width, rectangle_height), outer_square['color'])
        rectangle_left_right = np.full((rectangle_height, rectangle_width), outer_square['color'])

        # Draw the rectangle on the four edges of the outer square.
        output_grid = blit_sprite(grid=output_grid, sprite=rectangle_up_down, x=outer_square['x'], y=outer_square['y'] - inner_square['len'])
        output_grid = blit_sprite(grid=output_grid, sprite=rectangle_up_down, x=outer_square['x'], y=outer_square['y'] + outer_square['len'])
        output_grid = blit_sprite(grid=output_grid, sprite=rectangle_left_right, x=outer_square['x'] - inner_square['len'], y=outer_square['y'])
        output_grid = blit_sprite(grid=output_grid, sprite=rectangle_left_right, x=outer_square['x'] + outer_square['len'], y=outer_square['y'])

    return output_grid

def generate_input():
    # Generate the background grid with size of n x n.
    grid_len = random.randint(24, 30)
    n, m = grid_len, grid_len
    grid = np.zeros((n, m), dtype=int)

    # Randomly select the number of square pattern.
    num_square = random.randint(1, 2)

    # Ensure there is enough space for the square pattern to grow.
    max_square_len = grid_len // (num_square * 3)

    # Choose two colors for inner and outer square, and one color represents the boundary.
    # The boundary is used for leave enough space for the square pattern in output to grow.
    available_color = Color.NOT_BLACK.copy()
    two_colors = random.sample(available_color, k=2)
    available_color.remove(two_colors[0])
    available_color.remove(two_colors[1])
    boundary_color = available_color[0]

    for _ in range(num_square):
        # Randomly select the size of the square pattern.
        # The outer square is the inner square with a single pixel border around it.
        outer_square_len = random.randint(3, max_square_len)
        inner_square_len = outer_square_len - 2

        # The square will grow inner_square_len in four directions
        border_len = outer_square_len + inner_square_len * 2
        
        # Create the inner square, outer square, and border.
        outer_square = random_sprite(n=outer_square_len, m=outer_square_len, color_palette=[two_colors[1]], density=1.0)
        inner_square = random_sprite(n=inner_square_len, m=inner_square_len, color_palette=[two_colors[0]], density=1.0)
        border = random_sprite(n=border_len, m=border_len, color_palette=[boundary_color], density=1.0)
        
        # Get a random free location for the pattern
        posx, posy = random_free_location_for_sprite(grid=grid, sprite=border)

        # Draw the square pattern on the grid
        grid = blit_sprite(grid=grid, sprite=border, x=posx, y=posy)
        grid = blit_sprite(grid=grid, sprite=outer_square, x=posx + inner_square_len, y=posy + inner_square_len)
        grid = blit_sprite(grid=grid, sprite=inner_square, x=posx + inner_square_len + 1, y=posy + inner_square_len + 1)
    
    # Remove the boundary color from the grid
    grid = np.where(grid == boundary_color, Color.BLACK, grid)
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
