import numpy as np
from typing import *
black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.ndimage import label

# ------------------- API for generating Sprite (use as is, do not modify) -------------------
def apply_symmetry(sprite, symmetry_type):
    """Apply the specified symmetry within the bounds of the sprite."""
    n, m = sprite.shape
    if symmetry_type == 'horizontal':
        for y in range(m):
            for x in range(n // 2):
                sprite[x, y] = sprite[n - 1 - x, y] = sprite[x, y] or sprite[n - 1 - x, y]
    elif symmetry_type == 'vertical':
        for x in range(n):
            for y in range(m // 2):
                sprite[x, y] = sprite[x, m - 1 - y] = sprite[x, y] or sprite[x, m - 1 - y]
    return sprite

def apply_diagonal_symmetry(sprite):
    """Apply diagonal symmetry within the bounds of the sprite. Assumes square sprite."""
    n, m = sprite.shape
    if n != m:
        raise ValueError("Diagonal symmetry requires a square sprite.")
    for x in range(n):
        for y in range(x+1, m):
            sprite[x, y] = sprite[y, x] = sprite[x, y] or sprite[y, x]
    return sprite

def is_contiguous(sprite):
    """Check if a sprite is contiguous using flood fill (labeling approach)."""
    labeled_array, num_features = label(sprite > 0)
    return num_features == 1

def generate_sprite(n, m, symmetry_type, fill_percentage=0.5, max_colors=9, color_palate=None):
    # pick random colors, number of colors follows a geometric distribution truncated at 9
    if color_palate is None:
        n_colors = 1
        while n_colors < max_colors and random.random() < 0.3:
            n_colors += 1
        color_palate = random.sample(range(1, 10), n_colors)
    else:
        n_colors = len(color_palate)
    
    grid = np.zeros((n, m))
    if symmetry_type == "None":
        x, y = random.randint(0, n-1), random.randint(0, m-1)
    elif symmetry_type == 'horizontal':
        x, y = random.randint(0, n-1), m//2
    elif symmetry_type == 'vertical':
        x, y = n//2, random.randint(0, m-1)
    elif symmetry_type == 'diagonal':
        # coin flip for which diagonal orientation
        diagonal_orientation = random.choice([True, False])
        x = random.randint(0, n-1)
        y = x if diagonal_orientation else n - 1 - x

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    color_index = 0
    while np.sum(grid>0) < fill_percentage * n * m:
        grid[x, y] = color_palate[color_index]
        if random.random() < 0.33:
            color_index = random.choice(range(n_colors))
        dx, dy = random.choice(moves)
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < n and 0 <= new_y < m:
            x, y = new_x, new_y

    #return grid

    if symmetry_type == 'horizontal':
        grid = apply_symmetry(grid, 'horizontal')
    elif symmetry_type == 'vertical':
        grid = apply_symmetry(grid, 'vertical')
    elif symmetry_type == 'diagonal':
        
        # diagonal symmetry goes both ways, flip a coin to decide which way
        if diagonal_orientation:
            grid = np.flipud(grid)
            grid = apply_diagonal_symmetry(grid)
            grid = np.flipud(grid)
        else:
            grid = apply_diagonal_symmetry(grid)

    return grid

def generate_fixed_symmetry_sprite(n, m, p, symmetry_type = None, color_palate = None):
    """Generate a contiguous sprite with a fixed symmetry type."""
    # Decide on symmetry type before generating the sprites
    symmetry_types = ['horizontal', 'vertical', 'diagonal', "None"]
    symmetry_type = symmetry_type or random.choice(symmetry_types)
    # color = color or random.randint(1, 9)

    while True:
    # for i in range(100):
        # print ("iiooiioaii", n, m, symmetry_type, color_palate)
        sprite = generate_sprite(n, m, symmetry_type=symmetry_type, color_palate=color_palate)
        assert is_contiguous(sprite), "Generated sprite is not contiguous."
        # check that the sprite has pixels that are flushed with the border
        if np.sum(sprite[0, :]) > 0 and np.sum(sprite[-1, :]) > 0 and np.sum(sprite[:, 0]) > 0 and np.sum(sprite[:, -1]) > 0:
            return sprite
    return sprite

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
    dim1 = random.choice([3, 4])
    dim2 = random.choice([3, 4])
    # print ("calling this", dim1, dim2)
    sprite = generate_fixed_symmetry_sprite(dim1, dim2, 0.5, symmetry_type="None", color_palate=[red])
    # print ("called this")
    # red mass is the number of non-zero pixels in the sprite
    red_mass = np.sum(sprite > 0)
    # put the sprite somewhere random on the grid
    x, y = random.randint(0, n - dim1), random.randint(0, m - dim2)
    # check if the sprite is overlapping with the blue square
    if np.sum(grid[x:x+dim1, y:y+dim2] == blue) > 0:
        return generate_input()
    
    grid[x:x+dim1, y:y+dim2] = sprite

    # check if a column has both colors or a row has both colors
    for i in range(n):
        if blue in grid[i, :] and red in grid[i, :]:
            return grid
    for j in range(m):
        if blue in grid[:, j] and red in grid[:, j]:
            return grid
    print ("failed to line up the pattrerns")
    # return grid
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
    print ("red_indices", red_indices)    
    # the 4 sliding direction of left, up, down, right
    directions = [np.array([0, -1]), np.array([-1, 0]), np.array([1, 0]), np.array([0, 1])]
    # all directions by magnetudes 1, 2, 3, ... maximum amount
    for i in range(1, max(input_grid.shape)):
        for direction in directions:
            # check the slide
            if check_slide(input_grid, direction * i):
                # the slide is 1 less than this
                slide_amt = i - 1
                # get the direction of the slide amt
                slide_vector = direction * slide_amt
                # shift the red sprite by the slide vector
                red_indices = red_indices + slide_vector
                # update the grid
                output_grid = np.zeros_like(input_grid)
                for i in range(len(red_indices)):
                    output_grid[red_indices[i][0], red_indices[i][1]] = red
                # put the blue square back
                blue_indices = np.argwhere(input_grid == blue)
                for i in range(len(blue_indices)):
                    output_grid[blue_indices[i][0], blue_indices[i][1]] = blue
                return output_grid
    assert 0, "No valid slide found"

# ============= remove below this point for prompting =============

if __name__ == '__main__':

    random_input = generate_input()
    print(random_input)

    print (main(random_input))

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

