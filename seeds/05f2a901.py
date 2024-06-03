from common import *
import numpy as np
from typing import *
black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)
all_colors = range(10)

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.ndimage import label



# --------------------- input generator ---------------------
def generate_input():
    # make a black grid first as background, roughly 5 x 5 to 10x10 works
    n, m = random.randint(5, 20), random.randint(5, 20)
    grid = np.zeros((n, m), dtype=int)

    # make a 2x2 blue square, put it somewhere random on the grid
    x, y = random.randint(0, n - 2), random.randint(0, m - 2)
    grid[x:x+2, y:y+2] = blue
    blue_mass = 2 * 2

    # make a random sprite of [2,3,4] x [2,3,4] with a random symmetry type
    sprite = random_sprite([3,4], [3,4], symmetry="not_symmetric", color_palette=[red])

    # put the sprite somewhere random on the grid
    x, y = random_free_location_for_object(grid, sprite, background=black)

    blit(grid, sprite, x, y, transparent=black)    

    # check if a column has both colors or a row has both colors
    for i in range(n):
        if blue in grid[i, :] and red in grid[i, :]:
            return grid
    for j in range(m):
        if blue in grid[:, j] and red in grid[:, j]:
            return grid
    
    # if not, try again
    return generate_input()


def check_slide(grid, direction):
    # grab the indices of the red sprite
    red_indices = np.argwhere(grid == red)
    # update every index based on the direction
    for i in range(len(red_indices)):
        red_indices[i] = red_indices[i] + direction
    # check if any of the updated indices are out of bounds
    for i in range(len(red_indices)):
        if red_indices[i][0] < 0 or red_indices[i][0] >= grid.shape[0] or red_indices[i][1] < 0 or red_indices[i][1] >= grid.shape[1]:
            return False
    # check if any of the updated indices are blue
    for i in range(len(red_indices)):
        if grid[red_indices[i][0], red_indices[i][1]] == blue:
            return True
    return False

def main(input_grid):

    # get the index of the red sprite from the grid
    red_indices = np.argwhere(input_grid == red)

    # get just the blue object
    blue_object = np.zeros_like(input_grid)
    blue_object[input_grid == blue] = blue

    # get just the red object
    red_object = np.zeros_like(input_grid)
    red_object[input_grid == red] = red
    
    # the 4 sliding direction of left, up, down, right
    directions = [np.array([0, -1]), np.array([-1, 0]), np.array([1, 0]), np.array([0, 1])]
    # all directions by magnetudes 1, 2, 3, ... maximum amount
    for i in range(1, max(input_grid.shape)):
        for direction in directions:
            dx, dy = direction * i
            if collision(object1=blue_object, object2=red_object, x2=dx, y2=dy):
                dx, dy = direction * (i-1)
                output_grid = np.copy(blue_object)
                blit(output_grid, red_object, dx, dy, transparent=black)
                return output_grid
            
    assert 0, "No valid slide found"

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)

    # sprite = generate_fixed_symmetry_sprite(4, 3, 0.5, symmetry_type="None", color_palate=[red])
    # print(sprite)

    # Generate and display 10 random contiguous symmetric sprites with a fixed symmetry type
    # N,M,Ds=10,10,[3,5,8,10,20]
    # fig, axes = plt.subplots(N, M, figsize=(15, 6))
    # for i in range(N):
    #     for j in range(M):
    #         D = random.choice(Ds)
    #         sprite = generate_fixed_symmetry_sprite(D, D, 0.5, color_palate=[red])
    #         # generate a good color map with 0=black and 1-9 different colours
    #         # black, blue, red, green, yellow, grey, pink, orange, teal, maroon
    #         cmap = plt.cm.colors.ListedColormap(['black', 'red', 'blue', 'green', 'yellow', 'grey', 'pink', 'orange', 'teal', 'maroon'])
    #         axes[i, j].imshow(sprite, cmap=cmap, vmin=0, vmax=9)
    #         axes[i, j].axis('off')

    # plt.tight_layout()
    # plt.show()

