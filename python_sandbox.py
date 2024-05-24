import os, sys
# read the file that is /dataset/anpl_python/94.py
# and print the content of the file
import numpy as np
import matplotlib.pyplot as plt
import random, string

def file_to_executable(python_path):
    """
    take in a path of python code and turn it into a module
    as if you had imported it, and you can call its main function with an input
    """
    file = open(python_path, 'r')
    # Read the file
    content = file.read()
    # Create a temporary file
    with open('./sandbox/temp.py', 'w') as file:
        file.write(content)
    # Import the file
    import sandbox.temp as temp
    # Return the main function and the input generator
    return temp.main, temp.generate_input

# def str_to_executable(python_code):
#     """
#     take in a string of python code and turn it into a module
#     as if you had imported it, and you can call its main function with an input
#     """
#     # Create a temporary file
#     with open('./sandbox/temp.py', 'w') as file:
#         file.write(python_code)
#     # Import the file
#     import sandbox.temp as temp
#     # Return the main function and the input generator
#     return temp.main, temp.generate_input

def str_to_executable(python_code):
    """
    take in a string of python code and turn it into a module
    as if you had imported it, and you can call its main function with an input
    use exec to implement this
    """
    local_context = {}
    try:
        exec(python_code, local_context)
        return local_context['main'], local_context['generate_input']
    except Exception as e:
        print (f"[str_to_executable] failed to convert the given python code to an executable: {e}")
        return None, None

def display_grid(grid, save_name=None):
    grid = np.array(grid)
    # Example colors
    colors = ['#000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00', '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25', '#FAFAFA']

    # Define color map for the numbers 0-9 using the colors from the previous example
    cmap = plt.cm.colors.ListedColormap(colors[:11])

    # Display the grid as an image with the defined color map
    plt.imshow(grid, cmap=cmap, interpolation='nearest')

    # ensure the color map is from 0 to 10
    plt.clim(0, 11)

    if save_name is not None:
        plt.savefig(save_name)
        # make sure to close the plot to save memory
        plt.close()

    else:
        # Display the plot
        plt.show()

def view_io_from_file(file_path):
    main, input_gen = file_to_executable(file_path)
    for i in range(3):
        input_grid = input_gen()
        display_grid(input_grid)
        output_grid = main(input_grid)
        display_grid(output_grid)

if __name__ == '__main__':
    view_io_from_file('./seeds/05269061.py')

