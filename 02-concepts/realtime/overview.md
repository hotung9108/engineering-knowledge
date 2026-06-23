# Realtime Communication Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Web truyền thống hoạt động theo nguyên tắc: "Hỏi mới Trả lời" (Client gọi Request $\rightarrow$ Server trả Response). Nếu Client không hỏi, Server không có cách nào chủ động đưa thông tin cho Client. **Realtime Communication (Giao tiếp thời gian thực)** phá vỡ nguyên tắc đó. Nó cung cấp các công nghệ giúp Server có thể CHỦ ĐỘNG đẩy (Push) dữ liệu trực tiếp về màn hình của người dùng ngay lập tức. Đây là trái tim của các ứng dụng Chat, Live Stream, Giá chứng khoán hay Game Online.

</details>

> **Summary**: Traditional HTTP architecture operates strictly on a Request-Response paradigm (Client initiates, Server responds). The Server is inherently passive; it possesses no architectural mechanism to actively push state changes to a connected Client. **Realtime Communication** encompasses the networking protocols and design patterns engineered to break this limitation, enabling bi-directional, persistent, or Server-Push data flows. It is the foundational infrastructure powering instant messaging, live financial dashboards, multiplayer gaming, and collaborative editing.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang đợi thư trúng tuyển Đại học.
1. **Kiểu truyền thống (HTTP Polling)**: Cứ 5 phút bạn lại chạy ra hòm thư mở nắp xem có thư chưa. Bạn phải tự chạy ra 100 lần trong ngày, rất mệt mỏi, và 99 lần là hòm thư trống rỗng.
2. **Kiểu thời gian thực (Realtime)**: Bạn nối một sợi dây thừng từ Bưu điện về thẳng phòng ngủ của bạn. Khi nào có thư, bưu tá chỉ cần giật sợi dây, chuông trong phòng bạn reo lên và bức thư trượt dọc theo sợi dây rơi ngay vào tay bạn. Bạn không cần làm gì cả, chỉ việc ngồi đợi.

</details>

Imagine you are waiting for an urgent package delivery.
1. **Traditional HTTP (Polling)**: You walk out to your mailbox every 5 minutes, open it, check for a package, and walk back inside. You do this 200 times a day. 199 times, the mailbox is completely empty. You waste enormous amounts of energy (CPU/Network).
2. **Realtime Communication**: You install a dedicated pneumatic tube directly connecting the Post Office to your living room. You sit on your couch and do absolutely nothing. The exact millisecond the package arrives at the Post Office, they drop it into the tube, and it instantly lands in your lap.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 3 công nghệ Realtime phổ biến nhất, từ thô sơ đến hiện đại:
1. **Long-Polling (Giữ máy chờ)**: Client hỏi Server. Nếu Server chưa có tin, Server KHÔNG dập máy mà giữ liên lạc (treo kết nối). Khi nào có tin, Server trả lời rồi mới cúp máy. Xong Client lại gọi lại ngay lập tức.
2. **SSE - Server-Sent Events (Đường một chiều)**: Client gọi Server 1 lần duy nhất. Cúp máy. Nhưng để lại một cái "Ống nước" một chiều. Server cứ thế bơm dữ liệu từ từ qua ống nước đó về Client mãi mãi. (Rất hợp cho Thông báo/Giá chứng khoán).
3. **WebSocket (Đường hai chiều cao tốc)**: Client gọi Server. Hai bên đập bỏ giao thức HTTP cũ kỹ, nâng cấp lên giao thức mới (WS). Tạo ra một đường hầm siêu tốc 2 chiều. Cả Client và Server đều có thể bắn dữ liệu vào mặt nhau bất cứ lúc nào. (Bắt buộc dùng cho Game Online, App Chat).

</details>

Realtime architecture evolved through three primary iterations:
1. **Long-Polling (The Hack)**: A clever manipulation of standard HTTP. The Client makes a standard request. If the Server has no data, it intentionally *hangs* the connection open (does not return a response). The moment data appears, the Server completes the response. The Client instantly opens a new hanging connection.
2. **Server-Sent Events / SSE (Uni-directional)**: A standardized HTML5 API over HTTP. The Client opens a persistent connection. The Server utilizes chunked transfer encoding to continuously stream Text/Event data down to the Client over time. The Client cannot send data back through this specific pipe.
3. **WebSocket (Bi-directional Full Duplex)**: A completely distinct Layer 7 TCP protocol (not HTTP). It begins with an HTTP handshake, then "Upgrades" the connection into a persistent, full-duplex tunnel. Both the Client and the Server can push raw binary or text frames to each other completely asynchronously and independently.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong ứng dụng Chat (Ví dụ: Messenger). A nhắn tin cho B.
A gửi tin lên Server (Bằng HTTP bình thường). Server nhận được tin, ghi vào Database. 
Nhưng B đang cầm điện thoại không làm gì cả. Màn hình của B làm sao biết có tin mới để hiện lên?
Nếu bắt điện thoại của B cứ 1 giây lại F5 hỏi Server "Có tin nhắn không?" (Polling) $\rightarrow$ Pin điện thoại của B sẽ cạn sạch trong 2 tiếng, và Server cũng sẽ nổ tung vì nhận hàng tỷ request rác mỗi giây.
Realtime tồn tại để Server có năng lực "Ra lệnh cho Frontend tự cập nhật màn hình" mà không gây tốn tài nguyên vô ích.

</details>

Consider the architectural constraint of a Chat Application. User A sends a message to User B.
User A executes an HTTP `POST /messages`. The Server persists the message to the Database.
User B's phone is currently sitting idle. How does User B's screen know to update?
If the architecture relies on Short Polling (User B's phone executes `GET /messages` every 1 second), the phone's battery will drain rapidly due to constant radio transmission, and the Server will be DDoS'd by millions of empty `GET` requests (yielding `200 OK, No new messages`).
Realtime protocols exist to establish **Persistent State**. They invert the control flow, granting the Server the explicit capability to push state mutations directly to the Client's DOM with near-zero latency and minimal resource overhead.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh gánh nặng Mạng (Network Overhead) giữa Polling cũ và WebSocket mới.
</details>

Visualizing the HTTP Header bloat vs. TCP Framing overhead.

| Metric | Short Polling (Traditional HTTP) | WebSocket (Realtime) |
|---|---|---|
| **Connection Setup** | Client opens & closes TCP connection every 1s. | Client opens TCP connection **ONCE**. |
| **Header Overhead**| ~800 bytes of HTTP Headers per request. | ~2 to 10 bytes of Framing Data per message. |
| **Latency** | Extremely High (Wait 1s for next poll). | Nanoseconds (Instant wire transit). |
| **Directionality** | Client $\rightarrow$ Server exclusively. | Bi-directional (Full Duplex). |
| **Server Load** | **Catastrophic** (Wasting CPU on empty responses).| **Extremely Lightweight** (Idle connections cost almost nothing). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Ứng dụng Chat (Messenger, Slack, Discord)**: Rõ ràng phải dùng WebSocket. Bạn vừa phải gửi tin đi (Upload), vừa phải nhận tin về (Download) liên tục.
- **Bảng giá Chứng khoán / Tiền ảo (Binance)**: Dùng SSE (Server-Sent Events) là chuẩn nhất. Vì bạn chỉ "nhìn" giá thay đổi liên tục, chứ bạn không có nhu cầu gửi dữ liệu chứng khoán ngược lại cho sàn.
- **Google Docs (Chỉnh sửa trực tuyến)**: WebSocket (Hoặc WebRTC). Khi bạn gõ 1 chữ 'A', chữ 'A' đó ngay lập tức hiện lên màn hình của 5 người khác đang cùng xem file.
- **Chờ thanh toán Momo/ZaloPay**: Khi quét mã QR, màn hình web đứng im chờ điện thoại thanh toán xong để chuyển trang. Đây là bài toán hoàn hảo cho Long-Polling. Bạn gọi API 1 lần, chờ tối đa 60 giây. Trả tiền xong web tự nhảy. Chẳng cần kết nối WebSocket phức tạp làm gì.

</details>

- **Instant Messaging (Discord/Slack)**: Absolutely requires **WebSockets**. The architecture demands high-frequency, bi-directional text and binary frame exchange with absolute minimal latency.
- **Financial Dashboards (Crypto Trading/Stocks)**: Perfectly suited for **SSE (Server-Sent Events)**. The flow of data is almost entirely Uni-directional (Server continuously streaming price ticks down to the Client's browser). The Client rarely sends data back on that same channel.
- **Collaborative Editing (Figma/Google Docs)**: Requires **WebSockets** (or WebRTC for P2P). Capturing and broadcasting exact mouse coordinates and keystrokes to 10 other concurrent viewers requires persistent, full-duplex TCP tunnels.
- **Payment Gateway Status (QR Code scanning)**: The perfect domain for **Long-Polling**. The web browser displays a QR code and opens a Long-Poll request. It waits up to 60 seconds. The user scans the QR with their phone and pays. The Server completes the hanging Long-Poll request with `Status: PAID`, and the browser redirects. It requires zero complex WebSocket infrastructure for a one-time event.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Ping/Pong (Heartbeat)**: Các thiết bị mạng như Router hoặc Firewall của nhà mạng có một thói quen rất xấu: Hễ thấy cái kết nối mạng nào "im im" không gửi gì trong 60 giây, nó sẽ tự động dùng kéo "Cắt đứt" kết nối đó để tiết kiệm tài nguyên. Vì vậy, trong Realtime, Cứ 30 giây bạn phải viết code cho Client bắn một cái tin nhắn rỗng `Ping` lên Server, Server đáp lại `Pong`. Chỉ để cho Router thấy "À bọn này vẫn đang nói chuyện, đừng có cắt".
2. **Không dùng Realtime để tải file nặng**: WebSocket sinh ra để truyền các gói tin JSON nhỏ xíu (vài chục bytes) với tốc độ ánh sáng. Nếu bạn cố tình nhét một tấm ảnh 5MB vào WebSocket, nó sẽ nghẽn toàn bộ đường ống, các tin nhắn chat phía sau sẽ bị kẹt lại không qua được (Head-of-line blocking). Hãy upload ảnh bằng HTTP bình thường, lấy cái URL, rồi gửi cái URL đó qua WebSocket.

</details>

1. **Mandatory Heartbeats (Ping/Pong Frames)**: Intermediate network infrastructure (NAT routers, Corporate Firewalls, Load Balancers like AWS ALB) silently aggressively terminate idle TCP connections to conserve port exhaustion (often after 60 seconds of inactivity). If a user is staring at a Chat app but not typing, the WebSocket will be secretly severed. **Fix**: Implement a Heartbeat mechanism. The Client must transmit a lightweight `Ping` frame every ~30 seconds, and the Server replies with `Pong`. This artificial traffic mathematically guarantees the connection remains alive through hostile networks.
2. **Keep the Pipe Clean (No Heavy Payloads)**: WebSockets are engineered for high-frequency, ultra-low-latency micro-messages (JSON text or small binary coordinates). If a developer attempts to stream a 50MB 4K Video file directly through the WebSocket tunnel, it causes catastrophic **Head-Of-Line Blocking**. The massive binary blob clogs the TCP buffers. All subsequent, urgent text messages are trapped behind it. **Rule**: Use standard HTTP `POST` for heavy media uploads. Once uploaded, transmit the resulting image URL `string` through the WebSocket.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Vấn đề Scale (Cân bằng tải ngớ ngẩn)**: Web bình thường xài Load Balancer rất dễ, thằng nào rảnh thì vứt request cho thằng đó (Round Robin). Nhưng Realtime là "Kết nối cố định". User A cắm dây thẳng vào Server 1. User B cắm dây thẳng vào Server 2. Nếu A gửi tin nhắn cho B, Server 1 không biết B nằm ở đâu để đẩy tin xuống. 
   - *Cách giải quyết*: Phải dùng một hệ thống Pub/Sub trung gian (Thường là Redis Pub/Sub). Server 1 nhận tin của A $\rightarrow$ Bắn vào Redis $\rightarrow$ Redis ném cho Server 2 $\rightarrow$ Server 2 đẩy xuống mặt B. Đây là trái tim của kiến trúc Realtime ở quy mô lớn.
2. **Quên xử lý Đứt mạng (Reconnection Logic)**: Người dùng cầm điện thoại đi vào Thang máy $\rightarrow$ Mất mạng (Đứt WebSocket). Đi ra khỏi thang máy $\rightarrow$ Có mạng lại. Lập trình viên Front-end gà mờ thường không viết code tự động kết nối lại (Auto-Reconnect). Khiến User tưởng App bị đơ, chửi và xóa App.

</details>

1. **The Scaling Nightmare (Sticky Sessions vs. Pub/Sub)**: Traditional HTTP easily scales behind a Load Balancer using stateless Round Robin. Realtime protocols are heavily Stateful (Persistent TCP sockets). User A connects to `Node 1`. User B connects to `Node 50`. When A messages B, `Node 1` holds the message, but it has no physical connection to User B. The message dies.
   - *The Enterprise Fix*: The cluster MUST be backed by a Distributed Pub/Sub backplane (e.g., Redis Pub/Sub). `Node 1` receives the message and publishes it to Redis. Redis broadcasts it to all 50 Nodes. `Node 50` sees the message is for User B, identifies User B's active socket in its local RAM, and pushes it down.
2. **Naive Client Disconnection Handling**: Mobile users experience massive network volatility (walking into elevators, switching from WiFi to 4G). The OS will abruptly sever the WebSocket. Inexperienced frontend developers rely on the initial Page Load to establish the socket and forget to handle the `onclose` event. **Fix**: The Frontend architecture must include an aggressive, Exponential Backoff Auto-Reconnect loop. Furthermore, upon successful reconnection, it must explicitly fetch any messages missed during the offline window to prevent data holes.

---

## Related Topics

- For the specific implementations, see **[WebSocket](./websocket.md)**, **[Server-Sent Events](./sse.md)**, and **[Long-Polling](./long-polling.md)**.
- To understand the backend Pub/Sub architecture required to scale Realtime apps, see **[Messaging Patterns](../messaging/patterns.md)**.
- To handle the distributed architecture aspect, read **[Distributed Systems / Overview](../distributed-system/overview.md)**.
