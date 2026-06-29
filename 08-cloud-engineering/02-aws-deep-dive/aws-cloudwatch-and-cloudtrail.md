# AWS CloudWatch & CloudTrail

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Camera an ninh và bác sĩ khám bệnh của tài khoản AWS. Tìm hiểu cách phân biệt CloudWatch (Đo lường hiệu suất "CÁI GÌ đang xảy ra?") và CloudTrail (Kiểm toán bảo mật "AI vừa làm cái đó?"). Đây là kiến thức bắt buộc cho bất kỳ DevOps nào.

</details>

> **Summary**: The security cameras and health monitors of your AWS account. Learn the crucial difference between CloudWatch (Performance Monitoring: "WHAT is happening?") and CloudTrail (Security Auditing: "WHO did that?"). Mandatory knowledge for any Cloud Engineer.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Giả sử tài khoản AWS của bạn là một chiếc máy bay khổng lồ.
- **CloudWatch (Bảng đồng hồ lái)**: Nó cho phi công biết tốc độ gió là bao nhiêu, động cơ bên trái đang nóng bao nhiêu độ (Metrics), và báo động đỏ (Alarms) nếu máy bay sắp hết xăng. Nó quan tâm đến **"Cái gì" đang diễn ra bên trong hệ thống**.
- **CloudTrail (Hộp đen an ninh)**: Một kẻ xấu lẻn vào buồng lái và lén tắt động cơ. CloudWatch sẽ báo động: "Động cơ đã tắt!". Nhưng CloudWatch KHÔNG BIẾT AI đã tắt nó. Bạn mở CloudTrail ra xem, nó sẽ ghi rành rành: "Lúc 2:00 AM, tên hacker có IP 192.x.x.x đã dùng tài khoản John để bấm nút Tắt Động Cơ". Nó quan tâm đến **"Ai" đã làm gì với tài khoản AWS của bạn**.

</details>

Assume your AWS account is a massive commercial airplane.
- **Amazon CloudWatch (The Dashboard Dials)**: It tells the pilot the wind speed, the temperature of the left engine (Metrics), and triggers a loud red flashing light (Alarms) if the plane is running out of fuel. It is strictly concerned with **"WHAT is happening inside the system physically"**.
- **AWS CloudTrail (The Black Box Security Camera)**: A malicious actor sneaks into the cockpit and secretly turns off the engine. CloudWatch will scream: "The engine is off!". But CloudWatch DOES NOT KNOW WHO turned it off. You open CloudTrail, and it explicitly states: "At 2:00 AM, a hacker from IP 192.x.x.x used IAM User 'John' to click the 'Stop Engine' button". It is strictly concerned with **"WHO did what to your AWS infrastructure"**.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Amazon CloudWatch**: Dịch vụ Giám sát (Monitoring) và Quản lý (Management). Thu thập dữ liệu hoạt động dưới dạng Nhật ký (Logs), Chỉ số (Metrics) và Sự kiện (Events). Cung cấp cái nhìn toàn cảnh về tài nguyên AWS và ứng dụng của bạn.
- **AWS CloudTrail**: Dịch vụ Kiểm toán (Auditing) và Tuân thủ (Compliance). Nó ghi lại TẤT CẢ mọi lời gọi API (API calls) được thực hiện trong tài khoản AWS của bạn (Dù bạn bấm nút trên web, dùng AWS CLI, hay gọi bằng code Python).

</details>

- **Amazon CloudWatch**: A Monitoring and Management service. It collects operational data in the form of Logs, Metrics, and Events. It provides a unified view of AWS resources, applications, and services that run on AWS and on-premises servers.
- **AWS CloudTrail**: An Auditing, Governance, and Compliance service. It continuously records EVERY single API call made within your AWS account (Whether the action was performed via the AWS Management Console Web UI, the AWS CLI, or SDKs like Boto3).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu bạn mở một máy chủ EC2 tự quản lý (On-Premise), bạn phải tự cất công cài đặt các công cụ như Prometheus hay Zabbix để vẽ biểu đồ xem RAM/CPU có bị đầy không. Rất mất thời gian. **CloudWatch** tồn tại để làm việc đó tự động. Bất cứ khi nào bạn bật 1 dịch vụ AWS (EC2, RDS, Lambda), AWS TỰ ĐỘNG gửi các chỉ số CPU/RAM về CloudWatch để bạn xem.

Khi công ty bạn lớn lên, có 50 lập trình viên dùng chung 1 tài khoản AWS. Một buổi sáng, Database Production tự nhiên bốc hơi (Bị xóa). 50 lập trình viên đều nói "Không phải em làm!". Không có **CloudTrail**, bạn sẽ không bao giờ tìm ra thủ phạm. CloudTrail tồn tại như một bằng chứng pháp lý không thể chối cãi để điều tra sự cố.

</details>

If you run traditional On-Premise servers, you must manually install complex monitoring agents like Prometheus or Zabbix to generate CPU/RAM graphs. This is tedious. **CloudWatch** exists to provide out-of-the-box observability. The moment you provision an EC2, RDS, or Lambda resource, AWS AUTOMATICALLY streams default metrics directly to CloudWatch without you installing anything.

As your company scales, 50 developers might share one AWS account. One morning, the Production Database vanishes (Someone deleted it). All 50 developers claim "It wasn't me!". Without **CloudTrail**, you have zero visibility and cannot prove anything. CloudTrail exists as an immutable legal audit log. It is the undeniable proof of who did what, from where, and when.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**3 Cột trụ của CloudWatch:**
1. **CloudWatch Metrics**: Biểu đồ. (Ví dụ: CPU máy EC2 đang ở mức 90%, DynamoDB đang tiêu thụ 500 Read Capacity).
2. **CloudWatch Alarms**: Còi báo động. (Ví dụ: NẾU CPU > 90% TRONG 5 PHÚT -> Kích hoạt Auto Scaling gọi thêm EC2, và gửi email báo cho DevOps).
3. **CloudWatch Logs**: Nơi chứa chữ (Text). Mọi lệnh `console.log()` hoặc `print()` trong code Lambda/EC2 của bạn sẽ chạy thẳng vào đây để bạn gỡ lỗi.

</details>

### The 3 Pillars of Amazon CloudWatch

1. **CloudWatch Metrics**: The quantitative data points (Graphs/Charts). Example: EC2 CPU Utilization is at 90%, RDS Database free storage space is under 5GB, DynamoDB Consumed Read Capacity Units.
2. **CloudWatch Alarms**: The reactive trigger mechanism. You set a threshold: `IF (EC2 CPU > 80%) FOR (5 consecutive minutes) -> THEN (Trigger Auto Scaling to add 1 more instance AND send an SNS email to the DevOps team)`.
3. **CloudWatch Logs**: The qualitative text data. Every time your Node.js code executes a `console.log()` or Python executes a `print()`, those text lines are natively streamed into CloudWatch Logs so you can search them for errors (e.g., searching for "NullPointerException").

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Tự động mở rộng (Auto Scaling với CloudWatch)**: Đặt báo động CloudWatch nếu Số lượng Request vào Load Balancer tăng vọt, tự động đẩy cảnh báo cho EC2 Auto Scaling Group để sinh thêm máy chủ.
2. **Billing Alarm (Báo động tiền bạc)**: Đây là việc **ĐẦU TIÊN** bạn phải làm khi tạo tài khoản AWS! Đặt CloudWatch Alarm: "Nếu hóa đơn tháng này vượt quá $10, bắn tin nhắn cảnh báo ngay lập tức". Rất nhiều sinh viên bị trừ oan hàng ngàn đô la vì quên làm việc này.
3. **Pháp y điện tử (CloudTrail Forensics)**: Một tên hacker đánh cắp Access Key của bạn, hắn dùng key đó tạo ra 50 máy chủ EC2 đào Bitcoin (Rất phổ biến). Bạn dùng CloudTrail để điều tra xem hắn đã dùng IP nào, và gọi những lệnh API nào để xóa sạch mọi thứ hắn tạo ra, sau đó nộp bằng chứng cho AWS để xin hoàn tiền.

**Không nên làm (Anti-patterns):**
- **In thông tin nhạy cảm ra Log**: Tuyệt đối không dùng `console.log(user_password)` hoặc in ra số Thẻ tín dụng trong code. Vì nó sẽ được lưu thẳng vào CloudWatch Logs, và bất kỳ nhân viên nào có quyền xem Log đều có thể ăn cắp thẻ tín dụng của khách.

</details>

1. **Automated Elasticity (CloudWatch Alarms)**: Setting an alarm on an Application Load Balancer metric (`RequestCountPerTarget`). If traffic spikes, the alarm triggers the EC2 Auto Scaling Group to provision 3 new servers, completely automating scaling without human intervention.
2. **The Billing Alarm (Crucial)**: The **ABSOLUTE FIRST THING** you must do on a new AWS account. Create a CloudWatch Alarm for `EstimatedCharges > $10`. If you accidentally leave a massive Redshift cluster running, the alarm will email you before you rack up a $5,000 bill at the end of the month.
3. **Security Forensics (CloudTrail)**: A hacker steals an IAM Access Key from a public GitHub repo. They use it to spin up 50 massive GPU EC2 instances in the `ap-northeast-3` region to mine Bitcoin. You use CloudTrail to meticulously trace every single `RunInstances` API call they made, identify exactly what resources they created, destroy them, and submit the CloudTrail logs to AWS Support as proof to request a billing refund.

### Anti-Patterns
- **Logging Sensitive Data (PII/PCI)**: Never execute `console.log(user.creditCard)` or print unencrypted passwords in your backend code. AWS natively captures standard output streams. That sensitive data will be permanently written in plain text to CloudWatch Logs, causing a catastrophic compliance violation (PCI-DSS) where any junior developer with read-access to logs can steal credit cards.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. CloudWatch Log Insights (Truy vấn Log siêu tốc)**
Nếu bạn có 100 GB file log, việc cuộn chuột tìm lỗi là bất khả thi. AWS cung cấp tính năng **Log Insights**. Nó cho phép bạn dùng cú pháp giống hệt SQL để truy vấn log.
Ví dụ: `Lọc ra tất cả các dòng log có chứa chữ "ERROR", đếm số lượng, và xếp hạng 10 lỗi xuất hiện nhiều nhất`. Tốc độ quét là vài giây!

**2. Bật CloudTrail đa khu vực (Multi-Region Trail)**
Mặc định, CloudTrail cung cấp lịch sử 90 ngày miễn phí. Nhưng hacker rất khôn ngoan. Nếu chúng trộm tài khoản của bạn, chúng thường đổi khu vực sang một nước rất lạ (Ví dụ: Nam Phi - `af-south-1`) để đào Bitcoin, vì biết bạn hiếm khi check khu vực đó.
*Best Practice*: Phải tạo một Trail lưu vào S3 bucket và bật tùy chọn **Apply to all regions**. Nó sẽ bắt gọn mọi hành động của hacker ở bất kỳ quốc gia nào trên thế giới.

</details>

### 1. CloudWatch Logs Insights (Querying Logs)
When your microservices generate 100GB of text logs per day, manually scrolling to find a bug is impossible. AWS provides **CloudWatch Logs Insights**, a purpose-built query language (similar to SQL/Splunk).
You can write queries like: "Filter all log streams for the word 'Exception', parse out the specific Error Code, count the occurrences, and group them by the Lambda function name, sorted descending." It scans massive log files in seconds, vastly accelerating debugging during production incidents.

### 2. Multi-Region CloudTrail (The Security Best Practice)
By default, the AWS Console shows you 90 days of CloudTrail history for the Region you are currently looking at (e.g., `us-east-1`).
Hackers know this. When they steal credentials, they actively switch to obscure, rarely used regions (like `sa-east-1` São Paulo or `af-south-1` Cape Town) to spin up Bitcoin mining EC2s, hoping you won't notice.
*The DevOps Best Practice*: You must explicitly create a permanent Trail that delivers logs to an Amazon S3 Bucket, and you MUST check the box: **"Apply to all regions"**. This ensures that no matter where in the world a hacker tries to execute an API call, it is permanently recorded in your centralized S3 audit bucket.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đoạn Terraform này thiết lập hệ thống Báo động Thanh toán (Billing Alarm) quan trọng nhất. Nó sẽ gửi Email cho bạn ngay lập tức nếu tiền điện toán đám mây của bạn vượt qua $50.

</details>

### Provisioning a CloudWatch Billing Alarm (Terraform)

This is the most critical CloudWatch Alarm you will ever write. It prevents bankruptcy.

```hcl
# 1. Create an SNS Topic (The megaphone to send the email)
resource "aws_sns_topic" "billing_alerts" {
  name = "billing-alerts-topic"
}

# 2. Subscribe your personal email to the SNS Topic
resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.billing_alerts.arn
  protocol  = "email"
  endpoint  = "devops-team@mycompany.com" # You must click the confirmation link sent to this email!
}

# 3. Create the CloudWatch Metric Alarm
resource "aws_cloudwatch_metric_alarm" "billing_alarm" {
  alarm_name          = "account-billing-alarm-50-usd"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "EstimatedCharges"
  namespace           = "AWS/Billing"
  period              = 21600 # Evaluate every 6 hours (in seconds)
  statistic           = "Maximum"
  
  # The Threshold: Trigger the alarm if the bill hits $50.00
  threshold           = 50.00 

  # The metric requires this specific dimension to work correctly
  dimensions = {
    Currency = "USD"
  }

  # 4. The Action: If the threshold is breached, trigger the SNS Topic!
  alarm_actions = [aws_sns_topic.billing_alerts.arn]
}
```

---

## Related Topics

- [AWS IAM](./aws-iam.md) — CloudTrail monitors exactly which IAM Users and Roles are executing commands.
- [AWS EC2 Auto Scaling](./aws-ec2.md) — CloudWatch Alarms are the brain that tells Auto Scaling when to trigger.
- [DevOps: Monitoring & Observability](../../06-devops-engineering/README.md) — How CloudWatch fits into the broader DevOps culture of continuous monitoring.
