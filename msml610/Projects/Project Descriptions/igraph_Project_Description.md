**Description**

In this project, students will utilize igraph, a Python library for creating and analyzing graphs and networks, to explore complex relationships within various datasets. The tool provides a comprehensive set of functions for graph manipulation, visualization, and analysis, enabling students to uncover insights from relational data.

Technologies Used
igraph

- Provides efficient data structures for handling large graphs.
- Supports a wide range of algorithms for community detection, shortest paths, and centrality measures.
- Offers visualization capabilities for interactive graph representation.
- Facilitates network analysis with built-in functions for clustering and connectivity.

---

### Project 1: Social Network Analysis of Movie Ratings (Difficulty: 1)

**Project Objective**  
Investigate the relationships between users and movies based on ratings to identify influential users and popular movies within a social network.

**Dataset Suggestions**  
- Use the MovieLens 100K dataset available on Kaggle ([MovieLens 100K](https://grouplens.org/datasets/movielens/100k/)).

**Tasks**  
- **Data Preprocessing**: Load the MovieLens dataset and create a user-item rating matrix.
- **Graph Construction**: Construct a bipartite graph where users and movies are nodes, and edges represent ratings.
- **Network Analysis**: Calculate centrality measures to identify influential users and popular movies.
- **Community Detection**: Apply clustering algorithms to find groups of similar users based on their movie preferences.
- **Visualization**: Create visual representations of the user-movie network to highlight key insights.

---

### Project 2: Analyzing COVID-19 Transmission Networks (Difficulty: 2)

**Project Objective**  
Model and analyze the transmission networks of COVID-19 cases to identify super-spreader events and community clusters.

**Dataset Suggestions**  
- Utilize the COVID-19 case data from the COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University ([CSSE COVID-19 Data](https://github.com/CSSEGISandData/COVID-19)).

**Tasks**  
- **Data Ingestion**: Load the COVID-19 case data and preprocess it to extract relevant transmission information (e.g., case connections).
- **Graph Construction**: Create a directed graph where nodes represent individuals and edges represent confirmed transmission paths.
- **Network Metrics**: Calculate metrics such as degree distribution and average path length to understand network properties.
- **Community Detection**: Use algorithms to identify clusters of cases that may indicate local outbreaks or super-spreader events.
- **Visualization**: Visualize the transmission network to illustrate connections and clusters using igraph’s plotting capabilities.

---

### Project 3: Analyzing Co-authorship Networks in Scientific Publications (Difficulty: 3)

**Project Objective**  
Explore co-authorship networks in scientific publications to identify key researchers and collaboration patterns in a specific field.

**Dataset Suggestions**  
- Use the arXiv dataset available on Kaggle ([arXiv Dataset](https://www.kaggle.com/datasets/CornellUniv/arxiv)).

**Tasks**  
- **Data Preprocessing**: Extract relevant information from the arXiv dataset, focusing on authors and their publications.
- **Graph Construction**: Build an undirected graph where nodes represent authors and edges represent co-authored papers.
- **Network Analysis**: Analyze the graph to calculate metrics such as betweenness centrality and clustering coefficients to identify influential researchers and collaboration patterns.
- **Community Detection**: Apply community detection algorithms to uncover research groups and collaboration clusters within the network.
- **Temporal Analysis**: Investigate how the co-authorship network evolves over time by analyzing publication data in different time frames.
- **Visualization**: Create interactive visualizations of the co-authorship network to highlight key authors and their collaborations.

**Bonus Ideas (Optional)**  
- For Project 1, compare the MovieLens dataset with another social network dataset to identify differences in user behavior.
- For Project 2, explore the impact of public health interventions on the structure of the transmission network.
- For Project 3, analyze the impact of funding sources on collaboration patterns by incorporating funding data into the analysis.

