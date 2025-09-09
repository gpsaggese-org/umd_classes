**Description**

PyTorch Geometric is a library built on top of PyTorch designed for deep learning on irregular structures such as graphs. It provides a variety of tools and methods for working with graph-structured data, making it suitable for tasks like node classification, link prediction, and graph classification. 

Technologies Used
PyTorch Geometric

- Facilitates the implementation of graph neural networks (GNNs) with a focus on efficiency and scalability.
- Offers a range of pre-built models and layers for common graph tasks.
- Provides utilities for data loading, processing, and augmentation specific to graph data.

---

### Project 1: Social Network Node Classification
**Difficulty**: 1 (Easy)

**Project Objective**: The goal is to classify users in a social network based on their connections and attributes, optimizing for accuracy in predicting user types (e.g., influencers, casual users).

**Dataset Suggestions**: 
- Use the "Cora" dataset available on PyTorch Geometric (https://pytorch-geometric.readthedocs.io/en/latest/notes/introduction.html).

**Tasks**:
- **Data Loading**: Utilize PyTorch Geometric's data loaders to import the Cora dataset.
- **Graph Construction**: Construct a graph from the dataset, defining nodes and edges based on user relationships.
- **Model Training**: Implement a simple Graph Convolutional Network (GCN) to classify nodes.
- **Evaluation**: Measure the model's accuracy using train-test splits and visualize results with confusion matrices.

**Bonus Ideas**: 
- Experiment with different GNN architectures (e.g., GAT, GraphSAGE).
- Compare performance with traditional machine learning models like Random Forests or SVMs.

---

### Project 2: Molecular Property Prediction
**Difficulty**: 2 (Medium)

**Project Objective**: The objective is to predict molecular properties (e.g., solubility, toxicity) based on molecular graphs, optimizing for prediction accuracy and model interpretability.

**Dataset Suggestions**: 
- Use the "MoleculeNet" dataset, specifically the "ESOL" dataset for solubility prediction, available on Kaggle (https://www.kaggle.com/datasets/graphcore/esol).

**Tasks**:
- **Data Preparation**: Load and preprocess molecular graphs from the ESOL dataset.
- **Feature Engineering**: Generate features for nodes (atoms) and edges (bonds) in the molecular graphs.
- **Model Development**: Implement a GNN model to predict molecular properties.
- **Hyperparameter Tuning**: Optimize model parameters and evaluate using metrics like RMSE and MAE.

**Bonus Ideas**: 
- Extend the project to predict multiple properties simultaneously.
- Visualize molecular structures and their predicted properties using cheminformatics libraries.

---

### Project 3: Traffic Flow Prediction with Graph Neural Networks
**Difficulty**: 3 (Hard)

**Project Objective**: The goal is to predict traffic flow at various intersections in a city using historical traffic data represented as a graph, optimizing for forecasting accuracy and real-time performance.

**Dataset Suggestions**: 
- Use the "METR-LA" dataset, which contains traffic flow data from Los Angeles road networks, available on GitHub (https://github.com/liyaguang/DCRNN).

**Tasks**:
- **Data Ingestion**: Load and preprocess traffic flow data into a graph format, where nodes represent intersections and edges represent roads.
- **Graph Representation**: Create a temporal graph to capture traffic flow changes over time.
- **Modeling**: Implement a Spatio-Temporal Graph Convolutional Network (ST-GCN) for traffic flow prediction.
- **Evaluation**: Evaluate the model on unseen data using metrics like MAE and visualize the results on maps.

**Bonus Ideas**: 
- Incorporate external factors such as weather data or special events to improve predictions.
- Experiment with real-time prediction by integrating with a live traffic API (e.g., Google Maps Traffic API).

