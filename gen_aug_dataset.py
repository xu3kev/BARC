# import datasets

# # Load the dataset
# dataset = datasets.load_dataset("barc0/gpt-4_description_with_llama_codegen")

# # Print the dataset
# print(dataset)
# breakpoint()


from arc import train_problems, validation_problems
import os
import re
# from prompt import get_common_lib_from_file
import json
import numpy as np
import tiktoken
from datasets import Dataset
from tqdm import tqdm
from execution import multi_execute_transformation


# EXTRA_NEWLINE = "\n"
EXTRA_NEWLINE = ""
TRANSPOSE = False

COLOR_MAPPING = {
0: "Black",
1: "Blue",
2: "Red",
3: "Green",
4: "Yellow",
5: "Grey",  # instead of "Grey"
6: "Pink",
7: "Orange",
8: "Teal",
9: "Maroon"
}

COLOR_REPLACEMENTS = {
    "Grey": "Gray",
    "Teal": "Purple",
    "Maroon": "Brown",
}

# Fix Color Mapping
for k, v in COLOR_MAPPING.items():
    if v in COLOR_REPLACEMENTS:
        COLOR_MAPPING[k] = COLOR_REPLACEMENTS[v]

# Map a hard coded color to a deterministic some other color in source code, keeping cases same
def color_deterministic(problem_source_code, old_color, new_color):
    upper_template = f"(((?<=[^a-zA-Z])|^)({old_color.upper()})(?=[^a-zA-Z]|$))"
    capitalized_template = (
        f"(((?<=[^a-zA-Z])|^)({old_color.lower().capitalize()})(?=[^a-zA-Z]|$))"
    )
    lower_template = f"(((?<=[^a-zA-Z])|^)({old_color.lower()})(?=[^a-zA-Z]|$))"

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


def test_color_deterministic():
    problem_source_code = "teal, Teal, TEAL"
    ret = color_deterministic(problem_source_code, "teal", "purple")
    print(ret)


def convert_color_name(text, mapping):
    for old_color, new_color in mapping.items():
        text = color_deterministic(text, old_color, new_color)
    return text

def test_convert_color_name():
    text = "teal, Teal, TEAL\nMaroon COLOR>MAROON, maroon"
    ret = convert_color_name(text, COLOR_REPLACEMENTS)
    print(ret)


class IOPair:
    x: np.ndarray
    y: np.ndarray
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # check type
        assert isinstance(self.x, np.ndarray)
        assert isinstance(self.y, np.ndarray)
        # check shape
        assert len(self.x.shape) == 2
        assert len(self.y.shape) == 2

class Problem:
    # typing hint for the members
    filename: str
    seed_id: str
    code: str
    train_pairs: list
    test_pairs: list

    def __init__(self, filename=None, code=None, seed_id=None, train_pairs=None, test_pairs=None):
        self.filename = filename
        self.seed_id = None
        if filename:
            self.seed_id = filename.split(".")[0]
            if "_" in self.seed_id:
                self.seed_id= self.seed_id.split("_")[0]
        if seed_id:
            self.seed_id = seed_id
        if self.seed_id:
            pattern = r"[0-9a-f]{8}"
            assert re.match(pattern, self.seed_id)
            self.load_arc_problem(self.seed_id)

        self.code = code
        if train_pairs:
            self.train_pairs = train_pairs
        if test_pairs:
            self.test_pairs = test_pairs

        assert self.code, "Code is not provided"
        assert self.train_pairs, "Train pairs are not provided"
        assert self.test_pairs, "Test pairs are not provided"
        # check type
        assert isinstance(self.train_pairs, list)
        assert isinstance(self.test_pairs, list)
        assert all(isinstance(pair, IOPair) for pair in self.train_pairs)
        assert all(isinstance(pair, IOPair) for pair in self.test_pairs)


    def load_arc_problem(self, seed_id):
        # using train_problems
        arc_problem = None
        for problem in train_problems + validation_problems:
            if problem.uid == seed_id:
                arc_problem = problem
                break
        assert arc_problem is not None
        self.train_pairs = []
        for pair in arc_problem.train_pairs:
            self.train_pairs.append(IOPair(pair.x.T, pair.y.T))
        self.test_pairs = []
        for pair in arc_problem.test_pairs:
            self.test_pairs.append(IOPair(pair.x.T, pair.y.T))

def grid_to_input(grid, transpose: bool, color_mapping):
    if transpose:
        transformed_grid = grid.T
    else:
        transformed_grid = grid
    return "\n".join(" ".join(color_mapping[c] for c in row) for row in transformed_grid) + EXTRA_NEWLINE

def make_problem_input_str(problem: Problem, transpose: bool, color_mapping: dict):
    prompt = ""
    prompt += "The following is a puzzle from the ARC dataset. Given training examples of input and output grids, predict the output grid for the test inputs.\nEach grid is represented as a 2D array where each cell is represented by an color. The grid input and output are written as a string where each cell is separated by a space and each row is separated by a newline.\n"
    prompt += "Here are the input and output grids for the training examples:\n"
    for pair in problem.train_pairs:
        prompt += f"Input:\n{grid_to_input(pair.x, transpose, color_mapping)}\nOutput:\n{grid_to_input(pair.y, transpose, color_mapping)}\n\n" 
    prompt += "Here are the input grids for the test example:\n"
    prompt += "Input:\n" + "\n".join(grid_to_input(pair.x, transpose, color_mapping) for pair in problem.test_pairs)
    return prompt

    # if problem.code:
    #     prompt += "The code to transform the input grid to the output grid is given below:\n"
    #     prompt += problem.code

def make_input_prompt(problem: Problem, transpose: bool, color_mapping):
#     common_lib_prefix = f"""
# We first define a common library that contains the functions that you can use to solve the Puzzle.
# Here is the common library function signature and docstring that you can use to solve the problem (skipping the implementation for brevity):
# ```python
# {common_lib}
# ```
# """
    common_lib_prefix = ""
    question = common_lib_prefix + make_problem_input_str(problem, transpose=transpose, color_mapping=color_mapping)
    return question

DEFAULT_SYSTEM_PROMPT = "You are an world-class puzzle solver who are extremely good at spotting patterns and solving puzzles. You are also an expert Python programmer who can write code to solve puzzles."

def convert_chat_format(question, answer):
    messages =  {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
    }
    if answer:
        messages["messages"].append({"role": "assistant", "content": answer})
    return messages

def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_seeds", action="store_true")
    parser.add_argument("--load_file", type=str)

    args = parser.parse_args()

    SEEDS_PATH = "./seeds"

    seeds = os.listdir(SEEDS_PATH)
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    seeds = [seed for seed in seeds if re.match(pattern, seed)]


    # common_lib, _ = get_common_lib_from_file("seeds/common.py")

    seed_problems = []
    if args.use_seeds:
        for seed in seeds:
            with open(f"{SEEDS_PATH}/{seed}") as f:
                content = f.read()
                assert "# ============= remove below this point for prompting =============" in content
                content = content.split("# ============= remove below this point for prompting =============")[0].strip()
                content = content.split("def generate_input")[0].strip()
                content = content.replace("def main(", "def transform(")
                seed_problems.append(Problem(filename=seed, code=content))

    print(f"got {len(seed_problems)} seed problems")


    loaded_problems = []
    if args.load_file:
        assert args.load_file.endswith(".jsonl"), "Expected a jsonl file"
        assert os.path.exists(args.load_file), "File does not exist"
        loaded_data = []
        with open(args.load_file) as f:
            for line in f:
                loaded_data.append(json.loads(line))
                

        for d in loaded_data:
            all_pairs = []
            for example in d["examples"]:
                input_grid = np.array(example[0])
                output_grid = np.array(example[1])
                all_pairs.append(IOPair(input_grid, output_grid))

            code = d['source']
            if "def generate_input" not in code or "def main(" not in code:
                continue
            code = code.split("def generate_input")[0].strip()
            code = code.replace("def main(", "def transform(")
            # use first 3 pairs as train pairs and 4th pair as test pair
        
            problem = Problem(code=code, train_pairs=all_pairs[0:3], test_pairs=[all_pairs[3]])

            loaded_problems.append(problem)

    print(f"get {len(loaded_problems)} problems from file")
        

    train_data = []
    # random shuffle with seed 0
    import random
    random.seed(0)

    if loaded_problems:
        random.shuffle(loaded_problems)
    # loaded_problems = loaded_problems[0:3000]

    # TODO: actually, for the seed_problems, should NOT transpose
    problems = loaded_problems + seed_problems
    failed_problems = []
    COLOR_AUG_ITERATION = 3
    for _ in range(COLOR_AUG_ITERATION):
        for problem in tqdm(problems):

            code = problem.code
            augmented_code = convert_color_name(code, COLOR_REPLACEMENTS)

            # shuffle colors randomly
            all_non_black_colors = [v for k, v in COLOR_MAPPING.items() if k != 0]
            random_shuffle_colors = all_non_black_colors.copy()
            random.shuffle(random_shuffle_colors)
            # create a mapping from old color to new color
            random_color_replacement = {old_color: new_color for old_color, new_color in zip(all_non_black_colors, random_shuffle_colors)}

            new_color_mapping = COLOR_MAPPING.copy()
            for k, v in random_color_replacement.items():
                new_color_mapping[k] = v
            question = make_input_prompt(problem, transpose=TRANSPOSE, color_mapping=new_color_mapping)
            augmented_code = convert_color_name(augmented_code, random_color_replacement)

            # exec and check the code
            # output_grids = multi_execute_transformation(
            #     [augmented_code]* len(problem.train_pairs),
            #     [pair.x for pair in problem.train_pairs],
            #     random_seeds=[0]* len(problem.train_pairs),
            #     timeout=2,
            #     function_name="transform"
            # )

            # for idx, output_grid in enumerate(output_grids):
            #     Flag = False
            #     if not isinstance(output_grid, np.ndarray):
            #         break
            #     if len(output_grid.shape) != 2:
            #         break
            #     if output_grid.shape != problem.train_pairs[idx].y.shape:
            #         break
            #     if not np.array_equal(output_grid, problem.train_pairs[idx].y):
            #         break
            #     Flag = True

            # if not Flag:
            #     failed_problems.append(problem)
            #     continue

            answer = f"""Let's solve this puzzle using Python code with the common library functions. We first reasoning about the problem and then writing the code to solve it. The `transform` function will take the input grid and return the output grid. Here is the Python code and the comments describing how to solve the problem:
    ```python
    {augmented_code}
    ```
    """ 
            
            # print("==============before=============")
            # print(answer)
            
            # print("==============after=============")
            # print(answer)
            train_data.append(convert_chat_format(question, answer))

    # print(f"Failed problems: {len(failed_problems)}")
    # breakpoint()
    print("==============input=============")
    print(train_data[0]["messages"][1]["content"])
    print("==============output=============")
    print(train_data[0]["messages"][2]["content"])


    # calculate total number of tokens
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    token_counts = []
    filtered_train_data = []
    for data in train_data:
        token_count = 0 
        token_count += len(encoding.encode(data["messages"][0]["content"]))
        token_count += len(encoding.encode(data["messages"][1]["content"]))
        token_count += len(encoding.encode(data["messages"][2]["content"]))
        token_counts.append(token_count)
        if token_count < 8000:
            filtered_train_data.append(data)
    

    print(f"Total number of tokens: {sum(token_counts)}")
    print(f"Averge number of tokens per example: {sum(token_counts) / len(token_counts)}")
    print(f"Max number of tokens per example: {max(token_counts)}")

    print(f"Original number of examples: {len(train_data)}")
    print(f"Filtered number of examples: {len(filtered_train_data)}")

    with open("filtered_finetune_data.jsonl", "w") as f:
        f.write("\n".join(json.dumps(data) for data in train_data))



    
    # Shuffle the data
    random.shuffle(filtered_train_data)
    
    # Calculate split index (80% train, 20% test)
    split_index = int(0.95 * len(filtered_train_data))
    
    # Split the data
    train_data = filtered_train_data[:split_index]
    


    test_data = filtered_train_data[split_index:]
    
    # Create Hugging Face datasets
    train_dataset = Dataset.from_list(train_data)
    test_dataset = Dataset.from_list(test_data)
    
    # Combine into a DatasetDict
    from datasets import DatasetDict
    dataset_dict = DatasetDict({
        "train_sft": train_dataset,
        "test_sft": test_dataset
    })

    
    # Push to Hugging Face Hub
    dataset_dict.push_to_hub("barc0/barc_messages_format_color_augmentations_v0.0.1")


    
    

if __name__ == "__main__":
    main()
