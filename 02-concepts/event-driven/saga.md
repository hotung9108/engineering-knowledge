# Saga Pattern

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi làm Microservices, nếu giao dịch Mua Hàng phải chạy qua 3 Service (Trừ tiền $\rightarrow$ Trừ kho $\rightarrow$ Giao hàng). Nếu bước 3 bị lỗi, bạn không thể dùng lệnh `ROLLBACK` của SQL để lấy lại tiền ở bước 1 được (Vì chúng khác Database). **Saga Pattern** là một chiến thuật để giải quyết việc này. Bạn phải tự code tay một Giao dịch Bù đắp (Compensating Transaction) cho TỪNG bước. Nếu bước 3 sập, hệ thống sẽ tự động gọi Hàm Bù Đắp của bước 2 (Cộng lại kho) và Hàm Bù Đắp của bước 1 (Hoàn lại tiền). Đây là cách duy nhất để duy trì tính toàn vẹn dữ liệu trong Microservices.

</details>

> **Summary**: In a monolithic relational database, an ACID transaction guarantees that if Step 3 of a process fails, the database engine automatically `ROLLBACK`s Steps 1 and 2, ensuring absolute Atomicity. In a Microservices architecture utilizing Database-per-Service, this magic engine does not exist. A **Saga Pattern** is an architectural sequence of local transactions where each microservice updates its own database and publishes an Event to trigger the next microservice. If a local transaction fails, the Saga executes a series of explicitly coded **Compensating Transactions** that undo the changes made by the preceding local transactions, mimicking an ACID rollback across distributed boundaries.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn tổ chức một chuyến đi Đà Lạt cho công ty. Có 3 bước phải làm tuần tự: (1) Mua vé xe, (2) Đặt phòng KS, (3) Mua vé chơi trò chơi.
- Bạn mua vé xe xong.
- Bạn đặt phòng KS xong.
- Đến lúc mua vé trò chơi thì Công viên báo ĐÓNG CỬA. 
Lúc này, bạn không thể bấm một cái nút "Hủy chuyến đi" thần kỳ nào để tiền tự động quay về túi bạn được.
Bạn phải **TỰ MÌNH** thực hiện các bước LÙI LẠI (Hàm bù đắp): Gọi điện cho KS xin hủy phòng lấy lại tiền $\rightarrow$ Gọi điện cho Nhà xe xin hủy vé lấy lại tiền.
Quá trình bạn tự đi hủy từng thứ một đó chính là **Saga Pattern**.

</details>

Imagine organizing a vacation that requires 3 distinct bookings: (1) Flight, (2) Hotel, (3) Rental Car.
- You book the Flight. Success.
- You book the Hotel. Success.
- You attempt to book the Rental Car. The agency is completely out of cars. Failure.
Because these are three separate companies, you cannot press a magical "Undo" button on your keyboard to get all your money back.
You must manually execute **Compensating Actions** in reverse order: You explicitly call the Hotel to cancel your room and get a refund. Then you explicitly call the Airline to cancel your flight and get a refund. This orchestrated sequence of explicit cancellations is the **Saga Pattern**.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 2 kiểu để vận hành một Saga:
1. **Choreography (Múa tập thể - Không có sếp)**: Các Service tự nói chuyện với nhau thông qua Sự kiện (Event). Đặt hàng xong $\rightarrow$ Bắn Event. Kho nhận Event $\rightarrow$ Trừ kho xong bắn Event tiếp. Nếu Kho bị lỗi $\rightarrow$ Bắn Event báo lỗi. Service Đặt hàng nhận Event lỗi $\rightarrow$ Tự gọi hàm Hoàn tiền. (Nhanh, không có nút thắt cổ chai, nhưng luồng chạy rối rắm khó theo dõi).
2. **Orchestration (Nhạc trưởng điều khiển)**: Đẻ ra một Service mới tên là "Sếp" (Orchestrator). Sếp sẽ ra lệnh: "Mày trừ tiền đi", "Mày trừ kho đi". Nếu kho lỗi, Sếp sẽ ra lệnh: "Thằng đầu tiên, hoàn tiền lại mau!". (Dễ quản lý code, luồng chạy rõ ràng, nhưng Sếp bị sập là cả hệ thống chết).

</details>

A Saga can be implemented using two fundamentally different coordination mechanisms:
1. **Choreography (Event-Driven)**: Decentralized coordination. There is no central controller. Each Microservice listens for Domain Events, executes its local transaction, and publishes a new Event. If a failure occurs, the failing service publishes a `FailedEvent`. The upstream services listen for this and autonomously trigger their own Compensating Transactions. (Highly decoupled, no single point of failure, but workflows are implicit and notoriously difficult to debug).
2. **Orchestration (Command-Driven)**: Centralized coordination. A dedicated `Saga Orchestrator` component (often implemented via AWS Step Functions, Temporal, or Camunda) strictly commands the participants. It sends a Command to Service A. A replies "Done". It sends a Command to Service B. B replies "Failed". The Orchestrator then explicitly sends a "Compensate" Command to Service A. (Highly visible, easy to trace, but introduces a single point of failure/bottleneck).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao không dùng Giao thức 2PC (Two-Phase Commit) cho dễ?
2PC bắt buộc TẤT CẢ các Database phải bị **Khóa (Locked)** trong suốt quá trình Giao dịch. Nếu bạn dùng 2PC cho chuỗi: Đặt hàng $\rightarrow$ Thanh toán qua Momo $\rightarrow$ Giao hàng. Quá trình người dùng lấy điện thoại ra quét QR Momo mất 30 giây. Suốt 30 giây đó, Bảng Khách hàng, Bảng Sản phẩm, Bảng Kho bãi bị khóa chặt ngắc. 10.000 khách hàng khác muốn mua hàng sẽ bị nghẽn (Block) và màn hình web quay mòng mòng.
Saga KHÔNG khóa bất cứ Database nào. Xử lý xong bước nào là Commit bước đó luôn (Giải phóng Database). Đổi lại, Saga chấp nhận sự hy sinh: Trạng thái trung gian sẽ bị lộ ra ngoài (Dù chưa thanh toán nhưng Cột Kho đã bị trừ).

</details>

Why endure the immense complexity of Sagas instead of simply using a distributed Two-Phase Commit (2PC)?
**Availability and Lock Contention**. 2PC enforces strict ACID isolation by aggressively Locking all participating databases simultaneously until the Coordinator issues the final Commit. If your E-commerce checkout requires an external API call to Stripe (which takes 3 seconds), 2PC will lock the `Users`, `Inventory`, and `Orders` tables for 3 entire seconds. In a highly concurrent system, this causes catastrophic deadlock and brings throughput to near zero.
Saga, conversely, **surrenders Isolation for extreme Availability**. It never holds global locks. It relies on local commits. The consequence is **Eventual Consistency**: other users might read the database and temporarily see "half-completed" states before the Saga fully finishes or rolls back.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh luồng Chạy và Lùi của Orchestration Saga.
</details>

Visualizing the Execution and Compensation flows of an Orchestrated Saga.

| Step | Forward Execution (Happy Path) | Backward Compensation (Failure Path) |
|---|---|---|
| **1. Orchestrator** | Sends `Create_Order` CMD to OrderDB. | Sends `Create_Order` CMD to OrderDB. |
| **2. Order Service** | Executes `INSERT`. Returns OK. | Executes `INSERT`. Returns OK. |
| **3. Orchestrator** | Sends `Charge_Card` CMD to PaymentDB. | Sends `Charge_Card` CMD to PaymentDB. |
| **4. Payment Service**| Executes `UPDATE`. Returns OK. | **Card Declined. Returns ERROR**. |
| **5. Orchestrator** | Sends `Ship_Item` CMD to Shipping. | Orchestrator halts forward progress. |
| **6. Compensation** | Saga Completes Successfully. | Orchestrator sends `Cancel_Order` CMD to OrderDB. |
| **7. Final State** | Item shipped, money taken. | Order explicitly marked `CANCELLED`. Money untouched. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giao dịch TMĐT (E-Commerce)**: Hầu hết các hệ thống Đặt hàng Shopee, Tiki đều dùng Saga. Nút thắt là ở khâu Thanh toán và Khấu trừ Kho.
2. **Du lịch & OTA (Online Travel Agency)**: Khi bạn book 1 Tour đi Nhật, hệ thống phải gọi qua API của Hãng hàng không, API của Khách sạn, API của Bảo hiểm. Mỗi cái API đều có thể tạch bất cứ lúc nào. Saga Orchestration (Với các công cụ như Temporal.io) là bắt buộc.
3. **Food Delivery (GrabFood)**: (1) Trừ tiền thẻ tín dụng khách, (2) Báo nhà hàng làm món, (3) Tìm tài xế. Tìm không ra tài xế $\rightarrow$ Phải hủy món ở nhà hàng $\rightarrow$ Hoàn tiền thẻ cho khách.

</details>

1. **E-Commerce Fulfillment**: The quintessential Saga. An `Order` triggers `Payment`, `Inventory Deduction`, and `Logistics Scheduling`. If Logistics cannot find a courier, the Saga elegantly compensates by returning stock to Inventory and issuing a Stripe Refund.
2. **Travel & OTA (Agoda/Expedia)**: Booking a multi-city itinerary involves interacting with highly unreliable third-party APIs (Airlines, Hotels). These external domains do not participate in your internal database locks. You must use a Saga to manage the asynchronous confirmations and execute structured cancellations if the Hotel booking succeeds but the Airline booking fails.
3. **On-Demand Logistics (UberEats/DoorDash)**: The workflow is strictly asynchronous and distributed: (1) Charge Customer, (2) Ping Restaurant to accept, (3) Find available Driver. If Step 3 times out after 10 minutes, the Saga must compensate by notifying the Restaurant to stop cooking and refunding the Customer.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Idempotency là Sống còn**: Bắt buộc. Trong quá trình chạy Saga, mạng chập chờn có thể khiến Orchestrator gửi lệnh `Refund_Tiền` tới 2 lần. Hàm Bù đắp của bạn PHẢI LUÔN LUÔN được code để "Hoàn tiền 1 lần duy nhất", dù bị gọi bao nhiêu lần đi nữa.
2. **Trạng thái Chờ (Semantic Lock)**: Vì Saga không khóa Database, người dùng khác có thể chọc vào xem dữ liệu khi giao dịch mới chạy được một nửa. Ví dụ, tạo Đơn hàng xong nhưng chưa Trừ tiền, ĐỪNG để status của Đơn hàng là `SUCCESS`. Hãy đặt nó là `PENDING_PAYMENT`. Cột status này chính là cái "Khóa bằng cơm" để báo cho các hệ thống khác biết: "Đơn này đang dở dang, cấm đụng vào".

</details>

1. **Mandatory Idempotency in Compensations**: The most critical engineering rule. Network failures will cause the Saga Orchestrator to retry sending the `Refund_Payment` command. If the Payment Service is not idempotent, it will execute the refund twice, draining the company's bank account. You must track an `Idempotency-Key` (e.g., the `Saga_ID`) in a database constraint to guarantee compensations execute exactly once.
2. **Semantic Locking (The State Machine)**: Sagas sacrifice ACID Isolation. If Step 1 creates an Order, a concurrent process might try to read or cancel that Order while Step 2 (Payment) is still processing. You must implement Application-Level Semantic Locks. An Order does not start in a `CREATED` state; it starts in a `PENDING_VALIDATION` state. All other APIs must be coded to reject actions on any Order that is currently in a `PENDING_*` state.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lỗi khi Hàm Bù Đắp cũng bị Lỗi**: Saga đang chạy lùi để Hoàn Tiền. Đột nhiên Service Hoàn Tiền bị sập hoặc Database Hoàn tiền bị đầy ổ cứng, nó văng Exception. Chuỗi Saga chết kẹt ở giữa không lùi được nữa. Hệ thống rơi vào trạng thái Dữ liệu Bị Thối (Inconsistent State). 
   - *Cách giải quyết*: Hàm Bù đắp (Compensation) PHẢI LÀ HÀM KHÔNG BAO GIỜ LỖI về mặt nghiệp vụ. Nếu lỗi do mạng/phần cứng, nó phải được đưa vào hàng đợi `Dead Letter Queue (DLQ)` và liên tục Retry (Thử lại) hoặc báo động rít lên cho Kỹ sư can thiệp bằng tay.
2. **Choreography Spaghetti**: Lúc hệ thống mới có 3 Service, code kiểu Choreography (Sự kiện bắn qua bắn lại) chạy rất ngon. 3 năm sau, hệ thống to lên 20 Service. Sự kiện bắn tứ tung như rễ cây. Lập trình viên mới vào công ty bật khóc vì không thể biết "Một đơn hàng được tạo ra thì nó sẽ kết thúc ở đâu". Hãy chuyển sang Orchestration sớm khi hệ thống bắt đầu phức tạp.

</details>

1. **Compensation Failure (The Saga Deadlock)**: The forward path failed, so the Saga attempts to execute the `Refund_Payment` compensation. But the `PaymentService` Database is completely offline. The compensation itself fails. The Saga is now permanently stuck in a corrupted intermediate state.
   - *The Fix*: Compensating transactions must be mathematically infallible from a business logic perspective (e.g., you can't fail a refund because of "Insufficient Funds"). For infrastructural failures (DB offline), the compensation Command MUST be persisted to a highly durable Retry Queue. It must retry infinitely with exponential backoff, or trigger a Critical PagerDuty alert for manual DBA intervention.
2. **Choreography Spaghetti**: Startups often choose Choreography because it requires no central infrastructure. As the architecture scales to 50 microservices, the event flow becomes a totally untraceable, cyclical web. Tracing a single order workflow requires grepping through 10 different code repositories. **Rule**: If a business workflow spans more than 3 distinct bounded contexts, abandon Choreography immediately and explicitly model it using an Orchestrator (State Machine).

---

## Related Topics

- For the underlying mechanism that triggers the steps, see **[Messaging Patterns](../messaging/patterns.md)**.
- For handling the errors when compensations fail, read **[Messaging Error Handling](../messaging/error-handling.md)**.
- For the fundamental theory of events driving this, review **[Event-Driven Overview](./overview.md)**.
