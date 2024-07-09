from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, symmetry detection, pixel manipulation, objects

# description:
# In the input you will see a grid consisting of two different colored sprites (red and blue) that are repeatedly translated diagonally, forming a pattern of alternating sprites.
# To make the output:
# 1. Detect the translational symmetry of each sprite separately
# 2. Expand the grid to be a perfect square (the larger of width or height)
# 3. Continue the pattern of alternating sprites in both directions (up-left and down-right)
# 4. For each sprite, count the number of complete sprites of that color in the expanded grid
# 5. If the count of red sprites is greater, change all blue sprites to green. If the count of blue sprites is greater, change all red sprites to yellow. If counts are equal, leave colors unchanged.

def main(input_grid):
    # Plan:
    # 1. Separate red and blue sprites
    # 2. Find the repeated translation for each color
    # 3. Expand the grid to a square
    # 4. Continue the pattern in both directions
    # 5. Count complete sprites of each color
    # 6. Change colors based on the count

    red_grid = np.where(input_grid == Color.RED, Color.RED, Color.BLACK)
    blue_grid = np.where(input_grid == Color.BLUE, Color.BLUE, Color.BLACK)

    red_symmetries = detect_translational_symmetry(red_grid, ignore_colors=[Color.BLACK])
    blue_symmetries = detect_translational_symmetry(blue_grid, ignore_colors=[Color.BLACK])

    assert len(red_symmetries) > 0 and len(blue_symmetries) > 0, "No translational symmetry found"

    # Expand to square grid
    new_size = max(input_grid.shape[0], input_grid.shape[1])
    output_grid = np.full((new_size, new_size), Color.BLACK)

    # Continue pattern in both directions
    for color, symmetries in [(Color.RED, red_symmetries), (Color.BLUE, blue_symmetries)]:
        for x, y in np.argwhere(input_grid == color):
            for x2, y2 in orbit(output_grid, x, y, symmetries):
                if 0 <= x2 < new_size and 0 <= y2 < new_size:
                    output_grid[x2, y2] = color

    # Count complete sprites
    red_sprite = find_connected_components(red_grid, monochromatic=True)[0]
    blue_sprite = find_connected_components(blue_grid, monochromatic=True)[0]

    red_count = count_complete_sprites(output_grid, red_sprite, Color.RED)
    blue_count = count_complete_sprites(output_grid, blue_sprite, Color.BLUE)

    # Change colors based on count
    if red_count > blue_count:
        output_grid[output_grid == Color.BLUE] = Color.GREEN
    elif blue_count > red_count:
        output_grid[output_grid == Color.RED] = Color.YELLOW

    return output_grid

def count_complete_sprites(grid, sprite, color):
    count = 0
    for x in range(grid.shape[0] - sprite.shape[0] + 1):
        for y in range(grid.shape[1] - sprite.shape[1] + 1):
            if np.all(grid[x:x+sprite.shape[0], y:y+sprite.shape[1]] == sprite):
                count += 1
    return count

def generate_input():
    # Grid size between 5x5 and 10x10
    n, m = np.random.randint(5, 11), np.random.randint(5, 11)
    grid = np.full((n, m), Color.BLACK)

    # Create two sprites: red and blue
    red_sprite = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), 
                               symmetry="not_symmetric", color_palette=[Color.RED], density=0.6)
    blue_sprite = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), 
                                symmetry="not_symmetric", color_palette=[Color.BLUE], density=0.6)

    # Place sprites in a diagonal pattern
    x, y = 0, 0
    while x < n and y < m:
        if np.random.choice([True, False]):
            blit_sprite(grid, red_sprite, x, y)
            x += red_sprite.shape[0]
            y += red_sprite.shape[1]
        else:
            blit_sprite(grid, blue_sprite, x, y)
            x += blue_sprite.shape[0]
            y += blue_sprite.shape[1]

    return grid