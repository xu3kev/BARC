import os
import tqdm
import json
from openai import OpenAI
from make_dataset import Problem, make_input_prompt, convert_chat_format
from prompt import get_common_lib_from_file
from arc import validation_problems
def main():
    model_name="ft:gpt-3.5-turbo-1106:ellislab:test:9kkaKXeO"

    api_key = os.getenv("OPENAI_API_KEY")
    openai = OpenAI(api_key=api_key)

    common_lib, _ = get_common_lib_from_file("seeds/common.py")

    all_problem_answers = [] 
    for arc_problem in tqdm.tqdm(validation_problems):
        uid = arc_problem.uid
        problem = Problem(seed_id=arc_problem.uid)

        question = make_input_prompt(problem, common_lib=common_lib)
        messages = convert_chat_format(question, None)['messages']

        response = openai.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.8,
            max_tokens=1000,
            top_p=1.0,
            n=32
        )

        answers = [c.message.content for c in response.choices]
        all_problem_answers.append({"uid": uid, "responses": answers})

    with open("answers.jsonl", "w") as f:
        f.write("\n".join(json.dumps(p) for p in all_problem_answers))

if __name__ == "__main__":
    main()


