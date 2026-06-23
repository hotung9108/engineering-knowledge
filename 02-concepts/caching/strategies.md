# Caching Strategies

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Bạn đã biết Cache là gì, nhưng khi code thực tế, bạn sẽ lấy dữ liệu từ Cache hay từ DB trước? Khi có dữ liệu mới, bạn ghi vào Cache trước hay DB trước? **Caching Strategies (Chiến lược bộ đệm)** là các mẫu thiết kế (Design Patterns) giúp lập trình viên trả lời câu hỏi đó. Có 4 chiến lược kinh điển: Cache-Aside (Phổ biến nhất), Read-Through, Write-Through và Write-Behind.

</details>

> **Summary**: While integrating a cache layer (like Redis) significantly improves performance, the architectural challenge lies in data synchronization. Should the application query the cache or the database first? During a data update, which storage layer is written to first? **Caching Strategies** are established design patterns that dictate the interaction flow between the Application, the Cache, and the primary Database. The four foundational strategies are: Cache-Aside (the industry standard), Read-Through, Write-Through, and Write-Behind.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn là Nhân viên Bán hàng (Application), bạn có một cuốn Sổ tay nhỏ trên bàn (Cache) và một Kho chứa hàng khổng lồ dưới hầm (Database).
1. **Cache-Aside (Tự túc)**: Khách hỏi mua hàng. Bạn tự lật Sổ tay xem trước. Nếu không có, bạn tự chạy xuống hầm lấy hàng, rồi tự ghi thông tin món hàng đó vào Sổ tay để lần sau nhớ.
2. **Read-Through / Write-Through (Nhờ Quản lý)**: Bạn quá lười. Bạn ném việc cho ông Quản Lý Kho (Cache Provider). Khách hỏi, bạn cứ đòi ông Quản Lý. Nếu Sổ tay ổng không có, ổng tự chạy xuống hầm lấy rồi tự ghi vào Sổ tay, bạn chả cần làm gì. Khi nhập hàng mới, bạn cũng đưa cho ổng, ổng tự cập nhật Sổ tay rồi mang xuống hầm cất.
3. **Write-Behind (Làm biếng)**: Khi nhập hàng mới, bạn chỉ ghi vào Sổ tay rồi báo "Xong!". Đợi cuối ngày, khi rảnh rỗi, ông Quản lý mới vác một đống hàng xuống hầm cất một lượt.

</details>

Imagine you are a Cashier (Application), you have a small Notepad on your desk (Cache), and a massive Warehouse downstairs (Database).
1. **Cache-Aside**: A customer asks for an item. You physically check your Notepad. If it's missing, you walk to the Warehouse, find the item, and then explicitly write the item's details in your Notepad for next time.
2. **Read-Through / Write-Through**: You delegate the work. The Notepad is magically linked to the Warehouse via a Manager. You just ask the Manager for the item. If the Notepad lacks it, the Manager fetches it from the Warehouse and updates the Notepad automatically. When updating stock, you update the Manager, and the Manager immediately updates both the Notepad and the Warehouse.
3. **Write-Behind (Write-Back)**: When updating stock, you tell the Manager. The Manager writes it in the Notepad and instantly says "Done!" to the customer. He doesn't go to the Warehouse. Instead, at the end of the day, he takes all the accumulated updates and pushes them to the Warehouse in one large batch.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Cache-Aside (Lazy Loading)**
- Phổ biến nhất. Ứng dụng phải tự code logic giao tiếp với cả Cache và DB.
- Đọc: App hỏi Cache $\rightarrow$ Miss $\rightarrow$ App hỏi DB $\rightarrow$ App lưu vào Cache.

**2. Read-Through / Write-Through**
- Cache được đặt ngay "phía trước" DB như một cánh cửa. App chỉ biết nói chuyện với Cache, không bao giờ đụng tới DB.
- Cần một thư viện trung gian (Cache Provider) để tự động đồng bộ từ Cache xuống DB. Dữ liệu luôn an toàn và đồng nhất.

**3. Write-Behind (Write-Back)**
- App ghi thẳng vào Cache và lập tức trả về `200 OK` cho người dùng (Cực nhanh).
- Cache sẽ tự động gom các bản ghi lại (Batching) và ghi từ từ xuống DB dưới background (bất đồng bộ).

</details>

**1. Cache-Aside (Lazy Loading)**
The most ubiquitous strategy. The Application explicitly orchestrates communication between the Cache and the Database. The Cache and DB do not talk to each other.
- *Read Flow*: App queries Cache $\rightarrow$ (Miss) $\rightarrow$ App queries DB $\rightarrow$ App explicitly writes the result to the Cache.

**2. Read-Through / Write-Through**
The Cache sits inline, acting as a transparent proxy to the Database. The Application treats the Cache as the absolute main data store.
- *Flow*: The Application issues reads/writes to the Cache Provider. The Cache Provider synchronously fetches from or writes to the underlying Database. Ensures absolute data consistency.

**3. Write-Behind (Write-Back)**
Optimized for write-heavy workloads.
- *Flow*: The Application writes data to the Cache. The Cache immediately acknowledges success to the Application. Asynchronously, a background worker batches the changes and periodically flushes them to the persistent Database.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Mỗi chiến lược giải quyết một bài toán cụ thể:
- **Tại sao dùng Cache-Aside?** Dễ cài đặt nhất. Redis và PostgreSQL là 2 công nghệ khác nhau, việc viết code kết nối chúng ở tầng Application (Backend) là đơn giản nhất.
- **Tại sao dùng Write-Through?** Khi bạn có hệ thống Cập nhật Hồ sơ y tế, bạn không thể để Cache báo thành công mà DB chưa lưu. Bắt buộc phải ghi xong cả 2 nơi mới được báo thành công. Đảm bảo tính nhất quán tuyệt đối.
- **Tại sao dùng Write-Behind?** Bạn làm game online, người chơi liên tục nhặt được Vàng (1 giây nhặt 10 lần). Nếu cứ chọc vào DB 10 lần/giây thì DB sẽ nổ. Ta dùng Write-Behind để cộng Vàng vào RAM cực nhanh, rồi 5 phút sau mới lưu tổng số Vàng đó xuống DB một lần.

</details>

Each strategy is engineered to optimize a specific architectural constraint:
- **Why Cache-Aside?** Simplicity and architectural decoupling. Redis and PostgreSQL are entirely separate technologies. Implementing the coordination logic inside the Application layer (e.g., in NodeJS or Java) requires zero specialized middleware.
- **Why Write-Through?** Strict Data Consistency. In financial or healthcare systems, acknowledging a write as "Successful" before it is persistently committed to disk is catastrophic. Write-Through guarantees that the Cache and DB are always perfectly synchronized, at the cost of higher write latency.
- **Why Write-Behind?** Extreme Write Throughput. In massive multiplayer games or high-frequency IoT telemetry, devices might emit 10,000 updates per second. Sending these raw writes directly to a relational DB will cause immediate I/O exhaustion. Write-Behind absorbs the barrage in RAM, coalesces the writes, and flushes them to disk efficiently.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh ưu nhược điểm của các chiến lược ghi.
</details>

Visualizing the trade-offs of Write Operations.

| Strategy | Write Latency | Data Consistency | Risk of Data Loss | Use Case |
|---|---|---|---|---|
| **Write-Through** | **High** (Must wait for both Cache and DB IO) | **Perfect** (Always synchronized) | **Zero** | Banking, E-commerce Checkout |
| **Write-Behind** | **Zero** (Returns instantly after RAM write) | **Eventual** (DB is updated later) | **High** (If Cache crashes before flush) | Gaming, View Counters, IoT |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Cache-Aside**: Phù hợp cho **90% dự án web**. Dùng cho những dữ liệu "Đọc nhiều, Ghi ít" (Read-heavy) như: Bảng xếp hạng, Danh sách sản phẩm, Trang chủ tin tức. 
- **Read-Through**: Thường được dùng gián tiếp thông qua các ORM (như Hibernate L2 Cache của Java) hoặc AWS DynamoDB DAX. Lập trình viên không cần tự viết code Cache-Aside nữa.
- **Write-Behind (Write-Back)**: Lượt xem (View Count) của video YouTube. Không thể cập nhật DB mỗi khi có 1 người xem. YouTube cộng dồn lượt xem vào RAM, sau đó vài phút mới batch xuống DB một lần (đó là lý do đôi khi view bị đứng im ở 301).

</details>

- **Cache-Aside**: The universal standard for **Read-Heavy** applications. Extensively utilized for caching API responses, User Profiles, E-commerce catalogs, and dynamic HTML templates. It is resilient; if the Cache cluster fails, the application gracefully degrades to querying the Database directly.
- **Read-Through**: Commonly implemented via Object-Relational Mappers (ORMs) like Hibernate (Java) Second-Level Cache, or fully managed cloud solutions like AWS DynamoDB Accelerator (DAX). It simplifies the application codebase significantly.
- **Write-Behind (Write-Back)**: High-frequency Counters. A YouTube video view counter cannot execute `UPDATE views SET count = count + 1` directly on a relational database for 100,000 concurrent viewers. The system increments the counter in Redis (Write-Behind). A scheduled cron job eventually pulls the aggregate number and updates the persistent database.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khởi động Cache-Aside (Warm-up)**: Khi hệ thống mới bật lên, Cache hoàn toàn trống rỗng (Cold Cache). Nếu lúc này có 10.000 người vào trang chủ, Cache-Aside sẽ bị lủng, toàn bộ request đập thẳng vào DB gây sập. **Cách khắc phục**: Viết một script chạy ngầm khi khởi động App, tự động query DB lấy các dữ liệu Hot nhất và nạp sẵn vào Cache (gọi là Cache Warm-up) trước khi mở cửa cho User vào.
2. **Xử lý Cache Miss**: Trong mô hình Cache-Aside, nếu 1000 người cùng "Miss" một ID sản phẩm ở cùng 1 phần nghìn giây, cả 1000 người sẽ cùng chọc xuống DB lấy data và cùng lưu lại vào Cache (hiện tượng Thundering Herd). **Cách khắc phục**: Dùng kỹ thuật `Mutex Lock` (Khóa phân tán) trên Cache. Người đầu tiên Miss sẽ cầm chìa khóa xuống DB lấy data, 999 người còn lại phải đứng chờ 50ms cho đến khi người đầu tiên lưu xong vào Cache.

</details>

1. **Mandatory Cache Warm-Up**: When deploying a new cache cluster, it starts entirely empty (Cold Cache). In a Cache-Aside architecture, a sudden traffic spike at this exact moment causes a 100% Cache Miss rate, channeling the entire traffic tsunami directly into the fragile Database (a Cold Start Disaster). **Fix**: Implement an automated Cache Warm-Up script during the deployment pipeline. The script proactively queries the Database for the top 1000 most accessed records and pre-populates the Cache *before* routing actual user traffic to the instance.
2. **Mitigating the Thundering Herd Problem**: In Cache-Aside, if a highly popular key (e.g., trending news article) suddenly expires, 10,000 concurrent requests will experience a Cache Miss simultaneously. All 10,000 threads will independently query the Database and attempt to write to the cache. **Fix**: Implement a **Distributed Mutex Lock** (e.g., using Redis `SETNX`). When a Cache Miss occurs, the thread attempts to acquire the lock. Only the *one* thread that acquires the lock is permitted to query the Database. The other 9,999 threads sleep for 50ms and retry the cache, eventually hitting the freshly populated data.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Áp dụng Write-Behind sai chỗ**: Dùng Write-Behind cho Hệ thống Thanh toán Ngân hàng. Ghi giao dịch chuyển tiền vào RAM, báo khách hàng "Chuyển thành công". 1 giây sau Server cúp điện. RAM bị xóa. Khách hàng mất tiền nhưng DB chưa kịp ghi nhận. (Cực kỳ thảm họa).
2. **Quên xóa Cache khi Cập nhật DB (Data Stale)**: Trong mô hình Cache-Aside, bạn cập nhật Giá Sản phẩm trong Database từ 100k lên 200k, nhưng quên viết code ra lệnh cho Redis xóa cái giá cũ đi. Khách hàng vẫn nhìn thấy giá 100k trên web cho đến khi TTL hết hạn.

</details>

1. **Misapplying Write-Behind for Critical Data**: Architecting a Financial Transaction ledger using Write-Behind. A user deposits $500. The system writes to RAM and returns a `200 OK` success message. One second later, a kernel panic reboots the Cache server before the background job flushes the data to disk. The money is permanently obliterated from existence. **Absolute Rule**: Never use Write-Behind for financially or legally binding transactions.
2. **Orphaned Stale Data in Cache-Aside**: A developer updates a product's price from $10 to $20 in the Database via a direct SQL query, but entirely forgets to explicitly evict the corresponding key from the Redis cluster. Because Cache-Aside does not synchronize automatically, customers continue to see the $10 price on the frontend until the TTL naturally expires. This is the root cause of 99% of "The website is showing old data" bug reports.

---

## Related Topics

- For the foundational concepts, see **[Caching Overview](./overview.md)**.
- To solve the Stale Data problem mentioned above, study **[Cache Invalidation](./invalidation.md)**.
- For architectural deployment, see **[Distributed Caching](./distributed.md)**.
