from sklearn.manifold import TSNE

def get_descriptions_from_seed(seed):
    with open(f"seeds/{seed}.py") as f:
        content = f.read()
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "# description:" in line:
                while i+1 < len(lines) and lines[i+1].startswith("# "):
                    description.append(lines[i+1][2:])
                    i += 1
                description = " ".join(description)
    return seed

# get embeddings from seed descriptions
embeddings = []

tsne = TSNE(n_components=2, random_state=0)


