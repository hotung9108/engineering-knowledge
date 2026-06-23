# Command Query Responsibility Segregation (CQRS)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Chữ CQRS dài dòng thực chất chỉ có một nghĩa duy nhất: **Chia đôi luồng Đọc và Ghi**. Trong ứng dụng bình thường, bạn dùng chung 1 cái Database cho cả việc Ghi dữ liệu (Command) và Đọc dữ liệu (Query). CQRS bảo rằng: "Việc Đọc và việc Ghi có đặc thù hoàn toàn khác nhau. Sao không tách riêng nó ra làm 2 Database khác nhau luôn?". Một Database xịn chuyên để Ghi (Tốc độ cao, khóa an toàn). Một Database xịn chuyên để Đọc (Chứa dữ liệu nháp, search cực nhanh). Sự tách biệt này mở ra một chân trời mới về hiệu năng, nhưng đổi lại là cái giá phải trả cho sự đồng bộ dữ liệu.

</details>

> **Summary**: **Command Query Responsibility Segregation (CQRS)** is an architectural pattern that explicitly separates the data mutation operations (Commands/Writes) from the data retrieval operations (Queries/Reads) into distinct, independent execution pathways and, typically, completely separate data stores. In a traditional CRUD monolith, a single generic Data Model and a single relational Database handle both Reads and Writes, leading to severe locking contention and sub-optimal query performance. CQRS acknowledges that the Read workload and the Write workload possess fundamentally asymmetrical scaling requirements. By splitting them, architects can hyper-optimize the Write Database for high-throughput ACID compliance, while simultaneously hyper-optimizing the Read Database for sub-millisecond, denormalized querying.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một nhà hàng.
1. **Kiểu Truyền thống (CRUD)**: Chỉ có 1 Quyển Sổ Duy Nhất đặt ở quầy. Ông Thu ngân ghi món ăn vào sổ. Các ông Bếp trưởng, Bồi bàn, Khách hàng đều xúm lại tranh nhau mượn quyển sổ đó để Đọc xem có món gì. Lúc Thu ngân đang Ghi, thì 3 người kia phải đứng chờ (Bị Khóa/Block). Quán đông khách là vỡ trận.
2. **Kiểu CQRS (Chia Đọc/Ghi)**: Thu ngân có 1 quyển Sổ Bí Mật chỉ để GHI (Command DB). Thu ngân ghi món xong, lập tức hét lên cái Loa. Có 1 cậu nhân viên đứng nghe loa, lập tức chép cái món ăn đó lên cái BẢNG ĐEN khổng lồ dán ngoài tường (Read DB). Lúc này, hàng ngàn khách hàng có thể thoải mái ngước nhìn cái Bảng Đen (ĐỌC) mà không hề làm phiền ông Thu Ngân đang Ghi vào Sổ.

</details>

Imagine the operational flow of a Library.
1. **Traditional CRUD (Single Source)**: There is only one physical Master Ledger. The Librarian uses it to WRITE when someone borrows a book. However, all 50 patrons in the library must also line up and share that exact same ledger to READ and search for books. When the Librarian is writing, the patrons are blocked. When a patron is slowly searching, the Librarian is blocked. It is a massive bottleneck.
2. **CQRS**: The Librarian has a highly secure, private Ledger strictly for WRITING transactions (The Command Model). As soon as the Librarian writes a transaction, an assistant instantly updates a giant, public Digital Billboard (The Query Model) in the lobby. 5,000 patrons can stare at the Billboard simultaneously (READ) with zero latency, entirely decoupled from the Librarian's busy desk.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

CQRS chia ứng dụng làm 2 nửa riêng biệt (Thậm chí code khác nhau, DB khác nhau):
1. **Command (Lệnh - Đổi Trạng thái)**: Các hành động GHI (`Insert`, `Update`, `Delete`). Model này chứa các logic nghiệp vụ phức tạp (Validate dữ liệu, Kiểm tra số dư). Database thường là Relational DB (PostgreSQL/MySQL) hoặc Event Store để đảm bảo tính toàn vẹn (ACID).
2. **Query (Truy vấn - Đọc Trạng thái)**: Các hành động ĐỌC (`Select`). Model này KHÔNG chứa logic gì cả, chỉ việc lôi data ra trả về. Database thường là NoSQL, Caching, hoặc Search Engine (Elasticsearch) chứa dữ liệu đã được chế biến sẵn (Denormalized) cho từng cái màn hình UI, đọc cực nhanh.
3. **Synchronization (Sự đồng bộ)**: Khi Command cập nhật DB Ghi, nó phải bắn ra một Sự kiện (Event). Hệ thống Đọc sẽ hứng sự kiện đó và tự đi Update vào cái DB Đọc.

</details>

CQRS physically and logically bifurcates the application stack into two distinct hemispheres:
1. **The Command Side (Mutations)**: Responsible strictly for state-changing operations (`POST`, `PUT`, `DELETE`). The domain model here encapsulates rich, complex business logic, strict invariants, and validation rules. The backing storage is typically an ACID-compliant Relational Database or an append-only Event Store, engineered for flawless transaction integrity.
2. **The Query Side (Retrievals)**: Responsible strictly for data retrieval (`GET`). The domain model here is anemic; it contains absolutely zero business logic. It reads from a separate, heavily optimized Read Database (e.g., Elasticsearch, MongoDB, Redis). The data is pre-joined, materialized, and heavily **Denormalized** to perfectly match the JSON shape required by the Frontend UI, yielding nanosecond query times.
3. **The Synchronization Bridge (Event Bus)**: To keep the Query Database updated, the Command Side publishes Domain Events (e.g., `OrderCompleted`) to a Message Broker (Kafka) whenever state mutates. A background worker consumes this event and updates the Query Database accordingly.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Tối ưu hóa Sự mất cân đối (Asymmetrical Scaling)**: Trong đa số các ứng dụng (Đặc biệt là Web), tỷ lệ Đọc/Ghi là 100/1. Có 100 người lướt xem Shopee thì mới có 1 người bấm nút Đặt Hàng. Nếu dùng chung 1 cái Database, vì 1 thằng Đặt hàng mà 100 thằng Xem bị chậm đi. Với CQRS, bạn có thể cấp cho DB Đọc 10 con Server để gánh 100k lượt xem, trong khi DB Ghi chỉ cần 1 con Server là đủ. Tối ưu chi phí cực đỉnh.
**2. Giải quyết Sự phức tạp của DB**: Ghi dữ liệu thì chuộng cấu trúc DB Chuẩn hóa (Normalized - chia nhiều bảng, khóa ngoại) để dễ Update và không bị sai lệch. Nhưng Đọc dữ liệu lại cực ghét điều đó, vì muốn lấy dữ liệu để in ra màn hình phải `JOIN` 10 cái bảng lại tốn 5 giây. CQRS giúp ta Đọc trên 1 DB NoSQL phẳng lỳ không cần `JOIN`, và Ghi trên 1 DB SQL chặt chẽ. Cả 2 bên đều hạnh phúc.

</details>

**1. Asymmetrical Scaling Requirements**: In 95% of real-world internet applications, the Read-to-Write ratio is staggeringly disproportionate (e.g., 100:1 or 1000:1). Millions of users scroll a Twitter feed (Read) for every one user who posts a Tweet (Write). Forcing a single Database cluster to handle both workloads compromises both. CQRS allows you to horizontally scale the Query Database across 50 nodes to handle the massive read traffic, while keeping the Command Database running on a highly-consistent 3-node cluster.
**2. The Object-Relational Impedance Mismatch**: The optimal data structure for Writing is highly **Normalized** (3NF). It prevents update anomalies and enforces relational integrity via Foreign Keys. However, the optimal data structure for Reading is heavily **Denormalized**. The UI wants a massive, nested JSON object immediately; it abhors executing a 6-table `INNER JOIN` spanning millions of rows. CQRS solves this dichotomy. You Write to a Normalized DB, and Read from a Denormalized Document Store.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh luồng chạy khi Khách hàng load "Lịch sử mua hàng".
</details>

Visualizing the execution of a complex UI Query: "User's Order History Dashboard".

| Step | Monolithic CRUD Architecture | CQRS Architecture |
|---|---|---|
| **Query Engine** | Relational Database (PostgreSQL) | Query Database (MongoDB / Redis) |
| **Data Processing**| DB executes dynamic `JOIN` across `Users`, `Orders`, `Items`, `Shipping` tables. | DB simply executes `GET /user_dashboard_view/123`. |
| **CPU Cost** | Very High (Calculated on the fly every request). | Near Zero (Data is pre-calculated). |
| **Response Time**| 500ms - 2000ms. | 5ms - 10ms. |
| **Side Effects** | Blocks concurrent Write operations (Table Locks). | Completely isolated. Zero impact on Writes. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hệ thống Tìm kiếm (Elasticsearch)**: Mọi trang web có thanh Tìm kiếm mạnh mẽ đều xài CQRS. DB chính (SQL) chuyên để Ghi dữ liệu. Khi có Sản phẩm mới, nó bắn Event sang con Elasticsearch (DB Đọc). Người dùng gõ tìm kiếm thì sẽ gọi API vào Elasticsearch chứ tuyệt đối không dùng lệnh `LIKE` trên SQL.
2. **Kiến trúc Event Sourcing**: Như đã giải thích ở phần trước, Event Sourcing chỉ lưu lịch sử dạng "Cuộn băng", hoàn toàn mù tịt trong việc Query. BẮT BUỘC phải cắm thêm CQRS vào để xuất dữ liệu ra một DB Đọc thì Front-end mới xài được.
3. **Màn hình Thống kê (Dashboards / Analytics)**: Giám đốc mở màn hình Dashboard yêu cầu Thống kê Doanh thu 10 năm qua theo từng quý. Câu lệnh SQL này mất 10 phút để chạy. CQRS sẽ tạo một con Worker chạy ngầm, tính toán trước bảng Doanh thu đó vào ban đêm và nhét vào DB Đọc. Sáng ra Giám đốc bật Dashboard lên mất đúng 1 giây là có số liệu.

</details>

1. **Full-Text Search Engines (Elasticsearch)**: The most ubiquitous, stealthy implementation of CQRS. An E-commerce platform uses PostgreSQL as the Command DB to strictly manage Inventory updates and Orders. However, executing `SELECT * FROM products WHERE name LIKE '%shoe%'` is catastrophic. When a product is updated, PostgreSQL fires an event. Logstash/Debezium captures it and updates an Elasticsearch cluster (The Query DB). The Frontend UI directs all search traffic exclusively to Elasticsearch.
2. **The Symbiosis with Event Sourcing**: Event Sourcing and CQRS are architectural siblings. Because an Event Store is merely an unindexed, append-only log of chronological events, querying it for aggregate state (e.g., "Find all users aged 25") is computationally impossible. CQRS is fundamentally required. The Command side is the Event Store; the Query side consumes the Event Stream to project a queryable materialized view into a traditional database.
3. **High-Performance Dashboards & Materialized Views**: Complex Business Intelligence (BI) dashboards require aggregating billions of rows. Running these aggregate functions synchronously on the primary OLTP database degrades performance for active customers. CQRS mandates creating dedicated "Materialized Views" in a separate Read Data Store. Background workers pre-compute the heavy math asynchronously as events arrive.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Denormalization (Phi chuẩn hóa)**: Đã làm DB Đọc thì đừng ngần ngại việc Dư thừa Dữ liệu (Duplicate Data). Nếu màn hình hiển thị Tên khách hàng ở 5 chỗ khác nhau, hãy nhét cái tên đó vào 5 Document khác nhau trong MongoDB. Tiết kiệm dung lượng ở DB Đọc là tự sát.
2. **UX Lạc quan (Optimistic UI)**: Vì sự đồng bộ từ DB Ghi sang DB Đọc mất khoảng vài giây. Khách bấm nút "Thích", nếu F5 ngay lập tức có thể thấy nút chưa Thích. Hãy viết code ở Front-end kiểu "Lạc quan": Cứ cho nút Thích sáng lên và cộng số đếm ngay lập tức ở giao diện (Giả vờ là đã xong), che giấu đi sự chậm trễ của Backend.

</details>

1. **Aggressive Denormalization (Design for the Screen)**: In the Query Database, completely abandon Relational Normal Forms (3NF). Storage is cheap; Compute is expensive. Design the Read Model payload to exactly match the JSON structure the Frontend View component requires. If the user's `FullName` is needed on 5 different dashboard widgets, deliberately duplicate that string into 5 different NoSQL documents. When the Frontend queries the endpoint, the Backend should perform zero data transformation—it simply fetches the blob and fires it out.
2. **Optimistic UI (Masking Eventual Consistency)**: The greatest UX challenge in CQRS. Because the Command and Query databases are synchronized asynchronously via an Event Bus, there is a propagation delay (Eventual Consistency). A user edits their profile, clicks "Save", the page refreshes immediately, and they see their OLD profile name (because the Read DB hasn't caught up yet). **Fix**: The Frontend must employ Optimistic Updates. When the user clicks "Save", the Javascript immediately mutates the DOM locally to reflect the new state *assuming* the Command will succeed, masking the backend latency.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sự Nhất quán Tạm thời (Eventual Consistency Phobia)**: Code CQRS xong, thấy sửa dữ liệu xong mất 2 giây sau màn hình mới đổi. Lập trình viên hoảng sợ, viết thêm code bắt DB Ghi phải "Đợi" DB Đọc cập nhật xong mới trả về cho User. Việc này vô tình tạo ra một Giao dịch Phân tán Khóa chết cả 2 bên (Distributed Lock), PHÁ HỦY HOÀN TOÀN TÁC DỤNG CỦA CQRS. 
   - *Luật*: Làm CQRS là phải chấp nhận hệ thống có độ trễ đồng bộ.
2. **Áp dụng CQRS cho ứng dụng CRUD cơ bản**: CQRS code rất dài, rất tốn thời gian maintain. Nếu ứng dụng của bạn chỉ là cái Blog hoặc Admin Panel quản lý nhân sự nội bộ (Truy cập ít, query đơn giản), mà bạn vác CQRS ra xài thì bạn là tội đồ. Chỉ xài khi ứng dụng bị bóp nghẹt về hiệu năng do việc JOIN bảng quá phức tạp.

</details>

1. **Synchronizing the Asynchronous (Destroying the Pattern)**: The classic Junior Architect blunder. They implement CQRS, but the Product Manager complains about the 2-second Eventual Consistency delay. To "fix" it, the architect writes code in the Command handler that executes a synchronous API call to force the Query Database to update *before* returning `200 OK` to the client. They have just reintroduced Temporal Coupling, created a distributed lock, and completely neutralized all performance and scalability benefits of CQRS. **Rule**: Embrace Eventual Consistency. You cannot have High Availability, Partition Tolerance, AND Strong Consistency.
2. **Over-Engineering Trivial Domains**: Implementing Full CQRS (Separate bounded contexts, Kafka buses, dual databases) for a standard B2B Administrative CRUD application (e.g., "Add New Employee"). This introduces a massive architectural tax, mental overhead, and debugging complexity with absolutely zero ROI. The database would have easily handled the 5 requests per second using standard Entity Framework/Hibernate. **Rule**: Only deploy CQRS in highly complex domains where Read and Write performance requirements diverge drastically.

---

## Related Topics

- For the architecture that produces the events, see **[Event-Driven Architecture](./overview.md)**.
- For its closest partner pattern, read **[Event Sourcing](./event-sourcing.md)**.
- For understanding the tradeoff between Consistency and Performance, read **[CAP Theorem](../consistency/overview.md)**.
