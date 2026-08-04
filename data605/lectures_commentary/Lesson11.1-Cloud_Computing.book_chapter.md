---
title: "11.1: Cloud Computing"
---

<!-- git_hash=4f246573-d1k timestamp=20260804_171346 -->

<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides001.png){width=80%}

</center>
<center>

# 2 / 10: Cloud Computing

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides002.png){width=80%}

</center>
- **Computing as "service" instead of "product"**
  - *Storage and computing in the cloud*: This means that instead of owning physical hardware, users can access storage and computing power over the internet. This is flexible and can be scaled up or down based on needs.
  - *Edge devices (e.g., phones, laptops, tablets) interact with the cloud*: These devices connect to cloud services to perform tasks, reducing the need for powerful hardware on the device itself.

- **Advantages of cloud computing**
  - _Device agnostic_: Users can access cloud services from any device, ensuring
    a seamless experience across different platforms.
  - _On demand_: Resources can be accessed whenever needed, providing
    flexibility and convenience.
  - _Efficiency / scalability_: Cloud platforms use frameworks like Hadoop,
    Spark, and Dask to handle large-scale data processing efficiently, allowing
    businesses to grow without worrying about infrastructure limits.
  - _Reliability_: Cloud services often have high uptime and data redundancy,
    ensuring consistent availability.
  - _Cost: "pay-as-you-go" for resources_: Users only pay for what they use,
    making it more economical than maintaining personal hardware. This model
    treats computing resources like utilities such as electricity.

<center>

# 3 / 10: Buying Infrastructure

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides003.png){width=80%}

</center>
* **Buying Infrastructure**
  - *To buy or to rent* computers and infrastructure?
    - When deciding whether to buy or rent infrastructure, there's a balance between time and money. Buying might save money in the long run but requires a lot of upfront investment. Renting can be more expensive over time but is easier to start with.
    - It's tough to make this decision because it involves predicting future needs and costs, which can be uncertain.

- **Buying / building infrastructure**
  - This involves significant time and capital investments, known as Capex. This
    is especially challenging at the start when there might not be any revenue
    to support these costs.
    - A steady cash flow, where you pay a consistent amount each month, is often
      preferable to a large, one-time expense that can disrupt finances.
  - When you buy hardware like computers, storage, and network equipment, you
    need to estimate how much you need now. However, predicting future needs can
    be tricky, as technology and business demands change.
  - Hardware becomes outdated, so you'll need to plan for updates and
    replacements.
  - Owning hardware comes with ongoing operational expenses (Opex), such as
    costs for data centers, electricity, cooling, and fixing any issues that
    arise.
  - Managing the infrastructure also requires effort. This includes installing,
    updating, and maintaining the software that runs on your hardware.

<center>

# 4 / 10: Renting Infrastructure

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides004.png){width=80%}

</center>
* **Renting Infrastructure**
  - *Renting infrastructure* refers to using cloud computing services instead of owning physical hardware. This means you can access computing resources over the internet.
  - **Pay for what you use**
    - This model allows you to pay only for the resources you consume, similar to how you pay for utilities like electricity or water. This is beneficial because it reduces the need for a large upfront investment in hardware.
  - **Low initial capital investment**
    - Since you don't need to buy expensive servers or other hardware, you can start projects with minimal financial risk. This is especially useful for startups or small businesses that may not have a lot of capital.
  - **Ready systems with a click**
    - Cloud services provide pre-configured systems that you can deploy quickly. This means you can have a server up and running in minutes, which speeds up development and deployment times.
  - **No multi-year resource plan needed**
    - You don't have to predict your resource needs years in advance. Instead, you can scale your resources up or down based on current demand, making it easier to adapt to changing business needs.
  - **Choose machines based on your application and data needs**
    - Cloud providers offer a variety of machine types optimized for different tasks. You can select the best fit for your specific application, whether you need more processing power, memory, or storage. This flexibility ensures you get the most efficient performance for your workload.

<center>

# 5 / 10: Cloud Computing

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides005.png){width=80%}

</center>
- **Ideas of cloud computing around for a long time**
  - *Mainframes + thin clients (1960s)*: Early computing involved centralized mainframes accessed by simple terminals, laying the groundwork for cloud concepts.
  - *Personal computers (1980s)*: The rise of PCs shifted computing power to individual users but still relied on networked resources.
  - *Grid computing for supercomputers (1990s)*: This era saw the use of distributed computing resources to solve large-scale problems, similar to cloud resource pooling.
  - *Peer-to-peer architecture (early 2000s)*: Enabled decentralized resource sharing, influencing cloud's distributed nature.
  - *Client-server model (Web 1.0 and Web 2.0)*: These models introduced web-based applications, a precursor to cloud services.
  - *Cloud computing (2010s)*: Finally, the cloud became a mainstream solution, offering scalable and flexible computing resources.

- **Now, it finally works**
  - Cloud computing has matured, becoming reliable and efficient for various
    applications.

- **Why now?**
  - _A convergence of key technologies_:
    - **OS virtualization**: Allows multiple virtual machines on a single
      physical server, optimizing resource use.
    - **Large data centers**: Provide the infrastructure needed for cloud
      services, offering vast storage and processing power.
    - **Decreasing hardware costs**: Makes it economically feasible to deploy
      large-scale cloud solutions.
    - **Big data frameworks**: Enable the processing and analysis of massive
      datasets, a key cloud application.

<center>

# 6 / 10: Infrastructure-as-a-Service (IaaS)

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides006.png){width=80%}

</center>
- **Infrastructure-as-a-Service (IaaS)**
  - IaaS provides foundational cloud services, offering essential resources like virtual machines, storage, and networking. Users have control over these resources, allowing them to install and maintain their own operating systems and applications. This setup gives users significant flexibility and control over their computing environment.

- **Examples**
  - _AWS EC2_: Amazon's Elastic Compute Cloud offers scalable computing
    capacity.
  - _Google Compute Engine_: Provides virtual machines running in Google’s data
    centers.
  - _Microsoft Azure Virtual Machines_: Offers on-demand, scalable computing
    resources.
  - _IBM Cloud Infrastructure_: Provides a range of cloud computing services.

- **Benefits**
  - _Flexibility_: Users can manage resources according to their needs.
  - _Scalability_: Easily adjust resources to meet changing demands.
  - _Cost-effective_: Pay only for the resources you use, reducing waste.

- **Use Cases**
  - _Hosting websites and applications_: Ideal for businesses needing reliable
    hosting.
  - _Data analysis and processing_: Supports large-scale data operations.
  - _Development and testing environments_: Provides a flexible space for
    developers to test applications.

<center>

# 7 / 10: Platform-as-a-Service

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides007.png){width=80%}

</center>
- **Problem: Assembling your own software stack requires work**
  - *Install*: Setting up each component of a software stack can be time-consuming and complex.
  - *Configure*: Ensuring that all components work together smoothly often involves intricate configuration.
  - *Manage dependencies*: Handling incompatible versions of software can lead to significant challenges.

- **Solution: Get a pre-built software stack**
  - _Software stack as a virtualization solution_: Tools like VMware or Docker
    provide a ready-to-use environment.
    - _Pre-installed OS_: Operating systems are already set up, saving time and
      effort.
    - _Libraries_: Necessary libraries are included, reducing compatibility
      issues.
    - _Application software_: Applications are pre-installed, allowing for
      immediate use.

- **Business model built around this**
  - Examples include:
    - _Google App Engine_: Offers a platform for building and hosting
      applications.
    - _Managed Hadoop_: Provides a ready-to-use Hadoop environment.
  - Pre-built images for Hadoop:
    - _Hortonworks, Cloudera_: These offer Hadoop distributions with everything
      set up.
  - Pre-built distributions for Linux:
    - _RedHat, Gentoo, CentOS_: These distributions come with pre-configured
      software stacks.

The diagram illustrates the components of Platform-as-a-Service (PaaS),
highlighting integration, middleware, APIs, and core connectivity, which
abstract the complexities of hardware and facilities.

<center>

# 8 / 10: Software-as-a-Service (SaaS)

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides008.png){width=80%}

</center>
- **Software-as-a-Service (SaaS)**
  - *Cloud provides the application*
    - SaaS applications are hosted in the cloud, meaning you don't need to install them on your local machine. This allows you to access them directly via the internet.
    - Examples include:
      - _Dropbox_: This service lets you store and share files online, eliminating the need for local storage.
      - _Salesforce_: A platform for managing customer relationships, accessible entirely online.
      - Browser-based apps like Google Docs or Microsoft 365, which allow you to create and edit documents directly in your web browser.

- **Benefits**
  - Accessibility: You can use SaaS applications from any device with an
    internet connection, providing great flexibility.
  - Automatic updates: The service provider handles updates and maintenance,
    ensuring you always have the latest features without manual intervention.
  - Scalability: SaaS can easily accommodate growing user needs, making it
    suitable for businesses of all sizes.
  - Cost-effectiveness: By reducing the need for physical hardware and software
    installations, SaaS can lower operational costs.

The accompanying diagram illustrates the layered architecture of SaaS, showing
how different components like presentation, APIs, and data interact within the
cloud infrastructure.

<center>

# 9 / 10: X-as-a-Service

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides009.png){width=80%}

</center>
* **X-as-a-Service**
  - **After 2010, business model of *X-as-a-Service (XaaS)*:**
    - **Mobility-as-a-Service (e.g., Uber):** This model allows users to access transportation services via an app, providing convenience and flexibility without owning a vehicle. Uber is a prime example, offering rides on demand.
    - **Gaming-as-a-Service (e.g., Google Stadia):** This service lets users play video games over the internet without needing a gaming console or high-end PC. Google Stadia streams games directly to devices, making gaming more accessible.
    - **Storage-as-a-Service (e.g., S3, Google Drive):** This model provides cloud storage solutions, allowing users to store and access data online. Services like Amazon S3 and Google Drive offer scalable storage options for both individuals and businesses.
    - **Desktop-as-a-Service (e.g., AWS AppStream):** This service delivers virtual desktops to users over the internet, enabling access to a desktop environment from any device. AWS AppStream is an example that supports remote work and flexibility.
    - **Marketing-as-a-Service:** This model offers marketing solutions and strategies as a service, helping businesses reach their target audience without needing an in-house marketing team.
    - **Banking-as-a-Service:** This service provides banking infrastructure and capabilities to businesses, allowing them to offer financial services without being a traditional bank.
    - **..:** The "X" in XaaS can represent virtually any service, highlighting the flexibility and broad applicability of this business model across various industries.

<center>

# 10 / 10: Cloud Deployment Models

</center>
<center>

![](data605/lectures_commentary/Lesson11.1-Cloud_Computing.png/slides010.png){width=80%}

</center>
- **Private Cloud**
  - *Internal cloud hosted on organizational premises*: This means the cloud infrastructure is located within the organization itself, providing more control over data and security.
  - *Example*: A company's data center that runs virtualized services, allowing for customized solutions tailored to specific business needs.

- **Public Cloud**
  - _External cloud hosted by third-party providers_: These are managed by
    external companies, offering services over the internet.
  - _Example_: Providers like AWS, Azure, and GCP offer scalable compute and
    storage solutions, making them accessible and cost-effective for businesses.

- **Hybrid Cloud**
  - _Combines private and public environments_: This model leverages the
    benefits of both private and public clouds to optimize costs, enhance
    security, and improve scalability.
  - _Sensitive workloads stay internal_: Critical data and applications remain
    within the private cloud for security.
  - _Scalable tasks move to the public cloud_: Non-sensitive tasks can be
    shifted to the public cloud to take advantage of its scalability.

- **On-premises Resources**
  - _Example_: Corporate servers located within a company’s building, providing
    direct control over hardware and data.

- **Off-premises Resources**
  - _Example_: Cloud provider's distributed data centers, which offer
    flexibility and scalability without the need for physical infrastructure
    management.
