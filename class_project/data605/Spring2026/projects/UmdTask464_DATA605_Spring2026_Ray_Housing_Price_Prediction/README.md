# \# Ray Housing Price Prediction

# 

# A scalable end-to-end machine-learning pipeline that predicts California

# median house values using \*\*Ray\*\* for distributed data loading, parallel

# training, hyperparameter tuning, and model serving.

# 

# This project is a tutorial-style introduction to Ray's core APIs in the

# context of a realistic regression problem: a curious computer scientist

# should be able to read this README and the two notebooks and understand

# what Ray offers in roughly 60 minutes.

# 

# \---

# 

# \## Table of Contents

# 

# 1\. \[What is Ray?](#what-is-ray)

# 2\. \[Project Objective](#project-objective)

# 3\. \[File Layout](#file-layout)

# 4\. \[Quick Start](#quick-start)

# 5\. \[Running the Notebooks](#running-the-notebooks)

# 6\. \[Querying the Deployed Model](#querying-the-deployed-model)

# 7\. \[Results](#results)

# 8\. \[Architectural Decisions](#architectural-decisions)

# 9\. \[References](#references)

# 

# \---

# 

# \## What is Ray?

# 

# \[Ray](https://www.ray.io/) is an open-source framework for distributed

# Python. It provides a single API for scaling code across multiple cores

# and machines, plus a stack of higher-level libraries built on top of

# that core:

# 

# | Library       | What it does                                       |

# | ------------- | -------------------------------------------------- |

# | \*\*Ray Core\*\*  | Task and actor parallelism (`@ray.remote`)         |

# | \*\*Ray Data\*\*  | Distributed data loading and preprocessing         |

# | \*\*Ray Tune\*\*  | Distributed hyperparameter search                  |

# | \*\*Ray Serve\*\* | Scalable model serving as a REST endpoint          |

# 

# This project uses all four to take a problem from raw data to a live API.

# 

# \## Project Objective

# 

# Predict the \*\*median house value\*\* in California census tracts from

# features such as median income, average rooms, location, and population.

# The dataset is the standard scikit-learn `fetch\_california\_housing` dump

# (20,640 rows × 8 features), so the project is reproducible without any

# authentication or external download.

# 

# The pipeline:

# 

# 1\. Load and wrap the dataset with \*\*Ray Data\*\*

# 2\. Train a baseline `RandomForestRegressor` with scikit-learn

# 3\. Run multiple training jobs in parallel with \*\*Ray Core\*\* (`@ray.remote`)

# 4\. Search the hyperparameter space with \*\*Ray Tune\*\*

# 5\. Deploy the best model as a REST API with \*\*Ray Serve\*\*

# 

# \## File Layout

```

.

├── Dockerfile                  # python:3.12-slim base + Ray + ML stack

├── .dockerignore

├── .gitignore

├── README.md                   # this file

├── requirements.txt            # pinned Python dependencies

├── ray\_utils.py                # load\_data() helper (uses Ray Data)

├── ray\_housing.API.ipynb       # Tour of Ray's native APIs

├── ray\_housing.example.ipynb   # End-to-end housing pipeline

│

├── docker\_build.sh             # Build the project's Docker image

├── docker\_bash.sh              # Open a bash shell inside the container

├── docker\_jupyter.sh           # Start JupyterLab inside the container

├── docker\_clean.sh             # Remove the project's Docker image

├── docker\_cmd.sh               # Run an arbitrary command in the container

├── docker\_exec.sh              # Attach to a running container

├── docker\_push.sh              # Push the image to a registry

├── docker\_name.sh              # Image-naming configuration

├── run\_jupyter.sh              # JupyterLab launcher (called inside Docker)

├── version.sh                  # Logs Python/pip/Jupyter versions during build

├── bashrc                      # Container shell configuration

└── etc\_sudoers                 # Container sudoers file

```

The `docker\_\*.sh` scripts and the support files (`bashrc`, `etc\_sudoers`,

`version.sh`, `.dockerignore`, `Dockerfile`) come from the canonical

class template at `class\_project/project\_template/`. Only `Dockerfile`,

`docker\_name.sh`, and `requirements.txt` were customized for this

project.



\## Quick Start



\### Prerequisites



\- \[Docker Desktop](https://www.docker.com/products/docker-desktop/)

&#x20; (or any working Docker daemon) running on your machine

\- A Bash-compatible shell (Git Bash on Windows, any terminal on macOS / Linux)



\### Build the image



From this project directory:



```bash

./docker\_build.sh

```



The first build takes 5–10 minutes. It downloads `python:3.12-slim`,

installs Ray, scikit-learn, JupyterLab and all transitive dependencies,

and produces an image named:

```

gpsaggese/umd\_data605\_spring2026\_ray\_housing\_price\_prediction:latest

```

The final image is roughly 1.7 GB.



\### Verify the build



```bash

docker images gpsaggese/umd\_data605\_spring2026\_ray\_housing\_price\_prediction

```



You should see one row with size ≈ 1.7 GB.



\## Running the Notebooks



\### Start JupyterLab inside the container



```bash

./docker\_jupyter.sh

```



This:



\- Starts a container from the project image

\- Mounts the current directory at `/data` inside the container

\- Launches JupyterLab on port 8888 with no token / password (development mode)



Open <http://localhost:8888> in your browser. You'll see this project's

files in the file browser.



\### Notebook tour



\- \*\*`ray\_housing.API.ipynb`\*\* — A short, didactic walk through Ray's

&#x20; core APIs in isolation: `@ray.remote`, `ray.data.from\_pandas`,

&#x20; `tune.run`, `@serve.deployment`. Read this first if you've never used

&#x20; Ray.

\- \*\*`ray\_housing.example.ipynb`\*\* — The applied end-to-end pipeline:

&#x20; load housing data, train a baseline model, distribute multiple

&#x20; training runs, tune hyperparameters, and deploy the best model as a

&#x20; REST API.



Run the cells top-to-bottom. The Ray Tune section takes \~2–3 minutes;

everything else is fast.



\## Querying the Deployed Model



Once `ray\_housing.example.ipynb` has run the Ray Serve cell, the model

listens on port 8000 inside the container. Because the container maps

that port to the host, you can query it with `curl` or `requests`:



```bash

curl -X POST http://127.0.0.1:8000/ \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"features": \[8.3252, 41.0, 6.984, 1.024, 322.0, 2.556, 37.88, -122.23]}'

```



Expected response:



```json

{"prediction": 4.32}

```



The eight features, in order, are:

`MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude`.

The prediction is the median house value in \*\*hundreds of thousands of

dollars\*\* (so `4.32` ≈ $432,000), matching the `MedHouseVal` units in

the original dataset.



\## Results



Baseline `RandomForestRegressor` (`n\_estimators=100`, default depth):



| Metric  | Value |

| ------- | ----- |

| RMSE    | \~0.51 |

| R²      | \~0.81 |



After Ray Tune sweeps over `n\_estimators ∈ {50, 100, 200}` and

`max\_depth ∈ {5, 10, 20}`, the best configuration improves RMSE to

roughly 0.49 (final numbers depend on the random seed of each Tune

trial).



The tuned model is the one served by the Ray Serve endpoint.



\## Architectural Decisions



A few non-obvious choices worth flagging for graders and future

maintainers.



\*\*Base image: `python:3.12-slim`.\*\* The class template offers Ubuntu,

Python-slim, and `uv`-based variants. Slim was chosen because this

project doesn't need system tools like `postgresql-client` or `graphviz`,

and the smaller base shaves both build time and final image size.



\*\*Ray version: `2.49.0`.\*\* Pinned for reproducibility. Ray < 2.31 has no

Python 3.12 wheels; Ray 2.49 is recent enough to be supported and stable

enough to have known-good behavior with the Tune and Serve APIs used

here.



\*\*Ray Data inside `load\_data()`.\*\* The brief asks the project to use

Ray Data for loading and preprocessing. `ray\_utils.load\_data()` calls

`ray.data.from\_pandas(...)` and returns the materialized DataFrame, so

the rest of the pipeline can stay in pandas-land. A future iteration

could keep the data as a Ray `Dataset` and use `.map\_batches()` for

preprocessing.



\*\*Single REST endpoint.\*\* Ray Serve makes multi-endpoint deployments

trivial, but this project exposes one POST handler at `/` for clarity.

The class returns JSON with the predicted value and nothing else.



\## References



\- Ray documentation: <https://docs.ray.io/en/latest/>

\- California Housing dataset:

&#x20; \[`sklearn.datasets.fetch\_california\_housing`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch\_california\_housing.html)

\- Class project template guide:

&#x20; `class\_project/project\_template/README.md` in this repo

\- Project guidelines:

&#x20; `class\_project/data605/Spring2026/Class\_Project\_Guidelines.md`



\---



\*Project tag: `UmdTask464\_DATA605\_Spring2026\_Ray\_Housing\_Price\_Prediction`\*

