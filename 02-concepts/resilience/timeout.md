# Timeout

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Máy tính rất "ngu ngốc". Nếu bạn bảo nó gọi API lấy danh sách Sản phẩm, và API bên kia không bao giờ trả lời, máy tính của bạn sẽ ĐỨNG ĐÓ ĐỢI MÃI MÃI cho đến tận lúc vũ trụ sụp đổ. Hàng ngàn khách hàng vào web là hàng ngàn tiến trình (Thread) đứng đợi mãi mãi, RAM sẽ cạn kiệt và hệ thống sập. **Timeout (Ngắt chờ)** là việc bạn đặt đồng hồ đếm ngược: "Tôi gọi anh, nếu quá 3 giây anh không trả lời, tôi sẽ tự động cúp máy và báo lỗi". Nó là tấm khiên cơ bản và quan trọng nhất để bảo vệ máy chủ khỏi bị cạn kiệt tài nguyên.

</details>

> **Summary**: Computers are inherently literal. If an application initiates a synchronous HTTP request and the downstream server suffers a network partition without gracefully closing the TCP socket, the calling thread will wait *indefinitely*. As concurrent traffic arrives, thousands of threads will pool into a suspended waiting state, rapidly exhausting the OS memory and Thread Pool, leading to a catastrophic system-wide crash. The **Timeout Pattern** enforces a strict upper-bound mathematical limit on how long a thread is permitted to block (e.g., 3000ms). If the threshold is exceeded, the network driver aggressively severs the connection, throws a `TimeoutException`, and immediately frees the thread back to the application pool.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đi ăn nhà hàng và gọi món.
1. **Không có Timeout**: Bạn gọi món "Bò bít tết". Nhà bếp bị cháy, đầu bếp bỏ chạy hết. Nhưng bạn không biết, bạn cứ ngồi ở bàn ĐỢI MÃI MÃI. Từ sáng đến đêm, đến khi bạn chết đói ở bàn ăn. Quán đầy khách nhưng ai cũng ngồi đợi mãi mãi, không ai đứng dậy nhường bàn cho người mới.
2. **Có Timeout**: Bạn gọi món, và tự nhủ: "Nếu đúng 15 phút nữa đồ ăn không ra, tao sẽ đứng dậy đi ăn bún chả". Đúng 15 phút sau, không có đồ ăn. Bạn tức giận đứng dậy (Báo lỗi 504 Timeout) rời đi, nhường bàn lại cho khách hàng khác vào gọi món. Bạn sống sót và nhà hàng không bị kẹt bàn cứng ngắc.

</details>

Imagine ordering food at a Drive-Thru window.
1. **Without a Timeout**: You place your order. You pull up to the window. The cashier has suffered a heart attack and is lying on the floor. Because you have no Timeout, you sit in your car at the window staring blankly ahead. You wait for 3 days. The line of cars behind you stretches for 50 miles. The entire road network is paralyzed.
2. **With a Timeout**: You pull up to the window. You set a timer on your watch for exactly 3 minutes. The cashier is on the floor. After 3 minutes, your watch beeps. You aggressively press the gas pedal, drive away, and declare: "Transaction Failed!" The car behind you can now move up. You preserved the flow of traffic.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 2 loại Timeout chính trong lập trình mạng mà bạn bắt buộc phải phân biệt:
1. **Connection Timeout (Thời gian chờ Kết nối)**: Thời gian tối đa để Máy A tìm được đường đi và móc nối TCP/IP thành công với Máy B. Thường rất nhanh. Nếu quá 5 giây mà không kết nối được $\rightarrow$ Thường do Máy B tắt nguồn hoặc đứt cáp quang.
2. **Read Timeout (Thời gian chờ Đọc dữ liệu)**: Máy A đã kết nối thành công với Máy B rồi. Máy A đã gửi Yêu cầu xong rồi. Máy A đang há miệng đợi Máy B tính toán và nhả dữ liệu về. Thời gian chờ này dài hơn (Có thể 10 giây hoặc 30 giây). Nếu quá giờ $\rightarrow$ Thường do Máy B bị nghẽn CPU hoặc kẹt Database.

</details>

Every robust HTTP Client (e.g., `Axios`, `Java HttpClient`, `Go net/http`) explicitly separates Timeouts into two distinct phases of the TCP lifecycle:
1. **Connection Timeout**: The maximum time permitted to complete the initial TCP 3-Way Handshake (and TLS Handshake). This establishes the actual physical/logical network link between Server A and Server B. It should be extraordinarily short (e.g., `1000ms` - `3000ms`). If it trips, the downstream server is physically offline, or a firewall is blackholing the packet.
2. **Read Timeout (Socket Timeout)**: The connection is established, and the HTTP request has been fully transmitted. This timeout limits how long the client will wait for the downstream server to process the business logic and stream the HTTP Response bytes back. This is highly variable (e.g., `5000ms` for an API, but maybe `60000ms` for a heavy CSV export). If it trips, the downstream server is alive but functionally overloaded/deadlocked.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Mọi ngôn ngữ lập trình đều Cố Tình che giấu sự phức tạp của mạng. Khi bạn viết hàm `fetch('api.com')`, code trông có vẻ rất bình thường.
Nhưng mặc định, rất nhiều thư viện HTTP cũ (như `HttpURLConnection` của Java hoặc `requests` bản cũ của Python) cấu hình Timeout mặc định là... **Vô cực (Infinite)**, hoặc là thời gian timeout của Hệ điều hành (Lên tới vài phút).
Nếu bạn gọi API Momo để thanh toán mà Momo bị treo, tiến trình của bạn sẽ bị treo theo. 10.000 khách hàng bấm nút là 10.000 tiến trình bị treo. Server hết sạch RAM và bốc cháy.
Timeout không phải là một "Tính năng nâng cao". Nó là Lớp Phòng Thủ cơ bản nhất bắt buộc phải cấu hình thủ công mỗi khi bạn khởi tạo bất kỳ một HTTP Client nào. Nếu không có Timeout, hệ thống của bạn là một quả bom nổ chậm.

</details>

Timeouts exist to strictly prevent **Thread Exhaustion** and **Cascading Failures**.
Many default HTTP client libraries in older frameworks (e.g., Java's default `URLConnection`, or older versions of Python's `urllib`) historically shipped with the Timeout set to `0` (Infinite) or relied on the underlying OS TCP timeout (which can be over 2 minutes).
If an engineer blindly uses these libraries to call a 3rd-party `PaymentGateway`, and that gateway experiences an invisible backend deadlock, every single incoming user request will spin up a Thread that hangs for 2 minutes. A server with a 200-Thread pool will be completely paralyzed in under 10 seconds.
Explicitly defining Timeouts is not an optimization; it is an absolute mandatory architectural shield. It explicitly bounds the maximum time a resource (Memory/Thread) can be held hostage by a failing external dependency.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh khi API Gửi Email bị treo (Lag) mất 60 giây.
</details>

Visualizing the impact on a Login API when the secondary "Send Welcome Email" API hangs indefinitely.

| Scenario | No Timeout Configured | Read Timeout = 2 Seconds |
|---|---|---|
| **User Flow** | User clicks Login. | User clicks Login. |
| **Backend Wait**| Code hangs infinitely waiting for Email API. | Code waits 2 seconds. Kills connection. |
| **User UX** | Spinner spins forever. User thinks App is broken. | Logs in successfully. Email simply fails in background. |
| **Server Health**| Thread Pool exhausted. Server completely crashes. | Threads instantly freed. Server stays 100% healthy. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giao tiếp giữa các Microservices**: Đây là chuẩn mực bắt buộc. Dù 2 Microservice nằm chung 1 Server hay chung 1 cụm Kubernetes (Tốc độ ping rất nhanh), bạn vẫn phải đặt Timeout là 3-5 giây. Vì lỗi không đến từ tốc độ cáp mạng, lỗi đến từ việc CPU hoặc Database của Microservice kia bị nghẽn.
2. **Truy vấn Database (Query Timeout)**: Nếu bạn dùng lệnh `SELECT` để phân tích dữ liệu trên bảng có 1 tỷ dòng mà không có Index. DB sẽ kẹt cứng. Bắt buộc phải cài đặt lệnh `Statement Timeout` trên SQL (Ví dụ: Câu lệnh nào chạy quá 10 giây thì ép tự động ngắt) để bảo vệ Database khỏi bị treo cứng.
3. **Cổng API (API Gateway / Nginx)**: Nginx luôn có các cấu hình `proxy_read_timeout` và `proxy_connect_timeout` cực kỳ chặt chẽ (Thường là 60s). Dù Code Backend của bạn có ngu ngốc đứng đợi mãi mãi, thì Nginx đứng ở cửa cũng sẽ tự động cắt dây mạng và quăng lỗi `504 Gateway Timeout` vào mặt người dùng.

</details>

1. **Inter-Microservice RPC (HTTP/gRPC)**: The most critical vector. Even if `Service A` and `Service B` exist on the exact same physical Kubernetes Node (sub-millisecond ping), you MUST configure a strict Read Timeout (e.g., `3000ms`). The danger is not network transit time; the danger is that `Service B` hits an RDBMS Deadlock and holds the HTTP connection hostage.
2. **Database Query Timeouts**: Latency doesn't just happen over HTTP. A developer might accidentally deploy a Cartesian `JOIN` against a 500-million row table. Without limits, the PostgreSQL engine will aggressively consume 100% CPU trying to solve the query for the next 4 hours. Drivers and connection pools (like HikariCP) explicitly support `CommandTimeout` to ruthlessly kill runaway SQL queries after X seconds.
3. **Reverse Proxies (Nginx / Cloudflare)**: Nginx utilizes `proxy_connect_timeout` and `proxy_read_timeout` (default 60s). If your Node.js backend has a severe memory leak and hangs, Nginx will physically sever the TCP connection from the outside and return the infamous `HTTP 504 Gateway Timeout` to the browser, protecting its own worker threads.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Quy tắc Timeout giảm dần (Timeout Budgeting)**: Nếu Web gọi Service A (Cho phép 5s). Service A gọi Service B. Thì Timeout của Service B BẮT BUỘC phải nhỏ hơn 5s (Ví dụ 3s). Nếu bạn set Timeout của B là 10s, Service A sẽ bị quá giờ và chửi thẳng vào mặt Web (Lỗi 504) trước khi B kịp trả về.
2. **Luôn set Connection Timeout cực ngắn**: Thời gian để "Kết nối" (Connect) không bao giờ mất quá nhiều thời gian trừ khi đứt cáp quang. Đừng bao giờ set Connection Timeout là 30 giây. Hãy set nó là 2-3 giây. Nhanh chóng nhận ra lỗi đứt cáp để còn Fail-fast chuyển sang phương án Fallback.

</details>

1. **Timeout Budgeting (Distributed Deadlines)**: A critical architectural rule for deep call chains. If `Gateway` allows `Service A` 5000ms to respond, and `Service A` needs to call `Service B`, `Service A` MUST set its internal timeout to `Service B` to something strictly less than the total remaining budget (e.g., 3000ms). If `Service A` sets its timeout to 10000ms, the `Gateway` will time out at 5000ms and return a `504` to the user, rendering any subsequent work done by `Service B` completely useless and orphaned. (Advanced frameworks use "Deadline Propagation" via gRPC context headers to handle this automatically).
2. **Aggressive Connection Timeouts**: The TCP 3-Way handshake requires traversing the network path. It either succeeds in a few milliseconds, or it drops entirely due to a firewall/routing blackhole. Setting a Connection Timeout to 30 seconds is mathematically absurd; if the SYN-ACK isn't received in 2 seconds, it's not coming. Aggressively cap Connection Timeouts at `1000ms - 3000ms` to Fail Fast.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bóng ma Dữ liệu (Ghost Writes do Read Timeout)**: Đây là cạm bẫy cực kỳ thâm độc. Bạn gọi API trừ tiền. Service Thanh toán đã nhận lệnh và đang trừ tiền trong Database. Mới được 3 giây, Code của bạn hết kiên nhẫn (Read Timeout), tự động cúp máy và báo lỗi "Thanh toán thất bại". Tuy nhiên, cái Database bên kia VẪN ĐANG CHẠY. 1 giây sau nó chạy xong, tiền vẫn bị trừ. Khách hàng nhận thông báo "Thất bại" nhưng bị trừ mất tiền!
   - *Cách giải quyết*: Khi gặp lỗi Read Timeout ở các API quan trọng (POST), tuyệt đối KHÔNG ĐƯỢC báo "Lỗi" ngay cho khách hàng. Phải báo "Trạng thái đang được xử lý, vui lòng chờ", sau đó lưu một mã giao dịch vào hệ thống đối soát (Reconciliation) để nhân viên kiểm tra lại xem bên kia đã trừ tiền hay chưa.
2. **Dùng Timeout che giấu sự Yếu kém**: Thấy Database chậm, query mất 10 giây. Thay vì đi tạo Index cho Database, lập trình viên "Lách luật" bằng cách nâng Timeout lên 30 giây cho khỏi báo lỗi. Đây là cách nhanh nhất để phá nát hệ thống. Timeout sinh ra là để NGẮT những thứ bất thường, không phải để hợp thức hóa những đoạn code chậm chạp.

</details>

1. **The Ghost Write Anomaly (The Read Timeout Trap)**: The most dangerous edge case in distributed networking. A Client issues an `HTTP POST /charge` with a Read Timeout of 3000ms. The Server receives the packet and begins executing the database transaction. At exactly 3000ms, the Client enforces the Read Timeout, violently severs the TCP connection, and throws a `TimeoutException`. **CRITICAL FLAW**: The Server does not know the Client disconnected. The Server finishes the transaction at 3500ms and commits it to the DB. The Client tells the user "Payment Failed", but the money was successfully deducted.
   - *The Fix*: A Read Timeout on a mutating operation leaves the system in an **Unknown State**. You cannot safely retry without an Idempotency Key. The UI must explicitly inform the user: "Transaction Status Unknown. Please check your email for confirmation." Background Reconciliation jobs must subsequently poll the provider to verify the actual state.
2. **Using Timeouts as a Band-Aid for Bad Code**: An endpoint takes 15 seconds to load because it executes 500 N+1 Database queries. Instead of fixing the ORM logic, a Junior Developer explicitly increases the Read Timeout on the API Gateway to 30 seconds to "stop the 504 errors". This perfectly masks the underlying performance rot, guaranteeing that during the next traffic spike, the entire server will OOM (Out Of Memory) and crash completely. Timeouts are defensive shields, not performance optimizations.

---

## Related Topics

- For how to react safely when a Timeout occurs, read **[Retries & Backoff](./retries.md)**.
- For how to explicitly cut the connection before the Timeout even starts, see **[Circuit Breaker](./circuit-breaker.md)**.
- For solving the "Ghost Write" problem where money is deducted secretly, see **[Saga Pattern](../event-driven/saga.md)**.
