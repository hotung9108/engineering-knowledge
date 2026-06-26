# Advanced Redis Patterns

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Các chiến lược để sử dụng Redis trong các hệ thống tải cao, giảm thiểu các lỗi liên quan đến cache (Cache Stampede, Cache Penetration), triển khai Khóa phân tán (Distributed Locks) và sử dụng các Cấu trúc dữ liệu xác suất (Probabilistic Data Structures).

</details>

> **Summary**: Strategies for using Redis in high-throughput environments, mitigating cache failures (Cache Stampede, Cache Penetration), implementing Distributed Locks, and utilizing Probabilistic Data Structures.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Cache Stampede (Giẫm đạp lên nhau)**: Tưởng tượng một tờ giấy thi dán trên bảng tin. 10.000 học sinh đang xem tờ giấy đó. Đột nhiên tờ giấy bị rớt xuống (Cache hết hạn). Cả 10.000 học sinh cùng một lúc chạy ùa vào phòng thầy giáo (Database) để xin tờ mới. Thầy giáo sẽ chết ngất! Giải pháp: Dùng "Ổ khóa". Chỉ cho đúng 1 lớp trưởng vào xin thầy, 9.999 bạn kia đứng ngoài cửa chờ lớp trưởng mang tờ giấy mới dán lên.
- **Cache Penetration (Xuyên thủng)**: Ai đó liên tục hỏi bạn: "Sản phẩm mã số -999 có không?". Bạn tìm trong kho phụ (Redis) không thấy, bèn lóc cóc chạy vào kho chính (Database) tìm cũng không có. Ngày mai họ lại hỏi tiếp, bạn lại chạy vào kho chính. Cứ thế kho chính bị kiệt sức. Giải pháp: Nhớ luôn câu trả lời "Không có" vào kho phụ. Lần sau họ hỏi, bạn trả lời ngay "Không có" mà khỏi cần đi tìm.

</details>

- **Cache Stampede (Thundering Herd)**: Imagine an exam result sheet pinned to a noticeboard. 10,000 students are looking at it. Suddenly, the sheet falls down (Cache expires). All 10,000 students rush into the teacher's office (Database) at the exact same time to ask for a new copy. The teacher will faint! Solution: Use a "Lock". Only allow the class president to enter the office to get a new copy, while the other 9,999 wait outside until it's pinned back up.
- **Cache Penetration**: Someone keeps asking you: "Do you have product ID -999?". You check your quick-access shelf (Redis) and don't see it, so you walk all the way to the main warehouse (Database) and don't find it there either. Tomorrow they ask again, and you walk to the warehouse again. The warehouse gets exhausted. Solution: Memorize the answer "No" and put it on the quick-access shelf. Next time they ask, you instantly say "No" without walking.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Khóa phân tán (Distributed Locks)**: Cơ chế đảm bảo rằng các thao tác xung đột không được chạy song song trên nhiều máy chủ độc lập.
- **Cache Stampede (Dẫm đạp)**: Xảy ra khi một key cực kỳ phổ biến bị hết hạn (expire) và hàng ngàn request cùng lúc lao vào Database để lấy lại dữ liệu đó.
- **Cache Penetration (Xuyên thủng)**: Xảy ra khi hacker cố tình gọi các ID không tồn tại (ví dụ `id=-1`). Vì nó không có thật, nó không bao giờ được lưu vào Cache, nên mọi request đều đánh thẳng vào Database.
- **Bloom Filters**: Một cấu trúc dữ liệu xác suất siêu tiết kiệm RAM, dùng để trả lời câu hỏi: "Phần tử này có tồn tại không?" (Nó sẽ trả lời: "Chắc chắn KHÔNG" hoặc "Có thể CÓ").

**Phân loại:**
- **Loại**: Chiến lược Caching / Hệ thống phân tán.
- **Công nghệ**: Redis, Redisson (Thư viện cho Java).

</details>

- **Distributed Locks**: A mechanism ensuring that mutually exclusive operations are not executed concurrently across a cluster of independent nodes.
- **Cache Stampede (Thundering Herd)**: Occurs when a highly popular cache key expires, and thousands of concurrent requests all hit the database simultaneously to regenerate the cache.
- **Cache Penetration**: Occurs when attackers request non-existent keys (e.g., `id=-1`), bypassing the cache and hitting the database on every request.
- **Bloom Filters**: A highly space-efficient probabilistic data structure used to test whether an element is a member of a set (returns "Possibly in set" or "Definitely not in set").

### Classification
- **Type**: Caching Strategies / Distributed Systems Patterns.
- **Technology**: Redis, Redisson (Java Client).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Chỉ dùng lệnh `GET` và `SET` trong Redis là không đủ cho các hệ thống lớn.
- Nếu bạn có sự kiện Flash Sale và key "Tồn kho" bị hết hạn, 10.000 luồng (threads) sẽ cùng chọc vào SQL Database để truy vấn số lượng tồn kho. CPU của Database sẽ nhảy lên 100% và sập hệ thống dây chuyền.
- Nếu bạn có 10 máy chủ (instances) cùng chạy một lệnh hẹn giờ (`Cron Job`) lúc 00:00, cả 10 máy sẽ cùng thực hiện công việc đó trừ khi bạn dùng Khóa phân tán để ép chúng phải nhường nhau (chỉ 1 máy được chạy).

</details>

Standard `GET` and `SET` operations in Redis are insufficient for production systems. 
- If a flash sale goes live and the "Available Stock" cache key expires, 10,000 concurrent requests will hit the SQL database to fetch the stock. The database CPU will spike to 100%, causing a cascading failure. 
- If multiple application instances try to run a scheduled cron job at `00:00`, they will all execute it unless a Distributed Lock coordinates them.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có biện pháp phòng ngừa: Code đơn giản kiểm tra cache, nếu rỗng thì query DB. Dẫn đến sập DB nếu hàng ngàn người cùng gọi hàm này lúc cache vừa hết hạn.
Có khóa Redisson: Bọc đoạn gọi DB bằng một `Lock`. Trong 10.000 luồng, chỉ có 1 luồng duy nhất lấy được khóa để chọc vào DB. 9.999 luồng còn lại sẽ bị chặn lại và đứng chờ.

</details>

### Without Mitigation (Vulnerable to Cache Stampede)
```java
public Product getProduct(String id) {
    Product p = redisCache.get(id);
    if (p == null) {
        // VULNERABLE: If the cache expires, 10,000 threads will run this query simultaneously!
        p = database.findById(id); 
        redisCache.set(id, p, 10, TimeUnit.MINUTES);
    }
    return p;
}
```

### With Redisson Distributed Lock (Stampede Prevented)
```java
public Product getProduct(String id) {
    Product p = redisCache.get(id);
    if (p == null) {
        RLock lock = redissonClient.getLock("lock:product:" + id);
        try {
            // Only ONE thread out of 10,000 acquires this lock
            if (lock.tryLock(5, 5, TimeUnit.SECONDS)) { 
                p = redisCache.get(id); // Double-check pattern
                if (p == null) {
                    p = database.findById(id); // Only 1 database query runs
                    redisCache.set(id, p, 10, TimeUnit.MINUTES);
                }
            } else {
                // The other 9,999 threads fail to get the lock, wait a bit, and fetch from cache
                Thread.sleep(100);
                return redisCache.get(id); 
            }
        } finally {
            if (lock.isHeldByCurrentThread()) lock.unlock();
        }
    }
    return p;
}
```

| Threat | Definition | Mitigation Strategy |
|---|---|---|
| **Cache Stampede** | Hot key expires; concurrent requests crush the DB. | Distributed Locks (Redisson Mutex). |
| **Cache Penetration** | Requests for keys that don't exist in DB. | Bloom Filters or caching `null` values. |
| **Cache Avalanche** | Redis node crashes, or many keys expire at the exact same second. | Add random jitter to TTLs (e.g., `TTL = 1 hour + rand(5 mins)`). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Flash Sales / Quản lý tồn kho**: Dùng lệnh `DECR` để trừ kho nguyên tử trên Redis, kết hợp Khóa phân tán để đảm bảo không bị quá bán.
2. **Điều phối Cron Job**: Đảm bảo một tác vụ đặt lịch (`@Scheduled`) chỉ được chạy trên ĐÚNG MỘT máy chủ trong số 10 máy chủ đang bật.
3. **Idempotency (Tính lũy đẳng)**: Lưu ID của request đã xử lý vào Redis bằng `SETNX` (Set if Not eXists) để tránh trừ tiền khách hàng 2 lần.
4. **Rate Limiting**: Dùng thuật toán Sliding Log hoặc Token Bucket lưu trạng thái trên Redis.

**Không nên làm**:
- Tin tưởng hoàn toàn vào `@Cacheable` của Spring đối với dữ liệu nóng. Mặc định nó không chống được Stampede (trừ khi dùng `sync = true`, nhưng tính năng này lại chỉ hoạt động trên 1 máy ảo JVM, không áp dụng cho nhiều máy chủ).
- Giữ khóa Redis quá lâu: Lấy khóa xong rồi đi gọi API bên ngoài mất 10 giây. Khóa có thể bị hết hạn giữa chừng, làm luồng khác nhảy vào phá hỏng tính đồng bộ.

</details>

1. **Flash Sales / Inventory**: Using `DECR` operations for atomic stock reduction in Redis, combined with Distributed Locks to ensure consistency.
2. **Cron Job Coordination**: Ensuring a scheduled task (`@Scheduled`) only runs on ONE of your 10 microservice instances.
3. **Idempotency**: Storing processed request IDs in Redis using `SETNX` (Set if Not eXists) to prevent double-charging users.
4. **Rate Limiting**: Sliding log or token bucket algorithms stored in Redis.

### Anti-Patterns
- **Using `@Cacheable` blindly on hot data**: Spring's `@Cacheable` does NOT prevent Cache Stampedes by default (unless you use `sync = true`, which is limited to a single JVM, not distributed).
- **Long-held Redis Locks**: Acquiring a distributed lock and making a slow external API call. The lock might expire before the call finishes, allowing another thread in.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất**:
1. **Luôn dùng Redisson để tạo Khóa**: Đừng cố tự code Khóa phân tán bằng lệnh `SETNX`. Bạn sẽ quên xử lý các ca khó như: Tiến trình bị crash (cần cơ chế Watchdog), hay Redis cluster bị failover (cần thuật toán Redlock). Redisson xử lý hết giùm bạn.
2. **Thêm Jitter (độ nhiễu) vào TTL**: Đừng bao giờ set thời gian hết hạn cố định như `expire(60 * 60)`. Hãy luôn viết `expire(60 * 60 + random(0, 300))`. Điều này làm các key hết hạn rải rác ra, chống hiện tượng Tuyết lở (Cache Avalanche).
3. **Cache cả giá trị rỗng**: Để chống Penetration, nếu ai đó tìm `user_id = 999` mà không có, hãy mạnh dạn tạo cache `key:user:999` với giá trị `"EMPTY"` trong 1 phút.
4. **Dùng Bloom Filters cho tập dữ liệu khổng lồ**: Nếu cache `"EMPTY"` tốn quá nhiều RAM (do hacker sinh ra hàng triệu ID ngẫu nhiên), hãy dùng RedisBloom. Kiểm tra bộ lọc này trước, nếu nó bảo "Không có mặt", chặn luôn request mà không cần gọi Database.

**Cạm bẫy**:
1. **Deadlocks (Khóa chết)**: Server bị sập khi đang cầm Khóa. Nếu bạn quên cài Lease Time (thời gian thuê tối đa của khóa), khóa đó sẽ tồn tại vĩnh viễn không ai giải phóng.
2. **Luồng này mở khóa của luồng kia**: Luồng A lấy khóa, chạy quá chậm nên khóa tự hết hạn. Luồng B nhảy vào lấy khóa thành công. Lúc này luồng A chạy xong, gọi lệnh `unlock()`, vô tình mở cmn luôn Khóa của luồng B! *(Redisson đã chống được lỗi này nhờ việc cấp ID riêng cho mỗi luồng)*.

</details>

### Best Practices
1. **Always use Redisson for Locks**: Do not try to implement distributed locks manually using `SETNX`. You will fail to handle edge cases like thread crashes (requiring Watchdogs) or Redis cluster failovers (requiring Redlock algorithm). Redisson handles this automatically.
2. **Add Jitter to TTL**: Never set exactly `expire(60 * 60)`. Always do `expire(60 * 60 + random(0, 300))`. This spreads out expirations and prevents Cache Avalanches.
3. **Cache Empty Results**: To prevent Cache Penetration, if a user queries `user_id = 999` and it doesn't exist, cache `key:user:999` with the value `"EMPTY"` and a short TTL (e.g., 1 minute).
4. **Use Bloom Filters for massive datasets**: If caching `"EMPTY"` consumes too much memory (because attackers query millions of random IDs), use a RedisBloom filter. Check the filter first; if it says "Not present", block the request immediately without hitting the DB or caching.

### Common Pitfalls
1. **Deadlocks**: A server crashes while holding a lock. If you didn't set a lease time (TTL) on the lock, it stays locked forever.
2. **Lock Release by Wrong Thread**: A thread acquires a lock, runs slowly, the lock expires, Thread 2 gets the lock. Thread 1 finishes and calls `unlock()`, accidentally unlocking Thread 2's lock! *Fix: Redisson prevents this internally using thread IDs.*

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đoạn code dưới đây dùng Redisson để đảm bảo hàm thanh toán hằng ngày (chạy lúc 0h00) chỉ được thực thi trên ĐÚNG MỘT máy chủ. `tryLock(0, 5, MINUTES)` có nghĩa là: "Nếu thấy có người cầm khóa rồi thì bỏ cuộc luôn (0 chờ), và nếu tao giữ khóa thì sau 5 phút tự động tước khóa của tao phòng khi tao bị sập (Lease time)".

</details>

### Distributed Lock for Scheduled Tasks (Spring Boot + Redisson)

```java
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
public class BillingCronJob {

    private final RedissonClient redissonClient;

    public BillingCronJob(RedissonClient redissonClient) {
        this.redissonClient = redissonClient;
    }

    // Runs every day at midnight on ALL instances
    @Scheduled(cron = "0 0 0 * * ?")
    public void executeDailyBilling() {
        RLock lock = redissonClient.getLock("cron:daily-billing");
        
        try {
            // tryLock(waitTime, leaseTime, unit)
            // waitTime = 0: if another instance has the lock, give up immediately.
            // leaseTime = 5 min: lock automatically releases after 5 mins if thread crashes.
            if (lock.tryLock(0, 5, TimeUnit.MINUTES)) {
                log.info("Acquired lock. Executing billing process...");
                // Run heavy DB billing batch process
                Thread.sleep(60000); // Simulate work
            } else {
                log.info("Another instance is running the billing job. Skipping.");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
}
```

---

## Related Topics

- [Idempotency & Rate Limiting](../01-advanced-api-design/idempotency-and-rate-limiting.md) — How Redis distributed locks are used to guarantee idempotency.
- [JPA Performance Tuning](./jpa-performance-tuning.md) — What happens to the database when the cache is bypassed.
