import os
import tqdm
import json
from gen_dataset import Problem, make_input_prompt, convert_chat_format
from arc import validation_problems, train_problems
import re

from gen_dataset import TRANSPOSE, EXTRA_NEWLINE

# SPLIT="validation"
# SPLIT = "train"
# SPLIT = "selected-val-subset50.json"
SPLIT = "selected-train-subset50.json"

ALL_PROBLEMS = []

def main():

    # get problems under the seed directory
    seeds = os.listdir("../../seeds")
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    # get all files and its content
    seeds = [seed for seed in seeds if re.match(pattern, seed)]
    def extract_uid(seed):
        uid = ""
        if "." in seed:
            uid = seed.split(".")[0]
        if "_" in uid:
            uid = uid.split("_")[0]
        return uid
    seeds_uid = [extract_uid(seed) for seed in seeds]
    print(len(seeds))
    print(seeds_uid)


    import random
    random.seed(0)
    if SPLIT == "train":
        problems = list(train_problems)
        random.shuffle(problems)
    elif SPLIT == "validation":
        problems = list(validation_problems)
        random.shuffle(problems)
    elif SPLIT.endswith(".json"):
        # load the json file
        problems = []
        with open(SPLIT) as f:
            loaded_problem_data = json.loads(f.read())

        uids = [p['name'].split(".json")[0] for p in loaded_problem_data]
        for uid in uids:
            for arc_problem in train_problems + validation_problems:
                if arc_problem.uid == uid:
                    problems.append(arc_problem)
    else:
        raise ValueError(f"Invalid SPLIT value: {SPLIT}")

    # save all problems

    for arc_problem in tqdm.tqdm(problems):
        
        uid = arc_problem.uid
        if uid in seeds_uid:
            continue
        problem = Problem(seed_id=arc_problem.uid, code="# No code")

        question = make_input_prompt(problem, transpose=True)
    
        messages = convert_chat_format(question, None)['messages']
        ALL_PROBLEMS.append({"uid": uid, "messages": messages})
        

    # print([p['uid'] for p in ALL_PROBLEMS[0:50]])
    # print(f"The number of problems is {len(ALL_PROBLEMS)}")

    # breakpoint()
    
    if ".json" in SPLIT:
        split_filename = SPLIT.split(".json")[0]
    else:
        split_filename = SPLIT
    problem_file = f"arc_problems_{split_filename}_{len(ALL_PROBLEMS)}.jsonl"
    if TRANSPOSE:
        problem_file = f"arc_problems_{split_filename}_{len(ALL_PROBLEMS)}_transpose.jsonl"
    if EXTRA_NEWLINE:
        problem_file = f"arc_problems_{split_filename}_{len(ALL_PROBLEMS)}_extra_newline.jsonl"
    if TRANSPOSE and EXTRA_NEWLINE:
        problem_file = f"arc_problems_{split_filename}_{len(ALL_PROBLEMS)}_transpose_extra_newline.jsonl"
    
    print(f"Saving to {problem_file}")
    with open(problem_file, "w") as f:
        f.write("\n".join(json.dumps(p) for p in ALL_PROBLEMS))

    # with open(saving_file, "w") as f:
    #     f.write("\n".join(json.dumps(p) for p in all_problem_answers))

if __name__ == "__main__":
    main()
