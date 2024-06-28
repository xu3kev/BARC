import json
import argparse
import numpy as np
from utils import remove_trailing_code, generate_html_grid
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", type=str, required=True)
    args = parser.parse_args()

    with open(args.jsonl, "r") as f:
        data = [json.loads(line) for line in f]

    htmls = []
    for problem in data:
        code = problem["source"]
        code = remove_trailing_code(code)
        # try:
        #     function_calls = extract_function_calls(code)
        #     # set intersection to find common function names
        #     common_functions_calls = common_lib_function_names.intersection(set(function_calls))
        # except:
        #     print("Error in extracting function calls")

        print(f"Code:\n{code}")
        # print(f"Funtion calls: {function_calls}")
        # print(f"Common functions calls: {common_functions_calls}")
        examples = problem["examples"]
        input_grids = [np.array(example[0]) for example in examples[0:4]]
        output_grids = [np.array(example[1]) for example in examples[0:4]]
        print("Have", len(input_grids), "input grids")
        print("Have", len(output_grids), "output grids")
        examples_input_output = [ {"input": input_grid, "output": output_grid}
                                    for input_grid, output_grid in zip(input_grids, output_grids) 
                                    if isinstance(output_grid, np.ndarray) ]
        if len(examples_input_output) == 0:
            assert False, "No valid input-output examples found"

        # an html string showing the Common Lib Function call names
        info_html = "" #f"""<div>Used Common Library Functions: {", ".join(list(common_functions_calls))}</div>"""
        grid_html = generate_html_grid(examples_input_output)
        # an html string showing the function calls in the code, use syntax highlighting
        # Syntax highlighting for the code
        from pygments import highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import HtmlFormatter
        def highlight_code(code):
            formatter = HtmlFormatter()
            highlighted_code = highlight(code, PythonLexer(), formatter)
            style = f"<style>{formatter.get_style_defs('.highlight')}</style>"
            return style + highlighted_code
        code_html = highlight_code(code)
        htmls.append(grid_html + info_html + code_html)

    # Combining everything into a final HTML
    final_html = f"""
    <html>
    <head>
    <title>Code Visualization</title>
    </head>
    <body>
    {"<hr>".join(htmls)}
    </body>
    </html>
    """
    file_name = args.jsonl.replace(".jsonl", ".html")

    print(f"Writing to {file_name}")
    with open(file_name, "w") as f:
        f.write(final_html)
