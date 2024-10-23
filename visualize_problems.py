import json
import argparse
import numpy as np
from utils import remove_trailing_code, generate_html_grid
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import hashlib
import base64
import os

def highlight_code(code):
    formatter = HtmlFormatter()
    highlighted_code = highlight(code, PythonLexer(), formatter)
    style = f"<style>{formatter.get_style_defs('.highlight')}</style>"
    return style + highlighted_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", type=str, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--outdir", type=str, required=True)
    args = parser.parse_args()

    with open(args.jsonl, "r") as f:
        lines = f.readlines()
    
    print("Reading JSONL file...")
    from tqdm import tqdm
    data = [json.loads(line) for line in tqdm(lines)]

    try:
        print(f"Visualizing the subset from index {args.start} to {args.start + args.size - 1}")
        data = data[args.start:args.start + args.size]
    except IndexError:
        print(f"Error: Not enough problems in the JSONL file starting from index {args.start}")
        exit()

    total_problems = len(data)
    htmls = []

    all_uids = []
    for idx, problem in enumerate(data):
        code = problem["source"]
        seeds = problem["seeds"]
        
        code = remove_trailing_code(code)
        
        examples = problem["examples"]
        if len(examples) < 4:
            print(f"Skipping problem {idx} with less than 4 examples")
            continue
        input_grids = [np.array(example[0]) for example in examples[0:4]]
        output_grids = [np.array(example[1]) for example in examples[0:4]]

        # create unique ID for each problem
        hash_code = hashlib.md5(code.encode()).hexdigest()
        hash_examples = hashlib.md5(str(examples[0:4]).encode()).hexdigest()
        uid = f"{hash_code[0:8]}{hash_examples[0:8]}"
        all_uids.append(uid)

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
                "source_file": os.path.basename(args.jsonl)
            }
        }
        json_data_base64 = base64.b64encode(json.dumps(json_data).encode()).decode()
        # show a list of icon such as https://mc-larc.github.io/images/thumbnails/{seed_id}.png
        # along with the seed id as caption
        base_url = "https://mc-larc.github.io/images/thumbnails/"
        # seeds_html = "".join([f'<img src="{base_url}{seed_id[:-3]}.png" style="width: 100px; height: 100px; margin: 10px;">' for seed_id in seeds])
        def convert_seed_id(seed_id):
            ret = ""
            if seed_id.endswith(".py"):
                ret = seed_id[:-3]
            if "_" in ret:
                ret = ret.split("_")[0]
            return ret
        seeds_html = "".join([
    f'<div style="display: inline-block; text-align: center; margin: 10px;">'
    f'<img src="{base_url}{convert_seed_id(seed_id)}.png" style="width: 100px; height: 100px; margin: 10px;">'
    f'<div>{seed_id[:-3]}</div>'
    f'</div>'
    for seed_id in seeds
])

        problem_html = f"""
        <div class="problem" id="problem_{idx}" style="display: {'block' if idx == 0 else 'none'};">
            <h2>Problem UID {uid}</h2>
            <h3>Parent Seed IDs</h3>
            {seeds_html}
            <hr>
            {grid_html}
            <div style="text-align: center; margin-top: 20px;">
                <div style="font-size:32px">Problem Examples: <div style="font-size:17px">Considering the input/output examples, do they form a good ARC problem? A good ARC problem is one where you feel confident that you can explain the underlying transformation pattern to another person and where the problem is not overly trivial (although being easy is acceptable).</div></div>
                <button class="good-button" id="example_good_{idx}" onclick="annotate('example', 'good', {idx})">Good</button>
                <button class="ok-button" id="example_ok_{idx}" onclick="annotate('example', 'ok', {idx})">Ok</button>
                <button class="bad-button" id="example_bad_{idx}" onclick="annotate('example', 'bad', {idx})">Bad</button>
                <br>
                <div style="font-size:32px">Solution Code: <div style="font-size:17px">A solution code is "good" if the comment / code pair is consistent with a potential natural language transformation description</div></div>
                <button class="good-button" id="code_good_{idx}" onclick="annotate('code', 'good', {idx})">Good</button>
                <button class="ok-button" id="code_ok_{idx}" onclick="annotate('code', 'ok', {idx})">Ok</button>
                <button class="bad-button" id="code_bad_{idx}" onclick="annotate('code', 'bad', {idx})">Bad</button>
                <br>
                <button class="download-button" onclick="download_to_file('{uid}.py', '{code_base64}')">Download Source Code</button>
                <button class="download-button" onclick="download_with_annotations('{uid}.json', '{json_data_base64}', '{uid}')">Download JSON Data</button>
                <button class="download-button" onclick="download_div_to_image('img_{uid}', '{uid}.png')">Download Image</button>
            </div>
            {code_html}
        </div>
        """
        htmls.append(problem_html)

    all_uids_javascript_str = "const all_uids = " + json.dumps(all_uids) + ";"

    final_html = f"""
    <!DOCTYPE html>
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
        {all_uids_javascript_str}
        let currentProblem = 0;
        let currentUid = all_uids[currentProblem];
        const totalProblems = {total_problems};
        let annotatedCount = 0;

        const all_metrics = ['example', 'code'];

        //let annotations = new Array(totalProblems).fill(null).map(() => Object.fromEntries(all_metrics.map(metric => [metric, null])));
        // annotations is a dictionary of dictionaries, with the outer dictionary indexed by uid and the inner dictionary indexed by metric
        let annotations = {{}}
        all_uids.forEach(key => {{
            annotations[key] = {{}};
            all_metrics.forEach(metric => {{
                annotations[key][metric] = null;
            }});
        }});

        function getAnnotationCount() {{
            let count = 0;
            for (let i = 0; i < all_uids.length; i++) {{
                if (annotations[all_uids[i]]['example'] !== null && annotations[all_uids[i]]['code'] !== null) {{
                    count += 1;
                }}
            }}
            return count;
        }}
        function loadAnnotations() {{
            const savedAnnotations = localStorage.getItem('annotations');
            if (savedAnnotations) {{
                prev_annotations = JSON.parse(savedAnnotations);
                // get all notations from the previous annotations with the same uid
                for (let i = 0; i < all_uids.length; i++) {{
                    const uid = all_uids[i];
                    // check if the uid is in the previous annotations
                    if (uid in prev_annotations) {{
                        annotations[uid] = prev_annotations[uid];
                    }}
                }}
                annotatedCount = getAnnotationCount();
                updateProgress();
                updateButtons();
            }}
        }}

        function saveAnnotations() {{
            localStorage.setItem('annotations', JSON.stringify(annotations));
        }}

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
            annotations[all_uids[index]][metric_name] = annotation;
            annotatedCount = getAnnotationCount();
            saveAnnotations();
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
            if (annotations[all_uids[currentProblem]]['example'] === 'good') {{
                exampleGoodButton.classList.add('pressed');
            }} else if (annotations[all_uids[currentProblem]]['example'] === 'ok') {{
                exampleOkButton.classList.add('pressed');
            }} else if (annotations[all_uids[currentProblem]]['example'] === 'bad') {{
                exampleBadButton.classList.add('pressed');
            }}
            if (annotations[all_uids[currentProblem]]['code'] === 'good') {{
                codeGoodButton.classList.add('pressed');
            }} else if (annotations[all_uids[currentProblem]]['code'] === 'ok') {{
                codeOkButton.classList.add('pressed');
            }} else if (annotations[all_uids[currentProblem]]['code'] === 'bad') {{
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
            const loading = document.createElement('div');
            loading.textContent = 'Generating image...';
            loading.style.position = 'fixed';
            loading.style.fontSize = '32px';
            loading.style.fontWeight = 'bold';
            loading.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
            loading.style.padding = '10px';
            loading.style.borderRadius = '5px';
            loading.style.left = '50%';
            loading.style.top = '50%';
            loading.style.transform = 'translate(-50%, -50%)';
            loading.style.backdropFilter = 'blur(5px)';
            document.body.appendChild(loading);

            setTimeout(() => {{
                html2canvas(div).then(canvas => {{
                    document.body.removeChild(loading);
                    const image = canvas.toDataURL('image/png');
                    const a = document.createElement('a');
                    a.href = image;
                    a.download = filename;
                    a.click();
                }}).catch(error => {{
                    const loadingElement = document.getElementById('loadingPopup');
                    if (loadingElement) {{
                        document.body.removeChild(loadingElement);
                    }}
                    console.error('Error generating image:', error);
                }});
            }}, 100);
        }}

        function download_with_annotations(filename, jsonBase64, uid) {{
            const jsonData = JSON.parse(atob(jsonBase64));
            newJsonData = {{
                "uid": jsonData.uid,
                "annotations": annotations[uid],
                "metadata": jsonData.metadata,
                "examples": jsonData.examples,
                "code": jsonData.code,
            }};
            const updatedJsonBase64 = btoa(JSON.stringify(newJsonData, null, 2));
            download_to_file(filename, updatedJsonBase64);
        }}

        window.onload = function() {{
            loadAnnotations();
            showProblem(0);
        }};
    </script>
</body>
</html>
    """
    file_name = args.jsonl.replace(".jsonl", f"_start_{args.start}_size_{args.start + args.size}.html")
    if args.outdir:
        file_name = os.path.join(args.outdir, os.path.basename(file_name))

    print(f"Writing to {file_name}")
    with open(file_name, "w") as f:
        f.write(final_html)
