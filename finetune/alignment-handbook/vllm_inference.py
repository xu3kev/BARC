import time
# BASE_MODEL = "mistralai/Codestral-22B-v0.1"
# LORA_DIR = "data/barc-codestral-sft-qlora-v0.0.3-epoch3"

TEMPERATURE = 0.8
# BASE_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# BASE_MODEL = "./barc-llama3.1-8b-instruct-lora64-induction-gpt4-desc-llama-20k_lr2e-4_epoch3_merged"
# BASE_MODEL = "./barc-llama3.1-8b-instruct-lora64-induction-gpt4-desc-4omini20k_lr2e-4_epoch3_merged"
BASE_MODEL = "./barc-llama3.1-8b-instruct-lora64-induction-gpt4mini20k-llama20k_lr2e-4_epoch3_merged"
# BASE_MODEL = "barc0/barc-llama3.1-8b-instruct-fft-sft-induction35k_lr1e-5_epoch2"
# BASE_MODEL = "data/barc-llama3.1-8b-instruct-fft-induction_gpt4omini100k_lr1e-5_epoch2"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-qlora-v0.0.3"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-qlora-v0.0.2-v3-nopacking"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-data-mix-v0.0.1"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-data-llama-codegen"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-data-gpt4-descriptions"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-data-gpt4omini-codegen"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-gpt-4_description_20000_with_gpt-4o-mini_and_llama3_codegen"
LORA_DIR = None
# LORA_DIR = "barc0/barc-llama3.1-8b-instruct-lora64-induction-gpt4omini35k_lr2e-4_epoch3"


BATCH_SIZE = 16
num_of_samples_per_problem = 64
TENSOR_PARALLEL = 1


from transformers import AutoTokenizer
if LORA_DIR:
    tokenizer = AutoTokenizer.from_pretrained(LORA_DIR)
else:
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

import json
data = []
# problem_file = "./arc_problems_train_327.jsonl"
# problem_file = "./arc_problems_validation_400.jsonl"
# problem_file = "./arc_problems_selected-val-subset50_50_extra_newline.jsonl"
# problem_file = "./arc_problems_selected-train-subset50_50.jsonl"

# problem_file = "./arc_problems_selected-train-subset50_50_extra_newline.jsonl"
# problem_file = "./arc_problems_train_327_extra_newline.jsonl"
# problem_file = "./arc_problems_validation_400_extra_newline.jsonl"
problem_file = "./arc_problems_validation_400_extra_newline_v2.jsonl"

with open(problem_file) as f:
    for line in f:
        data.append(json.loads(line))

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

if LORA_DIR:
    llm = LLM(model=BASE_MODEL, enable_lora=True, max_lora_rank=256, max_model_len=12000,
            enable_prefix_caching=True, tensor_parallel_size=TENSOR_PARALLEL)
    lora_request=LoRARequest("barc_adapter", 1, LORA_DIR)
else:
    llm = LLM(model=BASE_MODEL, enable_lora=False, max_model_len=12000,
            enable_prefix_caching=True, tensor_parallel_size=TENSOR_PARALLEL)

import datetime
datetime_str = datetime.datetime.now().strftime("%m%d%H%M%S%f")
if LORA_DIR:
    saving_file = f"{problem_file.replace('.jsonl', '')}_{LORA_DIR.split('/')[-1]}_temp_{TEMPERATURE}_{datetime_str}.jsonl"
else:
    saving_file = f"{problem_file.replace('.jsonl', '')}_{BASE_MODEL.split('/')[-1]}_temp_{TEMPERATURE}_{datetime_str}.jsonl"
print(f"Saving to {saving_file}")
time.sleep(5)

from tqdm import tqdm
all_responses = []
for d in tqdm(data):
    messages = d["messages"]
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    inputs = tokenizer.apply_chat_template([
        {"role":"system", "content":messages[0]["content"]},
        {"role":"user", "content":messages[1]["content"]}
    ], tokenize=False, add_generation_prompt=True)
    input_tokens = tokenizer.apply_chat_template([
        {"role":"system", "content":messages[0]["content"]},
        {"role":"user", "content":messages[1]["content"]}
    ], tokenize=True, add_generation_prompt=True)
    # print(inputs)
    print(f"Number of tokens: {len(input_tokens)}")
    if len(input_tokens) > 8000:
        print("skip!!!!!")
        continue

    assert num_of_samples_per_problem % BATCH_SIZE == 0
    if  len(input_tokens) < 1750:
        tmp_batch_size = BATCH_SIZE * 4
    elif len(input_tokens) < 4000:
        # double the number of samples
        tmp_batch_size = BATCH_SIZE * 4
    elif len(input_tokens) < 5000:
        tmp_batch_size = BATCH_SIZE 
    else:
        tmp_batch_size = BATCH_SIZE

    print(f"batch size: {tmp_batch_size}")
    sampling_params = SamplingParams(temperature=TEMPERATURE, max_tokens=1536,
                                     n=tmp_batch_size)
    aggregate_outputs = []
    for i in range(num_of_samples_per_problem // tmp_batch_size):
        if LORA_DIR:
            outputs = llm.generate(
                inputs,
                sampling_params,
                lora_request=lora_request
            )
        else:
            outputs = llm.generate(
                inputs,
                sampling_params,
            ) 
        aggregate_outputs.append(outputs)

    if not aggregate_outputs:
        breakpoint()
    else:
        print(aggregate_outputs[0])


    # Print the outputs.
    responses = []
    for outputs in aggregate_outputs:
        for output in outputs:
            prompt = output.prompt
            print(f"Prompt: {prompt!r}")
            for i in range(len(output.outputs)):
                generated_text = output.outputs[i].text
                # print(f"Generated text: {generated_text!r}\n")
                responses.append(generated_text)

    all_responses.append({"uid": d["uid"], "prompt":inputs , "responses": responses, "base_model": BASE_MODEL, "lora_dir": LORA_DIR})

    with open(saving_file, "w") as f:
        f.write("\n".join(json.dumps(p) for p in all_responses))

print(f"Saving to {saving_file}")

time.sleep(15)