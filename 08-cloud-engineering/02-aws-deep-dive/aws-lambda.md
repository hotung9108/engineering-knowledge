# AWS Lambda (Serverless Compute)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Đỉnh cao của Cloud Computing. Khám phá mô hình Serverless, nơi bạn chỉ viết code, AWS tự lo toàn bộ máy chủ. Tìm hiểu cơ chế tính tiền theo mili-giây, Cold Starts (Khởi động lạnh) và kiến trúc Hướng sự kiện (Event-Driven).

</details>

> **Summary**: The pinnacle of Cloud Computing abstraction. Explore the Serverless paradigm where you only write code and AWS manages 100% of the servers. Understand millisecond billing, Cold Starts, and Event-Driven architectures.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Kiến trúc Server cũ (EC2/ECS)**: Giống như bạn thuê một tài xế taxi trả lương theo tháng. Dù bạn có đi xe hay không, bạn vẫn phải trả lương nguyên tháng cho ông ấy. Rất lãng phí.
- **AWS Lambda (Serverless)**: Giống như bạn dùng Grab/Uber. Khi bạn cần đi (Sự kiện xảy ra), bạn bấm nút gọi. Grab tới đón, chở bạn đi trong đúng 15 phút. Bạn trả tiền cho đúng 15 phút đó. Khi xuống xe, chiếc Grab biến mất. Không cần nuôi tài xế! Nếu có 1,000 người cùng gọi Grab, hệ thống lập tức gọi 1,000 chiếc xe đến đón.

</details>

- **Traditional Servers (EC2/ECS)**: Like hiring a full-time chauffeur on a monthly salary. Whether you travel 100 miles or sit at home all day, you pay them their full monthly wage. (Paying for idle time).
- **AWS Lambda (Serverless)**: Like using Uber/Grab. When you need to travel (an Event occurs), you tap a button. A car appears, drives you for exactly 15 minutes, and you pay for exactly 15 minutes. When the ride ends, the car disappears. You don't manage the driver or the car! If 1,000 people tap the button at the same time, the system magically summons 1,000 cars instantly.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**AWS Lambda** là dịch vụ tính toán Serverless (không máy chủ) cho phép bạn chạy code mà không cần khởi tạo hay quản lý máy chủ. 
Bạn chỉ cần upload code (bằng Python, Node.js, Java, Go...). AWS sẽ chạy code đó mỗi khi có "Sự kiện" (Event) kích hoạt nó. Bạn chỉ trả tiền cho chính xác số mili-giây (ms) mà code của bạn chạy. 

**Đặc điểm cốt lõi:**
- Không có hệ điều hành để vá lỗi, không có ổ cứng để quản lý.
- Tự động thu phóng (Auto-scaling) từ 0 lên hàng chục ngàn lượt chạy song song.
- Tính tiền theo 1ms (mili-giây). Nếu hàm chạy hết 200ms, bạn trả tiền 200ms. Nếu không ai gọi hàm, hóa đơn bằng $0.

</details>

**AWS Lambda** is a Serverless compute service that lets you run code without provisioning or managing servers.
You simply upload your code (in Python, Node.js, Java, Go, etc.). AWS executes your code only when triggered by an "Event". You pay only for the exact compute time you consume—billed down to the millisecond (ms).

**Core Characteristics:**
- No Operating Systems to patch, no disks to manage.
- Automatic scaling from 0 to tens of thousands of concurrent executions instantly.
- Millisecond billing. If your function runs for 200ms, you pay for exactly 200ms. If no one calls the function all month, your bill is $0.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trước đây, để viết một đoạn script nhỏ (Ví dụ: Chỉnh sửa kích thước ảnh mỗi khi người dùng upload lên S3), bạn phải tạo 1 máy chủ EC2, chạy nó 24/7 chỉ để ngồi "chờ" người dùng upload ảnh. Tiền thuê máy chủ EC2 tốn $10/tháng, dù mỗi ngày chỉ có 5 người upload ảnh. Sự lãng phí (Idle time) là rất lớn.

Lambda sinh ra để loại bỏ hoàn toàn Idle Time. Nó thay đổi mô hình tính toán từ "Always On" (Luôn bật) sang "Event-Driven" (Hướng sự kiện). AWS giúp bạn tối ưu hóa chi phí đến mức tuyệt đối.

</details>

Historically, if you wanted to run a tiny script (e.g., resizing an image every time a user uploads one to S3), you had to spin up an EC2 server and leave it running 24/7 just "waiting" for uploads. You paid $10/month for that server, even if only 5 people uploaded pictures a day. The cost of Idle Time was massive.

Lambda was created to completely eradicate Idle Time. It shifted the computing paradigm from "Always On" to "Event-Driven". AWS optimizes your cost to the absolute mathematical minimum.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Kiến trúc Server (EC2/ECS)**: Khởi động mất vài phút. Bị giới hạn tài nguyên vật lý. Rất khó chịu đựng lượng truy cập tăng vọt đột ngột (Spike traffic). Dễ bị sập. Tuy nhiên, khi chạy ổn định thì tốc độ cực nhanh và rẻ hơn nếu ứng dụng chạy liên tục 24/7.
- **Kiến trúc Lambda**: Khởi động mất vài chục mili-giây. Chịu đựng Spike traffic hoàn hảo. Nếu có 10,000 người vào cùng lúc, AWS tạo ra 10,000 bản sao Lambda chạy song song. Điểm yếu: Nếu gọi lần đầu tiên sau một thời gian dài nghỉ ngơi, sẽ bị trễ vài giây (Cold Start). Rất đắt nếu chạy liên tục 24/7 không nghỉ.

</details>

### Server-Based (EC2/ECS/EKS)
- **Scaling**: Booting a new server takes minutes. It struggles to handle sudden, massive spikes in traffic.
- **Cost**: Cheaper at massive, constant, predictable 24/7 scale.
- **Maintenance**: Requires OS patching, security hardening, and load balancer configuration.

### Serverless (AWS Lambda)
- **Scaling**: Booting a new Lambda environment takes milliseconds. It handles unpredictable, massive spikes flawlessly (bursting to 10,000 concurrent requests instantly).
- **Cost**: Highly cost-effective for intermittent, unpredictable, or low-volume traffic (Scale to Zero). Very expensive if a function runs continuously 24/7 without stopping.
- **Maintenance**: Zero. AWS handles everything beneath your code.

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Web APIs (RESTful)**: Dùng **API Gateway + Lambda** để làm Backend cho Website/App Mobile. Rất phổ biến vì giá quá rẻ lúc ban đầu.
2. **Xử lý sự kiện thời gian thực (Event-Driven)**: Một người upload ảnh gốc lên S3 -> S3 kích hoạt Lambda -> Lambda resize ảnh rồi lưu vào S3 thư mục `thumbnail/`.
3. **Cron Jobs tự động**: Thay vì dùng Linux Cron, dùng **EventBridge + Lambda** để dọn rác Database vào mỗi 2h sáng.

**Không nên làm (Anti-patterns):**
- **Dùng Lambda cho Long-running tasks**: Lambda bị giới hạn thời gian chạy tối đa là **15 phút**. Nếu bạn có một script Data Processing chạy mất 20 phút, Lambda sẽ tự động "giết" (kill) đoạn code của bạn ở phút thứ 15. Hãy dùng ECS Fargate cho các tác vụ chạy lâu.

</details>

1. **Serverless REST APIs**: Using **API Gateway + Lambda** to power the backend for Mobile Apps or SPAs (React/Vue). Extremely popular for startups because the architecture costs exactly $0 until you actually get users.
2. **Real-time File Processing**: A user uploads a raw HD image to S3 -> S3 triggers a Lambda function -> The function generates a 100x100 thumbnail and saves it back to S3.
3. **Automated Cron Jobs**: Instead of setting up a Linux server just to run a Cron tab, use AWS EventBridge to trigger a Lambda function every night at 2 AM to clean up stale database records.

### Anti-Patterns
- **Long-Running Tasks**: Lambda has a hard, unchangeable execution limit of **15 minutes**. If you have a Machine Learning model or a Data Engineering script that takes 20 minutes to run, Lambda will mercilessly kill the process at exactly 14m:59s. For long-running tasks, use AWS ECS Fargate or AWS Batch.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Khởi động lạnh (Cold Starts) - Kẻ thù số 1 của Lambda**
Khi một hàm Lambda không được gọi trong khoảng 15 phút, AWS sẽ thu hồi bộ nhớ của nó để tiết kiệm tài nguyên. Lần tiếp theo có người gọi, AWS phải mất thời gian tải lại code, nạp RAM, khởi động môi trường (mất khoảng 1 - 3 giây). Hiện tượng này gọi là **Cold Start**. Khách hàng sẽ thấy API phản hồi rất chậm ở lần gọi đầu tiên.
*Giải pháp*: Dùng tính năng *Provisioned Concurrency* (giữ cho hàm luôn ấm, đổi lại phải trả tiền cố định), hoặc viết code bằng Go/Rust thay vì Java để khởi động nhanh hơn.

**2. VPC Cold Start**
Trước năm 2019, nếu bạn nhét Lambda vào trong mạng VPC riêng (để kết nối với RDS Database riêng tư), Cold Start có thể lên tới 10 giây vì phải gắn Card mạng (ENI) vật lý. AWS đã sửa lỗi này. Hiện nay việc đặt Lambda trong VPC đã rất nhanh. Tuy nhiên, việc Lambda gọi vào Relational Database (MySQL/PostgreSQL) vẫn gây ra thảm họa "Cạn kiệt Connection Pool". Hàng ngàn Lambda gọi cùng lúc sẽ đánh sập DB.
*Giải pháp*: Dùng **RDS Proxy** đứng giữa để quản lý kết nối, hoặc dùng DynamoDB (Serverless DB).

</details>

### 1. The "Cold Start" Menace
When a Lambda function hasn't been invoked for a while (e.g., 15 minutes), AWS destroys the underlying container to save resources. When the next request arrives, AWS has to fetch your code, provision a new container, and boot the runtime. This delay (typically 0.5s to 3s) is a **Cold Start**. For user-facing Web APIs, a 3-second delay is terrible UX.
*Mitigations*: 
- Use **Provisioned Concurrency**: You pay AWS a flat fee to keep a set number of containers perpetually "warm".
- Optimize your language: Java and C# suffer brutal cold starts. Node.js, Python, Go, and Rust boot extremely fast.

### 2. Lambda + Relational Databases (The Connection Exhaustion Problem)
Lambda scales horizontally instantly. If you get a sudden spike and AWS spins up 5,000 concurrent Lambda instances, and each instance opens a direct connection to your Amazon RDS PostgreSQL database, your database will hit its `max_connections` limit instantly and crash violently. 
*Mitigations*:
- Use **Amazon RDS Proxy**: A fully managed connection pooler that sits between Lambda and RDS, absorbing the 5,000 connections and multiplexing them safely to the database.
- Better yet, use a Serverless Database like **DynamoDB** which handles HTTP-based concurrent connections natively.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một hàm Lambda viết bằng Python. Lưu ý cách phần "Khởi tạo kết nối DB" được đặt BÊN NGOÀI hàm `lambda_handler`. Điều này giúp những lần gọi sau (Warm Start) có thể dùng lại kết nối cũ mà không phải tạo lại.

</details>

### Python Lambda Function (Best Practice)

Notice how we declare the database connection *outside* of the `lambda_handler`. During a "Warm Start", the container is frozen and thawed. Code outside the handler retains its state in memory, allowing subsequent invocations to reuse the expensive database connection.

```python
import json
import boto3

# 1. INITIALIZATION CODE (Executes ONLY during a Cold Start)
# Connect to DynamoDB outside the handler.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UsersTable')

def lambda_handler(event, context):
    """
    2. HANDLER CODE (Executes on EVERY request)
    'event' contains the data passed in (e.g., HTTP Body from API Gateway)
    'context' contains AWS runtime information
    """
    try:
        # Extract user_id from the incoming API Gateway request
        user_id = event['queryStringParameters']['user_id']
        
        # Query DynamoDB (Reuses the connection created outside)
        response = table.get_item(Key={'userId': user_id})
        user_data = response.get('Item', {})
        
        # Return a standard HTTP 200 response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # CORS
            },
            'body': json.dumps({
                'message': 'Success',
                'data': user_data
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

---

## Related Topics

- [Event-Driven Architectures](../04-serverless/event-driven-architectures.md) — How Lambda integrates with queues and event buses.
- [AWS API Gateway](./aws-api-gateway.md) — The front door that exposes your Lambda functions as HTTP URLs to the web.
- [AWS DynamoDB](./aws-dynamodb.md) — The NoSQL database perfectly matched for Lambda's massive scaling.
