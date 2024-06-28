import json
import argparse
import numpy as np
from utils import remove_trailing_code, generate_html_grid
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def highlight_code(code):
    formatter = HtmlFormatter()
    highlighted_code = highlight(code, PythonLexer(), formatter)
    style = f"<style>{formatter.get_style_defs('.highlight')}</style>"
    return style + highlighted_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", type=str, required=True)
    args = parser.parse_args()

    with open(args.jsonl, "r") as f:
        data = [json.loads(line) for line in f]

    total_problems = len(data)
    htmls = []

    for idx, problem in enumerate(data):
        code = problem["source"]
        code = remove_trailing_code(code)
        
        examples = problem["examples"]
        input_grids = [np.array(example[0]) for example in examples[0:4]]
        output_grids = [np.array(example[1]) for example in examples[0:4]]

        examples_input_output = [ {"input": input_grid, "output": output_grid}
                                    for input_grid, output_grid in zip(input_grids, output_grids) 
                                    if isinstance(output_grid, np.ndarray) ]

        if len(examples_input_output) == 0:
            assert False, "No valid input-output examples found"

        grid_html = generate_html_grid(examples_input_output)
        code_html = highlight_code(code)
        
        problem_html = f"""
        <div class="problem" id="problem_{idx}" style="display: {'block' if idx == 0 else 'none'};">
            {grid_html}
            <div style="text-align: center; margin-top: 20px;">
                <button class="good-button" onclick="annotate('good', {idx})">Good</button>
                <button class="bad-button" onclick="annotate('bad', {idx})">Bad</button>
            </div>
            {code_html}
        </div>
        """
        htmls.append(problem_html)

    final_html = f"""
    <html>
    <head>
    <title>Code Visualization</title>
    <style>
        .navigation {{
            position: fixed;
            top: 10px;
            right: 10px;
        }}
        .good-button, .bad-button {{
            font-size: 24px;
            padding: 10px 20px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s, box-shadow 0.3s;
        }}
        .good-button {{
            background-color: #4CAF50;
            color: white;
        }}
        .good-button:hover {{
            background-color: #45a049;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .bad-button {{
            background-color: #f44336;
            color: white;
        }}
        .bad-button:hover {{
            background-color: #e53935;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
    </style>

    </head>
    <body>
    <div class="navigation">
        <button onclick="prevProblem()">Previous</button>
        <button onclick="nextProblem()">Next</button>
        <span id="progress">0/{total_problems}</span>
    </div>
    {"".join(htmls)}
    <script>
        let currentProblem = 0;
        let totalProblems = {total_problems};
        let annotatedCount = 0;

        function showProblem(index) {{
            document.querySelector(`#problem_${{currentProblem}}`).style.display = 'none';
            document.querySelector(`#problem_${{index}}`).style.display = 'block';
            currentProblem = index;
            updateProgress();
        }}

        function nextProblem() {{
            if (currentProblem < totalProblems - 1) {{
                showProblem(currentProblem + 1);
            }}
        }}

        function prevProblem() {{
            if (currentProblem > 0) {{
                showProblem(currentProblem - 1);
            }}
        }}

        function annotate(annotation, index) {{
            // Store the annotation (could be saved to a server or local storage)
            console.log(`Annotated problem ${{index}} as ${{annotation}}`);
            annotatedCount += 1;
            updateProgress();
        }}

        function updateProgress() {{
            document.getElementById('progress').textContent = `${{annotatedCount}}/${{totalProblems}}`;
        }}
    </script>
    </body>
    </html>
    """
    file_name = args.jsonl.replace(".jsonl", ".html")

    print(f"Writing to {file_name}")
    with open(file_name, "w") as f:
        f.write(final_html)
