# Terraform

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ngày xưa, để thuê Máy chủ, Lập trình viên phải đăng nhập vào trang web của AWS, bấm chuột chọn CPU, chọn Ổ cứng, tạo Tường lửa (Firewall) bằng tay. Việc "bấm chuột" này (ClickOps) có 3 hậu quả thảm khốc: Rất chậm, dễ bấm nhầm gây lỗi mạng, và Không thể lặp lại (Nếu AWS xóa tài khoản của bạn, bạn mất luôn hệ thống vì không nhớ nổi mình đã bấm những nút gì). Công ty HashiCorp đã tạo ra **Terraform** để khai sinh ra khái niệm **Infrastructure as Code (Hạ tầng là Mã nguồn)**. Thay vì bấm chuột, bạn mô tả kiến trúc mạng của mình bằng một đoạn Text (Ngôn ngữ HCL). Bạn gõ lệnh `terraform apply`, Terraform sẽ chạy ra ngoài nói chuyện với AWS API và tự động xây dựng hoàn chỉnh 100 máy chủ, 50 tường lửa y hệt như những gì bạn viết. Hệ thống mạng hàng triệu đô của công ty giờ đây được lưu trữ an toàn dưới dạng File Text trên Github.

</details>

> **Summary**: Managing cloud infrastructure manually via a Web GUI (ClickOps) or bash scripts is an anti-pattern. It leads to configuration drift, irreproducibility, and massive security vulnerabilities due to human error. **Terraform** by HashiCorp is the industry-standard tool for **Infrastructure as Code (IaC)**. It allows engineers to define entire Data Centers, Cloud VPCs, Kubernetes clusters, and Load Balancers using a declarative Configuration Language (HCL). You declare *what* you want (e.g., "I want 5 AWS EC2 instances"), and Terraform mathematically calculates the API calls necessary to achieve that state. Because infrastructure is now just text files, it can be version-controlled in Git, peer-reviewed via Pull Requests, and automatically provisioned via CI/CD pipelines. This ensures that a Staging environment is an exact, mathematically perfect replica of the Production environment.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn muốn Xây một Ngôi Nhà.
1. **ClickOps (Cách làm cũ)**: Bạn tự chạy ra chợ, mua gạch, tự trộn xi măng, tự gọi thợ điện, vừa xây vừa suy nghĩ. Xây xong, lỡ ngày mai bão thổi bay căn nhà, bạn khóc ròng vì không biết cách xây lại căn y hệt.
2. **Terraform (Bản vẽ Kiến trúc)**: Bạn KHÔNG đụng tay vào gạch. Bạn ngồi vào bàn, vẽ ra một Bản Vẽ chi tiết: "Nhà 3 lầu, 4 phòng ngủ, sơn màu xanh". Bạn đưa bản vẽ này cho một **Ông Thầu Xây Dựng (Terraform)**. Ông thầu tự gọi thợ, tự xây lên cái nhà y hệt bản vẽ trong chớp mắt. Lỡ nhà sập? Bạn chỉ cần cầm bản vẽ đó đưa cho thầu, 5 phút sau bạn có cái nhà mới y hệt.

</details>

Imagine configuring a Smart Home.
1. **ClickOps**: You walk into every room, manually setting the thermostat to 72°, turning the lights to 50%, and locking the doors. If the power goes out and resets everything, you have to walk to every room and manually press all those buttons again from memory.
2. **Terraform (Declarative IaC)**: You write a text document: *"Rule 1: All thermostats must be 72°. Rule 2: All lights must be 50%."* You hand this document to a Robot Butler (Terraform). The robot runs around the house and presses the buttons for you. If the power goes out, you just hand the document to the robot again, and it perfectly restores the entire house to exactly how it was.

---

## Layer 1: Core Concepts (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Terraform hoạt động dựa trên 3 trụ cột khái niệm:
1. **Mã nguồn (HCL - HashiCorp Configuration Language)**: Đây là ngôn ngữ lập trình của Terraform. Bạn dùng nó để khai báo các `resource` (Tài nguyên). Ví dụ: `resource "aws_instance" "my_server" { ... }`.
2. **State (Bản ghi nhớ Trạng thái)**: Đây là "Bộ não" của Terraform. Giả sử bạn gõ lệnh tạo 5 máy chủ. Lần sau, bạn đổi số 5 thành số 6. Làm sao Terraform biết chỉ cần tạo thêm 1 cái thay vì tạo mới cả 6 cái? Terraform dựa vào **File State** (Một file JSON bí mật ghi nhớ lại những gì nó đã tạo ra trước đó ở ngoài đời thực).
3. **Providers (Thợ thông dịch API)**: Terraform không chỉ hiểu AWS. Nó có hàng ngàn Providers do cộng đồng viết. Bạn khai báo `provider "aws"`, nó sẽ tải từ điển dịch ra lệnh của AWS. Khai báo `provider "google"`, nó sẽ dịch lệnh xây máy chủ chạy lên Google Cloud. Bạn dùng chung 1 ngôn ngữ HCL để điều khiển mọi Cloud trên thế giới.

</details>

Terraform operates on a completely declarative paradigm driven by three core components:
1. **Declarative Configuration (HCL)**: You do not write imperative loops (`for i in 1..5: createServer()`). You write declarative blocks using HashiCorp Configuration Language. You state the desired end-state: `resource "aws_instance" "web" { count = 5 }`. Terraform figures out the "How".
2. **The State File (`terraform.tfstate`)**: The source of truth and the most critical part of Terraform. It is a JSON file that maps the resources defined in your code to the real-world resources currently existing in AWS. When you change `count = 5` to `count = 6`, Terraform compares the code to the State file, realizes 5 already exist, and mathematically calculates that it only needs to issue exactly 1 API call to create 1 new server. (This state file must be stored securely in a remote backend like S3, never in Git).
3. **Providers**: The plugin ecosystem. Terraform Core doesn't know how to talk to AWS. It relies on the `aws` Provider (a binary plugin written in Go) to translate the HCL generic code into specific AWS REST API `POST` requests. There are providers for everything: AWS, GCP, Azure, Cloudflare, GitHub, and Datadog.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Terraform sinh ra để giải quyết 3 bài toán lớn nhất của Hạ tầng:
1. **Tính Nhất quán (Môi trường Test và Prod)**: Công ty thường có Môi trường Test (Cho Lập trình viên phá) và Môi trường Prod (Cho Khách hàng dùng). Nếu thiết lập bằng tay, sớm muộn gì 2 môi trường này cũng bị lệch cấu hình (Môi trường Test chạy được, Prod chết). Khi dùng Terraform, bạn chỉ có 1 file Code. Chạy file đó ở Test, thu được 1 Cụm y hệt Prod. Loại bỏ 100% lỗi do con người.
2. **Phục hồi sau thảm họa (Disaster Recovery)**: Hacker đánh cắp mật khẩu, vào tài khoản AWS của bạn Xóa toàn bộ máy chủ và Database. Công ty bạn sẽ phá sản nếu thao tác bằng tay. Với Terraform, bạn chỉ cần tạo tài khoản AWS mới, nhập Key mới, gõ lệnh `terraform apply`, 15 phút sau toàn bộ hệ thống khổng lồ được xây dựng lại nguyên vẹn như phép màu.
3. **Sự kết hợp đa Đám mây (Multi-Cloud)**: Nếu bạn dùng công cụ độc quyền của AWS (CloudFormation), bạn bị nhốt chặt ở AWS. Terraform là tiêu chuẩn mã nguồn mở. Nó cho phép bạn viết 1 dự án: Xây Database ở AWS, Xây Load Balancer ở Google Cloud, cấu hình DNS ở Cloudflare, tất cả quy tụ chung trong 1 tệp lệnh duy nhất.

</details>

Why is Terraform universally adopted over Cloud-native tools like AWS CloudFormation or simple Bash scripts?
1. **Idempotency and Consistency**: Bash scripts are imperative and dangerous. If a script fails halfway through creating 10 servers, running it again might create 10 *more* servers. Terraform is Idempotent. You can run `terraform apply` 100 times, and if the AWS environment already matches the Code, Terraform will safely do absolutely nothing. This guarantees Staging and Production are identical.
2. **Disaster Recovery (RTO/RPO)**: If an administrative error drops an entire AWS Region, reconstructing complex VPC peering, Subnets, and Security Groups manually from memory takes weeks. With Terraform, the entire architecture is mathematically defined in Git. Recreating the entire global infrastructure in a different Region is as simple as changing a variable and typing `terraform apply`.
3. **The Multi-Cloud Workflow**: AWS CloudFormation only works on AWS. Azure Bicep only works on Azure. Terraform is the undisputed Multi-Cloud lingua franca. A single Terraform workspace can provision DNS records on Cloudflare, boot EC2 instances on AWS, and configure PagerDuty alerts simultaneously, treating the entire internet ecosystem as a unified programmable API.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình "Tìm Lỗi" (Auditing) khi hệ thống Đột nhiên bị sập.
</details>

Visualizing Infrastructure Auditing.

| Metric | Manual Cloud Console (ClickOps) | Infrastructure as Code (Terraform) |
|---|---|---|
| **The Incident** | The website suddenly goes offline. | The website suddenly goes offline. |
| **Investigation** | The DevOps team logs into AWS, frantically clicking through 50 menus trying to figure out if someone accidentally deleted a Firewall rule. Nobody knows what happened. Takes 4 hours. | The DevOps team checks the Git Repository. They see a Pull Request merged 5 minutes ago by John: `Deleted port 443 from security_group.tf`. The root cause is identified instantly. |
| **Resolution** | Try to remember what the rule was and re-type it manually. | Click `Revert Git Commit` and the CI/CD pipeline instantly fixes the firewall. Takes 2 minutes. |

---

## Layer 4: The Terraform Workflow

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Quá trình làm việc với Terraform cực kì an toàn và luôn tuân theo 3 bước chuẩn mực:
1. `terraform init`: Cài đặt ban đầu. Tải các thư viện (Providers) từ mạng về. (Giống lệnh `npm install`).
2. `terraform plan`: **Bước Phác Thảo (Cực kì quan trọng)**. Nó KHÔNG HỀ chạm vào AWS. Nó chỉ đọc Code, so sánh với đời thực, và in ra màn hình một Danh sách: *"Sếp ơi, nếu sếp cho phép, em sẽ Xây thêm 2 máy chủ, Sửa đổi 1 cái Firewall, và XÓA 1 cái Database"*. Sếp đọc bảng danh sách này, nếu thấy chữ "XÓA" màu đỏ, sếp lập tức dừng lại để tránh thảm họa mất dữ liệu.
3. `terraform apply`: Bước Thực thi. Khi sếp gật đầu với bản phác thảo ở trên, gõ lệnh này. Terraform sẽ ra ngoài Internet, gọi API và biến bản phác thảo thành hiện thực.

</details>

Terraform operates on a strict, fail-safe CLI workflow designed to prevent catastrophic infrastructure mistakes:
1. **`terraform init`**: The initialization phase. It analyzes your `.tf` files, identifies required Providers (e.g., AWS, GCP), downloads their binary plugins, and establishes the connection to the remote State backend.
2. **`terraform plan` (The Dry Run)**: The most critical command. Terraform performs a "Dry Run". It mathematically compares the current real-world AWS State against your local HCL code. It then outputs an execution plan (a diff): *“I will CREATE 1 EC2 instance, I will MODIFY 1 Security Group, and I will DESTROY 1 RDS Database.”* This allows engineers to catch destructive actions (like accidental DB deletion) *before* they ever happen.
3. **`terraform apply`**: The execution phase. Once the human operator reviews the `plan` and types "yes", Terraform concurrently executes the necessary REST API calls to the Cloud Providers to mutate the infrastructure to match the code.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Remote State File (Khóa file trạng thái trên Đám mây)**: Mặc định, file State (bộ não của Terraform) nằm trên máy tính của bạn (`terraform.tfstate`). Nếu 2 lập trình viên cùng gõ lệnh `apply` một lúc, file State sẽ bị rách, AWS sẽ bị lỗi tạo trùng 2 máy chủ. *BẮT BUỘC* phải cấu hình lưu file State này lên Cloud (Ví dụ: Lưu vào AWS S3, và dùng bảng AWS DynamoDB làm "Ổ khóa"). Khi Dev A đang chạy lệnh, ổ khóa khóa lại, Dev B bấm lệnh sẽ bị cấm cho đến khi Dev A chạy xong.
2. **Sử dụng Modules (Code Tái sử dụng)**: Đừng bao giờ viết code tạo Máy ảo lặp đi lặp lại 10 lần. Hãy viết 1 cái Module "Tạo máy chủ chuẩn của công ty" (Đã cài sẵn Firewall bảo mật). Các Dev khác trong công ty chỉ việc gọi Module đó ra xài. Đảm bảo mọi máy chủ tạo ra đều an toàn.

</details>

1. **Remote State with State Locking**: By default, Terraform stores its critical state file locally on your laptop. If Developer A and Developer B both run `terraform apply` simultaneously on their laptops, a race condition occurs, causing massive infrastructure corruption and duplicate API calls. **Absolute Rule**: In a team environment, you MUST configure a "Remote Backend". Store the `terraform.tfstate` file in a centralized, versioned AWS S3 Bucket, and utilize an AWS DynamoDB table to enforce **State Locking**. This guarantees that only one pipeline can mutate the infrastructure at any given microsecond.
2. **Modularize and Parameterize**: Do not hardcode infrastructure logic in a single massive `main.tf` file. Follow software engineering principles. Create generalized Terraform Modules (e.g., `vpc-module`, `eks-module`). Instead of hardcoding `"us-east-1"`, pass it as a `var.region` variable. This allows you to reuse the exact same Module code to deploy a `Staging` cluster in Ohio and a `Production` cluster in Tokyo simply by passing different `terraform.tfvars` files.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lộ Mật khẩu trong File State**: Đây là tử huyệt của Terraform. Khi bạn dùng Terraform tạo một cái Database kèm Mật khẩu, Terraform BẮT BUỘC phải ghi lại cái Mật khẩu rành rành bằng chữ thường (Plaintext) vào bên trong File State `terraform.tfstate` để ghi nhớ. Nếu bạn lỡ tay đẩy file State này lên Github, Hacker sẽ thấy toàn bộ mật khẩu Database của bạn. *Luật: File State chứa bí mật cấp quốc gia. Tuyệt đối không bao giờ cho nó lên Git (Phải thêm vào `.gitignore`).*
2. **Trôi dạt cấu hình (Configuration Drift)**: Bạn dùng Code Terraform để xây 1 cái Máy chủ. Chiều nay, hệ thống bị sập khẩn cấp, Sếp của bạn sợ quá nên đăng nhập thẳng vào trang web AWS bấm chuột tay sửa lại Firewall cho nhanh. Lúc này, Code Terraform trên máy và thực tế AWS ĐÃ BỊ LỆCH NHAU (Drift). Ngày mai, bạn chạy `terraform apply`, Terraform thấy AWS không giống Code, nó sẽ lạnh lùng **XÓA BỎ** cái Firewall sếp vừa sửa hôm qua để ép hệ thống quay về đúng như Code. Hệ thống sập lần 2. *Luật: Đã dùng Terraform thì cấm tuyệt đối con người vào Web AWS bấm chuột sửa tay.*

</details>

1. **State File Plaintext Secrets Leakage**: The most dangerous vulnerability in Terraform. Because Terraform must track the exact state of resources, any passwords, API keys, or DB credentials passed into Terraform are stored in the `terraform.tfstate` file in **completely unencrypted plaintext**. If a junior developer accidentally commits `terraform.tfstate` to the Git repository, the entire cloud infrastructure is compromised. **Rule**: Always add `*.tfstate` to `.gitignore`. Remote State buckets (S3) must be strictly encrypted at rest (KMS) and locked down with IAM policies so only the CI/CD bot can read them.
2. **Configuration Drift and Manual Mutability**: You deploy a security group via Terraform. During a late-night outage, a SysAdmin logs into the AWS Web Console and manually opens Port 22 (SSH) to debug the issue. This creates "Configuration Drift". The AWS reality no longer matches the Git Terraform code. The next morning, a developer runs `terraform apply` for an unrelated change. Terraform detects the manual Port 22, realizes it's not in the code, and mathematically deletes it, instantly killing the SysAdmin's SSH connection. **Rule**: Once Terraform manages a resource, human GUI ClickOps are strictly forbidden. All changes MUST go through the code.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Cấu trúc 1 file Terraform cơ bản (main.tf) để tạo 1 cái Máy ảo trên AWS.
</details>

### The Essential `main.tf` Example
```hcl
# 1. Define the Provider (Tell Terraform we are talking to AWS)
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Region
provider "aws" {
  region = "us-east-1"
}

# 2. Define a Resource (Create an AWS EC2 Virtual Machine)
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0" # Ubuntu Linux OS Image ID
  instance_type = "t2.micro"              # The size of the VM (Free tier)

  # Tags are crucial for billing and identification
  tags = {
    Name        = "Production-Web-Server"
    Environment = "Prod"
  }
}

# 3. Define an Output (Print the IP address to the screen after it's built)
output "server_public_ip" {
  value       = aws_instance.web_server.public_ip
  description = "The public IP address of the newly created server."
}
```

### Essential CLI Commands
```bash
# Initialize the directory, download the AWS plugins
terraform init

# Check the syntax of your HCL code for typos
terraform validate

# The DRY RUN. Shows exactly what WILL happen without changing anything.
# (Look for green + (add), yellow ~ (change), red - (destroy))
terraform plan

# Execute the plan and build the infrastructure
terraform apply

# DANGER: Tear down and delete every single resource defined in the code
terraform destroy
```

---

## Related Topics

- Terraform is the language used to command Cloud Providers like **[AWS](./aws.md)**.
- While Terraform builds the hardware, tools like **[Docker](./docker.md)** and **[Kubernetes](./kubernetes.md)** run the software on top of that hardware.
