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

def grid_to_input(grid, transpose: bool):
    if transpose:
        transformed_grid = grid.T
    else:
        transformed_grid = grid
    return "\n".join(" ".join(COLOR_MAPPING[c] for c in row) for row in transformed_grid) + EXTRA_NEWLINE

def make_problem_input_str(problem: Problem, transpose: bool):
    # prompt = "You will be given several pairs of input-output grids as examples. Each input-output image pair follow the same transformation rule."
    # prompt += "Given training examples of input and output grids, predict the output grid for the test inputs.\nEach grid is represented as a 2D array where each cell is represented by an color. The grid input and output are written as a string where each cell is separated by a space and each row is separated by a newline.\n"
    prompt ="Given input-output grid pairs as reference examples, carefully observe the patterns to predict the output grid for new test input. Each pair follows the same transformation rule. Grids are 2D arrays represented as strings, with cells (colors) separated by spaces and rows by newlines."
    prompt += "\nHere are the input and output grids for the reference examples:\n"
    for i, pair in enumerate(problem.train_pairs):
        prompt += f"Example {i+1}\n"
        prompt += f"Input:\n{grid_to_input(pair.x, transpose)}\nOutput:\n{grid_to_input(pair.y, transpose)}\n\n" 
    prompt += "Here is the input grid for the test example:\n"
    prompt += "Input:\n" + "\n".join(grid_to_input(pair.x, transpose) for pair in problem.test_pairs)
    return prompt

    # if problem.code:
    #     prompt += "The code to transform the input grid to the output grid is given below:\n"
    #     prompt += problem.code

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
    parser.add_argument("--load_huggingface_dataset", type=str)
    parser.add_argument("--output_huggingface_dataset", type=str, required=False, default=None)
    args = parser.parse_args()

    SEEDS_PATH = "../../seeds"

    seeds = os.listdir(SEEDS_PATH)
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    seeds = [seed for seed in seeds if re.match(pattern, seed)]


    # common_lib, _ = get_common_lib_from_file("seeds/common.py")

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
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


    if args.load_file or args.use_seeds:
        assert args.output_huggingface_dataset , "output_huggingface_dataset is required"
        output_huggingface_dataset = args.output_huggingface_dataset.strip("/")
    elif args.load_huggingface_dataset:
        output_huggingface_dataset = args.load_huggingface_dataset.strip("/") + "_messages_format" + "_" + VERSION
        print(f"output_huggingface_dataset: {output_huggingface_dataset}")
    loaded_problems = []
    if args.load_file or args.load_huggingface_dataset:
        if args.load_file:
            assert args.load_file.endswith(".jsonl"), "Expected a jsonl file"
            assert os.path.exists(args.load_file), "File does not exist"
            loaded_data = []
            with open(args.load_file) as f:
                for line in f:
                    loaded_data.append(json.loads(line))
        else:
            # load from huggingface dataset
            import datasets
            print(datasets.load_dataset(args.load_huggingface_dataset))
            loaded_data = datasets.load_dataset(args.load_huggingface_dataset)['train']

        print(f"get {len(loaded_data)} problems from file")
        print(loaded_data)

        for d in tqdm(loaded_data):
            all_pairs = []
            for example in d["examples"]:
                input_grid = np.array(example[0])
                output_grid = np.array(example[1])
                if (input_grid.shape[0] > 30 or input_grid.shape[1] > 30 
                    or output_grid.shape[0] > 30 or output_grid.shape[1] > 30):
                    continue
                all_pairs.append(IOPair(input_grid, output_grid))

            if len(all_pairs) < 4:
                continue

            code = d['source']
            if "def generate_input" not in code or "def main(" not in code:
                continue
            code = code.split("def generate_input")[0].strip()
            code = code.replace("def main(", "def transform(")
            # use first 3 pairs as train pairs and 4th pair as test pair
        
            problem = Problem(code=code, train_pairs=all_pairs[0:3], test_pairs=[all_pairs[3]])

            loaded_problems.append(problem)

    print(f"get {len(loaded_problems)} problems from file")
        

    train_data_induction = []
    train_data_transduction = []
    # random shuffle with seed 0
    # TODO: actually, for the seed_problems, should NOT transpose
    problems = loaded_problems + seed_problems
    for problem in problems:
        question = make_input_prompt_induction(problem, transpose=TRANSPOSE)
        answer = f"""Let's solve this puzzle using Python code with the common library functions. We'll first reason about the problem and then write the code to solve it. The `transform` function will take the input grid and return the output grid. Here is the Python code with the comments describing how to solve the problem:
```python
{problem.code}
```
""" 
        answer = convert_color_name(answer, COLOR_REPLACEMENTS)
        train_data_induction.append(convert_chat_format_induction(question, answer))

        question = make_output_prompt_transduction(problem)
        answer =  answer = f"The output grid for the test input grid is:\n\n```\n{grid_to_input(problem.test_pairs[0].y, False).strip()}\n```"
        answer = convert_color_name(answer, COLOR_REPLACEMENTS)
        question = convert_color_name(question, COLOR_REPLACEMENTS)

        train_data_transduction.append(convert_chat_format_transduction(question, answer))


    print("==============input=============")
    print(train_data_induction[0]["messages"][1]["content"])
    print("==============output=============")
    print(train_data_induction[0]["messages"][2]["content"])

    print("==============input=============")
    print(train_data_transduction[0]["messages"][1]["content"])
    print("==============output=============")
    print(train_data_transduction[0]["messages"][2]["content"])
    print("==============input=============")


    # calculate total number of tokens
    # encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    token_counts_trans = []
    token_counts_ind = []
    filtered_train_data_transduction = []
    filtered_train_data_induction = []
    filtered_train_data_id = []
    for cnt, (data_induction, data_transduction) in enumerate(zip(train_data_induction, train_data_transduction)):
        token_count_ind = 0 
        token_count_ind += len(tokenizer.encode(data_induction["messages"][0]["content"]))
        token_count_ind += len(tokenizer.encode(data_induction["messages"][1]["content"]))
        token_count_ind += len(tokenizer.encode(data_induction["messages"][2]["content"]))

        token_count_trans = 0
        token_count_trans += len(tokenizer.encode(data_transduction["messages"][0]["content"]))
        token_count_trans += len(tokenizer.encode(data_transduction["messages"][1]["content"]))
        token_count_trans += len(tokenizer.encode(data_transduction["messages"][2]["content"]))

        if token_count_trans < 8000 and token_count_ind < 8000:
            filtered_train_data_induction.append(data_induction)
            filtered_train_data_transduction.append(data_transduction)

            token_counts_trans.append(token_count_trans)
            token_counts_ind.append(token_count_ind)
            filtered_train_data_id.append(cnt)
    
    print('Transduction')
    print(f"Total number of tokens: {sum(token_counts_trans)}")
    print(f"Averge number of tokens per example: {sum(token_counts_trans) / len(token_counts_trans)}")
    print(f"Max number of tokens per example: {max(token_counts_trans)}")

    print('Induction')
    print(f"Total number of tokens: {sum(token_counts_ind)}")
    print(f"Averge number of tokens per example: {sum(token_counts_ind) / len(token_counts_ind)}")
    print(f"Max number of tokens per example: {max(token_counts_ind)}")

    print(f"Original number of examples: {len(train_data_transduction)}")
    print(f"Filtered number of examples: {len(filtered_train_data_transduction)}")

    assert len(filtered_train_data_transduction) == len(filtered_train_data_induction)

    # with open("filtered_finetune_data_check.json", "w") as f:
    #     json.dump(filtered_train_data_transduction, f, indent=4)

    # with open("filtered_finetune_data_check_transduction.jsonl", "w") as f:
    #     f.write("\n".join(json.dumps(data) for data in filtered_train_data_transduction))
    
    # Shuffle the data
    def push_to_huggingface(filter_data, name):
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

        dataset_name  = output_huggingface_dataset.split('/')[-1]
        dataset_name = 'barc0/' + name + '_' + dataset_name
        dataset_dict.push_to_hub(dataset_name, private=True)

    push_to_huggingface(filtered_train_data_induction, 'induction')
    push_to_huggingface(filtered_train_data_transduction, 'transduction')

if __name__ == "__main__":
    main()
