from common import *
import numpy as np
from typing import *

# concepts:
# pattern recognition, pattern reconstruction

# description:
# In the input you will see a grid with one original color pattern and other incomplete patterns.
# To make the output grid, you should find the red and yellow indicator of original color pattern and 
# complete the incomplete patterns to the same pattern of the original color pattern.

def main(input_grid: np.ndarray) -> np.ndarray:
    grid = np.copy(input_grid)
    
    # Extract the colored objects and their boundary from grid
    objects = detect_objects(grid = grid, connectivity = 4)
    object_boundary = [bounding_box(grid = x) for x in objects]
    index = [i for i, sublist in enumerate(objects) if Color.GREEN in sublist][0]
    boundary = object_boundary[index]
    sprite = grid[boundary[0] : boundary[0] + boundary[2], boundary[1] : boundary[1] + boundary[3]]

    # Place the sub-pattern back into the grid
    for i in range(len(objects)):
        if i == index:
            continue
        for j in range(0, 2):
            sprite = np.fliplr(sprite)
            for k in range(0, 4):
                sprite = np.rot90(sprite, k = -1)
                sprite_red_pos = np.argwhere(sprite == Color.RED)[0]
                object_red_pos = [(x, y) for x, sublist in enumerate(objects[i]) for y, element in enumerate(sublist) if element == Color.RED][0]
                if (object_red_pos[0] < sprite_red_pos[0] or len(sprite) - sprite_red_pos[0] + object_red_pos[0] > len(grid) or
                    object_red_pos[1] < sprite_red_pos[1] or len(sprite[0]) - sprite_red_pos[1] + object_red_pos[1] > len(grid[0])):
                    continue
                
                flag = True
                for x in range(len(sprite)):
                    for y in range(len(sprite[0])):
                        mapping_x, mapping_y = x - sprite_red_pos[0] + object_red_pos[0], y - sprite_red_pos[1] + object_red_pos[1]
                        if sprite[x, y] == Color.YELLOW and grid[mapping_x, mapping_y] != Color.YELLOW:
                            flag = False
                if flag:
                    blit(grid = grid, sprite = sprite, x = object_red_pos[0] - sprite_red_pos[0], y = object_red_pos[1] - sprite_red_pos[1])
                    break

    return grid

def generate_input() -> np.ndarray:
    # Create a base yellow grid with random dimensions
    n, m = random.randint(3, 5), random.randint(3, 5)
    grid = random_sprite(n, m, color_palette=[Color.YELLOW])
    colors = [Color.RED] + [Color.BLUE] * random.randint(2, 4) + [Color.GREEN] * random.randint(2, 4)
    
    # Place the other colored tiles around, adjacent to the originally colored tiles
    for c in colors:
        while True:
            # Adjacent to the originally colored tiles
            x = random.randint(0, len(grid) - 1)
            y = random.randint(0, len(grid[0]) - 1)
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            dx, dy = direction[0], direction[1]
            if (grid[x, y] != Color.BLACK and
                (x + dx < 0 or x + dx >= len(grid) or
                y + dy < 0 or y + dy >= len(grid[0]) or
                grid[x + dx, y + dy] == Color.BLACK)):
                
                # Check (x + dx, y + dy) in the boundary of grid, and extand grid if not
                if x + dx < 0:
                    x = x + 1
                    empty_row = np.zeros(len(grid[0]), dtype=int)
                    grid = np.vstack([empty_row, grid])
                if x + dx >= len(grid):
                    empty_row = np.zeros(len(grid[0]), dtype=int)
                    grid = np.vstack([grid, empty_row])
                if y + dy < 0:
                    y = y + 1
                    empty_col = np.zeros((grid.shape[0], 1), dtype=int)
                    grid = np.hstack([empty_col, grid])
                if y + dy >= len(grid[0]):
                    empty_col = np.zeros((grid.shape[0], 1), dtype=int)
                    grid = np.hstack([grid, empty_col])

                grid[x + dx, y + dy] = c
                break

    # Create a larger grid and place multiple patterns
    sprite = grid.copy()
    no_red = grid.copy()
    no_red[no_red == Color.BLUE] = Color.BLACK
    no_red[no_red == Color.GREEN] = Color.BLACK

    # Initialize the input_grid and the flag array to mark the occupied grids
    init_width, init_height = 10, 10
    flag_arr = np.zeros((init_width, init_height), dtype=int)
    grid = np.zeros((init_width, init_height), dtype=int)

    for i in range(random.randint(3, 4)):
        put_sprite = sprite.copy() if i == 0 else no_red.copy()

        # It is possible to perform mirroring and rotation
        if random.randint(0, 1) == 0:
            put_sprite = np.fliplr(put_sprite)
        put_sprite = np.rot90(put_sprite, k=-1 * random.randint(0, 3))
        while True:
            # Try to place the sprite
            flag = False
            for j in range(20):
                x = random.randint(1, len(grid) - len(put_sprite) - 1)
                y = random.randint(1, len(grid[0]) - len(put_sprite[0]) - 1)
                sub_flag_arr = flag_arr[x - 1 : x + len(put_sprite) + 1, y - 1 : y + len(put_sprite[0]) + 1]
                if np.all(sub_flag_arr == 0):
                    flag = True
                    blit_sprite(grid, put_sprite, x, y)
                    sub_flag_arr.fill(1)
                    blit_sprite(flag_arr, sub_flag_arr, x - 1, y - 1)
                    break
            
            # If placement fails, try expanding the final input.
            if not flag:
                new_grid = np.zeros((len(grid) * 2, len(grid[0]) * 2), dtype=int)
                new_flag_arr = np.zeros((len(grid) * 2, len(grid[0]) * 2), dtype=int)
                blit_sprite(new_grid, grid, 0, 0)
                blit_sprite(new_flag_arr, flag_arr, 0, 0)
                grid = new_grid
                flag_arr = new_flag_arr
            else:
                break
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
