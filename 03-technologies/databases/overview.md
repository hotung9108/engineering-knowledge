# Databases Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Frontend là khuôn mặt, Backend là não bộ, thì **Database (Cơ sở dữ liệu)** chính là Bộ nhớ dài hạn. Mọi thứ xử lý trên RAM của Backend sẽ biến mất ngay lập tức khi cúp điện. Database là nơi duy nhất giữ cho dữ liệu sống sót (Persistence) mãi mãi trên ổ cứng. Việc chọn sai Database giống như xây tòa nhà 100 tầng trên nền cát. Ngành Kỹ thuật Dữ liệu phân chia thế giới thành hai thế lực khổng lồ: **SQL (Relational)** chuyên cho các dữ liệu có cấu trúc cực kì chặt chẽ như tiền bạc, kế toán; và **NoSQL (Non-Relational)** chuyên trị những dữ liệu siêu linh hoạt, siêu lớn như dòng thời gian mạng xã hội hay log sự kiện.

</details>

> **Summary**: While the Backend executes ephemeral Business Logic in volatile memory (RAM), the **Database** is the foundational bedrock of Data Persistence. It is engineered to write state to non-volatile storage (Disk/SSD), ensuring survival against power failures, crashes, and server reboots. Architectural database selection is the most critical and difficult decision in software engineering because, unlike stateless backend code, data has *gravity*. Migrating massive, live datasets between different database paradigms is an operational nightmare. The landscape is fundamentally bifurcated into two dominant ideologies: **SQL (Relational Database Management Systems - RDBMS)**, strictly enforcing ACID properties and normalized schemas for financial-grade integrity; and **NoSQL (Not Only SQL)**, prioritizing horizontal scalability, flexible schemas, and eventual consistency for massive, unstructured Big Data workloads.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn mở một Thư viện khổng lồ.
1. **SQL (Quan hệ - RDBMS)**: Giống như một cái tủ hồ sơ bằng sắt cực kì cứng nhắc. Bạn quy định: Tủ A chỉ đựng Sách (tên, tác giả). Tủ B chỉ đựng Thẻ thành viên (tên, ngày sinh). Nếu một cuốn sách không có đủ 2 thông tin đó, bạn cấm không cho cất vào tủ. Khi tìm kiếm, bạn dễ dàng nói: "Lấy cho tôi Thẻ của người đã mượn cuốn sách tên X". Rất chặt chẽ, không bao giờ nhầm lẫn.
2. **NoSQL (Phi Quan hệ)**: Giống như một cái kho bằng bìa các-tông khổng lồ. Khách hàng ném vào đó đủ thứ: Có cuốn sách thì ghim kèm bức ảnh, có cuốn sách lại kẹp thêm đĩa CD. Bạn không cần quy định trước hình thù của chúng. Gói đồ nào cũng được ném vào kho rất nhanh. Rất dễ mở rộng (chỉ việc mua thêm thùng các-tông), nhưng khi tìm kiếm sẽ vất vả hơn nếu bạn không sắp xếp cẩn thận.

</details>

Imagine running a massive Filing System.
1. **SQL (Relational)**: You buy rigid metal filing cabinets. You explicitly enforce rules: "Cabinet 1 is strictly for Employee ID Cards. Cabinet 2 is strictly for Salary Checks. To link them, you must use the exact Employee ID number." If someone tries to put a half-finished sticky note into the Salary cabinet, the cabinet physically locks and rejects it (Schema Validation). It is highly organized, strictly mathematical, and guarantees perfection.
2. **NoSQL (Document-Based)**: You use massive, flexible folders. Inside one folder, you toss the Employee ID, their Salary Check, a photo of their dog, and a random sticky note. You don't care about the format. It's incredibly fast to just dump everything into one folder and retrieve the whole folder at once. It's perfect for rapid, chaotic collection, but it's much harder to guarantee that *every* folder actually contains a Salary Check.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thế giới Database được chia làm các nhóm kiến trúc chính:
1. **Relational / SQL (PostgreSQL, MySQL, SQL Server)**: Dữ liệu được lưu dưới dạng Bảng (Cột và Hàng) y hệt như Microsoft Excel. Các Bảng được "nối" (Join) với nhau bằng Khóa ngoại (Foreign Keys). Chúng tuân thủ tuyệt đối định lý **ACID** (Bảo đảm tính toàn vẹn dữ liệu, không bao giờ có chuyện tiền bị trừ ở người chuyển mà chưa cộng cho người nhận).
2. **Document NoSQL (MongoDB)**: Dữ liệu lưu dưới dạng các tệp JSON khổng lồ (Document). Không có bảng, không có Cột cố định. Một Document có thể có 5 trường dữ liệu, Document kế bên có thể có 100 trường dữ liệu.
3. **Key-Value In-Memory (Redis)**: Dữ liệu không lưu trên Ổ cứng, mà lưu thẳng trên RAM theo kiểu `Khóa - Giá trị` (`Token123` = `User_A`). Tốc độ đọc/ghi cực nhanh (dưới 1 mili-giây), dùng làm bộ nhớ đệm (Cache) để giảm tải cho Database chính.
4. **Wide-Column NoSQL (Cassandra, ScyllaDB)**: Thiết kế cho dữ liệu siêu khổng lồ, dàn trải trên hàng trăm máy chủ. Nó hi sinh các câu lệnh Nối bảng (Join) phức tạp để đổi lấy tốc độ Ghi dữ liệu không có giới hạn (Thường dùng cho Log dữ liệu, IoT, lịch sử tin nhắn).

</details>

Database architectures are fundamentally classified by their Data Models and Storage Engines:
1. **Relational / SQL (e.g., PostgreSQL, MySQL)**: Data is structured into strict two-dimensional Tables (Rows and Columns). Relationships between entities are established mathematically using Primary and Foreign Keys. They strictly enforce the **ACID paradigm** (Atomicity, Consistency, Isolation, Durability), making them the mandatory choice for Financial Ledgers and highly normalized schemas.
2. **Document-Oriented NoSQL (e.g., MongoDB, DynamoDB)**: Data is stored as schema-less, nested JSON/BSON documents. Documents are highly polymorphic (they do not need to share the same structure). This denormalized approach eliminates expensive `JOIN` operations, allowing rapid fetching of deeply nested hierarchical data in a single read.
3. **In-Memory Key-Value Stores (e.g., Redis, Memcached)**: Operates primarily in RAM (bypassing slow Disk I/O). Data is stored as a simple Dictionary (Hash Map). It provides sub-millisecond read/write latency. It is exclusively used as an ephemeral Caching layer, Session Store, or Message Broker (Pub/Sub) to shield the primary database from read-heavy traffic.
4. **Wide-Column Stores (e.g., Cassandra, HBase)**: Engineered for extreme horizontal scalability across distributed datacenters. It uses a sparse, multi-dimensional map architecture. It completely abandons ACID transactions and `JOINs` in favor of high-availability and unbounded Write-throughput (perfect for IoT telemetry, Time-Series data, or massive Chat Histories).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong 40 năm, SQL (Oracle, MySQL) thống trị hoàn toàn thế giới phần mềm. Dữ liệu Kế toán, Nhân sự đều dùng SQL. Tại sao NoSQL lại xuất hiện?
Vấn đề nằm ở **Scale (Mở rộng)**. SQL được thiết kế để Scale theo chiều dọc (Scale Up). Nghĩa là nếu Database bị chậm, bạn phải mua một cái Máy chủ to hơn, xịn hơn (Thêm RAM, CPU). Nhưng máy chủ mạnh nhất thế giới cũng có giới hạn.
Đến thập niên 2000, Google và Facebook xuất hiện. Dữ liệu của họ không phải là vài triệu dòng Kế toán, mà là Hàng tỷ bài viết, Hàng tỷ lượt Like mỗi ngày. Không một máy chủ đơn lẻ nào chứa nổi. 
Họ tạo ra **NoSQL** để giải quyết bài toán Scale theo chiều ngang (Scale Out). Thay vì mua 1 máy chủ siêu khủng, NoSQL cho phép bạn mua 10.000 máy tính cùi bắp, nối chúng lại với nhau, và xẻ nhỏ dữ liệu (Sharding) ném vào 10.000 máy đó. Nếu cần thêm dung lượng, chỉ việc cắm thêm máy tính. Tốc độ Ghi gần như Vô hạn.

</details>

For decades, the Relational (SQL) model was a complete monopoly. Why did the NoSQL revolution occur?
The fundamental constraint of RDBMS architecture is **Vertical Scalability (Scaling Up)**. Because SQL heavily relies on referential integrity (Foreign Keys) and distributed ACID locks, it is notoriously difficult to split a single SQL database across multiple physical machines. When an SQL database hits its capacity limit, the only solution is to buy a massively expensive, single supercomputer (more CPU/RAM).
The Web 2.0 explosion (Facebook, Google, Amazon) generated Petabytes of unstructured data (User Analytics, Session Logs, Infinite Feeds). Vertical scaling became physically and financially impossible.
**NoSQL** was engineered to solve **Horizontal Scalability (Scaling Out)**. By completely abandoning strict schema validation and complex `JOIN` capabilities, NoSQL databases can aggressively partition (Shard) data across thousands of cheap commodity servers. If you need more storage or write-throughput, you simply add another server node to the cluster.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cách lưu trữ một bài viết (Post) có kèm Bình luận (Comments).
</details>

Visualizing Data Normalization (SQL vs NoSQL Document).

| Metric | SQL / Relational (Normalized) | NoSQL / MongoDB (Denormalized) |
|---|---|---|
| **Data Structure** | **Table 1 (Posts)**: `[ID: 1, Title: "Hello"]`<br>**Table 2 (Comments)**: `[ID: 9, Post_ID: 1, Text: "Nice!"]` | **1 JSON Document**: <br>`{`<br>` id: 1, title: "Hello",`<br>` comments: [{text: "Nice!"}]`<br>`}` |
| **Retrieving the Post + Comments** | Requires a computational `JOIN` operation across two separate tables. `SELECT * FROM Posts JOIN Comments ON...` | Extremely fast. The DB engine retrieves exactly 1 document from Disk. No Joins needed. |
| **Updating a Comment's Author Name** | Easy. You update the Author Table once, and all joined views are instantly updated (Consistency). | Nightmare. You must manually find and update every single nested JSON document where that author left a comment (Data Anomaly Risk). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là công thức chọn Database phổ biến nhất hiện nay:
1. **PostgreSQL (Sự lựa chọn mặc định)**: Bất cứ khi nào bạn bắt đầu dự án mới (SaaS, E-commerce, Tài chính), hãy nhắm mắt chọn PostgreSQL. Nó là hệ quản trị SQL xịn nhất mã nguồn mở. Nó chặt chẽ tuyệt đối, và hỗ trợ lưu cả JSON cực kì xịn xò. (Lưu ý: Chọn MySQL cũng tốt, nhưng PostgreSQL hiện đại hơn).
2. **MongoDB (Dữ liệu thay đổi hình thù liên tục)**: Khi bạn làm Game, Game có 100 loại quái vật, mỗi con có các chỉ số khác nhau (con có máu, con có giáp, con biết bay). Việc tạo 100 bảng SQL là thảm họa. Bạn hãy đẩy tất cả thành các cục JSON nhét vào MongoDB. Hoặc làm phần mềm dạng Catalog sản phẩm linh hoạt.
3. **Redis (Tăng tốc độ bàn thờ)**: Khi bạn có một Bảng Xếp Hạng (Leaderboard) được 1 triệu người F5 liên tục mỗi giây. Nếu gọi PostgreSQL 1 triệu lần, Server sẽ sập. Bạn sẽ dùng Redis để lưu tạm Bảng xếp hạng đó lên RAM. Đọc từ RAM không có độ trễ.
4. **Cassandra (Dữ liệu khổng lồ không thể mất)**: Khi bạn làm hệ thống Chat (như Discord), hoặc hệ thống lưu tọa độ GPS của 10 triệu chiếc xe Taxi. Mỗi giây có hàng chục vạn lượt Ghi dữ liệu. Cấu trúc cụm của Cassandra sinh ra để nuốt chửng lượng Write khổng lồ đó mà không bao giờ sập mạng.

</details>

The Modern Database Selection Matrix:
1. **The Default Champion (PostgreSQL)**: If you are building a B2B SaaS, E-Commerce, or FinTech platform, PostgreSQL is the undisputed default choice. It offers impenetrable ACID compliance for financial ledgers, immense extensibility (PostGIS for geolocation), and its `JSONB` column type effectively absorbs 80% of MongoDB's use cases within a relational context.
2. **Schema Polymorphism & Rapid Prototyping (MongoDB)**: Ideal for Catalog Management (where a Laptop has completely different attributes than a T-Shirt), Content Management Systems (CMS), and Game State storage. If the data structure morphs rapidly and relationships are heavily nested (Hierarchical data) rather than interconnected, Document NoSQL excels.
3. **Ultra-Low Latency Caching (Redis)**: Deployed explicitly as a protective shield in front of Postgres/Mongo. Used for storing ephemeral API session tokens (JWT blacklists), computing Real-Time Leaderboards via Sorted Sets, or caching computationally expensive SQL aggregation queries to prevent database CPU starvation during traffic spikes.
4. **Hyperscale Write-Intensive Workloads (Cassandra / ScyllaDB)**: When Discord logs billions of chat messages a day, or Uber tracks millions of concurrent driver GPS telemetry pings. Relational DB locks would collapse. Wide-column stores are masterless, distributed networks that absorb astronomical write-throughput with zero single-points-of-failure.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Đánh Index (Chỉ mục)**: Lỗi 99% người mới mắc phải. Bảng có 10 triệu dòng, bạn tìm `WHERE email = 'a@a.com'`. Database phải lật từng dòng từ trên xuống dưới (Full Table Scan), mất 5 giây. Nếu bạn tạo Index cho cột Email (giống như mục lục sách), Database sẽ dùng thuật toán B-Tree để tìm ra Email đó trong 0.001 giây. Việc đánh Index sai có thể làm Server sập khi có đông khách.
2. **Tách biệt Đọc / Ghi (Read Replica)**: Khi App quá lớn, một Database làm cả 2 việc sẽ nghẽn. Người ta nhân bản Database ra: 1 máy chủ xịn chỉ chuyên làm nhiệm vụ GHI (Master Node). 3 máy chủ phụ (Read Replicas) sẽ copy dữ liệu từ máy chính và chỉ phục vụ việc ĐỌC cho khách hàng.

</details>

1. **Aggressive Indexing Strategy (B-Trees)**: The single most impactful performance optimization in Backend Engineering. Executing a `SELECT * WHERE email = ?` on a 50-million-row table without an index forces a Sequential Table Scan (O(N) complexity), locking the CPU. Adding a B-Tree Index reduces search complexity to O(log N), returning results in milliseconds. **Caution**: Over-indexing is equally fatal. Every index drastically slows down `INSERT`/`UPDATE` operations because the database must recalculate the B-Tree upon every write. Only index columns heavily utilized in `WHERE`, `JOIN`, or `ORDER BY` clauses.
2. **CQRS & Read Replicas (Master-Slave Architecture)**: In heavily trafficked applications, Database CPU utilization hits 100%. The solution is architectural splitting. The Primary Database (Master) handles 100% of the ACID `INSERT`/`UPDATE`/`DELETE` mutations. Asynchronously, it replicates this state to 5 Secondary Databases (Read Replicas). The application routes 100% of `SELECT` queries to the Replicas. This isolates heavy analytical reads from blocking transactional writes.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng NoSQL cho Dữ liệu có Quan hệ chặt (Tự sát)**: Nhiều người mù quáng thần thánh hóa MongoDB vì code nhanh. Khi làm app Ngân hàng bằng Mongo, vì không có Ràng buộc Khóa ngoại (Foreign Key), dữ liệu bị rác. Lập trình viên phải tự viết code C# để Join dữ liệu bằng tay. Code vừa rườm rà, vừa sai lệch.
2. **Không kết nối Connection Pooling**: Mỗi lần Backend gọi Database, nó phải "bắt tay" (Mở kết nối mạng). Việc bắt tay này rất tốn thời gian. Nếu 1000 khách vào, mở 1000 kết nối, DB sẽ từ chối phục vụ (Too many connections). Luôn luôn phải cấu hình Connection Pool (Một bể chứa sẵn 50 kết nối luôn mở) để dùng lại.

</details>

1. **Misapplying NoSQL (The Relational Mirage)**: The most catastrophic architectural mistake of the 2010s. Developers chose MongoDB because JSON syntax was "easier", but modeled highly relational E-commerce data (Users $\rightarrow$ Orders $\rightarrow$ Invoices). Because NoSQL lacks server-side `JOIN` capabilities and Foreign Key constraints, developers were forced to implement "Joins in Application Memory" (fetching User, looping to fetch Orders), leading to N+1 network nightmares, Orphaned records, and massive Data Inconsistency anomalies. **Rule**: If your data fundamentally relies on Relationships, use a Relational Database.
2. **Connection Exhaustion (Ignoring Connection Pooling)**: Establishing a raw TCP/IP connection to PostgreSQL requires significant TCP/TLS handshaking overhead. If your Node.js application attempts to open a brand new connection for every incoming HTTP request, under load, the Database will instantly hit its `max_connections` limit and violently reject all traffic. **Rule**: Always configure a robust Database Connection Pool (e.g., PgBouncer). The backend opens 100 persistent connections at startup and heavily recycles them for thousands of concurrent requests.

---

## Related Topics

- For strictly structured Relational Data, proceed to **[PostgreSQL](./postgresql.md)**.
- For flexible Document storage, proceed to **[MongoDB](./mongodb.md)**.
- To accelerate database reads, layer it with **[Redis](./redis.md)**.
- For massive, distributed Write workloads, explore **[Cassandra](./cassandra.md)**.
