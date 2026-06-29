# SQS, SNS & EventBridge (Messaging)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Chìa khóa để xây dựng các hệ thống Microservices không bao giờ sập. Tìm hiểu cách chia cắt hệ thống (Decoupling) bằng Hàng đợi SQS, phát thanh tin nhắn bằng SNS (Pub/Sub) và định tuyến sự kiện thông minh với EventBridge.

</details>

> **Summary**: The key to building indestructible Microservices. Learn how to decouple monolithic systems using SQS Queues, broadcast messages with SNS (Pub/Sub), and intelligently route events using EventBridge.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Kiến trúc đồng bộ (Tồi)**: Khách hàng gọi món (Gửi API). Thu ngân hét vào bếp "Làm 1 burger". Thu ngân BẮT BUỘC phải đứng đợi đầu bếp làm xong (3 phút). Trong 3 phút đó, không khách nào khác được gọi món. Nếu đầu bếp lăn ra xỉu, thu ngân cũng báo lỗi với khách.
- **SQS (Hàng đợi - Queue)**: Thu ngân ghi món ăn ra một tờ giấy (Message), ghim nó lên "Bảng Đợi" (SQS Queue), rồi lập tức quay lại phục vụ khách tiếp theo. Đầu bếp cứ rảnh lúc nào thì ra Bảng Đợi xé 1 tờ giấy xuống làm. Nếu đầu bếp xỉu, giấy vẫn nằm an toàn trên Bảng Đợi. Khi có đầu bếp mới, họ lại tiếp tục làm. Hệ thống không bao giờ mất đơn hàng!
- **SNS (Phát thanh - Pub/Sub)**: Giống như một cái loa phát thanh. Khi Sếp nói "Có lương rồi" vào mic (Publisher), ngay lập tức TẤT CẢ nhân viên đăng ký kênh đó (Subscribers) đều nhận được tin báo cùng một lúc (Gửi Email, Gửi SMS, Gửi cho SQS).

</details>

- **Synchronous Architecture (Bad)**: A customer places an order (API Call). The Cashier turns to the Chef and says "Make 1 burger". The Cashier MUST stand there and wait for 3 minutes until the burger is done. During that time, no other customer can order. If the Chef faints, the Cashier also crashes and drops the order.
- **SQS (Queueing)**: The Cashier writes the order on a sticky note (Message), slaps it onto an Order Board (SQS Queue), and immediately turns around to serve the next customer. The Chef looks at the Order Board, pulls down one sticky note at a time, and cooks at their own pace. If the Chef faints, the sticky notes remain perfectly safe on the board. When a new Chef arrives, they just resume pulling tickets. No order is ever lost!
- **SNS (Pub/Sub Broadcasting)**: Like a mega-megaphone. When the Boss yells "Bonus Paid!" into the mic (Publisher), ALL employees who subscribed to that frequency (Subscribers) instantly receive the message at the exact same time (Email, SMS, or pushing to multiple SQS queues).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đây là bộ 3 dịch vụ tích hợp (Integration) giúp các phần mềm tách rời nhau (Decoupled).
1. **Amazon SQS (Simple Queue Service)**: Dịch vụ Hàng đợi. Máy gửi (Producer) ném tin nhắn vào SQS. Máy nhận (Consumer) liên tục hỏi SQS "Có tin nào không?" (Polling) để lấy về xử lý. Mô hình **1-to-1** (1 tin nhắn chỉ do 1 người xử lý).
2. **Amazon SNS (Simple Notification Service)**: Dịch vụ Phát thanh (Pub/Sub). Bạn gửi 1 tin vào SNS Topic. SNS sẽ chủ động "Đẩy" (Push) tin nhắn đó cho TẤT CẢ những ai đã đăng ký (Email, SMS, Lambda, SQS). Mô hình **1-to-Many**.
3. **Amazon EventBridge**: Phiên bản nâng cấp cực xịn của SNS. Nó nhận sự kiện từ khắp nơi trên AWS (VD: "Có EC2 vừa bị sập"), dùng các "Quy tắc lọc" (Rules) cực kỳ thông minh để quyết định xem nên gửi sự kiện đó cho ai.

</details>

These are the holy trinity of Application Integration on AWS, heavily used to decouple Microservices.
1. **Amazon SQS (Simple Queue Service)**: A Pull-based message queue. Producers throw messages into the queue. Consumers constantly poll (ask) the queue for messages, process them, and delete them. It is a **1-to-1** model (A message is processed by exactly one consumer).
2. **Amazon SNS (Simple Notification Service)**: A Push-based Pub/Sub (Publish/Subscribe) service. A Publisher sends a message to an SNS Topic. SNS actively "pushes" copies of that message to ALL Subscribers (Emails, SMS, Lambdas, SQS queues) simultaneously. It is a **1-to-Many** model.
3. **Amazon EventBridge**: The modern, highly advanced evolution of SNS. It is a Serverless Event Bus. It catches events from all over AWS (e.g., "An EC2 instance crashed"), applies intelligent filtering Rules (e.g., "Only if it crashed in Production"), and routes it to specific targets.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong hệ thống nguyên khối (Monolith), các hàm gọi trực tiếp lẫn nhau. Nếu hàm Gửi Email bị lỗi, cả chức năng Thanh toán Đơn hàng cũng bị lỗi theo (Chết chùm - Tightly Coupled).
Các kỹ sư muốn tách Hệ thống Thanh toán và Hệ thống Gửi Email ra. Làm sao để chúng nói chuyện?
- Cắm trực tiếp API? (Sai! Nếu máy Email sập, API sẽ Timeout và rớt đơn).
- Dùng SQS? (Chuẩn!). Hệ thống Thanh toán chỉ cần ném tờ giấy "Gửi email cho ID 123" vào SQS rồi kết thúc giao dịch thành công. Hệ thống Email cứ tà tà lấy giấy từ SQS ra để gửi. Dù hệ thống Email có chết 3 tiếng, lúc sống lại nó vẫn gửi bù được (Tin nhắn giữ trong SQS tối đa 14 ngày). **Đây gọi là Decoupling (Tách rời).**

</details>

In monolithic systems, functions call each other synchronously. If the `SendEmail()` function crashes, the entire `CheckoutOrder()` process fails and rolls back (Tightly Coupled).
Engineers wanted to separate the Order Service from the Email Service. How do they communicate?
- Direct HTTP API call? (Bad! If the Email server is down, the API times out and the user's order fails).
- Using SQS? (Perfect!). The Order Service simply drops a message ("Send email to ID 123") into the SQS Queue and instantly returns "Checkout Successful" to the user. The Email Service polls SQS at its own pace. Even if the Email server crashes for 3 hours, when it reboots, the messages are still waiting safely in the Queue (retention up to 14 days). **This is the supreme architectural principle of Decoupling.**

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**SQS Standard vs SQS FIFO**
AWS cung cấp 2 loại hàng đợi SQS:
1. **SQS Standard**: Nhanh vô đối (không giới hạn số lượng). Nhưng có 2 nhược điểm: Thứ tự tin nhắn có thể bị xáo trộn (Gửi 1-2-3, nhận 2-1-3), và đôi khi 1 tin nhắn bị gửi trùng 2 lần (At-least-once delivery).
2. **SQS FIFO (First-In-First-Out)**: Rất khắt khe. Tin nhắn vào trước CHẮC CHẮN ra trước (Gửi 1-2-3, nhận đúng 1-2-3). Đảm bảo 100% không bao giờ trùng lặp (Exactly-once). Đổi lại, tốc độ bị giới hạn (khoảng 3,000 tin/giây) và đắt hơn.

</details>

### Queue Types: SQS Standard vs. SQS FIFO

AWS provides two types of SQS Queues based on your exact business needs:
1. **SQS Standard**: Unlimited throughput. But it has two massive caveats: It uses "Best-Effort Ordering" (Messages sent 1-2-3 might be received 2-1-3), and it guarantees "At-Least-Once Delivery" (Very rarely, a message might be delivered twice). Ideal for tasks where order doesn't matter (e.g., resizing images).
2. **SQS FIFO (First-In-First-Out)**: Strict. It guarantees exact ordering (1-2-3 goes in, 1-2-3 comes out). It guarantees "Exactly-Once Processing" (Zero duplicates). *Trade-off*: It is capped at a strict throughput limit (up to 3,000 msgs/sec with batching) and costs more. Crucial for financial transactions (You don't want to process a "Withdraw $100" message twice!).

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Worker Queues (SQS + EC2 Auto Scaling)**: Một hàng đợi chứa 100,000 tin nhắn (đơn hàng cần xử lý). Gắn CloudWatch để theo dõi. Nếu hàng đợi dài ra, tự động gọi thêm EC2 Worker để phụ làm. Hàng đợi ngắn lại thì tắt bớt EC2.
2. **Mô hình Fan-out (SNS + SQS)**: Khách hàng mua hàng xong. Thay vì bắt hệ thống thanh toán gọi 3 cái API khác nhau, nó chỉ cần bắn 1 tin lên **SNS Topic**. Topic này tự động nhân bản tin nhắn đó ra, ném vào **3 cái SQS Queues khác nhau**: 1 cho team Kho bãi, 1 cho team Email, 1 cho team Kế toán. Các team tự đi mà xử lý song song.
3. **Event-Driven Security (EventBridge)**: Cấu hình EventBridge: "Nếu phát hiện ai đó đăng nhập Root User, ngay lập tức kích hoạt Lambda function khóa tài khoản và bắn tin nhắn Slack cho Giám đốc".

**Không nên làm (Anti-patterns):**
- **Dùng SQS để truyền dữ liệu lớn**: SQS giới hạn tin nhắn tối đa 256KB! Nó chỉ dùng để gửi "Lệnh" hoặc "Siêu dữ liệu". Nếu bạn muốn gửi 1 cái video 50MB qua SQS? Hãy đẩy video vào S3, rồi lấy cái URL của video đó gửi qua SQS.

</details>

1. **Worker Queues (SQS + Auto Scaling)**: A queue is filled with 100,000 background tasks. You configure an EC2 Auto Scaling Group metric based on the `ApproximateNumberOfMessagesVisible`. As the queue grows, AWS automatically spins up more EC2 instances to drain the queue faster.
2. **The Fan-Out Pattern (SNS -> Multiple SQS)**: A user purchases an item. The Order Service publishes exactly ONE message to an **SNS Topic**. This Topic pushes a clone of the message into **3 separate SQS Queues**: one for the Inventory team, one for the Shipping team, and one for the Email team. Each microservice team processes the queue at their own pace, totally isolated from the others.
3. **Automated Remediation (EventBridge)**: Configure an EventBridge Rule: "If an AWS CloudTrail event shows someone logging in as the Root User, instantly trigger a Lambda function that disables the account and sends a Slack alert."

### Anti-Patterns
- **Passing Large Payloads through SQS**: SQS has a hard maximum message size of **256 KB**. It is meant for passing tiny JSON instructions, not files. If you need to process a 50MB video, you upload the video to Amazon S3, and you send a tiny SQS message containing ONLY the `s3://bucket/video.mp4` URL. The Consumer reads the SQS message, then downloads the video from S3.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Dead Letter Queue (DLQ) - Bãi rác tái chế**
Điều gì xảy ra nếu code trong Consumer bị lỗi (Ví dụ: Thiếu thư viện), nó lấy tin nhắn từ SQS, xử lý lỗi, trả lại SQS, rồi lại lấy, lại lỗi... Tạo ra một vòng lặp vô hạn đốt cháy CPU.
*Giải pháp*: Luôn luôn cấu hình **DLQ**. Quy định: "Nếu 1 tin nhắn xử lý thất bại quá 3 lần, tự động vứt nó sang thùng rác DLQ". Ứng dụng sẽ tiếp tục chạy tin nhắn khác. Cuối tuần, Kỹ sư mở DLQ ra xem tại sao tin nhắn đó bị lỗi và sửa code.

**2. Visibility Timeout (Thời gian tàng hình)**
Khi EC2 kéo 1 tờ giấy (tin nhắn) khỏi SQS, tờ giấy đó KHÔNG bị xóa ngay. Nó bị làm "tàng hình" (Visibility Timeout) trong 30 giây để các EC2 khác không nhìn thấy. 
- Nếu trong 30s đó, EC2 xử lý xong, nó báo SQS: "Đã làm xong, xóa giấy đi".
- Nếu EC2 bị sập đột ngột? Sau 30s, tờ giấy tự động hiện hình lại trên SQS để EC2 khác lấy làm. Tuyệt đối không mất việc!

</details>

### 1. Dead Letter Queues (DLQ) - The Safety Net
What happens if a Consumer receives a message, but there is a bug in the code (e.g., a `NullPointerException`), so it crashes? The message goes back to SQS. The Consumer pulls it again, crashes again. This is an infinite loop that burns CPU and blocks the queue ("Poison Pill").
*Best Practice*: ALWAYS configure a **DLQ**. You set a rule: `maxReceiveCount = 3`. If a message fails to be processed 3 times, SQS forcefully evicts it from the main queue and drops it into the Dead Letter Queue. The system continues processing normal messages. An engineer can inspect the DLQ later to debug the Poison Pill.

### 2. Visibility Timeout (How SQS guarantees no message is lost)
When an EC2 Consumer pulls a message from SQS, the message is NOT deleted. It is simply made "Invisible" (Visibility Timeout - default 30 seconds) to all other Consumers.
- If the EC2 finishes the job, it explicitly sends a `DeleteMessage` API call to SQS. The message is gone forever.
- But what if the EC2 completely loses power mid-processing? It never sends the Delete signal. After 30 seconds, the Visibility Timeout expires, and the message *magically becomes visible again* on the queue. Another EC2 instance will pull it and process it. Zero data loss!

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một đoạn mã Terraform cực chuẩn để thiết lập mô hình **Fan-Out**. Khởi tạo một SNS Topic (Cái loa), tạo 2 SQS Queue (Người nghe), và nối chúng lại với nhau (Subscribe).

</details>

### The Fan-Out Architecture (Terraform)

This Terraform snippet creates the foundational SNS -> SQS Fan-Out architecture used globally in Microservices.

```hcl
# 1. Create the SNS Topic (The Publisher / Megaphone)
resource "aws_sns_topic" "order_created_topic" {
  name = "order-created-events"
}

# 2. Create the SQS Queues (The Subscribers / Workers)
resource "aws_sqs_queue" "inventory_queue" {
  name = "inventory-processing-queue"
}

resource "aws_sqs_queue" "shipping_queue" {
  name = "shipping-processing-queue"
}

# 3. Subscribe the Queues to the SNS Topic
resource "aws_sns_topic_subscription" "inventory_sub" {
  topic_arn = aws_sns_topic.order_created_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.inventory_queue.arn
}

resource "aws_sns_topic_subscription" "shipping_sub" {
  topic_arn = aws_sns_topic.order_created_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.shipping_queue.arn
}

# (Note: In a real production setup, you must also add an aws_sqs_queue_policy 
# to explicitly ALLOW the SNS Topic to write messages into the SQS Queues).
```

---

## Related Topics

- [AWS Lambda](./aws-lambda.md) — The most common Serverless consumer that reads from SQS automatically.
- [AWS EC2](./aws-ec2.md) — EC2 instances in an Auto Scaling Group reading from SQS is a classic decoupled architecture.
- [Event-Driven Architectures](../04-serverless/event-driven-architectures.md) — Expanding further on how these 3 services define modern serverless design.
