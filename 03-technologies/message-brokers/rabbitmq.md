# RabbitMQ

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Kafka là một cái Ống cống khổng lồ, thô bạo và chỉ biết xả dữ liệu thẳng xuống ổ cứng, thì **RabbitMQ** giống như một Trạm Bưu điện Trung tâm cực kỳ thông minh và tinh tế. Nó được xây dựng dựa trên giao thức chuẩn AMQP. Thay vì bắt các dịch vụ (Consumers) phải tự bơi vào đống dữ liệu để tìm thông tin của mình, RabbitMQ cung cấp một hệ thống Mạng lưới Định tuyến (Routing/Exchanges) phức tạp. Nó có thể phân loại: "Đơn hàng trên 1 triệu thì gửi vào kho VIP, Đơn hàng dưới 1 triệu gửi kho Thường, Đơn hàng bị lỗi gửi vào Thùng rác". Sự thông minh này biến RabbitMQ trở thành lựa chọn Số 1 cho các Hệ thống Giao dịch phức tạp, Fintech, E-Commerce nơi Logic Điều phối quan trọng hơn là Tốc độ luồng dữ liệu (Streaming).

</details>

> **Summary**: While Apache Kafka dominates the Big Data Streaming landscape through sheer brutal throughput, **RabbitMQ** remains the undisputed king of Traditional Message Queueing. Built natively to implement the Advanced Message Queuing Protocol (AMQP), RabbitMQ is characterized as a "Smart Broker with Dumb Consumers". Its architectural centerpiece is the **Exchange**, a sophisticated routing engine that acts before the Queue. Rather than dumping all messages into a unified log, Producers publish to an Exchange, which intelligently evaluates the message's `Routing Key` (or Headers) and mathematically binds it to specific individual queues based on complex regex patterns (Topic routing) or direct matches. It is highly stateful; it actively tracks the Acknowledgment (ACK) of every single message in RAM. Because of this intelligent routing and strict transactional reliability, RabbitMQ is the premier choice for complex Microservice Task Queuing, Financial state-machines, and E-Commerce order orchestration.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một Bưu điện Quốc gia (RabbitMQ).
1. **Người gửi (Producer)**: Bạn viết 100 bức thư, mỗi bức có ghi Địa chỉ rõ ràng (Routing Key) như: "Gửi team IT", "Gửi team Kế toán". Bạn ném tất cả vào Thùng thư màu đỏ trước bưu điện. Bạn đi về.
2. **Hệ thống phân loại (Exchange)**: Bên trong bưu điện có một cái máy quét siêu xịn. Máy quét đọc chữ "Gửi team IT" và lập tức ném bức thư đó vào cái Sọt (Queue) dành riêng cho team IT. Nếu bức thư có ghi "Gửi TẤT CẢ", nó lập tức copy bức thư ra làm 10 bản và ném vào 10 cái sọt khác nhau.
3. **Người nhận (Consumer)**: Các nhân viên bưu tá không cần suy nghĩ gì cả. Cứ thấy sọt của mình có thư thì thò tay vào bốc đi giao. Nếu giao thất bại (Khách đi vắng), nhân viên mang bức thư đó về ném lại vào sọt để hôm sau giao tiếp.

</details>

Imagine an Automated Mail Sorting Facility (RabbitMQ).
1. **The Producer**: A company drops off 10,000 packages. Each package has a specific zip code written on it (The Routing Key), e.g., "NY.Electronics" or "CA.Clothing".
2. **The Exchange (The Sorting Machine)**: The packages don't go straight to the delivery trucks. They go through a high-tech Sorting Machine. The machine reads the zip code. If the rule says "Send all NY.* to Truck 1", it slides it down that chute. If the rule says "Send all *.Clothing to Truck 2", it slides it down that chute.
3. **The Queues & Consumers**: The Trucks (Queues) and the Drivers (Consumers) are completely dumb. They don't know why a package was put in their truck. They just grab whatever is in their truck, deliver it, and ask the Sorting Facility for a Receipt of Delivery (ACK). If a driver crashes their truck, the Facility knows exactly which packages weren't delivered and puts them in a new truck.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

RabbitMQ có 4 thành phần "ma thuật" tạo nên sự khác biệt:
1. **Exchange (Máy phân loại)**: Tin nhắn KHÔNG BAO GIỜ được gửi thẳng vào Queue. Nó gửi vào Exchange. Có 4 loại máy phân loại: Direct (Gửi thẳng), Fanout (Gửi cho TẤT CẢ), Topic (Lọc theo mẫu `order.*`), Headers (Lọc theo siêu dữ liệu).
2. **Binding (Đường ống)**: Sự kết nối giữa Máy phân loại và Cái sọt (Queue).
3. **Queue (Hàng đợi)**: Nơi chứa tin nhắn chờ Consumer xử lý. RabbitMQ lưu tin nhắn trên RAM để chạy siêu nhanh, và có thể ghi xuống Ổ cứng (Durable) để đề phòng cúp điện.
4. **ACK / NACK (Xác nhận an toàn)**: Khi Consumer lấy tin ra, tin nhắn vẫn chưa bị xóa. Nếu Consumer chạy hàm 10 phút, báo lỗi, hoặc bị sập nguồn (Crash), RabbitMQ không nhận được lệnh "Đã xong" (ACK). Nó sẽ tự động hiện lại tin nhắn đó cho người khác xử lý. Không bao giờ mất tin.

</details>

RabbitMQ perfectly implements the AMQP Topology, strictly dividing the messaging pipeline into specialized components:
1. **The Exchange (The Router)**: Producers NEVER push messages directly to a queue. They publish payloads to an Exchange. The Exchange determines the message's destination based on mathematical rules.
   - *Direct Exchange*: Point-to-point exact string match.
   - *Fanout Exchange*: Pub/Sub broadcasting (clones the message to all bound queues).
   - *Topic Exchange*: Wildcard regex routing (e.g., routing key `payment.error.*`).
2. **Bindings**: The logical bridges linking an Exchange to a Queue. A Queue must "bind" itself to an Exchange and state: "Please send me all messages matching the word `error`".
3. **The Stateful Queue**: Queues hold the messages in RAM (and mirror them to disk if marked `Durable`). Unlike Kafka's log, RabbitMQ queues are ephemeral Data Structures. When a message is consumed and Acknowledged, it is physically deleted from the RAM.
4. **Strict Acknowledgements (ACK/NACK)**: RabbitMQ is highly stateful. It tracks the exact state of every message. If a Consumer pulls a message but disconnects the TCP socket before sending an `ACK` flag back to the broker, RabbitMQ assumes the Consumer died mid-processing and instantly re-queues the message to be picked up by another worker.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Giả sử bạn làm hệ thống Thanh toán thẻ tín dụng (FinTech).
Bạn có 1 cái Server Xử lý Thanh Toán (Consumer). Công việc này tốn 5 giây 1 lần. 
Vào ngày lễ, có 500.000 người mua hàng. Nếu dùng Kafka, mọi người xả 500.000 tin nhắn đó xuống cái Ống cống khổng lồ, Kafka sẽ cười nhạt vì chả xi nhê gì. Nhưng Server Thanh toán của bạn bị tắc nghẽn, nó đọc mãi không xong.
Lúc này, bạn khởi động thêm 50 Server Thanh toán (Scale up). Trong Kafka, bạn muốn 50 Server chạy song song thì phải cấu hình Partition phức tạp mệt mỏi.
Nhưng với RabbitMQ, nó hỗ trợ **Competing Consumers (Người tiêu dùng cạnh tranh)** hoàn hảo. Bạn chỉ cần cắm 50 Server đó vào CHUNG 1 cái Queue duy nhất. Bất kì máy nào rảnh rỗi là lập tức bốc 1 tin nhắn ra xử lý. Tự động chia đều tải (Load Balancing) mà không cần cấu hình thêm 1 dòng code nào. RabbitMQ sinh ra là để làm Task Queue (Hàng đợi công việc rác) hoàn hảo nhất.

</details>

Why use RabbitMQ when Apache Kafka can handle 10x the throughput?
Because high-throughput Streaming (Kafka) is fundamentally different from Task Queuing (RabbitMQ).
If you are building an Image Resizing microservice. Resizing a 4K image takes 10 seconds of heavy CPU time. During a spike, you receive 50,000 images.
In Kafka, distributing this work dynamically across a rapidly Auto-Scaling fleet of Kubernetes Pods is extremely painful, because Kafka locks a Partition to exactly ONE consumer. If you have 10 Partitions, you can only ever have 10 worker nodes.
RabbitMQ natively supports the **Competing Consumers Pattern**. You can have exactly ONE queue, but attach 500 Worker Nodes to it. As soon as a worker finishes its 10-second image, it reaches into the centralized Queue and pulls the next message. The broker automatically load-balances the workload fairly among all 500 workers without any Partition configurations. RabbitMQ exists to orchestrate complex, heavy, asynchronous Task Processing.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh tính năng Gửi Lại Tin Nhắn Lỗi (Retry Logic).
</details>

Visualizing Retries (Kafka vs RabbitMQ).

| Metric | Apache Kafka (Dumb Broker) | RabbitMQ (Smart Broker) |
|---|---|---|
| **Error Handling**| If a consumer hits an API timeout on Message #5, it crashes. Message #6 is stuck behind it. You must write manual code to skip #5 and push it to a secondary topic. | The consumer catches the timeout, replies with a `NACK` (Negative Ack), and the broker instantly puts Message #5 back in the queue for someone else to try. |
| **Dead Letter Queues (DLQ)** | Requires manual code architecture to implement. | **Natively Built-In**. If a message is NACK-ed 3 times, RabbitMQ's Exchange automatically routes it to a designated "Graveyard Queue" for manual developer review. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hàng đợi Công việc Nặng (Background Task Queues)**: Bạn nhấn "Xuất Báo cáo Excel". Backend tính toán mất 10 phút. Thay vì bắt bạn ngồi chờ Web xoay vòng vòng, Backend đẩy lệnh "Làm báo cáo số 123" vào RabbitMQ. 1 Server phụ chạy ẩn (Worker) sẽ lấy tin nhắn ra, hùng hục làm 10 phút, rồi bắn Notification về màn hình báo xong. Celery (Python) thường kẹp chung với RabbitMQ để làm việc này.
2. **Giao tiếp Microservices theo State (Trạng thái Đơn hàng)**: Khi Đơn hàng chuyển từ `CREATED` sang `PAID`, Exchange của RabbitMQ sẽ đọc chữ `PAID` và bắn tin nhắn sang Kho Hàng, Kế toán, và Giao Hàng. Lọc dữ liệu cực kì thông minh và độ trễ cực thấp.
3. **Delayed Messages (Hẹn giờ gửi tin)**: Tính năng mà Kafka không làm được (Hoặc làm rất khó). Bạn đăng ký tài khoản thành công. Bạn muốn hệ thống "Đợi đúng 3 ngày sau thì gửi Email nhắc nhở mua hàng". Bạn ném 1 tin nhắn vào RabbitMQ với thuộc tính `Delay = 72 giờ`. Tin nhắn sẽ nằm im trong ống nước 72 giờ, sau đó mới thò đầu ra cho Dịch vụ Email bắt lấy.

</details>

1. **Heavy Background Task Queues (Celery/Node workers)**: The canonical use case. A user clicks "Generate 50-page PDF Report". The HTTP API instantly returns 202 Accepted. The API pushes a JSON task to RabbitMQ. A fleet of Python `Celery` workers or Node.js background processors competitively pull from the Queue. RabbitMQ ensures that if a worker runs out of RAM mid-PDF, the task is safely redelivered to a healthy worker.
2. **Complex Microservice Routing (Event Topologies)**: In E-Commerce architectures, an order lifecycle is complex. A Topic Exchange acts as the central Nervous System. If a service publishes `order.payment.failed`, the Exchange natively routes this ONLY to the Fraud Detection Queue and the User Email Queue, completely bypassing the Shipping Queue. Kafka forces the Consumer to pull the data and ignore it manually; RabbitMQ filters it at the source, saving Consumer CPU.
3. **Delayed & Scheduled Messages**: A feature highly difficult to achieve in Kafka. A SaaS platform needs to "Send a Follow-up Email exactly 24 hours after Registration". With the RabbitMQ Delayed Message Plugin, you publish a message with a `delay: 86400000` header. The Broker holds the message invisibly in RAM for 24 hours, only dropping it into the Queue precisely when the timer expires.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Prefetch Count (Đừng tham lam ăn nhiều)**: RabbitMQ có thói quen "Đẩy" (Push) tin nhắn cho Consumer. Nếu trong Queue có 100.000 tin, nó đẩy hết cả 100.000 tin vào RAM của cái Server Consumer tội nghiệp. Server bị nghẽn RAM và chết.
   - *Luật bắt buộc*: Luôn cấu hình `Prefetch_Count = 1` hoặc `10`. Nghĩa là: "Chỉ đưa cho tôi 10 tin nhắn thôi. Tôi làm xong, tôi báo ACK (Xong), thì ông mới được đưa tôi 10 tin tiếp theo". Việc này đảm bảo Server không bao giờ bị quá tải.
2. **Sử dụng Dead Letter Exchanges (DLX)**: Không bao giờ được quên thiết lập DLX. Nếu hệ thống Email bị lỗi, tin nhắn gửi Email không thành công, Consumer sẽ báo lỗi. Nếu không có DLX, tin nhắn đó có thể bị xóa vĩnh viễn (Mất khách), hoặc bị nhét lại vào Queue lặp đi lặp lại vô hạn làm đứng hệ thống. DLX là "Thùng Rác An Toàn" để chứa các tin lỗi, đợi Dev vào sửa lỗi code rồi mới nhấn nút cho chạy lại.

</details>

1. **Mandatory QoS (Quality of Service) / Prefetch Limits**: Unlike Kafka where Consumers manually `Pull`, RabbitMQ actively `Pushes` messages to connected Consumers over TCP. If a Queue has 1 million messages, RabbitMQ will aggressively shove all 1 million into the Consumer's RAM buffer, instantly crashing the Node.js/Python process with an OOM Error. **Absolute Rule**: You must configure `channel.prefetch(10)`. This tells the Broker: "Only push a maximum of 10 unacknowledged messages to me. Stop sending until I reply with an ACK." This guarantees perfect Flow Control and prevents worker starvation.
2. **Architecting Dead Letter Exchanges (DLX)**: A Consumer encounters an unexpected `NullPointerException` and explicitly `NACKs` the message with `requeue=false`. Without a DLX, RabbitMQ permanently deletes the message, causing catastrophic data loss. **Rule**: Every single Queue you create MUST be configured with an `x-dead-letter-exchange` argument. When a message is rejected, expires (TTL), or the queue hits a length limit, the Broker automatically teleports the failed message to the DLX, dropping it into an "Investigation Queue" for developers to analyze the stack trace.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lầm tưởng RAM là Ổ Cứng**: RabbitMQ chạy cực nhanh vì nó để mọi thứ trên RAM. Đừng coi nó là Database. Nếu Consumer của bạn bị sập trong 3 ngày, 50 triệu tin nhắn bị kẹt lại trong RabbitMQ. Nó sẽ ăn cạn kiệt RAM của máy chủ, hệ điều hành Linux sẽ giết chết RabbitMQ (OOM Kill), và BẠN MẤT TOÀN BỘ 50 TRIỆU TIN NHẮN (dù có bật chế độ ghi ra đĩa Durable thì máy cũng sập). 
   - *Luật*: RabbitMQ phải được dọn dẹp liên tục. Nếu hàng đợi dài hơn 100.000, bạn đang có vấn đề khẩn cấp cần giải quyết ở Consumer.
2. **Sử dụng sai loại Exchange**: Dùng Fanout (Gửi cho tất cả) cho những tin nhắn bí mật, khiến dịch vụ khác nhận nhầm dữ liệu. Dùng Direct (Chuỗi chính xác) nhưng gõ sai 1 kí tự khiến tin nhắn bay vào Hố đen (Blackhole) vì không có Queue nào tên khớp với chữ đó. Phải luôn cẩn thận với Routing.

</details>

1. **The Infinite Backlog Memory Crash**: Kafka is perfectly happy holding 10 Terabytes of backlogged messages because it uses sequential disk files. RabbitMQ is highly stateful and stores message indices and metadata (and often the payloads) in RAM. If your Consumers die over the weekend, and RabbitMQ accumulates 10 million pending messages, the Erlang VM will exhaust the host OS RAM, trigger disk thrashing (Paging), and eventually crash entirely. **Rule**: RabbitMQ Queues must stay empty. It is a transit layer, not a datastore. Set Max Length policies (`x-max-length`) to physically drop old messages to protect the Broker if the Consumer backlog spirals out of control.
2. **The "Blackholing" of Messages**: In RabbitMQ, if a Producer publishes a message to an Exchange with a Routing Key of `order.canceled`, but no developer has created a Queue with a matching binding... the Exchange silently deletes the message. There is no error. It vanishes into a Blackhole. **Rule**: Utilize the Alternate Exchange (`alternate-exchange`) feature. If an Exchange cannot find a matching queue, it routes the orphaned message to a "Lost & Found" queue so administrators can catch architectural routing bugs.

---

## Related Topics

- For ultra-high throughput Append-Only logging and streaming, use **[Apache Kafka](./kafka.md)**.
- For asynchronous backend task processing (Celery/Bull), implement workers using **[Node.js](../backend/nodejs-express.md)** or **[Python](../backend/python-fastapi.md)**.
- For orchestrating massive multi-service workflows instead of event-choreography, consider **[Apache Airflow](../data-ai/apache-airflow.md)**.
