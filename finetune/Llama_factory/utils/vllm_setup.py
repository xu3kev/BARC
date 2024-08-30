import socket
import os
from time import sleep
import subprocess
from openai import OpenAI
import tempfile

HOME_DIRECTORY = "/home/kh844/Fine-tune/LLaMA-Factory/"

def find_available_port(start_port=8000, max_attempts=100):
    for port in range(start_port, start_port + max_attempts):
        try:
            # Create a new socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Try to bind the socket to the port
                sock.bind(("", port))
                # If successful, return the port
                return port
        except socket.error:
            # If there is an error binding to the port, continue to the next port
            continue
    # If no ports are available in the range, raise an exception
    raise RuntimeError(f"No available ports found starting from {start_port}.")

#  API_PORT=8000 llamafactory-cli api examples/inference/llama31_vllm.yaml

def start_model_server():
    def get_model(client):
        models = client.models.list()
        model = models.data[0].id
        return model
    
    available_port = find_available_port(8000)
    command_args = [
        'llamafactory-cli',
        'api',
        'examples/inference/llama31_vllm.yaml'
    ]

    myenv = os.environ.copy()
    myenv['API_PORT'] = str(available_port)
    stdout_tempfile = tempfile.NamedTemporaryFile("w", delete=False)
    stderr_tempfile = tempfile.NamedTemporaryFile("w", delete=False)
    print(f"Logging model outputs at {stdout_tempfile.name} and {stderr_tempfile.name}")
    cwd = HOME_DIRECTORY
    process = subprocess.Popen(
        command_args, stdout=stdout_tempfile, stderr=stderr_tempfile, env=myenv, cwd=cwd
    )

    client = OpenAI(base_url=f"http://localhost:{str(available_port)}/v1", api_key="empty")
    def wait_for_server():
        try:
            model = get_model(client)
            assert model
            print("Model server started successfully!")
            return True
        except Exception as e:
            with open(stdout_tempfile.name, 'r') as f:
                stdout = f.read()
            with open(stderr_tempfile.name, 'r') as f:
                stderr = f.read()
            print(stdout)
            print(stderr)
            sleep(10)
            return wait_for_server()

    wait_for_server()
    sleep(3)
    return process, available_port, f"http://localhost:{str(available_port)}/v1"