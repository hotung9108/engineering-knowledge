# Distributed Caching

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi Website của bạn lớn lên, chạy trên 1 Server là không đủ. Bạn phải mua 10 Servers để phục vụ hàng triệu người. Nếu mỗi con Server tự sắm 1 cái Cache cục bộ (In-Memory Cache), thì dữ liệu trên 10 cái Cache này sẽ không đồng nhất với nhau. Mọi thứ trở nên hỗn loạn. **Distributed Caching (Bộ nhớ đệm phân tán)** ra đời bằng cách gom tất cả Cache ra một cụm Server riêng biệt (Ví dụ: Redis Cluster). Cả 10 Servers web đều gọi chung vào cụm Cache đó. Dữ liệu luôn đồng bộ 100%.

</details>

> **Summary**: In monolithic architectures, a localized, in-memory cache (like a Python Dictionary or Java `ConcurrentHashMap`) suffices. However, as systems scale horizontally across 50 Application Servers behind a Load Balancer, local caches inevitably desynchronize, leading to catastrophic data inconsistency across nodes. **Distributed Caching** physically decouples the caching layer from the application layer. It deploys a dedicated, standalone cluster of cache nodes (e.g., Redis or Memcached) that all Application Servers access via the network. This architecture guarantees a unified, globally consistent, and highly available caching state.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn điều hành một hệ thống 5 Quán Cà phê.
1. **Local Cache (Sổ tay cá nhân)**: Mỗi quán cà phê tự mua một cuốn Sổ ghi nợ. Khách hàng A vay 50k ở Quán 1. Quán 1 ghi vào sổ. Hôm sau khách hàng A ra Quán số 2. Quán số 2 lật sổ của mình ra thấy trống trơn, bèn cho vay tiếp. (Lỗi dữ liệu nghiêm trọng).
2. **Distributed Cache (Hệ thống đám mây)**: Bạn dẹp hết Sổ tay cá nhân. Bạn mua một cái iPad dùng chung (Google Sheets). Bất kỳ quán cà phê nào có người vay tiền, đều cập nhật thẳng lên cái iPad đó. Quán số 2 chỉ cần mở iPad ra là biết ngay khách A đang nợ tiền từ Quán 1. (Dữ liệu đồng nhất hoàn toàn).

</details>

Imagine operating a chain of 5 Coffee Shops.
1. **Local In-Memory Cache**: Each barista maintains their own physical "Customer Debt" notepad at their counter. Customer John borrows $5 at Shop #1. Shop #1 writes it down. The next day, John visits Shop #2. Shop #2 checks their local notepad, sees no debt, and loans John another $5. The data is entirely fragmented and inconsistent.
2. **Distributed Cache**: You throw away the physical notepads. You issue an iPad to every shop, all connected to a single centralized Google Sheet. When John borrows $5 at Shop #1, they record it in the cloud. When John visits Shop #2, they check the unified Google Sheet over the network and instantly see the $5 debt. Total consistency is achieved.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Local Cache (Cache cục bộ)**: RAM nằm ngay bên trong con chip của Server chạy code (Ví dụ: Map, Dictionary, Guava Cache). Tốc độ bàn thờ (Vài nano giây), nhưng dung lượng rất ít và bị mất khi khởi động lại code.
**2. Distributed Cache (Cache phân tán)**: RAM nằm trên những cỗ máy chủ khác. Application phải gửi lệnh đi qua mạng LAN để lấy dữ liệu (Ví dụ: Redis, Memcached). Tốc độ chậm hơn một chút (Vài mili giây) nhưng dung lượng là vô hạn vì có thể ghép 100 máy Redis lại với nhau (Cluster).

</details>

**1. Local (In-Memory) Cache**: Memory allocated directly within the executing application's process space (e.g., Java's `Ehcache` / `Guava`, or a Node.js `Map`). Access times are nanoscopic (L1/L2 Cache speeds) because there is no network traversal. However, it suffers from hard memory limits, ephemeral lifecycles (data dies when the app restarts), and an inability to share state with other instances.
**2. Distributed Cache**: An external, network-attached storage layer (e.g., **Redis**, **Memcached**, **Hazelcast**). The Application must serialize the data and transmit it over a TCP/IP network. While introducing slight network latency (0.5ms - 2ms), it provides persistent state, independent scalability, and a single source of truth for an infinite number of horizontal application nodes.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi làm Microservices, bạn bắt buộc phải dùng Distributed Cache vì bài toán **Session Management (Quản lý phiên đăng nhập)**.
Người dùng đăng nhập thành công ở `Server A`. Lần nhấp chuột tiếp theo, Load Balancer đẩy người dùng sang `Server B`.
- Nếu dùng Local Cache: `Server B` sẽ hỏi: "Ủa, bạn là ai, đăng nhập lại đi". Người dùng sẽ phát điên.
- Nếu dùng Distributed Cache: `Server A` lưu Session vào Redis. Khi sang `Server B`, `Server B` thọc tay vào Redis lấy Session ra $\rightarrow$ Mượt mà như chưa từng có cuộc chia ly. Mọi máy chủ đều là "Stateless" (Không trạng thái).

</details>

Distributed Caches are the structural prerequisite for the **Stateless Architecture** demanded by Cloud-Native Microservices.
The classic problem is **Stateful Session Management**. A user authenticates via a Load Balancer, routing them to `App Node 1`. `Node 1` generates a Session and stores it in its Local Cache. On the user's very next HTTP request, the Load Balancer routes them to `App Node 2`. `Node 2` checks its Local Cache, finds nothing, and aggressively forces the user back to the login screen.
By extracting the Session State into an external Distributed Cache (Redis), every single App Node becomes entirely Stateless. Whether the user hits `Node 1`, `Node 50`, or a brand new autoscaled `Node 99`, the node simply queries Redis over the network and instantly recovers the user's session.

---

## Layer 3: Without vs. With Comparison (Compare)

### Data Desynchronization Risk

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự kinh hoàng khi Cập nhật Giá sản phẩm bằng Local Cache.
</details>

Visualizing the catastrophe of mutating state across horizontally scaled Local Caches.

| Step | Multi-Node Local Cache (Disaster) | Distributed Cache (Robust) |
|---|---|---|
| **1. Update** | Admin changes Item Price from $10 to $20 on Node 1. | Admin changes Price to $20. |
| **2. Storage** | Node 1 updates its internal RAM to $20. | Node 1 executes `redis.set('price', 20)`. |
| **3. Other Nodes**| Node 2, 3, and 4 are completely unaware of the change. | Redis globally holds the value $20. |
| **4. User Traffic**| User hits Node 2 and buys the item for the stale price of $10. | User hits Node 2, Node 2 queries Redis, sees $20. |
| **Result** | **Massive Revenue Loss & Chaos**. | **Globally Consistent Data**. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Lưu Session**: (Như đã giải thích ở trên). Redis là trùm lưu Session.
- **Rate Limiting (Chống Spam)**: Ngăn chặn 1 IP F5 trang web 100 lần/giây. Bạn phải dùng Redis để lưu số lần F5 của IP đó. Vì nếu dùng Local Cache, IP đó chọc vào 10 Server khác nhau thì mỗi Server lại đếm từ số 1, dẫn đến việc IP đó bypass (vượt mặt) được cơ chế Rate Limit.
- **Pub/Sub (Đồng bộ hóa)**: Ứng dụng chat. User A chat với User B. User A đang cắm vào Server 1. User B đang cắm vào Server 2. Làm sao Server 1 báo cho Server 2 biết có tin nhắn? Nó dùng kênh Pub/Sub của hệ thống Distributed Cache (Redis) làm người đưa thư đứng giữa.

</details>

- **Centralized Session Stores**: Replacing legacy database-backed sessions with Redis ensures sub-millisecond session validation across thousands of microservices globally.
- **Distributed Rate Limiting**: Enforcing an API limit of "100 requests per minute per IP". A Local Cache algorithm fails miserably behind a Round-Robin Load Balancer (an attacker can hit 10 different nodes, getting 1,000 requests instead of 100). A Distributed Cache guarantees the counter is incremented globally and atomically across the entire cluster.
- **Distributed Locking / Mutexes**: Preventing the "Thundering Herd" or race conditions. If a cron job must only be executed by *exactly one* worker out of 50, the nodes will race to set a lock in Redis (`SETNX - Set if Not eXists`). The single victor executes the job; the others yield.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Chiến thuật kết hợp (Two-Level Caching)**: Vì gọi qua mạng tốn 2ms, đôi khi người ta kết hợp cả 2. Level 1 là Local Cache (chỉ lưu 1 giây cho các API bị Spam quá nhiều). Cứ Miss ở L1 thì mới chạy qua Level 2 là Distributed Cache.
2. **Sharding / Partitioning**: Khi dung lượng Cache phình to lên 1000GB. Một con Redis không thể chịu nổi (Redis chạy đơn luồng). Ta phải cắt nhỏ 1000GB đó ra chia cho 10 con Redis (Mỗi con gánh 100GB). Kỹ thuật này gọi là Redis Cluster.

</details>

1. **Two-Level Caching (L1/L2 Architecture)**: While Distributed Caching is fast, network TCP overhead still incurs ~1ms of latency. For extreme-throughput endpoints (e.g., rendering a static homepage banner requested 50,000 times a second), architects employ an L1 Local Cache (e.g., Guava) with an aggressive 3-second TTL, backed by an L2 Distributed Cache. This absorbs 99.9% of the read volume directly in the CPU process, while falling back to the globally consistent Redis cluster.
2. **Consistent Hashing & Cluster Sharding**: A single Redis node operates on a single CPU thread and is constrained by the physical RAM of its host. To scale to Terabytes of cache, the dataset must be partitioned (Sharded). Tools like Redis Cluster utilize **Consistent Hashing** algorithms to evenly distribute keys across multiple nodes. This ensures that if one node crashes, only a fraction of the cache is lost, preventing a total system avalanche.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lạm dụng Distributed Cache cho mọi thứ**: Nhiều người lôi Cấu hình hệ thống (Ví dụ: Tiền tệ là VNĐ, Ngôn ngữ là VN) bỏ vào Redis. Những thứ này cả năm không đổi 1 lần, bỏ vào Redis sẽ làm hệ thống tự dưng bị dính độ trễ mạng (Network Latency) một cách ngớ ngẩn. Hãy bỏ nó vào Local Cache hoặc biến tĩnh trong Code.
2. **Nút thắt cổ chai Mạng (Network Bottleneck)**: Bạn ném một chuỗi JSON nặng 10MB vào Redis. Mỗi lần người dùng load trang, App của bạn phải kéo 10MB đó qua mạng cáp quang nội bộ. Băng thông mạng sẽ bị bóp nghẹt. Hãy nhớ: **Chỉ lưu dữ liệu nhỏ gọn vào Cache**.

</details>

1. **Unnecessary Network Overhead for Static Data**: Storing highly static application configurations (e.g., Tax Rates, Country Codes, Error Message templates) inside a Distributed Cache is an architectural anti-pattern. You are forcing the CPU to serialize data, open a TCP socket, wait for network transit, and deserialize the JSON, just to retrieve a string that hasn't changed in 5 years. Use simple in-memory constants or a Local Cache for immutable state.
2. **The "Fat Key" Network Bottleneck**: Storing monolithic, 5-Megabyte JSON blobs into a single Redis key. When 1,000 concurrent users request this key, the Application Servers attempt to drag 5 Gigabytes of data per second across the internal VPC network. This instantly saturates the Network Interface Cards (NICs), crashing the connection before the CPU or RAM even breaks a sweat. **Rule**: Cache payloads must be deeply granular and minimized.

---

## Related Topics

- For how multiple Database nodes coordinate (which applies to Redis Clusters too), see **[Distributed Systems / Consensus](../distributed-system/consensus.md)**.
- For managing Sessions effectively, read **[Authentication / JWT](../authentication/jwt.md)**.
- For the specific technology behind this, study **[Redis](../../03-technologies/database/redis.md)**.
