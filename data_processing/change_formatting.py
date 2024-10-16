from datasets import load_dataset
from datasets import Dataset
import json


def parse_examples(text):
    # Split the text into training and test sections
    train_text, test_text = text.split("***Test example:***")

    # Parse training examples
    train_examples = []
    for example in train_text.split("[Example"):
        if "Input:" in example and "Output:" in example:
            input_text = example.split("Input:")[1].split("Output:")[0].strip().strip('`')
            output_text = example.split("Output:")[1].strip().strip("`")
            input_lines = [line.strip() for line in input_text.split("\n") if line.strip()]
            output_lines = [line.strip() for line in output_text.split("\n") if line.strip()]
            train_examples.append(("\n".join(input_lines), "\n".join(output_lines)))

    # Parse test example
    test_lines = [line.strip() for line in test_text.split("\n") if line.strip() and "output" not in line.lower() and 'Input' not in line]
    test_example = "\n".join(test_lines)

    return train_examples, [test_example]


# DEFAULT_SYSTEM_PROMPT = "You are an world-class puzzle solver who are extremely good at spotting patterns and solving puzzles. You are also an expert Python programmer who can write code to solve puzzles."
# DEFAULT_SYSTEM_PROMPT = "You are an world-class puzzle solver who are extremely good at spotting patterns and solving puzzles."
DEFAULT_SYSTEM_PROMPT = "You are a world-class puzzle solver with exceptional pattern recognition skills. Your task is to analyze puzzles, spot patterns, and provide direct solutions."
def convert_chat_format(question, answer):
    messages =  {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
    }
    if answer:
        messages["messages"].append({"role": "assistant", "content": answer})
    return messages

def make_problem_input_str(train_examples, test_examples):
    prompt ="Given input-output grid pairs as reference examples, carefully observe the patterns to predict the output grid for new test input. Each pair follows the same transformation rule. Grids are 2D arrays represented as strings, with cells (colors) separated by spaces and rows by newlines."
    prompt += "\nHere are the input and output grids for the reference examples:\n"
    for i, pair in enumerate(train_examples):
        prompt += f"Example {i+1}\n"
        prompt += f"Input:\n{pair[0]}\n\nOutput:\n{pair[1]}\n\n\n" 
    prompt += "Here is the input grid for the test example:\n"
    prompt += "Input:\n" + test_examples[0]
    prompt += "\n\nDirectly provide the output grids corresponding to the given test input grids, based on the patterns observed in the reference examples."
    return prompt

if __name__ == "__main__":

    # Load the dataset
    # dataset = load_dataset("barc0/Data_for_transduction", split=["test", "validation"])
    data_files = {"train_sft": "finetune_transduction_dataset.json", "test_sft": "validation_for_finetuning_transduction.json"}
    dataset = load_dataset("barc0/Data_for_transduction", data_files=data_files)
    
    all_data = {"train_sft": [], "test_sft": []}
    
    for split in ["train_sft", "test_sft"]:
        for item in dataset[split]:
            message_data = item["messages"]
            content = message_data[1]["content"]
            train_examples, test_examples = parse_examples(content)
            test_output = message_data[2]["content"].split("```")[0].split("Output:")[1].strip()


            question = make_problem_input_str(train_examples, test_examples)
            answer = f"The output grid for the test input grid is:\n\n```\n{test_output}\n```"
            
            all_data[split].append(convert_chat_format(question, answer))


    print("==============input=============")
    print(all_data['train_sft'][0]["messages"][1]["content"])
    print("==============output=============")
    print(all_data['train_sft'][0]["messages"][2]["content"])


    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
    filtered_train_data = []
    token_counts = []
    from tqdm import tqdm
    for data in tqdm(all_data['train_sft']):
        token_count = 0 
        # token_count += len(encoding.encode(data["messages"][0]["content"]))
        # token_count += len(encoding.encode(data["messages"][1]["content"]))
        # token_count += len(encoding.encode(data["messages"][2]["content"]))
        token_count += len(tokenizer.encode(data["messages"][0]["content"]))
        token_count += len(tokenizer.encode(data["messages"][1]["content"]))
        token_count += len(tokenizer.encode(data["messages"][2]["content"]))
        if token_count < 8000:
            filtered_train_data.append(data)
            token_counts.append(token_count)

    
    print(f"Total number of tokens: {sum(token_counts)}")
    print(f"Averge number of tokens per example: {sum(token_counts) / len(token_counts)}")
    print(f"Max number of tokens per example: {max(token_counts)}")

    print(f"Original number of examples: {len(all_data['train_sft'])}")
    print(f"Filtered number of examples: {len(filtered_train_data)}")

    import random
    random.seed(0)

    random.shuffle(filtered_train_data)

    train_dataset = Dataset.from_list(filtered_train_data)
    test_dataset = Dataset.from_list(all_data['test_sft'])
    # Combine into a DatasetDict
    from datasets import DatasetDict
    dataset_dict = DatasetDict({
        "train_sft": train_dataset,
        "test_sft": test_dataset
    })

            
    dataset_dict.push_to_hub("barc0/transduction_data", private=False)