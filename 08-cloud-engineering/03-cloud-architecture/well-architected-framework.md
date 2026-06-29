# AWS Well-Architected Framework

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Bộ 6 nguyên tắc vàng của AWS giúp bạn xây dựng hệ thống đám mây an toàn, hiệu suất cao, kiên cường và tiết kiệm. Đây không phải là code, đây là tư duy thiết kế (Mindset) bắt buộc phải có đối với mọi Kỹ sư Đám mây.

</details>

> **Summary**: The 6 Golden Pillars of AWS that help you build secure, high-performing, resilient, and efficient infrastructure. This is not about code; this is the mandatory architectural mindset for every Cloud Engineer.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Giả sử bạn xây một tòa lâu đài (Hệ thống Cloud):
1. **Vận hành xuất sắc**: Bạn có lính gác đi tuần mỗi giờ và hệ thống báo cháy tự động không? (Có giám sát và tự động hóa không?)
2. **Bảo mật**: Cửa thành có khóa chắc chắn không? Lính gác có kiểm tra giấy tờ mọi người ra vào không?
3. **Độ tin cậy**: Nếu một góc tường bị sập do động đất, tòa lâu đài có đứng vững không, hay sụp đổ toàn bộ?
4. **Hiệu suất**: Khi có 10,000 khách đến dự tiệc, lâu đài có đủ bếp và nhà vệ sinh để phục vụ nhanh chóng không?
5. **Tối ưu chi phí**: Bạn có đang thắp sáng 100 căn phòng trống không ai ở không? (Lãng phí tiền điện).
6. **Bền vững**: Lâu đài của bạn có xả rác ra sông và phá hủy môi trường xung quanh không?

</details>

Assume you are building a medieval Castle (Your Cloud Infrastructure):
1. **Operational Excellence**: Do you have guards patrolling every hour and automatic fire alarms? (Do you monitor logs and automate deployments?)
2. **Security**: Are the gates heavily locked? Do guards check the ID of every single person entering? (IAM and Encryption).
3. **Reliability**: If an earthquake destroys the East Wall, does the entire castle collapse, or can it stand on the remaining walls? (Fault Tolerance).
4. **Performance Efficiency**: When 10,000 guests arrive for a banquet, do you have enough kitchens to serve them quickly? (Auto Scaling).
5. **Cost Optimization**: Are you burning expensive candles in 100 empty rooms where no one sleeps? (Wasting money on idle servers).
6. **Sustainability**: Is your castle dumping toxic waste into the local river? (Energy consumption and carbon footprint).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**AWS Well-Architected Framework** là một tập hợp các phương pháp hay nhất (Best Practices) được AWS đúc kết từ việc phục vụ hàng triệu khách hàng. Nó giúp các Kiến trúc sư phần mềm (Cloud Architects) đánh giá hệ thống của họ và thiết kế ra những kiến trúc có khả năng mở rộng tốt.

Nó bao gồm **6 Trụ cột (6 Pillars)**:
1. Operational Excellence (Vận hành xuất sắc)
2. Security (Bảo mật)
3. Reliability (Độ tin cậy)
4. Performance Efficiency (Hiệu suất)
5. Cost Optimization (Tối ưu chi phí)
6. Sustainability (Bền vững)

</details>

The **AWS Well-Architected Framework** is a set of best practices distilled by AWS from reviewing millions of customer architectures. It provides a consistent approach for Cloud Architects to evaluate architectures and implement scalable designs.

It is composed of **6 Pillars**:
1. Operational Excellence
2. Security
3. Reliability
4. Performance Efficiency
5. Cost Optimization
6. Sustainability

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đám mây mang lại sức mạnh to lớn, nhưng "Quyền lực lớn đi kèm trách nhiệm lớn". 
Một Junior Developer có thể viết code rất giỏi, lên AWS bấm nút tạo máy chủ rất nhanh. Nhưng nếu họ tạo máy chủ mở port công khai 22 (Lỗi Bảo mật), mua ổ cứng quá to không dùng hết (Lỗi Chi phí), và chỉ đặt máy chủ ở 1 tòa nhà duy nhất (Lỗi Độ tin cậy), thì dự án đó sẽ trở thành thảm họa khi ra mắt thực tế.

Framework này tồn tại để làm một "Bảng kiểm tra sức khỏe" (Checklist). Trước khi hệ thống Go-Live, Giám đốc Công nghệ (CTO) sẽ dùng Framework này để rà soát toàn bộ kiến trúc, đảm bảo không có lỗ hổng chết người nào.

</details>

The Cloud provides immense power, but "With great power comes great responsibility".
A Junior Developer might write excellent code and provision an EC2 instance in 5 minutes. But if they leave SSH Port 22 open to the world (Security Failure), provision a massively oversized hard drive they don't need (Cost Failure), and deploy the server in only a single Availability Zone (Reliability Failure), the project will be a catastrophic disaster in Production.

This Framework exists as a structural Checklist. Before a system goes live, Cloud Architects use the Well-Architected Tool to review the architecture, answering a series of strict questions to ensure no fatal architectural flaws make it into Production.

---

## Layer 3 & 4: Deep Dive into the 6 Pillars

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy đi sâu vào từng trụ cột và cách áp dụng chúng vào thực tế.

</details>

Let's break down exactly what each pillar means and how to apply them.

### 1. Operational Excellence (Vận hành xuất sắc)
*The ability to support development and run workloads effectively, gain insight into their operations, and continuously improve.*

- **ELI5**: Đừng thao tác bằng tay. Hãy tự động hóa mọi thứ.
- **Design Principles**: 
  - **Perform operations as code**: Use Infrastructure as Code (Terraform, CloudFormation) instead of clicking in the Web Console.
  - **Make frequent, small, reversible changes**: Use CI/CD pipelines.
- **Key AWS Services**: AWS CloudFormation, AWS CloudTrail, AWS CloudWatch.

### 2. Security (Bảo mật)
*The ability to protect data, systems, and assets to take advantage of cloud technologies to improve your security.*

- **ELI5**: Không tin tưởng ai cả. Khóa mọi cánh cửa. Cấp quyền ít nhất có thể.
- **Design Principles**:
  - **Apply security at all layers**: Don't just rely on a firewall. Protect the VPC, the EC2 OS, the Database, and the App code. (Defense in depth).
  - **Principle of Least Privilege**: Give users the absolute minimum permissions needed.
  - **Protect data in transit and at rest**: Always use HTTPS (SSL) and encrypt EBS/S3 data using AWS KMS.
- **Key AWS Services**: AWS IAM, AWS KMS (Key Management Service), AWS WAF, Security Groups.

### 3. Reliability (Độ tin cậy)
*The ability of a workload to perform its intended function correctly and consistently when it’s expected to.*

- **ELI5**: Thiết kế hệ thống sao cho khi một máy tính bị cháy, hệ thống vẫn chạy bình thường.
- **Design Principles**:
  - **Automatically recover from failure**: Use Auto Scaling. If a server dies, Auto Scaling detects it and spins up a new one instantly.
  - **Scale horizontally to increase aggregate workload availability**: Replace one giant EC2 instance with 10 smaller EC2 instances.
  - **Stop guessing capacity**: In the cloud, you can provision resources on-demand. Don't buy servers you *might* need next year.
- **Key AWS Services**: Multi-AZ RDS, EC2 Auto Scaling, Route 53 (Health Checks).

### 4. Performance Efficiency (Hiệu suất)
*The ability to use computing resources efficiently to meet system requirements, and to maintain that efficiency as demand changes and technologies evolve.*

- **ELI5**: Sử dụng công nghệ mới nhất và phù hợp nhất cho công việc. Không lấy dao mổ trâu đi giết gà.
- **Design Principles**:
  - **Democratize advanced technologies**: Instead of building your own Machine Learning team, just use Amazon Rekognition via API.
  - **Go global in minutes**: Use CloudFront (CDN) to place your application physically closer to users worldwide to reduce latency.
  - **Use Serverless architectures**: Remove the burden of managing servers completely (Lambda, DynamoDB).
- **Key AWS Services**: AWS Lambda, Amazon CloudFront, Amazon ElastiCache (Redis).

### 5. Cost Optimization (Tối ưu chi phí)
*The ability to run systems to deliver business value at the lowest price point.*

- **ELI5**: Chỉ trả tiền cho những gì bạn thực sự dùng. Tắt điện khi ra khỏi phòng.
- **Design Principles**:
  - **Adopt a consumption model**: Pay only for the computing resources you consume, and increase or decrease usage depending on business requirements.
  - **Stop spending money on undifferentiated heavy lifting**: AWS does the data center racking, stacking, and powering. Use PaaS (RDS) instead of managing your own DB.
- **Key AWS Services**: AWS Cost Explorer, AWS Budgets, EC2 Spot Instances, S3 Lifecycle Policies.

### 6. Sustainability (Bền vững) - *Added in 2021*
*The environmental impact of the services used by your workloads.*

- **ELI5**: Mã lập trình kém hiệu quả sẽ ngốn nhiều điện năng của máy chủ, làm xả nhiều CO2 ra môi trường.
- **Design Principles**:
  - **Maximize utilization**: Don't run servers at 10% CPU. Pack them tightly (using Containers/ECS) to run at 80% CPU so you need fewer physical servers.
  - **Use managed services**: Sharing services (like S3) with other customers is drastically more energy-efficient than everyone having their own private hard drives.

---

## Layer 5: Deep Practice (The Well-Architected Tool)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**AWS Well-Architected Tool**
AWS cung cấp một công cụ miễn phí ngay trong giao diện điều khiển. Nó là một bài kiểm tra gồm khoảng 50 câu hỏi trắc nghiệm siêu khó.
Ví dụ câu hỏi Trụ cột Bảo mật: "Làm thế nào bạn quản lý thông tin xác thực cho máy chủ (Database Passwords)?"
- A) Tôi ghi trực tiếp mật khẩu vào code (Hardcode). (Hệ thống đánh dấu: LỖI NGHIÊM TRỌNG HRI - High Risk Issue).
- B) Tôi lưu mật khẩu trong file `.env` trên EC2.
- C) Tôi dùng dịch vụ AWS Secrets Manager. (Vượt qua bài kiểm tra).

Kỹ sư Cloud cấp cao sẽ phải trả lời 50 câu hỏi này, lấy báo cáo các lỗi HRI, và lên kế hoạch sửa chữa chúng.

</details>

### The AWS Well-Architected Tool (Console Service)
AWS provides a free tool inside the AWS Management Console to run this audit. It is a grueling, 50-question architectural exam about your specific workload.

**Example Security Question from the Tool:**
*"How do you manage credentials and secrets for your application?"*
- [ ] We hardcode database passwords in the source code. (Triggers a **High Risk Issue - HRI**).
- [ ] We store them in `.env` files on the EC2 instances.
- [X] We use AWS Secrets Manager and IAM Roles to fetch them dynamically. (Best Practice achieved).

Senior Cloud Architects use this tool to generate a PDF report of High Risk Issues (HRIs) and Medium Risk Issues (MRIs), which becomes the immediate engineering backlog to fix before the application is allowed to launch.

---

## Layer 6: Code Templates & Integration (Security Pillar Example)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là ví dụ áp dụng Trụ cột Bảo mật (Security Pillar): Không bao giờ lưu mật khẩu trong code. Hãy dùng AWS Secrets Manager và code Terraform để tự động sinh mật khẩu ngẫu nhiên cho Database.

</details>

### Applying the Security Pillar (Infrastructure as Code)

To satisfy the Security Pillar's mandate to "Protect Secrets", we NEVER hardcode database passwords. We use Terraform to randomly generate a secure password, store it directly in AWS Secrets Manager, and pass it to RDS without any human ever seeing it.

```hcl
# 1. Generate a strong, random password programmatically
resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# 2. Create an AWS Secrets Manager secret container
resource "aws_secretsmanager_secret" "db_secret" {
  name        = "production/rds/db_password"
  description = "Master password for Production Database"
}

# 3. Store the generated password securely inside the secret container
resource "aws_secretsmanager_secret_version" "db_secret_version" {
  secret_id     = aws_secretsmanager_secret.db_secret.id
  secret_string = jsonencode({
    username = "admin_user"
    password = random_password.db_password.result
  })
}

# 4. Create the Database, fetching the password dynamically
resource "aws_db_instance" "prod_db" {
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  username             = "admin_user"
  # FETCH THE PASSWORD DYNAMICALLY - No human ever sees it in the TF code!
  password             = jsondecode(aws_secretsmanager_secret_version.db_secret_version.secret_string)["password"]
  allocated_storage    = 20
}
```

---

## Related Topics

- [High Availability & Disaster Recovery](./ha-and-disaster-recovery.md) — Deep dive into the *Reliability* Pillar.
- [Cost Optimization Strategies](./cost-optimization.md) — Deep dive into the *Cost Optimization* Pillar.
- [AWS IAM](../02-aws-deep-dive/aws-iam.md) — The fundamental foundation of the *Security* Pillar.
