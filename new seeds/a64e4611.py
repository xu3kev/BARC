from common import *
import numpy as np
from typing import *

# concepts:
# - Grid manipulation: Finding and marking specific regions in a grid.
# - Random grid generation: Creating a grid with scattered colored regions and adding rectangles.

# description:
# - The `main` function processes an input grid to identify and mark specific regions (rectangles) with a particular color (GREEN).
# - The `generate_input` function creates a grid with random colored patterns and adds random rectangles for testing.

def main(input_grid):
    """
    Processes the input grid to find and mark regions of contiguous black cells with green rectangles.
    
    Parameters:
    input_grid (np.ndarray): The input grid with various colored cells.
    
    Returns:
    np.ndarray: The processed grid with marked green rectangles.
    """
    # Get unique colors in the input grid
    two_color = np.unique(input_grid)
    # Make a copy of the input grid to work on
    grid = np.copy(input_grid)
    output_grid = np.copy(input_grid)  # Copy for output
    n, m = grid.shape  # Get the dimensions of the grid

    # Iterate over possible rectangle sizes (from larger to smaller)
    for i in range(8, 2, -1):
        for j in range(30, 9, -1):
            # Traverse through each cell in the grid
            for x in range(n):
                for y in range(m):
                    # Check for a rectangle of size i x j with all cells being black
                    if x + i <= n and y + j <= m and np.all(grid[x : x + i, y : y + j] == Color.BLACK) and (x == 0 or x + i == n - 1 or y == 0 or y + j == m - 1):
                        # Determine if there are non-black cells around the rectangle
                        ux, vx = 1 if (x > 0) else 0, 1 if (x + i < n - 1) else 0
                        uy, vy = 1 if (y > 0) else 0, 1 if (y + j < m - 1) else 0
                        # Mark the rectangle with green color
                        output_grid[x + ux : x + i - vx, y + uy : y + j - vy] = Color.GREEN
                    # Check for a rectangle of size j x i with all cells being black (rotated)
                    if x + j <= n and y + i <= m and np.all(grid[x : x + j, y : y + i] == Color.BLACK) and (x == 0 or x + j == n - 1 or y == 0 or y + i == m - 1):
                        # Determine if there are non-black cells around the rectangle
                        ux, vx = 1 if (x > 0) else 0, 1 if (x + j < n - 1) else 0
                        uy, vy = 1 if (y > 0) else 0, 1 if (y + i < m - 1) else 0
                        # Mark the rectangle with green color
                        output_grid[x + ux : x + j - vx, y + uy : y + i - vy] = Color.GREEN
    return output_grid

def generate_input():
    """
    Generates a grid with random color patterns and adds random rectangles.

    Returns:
    np.ndarray: The generated grid with random patterns and added rectangles.
    """
    n, m = 30, 30  # Define the dimensions of the grid
    grid = np.zeros((n, m), dtype=int)  # Initialize the grid with zeros (black color)

    # Define available colors (excluding green)
    avaliable_colors = [c for c in Color.NOT_BLACK if c != Color.GREEN]
    selected_color = np.random.choice(avaliable_colors)  # Choose a random color for scattered points

    def random_scatter_point_on_grid(grid, color, density):
        """
        Scatter colored points on the grid based on density.

        Parameters:
        grid (np.ndarray): The grid to scatter points on.
        color (int): The color to use for scattering.
        density (float): The density of scattered points.

        Returns:
        np.ndarray: The grid with scattered points.
        """
        n, m = grid.shape
        colored = 0
        while colored < density * n * m:
            x = np.random.randint(0, n)
            y = np.random.randint(0, m)
            if grid[x, y] == Color.BLACK:
                grid[x, y] = color
                colored += 1
        return grid
    
    # Scatter colored points on the grid
    grid = random_scatter_point_on_grid(grid=grid, color=selected_color, density=0.7)

    # Define the number of rectangles to add
    rectangle_num = np.random.randint(2, 4)

    for _ in range(rectangle_num):
        # Define dimensions for the rectangles
        width = np.random.randint(3, 8)
        height = 30 if np.random.random() < 0.7 else np.random.randint(10, 20)
        if np.random.choice([True, False]):
            width, height = height, width  # Swap width and height randomly
        
        # Create a random sprite (rectangle) to add
        sprite = random_sprite(n=width, m=height, color_palette=[Color.BLACK], background=selected_color, density=1.0, connectivity=4)
        
        # Determine position for the rectangle
        if width > height:
            x = 0
            y = np.random.randint(0, m - height)
        else:
            x = np.random.randint(0, n - width)
            y = 0

        # Place the rectangle on the grid
        grid = blit_sprite(grid=grid, sprite=sprite, x=x, y=y, background=selected_color)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
