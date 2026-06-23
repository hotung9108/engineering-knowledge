# Apache Kafka

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Năm 2010, LinkedIn đối mặt với một vấn đề thảm họa: Hệ thống của họ sinh ra 1.000 tỷ tin nhắn mỗi ngày (Lượt Click, Lịch sử xem trang, Chat). Các hệ thống Message Broker truyền thống (như RabbitMQ) chạy quá chậm và liên tục sập vì cạn kiệt bộ nhớ. LinkedIn quyết định "đập đi xây lại" và tạo ra **Apache Kafka**. Thay vì cố gắng làm một người Môi giới thông minh quản lý từng tin nhắn, Kafka tự biến mình thành một **Cái Ống cống khổng lồ**. Nó không thèm quan tâm tin nhắn bay đi đâu, nó chỉ đơn thuần Ghi nối tiếp tất cả tin nhắn xuống Ổ cứng máy tính theo một hàng dọc liên tục (Append-only Log). Nhờ sự ngu ngốc và cục súc này, tốc độ của Kafka nhanh đến mức điên rồ. Nó có thể nuốt hàng triệu tin nhắn mỗi giây mà không bao giờ sập. Ngày nay, 80% các công ty Fortune 100 dùng Kafka làm xương sống cho toàn bộ dữ liệu của họ.

</details>

> **Summary**: In 2010, LinkedIn encountered a catastrophic scaling bottleneck. Traditional Message Brokers (like ActiveMQ/RabbitMQ) were inherently stateful; they actively tracked the acknowledgment status of every single message in memory. When LinkedIn attempted to pipe billions of User Activity events (clicks, page views) through these brokers, the memory tracking overhead caused fatal cluster collapses. LinkedIn engineered **Apache Kafka** by fundamentally inverting the architectural paradigm. Kafka is not a smart broker; it is a "Dumb Broker with Smart Consumers". It operates as a highly distributed, infinitely scalable, immutable **Commit Log**. Instead of maintaining complex routing tables, Kafka simply appends incoming bytes directly to disk sequentially. By leveraging the OS Page Cache and Zero-Copy network transfers, Kafka bypasses JVM memory entirely, achieving astronomical throughput (Millions of messages per second) and rendering legacy brokers obsolete for Big Data streaming pipelines.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một Đài Phát Thanh (Radio Station).
1. **RabbitMQ (Người đưa thư)**: Ai có nhu cầu nghe tin tức, Người đưa thư sẽ cầm tờ báo chạy đến tận nhà gõ cửa từng người, tận tay đưa báo, đợi người ta kí nhận rồi mới quay về. Rất an toàn, nhưng nếu có 1 triệu người đọc, Người đưa thư chết vì kiệt sức.
2. **Kafka (Đài Phát Thanh)**: Đài phát thanh chỉ làm đúng 1 việc: Gắn loa lên cột điện và phát oang oang ra ngoài đường. Nó không thèm quan tâm ai đang nghe, người nghe đã hiểu chưa, hay người nghe có ở nhà không. Ai muốn nghe thì Tự mua cái Đài Radio, tự dò đúng Tần số (Topic) và tự vểnh tai lên mà nghe (Consumer tự quản lý). Nhờ không phải đi giao thư, Đài Phát thanh có thể phục vụ hàng tỷ người nghe cùng một lúc mà không hề tốn thêm một giọt mồ hôi nào.

</details>

Imagine a Teacher assigning homework.
1. **RabbitMQ (The Stateful Tutor)**: The Tutor walks to Student A, hands them the math worksheet, waits for them to finish, grades it, takes the paper back, and then walks to Student B. If there are 10,000 students, the Tutor cannot physically track who has finished what.
2. **Kafka (The Public Noticeboard)**: The Teacher acts as a completely stateless entity. Every morning, they just staple a new Worksheet to a massive Public Noticeboard in the hallway (The Log). The Teacher does not care who looks at it. Student A might read Worksheet 1 today. Student B might be sick, come back 3 days later, and read Worksheets 1, 2, and 3 all at once. The Students (Consumers) are entirely responsible for remembering which Worksheet they are currently on (The Offset). The Teacher's only job is to infinitely staple new papers to the board.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cấu trúc của Kafka cực kì dị biệt so với các Broker khác:
1. **Topic & Partition**: Bạn không tạo Queue, bạn tạo Topic (Chủ đề). Ví dụ Topic `User_Clicks`. Để Scale, Topic này được băm ra thành nhiều ống nhỏ gọi là Partitions.
2. **Append-Only Log (Ghi nối tiếp)**: Tin nhắn rơi vào Topic sẽ được viết thẳng xuống Ổ cứng máy tính theo một hàng dọc (như file txt). Nó sẽ nằm chết ở đó. Không ai được quyền sửa hay xóa nó. Nó là Lịch sử bất biến (Immutable).
3. **Offset (Cột mốc)**: Consumer vào Topic đọc tin nhắn. Consumer đọc đến dòng số 5, nó tự ghi nhớ một con số gọi là `Offset = 5`. Lần sau nó vào, nó tự biết phải đọc tiếp từ dòng số 6.
4. **Retention (Khả năng lưu trữ vĩnh viễn)**: Khác với RabbitMQ (Consumer đọc xong là tin nhắn biến mất). Tin nhắn trong Kafka có thể được lưu trữ 7 ngày, 1 tháng, hoặc VĨNH VIỄN trên ổ cứng nếu bạn muốn. Nếu Consumer bị lỗi làm hỏng dữ liệu, nó hoàn toàn có thể "Tua lại thời gian" (Reset Offset về 0) và đọc lại từ đầu.

</details>

Kafka’s architecture completely abandons legacy Queueing theory in favor of Distributed Log theory:
1. **Topics & Partitions (The Unit of Scale)**: Messages are published to a categorized `Topic`. To achieve horizontal scalability, a Topic is physically divided into multiple `Partitions` distributed across numerous broker nodes. Partitions allow multiple Consumers to read the exact same Topic simultaneously in parallel without locking each other.
2. **The Immutable Commit Log**: Kafka does not hold messages in complex RAM data structures. It appends raw bytes sequentially to a `.log` file on Disk. Because it strictly utilizes sequential disk I/O, writing to a cheap HDD is actually faster than executing random writes to RAM. Data in Kafka is immutable; it cannot be updated or deleted individually.
3. **Consumer Offsets**: The Broker is dumb; it does not track Message Acknowledgements. The Consumer tracks its own state via an `Offset` (an integer pointing to the specific log line it just read). This radically reduces Broker CPU overhead.
4. **Data Retention (Replayability)**: In traditional Queues, once a message is consumed, it is destroyed. Kafka acts as a persistent database. Messages remain on disk according to a Time-To-Live policy (e.g., 7 days) or forever. This enables **Event Replay**—if a Consumer deploys buggy code and corrupts its database, engineers can simply revert the Consumer's Offset back 3 days and re-process the exact historical stream flawlessly.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vì sao Netflix, Uber, Spotify đều tôn thờ Kafka?
Giả sử bạn làm Uber. Mỗi 1 giây, 1 triệu chiếc xe ô tô gửi Tọa độ GPS lên Server. 
Bạn muốn:
- Dịch vụ Bản đồ lấy tọa độ để vẽ lên màn hình.
- Dịch vụ Tính tiền lấy tọa độ để tính cước phí.
- Dịch vụ AI lấy tọa độ để đoán xem chỗ nào đang kẹt xe.
Nếu dùng RabbitMQ, hệ thống phải tự "Copy" tin nhắn đó ra làm 3 bản và đẩy vào 3 cái ống cho 3 dịch vụ. 1 triệu x 3 = 3 triệu tin nhắn phải copy trong bộ nhớ. Máy chủ nổ tung.
Với Kafka, tin nhắn chỉ ghi ĐÚNG 1 LẦN xuống ổ cứng. Sau đó 3 dịch vụ kia tự bơi vào ổ cứng mà đọc. Dù có thêm 100 dịch vụ nữa vào đọc cũng không làm tăng tải cho máy chủ Kafka một chút nào. Sự chia tách tuyệt đối (Decoupling) này là lý do nó trở thành Xương sống (Backbone) của các công ty công nghệ lớn.

</details>

Why is Kafka the undisputed nervous system of every Fortune 500 tech architecture?
In modern Microservices, an event (e.g., `Payment_Completed`) must often be consumed by 10 completely different downstream services (Billing, Fraud Detection, Analytics, Email, Shipping).
In a legacy Push-Broker (RabbitMQ), the broker must physically clone the payload in memory and push it into 10 distinct queues. If the throughput is 100,000 messages/sec, the broker must execute 1,000,000 memory-intensive routing operations per second, causing GC pauses and cluster crashes.
Kafka operates on a **Pull Model**. The Producer writes the `Payment_Completed` event to Disk exactly once. The 10 downstream Consumer Groups independently connect to the broker and sequential read the exact same file from Disk using the OS Page Cache. Adding a 11th Consumer Group adds mathematically zero Write-Overhead to the Broker. This absolute decoupling allows Kafka to act as the Central Nervous System for massively distributed Data Lakes and Event-Driven Architectures.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh luồng xử lý tin nhắn Đặt hàng.
</details>

Visualizing Broker Paradigms (Smart Routing vs Dumb Log).

| Metric | RabbitMQ (Smart Broker) | Apache Kafka (Dumb Log) |
|---|---|---|
| **Routing** | Can easily route messages: "If VIP Customer, route to Queue A. Else, Queue B". | **Cannot route natively**. You must write a separate Microservice (Kafka Streams) to read the message, check if VIP, and write it to another Topic. |
| **Throughput** | Handles ~50,000 messages/sec. Begins to slow down if queues get too long (Millions of backlogged messages). | Handles **Millions** of messages/sec. Performance does not degrade even if the backlog is 5 Terabytes long, because it's just reading sequential disk blocks. |
| **Consumer Failure**| If Consumer crashes, message remains safely in the queue. | If Consumer crashes and restarts, it looks at its last saved `Offset` and resumes reading exactly where it left off. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Website Activity Tracking (Theo dõi hành vi người dùng)**: Khi bạn lướt Tiktok hay Shopee, mọi cú click, mọi lần dừng lại xem video đều được gửi về Server. Số lượng này khổng lồ đến mức phi lý. Chỉ có Kafka mới nuốt nổi lượng dữ liệu này để sau đó đưa vào cho AI học (Gợi ý video tiếp theo).
2. **Event Sourcing (Kiến trúc lưu trữ dạng Sự kiện)**: Thay vì lưu Database kiểu: `User: Tùng, Số dư: 50k`. Người ta lưu TẤT CẢ sự kiện tạo nên con số 50k đó vào Kafka: `[Nạp 100k, Mua áo 30k, Mua trà sữa 20k]`. Số dư 50k chỉ là kết quả tính toán cuối cùng. Nhờ lưu Lịch sử vĩnh viễn, khi bị Hacker tấn công hoặc tính sai tiền, chỉ cần Tua lại lịch sử (Replay Events) từ đầu là khôi phục được dữ liệu chuẩn xác nhất.
3. **Microservices Communication (Giao tiếp Dịch vụ quy mô lớn)**: Làm ống dẫn dữ liệu trung tâm cho hàng trăm dịch vụ siêu nhỏ trao đổi thông tin với nhau mà không sợ sập mạng.

</details>

1. **High-Velocity Telemetry & Clickstream Data**: The original LinkedIn use-case. Capturing granular User Activity events (mouse tracking, ad impressions, video watch-time metrics). This data is exceptionally high-volume but structurally simple. Kafka ingests these streams flawlessly and pipes them into Data Lakes (Snowflake/Hadoop) for offline Machine Learning model training.
2. **Event Sourcing Architectures**: In standard CRUD databases, an `UPDATE` irrevocably destroys the previous state. In highly audited environments (FinTech), destroying history is illegal. Event Sourcing dictates that Application State is derived from a chronological sequence of immutable Events (`Account_Created` $\rightarrow$ `Deposited_100` $\rightarrow$ `Withdrew_50`). Because Kafka natively provides an immutable, ordered, replayable Log, it is the perfect backing store for Event Sourcing implementations.
3. **Stream Processing (Real-Time ETL)**: Using **Kafka Streams** or Apache Flink. Instead of running a nightly Cron Job to aggregate Sales Data, a Kafka Streams application continuously reads the incoming `Orders` topic, calculates the moving 5-minute average Revenue in real-time, and outputs the result to a `Live_Dashboard` topic, enabling real-time analytics.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiểu rõ Sức mạnh của Partition (Phân vùng)**: 1 Topic trong Kafka bị giới hạn tốc độ bởi 1 Consumer. Nếu bạn muốn 10 Consumer chạy song song ăn dữ liệu cùng lúc, bạn PHẢI chia Topic đó ra thành ít nhất 10 Partitions. (1 Partition chỉ cho phép tối đa 1 Consumer trong 1 nhóm đọc). Số lượng Partition quyết định khả năng Scale của hệ thống.
2. **Sử dụng Partition Key khôn ngoan để đảm bảo Thứ tự**: Kafka KHÔNG đảm bảo thứ tự trên toàn Topic, nó chỉ đảm bảo thứ tự trên CÙNG 1 PARTITION. Nếu khách hàng thực hiện `Tạo Đơn Hàng` và ngay sau đó `Hủy Đơn Hàng`. Bạn bắt buộc phải gán `Key = Order_ID` cho 2 tin nhắn đó. Lúc này, Kafka sẽ dùng thuật toán Hashing để đẩy cả 2 tin nhắn đó vào chung 1 cái ống (Partition). Nhờ vậy, máy chủ Consumer chắc chắn sẽ đọc được lệnh `Tạo` trước, rồi mới đọc lệnh `Hủy`. Nếu bạn không gán Key, 2 tin văng vào 2 ống khác nhau, lệnh `Hủy` chạy trước lệnh `Tạo` $\rightarrow$ Bug hệ thống nghiêm trọng.

</details>

1. **Scale via Partitions (The Concurrency Model)**: In RabbitMQ, you can attach 50 consumers to 1 Queue. In Kafka, Concurrency is strictly bounded by the number of Partitions. If a Topic has 3 Partitions, you can have a maximum of 3 active Consumers in a Consumer Group. If you attach 5 Consumers, 2 will sit completely idle. **Rule**: Always over-provision Partitions initially (e.g., 30 partitions) to allow future horizontal scaling of your Kubernetes Consumer deployments. (Note: Changing partitions later breaks Key Hashing logic).
2. **Mastering the Partition Key (Guaranteeing Message Ordering)**: This is the most complex mechanic in distributed messaging. Kafka only guarantees strict chronological ordering *within a single Partition*. If a User clicks `Update_Profile_Name` to "Alex" and then to "Bob", those events must be processed sequentially. If you publish without a Key, Kafka Round-Robins them to different Partitions. Consumer 2 might process "Bob" before Consumer 1 processes "Alex", leaving the database permanently corrupted with the name "Alex". **Rule**: Always assign a unique Semantic Key (e.g., `User_ID` or `Order_ID`) to the Kafka Message. Kafka hashes the key and guarantees that all messages with the same ID mathematically route to the exact same Partition, preserving strict chronological ordering.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hội chứng "Đầu độc" (Poison Pill)**: Khác với RabbitMQ có tính năng tự động đá tin lỗi sang chỗ khác. Nếu Kafka Consumer đọc trúng 1 tin nhắn bị lỗi Format JSON, nó ném lỗi (Crash) và tự khởi động lại. Lần khởi động sau, Offset vẫn nằm ở chỗ cũ, nó LẠI ĐỌC TRÚNG tin nhắn đó và lại Crash. Hệ thống kẹt cứng mãi mãi ở 1 dòng dữ liệu.
   - *Cách giải quyết*: Phải dùng khối `try/catch` bắt lỗi triệt để. Nếu lỗi, bắt buộc phải tự viết code gửi tin lỗi đó sang một Topic riêng (Dead Letter Topic) và bằng mọi giá phải LƯU OFFSET để đi tiếp qua tin nhắn tiếp theo.
2. **Kafka không dành cho App bé**: Đừng xài Kafka nếu bạn chỉ có vài chục request mỗi phút. Hệ sinh thái Kafka phụ thuộc vào Zookeeper/KRaft, tốn cực kỳ nhiều RAM (Java) và công sức vận hành. Giết gà đừng dùng đao mổ trâu.

</details>

1. **The Poison Pill Deadlock**: The most fatal operational bug in Kafka. Kafka lacks native Dead Letter Queues (unlike AWS SQS or RabbitMQ). If a Consumer encounters an un-parseable JSON payload, throws an Exception, and fails to commit its Offset, it will crash. Upon Kubernetes restart, it fetches the exact same offset, hits the exact same bad payload, and crashes infinitely. The entire Partition is permanently blocked. **Rule**: Your Consumer MUST wrap the deserialization and processing logic in an impenetrable `try/catch` block. If parsing fails, the Consumer must explicitly publish the raw payload to a custom `Dead_Letter_Topic`, catch the error gracefully, and manually `Commit` the offset to advance past the poison pill.
2. **Operational Overhead (The Big Data Trap)**: Kafka is not a lightweight Docker container. It is a massive JVM application traditionally reliant on ZooKeeper for cluster consensus (though KRaft is replacing it). Operating a Highly-Available production Kafka cluster requires immense JVM tuning, disk I/O monitoring, and dedicated DevOps personnel. **Rule**: Do not adopt Kafka for simple asynchronous task queues (like sending Emails or resizing images). For simple task routing, stick to **RabbitMQ** or Redis.

---

## Related Topics

- For complex, stateful Microservice routing, use **[RabbitMQ](./rabbitmq.md)** instead.
- Kafka is often the backbone for Data Lakes and ML pipelines heavily written in **[Python](../data-ai/python-ai.md)**.
- Kafka pairs perfectly with **[Go](../backend/go.md)** for writing hyper-fast, low-memory Consumers.
