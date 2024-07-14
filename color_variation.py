from seeds import common
import random
import re
import time


# Function to process each line, preserving indentation
def process_line(line, color_dict):
    # Find leading whitespace (indentation)
    leading_whitespace = re.match(r"\s*", line).group()

    # Split the line into words, preserving the rest of the structure
    words = line.strip().split()

    # Process each word in the line
    processed_words = []
    for i in words:
        for color in color_dict.keys():
            if i.find(color) != -1:
                i = i.replace(color, color_dict[color])
                break
            if i.find(color.lower()) != -1:
                i = i.replace(color.lower(), color_dict[color].lower())
                break
        processed_words.append(i)

    # Reassemble the line with original leading whitespace
    processed_line = leading_whitespace + " ".join(processed_words)
    return processed_line


# Map every hard coded color except black to some other random colors
def color_variation(problem_source_code, input_grids, output_grids):
    random.seed(time.time())
    # Creates a color mapping of all colors except BLACK.
    color_list = [
        "BLUE",
        "RED",
        "GREEN",
        "YELLOW",
        "GREY",
        "PINK",
        "ORANGE",
        "TEAL",
        "MAROON",
    ]
    new_color_map = color_list.copy()
    random.shuffle(new_color_map)
    color_dict = {}
    for i in range(len(color_list)):
        color_dict[color_list[i]] = new_color_map[i]
    color_dict["GRAY"] = color_dict["GREY"]

    # Replace all colors in the problem source code
    # Assuming problem_source_code contains the Python code to process
    lines = problem_source_code.splitlines()

    # Process each line
    processed_lines = [process_line(line, color_dict) for line in lines]

    # Join the processed lines back into the full text
    problem_source_code = "\n".join(processed_lines)

    # Replace all colors in the input grids
    for i in range(len(input_grids)):
        for x in range(len(input_grids[i])):
            for y in range(len(input_grids[i][x])):
                if input_grids[i][x][y] != 0:
                    input_grids[i][x][y] = (
                        color_list.index(new_color_map[input_grids[i][x][y] - 1]) + 1
                    )

    # Replace all colors in the output grids
    for i in range(len(output_grids)):
        for x in range(len(output_grids[i])):
            for y in range(len(output_grids[i][x])):
                if output_grids[i][x][y] != 0:
                    output_grids[i][x][y] = (
                        color_list.index(new_color_map[output_grids[i][x][y] - 1]) + 1
                    )

    return problem_source_code, input_grids, output_grids


# Test with python color_variation.py <seed>.py
def test():
    import sys, os
    from problem_generation import generate_problem

    file = sys.argv[1]

    current_file_dir = os.path.dirname(os.path.realpath(__file__))

    with open(f"{current_file_dir}/seeds/{file}") as f:
        problem_source_code = f.read()
        problem, stats = generate_problem(
            problem_source_code,
            num_input_grids=2,
            num_deterministic_check=1,
            num_color_permute_check=1,
            timeout=1,
            total_timeout=30,
        )
        input_grids = []
        output_grids = []
        print(problem_source_code)
        for i in problem.examples:
            input_grid, output_grid = i
            common.show_colored_grid(input_grid)
            common.show_colored_grid(output_grid)

        for i in problem.examples:
            input_grid, output_grid = i
            input_grids.append(input_grid)
            output_grids.append(output_grid)
        code, input_grids, output_grids = color_variation(
            problem_source_code, input_grids, output_grids
        )

        # Code check
        problem, stats = generate_problem(
            code,
            num_input_grids=2,
            num_deterministic_check=1,
            num_color_permute_check=1,
            timeout=1,
            total_timeout=30,
        )
        print(code)

        # See if code execution leads to correct grids.
        for i in problem.examples:
            input_grid, output_grid = i
            common.show_colored_grid(input_grid)
            common.show_colored_grid(output_grid)

        # See if grids are transformed correctly
        # for i in input_grids:
        #    common.show_colored_grid(i)

        # for i in output_grids:
        #    common.show_colored_grid(i)


if __name__ == "__main__":
    test()
