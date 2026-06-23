# Redis

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Dù PostgreSQL hay MongoDB có xịn đến đâu, chúng vẫn lưu dữ liệu trên Ổ cứng (Disk). Mà tốc độ đọc ổ cứng thì vĩnh viễn chậm hơn hàng trăm lần so với đọc RAM. Khi ứng dụng của bạn có hàng triệu người dùng liên tục bấm F5 tải trang web, việc bắt Database lật ổ cứng ra đọc đi đọc lại 1 bài báo là sự lãng phí thảm họa, dẫn đến sập Server. **Redis** (Remote Dictionary Server) ra đời làm Vị cứu tinh. Nó là một cơ sở dữ liệu NoSQL lưu trữ mọi thứ 100% trên RAM. Nhờ vậy, tốc độ đọc/ghi của nó đạt mức *dưới 1 phần ngàn giây (sub-millisecond)*. Redis thường không đứng một mình, nó đóng vai trò "Lá chắn" (Cache) đứng chắn trước Database chính, giúp hệ thống chịu được lưu lượng truy cập khổng lồ mà không tốn thêm tiền mua máy chủ.

</details>

> **Summary**: The fundamental bottleneck of any web architecture is Disk I/O. Even highly optimized Relational Databases (PostgreSQL) or Document Stores (MongoDB) fundamentally rely on solid-state drives for persistence, resulting in query latencies typically measured in milliseconds. When applications face hyperscale read-heavy traffic (e.g., a viral news article or a live leaderboard), relentlessly querying the primary database causes CPU starvation and catastrophic latency spikes. **Redis** is an advanced, open-source, In-Memory Data Structure Store. By persisting its dataset entirely within volatile RAM, it bypasses disk latency entirely, achieving deterministic sub-millisecond execution times. While it functions as an independent database, its primary architectural role is serving as an ultra-fast, ephemeral Caching Layer, Session Store, and Pub/Sub Message Broker positioned strategically in front of the primary database.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn là một Thủ thư trong một Thư viện khổng lồ (Database chính).
1. **Không có Redis**: Một người vào hỏi: *"Cuốn Harry Potter nằm ở đâu?"*. Bạn phải đi bộ xuống tầng hầm, lật 10 cái tủ sách, tìm ra cuốn sách và đưa cho khách (Mất 5 phút). Ngay sau đó, người thứ 2, thứ 3... thứ 1000 bước vào đều hỏi mượn cuốn Harry Potter. Bạn cứ chạy lên chạy xuống tầng hầm 1000 lần. Bạn kiệt sức và gục ngã (Server sập).
2. **Có Redis (Bộ nhớ đệm)**: Lần đầu tiên người ta hỏi mượn cuốn Harry Potter, bạn vẫn xuống hầm lấy. Nhưng sau đó, bạn KHÔNG cất nó xuống hầm nữa. Bạn để luôn cuốn sách trên Bàn làm việc (RAM/Redis). Khi 1000 người tiếp theo vào hỏi, bạn chỉ việc đưa tay lấy trên bàn và đưa cho họ trong nháy mắt. Tốc độ phục vụ tăng gấp hàng ngàn lần.

</details>

Imagine running a very busy Restaurant Kitchen.
1. **Without Redis**: Every single time a customer asks for a glass of water, the waiter walks all the way to the deep freeze in the basement, chisels a block of ice, melts it, pours it, and walks it back. It takes 5 minutes per glass. If 1,000 customers ask for water, the waiter collapses from exhaustion (Database CPU crash).
2. **With Redis (The Cache)**: The waiter brings a large jug of ice water and places it directly on the dining table (The RAM). When the first customer asks for water, the waiter goes to the basement to fill the jug. But for the next 1,000 customers, they just pour it instantly from the jug on the table. It takes 1 second. Only when the jug is empty (Cache Expiry/Eviction) does the waiter walk back to the basement.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Redis lưu dữ liệu theo kiểu **Key-Value (Chìa khóa - Giá trị)** trên RAM. Khác với Memcached (một bộ nhớ đệm cũ chỉ lưu được chuỗi Text), Redis là một "Data Structure Store", nghĩa là nó hiểu được các Cấu trúc dữ liệu phức tạp:
1. **Strings (Chuỗi)**: Lưu số, văn bản, hoặc file JSON.
2. **Hashes (Băm)**: Giống như một Object của JavaScript (Ví dụ lưu thông tin `User:{name: "A", age: 10}`).
3. **Lists (Danh sách)**: Mảng dữ liệu, dùng làm Hàng đợi (Queue) tin nhắn.
4. **Sorted Sets (Tập hợp có sắp xếp)**: Vũ khí hủy diệt của Redis. Lưu một danh sách người chơi game kèm theo Điểm số. Redis tự động sắp xếp điểm số này theo thời gian thực cực kì nhanh.

</details>

Redis is fundamentally a Key-Value store, but it distinguishes itself from legacy caching solutions (like Memcached) by being a **Data Structure Server**. It natively understands and manipulates advanced programmatic data types directly in RAM:
1. **Strings**: The foundational type. Can store text, integers (supporting atomic increments), or serialized JSON payloads (up to 512MB per key).
2. **Hashes**: Maps between string fields and string values. Perfect for representing objects (e.g., storing a User Profile without serializing it to a massive string).
3. **Lists**: Linked Lists of strings. Heavily utilized for implementing Producer/Consumer queues (e.g., pushing background jobs into a list using `LPUSH` and worker nodes popping them using `RPOP`).
4. **Sorted Sets (ZSET)**: The crown jewel of Redis. A collection of unique strings, each associated with a floating-point score. Elements are inherently sorted by this score in memory. It is the industry standard mechanism for building massive Real-Time Leaderboards.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Redis sinh ra để xử lý bài toán **Độ Trễ (Latency)** và **Tải Đọc (Read Load)**.
Khi bạn có một truy vấn SQL rất phức tạp (`JOIN` 5 bảng, đếm số lượng thống kê), máy chủ Postgres phải chạy mất 2 giây. Nếu có 100 người gọi API đó, Postgres phải tính toán lại cục đó 100 lần, CPU tăng lên 100%. 
Thay vì bắt Database tính lại, Backend sẽ chạy truy vấn đó ĐÚNG 1 LẦN. Sau khi có kết quả, Backend ném kết quả đó vào Redis và dán nhãn: `Lưu trong 10 phút nhé (TTL - Time to Live)`. 
100 người tiếp theo gọi API, Backend sẽ chui vào Redis lấy kết quả ra (mất 0.001 giây) rồi trả về luôn, KHÔNG cần chạm tới Postgres. Postgres hoàn toàn thảnh thơi để làm việc khác.

</details>

Redis exists to mitigate the physical limitations of Disk I/O and relieve the computational burden on primary databases (PostgreSQL/MongoDB).
In standard architectures, executing an expensive analytical query (e.g., calculating the total sales of all products across 5 regions) requires the SQL database to load massive indexes into memory and perform heavy CPU aggregation. If this endpoint receives 1,000 HTTP requests per second, the Database CPU immediately spikes to 100% and crashes.
Redis solves this via **The Cache-Aside Pattern**. The backend application intercepts the request. It first checks Redis. If the data exists (Cache Hit), it returns it instantly. If the data is missing (Cache Miss), the backend queries the heavy PostgreSQL database *once*, returns the data to the user, and simultaneously saves the result in Redis with a Time-To-Live (TTL) expiration of 5 minutes. For the next 5 minutes, PostgreSQL handles zero load for that specific query.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc xây dựng Bảng Xếp Hạng (Leaderboard) cho một Game có 1 triệu người chơi đang bắn nhau liên tục.
</details>

Visualizing Real-Time Leaderboards (Postgres vs Redis).

| Metric | Primary Database (PostgreSQL) | In-Memory Cache (Redis) |
|---|---|---|
| **Updating Score** | `UPDATE users SET score = score + 10 WHERE id = 1` | `ZINCRBY leaderboard 10 "user_1"` |
| **Getting Top 10** | `SELECT * FROM users ORDER BY score DESC LIMIT 10`. Extremely CPU-heavy on a 1-million row table. | `ZREVRANGE leaderboard 0 9`. **Instantaneous**. Redis mathematically maintains the sort order in RAM automatically. |
| **Performance Impact**| If players check the leaderboard constantly, the Database grinds to a halt. | Redis can handle 100,000+ reads per second on a single thread without breaking a sweat. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Caching API (Bộ đệm web)**: Lưu trữ các kết quả API nặng, hoặc cấu hình web thay đổi ít (Danh mục sản phẩm, Bài viết Trang chủ).
2. **Session Store (Lưu phiên đăng nhập)**: Khi bạn có 10 máy chủ Backend chạy song song, khách hàng đăng nhập vào máy số 1, thì máy số 2 không biết người đó là ai. Người ta dùng Redis làm kho lưu Session ở giữa. Cả 10 máy chủ đều nhìn vào Redis để kiểm tra xem khách đã Đăng nhập chưa. Rất nhanh và an toàn.
3. **Giới hạn tốc độ (Rate Limiting)**: Chống Hacker spam API (Ví dụ: "Mỗi người dùng chỉ được gọi API 5 lần trong 1 giây"). Dùng lệnh `INCR` của Redis, mỗi lần khách gọi, tăng số đếm lên 1. Vượt quá 5 thì khóa mõm. Tốc độ RAM giúp việc khóa này diễn ra theo thời gian thực.
4. **Hàng đợi tin nhắn (Message Broker / PubSub)**: Giống như phòng chat. Người dùng ném một bản tin vào Redis (Pub), 10 máy chủ khác đang lắng nghe sẽ lập tức nhận được (Sub). Tuy nhiên, nếu máy chủ bị tắt, bản tin có thể bị mất (Kém an toàn hơn RabbitMQ/Kafka).

</details>

1. **API Response Caching**: The most ubiquitous use case. Storing the JSON output of expensive HTTP endpoints (e.g., Homepage Catalog, User Profiles) with an automated Time-To-Live (TTL) expiry.
2. **Distributed Session State**: In a horizontally scaled architecture with a Load Balancer distributing traffic across 5 Node.js servers, storing user Login Sessions in the memory of Server A is catastrophic if the next request routes to Server B. Redis acts as a centralized, ultra-fast Session Store. All 5 Node.js servers read/write session cookies directly to the Redis cluster.
3. **Rate Limiting & DDoS Protection**: Throttling malicious traffic or enforcing API tier limits (e.g., "Free Tier: 100 requests / minute"). Utilizing Redis's atomic `INCR` (increment) command paired with `EXPIRE`, a backend can mathematically track and block incoming IP addresses in sub-milliseconds without touching the primary database.
4. **Pub/Sub and Task Queues**: Redis supports Publish/Subscribe messaging paradigms natively. A web-server can `PUBLISH` a "Video Uploaded" event, and 3 background worker-nodes `SUBSCRIBE` to the channel to instantly start transcoding the video. (Note: For guaranteed persistence and complex routing, dedicated brokers like RabbitMQ/Kafka are superior).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **LUÔN LUÔN cài đặt TTL (Thời gian sống)**: Lỗi 99% người mới mắc phải là lưu dữ liệu vào Redis mà quên cài đặt `EXPIRE` (TTL). Cứ mỗi ngày dữ liệu lại phình ra một chút. Do RAM máy chủ rất bé (thường chỉ 4GB-16GB), sau vài tháng RAM bị đầy 100%. Lúc đó, Redis sẽ Crash hoặc bóp méo dữ liệu, kéo theo sập toàn bộ hệ thống.
2. **Chọn Chiến lược Dọn dẹp (Eviction Policy)**: Khi RAM đầy, Redis có thể tự động xóa bớt dữ liệu để lấy chỗ trống. Hãy cấu hình nó là `allkeys-lru` (Least Recently Used) - Xóa những dữ liệu nào lâu ngày không có ai đọc.

</details>

1. **Always Enforce a TTL (Time-To-Live)**: The most fatal operational error in Redis architecture. Developers write `SET session_token "123"` but forget to append an expiration. Because RAM is orders of magnitude more expensive than Disk storage, a typical Redis server might only have 4GB of capacity. Without TTLs, the cache grows infinitely. Within weeks, it hits OOM (Out Of Memory), the OS kills the process, and every API call that relies on the cache fails catastrophically. **Rule**: Every single non-critical Cache key MUST have an explicit `EXPIRE` command attached.
2. **Configure an Eviction Policy (LRU)**: You must tell Redis exactly what to do when it physically runs out of RAM. The default policy is `noeviction` (which throws a hard error on new writes). **Best Practice**: Change the `maxmemory-policy` in `redis.conf` to `allkeys-lru`. This algorithm automatically deletes the "Least Recently Used" keys to make room for new data, ensuring the cache is always filled with the most actively requested information.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiệu ứng Tuyết lở (Cache Avalanche)**: Bạn dán nhãn 10.000 bài báo lưu vào Redis và cho hết hạn CÙNG LÚC vào lúc 12h đêm. Đúng 12h đêm, toàn bộ Cache bị xóa sạnh. Ngay giây tiếp theo, có 5000 người vào đọc báo. Vì Redis trống trơn (Cache Miss), Backend hoảng hốt ném toàn bộ 5000 truy vấn đó thẳng vào Database chính (Postgres). Postgres bị sốc nhiệt và chết tươi ngay lập tức.
   - *Luật*: Khi cài TTL, đừng bao giờ cài số cứng (10 phút). Hãy cộng thêm một vài giây ngẫu nhiên (Random Jitter). Bài 1 hết hạn lúc 10p 1s, bài 2 hết hạn lúc 10p 5s. Việc này giúp Database xả hơi.
2. **Xài lệnh KEYS trên môi trường thật**: Trong lúc code ở nhà, bạn hay gõ lệnh `KEYS *` để xem toàn bộ danh sách dữ liệu trong Redis. Redis là ĐƠN LUỒNG (Single-Threaded). Khi bạn gõ lệnh này trên Server có 10 triệu Key, cái luồng duy nhất đó sẽ bị KHÓA ĐỨNG trong 5 giây để quét toàn bộ. Hàng ngàn truy vấn khác sẽ bị tắc nghẽn và treo cứng App. *Tuyệt đối không dùng lệnh KEYS, hãy dùng lệnh SCAN.*

</details>

1. **Cache Avalanche (The Thundering Herd Problem)**: A system failure occurring when massive amounts of cached data expire simultaneously. If a script caches 50,000 Product pages at 1:00 AM with exactly a 2-hour TTL, all 50,000 keys expire at exactly 3:00 AM. At 3:00:01 AM, thousands of user requests hit the backend. Experiencing massive "Cache Misses", the backend aggressively routes ALL traffic directly to PostgreSQL simultaneously. The primary database instantly crashes. **The Fix**: Add Random Jitter. Instead of setting TTL to exactly 7200 seconds, set it to `7200 + random(0, 300)` seconds. This staggers the expirations smoothly over time.
2. **Executing `KEYS *` in Production**: Because Redis operates on a Single-Threaded Event Loop, executing O(N) commands physically blocks all other operations. Running `KEYS *` on a production database with 5 million keys will freeze the entire Redis server for several seconds. Every pending HTTP request relying on Redis will timeout. **Rule**: Never use `KEYS`. Always use the non-blocking cursor-based `SCAN` command for key discovery.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cách dùng thư viện `redis` (Node.js/TypeScript) trong mô hình Cache-Aside.
</details>

### Connection & Basic Cache-Aside Pattern
The canonical pattern: Check Cache $\rightarrow$ If Miss, Query DB $\rightarrow$ Save to Cache $\rightarrow$ Return Data.

```typescript
import { createClient } from 'redis';
import { db } from './my-database'; // Fictional PostgreSQL driver

// 1. Initialize and Connect
const redisClient = createClient({ url: 'redis://localhost:6379' });
await redisClient.connect();

async function getUserProfile(userId: string) {
    const cacheKey = `user_profile:${userId}`;

    // STEP 1: Check Redis
    // get() is extremely fast (O(1) complexity)
    const cachedData = await redisClient.get(cacheKey);
    
    if (cachedData) {
        console.log("CACHE HIT! Returning instantly from RAM.");
        return JSON.parse(cachedData);
    }

    console.log("CACHE MISS! Querying heavy PostgreSQL database...");
    
    // STEP 2: Query the slow primary database
    const user = await db.query(`SELECT * FROM users WHERE id = $1`, [userId]);

    if (user) {
        // STEP 3: Save to Redis for the NEXT person.
        // EX: 3600 explicitly means Time-To-Live is 3600 seconds (1 hour). NEVER FORGET THIS!
        await redisClient.set(cacheKey, JSON.stringify(user), {
            EX: 3600 
        });
    }

    return user;
}
```

### Advanced Data Structures (Sorted Sets & Rate Limiting)

**Building a Gaming Leaderboard (Sorted Sets)**
```bash
# In Redis CLI
# Add users with their specific scores
> ZADD global_leaderboard 1500 "Player_Alice"
> ZADD global_leaderboard 2300 "Player_Bob"
> ZADD global_leaderboard 800  "Player_Charlie"

# Fetch the Top 2 players (Highest scores first)
# ZREVRANGE: Reverse Range (Index 0 to Index 1)
> ZREVRANGE global_leaderboard 0 1 WITHSCORES
1) "Player_Bob"
2) "2300"
3) "Player_Alice"
4) "1500"
```

**Implementing a Rate Limiter (TypeScript)**
```typescript
async function checkRateLimit(ipAddress: string): Promise<boolean> {
    const key = `rate_limit:${ipAddress}`;
    
    // INCR atomically creates the key if it doesn't exist and increments it to 1.
    const requestsCount = await redisClient.incr(key);
    
    // If it's the very first request, set the expiry window to 60 seconds
    if (requestsCount === 1) {
        await redisClient.expire(key, 60);
    }
    
    // Enforce the rule: Max 10 requests per minute
    if (requestsCount > 10) {
        return false; // BLOCKED
    }
    
    return true; // ALLOWED
}
```

---

## Related Topics

- Redis acts as a shield for heavy relational databases like **[PostgreSQL](./postgresql.md)**.
- For persisting heavy document structures that don't fit in RAM, see **[MongoDB](./mongodb.md)**.
- To execute background tasks delayed by Redis queues, use the backend logic in **[Node.js](../backend/nodejs-express.md)**.
