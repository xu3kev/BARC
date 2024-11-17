import datetime
import random
from tqdm import tqdm
from vllm import LLM, SamplingParams
import numpy as np
import torch
from transformers import AutoTokenizer
import gc
import os
import argparse
import json
from itertools import permutations

torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()
torch.cuda.reset_accumulated_memory_stats()

# Constants
BASE_MODEL = "barc0/Llama-3.1-ARC-Heavy-Transduction-8B" #Heavy
# BASE_MODEL = "barc0/engineer1-heavy-barc-llama3.1-8b-ins-fft-transduction_lr1e-5_epoch3" #Potpurri
NUM_OF_SAMPLES_PER_PROBLEM = 10
TENSOR_PARALLEL = 1
MAX_PERMUTATIONS = 1  # Maximum number of permutations to consider, including original
TRANSFORMATIONS = ["original", "color_permutation", "transpose"] # Different invertible functions applied

#TASK i : Prompt (training examples + test input)
# 1. Generate 10 samples (beam search) with original prompt {y}_orig
# 2. Generate 10 samples (beam search) with color swapped prompt {y}_color (remember to invert them to original mapping)
# 3. Generate 10 samples (beam search) with transpose prompt {y}_transpose (remember to transpose them to original shape)

# Color mapping
color_dict = {
    0: "Black",
    1: "Blue",
    2: "Red",
    3: "Green",
    4: "Yellow",
    5: "Gray",
    6: "Pink",
    7: "Orange",
    8: "Purple",
    9: "Brown",
}
reverse_color_dict = {v: k for k, v in color_dict.items()}

def transpose_grid(grid):
    """Transpose a grid correctly by swapping rows and columns."""
    n_rows = len(grid)
    n_cols = len(grid[0]) if grid else 0
    return [[grid[row][col] for row in range(n_rows)] for col in range(n_cols)]

def generate_color_permutation():
    """Generate a random permutation of colors."""
    colors = list(range(len(color_dict)))
    perm = list(np.random.permutation(colors))
    return {old: new for old, new in zip(colors, perm)}

def apply_color_permutation(grid, color_mapping):
    """Apply a color permutation to a grid."""
    return [[color_mapping[cell] for cell in row] for row in grid]

def invert_transposition(candidate_str):
    """Invert transposition on a candidate string response."""
    try:
        # Extract grid from candidate string
        grid_str = candidate_str.split("```")[0].strip()        
        grid = parse_grid(grid_str)
        inverted_grid = transpose_grid(grid)  # Transpose is its own inverse
        return grid_to_string(inverted_grid)
    except Exception as e:
        print(f"Error inverting transposition: {e}")
        return candidate_str

def invert_color_permutation(candidate_str, inverse_mapping):
    """Invert color permutation on a candidate string response."""
    try:
        # Extract grid from candidate string
        grid_str = candidate_str.split("```")[0].strip()
        grid = parse_grid(grid_str)
        inverted_grid = apply_color_permutation(grid, inverse_mapping)
        return grid_to_string(inverted_grid)
    except Exception as e:
        print(f"Error inverting color permutation: {e}")
        return candidate_str

def transform_examples(train_examples, transform_type, color_mapping=None):
    """Apply a transformation to all examples."""
    transformed = []
    for example in train_examples:
        if transform_type == "transpose":
            transformed_input = transpose_grid(example['input'])
            transformed_output = transpose_grid(example['output'])
        elif transform_type == "color_permutation":
            if not color_mapping:
                color_mapping = generate_color_permutation()
            transformed_input = apply_color_permutation(example['input'], color_mapping)
            transformed_output = apply_color_permutation(example['output'], color_mapping)
        transformed.append({
            'input': transformed_input,
            'output': transformed_output
        })
    return transformed, color_mapping

def build_transformed_prompt(messages, tokenizer, transformed_examples, transformed_test, perm_order):
    """Build prompt with permuted examples (transformation already applied)."""
    system_msg = messages[0]["content"]
    original_user_msg = messages[1]["content"]
    assistant_msg = messages[2]["content"]
    
    parts = original_user_msg.split("Here are the input and output grids for the reference examples:")
    prefix = parts[0].strip()
    
    # Build examples section with permuted order
    examples_str = "Here are the input and output grids for the reference examples:\n\n"
    for idx, example_idx in enumerate(perm_order, 1):
        example = transformed_examples[example_idx]  # Get example in permuted order
        examples_str += f"Example {idx}:\n"
        examples_str += f"Input:\n{grid_to_string(example['input'])}\n"
        examples_str += f"Output:\n{grid_to_string(example['output'])}\n\n"
    
    test_str = f"Here is the input grid for the test example:\nInput:\n{grid_to_string(transformed_test)}\n\nDirectly provide the output grids corresponding to the given test input grids, based on the patterns observed in the reference examples."
    transformed_user_msg = f"{prefix}\n\n{examples_str}\n{test_str}"
    
    prompt = tokenizer.apply_chat_template([
        {"role": "system", "content": system_msg},
        {"role": "user", "content": transformed_user_msg},
        {"role": "assistant", "content": assistant_msg}
    ], tokenize=False, add_generation_prompt=False)
    
    if prompt.endswith("<|eot_id|>"):
        prompt = prompt[:-len("<|eot_id|>")] + '\n'
        
    return prompt


def get_last_processed_index(output_file):
    """Returns the index of the last processed item if the output file exists"""
    if not os.path.exists(output_file):
        return -1

    last_index = -1
    try:
        with open(output_file, "r") as f:
            for line in f:
                data = json.loads(line)
                last_index = max(last_index, data.get("data_index", -1))
    except Exception as e:
        print(f"Warning: Error reading output file: {e}")
    return last_index


def int_to_color(int_value):
    return color_dict.get(int_value, "Unknown")


def parse_grid(grid_str):
    grid = [
        [
            reverse_color_dict.get(color, -1)
            for color in row.split()
            if color != "Unknown"
        ]
        for row in grid_str.strip().split("\n")
        if "Unknown" not in row
    ]
    if grid and all(cell == -1 for cell in grid[-1]):
        grid.pop()
    return grid


def grid_to_string(grid):
    return "\n".join(" ".join(int_to_color(cell) for cell in row) for row in grid)


def transform_prompt_to_grid(prompt: str):
    parts = prompt.split("Here is the input grid for the test example:")
    train_examples_str, test_input_str = parts[0].strip(), parts[1].strip()

    train_examples = []
    for example in train_examples_str.split("Example")[1:]:
        input_str, output_str = example.split("Output:")
        input_grid = parse_grid(input_str.split("Input:")[1].strip())
        output_grid = parse_grid(output_str.strip())
        input_grid = [row for row in input_grid if -1 not in row]
        output_grid = [row for row in output_grid if -1 not in row]
        if input_grid and output_grid:
            train_examples.append({"input": input_grid, "output": output_grid})

    test_input = parse_grid(test_input_str.split("Input:")[1].strip())
    test_input = [row for row in test_input if -1 not in row]

    return train_examples, test_input
    

def generate_candidates(llm, prompt, num_candidates=NUM_OF_SAMPLES_PER_PROBLEM):
    with torch.no_grad():
        sampling_params = SamplingParams(
            temperature=0,
            max_tokens=1536,
            n=num_candidates,
            use_beam_search=True,
            best_of=num_candidates,
            top_p=1.0,
            logprobs=1,
        )
        outputs = llm.generate(prompt, sampling_params)

    responses = []
    cumulative_logprobs = []
    token_counts = []

    for output in outputs:
        for generated_output in output.outputs:
            responses.append(generated_output.text)
            cumulative_logprobs.append(generated_output.cumulative_logprob)
            token_counts.append(
                sum(1 for logprob in generated_output.logprobs if logprob is not None)
            )

    return responses, cumulative_logprobs, token_counts


def frequency_ranking(candidates_per_perm, scores_per_perm):
    """Aggregate candidates across permutations and sort by frequency and average score"""
    candidate_stats = {}

    for cands, scores in zip(candidates_per_perm, scores_per_perm):
        for cand, score in zip(cands, scores):
            # Clean candidate for comparison
            clean_cand = cand.split("```")[0].strip()

            if clean_cand in candidate_stats:
                candidate_stats[clean_cand]["scores"].append(score)
                candidate_stats[clean_cand]["count"] += 1
            else:
                candidate_stats[clean_cand] = {
                    "original": cand,
                    "scores": [score],
                    "count": 1,
                }

    # Create sorted list with more detailed statistics
    frequency_ranked_candidates = []
    for clean_cand, stats in candidate_stats.items():
        avg_score = sum(stats["scores"]) / len(stats["scores"])
        frequency_ranked_candidates.append({
            "text": stats["original"],
            "avg_score": avg_score,
            "frequency": stats["count"],
            "all_scores": stats["scores"]
        })

    # Sort by frequency first, then by average score
    frequency_ranked_candidates.sort(key=lambda x: (-x["frequency"], -x["avg_score"]))
    return frequency_ranked_candidates
    
    
def get_timestamp_filename(base_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(base_name)
    return f"{name}_{timestamp}{ext}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run validation script with options for file handling."
    )
    parser.add_argument(
        "--new_file",
        action="store_true",
        help="Create a new file instead of appending to existing one",
    )
    parser.add_argument(
        "--file_name",
        type=str,
        default=f"validation_transformations_samples_{NUM_OF_SAMPLES_PER_PROBLEM}_perm_{MAX_PERMUTATIONS}.jsonl",
        help="Name of the file to save results",
    )
    parser.add_argument(
        "--skip_indices",
        type=str,
        default="1000",
        help="Comma-separated indices to skip",
    )
    args = parser.parse_args()

    skip_indices = [int(idx) for idx in args.skip_indices.split(",")]
    print(f"Skipping indices: {skip_indices}")

    # Initialize model and tokenizer
    llm = LLM(
        model=BASE_MODEL,
        enable_lora=False,
        max_model_len=16000,
        gpu_memory_utilization=0.95,
        enable_prefix_caching=True,
        cpu_offload_gb=5,
        tensor_parallel_size=TENSOR_PARALLEL,
    )
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

    # Load data
    with open("validation_data.jsonl") as f:
        data = [json.loads(line) for line in f]

    # Setup output file
    saving_file = (
        args.file_name if not args.new_file else get_timestamp_filename(args.file_name)
    )
    last_processed = get_last_processed_index(saving_file)
    start_index = 0 if args.new_file else last_processed + 1
    file_mode = "w" if args.new_file or last_processed < 0 else "a"

    print(f"Saving to {saving_file}, starting from index {start_index}")
    correct_counter = 0
    correct_original = 0
    total_processed = 0

    # Process existing results if appending
    if file_mode == "a":
        with open(saving_file, "r") as f:
            for line in f:
                existing_data = json.loads(line)
                if existing_data["is_correct_frequency"]:
                    correct_counter += 1
                if existing_data["is_correct_original"]:
                    correct_original += 1
                total_processed += 1
                
    EXAMPLE_NUM = len(data)
    with open(saving_file, file_mode) as f:
        for index in range(start_index, EXAMPLE_NUM):
            if index in skip_indices:
                # print(f"Skipping index {index}")
                continue

            d = data[index]
            messages = d["messages"]
            assert messages[0]["role"] == "system"
            assert messages[1]["role"] == "user"
            base_prompt = tokenizer.apply_chat_template([
                {"role":"system", "content":messages[0]["content"]},
                {"role":"user", "content":messages[1]["content"]},
                {"role":"assistant", "content":messages[2]["content"]}
            ], tokenize=False, add_generation_prompt=False)
        
            trailing_str = "<|eot_id|>"
            # remove trailing
            assert base_prompt.endswith(trailing_str)
            base_prompt = base_prompt[:-len(trailing_str)] + '\n'

            train_examples, test_input = transform_prompt_to_grid(base_prompt)
            test_input = [lst for lst in test_input if lst]

            # Generate all permutations but select at most MAX_PERMUTATIONS including original
            all_perms = list(permutations(range(len(train_examples))))
            original_perm = tuple(range(len(train_examples)))  # Original order (0,1,2,...)
            
            # Always include original permutation and select random others up to total of MAX_PERMUTATIONS
            if len(all_perms) > MAX_PERMUTATIONS:
                other_perms = [p for p in all_perms if p != original_perm]
                selected_perms = random.sample(other_perms, MAX_PERMUTATIONS-1)  # Get random permutations
                selected_perms = [original_perm] + selected_perms  # Add original at start
            else:
                selected_perms = all_perms  # Use all if less than MAX_PERMUTATIONS
            
            print(f"Using {len(selected_perms)} permutations out of {len(all_perms)} possible")
            
            # First apply transformations to get all transformed versions
            transformed_sets = []
            inverse_mappings = []
            for transform_type in TRANSFORMATIONS:
                if transform_type == "original":
                    transformed_examples_set = train_examples
                    transformed_test = test_input
                    inverse_mapping = None
                elif transform_type == "color_permutation":
                    color_mapping = generate_color_permutation()
                    #{0: 1, 1: 5, 2: 0....}
                    transformed_examples_set, _ = transform_examples(train_examples, transform_type, color_mapping)
                    transformed_test = apply_color_permutation(test_input, color_mapping)
                    inverse_mapping = {v: k for k, v in color_mapping.items()}
                    #{0: 2, 1: 0, ......}
                elif transform_type == "transpose":
                    transformed_examples_set, _ = transform_examples(train_examples, transform_type)
                    transformed_test = transpose_grid(test_input)
                    inverse_mapping = "transpose"
                
                transformed_sets.append((transform_type, transformed_examples_set, transformed_test))
                inverse_mappings.append(inverse_mapping)
            
            # Now iterate over transformations and permutations
            candidates_per_perm = []
            scores_per_perm = []
            
            for (transform_type, transformed_examples_set, transformed_test), inverse_mapping in zip(transformed_sets, inverse_mappings):
                for perm in selected_perms:
                    print(f"\nTransformation: {transform_type}, Permutation: {perm}")
                    print("--------------------------------------------------------")
                    print("--------------------------------------------------------")
                    
                    # Build prompt with permuted examples (but keeping transformation)
                    transformed_prompt = build_transformed_prompt(
                        messages, 
                        tokenizer, 
                        transformed_examples_set,  # Already transformed examples
                        transformed_test,          # Already transformed test
                        perm                       # Just the permutation
                    )

                    candidates, scores, _ = generate_candidates(llm, transformed_prompt)

                    # Invert transformation on candidates if needed
                    if transform_type == "color_permutation":
                        candidates = [invert_color_permutation(c, inverse_mapping) for c in candidates]
                    elif transform_type == "transpose":
                        candidates = [invert_transposition(c) for c in candidates]
                        
                    scores = [np.exp(score) for score in scores]
                    # Dealing with same candidates in the beam 
                    # (how many times repeated candidates are the right answer?)
                    unique_candidates = {}
                    for candidate, score in zip(candidates, scores):
                        if candidate not in unique_candidates:
                            unique_candidates[candidate] = score
                    
                    candidates_per_perm.append(list(unique_candidates.keys()))
                    scores_per_perm.append(list(unique_candidates.values()))

                    # Clear GPU memory after each permutation
                    torch.cuda.empty_cache()
                    torch.cuda.reset_peak_memory_stats()

            original_candidates = [
                {
                    "text": cand,
                    "score": float(score)
                }
                for cand, score in zip(candidates_per_perm[0], scores_per_perm[0])
            ]

            # Get frequency-based ranking
            frequency_ranked_candidates = frequency_ranking(
                candidates_per_perm, scores_per_perm
            )
            
            answer = d["answer"].replace("```", "").strip()
            
            is_correct_original = any(
                cand["text"].split("```")[0].strip() == answer
                for cand in original_candidates[:2]
            )

            is_correct_frequency = any(
                cand["text"].split("```")[0].strip() == answer
                for cand in frequency_ranked_candidates[:2]
            )

            # Update counters
            if is_correct_original:
                correct_original += 1
            if is_correct_frequency:
                correct_counter += 1

            # Save results
            response = {
                "data_index": index,
                "prompt": base_prompt,
                "original_candidates": original_candidates,
                "frequency_ranked_candidates": frequency_ranked_candidates,
                "scores_per_permutation": [
                    [float(s) for s in scores] for scores in scores_per_perm
                ],
                "permutations": [list(p) for p in selected_perms],
                "answer": answer,
                "is_correct_original": is_correct_original,
                "is_correct_frequency": is_correct_frequency,
                "base_model": BASE_MODEL,
            }

            # Print results
            print(f"\nResult for problem {index}:")
            print(f"- Correct (in top 2) original: {'Yes' if is_correct_original else 'No'}")
            print(f"- Correct (in top 2) frequency ranking: {'Yes' if is_correct_frequency else 'No'}")

            total_processed += 1
            # Print running accuracy for each method
            print(f"- Running accuracy:")
            print(f"  Original: {correct_original}/{total_processed} ({(correct_original/total_processed)*100:.2f}%)")
            print(f"  Frequency: {correct_counter}/{total_processed} ({(correct_counter/total_processed)*100:.2f}%)")

            f.write(json.dumps(response) + "\n")
            f.flush()

            # Memory cleanup
            del candidates_per_perm, scores_per_perm, frequency_ranked_candidates, response
            gc.collect()
            torch.cuda.empty_cache()

            # Print memory stats
            print(f"GPU Memory Usage:")
            print(f"  Allocated: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
            print(f"  Cached: {torch.cuda.memory_reserved() / 1024**2:.2f} MB")
            print("-------------------")

    print(f"Final Results:")
    print(f"Original ranking - Correct: {correct_original}/{len(data)}")
    print(f"Frequency ranking - Correct: {correct_counter}/{len(data)}")