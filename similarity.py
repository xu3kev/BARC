import os
import re
import textwrap

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from adjustText import adjust_text
from tqdm import tqdm
from sklearn.manifold import TSNE
from llm import *
from utils import get_description_from_lines, get_concepts_from_lines

def main():
    import argparse
    parser = argparse.ArgumentParser(description = "problem generator")

    parser.add_argument("--model", "-m", type=str, default="text-embedding-ada-002", help="which model to use for embedding",
                        choices=[m.value for model_list in LLMClient.AVAILABLE_MODELS.values() for m in model_list])
    parser.add_argument("--annotate_description", "-ad", action="store_true", default=False, help="whether to annotate the points with the description")
    parser.add_argument("--annotate_seed", "-as", action="store_true", default=False, help="whether to annotate the points with the seed")
    parser.add_argument("--use_concepts", "-uc", action="store_true", default=False, help="whether to use concept embeddings in addition to description embeddings")
    
    arguments = parser.parse_args()

    add_seed = arguments.annotate_seed
    add_description = arguments.annotate_description

    # convert model into enum
    for provider, model in [(provider, model) for provider, model_list in LLMClient.AVAILABLE_MODELS.items() for model in model_list]:
        if model.value == arguments.model:
            # should break on the correct values of model and provider, so we can use those variables later
            break
    
    # get all files in seeds directory
    # get current directory path
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    seeds = os.listdir(os.path.join(current_file_dir, "seeds"))
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    # get all files and its content
    seeds = [seed for seed in seeds if re.match(pattern, seed)]
    print(seeds)
    seeds_contents = []
    for seed in seeds:
        with open(os.path.join(current_file_dir, "seeds", seed)) as f:
            seeds_contents.append((seed, f.read()))

    # initialize the client
    client = LLMClient(provider=provider, cache_dir=f"{current_file_dir}/cache")

    # get seed descriptions
    seed_descriptions = []
    for seed, content in seeds_contents:
        lines = content.split("\n")
        seed_descriptions.append(get_description_from_lines(lines))
    print("got descriptions")

    # generate embedding for the problem descriptions
    print("generating description embeddings...")
    description_embeddings = [client.generate_embedding(description, model=model) for description in tqdm(seed_descriptions)]

    if arguments.use_concepts:
        # get seed concepts
        seed_concepts = []
        for seed, content in seeds_contents:
            lines = content.split("\n")
            seed_concepts.append(", ".join(get_concepts_from_lines(lines)))
        print("got concepts")

        print("generating concept embeddings...")
        concept_embeddings = [client.generate_embedding(concepts, model=model) for concepts in tqdm(seed_concepts)]

        description_embeddings = np.array(description_embeddings)
        concept_embeddings = np.array(concept_embeddings)

        # append concept embeddings to the end of description embeddings
        embeddings = np.hstack([description_embeddings, concept_embeddings])
    else:
        embeddings = description_embeddings
    print("finished generating embeddings")


    embeddings = np.array(embeddings)
    print(embeddings.shape)

    # Instantialte tsne, specify cosine metric
    tsne = TSNE(random_state = 0, metric = 'cosine')

    # Fit and transform
    embeddings2d = tsne.fit_transform(embeddings)

    if add_description:
        n = 52
        m = 39
    else:
        n = 16
        m = 12

    # Plotting the t-SNE results
    plt.figure(figsize=(n, m))
    plt.scatter(embeddings2d[:, 0], embeddings2d[:, 1], c='blue', alpha=0.5)
    plt.title('t-SNE Results')
    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')

    # Function to wrap text
    def wrap_text(text, width=40):
        return '\n'.join(textwrap.wrap(text, width))

    if add_seed or add_description:
        # Collect all text objects for adjusting
        texts = []
        for i, (seed, description) in enumerate(zip(seeds, seed_descriptions)):
            text = ""
            if add_seed:
                text += f"{seed}\n"
            if add_description:
                text += f"{description}"
            wrapped_annotation = wrap_text(text)
            text = plt.annotate(wrapped_annotation, 
                                (embeddings2d[i, 0], embeddings2d[i, 1]), 
                                fontsize=8, 
                                alpha=0.7,
                                bbox=dict(facecolor='white', alpha=0.5, boxstyle='round,pad=0.3'),
                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1'))
            texts.append(text)

        # Adjust the text to avoid overlap
        adjust_text(texts, arrowprops=dict(arrowstyle='->', color='black'))

    # Save the plot to a PNG file
    png_file_base = 'tsne_results'
    if add_seed:
        png_file_base += '_with_seeds'
    if add_description:
        png_file_base += '_with_descriptions'
    if arguments.use_concepts:
        png_file_base += '_with_concepts'
    plt.savefig(f'{png_file_base}.png', dpi=150, bbox_inches='tight')
    plt.close()
    # plt.show()


if __name__ == "__main__":
    main()


