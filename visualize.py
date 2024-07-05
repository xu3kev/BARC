import json
import argparse
import numpy as np
from utils import remove_trailing_code, generate_html_grid
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import hashlib

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

        # create unique ID for each problem
        # The ID string consists of two parts: hash from the code and hash from the examples
        # This is to ensure that the ID is unique for each problem

        hash_code = hashlib.md5(code.encode()).hexdigest()
        # use the first 4 examples to create the hash
        hash_examples = hashlib.md5(str(examples[0:4]).encode()).hexdigest()
        uid = f"{hash_code[0:8]}{hash_examples[0:8]}"

        examples_input_output = [ {"input": input_grid, "output": output_grid}
                                    for input_grid, output_grid in zip(input_grids, output_grids) 
                                    if isinstance(output_grid, np.ndarray) ]

        if len(examples_input_output) == 0:
            assert False, "No valid input-output examples found"

        grid_html = generate_html_grid(examples_input_output)
        code_html = highlight_code(code)
        
        problem_html = f"""
        <div class="problem" id="problem_{idx}" style="display: {'block' if idx == 0 else 'none'};">
            <h2>Problem UID {uid}</h2>
            {grid_html}
            <div style="text-align: center; margin-top: 20px;">
                <button class="good-button" id="good_{idx}" onclick="annotate('good', {idx})">Good</button>
                <button class="bad-button" id="bad_{idx}" onclick="annotate('bad', {idx})">Bad</button>
            </div>
            {code_html}
        </div>
        """
        htmls.append(problem_html)

    final_html = f"""
    <html>
    <head>
    <title>Code Visualization</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {{
            padding: 0 10%;
        }}
        .navigation-arrow {{
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            font-size: 48px;
            color: #333;
            cursor: pointer;
            z-index: 1000;
        }}
        .prev-arrow {{
            left: 10px;
        }}
        .next-arrow {{
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
.good-button.pressed {{
    background-color: #2E7D32; /* Darker green */
    box-shadow: inset 0 0 10px #000; /* More pronounced shadow */
    transform: translateY(2px); /* Slight downward movement */
    color: #fff; /* Ensure text color remains white */
    font-weight: bold; /* Make text bold when pressed */
}}
.bad-button.pressed {{
    background-color: #C62828; /* Darker red */
    box-shadow: inset 0 0 10px #000; /* More pronounced shadow */
    transform: translateY(2px); /* Slight downward movement */
    color: #fff; /* Ensure text color remains white */
    font-weight: bold; /* Make text bold when pressed */
}}
        #progress {{
            position: fixed;
            top: 10px;
            right: 10px;
            font-size: 24px;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
    </head>
    <body>
    <div class="navigation-arrow prev-arrow" onclick="prevProblem()">
        <i class="fas fa-arrow-left"></i>
    </div>
    <div class="navigation-arrow next-arrow" onclick="nextProblem()">
        <i class="fas fa-arrow-right"></i>
    </div>
    <div id="progress">0/{total_problems}</div>
    <div>
        {"".join(htmls)}
    </div>
    <script>
        let currentProblem = 0;
        let totalProblems = {total_problems};
        let annotatedCount = 0;
        let annotations = new Array(totalProblems).fill(null);

        function showProblem(index) {{
            document.querySelector(`#problem_${{currentProblem}}`).style.display = 'none';
            document.querySelector(`#problem_${{index}}`).style.display = 'block';
            currentProblem = index;
            updateProgress();
            updateButtons();
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
            annotations[index] = annotation;
            annotatedCount = annotations.filter(a => a !== null).length;
            updateProgress();
            updateButtons();
        }}

        function updateProgress() {{
            document.getElementById('progress').textContent = `${{annotatedCount}}/${{totalProblems}}`;
        }}

        function updateButtons() {{
            const goodButton = document.getElementById(`good_${{currentProblem}}`);
            const badButton = document.getElementById(`bad_${{currentProblem}}`);
            goodButton.classList.remove('pressed');
            badButton.classList.remove('pressed');
            if (annotations[currentProblem] === 'good') {{
                goodButton.classList.add('pressed');
            }} else if (annotations[currentProblem] === 'bad') {{
                badButton.classList.add('pressed');
            }}
        }}
    </script>
    </body>
    </html>
    """
    file_name = args.jsonl.replace(".jsonl", ".html")

    print(f"Writing to {file_name}")
    with open(file_name, "w") as f:
        f.write(final_html)
