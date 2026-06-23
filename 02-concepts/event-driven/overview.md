# Event-Driven Architecture Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Thay vì ra lệnh trực tiếp kiểu "Ê làm cái này đi", Hệ thống Hướng sự kiện (Event-Driven Architecture - EDA) hoạt động dựa trên việc "Thông báo những gì đã xảy ra". Khi một sự việc xảy ra (Khách hàng bấm Đặt hàng), hệ thống tạo ra một Sự kiện (Event) và phát loa thông báo cho toàn công ty. Ai cần biết thì tự nghe và tự làm việc của mình. Kiến trúc này giúp các thành phần tách rời nhau hoàn toàn (Decoupled), dễ dàng thêm tính năng mới, và cực kỳ phù hợp với hệ thống Microservices hiện đại.

</details>

> **Summary**: Traditional Request-Driven architectures rely on explicit Command patterns ("Do this action"). This inevitably creates tight coupling and orchestrated bottlenecks. **Event-Driven Architecture (EDA)** fundamentally inverts this paradigm. It operates on Choreography. When a state mutation occurs, the system simply emits an immutable **Event** ("This fact just happened"). Downstream systems autonomously subscribe to these events and react independently. EDA enforces extreme Decoupling, promotes massive horizontal scalability, and is the definitive architectural pattern for modern, complex Microservice ecosystems.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang điều hành một Nhà hàng.
1. **Kiểu Ra lệnh (Request-Driven)**: Khách gọi món. Người Phục vụ phải chạy vào bếp hét: "Nấu bò bít tết đi!". Xong chạy sang quầy Bar hét: "Pha rượu đi!". Xong chạy ra bãi xe hét: "Chuẩn bị xe cho khách đi!". Phục vụ phải biết và quản lý TẤT CẢ mọi việc (Quá mệt và dễ lỗi).
2. **Kiểu Hướng sự kiện (Event-Driven)**: Khách gọi món. Người Phục vụ đi ra giữa nhà hàng, lấy một cái chuông bấm Kính Koong, và nói đúng 1 câu: "Sự kiện: Bàn số 5 đã gọi Bò bít tết và Rượu". Xong! Phục vụ đi làm việc khác. Đầu bếp nghe thấy tiếng chuông, tự động nấu bò. Bartender nghe thấy, tự động pha rượu. Người trông xe chả quan tâm món bò bít tết, phớt lờ tiếng chuông.

</details>

Imagine operating a massive Warehouse.
1. **Request-Driven (Orchestration)**: A Manager receives a box. He explicitly commands Bob: "Take this to aisle 5". Then he commands Alice: "Update the inventory spreadsheet". Then he commands Charlie: "Send a receipt to the vendor". The Manager must know exactly who everyone is and micromanage every single step. If Alice goes on vacation, the Manager crashes.
2. **Event-Driven (Choreography)**: A Manager receives a box. He places it on a glowing red pedestal and shouts: "EVENT: Box Received!". He walks away. Bob is trained to move boxes from red pedestals, so he takes it. Alice is trained to listen for the shout, so she updates the spreadsheet. Charlie ignores it entirely. If you want to add a new Security Guard tomorrow, you don't need to teach the Manager anything; the Guard simply listens for the shout.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Ba thành phần cốt lõi của Kiến trúc Hướng sự kiện:
1. **Event (Sự kiện)**: Là một sự thật đã xảy ra trong quá khứ. Đã là quá khứ thì KHÔNG THỂ THAY ĐỔI (Immutable). Ví dụ: `Order_Created`, `User_Registered`. Chú ý: Đặt tên bằng thì Quá khứ.
2. **Event Producer (Nơi phát sự kiện)**: Dịch vụ tạo ra sự kiện và ném nó vào một cái Ống truyền tin (Message Broker). Nó ném xong là xong, KHÔNG BAO GIỜ chờ xem có ai nhận hay chưa.
3. **Event Consumer (Nơi tiêu thụ sự kiện)**: Dịch vụ ngồi chầu chực ở Ống truyền tin. Thấy sự kiện mình quan tâm trôi ngang qua là bốc lấy và xử lý logic nội bộ của mình.

</details>

EDA architecture consists of three structural pillars:
1. **The Event (The Immutable Fact)**: A serialized payload (JSON/Protobuf) representing a specific state mutation that has definitively occurred in the past. Because it is a historical fact, it is strictly **Immutable**. Conventionally named in the past tense (e.g., `Invoice_Paid`, `Item_Shipped`).
2. **The Event Producer (Publisher)**: The upstream service that experiences the state change. It fires the Event into the Event Router (Broker) and immediately returns. It has absolutely zero knowledge of who, if anyone, will consume the event.
3. **The Event Consumer (Subscriber)**: The downstream service that independently binds to the Event Router. It filters for specific Events, consumes them, and executes its isolated business domain logic (e.g., sending an email or updating a search index) autonomously.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Giải phóng Nút thắt cổ chai (Bottlenecks)**
Kiến trúc Microservices kiểu cũ hay dùng HTTP REST để gọi chéo nhau. A gọi B, B gọi C, C gọi D. Nếu D sập, C bị treo, kéo theo B treo, và cuối cùng toàn bộ hệ thống tê liệt. Với Event-Driven, A chỉ cần thảy một Event ra chợ rồi quay lưng đi làm việc khác. A không bao giờ bị treo chờ ai cả.
**2. Khả năng Mở rộng (Extensibility) vô tận**
Khi công ty thêm một phòng ban mới (Ví dụ: Đội AI Phân tích dữ liệu). Đội AI cần dữ liệu Đặt hàng. Với kiến trúc cũ, bạn phải vào code của Service Đặt Hàng, viết thêm API đẩy data sang Đội AI. Rất dễ sinh Bug. Với Event-Driven, Đội AI tự động "Cắm ống hút" vào kênh `Order_Created` để hút dữ liệu về phân tích. Code của Service Đặt Hàng không bị đụng tới một dòng nào.

</details>

**1. Eradicating Temporal Coupling (Cascading Failures)**
In strict Request-Driven Microservices (using HTTP/gRPC), services are temporally coupled. If Service A synchronously calls Service B, and B is down, Service A blocks, timeouts, and fails. This creates a brittle, tightly-coupled distributed monolith. EDA completely decouples services in Time. Service A publishes an Event and succeeds instantly. If Service B is offline, the Event sits safely in the Broker. When Service B reboots, it processes the backlog. The system achieves infinite fault isolation.
**2. Infinite Domain Extensibility (The Open/Closed Principle)**
Consider adding a new `FraudDetectionService` to an existing E-commerce pipeline. In a Request-Driven architecture, you must manually modify the core `CheckoutService` to explicitly invoke the new Fraud API, requiring dangerous code changes, recompilation, and redeployment of mission-critical systems. In an EDA architecture, the `CheckoutService` remains 100% untouched. The new `FraudDetectionService` simply subscribes to the existing `Order_Placed` event stream. The architecture conforms perfectly to the SOLID Open/Closed Principle.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh luồng tạo Tài khoản mới trên Hệ thống.
</details>

Visualizing the workflow of User Registration across domains.

| Action | Request-Driven (Orchestration) | Event-Driven (Choreography) |
|---|---|---|
| **Initiation** | `UserService` saves User to DB. | `UserService` saves User to DB. |
| **Step 1** | `UserService` calls `EmailAPI.send()`. | `UserService` emits `User_Registered` Event. |
| **Step 2** | `UserService` calls `PromoAPI.create()`. | `EmailService` hears Event $\rightarrow$ Sends Email. |
| **Step 3** | `UserService` calls `AnalyticsAPI.log()`. | `PromoService` hears Event $\rightarrow$ Creates Code. |
| **Code Dependency**| `UserService` must know URLs of 3 other APIs.| `UserService` knows absolutely nothing. |
| **Latency** | **Very High** (Waits for all 3 to finish). | **Zero** (Returns instantly after DB save). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hệ thống E-commerce đa bộ phận**: Một nút "Thanh toán" làm nổ ra hàng tá sự kiện ở các Service khác nhau (Kho, Kế toán, Vận chuyển, Chăm sóc khách hàng). Tất cả nhảy vào xử lý song song nhờ lắng nghe Event.
2. **Đồng bộ hóa Dữ liệu (Data Replication)**: Thay vì mỗi đêm chạy Cronjob Copy cái Database nặng 1TB sang máy chủ Dự phòng. Người ta dùng EDA. Bất cứ khi nào DB chính có 1 lệnh `Insert/Update`, nó sinh ra một Event. DB phụ bắt lấy Event đó và Update y chang (Change Data Capture - CDC). Dữ liệu đồng bộ gần như tức thời (Realtime).
3. **Internet of Things (IoT)**: 10.000 cái Nhiệt kế cứ 1 giây lại gửi nhiệt độ (Event) về trung tâm. Trung tâm không ra lệnh gì cho Nhiệt kế cả, chỉ im lặng hứng Event để vẽ biểu đồ và Cảnh báo cháy.

</details>

1. **E-commerce Domain Choreography**: The textbook example. Clicking "Complete Checkout" publishes an `Order_Paid` event. The `InventoryDomain` deducts stock. The `FulfillmentDomain` prints a shipping label. The `LoyaltyDomain` awards VIP points. All executed perfectly in parallel, decoupled domains.
2. **Real-Time Data Replication & Search Indexing**: A monolithic database performs poorly for text-searching. You need Elasticsearch. Instead of writing slow Cron batch jobs to sync the DB to Elasticsearch, you implement CDC (Change Data Capture). Every row mutation in PostgreSQL instantly fires a `Row_Updated` Event via Debezium. An Elasticsearch worker consumes the Event and updates the search index instantly.
3. **Massive IoT Telemetry Pipelines**: 100,000 smart meters transmitting kilowatt usage every 5 minutes. The meters are purely Event Producers. They fire generic `Meter_Reading` events into an MQTT broker and sleep. Downstream Big Data pipelines ingest these events to calculate regional power grids.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Đính kèm đủ Dữ liệu (Event-Carried State Transfer)**: Khi gửi Event `Order_Created`, đừng chỉ gửi mỗi cái `{ "order_id": 123 }`. Service Email nhận được ID 123, nó lại phải vòng ngược lại gọi API của Service Đặt Hàng để hỏi: "123 là của ai? Mua cái gì?". Việc này phá vỡ hoàn toàn lợi ích của Event. Hãy nhét đầy đủ thông tin vào Event: `{ "id": 123, "email": "a@b.com", "total": 500 }`. Service Email có đủ đồ nghề để làm việc luôn.
2. **Thiết kế Idempotency (Bắt buộc)**: Vì Event bắn qua mạng nên Broker có thể gửi trùng 1 Event thành 2 lần (At-Least-Once Delivery). Code của Consumer phải kiểm tra Database xem Event ID này đã xử lý chưa, để tránh việc gửi 2 cái Email chúc mừng cho cùng 1 người.

</details>

1. **Event-Carried State Transfer**: A catastrophic architectural mistake is publishing "Thin Events" containing only identifiers (e.g., `{"event": "User_Updated", "user_id": 99}`). When the 5 downstream Consumers receive this, they all instantly fire synchronous HTTP `GET` requests back to the `UserService` to fetch the actual User data. This accidentally DDoSes the `UserService` and re-introduces tight coupling. **Rule**: Publish "Fat Events". Include all contextual state required for the consumer to act (e.g., `{"user_id": 99, "new_email": "john@x.com", "plan": "PRO"}`).
2. **Absolute Requirement: Idempotency**: Distributed message brokers guarantee *At-Least-Once* delivery. Inevitably, due to network timeouts or client crashes, a Consumer *will* receive the exact same Event twice. If your Consumer logic is not Idempotent, you will charge the customer's credit card twice. Always maintain an `Idempotency_Key` (e.g., the Event ID) in a database table to safely ignore duplicate events.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lạc mất dòng chảy (Loss of Traceability)**: Trong kiểu gọi API cũ, A gọi B gọi C, đọc Log một phát là ra hết luồng chạy. Trong EDA, A vứt Event ra chợ rồi đi ngủ. B bốc Event lên làm. C bốc Event lên làm. Nếu hệ thống xảy ra lỗi, bạn không thể biết sự kiện bắt đầu từ đâu và kết thúc ở đâu. 
   - *Cách giải quyết*: Phải dùng **Distributed Tracing (Truy vết phân tán)** như Jaeger hoặc Zipkin. Gắn một cái `Trace_ID` (Mã số dán nhãn) vào Event đầu tiên, và truyền cái ID đó xuyên qua tất cả các Broker và Consumer để nối chúng lại thành một câu chuyện hoàn chỉnh.
2. **Ngộ nhận Sự nhất quán (Eventual Consistency Phobia)**: Trong EDA, sau khi Đặt hàng xong, tiền sẽ chưa được cộng ngay cho Người bán. Sẽ có một khoảng trễ vài giây để Event trôi trong mạng. Nhiều sếp khó tính không chấp nhận việc "Vừa F5 chưa thấy tiền cập nhật", bắt Lập trình viên phải dùng Database chung (Khóa DB). Nếu đã chấp nhận dùng Event-Driven, phải thay đổi tư duy sang **Tính Nhất Quán Tạm Thời (Eventual Consistency)**.

</details>

1. **The Distributed Spaghetti (Loss of Traceability)**: The greatest nightmare of EDA. In a Monolith, you have a beautiful, linear Stack Trace. In EDA, an Event bounces asynchronously across 10 Microservices and 3 Kafka Topics. If a bug occurs at Service 8, trying to trace *why* it happened or *who* initiated the flow is nearly impossible using raw text logs. **Fix**: You MUST implement robust **Distributed Tracing** (OpenTelemetry, Jaeger). Every Event must carry a globally unique `Correlation_ID` in its metadata headers, allowing observability tools to visualize the entire asynchronous, scattered workflow as a single, coherent timeline.
2. **Failing to Embrace Eventual Consistency**: EDA fundamentally destroys immediate ACID consistency. When a user updates their Profile Picture, the `Image_Uploaded` event takes 500ms to propagate to the `CommentService`. If the user instantly refreshes the page, their old comments might still show the old picture. Junior developers panic and try to introduce synchronous locks over the Event Bus to "fix" this. **Rule**: Stop fighting physics. Educate the Product/Business teams. Design the UI to mask the propagation delay (e.g., Optimistic UI Updates). Embrace Eventual Consistency.

---

## Related Topics

- For how to actually transport these events securely, see **[Messaging Patterns](../messaging/patterns.md)**.
- For a specific, radical form of Event-Driven design, see **[Event Sourcing](./event-sourcing.md)**.
- For splitting Reads from Writes using Events, see **[CQRS](./cqrs.md)**.
