---
title: "09.3: Python Dask"
---

<!-- git_hash=557fc735-4en timestamp=20260804_170444 -->

<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides001.png){width=80%}

</center>
<center>

# 2 / 16: Dataset Size Issues

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides002.png){width=80%}

</center>
- **Small datasets (< 1 GB)**
  - These datasets can easily fit into a computer's RAM, allowing for fast data processing without the need for disk paging. This means that operations can be performed quickly and efficiently using tools like Python and Pandas.

- **Medium datasets (< 1TB)**
  - Medium-sized datasets are too large to fit into RAM but can be stored on a
    local disk. However, accessing data from a disk is slower than from RAM,
    leading to a performance penalty.
  - To handle these datasets effectively, multiple CPU cores are needed.
    However, leveraging parallelism in Python, especially with Pandas, can be
    challenging due to its limitations in handling parallel processing.

- **Large datasets (> 1TB)**
  - These datasets exceed the capacity of both RAM and local disk storage,
    requiring multiple servers for processing.
  - Python and Pandas are not designed for distributed datasets, so alternative
    frameworks are necessary. Tools like Hadoop, Spark, Dask, and Ray are
    specifically built to manage and process massive datasets across distributed
    systems, enabling efficient data handling and analysis.

<center>

# 3 / 16: Dataset Size Issues

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides003.png){width=80%}

</center>
* **Dataset Size Issues**

- **Small datasets**: These are datasets that are less than 1 gigabyte in size.
  They are typically easy to handle with standard tools like Excel or simple
  scripts in Python or R.

- **Medium datasets**: These datasets are less than 1 terabyte. They require
  more robust tools and computing power, such as SQL databases or more advanced
  data processing libraries like Pandas.

- **Large datasets**: These datasets exceed 1 terabyte and often require
  distributed computing frameworks like Hadoop or Spark to process efficiently.

- **The thresholds are fuzzy and changing over time**
  - As technology advances, the definitions of what constitutes a small, medium,
    or large dataset can change. What was considered large a few years ago might
    now be seen as medium due to improvements in storage and processing
    capabilities.

  - _Scaling up_ computing resources by 10 times can allow you to handle
    datasets that are 10 times larger, but this isn't always straightforward or
    cost-effective.

- **Problem with scaling datasets**
  - **Long run times**: As datasets grow, the time required to process them
    increases, which can be a bottleneck in data analysis.

  - **Rewriting code for different dataset sizes**: Code that works for small
    datasets might not be efficient or even feasible for larger datasets,
    necessitating rewrites or optimizations.

  - **Plan what and how to do efficiently**: It's crucial to plan your data
    processing strategy to ensure efficiency, especially as datasets grow in
    size.

  - **Cumbersome framework**: Some frameworks are easier to use than others. For
    example, Pandas is user-friendly for small to medium datasets, while Hadoop
    can be more complex and challenging to work with for large datasets.

<center>

# 4 / 16: Dask

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides004.png){width=80%}

</center>
- **Dask is written in Python**
  - Dask is designed to scale popular Python libraries like Numpy, Pandas, and sklearn. This means you can work with larger datasets and more complex computations without changing your existing codebase significantly.
  - Dask objects act as wrappers around library objects such as Pandas DataFrames or numpy arrays. This allows you to use familiar tools while benefiting from Dask's parallel computing capabilities.
  - The parallel processing in Dask is achieved through "chunks" or "partitions." These are smaller pieces of your data that can be processed independently.
    - These chunks are queued for work, allowing efficient task scheduling.
    - They can be distributed across different machines, enabling scalable computations.
    - Local processing is also possible, making it versatile for different environments.

- **Pros**
  - Dask allows you to use interfaces you are already familiar with, reducing
    the learning curve.
  - You can write code that is optimized for parallel execution, and Dask takes
    care of the complex parts of parallel computing.

- **Scaling Dask is easy**
  - You can start by prototyping on your local machine and then scale up to a
    cluster when necessary, without needing to rewrite your code.
  - Dask abstracts away cluster-specific issues like resource management and
    data recovery, simplifying the scaling process.
  - It can run on multi-core systems and integrates with various cluster
    managers such as Yarn, Mesos, Kubernetes, and AWS ECS, providing flexibility
    in deployment.

<center>

# 5 / 16: Dask Layers

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides005.png){width=80%}

</center>
- **High-level APIs**
  - *Dask Array*: This is similar to NumPy but designed for parallel computing. It allows you to work with large arrays that don't fit into memory.
  - *Dask Bag*: Functions like parallel lists, useful for processing semi-structured data like JSON or log files.
  - *Dask DataFrame*: Mimics Pandas DataFrames but operates in parallel, enabling handling of larger-than-memory datasets.
  - *Dask ML*: Integrates with scikit-learn to provide parallel machine learning capabilities.

- **Low-level APIs**
  - _Dask Delayed_: Allows for lazy evaluation, meaning computations are only
    performed when needed. This is useful for building complex workflows.
  - _Dask Futures_: Provides eager execution, where tasks are executed
    immediately. This is beneficial for real-time data processing.

- **Dask Subsystem**
  - _Scheduler_: The core component that manages task execution. It creates and
    manages Directed Acyclic Graphs (DAGs) to organize tasks and efficiently
    distribute them across workers. This ensures optimal resource utilization
    and parallel processing.

This slide illustrates how Dask is structured to handle large-scale data
processing by providing both high-level abstractions for ease of use and
low-level controls for flexibility.

<center>

# 6 / 16: Scaling Up vs Scaling Out

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides006.png){width=80%}

</center>
- **Scaling Up**
  - This approach involves upgrading existing equipment to more powerful versions. For example, replacing a small pot with a larger one or using a food processor instead of a knife.
  - **Pros**
    - You get better hardware performance without needing to change your existing code.
  - **Cons**
    - Eventually, you might hit the limits of what a single machine can handle.
    - More powerful machines can be quite expensive, increasing costs significantly.

- **Scaling Out**
  - This method involves distributing tasks across multiple workers or machines,
    similar to hiring more cooks and using more pots in a kitchen.
  - **Pros**
    - A task scheduler can efficiently manage and assign tasks, making it a
      cost-effective solution.
    - You don’t need specialized hardware, which can save money.
  - **Cons**
    - You need to write code that can handle parallel processing, which can be
      complex.
    - Managing and maintaining a cluster of machines can incur additional costs.

<center>

# 7 / 16: Dask: Computation

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides007.png){width=80%}

</center>
* **Dask: Computation**

- **Lazy computations**
  - _Lazy computations_ mean that Dask doesn't immediately execute operations
    when you define them. Instead, it sets up a plan or a series of
    transformations that will be applied to the data later. This allows you to
    define what you want to do without actually doing it right away.
  - By defining the next steps without waiting for the current ones to finish,
    Dask can optimize the entire process, making it more efficient.
  - Dask processes data in chunks, which is crucial for handling large datasets
    that don't fit into memory all at once. For example, if you have a 2GB file,
    you can split it into smaller 64MB chunks. This way, you can process these
    chunks one at a time or in parallel, using less memory.
  - In the example, operating on 8 chunks per server means you only need 512MB
    of memory at a time, which is much more manageable.
  - Dask keeps track of the size and type of data objects, but it doesn't
    execute any code until you tell it to.

- **`compute()`**
  - The `compute()` function is used to actually run the computations you've
    defined. This is when Dask takes all the planned operations and executes
    them to produce a result.
  - For instance, if you have a variable `missing_count` that represents a
    series of operations to count missing values, calling
    `missing_count.compute()` will perform those operations and give you the
    final count.

- **`persist()`**
  - The `persist()` function helps manage memory by discarding unnecessary
    intermediate results. This is useful when you want to keep certain results
    in memory for further use without redoing all the previous computations.
  - It allows you to keep intermediate results in memory, which can be reused
    for additional computations, speeding up the process, especially for complex
    tasks that involve large Directed Acyclic Graphs (DAGs).

<center>

# 8 / 16: Dask: Data Structures

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides008.png){width=80%}

</center>
- **Dask DataFrame**
  - *Implements Pandas DataFrame*: Dask DataFrame is designed to work like a Pandas DataFrame but can handle larger-than-memory datasets by breaking them into smaller, manageable chunks.
  - *Tabular/relational data*: It is ideal for working with structured data, similar to what you would find in a database or spreadsheet, allowing for operations like filtering, grouping, and aggregating.

- **Dask Array**
  - _Implements numpy ndarray_: Dask Array mimics the functionality of NumPy
    arrays, enabling operations on large, multi-dimensional arrays that don't
    fit into memory.
  - _Multidimensional array_: This structure is useful for scientific computing
    and data analysis tasks that require handling large datasets with multiple
    dimensions.

- **Dask Bag**
  - _Coordinates Python lists of objects_: Dask Bag is designed for processing
    collections of Python objects, similar to a list, but optimized for parallel
    computation.
  - _Parallelize computations on unstructured/semi-structured data_: It is
    particularly useful for tasks involving text processing or JSON data, where
    the data structure is not strictly tabular.

<center>

# 9 / 16: Dask Reading Data

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides009.png){width=80%}

</center>
- **Consider:**
  - The code snippet demonstrates how to use Dask to read a CSV file. 
  - `dask.dataframe` is imported to handle large datasets efficiently.
  - `dd.read_csv('nyc-parking-tickets-2017.csv')` reads the CSV without loading the entire file into memory, which is useful for large datasets.
  - `df.isnull().sum()` calculates the number of missing values in each column.

- **`dask.dataframe.read_csv()`:**
  - _Doesn't load data in memory:_ Dask reads data in chunks, allowing for
    processing of large files that don't fit in memory.
  - _Infers column types:_ Dask samples the data to determine data types, which
    can be adjusted if needed.
  - _Use Parquet for data and types together:_ Parquet files store data and
    schema, making them efficient for storage and retrieval.

- **Partitions = independent data chunks:**
  - Data is divided into partitions, allowing parallel processing.
  - Example shows 33 partitions, resulting in 99 tasks in the computation graph.
  - Each partition is processed independently, reading and splitting data, and
    initializing a DataFrame object.

- **Graph Visualization:**
  - The diagram illustrates the task graph, showing the sequence of operations.
  - Tasks like `read-csv`, `isnull`, and aggregation are represented as nodes in
    the graph.
  - This structure allows Dask to optimize and parallelize operations
    efficiently.

<center>

# 10 / 16: Low Level APIs: Delayed

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides010.png){width=80%}

</center>
- **Low Level APIs: Delayed**
  - *Purpose*: These APIs are used to manage computations that don't naturally fit into Dask's built-in data structures like Dask DataFrame.
  - *Example*: The code snippet demonstrates how computations can be parallelized using basic Python functions.
  
- **Code Explanation**
  - **Functions**:
    - `inc(x)`: Increments the input `x` by 1.
    - `double(x)`: Multiplies the input `x` by 2.
    - `add(x, y)`: Adds two numbers `x` and `y`.
  - **Data**: A list `[1, 2, 3, 4, 5]` is processed.
  - **Computation**:
    - For each element `x` in `data`, `inc(x)` and `double(x)` are computed.
    - The results are added using `add(a, b)`.
    - The output is appended to a list, resulting in `[4, 7, 10, 13, 16]`.
  - **Result**: The sum of the output list is calculated, yielding `50`.

- **Parallelism Potential**
  - The diagram illustrates the dependency graph of the operations.
  - _Parallelism_: The `inc` and `double` functions can be executed
    independently for each element, showcasing potential for parallel execution.
- **Context**
  - This example highlights how Dask's low-level APIs can be used to optimize
    computations by exploiting parallelism, even when data doesn't fit into
    standard Dask structures.

<center>

# 11 / 16: Low Level APIs: Futures

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides011.png){width=80%}

</center>
- **In parallel programming, a "future" encapsulates asynchronous execution, representing the eventual result**
  - A *future* is a placeholder for a result that is initially unknown because the computation is still ongoing.
  - It allows programs to continue running other tasks while waiting for the result.

- **Python `concurrent.futures`**
  - Provides a high-level interface for executing tasks asynchronously.
  - Supports both thread-based and process-based parallelism through the
    `Executor` interface.
  - Useful for managing and coordinating multiple tasks that can run
    concurrently.

- **Dask extends `concurrent.futures`**
  - Dask builds on this concept by allowing everything to be expressed as
    futures.
  - Offers flexibility to specify whether tasks should block (wait for
    completion) or not, enhancing control over task execution.

The images illustrate how futures work in practice:

- The first image shows a timeline of I/O waiting and CPU processing,
  highlighting how tasks can overlap in execution.
- The code snippets demonstrate submitting tasks to a client, where tasks are
  represented as futures.
- The status of a future can be checked, and the result can be retrieved once
  the task is complete, as shown in the last image.

<center>

# 12 / 16: Different Types of Parallel Workload

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides012.png){width=80%}

</center>
* **Different Types of Parallel Workload**
  - **Break program in medium-size tasks of computation**
    - This involves dividing a program into smaller, manageable tasks that can be executed simultaneously. This approach helps in efficiently utilizing computational resources and reducing execution time.

- **MapReduce**
  - **Hadoop/Spark/Dask**
    - MapReduce is a programming model used for processing large data sets with
      a distributed algorithm. It involves two main steps: _Map_, which
      processes and filters data, and _Reduce_, which aggregates the results.
    - Tools like Hadoop, Spark, and Dask implement this model to handle big data
      efficiently.

- **Embarrassingly Parallel**
  - **Hadoop/Spark/Dask/Airflow/Prefect**
    - This type of workload involves tasks that can be executed independently
      without requiring communication between them. It is ideal for scenarios
      where tasks do not depend on each other.
    - Frameworks such as Airflow and Prefect, along with Hadoop, Spark, and
      Dask, support this model, making it easy to scale and manage.

- **Full Task Scheduling**
  - **Dask/Airflow/Prefect**
    - Full task scheduling involves managing complex workflows where tasks may
      have dependencies. This requires careful scheduling to ensure tasks are
      executed in the correct order.
    - Dask, Airflow, and Prefect are tools that provide robust scheduling
      capabilities, allowing for efficient execution of intricate workflows.

<center>

# 13 / 16: Encoding Task Graph

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides013.png){width=80%}

</center>
* **Encoding Task Graph**
  - **Dask encodes tasks in terms of Python dicts and functions**

- **Python Functions and Variables**:
  - The code snippet shows two simple functions, `inc` and `add`, which
    increment a number and add two numbers, respectively.
  - Variables `x`, `y`, and `z` are defined using these functions.

- **Task Graph Representation**:
  - Dask represents computations as task graphs using Python dictionaries.
  - Each key in the dictionary represents a task, and the value is a tuple
    containing the function and its arguments.
  - For example, `d = {'x': 1, 'y': (inc, 'x'), 'z': (add, 'y', 10)}` shows how
    tasks are encoded.

- **Visual Representation**:
  - The task graph is visually represented with nodes and edges, showing
    dependencies between tasks.
  - This helps in understanding the flow of computations and parallel execution.

- **Dask DataFrame Example**:
  - Dask can handle large datasets by breaking them into smaller chunks.
  - The code reads multiple CSV files, adds 100 to each element, and filters
    rows where the name is 'Alice'.

- **Task Graph for DataFrame Operations**:
  - The task graph for these operations is shown as a dictionary.
  - Each operation (`read-csv`, `add`, `filter`) is broken down into tasks for
    each file chunk.
  - This allows Dask to execute operations in parallel, improving efficiency.

- **Parallel Processing**:
  - By encoding tasks this way, Dask can optimize and parallelize computations,
    making it suitable for big data processing.

<center>

# 14 / 16: Task Scheduling

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides014.png){width=80%}

</center>
- **Task Scheduling**
  - In data processing, collections like *Bags*, *Arrays*, and *DataFrames* are used to create task graphs. These graphs represent the workflow of operations.
  - **Nodes** in the graph are Python functions that perform specific tasks.
  - **Edges** represent dependencies, meaning the output of one task is used as the input for another.

- **Schedule task graphs for execution**
  - **Single-machine scheduler**
    - Utilizes local resources such as process or thread pools.
    - Designed to run on a single machine, making it suitable for smaller tasks
      or development purposes.
  - **Distributed scheduler**
    - Can operate locally or across a cluster of machines.
    - Ideal for handling larger datasets and more complex computations by
      distributing tasks across multiple machines.

- The diagram illustrates the flow from collections to task graphs and finally
  to schedulers, highlighting the transition from data structures to execution
  strategies.

<center>

# 15 / 16: Task Scheduling

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides015.png){width=80%}

</center>
- **Task Scheduling**
  - *Dask task scheduler orchestrates work dynamically*
    - Unlike static scheduling found in relational databases, Dask uses a dynamic approach. This means it can adjust the scheduling of tasks on-the-fly based on current conditions.
    - During computation, Dask evaluates:
      - **Completed tasks**: Keeps track of what has been finished to avoid redundant work.
      - **Remaining tasks**: Identifies what still needs to be done.
      - **Free resources (CPUs)**: Allocates tasks to available processors to optimize performance.
      - **Data location**: Considers where data is stored to minimize data transfer times.

- **Dynamic approach handles various issues**
  - **Worker failure**
    - If a worker fails, Dask can re-run tasks on other available workers,
      ensuring reliability.
  - **Workers completing at different speeds**
    - Variability in task completion can occur due to:
      - Different computational requirements for tasks.
      - Hardware differences among workers.
      - Varying workloads on servers.
      - Slower access to data.
  - **Network unreliability**
    - Dask can re-run tasks or remove nodes that become isolated due to network
      issues, maintaining the integrity of the computation process.

<center>

# 16 / 16: Dask vs Spark

</center>
<center>

![](data605/lectures_commentary/Lesson09.3-Dask.png/slides016.png){width=80%}

</center>
* **Dask vs Spark**
- **Pros**
  - **Popular framework for large datasets**: Both Dask and Spark are widely used for handling large datasets. They are designed to process data that doesn't fit into the memory of a single machine, making them suitable for big data applications.
  - **In-memory alternative to MapReduce/Hadoop**: Unlike traditional MapReduce or Hadoop, which rely heavily on disk storage, both Dask and Spark perform computations in memory. This can lead to faster processing times as data doesn't need to be read from or written to disk as frequently.

- **Cons**
  - **Java library, supports Python via PySpark API**: Spark is primarily a
    Java-based library. While it supports Python through the PySpark API, this
    means that Python code is executed on the Java Virtual Machine (JVM).
    - **Python code runs on JVM**: This can introduce some overhead and
      complexity, as Python code is not running natively.
    - **Debugging is difficult as execution is outside Python**: Debugging can
      be challenging because the execution context is outside of the native
      Python environment, making it harder to trace errors.
  - **Different DataFrame API than Pandas**: Spark's DataFrame API is different
    from Pandas, which is a popular data manipulation library in Python.
    - **Learn "the Spark way"**: Users need to learn Spark's specific way of
      handling data, which can be a learning curve for those familiar with
      Pandas.
    - **May need to implement twice for exploratory analysis and production**:
      Often, data scientists use Pandas for exploratory data analysis and then
      need to rewrite the code in Spark for production, which can be
      time-consuming.
  - **Optimized for MapReduce operations**: Spark is particularly optimized for
    MapReduce-style operations, which might not be ideal for all types of data
    processing tasks.
  - **Difficult to set up and configure**: Setting up and configuring Spark can
    be complex, especially for those who are new to distributed computing
    frameworks. This can be a barrier to entry for smaller teams or individuals.
