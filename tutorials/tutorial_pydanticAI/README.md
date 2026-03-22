<!-- toc -->

- [Project files](#project-files)
- [Setup and Dependencies](#setup-and-dependencies)
  * [Building and Running the Docker Container](#building-and-running-the-docker-container)
    + [Environment Setup](#environment-setup)

<!-- tocstop -->

# Project files

This project contains the following files.

- `README.md`: This file
- `pydanticai.API.ipynb`: notebook describing core PydanticAI APIs
- `pydanticai.example.ipynb`: notebook with applied, end-to-end examples
- `requirements.txt`: Python dependencies used by this tutorial
- `example_dataset/`: supporting markdown files used in examples
  - `api.md`
  - `billing.md`
  - `integrations.md`
  - `limits.md`
  - `overview.md`
  - `security.md`
  - `support.md`
  - `troubleshooting.md`
- Docker/dev runtime files
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

# Setup and Dependencies

## Building and Running the Docker Container

- Go to the project directory:
  ```bash
  > cd tutorials/tutorial_pydanticAI
  ```
- Build Docker image:
  ```bash
  > ./docker_build.sh
  ```
- Run container shell:
  ```bash
  > ./docker_bash.sh
  ```
- Launch Jupyter Notebook:
  ```bash
  > ./docker_jupyter.sh
  ```

### Environment Setup

Set the `OPENAI_API_KEY` environment variable for API access:

```python
import os
os.environ["OPENAI_API_KEY"] = "<your_openai_api_key>"
```

