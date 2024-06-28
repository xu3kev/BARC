from common import *

import numpy as np
from typing import *
import time

# concepts:
# Path finding, backtracking


# description:
# Given a grid of size n x n, there will be some randomly placed teal pixels and a
# start point (denoted by two adjacent green pixels) and end point (denoted by two adjacent red pixels).
# Every time you encounter a teal pixel that blocks your way, you can change the direction you are moving.
# You will start with a direction that is parallel to the starting two pixels.
# Your goal is to go from the start point to the end point.

# Negative x coord sometimes?


def calc_neighbors(grid, start_x, start_y):
    directions = {(1, 0): None, (-1, 0): None, (0, 1): None, (0, -1): None}
    for i in directions:
        coord = (start_x + i[0], start_y + i[1])
        if (
            coord[0] >= 0
            and coord[0] < grid.shape[0]
            and coord[1] >= 0
            and coord[1] < grid.shape[1]
        ):
            directions[i] = grid[coord[0], coord[1]]
        else:
            directions[i] = None
    return directions


def find_path(start_x, start_y, grid, dptable):
    if Color.GREEN not in grid and Color.BLUE not in grid:
        return None
    dptable[(start_x, start_y)] = {
        (1, 0): None,
        (-1, 0): None,
        (0, 1): None,
        (0, -1): None,
    }
    # print(dptable)
    # Look at neighboring pixels
    # print(start_x, start_y)
    show_colored_grid(grid)
    print("\n")
    # time.sleep(1)
    print(start_x, start_y)
    directions = calc_neighbors(grid, start_x, start_y)
    print(directions)
    print(start_x, start_y)

    # Handle exit case
    if Color.RED in directions.values():
        return grid
    # If you get stuck, backtrack to the previous turning point, mark the backtracked path as yellow
    if (
        Color.BLACK not in directions.values()
        and Color.GREEN not in directions.values()
    ) or (None in directions.values() and grid[start_x, start_y] == Color.BLUE):
        print("backtrack")
        print(grid[start_x, start_y])
        for i in dptable[(start_x, start_y)]:
            dptable[(start_x, start_y)][i] = -1

        # Find previous start point
        for start, dic in dptable.items():
            for dir, dest in dic.items():
                if dest == (start_x, start_y):

                    draw_line(
                        grid,
                        start[0],
                        start[1],
                        max(abs(start_x - start[0]) + 1, abs(start_y - start[1]) + 1),
                        Color.YELLOW,
                        dir,
                    )
                    print("inside_loop")
                    start_x, start_y = start
        temp_path = find_path(start_x, start_y, grid, dptable)
        if temp_path is not None:
            return temp_path
    else:
        greedy_directions = []
        end_x, end_y = np.argwhere(grid == Color.RED)[0]
        dist_to_end = (end_x - start_x, end_y - start_y)
        dir_to_end_vertical = (0, np.sign(dist_to_end[1]))
        dir_to_end_horizontal = (np.sign(dist_to_end[0]), 0)
        for i in [dir_to_end_horizontal, dir_to_end_vertical]:
            print(i)
            if i in directions.keys():

                greedy_directions.append((i, directions[i]))
        print(greedy_directions)
        for i in directions.keys():
            for k, v in greedy_directions:
                if i[0] != k[0] or i[1] != k[1]:
                    greedy_directions.append((i, directions[i]))
        print(greedy_directions)
        for k, v in greedy_directions:
            # If black / green, we want to try that direction.
            # We will color back the green start point in main function later.
            if v == Color.RED:
                return grid
            if v == Color.BLACK or v == Color.GREEN:
                draw_line(
                    grid,
                    start_x,
                    start_y,
                    None,
                    Color.BLUE,
                    k,
                    stop_at_color=[Color.TEAL, Color.RED],
                )
                new_x = start_x
                new_y = start_y
                # Updating index accordingly
                while (
                    new_x + k[0] < grid.shape[0]
                    and new_x + k[0] >= 0
                    and new_y + k[1] < grid.shape[1]
                    and new_y + k[1] >= 0
                    and grid[new_x + k[0], new_y + k[1]] != Color.TEAL
                ):
                    if grid[new_x, new_y] == Color.RED:
                        return grid
                    new_x += k[0]
                    new_y += k[1]
                print("new")
                print(new_x, new_y)
                if (new_x, new_y) not in dptable.keys() or dptable[(new_x, new_y)][
                    k
                ] != -1:
                    dptable[(start_x, start_y)][k] = (new_x, new_y)
                    temp_path = find_path(new_x, new_y, grid, dptable)
                    if temp_path is not None:
                        return temp_path
                else:
                    dptable[(start_x, start_y)][k] = -1
                    draw_line(
                        grid,
                        start_x,
                        start_y,
                        None,
                        Color.YELLOW,
                        k,
                        stop_at_color=[Color.TEAL, Color.RED],
                    )


def main(input_grid):
    # Finds the start point of grid
    green_loc = np.argwhere(input_grid == Color.GREEN)
    start_x, start_y = green_loc[0]
    neighbors = calc_neighbors(input_grid, start_x, start_y)
    dptable = {}
    grid = find_path(start_x, start_y, input_grid.copy(), dptable)
    # Put back start point
    for x, y in green_loc:
        grid[x, y] = Color.GREEN

    # Color path to green
    grid[grid == Color.BLUE] = Color.GREEN

    # Color visited dead ends to black
    grid[grid == Color.YELLOW] = Color.BLACK

    return grid


def add(tuple1, tuple2):
    return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]


def generate_input():
    # We want to first generate a successful path and add some noise teal pixels.
    # Finally, we will remove the intermediate pixels in the path.

    # Initialize grid
    n = random.randint(14, 20)
    grid = np.zeros((n, n), dtype=int)

    # Generate start point
    start_sprite = random_sprite(1, 2, density=1, color_palette=[Color.GREEN])
    # With 1/2 probability make it a horizontal start point
    if random.randint(0, 1):
        start_sprite = np.rot90(start_sprite)

    # Generate end point

    end_sprite = random_sprite(1, 2, density=1, color_palette=[Color.RED])

    # With 1/2 probability make it a horizontal end point
    if random.randint(0, 1):
        end_sprite = np.rot90(end_sprite)

    # Draw start point
    start_x, start_y = random_free_location_for_object(
        grid, start_sprite, border_size=3
    )
    blit(grid, start_sprite, start_x, start_y)

    # Draw end point
    end_x, end_y = random_free_location_for_object(
        grid, end_sprite, border_size=3, padding=2
    )

    blit(grid, end_sprite, end_x, end_y)

    current_point = (start_x, start_y)
    directions = calc_neighbors(grid, start_x, start_y)
    current_direction = random.choice(list(directions.keys()))
    # Draw a path from start to end, adding teal pixels for turning
    while True:
        dist_to_end = (end_x - current_point[0], end_y - current_point[1])
        dir_to_end_vertical = (0, np.sign(dist_to_end[1]))
        dir_to_end_horizontal = (np.sign(dist_to_end[0]), 0)

        # Look at the neighboring colors
        for k, v in directions.items():
            coord = add(current_point, k)
            try:
                directions[k] = grid[coord[0], coord[1]]
            except:
                directions[k] = None
        states = directions.values()
        # If we are at a black pixel, color it as visited (blue)
        if grid[current_point[0], current_point[1]] == Color.BLACK:
            grid[current_point[0], current_point[1]] = Color.BLUE
        # If we are adjacent to end point, we are almost there!
        if Color.RED in states:
            temp = add(current_point, current_direction)
            temp2 = add(temp, current_direction)
            if (
                grid[temp[0], temp[1]] != Color.RED
                or grid[temp2[0], temp2[1]] != Color.RED
            ):
                # Color the next two pixels of current direction red
                grid[grid == Color.RED] = Color.BLACK
                grid[temp[0], temp[1]] = Color.RED
                grid[temp2[0], temp2[1]] = Color.RED
            break

        # Handle at edge case
        if directions[current_direction] == None:
            # Color current point teal
            grid[current_point[0], current_point[1]] = Color.TEAL

            # Change direction
            current_direction = random.choice(
                [k for k, v in directions.items() if v == Color.BLACK]
            )

        # With 0.2 probability, or if current direction is not going towards where the end point is,
        # we turn to a direction with black pixel.
        if (
            (
                random.random() < 0.2
                or (
                    current_direction != dir_to_end_horizontal
                    and current_direction != dir_to_end_vertical
                )
            )
            and directions[current_direction] == Color.BLACK
            and Color.GREEN not in states
        ):
            # Choose a turn direction
            # Check if there's a direction to turn to, prioritizing turning to end point direction
            turn_dir_available = [
                i
                for i in directions.keys()
                if directions[i] == Color.BLACK and i != current_direction
            ]
            prioritized_dir = []
            if dir_to_end_horizontal in turn_dir_available:
                prioritized_dir.append(dir_to_end_horizontal)
            if dir_to_end_vertical in turn_dir_available:
                prioritized_dir.append(dir_to_end_vertical)
            if prioritized_dir != []:
                turn_dir_available = prioritized_dir
            if turn_dir_available != []:
                turn_direction = random.choice(turn_dir_available)
                # Color the next pixel in current direction teal
                teal_x, teal_y = add(current_point, current_direction)
                grid[teal_x, teal_y] = Color.TEAL

                # Update current direction
                current_direction = turn_direction
        # If at start point, we must go in the direction of the start point
        if grid[current_point[0], current_point[1]] == Color.GREEN:
            # Move past the adjacent green pixel to a black pixel
            current_direction = [
                i for i in directions.keys() if directions[i] == Color.GREEN
            ][0]
            current_point = add(current_point, current_direction)

        current_point = add(current_point, current_direction)

    # For every other black pixel, mutate them to teal with 0.5 probability to add noise to grid
    for i in range(n):
        for j in range(n):
            if grid[i, j] == Color.BLACK:
                if random.random() < 0.3:
                    grid[i, j] = Color.TEAL
    show_colored_grid(grid)
    # Make intermediate pixels black to remove the path
    grid[grid == Color.BLUE] = Color.BLACK

    return grid


# ============= remove below this point for prompting =============

if __name__ == "__main__":
    visualize(generate_input, main)
