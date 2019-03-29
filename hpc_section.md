:o: Do not review yet, its not yet in .md format


# X High Performance Computing in the Cloud
## X.0 Definition (from [[1]](https://searchdatacenter.techtarget.com/definition/high-performance-computing-HPC) and [[2]](https://www.techopedia.com/definition/4595/high-performance-computing-hpc))
The use of computers to solve complex problems or to run advanced application programs efficiently, reliably, and quickly, typically through parallel processing techniques.[1] Formally, these calculations are performed with at least a performance of one teraflop and can span activities such as computer modeling, simulation, and analysis.[2](https://www.techopedia.com/definition/4595/high-performance-computing-hpc)

## X.1 Introduction
Demand for High Performance Computing (HPC) resources has been rapidly increasing in recent years. HPC provides a means for large discoveries in both science and engineering. For example, data analytics for finance and the healthcare community, computational modelling of proteins, the simulation of large biological systems, weather simulations, as well as other applications in design and engineering.

Other applications of HPC include: (from [[2]](https://www.techopedia.com/definition/4595/high-performance-computing-hpc) and [[3]](https://aws.amazon.com/hpc/)):
* Research labs
  * Life sciences
  * Energy and earth sciences
* Oil and gas industry modeling
* Design and engineering
  * Electronics design automation
  * 3D rendering
* Climate modeling
* Media and entertainment

## X.2 Structure
Many of these problems require an enormous amount of computing power to solve and typical commercial desktop or laptops fall short. High performance computers can provide the large amount of processors, memory, and disk space required for these applications. Two main barriers lie between the user and these high performance machines—cost and ease of usage. Firstly, the cost of computing power required for HPC is too large for personal use.

Figure 1. Structure of a HPC system (from [[4]](https://www.netapp.com/us/info/what-is-high-performance-computing.aspx))

Typically, a cluster of many computers can be constructed (See Figure 1), however set up, interfacing between many computers (or nodes), and storing the data can be difficult and require expertise in computer architecture and parallel computing. Alternatively, HPC can be treated as a service from a cloud provider. HPC in the cloud provides solutions to both of these problems. These services require the user to pay only for computing power and provide built in functions and features for ease of use. On-premise HPC resources introduce expenses for keeping the system running (even when not directly running computations) along with other maintenance fees, costly contracts, and licensing agreements. Cloud-based HPC services removes the overhead cost as many offer an “only pay for what you use” policy,[[3]](https://aws.amazon.com/hpc/) charging by time and size of the computing power.

Cloud providers (such as Amazon) allow for the HPC computations, storage of data, analysis, and visualization to be performed remotely (See Figure 2). This service circumvents the need to have computing clusters on-premises (for most applications) and allows the access to HPC from command lines and browsers on electronic devices.

Figure 2. Structure of AWS (Amazon) HPC infrastructure (from [[5]](https://d1.awsstatic.com/HPC2019/18-AWS-001%20HCLS%20Infographic_final.pdf))

Additionally, the major commercial providers for cloud-based HPC such as AWS (Amazon), Azure (Microsoft), and Google have a vast amount of research and development going into their services, allowing any user to benefit from the implementation of features, such as PaaS, parallel computing, artificial intelligence (AI), and machine learning, without the need for each user to develop it themselves. Thus, a large push to the use of cloud-based HPC services will allow more users to solve more problems remotely in a quicker, more cost-effective manner.

## X.2.1 References and Resources
[1] https://searchdatacenter.techtarget.com/definition/high-performance-computing-HPC
[2] https://www.techopedia.com/definition/4595/high-performance-computing-hpc
[3] https://aws.amazon.com/hpc/
[4] https://www.netapp.com/us/info/what-is-high-performance-computing.aspx
[5] https://d1.awsstatic.com/HPC2019/18-AWS-001%20HCLS%20Infographic_final.pdf
[6] https://insidehpc.com/

## X.3 Features
Cloud-based HPC providers including AWS[[1]](https://aws.amazon.com/hpc/), Azure[[2]](https://azure.microsoft.com/en-us/solutions/big-compute/), and Google[[3]](https://cloud.google.com/solutions/hpc/) all have many features which can in their respective sections or in the resources below. (link to other sections)

## X.3.1 Comparison with IU Supercomputing facilities
AWS features 8 different instances for high performance computing (from [[1]](https://aws.amazon.com/hpc/)):
* Compute Optimizes (C5n): 36 cores, 192 GB memory
* General Purpose (M5): 48 cores, 384 GB memory
* Memory Optimizes (R5): 48 cores, 768 GB memory
* Accelerated Computing (P3): 8 accelerators (GPU)
* Accelerated Computing (F1): 8 FPGA devices
* Accelerated Computing (G3): 4 accelerators (GPU)
* Memory Optimizes (X1): 64 cores, 1.95 TB memory
* Memory Optimized (X1e): 64 cores, 3.84 TB memory

AWS also provides long and short term cloud storage for data, including Amazon S3 and Amazon Glacier.
Indiana University (IU) has 3 main systems for HPC: Big Red II, Carbonate, and Karst, all of which can be accessed by students at IU. Each is managed by the university and has available software packages already preinstalled. These HPC systems work with a queue, where users may have to wait a long period of time for their job to be submitted if there are other users occupying the nodes.

Big Red II has two types of computer nodes:
* XE6 (CPU): 32 cores, 64 GB memory
* XE7 (GPU-accelerated): 16 core, 32 GB memory

Carbonate is comprised of 72 computer nodes with 256GB of RAM and 8 larger nodes with 512GB of RAM.
Karst has two types of nodes: compute nodes with 32 GB and data nodes with 64 GB. Theses nodes can handle “large amounts of processing capacity over long periods of time”[4] as well as “high throughput and data-intensive parallel computing jobs.” [[4]](https://kb.iu.edu/d/alde)
AWS has a much larger selection of nodes to choose from, with larger amount of memory and storage than IU supercomputers. Also, due to their large selection, the queue time will be much less for AWS.

## X.3.2 Resources
[1] https://aws.amazon.com/hpc/
[2] https://azure.microsoft.com/en-us/solutions/big-compute/
[3] https://cloud.google.com/solutions/hpc/
[4] https://kb.iu.edu/d/alde
