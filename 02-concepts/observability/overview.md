# Observability Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu bạn lái ô tô ban đêm mà bị mù, tắt đèn pha, và che luôn đồng hồ tốc độ, bạn chắc chắn sẽ lao xuống vực. **Observability (Khả năng quan sát)** chính là hệ thống Đèn pha và Đồng hồ đo lường của Hệ thống phần mềm. Khi bạn có 1 cái Server, bạn dùng lệnh `console.log` để tìm lỗi. Khi bạn có 1000 cái Microservices chạy ẩn trên Cloud, bạn không thể SSH vào từng cái để đọc log được. Observability giúp Kỹ sư nhìn thấu được "sức khỏe" và "vấn đề" của toàn bộ hệ thống ngay từ bên ngoài, thông qua 3 Trụ cột: **Logs, Metrics, và Traces**.

</details>

> **Summary**: Operating a distributed microservice architecture without robust Observability is equivalent to flying a commercial airliner blindfolded. When an HTTP `500` error occurs randomly across a 50-node Kubernetes cluster, relying on manual SSH and localized `tail -f` log inspection is impossible. **Observability (O11y)** is the architectural property of a system that allows engineers to understand its internal state strictly from its external outputs. It transforms a black-box architecture into a transparent, debuggable entity. Achieving true Observability requires the instrumentation and aggregation of the **Three Pillars: Metrics (Is there a problem?), Logs (What is the exact problem?), and Traces (Where did the problem happen?).**

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang điều hành một Bệnh viện lớn.
1. **Thiếu Observability**: Một bệnh nhân (Request) kêu đau bụng. Bác sĩ (Kỹ sư) không có ống nghe, không có máy X-Quang, không có máy đo huyết áp. Bác sĩ đành mổ banh bụng bệnh nhân ra để tìm xem ruột thừa nằm ở đâu. (Mất thời gian, hệ thống có thể chết trước khi tìm ra bệnh).
2. **Có Observability**: Bệnh nhân vừa bước vào, Bác sĩ nhìn lên màn hình:
   - **Metrics (Nhịp tim)**: Máy báo nhịp tim đập 150 lần/phút (Hệ thống báo động đỏ CPU 100%). Bác sĩ biết ngay CÓ VẤN ĐỀ.
   - **Traces (Đường đi)**: Camera an ninh ghi lại: Bệnh nhân ăn hải sản ở cổng $\rightarrow$ Đi vào thang máy $\rightarrow$ Ôm bụng ở lầu 3. Bác sĩ biết ngay VẤN ĐỀ NẰM Ở ĐÂU.
   - **Logs (Chi tiết)**: Bác sĩ giở hồ sơ bệnh án đọc dòng chữ: "Dị ứng tôm sú". Bác sĩ biết CHÍNH XÁC NGUYÊN NHÂN. Chữa bệnh chỉ trong 1 phút.

</details>

Imagine diagnosing a completely broken Car engine.
1. **Without Observability**: You open the hood. It's a solid block of metal. You have no dashboard, no check engine light, and no temperature gauge. The only way to find the broken spark plug is to physically disassemble the entire engine, piece by piece. (Debugging in Production without tools).
2. **With Observability**: You sit in the driver's seat. 
   - **Metrics (The Dashboard)**: The Temperature gauge is in the Red Zone. You instantly know *SOMETHING IS WRONG*.
   - **Traces (The OBD2 Scanner)**: You plug in a computer. It traces the electrical signal and tells you: The fault is in Cylinder #4. You instantly know *WHERE IT IS WRONG*.
   - **Logs (The Mechanic's Notes)**: You pull the log file from the car's computer. It says: "Cylinder 4 Misfire due to lack of fuel pressure at 14:03:00". You instantly know *WHY IT IS WRONG*.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Observability không phải là một "công cụ" (Ví dụ: Không phải tải Grafana về cài là xong). Nó là văn hóa viết Code. Một hệ thống O11y hoàn chỉnh phải phát ra 3 loại dữ liệu (The Three Pillars):
1. **Metrics (Chỉ số)**: Các con số tổng quát để vẽ Biểu đồ. Ví dụ: `CPU = 80%`, `Memory = 2GB`, `Lỗi 500 = 50 req/s`. Rất nhẹ, dùng để bắn Còi Báo Động (Alerting).
2. **Logs (Nhật ký)**: Các dòng chữ mô tả chi tiết 1 sự kiện. Ví dụ: `[ERROR] User 123 sai mật khẩu tại hàm Login`. Rất nặng, tốn nhiều ổ cứng, dùng để đọc chi tiết lúc sửa lỗi.
3. **Traces (Dấu vết)**: Sợi dây liên kết. Nếu 1 Request đi qua 5 Microservices (Web $\rightarrow$ Auth $\rightarrow$ Order $\rightarrow$ Payment $\rightarrow$ DB). Trace sẽ xâu chuỗi 5 bước đó lại thành 1 cái Waterfall (Thác nước) để xem thằng nào làm chậm cả đội.

</details>

Observability is not a vendor product you can simply install; it is a fundamental property of the codebase. A highly observable system is explicitly instrumented to emit the **Three Pillars of Telemetry**:
1. **Metrics (The Aggregates)**: Numeric representations of data measured over time intervals. Extremely lightweight. Examples: `HTTP 500 Rate: 12/sec`, `CPU Utilization: 88%`, `DB Query Latency p99: 45ms`. Used strictly for Dashboards and automated Alerting (PagerDuty).
2. **Logs (The Events)**: Immutable, timestamped, verbose text records of discrete events. Examples: `[ERROR] 2023-10-01 14:00:00 NullPointerException at CheckoutController:45`. Highly storage-intensive. Used for deep forensic analysis after an alert fires.
3. **Traces (The Causality)**: A representation of a single request's journey across an arbitrary number of distributed microservices. It links the logs from the `Gateway` to the `OrderService` to the `PaymentService` into a single, cohesive Flame Graph, exposing exactly which service caused the 5-second latency spike.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Ngày xưa, khi làm web Monolithic (1 cục to đùng). Lỗi xảy ra, Lập trình viên chỉ cần mở file `error.log` trên máy chủ đó ra đọc là xong.
Nhưng khi chuyển sang Microservices hoặc Serverless. Một cái click chuột của người dùng kích hoạt 20 cái API chạy trên 20 máy chủ khác nhau. Lúc này, file `error.log` nằm ở máy số 17. Làm sao bạn biết phải SSH vào máy số 17 mà tìm? Và làm sao bạn biết cái lỗi ở máy số 17 lại là nguyên nhân làm máy số 1 bị chậm?
Sự phân mảnh (Fragmentation) này tạo ra "Vùng mù" cực lớn. Observability sinh ra để hút toàn bộ dữ liệu từ 20 máy chủ đó, gom chung về 1 màn hình duy nhất. Giúp Kỹ sư nhìn xuyên thấu hệ thống từ trên cao.

</details>

In a legacy Monolithic architecture, Observability was trivial. If the application crashed, the developer SSH'd into the single Linux server, ran `tail -f /var/log/application.log`, and read the stack trace.
The migration to Microservices, Kubernetes, and Serverless architectures destroyed this paradigm. A single User Checkout action now traverses an API Gateway, an Auth Lambda, an Order Container, a Payment Container, an Event Bus, and an Inventory Container.
If the Checkout process is "slow", you cannot SSH into 6 different ephemeral containers simultaneously. Furthermore, the root cause might be a noisy neighbor in the Event Bus, completely invisible to the Order Container's logs. Distributed architectures introduce catastrophic **Blind Spots**. Observability exists to centralize, correlate, and index telemetry from highly fragmented infrastructure into a single Pane of Glass (e.g., Datadog, New Relic).

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cảnh tượng 2h sáng, Giám đốc gọi: "Web đang sập, khách hàng không thanh toán được!"
</details>

Visualizing a 2:00 AM Outage (Mean Time To Resolution - MTTR).

| Action Phase | Without Observability (Blind) | With Observability (O11y) |
|---|---|---|
| **1. Detection** | Customer complains on Twitter. CEO calls you. (Takes 30 mins to notice). | Grafana Metric drops. Automated PagerDuty alarm wakes you up. (Takes 1 min). |
| **2. Triage** | You randomly check 5 different servers trying to find errors. | Trace graph instantly highlights `PaymentService` is returning `503`. |
| **3. Diagnosis** | You grep through gigabytes of raw text logs. | You click the Trace, it shows the exact Log: `Redis Connection Timeout`. |
| **MTTR** | **3 to 5 Hours.** | **5 Minutes.** |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bộ Đôi ELK (Elasticsearch, Logstash, Kibana)**: Đây là huyền thoại trong làng Gom Logs. Mọi máy chủ đều gắn 1 cái vòi (Logstash), hút chữ từ các file Log đẩy về kho trung tâm (Elasticsearch). Sau đó dùng Kibana để gõ lệnh tìm kiếm `error AND payment` siêu nhanh trên toàn bộ hệ thống.
2. **Prometheus & Grafana (Vua của Biểu đồ)**: Chuyên dùng cho Metrics. Prometheus 5 giây 1 lần sẽ chạy đi hỏi các Server: "CPU mày bao nhiêu? RAM bao nhiêu?". Rồi nó đưa số liệu cho Grafana vẽ thành những cái biểu đồ màu sắc xanh đỏ nhấp nháy trên màn hình Tivi lớn trong phòng làm việc.
3. **Datadog / New Relic (Nhà giàu)**: Nếu công ty bạn giàu, bạn không cần tự cài đặt ELK hay Prometheus cho khổ. Bạn mua Datadog. Trả tiền hàng tháng. Nó gom đủ cả 3 trụ cột (Logs, Metrics, Traces) vào 1 màn hình cực xịn. Cứu rỗi hàng ngàn giờ làm việc của kỹ sư.

</details>

1. **The ELK Stack (Logs)**: The industry standard open-source log aggregation pipeline. Application nodes run lightweight forwarders (Filebeat/Logstash) that constantly tail local `.log` files and stream the text across the network into **Elasticsearch**. Engineers use the **Kibana** UI to execute complex Lucene queries (e.g., `level: ERROR AND service: checkout`) across the entire global cluster in milliseconds.
2. **Prometheus + Grafana (Metrics)**: The CNCF standard for cloud-native metrics. Applications expose a `/metrics` HTTP endpoint. **Prometheus** (the scraper) visits this endpoint every 15 seconds, pulling numerical data (e.g., Memory usage) into its Time-Series Database. **Grafana** connects to Prometheus to render beautiful, real-time dashboard visualizations and evaluate Alerting thresholds.
3. **Commercial APM Vendors (Datadog / New Relic)**: Application Performance Monitoring (APM) SaaS. For enterprise budgets, managing ELK and Prometheus is a massive operational burden. Datadog provides a proprietary agent that automatically injects itself into your Java/Node.js bytecode, instantly extracting Logs, Metrics, and Distributed Traces with zero code changes, unifying them in a deeply correlated, magical UI.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cấu trúc hóa Log (Structured Logging)**: Tội ác lớn nhất là in Log bằng câu văn: `console.log("User 123 login failed because of wrong password")`. Máy tính không hiểu câu văn. Bạn không thể tìm kiếm hay đếm số lượng lỗi bằng câu văn. Bắt buộc phải in Log dưới dạng JSON: `{"event": "login_fail", "user_id": 123, "reason": "wrong_password"}`. Elasticsearch sẽ đọc và phân tích JSON cực kỳ hoàn hảo.
2. **Dùng ID Theo Dõi (Correlation ID)**: Chìa khóa của Tracing. Khi người dùng bấm nút Mua, ngay ở cánh cửa đầu tiên (API Gateway), hãy tạo ra 1 cái ID duy nhất (Ví dụ: `Req_999`). Truyền cái `Req_999` này đi qua XUYÊN SUỐT 5 cái Microservices tiếp theo ở trong HTTP Header. Bất cứ service nào in Log cũng phải kẹp cái `Req_999` này vào. Khi có lỗi, bạn chỉ cần gõ `Req_999` vào thanh tìm kiếm, toàn bộ đường đi của Request đó sẽ hiện ra.

</details>

1. **Mandatory Structured Logging**: The most widespread Observability anti-pattern is logging unstructured prose (e.g., `logger.error("Failed to charge user 456 for item 789")`). This requires brittle Regex parsing in the log aggregator. Codebases MUST output logs entirely in JSON format: `{"level":"error", "action":"charge", "user_id":456, "item_id":789}`. This allows Elasticsearch to index every field dynamically, enabling hyper-fast analytical queries like `SELECT count(*) WHERE action='charge' AND level='error'`.
2. **Global Correlation IDs (Distributed Tracing)**: The absolute linchpin of microservice debugging. When a request hits the Edge Gateway, the Gateway must generate a cryptographically unique UUID (e.g., `X-Correlation-ID: 123e45`). This HTTP Header MUST be meticulously propagated downward to every subsequent internal gRPC/HTTP call. Every single log statement written by any service MUST append this ID. During an outage, searching for `123e45` in Datadog instantly reconstructs the precise chronological path of that exact user's request across the entire distributed network.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Đội giá tiền mây (Log Spam & Billing)**: Lập trình viên lười biếng, rải `console.log()` khắp mọi nơi, in cả mã Base64 của tấm ảnh ra Log. Hậu quả là 1 ngày hệ thống sinh ra 500GB Log rác. Khi đẩy 500GB này lên Datadog, cuối tháng công ty nhận hóa đơn 100.000$ (Tiền lưu trữ Log đắt hơn cả tiền chạy Server).
   - *Luật*: Phải có công tắc `Log Level` (INFO, DEBUG, ERROR). Trên môi trường Production CHỈ ĐƯỢC PHÉP in `ERROR` và `WARN`.
2. **Cảnh báo rác (Alert Fatigue)**: Đặt luật "Cứ có lỗi 500 là gửi tin nhắn SMS báo động cho Kỹ sư". Lúc hệ thống chạy, có vài người dùng nghịch ngợm gửi data sai, văng lỗi 500 (Thực ra chả ảnh hưởng gì). Điện thoại kỹ sư reo liên tục 50 lần 1 ngày. Dần dần, Kỹ sư bị "Tắt thông báo" hoặc "Lờ đi". Đến lúc Server bốc cháy thật, Kỹ sư cũng tưởng là báo rác nên cứ ngủ tiếp. (Chỉ nên đặt Alert cho những lỗi Đe dọa Doanh thu).

</details>

1. **Telemetry Hyper-Inflation (The Billing Trap)**: A junior developer enables `DEBUG` logging in Production or logs massive JSON payloads (e.g., Base64 images). The microservice cluster generates 2 Terabytes of Logs per day. Cloud APM vendors (Datadog/Splunk) charge violently for ingestion bandwidth and indexing storage. The Observability bill quickly eclipses the EC2 compute bill. **Fix**: Strictly enforce Log Levels. Production environments must default to `WARN` or `ERROR`. Implement Log Sampling (e.g., only tracing 10% of successful `GET` requests) to drastically curtail ingestion volume.
2. **Alert Fatigue (The Boy Who Cried Wolf)**: An eager Operations team configures PagerDuty to page the on-call engineer every time CPU hits 80% or a single HTTP 500 occurs. The engineer receives 40 pages a week for transient, self-healing issues that require no human intervention. The engineer develops "Alert Fatigue" and begins subconsciously ignoring the pager. When the Database actually suffers a catastrophic failure, the alert is ignored, and the system burns. **Rule**: Alerts must be strictly actionable. Only page a human if a critical SLI (Service Level Indicator) threatens the business SLA and requires manual engineering intervention.

---

## Related Topics

- For deep dives into the 3 pillars, read: **[Logging](./logging.md)**, **[Metrics](./metrics.md)**, and **[Tracing](./tracing.md)**.
- For how observing traffic helps stop bad actors, review **[Rate Limiting](../scalability/rate-limiting.md)**.
