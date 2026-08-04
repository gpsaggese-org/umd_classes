---
title: "11.3: AWS Overview"
---

<!-- git_hash=4f246573-p7z timestamp=20260804_171637 -->

<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides001.png){width=80%}

</center>
<center>

# 2 / 33: Amazon Web Services (AWS)

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides002.png){width=80%}

</center>
- **Amazon Web Services (AWS)**
  - *AWS is a platform offering complete cloud solutions*
    - **Computing (e.g., EC2)**: AWS provides Elastic Compute Cloud (EC2), which allows users to rent virtual computers to run their applications. This is a flexible and scalable way to handle computing needs without owning physical hardware.
    - **Storage (e.g., S3)**: Simple Storage Service (S3) is AWS's storage solution, offering scalable and secure storage for data. It's commonly used for storing large amounts of data, such as backups or media files.
    - **Networking**: AWS offers various networking services to connect and manage resources, ensuring secure and efficient data transfer across the cloud.

- _Offers different levels of abstraction_
  - **IaaS, PaaS, SaaS**: AWS provides Infrastructure as a Service (IaaS),
    Platform as a Service (PaaS), and Software as a Service (SaaS). These range
    from basic virtual hardware to complete software solutions, catering to
    different user needs.
    - **Host websites**: AWS can host websites, providing the necessary
      infrastructure and tools to manage web traffic and content.
    - **Run enterprise software**: Businesses can run their enterprise
      applications on AWS, benefiting from its scalability and reliability.
    - **Run machine learning applications**: AWS supports machine learning
      workloads, offering services like SageMaker to build, train, and deploy
      models.

- _Control services in different ways_
  - **Web interface (console)**: Users can manage AWS services through a
    user-friendly web interface, making it easy to configure and monitor
    resources.
  - **CLI: `aws` command**: The Command Line Interface (CLI) allows for
    scripting and automation of AWS tasks, providing a powerful tool for
    developers and system administrators.
  - **Language libraries, SDKs (e.g., Python `boto3`)**: AWS offers Software
    Development Kits (SDKs) for various programming languages, such as Python's
    `boto3`, enabling developers to integrate AWS services into their
    applications seamlessly.

<center>

# 3 / 33: AWS as Business

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides003.png){width=80%}

</center>
- **Services charge a pay-per-use pricing model**
  - AWS operates on a *pay-per-use* model, meaning customers only pay for the resources they consume. This flexibility is attractive to businesses of all sizes, allowing them to scale usage according to their needs.
  - With 500 new services and features added annually, AWS continuously evolves to meet diverse customer demands, staying ahead in the competitive cloud market.

- **Data centers distributed globally**
  - AWS has a global presence with data centers in key regions such as the US,
    Europe, Asia, and South America. This distribution ensures low latency and
    high availability for users worldwide, enhancing performance and
    reliability.

- **Extremely profitable**
  - AWS generates $91 billion in annual revenue as of 2023, showcasing its
    significant impact on the cloud industry.
  - The business grows at an impressive rate of 42% year-over-year, reflecting
    its strong market position and customer trust.
  - AWS controls 30% of the cloud business, making it a leader in the industry
    and a major contributor to Amazon's overall success.

The images humorously depict the transformation of Amazon's business model from
selling books to becoming a dominant force in the cloud computing industry. The
growth chart further illustrates AWS's rapid revenue increase over the years.

<center>

# 4 / 33: Types of Cloud Computing

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides004.png){width=80%}

</center>
- **Types of Cloud Computing**
  - Cloud computing is a technology that allows users to access a *shared pool of configurable computing resources*. This means that instead of owning and maintaining physical hardware, users can use resources like servers, storage, and applications over the internet.
    - **Examples**: These resources can include things like servers, storage, networks, applications, and services. This flexibility allows businesses to scale their operations without investing in physical infrastructure.
    - **Accessible from anywhere**: One of the key benefits of cloud computing is that it can be accessed from virtually anywhere with an internet connection, making it highly convenient for users.
    - **Convenient**: Users can easily access and manage resources without needing to worry about the underlying hardware.
    - **On-demand**: Resources can be provisioned and released as needed, allowing for efficient use of resources and cost savings.

- **Clouds can be**:
  - **_Public_**: These are cloud services offered to the general public by
    companies like Amazon Web Services (AWS). They are typically cost-effective
    and scalable, but users share the infrastructure with others.
  - **_Private_**: These clouds are used exclusively by one organization. They
    offer more control and security, making them ideal for sensitive data or
    specific regulatory requirements, such as those in government sectors.
  - **_Hybrid_**: This approach combines both public and private clouds,
    allowing organizations to take advantage of the benefits of both. For
    example, they might use a private cloud for sensitive data and a public
    cloud for less critical operations.

<center>

# 5 / 33: AWS vs Google Cloud vs Microsoft Azure

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides005.png){width=80%}

</center>
- **Similarities:**
  - All three cloud providers—AWS, Google Cloud, and Microsoft Azure—offer a *global infrastructure*, meaning they have data centers spread across the world. This allows for high availability and low latency.
  - They provide *Infrastructure as a Service (IaaS)*, which includes computing, networking, and storage solutions. For example, AWS offers EC2 for computing, Google Cloud has Compute Engine, and Azure provides Virtual Machines (VMs). Similarly, for storage, AWS has S3, Google Cloud offers Cloud Storage, and Azure provides Blob Storage.
  - They all use a *pay-as-you-go pricing model*, which means you only pay for the resources you use, making it cost-effective and flexible.

- **Differences:**
  - **AWS** is known as the _market leader_ in cloud services. It is considered
    mature and powerful, with a wide range of services and a strong focus on
    utilizing open-source technologies.
  - **Azure** is particularly strong in offering the _Microsoft stack_ in the
    cloud, making it a preferred choice for businesses already using Microsoft
    products.
  - **Google Cloud** focuses on _cloud-native applications_, emphasizing modern,
    scalable, and containerized applications, which is ideal for developers
    looking to build innovative solutions.

<center>

# 6 / 33: From On-premise to AWS: 1/3

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides006.png){width=80%}

</center>
- **From On-premise to AWS: 1/3**
  - This slide introduces the concept of *cloud transformation*, which involves moving services from local servers to cloud-based solutions like AWS.

- **Example: Move a medium-sized e-commerce site from on-premise to the cloud**
  - This example illustrates the transition of a typical e-commerce platform to
    a cloud environment, highlighting the benefits and changes involved.

- **No-cloud (On-premise)**
  - **Web-server**: Manages customer requests directly on local servers,
    requiring manual maintenance and scaling.
  - **DB (Database)**: Stores critical data such as product information and
    customer orders, also maintained on-site.
  - **Static content**: Includes items like JPEG images, which are delivered via
    a Content Delivery Network (CDN) to reduce server load.
  - **Dynamic content**: Consists of HTML pages with real-time data like product
    details and prices, served by the web server.

- **AWS Transition**
  - The diagram shows a shift from on-premise servers to AWS, where the database
    can be managed by Amazon RDS, reducing maintenance efforts.
  - AWS offers a more scalable and maintenance-free environment, allowing
    businesses to focus on growth rather than infrastructure management.

<center>

# 7 / 33: From On-premise to AWS: 2/3

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides007.png){width=80%}

</center>
- **Move to cloud**
  - **Keep the same architecture**
    - When transitioning from on-premise to the cloud, one approach is to maintain the existing architecture. This means replicating the current setup in the cloud environment without making significant changes. It allows for a smoother transition as the system's structure remains familiar.
  
  - **Move components to cloud**
    - This involves transferring specific components of the system to the cloud. For example, the database might be moved to a cloud service like Amazon RDS, which is fully managed by AWS. This reduces the maintenance burden on the organization, as AWS handles updates, backups, and scaling.
  
- **Diagram Explanation**
  - The diagram illustrates a user accessing services over the internet. On the left, the on-premise setup shows both the web server (WWW) and database requiring maintenance. On the right, the AWS setup shows the web server still requiring maintenance, but the database is now managed by Amazon RDS, which is maintenance-free. This highlights the benefit of using managed services in the cloud to reduce operational overhead.

<center>

# 8 / 33: From On-premise to AWS: 3/3

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides008.png){width=80%}

</center>
- **Design for the cloud**
  - **DNS**: Domain Name System (DNS) is crucial for translating domain names into IP addresses, enabling users to access services easily. In the cloud, DNS services are optimized for performance and reliability.
  - **Database**: Using cloud-managed databases like Amazon RDS reduces maintenance costs and complexity. AWS handles backups, scaling, and updates, allowing you to focus on application development.
  - **Object store (S3)**: Amazon S3 provides scalable storage for objects like images and videos. It's cost-effective and integrates with other AWS services, enhancing data accessibility and durability.
  - **Managed solutions**: AWS offers managed services that handle infrastructure tasks, freeing up resources to focus on innovation and application logic.
  - **Use multiple smaller virtual services with a load balancer**: Distributing traffic across multiple instances with a load balancer increases reliability and availability. This setup ensures that if one instance fails, others can handle the load, maintaining service continuity.

- **Image Explanation**
  - The diagram illustrates a cloud architecture where users interact with
    services via the internet.
  - **Load balancer**: Enhances reliability by distributing incoming traffic
    across multiple servers.
  - **DNS**: Improves performance by efficiently routing requests.
  - **CDN**: Content Delivery Network (CDN) accelerates the delivery of static
    content, improving user experience.
  - **Amazon RDS**: A fully managed database service that reduces maintenance
    overhead.
  - **Object store**: Provides scalable storage for static content, integrated
    with CDN for faster access.

<center>

# 9 / 33: Capacity Scaling

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides009.png){width=80%}

</center>
- **No need to plan for capacity**
  - *Do not predict capacity*: With cloud services, there's no need to estimate future needs. Resources can be adjusted as required.
  - *Schedule capacity on-the-fly*: Resources like virtual machines (VMs) and storage can be allocated dynamically, allowing for immediate scaling.
  - *No concern for rack space, switches, power supplies*: Physical infrastructure concerns are minimized, as cloud providers handle these aspects.
  - *Add more VMs and storage as needed*: Easily scale from a few to thousands of VMs and from gigabytes to petabytes of storage.

- **Handle seasonal traffic by scaling up/down**
  - _Day vs night_: Adjust resources based on daily usage patterns.
  - _Weekday vs weekend_: Scale according to weekly traffic variations.
  - _Holidays_: Increase capacity during peak times like holidays.
  - _No test system needed when the team is off_: Reduce resources when not in
    use, saving costs.

- **Worldwide presence**
  - _AWS has many data centers_: A global network of data centers ensures low
    latency and high availability.
  - _Deploy applications close to customers_: Position applications near users
    to improve performance and user experience.

<center>

# 10 / 33: Pay-per-use

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides010.png){width=80%}

</center>
- **Pay-per-use Model**
  - *AWS Bill*: This is similar to how you pay for utilities like electricity. You are charged based on how much you use the services.
    - **Virtual Server Hours**: You pay for the hours your virtual servers are running, rounded up to the nearest hour.
    - **Storage Usage**: Charges are based on the gigabytes of storage you use, whether it's allocated or actually used.
    - **Data Traffic**: You are billed for the amount of data transferred, measured in gigabytes or by the number of requests.

- **Free Tier**
  - AWS offers a _free tier_ for new users, allowing them to use certain
    services without charge for the first 12 months.
  - This is a great opportunity to _experiment_ with AWS services like EC2
    (Elastic Compute Cloud) and S3 (Simple Storage Service).
  - Be cautious: if you exceed the free tier limits, you will start incurring
    charges without any notification. It's wise to set up an _alarm_ to monitor
    usage.

- **Usage and Costs Table**
  - The table provides a comparison of service usage and costs between January
    and February.
  - Noticeable increases in usage, such as the jump in website visits and
    virtual machine hours, lead to higher charges.
  - This highlights the importance of monitoring usage to manage costs
    effectively.

<center>

# 11 / 33: Pay-per-use

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides011.png){width=80%}

</center>
- **Advantages**
  - **No upfront investments or commitment**
    - Pay-per-use models allow businesses to avoid large initial costs. This is particularly beneficial for startups or projects with uncertain futures, as it reduces financial risk.
  
  - **Lower project startup cost**
    - By only paying for what you use, initial expenses are minimized. This makes it easier to launch projects without needing significant capital.

- **Easier to divide the system into smaller parts**
  - Flexibility in resource allocation means you can choose between one large
    server or multiple smaller ones without cost differences. This allows for
    tailored solutions that fit specific needs.

- **Affordable fault tolerance/high performance**
  - The model supports scalability. For instance, using one server for 1000
    hours is equivalent in cost to using 1000 servers for one hour. This
    flexibility ensures that systems can handle varying workloads efficiently
    without overspending.

The image seems to humorously depict strong, influential figures, possibly
symbolizing the robustness and flexibility of the pay-per-use model.

<center>

# 12 / 33: Interacting with AWS

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides012.png){width=80%}

</center>
- **GUI (Management Console)**
  - The AWS Management Console provides a user-friendly graphical interface to interact with AWS services. It is ideal for beginners as it simplifies the process of setting up and managing cloud infrastructure. This tool is particularly useful for development and testing environments where visual feedback is beneficial.

- **Command-line tool (CLI)**
  - The AWS CLI allows users to manage AWS services through commands. It is
    powerful for automating tasks, making it a preferred choice for developers
    who need to script and automate repetitive processes. This tool is essential
    for integrating AWS services into automated workflows.

- **SDKs**
  - AWS SDKs offer libraries for various programming languages, enabling
    developers to interact with AWS services directly from their applications.
    This integration is seamless and allows for more complex and customized
    interactions. For example, `boto3` is the SDK for Python, widely used for
    scripting and automation.

- **Blueprints**
  - Blueprints describe the architecture of a system, including all services and
    dependencies, without detailing the construction process. This approach is
    part of Infrastructure as Code (IaC), where the blueprint is transformed
    into a running infrastructure, ensuring consistency and repeatability in
    deployments.

<center>

# 13 / 33: Accounts and Users

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides013.png){width=80%}

</center>
- **Users**
  - *One root AWS account*: This is the main account with full access to all AWS services and resources. It's crucial to protect this account as it has unrestricted access.
  - *Attach multiple users to an account*: You can create multiple users under the main account, each with specific permissions. This helps in managing access and isolating workloads, ensuring that users only have access to what they need.

- **Be safe**
  - _Never use root account to develop_: The root account should be reserved for
    essential tasks only. Using it for development increases the risk of
    accidental changes or security breaches.
  - _Always use 2FA_: Two-factor authentication adds an extra layer of security,
    making it harder for unauthorized users to access your account.
  - _Avoid costly mistakes_: By limiting the use of the root account and using
    2FA, you reduce the risk of making expensive errors.

- **Key pair**
  - _Create a key pair to access a virtual server_: Key pairs are used for
    secure access to AWS virtual servers. They consist of a public key and a
    private key.
  - _Public key_: Stored in AWS and on virtual servers, allowing secure
    communication.
  - _Private key is your secret_: It's crucial to keep the private key safe. If
    lost, it cannot be retrieved, and access to the server will be lost.

<center>

# 14 / 33: Create User Account

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides014.png){width=80%}

</center>
- **Create a new user**
  - It's important to avoid using the AWS root account for everyday development tasks. The root account has unrestricted access, which can pose security risks if compromised.
  - **IAM (Identity and Access Management)** is a service that helps manage access to AWS resources securely. It allows you to create and manage AWS users and groups and use permissions to allow and deny their access to AWS resources.
  - When creating a user, you'll receive an *access key ID* and a *secret access key*. These are used for programmatic access to AWS services.

- **Access control**
  - _Programmatic access_ enables users to interact with AWS services through
    APIs, SDKs, or the AWS CLI.
  - _Console access_ allows users to log into the AWS Management Console to
    manage services visually.
  - It's crucial to limit user actions through policies. Policies define
    permissions and can restrict what actions a user can perform, enhancing
    security by following the principle of least privilege.

<center>

# 15 / 33: AWS VMs

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides015.png){width=80%}

</center>
- **With virtualization**
  - *Multiple VMs run on the same hardware*: Virtualization allows several virtual machines (VMs) to operate on a single physical server, optimizing resource use and reducing costs.
  - *Start and stop VMs on-demand*: This flexibility means you can easily scale resources up or down based on current needs, enhancing efficiency.

- **Physical server**
  - _Aka "host machine", "bare metal"_: This is the actual physical hardware
    that provides the resources for virtualization.
  - _Consists of CPUs, memory, networking interfaces, storage_: These components
    are essential for running applications and services.

- **Hypervisor**
  - _Software + CPU hardware_: The hypervisor is crucial for managing VMs,
    acting as a bridge between the physical hardware and the virtual
    environments.
  - _Isolates guests_: It ensures that each VM operates independently, providing
    security and stability.
  - _Schedules hardware requests_: Efficiently allocates resources to VMs as
    needed.

- **AWS**
  - _Used Xen hypervisor (open-source) before_: AWS initially utilized Xen for
    virtualization.
  - _Switched to AWS Nitro_: AWS transitioned to Nitro for improved performance.
    - _Hardware-assisted virtualization_: Nitro uses specialized hardware to
      enhance virtualization.
    - _Performance close to bare metal_: Offers near-native performance, making
      it highly efficient.

- **Virtual servers**
  - _Isolated on the same hardware_: Each VM runs independently, ensuring that
    issues in one do not affect others.

<center>

# 16 / 33: Select Region

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides016.png){width=80%}

</center>
- **Select Region**
  - The slide discusses the importance of selecting a region for data centers, using `us-east-1` as an example. This is a common region identifier used by cloud service providers like AWS.
  - *21155 Smith Switch Road, Ashburn, VA, USA* is highlighted as a key location. Ashburn is known for its dense concentration of data centers.

- **Major Internet Backbone in Ashburn, VA**
  - Ashburn is a critical hub for internet infrastructure, often referred to as
    "Data Center Alley."
  - **Equinix, Digital Realty, Vantage Data Centers, H5 Data Centers**: These
    are some of the major companies operating data centers in the area. They
    provide essential services for cloud computing, data storage, and internet
    connectivity.
  - The presence of these companies underscores Ashburn's role as a major node
    in the global internet backbone, facilitating vast amounts of data traffic.

- **Images**
  - The images likely depict the physical infrastructure and geographical
    location of these data centers, emphasizing their scale and strategic
    placement.
  - The maps provide a visual context of Ashburn's proximity to major cities
    like Washington, D.C., highlighting its accessibility and strategic
    importance.

<center>

# 17 / 33: Starting an EC2 Instance

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides017.png){width=80%}

</center>
- **Select OS**
  - *Amazon Machine Image (AMI)*: This is a template that includes the operating system and any pre-installed software. It simplifies the setup process by eliminating the need to manually install the OS and software packages.
  - *Saves time*: Using an AMI can significantly reduce the time needed to get your instance up and running, as everything is pre-configured.

- **Choose instance parameters**
  - _Example: `t2.micro`_: This is a specific type of instance that is often
    used for testing and development due to its low cost and eligibility for the
    free tier.
  - _More info later_: Details about different instance types and their
    specifications will be provided later.

- **Configure instance**
  - _Network_: Set up the network settings to ensure your instance can
    communicate with other resources.
  - _Shutdown behavior_: Decide what happens when the instance is shut down
    (e.g., stop or terminate).
  - _Termination protection_: Enable this to prevent accidental termination of
    the instance.
  - _Monitoring_: Set up monitoring to keep track of the instance's performance
    and health.

These steps are part of launching a virtual machine on AWS using the EC2
service, which allows you to run applications in the cloud efficiently.

<center>

# 18 / 33: AWS Instance Type

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides018.png){width=80%}

</center>
- **AWS Instance Type**: This refers to the specific configuration of virtual hardware that AWS provides. It determines the computing power available for your tasks.

- **Instance Family**: AWS categorizes instances into families based on their
  primary use case:
  - **`T`**: _Cheap, baseline performance_ instances suitable for low-cost
    applications.
  - **`M`**: _General purpose_ instances that balance compute, memory, and
    networking resources.
  - **`C`**: _Compute optimized_ instances designed for compute-intensive
    applications.
  - **`R`**: _Memory optimized_ instances for memory-intensive tasks.
  - **`D`**: _Storage optimized for HDD_ for applications requiring high disk
    throughput.
  - **`I`**: _Storage optimized for SSD_ for high random I/O performance.
  - **`F`**: Instances with _FPGAs_ for hardware acceleration.
  - **`P, G, CG`**: Instances with _GPUs_ for graphics or compute-intensive
    tasks.

- **AWS EC2 List**: A comprehensive list of available instance types can be
  found on the
  [AWS EC2 instance types page](https://aws.amazon.com/ec2/instance-types).

- **Example Instances**:
  - **`t2.micro`**:
    - _Family_: `t` (small, cheap)
    - _Generation_: `2` (second)
    - _Size_: `micro` (1 vCPU, 1GB memory)
    - _Cost_: $0.013 per hour
  - **`m4.large`**:
    - _Family_: `m` (general purpose)
    - _Size_: `large` (2 vCPUs, 8GB memory)
    - _Cost_: $0.10 per hour

These examples illustrate how AWS instances are named and priced, helping users
choose the right configuration for their needs.

<center>

# 19 / 33: AWS Instance Type

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides019.png){width=80%}

</center>
- **AWS Instance Type**
  - When looking at AWS pricing, it can be confusing because there are many factors that affect the cost. 
    - **Burst mode**: Some instances can temporarily increase their performance, which can affect pricing.
    - **vCPUs**: This stands for virtual CPUs, which are the processing power of the instance. More vCPUs generally mean higher costs.
    - **Multi-tenancy**: This refers to whether the instance is shared with other users or dedicated to one user, impacting the price.
    - **On-demand vs. spot vs. reserved vs. pre-paid**: These are different pricing models. On-demand is pay-as-you-go, spot instances are cheaper but can be interrupted, reserved instances are paid upfront for a discount, and pre-paid options can offer savings.

- **642 types of EC2 machines (as of 2023)**
  - AWS offers a wide range of EC2 instances to fit different needs and budgets.
  - The **cheapest instance** costs about $37 USD per year, which is suitable
    for very light workloads.
  - The **most expensive instance** can cost up to $1.91 million USD per year,
    offering massive computing power with 500 CPUs and 24TB of memory, ideal for
    large-scale enterprise applications.

- **[Alternative sites](https://instances.vantage.sh) tracking prices**
  - There are websites like Vantage that help track and compare AWS instance
    prices, which can be useful for finding the best deals and understanding
    pricing trends.

<center>

# 20 / 33: Starting an EC2 Instance

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides020.png){width=80%}

</center>
- **Add storage**
  - *Volume size*: This refers to the amount of storage you allocate to your EC2 instance. In the example, 8 GiB is configured for the root volume.
  - *Volume type*: You can choose between SSD (Solid State Drive) and magnetic HDD (Hard Disk Drive). SSDs, like the gp2 type shown, offer faster performance.

- **Tag**
  - Tags are labels that help you organize and manage your AWS resources. They
    can include information like the environment (e.g., development, production)
    or the project name.

- **Configure firewall**
  - _How to access using SSH_: Secure Shell (SSH) is a protocol used to securely
    connect to your instance. Ensure SSH access is configured correctly.
  - _Select key pair_: A key pair is used for SSH access. You must select or
    create a key pair to connect securely to your instance.

- **How to monitor the instance**
  - _E.g., CloudWatch_: AWS CloudWatch is a monitoring service that provides
    data and actionable insights to monitor your applications, respond to
    system-wide performance changes, and optimize resource utilization.

<center>

# 21 / 33: Starting an EC2 Instance

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides021.png){width=80%}

</center>
- **Start instance**
  - To begin using an EC2 instance, you first need to start it from the AWS Management Console. This involves selecting the instance you want to run and clicking the "Start" button. This action boots up the virtual server.

- **Find public IP**
  - Once the instance is running, you need to locate its public IP address. This
    IP is essential for connecting to the instance remotely. You can find it in
    the instance details within the AWS console.

- **Connect to the machine**
  - Use SSH to connect to your EC2 instance. The command provided uses a private
    key (`mykey.pem`) and the public IP address of the instance.
  - ```bash
    > ssh -i $PATH/mykey.pem ubuntu@$PUBLIC_IP
    ```
  - After connecting, you can check system information using commands like
    `cat /proc/cpuinfo` for CPU details and `free -m` for memory usage.
  - Update the system and install necessary packages using:
    ```bash
    > sudo apt-get update
    > sudo apt-get install ...
    ```

- **Download logs**
  - The image shows the EC2 Management Console where you can download system
    logs. These logs are useful for troubleshooting and analyzing the instance's
    behavior. You can copy or download them for further inspection.

<center>

# 22 / 33: States of a VM

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides022.png){width=80%}

</center>
* **States of a VM**

- **@Start@**
  - This action initiates a stopped virtual machine (VM), bringing it back to an
    active state.

- **@Stop@**
  - When a VM is stopped, it is not billed for compute resources.
  - The network-attached hard disk drive (HDD) continues to exist and incurs
    storage charges.
  - The local disk storage does not persist, meaning any data stored locally is
    lost.
  - Upon restarting, the VM may be assigned to a different host, resulting in a
    different IP address.

* **@Reboot@**
  - The network HDD remains intact, preserving data.
  - Local disk storage is not retained, leading to data loss on local drives.
  - Installed software remains unaffected and continues to exist on the VM.
  - The VM may restart on a different host, similar to the stop/start process.

* **@Terminate@**
  - This action deletes the VM, making it impossible to restart.
  - The network HDD persists, allowing data recovery or reuse.
  - Local disk storage is completely wiped out, erasing all locally stored data.

The diagram illustrates the lifecycle of a VM, showing transitions between
states like pending, running, stopping, and terminated. It highlights how
actions like start, stop, reboot, and terminate affect the VM's state and data
persistence.

<center>

# 23 / 33: Moving / Upgrading EC2 Instances

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides023.png){width=80%}

</center>
- **Moving / Upgrading EC2 Instances**

- _Scale up / down_
  - When you need more computing power, you can **increase the size of your
    virtual machine (VM)**. This means choosing a larger instance type that
    offers more CPU, memory, or other resources.
  - To change the instance type, you must first **stop the VM**. This is
    necessary because the instance type cannot be changed while the VM is
    running.
  - After stopping the VM, you can **change the instance type** to something
    like `m3.large`, which is a specific configuration of resources.
  - Once the instance type is changed, you can **start the VM** again to resume
    operations.
  - Be aware that **IP addresses will change** when you stop and start the VM,
    which might affect how you connect to it.

- **AWS regions**
  - AWS regions are essentially **collections of data centers** located in
    different parts of the world.
  - Each region operates **independently**, meaning they don't automatically
    share data with each other.
  - There is **no automatic data transfer across regions**, so if you need data
    in multiple regions, you must handle the transfer yourself.
  - Some AWS services, like **IAM (Identity and Access Management), CDN (Content
    Delivery Network), and DNS (Domain Name System)**, are considered global and
    are not confined to a single region.

- **Why move across AWS regions**
  - **Proximity to users** is a key reason to choose a specific region. Hosting
    your services closer to your users can reduce latency and improve
    performance.
  - **Compliance** is another factor, as different regions have different rules
    about data storage and processing. You may need to store data in a specific
    region to comply with local laws.
  - **Service availability** can vary by region. Some AWS services might not be
    available in every region, so you might need to move to a region where the
    services you need are offered.
  - **Redundancy** is important for disaster recovery. By using multiple
    regions, you can ensure that your services remain available even if one
    region experiences an outage.
  - **Costs** can differ between regions, so you might choose a region based on
    pricing to optimize your expenses.

<center>

# 24 / 33: Optimizing Costs

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides024.png){width=80%}

</center>
- **Optimizing Costs**
  - **On-demand instances**
    - These instances offer *maximum flexibility* because there are no long-term commitments or restrictions. You can start and stop virtual machines (VMs) whenever you need, which is great for unpredictable workloads or short-term projects. The cost is straightforward as you pay by the hour for the time you use the instances. This option is ideal if you need quick access to computing resources without any upfront commitment.

- **EC2 / Compute saving plans**
  - With these plans, you can choose between a 1-year or 3-year commitment to a
    certain number of computing hours. This commitment allows you to receive
    significant discounts, making it up to 3 times cheaper than on-demand
    instances. You have flexible payment options: pay everything upfront,
    partially, or nothing upfront. These plans are particularly useful for
    development servers where you have a predictable workload and can commit to
    long-term usage.

- **Capacity reservation**
  - This option ensures that you have access to the computing resources you
    need, even during peak usage times. It's like reserving a spot in advance,
    so you don't have to worry about availability when demand is high. This is
    crucial for applications that require guaranteed performance and
    availability.

- **Spot instances**
  - Spot instances allow you to bid for unused computing capacity at a
    significantly reduced cost, sometimes up to 10 times cheaper than on-demand
    instances. The price fluctuates based on supply and demand, so it's ideal
    for tasks that are flexible with timing, such as asynchronous or batch
    processing tasks. This option is great for cost savings if your applications
    can handle interruptions and are not time-sensitive.

<center>

# 25 / 33: Low-Cost Processing

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides025.png){width=80%}

</center>
* **Low-Cost Processing**
  - Many batch jobs are not time-sensitive and can be scheduled to run at specific times. This means they don't need to be processed immediately and can be planned to optimize costs.
    - *Analyze data daily*: This involves processing data once a day, which is often sufficient for many business needs. It allows for the accumulation of data over a 24-hour period before analysis.
    - *Generate reports from a database*: Reports are typically generated periodically, such as daily or weekly, and do not require real-time processing. This makes them ideal candidates for scheduled batch processing.

1. **Allocate machines on demand**
   - Using cloud services like AWS, you can allocate virtual machines (VMs) only
     when you need them. AWS charges for VMs by the minute, so you only pay for
     the time the machines are actually running jobs. This is cost-effective for
     non-critical batch jobs that don't need constant processing power.

2. **AWS Batch**
   - AWS Batch is a service that allows you to run batch computing workloads
     using AWS's spare capacity. This spare capacity is offered at a discounted
     rate, which can save you up to 50% compared to regular pricing. It runs
     jobs when there is available capacity, making it a cost-efficient option
     for non-urgent tasks.

3. **AWS Lambda**
   - AWS Lambda is a serverless computing service that lets you run code without
     provisioning or managing servers. It automatically scales with the size of
     the workload and you only pay for the compute time you consume. This is
     ideal for small, event-driven tasks that can be executed quickly and
     efficiently.

<center>

# 26 / 33: Programming the Infrastructure

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides026.png){width=80%}

</center>
- **On AWS everything can be *controlled via an API***
  - AWS allows users to manage resources programmatically. This means you can automate tasks like starting a virtual machine (VM), creating storage, or launching a Hadoop cluster using API calls.
  
- **Use:**
  - **AWS GUI console**: A web-based interface for managing AWS services.
  - **HTTP requests to API**: Directly interact with AWS services using HTTP requests.
  - **CLI (Command Line Interface)**: Execute AWS API commands from the terminal, offering a scriptable way to manage resources.
  - **SDK (Software Development Kit)**: Integrate AWS services into your applications by calling APIs from your code.
  - **CloudFormation**: Use templates to define infrastructure, which are then translated into API calls to create and manage AWS resources.

- **Jeff Bezos 2002 API mandate**
  - This mandate emphasized the importance of service interfaces for
    communication between teams. It required all teams to expose their data and
    functionality through APIs, ensuring no direct access to data stores or
    shared memory. This approach facilitated scalability and externalization,
    contributing significantly to AWS's success.

<center>

# 27 / 33: Infrastructure-as-Code

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides027.png){width=80%}

</center>
* **Infrastructure-as-Code**
  - The idea here is to manage and provision IT infrastructure using code, just like you would with software applications. This means you can use a *high-level programming language* to automate the setup and management of servers, networks, and other infrastructure components. This approach makes infrastructure management more efficient and less error-prone.

- **Apply software development principles to infrastructure**
  - By treating infrastructure as code, you can store it in a _code repository_,
    just like application code. This allows for version control and
    collaboration.
  - You can also run _automated tests_ to ensure that changes to the
    infrastructure code don't break anything.
  - _Continuous integration_ means that changes to the infrastructure code are
    automatically tested and integrated, ensuring that the infrastructure is
    always in a deployable state.

- **DevOps (SRE in Google parlance)**
  - DevOps is about bringing together developers and operations teams to work
    more closely. This collaboration helps in building and maintaining systems
    that are both reliable and scalable.
  - By using software tools and practices, DevOps aims to bridge the gap between
    development and operations, making the process more seamless.
  - An important aspect is role-switching, where developers take on operational
    tasks like being on-call, and operations staff get involved in development.
    This helps each team understand the other's challenges and fosters better
    _communication and collaboration_.

<center>

# 28 / 33: Infrastructure-as-Code: Advantages

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides028.png){width=80%}

</center>
- **Save time**
  - *Reuse scripts or blueprints*: By using pre-written scripts, you can quickly set up infrastructure without starting from scratch each time.
  - *Automate tasks*: Automation reduces manual intervention, speeding up processes and reducing human error.
  - *Copy-paste vs. click-click-click*: Using code to manage infrastructure is faster and more efficient than manually configuring settings through a user interface.

- **Fewer mistakes**
  - _Push-button flow_: Automating deployments with scripts minimizes the chance
    of human error, as the same process is repeated consistently.

- **Consistency of actions**
  - _Multiple deployments per day_: Infrastructure-as-Code (IaC) allows for
    frequent and reliable deployments, ensuring that environments remain
    consistent.

- **Deployment pipeline**
  - _Commit changes to source code_: Changes are tracked and managed through
    version control, ensuring transparency and traceability.
  - _Build application from source_: Automates the building process, ensuring
    that the latest code is always used.
  - _Automatic tests (e.g., integration tests)_: Tests are run automatically to
    catch issues early in the deployment process.
  - _Build testing environment_: Creates a separate environment for testing,
    ensuring that tests do not affect production.
  - _Run acceptance tests in isolation_: Ensures that new changes meet
    requirements before going live.
  - _Propagate changes to production_: Once tests pass, changes are
    automatically deployed to production, reducing downtime.

- **Scripts as detailed documentation**
  - _Explains what and how, not why_: Scripts serve as a record of what actions
    are taken and how they are executed, providing clear documentation of the
    infrastructure setup.

<center>

# 29 / 33: AWS Command Line Interface (CLI)

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides029.png){width=80%}

</center>
- **AWS Command Line Interface (CLI)**
  - The AWS CLI is a tool that allows you to interact with AWS services using commands in your command-line shell. This is useful for automating tasks and managing AWS resources without needing to use the AWS Management Console.
  - **Provides a *unified interface* to all AWS services**
    - This means you can use the same tool to manage different AWS services, making it easier to automate workflows and integrate AWS into your existing processes.
    - The output from AWS CLI commands is typically in JSON format, which is a lightweight data-interchange format that's easy for both humans and machines to read and write.
    - To install the AWS CLI on a Linux system, you can use the command: `apt-get install awscli`. This command uses the package manager to download and install the AWS CLI tool.

- **Authenticate**
  - Before you can use the AWS CLI, you need to authenticate it with your AWS
    account credentials. This is done using the `aws configure` command.
  - **AWS access key ID**
    - This is a unique identifier associated with your AWS account. It acts like
      a username for programmatic access.
  - **AWS secret access key**
    - This is a secret key that acts like a password. It should be kept
      confidential to ensure the security of your AWS resources.
  - **Default region name**
    - AWS services are hosted in different regions around the world. By setting
      a default region, you specify where your commands will be executed unless
      you specify otherwise.

- **Execute command**
  - Once authenticated, you can execute commands using the AWS CLI. The general
    format is: `aws <service> <action> --key value`.
  - Here, `<service>` refers to the AWS service you want to interact with (e.g.,
    EC2, S3), and `<action>` is the specific operation you want to perform
    (e.g., start, stop, list).
  - The `--key value` part allows you to specify additional options or
    parameters for the command, tailoring it to your specific needs.

<center>

# 30 / 33: Software Development Kit (SDK)

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides030.png){width=80%}

</center>
- **SDK Overview**
  - An SDK, or Software Development Kit, is a collection of tools and libraries that allows developers to interact with AWS services using their preferred programming languages, such as Python, Go, C++, and JavaScript.
  - It simplifies the process of making API calls to AWS services, enabling developers to integrate AWS functionalities into their applications more easily.

- **Pros of Using SDKs**
  - **Authentication**: SDKs manage the authentication process, ensuring secure
    access to AWS services.
  - **Retry on Error**: They automatically handle retries in case of errors,
    improving the reliability of applications.
  - **HTTPS Communication**: SDKs ensure secure data transmission over HTTPS.
  - **XML/JSON De-/Serialization**: They handle the conversion of data formats,
    making it easier to work with AWS services that use XML or JSON.

- **Cons of Using SDKs**
  - **Imperative Approach**: SDKs often require an imperative programming style,
    which may not be as intuitive for some developers.
  - **Dealing with Dependencies**: Managing dependencies can be challenging,
    especially when integrating multiple AWS services.

- **Code Example Explanation**
  - The code snippet demonstrates how to use the Boto3 SDK in Python to interact
    with AWS DynamoDB.
  - It shows how to create a DynamoDB table named 'users' with specific key
    schemas and attribute definitions.
  - The code waits for the table to be created and then prints the item count,
    illustrating basic operations with DynamoDB using the SDK.

<center>

# 31 / 33: AWS CloudFormation

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides031.png){width=80%}

</center>
* **AWS CloudFormation**
  - *Use templates to describe infrastructure*
    - AWS CloudFormation allows you to define your cloud resources using templates. These templates can be written in JSON or YAML, which are both human-readable formats. This means you can easily describe what your infrastructure should look like without manually setting up each component.

- _Declarative vs imperative approach_
  - With CloudFormation, you use a declarative approach. This means you specify
    what the final system should look like, rather than detailing each step to
    build it. It's like saying "I want a house with three bedrooms" instead of
    "first lay the foundation, then build the walls."

- _AWS Stacks processes CloudFormation templates_
  - When you create a CloudFormation template, AWS uses something called a
    "Stack" to process and manage the resources defined in your template. This
    helps automate the setup and management of your infrastructure.

- **Pros**
  - **Consistent infrastructure description**
    - Using templates ensures that your infrastructure is described consistently
      every time you deploy it, reducing errors.
  - **Handles dependencies**
    - CloudFormation automatically manages dependencies between resources, so
      you don't have to worry about the order of creation.
  - **Customizable**
    - You can inject parameters into your templates to customize them for
      different environments or use cases.
  - **Testable**
    - You can create infrastructure from a template, test it, and then shut it
      down, which is great for development and testing purposes.
  - **Updatable**
    - If you need to make changes, you can update the template, and the Stack
      will apply those changes automatically.
  - **Serves as documentation**
    - Since templates are written as code, they can be stored in source control
      systems, serving as documentation for your infrastructure.

<center>

# 32 / 33: Securing Your System

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides032.png){width=80%}

</center>
- **Always install software updates**
  - Keeping your software up-to-date is crucial because updates often include patches for security vulnerabilities. These vulnerabilities can be exploited by attackers, so prompt installation helps protect your system.

- **Restrict access to AWS account**
  - It's important to manage access to your AWS account carefully. By using
    separate accounts for individuals and scripts, you can better control who
    has access to what. The principle of "least privilege" means giving users
    only the permissions they need to perform their tasks, reducing the risk of
    accidental or malicious actions.

- **Restrict network traffic**
  - Limiting network traffic to only essential ports, such as 80 for HTTP and
    443 for HTTPS, helps minimize exposure to potential attacks. Closing
    unnecessary ports and encrypting both traffic and data further enhances
    security by protecting information from being intercepted or tampered with.

- **Create a private network**
  - Setting up a private network involves using subnets that are not directly
    accessible from the Internet. This adds an extra layer of security by
    isolating sensitive resources, such as databases and internal servers, from
    external threats. The diagram illustrates a typical setup with a public
    subnet for internet-facing components and a private subnet for internal
    resources.

<center>

# 33 / 33: AWS Shared-responsibility Principle

</center>
<center>

![](data605/lectures_commentary/Lesson11.3-AWS_Overview.png/slides033.png){width=80%}

</center>
- **AWS Shared-responsibility Principle**
  - This principle is a key concept when using AWS services. It defines the division of security and compliance responsibilities between AWS and the customer. Understanding this division is crucial for maintaining a secure cloud environment.

- **AWS is responsible for**:
  - _Protecting the network by monitoring Internet access_: AWS ensures that the
    infrastructure is secure by monitoring and controlling access to its
    network.
  - _Preventing DDoS attacks_: AWS has measures in place to protect against
    Distributed Denial of Service attacks, which can overwhelm systems and cause
    downtime.
  - _Ensuring the physical security of data centers_: AWS takes care of the
    physical security of its data centers, ensuring that only authorized
    personnel have access.
  - _Decommissioning storage devices after end of life_: AWS securely handles
    the disposal of storage devices to prevent data leaks.

- **You are responsible for**:
  - _Restricting access using IAM_: You must manage who can access your AWS
    resources by setting up Identity and Access Management (IAM) policies.
  - _Encrypting network traffic (e.g., HTTPS)_: It's your job to ensure that
    data transmitted over the network is encrypted to protect it from
    interception.
  - _Configuring firewalls and VPNs_: You need to set up firewalls and Virtual
    Private Networks (VPNs) to control and secure traffic to and from your AWS
    resources.
  - _Encrypting data_: You should encrypt your data both at rest and in transit
    to safeguard it from unauthorized access.
  - _Updating the OS and software_: Keeping your operating systems and
    applications up to date is your responsibility to protect against
    vulnerabilities.
