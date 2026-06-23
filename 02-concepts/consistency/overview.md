# Consistency Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Consistency (Tính Nhất Quán) là thước đo độ "Chính xác và Đồng bộ" của dữ liệu. Nếu bạn có 1 tỷ đồng trong ngân hàng, bạn rút ra 500 triệu. Lúc này, dù bạn dùng App điện thoại, ra máy ATM, hay nhờ nhân viên quầy kiểm tra, thì **TẤT CẢ** đều phải nhìn thấy số dư chính xác là 500 triệu. Nếu App điện thoại báo 500, nhưng máy ATM lại báo 1 tỷ (do máy ATM chưa cập nhật kịp), thì hệ thống của bạn đã bị Bất nhất quán (Inconsistent). Trong hệ thống lớn chạy nhiều máy chủ, đảm bảo mọi máy chủ đều "Nói cùng 1 sự thật" cùng một lúc là điều cực kỳ khó.

</details>

> **Summary**: **Consistency** is a fundamental metric of data integrity and synchronization across a system. In a distributed environment where data is replicated across multiple independent physical nodes, Consistency dictates the mathematical guarantee that a Read operation will return the absolute most recent, correct Write operation. If a user mutates data on Server A, and immediately queries Server B, does Server B return the new data, or the stale old data? Resolving this discrepancy is the central conflict of Distributed Systems engineering. Strict Consistency guarantees absolute correctness but massacres performance.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đổi Mật khẩu Wifi ở nhà.
1. **Strong Consistency (Nhất quán Mạnh)**: Bạn vừa bấm nút "Đổi mật khẩu" trên Cục phát Wifi. NGAY LẬP TỨC, máy tính, điện thoại, TV của bạn và tất cả mọi người trong nhà đều bị ngắt mạng và đòi mật khẩu mới. Mọi thứ đồng bộ hoàn hảo ở cùng 1 giây.
2. **Eventual Consistency (Nhất quán Tạm thời)**: Bạn bấm "Đổi mật khẩu". Điện thoại của bạn thì bị ngắt mạng ngay. Nhưng cái TV ở phòng khách vẫn xài được mạng thêm 5 phút nữa, rồi nó mới bắt đầu bị ngắt và đòi mật khẩu mới. Trong suốt 5 phút đó, Cục Wifi và cái TV "bất đồng quan điểm" với nhau. Nhưng Cuối Cùng (Eventual) thì tụi nó cũng đồng nhất.

</details>

Imagine a Teacher changing the rules of a game in a large schoolyard.
1. **Strong Consistency**: The Teacher blows a whistle. Every single child in the schoolyard instantly freezes, listens to the new rule, and instantly plays by the new rule at the exact same millisecond. Perfect synchronization.
2. **Eventual Consistency**: The Teacher whispers the new rule to two children and tells them to pass it on. For the next 10 minutes, half the schoolyard is playing by the old rules, and half is playing by the new rules. It is chaotic and "inconsistent". However, eventually, the gossip spreads completely, and the entire schoolyard is playing by the new rule.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong thế giới Database, có 3 mức độ Nhất quán chính:
1. **Strong Consistency (Nhất quán Mạnh mẽ)**: Bất kỳ thao tác Đọc nào, ở bất kỳ máy chủ nào, cũng LUÔN LUÔN trả về dữ liệu mới nhất. Nếu chưa cập nhật xong dữ liệu cho tất cả máy chủ, nó sẽ Khóa (Block) không cho ai đọc. Tuyệt đối chính xác, nhưng chạy siêu chậm.
2. **Eventual Consistency (Nhất quán Cuối cùng)**: Chấp nhận việc dữ liệu bị sai lệch hoặc cũ (Stale) trong một khoảng thời gian ngắn (Vài mili-giây hoặc vài giây). Tốc độ cực nhanh vì không phải Khóa ai cả. Đa số các hệ thống như Facebook, Youtube đều dùng cái này.
3. **Read-Your-Own-Writes Consistency**: Mức độ lai tạp rất hay gặp. Khi người dùng A sửa Avatar, chỉ người dùng A là thấy Avatar mới ngay lập tức (Strong). Còn những người dùng khác có thể 5 phút sau mới thấy Avatar của A đổi (Eventual).

</details>

Data Consistency spans a spectrum, primarily categorized into three operational models:
1. **Strong Consistency (Linearizability)**: The absolute gold standard of correctness. It guarantees that once a Write completes, any subsequent Read—regardless of which physical replica node it queries—will unequivocally return that updated value. To achieve this, the system must aggressively lock out all Readers until the Write is perfectly replicated across the cluster. It suffers severe Latency penalties.
2. **Eventual Consistency**: The pragmatic standard for hyperscale Cloud architecture. It guarantees that if no new updates are made to an object, eventually all accesses will return the last updated value. During the propagation window (which could be 50ms or 5 seconds), querying a secondary replica might return stale, outdated data. It provides blistering speed at the cost of transient UI confusion.
3. **Read-Your-Own-Writes (Session Consistency)**: A highly specialized, UX-focused consistency model. It guarantees that a specific Client will *always* see their own immediate Writes, even if they are routed to a stale replica. However, it makes zero guarantees about what *other* clients will see. It perfectly masks Eventual Consistency from the perspective of the mutating user.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao không làm cho mọi thứ Nhất quán Mạnh luôn đi cho dễ lập trình?
Vì **Khoảng cách Địa lý** và **Tốc độ Ánh sáng**.
Bạn có 1 Server ở Việt Nam và 1 Server ở Mỹ (Phải chép dữ liệu qua lại để dự phòng). Tốc độ ánh sáng chạy qua cáp quang dưới biển mất 200ms. 
Nếu bạn chọn Strong Consistency: Khách Việt Nam bấm "Lưu bài viết". Server VN phải gửi tin nhắn qua Mỹ (Đợi Mỹ lưu xong mất 200ms) rồi mới báo cho Khách là "Đã lưu". Khách hàng sẽ phải đợi rất lâu. Nếu cáp biển đứt $\rightarrow$ Server VN đành phải BÁO LỖI luôn vì không kết nối được qua Mỹ. Hệ thống sập.
Do đó, các kỹ sư tạo ra các mức độ Consistency yếu hơn (Như Eventual) để lách luật vật lý, đánh đổi một chút "Độ chính xác" lấy "Tốc độ chớp nhoáng" và "Khả năng sống sót khi đứt cáp".

</details>

Why not engineer every system to simply use Strong Consistency and avoid the headache?
Because of **The Speed of Light** and **Network Partitions**.
Imagine a geographically distributed Database: Master Node in New York, Read Replica in Tokyo. The physical fiber-optic round-trip time (ping) is `200ms`.
If you enforce Strong Consistency, a Write operation in New York MUST synchronously replicate to Tokyo before returning `200 OK` to the user. Every single Write operation is brutally penalized by a `200ms` latency floor. Furthermore, if the trans-pacific cable is severed by an anchor, New York cannot reach Tokyo. Under Strong Consistency rules, the New York Master MUST completely halt and reject all Writes (Downtime) to prevent divergence.
To achieve sub-millisecond latency and 99.999% High Availability, architects are mathematically forced to abandon Strong Consistency in favor of Eventual Consistency.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh trải nghiệm khi bạn Comment vào Video Youtube của chính mình.
</details>

Visualizing UX under different Consistency Models when User A posts a Comment on a Video.

| Metric | Strong Consistency | Eventual Consistency | Read-Your-Own-Writes |
|---|---|---|---|
| **Write Latency** | **Slow** (Waits for global DB replication). | **Instant** (Returns as soon as DB receives it). | **Instant**. |
| **User A's View** | Sees their comment instantly. | Presses F5, comment **disappears**! (Stale read). | Sees their comment instantly. |
| **User B's View** | Sees User A's comment instantly. | Sees User A's comment 2 seconds later. | Sees User A's comment 2 seconds later. |
| **System Availability**| Highly vulnerable to network drops. | **100% Highly Available**. | Highly Available. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Strong Consistency (Hệ thống Tiền tệ)**: Chuyển khoản ngân hàng, Giao dịch Chứng khoán, Mua vé máy bay (Chỉ còn 1 ghế). Ở những nơi này, thà bắt Khách hàng đợi 10 giây hoặc báo "Lỗi mạng", còn hơn là cho phép 2 người cùng book trùng 1 cái ghế hoặc tiền bị nhân đôi. (Dùng SQL Database, 2PC, Raft).
2. **Eventual Consistency (Mạng xã hội / E-commerce)**: Lượt Like của Facebook, Số người đang xem Livestream, Tên bài viết Blog. Bạn Like bài viết, nếu người khác chưa thấy ngay cũng chả chết ai. Cứ làm cho web chạy mượt trước đã. (Dùng NoSQL, Redis, Kafka, CQRS).

</details>

1. **Strong Consistency Domains (Financial/Inventory)**: Core Banking ledgers, Stock Market Trading platforms, and Airline Seat booking engines. In these domains, stale data causes catastrophic financial or legal liability (e.g., Double-spending, or selling the exact same Airplane seat to two different people). Architects explicitly trade Latency and Availability to strictly enforce ACID isolation and Strong Consistency via Relational Databases and Quorum reads.
2. **Eventual Consistency Domains (Social/Analytics/IoT)**: The Facebook "Like" counter, YouTube View Counts, Instagram Feeds, and massive IoT sensor ingestion pipelines. If a YouTube video goes viral, it does not matter if User A sees `1,005,000` views while User B concurrently sees `1,004,800` views. The business value demands 0ms latency and 100% uptime; perfect synchronization is entirely irrelevant.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giấu đi sự "Eventual" bằng Front-end (Optimistic UI)**: Khi dùng Eventual Consistency, dữ liệu sẽ bị trễ. Khách hàng xóa 1 tấm ảnh, 3 giây sau Backend mới xóa xong. Đừng bắt khách hàng nhìn tấm ảnh đó 3 giây. Ở Front-end, hãy viết code Javascript ẨN tấm ảnh đó ngay lập tức (Che mắt người dùng). Dù ngầm bên dưới Backend vẫn đang loay hoay xóa.
2. **Chọn đúng loại Database**: Đừng cố ép MongoDB hay Cassandra chạy Strong Consistency (Sẽ rất chậm và phi lý). Cũng đừng ép PostgreSQL chạy Eventual Consistency. Việc chọn cấu trúc dữ liệu ban đầu sẽ định hình toàn bộ tư duy Consistency của bạn.

</details>

1. **Masking Eventual Consistency via Optimistic UI**: The ultimate developer trick. Eventual Consistency introduces a 2-second propagation delay. If a user clicks "Delete Post", and the UI executes a standard synchronous reload, the Read Replica will return stale data, and the deleted post will mysteriously reappear on the screen, horrifying the user. **The Fix**: The Frontend must implement Optimistic Updates. Upon clicking "Delete", the JS framework instantly mutates the local DOM, removing the post from the screen *assuming* the backend will eventually succeed. The user experiences zero latency, entirely oblivious to the backend synchronization chaos.
2. **Aligning the Data Store to the Constraint**: Do not fight the inherent architecture of your Database. Apache Cassandra and Amazon DynamoDB are specifically engineered, from the ground up, to be Highly Available, AP (Eventual Consistency) systems. Forcing them to execute Quorum-based Strongly Consistent reads violently degrades their performance. Conversely, PostgreSQL is natively an ACID, CP (Strong Consistency) engine. Match the physical Data Store to the Business Domain's consistency requirements.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Không biết mình đang xài Eventual Consistency**: Sai lầm kinh điển của Junior. Trong hệ thống có Master-Slave Database. Thằng Junior viết 1 API: Dòng 1 `Insert` User vào DB. Dòng 2 `Select` cái User đó ra để trả về cho Front-end. Chạy ở Localhost cực mượt. Lên Production, dòng 1 ghi vào Master, dòng 2 lại đi đọc ở Slave. Do Slave chưa kịp đồng bộ (Mất 50ms), dòng 2 báo lỗi "Không tìm thấy User". Thằng Junior vò đầu bứt tai không hiểu tại sao.
   - *Luật*: Khi đã xài Replicas, phải luôn ý thức được độ trễ (Replication Lag).
2. **Sự ám ảnh "Mọi thứ phải hoàn hảo"**: Giám đốc bắt Lập trình viên: "Số lượng Like của bài viết phải cập nhật chính xác 100% ngay lập tức cho tất cả mọi người". Lập trình viên cắm đầu đi viết hệ thống Khóa (Lock) Database phức tạp. Kết quả web sập vì nghẽn. Thay vào đó, Lập trình viên phải có khả năng thuyết phục Giám đốc: "Sếp ơi, số Like trễ 2 giây chả ảnh hưởng đến doanh thu đâu, bỏ qua đi".

</details>

1. **Replication Lag Ignorance (The Read-After-Write Bug)**: The most prevalent bug encountered by Junior Engineers transitioning to distributed architectures. They write an API: Line 1 executes an `INSERT` (which routes to the Master DB). Line 2 executes a `SELECT` to fetch the auto-generated ID (which routes to the Read Replica). Locally, with zero latency, it passes Unit Tests. On Production, under load, Binlog replication takes 100ms. Line 2 executes at 5ms, querying a Replica that hasn't received the data yet. It returns `NullPointerException`. **The Fix**: Engineers must strictly enforce *Read-Your-Own-Writes* logic (routing immediate subsequent reads directly to the Master).
2. **Over-Engineering Strong Consistency (The Perfection Trap)**: Non-technical Product Managers will always instinctively demand "100% Real-time Perfect Accuracy" for trivial features (like a Social Media View Counter). An inexperienced architect will obey, implementing brutal Distributed Locks and Quorum reads, suffocating the database throughput. A Senior Architect negotiates the constraint. They mathematically prove to the Business that eventual consistency saves $50,000/month in server costs and provides a 5x faster UX, explicitly trading theoretical perfection for pragmatic scalability.

---

## Related Topics

- For the mathematical theorem that proves this is a real problem, read **[CAP Theorem](./cap-theorem.md)**.
- For how DBs split the concept of Consistency vs Availability, read **[ACID vs BASE](./acid-vs-base.md)**.
- For patterns that force you into Eventual Consistency, see **[Saga Pattern](../event-driven/saga.md)** or **[CQRS](../event-driven/cqrs.md)**.
