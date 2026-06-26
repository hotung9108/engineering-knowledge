# Transactional Outbox Pattern

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Một mẫu thiết kế hệ thống phân tán đảm bảo rằng việc cập nhật cơ sở dữ liệu cục bộ và việc gửi tin nhắn (lên Kafka/RabbitMQ) xảy ra một cách nguyên tử (hoặc thành công cả hai, hoặc thất bại cả hai), mà không cần dựa vào giao thức Two-Phase Commit (2PC) vốn thiếu ổn định.

</details>

> **Summary**: A distributed systems pattern to guarantee that local database updates and message publishing (to Kafka/RabbitMQ) happen atomically, without relying on unreliable Two-Phase Commits (2PC).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tưởng tượng bạn vừa viết xong một bức thư quan trọng (Lưu Database) và bạn nhờ con chó cưng chạy đi gửi bức thư đó cho bưu điện (Gửi Kafka).
- **Vấn đề**: Bạn viết thư xong, đưa cho con chó, nhưng con chó chạy ra cửa thì bị xe tông hoặc nó làm rơi thư dọc đường. Thư bị mất vĩnh viễn!
- **Giải pháp (Outbox Pattern)**: Thay vì nhờ con chó, bạn xây một cái "Hộp Thư Đi" (Outbox Table) ngay trước cửa nhà. Bạn viết thư xong thì bỏ luôn vào cái Hộp Thư Đi đó rồi khóa cửa lại (Database Transaction). Sau đó, ông đưa thư (Một tiến trình ngầm) sẽ đi ngang qua, mở hộp thư, lấy thư đi gửi bưu điện. Nếu ông đưa thư vấp ngã giữa đường, ông ấy sẽ quay lại lấy lá thư (vì nó vẫn nằm trong hộp thư của bạn) và đi gửi lại. Đảm bảo 100% thư sẽ tới nơi!

</details>

Imagine you just wrote an important letter (Save to Database) and you ask your pet dog to run and deliver it to the post office (Send to Kafka).
- **The Problem**: You finish writing the letter, hand it to the dog, but the dog runs out the door and gets distracted or drops the letter on the way. The letter is permanently lost!
- **The Solution (Outbox Pattern)**: Instead of trusting the dog, you build an "Outbox" right at your front door. When you finish writing the letter, you put it in the Outbox and lock the door (Database Transaction). Later, a postman (a background process) comes by, opens the Outbox, and takes the letter to the post office. If the postman trips and loses it, they can just come back, get the letter again (because it's still in your Outbox), and retry. 100% guaranteed delivery!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Transactional Outbox Pattern** đảm bảo việc giao tin nhắn đáng tin cậy trong các kiến trúc hướng sự kiện (Event-Driven). Thay vì gửi trực tiếp tin nhắn cho Broker, ứng dụng ghi tin nhắn vào một bảng "outbox" trong chính Database cục bộ của nó, và việc ghi này nằm chung trong 1 Transaction với việc cập nhật nghiệp vụ chính. Một tiến trình riêng biệt sẽ đọc bảng outbox này và chuyển tiếp tin nhắn đến Broker.

**Phân loại:**
- **Loại**: Mẫu Kiến trúc Hướng sự kiện / Microservices.
- **Phụ thuộc vào**: Local ACID Database Transactions (Giao dịch cục bộ).
- **Triển khai**: Polling Publisher (Truy vấn định kỳ), Change Data Capture (CDC) qua Debezium.

</details>

The **Transactional Outbox Pattern** ensures reliable message delivery in event-driven architectures. Instead of directly sending a message to a broker, the application writes the message to an "outbox" table in its local database as part of the same transaction that updates the business entities. A separate process reads this outbox table and forwards the messages to the broker.

### Classification
- **Type**: Microservices / Event-Driven Architecture Pattern.
- **Relies on**: Local ACID Database Transactions.
- **Implementations**: Polling Publisher, Change Data Capture (CDC) via Debezium.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn không thể gom việc `INSERT` database và lệnh `send()` của Kafka vào chung một giao dịch (transaction) được. Chúng là 2 hệ thống hoàn toàn khác nhau.

**Vấn đề Ghi kép (Dual Write Problem)**:
Nếu bạn lưu đơn hàng vào DB thành công, nhưng đúng lúc đó mạng rớt, lệnh gửi Kafka bị thất bại. Đơn hàng đã nằm trong DB nhưng các hệ thống khác (Kho hàng, Vận chuyển) không bao giờ nhận được thông báo về đơn hàng đó.

Outbox pattern ra đời để đảm bảo **Tính nguyên tử (Atomicity)** giữa việc thay đổi dữ liệu cục bộ và việc phát ra sự kiện. 

</details>

You cannot wrap a database `INSERT` and a Kafka `send()` in a single transaction. They are two different systems. 

**The Dual Write Problem**:
```java
@Transactional
public void createOrder(Order req) {
    orderRepository.save(req); // Step 1: Commits to DB
    
    // Step 2: What if the application crashes RIGHT HERE? 
    // Or what if Kafka is down? The event is permanently lost.
    kafkaTemplate.send("orders", new OrderEvent(req));
}
```

If the event is lost, downstream services (like Inventory or Billing) will never process the order. The Outbox pattern ensures **Atomicity** between the local state change and the event emission.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có Outbox: Gọi hàm lưu DB, rồi gọi hàm gửi RabbitMQ. Nhìn thì ngắn gọn nhưng cực kỳ rủi ro mất dữ liệu nếu máy chủ chết giữa chừng.
Có Outbox: Gọi hàm lưu DB, tạo một Event và LƯU EVENT ĐÓ VÀO DB luôn (chung một transaction). Bất tử! Cho dù Kafka có bảo trì 2 ngày thì event của bạn vẫn nằm an toàn trong DB chờ được gửi đi.

</details>

### Without Outbox (Dual Write Anti-Pattern)
```java
// Risk of data inconsistency if the network drops between save() and send()
public void processPayment(Payment payment) {
    paymentRepo.save(payment); 
    rabbitTemplate.convertAndSend("payment-exchange", "success", payment);
}
```

### With Outbox (Atomic Write)
```java
@Transactional
public void processPayment(Payment payment) {
    // 1. Save business entity
    paymentRepo.save(payment); 
    
    // 2. Save event to Outbox table in the SAME transaction.
    // If step 2 fails, step 1 rolls back automatically.
    OutboxEvent event = new OutboxEvent("payment-exchange", payment.toJson());
    outboxRepo.save(event);
}

// 3. A separate async thread (or Debezium) reads the Outbox table and sends to RabbitMQ
```

| Aspect | Dual Write | Transactional Outbox |
|---|---|---|
| Consistency | High risk of data loss | Guaranteed (At-least-once delivery) |
| Performance | Fast (direct send) | Slower (requires DB write + background read) |
| Architecture | Simple | Complex (Requires background poller or CDC) |
| Reliability | Low (Fails if broker is down) | High (Broker outages do not block DB commits) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Saga Choreography**: Phát ra các sự kiện để kích hoạt bước tiếp theo của chuỗi Saga (ví dụ: `OrderCreated` gọi Inventory).
2. **Event Sourcing Lai**: Dùng DB quan hệ truyền thống nhưng vẫn muốn bắn toàn bộ sự thay đổi ra Kafka để đẩy vào Elasticsearch (Search Engine).
3. **Đồng bộ dữ liệu (Data Replication)**: Đồng bộ dữ liệu bất đồng bộ từ SQL Database (chuyên ghi) sang NoSQL Database (chuyên đọc).

**Các cách triển khai (Implementations):**
1. **Polling Publisher**: Viết 1 job `@Scheduled` chạy mỗi giây, query `SELECT * FROM outbox WHERE processed = false`, gửi lên Kafka rồi update lại `true`. (Dễ làm nhưng hại DB).
2. **Change Data Capture (CDC)**: Dùng Tool như Debezium theo dõi trực tiếp file nhật ký của DB (PostgreSQL WAL). Khi có dòng mới vào bảng `outbox`, nó tự động stream thẳng lên Kafka. (Siêu nhanh, không hại DB, nhưng setup phức tạp).

**Không nên làm**:
- **Bỏ quên Idempotency bên phía người nhận**: Outbox đảm bảo gửi *ít nhất 1 lần*. Lỡ Job của bạn gửi lên Kafka thành công rồi nhưng lúc update `processed = true` lại chết thì sao? Lần chạy sau nó sẽ gửi lại. Nên người nhận BẮT BUỘC phải tự kiểm tra chống trùng lặp.

</details>

1. **Saga Choreography**: Emitting the domain events required to trigger the next step of a Saga (e.g., `OrderCreated` triggers Inventory service).
2. **Event Sourcing Hybrid**: When you use a traditional relational DB but still want to publish state changes to an Event Bus for analytics or search indexing (Elasticsearch).
3. **Data Replication**: Replicating data from a high-write primary SQL database to a high-read NoSQL database asynchronously.

### Implementations

1. **Polling Publisher**: A `@Scheduled` cron job in Spring Boot queries `SELECT * FROM outbox WHERE processed = false`, sends to Kafka, and then marks `processed = true`.
   - *Pros*: Easy to implement.
   - *Cons*: Database polling overhead, higher latency.
2. **Change Data Capture (CDC)**: Tools like Debezium monitor the database transaction log (e.g., PostgreSQL WAL or MySQL binlog). When an INSERT happens in the `outbox` table, Debezium streams it directly to Kafka.
   - *Pros*: Extremely fast, zero polling overhead, highly scalable.
   - *Cons*: High infrastructure complexity.

### Anti-Patterns
- **Not using Idempotency on the Consumer**: The Outbox pattern guarantees *at-least-once* delivery. If the poller crashes after sending to Kafka but before marking the outbox row as "processed", it will send the message again. Consumers MUST be idempotent.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất**:
1. **Luôn ưu tiên CDC hơn Polling**: Với các hệ thống lớn, hãy dùng Debezium. Việc chạy lệnh query `SELECT` vào bảng khổng lồ mỗi 1 giây sẽ giết chết CPU của Database.
2. **Dữ liệu JSON**: Lưu nội dung event dưới dạng text JSON hoặc cột `JSONB`. Đừng bao giờ tạo cấu trúc bảng quan hệ phức tạp cho Event.
3. **Dọn rác (Clean up)**: Bảng Outbox sẽ phình to vô hạn. Hãy tạo thêm 1 job khác để `DELETE` các tin nhắn đã gửi thành công sau 7 ngày, hoặc chia Partition cho bảng theo ngày và drop nguyên bảng cũ đi.
4. **Thứ tự (Ordering)**: Nếu thứ tự tin nhắn quan trọng, phải đảm bảo bảng Outbox có ID tự tăng hoặc Timestamp chuẩn xác để Job có thể đọc theo đúng thứ tự (`ORDER BY id ASC`).

**Cạm bẫy**:
1. **Nghẽn cổ chai khi Polling**: Nếu bạn dùng `@Scheduled` Poller, điều gì xảy ra nếu bạn chạy 10 máy chủ Spring Boot? Cả 10 máy sẽ query cùng một dòng trong Database, lôi nó ra và ném lên Kafka 10 lần.
   - *Cách khắc phục*: Dùng Redisson Lock để chỉ 1 máy được chạy Poller. Hoặc dùng `SELECT ... FOR UPDATE SKIP LOCKED` (nếu dùng PostgreSQL) để nhiều máy có thể nhảy vào chia nhau lấy dữ liệu mà không đụng hàng.
2. **Transaction quá béo (Too Large)**: Nếu bạn nhét đủ thứ nghiệp vụ tính toán nặng nề vào chung 1 cục `@Transactional` kèm với lệnh lưu Outbox, kết nối tới DB sẽ bị giam giữ quá lâu. Hãy giữ transaction thật mỏng nhẹ.

</details>

### Best Practices
1. **CDC over Polling**: For high-throughput systems, always use Debezium (CDC) instead of polling. Polling a large table every 1 second will kill your database CPU.
2. **JSON Payloads**: Store the event payload as a JSON string or `JSONB` column in the Outbox table. Do not try to create a relational structure for events.
3. **Clean up**: The Outbox table will grow infinitely. Implement a separate job to `DELETE` processed messages that are older than 7 days, or partition the table by date and drop old partitions.
4. **Ordering**: If event order matters (e.g., `UserCreated` then `UserUpdated`), ensure your outbox table has an auto-incrementing ID or strict timestamp, and ensure your poller/CDC respects this order.

### Common Pitfalls
1. **Polling Bottlenecks**: If you use a `@Scheduled` poller, what happens if you have 10 instances of your microservice? All 10 will try to read and process the same Outbox rows, resulting in 10x duplicate messages.
   - *Fix*: Use a Distributed Lock (Redisson) so only 1 instance polls at a time, or use `SELECT ... FOR UPDATE SKIP LOCKED` in PostgreSQL to allow concurrent workers.
2. **Transaction Too Large**: If you do heavy processing, save the entity, and save the outbox event all in one massive `@Transactional` block, you hold the database connection open too long. Keep transactions short.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Kỹ thuật Outbox Poller cực kỳ xịn sò với PostgreSQL `SKIP LOCKED`. Lệnh này giúp Database nói rằng: "Dòng này máy số 1 đang khóa để đọc rồi, mày (máy số 2) nhảy sang đọc dòng tiếp theo đi". Nó giúp 10 máy chủ có thể cùng xúm vào giải quyết bảng Outbox mà không bao giờ bị đụng độ trùng lặp tin nhắn.

</details>

### Outbox Poller with PostgreSQL `SKIP LOCKED` (Spring Boot)

Using `SKIP LOCKED` allows multiple instances to poll the outbox table concurrently without blocking each other.

```java
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.QueryHints;
import jakarta.persistence.QueryHint;
import java.util.List;

public interface OutboxRepository extends JpaRepository<OutboxEvent, Long> {

    // SKIP LOCKED prevents concurrent instances from picking up the same rows
    @Query(value = """
        SELECT * FROM outbox 
        WHERE status = 'PENDING' 
        ORDER BY created_at ASC 
        LIMIT 100 
        FOR UPDATE SKIP LOCKED
    """, nativeQuery = true)
    List<OutboxEvent> findPendingEventsAndLock();
}

@Service
public class OutboxRelayService {

    private final OutboxRepository outboxRepository;
    private final KafkaTemplate<String, String> kafkaTemplate;

    @Scheduled(fixedDelayString = "1000") // Run every 1 second
    @Transactional
    public void processOutbox() {
        List<OutboxEvent> events = outboxRepository.findPendingEventsAndLock();
        
        for (OutboxEvent event : events) {
            // Send to Kafka
            kafkaTemplate.send(event.getTopic(), event.getPayload());
            
            // Mark as processed (will commit at end of transaction)
            event.setStatus("PROCESSED");
            outboxRepository.save(event);
        }
    }
}
```

---

## Related Topics

- [Distributed Transactions](../02-software-architecture/distributed-transactions.md) — How the Outbox pattern enables Saga Choreography.
- [Kafka vs RabbitMQ](./kafka-vs-rabbitmq-at-scale.md) — The target brokers for Outbox messages.
- [Idempotency](../01-advanced-api-design/idempotency-and-rate-limiting.md) — Required for consumers handling Outbox messages (At-least-once delivery).
