# Server-Sent Events (SSE)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu WebSocket là đường cao tốc 2 chiều đắt đỏ, thì **SSE (Server-Sent Events)** là đài phát thanh 1 chiều. Rất nhiều ứng dụng (Ví dụ: Bảng giá chứng khoán, Luồng tin tức (News Feed), Thông báo Facebook) chỉ có nhu cầu "Nhận dữ liệu từ Server", chứ Frontend ít khi cần bắn dữ liệu gì phức tạp lên. SSE cho phép Server mở một "Đường ống nước" bằng HTTP bình thường, và liên tục bơm dữ liệu trả về cho Frontend theo thời gian thực. Cực kỳ nhẹ, cực kỳ dễ dùng, và tận dụng được mọi ưu điểm của chuẩn HTTP cũ.

</details>

> **Summary**: While WebSockets provide bi-directional framing, many Realtime applications possess a strictly Uni-directional data flow (e.g., Live Sports Scores, Cryptocurrency Tickers, Social Media Notifications). The Client only needs to *listen* to the Server, not speak back to it. **Server-Sent Events (SSE)** is an elegant HTML5 API built entirely on top of traditional HTTP. It allows the Client to open a persistent HTTP connection, while the Server utilizes Chunked Transfer Encoding to continuously stream discrete event messages down the pipe over an extended period. It is remarkably lightweight and leverages existing HTTP infrastructure seamlessly.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang xem một trận Bóng đá qua Radio.
1. **WebSocket (Điện thoại)**: Bạn cầm điện thoại gọi cho Bình luận viên. Bình luận viên báo: "Ronaldo có bóng". Rồi bạn lại nói vào điện thoại: "Hay quá anh ơi". Cả 2 cùng nói chuyện. (Tốn kém cước điện thoại, rườm rà).
2. **SSE (Đài Radio)**: Bạn bật đài Radio lên. Bạn CHỈ CÓ THỂ NGHE bình luận viên nói: "Phút 12, Messi ghi bàn... Phút 15, thẻ vàng...". Bạn không thể chửi đổng vào cái đài Radio mong ông bình luận viên nghe thấy được. Nó là **Đường một chiều (Uni-directional)**. Nhưng bù lại, nó siêu rẻ, 1 bình luận viên có thể phát sóng cho 1 triệu cái Radio cùng lúc rất dễ dàng.

</details>

Imagine receiving live updates for a Football match.
1. **WebSocket (The Telephone Call)**: You call the Announcer. The Announcer says "Goal!". You reply, "Wow, great!". Both of you can speak at any time. (Expensive setup, unnecessary complexity if you just want to listen).
2. **SSE (The Radio Broadcast)**: You tune your radio to the station. You can ONLY listen. The Announcer continuously streams updates: "Minute 12, Penalty... Minute 15, Red Card...". You cannot yell back into your radio to talk to the Announcer. It is strictly **Uni-directional**. However, it is incredibly efficient, and the Announcer can easily broadcast to 1 million radios simultaneously without heavy TCP multiplexing overhead.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Vẫn là HTTP Thuần (Pure HTTP)**: Không giống WebSocket phải đổi giao thức (`ws://`), SSE dùng luôn đường link HTTP bình thường (`http://`). 
**2. Bí mật của SSE (Header đặc biệt)**: Khi Server nhận request, thay vì gom toàn bộ dữ liệu rồi trả về cùng lúc kèm mã `Content-Length`, Server sẽ trả về cái Header: `Content-Type: text/event-stream`. Header này báo cho Trình duyệt biết: "Này, tôi sẽ gửi dữ liệu từ từ thành nhiều đợt nhé, đừng có tự động ngắt kết nối".
**3. Dữ liệu dạng Văn bản (Text-Only)**: SSE chỉ truyền được chữ (Text/JSON), KHÔNG truyền được hệ Nhị phân (Binary) như ảnh, video gốc (Phải Base64). Dữ liệu gửi xuống có định dạng rất đơn giản, bắt đầu bằng chữ `data:` và kết thúc bằng `\n\n` (Hai lần xuống dòng).

</details>

**1. Pure HTTP Architecture**: Unlike WebSockets which hijack the TCP socket to create a custom protocol, SSE remains strictly within the bounds of HTTP/1.1 or HTTP/2. It operates over standard `http://` or `https://` URLs, traversing enterprise firewalls effortlessly.
**2. The Mechanism (Event-Stream)**: The magic lies in the HTTP Response Headers. The Server responds with `Content-Type: text/event-stream` and `Transfer-Encoding: chunked`. This explicitly instructs the Browser's HTTP client: "Do not close this connection. I will stream discrete chunks of text data over an indefinite period of time."
**3. Plaintext Protocol**: SSE strictly streams UTF-8 encoded text. It does not support native Binary frames (ArrayBuffers) like WebSockets do. A standard SSE message over the wire looks like plain text separated by double newlines: 
`data: {"price": 5000}`
`\n\n`

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao phải đẻ ra SSE khi đã có WebSocket?**
Bởi vì WebSocket quá "to" và "khó nuôi". 
Khi dùng WebSocket, bạn mất đi toàn bộ sức mạnh của hệ thống HTTP (như Nginx Caching, Load Balancing tự động, HTTP/2 Multiplexing). Code để vận hành WebSocket trên Server vô cùng phức tạp.
Trong khi đó, với SSE, Lập trình viên Backend chỉ cần viết ĐÚNG 5 DÒNG CODE là tạo ra được một luồng Realtime đẩy dữ liệu xuống. Frontend cũng dùng cái API `EventSource` có sẵn trong trình duyệt cực kỳ nhàn hạ. SSE sinh ra để giải quyết triệt để 90% các bài toán "Thông báo" mà không cần vác dao mổ trâu (WebSocket) ra giết gà.

</details>

**Why engineer SSE when WebSocket exists?**
Because WebSockets are architecturally heavy, stateful, and entirely opaque to standard HTTP infrastructure. 
When you upgrade to WebSockets, you instantly lose the native benefits of the HTTP ecosystem: You cannot use HTTP caching, AWS CloudFront Edge caching struggles, Corporate Firewalls often arbitrarily drop raw TCP framing, and standard Load Balancing algorithms fail.
**SSE resolves this**. Because SSE is just a long-lived HTTP request, it plays perfectly nicely with Nginx, HAProxy, and Firewalls. Furthermore, modern HTTP/2 inherently supports connection multiplexing. SSE over HTTP/2 allows the browser to stream data alongside other standard API requests over a single TCP connection, making it vastly more network-efficient than dedicating a separate TCP socket purely for WebSockets.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh độ phức tạp khi xây dựng hệ thống "Thông báo có Email mới".
</details>

Visualizing the implementation complexity for a "New Notification" feature.

| Feature | WebSocket | Server-Sent Events (SSE) |
|---|---|---|
| **Protocol** | Custom TCP (`ws://`) | Standard HTTP (`http://`) |
| **Direction** | Bi-directional | Uni-directional (Server $\rightarrow$ Client) |
| **Auto-Reconnect**| No (Must be coded manually). | **Yes** (Browser automatically reconnects). |
| **Firewall Issues**| High (Often blocked by strict proxies). | Low (Appears as standard HTTP traffic). |
| **Backend Code** | Complex (Requires specific WS Libraries). | Trivial (Just emit text strings via standard HTTP Controller). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Ứng dụng AI Chat (ChatGPT, Claude)**: Khi bạn hỏi ChatGPT một câu, nó không trả lời nguyên 1 đoạn văn cùng lúc. Nó "nhả" ra từng chữ một trên màn hình (Streaming). OpenAI dùng 100% kiến trúc SSE để thực hiện việc này vì nó là Đường một chiều tuyệt vời nhất.
2. **Cập nhật Tiến trình (Progress Bar)**: Bạn Upload 1 file CSV chứa 10.000 dòng lên Server để xử lý. Bạn muốn Frontend hiện thanh phần trăm (10%... 50%... 100%). Dùng SSE là chuẩn mực nhất.
3. **Mạng xã hội (Feed & Notification)**: Twitter (X) đẩy luồng Tweet mới, hay Facebook đẩy cái chấm đỏ "Có thông báo" xuống thiết bị của bạn. Chỉ cần Server chủ động nói cho Client là đủ.

</details>

1. **AI / LLM Token Streaming (ChatGPT/Claude)**: The absolute definitive use-case in the modern era. When you prompt a Large Language Model, it does not generate the entire 500-word essay instantly. It infers token by token. OpenAI utilizes standard HTTP SSE. The Server streams `data: "The "`, then `data: "quick "`, then `data: "brown "` down the connection, allowing the Frontend UI to render the typing effect in realtime.
2. **Background Task Progress Indicators**: A user uploads a massive dataset for processing. The Frontend needs a progress bar (1%... 50%... 100%). Opening a WebSocket is architectural overkill. Standard HTTP Polling is inefficient. The Frontend simply establishes an SSE `EventSource` connection. The background worker emits percentage updates via SSE until 100% is reached, and the connection gracefully closes.
3. **Live Tickers & Feeds**: Continuously updating Cryptocurrency spot prices on Binance, Live Sports Scoreboards, or realtime Social Media Activity Feeds. The data is entirely read-only from the Client's perspective.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Tận dụng HTTP/2**: Ngày xưa, trình duyệt giới hạn chỉ cho phép mở tối đa 6 kết nối HTTP cùng lúc tới 1 tên miền. Nếu bạn mở 6 tab trang web dùng SSE (HTTP/1.1), kết nối thứ 7 sẽ bị đứng vĩnh viễn không chạy được. Bắt buộc phải cấu hình Server chạy **HTTP/2**. HTTP/2 gộp chung tất cả các luồng vào 1 đường dây duy nhất (Multiplexing), giải quyết hoàn toàn giới hạn 6 kết nối.
2. **Sử dụng Last-Event-ID (Tự động nối lại)**: SSE có một sức mạnh vô đối: Nếu rớt mạng, trình duyệt tự động gọi lại Server. Càng tuyệt vời hơn, nếu mỗi dòng dữ liệu bạn gán cho nó một cái `id` (Ví dụ: `id: 105`). Khi trình duyệt gọi lại sau khi đứt mạng, nó tự động gửi kèm Header `Last-Event-ID: 105`. Backend chỉ việc lấy dữ liệu từ số 106 trở đi để gửi tiếp. Không sót một tin nào!

</details>

1. **Mandatory HTTP/2 Deployment**: A catastrophic limitation of legacy HTTP/1.1 is that modern browsers strict-cap active connections to a single domain at exactly **6 concurrent connections**. Because SSE holds the connection open, opening 6 tabs of an SSE-enabled web app completely exhausts the browser's connection pool. Any subsequent API requests (like loading an image) will remain eternally Pending. **The Solution**: You MUST deploy your API behind HTTP/2. HTTP/2 utilizes Multiplexing over a single TCP socket, allowing hundreds of concurrent SSE streams to coexist flawlessly in a single tab without connection exhaustion.
2. **Leveraging the Automatic Retry and `Last-Event-ID`**: Unlike WebSockets, the native browser `EventSource` API handles reconnections autonomously. If the WiFi drops, the browser initiates an Exponential Backoff reconnect sequence. As an Engineer, you must exploit the `id` field. If the Server emits `id: 800 \n data: "hello"`, and the connection drops, upon reconnecting, the browser automatically injects the HTTP Header `Last-Event-ID: 800`. The Backend Database must intercept this header and seamlessly replay the stream starting from event `801`, guaranteeing zero data loss during network blips.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Timeouts bị ngắt bởi Proxy/Nginx**: Đau đầu nhất khi code SSE là bạn test trên máy Local thì chạy ngon, lên Production thì cứ chạy được 1 phút là bị đứt. Lý do là Nginx/Load Balancer thường có cấu hình `proxy_read_timeout 60s`. Nó thấy cái kết nối này sao mở lâu quá mà không chịu kết thúc, nó tưởng treo nên nó Cắt đứt cái rụp.
   - *Cách giải quyết*: Phải cấu hình Nginx bỏ qua Timeout cho những link có SSE, và thỉnh thoảng Server phải gửi một dòng Comment rỗng (Ví dụ: `: ping`) để báo cho Nginx biết là luồng này vẫn còn sống.
2. **Client không gửi được Header Xác thực (Auth)**: Đối tượng `new EventSource(url)` của Javascript có một điểm yếu chết người: Bạn KHÔNG THỂ nhét Token JWT vào Custom Header (Ví dụ: `Authorization: Bearer`). 
   - *Cách giải quyết*: Nếu không muốn nhét Token lộ liễu lên URL, bạn phải dùng thư viện ngoài (như `fetch-event-source` của Microsoft) để thay thế `EventSource` mặc định của trình duyệt. Nó cho phép gắn đủ loại Header bảo mật.

</details>

1. **Reverse Proxy (Nginx) Timeout Brutality**: The #1 reason SSE fails in production. You write perfect SSE code locally. On production, the connection mysteriously dies exactly every 60 seconds. Reverse Proxies (Nginx, AWS ALB) enforce strict `proxy_read_timeout` policies to kill slow clients. Because SSE deliberately holds the connection open, Nginx assumes the backend has frozen and terminates the socket. **Fix**: You must aggressively reconfigure Nginx (`proxy_buffering off; proxy_read_timeout 86400;`). Furthermore, the Backend must periodically emit a Keep-Alive comment (`: heartbeat \n\n`) every 15 seconds to appease the Proxy's inactivity timers.
2. **The `EventSource` Authentication Flaw**: The native HTML5 `EventSource` interface is notoriously rigid. It fundamentally lacks the capability to inject custom HTTP Headers (e.g., `Authorization: Bearer <token>`). **The Anti-Pattern**: Passing the JWT in the URL query string (`/stream?token=abc`), immediately leaking the credential into proxy access logs. **The Fix**: Discard the native `EventSource`. Utilize advanced polyfill libraries (like `@microsoft/fetch-event-source`) that leverage the modern `fetch()` API under the hood, natively supporting custom Headers, `POST` bodies, and granular retry controls while parsing the event-stream.

---

## Related Topics

- For full Bi-directional realtime needs, see **[WebSocket](./websocket.md)**.
- To understand why we used HTTP for so long before SSE, see **[Long-Polling](./long-polling.md)**.
- For AI token streaming implementation, study how Large Language Models work.
