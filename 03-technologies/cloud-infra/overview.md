# Cloud & Infrastructure Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước những năm 2010, muốn chạy một trang Web, các công ty phải chi hàng chục ngàn đô la mua những thùng Máy chủ sắt thép to tướng, cắm điện, kéo cáp mạng, ròng rã hàng tháng trời. Khi có quá đông khách hàng, máy chủ bốc khói, trang web sập, và bạn không thể mua máy chủ mới ngay trong 1 ngày. Kỷ nguyên **Điện toán Đám mây (Cloud Computing)** ra đời để tiêu diệt hoàn toàn khái niệm "Phần cứng vật lý" đó. AWS, Google Cloud, và Azure đã mua sẵn hàng triệu máy chủ khổng lồ đặt khắp thế giới. Giờ đây, thay vì mua máy sắt, bạn chỉ việc gõ vài dòng Code. Trong chớp mắt, một máy chủ ảo (Virtual Machine) được sinh ra bên Mỹ. Nếu trang web của bạn bị quá tải, bạn gõ thêm 1 dòng code, 100 máy chủ mới được nhân bản ngay trong 1 phút. Sự kỳ diệu này biến Hạ tầng Mạng (Infrastructure) thành Phần mềm (Code).

</details>

> **Summary**: Prior to the Cloud era, deploying an application required enormous Capital Expenditure (CapEx). Companies had to physically purchase bare-metal servers, rack them in data centers, configure HVAC cooling, and manually pull Ethernet cables. Scaling up required months of procurement delays. If traffic spiked unexpectedly, the application died. The advent of **Cloud Computing** (led fundamentally by AWS) abstracted away physical hardware into infinitely scalable, API-driven Virtual Resources. This shifted the industry to an Operational Expenditure (OpEx) model—you rent compute power by the second. Modern Infrastructure Engineering is now defined by Virtualization, Containerization (Docker), and Orchestration (Kubernetes). You no longer click buttons in a UI or plug in cables; you write **Infrastructure as Code (IaC)**, defining your entire global network topology in text files (Terraform) that can be version-controlled, audited, and deployed instantaneously.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn muốn mở một Tiệm Bánh.
1. **On-Premise (Máy chủ Cục bộ - Cách cũ)**: Bạn phải tự mua đất, tự xây nhà, tự xây lò nướng. Mất 1 năm mới xong. Nếu khách đông, bạn muốn mở rộng quán, bạn lại phải đập tường xây thêm, rất tốn kém và mất thời gian. Nếu ế khách, cái lò nướng khổng lồ của bạn nằm im lãng phí tiền.
2. **Cloud Computing (Đám mây - Cách mới)**: Bạn không xây gì cả. Có một Siêu Thị khổng lồ tên là AWS. Bạn bước vào và nói: *"Cho tôi thuê 1 cái bếp nhỏ trong 1 tiếng"*. 1 phút sau bạn có bếp. Đột nhiên có 10.000 khách đặt bánh? Bạn nói: *"Cho tôi thuê gấp 100 cái bếp ngay lập tức!"*. Bạn nướng xong, trả bếp, và chỉ trả đúng số tiền cho 1 giờ thuê. Cực kì nhanh, siêu tiết kiệm.

</details>

Imagine wanting to launch a Delivery Business.
1. **On-Premise (Bare-Metal Era)**: You must physically buy a fleet of 50 delivery trucks. You pay upfront. If your business fails, you are stuck with 50 useless trucks. If a massive holiday hits and you need 200 trucks, it takes 3 months to order and receive them. Your customers are angry.
2. **Cloud Computing (The Modern Era)**: You don't buy trucks. You use a massive rental agency (AWS/GCP). On a normal Tuesday, you click a button and rent 10 trucks by the minute. On Black Friday, your software detects a traffic spike, executes an API call, and instantly rents 500 trucks. The moment the holiday is over, it returns 490 trucks. You only pay for exactly what you used, down to the millisecond.

---

## Layer 1: The Three Pillars of Cloud (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thế giới Cloud được chia làm 3 tầng dịch vụ, từ thấp lên cao:
1. **IaaS (Hạ tầng như một Dịch vụ)**: Mức thấp nhất. Bạn thuê một "Cái máy tính trống không" (Ví dụ: AWS EC2). Họ cài sẵn hệ điều hành Linux cho bạn. Bạn có toàn quyền (Root) vào máy đó để tự cài Database, tự cài Node.js, tự sửa lỗi nếu sập. Rất tự do nhưng phải tự quản lý nhiều.
2. **PaaS (Nền tảng như một Dịch vụ)**: Bạn không thèm quan tâm hệ điều hành là gì. Bạn chỉ có 1 file code Node.js. Bạn vứt file code đó lên Heroku hoặc Vercel. Chúng sẽ TỰ ĐỘNG cài Node.js, tự chạy code, tự lấy đường dẫn web cho bạn. Bạn chỉ việc lo viết Code. Đổi lại, bạn bị giới hạn quyền và giá hơi đắt.
3. **SaaS (Phần mềm như một Dịch vụ)**: Mức cao nhất. Bạn không viết code, không mượn máy chủ. Bạn vào Gmail, Google Docs, hay Spotify để dùng luôn phần mềm người khác viết sẵn và đóng tiền hàng tháng.

</details>

Cloud providers classify their offerings into three distinct layers of abstraction (The "As-A-Service" pyramid):
1. **IaaS (Infrastructure as a Service)**: The lowest level of abstraction. The provider gives you raw virtual hardware (Virtual Machines, Storage Buckets, Virtual Networks). Examples: *AWS EC2, Google Compute Engine*. You have root SSH access. You are 100% responsible for patching the OS, installing runtimes (Node/Python), and managing security. Maximum flexibility, maximum operational burden.
2. **PaaS (Platform as a Service)**: The middle layer. The provider abstracts away the Operating System and network topology. You simply provide your application Source Code, and the platform automatically provisions the hidden VMs, installs dependencies, and serves the app. Examples: *Heroku, Vercel, AWS Elastic Beanstalk*. High developer velocity, but you lose low-level system control (Vendor Lock-in).
3. **SaaS (Software as a Service)**: The highest abstraction. You don't manage code or infrastructure. You simply consume a finished software product over the web, usually via subscription. Examples: *Gmail, Slack, Salesforce*.

---

## Layer 2: Why did it evolve into Containers? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dù có Cloud (Máy ảo), lập trình viên vẫn gặp một cơn ác mộng tồi tệ nhất: **"Nó chạy ngon trên máy tính của tôi, sao đem lên Cloud lại lỗi?"**
Lý do là máy của lập trình viên dùng Windows, cài Node.js bản 14. Máy ảo trên Cloud dùng Linux, vô tình cài Node.js bản 16. Môi trường khác nhau khiến Code bị lỗi.
Năm 2013, **Docker (Container)** ra đời và cứu rỗi toàn thế giới. Thay vì chỉ mang File Code lên Cloud. Docker gỡ luôn cả Hệ điều hành, thư viện, và Node.js bản 14 trên máy lập trình viên, nhét vào 1 cái "Thùng Container" (Image) đóng kín bưng lại. 
Sau đó ném nguyên cái Thùng đó lên Cloud. Vì bên trong cái thùng chứa sẵn môi trường y hệt máy Lập trình viên, nên Code CHẮC CHẮN 100% SẼ CHẠY ĐƯỢC ở bất kì đâu.

</details>

While Cloud VMs (IaaS) solved hardware provisioning, a massive software deployment problem remained: **The "It works on my machine" syndrome.**
A developer writes a Python app on a Macbook running Python 3.9 and specific C-libraries. When they deploy it to an AWS Linux VM running Python 3.7, the application fatally crashes due to missing dependencies and environmental mismatches.
**Containerization (Docker)** was invented to eradicate this friction. A Container does not just package the Application Code. It packages the Code, the exact version of the Runtime (Python 3.9), all system libraries, and the exact environmental variables into an immutable, sealed artifact (A Docker Image).
Because the Container isolates its own runtime environment from the Host OS, you can drop that Docker Image onto a Macbook, a Windows laptop, or an AWS Linux server, and it is mathematically guaranteed to execute exactly the same way.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình Bố trí Mạng (Cài đặt 10 máy chủ, mở tường lửa, cấu hình IP).
</details>

Visualizing Infrastructure Management (ClickOps vs IaC).

| Metric | "ClickOps" (Manual Web Console) | Infrastructure as Code (Terraform) |
|---|---|---|
| **The Process** | The DevOps engineer logs into the AWS Website, clicks 50 buttons to create a network, types in IPs manually, clicks "Create Server". | The engineer writes a text file describing the network. Runs `terraform apply`. Terraform talks to the AWS API and builds everything in 30 seconds. |
| **Disaster Recovery**| A hacker deletes your AWS account. You must try to remember exactly which 50 buttons you clicked 2 years ago to rebuild it. Impossible. | Your account is deleted. You just run `terraform apply` on a new account. The exact identical infrastructure is rebuilt perfectly in 5 minutes. |
| **Code Review** | Nobody knows who clicked what button or why the server suddenly crashed yesterday. | Every server change is a Git Commit. You can see exactly which developer changed the Firewall rule on Line 42. |

---

## Layer 4: The Modern Cloud Stack

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hạ tầng hiện đại không có ai thao tác bằng tay nữa, nó là sự kết hợp của 4 công nghệ lõi:
1. **Nền tảng Cloud (AWS, GCP)**: Nơi cung cấp điện, CPU, Ổ cứng vô hạn.
2. **Docker (Đóng gói)**: Biến mọi thứ phần mềm trên đời thành những cái Thùng Container vuông vức, bất biến, dễ dàng quăng quật đi khắp nơi.
3. **Kubernetes (Chỉ huy Container)**: Khi bạn có 1 cái Container, Docker là đủ. Nhưng khi bạn có 5000 cái Container, làm sao biết cái nào chết để khởi động lại? Làm sao cập nhật bản mới mà không tắt web? K8s (Kubernetes) là vị Nhạc trưởng, tự động điều phối hàng ngàn Container đó trơn tru mà con người không cần can thiệp.
4. **Terraform (Mã hóa Hạ tầng)**: Mã nguồn quản lý 3 ông ở trên. Xóa sổ nghề "Quản trị Hệ thống bằng tay". Biến cấu hình máy chủ thành những dòng Code.

</details>

The modern Cloud-Native infrastructure stack has standardized around a specific evolution of abstraction:
1. **The Cloud Provider (AWS / Azure / GCP)**: The foundational physical layer. They provide the massive datacenters, the hypervisors, the BGP routing, and the physical security. They expose these primitives via REST APIs.
2. **Containerization (Docker)**: The standardization of the Application payload. Developers no longer ship ZIP files of code; they ship immutable Docker Images to a centralized Registry (Docker Hub / ECR).
3. **Container Orchestration (Kubernetes)**: Managing 5 containers on 1 server is easy. Managing 10,000 containers across 500 servers is impossible for humans. Kubernetes acts as the automated Cloud Operating System. You declare the desired state ("I want 5 copies of the Login container running"). Kubernetes continuously monitors the cluster. If a server burns down and 2 containers die, Kubernetes instantly respawns them on a healthy server without human intervention.
4. **Infrastructure as Code (Terraform)**: The automation of the Cloud Provider itself. Before deploying Kubernetes, you need VPCs, Subnets, IAM Roles, and Load Balancers. Terraform allows you to define this entire AWS infrastructure in declarative HashiCorp Configuration Language (HCL).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nguyên tắc "Cầm thú" (Cattle, not Pets)**: Ngày xưa, quản trị viên đặt tên cho Máy chủ là "Bé Miu", "Bé Bông", cưng nựng chúng, nếu chúng bệnh thì cài thuốc (Update) chữa cẩn thận. Ở kỷ nguyên Cloud, Máy chủ là **Gia súc**. Chú bò số 123 bị lỗi mạng? Rút súng bắn bỏ ngay lập tức (Xóa máy ảo), bấm nút đẻ ra chú bò số 124 thay thế trong 5 giây. Không bao giờ SSH vào một máy chủ trên Cloud để "Sửa lỗi bằng tay". Máy chủ phải là thứ Bất biến (Immutable).
2. **Phân quyền Tối thiểu (Principle of Least Privilege - IAM)**: Lỗi bảo mật lớn nhất thế giới không phải do Hacker phá mã hóa, mà do Lập trình viên lỡ đẩy cái Chìa khóa AWS (Access Key) lên Github. Hãy luôn dùng IAM Roles. Máy chủ A chỉ được quyền "Đọc hình ảnh", tuyệt đối không cấp quyền "Xóa hình ảnh" hay "Truy cập Database B" cho nó.

</details>

1. **Cattle, Not Pets (Immutable Infrastructure)**: The most fundamental paradigm shift in DevOps. Historically, servers were "Pets". They were given cute names (Zeus, Apollo), manually configured, and carefully patched when sick. In Cloud-Native, servers are "Cattle". They are numbered (Node-1045), completely disposable, and identical. If Node-1045 exhibits high CPU or network errors, you DO NOT SSH into it to debug and fix it. You mercilessly terminate it. The Auto-Scaling Group instantly spins up a fresh, identical replacement. You never modify running servers; you modify the Terraform code and redeploy a fresh server.
2. **The Principle of Least Privilege (IAM)**: 99% of devastating Cloud breaches occur because of compromised Identity and Access Management (IAM) credentials. A developer writes a Lambda function to upload images to S3, but naively grants the Lambda an `AdministratorAccess` IAM Role. A hacker finds an exploit in the Lambda code, assumes the Admin role, and deletes the company's entire database. **Rule**: Every single microservice must have a distinct IAM Role that grants *only* the exact mathematical permissions it needs to function (e.g., `s3:PutObject` on exactly `arn:aws:s3:::my-bucket` and nothing else).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Ác mộng Hóa đơn (Cloud Shock)**: Khởi động 1 máy chủ xịn trên AWS mất 3 cái click chuột. Lập trình viên làm xong quên tắt. Cuối tháng AWS gửi hóa đơn 20.000 USD. 
   - *Luật*: Luôn cài đặt Cảnh báo Ngân sách (Billing Alarms). Nếu chi phí vượt 50$, hệ thống tự động gởi Email hoặc tự động ngắt máy chủ.
2. **Vendor Lock-in (Trói buộc với Nhà cung cấp)**: Bạn dùng các dịch vụ quá xịn của AWS (như DynamoDB, Lambda). Bạn viết hàng chục ngàn dòng code xoay quanh chúng. Ngày mai, AWS tăng giá gấp 3 lần. Bạn muốn dời nhà sang Google Cloud? Bạn nhận ra mình phải Vứt bỏ toàn bộ Code và viết lại từ đầu.
   - *Luật*: Nếu công ty bạn sợ bị trói buộc, hãy dùng những công nghệ Tiêu chuẩn mở. Dùng Postgres thay vì DynamoDB. Dùng Kubernetes thay vì AWS Lambda. Lúc đó, việc chuyển nhà từ AWS sang Google Cloud diễn ra cực kì trơn tru.

</details>

1. **Cloud Bill Shock (Runaway CapEx)**: In the On-Premise era, spending $50,000 required 4 layers of managerial signature approvals. In AWS, a Junior Developer can accidentally spin up a cluster of `p4d.24xlarge` GPU instances with 3 clicks and accumulate a $30,000 bill over the weekend. Cloud resources run endlessly until explicitly destroyed. **Rule**: Implement strict Cloud Financial Operations (FinOps). Immediately configure **AWS Budgets and Billing Alarms** on Day 1. Use Terraform to tag all resources with `Environment: Dev` and run cron jobs that automatically shut down all `Dev` environments at 6:00 PM every Friday.
2. **The Vendor Lock-in Dilemma**: Cloud providers entice you with hyper-optimized managed services (e.g., AWS DynamoDB, AWS SQS, AWS Lambda). While these drastically accelerate early development, your Application Code becomes deeply coupled to AWS-proprietary SDKs. If AWS raises prices aggressively, migrating your DynamoDB app to Google Cloud requires a complete, multi-month code rewrite. **The Kubernetes Escape Hatch**: To maintain Cloud Agnosticism, mature engineering teams avoid proprietary SaaS. They deploy a generic Kubernetes cluster. They run standard open-source tools (PostgreSQL, Kafka) inside K8s. Because K8s is a universal API, migrating the entire infrastructure from AWS (EKS) to Google Cloud (GKE) requires minimal friction.

---

## Related Topics

- For the undisputed leader in Cloud Computing, see **[AWS](./aws.md)**.
- For packaging applications into isolated environments, learn **[Docker](./docker.md)**.
- For orchestrating thousands of containers dynamically, proceed to **[Kubernetes](./kubernetes.md)**.
- To manage Cloud networks using Code instead of mouse clicks, explore **[Terraform](./terraform.md)**.
