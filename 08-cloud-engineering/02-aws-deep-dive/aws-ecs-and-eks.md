# AWS ECS & EKS (Containers)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Bước tiến hóa tiếp theo từ EC2. Khám phá cách chạy Docker Containers trên quy mô lớn với Amazon ECS (đơn giản, chuẩn AWS) và Amazon EKS (Kubernetes tiêu chuẩn ngành). Tìm hiểu chế độ Fargate không cần quản lý máy chủ.

</details>

> **Summary**: The evolutionary step up from EC2. Explore how to run Docker Containers at massive scale using Amazon ECS (AWS native, simple) and Amazon EKS (industry-standard Kubernetes). Learn about Fargate serverless compute for containers.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Docker Container**: Thay vì mua một chiếc xe tải lớn (EC2) để chở 1 loại hàng, bạn đóng gói hàng vào các thùng Container tiêu chuẩn. Bạn có thể chở hàng trăm thùng Container trên cùng một chiếc xe tải. Nó giúp tiết kiệm không gian và dễ dàng bốc dỡ.
- **ECS / EKS**: Là "Cần cẩu và Người điều phối cảng". Nếu bạn có 50 chiếc xe tải và 5,000 thùng container, bạn không thể dùng sức người để bê từng thùng lên xe được. ECS/EKS sẽ tự động tính toán xem xe nào còn chỗ trống để xếp thùng container lên, tự khởi động lại thùng nếu nó bị vỡ, và tự động gọi thêm xe tải nếu hàng về quá nhiều.
- **Fargate**: Là "Cảng tự động 100%". Bạn không thèm thuê xe tải (EC2) nữa. Bạn chỉ mang thùng Container đến, Fargate sẽ tự tìm cách chở đi và tính tiền dựa trên cân nặng của thùng. Bạn không bao giờ phải thấy chiếc xe tải nào cả!

</details>

- **Docker Container**: Instead of buying a massive truck (EC2) to haul one type of cargo, you pack your cargo into standard shipping containers. You can stack hundreds of containers onto the same truck, saving space and isolating the cargo.
- **ECS / EKS (Container Orchestration)**: The "Port Crane and Manager". If you have 50 trucks and 5,000 containers, a human cannot manually decide which container goes on which truck. ECS/EKS automatically calculates which truck has empty space, places the container there, restarts it if it crashes, and summons more trucks (Auto Scaling) if there are too many containers.
- **Fargate**: The "100% Automated Port". You stop buying and managing trucks (EC2 instances) entirely. You just hand your Container to Fargate, and they magically transport it, charging you based on the container's exact weight and dimensions. You never see or manage the underlying truck!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Container Orchestration** là việc quản lý tự động vòng đời của các Docker Containers (khởi động, nhân bản, load balancing, tắt đi).
- **Amazon ECS (Elastic Container Service)**: Dịch vụ điều phối container độc quyền của AWS. Nó cực kỳ đơn giản, tích hợp chặt chẽ với IAM, ALB và CloudWatch. Dễ học, dễ dùng.
- **Amazon EKS (Elastic Kubernetes Service)**: Kubernetes (K8s) dạng Managed. Kubernetes là tiêu chuẩn mã nguồn mở của toàn ngành IT. Nó phức tạp hơn ECS rất nhiều nhưng cực kỳ mạnh mẽ và không bị trói buộc vào AWS (Vendor Lock-in).

**Launch Types (Chế độ chạy):**
Bạn có thể chạy ECS/EKS trên 2 loại hạ tầng:
1. **EC2 Launch Type**: Bạn tự quản lý các máy chủ EC2 (Data Plane). ECS chỉ đóng vai trò bộ não (Control Plane) xếp container lên EC2 của bạn. Bạn phải tự vá lỗi hệ điều hành EC2.
2. **Fargate Launch Type (Serverless)**: Bạn không quản lý EC2 nào cả. Bạn chỉ cung cấp file Docker, AWS tự lo phần cứng bên dưới.

</details>

**Container Orchestration** is the automated lifecycle management of Docker Containers (scheduling, scaling, load balancing, terminating).
- **Amazon ECS (Elastic Container Service)**: AWS's proprietary container orchestration engine. It is highly opinionated, extremely simple to learn, and integrates flawlessly with AWS IAM, ALBs, and CloudWatch.
- **Amazon EKS (Elastic Kubernetes Service)**: Managed Kubernetes (K8s). Kubernetes is the open-source industry standard. It has a brutally steep learning curve but is incredibly extensible and avoids Vendor Lock-in.

**Launch Types (The Infrastructure underlying the containers):**
You can run ECS/EKS on two types of infrastructure (Data Plane):
1. **EC2 Launch Type**: You manage the raw EC2 servers. ECS just acts as the brain (Control Plane) telling your EC2s which containers to run. You must patch the OS of the EC2s.
2. **Fargate Launch Type (Serverless)**: You manage ZERO servers. You give AWS your Docker image and say "I need 2 CPUs and 4GB RAM". AWS provisions invisible hardware instantly.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Quản lý một ứng dụng nguyên khối (Monolith) trên một vài máy chủ EC2 thì dễ. Nhưng khi chuyển sang kiến trúc **Microservices** (hàng chục dịch vụ nhỏ nhắn giao tiếp với nhau), quản lý EC2 thủ công là ác mộng.
Mỗi service cần thư viện (dependencies) khác nhau, chạy port khác nhau. Docker giải quyết bài toán đóng gói. Nhưng khi bạn có 500 containers, ai sẽ khởi động chúng? Ai sẽ kiểm tra sức khỏe của chúng? 

Đó là lý do ECS và Kubernetes (EKS) ra đời. Chúng giải quyết bài toán vận hành Microservices ở quy mô hàng ngàn container, đảm bảo tính sẵn sàng cao (High Availability) mà con người không thể tự làm bằng tay.

</details>

Managing a Monolithic application on a few EC2 instances is easy. But when the industry shifted to **Microservices** (dozens of small, decoupled services communicating via APIs), managing manual EC2s became an absolute nightmare.
Every microservice needs different dependencies, Node.js versions, and ports. Docker solved the packaging problem. But when you have 500 containers, who starts them? Who monitors if one crashes? Who maps their network ports dynamically?

That is why Container Orchestration (ECS/K8s) exists. They solve the operational complexity of Microservices at scale, providing Service Discovery, Auto Healing, and Zero-Downtime deployments out of the box.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Nên chọn ECS hay EKS?**
- **Chọn ECS**: Nếu bạn là công ty nhỏ/vừa, team không có chuyên gia DevOps K8s cứng cựa, và bạn cam kết dùng hệ sinh thái AWS lâu dài. Setup ECS chỉ mất 1 ngày.
- **Chọn EKS (Kubernetes)**: Nếu bạn có đội ngũ lớn, cần dùng các công cụ mã nguồn mở phức tạp (Istio, Prometheus, ArgoCD), hoặc bạn bắt buộc phải thiết kế hệ thống Multi-Cloud (chạy được trên cả AWS và On-Premise). Setup và bảo trì EKS tốn rất nhiều thời gian.

</details>

### ECS vs EKS Decision Matrix

| Feature | Amazon ECS | Amazon EKS (Kubernetes) |
|---|---|---|
| **Learning Curve** | Low (AWS native logic) | Very High (Steep K8s concepts) |
| **Control Plane Cost** | Free ($0) | ~$73/month per Cluster |
| **Vendor Lock-in** | High (Tied to AWS API) | Low (K8s YAML works anywhere) |
| **Ecosystem** | Standard AWS tools (CloudWatch) | Massive Open Source ecosystem (Helm) |
| **Best For** | Fast moving startups, small teams | Enterprise multi-cloud, complex microservices |

### EC2 vs Fargate Launch Type
- **EC2**: Cheaper per minute. Good if you have highly predictable traffic or need GPU instances. You must manage OS patching.
- **Fargate**: Slightly more expensive per minute, but often cheaper overall because you don't pay for idle EC2 capacity. **Zero OS maintenance**. Highly recommended for 90% of workloads.

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **ECS Fargate cho Web App (Chuẩn Vàng)**: Triển khai backend Node.js hoặc Python API lên ECS Fargate. Đây là cách hiện đại, an toàn và nhàn hạ nhất để host web trên AWS hiện nay.
2. **EKS cho Hệ sinh thái Mã nguồn mở**: Công ty bạn muốn dùng Apache Spark on K8s, Kubeflow cho Machine Learning, và ArgoCD cho GitOps. Những công cụ phức tạp này chỉ chạy tốt trên chuẩn Kubernetes.
3. **Batch Processing (Xử lý hàng loạt)**: Dùng ECS Scheduled Tasks (như Cronjob) để bật một Fargate Container lên lúc 2h sáng, nén video trong 10 phút, rồi tắt đi. Trả tiền đúng 10 phút.

**Không nên làm (Anti-patterns):**
- **Lưu Database trên ECS/EKS**: Đừng bao giờ chạy Database (MySQL, PostgreSQL) bên trong Docker Container trên production. State (Dữ liệu tĩnh) rất khó quản lý trong Container Orchestration. Container sinh ra để chạy Stateless (Không lưu trạng thái). Luôn dùng dịch vụ PaaS như RDS cho Database.

</details>

1. **The Modern Web App Standard (ECS Fargate)**: Deploying your Node.js, Python, or Go APIs as Docker containers onto ECS Fargate behind an Application Load Balancer. This is arguably the most stress-free, scalable, and secure way to host APIs on AWS today.
2. **EKS for the Cloud-Native Ecosystem**: Your company wants to leverage advanced open-source tooling like Kubeflow (for ML), Istio (Service Mesh), and ArgoCD (GitOps). These tools strictly require the standard Kubernetes API. EKS is mandatory here.
3. **Batch Processing (ECS Tasks)**: Using ECS Scheduled Tasks (like a cron job) to spin up a heavy Fargate container at 2 AM, process 10,000 images in 15 minutes, and terminate. You pay for exactly 15 minutes of compute.

### Anti-Patterns
- **Running Databases inside Containers (ECS/EKS)**: Running stateful workloads like MySQL or PostgreSQL inside Kubernetes/ECS in Production is a notorious anti-pattern for 99% of teams. Containers are ephemeral; they crash and move around. Managing persistent storage volumes across AZs for K8s pods is brutally hard. **Rule of thumb: Containers are for Stateless compute. Use Amazon RDS for Stateful databases.**

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. IAM Task Role vs Task Execution Role (Rất hay nhầm lẫn)**
Trong ECS, có 2 loại Role khiến người mới "phát điên":
- **Task Execution Role**: Là quyền cấp cho CÁI MÁY CHỦ ECS (hoặc Fargate agent) để nó có quyền KÉO image từ ECR (Docker Hub của AWS) và ĐẨY log lên CloudWatch.
- **Task Role**: Là quyền cấp cho ĐOẠN CODE APPLICATION của bạn (bên trong container). Nếu code Python của bạn cần gọi S3 hay DynamoDB, bạn phải cấp quyền vào Task Role!

**2. VPC Networking (Fargate)**
Khi chạy Fargate, AWS cấp cho mỗi Container (Task) một card mạng ảo (ENI) và một địa chỉ IP nội bộ đàng hoàng y như một máy chủ EC2 thật sự (chế độ `awsvpc`). Điều này nghĩa là bạn có thể gắn Security Group trực tiếp cho từng Container để bảo vệ nó, chứ không phải gắn chung cho cả cái máy chủ to.

</details>

### 1. ECS IAM Roles (The Classic Confusion)
ECS requires two distinctly different IAM Roles. Mixing them up guarantees your deployment will fail.
- **Task Execution Role**: Think of this as the "Agent's permissions". ECS needs this role to *pull the Docker Image* from ECR (Elastic Container Registry) and *push logs* to CloudWatch. The application inside never uses this role.
- **Task Role**: Think of this as the "Application's permissions". If your Node.js code inside the container needs to read an S3 bucket or query DynamoDB, those permissions MUST be placed in the Task Role.

### 2. Deep Networking (`awsvpc` mode)
In traditional Docker, containers share the host's IP address and rely on complicated port mapping (e.g., Host Port 32001 maps to Container Port 80).
In ECS Fargate (using `awsvpc` network mode), every single Container (Task) is injected with its own dedicated Elastic Network Interface (ENI) and its own private IP address directly from the VPC subnet. 
*Why does this matter?* Because you can now attach an AWS Security Group **directly to the container**. You can write a firewall rule that says: "This specific backend container only accepts traffic from the Load Balancer." Maximum security isolation!

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là file `task-definition.json` - bản thiết kế (Blueprint) của ECS. Nó cho AWS biết cần kéo Docker image nào, cấp bao nhiêu CPU/RAM, chạy port mấy, và cấp Task Role nào.

</details>

### ECS Task Definition (JSON)

The core blueprint of ECS is the Task Definition. It tells ECS exactly how to run your container.

```json
{
  "family": "my-backend-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256", 
  "memory": "512",
  "taskRoleArn": "arn:aws:iam::123456789012:role/MyApplicationTaskRole",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "node-backend-container",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-api:v1.0.3",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-backend-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

---

## Related Topics

- [AWS EC2](./aws-ec2.md) — The underlying compute power if you choose not to use Fargate.
- [AWS VPC](./aws-vpc.md) — Understanding `awsvpc` mode requires deep knowledge of Subnets and Security Groups.
- [DevOps CI/CD Pipelines](../../06-devops-engineering/README.md) — Automating the building of the Docker image, pushing to ECR, and forcing ECS to restart with the new image.
