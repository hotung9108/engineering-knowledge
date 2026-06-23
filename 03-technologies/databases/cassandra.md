# Cassandra / ScyllaDB

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: SQL thì an toàn nhưng không Scale được. MongoDB thì linh hoạt nhưng giới hạn Ghi. Nếu bạn xây dựng Discord, Uber, hay hệ thống giám sát Nhiệt độ với hàng triệu điểm dữ liệu gửi lên mỗi giây, tất cả các Database kể trên đều sẽ bốc cháy vì Quá tải. Đó là lúc **Apache Cassandra** xuất hiện. Nó là một cơ sở dữ liệu NoSQL "Cột rộng" (Wide-Column Store) được Facebook tạo ra để giải quyết một bài toán duy nhất: **Tốc độ GHI (Write) dữ liệu không có giới hạn**. Cassandra được thiết kế dạng Mạng lưới Phi tập trung (Masterless). Không có máy chủ nào là "Trưởng nhóm". Bạn cần ghi 10 triệu dòng/giây? Chỉ cần mua thêm máy chủ cắm vào mạng lưới, sức mạnh sẽ tăng lên tuyến tính mà không bao giờ bị nghẽn mạng hay sập toàn hệ thống. **ScyllaDB** là phiên bản viết lại của Cassandra bằng C++, giúp tốc độ tăng gấp 10 lần.

</details>

> **Summary**: Relational DBs bottleneck on vertical scaling. Document DBs (MongoDB) offer sharding, but often struggle under extreme, sustained Write-throughput. When hyperscale tech giants (Facebook, Apple, Netflix, Uber) needed to ingest millions of telemetry pings, chat messages, or time-series data points per second, they required a radically different architecture. **Apache Cassandra** is a highly scalable, distributed, Wide-Column NoSQL database. Its defining architectural trait is its **Masterless Ring Topology**. There is no "Primary" node to bottleneck writes; every node is equal. This allows for mathematically linear write scalability—if you need to double your write speed, you simply double the number of nodes. It achieves high availability and fault tolerance by replicating data across multiple datacenters with tunable eventual consistency. **ScyllaDB** is a modern, drop-in replacement for Cassandra, completely rewritten in C++ (Seastar framework) to bypass JVM garbage collection pauses, delivering an order-of-magnitude increase in throughput and sub-millisecond tail latencies.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một Bưu điện xử lý thư từ.
1. **SQL (Master-Slave)**: Có một Giám đốc (Máy chủ Master) nhận TẤT CẢ các bức thư gửi đến. Ông ta ghi sổ sách rồi mới phát cho các nhân viên phụ (Replica) đi giao. Nếu có 1 triệu người gửi thư cùng lúc, ông Giám đốc bị quá tải, gục ngã, và toàn bộ bưu điện đóng băng.
2. **Cassandra (Masterless Ring)**: Bưu điện không có Giám đốc. Chỉ có 100 nhân viên đứng thành một Vòng tròn. Khách hàng ném thư cho BẤT KỲ nhân viên nào cũng được. Nhân viên đó sẽ nhìn vào Bảng chia việc (Hash Ring) và chuyển bức thư đó cho 3 người chịu trách nhiệm lưu trữ nó. Nếu 1 nhân viên bị ốm (Máy chủ chết), những người khác vẫn làm việc bình thường. 1 triệu bức thư được chia đều cho 100 người nhận cùng một lúc. Không có nút cổ chai nào cả.

</details>

Imagine a Call Center handling customer complaints.
1. **Traditional SQL (Primary-Replica)**: There is exactly ONE Manager (The Primary Node). Every single incoming phone call MUST be answered by the Manager first. The Manager writes down the complaint, then hands copies to 5 assistants (Read Replicas). If 100,000 people call simultaneously, the Manager's phone line gets busy, and the entire system crashes. You cannot have two Managers.
2. **Cassandra (Masterless Ring Architecture)**: There are 50 Operators sitting in a circle. There is no Manager. A customer can call ANY of the 50 Operators. The Operator takes the call, uses a math formula (Consistent Hashing) to figure out which 3 specific operators are legally required to keep a copy of this complaint, and instantly forwards it to them. If 5 Operators die of a heart attack, the system doesn't care; the customers just call the other 45. There is zero single-point-of-failure.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cassandra là một cỗ máy Ghi dữ liệu khổng lồ với 3 khái niệm cốt lõi:
1. **Masterless Architecture (Không có máy chủ chủ)**: Các máy chủ (Nodes) kết nối với nhau thành một vòng tròn. Mọi Node đều có quyền Nhận dữ liệu (Ghi) và Trả dữ liệu (Đọc). Mất 1 Node không làm sập mạng.
2. **LSM-Tree (Cấu trúc ghi siêu tốc)**: Khác với SQL dùng B-Tree phải lật từng trang ổ cứng để tìm chỗ chèn dữ liệu. Cassandra ghi dữ liệu thẳng vào RAM (MemTable), sau đó khi RAM đầy, nó "Xả" (Flush) toàn bộ xuống ổ cứng thành một file liên tục. Việc chỉ GHI NỐI TIẾP (Append-only) giúp tốc độ Ghi của Cassandra nhanh bằng với tốc độ tối đa của ổ cứng.
3. **CQL (Cassandra Query Language)**: Cassandra không dùng JSON như Mongo, mà dùng ngôn ngữ truy vấn tên là CQL, nhìn giống hệt SQL (`SELECT * FROM users`). Điều này giúp các lập trình viên SQL chuyển sang học Cassandra cực kỳ dễ dàng.

</details>

Cassandra’s architecture is an amalgamation of Amazon's Dynamo (distributed hashing) and Google's BigTable (storage engine):
1. **Masterless Ring & Consistent Hashing**: Cassandra nodes form a peer-to-peer ring. Data is distributed across the nodes using a Partition Key. A hashing algorithm determines exactly which node owns which piece of data. Because every node can accept `WRITE` requests, there is no single point of failure (SPOF).
2. **The LSM-Tree Storage Engine (Log-Structured Merge-Tree)**: The secret to Cassandra's astronomical Write speed. Relational DBs use B-Trees, which require expensive, random disk I/O to update in-place. Cassandra is an *Append-Only* database. `WRITEs` are instantly appended to a sequential CommitLog on disk, and kept in memory (MemTable). When the MemTable fills, it flushes sequentially to disk as an Immutable SSTable (Sorted String Table). Sequential disk writes are exponentially faster than random writes.
3. **CQL (Cassandra Query Language)**: To bridge the learning curve, Cassandra interface looks identical to SQL. Developers define Tables, Columns, and use `SELECT` and `INSERT` statements. However, under the hood, there are NO `JOINs`, NO Foreign Keys, and NO subqueries.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Năm 2008, Facebook ra mắt tính năng "Inbox Search" (Tìm kiếm trong hàng tỷ tin nhắn của người dùng). Dữ liệu này quá khổng lồ, được ghi liên tục mỗi giây. MySQL bị quá tải. Họ tự chế ra Cassandra để giải quyết.
Cassandra tồn tại để giải quyết bài toán: **"Tôi có dữ liệu siêu to, tôi cần Ghi liên tục không ngừng nghỉ, tôi không cần JOIN dữ liệu, và tôi chấp nhận dữ liệu có thể bị trễ một chút (Eventual Consistency)"**.
Ví dụ: Lượt Like của một bức ảnh trên Instagram. Nếu bạn thấy 1000 Like, nhưng bạn của bạn ở Mỹ lại thấy 998 Like, chuyện đó hoàn toàn KHÔNG SAO CẢ. Không ai chết vì sai lệch 2 cái Like. Cassandra sinh ra cho những hệ thống chấp nhận sự sai lệch tạm thời để đổi lấy Tốc độ vô hạn và Khả năng sống sót tuyệt đối.

</details>

Cassandra was explicitly birthed at Facebook in 2008 to solve the "Inbox Search" problem—storing billions of messages with zero downtime and infinitely scalable write-throughput.
According to the **CAP Theorem** (Consistency, Availability, Partition Tolerance), a distributed system can only guarantee two of the three. Relational Databases choose **CP** (Consistency over Availability; if a node dies, the DB locks up to prevent bad data).
Cassandra exists because hyperscale applications (Netflix, Uber) choose **AP** (Availability over Consistency). If a Netflix server in Europe crashes, Netflix does not want the entire global database to freeze. Cassandra keeps accepting `WRITEs` and `READs` no matter what. It utilizes **Eventual Consistency**—meaning if you update your profile picture, a user in Japan might see the old picture for 2 seconds until the nodes synchronize in the background. For 99% of global internet applications (Likes, Comments, GPS coordinates, Chat logs), 2-second eventual consistency is perfectly acceptable in exchange for 100% uptime.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh Kiến trúc High-Availability (Đảm bảo máy chủ không sập).
</details>

Visualizing High Availability and Scaling.

| Metric | Traditional SQL (Primary-Replica) | Cassandra (Masterless Ring) |
|---|---|---|
| **Scaling Write Speed** | Very Difficult. You must buy a bigger Primary Server, or manually shard the database at the Application layer. | **Trivial**. Boot up 5 new Linux servers, install Cassandra, and point them to the Ring. The cluster auto-balances the data. Write speed instantly doubles. |
| **Node Failure (Crash)**| The Primary dies. The DB is completely locked for `WRITES`. A complex Failover script must promote a Replica to Primary (Takes 30s to 5 minutes of Downtime). | A Node dies. The Client driver instantly routes the `WRITE` to another Node holding a replica of the data. **Zero Downtime**. The Application doesn't even notice. |
| **Multi-Datacenter** | Extreme latency for cross-world replication. | Natively built-in. Data written in New York is asynchronously replicated to Tokyo automatically. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hệ thống Telemetry & IoT**: Giám sát nhiệt độ, Phân tích log của hàng ngàn máy chủ. Dữ liệu đổ về như thác nước mỗi giây (Time-series data). Cấu trúc LSM-Tree của Cassandra sinh ra để nuốt chửng lượng dữ liệu khổng lồ này.
2. **Ứng dụng Nhắn tin & Mạng xã hội**: Discord, Instagram, X (Twitter). Lưu trữ lịch sử nhắn tin của hàng tỷ người dùng. Dữ liệu này chỉ cần lưu tuần tự theo thời gian, không bao giờ cần `JOIN` phức tạp.
3. **Giỏ hàng E-Commerce (Cart)**: Tại Apple hay Amazon, khách hàng cho đồ vào giỏ liên tục. Hệ thống không được phép từ chối bất kỳ cú click "Add to Cart" nào dù máy chủ có đang bảo trì. Tính năng High Availability của Cassandra đảm bảo Giỏ hàng luôn sống sót.

</details>

1. **Time-Series, Telemetry & IoT Data**: The canonical Cassandra use-case. An energy company deploying 50,000 smart meters that ping electrical usage every second. This generates a tsunami of `WRITE` operations. Cassandra absorbs these writes in-memory and flushes them to disk without breaking a sweat.
2. **Messaging Systems & Social Feeds**: Discord natively uses ScyllaDB (the C++ clone of Cassandra) to store Trillions of chat messages. Chat logs are immutable (mostly Append-Only) and partitioned perfectly by `Channel_ID`. They never require relational `JOINs` to other tables, fitting Cassandra's data model flawlessly.
3. **High-Availability E-Commerce Carts**: Amazon's Dynamo paper (the inspiration for Cassandra) explicitly stated: *"Adding an item to a shopping cart must never fail"*. During Black Friday, Relational DBs lock up under the Write-load. Cassandra ensures that the `WRITE` (Adding to Cart) succeeds instantly on available nodes, reconciling the data later in the background.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Thiết kế theo Truy vấn (Query-Driven Modeling)**: Đây là CÚ SỐC lớn nhất với các Dev SQL. Trong SQL, bạn thiết kế Bảng trước, rồi viết `SELECT` sau. Trong Cassandra, bạn PHẢI BIẾT TRƯỚC màn hình UI cần hiển thị cái gì, và bạn thiết kế một cái Bảng CHỈ ĐỂ PHỤC VỤ riêng cho cái màn hình đó. Nếu màn hình đó cần Tên User và Tên Bài Viết, bạn KHÔNG ĐƯỢC JOIN 2 bảng. Bạn phải tạo ra Bảng thứ 3 chứa sẵn Tên User và Tên Bài viết (Khử chuẩn hóa - Data Duplication). Trong Cassandra, "Ổ cứng cực rẻ, Tốc độ là vàng". Việc copy dữ liệu ra làm 3 bản cho 3 màn hình khác nhau là chuyện bắt buộc.
2. **Chọn Partition Key cực chuẩn**: Dữ liệu trong Cassandra bị băm ra dựa trên cái Chìa khóa (Partition Key). Nếu bạn làm app Chat, chọn `Channel_ID` làm Key là chuẩn. Nhắn tin vào Channel nào thì lưu ở đúng máy chủ đó. Nhưng nếu bạn chọn `Day` (Ngày) làm Key, thì ngày hôm nay TOÀN BỘ tin nhắn của cả thế giới sẽ dồn hết vào 1 cái máy chủ duy nhất (Hot Partition), làm máy đó cháy khét, trong khi 99 máy khác ngồi chơi.

</details>

1. **Query-Driven Data Modeling (Denormalization is Mandatory)**: The most difficult paradigm shift for Relational Engineers. In SQL, you model Entities (Users, Orders). In Cassandra, you model Queries. **Rule**: If your Application needs to display "Orders by User" on one screen, and "Orders by Date" on another screen, you do NOT create one table and use different `WHERE` clauses. You physically create TWO separate tables (`orders_by_user` and `orders_by_date`) and duplicate the data into both. Storage is cheap; CPU `JOINs` and network hops are expensive.
2. **Mastering the Partition Key (Avoiding Hotspots)**: Cassandra distributes data across the Ring using a hash of the Partition Key. The Golden Rule of Cassandra is: **"One Query = One Partition (One Node)"**. If you select `Country` as the Partition Key, and 80% of your users are in the `USA`, then 80% of your traffic hits exactly ONE node in the cluster, melting its CPU while the other nodes sit idle (A Hot Partition). The Partition Key must explicitly ensure an even mathematical distribution of data across the entire cluster (e.g., `Device_ID` or `User_ID`).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Xóa Dữ Liệu (Tombstones)**: Đừng dùng Cassandra nếu bạn cần `UPDATE` hoặc `DELETE` dữ liệu liên tục. Khi bạn Xóa 1 dòng, Cassandra KHÔNG XÓA NÓ (vì cấu trúc LSM không cho phép xóa giữa chừng). Nó tạo ra một "Bia mộ" (Tombstone) đánh dấu dòng đó là "đã chết". Nếu bạn xóa quá nhiều, máy chủ sẽ ngập tràn Bia mộ. Khi Đọc dữ liệu, hệ thống phải quét qua hàng triệu cái Bia mộ rác, làm tốc độ cực kì chậm.
2. **Dùng Cassandra cho Dự án nhỏ**: Thiết lập một cụm Cassandra yêu cầu tối thiểu 3 máy chủ lớn, tốn rất nhiều tiền và công sức vận hành (DevOps). Chỉ dùng nó khi bạn thực sự có HÀNG TRIỆU giao dịch mỗi giây. Dưới mức đó, Postgres hoàn toàn làm tốt hơn và nhàn hơn rất nhiều.

</details>

1. **The Tombstone Catastrophe (Antipattern: Deletions/Queues)**: Because Cassandra uses immutable SSTables on disk, you cannot physically overwrite or delete data in place. When you issue a `DELETE`, Cassandra writes a brand new record called a "Tombstone" (a marker saying the data is dead). If you use Cassandra as a Message Queue (inserting and deleting millions of messages a day), you will generate millions of Tombstones. When an Operator queries the database, Cassandra must sequentially scan through all the dead Tombstones to find the living data, causing catastrophic Read Latency timeouts. **Rule**: Cassandra is an Append-Heavy database. Avoid massive deletion workloads.
2. **Premature Optimization (The Small Data Trap)**: Adopting Cassandra requires immense operational complexity (DevOps). A production cluster requires a minimum of 3 (usually 6+) massive JVM-tuned Linux nodes. Maintaining consistency levels, running repairs, and monitoring GC pauses is a full-time job. **Rule**: Do NOT use Cassandra unless your database has physically outgrown the vertical scaling limits of PostgreSQL (i.e., you are sustaining 10,000+ Writes per second or storing 50+ Terabytes of active data).

---

## Related Topics

- Cassandra handles distributed storage, but if you need an In-Memory cache for reads, look at **[Redis](./redis.md)**.
- If your data is highly relational and requires ACID transactions, stay with **[PostgreSQL](./postgresql.md)**.
- If you need flexible JSON structures but not necessarily hyperscale write speed, see **[MongoDB](./mongodb.md)**.
