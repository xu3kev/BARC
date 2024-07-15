from common import *

import numpy as np
from typing import *

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the partition color (the color that forms the grid partitions)
    partition_color = None
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            color = input_grid[i, j]
            if np.all(input_grid[:, j] == color) or np.all(input_grid[i, :] == color):
                partition_color = color
                break
        if partition_color:
            break

    assert partition_color is not None, "No partition color found"

    # Determine the regions by flood filling the areas between partitions
    regions = find_connected_components(input_grid, background=partition_color, connectivity=4, monochromatic=True)

    regions_cropped = [crop(region) for region in regions]

    # Create an empty output grid with the same shape as the input_grid
    output_grid = np.zeros_like(input_grid)

    # Fill the output grid with the partition color
    output_grid[input_grid == partition_color] = partition_color

    # Reflect each region over the main diagonal and place it in the output grid
    for region in regions_cropped:
        x, y, w, h = bounding_box(region)
        reflected_region = np.transpose(region)

        # Find an appropriate position for the reflected region
        for rx in range(input_grid.shape[0] - h + 1):
            for ry in range(input_grid.shape[1] - w + 1):
                # Check for collisions before placing the reflected region
                if not collision(object1=output_grid, object2=reflected_region, x2=rx, y2=ry, background=Color.BLACK):
                    blit(output_grid, reflected_region, rx, ry, background=Color.BLACK)
                    break
            else:
                continue
            break

    return output_grid

def generate_input() -> np.ndarray:
    # Make a 15x15 grid for the background
    grid_size = 15
    grid = np.zeros((grid_size, grid_size), dtype=int)

    # Pick a non-black color for the partition lines
    partition_color = np.random.choice(Color.NOT_BLACK)

    # Create horizontal and vertical partition lines
    for i in range(4, grid_size, 5):
        grid[i, :] = partition_color
        grid[:, i] = partition_color

    # Fill each region with random colors
    colors = list(Color.NOT_BLACK)
    for x in range(0, grid_size, 5):
        for y in range(0, grid_size, 5):
            region_color = np.random.choice(colors)
            for i in range(5):
                for j in range(5):
                    if grid[x + i, y + j] == 0:
                        grid[x + i, y + j] = region_color

    return grid