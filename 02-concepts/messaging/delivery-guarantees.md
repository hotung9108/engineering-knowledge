# Delivery Guarantees

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi bạn gửi một kiện hàng qua bưu điện, bạn luôn có nỗi sợ: "Nhỡ hàng bị mất thì sao?". Trong hệ thống Messaging cũng vậy, dữ liệu truyền qua mạng có thể bị rớt do đứt cáp, sập server. **Delivery Guarantees (Các mức độ Đảm bảo Giao hàng)** là những bản cam kết của Message Broker về khả năng sống sót của tin nhắn. Có 3 mức độ: At-Most-Once (Chỉ gửi 1 lần, mất ráng chịu), At-Least-Once (Chắc chắn tới nơi, nhưng có thể bị nhận trùng 2 lần), và Exactly-Once (Chén thánh: Chắc chắn tới nơi đúng 1 lần duy nhất).

</details>

> **Summary**: Network partitions, node crashes, and consumer timeouts are mathematical certainties in distributed systems. When a Publisher emits a message, what guarantees does the system provide regarding its successful delivery to the Consumer? **Delivery Guarantees** define the rigorous architectural contracts provided by a Message Broker. Software engineers must choose between three fundamental paradigms: **At-Most-Once** (Fire and forget, potential data loss), **At-Least-Once** (Guaranteed delivery, potential duplication), and the elusive **Exactly-Once** (The Holy Grail of messaging, mathematically complex and highly resource-intensive).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (Producer) ném một quả bóng (Tin nhắn) cho một người bạn đứng bên kia bờ sông (Consumer). Sông hay có gió mạnh thổi bay bóng.
1. **At-Most-Once (Tối đa 1 lần)**: Bạn ném quả bóng đi. Kệ nó. Rớt xuống sông thì thôi, bạn không ném lại quả khác. Bạn của bạn hoặc chụp được, hoặc không có gì. Không bao giờ có chuyện nhận 2 quả bóng.
2. **At-Least-Once (Ít nhất 1 lần)**: Bạn ném quả bóng đi. Nếu trong 5 giây mà bạn không nghe thằng bạn hét lên "Bắt được rồi!", bạn sẽ lấy quả bóng khác ném tiếp. Đôi khi thằng bạn bắt được quả 1 rồi, nhưng hét hơi nhỏ nên bạn không nghe thấy, bạn lại ném thêm quả 2. Kết quả: Thằng bạn chắc chắn có bóng, nhưng có lúc ôm tận 2 quả.
3. **Exactly-Once (Đúng 1 lần duy nhất)**: Bằng một phép màu ma thuật nào đó, hệ thống luôn đảm bảo thằng bạn chỉ có đúng 1 quả bóng trên tay. Không mất, cũng không dư.

</details>

Imagine you (The Publisher) are firing a t-shirt cannon into a massive crowd, aiming for a specific person (The Consumer).
1. **At-Most-Once (Fire and Forget)**: You fire the t-shirt into the crowd and instantly turn away. Maybe the person caught it. Maybe someone else intercepted it. Maybe it hit the ceiling and fell into the trash. You don't care. The person gets zero or one t-shirt.
2. **At-Least-Once (Guaranteed Delivery)**: You fire the t-shirt. You stare at the person. If they do not explicitly raise their hand and yell "I GOT IT!" within 10 seconds, you fire a *second* t-shirt. Sometimes, they catch the first one but forget to yell. So they catch the second one too. They now have two t-shirts (Duplication). But you guarantee they have *at least* one.
3. **Exactly-Once (The Holy Grail)**: Through complex cryptographic accounting and perfectly synced stopwatches, the system mathematically guarantees that the person walks away with precisely one t-shirt. No lost shirts, no duplicate shirts.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. At-Most-Once (Tối đa 1 lần)**
- Tin nhắn gửi đi một lần duy nhất. Tốc độ cực nhanh (Vì không tốn công chờ xác nhận ACK).
- Nguy cơ: Mất dữ liệu vĩnh viễn nếu mạng bị lag hoặc Consumer chết giữa chừng.

**2. At-Least-Once (Ít nhất 1 lần)**
- Broker sẽ giữ tin nhắn cho đến khi Consumer gửi phản hồi `ACK` (Tôi đã xử lý xong). Nếu sau 1 phút không thấy `ACK`, Broker sẽ gửi lại tin nhắn đó lần 2.
- Nguy cơ: Xử lý trùng lặp. (Consumer đã xử lý xong, nhưng lúc gửi `ACK` thì đứt mạng. Broker tưởng chưa xong nên gửi lại lần 2).

**3. Exactly-Once (Đúng 1 lần)**
- Sự kết hợp hoàn hảo. Đảm bảo 100% tin nhắn đến đích và 100% không bao giờ xử lý trùng.
- Đòi hỏi sự phối hợp cực độ giữa Producer (Idempotent Key), Broker (Deduplication) và Consumer (Transactional State). Tốc độ rất chậm.

</details>

**1. At-Most-Once (Fire and Forget)**
- **Mechanics**: The Publisher transmits the message and immediately considers it "Done". There is no network acknowledgment (`ACK`) required from the Broker or the Consumer.
- **Trade-off**: Absolute maximum throughput and zero latency overhead. Extremely high risk of permanent data loss during network partitions.

**2. At-Least-Once (Acknowledge and Retry)**
- **Mechanics**: The Broker retains the message in memory/disk. The Consumer processes the message and explicitly sends an `ACK` signal back to the Broker. Only upon receiving the `ACK` does the Broker permanently delete the message. If the `ACK` times out, the Broker re-delivers the message.
- **Trade-off**: Guarantees zero data loss. High risk of Duplicate Processing (e.g., if the Consumer processes the data successfully but crashes milliseconds before transmitting the `ACK`).

**3. Exactly-Once (Transactional Messaging)**
- **Mechanics**: The system guarantees that a message is processed and its effects are persisted to the database exactly one time. This requires complex transactional boundaries spanning the Publisher, Broker, and Consumer.
- **Trade-off**: The gold standard of data integrity. Extremely difficult to implement correctly and incurs massive performance penalties due to distributed locking and multi-phase commits.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao không dùng `Exactly-Once` cho tất cả mọi thứ? Vì nó quá tốn kém và làm chậm hệ thống. Trong kỹ thuật, chúng ta phải "Đánh đổi" (Trade-off) dựa trên bài toán thực tế.
- **Khi nào chọn At-Most-Once?** Ứng dụng đo nhiệt độ máy chủ. 1 giây gửi 100 tin nhắn báo nhiệt độ. Mất 1 tin nhắn không sao cả, giây sau lại có tin nhắn mới. Tốc độ là ưu tiên số 1.
- **Khi nào chọn At-Least-Once?** 99% các hệ thống thực tế dùng cái này. Việc thiết lập nó dễ, đảm bảo không mất dữ liệu. Chỉ cần lập trình viên code thêm tính năng "Chống trùng lặp" (Idempotency) ở phía Consumer là hệ thống an toàn tuyệt đối.
- **Khi nào chọn Exactly-Once?** Các hệ thống giao dịch Tài chính, Ngân hàng lõi (Core Banking). Nơi mà sai 1 đồng cũng là đi tù.

</details>

Architects do not default to `Exactly-Once` because of the **CAP Theorem** and raw physics. Forcing strict transactional consensus across a distributed network introduces crippling Latency and reduces Availability. System Design is the art of Trade-offs.
- **Why At-Most-Once?** High-frequency, low-value telemetry. IoT sensors emitting temperature readings 100 times a second. Losing a single data packet is statistically irrelevant. The architecture prioritizes raw network throughput and minimal memory utilization.
- **Why At-Least-Once?** The industry standard default for 99% of business applications (e.g., E-commerce orders). It guarantees the Order is never lost. The resulting duplication risk is gracefully handled by enforcing Idempotency at the application layer, balancing high throughput with data safety.
- **Why Exactly-Once?** Absolute Financial/Legal requirements. Core Banking ledgers, Stock Market trades, or Billing engines where processing a $50,000 transaction twice results in catastrophic real-world legal consequences.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt khi Mạng bị lỗi ở giai đoạn gửi ACK.
</details>

Visualizing the failure state when the Consumer processes the data but fails to send the Acknowledgment.

| Event Sequence | At-Most-Once | At-Least-Once | Exactly-Once |
|---|---|---|---|
| **1. Delivery** | Broker sends MSG. | Broker sends MSG. | Broker sends MSG. |
| **2. Processing**| Consumer deducts $50. | Consumer deducts $50. | Consumer deducts $50. |
| **3. Network Error**| (No ACK needed anyway) | `ACK` is lost in transit. | `ACK` is lost in transit. |
| **4. Broker Action**| MSG is already deleted. | Timeout! Broker re-sends MSG. | Timeout! Broker re-sends MSG. |
| **5. Consumer Action**| Does nothing. | Consumer deducts **another $50**. | Consumer detects duplicate ID, drops MSG. |
| **Final Result** | Perfect (Lucky). | **Customer loses $100**. | Perfect (Safe). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **At-Most-Once (Tối đa 1 lần)**: Gửi Log (Log Aggregation), Ghi nhận lượt xem Video, Thống kê người dùng Online. Những hệ thống mà độ chính xác 99.9% là đủ tốt, không cần đến 100%.
- **At-Least-Once (Ít nhất 1 lần)**: Gửi Email Xác nhận, Xử lý Đơn hàng E-commerce, Tạo tài khoản. Nếu hệ thống vô tình gửi 2 email giống hệt nhau, người dùng hơi phiền một chút nhưng không mất mát tiền bạc.
- **Exactly-Once (Đúng 1 lần)**: Apache Kafka có hỗ trợ Exactly-Once Semantics (EOS). Được dùng trong hệ thống Thanh toán thẻ tín dụng, Xử lý giao dịch Blockchain, Hệ thống Kế toán cốt lõi.

</details>

- **At-Most-Once Use Cases**: Telemetry, Metrics, and Non-Critical Logs. A web server firing "Page View" events to Google Analytics. If a network blip causes a single page view event to drop out of 10 million, the resulting analytical graph is functionally identical.
- **At-Least-Once Use Cases**: Standard Business Workflows (e.g., E-commerce Order Pipelines). Sending an "Order Confirmed" email. It is acceptable if a user occasionally receives two identical confirmation emails due to a retry logic. It is *unacceptable* if they receive zero emails and think their order failed.
- **Exactly-Once Use Cases**: Financial Ledgers and Distributed Databases. When a payment gateway processes a Stripe transaction. Kafka Streams architectures utilizing the EOS (Exactly-Once Semantics) configuration to ensure financial aggregates are mathematically perfect.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Idempotency là chìa khóa vàng**: Vì Exactly-Once quá khó cài đặt, các kỹ sư phần mềm tạo ra một "Cú lừa" hoàn hảo. Họ cấu hình Broker chạy ở mức `At-Least-Once` (rất nhanh và dễ). Sau đó họ viết code ở Consumer sao cho nó có tính **Idempotent** (Dù nhận trùng 100 tin nhắn thì cũng chỉ tính là 1). Vậy là họ đạt được Exactly-Once mà không tốn tài nguyên cấu hình mạng.
2. **Quản lý Dead Letter Queue (DLQ)**: Khi chạy `At-Least-Once`, Broker sẽ gửi lại tin nhắn mãi mãi nếu không nhận được ACK. Nếu lỗi xảy ra do Code của bạn sai (chứ không phải do mạng), tin nhắn đó sẽ bị kẹt vĩnh viễn (Poison Message). Bắt buộc phải set số lần Retry tối đa (Ví dụ: 3 lần), sau đó vứt tin nhắn đó vào Thùng rác (DLQ) để xử lý bằng tay sau.

</details>

1. **The Idempotency Hack (Pseudo-Exactly-Once)**: In modern cloud architecture, achieving native Exactly-Once routing at the TCP network layer is heavily discouraged due to performance constraints. The industry standard "Hack" is to configure the Message Broker for **At-Least-Once** delivery (which is extremely fast and guarantees no data loss), and shift the responsibility to the Application layer. The Consumer's code is strictly written to be **Idempotent**. It checks a database index (e.g., `SELECT exists FROM processed_events WHERE message_id = X`) before executing. This achieves Exactly-Once business outcomes without network overhead.
2. **DLQ Routing for Poison Messages**: In an At-Least-Once topology, a Consumer will automatically `NACK` (Negative Acknowledge) or simply crash if a message payload is structurally malformed (e.g., missing a required JSON bracket). The Broker will relentlessly retry delivering this "Poison Pill", causing an infinite loop that paralyzes the queue. You **MUST** define a `MaxReceiveCount` policy. After 3 or 5 retries, the Broker automatically redirects the unprocessable message to a Dead Letter Queue (DLQ) for manual engineering investigation.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Gửi ACK quá sớm**: Code lỗi sơ đẳng nhất. Vừa lấy tin nhắn từ Broker ra, Lập trình viên lập tức gọi lệnh gửi `ACK` luôn (vì nghĩ là chắc chắn code sẽ chạy xong). Giữa chừng code bị lỗi Null Pointer Exception. Tin nhắn biến mất khỏi Broker vĩnh viễn $\rightarrow$ Hệ thống bị mất dữ liệu. 
   - *Luật tối thượng*: Chỉ gửi `ACK` ở dòng code CUỐI CÙNG sau khi đã Lưu vào Database thành công.
2. **Không khóa Database khi dùng Idempotency**: Khi 2 tin nhắn trùng lặp đến CÙNG MỘT PHẦN NGHÌN GIÂY. Hai luồng code cùng kiểm tra DB: "Tin nhắn này xử lý chưa?". DB trả lời cả 2: "Chưa". Thế là cả 2 luồng cùng nhào vô xử lý, tính Idempotency bị phá vỡ. Phải dùng lệnh khóa DB (Ví dụ: `SELECT FOR UPDATE` hoặc Unique Constraint) để chặn.

</details>

1. **Premature Acknowledgment (Data Loss)**: A critical developer anti-pattern. A Junior Engineer pulls a message from RabbitMQ and immediately executes `channel.basicAck()`, *before* executing the complex database insertion logic. If the database insertion throws a `SQLException` or the pod crashes, the data is permanently lost because the Broker already deleted the message. **Absolute Rule**: Auto-Acknowledgment MUST be disabled. Manual `ACK` must be the absolute final line of code executed in the try block, strictly *after* the Database `COMMIT` is successful.
2. **Race Conditions in Idempotency Checks**: A system configures an Idempotency table in MySQL. A network glitch causes the Broker to deliver the exact same message to two different Consumer instances simultaneously. Both instances execute `SELECT count FROM logs WHERE msg_id = 123` at the exact same millisecond. Both receive `0`. Both proceed to charge the credit card. **Fix**: Do not rely on sequential `SELECT` then `INSERT`. You must enforce a Database-level `UNIQUE CONSTRAINT` on the `message_id` column. The second thread will be violently rejected by the database engine with a Unique Key Violation, preserving the idempotency.

---

## Related Topics

- For a high-level theoretical overview, see **[Messaging Overview](./overview.md)**.
- To understand why duplicate messages happen, study **[Messaging Patterns](./patterns.md)**.
- For managing failed messages (Poison Pills), read **[Error Handling](./error-handling.md)**.
