import os
import tqdm
import json
from openai import OpenAI
from make_dataset import Problem, make_input_prompt, convert_chat_format
from prompt import get_common_lib_from_file
from arc import validation_problems, train_problems

# SPLIT="validation"
SPLIT = "train"

ALL_PROBLEMS = []

def main():
    model_name="ft:gpt-3.5-turbo-1106:ellislab:test:9kkaKXeO"
    model_name="ft:gpt-4o-mini-2024-07-18:ellislab:llama2000-seeds:9qjZpfTA"
    model_name="ft:gpt-4o-mini-2024-07-18:ellislab:llama3000-seeds:9qs7cbH2"

    saving_file = f"answers_{model_name.replace(':', '_')}_{SPLIT}.jsonl"
    print(f"Saving to {saving_file}")

    api_key = os.getenv("OPENAI_API_KEY")
    openai = OpenAI(api_key=api_key)

    common_lib, _ = get_common_lib_from_file("seeds/common.py")

    all_problem_answers = [] 
    if SPLIT == "train":
        problems = train_problems
    elif SPLIT == "validation":
        problems = validation_problems

    for arc_problem in tqdm.tqdm(problems):
        uid = arc_problem.uid
        problem = Problem(seed_id=arc_problem.uid, code="# No code")

        question = make_input_prompt(problem, common_lib=common_lib)
        messages = convert_chat_format(question, None)['messages']
        ALL_PROBLEMS.append({"uid": uid, "messages": messages})

        # response = openai.chat.completions.create(
        #     model=model_name,
        #     messages=messages,
        #     temperature=0.8,
        #     max_tokens=1000,
        #     top_p=1.0,
        #     n=32
        # )
        # answers = [c.message.content for c in response.choices]
        # all_problem_answers.append({"uid": uid, "responses": answers})

    breakpoint()
    # save all problems
    problem_file = f"arc_problems_{SPLIT}.jsonl"
    with open(problem_file, "w") as f:
        f.write("\n".join(json.dumps(p) for p in ALL_PROBLEMS))

    # with open(saving_file, "w") as f:
    #     f.write("\n".join(json.dumps(p) for p in all_problem_answers))

if __name__ == "__main__":
    main()
