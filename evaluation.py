from tqdm import tqdm
import orjsonl
import os
from collections import Counter
from datasets import load_dataset
from arc import validation_problems

# We provide the samples and execution results on Huggingface. Please check README.md to see the links.

MAX_FILES_TO_LOAD = 10000 # Very large number to load all the files
INDUCTION_SAMPLE_EXEC_RESULTS_DIRS_AND_SAMPLE_SIZE = [("induction_samples_with_execution_results/ARC-Potpourri/", 20000),
                                                      ("induction_samples_with_execution_results/ARC-Potpourri-AugmentedPrompt/", 20000),]
TRANSDUCTION_SAMPLE_FILE = "transduction_experimental_results/evaluation_dataset_results/Llama-3.1-ARC-Potpourri-Transduction-8B-test-time-finetune.jsonl"


def grid_2d_to_tuple(grid):
    return tuple(tuple(row) for row in grid)

def tuple_to_grid_2d(t):
    return [list(row) for row in t]

def color_to_number(color):
    mapping = {
        'BLACK': 0,
        'BLUE': 1, 
        'RED': 2,
        'GREEN': 3,
        'YELLOW': 4,
        'GREY': 5,
        'GRAY': 5,  # Alternative spelling
        'PINK': 6,
        'ORANGE': 7,
        'PURPLE': 8,
        'BROWN': 9
    }
    n = mapping.get(color.upper(), -1) 
    assert n != -1, f"Color {color} not found in mapping"
    return n

def color_grid_to_int_grid(grid_str):
    grid = grid_str.split("\n")
    grid = [row.split() for row in grid if row.strip()]
    grid = [[color_to_number(cell) for cell in row] for row in grid]
    return grid

def main():
    # load all the jonsl files in the directory
    # use orjsonl for faster loading

    # load transduction results
    transduction_responses = orjsonl.load(path=TRANSDUCTION_SAMPLE_FILE)

    # convert transduction responses back to uid my mapping the test_input to the uid 
    test_input_to_uid_test_idx = {}     
    for p in validation_problems:
        for test_idx, test_pair in enumerate(p.test_pairs):
            test_input = grid_2d_to_tuple(test_pair.x.tolist())
            assert test_input not in test_input_to_uid_test_idx
            test_input_to_uid_test_idx[test_input] = (p.uid, test_idx)

    # convert string color back to int
    uid_to_problem = {p.uid:p for p in validation_problems}
    transduction_pass_at_2_counter = 0.0
    transduction_submission = {p.uid:[] for p in validation_problems}
    for r in transduction_responses:
        responses = r["responses"]
        prompt = r["prompt"]
        test_color_grid = prompt.split("example:\nInput:\n")[-1].split("\nDirect")[0]
        test_input = color_grid_to_int_grid(test_color_grid)
        assert grid_2d_to_tuple(test_input) in test_input_to_uid_test_idx
        uid, test_idx = test_input_to_uid_test_idx[grid_2d_to_tuple(test_input)]
        top2 = []
        for response in responses[0:2]:
            response = response.strip("`")
            grid = None
            try:
                grid = color_grid_to_int_grid(response)
            except:
                grid = None
                print(f"Failed to convert response to grid: {response}")
            top2.append(grid)
        problem = uid_to_problem[uid]
        assert len(top2) == 2
        if any(grid_2d_to_tuple(grid) == grid_2d_to_tuple(problem.test_pairs[test_idx].y.tolist()) for grid in top2):
            transduction_pass_at_2_counter += 1.0/len(problem.test_pairs)
        if len(transduction_submission[uid]) == 0:
            transduction_submission[uid] = [[] for _ in range(len(problem.test_pairs))]
        transduction_submission[uid][test_idx] = top2
            
    print(f"Transduction pass@2: {transduction_pass_at_2_counter}/{len(validation_problems)} = {transduction_pass_at_2_counter/len(validation_problems)}")
    
    # get all the jsonl files in the directory
    data_from_each_folder = []
    for induction_sample_exec_results_dir, num_induction_samples_used in INDUCTION_SAMPLE_EXEC_RESULTS_DIRS_AND_SAMPLE_SIZE:
        jsonl_files = [f for f in os.listdir(induction_sample_exec_results_dir) if f.endswith(".jsonl")]
        all_data = []
        
        # sort json_files to make sure the order is consistent
        jsonl_files.sort()
        jsonl_files = jsonl_files[:MAX_FILES_TO_LOAD]
        print(f"Loading {len(jsonl_files)} jsonl files from {induction_sample_exec_results_dir}")
        for file in tqdm(jsonl_files):
            all_data.append(orjsonl.load(path=os.path.join(induction_sample_exec_results_dir, file)))

        data = {}
        print("gathering induction samples")
        for d in tqdm(all_data):
            for problem in d:
                uid = problem["uid"]
                if uid not in data:
                    data[uid] = {"train_verdicts":[], "output_grids":[]}
                data[uid]["train_verdicts"].extend(problem["train_verdicts"])
                data[uid]["output_grids"].extend(problem["output_grids"])

        for uid, d in data.items():
            # cap the number of samples used for induction
            data[uid]["train_verdicts"] = d["train_verdicts"][0:num_induction_samples_used]
            data[uid]["output_grids"] = d["output_grids"][0:num_induction_samples_used]
            assert len(d["train_verdicts"]) == len(d["output_grids"]) == num_induction_samples_used

        data_from_each_folder.append(data)

    # merge the data from each folder
    data = {}
    for d in data_from_each_folder:
        for uid, v in d.items():
            if uid not in data:
                data[uid] = {"train_verdicts":[], "output_grids":[]}
            data[uid]["train_verdicts"].extend(v["train_verdicts"])
            data[uid]["output_grids"].extend(v["output_grids"])


    for _, d in data.items():
        assert len(d["train_verdicts"]) == len(d["output_grids"])
        assert len(d["train_verdicts"]) == sum(size for _, size in INDUCTION_SAMPLE_EXEC_RESULTS_DIRS_AND_SAMPLE_SIZE)

    induction_submission = {p.uid:[] for p in validation_problems}

    for uid, d in data.items():
        counter = Counter()
        problem = uid_to_problem[uid]
        number_of_test_pairs = len(problem.test_pairs)
        number_of_train_pairs = len(problem.train_pairs)
        for test_idx in range(number_of_test_pairs):
            for train_verdict, output_grids in zip(d["train_verdicts"], d["output_grids"]):
                if train_verdict: # pass all the train examples
                    counter[grid_2d_to_tuple(output_grids[number_of_train_pairs + test_idx])] += 1
            top2 = counter.most_common(2)
            test_output = []
            for k, v in top2:
                test_output.append(tuple_to_grid_2d(k))
            induction_submission[uid].append(test_output)

    induction_pass_at_2_counter = 0.0
    for uid, outputs in induction_submission.items():
        for test_idx, test_pair in enumerate(uid_to_problem[uid].test_pairs):
            ground_truth = test_pair.y.tolist()
            test_outputs = outputs[test_idx]
            assert len(test_outputs) <= 2
            if any(output == ground_truth for output in test_outputs):
                induction_pass_at_2_counter += 1.0/len(uid_to_problem[uid].test_pairs)

    print(f"Induction pass@2: {induction_pass_at_2_counter}/{len(validation_problems)} = {induction_pass_at_2_counter/len(validation_problems)}")

    # ensemble both results
    # use induction when available, otherwise use transduction

    ensemble_submission = {p.uid:[] for p in validation_problems}

    for uid in ensemble_submission:
        if induction_submission[uid][0]:
            ensemble_submission[uid] = induction_submission[uid]
        else:
            ensemble_submission[uid] = transduction_submission[uid]

    # checking ensemble results
    ensemble_pass_at_2_counter = 0.0
    for uid, outputs in ensemble_submission.items():
        for test_idx, test_pair in enumerate(uid_to_problem[uid].test_pairs):
            ground_truth = test_pair.y.tolist()
            test_outputs = outputs[test_idx]
            assert len(test_outputs) <= 2
            if any(output == ground_truth for output in test_outputs):
                ensemble_pass_at_2_counter += 1.0/len(uid_to_problem[uid].test_pairs) 

    print(f"Ensemble pass@2: {ensemble_pass_at_2_counter}/{len(validation_problems)} = {ensemble_pass_at_2_counter/len(validation_problems)}")

if __name__ == "__main__":
    main()
