# WebSocket: Real-Time Two-Way Communication

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Giao thức HTTP truyền thống chạy theo mô hình "Hỏi - Đáp": Trình duyệt hỏi (Request), Máy chủ đáp (Response), xong rồi cắt đứt liên lạc. Nếu máy chủ có dữ liệu mới (ví dụ: Tin nhắn chat tới), máy chủ KHÔNG THỂ chủ động gửi cho Trình duyệt được. **WebSocket** ra đời để phá bỏ giới hạn này. Nó tạo ra một "đường ống nước" mở 24/7 giữa Trình duyệt và Máy chủ, cho phép cả hai bên tự do ném dữ liệu vào mặt nhau bất cứ lúc nào với tốc độ ánh sáng (Độ trễ mili-giây).

</details>

> **Summary**: The traditional HTTP protocol strictly enforces a Request-Response paradigm: The Client initiates communication, the Server replies, and the connection is immediately terminated. If the Server receives new data (e.g., a live chat message), it is physically impossible for the Server to proactively push it to the Client. **WebSocket** shatters this limitation. It upgrades an HTTP connection into a persistent, Full-Duplex TCP socket, establishing a 24/7 open pipeline. Both Client and Server can blast data payloads at each other simultaneously with absolute zero handshake latency.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang chờ bưu tá giao thư báo điểm thi đại học.
- **HTTP (Kiểu truyền thống - Polling)**: Cứ 5 phút bạn lại chạy ra mở cửa hòm thư xem có thư không. Mở ra không thấy, lại đi vào. 5 phút sau lại chạy ra. Bạn chạy ra chạy vào 100 lần, cực kỳ mệt mỏi và tốn sức (Hại Server).
- **WebSocket (Có điện thoại kết nối sẵn)**: Bưu tá gọi điện thẳng cho bạn và giữ máy không cúp. Bưu tá bảo: "Cứ để loa ngoài đấy, tao đang trên đường đi lấy điểm, lúc nào có điểm tao hét lên cho mày nghe". Ngay giây phút có điểm, bưu tá hét lên, bạn nghe được luôn. Nhanh gọn, không tốn sức chạy ra mở cửa.

</details>

Imagine you are frantically waiting for a highly anticipated letter (exam results) to arrive in your mailbox.
- **HTTP Polling (The Traditional Way)**: You walk out to your mailbox every 5 minutes to check for the letter. It's empty. You walk back inside. You repeat this exhausting physical cycle 100 times throughout the day, burning massive amounts of energy (Server CPU/Bandwidth overhead).
- **WebSocket (The Persistent Phone Call)**: The postman calls you on the phone and neither of you hangs up. The postman says, "Just leave the phone on speaker. I'm waiting for the results. The exact millisecond the results are printed, I will shout them into the phone." You instantly receive the results with zero delay, and you didn't waste any energy walking to the mailbox.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Bản chất**: WebSocket không bắt đầu bằng cổng riêng. Nó bắt đầu y hệt một request HTTP bình thường (cổng 80/443).
**2. Quá trình Upgrade (Nâng cấp ống nước)**: Trình duyệt gửi request HTTP kèm dòng chữ: "Ê Server, đổi giao thức sang WebSocket nhé". Server đồng ý trả về `101 Switching Protocols`. BÙM! Lập tức đường truyền HTTP biến thành một đường truyền TCP hai chiều mở toang hoác.
**3. Full-Duplex (Hai chiều đồng thời)**: Giống như con đường hai làn xe. Trình duyệt vừa gửi dữ liệu lên, Server cũng vừa xả dữ liệu xuống cùng một tíc tắc.

</details>

**1. The Mechanics**: WebSocket does not require a custom network port. It deliberately initiates over standard HTTP (Port 80/443) to effortlessly bypass corporate Firewalls.
**2. The HTTP Upgrade Handshake**: The Client sends a standard HTTP `GET` request containing a specific header: `Upgrade: websocket`. If the Server supports it, it replies with an `HTTP 101 Switching Protocols` status code. The HTTP protocol is instantly jettisoned, and the underlying TCP socket is held permanently open.
**3. Full-Duplex Communication**: It operates like a two-lane highway. The Client can stream data *Up* while the Server simultaneously streams data *Down* at the exact same millisecond, with zero HTTP header bloat attached to the payloads.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Để làm ứng dụng Nhắn tin (Chat), ngày xưa lập trình viên phải xài thủ thuật **Long-Polling**: Bắt Trình duyệt dùng Javascript gửi request HTTP lên Server liên tục mỗi 1 giây (để hỏi xem có ai chat với mình không).
Việc này sinh ra 2 thảm họa:
1. **DDoS tự sát**: Nếu có 1 triệu User đang online, mỗi giây Server nhận 1 triệu request HTTP chỉ để trả lời "Không có tin nhắn nào mới đâu". Server sập ngay lập tức vì quá tải TCP Handshake.
2. **Độ trễ cao (Latency)**: Tin nhắn mới có thể mất tới 1 giây mới hiện lên, không đủ nhanh cho các Game bắn súng hay Giao dịch chứng khoán.
WebSocket ra đời để dập tắt kiểu truy vấn mù quáng này.

</details>

Historically, engineering Real-Time applications (Chat rooms, Stock tickers) over HTTP required a horrific anti-pattern known as **Long-Polling**. The JavaScript client executed an infinite loop, firing a new AJAX HTTP request every 1 second asking, "Are there any new messages?"
This triggered two catastrophic architectural failures:
1. **Self-Inflicted DDoS**: If 1 million users are online, the Server is pulverized by 1,000,000 HTTP requests per second, where 99% of the responses are an empty array `[]`. The overhead of establishing and tearing down TCP HTTP connections annihilates the CPU.
2. **Unacceptable Latency**: Polling intervals inherently introduce artificial latency. You cannot build a multiplayer First-Person Shooter or a High-Frequency Trading terminal on 1-second interval loops.
WebSocket was engineered to completely eradicate polling, providing true, unbuffered, sub-millisecond data pushing.

---

## Layer 3: Without vs. With Comparison (Compare)

### Overhead Comparison (HTTP Polling vs WebSocket)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh gánh nặng mạng giữa việc Polling (Hỏi liên tục bằng HTTP) và WebSocket.
</details>

Analyzing the brutal network overhead of HTTP compared to the efficiency of WebSocket for transmitting a tiny 10-byte message.

| Action | HTTP Short Polling (Every 1 second) | WebSocket |
|---|---|---|
| **Connection Setup** | 3-Way TCP Handshake EVERY SECOND. | 1 TCP Handshake at the very beginning. |
| **Header Overhead** | ~800 Bytes of HTTP Headers (Cookies, User-Agent) sent EVERY SECOND. | ~2 Bytes of framing data per message. |
| **Data Transmitted** | 10 Bytes payload + 800 Bytes junk. | 10 Bytes payload. |
| **Server Action** | Server burns CPU repeatedly opening/closing sockets. | Server easily pushes 10 Bytes down the open pipe. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Bắt buộc dùng WebSocket**: Ứng dụng Chat (Messenger, Zalo), Game Online nhiều người chơi (Multiplayer), Bảng điện Chứng khoán / Tiền ảo (Nhảy giá từng mili-giây), App theo dõi vị trí tài xế Grab/Uber trên bản đồ.
- **Không nên dùng WebSocket**: Trang web đọc tin tức, Blog, Cửa hàng bán quần áo. Việc giữ một kết nối 24/7 trên Server tốn rất nhiều RAM. Nếu App của bạn thỉnh thoảng mới tải dữ liệu, hãy cứ dùng HTTP REST API bình thường!

</details>

- **Mandatory WebSocket Domains**: Massive Multiplayer Online Games (MMOs), Real-time Chat Applications (Discord, Slack, Messenger), High-Frequency Financial Trading Dashboards (Crypto/Stock tickers rendering sub-millisecond price fluctuations), and Live GPS Tracking (Watching the Uber driver approach on a map).
- **The Anti-Pattern (When to AVOID WebSocket)**: Standard E-Commerce catalogs, Blogs, and News websites. Holding a TCP socket open permanently consumes Server RAM (specifically, File Descriptors). If 5 million users are reading a static news article, keeping 5 million WebSockets open will crash your server with `Too many open files` errors. For static or infrequently updated data, standard REST HTTP is vastly superior and highly cacheable via CDNs.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Xử lý Đứt Kết Nối (Reconnection Strategy)**: Mạng điện thoại (3G/4G) chập chờn liên tục. Khi user đi vào thang máy, WebSocket sẽ bị đứt. Khi ra khỏi thang máy, Client (Javascript) phải TỰ ĐỘNG nhận biết để gọi lệnh `new WebSocket()` nối lại đường ống ngay lập tức. (Thư viện như `Socket.io` tự làm việc này cho bạn).
2. **Ping/Pong (Bắt Mạch)**: Làm sao Server biết thằng User đã tắt Wifi đi ngủ để mà ngắt kết nối (giải phóng RAM)? Cứ mỗi 30 giây, Server ném một cục đá nhỏ `PING` xuống Client. Nếu Client chọi lại cục đá `PONG`, nghĩa là nó còn sống. Nếu chọi 3 lần không thấy `PONG`, Server tự động vứt ống nước đó đi.

</details>

1. **Implement Aggressive Reconnection Logic**: Mobile network connections (4G/5G) are highly volatile. When a user drives through a tunnel, the TCP socket violently severs. The Native WebSocket API in the browser does *not* auto-reconnect. You must engineer robust Javascript logic (Exponential Backoff) to detect the `onclose` event and continuously attempt to re-establish the connection. (Note: Abstraction libraries like `Socket.io` or `SignalR` handle this automatically).
2. **Heartbeats (Ping/Pong Frames)**: How does a Server know if a User's iPhone battery died, or if they just haven't typed a message in 10 minutes? Unused TCP sockets quietly consume Server RAM. You must implement a Heartbeat protocol. The Server emits a `PING` frame every 30 seconds. The Client must immediately return a `PONG`. If the Server misses 3 consecutive `PONGs`, it aggressively tears down the socket to prevent Memory Leaks (Zombie Connections).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Vấn đề Scale (Cân bằng tải ngớ ngẩn)**: Bạn có 2 Server Chat. User A kết nối vào Server 1. User B kết nối vào Server 2. User A chat với User B. Server 1 nhận tin nhắn, nhưng nhìn quanh không thấy User B đâu (vì B ở bên Server 2). Tin nhắn bị mất hút! Giải pháp: Các Server WebSocket BẮT BUỘC phải cắm chung vào một hệ thống "Loa phát thanh trung tâm" (Pub/Sub như Redis) để gào tên nhau lên.
2. **Bỏ quên Bảo mật (Authentication)**: Khác với HTTP có Header Authentication, đường ống WebSocket sau khi mở ra là "lõa thể". Nếu hacker đoán được địa chỉ IP WebSocket của bạn, nó cắm thẳng ống vào và gửi/nhận dữ liệu. Bắt buộc phải nhét thẻ Ticket/Token vào ngay gói tin đầu tiên khi mở kết nối để xác thực.

</details>

1. **The Sticky Session / Horizontal Scaling Crisis**: Horizontal scaling breaks WebSockets by default. User A's WebSocket is connected to Server Node 1. User B's WebSocket is connected to Server Node 2. If User A messages User B, Node 1 searches its local RAM for User B's socket and fails to find it. The message drops. **Solution**: Stateless WebSockets require a highly performant **Pub/Sub Backplane** (like Redis Pub/Sub or Kafka). Node 1 publishes the message to Redis. Redis broadcasts it to all Nodes. Node 2 hears it, finds User B's socket in its RAM, and pushes the message down.
2. **Authentication Negligence**: Establishing a WebSocket connection bypasses standard HTTP REST middlewares. Developers often forget to secure the `ws://` endpoint. Malicious actors can open raw sockets and flood the server with spam. You must intercept the initial HTTP Upgrade Handshake, extract the JWT token (either from a query parameter or a secure Cookie), and aggressively terminate the handshake (`HTTP 401`) if the token is invalid.

---

## Related Topics

- For establishing standard Request/Response architecture, review **[REST API](./rest-api.md)**.
- See how WebSockets relate to the transport layer in **[TCP/IP Model](./tcp-ip.md)**.
- Understand the security headers necessary to initiate connections safely via **[HTTP & HTTPS](./http-https.md)**.
