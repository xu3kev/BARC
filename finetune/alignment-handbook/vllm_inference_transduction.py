# BASE_MODEL = "mistralai/Codestral-22B-v0.1"
# LORA_DIR = "data/barc-codestral-sft-qlora-v0.0.3-epoch3"

# BASE_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# BASE_MODEL = "./data/barc-llama3.1-8b-instruct-fft-sft-induction_transduction_balance_lr1e-5"
# BASE_MODEL = "./data/barc-llama3.1-8b-instruct-fft-sft-induction_transduction_fixed_balance_lr1e-5_epoch3/checkpoint-1086"
# BASE_MODEL = "barc0/barc-llama3.1-8b-instruct-fft-sft-induction-transduction-fixed-balance-checkpoint-1086"
# BASE_MODEL = "./data/barc-llama3.1-8b-instruct-fft-sft-transduction_lr1e-5_epoch2/checkpoint-266"
# BASE_MODEL = "./data/barc-llama3.1-8b-instruct-fft-sft-transduction_lr1e-5_epoch2"
BASE_MODEL = "barc0/barc-llama3.1-8b-instruct-fft-sft-both_35k_and_35k_lr1e-5_epoch2"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-qlora-v0.0.3"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-qlora-v0.0.2-v3-nopacking"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-data-mix-v0.0.1"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-data-llama-codegen"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-data-gpt4-descriptions"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-data-gpt4omini-codegen"
# LORA_DIR = "data/barc-llama3.1-8b-instruct-sft-lora-gpt-4_description_20000_with_gpt-4o-mini_and_llama3_codegen"
LORA_DIR = None


BATCH_SIZE = 16
num_of_samples_per_problem = 16
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
problem_file = "../../data_processing/validation_transduction_prompt.jsonl"

import datetime
datetime_str = datetime.datetime.now().strftime("%m%d%H%M%S%f")

with open(problem_file) as f:
    for line in f:
        data.append(json.loads(line))

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest



if LORA_DIR:
    llm = LLM(model=BASE_MODEL, enable_lora=True, max_lora_rank=256, max_model_len=12000,
            enable_prefix_caching=True, tensor_parallel_size=TENSOR_PARALLEL)
    lora_request=LoRARequest("barc_adapter", 1, LORA_DIR)
    saving_file = f"{problem_file.replace('.jsonl', '')}_{LORA_DIR.split('/')[-1]}_{datetime_str}.jsonl"
    print(f"Saving to {saving_file}")
else:
    llm = LLM(model=BASE_MODEL, enable_lora=False, max_model_len=16000,
            enable_prefix_caching=True, tensor_parallel_size=TENSOR_PARALLEL)
    lora_request = None
    if 'checkpoint' in BASE_MODEL.split('/')[-1]:
        model_name = BASE_MODEL.split('/')[-2] + "_" + BASE_MODEL.split('/')[-1]
    else:
        model_name = BASE_MODEL.split('/')[-1]
    saving_file = f"{problem_file.replace('.jsonl', '')}_{model_name}_{datetime_str}.jsonl"



from tqdm import tqdm
all_responses = []
correct_counter = 0
for d in tqdm(data):
    messages = d["messages"]
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    inputs = tokenizer.apply_chat_template([
        {"role":"system", "content":messages[0]["content"]},
        {"role":"user", "content":messages[1]["content"]},
        {"role":"assistant", "content":messages[2]["content"]}
    ], tokenize=False, add_generation_prompt=False)

    trailing_str = "<|eot_id|>"
    # remove trailing
    assert inputs.endswith(trailing_str)
    inputs = inputs[:-len(trailing_str)] + '\n'

    input_tokens = tokenizer.apply_chat_template([
        {"role":"system", "content":messages[0]["content"]},
        {"role":"user", "content":messages[1]["content"]},
        {"role":"assistant", "content":messages[2]["content"]}
    ], tokenize=True, add_generation_prompt=False)

    print(f"Number of tokens: {len(input_tokens)}")
    if len(input_tokens) > 16000:
        print("skip!!!!!")
        continue

    tmp_batch_size = BATCH_SIZE
    print(f"batch size: {tmp_batch_size}")
    sampling_params = SamplingParams(temperature=0, max_tokens=1100,
                                     n=tmp_batch_size, best_of=16, use_beam_search=True)
    # sampling_params = SamplingParams(temperature=0.7, max_tokens=1100,
    #                                     n=tmp_batch_size)
    aggregate_outputs = []
    for i in range(num_of_samples_per_problem // tmp_batch_size):
        outputs = llm.generate(
            inputs,
            sampling_params,
            lora_request=lora_request
        ) 
        aggregate_outputs.append(outputs)

    print(inputs)
    if not aggregate_outputs:
        breakpoint()


    # Print the outputs.
    responses = []
    generated_texts = []
    for outputs in aggregate_outputs:
        for output in outputs:
            prompt = output.prompt
            print(f"Prompt: {prompt!r}")
            for i in range(len(output.outputs)):
                generated_text = output.outputs[i].text
                # print(f"Generated text: {generated_text!r}\n")
                responses.append(generated_text)
                generated_texts.append(generated_text)

    all_responses.append({"uid": d["uid"], "prompt":inputs , "responses": responses, "base_model": BASE_MODEL, "lora_dir": LORA_DIR})

    print("====generated_texts====")
    print(generated_texts[0])
    print("---------")
    if len(generated_texts) > 1:
        print(generated_texts[1])
    print("====answer====")
    print(d['answer'])
    # parse output and compare to answer
    top_generated_text = generated_texts[0]
    if "```" in top_generated_text:
        parsed_generated_text = top_generated_text.split("```")[0].strip()
        if parsed_generated_text == d['answer'].strip():
            print("Correct!")
            correct_counter += 1
        else:
            print("Incorrect!")
    else:
        print("Wrong output format")

    print(f"Correct: {correct_counter}/{len(all_responses)}")

    with open(saving_file, "w") as f:
        f.write("\n".join(json.dumps(p) for p in all_responses))

print(f"Saving to {saving_file}")
print(f"Correct: {correct_counter}/{len(data)}")
import time
time.sleep(15)