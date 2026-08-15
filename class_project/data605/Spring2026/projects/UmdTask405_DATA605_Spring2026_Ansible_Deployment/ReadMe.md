# Ansible

## Description
- Ansible is an open-source automation tool used for application deployment,
  configuration management, and task automation.
- It uses a simple, human-readable YAML syntax to define automation tasks,
  making it accessible for users without extensive programming knowledge.
- Ansible operates in an agentless manner, meaning it does not require any
  software to be installed on the target machines, allowing for easier
  management of systems.
- It supports a wide range of modules for various tasks, including cloud
  provisioning, orchestration, and security compliance, enabling extensive
  automation capabilities.
- Ansible is designed to be idempotent, which means that running the same
  playbook multiple times will not change the system beyond the initial
  application, ensuring stability and predictability.

## How to run the project
## 🚀 Step-by-Step Execution


### Step 1 — Build the Docker image

```bash
docker build -t house-price-project .
```

> This installs all dependencies from `requirements.txt` and sets up
> JupyterLab inside the container. Takes ~3–5 minutes on first build.

### Step 2 — Start the container

```bash
docker run -it -p 5001:5000 -p 8888:8888 \
  --name house-price \
  -v $(pwd):/project \
  house-price-project
```
| Flag | Meaning |
|------|---------|
| `-it` | Interactive shell |
| `-p 5001:5000` | Mac port 5001 → container port 5000 (Flask API) |
| `-p 8888:8888` | Mac port 8888 → container port 8888 (JupyterLab) |
| `--name house-price` | Give the container a fixed name |
| `-v $(pwd):/project` | Mount project folder so files persist |

You will land inside the container at `root@container:/project#`.

### Step 3 — Train the model

Inside the container:

If you want to run the JupyterLab interface, execute:
```bash
PORT=5000 jupyter lab --ip=0.0.0.0 --no-browser --allow-root
```

 if you want to run the training script, execute:
```bash
python template.example.py
```

Expected output:
WARNING: File 'ml_model/train.csv' not found – generating synthetic dataset.
INFO: Dataset shape: (1460, 16)
INFO: Cross-validating GradientBoosting (5 folds)…
INFO: Cross-validating RandomForest (5 folds)…
INFO: Cross-validating Ridge (5 folds)…
INFO: Best model: GradientBoosting
INFO: Test R²: 0.9822
INFO: Model saved to '/project/ml_model/house_price_model.pkl'.

> If you have the Kaggle dataset, place `train.csv` in `ml_model/` before
> running this step to train on real data instead of synthetic data.

### Step 4 — Start the Flask API

Inside the container (keep this terminal open):

```bash
PORT=5000 python app.py
```

then in Jupyter Notebook run template.API.py inside the notebook and run the cells

Once everything is done, you can run the whole process using Ansible. Make sure you have ansible installed and configured properly. Then, execute the following command in your terminal:

```bash
ansible-playbook playbook.yml
```


## Project Objective
The goal of the project is to automate the deployment of a machine learning
model using Ansible. Students will create a playbook that provisions a virtual
machine, installs necessary dependencies, and deploys a pre-trained model to
serve predictions via a REST API. The project will optimize the deployment
process to ensure it is efficient and reproducible.

## Dataset Suggestions
1. **Kaggle House Prices Dataset**
   - **Source Name**: Kaggle
   - **URL**:
     [Kaggle House Prices](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data)
   - **Data Contains**: Various features of houses in Ames, Iowa, including sale
     prices, which can be used for regression tasks.
   - **Access Requirements**: Free account on Kaggle.

2. **UCI Machine Learning Repository: Wine Quality Dataset**
   - **Source Name**: UCI Machine Learning Repository
   - **URL**:
     [Wine Quality Dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality)
   - **Data Contains**: Chemical properties of wine samples along with quality
     ratings, suitable for classification tasks.
   - **Access Requirements**: No authentication required.

3. **Open Government Data: NYC Taxi Trip Data**
   - **Source Name**: NYC Open Data
   - **URL**: [NYC Taxi Trip Data](https://opendata.cityofnewyork.us/)
   - **Data Contains**: Trip records including pickup and drop-off locations,
     times, and fares, which can be used for regression or clustering tasks.
   - **Access Requirements**: Publicly available without authentication.

## Tasks
- **Set Up Virtual Environment**: Create a virtual machine using Ansible to host
  the machine learning model.
- **Install Dependencies**: Write Ansible tasks to install necessary libraries
  and frameworks (e.g., Flask, scikit-learn) for serving the model.
- **Deploy Model**: Use Ansible to copy the pre-trained model files to the
  virtual machine and configure the application to serve predictions.
- **Create REST API**: Implement a simple REST API using Flask to handle
  incoming prediction requests and return results.
- **Testing and Validation**: Write Ansible tasks to test the deployment and
  validate that the API is returning the expected outputs.

## Bonus Ideas
- **Monitoring and Logging**: Extend the project by integrating monitoring tools
  (e.g., Prometheus) to keep track of API performance and logs.
- **Scaling Deployment**: Explore how to scale the deployment across multiple
  servers using Ansible's orchestration capabilities.
- **CI/CD Pipeline**: Implement a continuous integration/continuous deployment
  (CI/CD) pipeline to automate updates to the model and application.

## Useful Resources
- [Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html)
- [Ansible GitHub Repository](https://github.com/ansible/ansible)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
- [Flask Documentation](https://flask.palletsprojects.com/)