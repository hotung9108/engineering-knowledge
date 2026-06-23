# Consistency Patterns (CAP, ACID vs BASE)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Để quản lý tính nhất quán (Consistency), kỹ sư phần mềm phải dựa vào 2 nền tảng lý thuyết tối cao: **Định lý CAP** và các mô hình Giao dịch (**ACID vs BASE**). Định lý CAP khẳng định rằng bạn KHÔNG THỂ có một hệ thống vừa Hoàn hảo, vừa Không bao giờ sập. Bạn luôn phải đánh đổi. Từ đó, sinh ra 2 trường phái thiết kế Database: Trường phái Cổ điển (ACID - Thà báo lỗi chứ không cho phép sai lệch) và Trường phái Đám mây (BASE - Chấp nhận sai lệch tạm thời để hệ thống luôn sống sót và mượt mà).

</details>

> **Summary**: Managing Consistency in distributed systems is not merely a coding challenge; it is constrained by fundamental mathematical laws. The **CAP Theorem** mathematically proves that absolute perfection is impossible in a distributed network; architects must explicitly trade Consistency for Availability when networks inevitably partition. This unavoidable tradeoff birthed two opposing persistence philosophies: **ACID** (Atomicity, Consistency, Isolation, Durability) which fiercely prioritizes rigid correctness, and **BASE** (Basically Available, Soft state, Eventual consistency) which prioritizes extreme Availability and hyperscaling, accepting transient data staleness as a necessary architectural tax.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn gọi điện cho Thư viện để mượn sách. Thư viện có 2 chi nhánh: Quận 1 và Quận 2.
1. **Định lý CAP (Phải chọn 2 trong 3)**: Đột nhiên đường dây điện thoại giữa Quận 1 và Quận 2 bị đứt (Partition). Một khách hàng gọi cho Quận 1 hỏi mượn cuốn Harry Potter.
   - *Cách 1 (Bảo vệ Tính nhất quán - ACID)*: Quận 1 báo: "Mạng bị đứt rồi, tôi không kiểm tra được Quận 2 có ai mượn chưa. Xin lỗi, để đảm bảo không bị mượn trùng, thư viện xin phép ĐÓNG CỬA nghỉ bán". (Hệ thống thà chết chứ không làm sai).
   - *Cách 2 (Bảo vệ Tính Sẵn sàng - BASE)*: Quận 1 báo: "Bên tôi ghi nhận sách còn, cứ cho mượn bừa đi, lỡ Quận 2 có cho mượn rồi thì tính sau (Xin lỗi khách)". Thư viện vẫn hoạt động mượt mà, nhưng chấp nhận rủi ro dữ liệu bị sai lệch.

</details>

Imagine a Bank with an ATM in New York and an ATM in London.
1. **The CAP Theorem**: The underwater internet cable breaks (Partition). A user in London tries to withdraw $100.
   - *Option 1 (ACID / Consistency focus)*: The London ATM says: "I cannot talk to New York to verify your balance. I must freeze your account and refuse the transaction." The system guarantees absolute math correctness but causes terrible downtime for the user.
   - *Option 2 (BASE / Availability focus)*: The London ATM says: "I can't talk to New York, but I'll assume you have the money and dispense $100 anyway just to keep you happy." The system guarantees 100% uptime, but creates a massive accounting headache (Inconsistency) if the user actually had $0 in New York.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Định lý CAP (Phát minh bởi Eric Brewer)**
Trong một hệ thống phân tán, bạn chỉ có thể chọn TỐI ĐA 2 trong 3 thuộc tính:
- **C (Consistency - Nhất quán)**: Mọi máy chủ đều trả về dữ liệu giống nhau.
- **A (Availability - Sẵn sàng)**: Hệ thống luôn luôn trả lời (Không bao giờ báo lỗi `500`).
- **P (Partition Tolerance - Chống chịu đứt mạng)**: Hệ thống vẫn chạy dù các máy chủ bị đứt kết nối với nhau.
*Sự thật phũ phàng*: Vì Internet LUÔN LUÔN đứt mạng (P là bắt buộc). Nên thực chất định lý CAP bắt bạn phải chọn: Khi đứt mạng, bạn chọn C (Đóng cửa) hay chọn A (Bán bừa)?

**2. ACID vs BASE (2 Trường phái Database)**
- **ACID (SQL)**: Đại diện cho phe C (Consistency). Nó khóa (Lock) dữ liệu cực kỳ chặt. Nó đảm bảo tiền không bao giờ bị nhân đôi. (Ví dụ: PostgreSQL, Oracle).
- **BASE (NoSQL)**: Đại diện cho phe A (Availability). Khái niệm cốt lõi của nó là **Eventual Consistency** (Nhất quán tạm thời). Nó không thèm khóa ai cả, cứ cho Ghi dữ liệu tẹt ga. Dữ liệu sẽ tự động đồng bộ ngầm sau vài giây. (Ví dụ: Cassandra, DynamoDB).

</details>

**1. The CAP Theorem (Brewer's Theorem)**
A mathematical proof stating that a distributed data store can only simultaneously provide two of the following three guarantees:
- **C (Consistency)**: Every read receives the most recent write or an error.
- **A (Availability)**: Every request receives a non-error response (but without the guarantee that it contains the most recent write).
- **P (Partition Tolerance)**: The system continues to operate despite an arbitrary number of messages being dropped by the network.
*The Physical Reality*: Because network partitions (P) are an unavoidable law of physics, CAP is effectively a tradeoff: **During a network failure, do you choose Consistency (Halt the system) or Availability (Serve stale data)?**

**2. ACID vs. BASE Paradigms**
- **ACID (Atomicity, Consistency, Isolation, Durability)**: The traditional Relational DB paradigm. It chooses **CP** (Consistency + Partition Tolerance). It rigorously locks records and enforces Foreign Keys to guarantee state perfection. If it cannot guarantee perfection, it aborts the transaction.
- **BASE (Basically Available, Soft state, Eventual consistency)**: The Cloud-Native NoSQL paradigm. It chooses **AP** (Availability + Partition Tolerance). It prioritizes blistering speed and horizontal scaling. It explicitly abandons Locks and Isolation, embracing "Eventual Consistency".

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao các gã khổng lồ như Amazon, Netflix lại đẻ ra cái BASE (Chấp nhận dữ liệu sai lệch)?
Bởi vì trong kinh doanh E-commerce, **Downtime (Sập web) đáng sợ hơn Dữ liệu sai**.
Nếu dùng ACID: Đứt mạng $\rightarrow$ Nút "Thêm vào giỏ hàng" bị khóa chặn $\rightarrow$ Khách hàng không mua được hàng $\rightarrow$ Amazon mất hàng tỷ đô mỗi phút.
Nếu dùng BASE: Đứt mạng $\rightarrow$ Nút "Thêm vào giỏ" vẫn bấm được mượt mà. Lỡ mà hệ thống vô tình bán lố 1 cuốn sách (Do 2 người mua cùng 1 lúc mà kho chỉ còn 1). Không sao cả! Amazon thà gọi điện xin lỗi 1 khách hàng và đền cho họ cái Voucher 10$, còn hơn là đóng cửa toàn bộ Website làm mất hàng triệu khách hàng khác. Đánh đổi (Trade-off) là bản chất của System Design.

</details>

Why did tech giants like Amazon abandon mathematically perfect ACID databases for conceptually "flawed" BASE systems?
Because in consumer-facing hyper-scale applications, **Availability translates directly to Revenue**.
If Amazon's Checkout Cart relies on a Strongly Consistent ACID database, and a network partition occurs between their East and West datacenters, the system must choose Consistency. It locks the Cart. Millions of users click "Add to Cart" and receive `HTTP 500 Error`. Amazon loses tens of millions of dollars in minutes.
By architecting DynamoDB as a BASE (AP) system, the Cart is *always* available. If a network partition occurs, users can still add items. Does this risk selling 2 copies of a book when only 1 exists in the warehouse? Yes. But Amazon calculated that apologizing to 1 customer and sending them a $10 gift card is infinitely cheaper than shutting down the entire global storefront.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc chọn ACID và BASE khi thiết kế Game Online.
</details>

Visualizing the Tradeoff (ACID vs BASE) in architectural decision-making.

| Feature | Paradigm | Behavior during Network Stress | Business Impact |
|---|---|---|---|
| **Player Gold / Inventory**| **ACID (CP)** | Trade fails. "Network Error, try again." | Safe. Prevents item duping/hacking. |
| **Global Chat Box** | **BASE (AP)** | Message sends instantly. Other players see it 2s later. | Excellent UX. Nobody cares if a chat message is 2s late. |
| **Matchmaking Queue** | **BASE (AP)** | Player joins queue instantly. | Fast matchmaking. |
| **Ranked Match Result** | **ACID (CP)** | System freezes until MMR is safely recorded in DB. | Fair competitive integrity. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Các hệ thống AP (Availability + Partition Tolerance)**: Hệ thống luôn sống, tốc độ siêu nhanh, nhưng dữ liệu có thể bị trễ. Phù hợp cho: Bình luận mạng xã hội (Facebook), Bộ đếm lượt xem (Youtube), Lưu trữ Giỏ hàng, Thu thập Log dữ liệu (Data Analytics). Các Database tiêu biểu: **Cassandra, DynamoDB, Couchbase**.
2. **Các hệ thống CP (Consistency + Partition Tolerance)**: Hệ thống chậm hơn, dễ báo lỗi, nhưng dữ liệu luôn luôn chính xác 100%. Phù hợp cho: Chuyển khoản ngân hàng, Giao dịch Tiền ảo, Thanh toán Hóa đơn, Quản lý Tồn kho chính xác. Các Database tiêu biểu: **PostgreSQL, MongoDB (Cấu hình Majority), etcd/Zookeeper**.
3. **Còn CA thì sao? (Consistency + Availability)**: Định lý CAP nói rõ: CA chỉ tồn tại khi KHÔNG CÓ ĐỨT MẠNG (Tức là KHÔNG PHẢI hệ thống phân tán). Nếu bạn cài 1 con MySQL duy nhất chạy trên 1 cái máy tính cùi bắp, đó chính là hệ thống CA.

</details>

1. **AP Systems (Availability First)**: Optimizes for 100% uptime and hyper-low latency. Stale reads are an acceptable business risk. Used universally in: Social Media Feeds (Instagram/X), Shopping Cart Persistence, IoT Telemetry ingestion, and View Counters. Representative Technologies: **Apache Cassandra, Amazon DynamoDB, Riak**.
2. **CP Systems (Consistency First)**: Optimizes for absolute data integrity. If Quorum cannot be achieved, the system violently rejects Writes. Used universally in: Financial ledgers, Cryptographic ledgers, Centralized Identity/Auth Systems, and Cluster Configuration. Representative Technologies: **PostgreSQL (Synchronous Rep), etcd, Apache ZooKeeper, MongoDB (with `writeConcern: majority`)**.
3. **The CA Illusion**: A system that provides Strong Consistency and 100% Availability. According to the CAP theorem, this is *only* mathematically possible if `P = 0` (Network Partitions never happen). This physically only exists in a non-distributed, single-node monolithic Database (A single Oracle instance sitting in a closet).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Polyglot Persistence (Mix cả 2)**: Đừng bao giờ chọn 1 phe cho toàn bộ công ty. Một kiến trúc giỏi là phải biết dùng cả hai. Trữ Tiền (Ví điện tử) thì bắt buộc xài PostgreSQL (ACID). Nhưng chức năng Lịch sử giao dịch (Chỉ để cho khách hàng xem) thì đẩy nó sang Elasticsearch hoặc Cassandra (BASE) để search cho nhanh.
2. **Thiết kế Idempotency để bù đắp cho BASE**: Nếu bạn xài Eventual Consistency, thỉnh thoảng hệ thống sẽ bị lỗi do "2 người dùng cập nhật cùng 1 lúc" (Conflict). Bạn phải thiết kế code có khả năng tự sửa sai (Conflict Resolution) như `Last-Write-Wins` (Thằng nào ghi cuối thì thắng) hoặc lưu các ID chống trùng lặp.

</details>

1. **Polyglot Persistence (Architectural Pragmatism)**: The hallmark of a Senior Architect is refusing to apply a single Database paradigm to the entire system. You physically segment the Bounded Contexts. The `BillingContext` absolutely demands an ACID PostgreSQL instance. The `ProductCatalogContext` absolutely demands an AP Elasticsearch/MongoDB instance. You orchestrate synchronization between them via an Event Bus (Kafka).
2. **Conflict Resolution Engineering (CRDTs)**: When you embrace BASE/AP systems, Network Partitions *will* cause Divergent States (Node A saves "Red", Node B saves "Blue"). You must explicitly engineer Conflict Resolution into your application code. Common strategies include `Last-Write-Wins` (using timestamps, though dangerous due to clock drift), Application-Level Resolution (e.g., merging Shopping Carts), or utilizing mathematically advanced Conflict-free Replicated Data Types (CRDTs) native to DBs like Riak.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng NoSQL để làm Giao dịch Tài chính**: Rất nhiều công ty Startup nghe đồn MongoDB/Cassandra "Scale xịn lắm" nên bê vào làm Core Database cho App Giao hàng. Lúc làm chức năng "Trừ tiền Ví tài xế", vì NoSQL mặc định không có lệnh Khóa Transaction mạnh như SQL, dẫn đến việc tài xế bị trừ tiền âm, tiền bị nhân đôi khi spam click.
   - *Luật*: Chạm đến Tiền là chạm đến ACID. Phải dùng SQL hoặc các Database NewSQL (CockroachDB) chuyên dụng.
2. **Hiểu lầm Định lý CAP**: Định lý CAP không phải là trò chơi "chọn 1 cái DB lúc bắt đầu dự án rồi vứt xó". Cassandra mặc định là AP, nhưng bạn hoàn toàn có thể chỉnh thông số `Consistency_Level = ALL` trong code để ép Cassandra trở thành CP (Chạy chậm rề). Ngược lại, MongoDB mặc định là CP, nhưng bạn có thể cấu hình `ReadPreference = Secondary` để biến nó thành AP.

</details>

1. **Financial Ledgers on Naïve NoSQL**: Junior teams enamored with the "Web Scale" hype of NoSQL databases (Cassandra/MongoDB) deploy them as the primary datastore for an E-Wallet application. Because AP systems fundamentally lack Cross-Document ACID Isolation and Row-Level Locks, concurrent race conditions quickly manifest. Drivers tap "Withdraw" twice rapidly, the AP system processes both, and the Wallet balance goes deeply negative. **Absolute Rule**: Core financial mutations strictly belong in ACID SQL environments or highly specialized Distributed SQL ledgers (e.g., CockroachDB).
2. **Static CAP Labeling (The Configuration Myth)**: A massive misconception is treating Databases as static CAP entities (e.g., "Cassandra is strictly AP"). Modern distributed databases are highly tunable *per-query*. You can execute a query in Cassandra with `ConsistencyLevel.ALL`, forcing it to behave as a rigid, slow **CP** system. You can configure MongoDB to `readPreference=secondary`, forcing it to behave as a fast, stale **AP** system. The CAP tradeoff is a dial, not a hardcoded switch.

---

## Related Topics

- For a deep dive into the Database that forces CP, see **[SQL / ACID](../../03-technologies/databases/sql.md)** (Databases).
- For a deep dive into the Database that forces AP, see **[NoSQL / BASE](../../03-technologies/databases/nosql.md)** (Databases).
- For how logic handles failures in these states, review **[Saga Pattern](../event-driven/saga.md)**.
