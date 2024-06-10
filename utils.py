import ast

def extract_functions(code):
    class FunctionExtractor(ast.NodeVisitor):
        def __init__(self):
            self.functions = []

        def visit_FunctionDef(self, node):
            func_name = node.name
            docstring = ast.get_docstring(node)
            func_code = ast.get_source_segment(code, node)
            # the api definition is just the source go to the function MINUS the actual implementation, so just the name, type signature/arguments, and docstring
            api_definition = ast.FunctionDef(name=node.name, args=node.args, decorator_list=node.decorator_list, returns=node.returns,
                                             type_comment=node.type_comment, body=node.body[:1] if docstring else node.body[:0])
            api_definition = ast.unparse(ast.fix_missing_locations(api_definition))
            if not docstring:
                api_definition = api_definition + "\n    pass"
            self.functions.append({
                'name': func_name,
                'docstring': docstring,
                'code': func_code,
                'api_definition': api_definition
            })
            self.generic_visit(node)

    tree = ast.parse(code)
    extractor = FunctionExtractor()
    extractor.visit(tree)
    return extractor.functions

def extract_class_definitions(code):
    class ClassExtractor(ast.NodeVisitor):
        def __init__(self):
            self.classes = []

        def visit_ClassDef(self, node):
            class_name = node.name
            docstring = ast.get_docstring(node)
            class_code = ast.get_source_segment(code, node)
            api_definition = ast.ClassDef(name=node.name, bases=node.bases, keywords=node.keywords, decorator_list=node.decorator_list,
                                          body=node.body[:1] if docstring else node.body[:0])
            api_definition = ast.unparse(ast.fix_missing_locations(api_definition))
            self.classes.append({
                'name': class_name,
                'docstring': docstring,
                'code': class_code,
                'api_definition': api_definition
            })
            self.generic_visit(node)

    tree = ast.parse(code)
    extractor = ClassExtractor()
    extractor.visit(tree)
    return extractor.classes

def extract_function_calls(function_code):
    class FunctionCallExtractor(ast.NodeVisitor):
        def __init__(self):
            self.called_functions = set()

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                self.called_functions.add(node.func.id)
            self.generic_visit(node)

    tree = ast.parse(function_code)
    extractor = FunctionCallExtractor()
    extractor.visit(tree)
    return list(extractor.called_functions)

def generate_html_grid(data):
    color_map = {
        0: 'black',
        1: 'blue',
        2: 'red',
        3: 'green',
        4: 'yellow',
        5: 'grey',
        6: 'pink',
        7: 'orange',
        8: 'teal',
        9: 'maroon'
    }

    def array_to_html(array):
        html = '<table style="border-collapse: collapse;">'
        for row in array:
            html += '<tr>'
            for cell in row:
                color = color_map.get(cell, 'white')
                html += f'<td style="width: 20px; height: 20px; background-color: {color};"></td>'
            html += '</tr>'
        html += '</table>'
        return html

    html = '<div>'
    for item in data:
        input_html = array_to_html(item['input'])
        output_html = array_to_html(item['output'])
        html += f'<div style="display: inline-block; margin: 10px;">'
        html += f'<div>Input:</div>{input_html}'
        html += f'<div>Output:</div>{output_html}'
        html += '</div>'
    html += '</div>'

    return html


def remove_trailing_code(code_str):
    lines = code_str.strip().split('\n')
    main_start = None

    for i, line in enumerate(lines):
        if line.strip().startswith('if __name__ == "__main__":'):
            main_start = i
            break

    if main_start is not None:
        # Remove the main block and any trailing non-function lines
        lines = lines[:main_start]

    # Ensure there are no trailing non-function lines
    while lines and lines[-1].strip() == "":
        lines.pop()

    return '\n'.join(lines).strip()

def parse_code(paragraph):
    """
    This function extracts all Markdown code blocks from a given paragraph.
    Args:
        paragraph (str): The input paragraph containing the Markdown code blocks.
    Returns:
        list: A list of extracted code blocks.
    """
    # Regular expression to match Markdown code blocks
    code_block_pattern = re.compile(r"```python(.*?)```", re.DOTALL)

    # Find all code blocks in the paragraph
    matches = code_block_pattern.findall(paragraph)

    # Strip any leading/trailing whitespace from each code block
    code_blocks = [match.strip() for match in matches]

    return code_blocks


if __name__ == "__main__":
    code = """
def foo():
    \"""
    This is a docstring for foo.
    \"""
    return "foo"

def bar(x):
    \"""
    This is a docstring for bar.
    \"""
    return x * 2

def example_function(x):
    y = foo(x)
    z = bar(y)
    return z
"""

    expected_functions_output = [
        {
            'name': 'foo',
            'docstring': 'This is a docstring for foo.',
            'code': 'def foo():\n    """\n    This is a docstring for foo.\n    """\n    return "foo"', 
            'api_definition': 'def foo():\n    """\n    This is a docstring for foo.\n    """'
        },
        {
            'name': 'bar',
            'docstring': 'This is a docstring for bar.',
            'code': 'def bar(x):\n    """\n    This is a docstring for bar.\n    """\n    return x * 2', 
            'api_definition': 'def bar(x):\n    """\n    This is a docstring for bar.\n    """'
        },
        {
            'name': 'example_function',
            'docstring': None,
            'code': 'def example_function(x):\n    y = foo(x)\n    z = bar(y)\n    return z', 
            'api_definition': 'def example_function(x):\n    pass'
        }
    ]

    expected_calls_output = ['foo', 'bar']

    functions = extract_functions(code)
    assert functions == expected_functions_output, f"Expected {expected_functions_output}, but got {functions}"
    
    example_function_code = functions[2]['code']
    called_functions = extract_function_calls(example_function_code)
    assert sorted(called_functions) == sorted(expected_calls_output), f"Expected {expected_calls_output}, but got {called_functions}"
    
    print("All tests passed!")
