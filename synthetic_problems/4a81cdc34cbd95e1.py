from common import *
import numpy as np

# concepts:
# color mapping, surrounding

# description:
# Step 1: Change GREEN pixels to YELLOW and BLUE pixels to GREY
# Step 2: Surround every YELLOW pixel with PINK pixels

color_map = {
    Color.GREEN: Color.YELLOW,
    Color.BLUE: Color.GREY
}

def main(input_grid: np.ndarray) -> np.ndarray:
    # Step 1: Perform color mapping
    output_grid = input_grid.copy()
    for original_color, new_color in color_map.items():
        output_grid[input_grid == original_color] = new_color
    
    # Step 2: Surround every YELLOW pixel with PINK pixels
    for i in range(len(output_grid)):
        for j in range(len(output_grid[i])):
            if output_grid[i, j] == Color.YELLOW:
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if (di != 0 or dj != 0) and 0 <= i + di < output_grid.shape[0] and 0 <= j + dj < output_grid.shape[1]:
                            output_grid[i + di, j + dj] = Color.PINK

    return output_grid


def generate_input() -> np.ndarray:
    # Create a random grid size between 5x5 and 10x10
    n = np.random.randint(5, 11)
    input_grid = np.random.choice(list(Color.NOT_BLACK), size=(n, n))
    return input_grid

# Example usage (for testing purposes):