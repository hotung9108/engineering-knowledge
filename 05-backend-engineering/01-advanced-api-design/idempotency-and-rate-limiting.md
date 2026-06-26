# Idempotency & Rate Limiting

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Kỹ thuật thiết yếu để thiết kế API mạnh mẽ có thể xử lý an toàn các request trùng lặp (Idempotency - Tính lũy đẳng) và bảo vệ hệ thống khỏi tình trạng quá tải (Rate Limiting - Giới hạn tỷ lệ).

</details>

> **Summary**: Essential techniques for designing robust APIs that can safely handle duplicate requests (Idempotency) and protect systems from overload (Rate Limiting).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Idempotency (Tính lũy đẳng)**: Tưởng tượng nút "Gọi Thang Máy". Bạn bấm 1 lần hay bấm liên tục 10 lần thì kết quả vẫn chỉ là 1 cái thang máy chạy tới đón bạn. Thang máy không bao giờ mang tới 10 cái lồng sắt chỉ vì bạn lỡ tay bấm 10 lần. API cũng phải như vậy: Bấm nút "Thanh Toán" 10 lần do mạng lag thì hệ thống cũng chỉ trừ tiền 1 lần.
- **Rate Limiting (Giới hạn tỷ lệ)**: Tưởng tượng một quán phở rất ngon nhưng chỉ có 1 bác đầu bếp. Nếu 100 khách ùa vào đòi ăn ngay cùng lúc, bác đầu bếp sẽ ngất xỉu. Giải pháp: Phát cho mỗi người 1 cái vé số. Một phút bác chỉ phục vụ đúng 5 vé. Ai hết vé thì mời đứng đợi ngoài cửa. Hệ thống máy chủ sẽ được cứu!

</details>

- **Idempotency**: Imagine an elevator call button. Whether you press it once or smash it 10 times, the result is the same: one elevator arrives to pick you up. The system doesn't send 10 elevators just because you pressed it 10 times. APIs must behave similarly: If a user clicks "Pay" 10 times because their internet is lagging, the system should only charge them once.
- **Rate Limiting**: Imagine a popular noodle shop with only one chef. If 100 customers rush in and demand food all at once, the chef will pass out. Solution: Hand out tickets. The chef only serves 5 tickets per minute. Anyone without a ticket waits outside. This saves the server from crashing!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Idempotency**: Một thuộc tính của API nơi mà việc gọi một request nhiều lần sẽ mang lại kết quả y hệt như gọi một lần. REST định nghĩa `GET`, `PUT`, và `DELETE` sinh ra đã có sẵn tính lũy đẳng, trong khi `POST` thì không.
- **Rate Limiting**: Cơ chế kiểm soát tốc độ lưu lượng mạng gửi hoặc nhận của một API. Nó áp đặt một hạn ngạch (quota) nghiêm ngặt (ví dụ: 100 request / phút / người dùng).

**Phân loại:**
- **Loại**: Mẫu kiến trúc Backend / API Gateway.
- **Thuật toán (Rate Limiting)**: Token Bucket, Leaky Bucket, Fixed Window, Sliding Window.
- **Lớp triển khai**: Thường nằm ở tầng API Gateway (Kong, AWS API Gateway) hoặc dùng Redis ở tầng Application.

</details>

- **Idempotency**: A property of an API endpoint where making multiple identical requests has the same effect as making a single request. REST defines `GET`, `PUT`, and `DELETE` as naturally idempotent, while `POST` is not.
- **Rate Limiting**: A mechanism to control the rate of traffic sent or received by a network interface or API. It enforces a strict quota (e.g., 100 requests per minute per user).

### Classification
- **Type**: API Gateway / Backend Architecture Patterns.
- **Algorithms (Rate Limiting)**: Token Bucket, Leaky Bucket, Fixed Window, Sliding Window.
- **Implementation Layer**: Typically handled at the API Gateway (Kong, AWS API Gateway) or via Redis at the application layer.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề nếu thiếu Idempotency**
Trong hệ thống mạng, kết nối luôn thiếu ổn định. Nếu điện thoại gửi lệnh `POST /payments`, máy chủ xử lý trừ tiền thành công nhưng đang trả kết quả về thì rớt mạng. Điện thoại tưởng lỗi nên gửi lại lệnh trừ tiền lần nữa. Thiếu Idempotency, khách hàng sẽ bị trừ tiền 2 lần.

**Vấn đề nếu thiếu Rate Limiting**
Nếu không có giới hạn, một người dùng ác ý (hoặc code bị lỗi tạo vòng lặp vô hạn) có thể bắn hàng triệu request vào API của bạn. Nó sẽ vắt kiệt CPU và Database, làm sập toàn bộ hệ thống, khiến những khách hàng khác không thể sử dụng (Vấn đề Hàng xóm ồn ào - Noisy Neighbor).

</details>

### The Problem without Idempotency
In distributed systems, networks are unreliable. If a client sends a `POST /payments` request, the server processes the payment but fails to send the HTTP 200 response due to a network timeout. The client retries the exact same request. Without idempotency, the user is charged twice.

### The Problem without Rate Limiting
Without strict limits, a single misconfigured client (or a malicious actor) can flood your API with requests, consuming all database connections and CPU, causing a total system outage for all other customers (Noisy Neighbor problem).

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu không có Idempotency: API Thanh toán cực kỳ nguy hiểm. Gửi lại request = Trừ tiền lần nữa.
Nếu có Idempotency: API yêu cầu một cái "Mã Hóa Đơn" (Idempotency-Key). Nó dùng mã đó lưu vào Redis. Lần sau gửi đúng mã đó lên, hệ thống phát hiện ra ngay và chỉ trả về kết quả cũ.

</details>

### Without Idempotency (Vulnerable Payment API)
```java
@PostMapping("/pay")
public PaymentResponse charge(@RequestBody PaymentRequest req) {
    // If client retries due to network timeout, they get charged multiple times!
    return paymentService.process(req.getAmount(), req.getUserId());
}
```

### With Idempotency (Safe Payment API)
```java
@PostMapping("/pay")
public PaymentResponse charge(
        @RequestHeader("Idempotency-Key") String idempotencyKey,
        @RequestBody PaymentRequest req) {
    
    // Check if we already processed this exact key
    if (redisCache.exists(idempotencyKey)) {
        return redisCache.get(idempotencyKey); // Return cached response safely
    }

    // Process and cache the result
    PaymentResponse response = paymentService.process(req.getAmount(), req.getUserId());
    redisCache.put(idempotencyKey, response, Duration.ofHours(24));
    
    return response;
}
```

| Aspect | Without | With (Idempotency & Rate Limiting) |
|---|---|---|
| Safe Retries | No (causes duplicate data) | Yes (safe to retry infinitely) |
| System Protection | Vulnerable to DDoS & Overload | Protected by strict quotas |
| Complexity | Low | Medium (requires Redis or database locking) |
| Client DX | Poor (must handle ambiguous timeouts manually) | Excellent (can safely auto-retry on 5xx) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Idempotency**
1. **Xử lý thanh toán**: Stripe bắt buộc bạn phải truyền header `Idempotency-Key` cho mọi thao tác `POST`.
2. **Tạo đơn hàng**: Chống tạo 2 đơn nếu người dùng click đúp (double-click) nút "Mua hàng".
3. **Webhooks**: Xử lý an toàn các luồng webhook vì các hệ thống ngoài (GitHub, Stripe) thường gửi cùng 1 webhook nhiều lần để đảm bảo không bị sót.

**Rate Limiting**
1. **API Công khai**: Chia gói giá (Gói Free: 100 req/phút, Gói Pro: 1000 req/phút).
2. **Đăng nhập**: Giới hạn số lần thử mật khẩu sai để chống Brute-force.
3. **Chức năng hao tài nguyên**: Đặt giới hạn gắt gao cho các thao tác xuất PDF hoặc AI suy luận.

**Không nên làm**:
- Dùng khóa Unique DB để làm Idempotency. Nó chặn trùng lặp nhưng lại quăng lỗi 500. Một API chuẩn phải trả về kết quả y chang lần 1 (200 OK) chứ không phải báo lỗi.

</details>

### Idempotency
1. **Payment Processing**: Stripe requires an `Idempotency-Key` header for all `POST` requests.
2. **Order Creation**: Preventing duplicate e-commerce orders if the user double-clicks the checkout button.
3. **Webhooks**: Handling webhooks safely, as providers (like GitHub or Stripe) guarantee "at least once" delivery, meaning you will often receive the same webhook twice.

### Rate Limiting
1. **Public APIs**: Offering Free (100 req/min) and Pro (1000 req/min) pricing tiers.
2. **Login Endpoints**: Preventing brute-force password guessing.
3. **Resource-Heavy Endpoints**: Limiting expensive operations like PDF generation or AI model inference.

### Anti-Patterns
- **Relying on DB Unique Constraints for Idempotency**: While a `UNIQUE` constraint prevents duplicates, it throws a 500/409 error on retry. A true idempotent endpoint should return the *same successful response* as the original request, not an error.
- **In-Memory Rate Limiting in Distributed Systems**: Using `ConcurrentHashMap` for rate limiting fails when you run multiple instances of your app behind a Load Balancer. You must use Redis.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn Idempotency**:
1. Client (Mobile/Web) phải là người tự sinh ra một mã UUID v4 và nhét vào header `Idempotency-Key`.
2. Phải khóa (Distributed Lock) request. Nếu 2 request y hệt nhau bay tới server cách nhau đúng 1 phần nghìn giây, bạn phải khóa 1 cái lại bắt đợi, nếu không hàm xử lý tiền sẽ chạy 2 lần song song. Redisson là thư viện tuyệt vời cho việc này.
3. Cache kết quả trong 24 giờ là chuẩn chung.

**Thực tiễn Rate Limiting**:
1. Khi chặn, LUÔN LUÔN trả về mã HTTP `429 Too Many Requests`.
2. Phải có Headers báo tình trạng: `X-RateLimit-Limit` (Tổng số), `X-RateLimit-Remaining` (Còn lại), `X-RateLimit-Reset` (Mấy giờ thì được gửi tiếp).

</details>

### Best Practices for Idempotency
1. **Idempotency Key Generation**: Clients should generate a V4 UUID and send it in the `Idempotency-Key` header.
2. **Payload Hashing**: If a client sends the same key but a *different* payload, reject the request with HTTP 400. Idempotency keys map 1:1 to a specific payload.
3. **Distributed Locks**: You must acquire a distributed lock (e.g., Redisson) when processing the request. If two requests with the same key arrive at the exact same millisecond, you must block one while the other processes to prevent race conditions.
4. **Lifecycle**: Idempotency keys should expire. 24 hours is standard for payment APIs.

### Best Practices for Rate Limiting
1. **Return HTTP 429**: When a limit is breached, always return `429 Too Many Requests`.
2. **Rate Limit Headers**: Always include standard headers so clients know when to retry:
   - `X-RateLimit-Limit`: The quota.
   - `X-RateLimit-Remaining`: Remaining quota.
   - `X-RateLimit-Reset`: Unix timestamp when the quota resets.
3. **Algorithm Selection**: Token Bucket is generally preferred for APIs as it allows for small bursts of traffic, unlike Fixed Window which can cause stampedes at the top of the minute.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Sử dụng Spring Boot Interceptor để chặn ở cửa ngõ. Lệnh `setIfAbsent` (hay `SETNX` trong Redis) là chìa khóa vàng: Nó vừa ghi vào Redis vừa kiểm tra xem đã có ai ghi trước đó chưa trong 1 thao tác duy nhất (Atomic), giúp chặn đứng Race Condition.

</details>

### Advanced Redis-based Idempotency Interceptor (Spring Boot)

```java
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.data.redis.core.StringRedisTemplate;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.time.Duration;

@Component
public class IdempotencyInterceptor implements HandlerInterceptor {

    private final StringRedisTemplate redisTemplate;

    public IdempotencyInterceptor(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if (!request.getMethod().equals("POST")) {
            return true; // Only intercept POST requests
        }

        String idempotencyKey = request.getHeader("Idempotency-Key");
        if (idempotencyKey == null) {
            response.sendError(400, "Idempotency-Key header is required");
            return false;
        }

        String redisKey = "idemp:" + idempotencyKey;
        
        // Use SETNX (Set if Not eXists) for atomic locking
        Boolean isNewRequest = redisTemplate.opsForValue()
            .setIfAbsent(redisKey, "PROCESSING", Duration.ofHours(24));

        if (Boolean.FALSE.equals(isNewRequest)) {
            String status = redisTemplate.opsForValue().get(redisKey);
            if ("PROCESSING".equals(status)) {
                response.sendError(409, "Concurrent request is already processing");
                return false;
            } else {
                // Return cached response (In production, cache the full JSON response)
                response.setStatus(200);
                response.getWriter().write(status);
                return false;
            }
        }

        return true;
    }
}
```

### Rate Limiting with Resilience4j (Spring Boot)

```yaml
# application.yml
resilience4j.ratelimiter:
  instances:
    api-gateway:
      limitForPeriod: 10
      limitRefreshPeriod: 1s
      timeoutDuration: 0
```

```java
import io.github.resilience4j.ratelimiter.annotation.RateLimiter;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HighTrafficController {

    @GetMapping("/api/resource")
    @RateLimiter(name = "api-gateway", fallbackMethod = "rateLimitFallback")
    public String getResource() {
        return "Resource data";
    }

    public String rateLimitFallback(Exception e) {
        // Automatically invoked when rate limit is exceeded
        return "HTTP 429: Too Many Requests. Please try again later.";
    }
}
```

---

## Related Topics

- [Advanced Redis Patterns](../03-high-performance-data/advanced-redis-patterns.md) — For deep dives into SETNX and Redisson distributed locks.
- [Transactional Outbox Pattern](../04-distributed-async/transactional-outbox-pattern.md) — Ensures events are emitted reliably, complementing idempotency.
