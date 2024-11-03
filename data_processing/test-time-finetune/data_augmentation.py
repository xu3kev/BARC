import json
import random
import os
import numpy as np
from tqdm import tqdm

def permuate_list(permuate_partial=0.5, permuate_all=0.1):
    random_flag = random.uniform(0, 1)
    if random_flag < permuate_partial:
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        numbers = [0] + numbers
        return numbers
    elif random_flag < permuate_all + permuate_partial:
        numbers = list(range(10))
        random.shuffle(numbers)
        return numbers
    else:
        return None
def get_transform(prob_if_flip, prob_if_mirror, prob_if_rotate, prob_if_scale, max_scale):
    if_flip = random.random() < prob_if_flip
    if_mirror = random.random() < prob_if_mirror
    rotate_degree = 0
    if random.random() < prob_if_rotate:
        rotate_degree = random.choice([90, 180, 270])
    scale = 1
    if random.random() < prob_if_scale:
        scale = random.choice(range(1, max_scale + 1))
    return if_flip, if_mirror, rotate_degree, scale

def rotate_flip_mirror_grid(grid, if_flip, if_mirror, rotate_degree):
    if if_flip:
        grid = [row[::-1] for row in grid]
    if if_mirror:
        grid = grid[::-1]
    if rotate_degree == 90:
        grid = [list(row) for row in zip(*grid[::-1])]
    elif rotate_degree == 180:
        grid = [row[::-1] for row in grid[::-1]]
    elif rotate_degree == 270:
        grid = [list(row) for row in zip(*grid)][::-1]
    return grid

def enlarge_grid_n_times(grid, n):
    new_grid = []
    for row in grid:
        new_row = []
        for element in row:
            new_row += [element] * n
        new_grid += [new_row] * n
    return new_grid

def grid_to_input(grid, permuate_list=None, if_flip=False, if_mirror=False, rotate_degree=0, scale=1):
    grid = rotate_flip_mirror_grid(grid, if_flip, if_mirror, rotate_degree)
    grid = enlarge_grid_n_times(grid, scale)
    if permuate_list is not None:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j] = permuate_list[grid[i][j]]
    return grid

def process_all_data(dataset_name, aug_time, prob_if_flip=0, prob_if_mirror=0, prob_if_rotate=0, prob_if_scale=0, if_permuate=False):
    random.seed(42)
    arc_subset_test = []
    with open('dataset/' + dataset_name, 'r') as f:
        # arc_subset_test = [json.loads(line) for line in f]
        arc_subset_test = json.load(f)
    augmented_data = []

    for _ in tqdm(range(aug_time)):
        cur_task_id = 0
        for task in tqdm(arc_subset_test):
            # print(i, '/', len(arc_subset_test))
            task = task['data']
            flag = False
            if cur_task_id == 0:
                print(len(task))
            max_len = 0
            for cnt, example in enumerate(task['train'] + task['test']):
                if len(example['input']) == 0 or len(example['output']) == 0:
                    flag = True
                    break
                for row in example['input']:
                    for element in row:
                        if element > 9 or element < 0:
                            flag = True
                            break
                for row in example['output']:
                    for element in row:
                        if element > 9 or element < 0:
                            flag = True
                            break
                max_len = max(max(max_len, len(example['input'])), len(example['output']))
                max_len = max(max(max_len, len(example['input'][0])), len(example['output'][0]))
            if max_len > 30 or max_len == 0:
                continue  
            max_scale = 30 // max_len
            if flag:
                continue

            if if_permuate:
                permuate_list_tmp = permuate_list()
            else:
                permuate_list_tmp = None
            if_flip, if_mirror, rotate_degree, scale = get_transform(prob_if_flip, prob_if_mirror, prob_if_rotate, prob_if_scale, max_scale)

            all_examples = []
            for _, train_example in enumerate(task['train']):
                example_pair = {'input': grid_to_input(train_example["input"], permuate_list_tmp, if_flip, if_mirror, rotate_degree, scale), 'output': grid_to_input(train_example["output"], permuate_list_tmp, if_flip, if_mirror, rotate_degree, scale)}
                all_examples.append(example_pair)

            # Make sure it has at least 3 examples
            appendix = []
            for _, train_example in enumerate(task['train']):
                example_pair = {'input': grid_to_input(train_example["input"], permuate_list_tmp, not if_flip, not if_mirror, (rotate_degree + 90) % 360, scale), 'output': grid_to_input(train_example["output"], permuate_list_tmp, not if_flip, not if_mirror, (rotate_degree + 90) % 360, scale)}
                appendix.append(example_pair)
            
            random.shuffle(appendix)
            all_examples += appendix

            test_example = {'input': grid_to_input(task['test'][0]['input'], permuate_list_tmp, if_flip, if_mirror, rotate_degree, scale), 'output': grid_to_input(task['test'][0]['output'], permuate_list_tmp, if_flip, if_mirror, rotate_degree, scale)}
            augmented_data.append({'task': cur_task_id, 'data': {'train': all_examples[0:3], 'test': [test_example]}})
            cur_task_id += 1
        
    print(len(augmented_data))
    dataset_name += 'l'
    with open(f'dataset/augmented_test_time_{dataset_name}', 'w') as f:
        for data in augmented_data:
            f.write(json.dumps(data) + '\n') 

process_all_data('arc_all_evaluation_new_seperate.json', 10, 0.5, 0.5, 0.5, 0.5, True)