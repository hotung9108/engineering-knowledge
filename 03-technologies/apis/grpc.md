# gRPC (gRPC Remote Procedure Calls)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi hệ thống của bạn chia nhỏ thành 100 Microservices. Dịch vụ Đặt Hàng phải gọi Dịch vụ Tồn Kho 1 triệu lần mỗi giây qua mạng. Nếu dùng REST API và JSON, mỗi lần gọi, máy chủ phải tốn CPU để dịch chữ JSON ra Object, rồi lại dịch từ Object thành JSON để gửi đi. Việc này tạo ra một độ trễ khổng lồ và lãng phí CPU. Google đã tạo ra **gRPC** để giải quyết triệt để bài toán này. Nó vứt bỏ hoàn toàn chữ JSON. Nó ép cả 2 máy chủ phải dùng chung một bản hợp đồng (Protobuf). Dữ liệu sẽ được nén thành mã Nhị phân (Binary) siêu nhỏ và truyền qua đường ống HTTP/2. Nhờ đó, 2 máy chủ nói chuyện với nhau ở tốc độ Ánh sáng, bỏ qua hoàn toàn bước "Dịch thuật".

</details>

> **Summary**: In a massively distributed Microservices architecture, internal Server-to-Server communication constitutes the bulk of network traffic. Utilizing REST and JSON over HTTP/1.1 for these internal calls introduces unacceptable overhead. JSON strings are bloated, lack strong typing, and require heavy CPU serialization/deserialization. To eliminate this bottleneck, Google open-sourced **gRPC**. It abandons the Resource-Oriented architecture of REST and reverts to RPC (Remote Procedure Calls), allowing Server A to execute a function on Server B as if it were a local function call. Its extreme performance derives from two technological pillars: **Protocol Buffers (Protobuf)**, which serializes data into highly compressed, strictly-typed binary payloads, and **HTTP/2**, which allows multiplexed, bidirectional streaming over a single TCP connection. gRPC routinely achieves 7x to 10x the throughput of traditional REST architectures.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (Người Việt) cần ra lệnh cho một người thợ (Người Pháp) xây nhà.
1. **REST (JSON)**: Bạn phải thuê một người Phiên dịch. Bạn đọc câu lệnh bằng tiếng Việt. Người phiên dịch chép ra giấy, dịch sang tiếng Anh (JSON), rồi gửi cho người Pháp. Người Pháp nhận tờ giấy tiếng Anh, lại dịch ra tiếng Pháp để hiểu. Trải qua 2 bước dịch, mất 10 phút mới xong một câu. Rất an toàn, nhưng cực kì chậm.
2. **gRPC (Protobuf)**: Bạn và người thợ Pháp đồng ý học chung một Ngôn ngữ Kí hiệu Đặc biệt (Bản hợp đồng Protobuf). Bạn giơ 2 ngón tay lên (Mã nhị phân). Người thợ Pháp nhìn thấy 2 ngón tay, lập tức hiểu ngay là "Lấy gạch". Không cần ai phiên dịch, không cần ghi ra giấy. Tốc độ giao tiếp diễn ra trong 0.001 giây.

</details>

Imagine giving coordinates to an automated Drone.
1. **REST / JSON**: You write a lengthy English letter: *"Dear Drone, please fly to Latitude 40.71, and Longitude -74.00. Thank you."* You put it in an envelope and mail it. The drone receives it, uses a dictionary to translate the English words into numbers, and then flies. The letter is bloated with unnecessary text.
2. **gRPC / Protocol Buffers**: You don't use words. You plug a wire directly into the Drone and transmit exactly 8 bytes of raw binary code `0100101...` The drone natively understands binary. It doesn't read. It doesn't translate. It just executes instantly. The payload size is 10 times smaller, and the execution is instantaneous.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

gRPC phá vỡ mọi quy tắc của REST, dựa trên 3 trụ cột:
1. **RPC (Remote Procedure Call)**: Khác với REST dùng URL (`GET /users`), gRPC ép bạn gọi một hàm trực tiếp xuyên qua mạng. Mã nguồn Backend của bạn gọi `Inventory.SubtractItem(5)`. Lệnh này sẽ bay sang máy chủ Tồn kho và chạy hàm đó y như thể nó nằm chung trên 1 máy tính.
2. **Protocol Buffers (Protobuf)**: Đây là vũ khí bí mật. Thay vì viết tài liệu API bằng Word, bạn viết một file `.proto`. File này định nghĩa chặt chẽ: "Hàm này nhận vào 1 con Số (Int), trả về 1 chuỗi Chữ (String)". Sau đó, bạn dùng Tool để **Sinh code tự động** ra hàng chục ngôn ngữ (Go, Java, Python).
3. **HTTP/2**: REST dùng HTTP/1.1 (Gọi xong 1 lệnh, ngắt kết nối mạng. Gọi lệnh 2, mở lại kết nối). gRPC ép buộc dùng HTTP/2. Nó mở ĐÚNG 1 CÁI ỐNG NƯỚC, và bơm hàng ngàn lệnh qua cái ống đó cùng lúc (Multiplexing). Thậm chí hỗ trợ gọi Video Call/Livestream 2 chiều mượt mà.

</details>

gRPC is defined by a complete departure from textual representation and stateless constraints:
1. **The RPC Paradigm (Action-Oriented)**: REST is Noun-based (Resources). gRPC is Verb-based (Actions). It allows a microservice written in Go to execute a function explicitly named `CalculateTaxes(TaxRequest)` on a microservice written in Java, completely abstracting away the network logic.
2. **Protocol Buffers (The IDL & Serialization)**: JSON is schema-less text. Protobuf is an Interface Definition Language (IDL) and a Binary Serialization format. You define your Data Structures and Service Methods in a `.proto` file. The Protocol Buffer Compiler (`protoc`) then mathematically generates highly optimized Client Stubs and Server Skeletons natively in C++, Java, Python, Go, etc. Data is serialized into a dense binary stream (stripping away all field names like "firstName"), transferring only the raw values and their positional tags.
3. **HTTP/2 Transport**: gRPC inherently mandates HTTP/2. This unlocks true Multiplexing (sending hundreds of concurrent requests over a single TCP connection without Head-of-Line blocking). Furthermore, it enables native **Streaming**: Unary (1 request, 1 response), Client Streaming, Server Streaming, and Bidirectional Streaming (like WebSockets, but binary and strictly typed).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy hình dung một Hệ thống siêu lớn (như Netflix hay Uber). Mở App lên, cần gọi 20 Microservices chéo nhau để có đủ dữ liệu.
Nếu dùng JSON: Quá trình "Serialize" (Dịch Object thành chữ JSON) và "Deserialize" (Dịch chữ JSON thành Object) tiêu tốn một lượng CPU khổng lồ một cách vô ích. Các máy chủ thay vì dùng CPU để tính tiền, lại phải dùng CPU để ngồi "dịch chữ".
Thêm nữa, Lập trình viên Python viết nhầm tên biến `userID` thành `user_id`. Không có gì báo lỗi lúc viết code, lúc chạy hệ thống mới sập.
gRPC sinh ra để giải quyết 2 điều đó:
1. **Nén Binary**: Gửi số 0 và 1, máy tính không cần dịch. Tiết kiệm 80% sức mạnh CPU.
2. **Type-Safe (Bắt lỗi từ trong trứng)**: Vì dùng chung file `.proto`, bạn gõ sai chữ `user_id`, màn hình code sẽ gạch đỏ báo lỗi ngay lập tức. Không bao giờ có chuyện 2 máy chủ bị lệch cấu trúc dữ liệu.

</details>

gRPC was explicitly engineered for **Inter-Service Microservice Optimization** and **Polyglot Consistency**.
In a cluster of 500 Microservices running on Kubernetes, network latency and serialization CPU overhead compound disastrously. JSON is horribly inefficient. The CPU spends 20% of its total lifecycle just parsing quotation marks and brackets.
Furthermore, relying on REST API documentation (Swagger/OpenAPI) is often unreliable. If the Java team updates the JSON response but forgets to tell the Node.js team, the system crashes at runtime.
gRPC enforces an iron-clad **Contract-First Development** methodology. The `.proto` file is the absolute source of truth. If the Java team changes a field type from `int32` to `string`, the Go team's build pipeline will immediately fail at compile-time. This strict Type-Safety prevents catastrophic runtime schema mismatches across a polyglot infrastructure.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh Truyền tải dữ liệu: "Gửi thông tin một Người dùng tên Alex, 30 tuổi".
</details>

Visualizing Data Serialization (JSON vs Protobuf).

| Metric | REST API (JSON) | gRPC (Protocol Buffers) |
|---|---|---|
| **The Payload** | `{"name":"Alex","age":30}`<br>(Size: ~25 bytes) | `\x0A\x04Alex\x10\x1E`<br>(Size: **8 bytes**) |
| **Serialization Overhead**| The CPU reads the string character by character, parses the quotes, matches keys, and constructs a memory object. Slow. | The CPU reads the binary positions directly into memory structures. Natively executed at the C++ level. Lightning fast. |
| **Code Generation** | Developer manually writes `fetch()` and manually casts the JSON to a TypeScript interface. | The compiler generates the entire SDK. Developer just calls `client.GetUser()`. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giao tiếp nội bộ giữa các Microservices**: Đây là lý do chính gRPC tồn tại. Ví dụ: Dịch vụ Xác thực (Auth) dùng Go, Dịch vụ Giỏ hàng dùng Node.js, Dịch vụ AI dùng Python. Tất cả sẽ nói chuyện với nhau bằng gRPC qua cổng HTTP/2 để đạt tốc độ tối đa trong nội bộ Datacenter.
2. **Hệ thống Streaming 2 chiều (Bidirectional Streaming)**: Ứng dụng chat thời gian thực, Game Multiplayer, hoặc các cảm biến IoT gửi tọa độ liên tục mỗi mili-giây. Kết nối mở liên tục, dữ liệu đẩy qua lại 2 chiều siêu mượt không cần chờ đợi.
3. **App Mobile và Thiết bị IoT cấu hình yếu**: App trên Smartwatch có pin cực yếu, CPU siêu cùi. Nếu bắt nó parse JSON nó sẽ tốn pin. Dùng gRPC đẩy cục nhị phân thẳng vào, CPU không phải làm gì, giúp tiết kiệm pin tối đa. (Lưu ý: Web Browser chạy gRPC rất khó, gRPC sinh ra chủ yếu cho App Native/Server).

</details>

1. **Internal Microservice-to-Microservice Communication**: The absolute primary use-case. In an AWS VPC, replacing REST with gRPC between the Payment Gateway and the Fraud Detection service instantly drops latency from 30ms to 3ms, saving significant compute costs and improving the end-user response time.
2. **Polyglot Ecosystems**: When an organization uses Go for networking, Java for enterprise logic, and Python for Machine Learning. Protobuf acts as the universal translator, generating native, perfectly typed client libraries for every language from a single repository of `.proto` files.
3. **Real-Time Bidirectional Streaming**: Telemetry from IoT devices, real-time multiplayer game state synchronization, or streaming massive chunks of a file. Unlike WebSockets (which transmit unstructured text/binary), gRPC Bidirectional Streams maintain strict Protobuf typing while keeping the TCP socket open indefinitely.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Quản lý file `.proto` tập trung**: File Protobuf là Trái tim của hệ thống. Hãy tạo một Kho mã nguồn (Git Repo) riêng biệt CHỈ ĐỂ CHỨA file `.proto`. Cả Team Backend và Team Frontend đều phải clone Repo này về. Khi ai muốn sửa API, phải tạo Pull Request (PR) ở Repo này. Nhờ đó, cả công ty luôn thống nhất một cấu trúc dữ liệu duy nhất.
2. **KHÔNG BAO GIỜ đổi số thứ tự (Tag Numbers)**: Trong file `.proto`, bạn khai báo `string name = 1; int32 age = 2;`. Nếu bạn không thích tuổi nữa, XÓA chữ `age` đi, nhưng TUYỆT ĐỐI không được dùng lại số `2` cho biến khác (Ví dụ: `string email = 2`). Mã nhị phân chỉ nhớ số, không nhớ chữ. Nếu bạn gán số 2 cho Email, hệ thống cũ bắn số vào hệ thống mới sẽ bị sai lệch cấu trúc và sập toàn bộ dữ liệu. Hãy đánh dấu nó là `reserved 2;`.

</details>

1. **Centralized Schema Repository**: The `.proto` files dictate the entire nervous system of your architecture. Do not scatter them across different Microservice repositories. **Rule**: Create a dedicated, standalone Git repository (e.g., `company-protobuf-schemas`). All microservices import this repo as a submodule. This ensures that any architectural change to the API contract triggers a centralized code review.
2. **Never Reuse Field Tags (Forward/Backward Compatibility)**: The most fatal mistake in Protobuf design. A message is defined as `string title = 1; int32 price = 2;`. The numbers (1, 2) are how the binary stream identifies the fields. The field names are ignored. If you decide to deprecate `price`, you can delete it. But if you accidentally assign `string author = 2;` in the next version, an old Client will send an integer (price) into a field the new Server expects to be a string (author), causing catastrophic binary deserialization failures. **Rule**: Always use the `reserved` keyword for deleted tags (`reserved 2;`).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cố chấp dùng gRPC cho Web Frontend (Trình duyệt)**: Trình duyệt web (Chrome, Safari) chưa hỗ trợ gọi trực tiếp HTTP/2 gRPC. Nếu bạn cố ép Website ReactJS kết nối gRPC, bạn PHẢI cài một cổng trung gian tên là `gRPC-Web` (Envoy Proxy). Quá trình cài đặt cực kì đau khổ, rườm rà và khó gỡ lỗi vì dữ liệu bay trên mạng là mã nhị phân không đọc được bằng mắt người.
   - *Luật*: Chừa gRPC cho nội bộ Server, hoặc App Mobile Native (iOS/Android). Đối với Web React/Vue, hãy tiếp tục dùng REST hoặc GraphQL.
2. **Mất khả năng Debug bằng Mắt thường**: Ở REST, bật tab Network của Chrome lên, bạn thấy dòng JSON `{"error": "sai mật khẩu"}` rõ mồn một. Ở gRPC, nếu bạn chặn đường truyền mạng, bạn chỉ thấy một đống giun dế mã nhị phân `\x00\x05...`. Việc tìm lỗi (Debug) trở nên khó khăn gấp 10 lần. Bạn bắt buộc phải xài các công cụ chuyên dụng như `gRPCurl` hoặc Postman bản mới hỗ trợ gRPC.

</details>

1. **Forcing gRPC into the Browser (gRPC-Web Friction)**: Native gRPC relies on strict access to HTTP/2 trailers, which standard browser APIs (`fetch`, `XMLHttpRequest`) physically do not expose. You cannot call a gRPC server directly from React or Angular. You are forced to deploy a specialized reverse proxy (Envoy) and use the `gRPC-Web` protocol to translate HTTP/1.1 calls into gRPC. It is operationally painful and defeats many performance benefits. **Rule**: Use REST or GraphQL for the Frontend-to-Backend boundary. Reserve gRPC exclusively for the Backend-to-Backend (Microservice) boundary.
2. **The Loss of Human Readability (Debugging Hell)**: Because payloads are raw binary, you cannot simply `curl` an endpoint in your terminal or inspect the payload using Wireshark/Chrome DevTools. A binary payload looks like absolute gibberish. **Fix**: You must adopt specialized tooling. Ensure Server Reflection is enabled in Development environments, and utilize tools like **gRPCurl** or BloomRPC/Postman to dynamically translate the binary back into JSON for human debugging.

---

## Related Topics

- For strictly typed API contracts, gRPC utilizes **Protocol Buffers**.
- For defining the Gateway that translates REST calls from the web into gRPC calls for the backend, explore **[Envoy Proxy](../web-servers/envoy.md)** *(coming soon)*.
- If you are building Web/React applications, stick to **[REST](./rest.md)** or **[GraphQL](./graphql.md)** instead.
