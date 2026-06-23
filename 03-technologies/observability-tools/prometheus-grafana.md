# Prometheus & Grafana

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu bạn muốn biết máy chủ của mình còn sống hay đã chết, CPU đang chạy bao nhiêu phần trăm, thì bộ đôi **Prometheus và Grafana** là tiêu chuẩn vàng miễn phí của thế giới mã nguồn mở. Chúng luôn đi thành một cặp bài trùng. 
> - **Prometheus** là Kẻ Thu Thập. Nó là một Database dạng Thời gian (Time-series Database). Cứ mỗi 15 giây, nó tự động gõ cửa hàng ngàn cái máy chủ của bạn để gom các con số thống kê (Metrics) đem về cất vào kho. Đồng thời nó có chức năng Báo động (Alertmanager) để hú còi khi có máy chủ sập.
> - **Grafana** là Họa Sĩ. Những con số trong kho của Prometheus rất khô khan và khó đọc. Grafana lấy những con số đó, vẽ ra những biểu đồ, đồng hồ đo cực kì đẹp mắt, đầy màu sắc, giúp Sếp của bạn nhìn vào là hiểu ngay hệ thống đang khỏe hay yếu.

</details>

> **Summary**: In the Cloud-Native ecosystem, **Prometheus** and **Grafana** are the undisputed open-source champions for Metrics monitoring and Alerting. They are almost exclusively deployed together as a symbiotic stack. 
> - **Prometheus** is the engine. Born at SoundCloud, it is a Time-Series Database (TSDB) equipped with a highly efficient "Pull-based" scraping mechanism and a powerful query language (PromQL). It constantly reaches out to your infrastructure, collects numeric metrics (e.g., CPU %, request latency), and stores them efficiently. It also includes the Alertmanager to trigger PagerDuty or Slack notifications when thresholds are breached.
> - **Grafana** is the visualization layer. While Prometheus stores the raw data, Grafana connects to Prometheus and renders that data into stunning, interactive, real-time dashboards. It democratizes Observability by allowing engineers and executives alike to visually comprehend the health of a massively distributed system at a glance.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn điều hành một chuỗi 100 Cửa hàng Tiện lợi.
1. **Prometheus (Ông Thanh tra)**: Bạn thuê một ông Thanh tra cực kì chăm chỉ. Cứ đúng 15 phút, ông Thanh tra này đạp xe đến từng cửa hàng (Pull-based), hỏi đúng 3 câu: *"Hôm nay bán được mấy lon nước? Nhiệt độ tủ lạnh là bao nhiêu? Có ai bị ốm không?"*. Ông ta ghi chép tất cả các con số đó vào một cuốn Sổ tay khổng lồ (Time-series Database). Nếu thấy tủ lạnh nóng hơn 10 độ, ông ta rút điện thoại gọi điện báo cảnh sát ngay lập tức (Alertmanager).
2. **Grafana (Bảng Điều khiển)**: Cuốn sổ tay của ông Thanh tra toàn là những con số chằng chịt, sếp không thể nào đọc hiểu nổi. Grafana là cái Tivi màn hình phẳng đặt trong phòng sếp. Nó đọc cuốn sổ tay đó, và vẽ lên Tivi một cái Bản đồ đỏ rực, một cái biểu đồ cột thể hiện doanh thu, và một cái đồng hồ đo nhiệt độ. Sếp chỉ cần nhâm nhi ly cà phê, nhìn lên Tivi là biết mọi thứ.

</details>

Imagine operating a fleet of 500 Delivery Trucks.
1. **Prometheus (The Data Logger)**: Every truck has sensors (speed, fuel, engine temp). Prometheus is a massive radio tower at headquarters. Every 10 seconds, it sends a signal to every single truck asking: *"Give me your current numbers."* (The Pull Model). It efficiently stores billions of these tiny numbers in a massive ledger. If it notices Truck #42's engine temp is over 120°C, it automatically sends an SMS to the mechanic (Alerting).
2. **Grafana (The Dashboard)**: Looking at a ledger of billions of numbers is useless to a human. Grafana is the massive glowing dashboard in the Dispatcher's office. It connects to the ledger and translates the raw numbers into beautiful speedometers, pie charts, and red/green traffic lights. It allows human operators to instantly spot that Truck #42 is broken.

---

## Layer 1: Core Concepts (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hệ thống hoạt động dựa trên 3 khái niệm:
1. **Mô hình Kéo (Pull Model)**: Đây là điểm độc đáo nhất của Prometheus. Ở các hệ thống khác (Push), các máy chủ tự động "Bắn" dữ liệu về trung tâm. Nếu 10.000 máy chủ cùng bắn 1 lúc, máy chủ trung tâm sẽ sập do quá tải (DDoS). Prometheus thì khác, nó tự chủ động đi "Kéo" (Pull) dữ liệu. Nó quy định: "Cứ 15s tao sẽ đi hỏi thăm tụi mày 1 lần". Nhờ vậy, Prometheus kiểm soát được hoàn toàn băng thông mạng và không bao giờ bị quá tải.
2. **Exporters (Máy phiên dịch)**: Prometheus chỉ hiểu một loại ngôn ngữ con số duy nhất. Nhưng máy chủ Linux, Database Postgres, Redis lại nói những ngôn ngữ khác nhau. **Exporter** là những đoạn code nhỏ xíu gắn vào các máy chủ đó, làm nhiệm vụ dịch các chỉ số của máy chủ sang ngôn ngữ của Prometheus để nó đến lấy.
3. **PromQL**: Ngôn ngữ truy vấn siêu mạnh. Bạn muốn biết: "Tỉ lệ phần trăm lỗi 500 của Web Server trong 5 phút qua chia cho tổng số lượng truy cập?". Chỉ cần gõ 1 dòng PromQL, nó sẽ tính toán trong 0.01 giây trên hàng tỷ con số.

</details>

The architecture is defined by its data collection model and querying capabilities:
1. **The Pull-Based Model**: This is Prometheus's most defining architectural choice. Legacy monitoring systems use a *Push* model (where 10,000 servers aggressively fire HTTP requests at the central monitoring server, often causing an internal DDoS during a massive outage). Prometheus uses a *Pull* model. Prometheus holds a registry of all active targets. Every 15 seconds, it systematically executes an HTTP GET request to the `/metrics` endpoint of every target. This ensures the central Prometheus server controls the ingestion rate and prevents network saturation.
2. **Exporters**: Prometheus only understands a specific plaintext metric format. An `Exporter` is a tiny sidecar binary deployed next to your application. E.g., The `node_exporter` translates Linux kernel metrics (CPU, RAM) into Prometheus format. The `postgres_exporter` executes SQL queries and translates the results (active connections, cache hits) into Prometheus format.
3. **PromQL (Prometheus Query Language)**: A highly specialized, Turing-incomplete functional query language designed explicitly for evaluating Time-Series data. It allows engineers to slice, dice, and mathematically aggregate metrics instantly. Example: calculating the per-second rate of HTTP 500 errors over the last 5 minutes: `rate(http_requests_total{status="500"}[5m])`.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi công ty dùng Kubernetes, hàng trăm Máy ảo (Pod) liên tục được đẻ ra và chết đi.
Làm sao hệ thống giám sát biết được IP của các máy ảo mới này để đi thu thập số liệu? Nếu cấu hình bằng tay thì con người không thể làm kịp.
Prometheus được sinh ra làm Vợ/Chồng hoàn hảo của Kubernetes. Nó có khả năng **Auto-Discovery (Tự động khám phá)**. Prometheus móc nối thẳng vào Não bộ của Kubernetes. Ngay cái giây phút K8s đẻ ra 1 cái Pod mới, Prometheus lập tức biết cái Pod đó IP là gì, và nó tự động chạy tới gõ cửa lấy dữ liệu. Mọi thứ tự động 100%.

</details>

Prometheus became the industry standard specifically because it perfectly complements the dynamic nature of Kubernetes.
In a static On-Premise environment, you configure your monitoring tool with a hardcoded list of IPs (`10.0.0.1`, `10.0.0.2`). In Kubernetes, 50 Pods spin up and die every minute; their IP addresses are completely ephemeral. A static configuration file is useless.
Prometheus natively integrates with the Kubernetes API via **Service Discovery**. The exact millisecond Kubernetes schedules a new Pod, Prometheus detects the API event, discovers the Pod's new internal IP address, dynamically adds it to its internal scraping target list, and begins pulling metrics. When the Pod dies, Prometheus silently stops scraping it without throwing false alarms. This dynamic auto-discovery makes it the only viable open-source metrics solution for Cloud-Native architectures.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình Báo động (Alerting) khi hệ thống bị đầy ổ cứng.
</details>

Visualizing Alerting and Visualization.

| Metric | Basic Cloud Monitoring (AWS CloudWatch) | Prometheus + Grafana |
|---|---|---|
| **Alerting Flexibility** | Set a basic alarm: "If CPU > 90% for 5 mins, send an email." | Use PromQL for predictive alerting: "If the hard drive fills up at the current rate, it will hit 100% in exactly 4 hours. Send a Slack message NOW so we can fix it before it crashes." |
| **Dashboards** | Ugly, basic line charts limited only to AWS metrics. | Beautiful, dark-mode, highly interactive Grafana dashboards integrating data from AWS, Kubernetes, Postgres, and custom App logic on a single pane of glass. |

---

## Layer 4: Common Architectures & Roles

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giám sát Hệ điều hành (Node Exporter)**: Công dụng cơ bản nhất. Bạn cài 1 cái app nhỏ (Node Exporter) lên mọi máy chủ Linux. Grafana sẽ vẽ ra cái màn hình cho sếp thấy: Máy nào đang full RAM, máy nào đang rớt mạng.
2. **Giám sát Ứng dụng (Application Metrics)**: Bạn đang viết code Node.js hoặc Spring Boot. Bạn dùng thư viện chèn thêm vài dòng code: "Cứ mỗi lần có người nhấn Mua Hàng, cộng con số này lên 1". Prometheus sẽ gom con số đó về, Grafana sẽ vẽ biểu đồ "Doanh thu theo thời gian thực".
3. **Alertmanager (Gửi tin nhắn chửi bới)**: Prometheus nhận ra có lỗi, nó đẩy tín hiệu sang Alertmanager. Alertmanager rất thông minh. Nếu 100 máy chủ cùng sập 1 lúc do đứt cáp mạng. Thay vì nó gửi 100 cái email làm cháy hộp thư của bạn, nó sẽ "Gom nhóm" (Grouping) lại thành đúng 1 cái Email duy nhất: *"Sếp ơi, nguyên cụm máy chủ chết rồi"*.

</details>

1. **Infrastructure Monitoring (`node_exporter`)**: The baseline implementation. You deploy `node_exporter` to every EC2 instance (or as a DaemonSet in Kubernetes). It exposes low-level OS metrics (CPU load, memory allocation, disk I/O, network throughput). Grafana consumes this to provide a global heat-map of your entire physical infrastructure health.
2. **Application-Level Instrumentation**: You embed Prometheus client libraries directly into your Java, Go, or Node.js application code. You define custom Counters (e.g., `total_checkouts_completed`) and Histograms (e.g., `http_request_duration_seconds`). This allows you to monitor deeply specific Business Logic, not just CPU charts.
3. **The Alertmanager**: Prometheus evaluates alert rules (e.g., "Is the API returning > 5% error rate?"). If true, it fires the alert to the Alertmanager. The Alertmanager handles Deduplication, Grouping, and Routing. If a core database goes down, it causes 50 microservices to throw cascading alerts. Instead of spamming the DevOps engineer with 5,000 separate SMS messages, Alertmanager logically groups them and sends exactly *one* PagerDuty notification indicating a widespread Database Outage.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Không dùng Prometheus để lưu Logs**: Prometheus là cái Máy tính bỏ túi, nó CHỈ BIẾT LƯU CON SỐ (1, 2, 3, 50.4). Nếu bạn cố ép nó lưu những câu chữ dài thòng (Ví dụ: "User A vừa đăng nhập lúc 3h chiều bằng IP 1.2.3.4"), nó sẽ bị "Tràn bộ nhớ" (Cardinality Explosion) và sập ngay lập tức. Những thứ bằng "Chữ" bắt buộc phải đem qua ELK Stack lưu.
2. **Dùng các Dashboard có sẵn của cộng đồng**: Grafana có một cái "Chợ" (Dashboard ID). Bạn không cần tự mài mò vẽ biểu đồ vẽ cái đồng hồ đo CPU mất cả tuần. Bạn chỉ cần lên web, copy mã ID "1860" (Node Exporter Full), dán vào Grafana. Bùm! Trong 1 giây bạn có 1 cái Dashboard tuyệt đẹp đầy đủ mọi chỉ số giống hệt các công ty công nghệ lớn.

</details>

1. **Beware Cardinality Explosion (Do Not Store Logs as Labels)**: The most fatal mistake in Prometheus instrumentation. Prometheus is highly optimized for storing numbers. It indexes Time-Series by their "Labels". If you create a metric `http_requests_total{status="200", user_id="12345"}`, Prometheus creates a unique time-series array in RAM for *every single unique User ID*. If you have 5 million users, Prometheus instantly exhausts its RAM and crashes violently. **Rule**: Labels must have low cardinality (e.g., `status_code`, `http_method`). Never put high-cardinality data (User IDs, Email Addresses, raw Log messages) into Prometheus. Use an ELK stack for that.
2. **Leverage Community Grafana Dashboards**: Building a highly optimized, visually dense Grafana dashboard from scratch requires deep PromQL expertise. **Rule**: Do not reinvent the wheel. The Grafana website hosts thousands of community-vetted Dashboard JSON templates. You simply import Dashboard ID `1860` (Node Exporter Full) or `315` (Kubernetes Cluster), and instantly possess an enterprise-grade monitoring screen that would have taken weeks to build manually.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Prometheus rất mau quên (Không dùng để lưu trữ lâu dài)**: Prometheus lưu dữ liệu trên Ổ cứng thật cục bộ. Thiết kế mặc định của nó chỉ cho phép lưu con số trong 15 ngày. Qua ngày 16 nó xóa số cũ đi. Nó KHÔNG PHẢI là chỗ để bạn lưu trữ dữ liệu doanh thu của cả năm. Nếu muốn lưu dữ liệu nhiều năm, bạn phải gắn Prometheus vào các hệ thống bên thứ ba khổng lồ (như Thanos hoặc Cortex).
2. **Cảnh báo rác (Alert Fatigue)**: Bạn cài cấu hình: "CPU vượt 70% thì gửi Zalo". Nửa đêm, máy chủ đang chạy Backup, CPU vọt lên 80% trong 2 phút rồi tự xuống. Điện thoại của bạn réo inh ỏi lúc 2h sáng. Bạn tỉnh dậy mệt mỏi, thấy chả có lỗi gì. Sau 1 tháng bị phá giấc ngủ vô ích, bạn bực mình TẮT LUÔN CÁI BÁO ĐỘNG. Tháng sau sập server thật, không ai biết.
   - *Luật*: Chỉ báo động những lỗi làm ảnh hưởng ĐẾN NGƯỜI DÙNG (Khách hàng không mua được hàng). Còn CPU cao thì cứ để mặc nó, khi nào vượt 95% liên tục trong 15 phút hẵng báo.

</details>

1. **Treating Prometheus as Long-Term Storage**: Prometheus is engineered for ultra-fast, short-term Operational intelligence. It uses a local append-only database. By default, it aggressively deletes data older than 15 days to conserve disk space. It is inherently NOT highly-available (running two Prometheuses just means two separate, disjointed databases). **Rule**: If your business requires storing metrics for 5 years for compliance auditing, you cannot rely purely on Prometheus. You must integrate it with a Remote Storage backend designed for infinite scaling, such as **Thanos** or **Cortex**, which archive the Prometheus data into AWS S3 buckets globally.
2. **Alert Fatigue (The "Boy Who Cried Wolf" Syndrome)**: The psychological destroyer of DevOps teams. If you configure alerts based on arbitrary system thresholds (e.g., "Alert if CPU > 80%"), you will receive hundreds of meaningless PagerDuty calls during normal operational spikes. Engineers will learn to actively ignore the alerts. When a real outage occurs, it gets ignored. **Rule**: Alert purely on **Symptoms (User Impact)**, not Causes. Alert when the "HTTP Error Rate > 5%", or "Checkout Latency > 2s". Do not alert on "CPU > 80%". CPU is supposed to be used; as long as the user isn't seeing errors, let the CPU burn.

---

## Related Topics

- Prometheus exclusively handles numerical Metrics. For processing Text Logs, you must use the **[ELK Stack](./elk-stack.md)**.
- If you don't want to self-host Prometheus and Grafana, you can pay for the expensive, fully-managed SaaS alternative: **[Datadog](./datadog.md)**.
- Prometheus was explicitly designed to monitor workloads running on **[Kubernetes](../cloud-infra/kubernetes.md)**.
