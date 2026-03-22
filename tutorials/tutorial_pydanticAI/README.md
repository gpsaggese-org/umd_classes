# Summary
This directory contains a Docker-based development environment for the
`tutorial_pydanticAI` project with:

- Docker utility scripts for build, shell, command execution, cleanup, and push
- Jupyter launch scripts with configurable port, mount directory, and vim mode
- Tutorial notebooks and supporting markdown dataset files

## Project Files
- `README.md`
- `pydanticai.API.ipynb`
- `pydanticai.example.ipynb`
- `requirements.txt`
- `example_dataset/`
- Docker runtime files:
  - `Dockerfile`
  - `docker_build.sh`
  - `docker_bash.sh`
  - `docker_jupyter.sh`
  - `docker_exec.sh`
  - `docker_cmd.sh`
  - `docker_clean.sh`
  - `docker_push.sh`
  - `docker_name.sh`
  - `version.sh`
  - `run_jupyter.sh`
  - `etc_sudoers`

## Workflows
- Run all commands from this project directory:
  ```bash
  > cd tutorials/tutorial_pydanticAI
  ```

- Build the container:
  ```bash
  > ./docker_build.sh
  > ./docker_build.sh --no-cache
  > ./docker_bash.sh ls
  ```

- Enable verbose tracing:
  ```bash
  > ./docker_build.sh -v
  > ./docker_bash.sh -v
  ```

- Get help on any Docker script:
  ```bash
  > ./docker_build.sh -h
  > ./docker_jupyter.sh -h
  ```

- Start Jupyter:
  ```bash
  > ./docker_jupyter.sh
  # Open localhost:8888
  ```

- Start Jupyter on a specific port with vim keybindings:
  ```bash
  > ./docker_jupyter.sh -p 8890 -u
  # Open localhost:8890
  ```

## Environment Setup
Set the `OPENAI_API_KEY` environment variable before running notebook examples:

```python
import os
os.environ["OPENAI_API_KEY"] = "<your_openai_api_key>"
```
