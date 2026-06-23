# gRPC: High-Performance RPC Framework

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: REST API dùng cấu trúc JSON (Text) rất thân thiện với con người, nhưng nó lại quá chậm và cồng kềnh đối với Máy tính. Khi bạn xây dựng một hệ thống khổng lồ với hàng trăm Microservices gọi nội bộ lẫn nhau, sự chậm trễ của JSON sẽ làm sập máy chủ. **gRPC** (do Google phát minh) ném bỏ JSON, thay bằng việc nén dữ liệu thành mã Nhị phân (Protobuf) và truyền qua siêu tốc lộ HTTP/2. Kết quả: Tốc độ gọi API tăng vọt gấp 10 lần, băng thông giảm 60%.

</details>

> **Summary**: REST APIs, utilizing verbose JSON payloads over HTTP/1.1, are universally optimized for human readability and Frontend browser consumption. However, in massive Microservice architectures where Backend servers relentlessly ping other Backend servers thousands of times a second, the CPU overhead of parsing text-based JSON becomes a catastrophic bottleneck. **gRPC** (gRPC Remote Procedure Calls), engineered by Google, aggressively discards JSON in favor of ultra-compressed Binary serialization (**Protocol Buffers**), transmitted over the highly multiplexed **HTTP/2** protocol. The result is a 10x velocity multiplier and a 60% reduction in network payload size.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (Microservice A) muốn nhắn tin cho bạn thân (Microservice B).
- **REST API (Viết thư tay JSON)**: Bạn viết một bức thư rất lịch sự, dài dòng: "Xin chào bạn, tôi là A, tôi muốn yêu cầu bạn cấp cho tôi dữ liệu người dùng số 1". Bỏ vào phong bì và gửi đi (HTTP/1). Bạn kia nhận được, phải đeo kính vào ngồi đọc từng chữ rồi mới hiểu. Rất chậm!
- **gRPC (Mật mã nhị phân Protobuf)**: Hai người ngầm hẹn trước với nhau một Cuốn sổ Mật mã (File `.proto`). Khi cần gọi, bạn chỉ bấm máy tít tít mã Morse: `010`. Người kia nghe tiếng `010`, giở Cuốn sổ ra đối chiếu và hiểu ngay lập tức ý bạn muốn gì. Cực kỳ bảo mật, siêu tốc độ, nhưng người ngoài nghe thì điếc tai không hiểu gì cả.

</details>

Imagine you (Backend Service A) need to rapidly communicate with your colleague (Backend Service B).
- **REST API (Writing a formal English letter)**: You write a highly verbose, grammatically perfect letter: *"Greetings. My name is Service A. I hereby request the User Profile corresponding to ID 42."* You mail it via traditional post (HTTP/1.1). Service B receives it, puts on their reading glasses, and spends precious seconds manually parsing the English text (JSON parsing).
- **gRPC (Military Encrypted Morse Code)**: Before communicating, you both memorize the exact same Military Codebook (The `.proto` Schema). When you need data, you instantly blast an encrypted burst: `01 2A`. Service B receives the binary burst, bypasses human parsing completely, looks at the Codebook, and instantly executes the command. Blazingly fast, but completely unreadable to anyone lacking the Codebook.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

gRPC là sự kết hợp của 2 công nghệ cốt lõi:
1. **Protocol Buffers (Protobuf)**: Thay vì dùng JSON, gRPC định nghĩa cấu trúc dữ liệu bằng file `.proto`. File này sau đó sẽ tự động generate (đẻ ra) Code cho cả Java, Python, Go,... Dữ liệu bay trên mạng sẽ bị nén thành cục nhị phân 0101 vô nghĩa, siêu nhẹ.
2. **HTTP/2**: REST dùng HTTP/1.1, mỗi lần gọi API phải mở 1 kết nối TCP mới, gọi xong thì đóng lại (Rất tốn thời gian). gRPC dùng HTTP/2. Nó mở 1 cái ống nước duy nhất giữa 2 Server, và xả hàng ngàn luồng dữ liệu (Multiplexing) chạy song song trong cái ống đó 24/7. Không tốn thời gian khởi tạo kết nối.

</details>

gRPC achieves its extreme performance through the rigid marriage of two specific technologies:
1. **Protocol Buffers (Protobuf as the IDL)**: It entirely abandons JSON. Instead, architects define strict Data Contracts in an Interface Definition Language (IDL) via `.proto` files. The gRPC compiler then automatically generates boilerplate Native Client/Server Code in C++, Java, Go, Python, etc. Network payloads are heavily compressed into unintelligible Binary byte-streams.
2. **HTTP/2 (The Transport Protocol)**: Traditional REST utilizes HTTP/1.1, which suffers from Head-of-Line Blocking and high TCP Handshake overhead. gRPC exclusively utilizes HTTP/2. It establishes a single, persistent TCP connection between Microservices and aggressively **Multiplexes** thousands of concurrent, bi-directional binary streams through that single pipe, entirely eliminating latency bottlenecks.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề của Hệ thống Microservices phân tán**:
Khi bạn lên Shopee bấm "Đặt hàng". Lệnh đó không chạy vào 1 cục Server. Nó gọi Server Đặt hàng. Server Đặt hàng (gọi REST API) sang Server Thanh toán. Server Thanh toán (gọi REST API) sang Server Khuyến mãi và Server Giao Hàng.
Một cú click chuột sinh ra 20 cuộc gọi API nội bộ! Việc Parse JSON (dịch text thành Object) tiêu tốn cực kỳ nhiều CPU. Độ trễ (Latency) của mạng cộng dồn lại khiến user phải chờ 5 giây mới đặt xong hàng.

**Giải pháp gRPC**:
Google đẻ ra gRPC để giải quyết triệt để bài toán này. Bằng việc đẩy dữ liệu qua Nhị phân và dùng HTTP/2, độ trễ giữa các máy chủ Backend giảm xuống gần bằng Không. User click chuột, giao dịch xuyên qua 20 máy chủ chỉ trong 0.1 giây.

</details>

**The Latency Compounding Crisis in Microservices**:
In a colossal distributed architecture (e.g., Netflix or Uber), a single user action (clicking "Ride Now") does not hit one monolithic server. It hits the API Gateway, which pings the User Service, which pings the Billing Service, which pings the Geospatial Routing Service. 
One single user click triggers a cascading waterfall of 25 internal Server-to-Server network calls. If those calls rely on REST/JSON over HTTP/1.1, the network latency and CPU JSON-parsing overhead compounds violently. A 20ms delay multiplied by 25 hops results in a 500ms timeout. The entire system architecture collapses under its own communication weight.

**The gRPC Solution**:
Google engineered gRPC specifically for this Inter-Service communication. By mathematically compressing payloads via Protobuf and blasting them through persistent HTTP/2 streams, the CPU parsing overhead drops to near zero. The 25 network hops are executed in a fraction of a millisecond.

---

## Layer 3: Without vs. With Comparison (Compare)

### REST vs gRPC Performance Breakdown

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh gRPC và REST.
</details>

Analyzing the architectural disparities between the standard REST payload and gRPC.

| Feature | REST (Representational State Transfer) | gRPC (gRPC Remote Procedure Calls) |
|---|---|---|
| **Data Format** | JSON (Text, Human-readable). Heavy CPU usage to parse. | Protobuf (Binary, Machine-readable). Blazing fast parsing. |
| **Transport** | HTTP/1.1 (Sequential, Head-of-line blocking). | HTTP/2 (Multiplexed, Persistent Streams). |
| **Contract (Schema)** | Optional/Loose (OpenAPI/Swagger must be written manually). | **Strictly Mandatory** (`.proto` file is the absolute source of truth). |
| **Code Generation** | You manually write the HTTP `fetch()` logic. | Compiler auto-generates the Client/Server networking code. |
| **Browser Support** | Universal. All browsers speak HTTP/1 JSON perfectly. | Very Poor. Browsers cannot easily manipulate raw HTTP/2 Binary frames (Requires `grpc-web` proxy). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Bắt buộc dùng gRPC**: Liên lạc Đáy biển (Backend to Backend). Bất kỳ khi nào 2 con Server của bạn cần nói chuyện với nhau ở cường độ cao (vài ngàn request/s).
- **Luồng dữ liệu thời gian thực (Streaming)**: Nhờ HTTP/2, gRPC hỗ trợ Stream dữ liệu 2 chiều. Bạn có thể thiết kế một hệ thống Chat hoặc Bắn dữ liệu chứng khoán liên tục mà không bao giờ bị đứt kết nối.
- **Không nên dùng gRPC**: Giao tiếp trực tiếp với Trình duyệt (Browser to Backend). Trình duyệt Chrome/Firefox rất kém trong việc đọc mã nhị phân HTTP/2 gRPC. Bắt buộc phải dựng một cái Proxy (Envoy) đứng giữa để dịch từ gRPC sang REST JSON cho Trình duyệt đọc. Chỗ này cứ dùng REST cho nhẹ đầu.

</details>

- **The Gold Standard Use Case**: Internal Microservice-to-Microservice communication within a Kubernetes Cluster or AWS VPC. If the Billing Service must validate millions of transactions against the Ledger Service, gRPC is the only architecturally sound choice to prevent latency cascading.
- **Bi-Directional Streaming**: Because gRPC operates on HTTP/2, it natively supports complex streaming paradigms. A Client can open a single persistent connection and continuously stream Gigabytes of telemetry data to the Server (Client Streaming), or both can blast data simultaneously (Bi-directional Streaming, ideal for low-latency Chat/Voice applications).
- **The Anti-Pattern (Browser-to-Backend)**: Do not attempt to expose pure gRPC directly to a Frontend Web Browser (React/Vue). Browsers enforce strict CORS rules and lack robust low-level HTTP/2 frame control to decrypt Protobuf streams natively. While `grpc-web` exists, it requires deploying an Envoy Reverse Proxy to translate the traffic. For Browser-facing APIs, stick to traditional REST JSON or GraphQL.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khả năng tương thích ngược của File `.proto`**: Khi bạn sửa file `.proto` (Thêm cột mới, đổi tên biến), TUYỆT ĐỐI KHÔNG ĐƯỢC ĐỔI SỐ THỨ TỰ (Tag Number) của các biến cũ. Nếu biến `string name = 1`, sang năm bạn xóa nó đi, hãy để trống số 1, tạo biến mới là `int age = 2`. Nếu bạn tái sử dụng số 1, toàn bộ hệ thống gRPC sẽ dịch mã nhị phân sai bét nhè và sập toàn tập.
2. **Chia sẻ file `.proto` (Schema Registry)**: Đừng copy/paste file `.proto` rải rác khắp 10 repo code khác nhau. Hãy tạo 1 kho Git riêng (Central Registry) chỉ chứa file `.proto`. Mọi team Backend phải lên đó tải bản thiết kế chuẩn nhất về để generate code.

</details>

1. **Strict Protobuf Forward/Backward Compatibility**: The core of gRPC's binary compression is the Tag Number assigned in the `.proto` file (e.g., `string email = 2;`). The binary payload *never* sends the word "email"; it only sends the number `2`. **Golden Rule**: If you deprecate a field, NEVER reuse its Tag Number for a new field. If you do, older Clients will deserialize your new "Age" integer into their legacy "Email" string variable, triggering catastrophic ClassCastExceptions and immediate system crashes. Mark deprecated fields as `reserved 2;`.
2. **Centralized Schema Management**: Do not physically copy/paste `.proto` files across 50 different microservice Git repositories. This inevitably leads to version drift, where Service A is compiling against v1, and Service B is compiling against v3. Architect a dedicated, centralized "Schema Registry" Git repository. CI/CD pipelines automatically trigger code-generation and push versioned SDK packages (NPM/Maven/Go modules) containing the compiled gRPC clients to your internal artifact server.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Load Balancing gRPC khó hơn REST**: Ở REST, mỗi Request là 1 kết nối TCP riêng biệt, nên Load Balancer (Nginx/AWS ALB) dễ dàng chia đều traffic ra 5 server. Nhưng gRPC mở đúng MỘT KẾT NỐI (HTTP/2) và giữ chặt nó mãi mãi. Nếu bạn dùng Load Balancer cấp thấp (L4), toàn bộ traffic gRPC sẽ bị đổ dồn vào duy nhất 1 Server, 4 con kia ngồi chơi! Bắt buộc phải dùng Load Balancer L7 (Như Envoy proxy hoặc gRPC Client-side load balancing) để chẻ luồng bên trong HTTP/2 ra.
2. **Lạm dụng gRPC cho việc đơn giản**: Đừng vác dao mổ trâu đi giết gà. Nếu dự án của bạn chỉ là 1 con Backend bé xíu kết nối với ReactJS, việc setup file `.proto`, cài đặt Compiler C++, quản lý gRPC Gateway sẽ làm độ phức tạp của dự án tăng x10 lần mà chả mang lại lợi ích gì. Dùng REST cho nhanh!

</details>

1. **The gRPC Load Balancing Trap (L4 vs L7)**: A devastating architectural oversight. Because gRPC heavily relies on persistent HTTP/2 TCP connections, a standard Layer 4 TCP Load Balancer (like AWS Classic ELB or basic HAProxy) will establish the connection to Server A and route *all* subsequent multiplexed requests to Server A forever. Servers B, C, and D will sit at 0% CPU utilization while Server A melts down. You MUST utilize Layer 7 Load Balancing (e.g., Envoy, Linkerd, Istio, or AWS ALB with gRPC support) capable of deeply inspecting the HTTP/2 frames and routing individual streams across the cluster.
2. **Premature Optimization (Over-engineering)**: Adopting gRPC for a simple CRUD Monolith communicating with a React Frontend. gRPC introduces massive operational overhead: managing `.proto` compilation chains, complex debugging (you cannot just read network requests in the Chrome DevTools Network Tab because it's encrypted binary), and deploying translation proxies. If you do not have a massive microservice mesh suffering from proven CPU JSON-parsing bottlenecks, stick to REST.

---

## Related Topics

- Compare gRPC's binary format to REST's JSON format in **[Data Formats](../web-fundamentals/data-formats.md)**.
- Understand the transport layer protocols gRPC is built upon in **[TCP/IP Model](./tcp-ip.md)**.
- To compare architecture, review standard **[REST API](./rest-api.md)**.
