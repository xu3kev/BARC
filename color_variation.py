from seeds import common
import random
import re
import time


# Map a hard coded color to a deterministic some other color in source code, keeping cases same
def color_deterministic(problem_source_code, old_color, new_color):
    upper_template = f"(((?<=[^a-zA-Z])|^)({old_color.upper()})(?=[^a-zA-Z]))"
    capitalized_template = (
        f"(((?<=[^a-zA-Z])|^)({old_color.lower().capitalize()})(?=[^a-zA-Z]))"
    )
    lower_template = f"(((?<=[^a-zA-Z])|^)({old_color.lower()})(?=[^a-zA-Z]))"

    # Do findall operation with this regex
    upper_regex = re.compile(upper_template)
    capitalized_regex = re.compile(capitalized_template)
    lower_regex = re.compile(lower_template)

    replace_upper = re.sub(
        upper_regex, lambda x: new_color.upper(), problem_source_code
    )

    replace_capitalized = re.sub(
        capitalized_regex,
        lambda x: new_color.lower().capitalize(),
        replace_upper,
    )

    replace_lower = re.sub(
        lower_regex,
        lambda x: new_color.lower(),
        replace_capitalized,
    )

    return replace_lower


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

    # Write a regex that matches only colors
    upper_template = ""
    capitalized_template = ""
    lower_template = ""
    for color in color_list:
        upper_template += f"(((?<=[^a-zA-Z])|^)({color})(?=[^a-zA-Z]))|"
        capitalized_template += (
            f"(((?<=[^a-zA-Z])|^)({color.lower().capitalize()})(?=[^a-zA-Z]))|"
        )
        lower_template += f"(((?<=[^a-zA-Z])|^)({color.lower()})(?=[^a-zA-Z]))|"
    upper_template = upper_template[:-1]
    capitalized_template = capitalized_template[:-1]
    lower_template = lower_template[:-1]

    # Do findall operation with this regex
    upper_regex = re.compile(upper_template)
    capitalized_regex = re.compile(capitalized_template)
    lower_regex = re.compile(lower_template)

    replace_upper = re.sub(
        upper_regex, lambda x: color_dict[x.group()], problem_source_code
    )

    replace_capitalized = re.sub(
        capitalized_regex,
        lambda x: color_dict[x.group().upper()].lower().capitalize(),
        replace_upper,
    )

    replace_lower = re.sub(
        lower_regex,
        lambda x: color_dict[x.group().upper()].lower(),
        replace_capitalized,
    )

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

    return replace_lower, input_grids, output_grids


# Usage: python color_variation.py <seed>.py for randomized color change
# Usage: python color_variation.py <seed>.py <old_color> <new_color> for deterministic color change
def test():
    import sys, os
    from problem_generation import generate_problem

    file = sys.argv[1]

    current_file_dir = os.path.dirname(os.path.realpath(__file__))

    with open(f"{current_file_dir}/seeds/{file}") as f:
        problem_source_code = f.read()
        if len(sys.argv) == 4:
            old_color = sys.argv[2]
            new_color = sys.argv[3]
            code = color_deterministic(problem_source_code, old_color, new_color)
            print(code)
        else:
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
