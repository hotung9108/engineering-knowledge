# Distributed Tracing

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Log (Nhật ký) là từng khung hình rời rạc, thì **Tracing (Dấu vết)** là cuốn băng Video quay lại toàn bộ chuyến đi của một Khách hàng. Khi khách hàng bấm nút "Thanh toán", tín hiệu mạng sẽ nhảy từ Web $\rightarrow$ API Gateway $\rightarrow$ Service Order $\rightarrow$ Service Payment $\rightarrow$ Database. Tổng cộng mất 5 giây. Khách hàng chửi "Web chậm!". Nếu chỉ đọc Log, bạn không thể biết Service nào trong 5 cái kia làm chậm. **Distributed Tracing** là kỹ thuật tạo ra một cái Thẻ căn cước (`Trace ID`), đeo nó vào cổ cái tín hiệu mạng đó từ lúc bắt đầu cho đến khi kết thúc. Nhờ vậy, trên Datadog, bạn sẽ nhìn thấy một Biểu đồ Thác nước (Waterfall), chỉ đích danh: "API Gateway 10ms, Order 20ms, Payment 4900ms". Bạn bắt được ngay thủ phạm.

</details>

> **Summary**: In a monolithic application, analyzing performance is trivial via a localized stack trace. In a Microservice architecture, a single user transaction initiates a hyper-complex, asynchronous graph of network calls spanning dozens of independent services, queues, and databases. If the overarching HTTP request degrades to 5000ms, standard Logs cannot structurally answer: "Which exact network hop induced the latency?" **Distributed Tracing** solves this macroscopic causality problem. It injects a globally unique identifier (`Trace ID`) into the HTTP Header at the Edge Gateway and explicitly propagates it through every internal Service. Observability platforms aggregate these spans to render a deterministic Waterfall Graph, illuminating the precise critical path and isolating systemic bottlenecks.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một món Hàng (Request) được chuyển qua 4 trạm Bưu điện (Microservices) để đến tay bạn.
1. **Chỉ có Logs (Thiếu Tracing)**: Hàng giao trễ 1 tháng. Bạn gọi lên Tổng đài chửi. Tổng đài viên gọi xuống từng trạm bưu điện để hỏi. Trạm 1 bảo: "Tôi đã nhận rồi". Trạm 2 bảo: "Tôi nhận rồi chuyển đi ngay". Không trạm nào chịu nhận lỗi vì họ chỉ xem sổ nhật ký của ĐÚNG TRẠM ĐÓ. Không ai nhìn thấy bức tranh tổng thể.
2. **Có Distributed Tracing**: Món hàng được dán một cái Mã Vạch (Trace ID) ngay từ lúc gửi. Mỗi trạm bưu điện đều bắt buộc phải dùng máy quét mã vạch này: "Đã vào trạm 1 lúc 8h, Đã ra trạm 1 lúc 9h". Bạn mở app điện thoại lên xem (Grafana/Datadog), bạn thấy rõ ràng dòng chữ màu đỏ: "Hàng nằm ở Trạm số 3 suốt 28 ngày!". Thủ phạm đã lộ diện.

</details>

Imagine tracking a piece of luggage traveling through 4 different Airports.
1. **Without Tracing (Just Logs)**: Your bag is lost. You call the airline. They have to manually call Airport 1, Airport 2, Airport 3, and Airport 4. Each airport checks their local ledger book. It takes 5 days to piece together the story and figure out where the bag stopped.
2. **With Distributed Tracing**: A barcode (`Trace ID`) is physically taped to the bag at Check-In. As the bag moves through the conveyor belts, lasers scan the barcode and send the exact Timestamp to a central database. You open an App on your phone and instantly see a visual timeline: `JFK: 2 hrs -> LHR: 5 hrs -> NRT: LOST`. You instantly know exactly which airport to blame.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Một hệ thống Tracing được cấu tạo bởi 2 khái niệm toán học:
1. **Trace (Chuyến đi lớn)**: Đại diện cho toàn bộ 1 Request của người dùng từ lúc bấm nút đến lúc nhận kết quả. Nó có 1 cái tên là `Trace_ID` (Ví dụ: `Trace_123`).
2. **Span (Chặng đường nhỏ)**: Chuyến đi lớn được chặt ra làm nhiều chặng nhỏ. Mỗi thao tác (Gọi Database, Gọi Redis, Gọi API khác) là 1 Span. Mỗi Span có 1 cái tên riêng (`Span_ID`), và có thời gian Bắt đầu / Kết thúc. Đặc biệt, Span con phải ghi nhớ tên của Span cha (`Parent_ID`) để lát nữa hệ thống vẽ sơ đồ cây không bị nhầm.

</details>

Distributed Tracing relies on a strictly defined directed acyclic graph (DAG) data model, consisting of two primary primitives:
1. **The Trace**: Represents the macroscopic lifecycle of a single distributed transaction (e.g., a User clicking "Checkout"). It is identified by a globally unique `Trace ID` (e.g., a 128-bit UUID generated at the API Gateway).
2. **The Span**: Represents a contiguous segment of work within a Trace (e.g., executing an SQL Query, or calling the Auth Service via gRPC). Every Span possesses its own unique `Span ID`, a `Start Time`, a `Duration`, and crucially, a `Parent Span ID`. This precise parent-child pointer architecture enables the aggregator to mathematically reconstruct the exact hierarchical Waterfall visualization of the execution flow.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

"Đổ thừa" (Fingerpointing) là môn thể thao vua của các team IT trong công ty.
Team Giao diện (Frontend) chửi: "Web load chậm quá, API của Backend cùi bắp!".
Team Backend gắt lại: "Code tao chạy có 5ms, chậm là do bọn Database!".
Team Database cãi: "Tao trả dữ liệu trong 1ms, tụi bây xem lại mạng LAN đi!".
Nếu không có Tracing, công ty sẽ chìm trong những cuộc cãi vã vô tận vì ai cũng có cái Log chứng minh mình đúng (Và họ đúng thật, nhưng lỗi nằm ở cái Ranh giới kết nối giữa các Service).
Tracing tồn tại để tiêu diệt sự phỏng đoán. Khi mở Datadog lên, Biểu đồ Thác nước (Waterfall) vẽ ra rành rành: Frontend mất 50ms, Backend mất 5ms, Database mất 1ms. NHƯNG khoảng thời gian trống giữa Backend và Database là 5000ms. Thủ phạm chính là độ trễ của Cáp Mạng, không ai phải đổ thừa ai nữa.

</details>

In a microservice engineering organization, Latency Degradation initiates vicious inter-team finger-pointing.
The Frontend Team blames the Core API. The Core API team checks their local metrics (`avg_latency: 5ms`) and blames the Database Team. The Database Team checks their logs (`query_time: 1ms`) and blames the Network Team.
Without Tracing, isolating the fault is scientifically impossible because local Logs and Metrics inherently lack Cross-Service Context. The fault might reside in an overloaded DNS resolver, a saturated Redis connection pool, or TCP packet loss.
Tracing exists to definitively eradicate architectural ambiguity. The distributed Waterfall Graph visualizes the literal flow of execution across service boundaries. If the Core API finishes its span at `T=10ms`, but the downstream Payment Service span doesn't begin until `T=5000ms`, the trace explicitly proves that the 5-second latency was induced by Network transit or a saturated thread pool queue between the two services.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc tìm nguyên nhân làm API Đăng ký tài khoản bị trễ (Mất 3 giây).
</details>

Visualizing Root Cause Analysis (RCA) for a 3-second latency degradation.

| Diagnostic Step | Logging & Metrics Only | Distributed Tracing (Waterfall) |
|---|---|---|
| **1. Symptom** | API `/register` p99 latency is `3000ms`. | API `/register` p99 latency is `3000ms`. |
| **2. Investigation**| SSH into `AuthService`. Tail logs. | Click the Slow Trace in Datadog UI. |
| **3. Finding** | Logs show "Successfully inserted User". | Waterfall UI expands instantly. |
| **4. Root Cause** | Unknown. Did the DB take long? Did email take long? | Waterfall explicitly highlights the `SendEmail_API` span taking `2950ms` in red. |
| **Time to Fix** | Hours (Guessing and deploying extra logs). | **15 Seconds** (Absolute certainty). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Chuẩn OpenTelemetry (OTel)**: Ngày xưa mỗi công ty Tracing (Datadog, Jaeger) đẻ ra 1 cách viết Trace riêng. Đổi nhà cung cấp là phải viết lại toàn bộ Code. Giờ đây thế giới thống nhất dùng chuẩn OpenTelemetry. Bạn viết code theo chuẩn này, dữ liệu phát ra có thể dễ dàng ném cho Datadog, Jaeger hay Zipkin đọc đều được.
2. **Service Mesh (Istio / Envoy)**: Gắn Tracing vào code rất cực. Lập trình viên phải tự viết Header, tự đẻ Trace ID. Trong môi trường Kubernetes, Service Mesh (Istio) sẽ đứng ra làm thay việc đó. Ký sinh trùng Envoy nằm ngoài cái Container sẽ TỰ ĐỘNG đo thời gian mạng đi vào đi ra, tự động nối Trace ID và ném lên màn hình Jaeger mà không cần sửa 1 dòng code Backend nào.
3. **Truy vấn Database (N+1 Query Detection)**: Tracing cực kỳ giỏi trong việc bắt lỗi Database N+1. Nhìn lên Waterfall, thay vì thấy 1 cái Span Database dài thòng. Bạn sẽ thấy 500 cái Span Database ngắn tí hon rải rác. Biết ngay thằng Dev nào dùng ORM ngu ngốc để loop Query trong vòng For.

</details>

1. **The OpenTelemetry (OTel) Standard**: Historically, Tracing libraries were strictly vendor-locked (e.g., Datadog APM SDK vs. New Relic SDK). Migrating vendors required rewriting thousands of lines of manual instrumentation. The CNCF introduced **OpenTelemetry (OTel)**, the universal open-source standard for generating telemetry data. Engineers instrument their Java/Node apps using the vendor-neutral OTel SDKs. The OTel Collector then exports the standardized spans to any backend (Jaeger, Zipkin, Datadog) interchangeably.
2. **Service Mesh Auto-Instrumentation (Istio / Envoy)**: Manually passing HTTP `X-B3-TraceId` headers through application logic is tedious and error-prone. Modern Kubernetes environments leverage a Service Mesh to abstract this complexity. The Envoy sidecar proxy transparently intercepts all inbound and outbound network traffic. Envoy automatically generates the trace context, measures the network transit spans, and propagates the headers to downstream Pods, delivering distributed tracing with "Zero-Code Changes".
3. **Detecting ORM N+1 Anomalies**: Tracing is not just for network hops; APM agents automatically instrument database drivers (JDBC/Prisma). When an inexperienced developer writes a `for` loop that queries the database, the Tracing UI will vividly render a disastrous visual pattern: 500 individual, perfectly sequential 2ms DB Spans inside a single HTTP transaction. It visually exposes the N+1 problem instantly.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Truyền Header thủ công (Context Propagation)**: Service Mesh chỉ giúp đo lường mạng, nhưng nó không biết code bên trong Container làm gì. Khi Web gọi API A (Truyền cái `Trace_ID = 123` ở Header). API A xử lý xong, lúc gọi sang API B, lập trình viên BẮT BUỘC PHẢI viết code lôi cái `Trace_ID` từ Request cũ, nhét vào Header của Request mới gửi cho B (Gọi là Propagate). Chỉ cần 1 Service lười không nhét Header, sợi dây Trace sẽ bị đứt đôi vĩnh viễn.
2. **Kẹp Trace_ID vào Log (Log Correlation)**: Tracing vẽ được biểu đồ nhưng không nói được câu văn chi tiết. Log in được câu văn nhưng không có biểu đồ. Bạn phải kẹp cái `Trace_ID` vào mọi dòng Log. Trên Datadog, khi đang xem biểu đồ Tracing, bạn nhấn chuột phải vào 1 cái Span bị lỗi $\rightarrow$ Chọn "Xem Logs". Nó sẽ lôi ĐÚNG cái dòng Log lỗi của riêng cái Request đó ra. Đây là cảnh giới tối cao của Debugging.

</details>

1. **Relentless Context Propagation**: The most critical operational requirement for Tracing is unbroken Context Propagation (typically via the W3C `traceparent` HTTP header). If `Service A` initiates an asynchronous Kafka message to `Service B`, the application developer MUST explicitly extract the Trace Context from the incoming HTTP request and actively inject it into the Kafka Message Header. If this injection is missed, the Distributed Trace physically breaks into two orphaned, disconnected graphs, destroying visibility.
2. **Log & Trace Correlation (The Holy Grail)**: Traces visualize *Where* and *How Long*; Logs explain *Why*. To achieve hyper-efficient Root Cause Analysis, these two pillars must mathematically intersect. Your logging framework (e.g., Logback/Winston) must be configured to extract the current active `Trace_ID` and append it to every JSON log payload. In a modern UI like Datadog, clicking on a red, failing Span instantly pivots the view to display the precise, filtered text logs emitted by that specific thread during that exact microsecond.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lấy mẫu 100% (100% Sampling Rate - Cháy túi)**: Trace lưu trữ hàng tỷ cái Spans siêu nhỏ. Nếu hệ thống lớn có 10.000 req/s, mà bạn đòi Trace lại MỌI Request, bạn sẽ mất hàng triệu Đô-la tiền lưu trữ.
   - *Luật (Sampling)*: Chỉ cấu hình lưu lại 1% hoặc 5% số lượng Request ngẫu nhiên. Tracing dùng để tìm "Bức tranh tổng thể", không phải đi tìm từng hạt cát. (Lưu ý: Đối với các Trace bị lỗi 500, thì hệ thống thường đủ thông minh để giữ lại 100% để debug).
2. **Tự viết Tracing bằng tay**: Cố gắng viết các hàm tính toán `start_time` và `end_time` thủ công. Không ai làm thế cả. Hãy cài các Agent APM (Application Performance Monitoring) như của Datadog hoặc OpenTelemetry. Nó sẽ tự động tiêm ngầm vào Code (Bytecode instrumentation) và tự động tạo Span cho mọi câu lệnh SQL, Redis, HTTP mà không cần viết 1 dòng code nào.

</details>

1. **100% Sampling Rate (Financial Catastrophe)**: Retaining 100% of Distributed Traces for a high-throughput API (e.g., 50,000 requests/sec) will instantly overwhelm the OTel Collector, obliterate the Elasticsearch backend, and incur astronomical APM vendor costs. **The Fix**: You must configure **Probabilistic Sampling** (e.g., retaining only 5% of successful requests). For robust debugging, utilize **Tail-based Sampling**: The collector caches all spans in memory for 10 seconds. If the overarching Trace resulted in an `HTTP 500` or exceeded a `5000ms` latency threshold, the collector explicitly retains 100% of that specific Trace while discarding the healthy ones.
2. **Manual Instrumentation Hubris**: Junior developers attempt to manually create Spans by wrapping functions in `span.start()` and `span.finish()`. This pollutes the business logic and inevitably misses crucial DB driver context. **Rule**: Leverage Automatic Instrumentation exclusively. In Java/Node.js, APM agents (Datadog/OTel) utilize Bytecode Manipulation (Agent JVM args) to deeply monkey-patch standard libraries (HTTP/JDBC/Redis). They automatically emit pristine Traces for 95% of standard infrastructure operations without altering a single line of application code.

---

## Related Topics

- For the detailed text strings you see when you click a Trace, read **[Logging](./logging.md)**.
- For the high-level numbers that tell you to open the Trace UI, read **[Metrics](./metrics.md)**.
- For isolating these traced errors so they don't crash everything, read **[Resilience Overview](../resilience/overview.md)**.
