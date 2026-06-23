# Long-Polling

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước khi HTML5 đẻ ra SSE và WebSocket, làm sao để web có chức năng Realtime? Các kỹ sư đã "hack" giao thức HTTP cũ kỹ bằng kỹ thuật **Long-Polling (Giữ kết nối dài)**. Thay vì gọi Server rồi Server trả lời ngay (dù không có dữ liệu), Long-Polling bắt Server "Treo máy chờ". Server cứ im lặng chờ từ 30s đến 60s. Khi nào có dữ liệu mới thì mới nhả về cho Client. Vừa trả về xong, Client lập tức gọi lại ngay một cuốc "treo máy" mới. Dù lỗi thời, nó vẫn là giải pháp cực kỳ tin cậy và không bao giờ bị Firewall chặn.

</details>

> **Summary**: Prior to the standardization of native HTML5 Realtime protocols (WebSocket and SSE), software engineers required a mechanism to simulate Server-Push capabilities over a stateless protocol. They engineered a clever, slightly abusive architectural pattern called **Long-Polling**. Instead of the Server immediately returning an empty response when no new data is available, the Server intentionally hangs the HTTP request open. It stalls for up to 60 seconds. The moment an event occurs, the Server completes the response. The Client parses the data and immediately initiates a new hanging connection. While considered legacy, it remains the ultimate fallback mechanism due to its 100% compatibility with all proxies and firewalls.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn gọi điện cho cửa hàng hỏi mua iPhone 16.
1. **Short-Polling (Hỏi dồn dập)**: Bạn gọi: "Có hàng chưa?". Nhân viên: "Chưa". Cụp máy. 5 phút sau bạn lại gọi. Một ngày bạn gọi 200 cuộc, tốn tiền điện thoại mà vẫn không có hàng.
2. **Long-Polling (Treo máy)**: Bạn gọi: "Có hàng chưa?". Nhân viên: "Anh cứ giữ máy đấy, bao giờ xe hàng về em báo luôn, nếu 1 tiếng sau xe chưa về thì em tự tắt máy nhé". Bạn để điện thoại trên bàn. Đúng 30 phút sau xe về, nhân viên hét lên: "Có hàng rồi anh!". Cụp máy. Bạn (Client) lập tức gọi lại cuộc gọi mới để chờ mua iPhone 17.

</details>

Imagine calling a Bakery to see if fresh bread is ready.
1. **Short-Polling (The Annoying Customer)**: You call: "Is it ready?". Baker: "No." *Click*. You call 1 minute later: "Is it ready?". Baker: "No." *Click*. You exhaust the Baker and your own phone battery.
2. **Long-Polling (The Waiting Game)**: You call: "Is it ready?". The Baker says: "Hang on, let me watch the oven. Don't hang up." You hold the phone to your ear for 20 minutes in silence. Suddenly, the oven dings. The Baker says: "It's ready, come get it!" *Click*. If you want the next batch, you immediately call back and hold the line again in silence.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Vẫn là HTTP Request bình thường**: Long-Polling không phải là giao thức mới. Nó là HTTP GET/POST 100% truyền thống.
**2. Nghệ thuật "Trì hoãn" (Hanging)**: Điểm khác biệt là ở Backend. Thay vì code Backend chạy `return response` ngay lập tức, Backend được lập trình một cái vòng lặp `while(true)` hoặc `Sleep`. Nó thức canh Database/Redis. Chừng nào có dữ liệu, nó mới chạy lệnh `return`.
**3. Timeout (Giới hạn thời gian)**: Không thể treo máy vĩnh viễn vì Router/Firewall sẽ tự động cắt mạng. Thường Server chỉ dám treo tối đa 30 đến 60 giây. Nếu sau 60s không có dữ liệu, Server sẽ trả về `HTTP 204 No Content`. Client nhận được 204 thì lập tức tạo một request treo 60s mới.

</details>

**1. Strictly Legacy HTTP**: Long-Polling requires zero protocol upgrades. It operates purely on HTTP/1.0 or HTTP/1.1 semantics.
**2. Intentional Thread Hanging**: The architectural core is Server-side manipulation. Instead of immediately flushing an HTTP Response, the Backend Controller explicitly pauses execution. It subscribes to an internal Event Bus or Redis channel. It holds the network socket hostage. Only when a relevant payload arrives does the Backend serialize the JSON and flush the Response, completing the HTTP transaction.
**3. The Timeout Window**: TCP sockets cannot hang indefinitely. Intermediate proxies (Load Balancers, NATs) forcefully drop idle connections (usually at the 60-second mark). Therefore, Long-Polling implements a controlled Timeout. If no data arrives within 50 seconds, the Server gracefully returns a `200 OK` (with an empty body) or `204 No Content`. The Client receives this, and instantaneously fires an identical 50-second request to resume waiting.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Khả năng tương thích 100% (Maximum Compatibility)**: Tại sao ngày nay người ta vẫn dùng cái đồ cổ này? Vì WebSocket đôi khi bị mạng của Công ty, Trường học, hoặc Firewall chặn đứng (Chặn cổng, chặn giao thức lạ). SSE thì hay bị Proxy cắt ngang. Nhưng Long-Polling thì "hòa tan" hoàn toàn vào mạng Internet. Bất kỳ Firewall nào cho phép truy cập Web (`http`) thì đều phải cho phép Long-Polling đi qua.
**2. Sự cứu rỗi của Socket.IO (Fallback)**: Khi bạn dùng thư viện Socket.IO, mặc định nó sẽ thử mở WebSocket. Nếu thất bại (do mạng người dùng cấu hình cực đoan), nó sẽ "Hạ cấp" (Downgrade) tự động chuyển sang Long-Polling. Người dùng vẫn dùng App mượt mà, không hề biết ở dưới mui xe có sự thay đổi lớn.

</details>

**1. Absolute Universal Compatibility**: Why does a legacy hack still exist in modern architectures? **Hostile Networks**. Enterprise firewalls, strict DPI (Deep Packet Inspection) boxes, and aggressive antivirus software often arbitrarily block WebSocket `Upgrade` headers. SSE connections are frequently butchered by aggressive Nginx reverse proxies. Long-Polling, however, is cosmetically identical to standard HTTP traffic. If a user can load a webpage, Long-Polling will work. It mathematically guarantees connectivity.
**2. The Ultimate Fallback (Socket.IO)**: This is the exact architectural premise of libraries like Socket.IO or SignalR. They execute an initial probe. If WebSocket establishment fails or times out due to hostile network topology, the engine gracefully degrades (Fallbacks) to XHR Long-Polling. The Realtime application continues functioning flawlessly without dropping data, providing extreme resilience.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh độ hao tốn tài nguyên khi đợi 1 tin nhắn mất 3 phút mới tới.
</details>

Visualizing the Request/Response cycle when an event takes exactly 3 minutes (180 seconds) to occur.

| Metric | Short Polling (Every 1s) | Long-Polling (60s Timeout) |
|---|---|---|
| **Total Requests Made**| 180 Requests | 3 Requests |
| **Server Actions** | Server processes 180 DB queries. | Server idles 3 times, queries DB once. |
| **Bandwidth Wasted** | Massive (180 sets of HTTP Headers sent).| Minimal (3 sets of HTTP Headers sent). |
| **Latency of Event** | Between 0ms to 1000ms. | Instantaneous (The open connection captures it). |
| **Verdict** | Brutal Server DDoS. | Efficient, simulated Server-Push. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Trạng thái Thanh toán QR (Payment Gateways)**: Bạn quét mã Momo trên màn hình máy tính. Trang web tự động nhảy sang "Thành công" khi bạn vừa bấm nút trên điện thoại. Thay vì setup WebSocket phức tạp cho việc 1 lần này, Frontend gọi Long-Polling lên API Check_Order. Server treo máy chờ Webhook của Momo bắn về. Bắn về phát nhả cho Frontend nhảy trang luôn.
2. **Ứng dụng Doanh nghiệp cũ (Legacy B2B)**: Các hệ thống Ngân hàng cũ, Cổng thông tin Chính phủ nội bộ, nơi mà mạng LAN cấu hình bảo mật siết rất chặt, chặn hết mọi giao thức lạ. Long-Polling là vị cứu tinh duy nhất để làm tính năng Thông báo.
3. **Các chiến dịch Marketing có tải trọng khủng khiếp (Flash Sale)**: 1 triệu người dùng cùng lúc lao vào chờ kết quả Quay số lúc 12h đêm. Nếu dùng WebSocket, Server đứt bóng vì thiếu RAM giữ kết nối. Nếu dùng Short Polling, Server đứt bóng vì nghẽn CPU. Long-Polling kết hợp với Nginx/Redis là giải pháp sinh tồn mượt mà.

</details>

1. **QR Code Payment Verification (One-Off Events)**: A user generates a Stripe/PayPal QR code on a desktop. The desktop browser needs to know exactly when the mobile phone completes the transaction. Opening a WebSocket for a single, transient transaction is architectural overkill. The Frontend simply issues a 60-second Long-Poll `GET /order/{id}/status`. The Backend hangs. When the Payment Gateway fires the async Webhook to the Backend, the Backend resolves the Long-Poll. Perfect latency, zero complexity.
2. **Hostile Intranet Environments (B2B/Gov)**: Enterprise software deployed inside highly restrictive Government or Military networks where proxy servers rigorously strip non-standard HTTP Headers, completely neutralizing WebSockets and SSE. Long-Polling guarantees the "Live Dashboard" feature functions regardless of network paranoia.
3. **Massive Flash Sales / Ticking Clocks**: "Waiting Rooms" for ticket sales (e.g., Taylor Swift concerts). 5 million users waiting for a counter to hit zero. Long-Polling allows the CDN (like Cloudflare) to absorb the massive held connections at the Edge, periodically refreshing them, and instantly flushing the "Open" signal to millions of clients simultaneously without routing 5 million raw TCP sockets to the origin server.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Xử lý Timeout cẩn thận**: Khi Client gửi Request treo 60s, bạn phải code sao cho Backend nhả về kết quả trước mốc 60s (Ví dụ: Đúng 55 giây là tự động trả về `204 No Content`). Nếu bạn để quá lố, Nginx sẽ ném lỗi `504 Gateway Timeout` (Lỗi Đỏ lòm trên Console của Trình duyệt), trông rất thiếu chuyên nghiệp và dễ gây rác Log hệ thống.
2. **Đừng treo Thread (Cạn kiệt Thread Pool)**: Sai lầm khủng khiếp nhất của Junior Dev là dùng hàm `Thread.sleep()` trong Java/C# để giữ Request. Nếu có 10.000 User vào web, Server sẽ tạo ra 10.000 Threads đang "Ngủ". Server sẽ sụp đổ vì quá tải bộ nhớ RAM (OOM). Bắt buộc phải dùng kiến trúc **Non-blocking I/O (Async/Await, WebFlux, NodeJS)** để giữ 10.000 kết nối chỉ với 1 Thread duy nhất.

</details>

1. **Precision Timeout Engineering**: Never allow the Reverse Proxy (Nginx) to sever the connection. If Nginx is configured with `proxy_read_timeout 60s`, your application code MUST forcefully resolve the pending request at exactly `55s` with an empty `200 OK`. If you allow Nginx to kill the connection, it generates a harsh `504 Gateway Timeout` error, polluting monitoring dashboards and triggering unnecessary PagerDuty alerts.
2. **Asynchronous Non-Blocking I/O (The Absolute Mandate)**: The most fatal architectural mistake is implementing Long-Polling using legacy Synchronous, Thread-Per-Request web servers (e.g., older Tomcat/Spring MVC setups). If you call `Thread.sleep(50000)` to wait for an event, that OS Thread is paralyzed. 10,000 concurrent Long-Polled users will spawn 10,000 idle threads, instantly causing a JVM `OutOfMemoryError` and crashing the node. You **MUST** utilize Event-Driven, Non-Blocking architectures (Node.js, Go Goroutines, Spring WebFlux, Python Asyncio) where 10,000 suspended connections consume virtually zero CPU/RAM.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Rủi ro mất tin nhắn (Data Loss trong tích tắc)**: Long-Polling có một điểm mù nguy hiểm. Client treo máy 60s $\rightarrow$ Hết 60s Server báo rỗng $\rightarrow$ Client chuẩn bị gửi Request mới (Tốn khoảng 50 mili-giây để nối lại mạng). ĐÚNG TRONG 50 MILI-GIÂY ĐÓ, có người gửi tin nhắn đến. Server không thấy Client đâu nên nó không gửi được, tin nhắn bay màu.
   - *Cách giải quyết*: Phải dùng ID tin nhắn (Cursor). Lần gọi tiếp theo Client nói: "Hồi nãy tao đọc đến tin nhắn số 10 rồi, đưa tao từ số 11". Dù Client có rớt mạng 5 giây đi nữa, kết nối lại vẫn lấy đủ.
2. **Cập nhật dữ liệu hàng loạt ngớ ngẩn**: Khi Server có 1 tin nhắn mới, nó nhả về cho Frontend. Lúc này Frontend có xu hướng "Tự làm mới toàn bộ danh sách" bằng cách gọi lại API Get Data nặng nề, thay vì chỉ Append (nối thêm) cái tin nhắn mới vào danh sách. Việc này tạo ra một cuộc tấn công tự DDoS hệ thống của chính mình.

</details>

1. **The In-Flight Data Loss Window**: Long-Polling suffers from a fundamental architectural blind spot. When the Server completes a request (Timeout or Data delivery), there is a fractional latency window (e.g., 50ms - 100ms) where the Client is transmitting the *next* HTTP request over the network. If a critical Realtime Event fires precisely during this 50ms window, the Server has no active connection to push it to. The data is "dropped".
   - *The Fix (Cursor-Based Pagination)*: The Client must always transmit an offset or timestamp: `GET /poll?last_event_id=99`. If an event (`id=100`) occurs during the blind spot, the Backend persists it to the DB. When the Client reconnects asking for `>99`, the Backend immediately flushes event `100`.
2. **The Auto-DDoS Re-fetch Anti-Pattern**: A junior developer uses Long-Polling purely as a "Ping" mechanism. When the Long-Poll resolves, the Frontend blindly executes a massive `GET /all_data` query to refresh the UI. If an event triggers for 10,000 users simultaneously, the Long-Poll releases 10,000 users at exactly the same millisecond. They instantly fire 10,000 massive `GET` requests, causing an immediate Database Avalanche. **Fix**: The Long-Poll response MUST contain the exact delta payload. The Frontend must surgically inject that payload into the DOM without re-fetching external data.

---

## Related Topics

- For the modern, superior 2-way alternative, see **[WebSocket](./websocket.md)**.
- For the modern, superior 1-way alternative, see **[Server-Sent Events](./sse.md)**.
- For understanding how the backend handles these massive connections, see **[Scalability / Overview](../scalability/overview.md)**.
