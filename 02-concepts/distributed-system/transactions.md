# Distributed Transactions

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Chuyển 100k từ tài khoản A sang tài khoản B. Rất dễ nếu cả A và B nằm chung trên 1 cục Database (Dùng Transaction của SQL là xong). Nhưng nếu làm Microservices: Tiền của A nằm ở Server Ngân Hàng, còn ví của B nằm ở Server Shopee. Làm sao để trừ tiền ở Ngân Hàng xong thì CHẮC CHẮN Shopee phải cộng tiền? Lỡ Ngân hàng trừ xong, mạng đứt, Shopee không cộng tiền thì sao? **Distributed Transactions (Giao dịch Phân tán)** là các kỹ thuật (Như 2PC, Saga) để đảm bảo tính toàn vẹn dữ liệu xuyên qua nhiều Database khác nhau.

</details>

> **Summary**: Executing an ACID transaction within a single relational database (e.g., PostgreSQL) is a solved problem. The engine guarantees Atomicity (All or Nothing). However, in a Microservices architecture, business logic spans multiple, physically isolated Databases. Deducting funds in the `Billing_DB` and subsequently shipping an item in the `Inventory_DB` constitutes a **Distributed Transaction**. If the network partitions between these two operations, the system is left in a corrupted, partially-committed state (e.g., Money taken, but no item shipped). Distributed Transactions are complex orchestrations (like Two-Phase Commit or the Saga Pattern) engineered to artificially enforce ACID-like guarantees across disparate network nodes.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn rủ 3 người bạn đi ăn nhà hàng, với quy tắc: "Phải 4 đứa cùng đi thì mới ăn, thiếu 1 đứa thì hủy kèo".
1. **Giao dịch đơn (Single DB)**: 4 đứa sống chung một nhà. Bạn đứng giữa nhà hét lên: "Đi ăn không?". 3 đứa kia cùng gật đầu. Thế là xách xe đi luôn. Rất dễ kiểm soát.
2. **Giao dịch Phân tán (Distributed DB)**: 4 đứa ở 4 thành phố khác nhau. Bạn gọi điện cho Tèo: "Đi ăn không?". Tèo nói: "Có". Bạn gọi cho Tý, Tý nói: "Có". Bạn gọi cho Mùi, Mùi tắt máy đi ngủ. Thế là vỡ kèo. Nhưng khổ nỗi, Tèo và Tý đã lỡ bắt xe taxi ra quán ngồi chờ rồi. Bọn họ bị kẹt (Lock) ở quán. Bạn lại phải cuống cuồng gọi lại cho Tèo và Tý: "Thôi về đi, Mùi không đi đâu". (Rất rườm rà, tốn thời gian, lỡ gọi lại mà Tèo khóa máy thì Tèo ngồi chờ ngoài quán đến sáng).

</details>

Imagine organizing a Heist with 3 independent teams in 3 different cities. The rule is: "All 3 banks must be robbed simultaneously. If one team fails, the other teams must abort and put the money back."
1. **Single Transaction**: Everyone is in the same room. You yell: "Go!". Everyone goes. If the door is locked, everyone stops immediately. Easy.
2. **Distributed Transaction**: Team A is in New York, Team B in London, Team C in Tokyo. You call A: "Ready?". A says "Yes". You call B: "Ready?". B says "Yes". You call C: "Ready?". C doesn't answer (Network Failure). The heist is ruined. But A and B are already inside the vaults holding the money. You now have to frantically call A and B back and yell: "ABORT! PUT THE MONEY BACK!". If the phone lines drop before you can tell them to abort, A and B are left standing in the vaults forever. This is the nightmare of Distributed Transactions.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 2 cách chính để giải quyết Giao dịch Phân tán:
1. **Two-Phase Commit (2PC - Cam kết 2 giai đoạn)**: Bầu ra một người làm "Trọng tài" (Coordinator). 
   - *Giai đoạn 1 (Chuẩn bị)*: Trọng tài hỏi tất cả DB: "Tụi mày khóa dữ liệu lại chuẩn bị Update nhé, được không?". Nếu tất cả nói "OK", chuyển sang Giai đoạn 2.
   - *Giai đoạn 2 (Thực thi)*: Trọng tài hô "Commit đi!". Tất cả đồng loạt Update. (Rất an toàn, nhưng khóa dữ liệu cực lâu, làm hệ thống siêu chậm).
2. **Saga Pattern (Chuỗi bù đắp)**: Khuyên dùng cho Microservices. Bỏ qua Trọng tài. Cứ cho Service 1 update xong đi, rồi ném tin nhắn báo cho Service 2 làm tiếp. Nếu Service 2 bị lỗi, nó sẽ bắn tin nhắn ngược lại cho Service 1: "Lỗi rồi, mày chạy code Hoàn Tiền (Compensating Transaction) đi!". (Tốc độ cực nhanh, nhưng code rất mệt).

</details>

There are two primary architectural patterns to solve Distributed Transactions:
1. **Two-Phase Commit (2PC) / JTA**: A synchronous, strictly ACID protocol governed by a central **Coordinator**.
   - *Phase 1 (Prepare)*: Coordinator asks all participating DBs: "Can you commit this? Lock the rows." Every DB votes Yes/No.
   - *Phase 2 (Commit/Rollback)*: If *all* vote Yes, Coordinator sends the `COMMIT` signal. If *any* vote No, Coordinator sends the `ROLLBACK` signal. (Provides perfect consistency but causes severe locking and catastrophic blocking if the Coordinator crashes).
2. **The Saga Pattern**: An asynchronous, Event-Driven approach heavily utilized in Microservices. It abandons absolute ACID for **Eventual Consistency**. A massive transaction is broken into a sequence of local transactions. `Service A` commits locally $\rightarrow$ publishes an event $\rightarrow$ `Service B` commits locally. If `Service B` fails, it publishes a Failure Event. `Service A` catches this and executes a **Compensating Transaction** (e.g., executing a Refund logic) to explicitly undo its previous work.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vì Microservices ép chúng ta phải dùng nguyên tắc **Database-per-Service (Mỗi Service một DB riêng)**. 
Nếu bạn để Service Đặt hàng và Service Kho bãi dùng chung 1 cái Database khổng lồ, bạn không cần quan tâm đến bài toán này. Nhưng như thế thì mất đi ý nghĩa của Microservices (Nếu DB sập thì cả 2 Service đều tèo).
Khi bạn đã tách 2 DB riêng biệt trên 2 Server khác nhau, thì lệnh `BEGIN; UPDATE; COMMIT;` của SQL chỉ có tác dụng trong cái Server đó thôi. Nó không có "phép thuật" gì vươn tay qua mạng LAN sang Server kia để Commit hộ được. Buộc lòng chúng ta phải đẻ ra 2PC hoặc Saga để giải quyết.

</details>

Distributed Transactions exist purely as the architectural consequence of the **Database-per-Service** Microservice pattern.
If an architect builds a Monolith, the `OrderModule` and `InventoryModule` interact with the exact same physical PostgreSQL database. Standard SQL `BEGIN ... COMMIT` absolutely guarantees Atomicity.
However, Microservices mandate data sovereignty. The `OrderService` owns a MySQL DB. The `InventoryService` owns a MongoDB cluster. A MySQL transaction manager has zero authority over a MongoDB cluster over a TCP/IP network. The fundamental guarantee of "All or Nothing" is physically shattered. We are forced to implement high-level, code-driven orchestration (Sagas) to artificially reconstruct that "All or Nothing" guarantee across disparate network boundaries.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cách xử lý khi Service Thanh toán hoạt động, nhưng Service Kho bãi BỊ LỖI (Hết hàng).
</details>

Visualizing a failure scenario: Payment succeeds, but Inventory deduct fails (Out of Stock).

| Metric | 2PC (Two-Phase Commit) | Saga Pattern (Choreography) |
|---|---|---|
| **Mechanism** | Central Coordinator locks both DBs first. | Message Broker routes events asynchronously. |
| **Failure Handling**| Coordinator sees Inventory vote "NO". Sends Rollback to Payment immediately. | Inventory fails. Fires `OrderFailed` event. Payment catches it and runs `Refund()` code. |
| **Data Consistency**| **Strong Consistency**. Data is never seen in a half-state. | **Eventual Consistency**. User sees money deducted for 3 seconds, then refunded. |
| **Performance** | **Extremely Slow**. DB locks cause massive bottlenecks. | **Lightning Fast**. No global locks. |
| **Code Complexity** | Low (Handled by DB drivers). | High (Must write explicit `Undo/Refund` code). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Two-Phase Commit (2PC)**: Chỉ dùng trong Ngân hàng Cốt lõi (Core Banking) nội bộ, nơi các máy chủ đặt cạnh nhau qua cáp mạng siêu tốc, và tính năng "Khóa dữ liệu" không bị cản trở bởi mạng chậm. Rất ít công ty Web hiện đại dùng 2PC.
2. **Saga Pattern**: Đây là "Tiêu chuẩn vàng" của Thương mại Điện tử và Ứng dụng Web. 
   - Đặt vé máy bay (Agoda, Traveloka). Bạn bấm đặt vé. Agoda trừ tiền bạn ngay (Service 1). Sau đó nó gửi thông báo sang hãng máy bay VietJet (Service 2). Nếu VietJet báo "Hết vé", Agoda sẽ chạy luồng bù đắp (Saga Compensation) để tự động hoàn tiền lại vào thẻ cho bạn kèm lời xin lỗi. Hệ thống rất trơn tru mà không hề bị nghẽn (Lock).

</details>

1. **Two-Phase Commit (2PC)**: Heavily restricted to legacy Enterprise architectures (e.g., internal Java EE/JTA environments interacting with Oracle databases over highly reliable, low-latency LANs). Modern cloud-native architectures actively avoid 2PC due to its catastrophic blocking nature and extreme vulnerability to Coordinator failure.
2. **The Saga Pattern**: The absolute Gold Standard for Cloud-Native Microservices.
   - **Travel Booking Pipelines**: Booking a vacation involves Flights, Hotels, and Car Rentals. These are 3 different external systems. 2PC is impossible. Saga is mandatory. The system books the Flight. Then the Hotel. The Car Rental fails. The Saga Coordinator executes Compensating Transactions: It sends a `Cancel` API call to the Hotel, then a `Cancel` API call to the Airline, returning the system to a clean state. The user experiences a 5-second "Processing..." spinner, ultimately receiving a "Failed" message.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Tránh Giao dịch phân tán bằng mọi giá**: Cách tốt nhất để thiết kế Distributed Transaction là... đừng dùng nó. Nếu 2 Bảng (Tables) luôn luôn phải update cùng nhau, hãy gộp 2 cái Microservices đó lại thành 1 Service. Sự ám ảnh với Microservices thuần túy dẫn đến những kiến trúc phức tạp quá đáng.
2. **Luôn Code hàm Bù đắp (Compensating)**: Trong Saga, phần khó nhất không phải là đi thẳng, mà là đi lùi. Nếu Service A là "Trừ 500k", thì bạn BẮT BUỘC phải code trước hàm `Refund()` để cộng lại 500k phòng khi Service B bị lỗi. Điều kiện kiên quyết là hàm `Refund()` phải có tính **Idempotent** (Được gọi bao nhiêu lần cũng chỉ trả 500k 1 lần duy nhất).

</details>

1. **The Ultimate Best Practice: Avoid Them**: The most elegant way to solve Distributed Transactions is to radically alter your domain boundaries to avoid them entirely. If `Entity A` and `Entity B` strictly demand atomic, synchronous co-updates 100% of the time, they belong in the exact same Microservice sharing the exact same Database. Refactor your Bounded Contexts. Do not implement complex Sagas just to justify a poorly designed Microservice split.
2. **Idempotent Compensating Transactions**: The hardest part of the Saga pattern is the rollback logic. If Step 3 fails, Step 2 and Step 1 must be unwound. You must explicitly author "Compensating Logic" (e.g., if Step 1 was `ChargeCreditCard`, the compensation is `ExecuteRefund`). Crucially, because network retries occur, the Compensating Logic MUST be perfectly **Idempotent**. If the Saga engine accidentally calls `ExecuteRefund` three times due to a network stutter, the user must only be refunded exactly once.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lỗi "Báo cáo Sai sự thật" (Phantom Reads trong Saga)**: Vì Saga không khóa Database. Giả sử người dùng có 1 triệu. Giao dịch 1 trừ đi 500k $\rightarrow$ Còn 500k. Nó đang chờ giao dịch 2 xử lý. Lúc này, người dùng mở app lên xem số dư, thấy còn 500k thật (Hệ thống đã lộ dữ liệu trung gian). 5 giây sau giao dịch 2 bị lỗi, Saga hoàn tiền 500k lại thành 1 triệu. Người dùng sẽ cực kỳ hoang mang: "Rõ ràng nãy tao thấy mất 500k sao giờ tiền lại quay lại?". (Saga vi phạm tính Cách ly Isolation của ACID).
   - *Cách giải quyết*: Trong DB, thêm 1 cột trạng thái: `SoDu_DangXuLy: 500k`. Trên giao diện, không hiện "Số dư: 500k", mà hiện "Số dư: 1 triệu (500k đang bị phong tỏa chờ xử lý)". Rõ ràng, dễ hiểu.

</details>

1. **Lack of Isolation (The Saga Anomaly)**: The Achilles heel of the Saga pattern is that it completely surrenders the `I` (Isolation) in ACID. Sagas do not lock records. While a 5-step Saga is executing Step 3, the database explicitly persists the intermediate states of Steps 1 and 2. A concurrent user executing a `SELECT` query will see this partial, half-finished data (A Dirty Read). If the Saga later fails and rolls back, the user made decisions based on data that "never actually happened".
   - *The Fix (Semantic Locks)*: Sagas require application-level semantic locking. Do not just blindly `UPDATE balance = balance - 50`. Add a `pending_balance` column, or mark the Order `status = PENDING_VERIFICATION`. Concurrent readers will query the `status` flag and understand that the data is highly volatile and untrustworthy until it transitions to `CONFIRMED`.

---

## Related Topics

- For how to communicate between these Microservices reliably, see **[Messaging / Patterns](../messaging/patterns.md)**.
- For the architectural style that forces us into this mess, see **[Microservices vs Monolith](../../10-system-design/architecture-patterns/microservices.md)** (System Design).
- For understanding eventual consistency, read **[Consistency / Overview](../consistency/overview.md)**.
