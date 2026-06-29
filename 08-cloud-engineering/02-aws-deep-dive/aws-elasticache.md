# AWS ElastiCache

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Bí quyết để ứng dụng chạy nhanh như chớp. Tìm hiểu về Caching (bộ nhớ đệm) trong bộ nhớ (In-Memory), cách giảm tải cho Database chính bằng ElastiCache for Redis và Memcached, và chiến lược lưu cache hiệu quả.

</details>

> **Summary**: The secret to lightning-fast applications. Learn about In-Memory caching, how to offload heavy read traffic from your primary Database using ElastiCache for Redis and Memcached, and effective caching strategies.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn là một thủ thư (Web Server).
- **Không có Cache (Truy cập Database)**: Khách hỏi bạn: "Năm 1945 xảy ra chuyện gì?". Bạn phải chạy bộ xuống tầng hầm (Database), tìm cuốn sách Lịch sử, giở từng trang tìm câu trả lời, rồi chạy lên trả lời khách (Mất 5 phút). 100 khách liên tục hỏi cùng một câu, bạn phải chạy lên chạy xuống 100 lần. Bạn kiệt sức (Database sập).
- **Có Cache (ElastiCache)**: Bạn mua một cuốn sổ tay nhỏ để ngay trên bàn làm việc (ElastiCache). Lần đầu tiên khách hỏi câu đó, bạn vẫn phải chạy xuống hầm. Nhưng khi lên, bạn chép ngay câu trả lời vào sổ tay. 99 khách sau hỏi lại, bạn chỉ cần liếc nhìn cuốn sổ tay và trả lời trong 1 giây! Khách vui, bạn khỏe. 

</details>

You are a Librarian (The Web Server).
- **Without Cache (Querying the Database)**: A customer asks: "What happened in 1945?". You have to walk down into the deep basement (the RDS Database), find the heavy History encyclopedia, flip through the pages, and walk back up to give the answer (Takes 5 minutes). If 100 people ask the exact same question, you run up and down the stairs 100 times. You collapse from exhaustion (The Database crashes).
- **With Cache (ElastiCache)**: You buy a small notepad and place it on your front desk (ElastiCache). The first time someone asks the question, you still have to go to the basement. But when you come back, you write the answer down on your notepad. When the next 99 people ask the exact same question, you just glance at your notepad and answer in 1 second! The customers are happy, and you aren't exhausted.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon ElastiCache** là một dịch vụ lưu trữ dữ liệu trong bộ nhớ (In-Memory Data Store) hoàn toàn được quản lý, tương thích với mã nguồn mở Redis và Memcached.
Vì nó lưu dữ liệu trên RAM thay vì Ổ cứng (SSD/HDD), tốc độ phản hồi của nó tính bằng micro-giây (phần triệu của giây), nhanh hơn Database truyền thống hàng ngàn lần.

**Các Engine hỗ trợ:**
- **Redis**: Rất mạnh mẽ. Hỗ trợ cấu trúc dữ liệu phức tạp (Lists, Sets, Hashes), hỗ trợ lưu trữ vĩnh viễn (Persistence) để không mất dữ liệu khi sập nguồn, và sao chép Multi-AZ.
- **Memcached**: Rất đơn giản. Chỉ lưu Key-Value đơn thuần, chạy đa luồng (Multi-threaded). Mất điện là mất hết dữ liệu. (Đa số mọi người hiện nay chọn Redis).

</details>

**Amazon ElastiCache** is a fully managed, in-memory data store and caching service that is compatible with open-source Redis and Memcached.
Because it stores data in RAM rather than on Disk (SSD/HDD), its response times are measured in microseconds (millionths of a second), making it thousands of times faster than traditional disk-based databases.

**Supported Engines:**
- **Redis**: Highly advanced. Supports complex data structures (Lists, Sets, Hashes, Geospatial), offers data persistence (saving RAM to disk so it survives reboots), and Multi-AZ replication.
- **Memcached**: Extremely simple. Purely a Key-Value string store. Multi-threaded. Ephemeral (if the server loses power, all data is instantly gone). *Industry trend: The vast majority of modern applications default to Redis.*

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hầu hết các ứng dụng Web có tỷ lệ Đọc/Ghi là 10:1 (Khách vào xem hàng 10 lần mới có 1 lần đặt mua).
Database truyền thống (RDS) đọc dữ liệu từ ổ cứng. Dù bạn có tăng kích thước (Scale Up) máy chủ Database lên lớn nhất, khi gặp đợt Flash Sale với hàng triệu lượt truy cập cùng xem 1 trang sản phẩm, Database vẫn sẽ sập vì quá tải.
Thay vì mua cái Database giá $1,000/tháng để gánh tải Đọc, bạn chỉ cần mua cái Database nhỏ $50/tháng và đặt phía trước nó một con ElastiCache giá $30/tháng. Cache sẽ đỡ 90% đạn (traffic) cho Database. Hệ thống vừa chạy nhanh hơn, vừa rẻ hơn rất nhiều!

</details>

The vast majority of Web applications have a Read-to-Write ratio of 10:1 (Users browse 10 product pages for every 1 purchase they make).
Traditional Databases (RDS) retrieve data from block storage (Disk). Even if you Scale Up your Database to the largest EC2 instance type, during a massive Flash Sale where millions of users repeatedly view the exact same "Top 10 Deals" page, the Database will inevitably crash due to I/O exhaustion.

Instead of provisioning a massive $1,000/month RDS Database just to survive read-spikes, you provision a modest $50/month Database and place a $30/month ElastiCache node in front of it. The Cache intercepts and serves 90% of the traffic directly from RAM. The architecture becomes exponentially faster, infinitely more resilient, and drastically cheaper!

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Không có Cache:**
1. User yêu cầu xem Top 10 bài hát.
2. Web Server gọi Database.
3. Database chạy lệnh SQL phức tạp `SELECT ... ORDER BY ... LIMIT 10`, mất 200ms.
4. Trả kết quả cho User.
*(Nếu 100k user gọi cùng lúc, DB tính toán lại câu lệnh SQL đó 100k lần, mất 200ms x 100k -> Sập).*

**Có Cache (Mô hình Lazy Loading):**
1. User yêu cầu xem Top 10 bài hát.
2. Web Server hỏi ElastiCache trước.
3. Nếu Cache có dữ liệu (Cache Hit), trả về ngay lập tức trong **1ms**.
4. Nếu Cache KHÔNG CÓ (Cache Miss), Web Server mới gọi Database (200ms), lấy kết quả, **GHI** vào Cache, rồi trả cho User.
*(100k user gọi cùng lúc, chỉ có user đầu tiên phải đợi 200ms, 99,999 user sau nhận kết quả trong 1ms. DB chỉ tính toán đúng 1 lần!).*

</details>

### Without Cache (Raw Database Queries)
1. User requests the "Top 10 Songs".
2. The Web Server queries the Database.
3. The Database executes a heavy SQL aggregation: `SELECT ... JOIN ... ORDER BY views DESC LIMIT 10`, taking 200ms to compute.
4. Result returned to User.
*(If 100,000 users refresh the page, the DB computes that exact same heavy SQL query 100,000 times concurrently -> The DB CPU hits 100% and crashes).*

### With Cache (Lazy Loading / Cache-Aside Pattern)
1. User requests the "Top 10 Songs".
2. The Web Server asks ElastiCache: "Do you have key `top_10_songs`?"
3. If ElastiCache has it (**Cache Hit**), it returns the JSON instantly in **1ms**.
4. If ElastiCache doesn't have it (**Cache Miss**), the Web Server queries the RDS Database (200ms). It then **WRITES** the result into ElastiCache (so the next person can use it), and returns the data to the User.
*(If 100,000 users refresh the page, only the 1st user suffers a 200ms delay. The other 99,999 users get a 1ms response. The DB computes the SQL exactly ONCE).*

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Database Caching**: Lưu trữ tạm thời các câu Query nặng, các bảng xếp hạng (Leaderboards), danh sách sản phẩm phổ biến.
2. **Session Store (Lưu phiên đăng nhập)**: Khi dùng nhiều Web Server (Load Balancer), nếu User đăng nhập ở Server 1, sau đó bị đẩy sang Server 2, Server 2 sẽ không biết User này. Ta dùng ElastiCache làm nơi lưu trạng thái chung ở giữa. Cả 2 Server đều đọc chung 1 Cache.
3. **Giới hạn tốc độ (Rate Limiting)**: Chống Spam/DDoS. Lưu số lần một IP gọi API vào Redis (vì Redis hỗ trợ tăng biến số tự động cực nhanh - `INCR`). Nếu IP gọi quá 100 lần/phút, block IP đó.

**Không nên làm (Anti-patterns):**
- **Dùng Cache làm Database chính (Source of Truth)**: ElastiCache được thiết kế để lưu dữ liệu "bốc hơi" (tạm thời). RAM rất đắt. Đừng bao giờ lưu dữ liệu duy nhất chưa từng backup (ví dụ: giỏ hàng chưa thanh toán của khách) VĨNH VIỄN trên Cache. Nếu máy chủ Redis khởi động lại, bạn sẽ mất trắng dữ liệu. Luôn có RDS/DynamoDB đằng sau làm hậu phương vững chắc.

</details>

1. **Database Query Caching**: Offloading heavy, frequently requested, and slowly changing data (e.g., Homepage product catalog, Global Leaderboards).
2. **Session State Management**: In a distributed Auto Scaling group, if a user logs in on Web Server A, and the Load Balancer routes their next request to Web Server B, Web Server B doesn't know they are logged in (Stateless). ElastiCache acts as a centralized Session Store that all Web Servers securely read from.
3. **API Rate Limiting**: Preventing DDoS or API abuse. Redis has highly efficient atomic increment (`INCR`) commands. You store the User's IP as a key, increment it on every API call, and if it exceeds 100 requests per minute, the API Gateway blocks them.

### Anti-Patterns
- **Using ElastiCache as the Source of Truth**: RAM is volatile and extremely expensive per GB compared to SSDs. While Redis supports persistence, it is primarily designed as an ephemeral layer. Do not store critical, non-reproducible data (like financial ledgers) *only* in ElastiCache. Always use RDS or DynamoDB as the persistent Source of Truth, and treat the Cache as a disposable speed-layer.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Vấn đề "Dữ liệu cũ" (Cache Invalidation / Stale Data)**
Đây là bài toán khó nhất trong Khoa học máy tính!
Giả sử bạn sửa giá iPhone từ $1000 xuống $900 trong Database. Nhưng trên ElastiCache vẫn đang lưu bản copy cũ là $1000. Khách hàng xem web sẽ thấy giá sai!
*Giải pháp*: 
- **Time-To-Live (TTL)**: Gắn thẻ thời hạn cho mọi dữ liệu trong Cache. Ví dụ: `TTL = 60s`. Cứ sau 1 phút, Cache sẽ tự xóa dữ liệu cũ, ép Web Server phải xuống Database lấy dữ liệu mới.
- **Write-Through**: Mỗi khi Backend code cập nhật giá mới vào RDS, bắt buộc phải viết code cập nhật luôn giá mới đó vào ElastiCache. (Rất an toàn nhưng code phức tạp).

**2. Vấn đề "Bão Cache" (Cache Stampede)**
Nếu một dữ liệu cực hot (Ví dụ: Trận chung kết World Cup) vừa bị hết hạn TTL và biến mất khỏi Cache. Đúng lúc đó, 10,000 khách truy cập. 10,000 Web Server cùng thấy Cache rỗng (Cache Miss), và cùng lúc ập xuống Database đòi chạy câu SQL nặng. Database nổ tung ngay lập tức!
*Giải pháp*: Dùng cơ chế "Khóa" (Lock/Mutex) trong Redis. Ai xuống trước lấy Khóa, 9,999 người kia phải đứng đợi (sleep) cho đến khi người đầu tiên mang dữ liệu lên bỏ vào Cache lại.

</details>

### 1. The "Stale Data" Problem (Cache Invalidation)
*"There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton*
If a CMS admin updates an article's title in the RDS database, but ElastiCache still holds the old title in RAM, users see outdated content (Stale Data).
*Mitigations*:
- **Time-To-Live (TTL)**: ALWAYS attach a TTL (e.g., 5 minutes) to every cached object. After 5 minutes, Redis automatically deletes it, forcing the app to fetch fresh data from the DB.
- **Write-Through Pattern**: Change your Backend code so that every time it runs an SQL `UPDATE`, it also actively pushes the new value into Redis. This ensures the cache is never stale, but slows down Write operations.

### 2. The Cache Stampede
Imagine the TTL for the "Live World Cup Score" expires. At that exact millisecond, 50,000 users refresh the page. All 50,000 threads experience a Cache Miss simultaneously. All 50,000 threads bypass the empty cache and query the fragile RDS database at the exact same time. The database is instantly annihilated.
*Mitigation*: Implement a Distributed Lock in Redis (e.g., Redlock algorithm). When a Cache Miss occurs, the first thread acquires a lock and goes to the Database. The other 49,999 threads check the lock, realize someone is already fetching the data, and simply sleep for 50ms, then check the Cache again.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một hàm Python (dùng thư viện `redis`) mô tả chính xác mô hình **Lazy Loading (Cache-Aside)** phổ biến nhất.

</details>

### The Cache-Aside (Lazy Loading) Pattern in Python

This pattern is the bedrock of implementing ElastiCache Redis in any web application backend.

```python
import redis
import json
import db_module # Fictional module representing your RDS connection

# Connect to ElastiCache Redis endpoint
cache = redis.Redis(host='my-elasticache-cluster.aws.com', port=6379, db=0)

def get_product_details(product_id):
    cache_key = f"product:{product_id}"
    
    # 1. Ask the Cache first
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print("CACHE HIT! Returning data in 1ms.")
        return json.loads(cached_data)
        
    print("CACHE MISS! Going to the Database...")
    # 2. If not in cache, execute the slow SQL query
    product_data = db_module.execute_slow_sql_query(product_id)
    
    if product_data:
        # 3. Write to Cache for the NEXT user. 
        # CRITICAL: Always set an expiration (ex=3600 seconds) to prevent Stale Data!
        cache.set(name=cache_key, value=json.dumps(product_data), ex=3600)
        
    return product_data
```

---

## Related Topics

- [AWS RDS](./aws-rds-and-aurora.md) — The persistent database that ElastiCache protects.
- [AWS EC2 / Auto Scaling](./aws-ec2.md) — The web servers that execute the Cache-Aside logic.
- [System Design: Caching](../../10-system-design/03-caching.md) — Broader architectural concepts beyond just AWS.
