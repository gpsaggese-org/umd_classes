---
title: "11.2: Technologies Enabling Cloud Computing"
---

<!-- git_hash=4f246573-ksw timestamp=20260804_171445 -->

<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides001.png){width=80%}

</center>
<center>

# 2 / 20: Data Centers: Capex

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides002.png){width=80%}

</center>
- **Data centers enable cloud computing**
  - Data centers are essential for cloud computing, providing the infrastructure needed to store and process vast amounts of data.
  - They allow for scalable and flexible computing resources, which are crucial for businesses and services that rely on cloud technology.

- **Large companies (e.g., AWS, Apple, Google, Facebook) build data centers
  globally**
  - Major tech companies invest heavily in building data centers around the
    world to support their services and ensure low latency and high
    availability.
  - This global presence helps them serve a diverse and widespread user base
    efficiently.

- **Data centers cost around 1 billion USD to build**
  - Building a data center is a significant capital expenditure (Capex), often
    reaching around 1 billion USD.
  - **Capex: Computing, memory, storage, networking**
    - The costs include investments in computing power, memory, storage
      solutions, and networking infrastructure.
  - **Prices are dropping**
    - Technological advancements and economies of scale are contributing to a
      decrease in the costs associated with building and maintaining data
      centers.
  - **Size is increasing**
    - As demand for cloud services grows, data centers are expanding in size to
      accommodate more servers and storage capacity.

<center>

# 3 / 20: Data Centers: Opex

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides003.png){width=80%}

</center>
- **Powering equipment cost**
  - Emphasizes the importance of *energy-efficient computing* to reduce operational expenses (Opex). This involves using technology that consumes less power while maintaining performance.

- **High cooling cost**
  - Effective _vent placement_ is crucial for managing thermal hotspots, which
    can lead to inefficiencies and increased costs.
  - **PUE (Power Usage Effectiveness)**
    - Measures how efficiently a data center uses energy; specifically, how much
      energy is used by the computing equipment in contrast to cooling and other
      overhead.
    - An ideal PUE is 1, meaning all energy is used for computation. Current PUE
      values range from 1.07 to 1.22, indicating room for improvement.
    - Smaller data centers find it challenging to optimize PUE, potentially
      driving the trend towards larger data centers.

- **Lots of research on energy-saving**
  - Ongoing research aims to find innovative ways to reduce energy consumption,
    which is a significant part of data center operational costs.

- **Data centers built**
  - Often located near _cheap energy sources_ and in _cold climates_ to
    naturally reduce cooling costs and improve energy efficiency. This strategic
    placement helps in minimizing operational expenses.

<center>

# 4 / 20: (Modular) Data Centers

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides004.png){width=80%}

</center>
- **Cooling**: 
  - The data center uses high-efficiency water-based cooling systems. 
  - These systems are less energy-intensive compared to traditional chillers.
  - Cold water circulates through containers to remove heat, eliminating the need for air-conditioned rooms.

- **Structure**:
  - The facility spans 24,000 square meters and houses 400 containers.
  - Containers are delivered by trucks and connect to a central infrastructure
    for network, power, and water.
  - The design avoids conventional raised floors, simplifying construction and
    maintenance.

- **Power**:
  - Two power substations supply a total of 300 megawatts to the data center.
  - 200 MW is allocated for computing equipment, while 100 MW is for cooling and
    electrical losses.
  - Backup power is provided by batteries and generators, ensuring reliability.

- **Container**:
  - Each container is 67.5 cubic meters and can house 2,500 servers.
  - This is about ten times the capacity of traditional data centers in the same
    space.
  - Containers integrate computing, networking, power, and cooling systems,
    making them highly efficient and scalable.

<center>

# 5 / 20: Meta

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides005.png){width=80%}

</center>
- **Global scale of data centers**
  - Meta operates 29 dedicated data centers worldwide, emphasizing their vast infrastructure.
  - These facilities are *hyperscale* and optimized for AI, indicating they are designed to handle massive amounts of data and complex computations efficiently.

- **Investment**
  - Meta plans to invest $600 billion in U.S. infrastructure by 2028,
    highlighting their commitment to expanding and enhancing their technological
    capabilities.
  - The El Paso data center represents a significant investment of $1.5 billion,
    showcasing the scale of individual projects.
  - The Louisiana campus is a major initiative with a $10 billion investment for
    nine buildings, reflecting a substantial expansion effort.
  - Over $3 billion is allocated for power infrastructure upgrades, ensuring
    that the data centers have the necessary energy resources to operate
    effectively.

- **Data Center Details**
  - The table provides specific details about various data centers, including
    their location, year of going online, number of buildings, square footage,
    and investment amount.
  - This information illustrates the geographical spread and scale of Meta's
    data center operations, with significant investments in both the U.S. and
    international locations.
  - The map visually represents the distribution of these data centers across
    the United States, emphasizing their strategic placement to optimize data
    processing and delivery.

<center>

# 6 / 20: Amazon Web Services

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides006.png){width=80%}

</center>
- **AWS**
  - **2022: 28 geographical regions**
    - *AWS*, or Amazon Web Services, is a leading cloud service provider.
    - In 2022, AWS had established 28 geographical regions worldwide.
    - Each region consists of multiple data centers, known as Availability Zones, which help ensure reliability and redundancy.
    - These regions allow AWS to provide services closer to users, reducing latency and improving performance.

- **2025: 38 regions**
  - AWS plans to expand to 38 regions by 2025.
  - This expansion reflects AWS's commitment to increasing its global footprint
    and meeting growing demand.
  - New regions will enhance service availability and provide more localized
    options for businesses.
  - The expansion also supports compliance with local data regulations, which
    can vary by country.

- **Map Visualization**
  - The map shows current and upcoming AWS regions.
  - Blue dots represent existing regions, while red dots indicate planned
    regions.
  - This visual helps illustrate AWS's strategic growth and global reach.

<center>

# 7 / 20: Amazon Web Services (EC2)

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides007.png){width=80%}

</center>
- **Widely used solution for cloud computing**
  - Amazon EC2 is a popular choice for businesses needing scalable computing power.
  - It offers a variety of instance types to match different workloads and requirements.
  - The competitive pricing is a result of the growing cloud market and competition among providers.

- **Small Instance – default**
  - _1.7 GB memory_ and _1 EC2 Compute Unit_ make it suitable for basic
    applications.
  - Comes with _160 GB instance storage_ and operates on a _32-bit platform_.
  - _I/O Performance_ is moderate, making it ideal for less demanding tasks.
  - API name: _m1.small_.

- **Large Instance**
  - Offers _7.5 GB memory_ and _4 EC2 Compute Units_ for more intensive
    applications.
  - Provides _850 GB instance storage_ on a _64-bit platform_.
  - High _I/O Performance_ supports more demanding workloads.
  - API name: _m1.large_.

- **Extra Large Instance**
  - Equipped with _15 GB memory_ and _8 EC2 Compute Units_ for high-performance
    needs.
  - Features _1,690 GB instance storage_ and a _64-bit platform_.
  - High _I/O Performance_ is suitable for data-intensive applications.
  - API name: _m1.xlarge_.

<center>

# 8 / 20: Amazon S3

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides008.png){width=80%}

</center>
- **Amazon S3**
  - **Amazon storage services (S3 = Simple Storage Solution)**
    - Amazon S3 is a cloud storage service that allows you to store and retrieve any amount of data at any time. It's called "Simple Storage Solution" because it provides a straightforward way to store data in the cloud.
    - **Pay for storage you use**: With Amazon S3, you only pay for the storage you actually use. This means you don't have to worry about overpaying for unused storage space, making it a cost-effective solution for many users.

- **Different tiers for reliability, cost, performance**
  - Amazon S3 offers various storage tiers, each designed to meet different
    needs in terms of reliability, cost, and performance. This flexibility
    allows users to choose the most suitable option based on their specific
    requirements.

- **Storage Tiers Overview**
  - **@Default@**: This is the standard storage class, offering the highest
    durability and availability. It's ideal for frequently accessed data.
  - **@RRS@ (Reduced Redundancy Storage)**: Offers lower durability at a reduced
    cost, suitable for non-critical data that can be easily reproduced.
  - **@IA@ (Infrequent Access)**: Designed for data that is accessed less
    frequently but requires rapid access when needed. It offers high durability
    but incurs retrieval fees.
  - **@Glacier@**: This tier is for archival storage, where data is accessed
    infrequently. It provides high durability at a low cost, but retrieval times
    can take minutes to hours, and there are retrieval fees.

- **Key Considerations**
  - **Durability**: Refers to the likelihood of data loss. Most tiers offer
    99.999999999% durability, meaning data is extremely safe.
  - **Availability**: Indicates how often the service is operational and
    accessible. Most tiers offer high availability, except for the Infrequent
    Access tier.
  - **Extra Fees**: Some tiers, like Infrequent Access and Glacier, charge
    additional fees for data retrieval, which is important to consider when
    planning your storage strategy.
  - **Real-Time Access**: Most tiers provide real-time access to data, except
    for Glacier, which is designed for archival purposes and has longer
    retrieval times.
  - **Frequently Accessed**: The Default and RRS tiers are suitable for data
    that needs to be accessed frequently, while IA and Glacier are better for
    data that is accessed less often.

<center>

# 9 / 20: Google App Engine

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides009.png){width=80%}

</center>
* **Google App Engine**
  - **Google Compute Engine (IaaS)**
    - This is Google's Infrastructure as a Service offering, similar to AWS EC2.
    - It provides virtual machines that run on Google's infrastructure.

- **Google Infrastructure (PaaS)**
  - Platform as a Service that allows running Docker containers on Google
    resources.
  - Offers managed services like databases, simplifying application deployment.

- **Google Docs (SaaS)**
  - Software as a Service providing cloud-based word processing, spreadsheets,
    and presentations.

* **Google Cloud's Compute Market Share**
  - Google was a pioneer in building software data centers, even before Amazon.
  - They invented key cloud technologies like Google File System, MapReduce, and
    BigTable.
  - Despite this, their market share is about three times smaller than AWS.
  - Challenges include:
    - Perception of being unfriendly to developers and customers.
    - Concerns over Google's commitment to services (often referred to as
      "Killed by Google").
    - Criticisms of poor customer service.

* **Virtualization**
  - The images show market share comparisons of cloud service providers.
  - AWS leads with a significant share, followed by Azure and Google Cloud.
  - The cloud infrastructure service revenue is substantial, indicating a
    growing market.

<center>

# 10 / 20: Virtualization

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides010.png){width=80%}

</center>
* **Virtualization**
  - **Virtual machines have been around for a long time**
    - Processors have had support since the 1980s
      - Virtual machines (VMs) are not a new concept; they have been supported by processors for several decades. This means that the technology has been evolving and improving over a long period, making it more reliable and efficient.
    - In the 2000s, they became efficient enough for cloud computing
      - By the 2000s, advancements in technology made VMs efficient enough to be used in cloud computing. This efficiency is crucial because it allows for the scalable and flexible use of computing resources, which is a hallmark of cloud services.

- **Basic idea of cloud computing**
  - Run virtual machines on servers and sell time on them
    - The core concept of cloud computing is to run VMs on powerful servers and
      offer these resources to users on a rental basis. This model allows
      businesses and individuals to access computing power without needing to
      own and maintain physical hardware.
  - E.g., AWS, Microsoft Azure, Google Cloud
    - Major companies like Amazon Web Services (AWS), Microsoft Azure, and
      Google Cloud have adopted this model, providing a wide range of cloud
      services that cater to different needs, from storage to computing power.

- **Many advantages**
  - _Security_: virtual machines have a strong boundary that enhances security
    - VMs provide a secure environment because they create isolated spaces for
      applications to run. This isolation helps protect against security
      breaches, as each VM operates independently.
  - _Multi-tenancy_: multiple VMs can run on the same server
    - Multi-tenancy refers to the ability to run multiple VMs on a single
      physical server. This capability maximizes resource utilization and allows
      different users or applications to share the same hardware without
      interfering with each other.
  - _Efficiency_: replace many underpowered machines with fewer high-powered
    machines
    - By using fewer high-powered machines instead of many underpowered ones,
      organizations can achieve greater efficiency. This consolidation reduces
      costs and simplifies management while maintaining or even improving
      performance.

<center>

# 11 / 20: Desktop vs Server Virtualization

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides011.png){width=80%}

</center>
- **Desktop Virtualization**
  - *VMware, Xen, VirtualBox*: These are popular tools used for desktop virtualization, allowing multiple operating systems to run on a single physical machine.
  - *Runs on host OS*: The virtualization software operates on top of the existing operating system, managing virtual machines (VMs) that host guest operating systems.
  - *Hypervisor/VM supports guest OS*: The hypervisor is responsible for creating and managing VMs, each of which can run a different guest OS.

- **Server Virtualization**
  - _Runs hypervisor on hardware_: Unlike desktop virtualization, server
    virtualization often involves running the hypervisor directly on the
    hardware, without a host OS, for better performance.
  - _Ideal for server farms, cloud computing_: This setup is well-suited for
    environments like data centers and cloud services where resource efficiency
    and scalability are crucial.
  - _Amazon used Xen on Red Hat_: Initially, Amazon used Xen hypervisor on Red
    Hat systems for its cloud services.
    - _Now it uses AWS Nitro_: Amazon has transitioned to using its own AWS
      Nitro system for improved performance and security.

- **Performance is tricky**
  - _Hard to reason about performance_: Virtualization can complicate
    performance analysis due to the abstraction layers involved.
  - _Identical VMs may deliver different performance_: Factors like
    multi-tenancy and varying hardware can lead to inconsistent performance
    across VMs.
  - _"Bare-metal" compute to improve performance_: Running applications directly
    on hardware, without virtualization, can enhance performance by eliminating
    overhead.

<center>

# 12 / 20: Docker

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides012.png){width=80%}

</center>
- **Docker**
  - Docker allows you to package all the necessary dependencies for an application into a single container. This means everything the application needs to run is bundled together, ensuring consistency across different environments.

- **Advantages**
  - **Containers are fast and portable**: Containers can be quickly started and
    stopped, and they can be easily moved across different environments, making
    them highly portable.
  - **Reduce virtualization overhead**: Unlike traditional virtual machines,
    containers share the host OS, which reduces the overhead associated with
    running multiple guest operating systems.
  - **All containers can run on a single host**: Multiple containers can
    efficiently run on a single physical machine, optimizing resource usage.
  - **Reduce OS licensing costs and maintenance overhead**: Since containers
    share the host OS, there is no need for multiple OS licenses, and
    maintenance is simplified.

- **Programming Frameworks**
  - The diagrams compare traditional machine virtualization with
    containerization. In machine virtualization, each application runs on its
    own guest OS, managed by a hypervisor. This setup can be resource-intensive.
  - In contrast, containers run on a shared OS with a container engine, which is
    more efficient. This setup reduces the need for multiple guest OS instances,
    leading to better resource utilization and simplified management.

<center>

# 13 / 20: Programming Frameworks

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides013.png){width=80%}

</center>
* **Programming Frameworks**
  - *Programming frameworks* have become essential tools in the world of computing. They are designed to help manage and execute large-scale computing tasks by allowing workloads to be spread out, or *scaled out*, across many machines. This means that instead of relying on a single computer to do all the work, the task is divided among thousands of machines, making the process faster and more efficient.

- **Parallel Approach**
  - The concept of using a _parallel approach_ to handle computing tasks isn't
    new. It involves running multiple processes simultaneously to speed up
    computation. However, this approach can be quite complex for programmers.
    They need to ensure that applications are properly parallelized, meaning the
    tasks are divided correctly among different processors. Additionally, they
    must manage how data is distributed across machines, deal with potential
    failures, and troubleshoot issues like debugging and race conditions, which
    are unpredictable bugs that occur when the timing of events affects the
    program's behavior.

- **The Difference is the User Interface**
  - What sets modern programming frameworks apart is their _user interface_.
    Google pioneered this shift with the development of MapReduce, which
    simplified the process of writing programs that process large amounts of
    data. This innovation led to the creation of other frameworks like Hadoop
    and Spark, which have become popular tools for big data processing.
    Additionally, cloud services like AWS offer similar capabilities, making it
    easier for businesses to leverage these technologies without needing to
    manage the underlying infrastructure themselves.

<center>

# 14 / 20: MapReduce Framework

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides014.png){width=80%}

</center>
- **MapReduce Framework**
  - The MapReduce framework is a *powerful tool* for processing large datasets across distributed systems. It provides a way to handle big data by breaking down tasks into smaller, manageable parts that can be processed in parallel. This framework is particularly useful for tasks that involve large-scale data processing, such as indexing web pages or analyzing logs.

- **Separation of responsibilities**
  - _Programmers_
    - Programmers are responsible for writing two key functions: `map` and
      `reduce`. The `map` function processes input data and produces
      intermediate key-value pairs, while the `reduce` function takes these
      intermediate results and combines them to produce the final output. This
      separation allows programmers to focus on the logic of data processing
      without worrying about the underlying system complexities.
  - _Framework_ handles
    - The framework itself takes care of the more complex aspects of distributed
      computing. It schedules tasks across different nodes in a cluster,
      ensuring that each part of the data is processed efficiently.
      Additionally, it provides fault tolerance, meaning that if a node fails,
      the framework can recover and continue processing without losing data.
      This makes the MapReduce framework robust and reliable for large-scale
      data processing tasks.

<center>

# 15 / 20: Other Programming Frameworks

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides015.png){width=80%}

</center>
- **Other Programming Frameworks**
  - There are many programming frameworks designed to overcome the limitations of MapReduce, which is a popular model for processing large data sets.
  - **High-performance Computing (HPC) Systems**
    - These systems use clusters of supercomputers to perform complex computations more efficiently.
    - Examples include GridRPC and MPI, which are more expressive and efficient than traditional MapReduce.
  - **Spark**
    - Spark is built on the concept of Resilient Distributed Datasets (RDD), which allows it to process data in-memory, making it faster and more efficient than MapReduce.
  - **Apache Storm, Spark Streaming**
    - These frameworks are designed to handle real-time streaming data, which is crucial for applications that require immediate data processing.
  - **Giraph, GraphLab, GraphX**
    - These are specialized systems for processing graph data, which is important for applications like social network analysis.
  - **Apache Hive**
    - Hive provides a SQL-like interface on top of Hadoop's HDFS, making it easier for users familiar with SQL to work with big data.
  - **Apache HBase**
    - HBase is a NoSQL database that is column-oriented and allows for random read and write access to large tables stored on Hadoop's HDFS.
    - It is modeled after Google's BigTable, providing a scalable and efficient way to handle large datasets.

<center>

# 16 / 20: Cloud Benefits (1/2)

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides016.png){width=80%}

</center>
- **Lower-cost, light end-devices**
  - The cloud allows us to move heavy computing tasks and data storage away from our personal devices to remote servers. This means that our personal computers, like PCs and laptops, don't need to have as much memory, disk space, or processing power. This is particularly beneficial for *thin clients*, which are devices designed to be lightweight and rely on a server for processing power. It also helps keep costs down for low-cost devices and allows older hardware to remain useful longer.

- **Scalability and elastic storage**
  - One of the biggest advantages of cloud computing is its ability to scale.
    This means you can store as much data as you need and handle varying
    workloads without worrying about running out of space or processing power.
    You don't have to buy extra hardware or plan for future needs because the
    cloud can adjust dynamically to your requirements, providing resources as
    needed.

- **Anywhere access and device independence**
  - With cloud services, you can access your work from any device that has an
    internet connection, whether it's a laptop, tablet, or smartphone. This
    means your documents, applications, and data are always with you, no matter
    what device you're using. This seamless transition between devices makes it
    easier to work on the go and ensures you have the most up-to-date
    information at your fingertips.

<center>

# 17 / 20: Cloud Benefits (2/2)

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides017.png){width=80%}

</center>
- **Cloud-native software and SaaS model**
  - With *cloud-native software* and the *Software as a Service (SaaS)* model, users can access full-featured applications directly over the internet. This means there's no need to install software on individual devices or worry about purchasing licenses. This approach simplifies access and reduces the burden on IT departments.
  - One of the significant advantages is that updates and patches are handled automatically. This ensures that users always have access to the latest features and security improvements without any manual intervention. It keeps the software up-to-date and secure, enhancing user experience and productivity.

- **Improved collaboration and version control**
  - Cloud services enable real-time, multi-user editing and sharing of documents
    from any location. This means that teams can work together seamlessly,
    regardless of where they are in the world, which is especially beneficial in
    today's remote work environment.
  - These services often include built-in revision history and tools to avoid
    conflicts when multiple users are editing the same document. This ensures
    that everyone is on the same page and reduces the risk of errors or data
    loss.

- **Faster development and deployment cycles**
  - Technologies like _containerization_, _serverless functions_, and
    _microservices_ allow for rapid provisioning and deployment of applications.
    This means that developers can quickly build, test, and deploy applications,
    speeding up the development process.
  - These technologies are particularly well-suited for modern workloads such as
    AI/ML, analytics, and distributed applications. They provide the flexibility
    and scalability needed to handle complex and resource-intensive tasks
    efficiently.

<center>

# 18 / 20: Modern Opportunities

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides018.png){width=80%}

</center>
* **Modern Opportunities**

- **Cloud-native support for AI/ML workloads**
  - Cloud providers now offer specialized hardware like _GPUs_ (Graphics
    Processing Units) and _TPUs_ (Tensor Processing Units). These are designed
    to handle the heavy computational demands of training and serving machine
    learning models.
  - This means businesses can scale their AI/ML operations without needing to
    invest in and maintain expensive hardware themselves. They can simply use
    these resources on-demand from cloud providers, making it more
    cost-effective and flexible.

- **Multi-cloud and hybrid-cloud strategies to boost resilience**
  - Many organizations are adopting strategies that involve using multiple cloud
    providers or a combination of cloud and on-premises resources. This is often
    in response to major outages that have affected single cloud providers.
  - By having a multi-cloud or hybrid-cloud setup, businesses can ensure that
    they have a backup plan in place, which increases their resilience and
    reduces the risk of downtime.

- **Improved data sovereignty and regulatory compliance**
  - New regulations, like the _EU Data Act of 2025_, are being introduced to
    enhance data portability and reduce the risk of being locked into a single
    vendor. This means businesses can move their data more freely between
    different service providers.
  - "Sovereign cloud" options are becoming available, which allow organizations
    to choose cloud services that comply with specific jurisdictional and legal
    requirements. This is particularly important for businesses that need to
    ensure their data is handled in accordance with local laws and regulations.

<center>

# 19 / 20: Cloud Limitations

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides019.png){width=80%}

</center>
* **Cloud provider dependency and vendor lock‑in**
  - When you choose a cloud provider, you often become dependent on their services and infrastructure. This is known as *vendor lock-in*. It can limit your ability to switch to another provider because each provider has unique tools and services that may not be compatible with others.
  - If you decide to switch providers, it can be a complex and expensive process. This is because you might need to redesign your applications or migrate large amounts of data, which can be both time-consuming and costly.

- **Security, privacy, and data‑ownership issues**
  - Storing data in the cloud means it is kept off-site, which can make it
    subject to the laws of the country where the data center is located. This
    can raise concerns about who can access your data.
  - For sensitive data, it is crucial to use encryption and have strong data
    governance policies. In some cases, it might be better to keep certain data
    on-premises to maintain control over it.

- **Outages and service disruptions**
  - Cloud services can experience outages, which can disrupt your operations.
    Even the most reliable providers can have downtime, so it's important to
    plan for these situations.
  - Designing your systems to handle failures, known as "design for failure," is
    essential to minimize the impact of these outages on your business.

- **Latency, bandwidth, and connectivity dependence**
  - Cloud services rely on a stable and fast Internet connection. In areas with
    unreliable connectivity, this can be a significant issue.
  - Applications that require low latency, such as real-time gaming or
    high-performance computing (HPC), might not perform well if there is a delay
    in data transmission. This can affect the user experience and the
    effectiveness of these applications.

<center>

# 20 / 20: Post‑2025 Challenges

</center>
<center>

![](data605/lectures_commentary/Lesson11.2-Cloud_Computing_Enablers.png/slides020.png){width=80%}

</center>
- **Increasing regulatory burden and data-sovereignty demands**
  - As we move past 2025, there is an expectation of more stringent regulations concerning data management. For example, the EU Data Act is a regulation that mandates cloud providers to ensure data can be easily moved between services (data portability), maintain transparency in their operations, and limit data access across borders. This means companies will need to navigate a complex web of rules, especially if they operate in multiple countries. Compliance with these regulations can be challenging and may require significant changes in how companies handle data.

- **Cloud sprawl and rising costs**
  - The use of multiple cloud services (multicloud) and a mix of on-premises and
    cloud resources (hybrid setups) can lead to what's known as "cloud sprawl."
    This situation makes it difficult to manage costs effectively. Companies
    might face unexpected charges, such as fees for moving data out of a cloud
    service (egress charges) or complex licensing fees. Without careful
    monitoring and management, resource usage can spiral out of control, leading
    to higher expenses.

- **Feature and performance limitations for specialized workloads**
  - While cloud services offer many benefits, they may not always meet the needs
    of specialized tasks. For instance, applications that run on a desktop might
    perform better than their cloud-based counterparts. Tasks that require a lot
    of computing power or need to be completed quickly (latency-sensitive) might
    not perform as well in the cloud. This means that for certain workloads,
    companies might still need to rely on traditional computing solutions to
    achieve the desired performance.
