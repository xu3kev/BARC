from common import *

import numpy as np
from typing import *
import time

# concepts:
# path finding


# description:
# In the input you will see teal pixels and a short green line and a short red line.
# Find a path starting from the green line and ending at the red line and color that path green, with the following constraints:
# You can't go through a teal pixel; you can only change direction when you hit a teal pixel; you have to start in the direction of the green line.

def main(input_grid):
    # Plan:
    # 1. Find the start and end points of the pathfinding problem
    # 2. Define the state space, initial state(s), successor function, and goal test
    # 3. Run bfs to find the shortest path from start to end
    # 4. Color the path green

    # 1. Parse the input, based on color
    # There is the start object, end object, and barriers object
    background = Color.BLACK
    start_object = input_grid.copy()
    start_object[start_object != Color.GREEN] = background
    end_object = input_grid.copy()
    end_object[end_object != Color.RED] = background
    barriers_object = input_grid.copy()
    barriers_object[barriers_object != Color.TEAL] = background

    # Determine the orientation of the start object
    x_coordinates = {x for x, y in np.argwhere(start_object == Color.GREEN)}
    y_coordinates = {y for x, y in np.argwhere(start_object == Color.GREEN)}
    # vertical line?
    if len(x_coordinates) == 1:
        possible_orientations = [(0, 1), (0, -1)]
    # horizontal line?
    elif len(y_coordinates) == 1:
        possible_orientations = [(1, 0), (-1, 0)]
    else:
        assert False, "Start object is not horizontal/vertical"
    
    # 2. Define the state space, initial state(s), successor function, and goal test
    # A state is a tuple of (x, y, orientation)
    # orientation is a tuple of (dx, dy)
        
    # Initially we begin at a point on the line, along the orientation of the line
    initial_states = [(x, y, orientation)
                      for x, y in np.argwhere(start_object == Color.GREEN)
                      for orientation in possible_orientations]
    

    def successors(state):
        x, y, orientation = state
        dx, dy = orientation

        if not (0 <= x + dx < input_grid.shape[0] and 0 <= y + dy < input_grid.shape[1]):
            return

        if barriers_object[x + dx, y + dy] == background:
            yield (x + dx, y + dy, orientation)
        if barriers_object[x + dx, y + dy] != background:
            # right angle turns
            new_orientations = [(dy, dx), (-dy, -dx)]
            for new_orientation in new_orientations:
                yield (x, y, new_orientation)
    
    def is_goal(state):
        x, y, (dx, dy) = state
        if not (0 <= x + dx < end_object.shape[0] and 0 <= y + dy < end_object.shape[1]):
            return False
        return end_object[x + dx, y + dy] == Color.RED
    
    # 3. Run bfs to find the shortest path from start to end
    queue = list(initial_states)
    visited = set(initial_states)
    parent = {}
    while queue:
        state = queue.pop(0)        
        if is_goal(state):
            break        
        for successor in successors(state):
            if successor not in visited:
                visited.add(successor)
                parent[successor] = state
                queue.append(successor)

    assert is_goal(state), "No path found"
    
    path = []
    while state in parent:
        path.append(state)
        state = parent[state]

    # 4. Color the path green
    # draw on top of the input grid
    output_grid = input_grid.copy()
    for x, y, _ in path:
        output_grid[x, y] = Color.GREEN

    return output_grid

def generate_input():
    # We want to first generate a successful path and add some noise teal pixels.
    # Finally, we will remove the intermediate pixels in the path.
    # Because the problem never uses the color 42, we will draw the path in that color, but finally erase it before returning the grid.

    # Initialize grid
    n = random.randint(14, 20)
    grid = np.zeros((n, n), dtype=int)

    # Generate start sprite, making it vertical (1x2 dimensions). We will rotate the final grid randomly to get a variety of orientations.
    start_sprite = random_sprite(1, 2, density=1, color_palette=[Color.GREEN])

    # Draw start sprite
    start_x, start_y = random_free_location_for_sprite(grid, start_sprite, border_size=4)
    blit_sprite(grid, start_sprite, start_x, start_y)

    # Make a random path from the start to the end, leaving color 42 along the path, and leaving teal pixels at each turn
    x,y = start_x, start_y-1
    orientation = (0, -1)
    target_length = random.randint(10, 20)
    for _ in range(target_length):
        # Draw the path
        grid[x, y] = 42        

        if random.random() < 0.2:
            # right angle turn
            dx, dy = orientation
            new_orientation = random.choice([(dy, dx), (-dy, -dx)])
            grid[x+dx, y+dy] = Color.TEAL
            orientation = new_orientation
        
        dx, dy = orientation
        x += dx
        y += dy

        if x < 0 or x >= n or y < 0 or y >= n: return generate_input()
    
    # Color the ending red
    grid[x, y] = Color.RED
    grid[x-dx, y-dy] = Color.RED

    # randomly sprinkle teal in unoccupied locations
    for x, y in np.argwhere(grid == Color.BLACK):
        if random.random() < 0.3:
            grid[x, y] = Color.TEAL

    # Replace the path with black
    grid[grid == 42] = Color.BLACK

    # Randomly rotate
    grid = np.rot90(grid, k=random.randint(0, 3))

    return grid

# ============= remove below this point for prompting =============

if __name__ == "__main__":
    visualize(generate_input, main, 10)
