from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, sprites, alignment by color

# description:
# In the input, you will see several objects of different colors scattered around a black background.
# Each object is a sprite that has either horizontal, vertical, or rotational symmetry.
# The goal is to find all objects of the same color, align them by their centers of symmetry,
# and overlay them to create a new, larger symmetric sprite for each color.
# The output should contain these new sprites, arranged from left to right in order of increasing size.

def main(input_grid):
    # Find all objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8)

    # Group objects by color
    color_groups = {}
    for obj in objects:
        color = next(c for c in np.unique(obj) if c != Color.BLACK)
        if color not in color_groups:
            color_groups[color] = []
        color_groups[color].append(obj)

    # Process each color group
    combined_sprites = []
    for color, group in color_groups.items():
        # Find the largest dimensions among all sprites of this color
        max_height = max(obj.shape[0] for obj in group)
        max_width = max(obj.shape[1] for obj in group)
        
        # Create a canvas for combining sprites
        combined = np.zeros((max_height, max_width), dtype=int)
        
        for obj in group:
            # Determine the type of symmetry
            if np.array_equal(obj, np.flipud(obj)):
                symmetry = 'horizontal'
            elif np.array_equal(obj, np.fliplr(obj)):
                symmetry = 'vertical'
            elif np.array_equal(obj, np.rot90(obj, 2)):
                symmetry = 'rotational'
            else:
                continue  # Skip non-symmetric objects
            
            # Find the center of symmetry
            h, w = obj.shape
            center_y, center_x = h // 2, w // 2
            
            # Calculate the position to place this object
            y = (max_height - h) // 2
            x = (max_width - w) // 2
            
            # Overlay the object onto the combined sprite
            combined[y:y+h, x:x+w] = np.where(obj != Color.BLACK, obj, combined[y:y+h, x:x+w])
        
        combined_sprites.append((combined, color))

    # Sort combined sprites by size (total non-black pixels)
    combined_sprites.sort(key=lambda x: np.sum(x[0] != Color.BLACK))

    # Create the output grid
    total_width = sum(sprite.shape[1] for sprite, _ in combined_sprites) + len(combined_sprites) - 1
    max_height = max(sprite.shape[0] for sprite, _ in combined_sprites)
    output_grid = np.zeros((max_height, total_width), dtype=int)

    # Place the combined sprites in the output grid
    x = 0
    for sprite, color in combined_sprites:
        h, w = sprite.shape
        y = (max_height - h) // 2
        output_grid[y:y+h, x:x+w] = sprite
        x += w + 1  # Add 1 for spacing between sprites

    return output_grid

def generate_input():
    grid = np.zeros((20, 20), dtype=int)
    colors = list(Color.NOT_BLACK)
    np.random.shuffle(colors)
    
    for color in colors[:3]:  # Use 3 random colors
        num_sprites = np.random.randint(2, 4)
        for _ in range(num_sprites):
            size = np.random.randint(3, 6)
            symmetry = np.random.choice(['horizontal', 'vertical', 'radial'])
            sprite = random_sprite(size, size, symmetry=symmetry, color_palette=[color], connectivity=8)
            
            try:
                x, y = random_free_location_for_sprite(grid, sprite, padding=1)
                blit_sprite(grid, sprite, x, y)
            except:
                pass  # Skip if can't place

    return grid