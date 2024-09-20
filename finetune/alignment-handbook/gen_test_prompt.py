import os
import tqdm
import json
from gen_dataset import Problem, make_input_prompt, convert_chat_format
from arc import validation_problems, train_problems
import re

# SPLIT="validation"
SPLIT = "train"

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
    breakpoint()


    if SPLIT == "train":
        problems = train_problems
    elif SPLIT == "validation":
        problems = validation_problems

    for arc_problem in tqdm.tqdm(problems):
        
        uid = arc_problem.uid
        if uid in seeds_uid:
            continue
        problem = Problem(seed_id=arc_problem.uid, code="# No code")

        question = make_input_prompt(problem)
        messages = convert_chat_format(question, None)['messages']
        ALL_PROBLEMS.append({"uid": uid, "messages": messages})
        

    # save all problems
    import random
    random.seed(0)
    random.shuffle(ALL_PROBLEMS)

    print([p['uid'] for p in ALL_PROBLEMS[0:50]])
    print(f"The number of problems is {len(ALL_PROBLEMS)}")

    breakpoint()
    
    problem_file = f"arc_problems_{SPLIT}_{len(ALL_PROBLEMS)}.jsonl"
    with open(problem_file, "w") as f:
        f.write("\n".join(json.dumps(p) for p in ALL_PROBLEMS))

    # with open(saving_file, "w") as f:
    #     f.write("\n".join(json.dumps(p) for p in all_problem_answers))

if __name__ == "__main__":
    main()
