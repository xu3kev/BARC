import numpy as np
from typing import *
black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

def main(input_grid: np.ndarray) -> np.ndarray:
    line = find_color(input_grid)
    out = color_between_same_color_pixels(input_grid, line)
    return out

def find_color(grid: np.ndarray) -> int:
    """
    Given a grid, this function finds the color of the line in the grid.
    
    Args:
    1. grid: np.ndarray - A numpy array representing the input grid.
    
    Returns:
    An integer representing the color of the line.
    """
    for color in range(10):
        if color != black:
            for i in range(grid.shape[0]):
                row = grid[i, :]
                col = grid[:, i]
                if np.all(row == color) or np.all(col == color):
                    return color
    return black

def color_between_same_color_pixels(grid: np.ndarray, line_color: int) -> np.ndarray:
    for color in range(10):
        if color != black and color != line_color:
            p = find_pixels_in_color(grid, color)
            grid = color_pixels_between_same_color_pixels(grid, p, color)
    return grid

def find_pixels_in_color(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """
    Given a grid and a color, this function returns a list of tuples representing the indices of all pixels in the grid
    that have the given color.
    
    Args:
    1. grid: np.ndarray - A numpy array representing the input grid.
    2. color: int - An integer representing the color to search for.
    
    Returns:
    A list of tuples representing the indices of all pixels in the grid that have the given color.
    """
    pixels = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i][j] == color:
                pixels.append((i, j))
    return pixels

def color_pixels_between_same_color_pixels(grid: np.ndarray, pixels: List[Tuple[int, int]], color: int) -> np.ndarray:
    """
    Given a grid, a list of pixels and a color, this function turns all black pixels between any two pixels in the list
    that are in the same row or column into the given color.
    
    Args:
    1. grid: np.ndarray - A numpy array representing the input grid.
    2. pixels: List[Tuple[int, int]] - A list of tuples representing the indices of pixels.
    3. color: int - An integer representing the color to turn the pixels into.
    
    Returns:
    A numpy array representing the updated grid.
    """
    for i in range(len(pixels)):
        for j in range(i + 1, len(pixels)):
            if pixels[i][0] == pixels[j][0]:
                for k in range(min(pixels[i][1], pixels[j][1]) + 1, max(pixels[i][1], pixels[j][1])):
                    if grid[pixels[i][0]][k] == black:
                        grid[pixels[i][0]][k] = color
            elif pixels[i][1] == pixels[j][1]:
                for k in range(min(pixels[i][0], pixels[j][0]) + 1, max(pixels[i][0], pixels[j][0])):
                    if grid[k][pixels[i][1]] == black:
                        grid[k][pixels[i][1]] = color
    return grid


# make a grid with cells of some kxk size
# the grid is one color
# the cells are black
def make_jail_cells(grid_size, cell_size, color):
    grid = np.zeros((grid_size, grid_size), dtype=int)
    r_offset_x, r_offset_y = np.random.randint(0, cell_size), np.random.randint(0, cell_size)
    # make horizontal bars with cell_size gaps
    for i in range(r_offset_x, grid_size, cell_size + 1):
        grid[i, :] = color
    # make vertical bars with cell_size gaps
    for i in range(r_offset_y, grid_size, cell_size + 1):
        grid[:, i] = color
    return grid, r_offset_x, r_offset_y

def flood_fill_at_coord(grid, x, y, color):
    # check that the color at x, y is black
    if grid[x, y] != black:
        return
    grid[x, y] = color
    # flood fill in all directions
    if x > 0:
        flood_fill_at_coord(grid, x - 1, y, color)
    if x < grid.shape[0] - 1:
        flood_fill_at_coord(grid, x + 1, y, color)
    if y > 0:
        flood_fill_at_coord(grid, x, y - 1, color)
    if y < grid.shape[1] - 1:
        flood_fill_at_coord(grid, x, y + 1, color)
    return


def generate_input() -> np.ndarray:
    # pick a non-black color
    color = np.random.randint(1, 10)
    # pick a random grid size
    grid_size = np.random.randint(5, 10)
    grid, offset_x, offset_y = make_jail_cells(32, 2, color)

    for _ in range(4):
        if np.random.random() < 0.3:
            continue
        # pick a different color not color
        other_color = np.random.randint(1, 10)
        while other_color == color:
            other_color = np.random.randint(1, 10)

        # get all coords of black cells
        black_coords = np.argwhere(grid == black)
        # pick a random black cell
        x, y = black_coords[np.random.randint(0, len(black_coords))]
        flood_fill_at_coord(grid, x, y, other_color)

        # flip a coin to decide if horizontal or vertical
        h_or_v = np.random.randint(0, 2)
        if h_or_v == 0:
            # horizontal
            # get all the black cells in the same row
            black_coords = np.argwhere(grid[x, :] == black)
            # pick a random black cell
            other_y = black_coords[np.random.randint(0, len(black_coords))]
            flood_fill_at_coord(grid, x, other_y, other_color)
        else:
            # vertical
            # get all the black cells in the same column
            black_coords = np.argwhere(grid[:, y] == black)
            # pick a random black cell
            other_x = black_coords[np.random.randint(0, len(black_coords))]
            flood_fill_at_coord(grid, other_x, y, other_color)

    return grid

if __name__ == '__main__':
    input_grid = generate_input()
    # # print the input and force numpy to display the entire grid
    # with np.printoptions(threshold=np.inf):
    #     print(input_grid)

    # print the whole grid, and put color on their corresponding numbers in terminal
    for row in input_grid:
        for cell in row:
            print(f"\033[9{cell}m{cell}\033[0m", end="")
        print()

    print ("---------------------")

    output_grid = main(input_grid)
    for row in output_grid:
        for cell in row:
            print(f"\033[9{cell}m{cell}\033[0m", end="")
        print()