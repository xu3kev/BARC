# BASE_MODEL = "mistralai/Codestral-22B-v0.1"
# LORA_DIR = "data/barc-codestral-sft-qlora-v0.0.3-epoch3"

BASE_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-qlora-v0.0.3"
LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-qlora-v0.0.2-v3-nopacking"


BATCH_SIZE = 16
num_of_samples_per_problem = 128
TENSOR_PARALLEL = 1


from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(LORA_DIR)

import json
data = []
problem_file = "./arc_problems_train_327.jsonl"
problem_file = "./arc_problems_validation_400.jsonl"
# problem_file = "./arc_problems_selected-train-subset50_50.jsonl"
with open(problem_file) as f:
    for line in f:
        data.append(json.loads(line))

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

llm = LLM(model=BASE_MODEL, enable_lora=True, max_lora_rank=256, max_model_len=12000,
          enable_prefix_caching=True, tensor_parallel_size=TENSOR_PARALLEL)
lora_request=LoRARequest("barc_adapter", 1, LORA_DIR)

import datetime
datetime_str = datetime.datetime.now().strftime("%m%d%H%M%S%f")
saving_file = f"{problem_file.replace('.jsonl', '')}_{BASE_MODEL.split('/')[1]}_{datetime_str}.jsonl"
print(f"Saving to {saving_file}")

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
    if len(input_tokens) > 7000:
        continue

    assert num_of_samples_per_problem % BATCH_SIZE == 0
    if  len(input_tokens) < 1750:
        tmp_batch_size = BATCH_SIZE * 4
    elif len(input_tokens) < 3500:
        # double the number of samples
        tmp_batch_size = BATCH_SIZE * 2
    else:
        tmp_batch_size = BATCH_SIZE

    sampling_params = SamplingParams(temperature=0.8, max_tokens=1024,
                                     n=tmp_batch_size)
    aggregate_outputs = []
    for i in range(num_of_samples_per_problem // tmp_batch_size):
        outputs = llm.generate(
            inputs,
            sampling_params,
            lora_request=lora_request
        ) 
        aggregate_outputs.append(outputs)


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

import time
time.sleep(15)