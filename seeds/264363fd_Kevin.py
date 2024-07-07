from common import *

import numpy as np
from typing import *

# concepts:
# objects, growing, pixel manipulation

# description:
# In the input you will see a small multicolor object, and a few big rectangles. Each rectangle has a few colored pixels sprinkled inside it. The background is NOT black.
# To make the output:
# 1. Remove the small object from the input
# 2. Place copies of the small object centered on top of the colored pixels sprinkled inside the rectangles
# 3. The small object has pointy things sticking out of it. Extend each pointy thing outward until it hits the edge of the rectangle

def main(input_grid):
    # Plan:
    # 1. Figure out the background color. Replace it with black (we'll swap it back later)
    # 2. Find the small object and delete it
    # 3. Identify the pointy things sticking out of the small sprite, and what their displacement vectors are
    # 4. For each rectangle, find the colored pixels inside it, put copies and extend the pointy things

    # For these inputs, background color is the most common color
    background_color = np.argmax(np.bincount(input_grid.flatten()))
    # Replace the background color with black
    input_grid[input_grid == background_color] = Color.BLACK

    # 2. Find the small object and delete it
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)
    smallest_object = min(objects, key=lambda x: np.count_nonzero(x))
    input_grid[smallest_object != Color.BLACK] = Color.BLACK    

    # Crop the object to get its sprite, and then decide if something is pointing:
    # Pointy means a pixel on the edge with its other edge-neighbors black
    sprite = crop(smallest_object)
    pointy_positions = get_points(sprite)    
    
    # 4. For each rectangle, find the colored pixels inside it, put copies and extend the pointy things
    output_grid = np.copy(input_grid)
    rectangles = find_connected_components(input_grid, monochromatic=False, connectivity=8)
    for rectangle in rectangles:
        # Figure out the most common color of the rectangle (apart from black, which is the background)
        main_rectangle_color = max(Color.NOT_BLACK, key=lambda x: np.count_nonzero(rectangle == x))
        colored_pixels = np.where((rectangle != Color.BLACK) & (rectangle != main_rectangle_color))
        for x, y in zip(*colored_pixels):
            # Place a copy of the sprite centered on the colored pixel. If any of the sprite goes out of bounds, crop it to the legal region (inside the rectangle)
            blit_sprite(output_grid, sprite, x - sprite.shape[0]//2, y - sprite.shape[1]//2, background=Color.BLACK)
            # bounds check accomplished by overwriting with black
            output_grid[input_grid == Color.BLACK] = Color.BLACK

            
            for point_x, point_y in pointy_positions:                
                # Extend the pointy things
                # Get the direction and color of the pointy thing, relative to the sprite
                dx, dy = np.sign([point_x - sprite.shape[0]//2, point_y - sprite.shape[1]//2])
                dx, dy = int(dx), int(dy)
                color = sprite[point_x, point_y]
                draw_line(output_grid, x + dx, y + dy, length=None, direction=(dx, dy), color=color, stop_at_color=[Color.BLACK])


    # Swap the background color back
    output_grid[output_grid == Color.BLACK] = background_color

    return output_grid

def get_points(sprite):
    """
    Returns the positions of the pointy things sticking out of the sprite.
    Something is pointy if it is on the edge the sprite, and both of its neighboring edge pixels are black
    """
    edge_indices = get_edge_indices(sprite)
    next_neighbor, previous_neighbor = edge_indices[1:] + edge_indices[:1], edge_indices[-1:] + edge_indices[:-1]
    pointy_positions = [ (x, y) for (x, y), (next_x, next_y), (prev_x, prev_y) in zip(edge_indices, next_neighbor, previous_neighbor)
                         if sprite[x, y] != Color.BLACK and sprite[next_x, next_y] == Color.BLACK and sprite[prev_x, prev_y] == Color.BLACK ]
    return pointy_positions

def get_edge_indices(sprite):
    """Returns a list of all the (i,j) locations of the edge pixels"""
    edge_indices = [ (x, 0) for x in range(sprite.shape[0]) ]
    edge_indices.extend([ (sprite.shape[0]-1, y) for y in range(1, sprite.shape[1]) ])
    edge_indices.extend([ (x, sprite.shape[1]-1) for x in range(sprite.shape[0]-2, -1, -1) ])
    edge_indices.extend([ (0, y) for y in range(sprite.shape[1]-2, 0, -1) ])
    return edge_indices

def generate_input():
    background_color = random.choice(Color.NOT_BLACK)
    rectangle_color = random.choice([color for color in Color.NOT_BLACK if color != background_color])
    marker_color = random.choice([color for color in Color.NOT_BLACK if color != background_color and color != rectangle_color])

    # Make the sprite, and then add pointy things to it
    w, h = random.choice([2, 3]), random.choice([2,3])
    sprite = random_sprite(w, h, symmetry="not_symmetric",
                            color_palette=[color for color in Color.NOT_BLACK if color not in [background_color, rectangle_color, marker_color]])
    # put a ring of black pixels around the sprite and then color some of them to be pointing
    sprite = np.pad(sprite, 1, constant_values=Color.BLACK)
    w, h = sprite.shape
    possible_pointy_positions = [ (w//2, 0), (w-1, h//2), (w//2, h-1), (0, h//2) ]
    pointy_positions = random.sample(possible_pointy_positions, np.random.randint(1, 4))
    for x, y in pointy_positions:
        sprite[x, y] = random.choice([color for color in Color.NOT_BLACK if color not in [background_color, rectangle_color, marker_color]])
    sprite = crop(sprite)
    
    # Make the grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.full((n, m), Color.BLACK)
    
    # Make the rectangles
    n_rectangles = random.choice([1, 2])
    for _ in range(n_rectangles):
        w, h = np.random.randint(n//3, 2*n//3), np.random.randint(m//3, 2*m//3)
        rectangle_sprite = np.full((w, h), rectangle_color)
        # sprinkle some colored pixels
        for _ in range(random.choice([1, 2, 3])):
            x, y = np.random.randint(1, w-1), np.random.randint(1, h-1)
            rectangle_sprite[x, y] = marker_color
        x, y = random_free_location_for_sprite(grid, rectangle_sprite, padding=1, padding_connectivity=8)
        blit_sprite(grid, rectangle_sprite, x, y)

    # Place the sprite in the grid
    x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8)
    blit_sprite(grid, sprite, x, y)

    # Change the background
    grid[grid == Color.BLACK] = background_color

    return grid
# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
