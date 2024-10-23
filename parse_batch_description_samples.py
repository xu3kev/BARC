import argparse
import json

from utils import get_description_from_lines, get_concepts_from_lines

def extract_concepts_and_descriptions(content):
    all_lines = content.split("\n")

    all_concepts = []
    all_descriptions = []

    last_concept_line = None
    # find the line containing "BEST SOLUTION"
    for i, line in enumerate(all_lines):
        if "# concepts" in line:
            last_concept_line = i
            lines = all_lines[last_concept_line:]
            # Extract the concepts, which come as a comment after the line containing "# concepts:"
            concepts = get_concepts_from_lines(lines)
            all_concepts.append(concepts)
            # Extract the descriptions, which come as a comment after the line containing "# description:"
            description = get_description_from_lines(lines)
            all_descriptions.append(description)

    return all_concepts, all_descriptions

def process_jsonl_line(response):
    list_of_concepts, list_of_descriptions = [], []
    sample = response['response']['body']['choices'][0]["message"]["content"]
    parsed_concepts_lst, parsed_description_lst = extract_concepts_and_descriptions(sample)
    for parsed_concepts, parsed_description in zip(parsed_concepts_lst, parsed_description_lst):
        if parsed_concepts != [] and parsed_description != []:
            parsed_concepts = ", ".join(parsed_concepts)
            list_of_concepts.append(parsed_concepts)
            list_of_descriptions.append(parsed_description)
    return list_of_concepts, list_of_descriptions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a JSONL file to extract concepts and descriptions.")
    parser.add_argument("jsonl_file", type=str, help="Path to the JSONL file containing samples.")
    args = parser.parse_args()
    concepts_descriptions = []

    with open(args.jsonl_file, 'r') as f:
        responses = [json.loads(line) for line in f]

    samples = [response['response']['body']['choices'][0]["message"]["content"] for response in responses]
    
    for sample in samples:
        parsed_concepts_lst, parsed_description_lst = extract_concepts_and_descriptions(sample)
        for parsed_concepts, parsed_description in zip(parsed_concepts_lst, parsed_description_lst):
            if parsed_concepts != [] and parsed_description != []:
                parsed_concepts = ", ".join(parsed_concepts)
                concepts_descriptions.append((parsed_concepts, parsed_description))
    print(len(concepts_descriptions))
    file_name_jsonl = args.jsonl_file.replace(".jsonl", "_parsed.jsonl")

    print(f"Writing to jsonl {file_name_jsonl}")
    with open(file_name_jsonl, "w") as f:
        # jsonl, one json per line
        import json
        for concepts, description in concepts_descriptions:
            f.write(json.dumps({"concepts": concepts,
                                "description": description,
                                }) + "\n")
    print(f"{len(concepts_descriptions)} descriptions written to {file_name_jsonl}")