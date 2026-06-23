# WebSocket

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: WebSocket là "vị vua" của giao tiếp thời gian thực hiện đại. Nếu HTTP giống như gửi thư qua đường bưu điện (Chậm, gửi xong là đứt liên lạc, muốn gửi tiếp phải dán tem mới), thì WebSocket giống như một cuộc gọi điện thoại (Nhanh, kết nối giữ nguyên, cả 2 bên có thể nói cùng lúc). WebSocket cung cấp kết nối TCP **Hai chiều (Bi-directional)** và **Toàn thời gian (Full Duplex)**, giúp tạo ra các ứng dụng độ trễ cực thấp như Game Online hay App Chat.

</details>

> **Summary**: WebSocket is the undisputed king of modern Realtime architectures. If traditional HTTP is analogous to sending a physical letter via the postal service (high overhead, discrete, disconnected after delivery), WebSocket is a continuous, open phone call. It establishes a persistent, **Bi-directional**, and **Full-Duplex** TCP connection over a single socket. This allows both the Client and the Server to push data frames to each other completely asynchronously, yielding the nanosecond latencies required for Multiplayer Gaming and Instant Messaging.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn gọi điện cho Sếp để hỏi việc.
1. **Dùng HTTP**: Bạn gọi Sếp: "Alo Sếp, em Tùng đây, dự án A xong chưa?". Sếp: "Xong rồi em". Cụp máy! (Tốn 10 giây). 1 phút sau bạn lại gọi: "Alo Sếp, em Tùng đây, dự án B xong chưa?". Sếp: "Chưa em". Cụp máy! Mỗi lần hỏi bạn lại phải chào hỏi lại từ đầu (Tốn thời gian mào đầu).
2. **Dùng WebSocket**: Bạn gọi Sếp: "Alo Sếp, em Tùng đây, cứ giữ máy nhé đừng cúp". Xong 2 anh em để điện thoại trên bàn. Cả ngày hôm đó, Sếp nghĩ ra việc gì là hét lên từ loa điện thoại báo cho bạn ngay lập tức. Bạn cần hỏi gì cũng hét lên ngay lập tức. Không ai phải chào hỏi lại từ đầu, không tốn thời gian kết nối lại.

</details>

Imagine talking to your Boss via Walkie-Talkies vs. an Open Phone Line.
1. **Traditional HTTP (Walkie-Talkie)**: You press the button: "Breaker 1-9, this is John, requesting Project Status. Over." The boss replies: "Status is green. Over and out." The connection closes. 5 minutes later, to ask another question, you must go through the entire rigid introduction handshake again. (High Overhead).
2. **WebSocket (Open Phone Line)**: You call your Boss once at 8:00 AM. You say: "Hey, keep the line open all day." You put the phone on speaker. At 2:15 PM, the Boss suddenly yells through the speaker: "Change of plans, halt production!" At 2:16 PM, you yell back: "Understood, halting!" Zero introductions, zero reconnection time, instant data transfer.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Không phải là HTTP**: Dù nó thường chạy trên cùng port 80/443, WebSocket là một giao thức hoàn toàn riêng biệt (Được định nghĩa là `ws://` hoặc bảo mật `wss://`).
**2. Quá trình Bắt tay (Handshake Upgrade)**: Nó luôn bắt đầu bằng một lệnh HTTP bình thường gửi từ Client với yêu cầu: "Này Server, chúng ta nâng cấp lên WebSocket nhé?". Nếu Server đồng ý, nó trả về mã `101 Switching Protocols`. Từ giây phút đó, HTTP chết, nhường chỗ cho đường ống TCP WebSocket.
**3. Truyền dữ liệu dạng Khung (Framing)**: HTTP truyền đi những cục Text/JSON khổng lồ đính kèm cả tá Header (Cookie, User-Agent...). WebSocket truyền đi những "Khung" (Frame) dữ liệu cực nhỏ gọn. Nó có thể truyền Text bình thường, hoặc truyền hệ Nhị phân (Binary - cực tốt cho Game).

</details>

**1. Protocol Distinct from HTTP**: While it heavily piggybacks on HTTP ports (80/443) to pass easily through corporate firewalls, WebSocket is an entirely separate Layer 7 protocol, designated by the URIs `ws://` (unencrypted) or `wss://` (TLS encrypted).
**2. The Handshake Upgrade**: The lifecycle *must* initiate with a standard HTTP `GET` request. The Client includes a special header: `Connection: Upgrade, Upgrade: websocket`. If the Server supports it, it responds with HTTP Status `101 Switching Protocols`. At this exact millisecond, the HTTP protocol is discarded, and the underlying TCP socket is held permanently open for raw WebSocket framing.
**3. Lightweight Framing**: HTTP encapsulates payloads in massive metadata headers (Cookies, User-Agents, Accept-Types) costing ~800 bytes per request. WebSocket utilizes a minimal **Framing mechanism** (as little as 2 bytes of overhead per message). It natively supports both UTF-8 Text frames and raw Binary frames (ArrayBuffers/Blobs).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Độ trễ thấp nhất có thể (Ultra-Low Latency)**: Trong game bắn súng (Ví dụ: CS:GO hoặc PUBG bản Web). Bạn bấm nút bắn, viên đạn phải nổ ngay lập tức trên máy của 99 người chơi khác. Trễ 100ms là trải nghiệm tồi tệ. HTTP Polling mất thời gian mở kết nối mạng (Bắt tay 3 bước TCP - Three-way Handshake) sẽ tốn mất 50ms-100ms vô ích. WebSocket đã mở kết nối sẵn, tốn 0ms để setup, bấm 1 cái là bay thẳng tới Server.
2. **Tiết kiệm Băng thông (Bandwidth Efficiency)**: Nếu ứng dụng Chat liên tục gửi Header chứa 1KB Cookie cứ mỗi 1 giây. Với 1 triệu User, bạn mất 1 Gigabyte băng thông mỗi giây chỉ để chở rác (Header vô ích). WebSocket đập bỏ Header đi, tiết kiệm 99% băng thông.

</details>

1. **Ultra-Low Latency (Microsecond Delivery)**: In an online Multiplayer Game, when User A clicks the "Fire Weapon" button, the coordinates and action must hit the Server and broadcast to 99 other players instantly. Traditional HTTP enforces a TCP Three-Way Handshake (SYN, SYN-ACK, ACK) and TLS Negotiation for *every single request*. This cryptographic and networking overhead adds 50ms - 200ms of latency before a single byte of data is sent. WebSockets eliminate this completely. The TCP connection is already established and warm. Data is flushed to the network socket instantaneously.
2. **Eradicating Header Bloat (Bandwidth Conservation)**: A typical HTTP request carries massive Cookie headers. In a high-frequency polling app, sending a 2-byte payload ("Ok") requires sending an 800-byte HTTP header. Over 1 million users polling every 1 second, the Server processes 800 Megabytes of pure metadata garbage per second. WebSocket's 2-byte framing overhead obliterates this inefficiency.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh Quá trình Giao tiếp.
</details>

Visualizing the Handshake and Lifecycle.

| Characteristic | Standard HTTP API | WebSocket Connection |
|---|---|---|
| **Initiation** | Client initiates every request. | Client initiates once; either side can send. |
| **Connection State**| Stateless (Closes immediately). | Stateful (Remains persistently open). |
| **Payload Size** | Heavy (Headers + Body). | Extremely Lightweight (Raw Frames). |
| **Latency** | Medium/High (Depends on TCP setup). | Nanoseconds. |
| **Best Used For** | Fetching a User Profile, Form Submit. | Live Chat, Multiplayer Games, Trading. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Game Multiplayer (IO Games)**: Slither.io, Agar.io hoạt động hoàn toàn bằng WebSocket truyền dữ liệu Nhị phân (Binary) tọa độ chuột của hàng ngàn người chơi liên tục.
- **Tính năng Chat Realtime**: Zalo, Messenger Web. Vừa gửi tin nhắn (Upload), vừa nhận tin nhắn của người khác (Download) cùng một lúc (Full Duplex).
- **Ứng dụng Cộng tác (Collaborative)**: Miro, Figma, Google Docs. Hàng chục con trỏ chuột chạy vòng vòng trên màn hình.

</details>

- **Multiplayer Browser Games (.io games)**: Titles like Slither.io or Agar.io stream thousands of raw binary X/Y coordinate vectors per second natively through WebSocket buffers.
- **Enterprise Chat & Support Widgets**: Slack, Discord, or Zendesk Customer Support widgets. They require symmetric communication—the client typing indicators going up, and incoming messages coming down simultaneously.
- **Collaborative Workspaces**: Figma, Google Docs, Notion. Broadcasting cursor positions, text delta changes (CRDTs or Operational Transformation algorithms), and selection highlights to all connected session members instantly.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng thư viện Socket.IO (Thay vì code chay)**: Việc code WebSocket thuần (`new WebSocket(url)`) rất đau khổ vì bạn phải tự xử lý kết nối lại khi rớt mạng, tự chia phòng (Rooms/Namespaces). Các thư viện như **Socket.IO** (NodeJS) hoặc **SignalR** (.NET) sẽ lo hết những việc khó nhất đó cho bạn. Nếu WebSocket bị lỗi Firewall chặn, Socket.IO sẽ tự động "hạ cấp" (Fallback) xuống dùng Long-Polling mà bạn không cần sửa code.
2. **Kiểm tra Xác thực (Authentication)**: Đừng truyền JWT Token vào Header của WebSocket lúc Bắt tay (Vì Javascript Web API cho WebSocket không hỗ trợ sửa Header tùy chỉnh). Có 2 cách:
   - Gắn Token vào URL Query String: `ws://server.com?token=xyz` (Không an toàn lắm vì bị lưu vào Log máy chủ).
   - *Cách tốt nhất*: Kết nối WebSocket rỗng trước. Sau khi kết nối xong, Client bắn tin nhắn WebSocket đầu tiên chứa Token. Server xác thực xong mới cho làm việc tiếp.

</details>

1. **Abstract with High-Level Libraries (Socket.IO / SignalR)**: Authoring raw HTML5 WebSockets (`const ws = new WebSocket()`) is brittle. You must manually engineer Auto-Reconnection logic, Ping/Pong heartbeats, and Pub/Sub Room multiplexing. Libraries like **Socket.IO** (Node.js/React) or **SignalR** (.NET) abstract this complexity. Crucially, they provide **Fallback Mechanisms**. If a strict Corporate Firewall actively blocks the HTTP `Upgrade` request (breaking WebSockets), Socket.IO automatically degrades gracefully to HTTP Long-Polling transparently.
2. **Architecting WebSocket Authentication (The Auth Handshake)**: The standard browser `WebSocket` constructor completely prohibits injecting custom HTTP Headers (like `Authorization: Bearer <JWT>`). Attempting to authenticate via WebSocket is notoriously difficult.
   - *Anti-Pattern*: Injecting the JWT via Query Params (`wss://api.com?token=abc`). The raw URL, including the secret token, is permanently recorded in the Nginx/ALB access logs (Severe Security Vulnerability).
   - *Best Practice (The Ticket Pattern or First-Frame Auth)*: Establish the WebSocket connection unauthenticated. Immediately require the Client to transmit an explicit JSON Auth Frame (`{"type": "authenticate", "token": "xyz"}`). The Server validates the JWT. If invalid, the Server aggressively terminates the socket.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **"Ăn hết" RAM của Server**: Khác với HTTP (Chạy xong giải phóng RAM), WebSocket là kết nối treo vĩnh viễn. Nếu bạn có 1 triệu User đang Online $\rightarrow$ Server của bạn phải duy trì 1 triệu luồng TCP mở liên tục trong RAM (Hiện tượng cạn kiệt Cổng Port - 10K Problem). Bắt buộc phải dùng công cụ Load Balancer chuyên dụng (như HAProxy, Nginx) và tăng giới hạn File Descriptor (`ulimit`) trên Linux.
2. **Ngộ nhận WebSocket có thể thay thế HTTP**: Chẳng ai dùng WebSocket để Load trang danh sách Sản phẩm, hay xử lý thanh toán cả. HTTP có hệ thống Cache, Routing, và Status Code (200, 404, 500) tuyệt vời. WebSocket chỉ là đường truyền dữ liệu thô (Raw Data), bạn phải tự code lại toàn bộ hệ thống Routing và Báo lỗi bằng tay (Rất mệt mỏi). Chỉ dùng WebSocket cho đúng chức năng Realtime của nó.

</details>

1. **The C10K / Port Exhaustion Crisis**: Unlike HTTP, which cleans up after a request, a WebSocket consumes a persistent TCP socket and holds an active File Descriptor (FD) on the Linux kernel. A single monolithic Node.js server attempting to hold 100,000 idle WebSockets will aggressively exhaust its RAM and hit the kernel's OS-level File Descriptor limits (`ulimit -n`), causing catastrophic crashing. **Fix**: You must horizontally scale WebSocket servers, tune Linux kernel parameters (`sysctl`), and utilize dedicated WebSocket-aware Load Balancers (AWS ALB or Nginx).
2. **WebSocket Over-Engineering (The Anti-Pattern)**: Believing "WebSockets are faster than HTTP, therefore I should build my entire REST API over WebSockets." This is a monumental mistake. Standard HTTP natively provides caching mechanisms, standardized Status Codes (`404`, `500`), idempotent `PUT/DELETE` semantics, and seamless integration with CDNs (Cloudflare). WebSockets provide none of this; it is just a dumb pipe. You will spend months re-inventing HTTP routing logic from scratch inside a giant JSON switch-statement. **Rule**: Use standard HTTP REST for CRUD operations. Use WebSockets strictly for highly volatile realtime streams.

---

## Related Topics

- For alternative Realtime solutions, see **[Server-Sent Events](./sse.md)**.
- For how to scale WebSockets across multiple servers, see **[Caching / Distributed](../caching/distributed.md)** (Redis is used to sync WebSockets).
