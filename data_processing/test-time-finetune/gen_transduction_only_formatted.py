import os
import re
import json
import numpy as np
from datasets import Dataset
from tqdm import tqdm
import random

VERSION = "0.3"

# EXTRA_NEWLINE = "\n"
EXTRA_NEWLINE = "\n"
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

def grid_to_input(grid, transpose: bool):
    if transpose:
        transformed_grid = grid.T
    else:
        transformed_grid = grid
    return "\n".join(" ".join(COLOR_MAPPING[c] for c in row) for row in transformed_grid) + EXTRA_NEWLINE

def make_problem_input_str(problem: Problem, transpose: bool):
    prompt ="Given input-output grid pairs as reference examples, carefully observe the patterns to predict the output grid for new test input. Each pair follows the same transformation rule. Grids are 2D arrays represented as strings, with cells (colors) separated by spaces and rows by newlines."
    prompt += "\nHere are the input and output grids for the reference examples:\n"
    for i, pair in enumerate(problem.train_pairs):
        prompt += f"Example {i+1}\n"
        prompt += f"Input:\n{grid_to_input(pair.x, transpose)}\nOutput:\n{grid_to_input(pair.y, transpose)}\n\n" 
    prompt += "Here is the input grid for the test example:\n"
    prompt += "Input:\n" + "\n".join(grid_to_input(pair.x, transpose) for pair in problem.test_pairs)
    return prompt

def make_input_prompt_induction(problem: Problem, transpose: bool):
    common_lib_prefix = ""
    question = common_lib_prefix + make_problem_input_str(problem, transpose=transpose)
    question += "\nWrite a Python function `transform` that can convert any given input grid to its corresponding output grid based on the pattern observed in the reference examples."
    return question

def make_output_prompt_transduction(problem: Problem):
    common_lib_prefix = ""
    question = common_lib_prefix + make_problem_input_str(problem, transpose=False)
    question += "\n\nDirectly provide the output grids corresponding to the given test input grids, based on the patterns observed in the reference examples."
    return question

# DEFAULT_SYSTEM_PROMPT = "You are an world-class puzzle solver who are extremely good at spotting patterns and solving puzzles. You are also an expert Python programmer who can write code to solve puzzles."

DEFAULT_SYSTEM_PROMPT_IND = "You are a world-class puzzle solver with exceptional pattern recognition skills and expertise in Python programming. Your task is to analyze puzzles and provide Python solutions."
DEFAULT_SYSTEM_PROMPT_TRAN = "You are a world-class puzzle solver with exceptional pattern recognition skills. Your task is to analyze puzzles, spot patterns, and provide direct solutions."

def convert_chat_format_induction(question, answer):
    messages =  {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT_IND},
            {"role": "user", "content": question},
        ]
    }
    if answer:
        messages["messages"].append({"role": "assistant", "content": answer})
    return messages

def convert_chat_format_transduction(question, answer):
    messages =  {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT_TRAN},
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
    parser.add_argument("--output_huggingface_dataset", type=str, required=False, default=None)
    args = parser.parse_args()

    SEEDS_PATH = "../../seeds"

    seeds = os.listdir(SEEDS_PATH)
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    seeds = [seed for seed in seeds if re.match(pattern, seed)]

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
    seed_problems = []

    print(f"got {len(seed_problems)} seed problems")


    if args.load_file:
        assert args.output_huggingface_dataset , "output_huggingface_dataset is required"
        output_huggingface_dataset = args.output_huggingface_dataset.strip("/")
   
    loaded_problems = []

    if args.load_file:
        assert args.load_file.endswith(".jsonl"), "Expected a jsonl file"
        assert os.path.exists(args.load_file), "File does not exist"
        loaded_data = []
        with open(args.load_file) as f:
            for line in f:
                loaded_data.append(json.loads(line))

        print(f"get {len(loaded_data)} problems from file")

        for d in tqdm(loaded_data):
            all_pairs = []
            for example in d["data"]['train'] + d["data"]['test']:
                input_grid = np.array(example['input'])
                output_grid = np.array(example['output'])
                if (input_grid.shape[0] > 30 or input_grid.shape[1] > 30 
                    or output_grid.shape[0] > 30 or output_grid.shape[1] > 30):
                    continue
                all_pairs.append(IOPair(input_grid, output_grid))
        
            problem = Problem(code="no code", train_pairs=all_pairs[0:-1], test_pairs=[all_pairs[-1]])

            loaded_problems.append(problem)

    # loaded_problems = loaded_problems[:40]
    print(f"get {len(loaded_problems)} problems from file")
        

    train_data_transduction = []
    # random shuffle with seed 0
    # TODO: actually, for the seed_problems, should NOT transpose
    problems = loaded_problems + seed_problems
    for problem in tqdm(problems):
        try:
            question = make_output_prompt_transduction(problem)
            answer =  answer = f"The output grid for the test input grid is:\n\n```\n{grid_to_input(problem.test_pairs[0].y, False).strip()}\n```"
            answer = convert_color_name(answer, COLOR_REPLACEMENTS)
            question = convert_color_name(question, COLOR_REPLACEMENTS)

            train_data_transduction.append(convert_chat_format_transduction(question, answer))
        except Exception as e:
            print(f"Error in converting problem: {problem.seed_id}")
            print(e)

    for i in range(3):
        print("==============input=============")
        print(train_data_transduction[i]["messages"][1]["content"])
        print("==============output=============")
        print(train_data_transduction[i]["messages"][2]["content"])
        print("==============input=============")

    # calculate total number of tokens
    # encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    token_counts_trans = []
    filtered_train_data_transduction = []
    for data_transduction in tqdm(train_data_transduction):
        token_count_trans = 0
        token_count_trans += len(tokenizer.encode(data_transduction["messages"][0]["content"]))
        token_count_trans += len(tokenizer.encode(data_transduction["messages"][1]["content"]))
        token_count_trans += len(tokenizer.encode(data_transduction["messages"][2]["content"]))

        if token_count_trans < 8000:
            filtered_train_data_transduction.append(data_transduction)

            token_counts_trans.append(token_count_trans)
    
    print('Transduction')
    print(f"Total number of tokens: {sum(token_counts_trans)}")
    print(f"Averge number of tokens per example: {sum(token_counts_trans) / len(token_counts_trans)}")
    print(f"Max number of tokens per example: {max(token_counts_trans)}")

    print(f"Original number of examples: {len(train_data_transduction)}")
    print(f"Filtered number of examples: {len(filtered_train_data_transduction)}")

    with open("dataset/transduction_formatted_test-time_finetune.jsonl", "w") as f:
        f.write("\n".join(json.dumps(data) for data in filtered_train_data_transduction))
    
    # Shuffle the data
    def push_to_huggingface(filter_data, name, dataset_name):
        random.seed(0)
        random.shuffle(filter_data)
        
        # Calculate split index (95% train, 5% test)
        split_index = int(0.95 * len(filter_data))

        # Split the data
        train_data = filter_data[:split_index]
        test_data = filter_data[split_index:]
        
        # Create Hugging Face datasets
        train_dataset = Dataset.from_list(train_data)
        test_dataset = Dataset.from_list(test_data)
        
        # Combine into a DatasetDict
        from datasets import DatasetDict
        dataset_dict = DatasetDict({
            "train_sft": train_dataset,
            "test_sft": test_dataset
        })
        dataset_dict.push_to_hub(dataset_name, private=True)

    def save_disk_file(filter_data, name, dataset_name):
        random.seed(0)
        random.shuffle(filter_data)
        
        # Calculate split index (95% train, 5% test)
        split_index = int(0.95 * len(filter_data))

        # Split the data
        train_data = filter_data[:split_index]
        test_data = filter_data[split_index:]
        
        # Create Hugging Face datasets
        train_dataset = Dataset.from_list(train_data)
        test_dataset = Dataset.from_list(test_data)

        os.makedirs('testtime-ft/', exist_ok=True)
        train_dataset.save_to_disk('testtime-ft/train_sft/')
        test_dataset.save_to_disk('testtime-ft/test_sft/')

    save_disk_file(filtered_train_data_transduction, 'transduction', output_huggingface_dataset)

if __name__ == "__main__":
    main()