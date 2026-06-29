# Cloud Computing Models

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Tìm hiểu các khái niệm cốt lõi của Điện toán Đám mây (Cloud Computing). Phân biệt giữa IaaS, PaaS, SaaS và thấu hiểu Mô hình Trách nhiệm Chia sẻ (Shared Responsibility Model) - nền tảng của an ninh đám mây.

</details>

> **Summary**: Understand the core concepts of Cloud Computing. Differentiate between IaaS, PaaS, SaaS, and deeply understand the Shared Responsibility Model—the absolute foundation of cloud security.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn muốn ăn Pizza:
1. **On-Premise (Tự làm ở nhà)**: Bạn tự mua bột, mua phô mai, tự nướng bằng lò của mình, tự rửa chén. (Bạn lo MỌI THỨ từ A-Z).
2. **IaaS (Mua vỏ bánh)**: Siêu thị bán sẵn đế bánh pizza. Bạn mang về, tự cho nhân lên, nướng bằng lò của bạn. (Cloud lo phần cứng, bạn lo phần mềm).
3. **PaaS (Giao bánh tận nhà)**: Bạn gọi điện, họ nướng xong giao tận nhà. Bạn chỉ việc tự dọn bàn ăn và chuẩn bị nước ngọt. (Cloud lo luôn cả hệ điều hành, bạn chỉ lo code của mình).
4. **SaaS (Ăn tại nhà hàng)**: Bạn đến nhà hàng, ngồi xuống, ăn, trả tiền rồi về. Không cần dọn rửa gì cả. (Cloud lo 100%, bạn chỉ việc xài).

</details>

Imagine you want to eat Pizza:
1. **On-Premise (Make it at home)**: You buy the dough, the cheese, bake it in your own oven, and wash the dishes. (You manage EVERYTHING from A-Z).
2. **IaaS (Take-and-bake)**: The store provides the dough. You add the toppings and use your oven. (The Cloud manages the raw hardware, you manage the software/OS).
3. **PaaS (Pizza Delivery)**: The pizzeria bakes the pizza and delivers it. You just provide the dining table and drinks. (The Cloud manages the OS/runtime, you only manage your application code).
4. **SaaS (Dine out)**: You go to a restaurant, eat, pay, and leave. Zero cleanup. (The Cloud manages 100% of the software; you just use it).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Điện toán Đám mây** là việc cung cấp các dịch vụ điện toán (server, ổ cứng, database, mạng) qua Internet ("đám mây") với mức giá dùng bao nhiêu trả bấy nhiêu (Pay-as-you-go).
Nó được chia thành 3 mô hình dịch vụ chính:
- **IaaS (Infrastructure as a Service)**: Cung cấp khối xây dựng cơ bản (Server ảo, Mạng, Ổ cứng). Ví dụ: AWS EC2.
- **PaaS (Platform as a Service)**: Ẩn đi hệ điều hành, cung cấp sẵn nền tảng để chạy code. Ví dụ: AWS Elastic Beanstalk, Heroku.
- **SaaS (Software as a Service)**: Phần mềm hoàn chỉnh người dùng cuối sử dụng qua trình duyệt. Ví dụ: Gmail, Salesforce, Dropbox.

**Phân loại:**
- **Loại**: Mô hình Dịch vụ (Service Models) / Cloud Engineering.

</details>

**Cloud Computing** is the on-demand delivery of IT resources (servers, storage, databases, networking) over the Internet with pay-as-you-go pricing.
It is divided into 3 main service models:
- **IaaS (Infrastructure as a Service)**: Provides the fundamental building blocks (Virtual Machines, Networking, Storage). Example: AWS EC2.
- **PaaS (Platform as a Service)**: Abstracts away the underlying Operating System, providing a managed platform to just run code. Example: AWS Elastic Beanstalk, Heroku.
- **SaaS (Software as a Service)**: A completed software product run and managed by the service provider, consumed by end-users via a browser. Example: Gmail, Salesforce.

### Classification
- **Type**: Service Models / Cloud Engineering.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Sự chấm dứt của On-Premise (Máy chủ vật lý)**
Ngày xưa (On-Premise), để mở một website, công ty phải mua máy chủ giá $50,000, thuê phòng lạnh, cắm cáp mạng. Mất 3 tháng mới mua xong. Đến ngày Black Friday, lượng người truy cập tăng gấp 10, máy chủ sập vì quá tải. Hôm sau, lượng truy cập giảm xuống, máy chủ lại ngồi không, gây lãng phí khủng khiếp.

Đám mây giải quyết bài toán này: Thay vì **Chi phí Vốn (CapEx)** - mua đứt máy chủ, doanh nghiệp chuyển sang **Chi phí Hoạt động (OpEx)** - thuê máy chủ theo giờ. Cần 100 máy chủ vào Black Friday? Bấm nút là có trong 2 phút. Qua ngày mai, trả lại máy chủ và không tốn thêm đồng nào. Sự "Đàn hồi" (Elasticity) này là lý do Cloud thống trị thế giới.

</details>

**The Death of On-Premise (Physical Servers)**
Historically (On-Premise), launching a website required buying a $50,000 server, renting an air-conditioned room, and plugging in cables. Provisioning took 3 months. On Black Friday, traffic spiked 10x, and the server crashed. The next day, traffic dropped to normal, and the server sat idle, wasting immense money.

The Cloud solved this paradigm by shifting from **Capital Expenditure (CapEx)**—buying physical hardware upfront—to **Operational Expenditure (OpEx)**—renting hardware by the hour. Need 100 servers for Black Friday? Click a button and get them in 2 minutes. Tomorrow, terminate them and stop paying. This "Elasticity" is exactly why Cloud Computing conquered the IT industry.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Bảo mật On-Premise**: Bạn phải tự xây tường rào, tự khóa cửa phòng server, tự vá lỗi (patch) hệ điều hành Windows, tự cập nhật mã nguồn ứng dụng. Lỗi ở đâu bạn tự chịu trách nhiệm ở đó.
- **Bảo mật Cloud (Shared Responsibility Model)**: AWS bảo vệ "CỦA đám mây" (Tường rào vật lý, ổ điện, ổ cứng vật lý). BẠN bảo vệ những thứ "TRONG đám mây" (Mật khẩu của bạn, hệ điều hành của EC2, dữ liệu khách hàng). Nếu hacker lấy được mật khẩu AWS của bạn, AWS hoàn toàn không có lỗi!

</details>

### Traditional Security (On-Premise)
You are responsible for literally everything. If a thief breaks the physical window of your server room and steals a hard drive, it's your fault.

### Cloud Security (The Shared Responsibility Model)
This is the most critical concept in Cloud Engineering. Security is split into two halves:
1. **Security OF the Cloud (Provider's Responsibility)**: AWS is responsible for protecting the infrastructure that runs all the services. This includes physical security of data centers, hardware, networking cables, and hypervisors. (If AWS data center catches fire, it's their problem).
2. **Security IN the Cloud (Customer's Responsibility)**: You are responsible for configuring the services securely. This includes OS patching, network firewall rules (Security Groups), IAM password policies, and encrypting your data. (If you put your database password on GitHub and get hacked, AWS is NOT responsible).

| Layer | IaaS (e.g., EC2) | PaaS (e.g., RDS) | SaaS (e.g., Gmail) |
|---|---|---|---|
| **Physical Hardware** | AWS | AWS | AWS |
| **Host OS / Hypervisor**| AWS | AWS | AWS |
| **Guest OS (Windows/Linux)** | **You** (Must patch it) | AWS | AWS |
| **Application Runtime** | **You** | AWS | AWS |
| **Customer Data** | **You** | **You** | **You** |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng IaaS (EC2)**: Khi bạn có một ứng dụng cũ kĩ (Legacy) cần chạy trên một phiên bản Windows Server năm 2012 cụ thể, hoặc khi bạn cần quyền Root để cài đặt driver nhân (kernel). Bạn có toàn quyền kiểm soát.
2. **Dùng PaaS (Elastic Beanstalk / RDS)**: Lựa chọn mặc định cho kỹ sư phần mềm. Bạn chỉ muốn đẩy code Python lên và chạy, hoặc bạn muốn có Database mà không phải thức đêm tự sao lưu (backup). Hãy để Cloud lo hệ điều hành.
3. **Dùng SaaS (Auth0, Datadog)**: Khi tính năng đó không phải là cốt lõi kinh doanh của bạn. Thay vì tự code hệ thống Đăng nhập (tốn 2 tháng), hãy mua luôn gói SaaS của Auth0 (tốn 10 phút tích hợp).

**Không nên làm (Anti-patterns):**
- **Dùng IaaS để tự cài Database (Cài MySQL trên EC2)**: Cực kỳ sai lầm! Bạn sẽ phải tự vá lỗi Linux, tự config Master-Slave, tự dọn rác ổ cứng. Hãy dùng PaaS (Amazon RDS) để AWS làm hộ bạn những việc nhàm chán này.

</details>

1. **Using IaaS (e.g., AWS EC2)**: When migrating a legacy application that requires a highly specific, outdated OS version (like Windows Server 2012), or when you need absolute root access to install kernel-level drivers. You have total control.
2. **Using PaaS (e.g., AWS RDS, Elastic Beanstalk)**: The default choice for modern software engineering. You just want to write Python code, or you want a PostgreSQL database without manually managing daily backups and OS security patches. Let the Cloud provider manage the tedious OS layer.
3. **Using SaaS (e.g., Auth0, GitHub)**: When the functionality is not your core business differentiator. Instead of spending 2 months building a secure Login system, just pay Auth0 a monthly fee (SaaS) and integrate it in 10 minutes.

### Anti-Patterns
- **Using IaaS to manually host a Database (Installing MySQL on EC2)**: A massive anti-pattern for 99% of companies. If you do this, you become responsible for patching the Linux OS, configuring Master-Slave replication manually, and taking 3 AM backups. Always use PaaS (Amazon RDS) to offload this "undifferentiated heavy lifting" to AWS.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Trượt dốc trách nhiệm (Responsibility Shift)**
Càng di chuyển từ IaaS -> PaaS -> SaaS (hoặc Serverless), ranh giới trách nhiệm của AWS càng phình to, và ranh giới của bạn càng nhỏ lại. Ví dụ với AWS Lambda (Serverless), bạn thậm chí không cần quản lý hệ điều hành, bạn CHỈ quản lý đúng dòng code Python của bạn và dữ liệu. Đội ngũ giỏi thường ưu tiên đi lên các cấp PaaS/Serverless để tiết kiệm tiền thuê nhân sự vận hành.

**2. Đa vùng (Multi-Region) & Tính sẵn sàng cao (High Availability)**
Cloud không bao giờ cam kết 100% không sập. SLA cao nhất thường là 99.99%.
- **Availability Zone (AZ)**: Là một Data Center độc lập (có nguồn điện riêng, mạng riêng). Luôn chạy app ở ít nhất 2 AZ (Multi-AZ) để nếu 1 Data Center bị cháy, app vẫn sống.
- **Region**: Là một khu vực địa lý (ví dụ: Tokyo, Singapore). Chạy Multi-Region rất tốn tiền và rất phức tạp để đồng bộ Database, chỉ dành cho các hệ thống siêu cấp quan trọng (Ngân hàng, Y tế).

</details>

### 1. The Responsibility Shift
As you move across the spectrum from IaaS -> PaaS -> SaaS (or Serverless), the Shared Responsibility boundary shifts dramatically. With AWS Lambda (Serverless), you don't even manage the Guest OS; AWS handles it. You ONLY manage your Python code and the IAM permissions attached to it. High-performing engineering teams actively strive to adopt PaaS/Serverless to eliminate operational overhead (undifferentiated heavy lifting).

### 2. High Availability (HA) & Fault Tolerance
Cloud providers never guarantee 100% uptime (SLAs max out around 99.99%). Hardware fails.
- **Availability Zones (AZ)**: One or more discrete data centers with redundant power and networking. *Best Practice*: Always deploy production workloads across at least 2 AZs (Multi-AZ). If one data center burns down, the other takes over instantly.
- **Regions**: Isolated geographic areas (e.g., `us-east-1` in Virginia, `ap-northeast-1` in Tokyo). *Best Practice*: Multi-Region deployments are extremely expensive and hard to synchronize (due to the speed of light / latency). Only use Multi-Region for ultra-critical Tier-1 systems (Banking, Healthcare) or global CDN edge caching.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong Cloud hiện đại, chúng ta không dùng chuột bấm giao diện web. Chúng ta dùng Code để tự động hóa việc tạo Cloud (Gọi là Infrastructure as Code - IaC). Dưới đây là ví dụ dùng Terraform để tạo một máy chủ ảo (IaaS - EC2).

</details>

### Infrastructure as Code (IaC) - Provisioning IaaS via Terraform

Modern Cloud Engineering strictly relies on IaC to provision resources rather than clicking through the AWS Web Console. This ensures reproducibility and version control.

```hcl
# main.tf
# Example of provisioning an IaaS component (AWS EC2 Virtual Machine)

provider "aws" {
  region = "us-east-1"
}

# Requesting a Virtual Machine (IaaS) from the Cloud Provider
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 Image
  instance_type = "t2.micro"              # The hardware size (CPU/RAM)

  tags = {
    Name        = "MyFirstCloudServer"
    Environment = "Production"
  }
}

# Output the IP address so we can connect to it
output "server_public_ip" {
  value       = aws_instance.web_server.public_ip
  description = "The public IP of the newly created IaaS server"
}
```

By running `terraform apply`, AWS will parse this code, allocate physical hardware in their data center, spin up a hypervisor, and hand you the keys to the Virtual Machine in less than 60 seconds.

---

## Related Topics

- [Multi-Cloud vs Hybrid Cloud](../05-multi-cloud/multi-cloud-strategies.md) — Expanding beyond a single cloud provider.
- [Serverless Event-Driven Architectures](../04-serverless/event-driven-architectures.md) — The ultimate abstraction of Cloud computing, moving beyond IaaS/PaaS.
- [DevOps Engineering](../../06-devops-engineering/README.md) — The discipline that relies heavily on Cloud infrastructure to automate CI/CD pipelines.
