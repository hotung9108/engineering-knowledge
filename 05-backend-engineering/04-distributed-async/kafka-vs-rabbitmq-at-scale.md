# Kafka vs RabbitMQ at Scale

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: So sánh kiến trúc chuyên sâu của hai Message Broker thống trị thị trường, tập trung vào ngữ nghĩa truyền tin (Dumb Broker vs Smart Broker), cách mở rộng nhóm tiêu thụ (consumer group scaling), lưu giữ nhật ký và các chiến lược xử lý hàng đợi chết (dead-letter queue).

</details>

> **Summary**: A deep architectural comparison of the two dominant message brokers, focusing on messaging semantics (Dumb Broker vs Smart Broker), consumer group scaling, log retention, and dead-letter queue strategies.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Kafka và RabbitMQ đều là người đưa thư nhưng cách làm việc hoàn toàn khác nhau.
- **RabbitMQ (Giống như bưu điện)**: Bưu điện nhận thư, phân loại rất thông minh và giao tận tay cho bạn. Khi bạn nhận được thư, bưu điện coi như hoàn thành nhiệm vụ và xóa thông tin về lá thư đó. Phù hợp cho việc gửi email, xử lý ảnh chạy ngầm.
- **Kafka (Giống như bảng tin khổng lồ)**: Nó chỉ dán các thông báo mới vào cuối bảng tin một cách mù quáng (Dumb Broker). Ai muốn đọc thì tự vác xác ra bảng tin mà đọc, và phải tự nhớ xem hôm qua mình đã đọc đến dòng thứ mấy (Offset). Nhờ vậy, Kafka chạy nhanh khủng khiếp và dữ liệu không bao giờ bị mất đi sau khi có người đọc.

</details>

Kafka and RabbitMQ are both message brokers but work very differently.
- **RabbitMQ (Like a Post Office)**: It receives letters, routes them smartly, and delivers them directly to you. Once you receive the letter, the post office considers its job done and deletes the record of the letter. Great for sending emails or processing background tasks.
- **Kafka (Like a Giant Noticeboard)**: It blindly pins new notices to the bottom of the board (Dumb Broker). If you want to read them, you have to go to the board and remember which line you read last time (Offset). Because of this simplicity, Kafka is insanely fast, and data is never deleted just because someone read it.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **RabbitMQ**: Một message broker mã nguồn mở tuân theo giao thức AMQP. Kiến trúc của nó dựa trên Queue (Hàng đợi), thiết kế cho độ trễ thấp, định tuyến phức tạp và dữ liệu tin nhắn tạm thời.
- **Apache Kafka**: Một nền tảng Event Streaming phân tán. Kiến trúc của nó dựa trên Log (Nhật ký chỉ ghi thêm), thiết kế cho thông lượng khổng lồ, lưu trữ dữ liệu bền vững và khả năng phát lại (replay) sự kiện.

**Phân loại:**
- **Loại**: Phân tán Bất đồng bộ / Message Brokers.
- **Kiến trúc**: Queue (RabbitMQ) so với Append-Only Log (Kafka).

</details>

- **RabbitMQ**: An open-source message broker implementing the AMQP protocol. It uses a queue-based architecture designed for low-latency, complex routing, and transient messages.
- **Apache Kafka**: A distributed event streaming platform. It uses a log-based architecture designed for high-throughput, data retention, and event replayability.

### Classification
- **Type**: Distributed Async / Message Brokers.
- **Architecture**: Queue (RabbitMQ) vs. Append-Only Log (Kafka).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Các Microservices cần giao tiếp bất đồng bộ để duy trì tính độc lập và khả năng chịu lỗi.

**RabbitMQ** được tạo ra cho các luồng định tuyến phức tạp và các hàng đợi tác vụ. Nếu một service cần xử lý ảnh chạy ngầm, nó ném tin nhắn vào queue, một worker sẽ lấy ra xử lý, và tin nhắn đó bị hủy.

**Kafka** được LinkedIn tạo ra vì các hệ thống Message Queue truyền thống không thể chịu tải nổi lượng truy cập khổng lồ (hàng triệu lượt click website mỗi giây). Kafka lưu trữ sự kiện vĩnh viễn trên ổ cứng, cho phép nhiều hệ thống khác nhau (ví dụ: Phân tích Dữ liệu, Chống gian lận, Thanh toán) đọc cùng một tập sự kiện đó một cách hoàn toàn độc lập với tốc độ của riêng chúng.

</details>

Microservices need to communicate asynchronously to remain decoupled and resilient. 

**RabbitMQ** was built for complex routing and task queues. If a service needs to process an image in the background, it drops a message in a queue, a worker processes it, and the message is destroyed.

**Kafka** was built by LinkedIn because traditional message queues couldn't handle the massive throughput of tracking millions of website clicks per second. Kafka stores events persistently on disk, allowing multiple different systems (e.g., Analytics, Fraud Detection, Billing) to read the same events independently at their own pace.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Kiến trúc RabbitMQ (Queue)**: Gửi tin -> Định tuyến vào Queue -> Consumer đọc -> Gửi cờ ACK (Xác nhận) -> Broker xóa tin.
**Kiến trúc Kafka (Log)**: Gửi tin -> Ghi vào cuối file Log trên ổ cứng -> Consumer tự tìm vị trí để đọc -> Consumer tự lưu lại vị trí (Offset) -> Broker kệ, không xóa tin.

</details>

### Architecture: RabbitMQ (Queue-based)
1. Producer sends message to an `Exchange`.
2. Exchange routes message to one or more `Queues` based on routing keys.
3. Consumer connects to the `Queue`.
4. Consumer reads message -> sends `ACK` -> RabbitMQ **deletes** the message.

### Architecture: Kafka (Log-based)
1. Producer sends message to a `Topic`.
2. Kafka appends the message to the end of a `Partition` on disk.
3. Consumer reads messages sequentially from its current `Offset`.
4. Consumer commits the `Offset`. The message **remains on disk** until the retention period expires (e.g., 7 days).

| Feature | RabbitMQ | Apache Kafka |
|---|---|---|
| Architecture | Smart Broker / Dumb Consumer | Dumb Broker / Smart Consumer |
| Data Retention | Deleted after ACK (Transient) | Retained for configurable time (Persistent) |
| Routing | Complex (Direct, Topic, Fanout, Headers) | Simple (Topic/Partition only) |
| Throughput | 10K - 50K msg/sec | 100K - 1M+ msg/sec |
| Event Replay | No (once consumed, it's gone) | Yes (just reset the consumer offset) |
| Scaling | Add more workers to read the queue | Max consumers = Max partitions |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Khi nào dùng RabbitMQ**
1. **Hàng đợi tác vụ**: Gửi email chào mừng, tạo PDF, xử lý ảnh nền.
2. **Định tuyến phức tạp**: Gửi tin nhắn vào các queue khác nhau dựa trên các giá trị header tự động.
3. **Hàng đợi ưu tiên**: Xử lý yêu cầu của tài khoản VIP trước tài khoản Free.
4. **Tin nhắn trễ hẹn**: Yêu cầu gọi lại API nếu lỗi đúng 5 phút sau (dùng Delay Exchange).

**Khi nào dùng Kafka**
1. **Event Sourcing**: Lưu mọi sự thay đổi trạng thái như là một sự kiện bất biến.
2. **Xử lý Stream**: Gom nhóm dữ liệu theo thời gian thực (ví dụ: Tính trung bình số tiền giao dịch trong khoảng thời gian cửa sổ 5 phút).
3. **Gom Log**: Hút log từ 1000 microservice vào một mỏ dữ liệu trung tâm.
4. **Fan-out cực lớn**: Một sự kiện `OrderPlaced` cần được 20 service khác nhau tiêu thụ độc lập mà không cần phải cấu hình các đường ống routing phức tạp.

**Không nên làm**:
- **Dùng Kafka cho các tác vụ ngầm đơn giản**: Kiến trúc Partition của Kafka khiến nó rất khó để làm các việc như "Hàng đợi ưu tiên" hoặc "Retry từng tin nhắn". RabbitMQ làm việc này tốt hơn gấp vạn lần.
- **Dùng RabbitMQ cho Event Sourcing**: RabbitMQ sẽ xóa tin nhắn. Bạn không thể tái tạo lại lịch sử Database từ một hàng đợi của Rabbit.

</details>

### When to use RabbitMQ
1. **Task Queues**: Sending welcome emails, generating PDFs, background image processing.
2. **Complex Routing**: Sending messages to different queues based on dynamic header values.
3. **Priority Queues**: Processing premium user requests before free user requests.
4. **Delayed Messaging**: Retrying a failed API call after exactly 5 minutes (using Delay Exchange).

### When to use Kafka
1. **Event Sourcing**: Storing every state change of an entity as an immutable event.
2. **Stream Processing**: Aggregating data in real-time (e.g., calculating the average transaction value over a 5-minute sliding window using Kafka Streams).
3. **Log Aggregation**: Collecting logs from 1000 microservices into a centralized data lake.
4. **Massive Fan-out**: One event (e.g., `OrderPlaced`) that needs to be consumed independently by 20 different microservices without configuring complex routing bindings.

### Anti-Patterns
- **Using Kafka for simple background jobs**: Kafka's partition architecture makes it difficult to implement simple priority queues or granular retries. RabbitMQ is much better for standard worker queues.
- **Using RabbitMQ for Event Sourcing**: RabbitMQ deletes messages. You cannot rebuild a database state from a RabbitMQ queue.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**RabbitMQ: Scale và Dead-Lettering**
1. **Dead-Letter Exchanges (DLX)**: Nếu 1 worker lỗi 3 lần khi đọc 1 tin nhắn, hãy cấu hình đẩy nó vào DLX (Hàng đợi chết). Sẽ có đội ngũ hoặc worker khác phân tích rác ở đây.
2. **Prefetch Count**: Tuyệt đối không để prefetch là vô cực. Nếu 1 worker kéo 10,000 tin vào RAM rồi bị crash, toàn bộ sẽ phải xử lý lại. Cài `prefetch=10` để nó làm tới đâu lấy tới đó.
3. **Tính sẵn sàng cao**: Dùng Quorum Queues (thuật toán Raft) thay vì kiểu Mirrored Queues cổ điển.

**Kafka: Partitions và Consumer Groups**
1. **Chiến lược Phân mảnh (Partition)**: Kafka CHỈ BẢO ĐẢM THỨ TỰ TRONG CÙNG 1 PARTITION. Nếu bạn cần các sự kiện của một user cụ thể phải chạy theo đúng thứ tự, hãy dùng `userId` làm khóa của tin nhắn. Kafka sẽ nhét tất cả tin của user đó vào cùng 1 partition.
2. **Giới hạn Scale**: Bạn không thể có số Consumer nhiều hơn số Partition. Topic có 3 part, bạn cắm 4 máy chủ vào đọc thì 1 máy sẽ ngồi chơi xơi nước. Hãy luôn khai báo dư Partition ngay từ đầu (vd: 30 partitions).
3. **Bão Rebalance**: Nếu 1 máy chủ đọc tin nhắn và xử lý quá lâu, Kafka tưởng máy đó chết nên đuổi cổ nó ra, đẩy tin nhắn sang máy khác. Máy khác lại xử lý lâu... gây ra vòng lặp vô tận (Bão Rebalance). Hãy chắc chắn code xử lý của bạn phải chạy nhanh!

</details>

### RabbitMQ: Scaling and Dead-Lettering
1. **Dead-Letter Exchanges (DLX)**: If a worker fails to process a message 3 times, configure the queue to route it to a DLX. A separate worker can inspect these poisoned messages or alert the team.
2. **Prefetch Count**: Never set prefetch to unlimited. If a worker fetches 10,000 messages into RAM and crashes, those messages must be re-queued. Set `prefetch=10` to ensure workers only take what they can handle.
3. **High Availability**: Use Quorum Queues (Raft consensus) instead of classic mirrored queues for modern, fault-tolerant RabbitMQ clusters.

### Kafka: Partitions and Consumer Groups
1. **Partitioning Strategy**: Kafka guarantees message ordering *only within a partition*. If you need order events for a specific user to be processed sequentially, use the `userId` as the message key. All messages for that user will go to the same partition.
2. **Scaling Limit**: You cannot have more active consumers in a group than you have partitions. If a topic has 3 partitions and you deploy 4 instances of your microservice, 1 instance will sit idle doing nothing. Always over-partition upfront (e.g., 30 partitions).
3. **The Rebalance Storm**: If a consumer takes too long to process a message (exceeds `max.poll.interval.ms`), Kafka thinks the consumer is dead and triggers a rebalance. The consumer gets kicked out, and the message is reassigned, causing an infinite processing loop. Ensure your processing logic is fast!

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- Bên RabbitMQ: Khai báo Main Queue đi kèm với các Argument cấu hình DLX. Nếu lỗi, rác tự động bay sang DLX.
- Bên Kafka: Khai báo `@KafkaListener` với concurrency (Số luồng chạy song song).

</details>

### Spring Boot: RabbitMQ Retry and Dead Letter Queue Setup

```java
import org.springframework.amqp.core.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitConfig {

    // 1. Define the Dead Letter Queue
    @Bean
    Queue deadLetterQueue() {
        return QueueBuilder.durable("order.dlq").build();
    }

    // 2. Define the Main Queue, pointing to the DLX on failure
    @Bean
    Queue mainQueue() {
        return QueueBuilder.durable("order.queue")
                .withArgument("x-dead-letter-exchange", "")
                .withArgument("x-dead-letter-routing-key", "order.dlq")
                .build();
    }
}
```

### Spring Boot: Kafka Key-Based Ordering & Consumer Group

```java
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Service;

@Service
public class OrderKafkaListener {

    // Listens to the 'orders' topic.
    // Kafka ensures all messages with the same key (e.g., orderId) 
    // are processed sequentially by this single thread.
    @KafkaListener(
        topics = "orders", 
        groupId = "inventory-service-group",
        concurrency = "3" // Spins up 3 threads (assuming topic has >= 3 partitions)
    )
    public void listen(String messagePayload, 
                       @Header(KafkaHeaders.RECEIVED_KEY) String key,
                       @Header(KafkaHeaders.RECEIVED_PARTITION) int partition) {
        
        System.out.printf("Processing order %s from partition %d: %s%n", 
                           key, partition, messagePayload);
        // Process business logic
    }
}
```

---

## Related Topics

- [Transactional Outbox Pattern](./transactional-outbox-pattern.md) — Publishing safely to Kafka/RabbitMQ.
- [Distributed Transactions](../02-software-architecture/distributed-transactions.md) — Using brokers to coordinate Sagas.
