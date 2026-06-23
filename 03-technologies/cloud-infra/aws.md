# Amazon Web Services (AWS)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khởi đầu chỉ là một công cụ nội bộ để giúp trang web bán sách Amazon không bị sập vào dịp Giáng sinh, **AWS (Amazon Web Services)** giờ đây đã trở thành Trụ cột nền tảng của toàn bộ Internet. Nó là nhà cung cấp Điện toán Đám mây lớn nhất thế giới, vượt xa Google Cloud hay Azure. Nét đặc trưng của AWS là nó sở hữu số lượng Dịch vụ (Services) khổng lồ đến mức choáng ngợp (hơn 200 dịch vụ). Thay vì bắt bạn tự xây dựng mọi thứ từ số 0, AWS cung cấp các "Khối Lego" làm sẵn: Bạn cần Lưu trữ file? Dùng Lego S3. Bạn cần Database? Dùng Lego RDS. Bạn cần AI? Dùng Lego SageMaker. Sức mạnh của AWS nằm ở hệ sinh thái khép kín vô cùng chặt chẽ và khả năng mở rộng (Scale) đến mức gần như vô tận, đáp ứng từ một trang web cá nhân nhỏ bé cho đến hệ thống chiếu phim toàn cầu của Netflix.

</details>

> **Summary**: Originally conceptualized as an internal infrastructure platform to handle Amazon.com's massive holiday traffic spikes, **AWS (Amazon Web Services)** essentially invented the modern Cloud Computing industry in 2006. Today, it possesses the largest market share, the most extensive global datacenter footprint, and the deepest feature set in the industry. AWS provides a staggering catalog of over 200 fully-featured services. It operates on a shared-responsibility model and embraces the "Lego Block" architectural philosophy. Instead of provisioning bare-metal servers and installing databases manually, architects wire together managed services: EC2 for raw compute, S3 for infinite object storage, RDS for managed relational databases, and Lambda for serverless execution. Its dominance is cemented by extreme reliability, infinite horizontal scalability, and an incredibly mature, enterprise-grade security model (IAM).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn muốn mở một Khu Vui Chơi.
1. **Tự làm (Không dùng AWS)**: Bạn phải đi mua đất, mua gạch, tự trộn xi măng xây nhà, tự kéo dây điện, tự mướn bảo vệ. Rất cực và mất nhiều năm. Lỡ xây xong mà không có ai chơi thì phá sản.
2. **Dùng AWS (Siêu thị xây dựng)**: AWS là một Siêu thị bán mọi thứ làm sẵn để xây Khu Vui Chơi, và ĐẶC BIỆT là họ cho thuê theo giờ.
   - Bạn muốn có nhà chui? Bấm nút thuê "EC2".
   - Bạn muốn có bảo vệ siêu xịn? Bấm nút thuê "IAM".
   - Bạn muốn kho chứa đồ chơi vô hạn? Bấm nút thuê "S3".
   - Bạn ghép các mảnh Lego này lại trong 1 ngày là có Khu Vui Chơi. Khi nào khách về hết, bạn trả lại đồ cho siêu thị và không tốn thêm đồng nào nữa.

</details>

Imagine building a City.
1. **On-Premise**: You have to mine the iron ore, forge the steel, build the power plant, lay the plumbing, and construct the buildings yourself. It takes 5 years and millions of dollars upfront.
2. **AWS (The City Builder Simulator)**: AWS provides you with a magical control panel. You want a Power Plant? Click `Provision EC2`. You want a giant Warehouse that magically expands forever? Click `Provision S3`. You want a Security Force? Click `Provision IAM`. You assemble these pre-built, highly-reliable components in an afternoon. The magic is: you only pay for the exact number of seconds you actually use these buildings.

---

## Layer 1: Core Primitives (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dù AWS có hơn 200 dịch vụ, 90% hệ thống trên thế giới chỉ xoay quanh 5 Dịch vụ "Huyền thoại" này:
1. **EC2 (Elastic Compute Cloud - Máy ảo)**: Đây là cái Cốt lõi nhất. Bạn thuê một cái máy tính chạy Linux hoặc Windows. Bạn muốn cài gì lên đó cũng được. Giao toàn quyền sinh sát cho bạn.
2. **S3 (Simple Storage Service - Kho lưu trữ)**: Một cái ổ cứng "Không bao giờ đầy" và "Không bao giờ mất dữ liệu". Nhét hình ảnh, video, file backup vào đây. Giá cực kì rẻ.
3. **RDS (Relational Database Service - Database làm sẵn)**: Nếu bạn tự cài Postgres lên EC2, bạn phải tự lo Backup, tự lo chống sập. Dùng RDS, AWS cài sẵn Postgres cho bạn. Họ tự động sao lưu dữ liệu mỗi ngày, nếu máy hỏng họ tự đổi máy mới. Bạn chỉ việc cắm vào và xài.
4. **VPC (Virtual Private Cloud - Mạng nội bộ)**: Đây là bức tường Tường lửa (Firewall) bao bọc toàn bộ hệ thống của bạn, tách biệt nó với Internet bên ngoài để chống Hacker.
5. **IAM (Identity and Access Management - Bảo vệ)**: Trái tim bảo mật của AWS. Cấp phát Chìa khóa và Quyền hạn cho từng người, từng cái máy chủ.

</details>

While the AWS console is famously overwhelming, 90% of architectural patterns rely on the same five foundational primitives:
1. **Compute (Amazon EC2)**: Elastic Compute Cloud. The absolute workhorse of the cloud. It provides resizable, raw Virtual Machines (Linux/Windows) in the cloud. You have full root SSH access to install any software stack.
2. **Storage (Amazon S3)**: Simple Storage Service. An infinitely scalable Object Store. It does not have a traditional file system structure. You upload files (objects) up to 5TB each. It guarantees 99.999999999% (11 nines) of durability. Used for image hosting, backups, and data lakes.
3. **Databases (Amazon RDS)**: Relational Database Service. A fully managed DB service. Instead of installing PostgreSQL on an EC2 instance manually, RDS provisions the database, automatically handles OS patching, takes automated daily snapshots, and handles Multi-AZ failover gracefully.
4. **Networking (Amazon VPC)**: Virtual Private Cloud. The security boundary. It allows you to provision a logically isolated section of the AWS Cloud where you launch your resources in a custom virtual network (Subnets, Route Tables, Internet Gateways).
5. **Security (AWS IAM)**: Identity and Access Management. The most critical service. It acts as the central brain for authentication and authorization. It dictates mathematically exactly *who* (Users/Roles) can do *what* (Actions) to *which* Resources.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao một công ty sẵn sàng trả cho AWS 100.000 USD/tháng thay vì tự mua máy chủ giá rẻ hơn?
Vì 3 lý do cốt lõi:
1. **Sự Đàn Hồi (Elasticity)**: Ngày thường bạn cần 5 máy chủ. Đúng đêm Black Friday, bạn cần 500 máy chủ. Tới sáng thứ 7, bạn lại chỉ cần 5 máy. AWS (chức năng Auto Scaling) cho phép bạn co giãn số lượng máy chủ trong chớp mắt. Nếu tự mua 500 máy, bạn sẽ lãng phí chúng trong suốt 364 ngày còn lại trong năm.
2. **Global Reach (Tầm vóc toàn cầu)**: Bạn ở Việt Nam, nhưng muốn mở App cho khách ở Mỹ và Châu Âu. Bạn chỉ việc chọn "Region: us-east-1" và "Region: eu-west-1", ứng dụng của bạn ngay lập tức có mặt ở Mỹ và Châu Âu với tốc độ mạng cực nhanh.
3. **Mô hình Dịch vụ Quản lý (Managed Services)**: Việc thuê kỹ sư giỏi Database để cấu hình High-Availability (Không bao giờ sập) cho Postgres tốn hàng chục ngàn đô tiền lương. Thay vì vậy, xài AWS RDS, đánh 1 dấu tick vào ô "Multi-AZ", AWS sẽ tự động làm điều đó hoàn hảo. Công ty chỉ tập trung lo viết Code kiếm tiền.

</details>

Why do massive enterprises migrate to AWS, accepting the premium operational costs over maintaining their own datacenters?
1. **Elasticity & Auto-Scaling (The Black Friday Problem)**: In traditional data centers, you must buy hardware based on your *Maximum Expected Peak Traffic*. If your peak is 10x your average load, 90% of your hardware sits idle (wasting money) for 364 days a year. AWS introduces **Elasticity**. Using EC2 Auto Scaling Groups, your infrastructure dynamically expands to 500 servers during a traffic spike, and gracefully shrinks back to 5 servers when the spike ends. You only pay for the precise duration the servers were active.
2. **Global Availability Zones (AZs)**: AWS operates Regions (e.g., `us-east-1` in Virginia) and Availability Zones (isolated datacenters within a Region with independent power and cooling). If a tornado destroys Datacenter A, the AWS Load Balancer instantly routes traffic to your mirrored servers in Datacenter B. Achieving this level of disaster recovery on-premise requires billions of dollars.
3. **The Shift to Managed Services (Reducing Operational Burden)**: Managing the underlying OS, patching security vulnerabilities, and configuring complex PostgreSQL replication takes immense engineering hours. By utilizing Managed Services (like RDS, DynamoDB, Elasticache), AWS handles the "undifferentiated heavy lifting", allowing your engineering teams to focus 100% on writing proprietary business logic.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình đối phó khi Ổ cứng bị hỏng (Mất dữ liệu).
</details>

Visualizing Disaster Recovery (On-Premise vs AWS).

| Metric | On-Premise (Bare Metal) | AWS Cloud |
|---|---|---|
| **Hard Drive Failure** | A physical hard drive dies. The database goes down. An engineer must drive to the datacenter at 2 AM to swap the drive. | The EBS (Elastic Block Store) volume underlying your database fails. AWS automatically detaches it, provisions a new one from your Snapshot, and reattaches it. You sleep through the night. |
| **Data Durability**| You backup to a second hard drive. If the building catches fire, both drives burn. Data is lost forever. | You upload files to S3. AWS transparently copies that file to 3 completely different geographic datacenters simultaneously. Data is mathematically invincible (11 nines). |

---

## Layer 4: Common Architectural Patterns

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Kiến trúc Máy ảo truyền thống (EC2 + RDS)**: Cách dễ nhất khi mới lên mây. Bạn thuê 3 máy EC2 để chạy Code Node.js, đặt 1 cái Load Balancer ở trước mặt. Đằng sau nối vào máy RDS (Database). 
2. **Kiến trúc Serverless (Không máy chủ - Lambda)**: Bạn LƯỜI đến mức không muốn quan tâm đến Máy chủ nữa. AWS sinh ra tính năng Lambda. Bạn chỉ việc tải 1 File Code chứa 1 cái Hàm (Function) lên AWS. Khi nào khách hàng gọi API, AWS tự động bật cái hàm đó lên chạy, chạy xong tắt ngay lập tức. Tính tiền theo số mili-giây hàm đó chạy. Khách hàng không gọi thì tốn 0 đồng.
3. **Kiến trúc Container (EKS / ECS)**: Thay vì dùng máy ảo EC2 nặng nề. Bạn đóng gói App thành Docker. Bạn giao hàng ngàn cái hộp Docker đó cho dịch vụ EKS (Kubernetes của AWS) quản lý.

</details>

AWS architecture typically evolves through stages of abstraction as teams mature:
1. **Re-hosting ("Lift and Shift" - EC2/RDS)**: The traditional starting point. You mimic your On-Premise architecture in the Cloud. You deploy a fleet of raw EC2 instances running your Java/Node code, hidden behind an Application Load Balancer (ALB), connected to a Managed RDS Database.
2. **Container Orchestration (EKS / ECS)**: Moving away from fragile VMs. You package your application into immutable Docker Containers. Instead of managing individual EC2 instances, you hand your containers to ECS (Elastic Container Service) or EKS (Elastic Kubernetes Service). AWS manages the scheduling and placement of these containers across the underlying infrastructure.
3. **Serverless Architectures (AWS Lambda + DynamoDB)**: The ultimate Cloud-Native paradigm. You completely surrender server management to AWS. You write a single JavaScript function and deploy it to **AWS Lambda**. The function sits completely dormant (costing $0.00). When an HTTP request hits the API Gateway, AWS instantly spins up a micro-environment, executes your function, returns the response, and kills the environment. You pay strictly per 1 millisecond of execution time.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Không bao giờ dùng tài khoản Root (Gốc)**: Khi mới đăng ký AWS, bạn có 1 cái email/mật khẩu gọi là Root. Nó có quyền xóa sổ toàn bộ công ty. Việc đầu tiên là bật Bảo mật 2 lớp (MFA) cho tài khoản Root, CẤT NÓ ĐI và không bao giờ xài nữa. Thay vào đó, dùng dịch vụ IAM tạo ra các tài khoản con (Admin, Dev) có quyền hạn vừa đủ để làm việc hằng ngày.
2. **Cảnh giác với tính năng Tự động co giãn (Auto-Scaling)**: Auto-scaling giúp web không sập khi đông khách, nhưng nó cũng là con dao hai lưỡi. Hacker có thể tạo ra một cuộc tấn công DDoS nhỏ giọt. Thay vì làm sập web của bạn, nó sẽ kích hoạt Auto-scaling đẻ ra hàng trăm máy chủ mới. Web vẫn sống, nhưng cuối tháng bạn nhận hóa đơn 50.000 USD phá sản. Luôn luôn phải cài đặt `Max Instances` (Số máy đẻ ra tối đa) để giới hạn tài chính.

</details>

1. **Lock Down the Root Account (IAM First)**: The most critical security mandate. The initial email/password used to create the AWS Account is the "Root User". It bypasses all permission boundaries and can delete the entire account. **Rule**: Enable hardware MFA on the Root User immediately. Lock the physical token in a safe. NEVER generate Access Keys for the Root User. Create a separate IAM User with `AdministratorAccess` for your daily work, and utilize strict IAM Roles for all Application/CI-CD access.
2. **Implement Financial Guardrails on Auto-Scaling**: Auto-Scaling is incredibly powerful, but it converts DDoS attacks into "Economic Denial of Sustainability" (EDoS) attacks. A hacker floods your API. The Auto-Scaling Group (ASG) detects high CPU, assumes it's legitimate traffic, and spins up 100 massive EC2 instances to handle the load. Your site stays online, but you go bankrupt. **Rule**: ALWAYS set a hard `MaxCapacity` limit on your ASG, deploy a WAF (Web Application Firewall) to block malicious traffic before it hits the compute layer, and set stringent AWS Billing Alarms.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lộ Access Key lên Github**: Tội lỗi tồi tệ nhất của Lập trình viên. Bạn code tính năng Upload hình lên S3. Bạn chép cái Chìa khóa (Access Key) của AWS thẳng vào code Node.js rồi đẩy lên Github (Dù là Repo Private). Các con Bot của Hacker rà quét Github 24/7. Chỉ mất 3 giây, Hacker lấy được Key, đăng nhập vào AWS của bạn và đào Bitcoin.
   - *Cách giải*: KHÔNG BAO GIỜ viết Key vào Code. Code chạy trên máy EC2 nào, hãy Gắn cái "Role IAM" cho cái máy EC2 đó. Code sẽ tự động lấy được quyền mà không cần bất kì dòng chữ mật khẩu nào.
2. **Để hở máy chủ Database ra Internet (Lỗi cấu hình VPC)**: Rất nhiều người mới dùng AWS cho cái máy Database RDS nằm ở "Public Subnet" (Khu vực có thể truy cập từ ngoài Internet) để tiện dùng phần mềm DBeaver kết nối vào xem dữ liệu. Hacker sẽ scan trúng cái Port 5432 đó và dò mật khẩu phá hoại. Database LUÔN LUÔN phải nằm ở "Private Subnet" (Khu vực cách ly). Muốn xem dữ liệu thì phải dùng VPN hoặc nhảy qua một cái máy chủ trung gian (Bastion Host).

</details>

1. **Leaking AWS Credentials (The GitHub Scraping Nightmare)**: The most common vector for cloud breaches. A junior developer hardcodes an `AWS_ACCESS_KEY_ID` into their Node.js source code to interact with S3. They commit the code to GitHub. Malicious bots scan public (and exposed private) GitHub repos 24/7. Within 10 seconds of the commit, the hacker extracts the keys, provisions 500 GPU instances across 10 regions, and mines cryptocurrency, saddling the company with a $100,000 bill. **Rule**: NEVER hardcode credentials. When applications run on AWS (EC2/EKS/Lambda), utilize **IAM Instance Profiles / Roles**. The underlying AWS infrastructure will securely inject temporary, rotating credentials directly into the application's environment natively.
2. **Architecting Databases in Public Subnets (VPC Misconfiguration)**: A catastrophic network design flaw. Developers often place their Managed RDS instance into a Public Subnet and attach an Internet Gateway, simply so they can connect their local PGAdmin/DBeaver GUI to it easily. This exposes the raw database port (e.g., 3306, 5432) to the entire global internet, making it a target for brute-force attacks and zero-day exploits. **Rule**: Databases MUST exclusively reside in **Private Subnets** with no inbound routing from the Internet. To access them, engineers must use AWS Systems Manager (SSM) Session Manager or connect via a hardened VPN/Bastion Host residing in the Public Subnet.

---

## Related Topics

- For managing infrastructure like AWS VPCs and EC2 instances via Code, you must learn **[Terraform](./terraform.md)**.
- AWS provides Managed Kubernetes via EKS. See **[Kubernetes](./kubernetes.md)**.
- To package your applications before deploying them to AWS, you must use **[Docker](./docker.md)**.
