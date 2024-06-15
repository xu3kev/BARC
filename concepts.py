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

def all_concepts():
    """Returns a dictionary mapping concept name to UID"""
    all_concepts = {}
    for f in os.listdir("seeds"):
        if f.endswith(".py") and f != "common.py":
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

if __name__ == "__main__":
    print_all_concepts()