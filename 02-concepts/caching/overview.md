# Caching Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Caching (Bộ nhớ đệm) là nghệ thuật "ghi nhớ". Thay vì bắt máy chủ làm đi làm lại một phép toán cực nhọc, hoặc lục lọi Database chắp vá dữ liệu tốn 5 giây, ta làm 1 lần thôi rồi lưu kết quả vào một chỗ siêu nhanh (RAM). Lần sau có ai hỏi y chang câu đó, ta lấy kết quả ở RAM quăng ra luôn trong 0.001 giây. Caching là vũ khí tối thượng số 1 để mở rộng quy mô hệ thống (Scalability) và giảm độ trễ (Latency).

</details>

> **Summary**: Caching is the architectural art of temporary memorization. It involves storing the results of highly expensive, computationally intensive, or I/O-bound operations (like complex Database joins or heavy mathematical processing) in an ultra-fast, transient storage layer (typically RAM). When subsequent requests demand the exact same data, the system bypasses the expensive operation and serves the data directly from the cache. Caching is the undisputed primary weapon for obliterating Latency and maximizing System Scalability.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn làm thủ thư ở Thư viện khổng lồ.
1. **Không có Cache**: Khách hàng tới hỏi "Sách Harry Potter tập 1 ở đâu?". Bạn chạy tít xuống tầng hầm, mò mẫm 15 phút, lấy sách đưa cho khách. 5 phút sau, một người khác tới hỏi đúng quyển Harry Potter tập 1. Bạn lại chạy xuống tầng hầm mò mẫm 15 phút nữa. Rất mệt và chậm!
2. **Có Cache**: Sau khi lấy quyển Harry Potter cho ông khách đầu tiên, thay vì cất nó xuống hầm, bạn **để nó ngay trên mặt bàn làm việc của bạn** (Đây là Cache). Khi người thứ hai tới hỏi, bạn với tay lấy ngay trên bàn đưa luôn trong 1 giây!

</details>

Imagine you are a Librarian in an infinitely massive library.
1. **Without Cache**: A patron asks for "The History of Rome." You walk down 5 flights of stairs, search through dusty archives for 20 minutes, retrieve the book, and hand it to them. 5 minutes later, another patron asks for the *exact same book*. You repeat the grueling 20-minute journey. This is painfully inefficient.
2. **With Cache**: After retrieving the book for the first patron, instead of returning it to the basement, you place it directly on your Front Desk (The Cache). When the second patron asks for it, you hand it to them instantly in 1 second. You have bypassed the expensive physical search.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Về mặt kỹ thuật, Cache là một lớp lưu trữ dữ liệu tốc độ cao (Thường là bộ nhớ RAM chứ không phải ổ cứng SSD/HDD).
Nó có 2 đặc điểm cốt lõi:
1. **Cực nhanh nhưng Dung lượng nhỏ**: Ổ cứng Database của bạn có thể chứa 10TB dữ liệu (Giá rẻ, nhưng chậm). RAM của Cache Server (như Redis) chỉ có khoảng 64GB (Giá cực đắt, nhưng siêu tốc). Do đó, bạn không thể nhét toàn bộ DB vào Cache được. Bạn chỉ được nhét những dữ liệu nào "được hỏi nhiều nhất" (Hot Data).
2. **Dữ liệu tạm thời (Transient)**: Nếu sập nguồn điện, ổ cứng DB vẫn còn dữ liệu, nhưng RAM của Cache sẽ bị xóa trắng hoàn toàn. Vì vậy, Cache không bao giờ được dùng để lưu trữ dữ liệu gốc quan trọng. Nó chỉ lưu "bản sao".

</details>

Architecturally, a Cache is a high-speed data storage layer (almost exclusively utilizing Volatile Memory / RAM, rather than persistent SSD/HDD storage).
It possesses two defining characteristics:
1. **Ultra-Low Latency, Extreme Cost (Small Size)**: Your persistent PostgreSQL Database might sit on a 10TB SSD (cheap per GB, but slow I/O). Your Redis Cache sits in 64GB of RAM (extremely expensive per GB, but nanosecond I/O). Consequently, you cannot cache the entire database. You must selectively cache only the most frequently accessed data (**Hot Data**).
2. **Transient/Volatile State**: If a catastrophic power failure occurs, the persistent Database SSD retains all records. The Cache RAM, however, is completely wiped. Therefore, the Cache must never be the absolute "Source of Truth". It is strictly a disposable replica of the truth.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hệ thống tồn tại Nút thắt cổ chai (Bottleneck) lớn nhất chính là: **Ổ Cứng (Disk I/O)** và **Mạng (Network I/O)**.
Ví dụ: Trang chủ của báo VnExpress. Mỗi khi có 1 người truy cập, hệ thống phải chui vào Database, nối (JOIN) 5 cái bảng lại với nhau (Bảng Bài viết, Bảng Tác giả, Bảng Danh mục...) để render ra trang chủ. Mất 500ms.
Nếu có 100.000 người truy cập cùng lúc $\rightarrow$ Database sụp đổ ngay lập tức vì quá tải (Overload).
Nhờ có Cache, hệ thống chỉ tính toán 500ms đó đúng 1 lần đầu tiên. 99.999 người truy cập phía sau sẽ lấy thẳng chuỗi HTML từ Redis trong 1ms. Database không hề hay biết là có 100.000 người đang vào web.

</details>

Modern software systems face an inescapable physical bottleneck: **Disk I/O and Network Latency**.
Consider a high-traffic News Homepage (e.g., The New York Times). To render the homepage, the backend must execute a complex SQL query, executing `JOIN` operations across 5 massive tables (Articles, Authors, Categories, Images, Tags). This takes 500ms.
If a breaking news event occurs and 100,000 concurrent users refresh the homepage, the Database is slammed with 100,000 heavy `JOIN` queries simultaneously. The CPU spikes to 100%, and the Database crashes instantly (Cascading Failure).
By placing a Cache in front of the Database, the expensive 500ms SQL query is executed exactly *once*. The serialized JSON/HTML result is saved to RAM. The subsequent 99,999 requests are intercepted by the Cache and served in 1ms. The Database remains entirely asleep, oblivious to the massive traffic spike.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh biểu đồ đường đi của Dữ liệu.
</details>

Visualizing the Request Lifecycle and Latency reduction.

| Metric | Without Cache (Direct to DB) | With Cache (Hit) |
|---|---|---|
| **Request Path** | Client $\rightarrow$ API $\rightarrow$ Database (Disk) $\rightarrow$ API $\rightarrow$ Client | Client $\rightarrow$ API $\rightarrow$ Redis (RAM) $\rightarrow$ API $\rightarrow$ Client |
| **I/O Type** | Disk Read (Milliseconds) | Memory Read (Microseconds) |
| **Avg Latency** | `100ms - 500ms` | `< 5ms` |
| **Max Concurrency**| Low (e.g., 5,000 req/sec before DB dies) | Extremely High (e.g., 100,000+ req/sec) |
| **Complexity** | Simple (Data is always 100% fresh) | Complex (Must deal with Stale Data and Invalidation) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Client/Browser Cache**: Trình duyệt của bạn tự động lưu hình ảnh, file CSS, JS vào ổ cứng máy tính. Lần sau vào lại trang web đó, ảnh tải ngay lập tức không cần mạng.
2. **CDN (Content Delivery Network)**: Cache ở biên mạng. Trang web đặt máy chủ ở Mỹ. User ở Việt Nam truy cập sẽ rất lag. CDN đặt một máy chủ Cache ở Việt Nam, copy sẵn hình ảnh video từ Mỹ về. User Việt Nam lấy ảnh từ máy chủ Việt Nam.
3. **Application/Backend Cache**: Nơi Lập trình viên Backend làm việc nhiều nhất (Redis / Memcached). Dùng để lưu Session đăng nhập, lưu kết quả truy vấn SQL nặng, hoặc đếm số lượt xem bài viết.

</details>

1. **Browser/Client Caching**: The user's web browser intercepts requests and caches static assets (Images, CSS, JS bundles) directly on the user's local hard drive based on `Cache-Control` HTTP headers.
2. **CDN (Content Delivery Network)**: Edge Caching. If the primary origin server is in New York, a user in Tokyo experiences massive physical network latency (ping). A CDN (like Cloudflare) deploys caching servers in Tokyo. The CDN caches the static assets in Tokyo, intercepting the request locally and reducing latency to zero.
3. **Application/Backend Caching**: The domain of Backend Engineers (utilizing Redis or Memcached). This layer caches expensive business logic: Compiled HTML templates, heavy SQL query results, aggregate analytics (e.g., "Total likes on a post"), and stateful Session IDs.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Quy tắc 80/20**: Đừng Cache tất cả mọi thứ! Chỉ 20% dữ liệu trong hệ thống phục vụ 80% lượng traffic. Hãy phân tích log để tìm ra "Hot Data" (Ví dụ: Trang chủ, Sản phẩm bán chạy) và chỉ nhét chúng vào Cache để tiết kiệm tiền mua RAM.
2. **Luôn set TTL (Time To Live)**: Đừng bao giờ nhét một món đồ vào Cache mà không cài đặt thời gian chết (Ví dụ: `expire = 60 phút`). Nếu quên set TTL, RAM của bạn sẽ bị rác băm dần dần cho đến khi đầy (OOM - Out of Memory) và sập Server Cache.

</details>

1. **The 80/20 Rule (Pareto Principle)**: Do not cache your entire database. It is financially disastrous. In almost all applications, 20% of the data (Hot Data) generates 80% of the read traffic (e.g., Homepage feeds, Top 10 products, User Sessions). Analyze telemetry to identify Hot Data and exclusively cache that, optimizing expensive RAM utilization.
2. **Mandatory TTL (Time To Live)**: Never insert a key-value pair into a cache without an explicit expiration timer (`TTL = 3600 seconds`). If you create infinite-lifetime keys, your cache will inevitably accumulate orphaned garbage data, eventually hitting 100% memory utilization, triggering an `OOM (Out Of Memory)` crash or forcing the cache to violently evict active data.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Thảm họa "Xuyên thủng Cache" (Cache Penetration)**: Hacker cố tình viết bot liên tục truy vấn một cái ID sản phẩm KHÔNG TỒN TẠI (Ví dụ: `id = -999`). 
   - Cache tìm không thấy $\rightarrow$ Chọc xuống DB. 
   - DB tìm không thấy $\rightarrow$ Trả về Null và KHÔNG lưu vào Cache. 
   - Hacker bắn 10.000 request/giây $\rightarrow$ Toàn bộ chọc thủng Cache xuyên thẳng vào DB làm DB sập. 
   - *Cách giải quyết*: Nếu DB trả về Null, hãy lấy cái Null đó LƯU LUÔN VÀO CACHE (với TTL ngắn khoảng 3 phút).
2. **"Tuyết lở Cache" (Cache Avalanche)**: Bạn ngu ngốc cài đặt TTL của 10.000 sản phẩm hot NHƯ NHAU. Đúng 12h đêm, 10.000 sản phẩm đó đồng loạt hết hạn (Bốc hơi khỏi Cache). Ngay lúc đó, có 10.000 users đang truy cập. Vì Cache rỗng, 10.000 requests này đổ ập xuống DB cùng một phần nghìn giây. DB sập ngay lập tức.
   - *Cách giải quyết*: Thêm "Nhiễu ngẫu nhiên" (Jitter) vào TTL. Ví dụ: Cài TTL ngẫu nhiên từ `50 phút đến 70 phút`. Để các món đồ chết lần lượt rải rác chứ không chết cùng một lúc.

</details>

1. **Cache Penetration**: A malicious attacker relentlessly requests a resource ID that *does not exist* in the system (e.g., `GET /users/-99999`). The request misses the cache. It hits the Database. The Database returns `NULL`. The backend naive code does *not* cache `NULL`. The attacker fires 50,000 RPS. Every single request pierces the cache armor, hitting the Database directly and crashing it. **Fix**: Cache empty results/Nulls with a short TTL (e.g., 3 minutes) to absorb the attack.
2. **Cache Avalanche**: You launch a marketing campaign at 8:00 AM. You load 10,000 product pages into the cache, setting every single key to expire in exactly 60 minutes. At 9:00 AM, all 10,000 keys expire *simultaneously*. A fraction of a second later, thousands of users request those pages. Because the cache is entirely empty (Cache Miss), thousands of massive SQL queries hit the Database at the exact same millisecond, instantly bringing down the entire production environment. **Fix**: Add **Jitter** (Randomness) to your TTLs. Instead of exactly 60 minutes, set the TTL to a random value between 50 and 70 minutes. Keys will gracefully expire one by one, spreading the Database load.

---

## Related Topics

- For how to actually write code to interact with Cache, see **[Caching Strategies](./strategies.md)**.
- For the hardest problem in Computer Science (keeping data fresh), see **[Cache Invalidation](./invalidation.md)**.
- For concrete implementation details, see **[Redis](../../03-technologies/database/redis.md)**.
