# Retries & Backoff

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trong môi trường mạng Internet hoặc Cloud, lỗi xảy ra liên tục nhưng đa số là **Lỗi Tạm Thời (Transient Faults)**. Một gói tin chạy qua đại dương đụng phải con cá mập $\rightarrow$ Rớt mạng trong 50 mili-giây. Nếu code của bạn ngay lập tức báo lỗi `500` cho khách hàng, trải nghiệm sẽ rất tệ. **Retry (Thử lại)** là cơ chế tự động gọi lại API đó thêm vài lần nữa. Rất có thể lần thứ 2 sẽ thành công vì gói tin đi qua đường khác. Tuy nhiên, nếu bạn Retry một cách "ngu ngốc" (nháy máy liên tục), bạn sẽ biến thành một Hacker đang tự DDoS chính hệ thống của mình. Thuật toán **Exponential Backoff & Jitter** sinh ra để giải quyết thảm họa này.

</details>

> **Summary**: In distributed cloud environments, the vast majority of network errors are **Transient Faults**—micro-outages caused by momentary TCP packet loss, BGP route recalculations, or microsecond Database deadlocks. Terminating the execution immediately and surfacing an Error to the UI for a 50ms transient glitch is terrible engineering. The **Retry Pattern** dictates that the caller should transparently re-attempt the failed operation. However, naïve immediate retries will instantly trigger a "Thundering Herd" self-DDoS attack on a recovering downstream service. To retry safely, architects strictly mandate the mathematical algorithm of **Exponential Backoff with Jitter**.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn gọi điện cho Tổng đài nhà mạng.
1. **Không Retry (Bỏ cuộc)**: Bạn gọi, nghe báo "Máy bận". Bạn lập tức ném điện thoại đi và chửi rủa: "Tổng đài sập rồi!". (Thực ra lúc đó có 1 người vừa cúp máy, mạng đã rảnh, chỉ cần bạn gọi lại là được).
2. **Retry Ngu ngốc (Spam)**: Bạn gọi "Máy bận". Bạn bấm gọi lại NGAY LẬP TỨC. Bạn bấm liên tục 10 lần 1 giây. Hàng ngàn khách hàng cũng làm y như bạn. Tổng đài vốn dĩ đang quá tải, giờ phải nhận thêm hàng vạn cuộc gọi rác. Tổng đài bốc cháy thật.
3. **Exponential Backoff (Thử lại Thông minh)**: Bạn gọi "Máy bận". Bạn tự nhủ: "Chắc họ đang đông". Bạn chờ **1 phút** rồi gọi lại. Vẫn bận. Bạn chờ **2 phút**. Vẫn bận. Bạn chờ **4 phút**. Lần này bạn gọi được. Tần suất chờ giãn ra theo cấp số nhân giúp Tổng đài có thời gian "Thở" để xử lý việc cũ.

</details>

Imagine dialing a popular Restaurant to make a reservation.
1. **No Retry (Fail Fast)**: You dial. You get a busy signal. You immediately hang up, assume the restaurant has burned to the ground, and eat instant noodles. (Terrible resilience).
2. **Naïve Retry (The DDoS)**: You get a busy signal. You instantly hit redial. And again. And again. You redial 100 times in 10 seconds. 5,000 other hungry customers do the exact same thing. The restaurant's phone system melts. You have actively contributed to a systemic outage.
3. **Exponential Backoff (The Gentleman's Retry)**: You get a busy signal. You hang up and wait exactly **1 minute**. You dial. Busy. You hang up and wait **2 minutes**. You dial. Busy. You wait **4 minutes**. It rings! By exponentially increasing your delay, you gave the hostess the critical breathing room required to clear the existing backlog of customers.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cơ chế Retry hoàn hảo có 3 yếu tố Toán học cấu thành:
1. **Maximum Retries (Số lần thử tối đa)**: Không bao giờ được gọi lại mãi mãi. Thường chỉ set tối đa 3 hoặc 5 lần. Nếu 3 lần vẫn tịt, hãy ngắt Cầu dao (Circuit Breaker).
2. **Exponential Backoff (Lùi bước theo Cấp số nhân)**: Thời gian chờ giữa các lần Retry không được cố định. Phải tăng theo cấp số nhân (`2^n`). Ví dụ: Chờ 100ms $\rightarrow$ 200ms $\rightarrow$ 400ms $\rightarrow$ 800ms.
3. **Jitter (Độ nhiễu Ngẫu nhiên)**: Cực kỳ quan trọng. Nếu Server sập lúc 12:00:00, 10.000 cái điện thoại cùng đếm đúng 100ms và cùng gọi lại lúc 12:00:01. Nó sẽ dội 1 cục tải cực lớn. Jitter là việc cộng thêm 1 số ngẫu nhiên vào thời gian chờ. Thay vì 100ms, máy A chờ `103ms`, máy B chờ `125ms`. 10.000 cuộc gọi sẽ tản đều ra trên thời gian, cứu sống Server.

</details>

A mathematically perfect Retry mechanism consists of 3 interlocked variables:
1. **Maximum Retries (The Cap)**: Never loop infinitely. A standard architecture strictly caps retries at `3` or `5` attempts. If the 3rd attempt fails, it is no longer a Transient Fault; it is a systemic outage. You must fail the request entirely and rely on the Circuit Breaker.
2. **Exponential Backoff (The Curve)**: The delay between attempts must never be a constant integer (e.g., waiting 100ms every time). The delay must scale exponentially (`Base_Delay * 2^attempt`). Example: 100ms $\rightarrow$ 200ms $\rightarrow$ 400ms $\rightarrow$ 800ms. This prevents traffic congestion.
3. **Jitter (The Chaos Variable)**: The absolute missing link. If a network switch drops for 1 second, 5,000 clients will experience an error simultaneously. Without Jitter, all 5,000 clients will wait exactly 100ms and retry at the exact same millisecond, unleashing a synchronous wave of traffic that crashes the recovering node. **Jitter** injects algorithmic randomness (`Wait_Time = Exponential_Time + Random(0, 50ms)`). Client A waits 112ms, Client B waits 145ms. The Thundering Herd is beautifully dispersed.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao Lỗi mạng xảy ra? Vì kiến trúc Cloud là môi trường chia sẻ (Shared Environment). Database của bạn có thể đang dùng chung ổ cứng vật lý với Database của công ty khác (Ồn ào - Noisy Neighbor). Công ty kia xuất báo cáo nặng làm ổ cứng bị khựng lại 1 nhịp. Lệnh `SELECT` của bạn đúng lúc đó bị văng lỗi `Timeout`.
Đây là Lỗi Tạm Thời. 1 giây sau ổ cứng chạy mượt lại.
Nếu không có Retry, bạn ném lỗi thẳng vào mặt người dùng. Người dùng chửi thề, F5 tải lại trang. (Chính con người đang đóng vai trò làm hàm Retry!).
Thay vì bắt người dùng F5, hãy để Code tự động chờ 100ms rồi F5 ngầm giùm người dùng. Trải nghiệm sẽ hoàn hảo, người dùng tưởng hệ thống rất xịn mà không biết ở dưới ngầm mạng rớt liên tục.

</details>

Why do Transient Faults occur? Cloud architecture relies heavily on multitenant virtualized infrastructure. Your AWS RDS instance shares a physical hypervisor and SAN storage with 10 other companies. If the "Noisy Neighbor" executes a massive BI export, the physical Disk I/O stalls for 50 milliseconds. Your lightweight `SELECT` query hits that specific 50ms stall, times out, and fails.
This failure is strictly transient. 100 milliseconds later, the hardware is perfectly healthy again.
If your code lacks a Retry Policy, it instantly surfaces an `HTTP 500` to the human user. The human gets angry, curses, and explicitly hits the "Refresh (F5)" button on their browser. **The human is manually executing the Retry**.
Good engineering dictates that the code should silently absorb the transient fault, delay 100ms, and retry the TCP request automatically. The UI spins for an extra 100ms, the data loads, and the human believes the system has perfect 100% uptime.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh hiện tượng khi 1.000 Khách hàng đồng loạt Retry vì Server bị khựng lại 1 giây.
</details>

Visualizing the "Thundering Herd" problem when 1,000 clients retry a failed connection.

| Mechanism | Timeline of Traffic Hits | Result on the Downstream Server |
|---|---|---|
| **Constant Retry (100ms)** | 1000 hits @ 100ms $\rightarrow$ 1000 hits @ 200ms | Immediate death by synchronized DDoS. |
| **Exponential Backoff** | 1000 hits @ 100ms $\rightarrow$ 1000 hits @ 200ms | Slower death, but still synchronized spikes. |
| **Exponential + Jitter** | 12 hits @ 101ms, 18 hits @ 105ms, 5 hits @ 110ms | Perfectly smoothed traffic wave. Server easily absorbs the load and Recovers. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giao tiếp Dữ liệu Đám mây (S3 / DynamoDB)**: Nếu bạn dùng các SDK của AWS (như `boto3` trong Python), bạn không cần viết code Retry. Bản thân cái SDK của AWS đã nhúng sẵn thuật toán Exponential Backoff + Jitter vào trong hàm `UploadFile` của nó rồi.
2. **Webhooks**: Nếu bạn bán hàng trên Shopify, khi có Đơn hàng mới, Shopify sẽ gọi Webhook (Bắn data) về server của bạn. Lỡ Server của bạn đang sập thì sao? Shopify sẽ không bỏ cuộc. Nó sẽ dùng Exponential Backoff để thử bắn lại sau 1 phút, 5 phút, 1 tiếng, và cao nhất là 2 ngày.
3. **Truy vấn Database bị Khóa (Deadlock)**: Khi 2 lệnh Update tranh nhau sửa 1 dòng, 1 lệnh sẽ bị Database giết chết bằng lỗi Deadlock. Thay vì báo lỗi cho khách hàng, Backend chỉ cần nhẹ nhàng bắt lấy cái lỗi Deadlock đó, chờ 50ms và chạy lại câu lệnh Update. Dòng đó đã được nhả khóa và Update thành công.

</details>

1. **Cloud Provider SDKs (AWS / Azure)**: The most ubiquitous implementation. You likely use Exponential Backoff every day without realizing it. When you execute an `s3.putObject()` call via the AWS SDK, the underlying HTTP client is hardcoded to natively intercept `503 Slow Down` errors and automatically execute Full Jitter Backoff retries before bubbling an exception up to your code.
2. **Third-Party Webhooks (Stripe / Shopify)**: Asynchronous Event Delivery natively relies on Retry queues. If Stripe attempts to send a `payment.succeeded` Webhook to your Application, and your Nginx is rebooting (returning `502 Bad Gateway`), Stripe does not drop the financial data. It queues the payload and executes an aggressive Exponential Backoff schedule, retrying over the course of 3 entire days until your server finally returns a `200 OK`.
3. **Optimistic Concurrency / Deadlock Resolution**: In high-contention RDBMS environments, two transactions updating the same row will cause a Deadlock or an Optimistic Locking `VersionConflictException`. This is a transient software fault. The optimal resolution is a simple `catch` block that executes a Jittered 50ms delay and re-selects the row.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Idempotency (Tính Lũy đẳng) là Sinh mệnh**: Giống y như bài học ở Saga Pattern. Lệnh GHI (POST/UPDATE) mà gọi 2 lần là rác Database (Trừ tiền 2 lần). Nếu bạn code tự động Retry cho API Thanh Toán, bạn BẮT BUỘC phải truyền kèm `Idempotency-Key: 123` trên Header. Backend nhận được chữ 123, biết đây là thằng ban nãy bị rớt mạng gọi lại, tao sẽ không trừ tiền nó thêm lần nữa.
2. **Chỉ Retry lỗi Hệ thống**: Không bao giờ Retry lỗi `400 Bad Request` (Gửi thiếu ID). Đã sai logic thì có gọi 1 triệu lần vẫn sai. Chỉ Retry lỗi `500`, `502`, `503`, `504` và lỗi Mạng (Connection Refused).

</details>

1. **The Idempotency Prerequisite**: The most lethal trap in distributed systems. If an HTTP request drops, the client does NOT know if the packet dropped *on the way to* the server (meaning the DB is untouched) or *on the way back from* the server (meaning the DB was successfully mutated). If you blindly retry a `POST /charge` endpoint, you will double-charge the credit card. **Absolute Law**: You may ONLY configure automatic retries on non-idempotent operations (POST) if the API explicitly supports an `Idempotency-Key` header, allowing the database to deduplicate the retry attempt safely.
2. **Surgical Error Targeting**: Never apply a blanket "Retry on Exception" rule. Retrying an `HTTP 401 Unauthorized` or `HTTP 400 Bad Request` (Invalid JSON) is a complete waste of network cycles; it will mathematically never succeed. You must explicitly constrain the Retry policy to `IOException` (Socket closures) and transient server errors (`HTTP 502, 503, 504`, and `429 Too Many Requests`).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Thảm họa Khuếch đại Retry (Retry Amplification)**: Một hệ thống có 4 lớp. Lớp Web $\rightarrow$ Lớp API $\rightarrow$ Lớp Logic $\rightarrow$ Lớp DB. 
Database bị sập. Lớp Logic thử gọi DB lại 3 lần. Lớp API thử gọi Lớp Logic lại 3 lần. Lớp Web thử gọi Lớp API lại 3 lần.
Tổng cộng: Khách hàng click 1 phát ở Web, nó biến thành $3 \times 3 \times 3 = 27$ cái request ồ ạt đập vào cái Database đang hấp hối. Hệ thống sập không cách nào cứu chữa.
   - *Cách giải quyết*: TUYỆT ĐỐI chỉ nên cài đặt Retry ở đúng 1 lớp duy nhất (Tốt nhất là lớp trực tiếp gọi DB hoặc ngoại vi). Các lớp ngoài cùng không được phép Retry chồng chéo.
2. **Code Jitter bị sai toán học**: Cố tình code thêm số Random vào hàm thời gian nhưng lại dùng sai công thức, làm cho thời gian chờ bị lệch hẳn (Quá nhỏ hoặc quá lớn), dẫn đến Jitter không có tác dụng tản tải. Hãy dùng các thư viện xịn như Resilience4j, đừng tự viết hàm Random.

</details>

1. **Retry Amplification (The Multiplier Effect)**: A catastrophic architectural anti-pattern in deep microservice call chains. Service A calls B. B calls C. C calls D. If Database D experiences a 500ms timeout, C retries 3 times. But B also has a retry policy, so B retries calling C 3 times. A retries calling B 3 times. A single user click initiates $3 \times 3 \times 3 = 27$ synchronized downstream requests hitting the struggling Database. **The Fix**: Strictly centralize Retry logic. Typically, only the Edge Gateway (retrying idempotent reads) OR the absolute deepest layer (Service C talking to the DB) should execute retries. Intermediary services must Fail Fast and propagate the error.
2. **Amateur Jitter Implementation**: Junior developers attempt to hand-roll Jitter logic using `Math.random()`. Poorly engineered Jitter algorithms either lack true entropy or inadvertently skew the distribution (e.g., heavily weighting the delay towards 0ms). This completely negates the Thundering Herd protection. **The Fix**: Never reinvent the mathematical wheel. Utilize hardened libraries like `Resilience4j` (Java), `Polly` (.NET), or AWS's published `FullJitter` backoff algorithm.

---

## Related Topics

- For how to completely cut off the connection after Retries fail, see **[Circuit Breaker](./circuit-breaker.md)**.
- For managing limits when other people retry against YOUR server, see **[Rate Limiting](../scalability/rate-limiting.md)**.
- For ensuring your Retries don't duplicate data, read about **[Idempotency in API Design](../../04-api-design/restful/idempotency.md)**.
