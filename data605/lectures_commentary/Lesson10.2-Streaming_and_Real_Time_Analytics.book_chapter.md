---
title: "10.2: Streaming and Real-time Analytics"
---

<!-- git_hash=4f246573-g2g timestamp=20260804_171201 -->

<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides001.png){width=80%}

</center>
<center>

# 2 / 21: Data Streams: Motivation

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides002.png){width=80%}

</center>
- **Data Streams: Motivation**
  - *Big Data is generated as a continuous, unbounded stream*
    - In today's world, data is not just stored in static databases. Instead, it flows continuously like a river. This means that data is always being generated and never stops, which is why we call it "unbounded."

- **Applications generate data at high velocity**
  - _Financial transactions and market feeds_: Stock markets and banks produce a
    lot of data every second as people buy and sell.
  - _Sensor instrumentation, RFID, IoT telemetry_: Devices like sensors and IoT
    gadgets send data constantly, such as temperature readings or location
    updates.
  - _Network and system monitoring_: Computers and networks are always being
    checked for performance and security, creating a steady stream of data.
  - _Continuous media (video, audio)_: Streaming services like Netflix or
    Spotify send data continuously as you watch or listen.

- _A data stream is a time-ordered sequence of events_
  - When we talk about data streams, we mean that the data comes in a specific
    order based on time. Stream processing is a way to handle this data as it
    comes in, treating it as important information that needs to be processed
    immediately.

- **Requirements**
  - _Ingest and handle high-throughput event streams_: Systems need to be able
    to take in and process large amounts of data quickly.
  - _Low-latency, near-real-time operations (e.g., time-series analytics)_: We
    need to process data almost instantly to make timely decisions, like
    analyzing trends over time.
  - _Efficient dissemination of relevant subsets to consumers_: Not all data is
    useful to everyone, so systems must efficiently send the right data to the
    right people or applications.
  - _Distributed processing to scale beyond a single machine_: To handle the
    vast amount of data, we need to use multiple computers working together, as
    one machine isn't enough.

<center>

# 3 / 21: Data Streams: Examples

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides003.png){width=80%}

</center>
* **Data Streams: Examples**

- **Continuous queries**
  - Continuous queries are like regular SQL queries but designed to run
    continuously over time. This means they keep processing data as it arrives,
    rather than just once.
  - For example, a query like _"compute moving average over last hour every 10
    mins"_ would continuously update the moving average every 10 minutes using
    the most recent hour of data. This is useful for real-time monitoring and
    decision-making.

- **Anomaly detection, pattern recognition**
  - These tasks involve identifying unusual patterns or sequences in data
    streams. For instance, you might want to _"alert me when A occurs and then B
    within 10 mins"_, which means you are looking for a specific sequence of
    events within a short time frame.
  - This often requires correlating events from different data streams to detect
    complex patterns or anomalies, which can be crucial for security or
    operational efficiency.

- **Statistical tasks**
  - Statistical tasks in data streams might involve cleaning or improving the
    quality of incoming data, such as de-noising measured readings to remove
    random fluctuations.
  - Building an online machine learning model means updating the model
    continuously as new data comes in, allowing it to adapt to changes over time
    and improve its predictions or classifications.

- **Process multimedia data**
  - Processing multimedia data in real-time can involve tasks like online object
    detection or activity detection. This means analyzing video or audio streams
    to identify objects or actions as they happen.
  - These tasks are computationally intensive and require efficient algorithms
    to handle the high volume and velocity of multimedia data.

<center>

# 4 / 21: Why Not Using Standard Solutions?

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides004.png){width=80%}

</center>
- **Example**
  - The task is to report the moving average of a variable, XYZ, over the last hour, updating every 10 minutes. This is a common requirement in data analysis where real-time insights are needed.

- **Solution**
  - A typical approach might involve inserting new data into a relational
    database table and then re-running the query to calculate the moving
    average. This method is straightforward but not efficient for real-time data
    processing.

- **Problems**
  - **Re-execution of Full Query**: Each time the query runs, it processes all
    data from scratch, which is inefficient and time-consuming.
  - **Lack of Incremental Updates**: The solution doesn't take advantage of
    incremental updates, which could save resources by only processing new data.
  - **Recursive Computations**: Many streaming computations require recursive
    logic, which is not easily handled by standard SQL queries.
  - **Complexity**: Some computations are too complex to express incrementally
    in a relational database.
  - **Scalability**: Real-world systems often need to handle thousands of
    continuous queries, which can overwhelm traditional database systems.

- **Streaming Concepts**
  - **Rolling Windows**: These are used to calculate metrics like moving
    averages over a specific time frame, updating as new data comes in.
  - **Mathematical Formulas**:
    - The first formula represents the basic calculation of a moving average.
    - The second formula shows an incremental approach, updating the moving
      average as new data arrives, which is more efficient for streaming data.

<center>

# 5 / 21: Pub-Sub Systems: Motivation

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides005.png){width=80%}

</center>
- **Modern distributed systems use small, independent components**
  - *Serverless architectures* and *microservices* are examples of this approach.
  - These systems, like those used by companies such as Uber, allow for easier evolution, isolation, and scalability.
  - By breaking down applications into smaller parts, each component can be developed, deployed, and scaled independently.

- **Publish-subscribe (pub-sub) systems**
  - Also known as "message queues" or "message brokers."
  - These systems connect producers (publishers) and consumers (subscribers) to
    facilitate event distribution.
  - Messages are grouped into _topics_, which cluster related messages together.
  - Pub-sub systems typically focus on lightweight message dissemination rather
    than complex querying.
  - Examples of pub-sub systems include AWS SQS, Kinesis, Kafka, RabbitMQ, Redis
    Streams, Celery, and JBoss.
  - These systems are crucial for enabling real-time data processing and
    communication between distributed components.

The accompanying image illustrates how publishers send messages to a central
topic, which are then distributed to multiple subscribers, highlighting the flow
and organization of messages in a pub-sub system.

<center>

# 6 / 21: Pub-Sub Systems: Architecture

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides006.png){width=80%}

</center>
- **Publishers**
  - *Role*: Publishers are responsible for sending messages or events into the system. They act as the source of information, generating data that needs to be communicated to interested parties.

- **Subscribers**
  - _Role_: Subscribers consume messages. They are the recipients who express
    interest in certain types of messages or events and receive them from the
    system.

- **Message Broker**
  - _Function_: The message broker is a crucial component that routes the flow
    of events between publishers and subscribers. It uses topics and
    subscriptions to determine how messages are distributed, ensuring that each
    subscriber receives the messages they are interested in.

- **Design Parameters**
  - **Event Distribution Model**: This involves organizing how messages are
    categorized and filtered. Topics are used to group messages, while filters
    can refine which messages are sent to which subscribers.
  - **Push vs. Pull Consumption**: This refers to how messages are delivered to
    subscribers. In a push model, messages are sent automatically, while in a
    pull model, subscribers request messages when they are ready to process
    them.
  - **Subscriber Interest Patterns**: This involves understanding and managing
    the different ways subscribers express interest in messages, which can
    affect how messages are routed and delivered.
  - **Delivery Guarantees**: These are assurances about how messages are
    delivered:
    - _At-most-once_: Messages are delivered no more than once, with the risk of
      some messages being lost.
    - _At-least-once_: Messages are delivered at least once, ensuring delivery
      but possibly resulting in duplicates.
    - _Exactly-once_: Messages are delivered exactly once, ensuring no
      duplicates and no losses, which is ideal but often more complex to
      implement.

<center>

# 7 / 21: Delivery Semantics: At-most once

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides007.png){width=80%}

</center>
- **Delivery Semantics: At-most once**
  - *At-most once* delivery means that a message might be lost and not delivered to the recipient. This is a common approach in systems where occasional data loss is acceptable.

- **Pros**
  - **Small implementation overhead, high-performance**: This method is
    efficient because it doesn't require complex mechanisms to ensure message
    delivery, which can slow down the system.
  - **Easy to implement: "fire-and-forget"**: The simplicity of this approach
    lies in its straightforwardness. Once a message is sent, the sender doesn't
    need to worry about its delivery status.

- **Works when occasional loss is acceptable**
  - This approach is suitable for scenarios where losing some messages doesn't
    significantly impact the overall system. For example, in monitoring metrics
    of a website, missing a few data points might not be critical as long as the
    overall trend is captured.

The diagram illustrates a typical setup where a producer sends messages to a
consumer through a message queue. In this setup, messages can be lost at any
stage, either during transmission to the queue or from the queue to the
consumer.

<center>

# 8 / 21: Delivery Semantics: At-least once

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides008.png){width=80%}

</center>
- **At-least once**: This delivery semantic ensures that messages are sent repeatedly until the sender receives an acknowledgment from the receiver. This approach is crucial in systems where message loss is unacceptable, as it guarantees that every message will eventually be delivered.

- **Pros**
  - _Ensures no loss_: The primary advantage of the at-least-once delivery is
    that it prevents message loss. Every message will reach its destination,
    which is vital for applications where missing data could lead to significant
    issues.
  - _Duplicates are possible_: While this method ensures delivery, it can result
    in the same message being delivered multiple times. This is because the
    system continues to send the message until it gets a confirmation, which
    might lead to duplicates if the acknowledgment is delayed or lost.

- **Cons**
  - _Requires idempotent operations or deduplication_: To handle potential
    duplicates, systems must implement idempotent operations—processes that can
    be applied multiple times without changing the result beyond the initial
    application. Alternatively, deduplication strategies can be used to filter
    out repeated messages, ensuring that each message is processed only once.

<center>

# 9 / 21: Delivery Semantics: Exactly once

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides009.png){width=80%}

</center>
- **Exactly once**: This delivery semantic ensures that each message is processed only once across the entire system. It is the most reliable form of message delivery, preventing duplicates and ensuring data consistency.

- **Most consumer-friendly but hardest to guarantee**:
  - This approach is ideal for consumers because it eliminates the risk of
    processing the same message multiple times, which can lead to errors or
    inconsistencies.
  - However, achieving this level of reliability is challenging due to the
    complexities involved in coordinating distributed systems. A classic example
    of this complexity is the "Two Generals' Problem," which illustrates the
    difficulties in achieving consensus in distributed networks.

- **Used in financial and mission-critical systems**:
  - Systems that require high reliability and accuracy, such as payment
    processing, trading platforms, and accounting systems, often implement
    exactly-once semantics.
  - In these contexts, processing a message more than once or not at all can
    have significant financial or operational consequences, making exactly-once
    delivery essential.

<center>

# 10 / 21: Event vs Processing Time

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides010.png){width=80%}

</center>
- **Event vs Processing Time**
  - In streaming and pub-sub architectures, understanding the difference between *event time* and *processing time* is crucial.
    - **Event time** refers to when each record is generated. This is the actual time the event occurs in the real world.
    - **Processing time** is when each record is received by the system. It includes the time taken for events to be ingested and processed, which can differ due to network delays or system load.

- **Problems with Events**
  - Events can arrive late or out of order, which complicates processing.
  - Determining how long to wait for late events, known as stragglers, is
    challenging.
  - Systems often set limits on how late data can be. Extremely late data might
    be ignored or cause the system to recompute results to maintain accuracy.

- **Apache Streaming Zoo Example**
  - The diagram illustrates the difference between event time and processing
    time.
  - Events (Post 1, Post 2, etc.) are generated at specific event times but are
    processed at different times due to delays.
  - This highlights the importance of handling late or out-of-order data in
    streaming systems.

<center>

# 11 / 21: Apache Streaming Zoo

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides011.png){width=80%}

</center>
- **Apache Streaming Zoo**
  - The term "Apache Streaming Zoo" refers to the variety of streaming frameworks developed under the Apache Software Foundation. These frameworks are designed to handle data streams in real-time, providing tools for processing and analyzing data as it flows.
  - **Examples**: Some popular frameworks include *Apache Apex*, *Apache Beam*, *Apache Flink*, *Apache Kafka*, *Apache Spark*, *Apache Storm*, and *Apache NiFi*. Each of these was initially developed by different companies to meet specific needs before being released as open-source projects.

- **Different workloads**
  - These frameworks are used for a range of tasks. **Real-time analytics**
    involves analyzing data as it is generated, which is crucial for
    applications like monitoring systems. **Continuous computation** refers to
    ongoing data processing without interruption.
  - **Streaming ML** (Machine Learning) involves applying machine learning
    models to data streams, allowing for real-time predictions. **ETL
    pipelines** (Extract, Transform, Load) are used to process and move data
    between systems. **Messaging and log aggregation** involve collecting and
    organizing log data from various sources for analysis.

- **Differences arise in**
  - Frameworks differ in their approach to data processing. Some are more suited
    to **batch processing**, where data is processed in chunks, while others
    excel in **streaming**, handling data continuously.
  - **Delivery semantics** refer to how data is delivered and processed,
    affecting reliability and consistency.
  - The role of a framework can be more focused on **compute** (processing data)
    or **pub-sub** (publish-subscribe, managing data flow between producers and
    consumers).
  - Key performance metrics include **throughput** (amount of data processed in
    a given time), **latency** (time taken to process data), and **fault
    tolerance** (ability to handle failures).
  - **API and language support** varies, with some frameworks offering more
    flexibility in terms of programming languages and interfaces, which can
    influence ease of use and integration with other systems.

<center>

# 12 / 21: Apache Storm

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides012.png){width=80%}

</center>
- **Apache Storm** is an open-source system designed for real-time computation. It was initially developed by Twitter, which later made it available to the public. This system is particularly useful for processing large streams of data in real-time.

- **Horizontal scalability** is a key feature of Apache Storm. This means you
  can add more machines to the system to handle increasing amounts of data,
  making it highly adaptable to growing data needs.

- **Directed Acyclic Graph (DAG)** is the structure used by Apache Storm to
  process data:
  - **Spouts** act as data sources, initiating the data flow.
  - **Bolts** are the processing units that perform computations on the data.
  - **Data streams** connect spouts and bolts, forming the edges of the graph.

- **Fault tolerance** is built into Apache Storm to ensure reliability:
  - It guarantees _at-least-once processing_, meaning data is processed at least
    once even if failures occur.
  - Tasks are automatically restarted if they fail.
  - The system can redistribute workloads to maintain performance.

- **Suitable for** complex data processing workflows, Apache Storm excels in
  scenarios requiring multiple stages and parallel processing, making it ideal
  for applications like real-time analytics and monitoring.

<center>

# 13 / 21: Apache Kafka

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides013.png){width=80%}

</center>
- **Open-source distributed streaming platform**
  - Apache Kafka is a powerful tool for handling real-time data feeds. It was originally developed at LinkedIn and became open-source in 2011. This means anyone can use, modify, and distribute it freely, which has contributed to its widespread adoption.

- **Core components**
  - **Producers**: These are the applications that send data to Kafka.
  - **Brokers**: These are the servers that store the data and serve it to
    consumers.
  - **Consumers**: These are the applications that read data from Kafka.
  - **Topics**: These are categories or feeds to which records are published.
  - **Partitions**: Each topic is split into partitions, allowing for parallel
    processing and scalability.

- **Delivery**: Kafka supports different delivery guarantees:
  - _At-least-once_: Ensures that messages are not lost but may be delivered
    more than once.
  - _At-most-once_: Ensures that messages are delivered at most once, but some
    may be lost.
  - _Exactly-once_: Ensures that messages are delivered exactly once, which is
    crucial for certain applications.

- **High throughput, low latency**
  - Kafka is designed for high throughput and low latency, making it suitable
    for handling large volumes of data quickly. It uses persistent, replicated
    log storage to ensure data durability and reliability.

- **Kafka Connect** for integration with external systems
  - This tool allows Kafka to connect with various data sources and sinks,
    making it easier to move data between Kafka and other systems.

- **Kafka Streams** for native stream processing
  - Kafka Streams is a client library for building applications and
    microservices, where the input and output data are stored in Kafka clusters.
    It allows for real-time processing of data streams.

<center>

# 14 / 21: Apache Flink

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides014.png){width=80%}

</center>
- **Apache Flink** is an open-source framework designed for distributed data processing. It excels in handling large-scale data streams and batch processing, making it a versatile tool for real-time analytics and data-driven applications.

- **Distributed Processing Engine**: Flink is built to efficiently process data
  across multiple nodes, providing strong support for _stateful streaming_. This
  means it can maintain and manage state information across streams, which is
  crucial for complex event processing.

- **Exactly-once Semantics**: Through checkpointing and robust state management,
  Flink ensures that each piece of data is processed exactly once, even in the
  event of failures. This reliability is essential for applications where data
  accuracy is critical.

- **Unified API**: Flink offers a unified programming model for both batch and
  streaming data, simplifying the development process and allowing developers to
  use the same codebase for different types of data processing tasks.

- **Rich Windowing Functions**: These functions allow users to define how data
  is grouped and processed over time, which is particularly useful for
  time-based analytics.

- **Deployment Flexibility**: Flink can run on various platforms, including
  standalone clusters, YARN, Mesos, Kubernetes, and cloud environments,
  providing flexibility in deployment and scalability.

- **Processing Styles**: The diagram illustrates how Flink integrates with
  various data sources and sinks, processing streams and queries to provide
  insights and drive applications. This highlights Flink's role in transforming
  raw data into actionable information.

<center>

# 15 / 21: Record-at-a-time Processing

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides015.png){width=80%}

</center>
- **Record-at-a-time Processing**
  - *Designed to handle infinite data streams*: This approach is ideal for systems that need to process continuous flows of data without interruption. Apache Kafka is a popular platform that implements this method, allowing for real-time data processing.

- **Distributed processing over multiple nodes**
  - _Nodes organized in a DAG_: A Directed Acyclic Graph (DAG) structure is used
    to organize nodes, ensuring that data flows in a single direction without
    cycles.
  - Each node continuously:
    - _Receives a single record_: Nodes handle one piece of data at a time,
      ensuring immediate processing.
    - _Processes the record immediately_: This minimizes delay, allowing for
      quick data handling.
    - _Forwards the output to the next node_: After processing, data is sent to
      the subsequent node, maintaining the flow.

- **Pros**
  - _Achieves extremely low latency_: The system is capable of responding in
    sub-millisecond times, making it highly efficient for real-time
    applications.

- **Cons**
  - _Poor fault tolerance_: The system's reliability can be compromised unless
    additional nodes or redundant paths are implemented for failover.
  - _Sensitive to stragglers_: If a node processes data slower than others, it
    can bottleneck the entire system, delaying the overall processing pipeline.

<center>

# 16 / 21: Micro-Batch Stream Processing

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides016.png){width=80%}

</center>
- **Micro-Batch Stream Processing**
  - This approach involves dividing a continuous data stream into *small batches*, such as 1-second windows. This method is implemented in systems like Spark Streaming, also known as "DStreams."

- **Pros**
  - **Recover from failures and stragglers with task scheduling**
    - The system can handle failures by scheduling the same task multiple times,
      ensuring reliability.
  - **Deterministic tasks**
    - Provides _exactly-once processing_, meaning each piece of data is
      processed only once, avoiding duplicates.
    - Offers a consistent API with the same semantics as RDDs (Resilient
      Distributed Datasets), which simplifies development.
    - Built-in _fault-tolerance_ ensures that the system can recover from errors
      without data loss.

- **Cons**
  - **Higher latency**
    - Processing in micro-batches can introduce latency, often in the range of
      seconds, which might not be suitable for applications requiring real-time
      processing.

<center>

# 17 / 21: Spark Structured Streaming

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides017.png){width=80%}

</center>
- **Unified DataFrame/SQL-based model for both batch and streaming**
  - Spark Structured Streaming provides a consistent way to handle both batch and streaming data using the same DataFrame and SQL APIs. This means you can apply the same operations and queries to both types of data, simplifying the development process.

- **System manages state, fault tolerance, incremental computation, and late
  data**
  - The system automatically handles complex tasks such as maintaining state
    across streaming operations, ensuring fault tolerance, and performing
    computations incrementally. It also deals with late-arriving data, ensuring
    that your results are accurate and up-to-date.

- **Streaming table abstraction**
  - _Conceptually an unbounded table continuously appended with new rows_: This
    abstraction allows you to think of streaming data as a table that is
    constantly growing as new data arrives.
  - _At time T, equivalent to a static DataFrame of all rows up to T_: At any
    given moment, the streaming table can be viewed as a snapshot of all the
    data received up to that point, similar to a static DataFrame. This makes it
    easier to reason about the data and apply transformations or queries.

<center>

# 18 / 21: Incrementalization

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides018.png){width=80%}

</center>
- **Framework identifies necessary state across micro-batches**
  - The framework is designed to handle data in small, manageable chunks called micro-batches.
  - It keeps track of the necessary state, which means it remembers what data has been processed so far.
  - This helps in efficiently updating results without reprocessing all data.

- **Uses DAG analysis to compute updated results from prior state**
  - DAG stands for Directed Acyclic Graph, a structure used to model the flow of
    data.
  - By analyzing the DAG, the system can determine how to update results based
    on previously processed data.
  - This method ensures that only the necessary computations are performed,
    saving time and resources.

- **Developers specify trigger conditions for updates**
  - Developers can set specific conditions that determine when the system should
    update the results.
  - These triggers can be based on time intervals or specific events.
  - This flexibility allows for tailored data processing that meets specific
    needs.

- **Results updated incrementally as events arrive**
  - As new data comes in, the system updates the results incrementally.
  - This means only the new data is processed, and the existing results are
    adjusted accordingly.
  - Incremental updates are efficient and allow for real-time data processing,
    which is crucial for streaming applications.

<center>

# 19 / 21: Triggering Modes

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides019.png){width=80%}

</center>
- **Triggering Modes**: These are methods to determine when a streaming data processing system should handle new data. They help manage how and when data is processed in a streaming environment.

- **@Default@**:
  - This mode processes a new batch of data as soon as the previous batch is
    completed. It's a straightforward approach that ensures data is processed as
    quickly as possible without any delay between batches.

- **@Trigger interval@**:
  - Here, you set a specific time interval for processing each batch of data.
    For example, you might choose to process data every 10 minutes. This allows
    for predictable processing times and can help manage system resources
    effectively.

- **@Once@**:
  - This mode waits for an external signal to start processing. For instance,
    you might choose to process data only at the end of the day. This can be
    useful for scenarios where data needs to be processed at specific times or
    under certain conditions.

- **@Continuous (experimental)@**:
  - In this mode, data is processed continuously, which can lead to lower
    latency, meaning data is processed almost in real-time. However, not all
    operations are supported in this mode, as it is still experimental. This
    approach is beneficial when immediate data processing is crucial, but it may
    require more advanced handling and resources.

<center>

# 20 / 21: Saving Modes

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides020.png){width=80%}

</center>
- **Saving Modes**
  - *Indicate when to save results and where*: This point is about deciding the timing and location for saving your data. It's crucial to have a strategy for saving data to ensure that you don't lose important information and that you can access it later for analysis or reporting. 
    - *Each time the result table updates, write to an external file system*: This means that every time your data table gets new information or changes, you should save it to an external storage system. Examples include **HDFS** (Hadoop Distributed File System), **AWS S3** (Amazon Web Services Simple Storage Service), or a database like **MySQL** or **Cassandra**. These systems are designed to handle large amounts of data efficiently.

- **Append mode**
  - _Append new rows since the last trigger_: In this mode, you only add new
    data that has come in since the last time you saved. This is useful when you
    are continuously collecting new data and don't need to change the existing
    data.
  - _Use when existing rows don't change_: This mode is ideal when your data is
    mostly static, and you are only interested in adding new entries without
    modifying the old ones.

- **Update mode**
  - _Write updated rows since the last trigger_: Here, you save only the rows
    that have changed since the last time you saved. This is efficient when you
    need to keep your data up-to-date without rewriting everything.
  - _Update in place_: This means you directly modify the existing data with the
    new changes, which can be more efficient than rewriting the entire dataset.

- **Complete mode**
  - _Write the entire updated result table_: This mode involves saving the whole
    data table every time there is an update. It's a comprehensive approach but
    can be resource-intensive.
  - _General but expensive_: While this method ensures that you have the most
    complete and up-to-date data, it can be costly in terms of storage and
    processing power, especially with large datasets.

<center>

# 21 / 21: Spark Streaming "Hello world"

</center>
<center>

![](data605/lectures_commentary/Lesson10.2-Streaming_and_Real_Time_Analytics.png/slides021.png){width=80%}

</center>
- **`lines` is a `DataStreamReader`**
  - Represents an *unbounded DataFrame*, meaning it can handle continuous data streams.
  - It sets up the reading process but doesn't start reading data immediately.

- **`words` splits data into words**
  - This step processes the incoming data by splitting each line into individual
    words.

- **`counts` is a streaming DataFrame**
  - Performs a running word count, continuously updating as new data arrives.

- **`select()`, `filter()` are stateless transformations**
  - These operations do not depend on previous data; they process each piece of
    data independently.

- **`count()` is a stateful transformation**
  - This operation maintains state over time, keeping track of word counts as
    data streams in.

- **Configuration**
  - Specifies how to write the processed output, such as writing to the
    `console`.
  - Defines the output mode, like `complete`, which updates word counts.
  - Sets the trigger for computation, e.g., every 1 second.
  - Determines where to save metadata to ensure exactly-once processing and
    recovery from failures.

- **`start()` processing (non-blocking)**
  - Begins the data processing stream without blocking other operations.
  - **`awaitTermination()`** blocks the process until data is available,
    ensuring the program waits for streaming data to process.
