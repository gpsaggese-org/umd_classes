## Working on the Project

### Tutorial Goal

For your course project, you are not just building something — you are also
teaching others how to use a Big Data, AI, LLM, or data science technology. The
deliverable is a hands-on, beginner-friendly tutorial that teaches the
technology in 60 minutes.

Each 60-minute tutorial follows this time breakdown for a reader:

1. **Setup (5 min)**: Clone repo, start Docker container, verify environment
2. **Introduction (10 min)**: Read overview markdown, understand use cases
3. **API Exploration (20 min)**: Work through `{project}.API.ipynb` notebook
4. **Complete Example (25 min)**: Work through `{project}.example.ipynb`
   notebook

Each tutorial aims to provide:

- **Conceptual understanding**: Clear explanations of what the technology is and
  when to use it
- **Practical application**: A complete example showing real-world usage and
  working code examples that run immediately
- **Reproducibility**: Guaranteed to work through automated testing with all
  dependencies and setup handled via Docker

### Invariants

All tutorials must maintain these standards:

- **Code repository**: All code is on GitHub in a format common to all tutorials
- **Dependency management**: All packages are handled through Docker in a
  standard approach (e.g., `docker_build`, `docker_bash`)
- **Consistent structure**: The format of the tutorial follows the same
  structure across all topics
- **Centralized location**: All tutorial material is in a directory in the
  [`tutorials`](https://github.com/gpsaggese/umd_classes/tree/master/tutorials)
  repo and in the [`//helpers`](https://github.com/causify-ai/helpers) sub-repo

### Understanding the Deliverables

- Use the example tutorials (e.g., `tutorials/autogen`, `tutorials/tensorflow`)
  and `class_project/project_template` to understand the deliverables and
  coding style. They consist of:

- **Utils Module** (`{project}_utils.py`):
  - Contains helper functions, reusable logic, and wrappers around the tool
  - Keep the notebooks focused on documentation and outputs; place all logic
    inside this module
- **API Notebook** (`{project}.API.ipynb`):
  - Explores the tool's native API: core classes, functions, and configuration
  - Describes the lightweight wrapper layer you have written on top
  - Contains a walkthrough of the library/package with examples
  - Uses simple/synthetic examples since it needs to run quickly
  - Most code should be moved to a `*_utils.py` file
- **Example Notebook** (`{project}.example.ipynb`):
  - Demonstrates an end-to-end application using your wrapper layer
  - Calls functions from `{project}_utils.py` to keep cells concise

In general:

- **For API notebook**: describe the tool's architecture, key abstractions, and
  how your wrapper simplifies it
- **For example notebook**: demonstrate the tool according to the specifications
  in your project description

### Docker Container

- The Docker container should:
  - Contain everything so that one is ready to run tutorials and develop with
    that technology
  - Often installing and getting a package to work (e.g., PyMC) takes a long
    time

- The Docker structure and approach should follow the template
  [`class_project/project_template/`](https://github.com/gpsaggese/umd_classes/tree/master/class_project/project_template)

### Jupyter Notebooks

- Each Jupyter notebook should:
  - Run end-to-end after a restart
    - It's super frustrating when a tutorial doesn't work because the version of
      the library is not compatible with the code anymore
    - This is enforced by the unit test through `pytest`, in this way we are
      guaranteed that it works
  - Be self-contained and linear
    - Each example is explained thoroughly without having to jump from tutorial
      to tutorial
    - Each cell and its output is commented and explained
  - Take less than a few minutes to execute end-to-end

### Markdown

- Markdown documents should cover information about:
  - What the technology/Python package or library is
  - What problem it solves
  - What are the alternatives, both open source and commercial with comments
    about advantages and disadvantages
  - A description of the native API of the technology
  - A description of the Docker container
  - Visual aids with `mermaid`, `graphviz`, `tikz` (e.g., flow diagrams, data
    transformation steps, and plots) to enhance understanding of how the library
    and the example works
  - References to books and in-depth tutorials that we have run and we think are
    awesome
  - All sources should be referred and acknowledged

- This is the same approach used in:
  - [DATA605](https://github.com/gpsaggese/umd_classes/blob/master/data605/tutorials)
    - E.g., Git, Docker, Docker Compose, Postgres, MongoDB, Airflow, Dask, Spark
  - [MSML610](https://github.com/gpsaggese/umd_classes/blob/master/msml610/tutorials/notebooks)

### Tools of the Trade

- Format a markdown file:
  ```bash
  > lint_txt.py -i ...
  ```

- Clean up the Python code using Claude Code:
  ```bash
  cc> Execute docs/ai_prompts/coding.lint.md on tutorials/Autogen/autogen_utils.py
  ```

- Render the blogs locally:
  ```bash
  > website/test.sh
  ```

## Submission

Your submission must include the following files:

- `{project}.API.ipynb`:
  - A `Jupyter` notebook exploring the tool's native API: core classes,
    functions, and configuration
  - Describes the lightweight wrapper layer you have written on top
  - Contains a walkthrough of the library/package with examples
  - Uses simple/synthetic examples so it runs quickly

- `{project}.example.ipynb`:
  - A `Jupyter` notebook demonstrating an end-to-end application
  - Calls functions from `{project}_utils.py` to keep cells concise

- `{project}_utils.py`:
  - A `Python` module containing reusable utility functions and wrappers around
    the package
  - The notebooks should invoke logic from this file instead of embedding
    complex code inline

### Folder Structure

```text
COURSE_CODE/
└── Term20xx/
    └── projects/
        └── TutorTaskXX_Name_of_issue/
            ├── {project}_utils.py       # reusable helper functions
            ├── {project}.API.ipynb      # tool's native API exploration
            ├── {project}.example.ipynb  # end-to-end application demo
            ├── Dockerfile
            ├── docker_build.sh          # build the Docker image
            ├── docker_bash.sh           # open a shell in the container
            ├── docker_jupyter.sh        # launch Jupyter inside the container
            ├── docker_clean.sh          # remove the container and image
            ├── requirements.txt
            └── README.md
```
