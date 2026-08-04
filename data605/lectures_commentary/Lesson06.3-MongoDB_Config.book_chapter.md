---
title: "06.3: MongoDB Config"
---

<!-- git_hash=b1afff2a-53x timestamp=20260804_162659 -->

<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides001.png){width=80%}

</center>
<center>

# 2 / 12: MongoDB Processes and Configuration

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides002.png){width=80%}

</center>
- **`mongod`: Database Instance (Server Process)**
  - This is the core server process for MongoDB. It handles data storage, retrieval, and management. Think of it as the engine that powers the database.

- **`mongosh`: Interactive Shell (Client)**
  - This is a command-line interface for interacting with MongoDB. It provides a
    JavaScript environment, allowing users to execute queries and manage the
    database directly.

- **`mongos`: Database Router**
  - Acts as a traffic controller for database requests. It processes incoming
    queries and determines which `mongod` instances should handle them,
    especially in a sharded setup.
  - It collates results from different shards and sends the final result back to
    the client.

- **Configuration Recommendations**
  - You can have a single `mongos` for the entire system, which simplifies
    management.
  - Alternatively, having a local `mongos` per client can reduce network
    latency, improving performance.

The diagram illustrates how `mongos` interacts with different shards, directing
queries and collating results to provide seamless data access across a
distributed database system.

<center>

# 3 / 12: MapReduce Functionality

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides003.png){width=80%}

</center>
- **Perform map-reduce computation on (key, value) pairs**
  - MapReduce is a programming model used for processing large data sets with a distributed algorithm on a cluster.
  - It involves two main functions: *map* and *reduce*. The map function processes input data and produces key-value pairs, while the reduce function aggregates these pairs.

- **Provide map function, reduction function, and result set name**
  - The code snippet shows how to implement MapReduce in a database context
    using a function call.
  - **`<map_function>`**: Defines how to transform input data into key-value
    pairs.
  - **`<reduce_function>`**: Specifies how to combine values associated with the
    same key.
  - **`out: <collection>`**: Determines where the result will be stored.
  - Additional options like **`query`**, **`sort`**, and **`limit`** allow for
    more control over the data processing.

- **Illustrations**
  - The first image illustrates the flow of data through the MapReduce process:
    input is split, mapped, shuffled, and reduced to produce the output.
  - The second image shows a more abstract representation of the MapReduce
    architecture, highlighting the separation of the map, shuffle, and reduce
    phases.

<center>

# 4 / 12: Data Replication

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides004.png){width=80%}

</center>
- **Data Replication** ensures several critical aspects of data management:
  - **Redundancy**: This means having multiple copies of data to prevent data loss.
  - **Backup**: Replication acts as a backup, safeguarding data against failures.
  - **Automatic Failover**: If a primary server fails, the system automatically switches to a backup without manual intervention.

- **Replication** is managed through groups of servers called _replica sets_:
  - **Primary Set**: This is where data updates occur directly. It handles all
    write operations.
  - **Secondary Set**: These servers duplicate data from the primary set. They
    can have various properties:
    - _Secondary-only_: Only stores replicated data.
    - _Hidden_: Not visible to client applications.
    - _Delayed_: Updates occur after a set delay.
    - _Arbiters_: Participate in elections but do not store data.
    - _Non-voting_: Do not participate in elections.

- In case the **primary server fails**, the secondary sets engage in a voting
  process to elect a new primary server, ensuring continuous availability and
  reliability.

<center>

# 5 / 12: Sync vs Async Replication

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides005.png){width=80%}

</center>
- **Synchronous Replication**: This method ensures that updates are propagated to all replicas within a single transaction. This means that the client must wait for confirmation from all replicas before the transaction is considered complete. This approach is reliable but can be complex and costly to implement.

- **Implementations**:
  - _2-Phase Commit (2PC)_: A protocol that ensures all nodes in a distributed
    system agree on a transaction before it is committed.
  - _Paxos_: A consensus algorithm that helps achieve agreement among
    distributed systems.
  - These methods are often complex and require significant resources.

- **Asynchronous Replication**: In this approach, the primary node sends updates
  to replicas, but the transaction is considered complete before the replicas
  are updated. This allows for faster transaction commits but may lead to
  temporary inconsistencies if failures occur.
  - The primary advantage is quick commits, which can improve performance.
  - However, this comes at the cost of consistency, as replicas may not always
    have the latest data immediately.

The diagrams illustrate the differences in communication flow between
synchronous and asynchronous replication, highlighting the waiting period in
synchronous replication and the immediate transaction completion in asynchronous
replication.

<center>

# 6 / 12: Data Consistency

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides006.png){width=80%}

</center>
* **Data Consistency**
  - *Data consistency* is about ensuring that data remains accurate and reliable across different parts of a system. It's crucial for maintaining trust in the data being used.

- **@Client decides how to enforce consistency for reads@**
  - The _client_ refers to the application or user accessing the database. They
    have the flexibility to choose how strictly they want the data to be
    consistent when they read it.
  - This choice impacts how up-to-date the data is when it's retrieved.

- **Reads to a primary have @strict consistency@**
  - **Reflect latest data changes**
    - When you read from the _primary_ database, you get the most recent data.
      This means any changes made are immediately visible.
  - **All writes and consistent reads go to primary**
    - All data updates (writes) and reads that require the most current data are
      directed to the primary. This ensures that the data is always up-to-date.

- **Reads to a secondary have @eventual consistency@**
  - **Updates propagate gradually**
    - Changes made to the data take some time to reach the _secondary_
      databases. This means there might be a delay before the secondary reflects
      the latest updates.
  - **May read previous database state**
    - When reading from a secondary, you might get an older version of the data
      because updates haven't reached it yet.
  - **Eventually consistent reads distributed among secondaries**
    - Over time, all secondary databases will catch up with the primary,
      achieving consistency. Reads are spread across these secondaries to
      balance the load and improve performance.

<center>

# 7 / 12: MongoDB: Sharding

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides007.png){width=80%}

</center>
- **Shard**: A shard is essentially a subset of data. In MongoDB, data is split based on a *shard key*, which is a specific field or set of fields. This allows the data to be distributed across different shards based on specific intervals or ranges, such as [a, b).

- **Sharding**: This is the method used to distribute data across multiple
  machines. It helps in managing large datasets by breaking them into smaller,
  more manageable pieces, which can be stored on different servers.

- **Horizontal scaling**: Sharding enables horizontal scaling, which means
  adding more servers to handle increased load. This divides both data and
  workload across multiple servers, though it introduces complexity in terms of
  infrastructure and maintenance.

- **`mongos`**: This component acts as a query router. It interfaces between
  clients and the sharded cluster, directing queries to the appropriate shards.
  Each shard is deployed as a replica set, ensuring data redundancy and
  availability. Config servers are crucial as they store metadata and
  configuration settings for the cluster, ensuring everything runs smoothly.

<center>

# 8 / 12: RDBMS Internals

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides008.png){width=80%}

</center>
* **RDBMS Internals**

- _Storage hierarchy_
  - **Map tables to files**: In a relational database management system (RDBMS),
    tables are stored as files on disk. This means that each table, which is a
    collection of rows and columns, is represented by a file or a set of files.
    This mapping is crucial because it determines how data is physically stored
    and accessed.
  - **Map tuples to disk blocks**: A tuple is essentially a row in a table.
    These tuples are stored in disk blocks, which are fixed-size units of
    storage. Mapping tuples to disk blocks efficiently is important for quick
    data retrieval and storage.

- _Buffer Manager_
  - **Bring pages from disk to memory**: The buffer manager is responsible for
    loading data from disk into the main memory. This is necessary because
    accessing data in memory is much faster than accessing it on disk.
  - **Manage limited memory**: Memory is a limited resource, so the buffer
    manager must decide which data to keep in memory and which to evict. This
    involves strategies to optimize the use of available memory while minimizing
    the need to access slower disk storage.

- _Query Processing Engine_
  - **Execute user query**: This component takes the SQL queries provided by
    users and executes them. It translates the high-level query into a series of
    operations that the database can perform.
  - **Specify sequence of pages for memory**: The engine determines the order in
    which data pages are accessed and processed in memory. This sequence is
    crucial for efficient query execution.
  - **Operate on tuples to produce results**: The engine processes the data
    (tuples) according to the query's requirements, such as filtering, joining,
    or aggregating, to produce the desired results for the user.

<center>

# 9 / 12: Query Optimizer

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides009.png){width=80%}

</center>
- **Query Optimizer in RDBMS**:
  - In a relational database management system (RDBMS), the *query optimizer* is a crucial component that operates in a static manner.
  - It assigns a *cost* to each potential query plan. This cost estimation helps in determining the efficiency of executing a query.
  - The optimizer estimates various parameters, such as the *time required to access data*. These estimates are based on statistics and data distribution.
  - The primary goal is to *search for the best query plan* that minimizes resource usage and execution time.
  - This process is a standard feature in traditional RDBMS systems, ensuring efficient data retrieval.

- **Diagram Explanation**:
  - The diagram illustrates the components involved in query optimization.
  - A _Query Transformer_ modifies the parsed query to improve efficiency.
  - The _Estimator_ uses statistics from the _Data Dictionary_ to predict the
    cost of different query plans.
  - The _Plan Generator_ creates the optimal query plan based on these
    estimates.

- **Books on Query Optimization**:
  - These books provide insights and strategies for optimizing queries in
    different database systems like PostgreSQL, MySQL, and SQL Server.
  - They are valuable resources for understanding advanced techniques and best
    practices in query optimization and performance tuning.

<center>

# 10 / 12: Query Optimizer

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides010.png){width=80%}

</center>
- **MongoDB's Query Optimizer**: MongoDB uses a dynamic query optimizer to improve query performance.
  - **Dynamic Plan Testing**: It tries different query plans to determine which performs best. This is crucial because the query plan space is relatively small, as MongoDB does not use joins.
  - **Parallel Execution**: Multiple query plans can be executed in parallel. Once one plan finishes, the others are terminated, ensuring efficiency.
  - **Caching**: Results from successful query plans are cached. This means if the same query is run again, MongoDB can quickly retrieve the results without recalculating.
  - **Adapting to Changes**: If a query plan starts performing poorly, perhaps due to changes in data or query parameters, MongoDB will try different plans to find a better one.

- **Flowchart Explanation**:
  - **Cache Matching**: The process begins by checking if there is a matching
    cache entry for the query.
  - **Plan Evaluation**: If a match is found, the plan's performance is
    evaluated. If it fails, the cache entry is evicted.
  - **Candidate Plans**: If no match is found, new candidate plans are generated
    and evaluated.
  - **Choosing a Plan**: The best-performing plan is chosen and a new cache
    entry is created.
  - **Result Generation**: Finally, the chosen plan is used to generate the
    result documents.

<center>

# 11 / 12: MongoDB: Strengths

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides011.png){width=80%}

</center>
* **MongoDB: Strengths**

- **Provide flexible, modern query language**
  - MongoDB uses a query language that is designed to be flexible and easy to
    use. This means you can perform complex queries on your data without needing
    to write complicated code. It's similar to SQL but tailored for the
    document-oriented nature of MongoDB.

- **High-performance**
  - **Implemented in C++**
    - MongoDB is built using C++, a programming language known for its speed and
      efficiency. This contributes to MongoDB's ability to handle large volumes
      of data quickly and efficiently.

- **Rapid development, open source**
  - **Supports many platforms**
    - Being open source means MongoDB is free to use and can be modified by
      anyone. It also runs on various operating systems, making it versatile for
      different development environments.
  - **Multiple language drivers**
    - MongoDB provides drivers for many programming languages, allowing
      developers to integrate it easily into their applications, regardless of
      the language they are using.

- **Built for distributed database systems**
  - **Sharding**
    - Sharding is a method for distributing data across multiple servers.
      MongoDB uses sharding to ensure that large datasets can be spread out,
      improving performance and scalability.
  - **Replica sets**
    - Replica sets are a way to ensure data redundancy and high availability.
      MongoDB can automatically replicate data across different servers, so if
      one server fails, another can take over.

- **Tunable consistency**
  - MongoDB allows you to adjust the level of consistency according to your
    needs. This means you can choose between strong consistency, where data is
    always up-to-date, or eventual consistency, which can improve performance.

- **Ideal for large data not needing relational model**
  - **Element relationships irrelevant**
    - MongoDB is perfect for situations where the relationships between data
      elements are not important. This is because it doesn't use a traditional
      relational database model.
  - **Focus on storing and retrieving large data quantities**
    - The primary goal of MongoDB is to efficiently store and retrieve large
      amounts of data, making it a great choice for applications that handle big
      data.

<center>

# 12 / 12: MongoDB: Limitations

</center>
<center>

![](data605/lectures_commentary/Lesson06.3-MongoDB_Config.png/slides012.png){width=80%}

</center>
- **No referential integrity**
  - *Referential integrity* refers to the enforcement of foreign key constraints, which ensure that relationships between tables remain consistent. MongoDB does not support this, meaning it doesn't automatically enforce relationships between collections. This can lead to potential data inconsistencies if not managed carefully by the application.

- **Lack of transactions and joins**
  - Traditional databases allow for transactions and joins, which help maintain
    data integrity and simplify complex queries. MongoDB, being a NoSQL
    database, traditionally lacked these features, although recent versions have
    introduced multi-document transactions. However, the absence of joins means
    that data often needs to be denormalized.

- **High degree of denormalization**
  - Denormalization involves storing data in multiple places to improve read
    performance. In MongoDB, this means that updates might need to be applied in
    several locations, increasing the risk of data inconsistency and
    complicating data management.

- **Lack of predefined schema is a double-edged sword**
  - MongoDB's flexibility allows for dynamic schemas, meaning documents in a
    collection can have different fields. While this provides flexibility, it
    can lead to inconsistencies and requires the application to enforce a data
    model.

- **CAP Theorem: targets consistency and partition tolerance, gives up on
  availability**
  - According to the CAP Theorem, a distributed database can only guarantee two
    out of three: Consistency, Availability, and Partition Tolerance. MongoDB
    prioritizes consistency and partition tolerance, which means it may
    sacrifice availability during network partitions. This trade-off is
    important to consider based on application needs.
