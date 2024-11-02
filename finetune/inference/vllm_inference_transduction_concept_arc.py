BASE_MODEL = 'barc0/heavy-barc-llama3.1-8b-ins-fft-transduction_lr1e-5_epoch3'
# BASE_MODEL = 'barc0/engineer1-heavy-barc-llama3.1-8b-ins-fft-transduction_lr1e-5_epoch3'
LORA_DIR = None


BATCH_SIZE = 20
TENSOR_PARALLEL = 1
BEST_OF = 3


from transformers import AutoTokenizer
if LORA_DIR:
    tokenizer = AutoTokenizer.from_pretrained(LORA_DIR)
else:
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

import json
data = []
problem_file = "../../data_processing/concept_arc_test_transduction_data.json"

import datetime
datetime_str = datetime.datetime.now().strftime("%m%d%H%M%S%f")

with open(problem_file) as f:
    data = json.load(f)

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest


if LORA_DIR:
    llm = LLM(model=BASE_MODEL, enable_lora=True, max_lora_rank=64, max_model_len=12000,
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

print('batch size:', BATCH_SIZE)

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
    sampling_params = SamplingParams(temperature=0, max_tokens=1536,
                                     n=tmp_batch_size, use_beam_search=True, best_of=BATCH_SIZE, top_p=1.0)

    outputs = llm.generate(
        inputs,
        sampling_params,
        lora_request=lora_request
    ) 

    print(inputs)
    # Print the outputs.
    responses = []
    for output in outputs:
        prompt = output.prompt
        print(f"Prompt: {prompt!r}")
        for i in range(len(output.outputs)):
            generated_text = output.outputs[i].text
            responses.append(generated_text)

    all_responses.append({"prompt":inputs, "responses": responses, "base_model": BASE_MODEL, "lora_dir": LORA_DIR})
    correct_task = []
    # parse output and compare to answer
    for i in range(BEST_OF):
        generated_text = responses[i]
        print(f"Generated text:\n{generated_text}\n")
        if "```" in generated_text:
            parsed_generated_text = generated_text.split("```")[0].strip()
            answer = d['answer'].strip()
            if "```" in d['answer']:
                answer = d['answer'].split("```")[0].strip()
            if parsed_generated_text == d['answer'].strip():
                print("Correct!")
                correct_counter += 1
                correct_task.append(d['uid'])
                print(d['uid'])
                break
            else:
                print("Incorrect!")
        else:
            print("Wrong output format")

    with open(saving_file, "w") as f:
        f.write("\n".join(json.dumps(p) for p in all_responses))

print(correct_task)
print(f"Saving to {saving_file}")
print(f"Correct: {correct_counter}/{len(data)}")
import time
time.sleep(15)