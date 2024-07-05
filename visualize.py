import json
import argparse
import numpy as np
from utils import remove_trailing_code, generate_html_grid
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import hashlib
import base64

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
        hash_code = hashlib.md5(code.encode()).hexdigest()
        hash_examples = hashlib.md5(str(examples[0:4]).encode()).hexdigest()
        uid = f"{hash_code[0:8]}{hash_examples[0:8]}"

        examples_input_output = [ {"input": input_grid.tolist(), "output": output_grid.tolist()}
                                    for input_grid, output_grid in zip(input_grids, output_grids) 
                                    if isinstance(output_grid, np.ndarray) ]

        if len(examples_input_output) == 0:
            assert False, "No valid input-output examples found"

        grid_html = generate_html_grid(examples_input_output, uid)
        code_html = highlight_code(code)

        # Encode the source code in base64
        code_base64 = base64.b64encode(code.encode()).decode()
        json_data = {
            "uid": uid,
            "examples": examples_input_output,
            "code": code,
            "metadata": {
                "source_file": args.jsonl
            }
        }
        json_data_base64 = base64.b64encode(json.dumps(json_data).encode()).decode()

        problem_html = f"""
        <div class="problem" id="problem_{idx}" style="display: {'block' if idx == 0 else 'none'};">
            <h2>Problem UID {uid}</h2>
            {grid_html}
            <div style="text-align: center; margin-top: 20px;">
                <div style="font-size:32px">Grid Example</div>
                <button class="good-button" id="example_good_{idx}" onclick="annotate('example', 'good', {idx})">Good</button>
                <button class="ok-button" id="example_ok_{idx}" onclick="annotate('example', 'ok', {idx})">Ok</button>
                <button class="bad-button" id="example_bad_{idx}" onclick="annotate('example', 'bad', {idx})">Bad</button>
                <br>
                <div style="font-size:32px">Solution Code</div>
                <button class="good-button" id="code_good_{idx}" onclick="annotate('code', 'good', {idx})">Good</button>
                <button class="ok-button" id="code_ok_{idx}" onclick="annotate('code', 'ok', {idx})">Ok</button>
                <button class="bad-button" id="code_bad_{idx}" onclick="annotate('code', 'bad', {idx})">Bad</button>
                <br>
                <button class="download-button" onclick="download_to_file('{uid}.py', '{code_base64}')">Download Source Code</button>
                <button class="download-button" onclick="download_to_file('{uid}.json', '{json_data_base64}')">Download JSON Data</button>
                <button class="download-button" onclick="download_div_to_image('img_{uid}', '{uid}.png')">Download Image</button>
            </div>
            {code_html}
        </div>
        """
        htmls.append(problem_html)

    final_html = f"""
    <html>
    <head>
    <title>Code Visualization</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
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
        .good-button, .ok-button, .bad-button, .download-button {{
            font-size: 24px;
            padding: 10px 20px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s, box-shadow 0.3s;
        }}
        .ok-button {{
            background-color: #FFC107;
            color: white;
        }}
        .ok-button:hover {{
            background-color: #FFA000;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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
        .ok-button.pressed {{
            background-color: #FFA000; /* Darker orange */
            box-shadow: inset 0 0 10px #000; /* More pronounced shadow */
            transform: translateY(2px); /* Slight downward movement */
            color: #fff; /* Ensure text color remains white */
            font-weight: bold; /* Make text bold when pressed */
        }}
        .download-button {{
            background-color: #2196F3;
            color: white;
        }}
        .download-button:hover {{
            background-color: #1976D2;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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
        all_metrics = ['example', 'code'];
        //let annotations = new Array(totalProblems).fill(null);
        // nested dict to store annotations for each metric
        let annotations = new Array(totalProblems).fill(null).map(() => Object.fromEntries(all_metrics.map(metric => [metric, null])));

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

        function annotate(metric_name, annotation, index) {{
            annotations[index][metric_name] = annotation;
            annotatedCount = annotations.filter(a => 
                            a !== null && a['example'] !== null && a['code'] !== null
            ).length;
            updateProgress();
            updateButtons();
        }}

        function updateProgress() {{
            document.getElementById('progress').textContent = `${{annotatedCount}}/${{totalProblems}}`;
        }}

        function updateButtons() {{
            const exampleGoodButton = document.getElementById(`example_good_${{currentProblem}}`);
            const exampleOkButton = document.getElementById(`example_ok_${{currentProblem}}`);
            const exampleBadButton = document.getElementById(`example_bad_${{currentProblem}}`);
            const codeGoodButton = document.getElementById(`code_good_${{currentProblem}}`);
            const codeOkButton = document.getElementById(`code_ok_${{currentProblem}}`);
            const codeBadButton = document.getElementById(`code_bad_${{currentProblem}}`);
            exampleGoodButton.classList.remove('pressed');
            exampleOkButton.classList.remove('pressed');
            exampleBadButton.classList.remove('pressed');
            codeGoodButton.classList.remove('pressed');
            codeOkButton.classList.remove('pressed');
            codeBadButton.classList.remove('pressed');
            if (annotations[currentProblem]['example'] === 'good') {{
                exampleGoodButton.classList.add('pressed');
            }} else if (annotations[currentProblem]['example'] === 'ok') {{
                exampleOkButton.classList.add('pressed');
            }} else if (annotations[currentProblem]['example'] === 'bad') {{
                exampleBadButton.classList.add('pressed');
            }}
            if (annotations[currentProblem]['code'] === 'good') {{
                codeGoodButton.classList.add('pressed');
            }} else if (annotations[currentProblem]['code'] === 'ok') {{
                codeOkButton.classList.add('pressed');
            }} else if (annotations[currentProblem]['code'] === 'bad') {{
                codeBadButton.classList.add('pressed');
            }}
        }}

        function download_to_file(filename, codeBase64) {{
            const code = atob(codeBase64);
            const blob = new Blob([code], {{ type: 'text/plain' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${{filename}}`;
            a.click();
            URL.revokeObjectURL(url);
        }}
        function download_div_to_image(div_id, filename) {{
            const div = document.getElementById(div_id);
            // add a pop-up indicating that the image is being generated
            const loading = document.createElement('div');
            loading.textContent = 'Generating image...';
            loading.style.position = 'fixed';
            loading.style.fontSize = '32px';
            loading.style.fontWeight = 'bold';
            loading.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
            loading.style.padding = '10px';
            loading.style.borderRadius = '5px';
            // center the loading pop-up
            loading.style.left = '50%';
            loading.style.top = '50%';
            loading.style.transform = 'translate(-50%, -50%)';
            loading.style.backdropFilter = 'blur(5px)';

            document.body.appendChild(loading);

    // add a short delay to ensure the loading pop-up is rendered
    setTimeout(() => {{
        html2canvas(div).then(canvas => {{
            // remove the loading pop-up
            document.body.removeChild(loading);
            // create an image from the canvas
            const image = canvas.toDataURL('image/png');
            // create a link to download the image
            const a = document.createElement('a');
            a.href = image;
            a.download = filename;
            a.click();
        }});
        }}, 100); // 100ms delay to ensure the pop-up is rendered
    }}
    </script>
    </body>
    </html>
    """
    file_name = args.jsonl.replace(".jsonl", ".html")

    print(f"Writing to {file_name}")
    with open(file_name, "w") as f:
        f.write(final_html)
