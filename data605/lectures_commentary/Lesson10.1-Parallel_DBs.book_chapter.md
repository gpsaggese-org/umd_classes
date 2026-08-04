---
title: "10.1: Parallel and Distributed Systems / DBs"
---

<!-- git_hash=557fc735-5ox timestamp=20260804_170612 -->

<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides001.png){width=80%}

</center>
<center>

# 2 / 16: Client-Server Architecture

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides002.png){width=80%}

</center>
**Client-Server Architecture**

- **Client-server model**: This is a framework for distributed applications
  where tasks are divided between two main components:
  - **Clients**: These are the entities that request services. Examples include
    dashboards, graphical user interfaces (GUIs), and client applications.
    Clients are typically the front-end users interact with.
  - **Servers**: These provide the necessary resources or services, such as
    databases. Servers handle the back-end processes and respond to client
    requests.

- **Architecture of a database system**:
  - **Back-end (Server)**: This part manages several critical functions:
    - Access management: Ensures only authorized users can access data.
    - Query evaluation and optimization: Processes and improves the efficiency
      of database queries.
    - Concurrency control: Manages simultaneous operations without conflicts.
    - Recovery: Ensures data integrity and restoration after failures.
  - **Front-end (Clients)**: Includes tools that users interact with, such as
    forms, report-writers, and GUIs.
- **Interface between front-end and back-end**:
  - **SQL**: A standard language for managing and manipulating databases.
  - **Application Programming Interface (API)**: Allows different software
    applications to communicate with each other, facilitating interaction
    between the client and server.

<center>

# 3 / 16: Parallel vs Distributed Computing

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides003.png){width=80%}

</center>
- **Parallel Computing**
  - *One computer, multiple CPUs*: This setup involves a single machine with several processors working together. Each CPU can handle different parts of a task simultaneously, increasing efficiency.
  - *Cluster: many computers, each with multiple CPUs*: A cluster consists of multiple computers, each equipped with several CPUs. These computers are connected and work together as a single system.
  - *Homogeneous, geographically close nodes*: The nodes in parallel computing are similar in terms of hardware and are located close to each other, often in the same physical location.
  - *Work on one task simultaneously*: All processors focus on a single task, dividing the workload to complete it faster.

- **Distributed Computing**
  - _Autonomous, geographically separate systems_: Distributed computing
    involves independent systems that are spread out over different locations.
    Each system operates on its own but contributes to a larger task.
  - _Heterogeneous and distant nodes_: The nodes can vary in hardware and
    software configurations and are often located far apart, sometimes across
    different countries.
  - _Perform separate tasks or parts of a larger task_: Each node in a
    distributed system may handle different tasks or parts of a larger task,
    working independently but contributing to a common goal.

<center>

# 4 / 16: Parallel Systems

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides004.png){width=80%}

</center>
- **Parallel systems** are computing architectures designed to perform multiple calculations simultaneously. They consist of:
  - **Multiple processors**: These are the brains of the system, allowing for simultaneous data processing.
  - **Multiple memories**: Each processor may have its own memory, or they may share memory, enabling efficient data access.
  - **Multiple disks**: These provide storage for data and programs, allowing for quick access and retrieval.
  - **Fast interconnection network**: This network connects the processors, memories, and disks, ensuring rapid communication and data transfer.

- **Coarse-grain parallel machine**:
  - Involves a **small number of powerful processors**.
  - Example: A typical laptop with multiple CPUs, where each CPU is capable of
    handling substantial tasks independently.

- **Fine-grain parallel machine**:
  - Also known as **massively parallel** systems.
  - Comprises **thousands of smaller processors**, offering a higher degree of
    parallelism.
  - Can operate **with or without shared memory**, depending on the
    architecture.
  - Examples include **GPUs** and historical systems like **The Connection
    Machine** from the 1980s, which was a pioneering effort in parallel
    computing.

<center>

# 5 / 16: Parallel Databases: Introduction

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides005.png){width=80%}

</center>
* **Parallel Databases: Introduction**

- **Parallel DBs were the standard approach before MapReduce**
  - Before the advent of MapReduce, parallel databases were the go-to solution
    for handling large-scale data processing tasks. They allowed for the
    distribution of data and queries across multiple machines, which helped in
    managing and processing large datasets efficiently.

- **Parallel machines have become common and affordable**
  - The cost of technology components like microprocessors, memory, and disks
    has decreased significantly over time. This price drop has made it feasible
    for even personal computers, like desktops and laptops, to have multiple
    processors. This trend is expected to continue, making parallel computing
    more accessible to a wider audience.

- **DBs are growing increasingly large**
  - The amount of data being collected and stored is growing rapidly. This
    includes not only traditional transaction data but also multimedia objects
    like images and videos. As a result, databases are becoming larger and more
    complex, necessitating more robust solutions for storage and analysis.

- **Large-scale parallel DBs increasingly used for:**
  - _Storing large volumes of data_: They are essential for managing the vast
    amounts of data generated daily.
  - _Processing time-consuming queries_: Parallel databases can handle complex
    queries more efficiently by distributing the workload across multiple
    processors.
  - _Providing high throughput for transaction processing_: They ensure that a
    large number of transactions can be processed quickly and efficiently, which
    is crucial for businesses that rely on real-time data processing.

<center>

# 6 / 16: Parallel Databases

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides006.png){width=80%}

</center>
- **Parallel Databases**
  - The rise of the *Internet* and *Big Data* has led to a demand for databases that are both large and fast. This is because modern applications, like e-commerce websites, need to store vast amounts of data, often measured in petabytes, and handle a high volume of transactions, sometimes thousands per second. This requires databases that can efficiently manage and process such large-scale operations.

- **Databases can be parallelized**
  - The nature of database queries, which are often set-oriented, makes them
    well-suited for parallel processing. This means that many database
    operations can be divided into smaller tasks that can be executed
    simultaneously. Some operations, like certain types of joins, are considered
    _embarrassingly parallel_, meaning they can be easily split into independent
    tasks. For example, a join operation between two tables `R` and `S` on a
    common attribute can be efficiently executed using a framework like
    MapReduce.

- **Parallel DBs**
  - The goal of parallel databases is to either increase the number of
    transactions processed per second or reduce the time it takes to execute a
    query. This involves balancing _throughput_ (the number of transactions
    processed in a given time) and _response time_ (how quickly a single query
    is completed). Additionally, there's a focus on achieving _speed-up_ (how
    much faster a task can be completed with more resources) and _scale-up_ (how
    well a system can handle a larger workload with more resources).

- **Perfect speedup doesn't happen due to:**
  - In practice, achieving perfect speedup is challenging because of several
    factors. _Start-up costs_ refer to the time and resources needed to initiate
    parallel tasks. _Task interference_ occurs when tasks compete for shared
    resources, leading to delays. _Skew_ happens when tasks are unevenly
    distributed, causing some processors to finish earlier than others, which
    can lead to inefficiencies. These factors prevent parallel databases from
    achieving ideal performance improvements.

<center>

# 7 / 16: How to Measure Parallel Performance

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides007.png){width=80%}

</center>
- **Throughput**
  - *Definition*: Throughput refers to the number of tasks completed in a given time frame. It is a measure of how much work is done.
  - *Improvement*: By processing tasks in parallel, throughput can be increased. This means more tasks are completed simultaneously, boosting overall productivity.

- **Latency**
  - _Definition_: Latency is the time taken to complete a single task from the
    moment it is submitted. It measures the delay before the task is finished.
  - _Reduction_: Performing subtasks in parallel can decrease latency, allowing
    tasks to be completed faster.

- **Throughput and Latency Relationship**
  - _Connection_: While related, throughput and latency are not the same.
    Improving one can affect the other.
  - _Strategies_:
    - Reducing latency can lead to increased throughput.
    - Pipelining, or overlapping task execution, is a method to enhance
      throughput. For example, in car manufacturing, although building a car
      takes weeks, the assembly line allows one car to be completed every hour.
      Similarly, pipelining in microprocessors allows multiple instructions to
      be processed simultaneously, improving efficiency.

<center>

# 8 / 16: Speed-Up and Scale-Up: Intuition

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides008.png){width=80%}

</center>
- **Speed-Up and Scale-Up: Intuition**
  - *You have a workload to execute*
    - **Change workload $M$**
      - This refers to the tasks or operations you need to perform, such as the number of database (DB) transactions or the amount of data you need to query. Essentially, it's about the size or complexity of the job you need to get done.
  
  - *You need to execute the workload on a machine*
    - **Change computing power $N$**
      - This involves enhancing the machine's ability to handle tasks. You can do
        this by upgrading to a better CPU, which is known as scaling vertically
        or scaling up. Alternatively, you can add more CPUs, which is called
        scaling horizontally or scaling out. Both methods aim to improve the
        machine's performance to handle the workload more efficiently.

- **Two ways to measure efficiency** when increasing workload and computing
  power
  - **_Speed-up_**
    - This approach focuses on keeping the workload size constant (problem size
      $M$) while increasing the machine's computing power ($N$). The goal is to
      see how much faster the workload can be completed with more powerful
      resources.
  - **_Scale-up_**
    - Here, both the workload size ($M$) and the machine's computing power ($N$)
      are increased. The aim is to understand how well the system can handle
      larger tasks as both the problem and the resources grow. This is crucial
      for systems that need to manage increasing amounts of data or transactions
      over time.

<center>

# 9 / 16: Speed-Up vs Scale-Up

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides009.png){width=80%}

</center>
- **Speed-Up vs Scale-Up**
  - These concepts relate to how we can improve computing performance by adjusting resources or workload.

- **Speed-Up**
  - _Definition_: Speed-up involves solving a fixed-sized problem on a larger
    system.
  - _Formula_:
    $\text{speed-up} = \frac{\text{small system elapsed time}}{\text{large system elapsed time}}$
  - _Linear Speed-Up_: Achieved when the speed-up equals the increase in
    resources ($N$). This means doubling resources halves the time.
  - _Graph Explanation_: The graph shows linear speed-up as a straight line,
    indicating proportional improvement with added resources. Sublinear speed-up
    curves below, showing diminishing returns.

- **Scale-Up**
  - _Definition_: Scale-up involves increasing both the problem size and the
    system size.
  - _Formula_:
    $\text{scale-up} = \frac{\text{small system-problem time}}{\text{big system-problem time}}$
  - _Linear Scale-Up_: Achieved when the scale-up ratio equals 1, meaning the
    system handles larger problems efficiently.
  - _Graph Explanation_: The graph shows linear scale-up as a flat line,
    indicating consistent performance with increased problem size. Sublinear
    scale-up curves downward, indicating less efficiency as problems grow.

These concepts are crucial in understanding how to optimize computing systems
for better performance and efficiency.

<center>

# 10 / 16: Factors Limiting Speed-up and Scale-up

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides010.png){width=80%}

</center>
- **Factors Limiting Speed-up and Scale-up**
  - *Speed-up* and *scale-up* are often less than expected because not all tasks
    can be done in parallel. This means that even if you add more resources, the
    improvement in performance might not be as large as anticipated.

- **Amdahl's Law**
  - This law helps us understand the limits of parallel computing. It shows how
    the fraction of a task that can be parallelized affects overall speed-up.
  - **Variables:**
    - **$p$**: The portion of the task that can be parallelized.
    - **$s$**: The number of nodes or processors used.
    - **$T$**: The time it takes to complete the task serially (without
      parallelization).
    - **$T(p)$**: The time it takes to complete the task using $s$ nodes.
  - **Formula:**
    - The speed-up is calculated as: $$ Speedup(s) = \frac{1}{(1 - p) +
      \frac{p}{s}} $$
  - **Examples:**
    - If 90% of a task is parallelizable, the maximum speed-up is 10 times,
      regardless of how many nodes are used.
    - If only 50% is parallelizable, the maximum speed-up is just 2 times, even
      with infinite nodes.

- **Graph Explanation**
  - The graph illustrates how different levels of parallelization affect
    speed-up as the number of processors increases.
  - As the parallel portion increases, the potential speed-up also increases,
    but it eventually levels off, showing diminishing returns.

<center>

# 11 / 16: Factors Limiting Speed-up and Scale-up

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides011.png){width=80%}

</center>
- **Startup costs**
  - When we talk about *startup costs*, we're referring to the initial time and
    resources needed to get a process up and running. This can be a significant
    factor because sometimes the time it takes to start a process can be longer
    than the time it takes to actually perform the task. For example, databases
    often create a thread pool when they start up, which can take a while and
    delay the actual processing of data.

- **Interference**
  - _Interference_ occurs when multiple processes are trying to use the same
    resources at the same time. This can lead to delays because processes have
    to wait for others to finish using shared resources like the system bus,
    disks, or locks. A real-world analogy is when developers work on the same
    piece of code, leading to merge conflicts that need to be resolved before
    progress can continue.

- **Cost of synchronization**
  - When tasks are broken down into smaller pieces, the need for
    _synchronization_ increases. This means more time and effort are required to
    coordinate these tasks. For instance, if a company hires many developers, it
    becomes more complex to manage and synchronize their work, which can slow
    down overall progress.

- **Skew**
  - _Skew_ refers to the uneven distribution of work among tasks, which can lead
    to some tasks taking much longer than others. This is problematic because
    the overall execution time is often determined by the slowest task. It's
    challenging to divide tasks perfectly evenly, and this variance can
    significantly impact the efficiency of a process.

<center>

# 12 / 16: Topology of Parallel Systems

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides012.png){width=80%}

</center>
- **Many ways to organize computation and storage**
  - In parallel systems, computation and storage can be organized in various ways
    using components like memory (M), processors (P), and disks (D).

- **Topology**
  - _Shared memory_: All processors access a common memory space. This setup can
    simplify programming but may lead to bottlenecks.
  - _Shared disk_: Each processor has its own memory, but disks are shared. This
    allows for data sharing while maintaining some independence.
  - _Shared nothing_: Each processor has its own memory and disk. This setup
    maximizes independence and scalability but requires efficient data
    distribution.
  - _Hierarchical_: Combines elements of the above topologies, often used to
    balance performance and resource sharing.

- **Problems**
  - _Cache coherency_: Ensuring that all processors have the most recent data in
    their caches.
  - _Data communication_: Efficiently transferring data between processors.
  - _Fault tolerance_: Maintaining system functionality despite failures.
  - _Resource congestion_: Avoiding bottlenecks in resource access, particularly
    in shared systems.

<center>

# 13 / 16: Topology of Parallel Systems: Comparison

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides013.png){width=80%}

</center>
- **Shared Memory**
  - *Communication between processors*: Extremely fast due to direct access to a common memory space.
  - *Scalability*: Limited to around 32 or 64 processors because the memory bus becomes a bottleneck.
  - *Notes*: Cache-coherency is a significant issue, as multiple processors need to maintain a consistent view of memory.
  - *Main use*: Suitable for low degrees of parallelism where fast communication is crucial.

- **Shared Disk**
  - _Communication between processors_: Fast, but relies on a disk interconnect.
  - _Scalability_: Not very scalable; the disk interconnect limits performance
    as more processors are added.
  - _Notes_: Transactions are complicated, but there is natural fault-tolerance
    due to shared disk access.
  - _Main use_: Not commonly used due to complexity and scalability issues.

- **Shared Nothing**
  - _Communication between processors_: Slowest, as it occurs over a LAN.
  - _Scalability_: Highly scalable, as each processor has its own memory and
    disk.
  - _Notes_: Distributed transactions are complex, involving challenges like
    deadlock detection.
  - _Main use_: Widely used in systems requiring high scalability and
    independence between nodes.

<center>

# 14 / 16: Distributed Databases

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides014.png){width=80%}

</center>
- **Distributed DBs**
  - *Definition*: Distributed databases are systems where the database is stored
    across multiple nodes located in different geographical locations. These
    nodes communicate via high-speed private networks or the Internet.
  - *Purpose*: They are essential for large corporations with global offices to
    ensure data redundancy and disaster recovery. This setup helps maintain high
    availability even during failures like natural disasters, power outages, or
    hacker attacks. However, distributed databases are not primarily designed for
    performance enhancement; parallel databases are more suited for that purpose.

- **Why needed?**
  - _Global Reach_: Useful for corporations with offices worldwide.
  - _Redundancy_: Provides backup and recovery options.
  - _High Availability_: Ensures continuous operation despite failures.
  - _Performance Note_: Not typically used for performance improvements;
    parallel databases are better for this.

- **Wide-area networks (WAN) vs Local-area networks (LAN)**
  - _Bandwidth and Latency_: WANs have lower bandwidth and higher latency
    compared to LANs, leading to a higher chance of failures and network
    partitioning.
  - _Memory and Disk Sharing_: There is no sharing of memory or disks in WANs,
    making communication delays more significant.
  - _Node Differences_: Nodes in distributed databases can vary in size and
    function, unlike parallel databases where nodes are usually similar.

<center>

# 15 / 16: Consistency Issues in Distributed DB Systems

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides015.png){width=80%}

</center>
- **Parallel and distributed DBs**
  - These databases are designed to handle large-scale data processing
    efficiently, especially for read-only queries. However, maintaining
    consistency across distributed nodes is crucial to ensure data integrity and
    reliability.

- **Atomicity issues**
  - The main challenge is ensuring that a transaction is completed entirely or
    not at all across different nodes. This is known as the all-or-nothing
    principle.
  - **Two-phase commit (2PC)**
    - This is a protocol used to ensure atomicity in distributed systems. It
      involves a centralized approach where a single coordinator node makes the
      commit decision.
    - Each participating node executes the transaction and reaches a "ready
      state." If all nodes are ready, the coordinator commits the transaction.
    - If a node fails while in the ready state, it can recover using mechanisms
      like write-ahead logs. If any node aborts, the coordinator will abort the
      entire transaction.
  - **Distributed consensus**
    - Protocols like Paxos and blockchain are used to achieve consensus across
      distributed systems, ensuring that all nodes agree on the transaction
      outcome. These methods help in maintaining consistency and reliability in
      distributed databases.

<center>

# 16 / 16: Consistency Issues in Distributed DB Systems

</center>
<center>

![](data605/lectures_commentary/Lesson10.1-Parallel_DBs.png/slides016.png){width=80%}

</center>
* **Consistency Issues in Distributed DB Systems**

- **Concurrency issues**
  - _Problem_: When multiple processes are writing and reading data at the same
    time, it can lead to inconsistencies. This is because one process might read
    data that is being modified by another process, leading to incorrect or
    unexpected results.
  - To manage this, systems use locks to control access to data. However, this
    can lead to deadlocks, where two or more processes are waiting for each
    other to release locks, causing the system to halt. Managing these locks and
    preventing deadlocks is crucial for maintaining consistency.

- **Autonomy issues**
  - _Problem_: Different units or departments within an organization often want
    to maintain control over their own systems. This can create challenges when
    trying to ensure consistency across a distributed database system.
  - For example, each unit might have its own schedule for administering
    systems, applying patches, or updating software. This lack of coordination
    can lead to inconsistencies and difficulties in maintaining a unified
    system. It's important to balance the need for autonomy with the need for
    consistency in a distributed environment.
