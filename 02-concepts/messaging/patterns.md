# Messaging Patterns

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi gửi một bức thư vào Bưu điện (Message Broker), bạn muốn bức thư đó được xử lý như thế nào? Bạn muốn chỉ một người duy nhất bóc thư ra làm (Tránh trùng lặp công việc), hay bạn muốn bức thư đó được copy ra làm 10 bản gửi cho 10 phòng ban khác nhau cùng đọc? **Messaging Patterns** là các mẫu thiết kế luồng đi của tin nhắn để giải quyết các nhu cầu đó. Hai mẫu kinh điển nhất là **Point-to-Point (Queue)** và **Publish/Subscribe (Pub/Sub)**.

</details>

> **Summary**: Once a message is ingested by a Message Broker, how should it be routed and consumed? Should it be processed exclusively by a single worker to prevent duplicate execution, or should it be broadcasted to multiple independent systems simultaneously? **Messaging Patterns** define the architectural routing topology of asynchronous communication. The two foundational paradigms that govern 99% of message-oriented middleware are the **Point-to-Point (Message Queue)** pattern and the **Publish/Subscribe (Pub/Sub)** pattern.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng Bưu điện là hệ thống Message Broker.
1. **Point-to-Point (Xếp hàng lấy gạo)**: Có một kho gạo. Có 10 người đứng xếp thành một hàng (Queue). Người phát gạo đưa 1 bao gạo cho người đứng đầu tiên. Người đó vác đi. Bao gạo đó biến mất. Người thứ 2 không bao giờ nhận được bao gạo đó nữa. Mẫu này dùng để CHIA ĐỀU CÔNG VIỆC, không ai làm trùng việc của ai.
2. **Pub/Sub (Loa phát thanh phường)**: Trưởng thôn đứng đọc loa: "Ngày mai đi họp!". Tất cả 100 người dân trong làng đều nghe thấy thông báo đó cùng một lúc. Lời thông báo được copy ra 100 bản vào tai 100 người. Mẫu này dùng để THÔNG BÁO CHO TẤT CẢ cùng biết để tự lo việc của mình.

</details>

Imagine the Message Broker as an administrative dispatch center.
1. **Point-to-Point (The Assembly Line)**: A conveyor belt drops a specific engine part. You have 5 workers standing by. Worker #1 picks up the part and installs it. Once Worker #1 picks it up, the part is physically gone. Worker #2 cannot pick it up. This pattern is engineered for **Load Balancing and Task Distribution**. It guarantees a task is executed exactly once by a single worker.
2. **Publish/Subscribe (The Radio Broadcast)**: The CEO sends out a company-wide email announcement: "Free pizza in the lobby!" All 500 employees receive an exact copy of the email simultaneously in their personal inboxes. This pattern is engineered for **Event Broadcasting**. It guarantees that an event triggers multiple, independent downstream reactions simultaneously.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Point-to-Point (P2P / Message Queue)**
- **Đặc điểm**: Mối quan hệ 1-1. Dù có 100 Consumer kết nối vào Queue, thì mỗi lá thư cũng CHỈ ĐƯỢC ĐỌC BỞI 1 CONSUMER DUY NHẤT. Sau khi đọc xong và báo `ACK` (Thành công), lá thư bị xóa vĩnh viễn khỏi Queue.
- **Công cụ tiêu biểu**: RabbitMQ, AWS SQS, ActiveMQ.

**2. Publish/Subscribe (Pub/Sub / Topic)**
- **Đặc điểm**: Mối quan hệ 1-N. Producer ném thư vào một cái "Chủ đề" (Topic). Có 5 hệ thống Consumer đang Lắng nghe (Subscribe) cái Topic đó. Cả 5 hệ thống ĐỀU NHẬN ĐƯỢC 1 BẢN COPY y chang nhau của lá thư đó.
- **Công cụ tiêu biểu**: Apache Kafka, AWS SNS, Google Cloud Pub/Sub.

</details>

**1. Point-to-Point (P2P / Work Queue)**
- **Topology**: 1-to-1 processing relationship. A Sender pushes a message into a specific `Queue`. Multiple Receivers (Consumers) can connect to the same Queue. However, the Broker ensures that a specific message is delivered to **EXACTLY ONE** Consumer. Once the Consumer acknowledges (`ACK`) the message, it is permanently deleted from the Queue.
- **Primary Tooling**: RabbitMQ, AWS SQS (Simple Queue Service).

**2. Publish/Subscribe (Pub/Sub / Topic)**
- **Topology**: 1-to-Many broadcast relationship. A Publisher pushes a message to a logical channel called a `Topic`. Multiple distinct Subscribers register their interest in that Topic. The Broker ensures that **EVERY SINGLE SUBSCRIBER** receives an independent copy of the message.
- **Primary Tooling**: Apache Kafka, AWS SNS (Simple Notification Service), Google Cloud Pub/Sub.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao cần Point-to-Point? (Chia tải)**
Giả sử bạn làm ứng dụng xử lý Video. Có 1000 người upload video cùng lúc. Quá trình Encode tốn 5 phút/video. Nếu gửi hết cho 1 Server, nó sẽ sập. Bạn mở thêm 10 con Server phụ. Nếu dùng Pub/Sub, cả 10 con Server sẽ cùng nhau Encode 1 cái Video $\rightarrow$ Ngu ngốc và tốn điện. Bạn phải dùng Queue (Point-to-Point). Con Server 1 lấy Video A thì con Server 2 phải lấy Video B. Đây là bài toán **Load Balancing (Cân bằng tải)**.

**Tại sao cần Pub/Sub? (Mở rộng tính năng không cần sửa Code)**
Khách hàng đặt mua 1 cái Áo. Hệ thống tạo ra sự kiện `OrderPlaced`. 
- Service Tích Điểm nghe thấy $\rightarrow$ Cộng điểm.
- Service Giao Hàng nghe thấy $\rightarrow$ Gọi shipper.
Tháng sau, Sếp yêu cầu: "Khi mua áo, tự động nhắn tin SMS cảm ơn!". Bạn KHÔNG CẦN sửa code của hệ thống Đặt hàng. Bạn chỉ cần viết một con Service SMS mới, cho nó Subscribe vào Topic `OrderPlaced`. Bùm! Tính năng mới hoạt động ngay lập tức. Đây là bài toán **Tách rời (Decoupling)**.

</details>

**The Necessity of Point-to-Point (Load Balancing)**:
Consider a highly CPU-bound architecture: Video Transcoding. 10,000 users upload videos. You spin up 50 Worker Nodes. If you utilized a Broadcast (Pub/Sub) pattern, all 50 Worker Nodes would receive the exact same video and attempt to transcode it simultaneously—a catastrophic waste of compute power. The architectural mandate here is **Competing Consumers**. You strictly require a Work Queue (P2P). If Worker Node #1 pulls Video A, the Broker locks Video A so Worker Node #2 is forced to pull Video B. It evenly distributes the computational load.

**The Necessity of Pub/Sub (Extensibility & Decoupling)**:
Consider an E-commerce architecture. An `OrderPlaced` event occurs. 
- The `InventoryService` needs it to deduct stock.
- The `LoyaltyService` needs it to award points.
Next quarter, the Business team demands a new feature: "Send a promotional SMS immediately when an order is placed." In a monolithic/P2P system, you would have to modify the core `OrderService` code to explicitly call the new `SMSService`. In a Pub/Sub architecture, the `OrderService` remains untouched. You simply deploy the new `SMSService` and configure it to Subscribe to the existing `OrderPlaced` Topic. The architecture scales in complexity without modifying existing, tested code.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt về Hành vi của 2 mẫu khi có 3 con Server Lắng nghe.
</details>

Visualizing the routing behavior when 1 Message is published and 3 Consumers are listening.

| Concept | Point-to-Point (Queue) | Publish/Subscribe (Topic) |
|---|---|---|
| **Message Count** | 1 Message | 1 Message |
| **Number of Listeners** | 3 Consumers (Node A, B, C) | 3 Subscribers (Service X, Y, Z) |
| **Delivery Mechanism**| Broker delivers to **Node A ONLY**. | Broker replicates and delivers to **X, Y, AND Z**. |
| **Data Persistence** | Message is deleted after Node A finishes. | Message is retained (Kafka) or dropped after delivery (SNS). |
| **Core Purpose** | Distribute Workload (Concurrency). | Broadcast Events (Choreography). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Point-to-Point (RabbitMQ / SQS)**: 
  - Gửi Email: Đẩy hàng triệu lệnh gửi Email vào Queue. Các Worker tranh nhau lấy ra gửi. Gửi xong thì xóa.
  - Xử lý Đơn hàng: Đảm bảo một đơn hàng chỉ được tạo trên Database đúng một lần duy nhất.
- **Pub/Sub (Kafka / SNS)**:
  - Thông báo hệ thống: Gửi Notification cho tất cả thiết bị của 1 User (Web, iOS, Android).
  - Kiến trúc Event-Driven: 1 hành động `Đăng ký User` kích hoạt hàng loạt hệ thống khác: Gửi Mail Welcome, Khởi tạo ví tiền ảo, Cập nhật CRM.

</details>

- **Point-to-Point Use Cases (Work Queues)**:
  - **Asynchronous Task Processing**: Sending out massive Email/SMS campaigns. You dump 1,000,000 tasks into AWS SQS. You spin up 100 EC2 instances. They compete to pull tasks off the queue until it hits zero.
  - **Payment Processing**: Ensuring a credit card charge request is processed exactly once by an available payment worker, never duplicated.
- **Publish/Subscribe Use Cases (Event Streams)**:
  - **Data Pipeline & Analytics**: User Clickstream data. When a user clicks a button, the frontend publishes an event. The `Analytics_Service` subscribes to generate dashboards, while the `MachineLearning_Service` simultaneously subscribes to train a recommendation algorithm.
  - **Microservice Choreography**: Standard Event-Driven Architecture. A single state change (`User_Registered`) broadcasts to trigger the creation of a billing profile, a CRM entry, and an introductory email sequence.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Kết hợp cả 2 mẫu (The Fan-Out Pattern)**: Trong thực tế, các công ty lớn kết hợp sức mạnh của CẢ HAI. Đầu tiên, dùng Pub/Sub (SNS) để bắn 1 tin nhắn ra 3 phòng ban khác nhau (Email, Kho, Kế toán). Nhưng ở mỗi phòng ban, họ lại thiết lập một cái Queue (SQS). Tin nhắn từ SNS sẽ rơi vào 3 cái SQS Queue riêng biệt. Lúc này, ở phòng Email, họ có thể bật 10 con Server để rỉa tin nhắn từ Queue của họ (P2P). Mô hình này gọi là `SNS -> SQS Fan-out`, hoàn hảo tuyệt đối.
2. **Kích thước tin nhắn (Message Payload)**: Đừng bao giờ nhét một cái file PDF nặng 50MB vào Kafka hay RabbitMQ. Broker sẽ nghẹt thở. Hãy upload file PDF đó lên S3 (Cloud Storage), lấy cái link URL tải file, và chỉ gửi cái Link URL đó qua Message Broker. Cực kỳ nhẹ và mượt.

</details>

1. **The Ultimate Combination: Fan-Out Architecture (SNS to SQS)**: In Enterprise architectures, relying strictly on one pattern is insufficient. Architects combine both to achieve decoupling AND scalability. The Publisher sends an event to a Pub/Sub Topic (e.g., AWS SNS). SNS broadcasts the event. However, instead of applications subscribing directly, SNS pushes the event into multiple downstream Point-to-Point Queues (AWS SQS).
   - *Result*: The system achieves Broadcast routing (1-to-N via SNS). Concurrently, the `Email_Queue` can be consumed by 50 Worker Nodes competing for tasks (P2P Load Balancing). This is the gold standard for AWS messaging architecture.
2. **The "Claim Check" Pattern (Payload Hygiene)**: Message Brokers are engineered to route millions of tiny, lightweight JSON payloads (under 256KB) rapidly. If a system attempts to push a 50MB PDF document or a massive Base64 Image directly into a Kafka Topic or RabbitMQ Queue, it will cause catastrophic memory exhaustion and network saturation. **Fix**: Use the Claim Check pattern. Upload the 50MB PDF to Object Storage (AWS S3). Retrieve the resulting S3 URL (`s3://bucket/doc.pdf`). Publish a tiny JSON message containing only the URL to the Broker. The downstream consumer receives the message and downloads the heavy PDF directly from S3.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng Kafka để làm Point-to-Point đơn giản**: Apache Kafka là một con quái vật Pub/Sub phức tạp, cần cả một team DevOps để vận hành (ZooKeeper, Partitioning). Nếu bài toán của bạn chỉ đơn giản là "Gửi mail chạy ngầm", dùng Kafka giống như vác súng cối đi bắn ruồi. Hãy dùng RabbitMQ hoặc AWS SQS, vừa rẻ vừa dễ setup.
2. **Quên xử lý Lỗi (Poison Pill)**: Trong mô hình Queue, nếu tin nhắn bị lỗi, Consumer từ chối (NACK). Tin nhắn lại quay về Queue. Một Consumer khác bốc lên lại lỗi. Cứ lặp đi lặp lại vô tận làm kẹt toàn bộ hệ thống. Bắt buộc phải cài đặt giới hạn: Nếu lỗi quá 3 lần, vứt tin nhắn đó sang "Thùng rác" (Dead Letter Queue).

</details>

1. **Over-engineering with Apache Kafka**: Kafka is an incredibly complex, high-throughput Distributed Commit Log engineered for Pub/Sub stream processing at petabyte scale. If a startup's only architectural requirement is a simple Point-to-Point Work Queue to send background password-reset emails, deploying and maintaining a clustered Kafka architecture is a massive anti-pattern (Operational Overkill). Use simpler, purpose-built Queue systems like RabbitMQ or managed AWS SQS.
2. **The "Poison Pill" Infinite Loop**: In a strict P2P Queue, if a Consumer encounters a fatal error parsing a message (e.g., a `NullPointerException`), it rejects the message. The Broker places it back at the front of the queue. The Consumer instantly pulls it again, crashes again, and loops infinitely. This single "Poison Pill" completely blocks the processing of all millions of healthy messages behind it. **Fix**: Always configure a Retry Limit and a Dead Letter Queue (DLQ). After 3 failed attempts, the Broker must automatically banish the poison pill to the DLQ, allowing the pipeline to continue.

---

## Related Topics

- For a high-level theoretical overview, see **[Messaging Overview](./overview.md)**.
- To understand why the Poison Pill happens, see **[Messaging Error Handling](./error-handling.md)**.
- For architectural implementation, see **[Event-Driven Architecture](../event-driven/overview.md)**.
