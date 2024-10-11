import sys
import os

def concepts_in_file(f):
    if os.path.exists(f): fn = f
    elif os.path.exists(f"{f}.py"): fn = f"{f}.py"
    elif os.path.exists(f"seeds/{f}.py"): fn = f"seeds/{f}.py"
    elif "# concepts" in f: fn = None
    else:
        assert False, f"File not found/could not be interpreted as source"

    if fn is not None:
        with open(fn, "r") as f:
            code = f.read()
    else:
        code = f
    
    # Find the line containing the text "# concepts:", and then look at the line after that
    # It will be a comment that contains a list of comma delimited concepts
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == "# concepts:":
            concepts = lines[i+1][len("# "):].split(", ")
            return concepts
    
    assert False, "error extracting concepts"

def description_in_file(f):
    if os.path.exists(f): fn = f
    elif os.path.exists(f"{f}.py"): fn = f"{f}.py"
    elif os.path.exists(f"seeds/{f}.py"): fn = f"seeds/{f}.py"
    elif "# description" in f: fn = None
    else:
        assert False, f"File not found/could not be interpreted as source"

    if fn is not None:
        with open(fn, "r") as f:
            code = f.read()
    else:
        code = f
    
    # Find the line containing the text "# description:", and then look at the lines after that up to and not including the first line that is not entirely comment
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == "# description:":
            start_of_description = i+1
            end_of_description = start_of_description
            while end_of_description < len(lines) and lines[end_of_description].strip().startswith("#"):
                end_of_description += 1
            n_description_lines = end_of_description - start_of_description + 1
            description = "\n".join(lines[start_of_description:start_of_description+n_description_lines])

            return description
            
    
    assert False, "error extracting description"

def all_concepts():
    """Returns a dictionary mapping concept name to UID"""
    all_concepts = {}
    for f in os.listdir("seeds"):
        if f.endswith(".py") and f not in ["common.py", "template.py"]:
            # trim the file extension
            f = f[:-3]
            for concept in concepts_in_file(f"seeds/{f}.py"):
                if concept in all_concepts:
                    all_concepts[concept].append(f)
                else:
                    all_concepts[concept] = [f]
    return all_concepts

def print_all_concepts():
    for concept, files in sorted(all_concepts().items()):
        print(f"{concept}: {' '.join(list(sorted(files)))}")

def all_descriptions():
    ds = []
    for f in os.listdir("seeds"):
        if f.endswith(".py") and f not in ["common.py", "template.py"]:
            # trim the file extension
            f = f[:-3]
            description = description_in_file(f"seeds/{f}.py")
            ds.append(description)
    return ds
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument("--thing_to_print", default="concepts", choices=["concepts", "description"])
    arguments = parser.parse_args()

    if arguments.thing_to_print == "concepts":
        print_all_concepts()
    elif arguments.thing_to_print == "description":
        descriptions = all_descriptions()
        import random
        random.shuffle(descriptions)
        for d in descriptions:
            print(d)
