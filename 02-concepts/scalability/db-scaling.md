# Database Scaling

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Máy chủ chạy Code (NodeJS/Java) là Stateless (Không trạng thái) nên bạn có thể nhân bản nó lên 1000 cái dễ như ăn kẹo. Nhưng Database thì chứa Dữ liệu (Stateful), bạn KHÔNG THỂ cứ thế mà nhân bản nó lên được. Nếu 2 khách hàng cùng sửa 1 dòng dữ liệu trên 2 cái DB khác nhau thì biết nghe ai? Vì vậy, việc Mở rộng Database (Database Scaling) là bài toán khó nhất, phức tạp nhất, và nguy hiểm nhất trong Hệ thống phân tán. Nó bao gồm các kỹ thuật như Master-Slave (Chia Đọc/Ghi), Partitioning (Cắt dọc), và Sharding (Băm nát dữ liệu ra nhiều máy).

</details>

> **Summary**: Scaling stateless application servers is trivially solved by placing them behind a Load Balancer. Scaling Stateful persistence layers (Databases) is arguably the most complex architectural challenge in Computer Science. Because Databases hold the absolute Truth, you cannot blindly duplicate them without introducing catastrophic synchronization and consistency anomalies (The CAP Theorem). **Database Scaling** encapsulates a progression of architectural patterns—from Vertical Scaling, to Read Replicas (Master-Slave), to Vertical Partitioning, and ultimately to Horizontal Sharding—designed to exponentially increase data storage and query throughput while frantically attempting to maintain ACID guarantees.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng Database là một Cuốn Sổ Ghi Nợ. Ban đầu có 1 ông Chủ tịch tự Ghi nợ và tự Đọc nợ cho khách nghe (Monolithic). Nhưng quán quá đông:
1. **Master-Slave (Đọc/Ghi)**: Ông Chủ tịch (Master) giờ CHỈ CHUYÊN GHI NỢ. Ổng thuê 3 cô Thư ký (Slave). Cứ mỗi lần ổng ghi xong 1 dòng, ổng đưa cho 3 cô chép lại y chang. Khách đến hỏi nợ thì 3 cô Thư ký sẽ ĐỌC cho khách nghe. Giải quyết được khâu Đọc.
2. **Sharding (Băm nhỏ)**: Quán siêu đông, 1 mình ông Chủ tịch ghi không xuể, gãy cả tay. Ổng quyết định xé Cuốn Sổ làm 3 phần. Ông A chuyên ghi nợ cho khách tên A-H. Ông B ghi cho khách I-Q. Ông C ghi cho khách R-Z. Quán đã xử lý được lượng Ghi khổng lồ, nhưng giờ muốn tính "Tổng nợ của quán" thì vô cùng cực khổ vì phải đi hỏi cả 3 ông rồi cộng lại.

</details>

Imagine the Database is a physical Ledger Book managed by a single Librarian.
1. **Read Replicas (Master-Replica)**: The library gets too busy. The Head Librarian (Master) decides he will *only* WRITE new entries. He hires 3 Assistants (Replicas). Every time he writes a line, he tells the 3 Assistants to copy it into their own books. When customers want to READ a book, they ask the Assistants. This brilliantly solves Read-heavy traffic.
2. **Sharding (Horizontal Partitioning)**: The library becomes massive. The Head Librarian's hand is cramping; he cannot WRITE fast enough. He takes the Ledger and rips it into three pieces. Librarian A handles Authors A-M. Librarian B handles N-Z. Now, you have completely eliminated the Write bottleneck. However, if a customer asks: "How many books do we have in total?", you must now manually ask both librarians and add the numbers together (Cross-shard querying is painful).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

4 cấp độ tiến hóa của Database Scaling:
1. **Scale Up (Nâng cấp phần cứng)**: Cách ngu ngốc nhưng hiệu quả nhất. Mua ổ cứng SSD NVMe, đắp 512GB RAM cho con MySQL. Tốn tiền nhưng không phải sửa code.
2. **Read Replicas (Chuyên môn hóa Đọc)**: Đa số web có tỷ lệ Đọc/Ghi là 10/1. Ta dựng 1 máy Master (Chỉ nhận lệnh `INSERT/UPDATE`), và cài đặt đồng bộ dữ liệu sang 3 máy Slave (Chỉ nhận lệnh `SELECT`).
3. **Vertical Partitioning (Chia dọc theo Bảng)**: Bảng `Users` thì để ở Máy chủ 1. Bảng `Orders` thì để ở Máy chủ 2. Giải phóng dung lượng ổ cứng. Nhược điểm: CẤM xài lệnh `JOIN` giữa 2 bảng.
4. **Sharding (Băm ngang theo Dòng)**: Cùng là bảng `Users`. Nhưng 10 triệu User Nam nhét vào Server 1. 10 triệu User Nữ nhét vào Server 2. Đây là cảnh giới tối cao của Database, khả năng mở rộng vô hạn.

</details>

The Evolutionary Tech Tree of Database Scaling:
1. **Vertical Scaling (The Wallet Method)**: Throwing money at AWS. Upgrading an RDS instance from `db.m5.large` to `db.m5.24xlarge` (768GB RAM, 96 vCPUs). It requires zero application code changes but hits a hard physics ceiling and costs thousands of dollars a month.
2. **Read Replicas (Master-Slave)**: Exploits the 90/10 Read/Write ratio of web apps. All `INSERT/UPDATE` operations strictly hit the Master Node. The Master uses an asynchronous Binlog replication stream to perfectly copy the data to 3 Read Replica Nodes. All `SELECT` queries are load-balanced across the Replicas.
3. **Vertical Partitioning (By Domain)**: Splitting tables across entirely different databases based on bounded contexts. `Users_DB` holds user data; `Inventory_DB` holds products. Pro: Reduces disk I/O contention. Con: Completely destroys the ability to perform Cross-Table `JOIN`s or enforce Foreign Keys.
4. **Sharding (Horizontal Partitioning)**: The ultimate endgame. Splitting a single massive 1-Billion-Row `Users` table across 10 physical Database Servers (100 million rows each). A Shard Key (e.g., `user_id % 10`) mathematically determines exactly which server holds which rows. Yields infinite scale.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn không thể dùng Load Balancer để "Cân bằng tải" Database như cách bạn làm với Web Server được. 
Nếu bạn có 1 tỷ người dùng, dung lượng Bảng `Users` là 500GB. Bất kỳ câu lệnh `SELECT` nào cũng phải quét qua cái cây Index khổng lồ đó, tốn cực nhiều CPU và Disk I/O (Tốc độ đọc ổ cứng). RAM của máy chủ không thể nhét vừa 500GB Index, dẫn đến việc liên tục phải đọc từ Ổ cứng (Page Fault), làm hệ thống chậm như rùa.
Sharding sinh ra để giải quyết triệt để nút thắt Disk I/O này. Xé 500GB ra thành 10 máy, mỗi máy giữ 50GB. 50GB thì thừa sức nhét vừa vào RAM. Tốc độ truy vấn lại nhanh như chớp.

</details>

You fundamentally cannot just "Put a Load Balancer in front of MySQL" and expect it to magically scale Writes. 
When a single Monolithic Table grows to 1 Billion rows (e.g., 500GB of data), the B-Tree Indexes grow proportionately massive. If the Index is 100GB, but the Server only has 32GB of RAM, the Database Engine cannot cache the Index. It suffers brutal **Cache Thrashing** and constant Disk I/O (Page Faults) to resolve queries. Queries degrade from 5ms to 5000ms.
**Sharding** exists purely to annihilate this structural Memory/Disk constraint. By mathematically sharding the 500GB table across 10 distinct Servers (50GB each), the Index on each server drops to 10GB. The 10GB Index fits perfectly inside the RAM of a cheap 16GB server. Queries are resolved 100% in-memory at lightning speed.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh truy vấn `SELECT * FROM Orders WHERE user_id = 999` trên bảng có 1 Tỷ dòng.
</details>

Visualizing a query on a 1 Billion row `Orders` table.

| Metric | Monolithic DB (No Sharding) | Sharded DB (10 Shards by `user_id`) |
|---|---|---|
| **Index Size** | 100 GB (Does not fit in RAM). | 10 GB per shard (Fits entirely in RAM). |
| **Disk I/O** | Heavy. Disk swapping required. | Zero. Query served purely from Memory. |
| **Query Routing**| Simple. Always hits the primary DB. | Application mathematically routes to Shard #9. |
| **Search Time**| $O(\log(1,000,000,000))$ = Slow | $O(\log(100,000,000))$ = Very Fast |
| **Danger** | Single point of absolute failure. | Cross-shard aggregation is nearly impossible. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Read Replicas**: Gần như mọi trang web (Blog, Báo điện tử, E-commerce) đều dùng. Vì Đọc luôn luôn nhiều hơn Ghi.
2. **Vertical Partitioning (Microservices)**: Shopee không dùng 1 DB. Bảng Chat nằm ở DB Cassandra (Chuyên ghi nhanh). Bảng User nằm ở MySQL. Bảng Search nằm ở Elasticsearch. Chọn DB phù hợp cho từng Bảng.
3. **Sharding (Chia Shard)**: 
   - *Theo Vị trí Địa lý (Geo-Sharding)*: Server Châu Á lưu data người Châu Á. Giúp tải web nhanh hơn và tuân thủ Luật bảo mật dữ liệu của từng quốc gia.
   - *Theo Thuật toán Hash*: Discord lưu hàng tỷ tin nhắn mỗi ngày. Họ dùng Cassandra/ScyllaDB để Hash cái `channel_id` và băm nhỏ data ra hàng ngàn Server khác nhau.

</details>

1. **Read Replicas**: The immediate default for 99% of growing architectures. A WordPress blog or Magento store gets hammered by `SELECT` queries during a traffic spike. Pointing the read queries to 3 Replicas instantly quadruples the capacity.
2. **Vertical Partitioning (Polyglot Persistence)**: The cornerstone of Microservices. You don't just split the tables; you split the technology. `Users` goes to PostgreSQL (ACID). `ProductCatalog` goes to MongoDB (Document flexibility). `Chat_Messages` goes to Cassandra (Insane write-throughput). `Search` goes to Elasticsearch.
3. **Horizontal Sharding**: 
   - *Geo-Sharding*: Required by Law (GDPR). EU users are mathematically sharded into Frankfurt Data Centers. US users into Virginia. Provides perfect data residency and massively lowers latency.
   - *Hash-Based Sharding*: Chat applications (Discord, Slack). Discord processes billions of messages. They hash the `guild_id` (Server ID). All messages for a specific Server reliably route to a specific Database Node, distributing the petabytes of data evenly across the cluster.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cố gắng KHÔNG xài Sharding**: Tác giả cuốn "Designing Data-Intensive Applications" khuyên: Đừng bao giờ đụng đến Sharding nếu chưa đi vào đường cùng. Hãy kiệt sức với Vertical Scaling, rồi đến Cache, rồi đến Read Replicas trước. Khi bạn Shard, bạn vĩnh viễn mất đi sức mạnh của SQL (`JOIN`, Khóa ngoại, Transaction).
2. **Chọn Shard Key cực kỳ cẩn thận**: Shard Key là cột dùng để băm dữ liệu (Ví dụ: `user_id`). Nếu bạn chọn sai, bạn sẽ chết. Giả sử bạn Shard theo `Ngày_Tạo`. Ngày hôm nay, TẤT CẢ bản ghi mới đều chui vào 1 cái Máy chủ của Ngày Hôm Nay. Máy đó sẽ bị bốc cháy (Hotspot), trong khi 9 máy chứa dữ liệu cũ ngồi chơi. Phải dùng **Hash Sharding** để dữ liệu tản đều ra.

</details>

1. **The Golden Rule of Sharding: Don't Shard**: Martin Fowler and Martin Kleppmann universally agree: Sharding is a weapon of last resort. It introduces unfathomable operational complexity. Schema migrations become a nightmare. Cross-shard `JOIN`s are structurally prohibited. Distributed Transactions require complex Sagas. Exhaust every other option first (Massive RAM upgrades $\rightarrow$ Aggressive Redis Caching $\rightarrow$ 5 Read Replicas) before ever considering manual horizontal sharding in an RDBMS.
2. **Shard Key Selection (Avoiding Hotspots)**: The most fatal mistake in Sharding is choosing a monotonically increasing Shard Key (e.g., `created_at` timestamp). If you shard by Month, during August, 100% of global Write traffic is violently funneled into the "August Shard" node, melting its CPU, while the other 11 nodes (Jan-July) sit completely idle at 0% CPU. This defeats the entire purpose of sharding. **Fix**: Use Consistent Hashing on a high-cardinality ID (e.g., `hash(user_id) % 10`). This guarantees statistically perfect, uniform distribution of reads and writes across all nodes.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lỗi Dữ liệu Cũ (Replication Lag)**: Khi dùng Read Replica, Master ghi xong sẽ mất khoảng `50ms` để chép sang Slave. Nếu Khách hàng đổi Tên, Master đã sửa thành Tên Mới, rồi UI gọi API Get Profile (API này chọc vào Slave). Do chưa tới 50ms, Slave vẫn giữ Tên Cũ $\rightarrow$ Giao diện hiện Tên Cũ. Khách hàng F5 liên tục vì tưởng web lag.
   - *Cách giải quyết (Read-Your-Own-Writes)*: Nếu bạn vừa Update một thứ gì đó, trong 5 giây tiếp theo, hãy ép hệ thống bẻ đường truyền của người dùng đó chạy thẳng vào Master để đọc. Hoặc hiển thị tạm bằng Javascript.
2. **Lỗi truy vấn đa Shard (Cross-shard JOINs)**: Khi đã cắt bảng `Orders` làm 10 phần ở 10 máy. Giám đốc đòi xem "Top 10 đơn hàng lớn nhất Hệ thống". Bạn khóc thét! Vì bạn phải viết code đi hỏi từng Máy chủ 1, lấy về 10 cái danh sách, rồi nhét vào RAM của máy Code để Sort lại. Rất chậm và tốn RAM. Đã Shard là phải hy sinh các truy vấn Phân tích tổng hợp (Analytics).

</details>

1. **Replication Lag (Stale Reads)**: The #1 bug in Master-Slave architectures. Asynchronous Binlog replication takes time (e.g., `50ms` to `2000ms` under heavy load). A user updates their Avatar. The Write hits the Master. The UI instantly redirects and issues a `GET /profile` which hits the Replica. The Replica hasn't received the binlog yet. It returns the old Avatar. The user thinks the save failed.
   - *The Fix (Read-Your-Own-Writes Consistency)*: The Backend must maintain state. If User A mutates data, the Backend caches a flag (e.g., `just_updated: true`) for 5 seconds. If that flag exists, the Router explicitly bypasses the Replicas and routes User A's reads directly to the Master DB, guaranteeing Strong Consistency for the mutating user while everyone else enjoys Eventual Consistency on the Replicas.
2. **Scatter-Gather (Cross-Shard Query Paralysis)**: Once sharded by `user_id`, retrieving data for a specific user (`WHERE user_id = X`) is $O(1)$ and perfectly isolated to one node. However, an Admin query like "Find the top 10 most expensive orders globally" is an architectural disaster. You cannot execute an `ORDER BY LIMIT 10` on the DB. You must perform a **Scatter-Gather**. The App Server queries ALL 10 Shards simultaneously, pulls the top 10 from *each*, loads 100 heavy rows into local Node.js RAM, and executes a manual Javascript `Array.sort()`. It is brutally inefficient.

---

## Related Topics

- For solving the Master/Slave sync delay, read about **[Eventual Consistency](../consistency/overview.md)**.
- For moving these DBs into different domains entirely, see **[Microservices](../../10-system-design/architecture-patterns/microservices.md)**.
- For a pattern that splits DBs structurally, see **[CQRS](../event-driven/cqrs.md)**.
