# BambooAI Tutorial

This folder contains the setup for running BambooAI tutorials within a
containerized environment.

## Quick Start

From the root of the repository, change your directory to the BambooAI tutorial folder:

```bash
> cd tutorials/BambooAI
```

Once the location has been changed to the repo run the command to build the image
to run dockers:

```bash
> ./docker_build.sh
```

Once the docker has been built you can then go ahead and run the container and
launch jupyter notebook using the created image using the command:

```bash
> ./docker_jupyter.sh
```

Once the `./docker_jupyter.sh` script is running, follow this sequence to explore
the tutorials:

1. **`bambooai.API.ipynb`**: Start here to master the fundamental classes,
   methods, and basic configurations of the BambooAI framework.
2. **`bambooai.example.ipynb`**: Proceed to this notebook to explore a complete,
   real-world application workflow using BambooAI.

For more information on the Docker build system refer to [Project template
README](https://github.com/gpsaggese/umd_classes/blob/master/class_project/project_template/README.md)

## Changelog

- 2026-03-15: Initial release
