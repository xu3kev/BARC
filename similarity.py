import os
import re
import textwrap
from tkinter import font

from PIL import Image
from httpx import get
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from adjustText import adjust_text
from tqdm import tqdm
from sklearn.manifold import TSNE

from llm import *
from utils import get_description_from_lines, get_concepts_from_lines

def get_seed_concepts(seeds_contents, client, model, description_embeddings):
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
    return np.hstack([description_embeddings, concept_embeddings])

def get_image(path, zoom=0.02, alpha=0.5):
        image = plt.imread(path)
        im = OffsetImage(image, zoom=zoom)
        im.set_alpha(alpha)
        return im       
        
def adjust_positions(data, annotations, zoom=0.02, threshold=0.05):
    from scipy.spatial import distance

    positions = data.copy()
    shifts = np.zeros_like(positions)

    for i, pos in enumerate(positions):
        for j, pos2 in enumerate(positions):
            if i != j:
                d = distance.euclidean(pos, pos2)
                if d < threshold:
                    direction = (pos - pos2) / d
                    shifts[i] += direction * (threshold - d)
    
    for i, ab in enumerate(annotations):
        ab.xybox = positions[i] + shifts[i]

def plot_with_thumbnails(embeddings2d, seeds_contents):
    # Plotting the t-SNE results
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.scatter(embeddings2d[:, 0], embeddings2d[:, 1], c='blue', alpha=0.5)
    ax.set_title('t-SNE Results with Cosine Metric')
    ax.set_xlabel('t-SNE 1')
    ax.set_ylabel('t-SNE 2')

    # Annotating the plot with images
    annotations = []
    for i, (seed, _) in enumerate(seeds_contents):
        image_path = os.path.join('images', 'thumbnails', f'{seed.replace(".py", ".png")}')  # Adjust extension if needed
        if os.path.exists(image_path):
            ab = AnnotationBbox(get_image(image_path), (embeddings2d[i, 0], embeddings2d[i, 1]), frameon=False)
            annotations.append(ab)
            ax.add_artist(ab)

    # Adjust the positions of the images to avoid overlap
    adjust_positions(embeddings2d, annotations, zoom=0.1, threshold=0.05)

    plt.savefig('tsne_results_with_thumbnails.svg', format='svg', bbox_inches='tight')
    plt.close()

def plot_without_thumbnails(embeddings2d, seeds, seed_descriptions, generated_problem_descriptions, add_seed=False, add_description=False, use_concepts=False, jsonl_model=None):
    if add_description:
        n = int(len(embeddings2d) * 0.5)
        m = int(len(embeddings2d) * 0.4)
    else:
        n = 16
        m = 12

    # Plotting the t-SNE results
    plt.figure(figsize=(n, m))
    plt.scatter(embeddings2d[:len(seed_descriptions), 0], embeddings2d[:len(seed_descriptions), 1], c='blue', alpha=0.5)
    plt.scatter(embeddings2d[len(seed_descriptions):, 0], embeddings2d[len(seed_descriptions):, 1], c='red', alpha=0.5)
    if jsonl_model:
        plt.title(f'Known ARC descriptions (Blue) and Descriptions Generated by {jsonl_model} (Red)', fontsize=20)
    else:
        plt.title('Known ARC descriptions (Blue) and Descriptions From Code Generate by gpt-4o (Red)', fontsize=20)
    # plt.xlabel('t-SNE 1')
    # plt.ylabel('t-SNE 2')

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
        for i, description in enumerate(generated_problem_descriptions):
            text = ""
            if add_description:
                text += f"{description}"
            wrapped_annotation = wrap_text(text)
            text = plt.annotate(wrapped_annotation, 
                                (embeddings2d[i+len(seed_descriptions), 0], embeddings2d[i+len(seed_descriptions), 1]), 
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
    if use_concepts:
        png_file_base += '_with_concepts'
    if jsonl_model:
        png_file_base += f'_with_{jsonl_model}'
    print(f"Saving plot to {png_file_base}.png")
    plt.savefig(f'{png_file_base}.png', dpi=150, bbox_inches='tight')
    plt.savefig(f'{png_file_base}.svg', format='svg', bbox_inches='tight')
    plt.close()

def main():
    import argparse
    parser = argparse.ArgumentParser(description = "problem generator")

    parser.add_argument("--csv", "-c", type=str, default=None, help="csv file containing the problems")
    parser.add_argument("--model", "-m", type=str, default="text-embedding-ada-002", help="which model to use for embedding",
                        choices=[m.value for model_list in LLMClient.AVAILABLE_MODELS.values() for m in model_list])
    parser.add_argument("--annotate_description", "-ad", action="store_true", default=False, help="whether to annotate the points with the description")
    parser.add_argument("--annotate_seed", "-as", action="store_true", default=False, help="whether to annotate the points with the seed")
    parser.add_argument("--use_concepts", "-uc", action="store_true", default=False, help="whether to use concept embeddings in addition to description embeddings")
    parser.add_argument("--thumbnails", "-t", action="store_true", default=False, help="whether to use thumbnails for the points")
    parser.add_argument("--jsonl", type=str, default=None, help="file containing generated descriptions to plot")
    
    arguments = parser.parse_args()

    add_seed = arguments.annotate_seed
    add_description = arguments.annotate_description
    use_concepts = arguments.use_concepts
    thumbnails = arguments.thumbnails
    jsonl_model = None
    if arguments.jsonl:
        # find the part of the string that is _temp then the model name is _{model}_temp. Extract the model name
        match = re.search(r"_([a-zA-Z0-9-.]+)_temp", arguments.jsonl)
        if match:
            jsonl_model = match.group(1)

    import json
    generated_problem_concepts = []
    generated_problem_descriptions = []
    # read the jsonl file
    print(f"Reading from {arguments.jsonl}")
    with open(arguments.jsonl) as f:
        data = f.readlines()
    for line in data:
        problem = json.loads(line)
        generated_problem_concepts.append(problem["concepts"])
        generated_problem_descriptions.append(problem["description"])

    # convert model into enum
    for provider, model in [(provider, model) for provider, model_list in LLMClient.AVAILABLE_MODELS.items() for model in model_list]:
        if model.value == arguments.model:
            # should break on the correct values of model and provider, so we can use those variables later
            break
    
    # get current directory path
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    if arguments.csv:
        # read the csv file
        df = pd.read_csv(arguments.csv)
        csv_contents = df[["task_name", "description_input", "description_output"]].values.tolist()
        seeds = [f"{task_name}.py" for task_name, _, _ in csv_contents]
        seeds_contents = [(f"{task_name}.py", f"# description:\n# {description_input}\n# {description_output}") for task_name, description_input, description_output in csv_contents]
        use_concepts = False
    
    else:
        # get all files in seeds directory
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
    description_embeddings_original = [client.generate_embedding(description, model=model) for description in tqdm(seed_descriptions)]
    description_embeddings_generated = [client.generate_embedding(description, model=model) for description in tqdm(generated_problem_descriptions)]

    if use_concepts:
        # get seed concepts
        embeddings_original = get_seed_concepts(seeds_contents, client, model, description_embeddings_original)
        # embeddings_generated = [np.hstack(description_embedding, client.generate_embedding(concepts, model=model)) for concepts, description_embedding in tqdm(zip(generated_problem_concepts, description_embeddings_generated))]
        concept_embeddings = [client.generate_embedding(concepts, model=model) for concepts in tqdm(generated_problem_concepts)]

        description_embeddings_generated = np.array(description_embeddings_generated)
        concept_embeddings = np.array(concept_embeddings)

        embeddings_generated = np.hstack([description_embeddings_generated, concept_embeddings])
    else:
        embeddings_original = description_embeddings_original
        embeddings_generated = description_embeddings_generated
    print("finished generating embeddings")


    embeddings = np.vstack([embeddings_original, embeddings_generated])
    print(embeddings.shape)

    # Instantialte tsne, specify cosine metric
    tsne = TSNE(random_state = 0, metric = 'cosine')

    # Fit and transform
    embeddings2d = tsne.fit_transform(embeddings)

    if not thumbnails:
        plot_without_thumbnails(embeddings2d, seeds, seed_descriptions, generated_problem_descriptions, add_seed, add_description, use_concepts, jsonl_model)
    else:
        plot_with_thumbnails(embeddings2d, seeds_contents)



if __name__ == "__main__":
    main()


