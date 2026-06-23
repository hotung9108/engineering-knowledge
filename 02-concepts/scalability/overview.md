# Scalability Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Scalability (Khả năng mở rộng) là năng lực của một hệ thống có thể xử lý lượng công việc tăng lên một cách mượt mà bằng cách đắp thêm tài nguyên, thay vì bị sụp đổ. Một website thiết kế tồi có thể chạy rất mượt với 100 người dùng, nhưng sập ngay lập tức khi có 1.000 người, và dù bạn có mua Server xịn gấp 10 lần thì nó vẫn sập. Khả năng mở rộng tốt nghĩa là: Khách tăng x10 $\rightarrow$ Trả tiền mua thêm Server x10 $\rightarrow$ Hệ thống vẫn chạy ngon lành, không cần đập đi viết lại code.

</details>

> **Summary**: **Scalability** is the architectural property of a system that allows it to gracefully handle increasing amounts of work, or its potential to be enlarged to accommodate that growth, purely by adding hardware resources without requiring significant codebase rewrites. A poorly designed architecture might function flawlessly with 100 concurrent users but will instantly crash at 10,000, and throwing 10x more RAM at it will not solve the structural bottlenecks. A highly scalable system guarantees that throughput increases linearly in direct proportion to the physical resources added to it.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn bán Bánh Mì.
1. **Thiếu khả năng mở rộng (Unscalable)**: Quán của bạn chỉ có đúng 1 cái cửa ra vào bé xíu và 1 người thu ngân. Nếu 10 khách đến, bán bình thường. Nếu 1.000 khách đến cùng lúc, họ chen chúc tắc nghẽn ở cửa. Giải pháp: Mua một cái lò nướng siêu to khổng lồ (Nâng cấp phần cứng). Nhưng khách vẫn bị kẹt ở cửa và tốc độ thu tiền vẫn chậm. Bạn phá sản.
2. **Có khả năng mở rộng (Scalable)**: Quán của bạn đập bỏ tường vách kính, mở ra không gian ngoài trời. Cứ thêm 100 khách, bạn lại thuê thêm 1 nhân viên thu ngân và kê thêm 1 cái bàn nướng bánh. 1.000 khách thì thuê 10 người. Mọi người tự do phân tán ra 10 quầy. Hệ thống hoạt động trơn tru.

</details>

Imagine you operate a Toll Booth on a highway.
1. **Unscalable**: You have exactly 1 lane and 1 toll collector. It handles 10 cars per minute perfectly. Suddenly, 500 cars per minute arrive. A massive traffic jam forms. Your "Fix" is to give the toll collector a faster computer and a highly caffeinated energy drink (Upgrading hardware). It barely helps. The single lane is the structural bottleneck.
2. **Scalable**: You redesign the plaza. When traffic increases, you dynamically pave 9 new lanes and hire 9 new toll collectors. Traffic distributes evenly across all 10 lanes. The throughput perfectly matches the hardware (lanes) you added.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 2 phương pháp mở rộng cốt lõi:
1. **Vertical Scaling (Mở rộng theo Chiều Dọc - Scale Up)**: Mua máy xịn hơn. Đang dùng RAM 8GB nâng lên 64GB, thay CPU từ 4 lõi lên 32 lõi. Dễ nhất, không phải sửa 1 dòng code nào. Nhưng có "Trần vật lý" (Không có máy nào RAM 1000TB) và rất đắt tiền.
2. **Horizontal Scaling (Mở rộng theo Chiều Ngang - Scale Out)**: Mua nhiều máy tính. Đang có 1 máy, mua thêm 10 cái máy cấu hình bình thường rồi kết nối chúng lại thành một cụm (Cluster). Rẻ, không có giới hạn trần, nhưng code phải thiết kế cực kỳ phức tạp (Xử lý Stateless, Phân tán dữ liệu).

</details>

There are two fundamental paradigms of scaling:
1. **Vertical Scaling (Scale Up)**: Upgrading the raw capacity of a single physical or virtual machine. Replacing a 16GB RAM / 4-core CPU server with a 256GB RAM / 64-core CPU server. It is incredibly simple (zero code changes required). However, it possesses a hard physical ceiling (supercomputers hit hardware limits) and the cost scales exponentially, not linearly.
2. **Horizontal Scaling (Scale Out)**: Distributing the workload across multiple independent machines. Instead of one 64-core server, you deploy 16 cheap 4-core servers behind a Load Balancer. It provides theoretically infinite scalability and fault tolerance. However, the software architecture MUST be explicitly designed for it (Statelessness, Distributed Caching, Sharded Databases).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao không code bừa đi rồi lúc nào đông khách thì Scale?
Vì kiến trúc phần mềm quyết định việc bạn CÓ THỂ Scale được hay không.
Ví dụ: Bạn lưu thông tin Đăng nhập (Session) vào bộ nhớ RAM của Server (Local State). Khi 10.000 khách vào, bạn mua thêm Server số 2. Load Balancer ném ông khách A sang Server 2. Server 2 không có RAM của Server 1, lập tức báo "Vui lòng đăng nhập lại". Bạn hoàn toàn **Bị khóa chặt (Vendor Lock-in)** vào mô hình 1 Server. Bạn không thể Horizontal Scale được trừ khi bạn đập đi code lại hệ thống Session bằng Redis. Scalability tồn tại để nhắc nhở Dev phải code các ứng dụng "Không Trạng Thái" (Stateless) ngay từ ngày đầu tiên.

</details>

Why can't we simply write bad code and throw hardware at it later?
Because unscalable software architecture imposes **Hard Structural Ceilings**.
Consider Stateful Session Management. A developer stores User Login Sessions directly inside the NodeJS RAM (Local State). Traffic spikes, so DevOps spins up Server #2 and adds a Load Balancer. User A logs into Server #1. On their next click, the Load Balancer routes them to Server #2. Server #2 has empty RAM, so it forces User A back to the Login screen. The architectural design fundamentally prohibits Horizontal Scaling. The system is fatally constrained to a single node. Scalability exists as an engineering discipline to enforce **Stateless Architecture (12-Factor Apps)** from Day 1, ensuring hardware can be added effortlessly.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh giới hạn Mở rộng khi Code chuẩn và Code tồi.
</details>

Visualizing the impact of architectural choices on limits.

| Architectural Choice | Scalability Limit | The Bottleneck |
|---|---|---|
| **Images saved on Local Disk**| 1 Server (Hard limit) | Server 2 cannot serve images uploaded to Server 1. |
| **Images saved on AWS S3** | Infinite | Decoupled Storage. All servers access S3 universally. |
| **Monolithic SQL Database** | High (Vertical limit) | All writes hit a single Master node (Disk I/O). |
| **Sharded NoSQL Database** | Infinite | Writes are distributed across 100 independent nodes. |
| **Polling for Events** | Low (CPU bound) | Thousands of empty HTTP requests consume thread pools. |
| **Event-Driven Pub/Sub** | Infinite | Asynchronous, non-blocking notification streams. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hành trình Mở rộng của một Startup điển hình:
1. **Level 1 (Mới mở)**: Mọi thứ nhét chung 1 Server (Code, DB, Ảnh). Ngon, bổ, rẻ. Đạt mốc 10.000 User $\rightarrow$ CPU Server báo đỏ.
2. **Level 2 (Tách DB)**: Tách cái Database ra một con Server riêng to bự (Vertical Scaling). Đạt mốc 100.000 User $\rightarrow$ Server Code báo đỏ do quá nhiều Request.
3. **Level 3 (Clone Server)**: Mua 5 con Server Code chạy song song, đặt Load Balancer ở trước. Rút toàn bộ Ảnh ra đẩy lên S3. Đạt mốc 1.000.000 User $\rightarrow$ Con Server DB (SQL) duy nhất quá tải, nghẽn mạng toàn hệ thống.
4. **Level 4 (Đập DB)**: Sử dụng Cache (Redis) để chặn bớt Request chọc xuống DB. Cắt nhỏ DB SQL ra thành nhiều cục (Database Sharding), chia cho 10 con Server khác nhau gánh. Hoặc nâng cấp hẳn lên Event-Driven Microservices.

</details>

The evolutionary roadmap of a scaling Startup:
1. **Level 1 (The Monolithic Box)**: App code, Database, and User Uploads live on a single $10/mo DigitalOcean droplet. Extremely cost-effective. Reaches 1,000 DAU (Daily Active Users) $\rightarrow$ CPU spikes.
2. **Level 2 (Decoupling Data)**: The Database is migrated to a dedicated, managed instance (Vertical Scaling the DB). User Uploads are offloaded to an Object Store (AWS S3) and served via CDN. Reaches 100,000 DAU $\rightarrow$ The Application Server begins dropping HTTP requests (Thread starvation).
3. **Level 3 (Horizontal Compute)**: The Application Server is clustered into 10 stateless nodes behind an AWS Application Load Balancer. Reaches 1,000,000 DAU $\rightarrow$ The 10 App nodes effortlessly bombard the single Master Database with SQL queries, melting its CPU (Disk I/O bottleneck).
4. **Level 4 (Data Sharding & Caching)**: Aggressive Distributed Caching (Redis) is deployed to absorb 90% of Read traffic. The SQL Database is horizontally Sharded across 5 distinct clusters based on `user_id`. The architecture is now capable of handling Hyper-Growth.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Stateless (Không trạng thái) tuyệt đối**: Máy chủ Code tuyệt đối không được phép "Nhớ" bất cứ thứ gì trên RAM hay Ổ cứng của chính nó (Session, File tạm, Token). Mọi dữ liệu phải được đẩy ra các dịch vụ lưu trữ bên ngoài (Redis, S3, Database). Khi máy chủ hoàn toàn trắng tinh, bạn có thể nhân bản nó lên 10.000 cái trong nháy mắt.
2. **Thiết kế theo Asynchronous (Bất đồng bộ)**: Mở rộng không chỉ là mua thêm máy, mà là tận dụng tối đa máy đang có. Nếu Khách hàng upload Video, đừng bắt CPU phải đứng chờ Encode video xong mới trả về. Hãy dùng Message Queue. Gửi thông báo "Đã nhận" ngay lập tức, và Encode ngầm dưới Background. Bằng cách này, 1 Server có thể tiếp 1000 khách thay vì chỉ tiếp 10 khách.

</details>

1. **Absolute Statelessness (12-Factor App methodology)**: Application compute nodes must be treated as highly disposable, completely amnesiac processing pipelines. They must never persist Local State to disk or RAM (no file-system uploads, no local user sessions). All state must be structurally offloaded to external backing services (Redis, AWS S3, PostgreSQL). This is the hard prerequisite for Kubernetes Auto-Scaling.
2. **Asynchronous Non-Blocking Processing**: Scalability is not just adding hardware; it's maximizing hardware utilization. If an endpoint generates a PDF report taking 5 seconds, an Apache/Tomcat thread is blocked for 5 seconds. 200 concurrent requests will exhaust the thread pool, paralyzing the server. **Fix**: Shift to an Asynchronous Architecture. The API immediately responds `202 Accepted` and dumps a payload into RabbitMQ. Background Worker nodes process the PDF at their own pace, drastically increasing API throughput per CPU core.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Quá ám ảnh về Tối ưu vi mô (Micro-optimization)**: Ngồi hì hục sửa vòng lặp `for` thành `while` để code chạy nhanh hơn 1 mili-giây, trong khi nguyên nhân thực sự làm web chậm là do không dùng Redis Cache hoặc viết câu SQL thiếu Index. *Luật*: Architecture Scaling (Sửa kiến trúc) luôn luôn mang lại hiệu quả gấp hàng ngàn lần Code Scaling (Sửa thuật toán).
2. **Tối ưu hóa quá sớm (Premature Optimization)**: Bạn mới khởi nghiệp, có 100 khách hàng, nhưng bạn lại đòi dựng hẳn hệ thống Kubernetes Microservices 30 containers với Kafka Event-Driven hệt như Netflix. Bạn tốn 6 tháng để setup hệ thống hạ tầng (Thay vì 1 tuần code Monolithic để ra mắt sản phẩm kiếm tiền). Và vì hệ thống quá phức tạp, bạn không đủ trình độ bảo trì, cuối cùng dự án phá sản. *Luật*: Chừng nào Đau thì mới tìm Thuốc.

</details>

1. **Obsessing over Micro-optimizations**: Junior developers spend days refactoring a Javascript `map()` function into a basic `for-loop` to save 2 milliseconds of CPU time, completely ignoring the fact that the endpoint executes an unindexed SQL query that takes 800 milliseconds of Disk I/O. **Rule**: Architectural scalability (Database Indexing, Distributed Caching, Sharding, CDNs) yields orders of magnitude higher ROI than algorithm micro-optimizations in modern web applications.
2. **Premature Optimization (The Startup Killer)**: A two-person startup building an MVP with zero users decides to mimic Netflix's architecture. They deploy a 40-microservice topology on Kubernetes utilizing Kafka Event Sourcing and CQRS. They spend 6 months fighting Infrastructure-as-Code bugs instead of finding Product-Market Fit. The startup goes bankrupt before launching. **Rule**: Scale is an evolutionary process. Begin with a cleanly modularized Monolith backed by a single SQL database. Solve scaling problems *when* they become actual constraints.

---

## Related Topics

- For how multiple stateless servers share the load, see **[Load Balancing](./load-balancing.md)**.
- For when the database inevitably becomes the bottleneck, see **[Database Scaling](./db-scaling.md)**.
- For artificially protecting the system from spikes, read **[Rate Limiting](./rate-limiting.md)**.
