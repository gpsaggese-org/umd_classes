---
title: "12.1: Graph Data Management"
---

<!-- git_hash=4f246573-rqb timestamp=20260804_174719 -->

<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides001.png){width=80%}

</center>
<center>

# 2 / 15: Graphs: Background

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides002.png){width=80%}

</center>
- **Graphs: Background**
  - A *graph* is a mathematical structure used to model pairwise relations between objects.
    - **Entities** are represented as vertices (or nodes). These are the individual objects or points in the graph.
    - **Connections** are represented as edges (or links, arcs, relationships). These show how the entities are related or connected to each other.

- **Applications of graphs in many fields**
  - Graphs are versatile and used in various domains:
    - **Social networks**: Representing connections between people or
      organizations.
    - **Biological networks**: Modeling interactions between biological entities
      like proteins or genes.
    - **Information networks**: Structuring data such as the World Wide Web or
      citation networks.
    - **Infrastructure networks**: Mapping out systems like transportation or
      utility networks.

- **Images Explanation**
  - The first image shows an _undirected, unweighted graph_, where edges have no
    direction and all connections are equal.
  - The second image illustrates a _directed, edge-weighted graph_, where edges
    have a direction and weights indicate the strength or capacity of the
    connection.

<center>

# 3 / 15: Graph Data Structures: Motivation

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides003.png){width=80%}

</center>
- **Graph data**:
  - With the explosion of data in recent years, there's a growing need to manage and analyze this information effectively. Graph data structures are particularly useful because they can represent complex relationships and interactions within data.
  - There's an increasing interest in using graph data for querying and reasoning, which means extracting meaningful insights and making informed decisions based on the data's structure.

- **Sectors**:
  - Graph data structures are being utilized across various sectors due to their
    ability to model relationships and interactions.
  - _Healthcare_: Used for understanding complex biological networks, such as
    protein interactions.
  - _Finance_: Helps in analyzing trading networks and detecting fraudulent
    activities.
  - _Logistics_: Optimizes supply chain networks and improves efficiency.

- **Example applications**:
  - _Fraud detection_: Graphs can reveal unusual patterns and connections that
    might indicate fraudulent behavior.
  - _Recommendation systems_: By analyzing user interactions and preferences,
    graphs can suggest relevant products or content.
  - _Network analysis_: Used to study and optimize various types of networks,
    from social media to transportation systems.

The images illustrate different types of networks, showcasing the versatility of
graph data structures in representing complex systems.

<center>

# 4 / 15: Graph Data Structures: Motivation

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides004.png){width=80%}

</center>
- **Traditional tools**:
  - Relational and NoSQL databases often face challenges when dealing with graph data. These databases are not inherently designed to handle the complex relationships and connections that graph data structures represent.
  - Querying graph-structured data can be inefficient and cumbersome with these traditional systems, leading to performance issues and limitations in data analysis.

- **Dedicated solutions**:
  - _Storing_: Neo4j is a popular graph database specifically designed to store
    and manage graph data efficiently. It allows for easy representation and
    querying of complex relationships.
  - _Processing_: Tools like Google Pregel, Apache Giraph, and Spark GraphX are
    designed to process large-scale graph data. They enable efficient
    computation and analysis of graph structures, which is crucial for
    applications like social network analysis and recommendation systems.

- **Images**:
  - The first image illustrates a global virtual trade network, highlighting the
    interconnectedness of countries through trade relationships. This type of
    data is naturally suited for graph representation.
  - The second image depicts a federal funds network, showcasing complex
    financial interactions that can be effectively analyzed using graph data
    structures.

<center>

# 5 / 15: Knowledge Graphs

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides005.png){width=80%}

</center>
* **Knowledge Graphs**
  - *Representation of knowledge in the form of graphs*: Knowledge graphs are a way to organize information using nodes and edges, where nodes represent entities (like people, places, or things) and edges represent the relationships between them. This structure helps in capturing complex relationships and properties of entities, offering a more intuitive and interconnected view of data.
  - They provide a structured view of real-world information, making it easier to understand and analyze. For example, the Google Knowledge Graph helps improve search results by connecting related information. Other examples include DBpedia and Wikidata, which are large-scale knowledge bases.
  - Knowledge graphs can be built using models like RDF (Resource Description Framework) or Property Graphs, which define how data is stored and accessed.

- **Applications**
  - Knowledge graphs enable machines to understand complex domains by providing
    context and relationships between data points. This understanding is crucial
    for tasks like semantic search, where the goal is to find information based
    on meaning rather than just keywords.
  - They support recommendation systems by identifying related items or
    concepts, and they enhance analytics by uncovering hidden patterns and
    insights.
  - Industries use knowledge graphs for data integration, allowing different
    data sources to work together seamlessly, and for knowledge discovery, which
    involves finding new insights from existing data. They are also integral to
    AI applications that require a deep understanding of data.

- **Ontologies**
  - Ontologies provide a formal and structured representation of knowledge,
    defining the types of things and how they relate to each other. They act
    like a set of rules and meanings that help interpret data into a knowledge
    graph.
  - By defining these relationships and meanings, ontologies promote
    interoperability across different knowledge bases, ensuring that data from
    various sources can be combined and understood in a consistent manner. This
    is essential for creating comprehensive and accurate knowledge graphs.

<center>

# 6 / 15: Graph Data Models: RDF

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides006.png){width=80%}

</center>
- **Resource Description Framework (RDF)**
  - RDF is a framework used to represent information about resources in the web.
  - It uses a structure called *triples*, which consist of three parts: subject, predicate, and object.
  - These triples connect a "subject" to an "object" through a "predicate," forming a simple statement. For example, "TomCruise-acted-TopGun" indicates that Tom Cruise acted in the movie Top Gun.

- **Used to Represent Knowledge Bases**
  - RDF is commonly used to create knowledge bases that can be queried using a
    language called SPARQL. This allows users to retrieve and manipulate data
    stored in RDF format efficiently.

- **Pros**
  - **Standardization**
    - RDF is standardized by the World Wide Web Consortium (W3C), ensuring a
      consistent way to model data.
    - Both subjects and objects can be Uniform Resource Identifiers (URIs),
      which are essential for the semantic web.
  - **Interoperability**
    - RDF allows for the merging of different RDF data stores, facilitating data
      integration across various sources.
  - **Extensibility**
    - It is easy to add new nodes and relationships in RDF, making it flexible.
    - RDF supports ontologies, which help define the relationships between
      different data elements, enhancing data understanding and reuse.

<center>

# 7 / 15: Graph Data Models: Property Graph

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides007.png){width=80%}

</center>
- **Graph Data Models: Property Graph**
  - A property graph is a type of directed graph where both nodes and edges can have associated key-value pairs known as *properties*. This allows for rich data representation, similar in expressive power to RDFs (Resource Description Frameworks).

- **No Universal Standard**
  - Property graphs lack a universal standard, which means there is less
    emphasis on a fixed _schema_. This flexibility can be advantageous for
    certain applications but makes it harder to ensure interoperability between
    different systems or databases.

- **Examples of Query Languages**
  - _Cypher_ is a popular query language used with Neo4j, a leading graph
    database that leverages property graphs.
  - _Gremlin_ is another query language, used with Apache TinkerPop, which is a
    graph computing framework that supports property graphs.

- **Image Explanation**
  - The image illustrates a simple property graph. Nodes represent entities like
    people or movies, and edges represent relationships such as "acted-in" or
    "married." Each node and edge can have properties, such as names, dates, or
    years, providing detailed context for the relationships.

<center>

# 8 / 15: Graph Data Models: XML

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides008.png){width=80%}

</center>
- **Graph Data Models: XML**
  - XML is a *common data model* used for flexible data representation. It is particularly useful for scenarios where data does not fit neatly into tables, such as hierarchical or nested data structures.
  - XML structures data as a **directed labeled tree**, where each node represents a data element, and edges represent relationships between these elements. This makes it ideal for representing complex data relationships.
  - XML is *popular for non-tabular data exchange* because it allows for a clear and structured way to represent data that can be easily shared and understood across different systems and platforms.

- **Example XML Structure**
  - The provided XML snippet illustrates a simple structure for representing
    movies and their actors.
  - The root element `<movies>` contains multiple `<movie>` elements, each with
    its own `<title>` and `<actors>`.
  - Each `<actor>` element includes details like `<name>` and `<born>`,
    showcasing how XML can encapsulate detailed information in a hierarchical
    manner.
  - The accompanying diagram visually represents this XML structure as a tree,
    highlighting the parent-child relationships between elements.

<center>

# 9 / 15: Comparison

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides009.png){width=80%}

</center>
- **Core data model**: 
  - *RDF* uses a simple structure called triples, which consist of a subject, predicate, and object. This is like a basic sentence structure.
  - *Property Graph* uses nodes and edges, where nodes represent entities and edges represent relationships, both of which can have properties.
  - *XML* organizes data in a hierarchical tree, similar to a family tree, with elements nested within each other.

- **How facts are stored**:
  - In _RDF_, each fact is stored as a separate triple, making it easy to add or
    remove facts.
  - _Property Graph_ stores facts as properties on nodes or edges, allowing for
    rich, detailed descriptions.
  - _XML_ uses nested tags with attributes to store facts, which can be complex
    but is very structured.

- **Attributes**:
  - In _RDF_, attributes are also modeled as triples, maintaining a consistent
    structure.
  - _Property Graph_ uses key-value pairs for attributes, which is
    straightforward and flexible.
  - _XML_ can use either attributes or child elements to represent additional
    information.

- **Semantics**:
  - _RDF_ has formal semantics, meaning it follows strict rules and standards
    (like RDF, RDFS, OWL) for meaning.
  - _Property Graph_ and _XML_ do not have built-in semantics, meaning their
    meaning is not standardized.

- **Ontology support**:
  - _RDF_ supports ontologies natively and is standardized, which helps in
    defining complex relationships.
  - _Property Graph_ offers optional ontology support, depending on the
    implementation.
  - _XML_ does not support ontologies, only schemas.

- **Reasoning & inference**:
  - _RDF_ has built-in reasoning and inference capabilities, allowing it to
    derive new information from existing data.
  - _Property Graph_ and _XML_ usually do not support reasoning or inference.

- **Data integration**:
  - _RDF_ excels at integrating heterogeneous data, making it ideal for
    combining different data sources.
  - _Property Graph_ requires manual mapping for integration.
  - _XML_ finds it challenging to integrate data across different schemas.

- **Query language**:
  - _RDF_ uses SPARQL, a powerful language for querying triples.
  - _Property Graph_ uses languages like Cypher, Gremlin, or GQL for querying.
  - _XML_ uses XPath and XQuery for navigating and querying data.

- **Query style**:
  - _RDF_ uses pattern matching to find data.
  - _Property Graph_ uses traversals, moving through nodes and edges.
  - _XML_ uses tree navigation to access data.

- **Schema**:
  - _RDF_ has optional schema support.
  - _Property Graph_ uses labels and constraints for schema.
  - _XML_ uses XSD or DTD for defining schemas.

- **Standards**:
  - _RDF_ and _XML_ follow W3C standards, ensuring wide acceptance and
    compatibility.
  - _Property Graph_ standards are often vendor-specific, leading to variations.

- **Interoperability**:
  - _RDF_ offers very high interoperability, making it easy to work with other
    systems.
  - _Property Graph_ has limited interoperability due to vendor-specific
    implementations.
  - _XML_ has high interoperability for document exchange.

- **Traversal performance**:
  - _RDF_ has moderate performance for data traversal.
  - _Property Graph_ is very fast at traversing data.
  - _XML_ performs poorly in traversal due to its hierarchical nature.

- **Use cases**:
  - _RDF_ is used for linked data and knowledge bases.
  - _Property Graph_ is ideal for fraud detection and recommendation systems.
  - _XML_ is used for documents, configurations, and data exchange.

- **Examples**:
  - _RDF_ examples include Wikidata and DBpedia.
  - _Property Graph_ examples include Neo4j and Amazon Neptune.
  - _XML_ examples include SOAP, RSS, and Microsoft Office documents.

<center>

# 10 / 15: Storing Graph Data

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides010.png){width=80%}

</center>
- **Storing Graph Data**

- **File systems**
  - _Simple_: File systems are straightforward to use for storing data, as they
    allow you to save files directly on your computer or server.
  - _No transactions, ACID compliance_: They do not support transactions or ACID
    (Atomicity, Consistency, Isolation, Durability) properties, which are
    important for ensuring data integrity and reliability.
  - _Minimal functionality_: File systems provide basic storage capabilities,
    but you need to build additional tools for data analysis or querying.

- **Relational databases**
  - _Mature technology_: Relational databases have been around for decades and
    are well-established in the industry.
  - _SQL, transactions, ACID compliance, toolchains_: They support SQL for
    querying, transactions for data integrity, and ACID compliance, making them
    reliable for many applications.
  - _Minimal functionality for graph data_: While powerful, they are not
    specifically designed for graph data, which can limit their effectiveness
    for such tasks.

- **NoSQL key-value stores**
  - _Handle large datasets efficiently in a distributed fashion_: These
    databases are designed to manage large volumes of data across multiple
    servers, making them scalable.
  - _Minimal native functionality for graph data_: They are not inherently
    equipped to handle graph-specific operations, requiring additional work to
    manage graph data.

- **Graph databases**
  - _Efficiently support complex queries/tasks (e.g., graph traversals)_:
    Specifically designed for graph data, these databases excel at handling
    complex queries like traversals.
  - _Less mature than RDBMSs_: They are newer compared to relational databases
    and may not have the same level of maturity or widespread adoption.
  - _Often lack declarative language like SQL_: Many graph databases do not have
    a standard query language like SQL, which means you might need to write
    custom programs to interact with the data.

<center>

# 11 / 15: Graph Databases

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides011.png){width=80%}

</center>
- **Graph Databases**
  - Graph databases are a type of database specifically designed to handle data that is interconnected, much like a network or web. They are particularly useful for applications where relationships between data points are as important as the data itself.

- **Many specialized graph DB systems**
  - There are several specialized systems for managing graph databases.
    **Neo4j**, **Titan**, **OrientDB**, and **AllegroGraph** are examples of
    popular graph database systems. Each of these systems has its own strengths
    and is chosen based on specific needs and use cases.

- **Key distinctions from relational / NoSQL databases**
  - **Store graph structure with pointers**
    - Unlike traditional relational databases that use tables and rows, graph
      databases store data in nodes and edges, using pointers to directly
      connect related data. This structure helps in avoiding complex joins,
      which can be computationally expensive.
    - This design simplifies _graph traversals_, making it easier and faster to
      navigate through connected data.

  - **Manage and query graph-structured data**
    - Graph databases are optimized for managing and querying data that is
      inherently structured as a graph. This includes writing queries and
      performing graph algorithms like _reachability_ (finding if a path exists
      between nodes) and _shortest paths_ (finding the shortest route between
      nodes).

  - **Support graph query languages: SPARQL, Cypher, Gremlin**
    - These databases support specialized query languages designed for graph
      data. **SPARQL**, **Cypher**, and **Gremlin** are examples of such
      languages, each offering unique features for querying and manipulating
      graph data.

  - **Declarative interfaces**
    - Graph databases often provide declarative interfaces, allowing users to
      specify _what_ they want to achieve without detailing _how_ to accomplish
      it. This abstraction simplifies complex queries and operations.

  - **Provide programmatic API for arbitrary graph algorithms**
    - They offer programmatic APIs that allow developers to implement custom
      graph algorithms, providing flexibility to perform complex operations
      tailored to specific application needs. This is crucial for applications
      that require advanced data analysis and manipulation.

<center>

# 12 / 15: Query Languages for Graph Databases

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides012.png){width=80%}

</center>
- **Query Languages for Graph Databases**: This slide compares three popular query languages used in graph databases: Cypher, Gremlin, and SPARQL. Each language has unique features and is suited for different types of graph data and use cases.

- **Data Model**:
  - **Cypher** and **Gremlin** both use the _Property Graph_ model, which
    represents data as nodes and edges with properties.
  - **SPARQL** uses the _RDF Triple_ model, which represents data as
    subject-predicate-object triples, ideal for semantic data.

- **Query Style**:
  - **Cypher** and **SPARQL** are _declarative_, meaning you specify what you
    want, not how to get it.
  - **Gremlin** is _imperative_, meaning you describe the steps to retrieve the
    data.

- **Syntax Example**:
  - **Cypher** has an _SQL-like_ syntax, making it familiar to those with SQL
    experience.
  - **Gremlin** uses a _Functional API_, which can be more complex.
  - **SPARQL** uses _Triple patterns_, aligning with its RDF data model.

- **Best For**:
  - **Cypher** excels in _pattern matching_, useful for finding relationships in
    data.
  - **Gremlin** is suited for _complex traversals_, handling intricate graph
    paths.
  - **SPARQL** is ideal for _semantic data_, such as linked data and knowledge
    graphs.

- **Standardization**:
  - **Cypher** is _Neo4j-specific_ but has an open version called OpenCypher.
  - **Gremlin** is part of the _Apache TinkerPop_ framework, supporting multiple
    platforms.
  - **SPARQL** is a _W3C Standard_, ensuring broad compatibility and support.

- **Backend Support**:
  - **Cypher** is mainly supported by _Neo4j_.
  - **Gremlin** is supported by _multi-platforms_ through TinkerPop.
  - **SPARQL** is used in _RDF stores_, which are databases designed for RDF
    data.

- **Learning Curve**:
  - **Cypher** has a _low_ learning curve, making it accessible for beginners.
  - **Gremlin** has a _high_ learning curve due to its imperative nature.
  - **SPARQL** has a _medium_ learning curve, balancing complexity and ease of
    use.

- **Use Cases**:
  - **Cypher** is great for _social graphs_ and _fraud detection_.
  - **Gremlin** is used for _distributed graph processing_, handling large-scale
    data.
  - **SPARQL** is best for _linked data_ and _knowledge graphs_, leveraging its
    semantic capabilities.

<center>

# 13 / 15: Query Languages: Cypher

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides013.png){width=80%}

</center>
- **Query Languages: Cypher**
  - **Purpose-Built for Property Graphs**
    - Cypher is specifically designed to work with *property graphs*, which are a type of graph database. In these graphs, data is stored in nodes and relationships, each of which can have properties in the form of key-value pairs. This structure allows for a flexible and intuitive way to represent complex data relationships.
  
  - **Declarative Syntax**
    - Cypher uses a *declarative* approach, meaning you specify *what* data you want to retrieve rather than detailing *how* to get it. This makes it easier to write and understand queries, as you focus on the desired outcome rather than the process to achieve it.

- **Optimized for Pattern Matching**
  - Cypher excels at finding specific patterns within a graph, such as
    identifying subgraph structures like "friends of friends." However, it has
    limitations when it comes to more complex graph analytics tasks, such as
    calculating reachability, finding the shortest paths, or determining
    centrality measures. These tasks often require more specialized algorithms
    or tools.

- **Neo4j Native**
  - Cypher is the native query language for Neo4j, a popular graph database
    platform. This means it is fully integrated and optimized for use with
    Neo4j, providing efficient and powerful querying capabilities for users of
    this system.

- **Example:**
  - The example query demonstrates how to use Cypher to find the names of people
    who know someone named "Alice." The `MATCH` clause specifies the pattern to
    look for: a `person` node connected by a `KNOWS` relationship to a `friend`
    node with the property `name: "Alice"`. The `RETURN` clause then specifies
    that the query should output the `name` property of the `person` node. This
    example highlights Cypher's ability to express complex queries in a
    straightforward and readable manner.

<center>

# 14 / 15: Query Languages: Gremlin

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides014.png){width=80%}

</center>
- **Query Languages: Gremlin**
  - Gremlin is a query language designed for graph databases. It allows users to interact with and query graph data structures efficiently.

- **Supports Multiple Models**
  - _Compatible with both Property Graphs and RDF_: Gremlin is versatile because
    it can work with different types of graph models. Property Graphs are a
    common way to represent graph data with nodes and edges having properties.
    RDF (Resource Description Framework) is another model used mainly for
    semantic web applications. Gremlin's compatibility with both means it can be
    used in a wide range of applications and systems.

- **Imperative Style**
  - _Describes how to traverse the graph step by step_: Unlike declarative query
    languages like SQL, which focus on what data to retrieve, Gremlin is
    imperative. This means you specify the exact steps to navigate through the
    graph, giving you more control over the query process.

- **Traversal-Based Semantics**
  - _Expresses computation as a flow of operations across vertices and edges_:
    In Gremlin, queries are expressed as traversals. This means you define a
    sequence of operations that move through the graph's nodes (vertices) and
    connections (edges) to compute the desired result.

- **Example**
  - _Find the names of people who know someone named "Alice"_: This example
    demonstrates a typical Gremlin query. It starts by selecting vertices
    labeled 'Person', then filters those who have an outgoing 'KNOWS' edge to a
    person named "Alice". Finally, it retrieves the names of these people. This
    step-by-step traversal highlights Gremlin's imperative nature and its
    ability to express complex graph queries succinctly.

<center>

# 15 / 15: Query Languages: SPARQL

</center>
<center>

![](data605/lectures_commentary/Lesson12.1-Graph_Data_Management.png/slides015.png){width=80%}

</center>
- **Query Languages: SPARQL**
  - **SQL-Like Syntax**
    - SPARQL is designed to feel familiar to those who have used SQL. It uses similar keywords like `SELECT`, `WHERE`, and `FILTER`, which makes it easier for people with SQL experience to learn and use SPARQL. This similarity helps in writing queries to retrieve specific data from databases.
  - **Built for RDF Data**
    - SPARQL is specifically created to query RDF (Resource Description Framework) data. RDF data is structured in triples, which consist of a subject, predicate, and object. This structure is essential for representing information on the Semantic Web, where data is interconnected.
  - **W3C Standard**
    - SPARQL is a standard developed by the World Wide Web Consortium (W3C). It plays a crucial role in the Semantic Web and Linked Data applications, allowing for the integration and querying of data across different sources on the web.

- **Example**
  - _Find the names of people who know someone named "Alice"_
    - This example demonstrates a SPARQL query. It uses a `PREFIX` to define a
      namespace, which helps in shortening URIs. The `SELECT` statement
      specifies the variable `?personName` to retrieve. The `WHERE` clause
      contains the pattern to match: it looks for a `?person` who knows a
      `?friend` with the name "Alice" and retrieves the name of the `?person`.
      This query highlights how SPARQL can be used to navigate relationships in
      RDF data.
