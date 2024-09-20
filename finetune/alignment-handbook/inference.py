from transformers import AutoModelForCausalLM
from peft import PeftModel
import torch

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("./data/barc-7b-sft-qlora-v0.0.2")

base_model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.3", torch_dtype=torch.float16, 
    device_map="cuda:0", low_cpu_mem_usage=True,
    attn_implementation="flash_attention_2",
)


peft_model_id = "./data/barc-7b-sft-qlora-v0.0.2"
model = PeftModel.from_pretrained(base_model, peft_model_id, adapter_name="sft")
model = torch.compile(model)

# The model is now ready to be used for inference

# get jsonl file from ../arc_problems_train.jsonl

import json
data = []
with open("./arc_problems_train.jsonl") as f:
    for line in f:
        data.append(json.loads(line))


from transformers import StoppingCriteria

class CodeListStoppingCriteria(StoppingCriteria):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        pass

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        ss = self.tokenizer.batch_decode(input_ids, skip_special_tokens=False)

        flag = True        
        for s in ss:
            # if "```" occurs twice in the string, then we have a code block
            if s.count("```") < 2:
                flag = False
        
        return flag

from transformers import StoppingCriteriaList
sc = CodeListStoppingCriteria(tokenizer)
scl = StoppingCriteriaList([sc])

responses = []
from tqdm import tqdm
for d in tqdm(data):
    messages = d["messages"]
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    inputs = tokenizer.apply_chat_template([
        {"role":"system", "content":messages[0]["content"]},
        {"role":"user", "content":messages[1]["content"]}
    ], tokenize=True, return_tensors="pt", add_generation_prompt=True).to("cuda")

    
    outputs = model.generate(inputs, max_new_tokens=1024, num_return_sequences=1,
        stopping_criteria=scl, temperature=0.2, do_sample=True)

    
    text = tokenizer.batch_decode(outputs, skip_special_tokens=False)
    
    print(text[0])
    # breakpoint()
    responses.append({"uid": d["uid"], "responses": text})

with open("ft_lora_mistral.jsonl", "w") as f:
    for response in responses:
        f.write(json.dumps(response) + "\n")