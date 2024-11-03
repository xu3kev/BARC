import json
import os
with open('arc_all_evaluation.json', 'r') as f:
    data = json.load(f)

all_dataset = []
cnt = 0
for task in data:
    training_data = task['data']['train']
    for i, train in enumerate(training_data):
        if len(training_data) == 2:
            print(task['name'])
            cnt += 1
            break
        new_train_dataset = [new_train for new_train in training_data if new_train != train]
        new_test_dataset = [train]
        all_dataset.append({'name': task['name'], 'data':{'train': new_train_dataset, 'test': new_test_dataset}})

os.makedirs('dataset/', exist_ok=True)

with open('dataset/arc_all_evaluation_new_seperate.json', 'w') as f:
    f.write('[\n')
    for i, task in enumerate(all_dataset):
        json.dump(task, f)
        if i != len(all_dataset) - 1:
            f.write(',\n')
        else:
            f.write(']')