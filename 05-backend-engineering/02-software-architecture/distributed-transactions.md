# Distributed Transactions

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Các mẫu kiến trúc nâng cao để duy trì tính nhất quán của dữ liệu trên nhiều microservice độc lập bằng cách sử dụng Saga Pattern, Two-Phase Commit (2PC) và Eventual Consistency (Nhất quán cuối).

</details>

> **Summary**: Advanced patterns for maintaining data consistency across multiple independent microservices using the Saga Pattern, Two-Phase Commit (2PC), and eventual consistency.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tưởng tượng bạn lên kế hoạch đi du lịch. Bạn cần làm 3 việc: Đặt vé máy bay, Đặt khách sạn, Thuê xe tự lái.
- **Cách cũ (Monolith)**: Bạn nhờ 1 đại lý du lịch (Database duy nhất). Nếu 1 trong 3 dịch vụ hết chỗ, đại lý sẽ lập tức hủy toàn bộ và báo: "Không đặt được". Mọi thứ cực kỳ an toàn (ACID Transaction).
- **Cách mới (Microservices)**: Mỗi dịch vụ là một công ty riêng biệt (Database riêng). Bạn tự đặt vé máy bay thành công. Chuyển sang đặt khách sạn thì khách sạn báo hết phòng. Lúc này vé máy bay đã đặt mất rồi!
- **Saga Pattern**: Giải quyết vấn đề bằng "Giao dịch bù trừ". Bạn phải gọi điện lại cho hãng hàng không và nói: "Tôi muốn hủy vé và chịu phí phạt". Saga là chuỗi các hành động tiến lên, nếu vấp ngã ở đâu thì phải có các hành động lùi lại (bù trừ) tương ứng để dọn dẹp.

</details>

Imagine planning a vacation. You need to do 3 things: Book a flight, Book a hotel, Rent a car.
- **The Old Way (Monolith)**: You use a single travel agent (Single Database). If any of the 3 services is fully booked, the agent instantly cancels everything and says, "Booking failed." Everything is extremely safe (ACID Transaction).
- **The New Way (Microservices)**: Each service is an independent company (Separate Databases). You successfully book the flight. Then you try to book the hotel, but they are fully booked. Now you are stuck with a flight you don't want!
- **Saga Pattern**: Solves this using "Compensating Transactions". You have to call the airline back and say, "I need to cancel my flight and pay the penalty." Saga is a chain of steps forward; if you stumble somewhere, you must trigger a chain of corresponding backward steps (compensations) to clean up.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Distributed Transactions (Giao dịch phân tán)** xử lý tính nhất quán dữ liệu trên các hệ thống mạng (Microservices) nơi không thể áp dụng các thuộc tính ACID tiêu chuẩn cho toàn cục.
- **Saga Pattern**: Một chuỗi các giao dịch cục bộ. Mỗi service cập nhật database của riêng nó và bắn ra một sự kiện (event) để kích hoạt bước tiếp theo. Nếu một bước thất bại, các giao dịch bù trừ (compensating transactions) sẽ được chạy để hoàn tác các bước trước đó.
- **Two-Phase Commit (2PC)**: Một giao thức chặt chẽ được điều phối bởi một quản lý trung tâm (Giai đoạn chuẩn bị -> Giai đoạn xác nhận). Rất chậm và dễ gây chết hệ thống.

**Phân loại:**
- **Loại**: Mẫu kiến trúc Microservices.
- **Triển khai**: Saga Choreography (Làm việc theo Sự kiện), Saga Orchestration (Làm việc theo Lệnh trung tâm), 2PC (Khóa phân tán).

</details>

**Distributed Transactions** handle data consistency across networked systems (Microservices) where standard ACID properties cannot be enforced globally.
- **Saga Pattern**: A sequence of local transactions. Each service updates its own database and publishes an event to trigger the next step. If a step fails, compensating transactions are executed to undo the previous steps.
- **Two-Phase Commit (2PC)**: A strict consistency protocol coordinated by a central manager. (Prepare phase -> Commit phase).

### Classification
- **Type**: Microservices Architecture Pattern.
- **Implementations**: Saga Choreography (Event-driven), Saga Orchestration (Command-driven), 2PC (Distributed locks).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong hệ thống thương mại điện tử Microservices:
1. `OrderService` tạo đơn hàng trong `DB_A`.
2. `InventoryService` trừ kho trong `DB_B`.
3. `PaymentService` trừ tiền người dùng trong `DB_C`.

Nếu `PaymentService` thất bại (tài khoản không đủ tiền), hệ thống BẮT BUỘC phải hoàn tác việc trừ kho trong `InventoryService` và hủy đơn hàng trong `OrderService`. Vì `DB_A`, `DB_B`, và `DB_C` không thể chia sẻ chung một Transaction của cơ sở dữ liệu, ta bắt buộc phải dùng các mẫu Giao dịch Phân tán.

</details>

In a microservices e-commerce system:
1. `OrderService` creates an order in `DB_A`.
2. `InventoryService` deducts stock in `DB_B`.
3. `PaymentService` charges the user in `DB_C`.

If `PaymentService` fails (insufficient funds), the system must rollback the stock deduction in `InventoryService` and cancel the order in `OrderService`. Since `DB_A`, `DB_B`, and `DB_C` cannot share a single database transaction, distributed transaction patterns are required.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu không dùng Saga (Dùng API gọi đồng bộ): Nếu gọi API sang dịch vụ Kho bị timeout (quá giờ), bạn không biết nó đã trừ kho hay chưa. Nếu lỗi, bạn phải tự viết code gọi lại API `khôi phục kho`. Code này rất rối và dễ sinh ra rác dữ liệu vĩnh viễn nếu mạng rớt.
Nếu dùng Saga: Hệ thống giao tiếp qua Kafka. Cứ xong 1 việc thì nhắn 1 tin. Nếu Payment trừ tiền xịt, nó ném lên Kafka 1 cái tin `PaymentFailed`. Kho và Order tự nghe tin đó và tự động chạy hàm bù trừ để khôi phục dữ liệu.

</details>

### Without Saga (The Microservices Nightmare)
```java
public void placeOrder(OrderRequest req) {
    orderRepository.save(new Order(req)); // Step 1: Commit DB_A
    
    // Step 2: Sync HTTP call to Inventory
    boolean hasStock = inventoryClient.deduct(req.getItemId()); 
    // What if this HTTP call times out? Did it deduct or not?
    
    // Step 3: Sync HTTP call to Payment
    boolean paid = paymentClient.charge(req.getUserId());
    // If paid == false, we must manually write code to call inventoryClient.restore()
    // What if inventoryClient.restore() fails? Data is permanently inconsistent.
}
```

### With Saga Pattern (Eventual Consistency)
```text
[Order Service] --(OrderCreatedEvent)--> [Kafka]
                                            |
[Kafka] --(Consume)--> [Inventory Service] (Deducts stock)
                                            |
[Inventory Service] --(StockDeductedEvent)--> [Kafka]
                                                |
[Kafka] --(Consume)--> [Payment Service] (Fails - Insufficient Funds)
                                                |
[Payment Service] --(PaymentFailedEvent)--> [Kafka]
                                                |
[Kafka] --(Consume)--> [Inventory Service] (Compensating action: Restores stock)
[Kafka] --(Consume)--> [Order Service]     (Compensating action: Cancels order)
```

| Aspect | 2PC (Two-Phase Commit) | Saga Pattern |
|---|---|---|
| Consistency | Strong (ACID) | Eventual (BASE) |
| Performance / Scalability | Poor (Locks resources across services) | Excellent (No global locks) |
| Failure handling | Blocks until coordinator recovers | Compensating actions (Rollbacks) |
| Best for | Monolithic databases, legacy systems | Microservices, High-throughput systems |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Saga Choreography (Vũ đạo - Sự kiện)**:
Các service tự ném sự kiện lên Message Broker (như Kafka) và tự nghe nhau. Không có trung tâm chỉ huy.
- **Thích hợp cho**: Quy trình đơn giản (2-4 service).
- **Điểm mạnh**: Rất rời rạc, không có điểm chết duy nhất (Single point of failure).
- **Điểm yếu**: Khó theo dõi toàn cảnh xem giao dịch đang kẹt ở đâu. Dễ bị dính lỗi lặp vòng tròn.

**2. Saga Orchestration (Nhạc trưởng - Ra lệnh)**:
Có một service trung tâm làm Nhạc trưởng. Nhạc trưởng sẽ chỉ đạo: "Kho ơi trừ đi", "Payment ơi trừ tiền đi".
- **Thích hợp cho**: Quy trình phức tạp (5+ service).
- **Điểm mạnh**: Dễ theo dõi, logic gom về 1 cục, không bị lặp vòng tròn.
- **Điểm yếu**: Nhạc trưởng chết là cả hệ thống đứng hình.

**Không nên làm**:
- **Dùng 2PC trong Microservices**: 2PC khóa database của mọi người lại. Nếu 1 service sập mạng, database của các service kia bị khóa vĩnh viễn, kéo sập toàn bộ công ty.
- **Dùng HTTP gọi đồng bộ (REST) cho Saga**: Cấm tuyệt đối. Hãy dùng Kafka hoặc RabbitMQ (Bảo đảm giao tin ít nhất 1 lần).

</details>

### Saga Choreography (Event-Driven)
Services publish events to a message broker. Other services listen and react. There is no central brain.
- **Best for**: Simple workflows (2-4 services).
- **Pros**: Highly decoupled, no single point of failure.
- **Cons**: Hard to track the overall status of the transaction. High risk of cyclical dependencies.

### Saga Orchestration
A central `OrderOrchestrator` service sends commands (via queue or async HTTP) to other services and waits for replies.
- **Best for**: Complex workflows (5+ services).
- **Pros**: Easy to monitor, clear central logic, prevents cyclic dependencies.
- **Cons**: The Orchestrator becomes a single point of failure and tightly couples the business logic.

### Anti-Patterns
- **Using 2PC in Microservices**: 2PC relies on blocking locks. If a service goes down during the commit phase, locks are held indefinitely, bringing the entire system down.
- **Synchronous HTTP for Sagas**: Never use `RestTemplate` or `FeignClient` to coordinate Sagas. If the network drops, the state is lost. Always use asynchronous message brokers (Kafka/RabbitMQ) ensuring "At-least-once" delivery.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất**:
1. **Idempotency là BẮT BUỘC**: Message broker luôn đảm bảo giao tin "ít nhất 1 lần", tức là nó có thể giao tin trùng lặp. Service kho có thể nhận lệnh trừ kho 2 lần cho 1 đơn. Bạn phải code sao cho nó chỉ trừ 1 lần (Dùng Idempotency-Key).
2. **Outbox Pattern**: Không bao giờ được gọi `Lưu Database` và `Gửi tin Kafka` chung với nhau. Nhỡ lưu thành công mà mạng tịt không gửi Kafka được thì sao? Bắt buộc phải dùng mẫu Transactional Outbox.
3. **Hiển thị trên UI**: Saga mất 2-3 giây để chạy. Frontend phải show cái màn hình "Đang xử lý..." (Spinner) và chờ WebSockets báo lại kết quả, chứ không nên bắt người dùng đợi HTTP phản hồi.

**Cạm bẫy**:
1. Hàm dọn dẹp (Compensating) thất bại: Ví dụ lệnh `Hủy đơn` lưu vào DB thất bại do đứt mạng. Đừng lo, Kafka sẽ gọi đi gọi lại hàm đó cho tới khi thành công. Chỉ cần đảm bảo logic nghiệp vụ không được phép từ chối lệnh hủy đơn.
2. Đọc rác (Dirty Reads): Người dùng khác có thể nhìn thấy món đồ đã bị trừ kho, rồi 2 giây sau lại thấy nó hiện về như cũ (Do Saga Rollback). Bạn phải chấp nhận điều này trong hệ thống Eventual Consistency.

</details>

### Best Practices
1. **Idempotency is Mandatory**: Because message brokers guarantee *at-least-once* delivery, a service might receive the `OrderCreatedEvent` twice. The local transaction must be idempotent to prevent deducting stock twice.
2. **The Outbox Pattern**: You cannot reliably update your local database AND publish an event to Kafka in one step. You must use the Transactional Outbox pattern to guarantee events are published if the local DB commits.
3. **Design for Commutativity**: Try to design operations so that the order of processing doesn't matter (e.g., adding a delta `+5` instead of setting an absolute value `qty = 10`).
4. **Visibility / Observability**: Because Sagas are async, the frontend will not immediately know if the order succeeded. Return a `202 Accepted` with a `transactionId`, and have the frontend poll or use WebSockets for updates.

### Common Pitfalls
1. **Compensating Action Failure**: What happens if the `restoreStock()` compensating transaction fails? 
   - *Fix*: Compensating transactions MUST NOT fail due to business logic (e.g., you can always add stock back). If they fail due to a DB outage, the message broker will infinitely retry until it succeeds.
2. **Read Isolation (Dirty Reads)**: While the Saga is running, a user might see an Order in "PENDING" state, and stock temporarily reduced, even if the Saga eventually rolls back. You must design the UI to handle these transient states.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đừng tự viết Orchestrator bằng tay, rất dễ lỗi. Trong thực tế (Production), các công ty lớn thường dùng công cụ xịn như **Temporal.io**, **Camunda** để làm Nhạc trưởng.
Đoạn code dưới đây chỉ mô phỏng tư duy của Nhạc trưởng: Lắng nghe sự kiện thất bại -> Sửa trạng thái nội bộ thành "Đang Hủy" -> Bắn lệnh yêu cầu các team khác dọn dẹp (Hủy kho, Hoàn tiền).

</details>

### Saga Orchestration with Spring State Machine or Temporal.io

Building an orchestrator manually is error-prone. In production, teams often use orchestration engines like **Temporal.io**, **Camunda**, or **Axon Framework**.

*Conceptual Orchestrator logic:*
```java
@Service
public class OrderOrchestrator {
    
    // Called when the Orchestrator receives a message from Kafka
    public void handlePaymentFailed(String orderId) {
        // Step 1: Update local state to CANCELLING
        updateOrderState(orderId, OrderState.CANCELLING);
        
        // Step 2: Send compensating commands to Kafka
        kafkaTemplate.send("inventory-commands", new RestoreStockCommand(orderId));
        
        // The orchestrator waits for the StockRestoredEvent to finally mark order as CANCELLED.
    }
}
```

---

## Related Topics

- [Transactional Outbox Pattern](../04-distributed-async/transactional-outbox-pattern.md) — The prerequisite for implementing Sagas safely.
- [Idempotency & Rate Limiting](../01-advanced-api-design/idempotency-and-rate-limiting.md) — Why idempotency is required for Saga consumers.
- [Kafka vs RabbitMQ](../04-distributed-async/kafka-vs-rabbitmq-at-scale.md) — The brokers used to route Saga events.
