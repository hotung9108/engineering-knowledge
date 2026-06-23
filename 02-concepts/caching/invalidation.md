# Cache Invalidation

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: "Có 2 thứ khó nhất trong ngành Khoa học máy tính: Đặt tên cho biến, và Xóa Cache (Cache Invalidation)" - *Phil Karlton*. Khi dữ liệu trong Database thay đổi, dữ liệu nằm trong RAM (Cache) lập tức trở thành đồ cũ (Stale Data). Nếu không xóa bản cũ đi, khách hàng sẽ chửi vì họ vừa đổi tên mà trên web vẫn hiện tên cũ. **Cache Invalidation** là các kỹ thuật để "Báo cho Cache biết là dữ liệu đã cũ rồi, hãy ném nó đi".

</details>

> **Summary**: *"There are only two hard things in Computer Science: cache invalidation and naming things."* — Phil Karlton. When a record in the primary Database is mutated (Updated or Deleted), the corresponding replica of that record sitting in the Cache instantly becomes **Stale Data**. If the system continues serving this stale replica, the user experiences data inconsistency (e.g., they change their profile picture, but the old picture stubbornly remains on the screen). **Cache Invalidation** encompasses the architectural strategies employed to aggressively evict or update these obsolete cache entries the moment the underlying truth changes.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn bán Bánh Mì. Bạn dán một tờ Bảng Giá trên tường (Đây là Cache).
1. **Time-To-Live (Chờ hết hạn)**: Mỗi sáng, bạn dán bảng giá mới. Hết ngày (Hết TTL), bạn lột bảng giá vứt đi. Bất chấp buổi trưa giá bột mì có tăng, bạn vẫn phải bán giá cũ cho đến hết ngày. (Dễ làm, nhưng giá bị sai lệch nguyên ngày).
2. **Event-Driven (Xóa chủ động)**: Khi giá bột mì tăng lúc 12h trưa, bạn lập tức chạy ra xé cái Bảng giá cũ đi và dán đè bảng giá mới lên. Khách hàng luôn luôn thấy giá mới nhất. (Khó làm, vì bạn phải luôn canh chừng giá bột mì để chạy ra xé giấy).

</details>

Imagine you run a Coffee Shop. You write the Daily Menu on a Chalkboard outside (The Cache).
1. **Time-To-Live (TTL Expiration)**: You write the menu at 8 AM and wipe it clean at 8 PM (A 12-hour TTL). If you run out of Croissants at 1 PM, the Chalkboard still says you have them until 8 PM. Customers order them and get angry. (Extremely easy to implement, but highly inconsistent).
2. **Active Invalidation (Event-Driven)**: The exact second the baker pulls the last Croissant from the oven and gives it to a customer, you sprint outside and aggressively erase "Croissant" from the Chalkboard. The next customer instantly knows it's sold out. (Perfectly consistent, but requires enormous operational effort and immediate communication).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 3 cách chính để làm cho Cache "chết đi":
1. **Purge (Xóa sạch)**: Dùng súng bắn rụng toàn bộ Cache. Xóa sạch mọi thứ không chừa cái gì.
2. **Absolute TTL (Sống đúng số giờ)**: Đặt bom nổ chậm. Ví dụ `TTL = 60s`. Mặc kệ thế giới, đúng 60 giây sau thì tự sát.
3. **Active Invalidation (Hủy theo sự kiện)**: Xóa mục tiêu bằng tia laser. Xóa đích danh 1 dòng Cache cụ thể ngay khi dòng đó ở dưới DB bị sửa đổi.

</details>

There are three primary mechanisms to evict data from a Cache:
1. **Global Purge (Flush All)**: The nuclear option. Executing a command (like Redis `FLUSHALL`) to instantly obliterate the entire Cache. Used only during massive system upgrades or catastrophic state corruption.
2. **Absolute Time-To-Live (TTL)**: The passive approach. Assigning a strict expiration timestamp upon creation (e.g., `EXPIRE 3600`). The cache automatically evicts the key after 1 hour, regardless of whether the underlying data changed.
3. **Active Invalidation (Event-Driven)**: The surgical approach. Programmatically executing an explicit `DELETE` command against a highly specific Cache Key (e.g., `DEL user:profile:123`) the exact millisecond the Database row for `user_id = 123` is mutated.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu dữ liệu của bạn là Lịch sử quay thưởng Xổ Số năm 2020, nó không bao giờ thay đổi, bạn không cần Invalidation (Set TTL = vô cực).
Nhưng hầu hết ứng dụng là dữ liệu Động (Dynamic Data). Bạn làm App Ngân hàng. Khách vừa chuyển đi 5 triệu. Nếu bạn không Xóa/Cập nhật Cache của số dư tài khoản, khách load lại trang web và thấy tiền vẫn còn y nguyên, họ sẽ hoảng loạn hoặc lợi dụng lỗi để chuyển tiền lần 2 (Double Spending). Cache Invalidation tồn tại để bảo vệ tính **Toàn vẹn Dữ liệu (Data Integrity)**.

</details>

If your application strictly serves immutable historical data (e.g., "Results of the 1994 World Cup"), Cache Invalidation is irrelevant. You cache it with an infinite TTL.
However, 99% of modern applications handle highly volatile, mutable state. Consider a Banking Dashboard. A user transfers $5,000 out of their account. The Database registers the deduction. If the backend fails to invalidate the `account:balance:99` cache key, the user refreshes the page and sees their original balance. They either panic (thinking the transfer failed) or maliciously attempt a Double-Spend attack. Cache Invalidation exists exclusively to enforce **Data Integrity** in distributed systems.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt khi code Cập nhật User Profile có và không có Invalidation.
</details>

Visualizing the code execution flow for a Profile Update.

| Step | Passive (TTL Only) - Vulnerable | Active Invalidation - Robust |
|---|---|---|
| **1. User Action** | Edits Name: `John` $\rightarrow$ `Johnny` | Edits Name: `John` $\rightarrow$ `Johnny` |
| **2. DB Update** | `UPDATE users SET name='Johnny'` | `UPDATE users SET name='Johnny'` |
| **3. Cache Action**| (Does nothing) | `REDIS.DEL("user:123")` |
| **4. User Refresh**| User sees `John` (angry, frustrated) | Cache Miss $\rightarrow$ Queries DB $\rightarrow$ Sees `Johnny` |
| **5. Consistency** | Stale for the next 59 minutes | Perfectly Consistent |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Gắn Tag dựa trên ID (Key Tagging)**: Để xóa Cache chính xác. Đừng đặt tên Cache chung chung như `cache_1`. Hãy đặt là `article:55:comments`. Khi bài viết số 55 có comment mới, bạn chỉ cần ra lệnh xóa đúng cái chìa khóa `article:55:comments`.
2. **Webhook Invalidation (Headless CMS)**: Bạn dùng WordPress hoặc Contentful. Khi nhà báo bấm nút "Xuất bản bài viết", Contentful sẽ bắn một cục API (Webhook) sang Server NextJS của bạn. Server NextJS nhận được lệnh, lập tức gọi hàm xóa Cache bài viết đó để độc giả thấy ngay lập tức.
3. **Change Data Capture (CDC - Debezium)**: Siêu nâng cao. Ở các công ty lớn như Uber/Grab, code Backend có cả ngàn file, rất dễ quên viết dòng lệnh xóa Cache. Họ dùng công cụ CDC (như Kafka + Debezium) cắm thẳng vào Database. Hễ Database nhúc nhích đổi dữ liệu, CDC tự động chớp lấy sự kiện và chạy đi xóa Cache hộ Backend. Không bao giờ quên!

</details>

1. **Semantic Key Tagging**: The foundation of surgical invalidation is establishing a rigid, semantic naming convention for Cache Keys. You do not name a key `home_data`. You namespace it structurally: `user:{id}:profile`. When the `UpdateProfile` endpoint is hit, the code knows exactly to execute `redis.del('user:123:profile')`.
2. **Webhook/On-Demand Revalidation (Next.js / ISR)**: Modern JAMStack frameworks (Next.js) heavily cache rendered HTML at the CDN edge. When an editor updates a post in a Headless CMS (Sanity/Contentful), the CMS fires an asynchronous Webhook payload to the Next.js API. The Next.js API executes `revalidatePath('/blog/post-1')`, which purges the edge cache explicitly for that single URL.
3. **Change Data Capture (CDC) via Debezium**: The enterprise pinnacle of invalidation. In massive microservice architectures, relying on human developers to remember to write `redis.del()` in every single mutation endpoint guarantees eventual human error (Stale Data leaks). Architects deploy CDC tools (Debezium) that physically tail the Database's Write-Ahead Log (WAL/Binlog). When a database row changes at the hardware level, Debezium streams an event to Kafka, which automatically and immutably invalidates the corresponding Cache replica.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Xóa Cache (Invalidate) tốt hơn Ghi đè (Update)**: Khi DB đổi tên thành `Johnny`. Thay vì bạn lấy chữ `Johnny` đó GHI ĐÈ vào Cache (Tốn CPU để tính toán/Format dữ liệu lại). Hãy cứ thẳng tay XÓA BỎ cái chìa khóa Cache đó đi. Lần sau ai đọc thì hệ thống sẽ tự chọc xuống DB lấy lên bản mới. Xóa luôn luôn an toàn hơn Ghi đè trong môi trường chạy song song (Concurrency).
2. **Luôn có Backup bằng TTL**: Ngay cả khi bạn tự tin là mình đã viết code Xóa Cache (Active Invalidation) ở khắp mọi nơi, hãy LUÔN LUÔN set một cái TTL (Ví dụ: 24 giờ). Nếu lỡ code bị bug không chạy lệnh xóa, thì cùng lắm 24h sau hệ thống cũng tự dọn rác. Đừng bao giờ set TTL vô hạn cho dữ liệu động.

</details>

1. **Delete (Invalidate) > Update (Mutate)**: When a Database record changes, you have two choices: recalculate the new JSON and `SET` it into the Cache, or simply `DEL` the cache key. **Always Delete**. Recalculating complex cache objects synchronously drastically increases write latency. More importantly, in highly concurrent systems with Race Conditions, Thread A might write older data *after* Thread B writes newer data, corrupting the Cache permanently. A `DEL` command elegantly forces the next read request to lazily fetch the absolute Source of Truth.
2. **The "Belt and Suspenders" Rule (Always use TTLs)**: Even if you have implemented a mathematically flawless Event-Driven Invalidation architecture, you **MUST** still assign a fallback TTL to every single key (e.g., `24 hours`). Software is fallible. Network partitions occur. Webhooks drop. If an invalidation event is lost in the network ether, a key without a TTL will remain stale for eternity. The TTL acts as the ultimate fail-safe garbage collector.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Thứ tự Ghi Cache & DB bị ngược (Race Condition)**:
   - Bạn viết code: `redis.del("user_1"); db.update("user_1");` (Xóa Cache xong mới Update DB).
   - *Lỗi xảy ra*: Bạn vừa Xóa Cache xong (chưa kịp Update DB), có một thằng User khác bay vào đọc. Nó thấy Cache trống, nó chạy xuống DB đọc cái tên cũ (Vì bạn chưa kịp update), xong nó mang cái tên Cũ rích đó LƯU LẠI VÀO CACHE. Thế là bạn Update DB xong vô ích, Cache vẫn dính data cũ mãi mãi.
   - *Luật tối thượng*: **LUÔN LUÔN UPDATE DB TRƯỚC, RỒI MỚI XÓA CACHE**.

</details>

1. **The Write-Invalidate Race Condition**: Ordering matters catastrophically.
   - *The Anti-Pattern*: `redis.del(key); db.update(key);`
   - *The Disaster*: Thread A deletes the Cache Key. Before Thread A can execute the DB update, Thread B executes a Read. Thread B encounters a Cache Miss. Thread B queries the Database, retrieving the *OLD* data. Thread B inserts the *OLD* data into the Cache. Finally, Thread A finishes updating the DB to the *NEW* data.
   - *The Result*: The Database has the new data, but the Cache is permanently poisoned with the old data.
   - *The Absolute Rule*: **Always mutate the primary Database FIRST, and execute the Cache Invalidation (`DEL`) SECOND.** (Though advanced architectures use Delayed Double Delete to be perfectly safe).

---

## Related Topics

- For the foundational definition of Caching, see **[Caching Overview](./overview.md)**.
- To understand when Cache Misses happen, see **[Caching Strategies](./strategies.md)**.
- For how CDC (Change Data Capture) works to automatically invalidate caches, see **[Event-Driven Architecture](../event-driven/overview.md)**.
