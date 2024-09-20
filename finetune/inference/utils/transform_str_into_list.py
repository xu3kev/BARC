color_dict = {
    0: "Black",
    1: "Blue",
    2: "Red",
    3: "Green",
    4: "Yellow",
    5: "Gray",  # or "Gray"
    6: "Pink",
    7: "Orange",
    8: "Purple",
    9: "Brown"
}

reverse_color_dict = {
    "Black": 0,
    "Blue": 1,
    "Red": 2,
    "Green": 3,
    "Yellow": 4,
    "Gray": 5,  # or "Gray"
    "Pink": 6,
    "Orange": 7,
    "Purple": 8,
    "Brown": 9
}

def count_differences(list1, list2):
    if len(list1) != len(list2) or len(list1[0]) != len(list2[0]):
        return -1
    
    differences = 0
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            if list1[i][j] != list2[i][j]:
                differences += 1
    return differences

def transform_str_into_list(input_str):
    input_str = input_str.replace('```', '').replace('Output:', '').strip()
    input_str = input_str.split('\n')
    input_str = [x for x in input_str if x]
    output_list = []
    for row_str in input_str:
        row_str = row_str.split(' ')
        row_str = [x for x in row_str if x]
        for item in row_str:
            if item in reverse_color_dict.keys():
                row_str[row_str.index(item)] = reverse_color_dict[item]
            else:
                row_str[row_str.index(item)] = -1
        output_list.append(row_str)

    return output_list