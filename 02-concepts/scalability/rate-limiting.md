# Rate Limiting

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Dù máy chủ của bạn xịn đến đâu, nếu một Hacker (hoặc 1 con Bot ngu ngốc) liên tục gửi 1 triệu request mỗi giây vào API Đăng nhập, Database của bạn sẽ bốc khói. **Rate Limiting (Giới hạn tỷ lệ)** là một cái cửa quay bảo vệ đặt trước máy chủ. Nó đếm số lần một IP hoặc một User gọi API. Ví dụ: "Chỉ cho phép 100 requests / 1 phút". Nếu bạn gọi request thứ 101, hệ thống sẽ chặn đứng bạn ở ngoài cửa và chửi thẳng vào mặt bằng lỗi `HTTP 429 Too Many Requests`. Nó bảo vệ Server khỏi bị đánh sập và ngăn chặn vét cạn tài nguyên.

</details>

> **Summary**: No matter how massively a system is horizontally scaled, raw compute power cannot outpace a targeted Distributed Denial of Service (DDoS) attack or an aggressive, misconfigured scraping bot. **Rate Limiting** is a defensive, throttle-based architectural pattern deployed at the network edge (via API Gateways or Load Balancers). It explicitly counts and strictly enforces a mathematical quota on incoming traffic (e.g., "Max 100 requests per IP per minute"). If a client exceeds this quota, the Gateway intercepts the request before it touches the application servers, abruptly terminating it with an `HTTP 429 Too Many Requests` status. It is the ultimate shield against resource exhaustion and brute-force attacks.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một tiệm Buffet Ăn uống Miễn phí.
1. **Không có Rate Limiting**: Một gã béo bước vào tiệm. Hắn ta dùng hai tay vơ vét liên tục toàn bộ Tôm Hùm trên khay. Hắn làm cực nhanh khiến những khách hàng khác không có gì để ăn. Đầu bếp cũng kiệt sức vì phải nấu tôm liên tục phục vụ mỗi mình hắn.
2. **Có Rate Limiting**: Ông chủ đặt một cái rào chắn và phát cho mỗi người 1 cái vé: "Mỗi người chỉ được lấy 1 con Tôm trong vòng 5 phút". Gã béo lấy xong 1 con, định thò tay lấy con thứ 2 thì bị bảo vệ đập vào tay, bắt đứng chờ đúng 5 phút sau mới được lấy tiếp (Lỗi 429). Nhờ vậy, Tôm Hùm được chia đều cho tất cả mọi người.

</details>

Imagine an All-You-Can-Eat Free Buffet.
1. **Without Rate Limiting**: A massive glutton runs in and starts shoveling all the Lobster into his bag at lightning speed. The kitchen cannot cook fast enough. The normal customers in line get absolutely nothing. The system is starved by one aggressive actor.
2. **With Rate Limiting**: The Manager institutes a strict policy: "1 Lobster per person, per 10 minutes." The glutton takes a lobster. 30 seconds later, he reaches for another. The Security Guard slaps his hand away and says: "Too Many Requests. Come back in 9 minutes and 30 seconds." The glutton is throttled, the kitchen is protected, and resources are distributed fairly to legitimate customers.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 4 thuật toán Rate Limiting phổ biến nhất:
1. **Token Bucket (Cái Xô đựng Xu)**: Bạn có 1 cái xô chứa tối đa 10 đồng xu. Mỗi lần gọi API, bạn mất 1 xu. Xô rỗng thì bị chặn (429). Cứ mỗi 1 phút, hệ thống lại ném thêm 2 xu vào xô. (Dễ code nhất, được dùng nhiều nhất ở AWS và Stripe).
2. **Leaky Bucket (Cái Xô lủng đáy)**: Request đổ vào xô từ trên miệng, nhưng xô bị lủng đáy nên chỉ nhỏ giọt xuống Server (xử lý) với tốc độ cố định (VD: 5 giọt/giây). Nếu Request đổ vào quá nhanh làm tràn xô $\rightarrow$ Bị vứt đi. Rất tốt để giữ cho Server chạy với tốc độ ổn định.
3. **Fixed Window (Cửa sổ Cố định)**: Phân theo phút đồng hồ (08:00 đến 08:01). Đúng 08:00 bạn được cấp 100 requests. 08:01 bạn lại được cấp 100 requests. Nhược điểm: Nếu lúc 08:00:59 bạn gọi 100 cái, và 08:01:01 bạn gọi 100 cái. Bạn đã dội 200 request vào Server chỉ trong 2 giây, phá vỡ giới hạn.
4. **Sliding Window (Cửa sổ Trượt)**: Bản nâng cấp của Fixed Window, khung thời gian trượt theo miligiây để khắc phục nhược điểm tụt đỉnh (Spike) của Fixed Window.

</details>

There are 4 core mathematical algorithms used to implement Rate Limiting:
1. **Token Bucket**: The industry standard (used by AWS, Stripe). A bucket holds a maximum capacity of Tokens (e.g., 10). Every API request costs 1 Token. If the bucket is empty, the request drops (`429`). A background refiller process adds a fixed number of Tokens back into the bucket at a constant rate (e.g., 2 tokens per second). It naturally allows for short, aggressive bursts of traffic.
2. **Leaky Bucket**: Operates like a queue. Requests pour into the top of the bucket at any speed. However, the bucket has a hole in the bottom, and requests "leak" out to the Application Server at a strictly constant rate (e.g., exactly 5 requests/sec). If the bucket fills up, new requests overflow and drop. It forces a perfectly smooth, constant workload onto the servers.
3. **Fixed Window Counter**: Time is divided into rigid, literal windows (e.g., `08:00:00` to `08:01:00`). The counter allows 100 reqs per minute. **The Flaw**: A malicious client can send 100 requests at `08:00:59`, and another 100 requests at `08:01:01`. They successfully hit the server 200 times within a 2-second interval, violently violating the intended hardware protection limits.
4. **Sliding Window Log/Counter**: Fixes the boundary flaw of the Fixed Window. It tracks the exact timestamp of each request in a Redis Sorted Set or uses overlapping percentages. It accurately guarantees that within *any* rolling 60-second span, the limit is strictly respected.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Bảo vệ Tài nguyên đắt tiền**: Một API Đăng nhập cần chạy hàm `Bcrypt` để kiểm tra Mật khẩu. Hàm này cố tình được thiết kế cực kỳ chậm và tốn CPU. Nếu bị dội 10.000 requests/giây vào API Đăng nhập, CPU Server sẽ đạt 100% và sụp đổ hoàn toàn. Phải Rate Limit mạnh tay API Đăng nhập (VD: 5 lần/phút/IP).
**2. Kiểm soát Chi phí (Cost Control)**: Nếu bạn dùng API bên thứ 3 (Ví dụ: Gửi SMS giá 500đ/tin). Nếu Hacker viết Bot gọi API gửi SMS của bạn 1 triệu lần 1 ngày. Cuối tháng bạn nhận hóa đơn 500 triệu VNĐ và phá sản. Rate Limiting cứu sống công ty bạn.

</details>

**1. Resource Exhaustion & Asymmetric Attacks**: Certain endpoints are computationally devastating. A `/login` endpoint executes a cryptographic hash (e.g., `bcrypt` or `Argon2`). These algorithms are intentionally engineered to consume massive CPU cycles to deter brute-forcing. An attacker with a cheap laptop can blast 5,000 HTTP requests per second to your Login endpoint. Your Server CPU hits 100% trying to hash them, crashing the entire infrastructure (An Asymmetric DDoS). Strict Rate Limiting (e.g., 5 attempts / minute / IP) neutralizes this mathematically.
**2. Cloud Economics (Billing Protection)**: In Serverless (AWS Lambda) or Third-Party API usage (Twilio SMS, OpenAI GPT-4), you are billed per invocation. A misconfigured script from a legitimate client running in an infinite loop could invoke a Twilio SMS API 100,000 times overnight. You wake up to a $5,000 invoice. Rate Limiting is mandatory financial armor.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh khi Hacker dùng Tool bắn 5.000 Request dò mật khẩu vào lúc 12:00.
</details>

Visualizing a Brute-Force attack against a `/login` API.

| Action | Monolith (No Limits) | API Gateway (Token Bucket = 10) |
|---|---|---|
| **Request 1 - 10** | Processed. Uses 10% CPU. | Processed. Bucket now empty. |
| **Request 11 - 5000**| Server tries to process all. CPU hits 100%. | Gateway drops all 4,990 requests. Returns `429`. |
| **Server Health** | **CRASHED (Out of Memory/CPU)** | **Healthy (Idling)** |
| **Valid Users** | Cannot load the site. | Unaffected (Their IPs have full buckets). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **API Gateway (Nginx / Kong)**: Thay vì tự viết code Rate Limit bằng Javascript/Java (rất hao RAM của máy chủ), người ta cấu hình nó ngay ở cánh cửa đầu tiên là API Gateway hoặc Load Balancer. Nginx có module `limit_req` cực kỳ mạnh.
2. **Theo cấp độ User (Monetization)**: Github API cho phép người dùng miễn phí gọi 60 requests/giờ. Nhưng nếu bạn mua gói VIP, bạn được gọi 5000 requests/giờ. Ở đây Rate Limiting đóng vai trò là "Sản phẩm kinh doanh", buộc khách hàng phải trả tiền để nâng cấp.
3. **Throttling (Bóp băng thông)**: Không trả về lỗi 429 chặn đứng, mà chỉ chủ động làm CHẬM lại. Nếu khách hàng tải Video quá nhiều, Youtube sẽ không khóa IP, mà chỉ bóp tốc độ tải xuống còn 500kb/s để nhường đường truyền cho người khác.

</details>

1. **Edge-Level Gateway Protection (Kong / Cloudflare / Nginx)**: The absolute worst place to implement Rate Limiting is inside your Node.js or Spring Boot application code. By the time the code executes, the TCP socket is open and the framework overhead is already consumed. Standard practice is pushing Rate Limiting to the Absolute Edge. Cloudflare WAF or an Nginx Ingress Controller intercepts the packet and drops it instantly in C-code, saving your Application Servers completely.
2. **API Monetization (Tiered Quotas)**: SaaS businesses (like Stripe or GitHub APIs) utilize user-based Rate Limiting not just for defense, but for monetization. A Free Tier developer is mathematically capped at 100 Requests/Hour. If they exceed it, they receive a `429` with an error message: "Upgrade to Pro for 5,000 Requests/Hour". The Rate Limit drives revenue.
3. **Traffic Throttling (Graceful Degradation)**: Instead of aggressively throwing `429` errors, ISPs and Video CDNs (Netflix) implement Bandwidth Throttling. If a user exceeds their high-speed data cap, the network simply delays their TCP packets, artificially capping their speed at 2Mbps. The connection stays alive, but it operates smoothly in a degraded state to protect global network throughput.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Trả về Header hướng dẫn**: Khi bạn tát vào mặt Client cái lỗi `429`, đừng cúp máy ngang. Cực kỳ lịch sự và chuẩn mực nếu bạn gửi kèm các HTTP Header:
   - `X-RateLimit-Limit: 100` (Mày được cấp tối đa 100).
   - `X-RateLimit-Remaining: 0` (Mày xài hết rồi).
   - `Retry-After: 30` (Vui lòng đi ngủ và gọi lại sau 30 giây nữa, tao sẽ mở khóa).
2. **Dùng Redis (Tốc độ cao)**: Để đếm số lượng Request của hàng triệu User, Database SQL sẽ chết ngắc vì không đủ tốc độ. Bắt buộc phải dùng bộ nhớ In-Memory cực nhanh như Redis (Lệnh `INCR` và `EXPIRE`) để lưu trữ cái bộ đếm này.

</details>

1. **Provide Informative HTTP Headers (The Etiquette)**: Blindly returning a `429 Too Many Requests` is hostile developer experience. A robust API MUST return standard Rate Limit HTTP Headers to allow the Client to programmatically back off.
   - `X-RateLimit-Limit: 60` (Your maximum quota).
   - `X-RateLimit-Remaining: 0` (You are out of tokens).
   - `Retry-After: 15` (Crucial: Tells the Client's `setTimeout` exactly how many seconds to wait before attempting the next request).
2. **Distributed Counters (Redis)**: If you have 5 Application Servers, you cannot use an in-memory variable (like a Java `HashMap`) to count requests. If a hacker hits Server 1, then Server 2, they bypass local limits. You MUST use a centralized, blistering fast In-Memory store like Redis. The App executes an atomic `INCR user_id:throttle` and sets a TTL (`EXPIRE`). Redis handles 100,000 Ops/sec effortlessly, providing a globally accurate counter for the entire cluster.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Chặn nhầm IP (NAT Gateway / Quán Cafe)**: Một sai lầm khủng khiếp của Junior Dev là Rate Limit cứng ngắc theo IP (Ví dụ: 1 IP chỉ được mở web 10 lần/phút). Bạn mang Laptop ra quán The Coffee House. Quán có 100 người xài chung 1 mạng Wifi (Chung 1 IP Public do NAT). Chỉ cần 10 người mở web của bạn lên, hệ thống của bạn nhận diện "1 IP gọi 10 lần" $\rightarrow$ Khóa IP. Kết quả: Toàn bộ 100 người trong quán Cafe đó bị chặn không vào được web của bạn nữa.
   - *Cách giải quyết*: Đừng bao giờ Rate Limit dựa hoàn toàn vào IP. Trừ những API vãng lai không đăng nhập. Nếu khách ĐÃ ĐĂNG NHẬP, bắt buộc phải Rate Limit theo `User_ID` (Hoặc Token). Dù 100 người dùng chung IP quán Cafe, họ xài 100 cái User_ID khác nhau thì vẫn được cho qua.

</details>

1. **The Shared IP Catastrophe (NAT Issues)**: The most destructive architectural oversight. A junior architect strictly Rate Limits by `Client_IP` (e.g., 50 req/min/IP). However, IPv4 exhaustion forces ISPs and Corporations to heavily utilize NAT (Network Address Translation). An entire University campus with 5,000 students might appear to the Internet as a single Public IP address. If 5 students use your app, they hit the 50 req/min limit. The other 4,995 students on campus are now permanently blocked with `429` errors.
   - *The Fix*: Never rely exclusively on IP addresses. For authenticated routes, you MUST rate limit strictly based on the `Authorization: Bearer <Token>` or the decoded `user_id`. If they are anonymous, augment the IP with Browser Fingerprinting or Session Cookies.
2. **The Redis Bottleneck**: You introduce Redis to hold the rate-limit counters. Suddenly, every single incoming HTTP request requires a synchronous network call to Redis *before* processing the logic. You have accidentally introduced a single point of failure and added 2ms latency to every request. If Redis goes down, your entire API goes down. **Fix**: Rate Limit checks must Fail-Open. If the Redis socket times out, the code should catch the exception, bypass the limit, and allow the request through to preserve availability, prioritizing uptime over strict quota enforcement.

---

## Related Topics

- For how multiple servers process these requests, read **[Load Balancing](./load-balancing.md)**.
- For protecting upstream services from failing, read about **[Circuit Breaker](../resilience/circuit-breaker.md)**.
- For protecting distributed transactions, review **[Saga Pattern](../event-driven/saga.md)**.
