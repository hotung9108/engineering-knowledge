# Bulkhead Pattern

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Thuật ngữ "Bulkhead" bắt nguồn từ ngành đóng tàu. Đáy tàu biển được chia thành nhiều khoang nhỏ bằng các vách ngăn bằng thép (Bulkhead). Nếu tàu đâm vào đá làm thủng 1 khoang, nước chỉ ngập đúng khoang đó, các khoang khác vẫn khô ráo, giúp tàu không bị chìm. Trong phần mềm, **Bulkhead Pattern** là việc cô lập (Cách ly) tài nguyên (như RAM, CPU, Thread) cho từng tính năng riêng biệt. Nếu tính năng "Upload Ảnh" bị kẹt và ngốn hết CPU của phần được cấp, nó sẽ không thể "ăn lẹm" sang phần CPU của tính năng "Đăng nhập", giúp ứng dụng của bạn không bao giờ chết chùm.

</details>

> **Summary**: The **Bulkhead Pattern** is an architectural concept borrowed directly from naval engineering, where a ship's hull is divided into strictly sealed, watertight compartments (bulkheads) to prevent a localized breach from flooding the entire vessel. In software resilience, a Bulkhead isolates system resources (Connection Pools, CPU Threads, Memory allocations) into distinct pools allocated per functional area or per downstream dependency. If one downstream API goes catastrophic and begins hanging, it will perfectly exhaust its dedicated thread pool, but it is physically prevented from cannibalizing the threads assigned to other, healthy APIs. This explicitly prevents cascading failure through Resource Exhaustion.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một ngân hàng có 10 quầy giao dịch và 10 nhân viên.
1. **Không có Bulkhead**: Một ngày nọ có 10 người đến làm thủ tục Vay Vốn (Cực kỳ lâu, tốn 2 tiếng). Cả 10 nhân viên đều bận tiếp 10 người này. Lúc này, có 50 khách hàng khác đến chỉ để Rút tiền (Mất 2 phút), nhưng họ cũng phải đứng ngoài cửa chờ vì không còn nhân viên nào rảnh. (Tính năng Vay Vốn đã "ăn cắp" toàn bộ nhân sự của tính năng Rút tiền).
2. **Có Bulkhead**: Giám đốc chia ranh giới rõ ràng: 2 quầy chuyên làm Vay Vốn, 8 quầy chuyên Rút tiền. Hôm nay có 10 người đến Vay Vốn. Họ phải xếp hàng chờ ở 2 cái quầy Vay Vốn. 8 quầy Rút tiền vẫn hoạt động với tốc độ bàn thờ và phục vụ 50 người kia một cách mượt mà. 

</details>

Imagine a Bank with 10 tellers.
1. **Without Bulkheads (Shared Pool)**: 10 customers walk in and demand complex Mortgage applications (Takes 2 hours each). All 10 tellers are now occupied. Suddenly, 50 normal customers walk in to deposit a check (Takes 1 minute each). They cannot be served. They must wait 2 hours. The complex Mortgage feature has completely starved the quick Deposit feature of resources.
2. **With Bulkheads (Isolated Pools)**: The Bank Manager enforces strict limits: Maximum 2 tellers are allowed to handle Mortgages. The other 8 tellers strictly handle standard Deposits. When the 10 Mortgage customers arrive, they fill up the 2 Mortgage tellers, and 8 of them sit in the waiting room. Meanwhile, the 8 Deposit tellers easily blast through the 50 standard customers. The slow feature is strictly contained.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bulkhead có 2 kiểu triển khai phổ biến trong Code:
1. **Thread Pool Bulkhead (Tách luồng xử lý)**: Server của bạn có 100 luồng (Threads) để xử lý Request. Bạn chia: Cấp 20 Threads cho API Đăng nhập, cấp 50 Threads cho API Mua hàng, cấp 30 Threads cho API Xuất báo cáo. Nếu hàm Xuất báo cáo bị lỗi lặp vô hạn, nó sẽ nuốt sạch 30 Threads của nó và báo lỗi (Cháy 1 khoang). Nhưng API Đăng nhập và Mua hàng (70 Threads kia) vẫn chạy trơn tru không hề hấn gì.
2. **Semaphore Bulkhead (Cấp thẻ bài)**: Không cần tách Thread. Bạn cứ xài chung 100 Threads. Nhưng bạn đặt luật: "Chỉ cho phép tối đa 10 người cùng lúc thực hiện hành động Upload File". Bất cứ ai thực hiện hành động Upload sẽ phải bốc 1 Thẻ bài. Hết 10 thẻ bài thì người thứ 11 sẽ bị từ chối ngay lập tức (Fast Fail), để dành 90 Threads còn lại làm việc khác.

</details>

There are two primary paradigms for implementing Software Bulkheads:
1. **Thread Pool Isolation**: The application explicitly allocates dedicated, independent OS Thread Pools for different outbound dependencies. For example, your `OrderService` communicates with the `PaymentService` (Allocated 20 threads) and the `ReviewService` (Allocated 10 threads). If the `ReviewService` completely hangs, its 10 threads will block and exhaust. However, it cannot borrow threads from the `PaymentService`. Core checkout flows remain 100% operational.
2. **Semaphore Isolation**: Instead of physically segregating OS threads (which incurs heavy Context Switching overhead), you utilize a single application thread pool but restrict concurrency using Semaphores (Virtual tokens). If the limit for calling `LegacyAPI` is 5, you instantiate a Semaphore of 5. The thread must acquire a token before making the call. If 5 tokens are acquired, the 6th thread is immediately rejected (Fast Fail), preserving the primary thread pool.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Một hệ thống bình thường luôn dùng một "Bể kết nối chung" (Shared Thread Pool). Tomcat mặc định có 200 Threads. Node.js dùng chung 1 Event Loop.
Lỗi phần mềm thường không làm sập máy tính ngay. Lỗi phần mềm thường làm MÁY TÍNH BỊ CHẬM LẠI (Ví dụ: một câu lệnh SQL thiếu Index làm mất 10 giây để chạy thay vì 10 mili-giây).
Sự "chậm lại" này cực kỳ độc hại. Nó hoạt động như một con Ký Sinh Trùng. Khi tính năng A bị chậm, các Request chọc vào tính năng A sẽ sống dai hơn bình thường, dần dần "bám rễ" và nuốt sạch toàn bộ 200 Threads của máy chủ. Lúc này máy chủ cạn kiệt Threads, nó sẽ từ chối phục vụ cả tính năng B, C, D (Dù B, C, D không hề bị lỗi). Bulkhead sinh ra để nhốt con Ký Sinh Trùng đó vào một chiếc lồng chật hẹp, để nó chết đói ở trong đó.

</details>

Default application server configurations (Tomcat, Kestrel, Node.js) utilize a **Global Shared Thread Pool**. This is highly efficient for normal operations but architecturally fatal during localized latency spikes.
Software failures rarely manifest as instantaneous hard crashes; they manifest as **Latency Degradation**. An unindexed database query causes the `/search` endpoint to degrade from `10ms` to `10,000ms`.
This latency acts as a systemic parasite. Because requests are taking 1,000 times longer to complete, they hold onto their threads 1,000 times longer. Within seconds, the `/search` endpoint will consume all 200 threads in the global Tomcat pool. The `/checkout` endpoint, which is perfectly healthy, now throws `503 Service Unavailable` because it cannot acquire a single thread. The Bulkhead exists to strictly quarantine this parasitic latency degradation.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh khi tính năng "In hóa đơn PDF" (Cực nặng) bị dội dồn dập vào máy chủ 100 luồng (Threads).
</details>

Visualizing Thread Exhaustion during an asymmetric attack on the "PDF Generation" endpoint.

| Metric | Monolithic Shared Pool (100 Threads) | Bulkhead Pattern (PDF limited to 10 Threads) |
|---|---|---|
| **Attack Vector** | 500 users click "Generate PDF". | 500 users click "Generate PDF". |
| **Thread Allocation**| PDF claims all 100 threads instantly. | PDF claims its maximum 10 threads. |
| **Remaining Load** | 400 requests sit in the OS waiting queue. | 490 PDF requests are instantly rejected (`503`). |
| **Other Features** | `/login` and `/checkout` completely fail. | `/login` perfectly uses the remaining 90 threads. |
| **System State** | System-wide Cascading Failure. | Localized feature failure. Core system survives. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giới hạn số lượng Kết nối Database (Connection Pooling)**: Ứng dụng của bạn có cái bồn chứa 50 kết nối (Connection) tới CSDL. Thay vì cho phép mọi tính năng dùng tự do. Bạn cấu hình: Tính năng "Đọc bài viết" chỉ được xài tối đa 10 kết nối, chừa lại 40 kết nối cho các tính năng "Viết bài" hoặc "Thanh toán".
2. **Phân vùng Microservices bằng Pod (Kubernetes)**: Thay vì gộp chung, ta tạo riêng biệt: 3 Pod chuyên để phục vụ Frontend UI, 10 Pod chuyên để xử lý Background Job (Gửi email). Dù hệ thống Gửi Email bị lỗi vòng lặp làm CPU tăng 100% thì cụm Frontend UI vẫn mượt mà. Đây là Bulkhead ở cấp độ Hạ tầng mạng.
3. **Netflix Hystrix / Resilience4j**: Các thư viện này được Netflix tạo ra để bọc các hàm gọi API. Khi bạn gọi API X, thư viện này tự động tạo một Semaphore bằng 10, đảm bảo rằng trong cùng 1 lúc không có quá 10 request đang chạy lệnh gọi API X đó.

</details>

1. **Database Connection Pooling**: A hidden form of Bulkheading. If your application has a maximum HikariCP pool of 50 Database Connections, a single complex Analytics query triggered by 50 users simultaneously can drain the entire pool, locking the OLTP transactional database completely. Advanced architectures deploy explicitly isolated Connection Pools (e.g., `Pool-Read-Fast`, `Pool-Write`, `Pool-Analytics-Slow`) to enforce physical bulkheads against database starvation.
2. **Kubernetes Node/Pod Segregation**: Architectural bulkheads. Instead of running background workers and frontend web servers on the same K8s Nodes, DevOps will taint nodes and use `nodeAffinity` to strictly isolate workloads. If a memory-leaking Video Transcoding Pod triggers an OS-level Out-Of-Memory (OOM) panic, it only crashes the "Worker" node pool. The "Web" node pool remains perfectly insulated.
3. **Library-Level RPC Protection (Resilience4j)**: When integrating with slow Legacy SOAP APIs, developers wrap the outbound HTTP client with a Resilience4j Bulkhead annotation (`maxConcurrentCalls = 5`). This guarantees that regardless of incoming traffic spikes, the application will only ever risk 5 concurrent threads when interacting with the brittle legacy system.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Kết hợp Bulkhead với Circuit Breaker**: Đây là bộ đôi hủy diệt. Bulkhead giúp cách ly lỗi (Không cho nó lây lan). Circuit Breaker giúp chém đứt lỗi đó (Không cho nó chạy nữa). Nếu chỉ có Bulkhead, 10 Threads của Bulkhead đó vẫn sẽ bị treo mãi mãi. Nếu kết hợp Circuit Breaker, 10 Threads đó sẽ được giải phóng ngay lập tức.
2. **Giám sát (Monitoring) độ kín của vách ngăn**: Bạn cấp 10 Threads cho tính năng B. Bạn làm sao biết 10 là thiếu hay đủ? Bắt buộc phải gắn công cụ theo dõi (Prometheus / Grafana). Nếu thấy biểu đồ báo 10 Threads này lúc nào cũng bị xài hết 100% (Từ chối khách hàng vô cớ), bạn phải điều chỉnh tăng lên thành 20. Tham số Bulkhead không được Code Cứng (Hardcode).

</details>

1. **The Holy Trinity (Bulkheads + Circuit Breakers + Timeouts)**: A Bulkhead is purely a containment strategy; it is not a recovery strategy. If you allocate a 10-thread Bulkhead to a downstream service, and that service hangs indefinitely, all 10 threads will permanently lock. The Bulkhead is full and useless. You **MUST** pair it with Timeouts (to forcefully kill the hanging thread after 2 seconds) and a Circuit Breaker (to instantly reject subsequent calls, keeping the 10 threads completely free).
2. **Dynamic Configuration & Observability**: Hardcoding `ThreadPoolSize = 20` in your Java code is an anti-pattern. Workload profiles change as the application scales. You must emit JMX or Prometheus metrics for `Bulkhead.AvailableConcurrentCalls`. If your Grafana dashboard shows that a Bulkhead is frequently hitting 100% saturation and artificially rejecting valid requests while the rest of the server is at 5% CPU, your Bulkhead is misconfigured. Use a Configuration Server (Consul) to tune the limits dynamically.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lạm dụng Thread Pool (Tạo quá nhiều Vách ngăn)**: Thấy hay quá, Lập trình viên thiết kế: Tính năng A (10 threads), B (10 threads), C (10 threads)... Dài cho đến Z. Kết quả là máy chủ phải quản lý tới 50 cái Thread Pool khác nhau (Mất cả ngàn Threads). Việc hệ điều hành (OS) phải liên tục "chuyển đổi ngữ cảnh" (Context Switching) qua lại giữa hàng ngàn Threads đó làm CPU tăng vọt 100% chỉ để quản lý, chứ chưa làm được việc gì hữu ích.
   - *Cách giải quyết*: Đừng lạm dụng Thread Pool. Trong kiến trúc hiện đại (Node.js, Go, WebFlux), hãy dùng Semaphore Bulkhead (Bộ đếm ảo). Nó cực nhẹ và không sinh ra thêm bất kỳ Thread vật lý nào.
2. **Kích thước quá bé (Starvation)**: Cấu hình Vách ngăn chứa được 2 Request. Lúc cao điểm hệ thống cần chạy 3 Request bình thường, Request thứ 3 bị từ chối oan uổng. Tự bóp dái hiệu năng của hệ thống.

</details>

1. **Context Switching Annihilation (Thread Pool Abuse)**: The most fatal execution error. An architect decides to create a physical Thread Pool Bulkhead for every single of their 50 downstream Microservices. The JVM is now forced to spin up and manage thousands of distinct OS threads. The Linux kernel spends 90% of its CPU cycles executing pure Context Switching (swapping threads in and out of the CPU core) rather than executing actual business logic. The server is crushed by its own resilience framework.
   - *The Fix*: Strongly prefer **Semaphore-based Bulkheads**. Semaphores use atomics and simple integer counters in RAM. They require exactly zero thread context switching and impose near-zero performance penalty.
2. **Pessimistic Sizing (Artificial Starvation)**: Setting the Bulkhead limit too conservatively (e.g., `Max_Concurrency = 2`). During normal, healthy traffic spikes, the application will require 5 concurrent connections. The Bulkhead falsely detects an attack and begins throwing `BulkheadFullExceptions`, causing severe user disruption while the Server CPU is idling at 1%. Bulkheads should be sized aggressively large enough to handle healthy peaks, but tight enough to prevent total server starvation.

---

## Related Topics

- For how to proactively cut off the connection, read **[Circuit Breaker](./circuit-breaker.md)**.
- For managing limits from EXTERNAL users, see **[Rate Limiting](../scalability/rate-limiting.md)**.
- For what happens when you finally stop failing fast and try again, read **[Retries & Backoff](./retries.md)**.
