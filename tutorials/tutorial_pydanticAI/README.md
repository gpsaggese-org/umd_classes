# PydanticAI Tutorial

This folder contains the setup for running PydanticAI tutorials within a
containerized environment.

## Quick Start

From the root of the repository, change your directory to the PydanticAI
tutorial folder:

```bash
> cd tutorials/tutorial_pydanticAI
```

Once the location has been changed to the repo run the command to build the
image to run dockers:

```bash
> ./docker_build.sh
```

Once the docker has been built you can then go ahead and run the container and
launch jupyter notebook using the created image using the command:

```bash
> ./docker_jupyter.sh
```

Once the `./docker_jupyter.sh` script is running, work through the following
notebooks in order.

For more information on the Docker build system refer to [Project template
README](/class_project/project_template/README.md)

## Tutorial Notebooks

Work through the following notebooks in order:

- [`pydanticai.API.ipynb`](pydanticai.API.ipynb): Core PydanticAI fundamentals
  - Understanding the PydanticAI framework architecture
  - Working with PydanticAI classes and methods
  - Building basic agent configurations
  - Integration with language models

- [`pydanticai.example.ipynb`](pydanticai.example.ipynb): Real-world application
  workflow
  - End-to-end agentic application example
  - Practical problem-solving with PydanticAI
  - Advanced agent interactions and workflows
  - Best practices and patterns

- [`pydanticai_API_utils.py`](pydanticai_API_utils.py): Utility functions
  supporting the API tutorial notebook

- [`pydanticai_example_utils.py`](pydanticai_example_utils.py): Utility
  functions supporting the example tutorial notebook
