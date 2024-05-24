import numpy as np
from typing import *
black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

def flood_fill_at_coord(grid, x, y, color):
    """
    Given a grid, a coordinate (x, y) and a color, this function fills the region of the grid that contains the coordinate
    (x, y) with the given color.
    
    Args:
    1. grid: np.ndarray - A numpy array representing the input grid.
    2. x: int - An integer representing the x-coordinate of the point to start the flood fill at.
    3. y: int - An integer representing the y-coordinate of the point to start the flood fill at.
    4. color: int - An integer representing the color to fill the region with.
    
    Returns:
    None
    """
    if x < 0 or x >= grid.shape[0] or y < 0 or y >= grid.shape[1]:
        return
    if grid[x, y] != black:
        return
    grid[x, y] = color
    flood_fill_at_coord(grid, x + 1, y, color)
    flood_fill_at_coord(grid, x - 1, y, color)
    flood_fill_at_coord(grid, x, y + 1, color)
    flood_fill_at_coord(grid, x, y - 1, color)

def make_input1():
    # first make a 20 x 20 black grid
    grid = np.zeros((20, 20), dtype=int)
    # then make the jail cells . . .
    # make horizontal bars skipping every 2, use yellow for bars
    for i in range(0, 20, 3):
        grid[i, 0:20] = yellow
    # make vertical bars skipping every 2, use yellow for bars
    for j in range(0, 20, 3):
        grid[0:20, j] = yellow

    # for the big cell coordinate 4, 4, convert it into grid coordinate
    x, y = 4 * 3 + 1, 4 * 3 + 1
    # floodfill it to be red in that cell
    flood_fill_at_coord(grid, x, y, red)

    # do the same, but at big coordinate 2, 4, use red
    x, y = 2 * 3 + 1, 4 * 3 + 1
    flood_fill_at_coord(grid, x, y, red)

    # make 2 green jail cells at big coordinate 1, 2 and 5, 2
    x, y = 1 * 3 + 1, 2 * 3 + 1
    flood_fill_at_coord(grid, x, y, green)
    x, y = 5 * 3 + 1, 2 * 3 + 1
    flood_fill_at_coord(grid, x, y, green)

    return grid

def make_input2():
    # do the same as make_input1, but use green for jail bars
    # use blue for the big cells
    grid = np.zeros((20, 20), dtype=int)
    for i in range(0, 20, 3):
        grid[i, 0:20] = green
    for j in range(0, 20, 3):
        grid[0:20, j] = green
    # fill the big coordinate at 4, 4 and 4, 6 with blue
    x, y = 4 * 3 + 1, 4 * 3 + 1
    flood_fill_at_coord(grid, x, y, blue)
    x, y = 4 * 3 + 1, 6 * 3 + 1
    flood_fill_at_coord(grid, x, y, blue)

    # fill the big coordinate at 3, 2 and 5, 2 with red
    x, y = 3 * 3 + 1, 2 * 3 + 1
    flood_fill_at_coord(grid, x, y, red)
    x, y = 5 * 3 + 1, 2 * 3 + 1
    flood_fill_at_coord(grid, x, y, red)

    return grid

# abstract the input generation as a function with arguments
# jail size, bar color, and two cell colors cell_color1 and cell_color2,
# along with 2 pairs of coordinates for the big cells
def make_input(jail_size, bar_color, group_coords_with_colors):
    grid = np.zeros((20, 20), dtype=int)
    for i in range(0, 20, jail_size + 1):
        grid[i, 0:20] = bar_color
    for j in range(0, 20, jail_size + 1):
        grid[0:20, j] = bar_color
    for group_coords in group_coords_with_colors:
        x1, y1 = group_coords[0]
        x2, y2 = group_coords[1]
        color = group_coords[2]
        x, y = x1 * (jail_size + 1) + 1, y1 * (jail_size + 1) + 1
        flood_fill_at_coord(grid, x, y, color)
        x, y = x2 * (jail_size + 1) + 1, y2 * (jail_size + 1) + 1
        flood_fill_at_coord(grid, x, y, color)

    return grid

# abstract the input generation as a function with no arguments
# instead, use random values for the arguments
def make_input_random():
    jail_size = np.random.randint(2, 5)
    bar_color = np.random.randint(1, 10)
    cell_color1 = np.random.randint(1, 10)
    cell_color2 = np.random.randint(1, 10)

    # compute the biggest possible coordinates for the big cells
    max_x = 20 // (jail_size + 1) - 1
    max_y = 20 // (jail_size + 1) - 1

    def make_big_group_coords():
        # decide if it is horizontal or vertical
        is_horizontal = np.random.random() < 0.5
        # if horizontal, pick one Y and two X
        if is_horizontal:
            y = np.random.randint(0, max_y)
            x1 = np.random.randint(0, max_x)
            x2 = np.random.randint(0, max_x)
            return (x1, y), (x2, y)
        # if vertical, pick one X and two Y
        else:
            x = np.random.randint(0, max_x)
            y1 = np.random.randint(0, max_y)
            y2 = np.random.randint(0, max_y)
            return (x, y1), (x, y2)
        
    # make 2 gropus of big cells, with colors
    group1_coords_with_colors = make_big_group_coords() + (cell_color1,)
    group2_coords_with_colors = make_big_group_coords() + (cell_color2,)

    return make_input(jail_size, bar_color, [group1_coords_with_colors, group2_coords_with_colors])

if __name__ == '__main__':
    input_grids = [make_input1(), make_input2(), make_input_random(), make_input_random()]
   

    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, len(input_grids))
    for _, input_grid in enumerate(input_grids):
        # use the color scheme listed above to color the grid
        colored_grid = np.zeros(input_grid.shape + (3,), dtype=int)
        for i in range(input_grid.shape[0]):
            for j in range(input_grid.shape[1]):
                if input_grid[i, j] == black:
                    colored_grid[i, j] = [0, 0, 0]
                elif input_grid[i, j] == blue:
                    colored_grid[i, j] = [0, 0, 255]
                elif input_grid[i, j] == red:
                    colored_grid[i, j] = [255, 0, 0]
                elif input_grid[i, j] == green:
                    colored_grid[i, j] = [0, 255, 0]
                elif input_grid[i, j] == yellow:
                    colored_grid[i, j] = [255, 255, 0]
                elif input_grid[i, j] == grey:
                    colored_grid[i, j] = [128, 128, 128]
                elif input_grid[i, j] == pink:
                    colored_grid[i, j] = [255, 192, 203]
                elif input_grid[i, j] == orange:
                    colored_grid[i, j] = [255, 165, 0]
                elif input_grid[i, j] == teal:
                    colored_grid[i, j] = [0, 128, 128]
                elif input_grid[i, j] == maroon:
                    colored_grid[i, j] = [128, 0, 0]
        axs[_].imshow(colored_grid)


    plt.show()