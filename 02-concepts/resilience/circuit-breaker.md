# Circuit Breaker

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu bạn cắm quá nhiều nồi cơm điện vào 1 ổ cắm, dòng điện quá tải sẽ làm dây điện bốc cháy và thiêu rụi cả căn nhà. Để chống lại điều đó, người ta phát minh ra **Cầu Dao Điện (Circuit Breaker)**. Khi thấy dòng điện quá cao, Cầu Dao sẽ tự động "Nhảy" (Ngắt điện) để cứu căn nhà. Trong Microservices cũng vậy, nếu Service B đang bị sập mà Service A cứ cố gắng gọi liên tục, Service A sẽ bị hết sạch RAM (Chờ đợi) và sập theo. Circuit Breaker là đoạn code nằm ở Service A, tự động NGẮT MẠNG sang Service B khi thấy B bị lỗi liên tục, bảo vệ Service A khỏi cái chết dây chuyền.

</details>

> **Summary**: In an electrical grid, a Circuit Breaker automatically trips to interrupt current flow when a fault is detected, preventing a catastrophic fire. In Distributed Systems, the **Circuit Breaker Pattern** serves the exact same life-saving function. When a downstream microservice experiences severe latency or crashes, upstream services that synchronously call it will exhaust their own thread pools waiting for responses, leading to a cascading systemic failure. A software Circuit Breaker explicitly monitors failure rates. When the failure threshold is crossed, it "Trips" (Opens), instantly failing all subsequent calls fast, thereby preventing resource exhaustion and giving the downstream service breathing room to recover.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn gọi điện cho Thợ sửa ống nước.
1. **Không có Cầu Dao**: Thợ sửa ống nước đang ngủ say. Bạn gọi, máy đổ chuông 3 phút mới tự tắt. Bạn cúp máy, **gọi lại ngay lập tức** (Retry). Lại đổ chuông 3 phút. Bạn gọi 100 lần. Bạn mất trắng cả buổi sáng chỉ để nghe tiếng tút tút, không làm được việc gì khác. (Hao tốn tài nguyên vô ích).
2. **Có Cầu Dao**: Bạn gọi lần 1 (Không bốc máy). Lần 2 (Không bốc máy). Lần 3 (Không bốc máy). Lúc này, não bạn tự động bật "Cầu Dao": **Ông này ngủ mẹ rồi, cấm không gọi nữa!**. Trong 2 tiếng tiếp theo, nếu ống nước bị rỉ, bạn lấy băng keo dán tạm (Fallback), chứ KHÔNG THÈM cầm điện thoại lên gọi ông kia nữa. 2 tiếng sau, bạn thử gọi lại 1 lần (Half-Open), nếu ổng nghe máy thì bạn mới nói chuyện tiếp.

</details>

Imagine knocking on a friend's door to ask a question.
1. **Without a Circuit Breaker**: Your friend is wearing noise-canceling headphones and can't hear you. You knock. You wait 5 minutes. No answer. You knock again. You wait 5 minutes. You stand outside their door for 3 hours doing absolutely nothing (Thread Exhaustion).
2. **With a Circuit Breaker**: You knock 3 times. No answer. You mentally "Trip the Breaker". You declare: "He is not available." For the next 30 minutes, you completely refuse to walk over to his door. If someone tells you to ask him a question, you instantly say: "He's busy, try again later" (Failing Fast). After 30 minutes, you cautiously knock *once* to see if he's available now.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cầu dao điện trong code hoạt động dựa trên 3 Trạng thái (State Machine):
1. **Đóng (CLOSED - Bình thường)**: Mọi API call đều được cho phép đi qua. Cầu dao âm thầm đếm số lượng lỗi. (Ví dụ: 5% API gọi bị lỗi).
2. **Mở (OPEN - Ngắt điện)**: Khi tỷ lệ lỗi vượt mức cho phép (Ví dụ: 50% API bị lỗi), cầu dao nhảy sang MỞ. Mọi API gọi tiếp theo đều bị chặn đứng lại NGAY LẬP TỨC ở client mà không hề gửi tín hiệu ra mạng. Code sẽ trả về lỗi `HTTP 503` hoặc chạy hàm Fallback (Dự phòng).
3. **Mở một nửa (HALF-OPEN - Thăm dò)**: Sau khi Mở được 1 khoảng thời gian (Ví dụ: 30 giây), cầu dao rón rén chuyển sang chế độ Thăm dò. Nó cho phép ĐÚNG 1 VÀI REQUEST đi qua thử. Nếu thành công, nó chốt lại là Service kia đã sống lại $\rightarrow$ Chuyển về CLOSED. Nếu vẫn lỗi $\rightarrow$ Lại ngắt điện OPEN.

</details>

A software Circuit Breaker is implemented strictly as a State Machine with 3 primary states:
1. **CLOSED (Normal Operation)**: The circuit is connected. All requests flow freely to the downstream service. The Breaker acts as an invisible monitor, maintaining a rolling window of metrics (Count of Successes vs. Failures/Timeouts).
2. **OPEN (Tripped / Failing Fast)**: The Failure Threshold (e.g., 50% of requests failed in the last 10 seconds) is breached. The Breaker actively severs the connection. Any subsequent attempt to execute the function is instantly rejected locally (throwing a `CircuitBreakerOpenException`), completely bypassing the network. It immediately executes Fallback logic.
3. **HALF-OPEN (Recovery Probing)**: After a predefined `SleepWindow` (e.g., 30 seconds), the Breaker tentatively transitions to Half-Open. It allows a severely limited number of "Probe" requests to pass through to the downstream service. If the probes succeed, the downstream service has recovered, and the Breaker resets to **CLOSED**. If the probes fail, it instantly snaps back to **OPEN**.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Bảo vệ Hệ thống gọi (Upstream)**: Như đã nói ở phần Overview, nếu Service B bị treo, Service A sẽ bị treo theo do phải đứng đợi quá lâu (Cạn kiệt Thread Pool). Circuit Breaker giúp Service A "Fail Fast" (Báo lỗi ngay lập tức trong 1 mili-giây), giải phóng RAM của A để phục vụ những việc khác.
**2. Cho máy chủ Lỗi cơ hội để Thở (Downstream Recovery)**: Nếu Service B đang quá tải, CPU lên 100%, nó đang cố sức khởi động lại. Lúc này mà Service A cứ liên tục "Retry" (Dội bom request vào B), thì B sẽ mãi mãi không bao giờ ngóc đầu lên nổi. Bằng cách Ngắt cầu dao 30 giây, Service A đã cho Service B một khoảng thời gian yên tĩnh tuyệt đối để nó tự phục hồi lại.

</details>

**1. Protecting the Caller (Preventing Thread Exhaustion)**: In synchronous HTTP/gRPC communication, a blocking call consumes a Thread. If `InventoryService` experiences an RDBMS deadlock and requests start taking 30 seconds to timeout, the `CheckoutService` will quickly open thousands of connections. The `CheckoutService` will exhaust its Thread Pool and violently crash (OutOfMemory/Thread Starvation). The Circuit Breaker instantly short-circuits the call, freeing the Thread immediately to handle other unaffected endpoints.
**2. Protecting the Callee (Allowing Recovery Time)**: If the `InventoryService` is struggling under heavy load (CPU at 100%), it is frantically trying to execute Garbage Collection and process its queue. If the `CheckoutService` aggressively Retries failing requests, it creates a "Thundering Herd" DDoS attack. It mathematically guarantees the `InventoryService` will never recover. The OPEN state provides explicit "Breathing Room". By halting all traffic for 30 seconds, the callee is granted the CPU cycles needed to recover and stabilize.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh khi Service "Đánh giá sao" (Rating) trên Shopee bị sập.
</details>

Visualizing the impact of a failing non-critical microservice (e.g., The "Product Reviews" API).

| Metric | Without Circuit Breaker | With Circuit Breaker + Fallback |
|---|---|---|
| **API Call Behavior** | Blocks for 10 seconds, then Timeouts. | Blocks for 10s (Few times) $\rightarrow$ Breaker Trips $\rightarrow$ Returns instantly in 1ms. |
| **Upstream CPU/RAM** | Exhausted. Hundreds of hanging threads. | Healthy. Threads are instantly freed. |
| **System Status** | **Cascading Failure (Entire App Crashes)**| **Graceful Degradation** |
| **User Experience** | White screen of death / 504 Timeout. | Page loads fast. Review section simply says "Reviews temporarily unavailable." |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Gọi API bên thứ ba (Third-Party APIs)**: Khi code của bạn gọi sang Momo, ZaloPay, Facebook API. Bạn hoàn toàn không kiểm soát được mạng của họ. BẮT BUỘC phải bọc lời gọi đó trong một cái Circuit Breaker.
2. **Truy vấn Database nặng**: Khi một câu lệnh `SELECT` quá nặng làm DB có nguy cơ bị sập, Circuit Breaker sẽ tự động ngắt kết nối DB, và code sẽ tự động trả về dữ liệu rác (hoặc dữ liệu rỗng) để cứu cái DB không bị nổtung.
3. **Service Mesh (Istio)**: Trong môi trường Kubernetes hiện đại, bạn không cần phải tự code Circuit Breaker bằng Java/NodeJS nữa. Cục Sidecar Proxy (Envoy) đứng chặn trước cửa cái Container sẽ tự động đếm lỗi và ngắt Cầu dao ngầm ở tầng Mạng.

</details>

1. **Third-Party API Integrations**: The most critical vector for failure. When calling Stripe, Twilio, or SendGrid, you are crossing the public internet. You have zero control over their BGP routing or internal server health. Wrapping these external HTTP clients in a Circuit Breaker is an absolute architectural mandate.
2. **Database Protection (Shedding Load)**: If an unoptimized Analytics SQL query starts locking tables and slowing down the primary Database, a Circuit Breaker can trip specifically for that Query class. Instead of bringing down the entire DB, the application gracefully returns a "Stats Currently Unavailable" message while explicitly shielding the Database from further harm.
3. **Infrastructure-Level Breakers (Service Mesh)**: While libraries like Resilience4j (Java) or Polly (.NET) exist, modern Kubernetes deployments extract this logic entirely. Istio configures Envoy proxies with `OutlierDetection`. If a specific Pod returns 5 consecutive `503` errors, Envoy automatically ejects that specific Pod from the load-balancing pool for 3 minutes without the application code ever knowing.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Phải luôn viết hàm Fallback (Dự phòng)**: Ngắt cầu dao ném ra lỗi `500` thì quá vô dụng. Khi cầu dao nhảy, code phải tự động chạy vào một hàm Fallback. 
   - Hàm Fallback xịn: Trả về dữ liệu lấy từ Redis Cache cũ.
   - Hàm Fallback cơ bản: Trả về một mảng Rỗng `[]`, giao diện khách hàng sẽ không có dữ liệu thay vì bị bể giao diện.
2. **Chỉ đếm các lỗi Ngoại lệ (System Exceptions)**: Cầu dao chỉ nên nhảy khi gặp lỗi `500 Internal Server Error`, `504 Gateway Timeout`, hoặc Mất mạng. TUYỆT ĐỐI KHÔNG để Cầu dao nhảy khi gặp lỗi `400 Bad Request` hoặc `401 Unauthorized` (Khách hàng nhập sai Pass). Đó là lỗi nghiệp vụ (Business Error), không phải lỗi hệ thống.

</details>

1. **Mandatory Graceful Fallbacks**: Tripping a Breaker and throwing a raw Java Exception up to the user is terrible engineering. You must author a deterministic Fallback method.
   - *Best*: Return stale data from a Local Cache.
   - *Good*: Return a hardcoded Default Object (e.g., `[]` or a generic "Guest" profile).
   - *Acceptable*: Return a cleanly formatted `200 OK` JSON with an internal `error_code` informing the UI to gracefully hide the affected component.
2. **Segregate Business vs. System Exceptions**: A Circuit Breaker should only track systemic infrastructure failures (Timeouts, Socket Closures, `HTTP 502/503/504`). If a client constantly sends invalid JSON payloads and receives `HTTP 400 Bad Request`, or fails a password check (`HTTP 401`), these are completely valid Business responses. If you configure the Breaker to count `400`s as failures, a single malicious user submitting bad data will trip the breaker and take down the entire API for legitimate users.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Kích thước mẫu (Sample Size) quá nhỏ**: Nếu bạn cài đặt "Tỷ lệ lỗi 50% thì ngắt cầu dao". Lúc 3h sáng vắng khách, có đúng 2 request gọi vào, xui thay 1 cái bị đứt mạng (Chiếm 50%). Cầu dao lập tức NGẮT, làm chết hệ thống hoàn toàn vô lý.
   - *Cách giải quyết*: Phải luôn cài đặt tham số `Minimum_Requests`. Yêu cầu: Bắt buộc phải có ít nhất 100 requests gọi trong 10 giây, thì mới bắt đầu tính toán phần trăm lỗi để ngắt cầu dao.
2. **Cấu hình Timeout tĩnh (Hardcoded)**: Code cứng `Timeout = 2s`. Sau này Database phình to ra, truy vấn bình thường cũng mất 2.5s. Kết quả Cầu dao nhảy liên tục dù hệ thống chả bị lỗi gì. Phải liên tục theo dõi (Monitoring) qua Grafana để tinh chỉnh tham số Cầu dao cho hợp lý với thực tế.

</details>

1. **The Small Sample Size Anomaly**: You configure the Breaker to trip at a 50% failure rate. At 4:00 AM, traffic is practically zero. Only 2 requests arrive. Due to a momentary TCP blip, 1 request times out. The failure rate is technically 50%. The Breaker violently trips, shutting down the API for an hour until traffic picks up. **Fix**: You must configure a Minimum Throughput Threshold (e.g., `minimumNumberOfCalls = 50`). The Breaker will not calculate the failure percentage or transition state until it has recorded at least 50 calls in the current sliding window.
2. **Stale Threshold Configurations**: An architect hardcodes the Breaker timeout to `1000ms`. Two years later, the Database grows from 1GB to 500GB. Normal, healthy queries now take `1200ms` due to disk I/O. Suddenly, the Circuit Breaker trips constantly during normal operation, creating catastrophic artificial downtime. **Rule**: Circuit Breaker parameters (Timeouts, Thresholds) must never be hardcoded constants. They must be dynamic variables tied to an external Configuration Server (like Consul or etcd), allowing DevOps to tune them in realtime without redeploying code.

---

## Related Topics

- For how to gracefully wait and try again BEFORE tripping the breaker, see **[Retries & Backoff](./retries.md)**.
- For limiting resource usage inside the app, see **[Bulkhead Pattern](./bulkhead.md)**.
- For the high-level concept this pattern belongs to, review **[Resilience Overview](./overview.md)**.
