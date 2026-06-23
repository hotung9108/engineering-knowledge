# Resilience Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Khả năng mở rộng (Scalability) là việc thuê thêm người khi quán đông khách, thì **Sức bật (Resilience - Tính kiên cường)** là việc quán vẫn có thể bán được hàng ngay cả khi 3 ông đầu bếp đột quỵ, cúp điện toàn khu phố, và xe chở thịt bị tai nạn. Trong hệ thống phân tán, MẠNG LUÔN LUÔN RỚT và PHẦN CỨNG LUÔN LUÔN HỎNG. Chấp nhận điều đó và thiết kế hệ thống sao cho nó "Hỏng một nửa nhưng vẫn xài được" (Graceful Degradation), thay vì chết chùm toàn bộ, đó chính là Resilience.

</details>

> **Summary**: While Scalability focuses on accommodating hyper-growth, **Resilience (Fault Tolerance)** focuses on surviving hyper-catastrophe. In a distributed architecture (Microservices, Cloud Native), hardware failure and network partitions are not rare exceptions; they are guaranteed, mathematical certainties. An API call traversing 10 microservices will inevitably encounter a dropped packet, a crashed container, or a massive latency spike. Resilience is the architectural engineering discipline of explicitly designing software to anticipate, absorb, and gracefully recover from these ubiquitous failures without causing a cascading, systemic collapse.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một con tàu biển chở khách.
1. **Thiếu Resilience (Tàu Titanic)**: Tàu rất to, rất nhanh (Scalable). Nhưng khoang chứa nước ở dưới đáy thông với nhau. Khi tàu đâm phải băng, nước tràn vào 1 khoang, nó sẽ chảy tràn sang tất cả các khoang khác. Cuối cùng tàu chìm nghỉm. (Lỗi dây chuyền - Cascading Failure).
2. **Có Resilience (Tàu ngầm hiện đại)**: Dưới đáy tàu được chia thành 20 khoang độc lập, có cửa sắt đóng kín (Bulkhead). Đâm phải đá tảng, 2 khoang bị ngập nước. Cửa sắt lập tức đóng sập lại. 18 khoang kia vẫn khô ráo. Con tàu sẽ chạy chậm đi một chút (Degradation), nhưng nó tuyệt đối không bao giờ chìm. Mọi người vẫn sống sót trở về.

</details>

Imagine a large ocean vessel.
1. **Fragile Architecture (The Titanic)**: The ship is incredibly fast and holds thousands of passengers (Highly Scalable). However, the watertight compartments at the bottom do not reach all the way to the ceiling. When the hull hits an iceberg, water fills one compartment, spills over the top into the next, and the next. The entire ship sinks. This is a **Cascading Failure**.
2. **Resilient Architecture (A Submarine)**: The hull is rigorously divided into 20 strictly sealed, independent compartments (Bulkheads). A torpedo blows a hole in Compartment #3. Water rushes in. The heavy steel doors seal shut instantly. Compartment #3 is completely destroyed. However, the other 19 compartments remain perfectly dry. The submarine loses some speed (Graceful Degradation), but it survives and returns home.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Resilience không phải là một thuật toán, nó là sự kết hợp của 4 "Tấm Khiên Bảo Vệ" bắt buộc phải có trong code:
1. **Timeouts (Ngắt kết nối)**: Đừng bao giờ gọi API mà đợi vô tận. 3 giây không trả lời là phải tự cúp máy ngay.
2. **Retries (Gọi lại)**: Do mạng hay chập chờn mili-giây. Cúp máy xong thì thử gọi lại 1-2 lần xem sao. Nhưng phải chờ lâu dần (Exponential Backoff) chứ đừng nháy máy liên tục.
3. **Circuit Breaker (Cầu dao điện)**: Nếu gọi 5 lần mà cái API bên kia đều báo lỗi, chứng tỏ máy chủ bên đó cháy rồi. Cúp Cầu Dao! Đừng có cố gọi nữa để cho nó thở.
4. **Bulkhead (Vách ngăn cách thủy)**: Chia RAM/CPU ra. Giới hạn tính năng X chỉ được xài tối đa 30% RAM. Tránh việc tính năng X bị lỗi nuốt sạch 100% RAM làm tính năng Y cũng chết theo.

</details>

Resilience is structurally implemented via four mandatory defensive Design Patterns:
1. **Strict Timeouts**: Never, ever execute a synchronous network call with an infinite timeout. If the downstream service freezes, your thread freezes. Enforce strict millisecond SLA timeouts.
2. **Intelligent Retries**: Network packets drop randomly. A failed HTTP request might succeed if re-attempted 100ms later. Implement retries, but strictly use **Exponential Backoff with Jitter** to avoid DDoSing the recovering server.
3. **The Circuit Breaker**: If Service A calls Service B and it fails 10 times in a row, Service B is clearly dead. Service A must instantly "Trip the Breaker" and stop calling B entirely, returning a cached/fallback response to give B time to reboot.
4. **Bulkheads**: Isolate resources. If the `ImageUploadService` memory leaks and crashes, it should not consume the thread pool required by the `LoginService`. Hard-cap thread pools per domain.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong hệ thống lớn (Microservices), sự nguy hiểm không đến từ máy chủ bị sập, mà đến từ máy chủ bị **CHẬM**.
Ví dụ: Service A (Giao diện) gọi Service B (Thanh toán). Bình thường mất 10ms.
Hôm nay, Database của B bị nghẽn, B mất 30 giây mới trả lời.
Nếu không có Resilience (Không có Timeout): 10.000 khách hàng bấm nút Thanh toán. 10.000 kết nối từ A mở ra và ĐỨNG CHỜ B trong 30 giây. Máy chủ A cạn kiệt toàn bộ RAM và Thread Pool để "chờ đợi". Hệ quả: A sập! Toàn bộ website trắng xóa không ai vào được, dù lỗi ban đầu chỉ là do B bị chậm. Đó gọi là Lỗi Dây Chuyền (Cascading Failure).
Resilience sinh ra để cầm cây kéo, cắt phăng sự liên kết đó, hy sinh thằng B để cứu sống thằng A.

</details>

In a Microservice architecture, the most dangerous failure mode is not a hard crash; it is **Latency**.
Consider: Service A (Gateway) synchronously calls Service B (Inventory). Normal latency is `10ms`.
Suddenly, Service B experiences a database lock. Its latency degrades to `30,000ms` (30 seconds).
If Service A lacks Resilience (No Timeouts configured): 5,000 users click "Buy". Service A opens 5,000 TCP sockets to Service B. Because B takes 30 seconds to reply, Service A holds those 5,000 threads open. Within seconds, Service A completely exhausts its Thread Pool and runs out of RAM. Service A crashes violently. The entire website goes offline.
The root cause was B, but the victim was A. This is a **Cascading Failure**. Resilience patterns (Timeouts, Circuit Breakers) act as structural fuses. They detect B's latency and intentionally amputate the connection to B, returning an immediate error to the user, strictly to ensure Service A's survival.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cảnh tượng khi Service "Gợi ý mua hàng" bị sập trên Shopee.
</details>

Visualizing a localized failure: The "Recommended Products" microservice dies.

| Metric | Monolithic/Fragile Architecture | Resilient Architecture (Circuit Breaker) |
|---|---|---|
| **Impact of Failure** | The entire Homepage fails to load. | The Homepage loads perfectly. |
| **User Experience** | White screen of death (Error 500). | The "Recommended" box is simply empty (Graceful Degradation). |
| **Upstream Services** | Blocked, waiting for recommendations. | Instantly returns a default/empty list. |
| **Recovery Speed**| Slow. Requires manual rebooting. | Fast. System auto-recovers when the service reboots. |
| **System Philosophy**| Perfection (Everything must work). | Pragmatism (Partial functionality is acceptable). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Service Mesh (Istio / Linkerd)**: Ngày xưa Lập trình viên phải tự viết code Timeout, Retry bằng Java/Go. Giờ đây, khi xài Kubernetes, hệ thống Service Mesh đứng ở ngoài sẽ TỰ ĐỘNG ngắt Cầu dao, tự động Retry giùm bạn. Lập trình viên không cần quan tâm đến Resilience nữa.
2. **Hệ thống Thanh toán Ngoại vi (Stripe/PayPal)**: Bạn không kiểm soát được server của Paypal. Nếu Paypal bảo trì, web của bạn không được phép chết. Bạn phải dùng Circuit Breaker: Khi Paypal chết $\rightarrow$ Ngắt cầu dao $\rightarrow$ Nút Paypal trên web lập tức bị Ẩn đi, chuyển sang trạng thái "Bảo trì", chỉ cho phép khách xài Momo.
3. **Netflix Chaos Monkey**: Netflix cố tình viết ra một con Bot tên là "Khỉ quậy phá". Con khỉ này sẽ đi dạo trong mạng LAN của Netflix và RÚT ĐIỆN các máy chủ một cách ngẫu nhiên vào lúc nửa đêm. Nhờ vậy, kỹ sư của Netflix BẮT BUỘC phải viết code Resilience hoàn hảo để phim vẫn chạy mượt dù máy chủ chết liên tục.

</details>

1. **Service Mesh (Istio / Envoy)**: Historically, developers explicitly authored Circuit Breaker logic within the application code using libraries like Netflix Hystrix or Resilience4j. Modern Cloud-Native architectures push this responsibility to the Infrastructure layer. A Service Mesh injects an Envoy proxy sidecar into every K8s Pod. Envoy intercepts all outbound HTTP calls and transparently applies Timeouts, Retries, and Circuit Breaking without altering a single line of application code.
2. **External 3rd-Party Integrations**: Your E-commerce core relies on an external logistics API (FedEx) to calculate shipping rates. You have zero control over FedEx's uptime. If FedEx goes offline, your Checkout cannot freeze. Resilience mandates a Fallback: The Circuit Breaker trips, and the system seamlessly defaults to a hardcoded "Standard Shipping: $5" flat rate. Business continues uninterrupted (Graceful Degradation).
3. **Chaos Engineering (Netflix Chaos Monkey)**: The ultimate test of Resilience. Netflix engineers created a software daemon that actively roams their production AWS environment, intentionally terminating EC2 instances and severing network cables during peak business hours. This forces engineers to architect systems that are intrinsically self-healing. If you know a monkey is pulling cables, you build a resilient system.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Luôn có kế hoạch B (Fallback)**: Cúp cầu dao (Circuit Breaker) báo lỗi là tốt, nhưng chưa đủ. Phải code "Phương án dự phòng". Ví dụ gọi API lấy "Danh sách phim hot" bị lỗi $\rightarrow$ Phương án B: Trả về Danh sách phim lưu trong ổ cứng (Dù hơi cũ nhưng khách vẫn có cái để xem).
2. **Chiến lược Retry khôn ngoan**: Không bao giờ Retry ngay lập tức. Nếu API bên kia đang sập vì quá tải, bạn gọi lại ngay lập tức là bạn đang bồi thêm 1 đao (DDoS) giết chết nó luôn. Bắt buộc dùng **Exponential Backoff**: Lần 1 chờ 1s, lần 2 chờ 2s, lần 3 chờ 4s, lần 4 chờ 8s.

</details>

1. **Explicit Fallback Mechanisms**: Tripping a Circuit Breaker prevents cascading failure, but returning an `HTTP 500` to the Frontend is still a poor UX. Resilient methods MUST define a deterministic Fallback path. If the `PersonalizedRecommendationService` times out, the `catch()` block should not throw an error; it should execute a Redis query to return the generic, pre-computed `Top_10_Trending_Items`. The user never realizes a failure occurred.
2. **Exponential Backoff & Jitter**: A critical networking mandate. If Service B is overloaded and drops 500 connections, and all 500 clients instantly execute a `while(true) retry()` loop at the exact same millisecond, they will unintentionally execute a massive DDoS attack, ensuring Service B never recovers. Retries MUST be delayed exponentially (Wait 1s, then 2s, then 4s). Furthermore, you must add **Jitter** (Randomized variation: Wait 1.1s, then 2.4s) to spread the retry spikes evenly across the timeline.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Retry những API không được phép Retry**: Hàm `Thanh_Toan_Momo()` bị Timeout (Bạn không biết là tiền đã trừ hay chưa do mất kết nối mạng). Bạn ngu ngốc cấu hình tự động Retry gọi lại 3 lần. Kết quả: Khách hàng bị trừ tiền 3 lần!
   - *Luật*: CHỈ ĐƯỢC PHÉP cấu hình Retry cho các hàm GET (Lấy dữ liệu). Tuyệt đối cấm Retry các hàm POST/Cập nhật dữ liệu, trừ khi API bên kia có hỗ trợ tính năng **Idempotency Key** (Key chống trùng lặp).
2. **Cấu hình Timeout quá dài**: Lập trình viên thường sợ lỗi nên setup "Timeout: 60 giây" cho nó chắc cú. Trong thế giới Web/App, người dùng chờ 5 giây là họ đã F5 hoặc chửi rồi. 60 giây là con số chết người khiến hệ thống cạn kiệt RAM vì phải "ôm" kết nối quá lâu. Hãy set Timeout tối đa là 3-5 giây cho API thường.

</details>

1. **Blindly Retrying Non-Idempotent Mutations**: The most destructive mistake in distributed engineering. An API call to `POST /charge_credit_card` encounters a network timeout. The client does not know if the Server processed the charge before the packet dropped. If the client blindly executes a Retry, they might charge the customer a second time. **Absolute Rule**: You may safely Retry `GET`, `PUT`, and `DELETE` requests natively. You must NEVER blindly retry a `POST` request unless the payload contains a strictly enforced cryptographic `Idempotency-Key` that the backend database verifies.
2. **Overly Generous Timeouts**: Junior developers encounter a `SocketTimeoutException` and "fix" it by aggressively increasing the HTTP client timeout from `3000ms` to `60000ms` (60 seconds) to "give it more time". This mathematically guarantees a Cascading Failure during a latency spike. If a human user is waiting for a web page, their psychological threshold is 3 seconds. Holding a backend Java Thread open for 60 seconds is a horrific waste of RAM for a user who already closed the browser tab. Timeouts should be viciously short (e.g., the 99th percentile response time + 50ms).

---

## Related Topics

- For the specific mechanism of stopping the bleeding, read **[Circuit Breaker](./circuit-breaker.md)**.
- For the correct way to try again, read **[Retries & Backoff](./retries.md)**.
- For managing these rules without code, see **[Service Mesh (Istio)](../../03-technologies/cloud-infrastructure/kubernetes.md)**.
