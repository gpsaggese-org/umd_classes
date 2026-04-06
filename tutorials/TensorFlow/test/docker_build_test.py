import os
import subprocess
import sys

# Docker image name
DOCKER_IMAGE = "gpsaggese/umd_tutorial_tensorflow:latest"
NOTEBOOK_DIR = "tutorials/TensorFlow"  # folder containing notebooks


def image_exists() -> bool:
    """
    Check if the Docker image already exists locally.
    """
    result = subprocess.run(
        ["docker", "images", "-q", DOCKER_IMAGE], capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def build_container():
    """
    Build the Docker container if it doesn't exist.
    """
    if image_exists():
        print(f"Docker image {DOCKER_IMAGE} already exists. Skipping build.")
        return
    print("Building Docker container...")
    result = subprocess.run(
        ["docker", "build", "-t", DOCKER_IMAGE, "."],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Docker build failed:")
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Docker build failed")
    print("Docker container built successfully.")


def run_notebooks_in_container():
    """
    Run all notebooks inside the Docker container using nbconvert.
    """
    print("Running notebooks inside Docker container...")
    project_dir = os.getcwd()
    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{project_dir}:/curr_dir",
        DOCKER_IMAGE,
        "bash",
        "-c",
        "for nb in /curr_dir/*.ipynb; do "
        "echo 'Running $nb...'; "
        'jupyter nbconvert --to notebook --execute --inplace "$nb" || exit 1; '
        "done",
    ]
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        print(" Notebook execution failed inside Docker container")
        sys.exit(1)
    print(" All notebooks ran successfully inside Docker container")


if __name__ == "__main__":
    build_container()
    run_notebooks_in_container()
