# Datadog

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu hệ thống Open-Source (Prometheus, ELK) là việc bạn tự mua gạch, xi măng về xây nhà, thì **Datadog** là việc bạn bỏ tiền tỷ ra thuê một Khách sạn 5 sao có sẵn mọi dịch vụ. Datadog là nền tảng Quan sát (Observability) dạng SaaS (Phần mềm dịch vụ) lớn nhất và mạnh nhất thế giới hiện nay. Bạn không cần phải cài đặt máy chủ Database, không cần thiết kế biểu đồ. Bạn chỉ việc cài đúng 1 phần mềm cực nhẹ (Datadog Agent) vào máy chủ của công ty. Ngay lập tức, nó tự động hút toàn bộ Logs, Metrics, và Traces gửi lên máy chủ của Datadog. Mở trình duyệt web lên, Datadog đã tự động vẽ sẵn hàng trăm biểu đồ tuyệt đẹp, tự động phát hiện Database nào đang chạy chậm bằng Trí Tuệ Nhân Tạo (AI). Nó là một "Phép màu" làm mù mắt giới DevOps vì quá xịn xò, nhưng cái giá phải trả (Hóa đơn hàng tháng) thì vô cùng đắt đỏ, có thể lên tới hàng triệu đô la một năm đối với các tập đoàn lớn.

</details>

> **Summary**: While the open-source Observability stack (Prometheus, ELK, Jaeger) offers incredible flexibility with zero licensing costs, it demands massive engineering effort to deploy, scale, and maintain. **Datadog** represents the absolute pinnacle of Enterprise SaaS Observability. It operates on a radically simplified premise: You deploy a single, unified Agent (written in Go) to your servers or Kubernetes clusters. This Agent auto-discovers your infrastructure (identifying if a container is running Postgres, Redis, or Node.js) and instantly streams Logs, Metrics, and Distributed Traces to Datadog's secure cloud platform. Datadog provides Out-Of-The-Box (OOTB) dashboards, machine-learning-driven anomaly detection (Watchdog), and seamless correlation across the Three Pillars of Observability. It transforms a fragmented monitoring strategy into a "Single Pane of Glass." However, this frictionless operational excellence comes at an astronomical financial cost.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn muốn lắp Hệ thống Camera An ninh cho một Tòa cao ốc.
1. **Open-Source (Tự làm)**: Bạn ra chợ mua 50 cái Camera, mua máy chủ lưu trữ, tự kéo dây điện, tự mua phần mềm ghép hình ảnh lại. Rất tốn công, camera thường xuyên đứt dây, nhưng chi phí rẻ.
2. **Datadog (Thuê dịch vụ Trọn gói 5 sao)**: Bạn gọi cho công ty an ninh xịn nhất thế giới. Họ cử người đến dán 1 miếng Cảm biến bằng ngón tay vào mỗi tầng lầu (Datadog Agent). Thế là xong phần việc của bạn! Bạn mở điện thoại lên, thấy toàn bộ hình ảnh 3D của tòa nhà. Hệ thống AI tự động phân tích: *"Có người lạ xâm nhập tầng 5"*, *"Nhiệt độ tầng 3 đang hơi nóng"*. Bạn nhàn nhã uống cà phê, nhưng cuối tháng nhận hóa đơn dịch vụ đắt đến mức chóng mặt.

</details>

Imagine outfitting a Modern Factory with sensors.
1. **The Open-Source Way (DIY)**: You buy sensors from different vendors. You hire an electrician to wire the temperature sensors to screen A (Prometheus), and the speed sensors to screen B (ELK). When a machine breaks, you must manually stare at both screens simultaneously to guess what happened.
2. **Datadog (The Smart Factory SaaS)**: You slap a single magical sticker (The Agent) onto every machine. The sticker magically figures out what the machine does. You open your laptop, and Datadog has already built a 3D hologram of the entire factory. A red laser points exactly at Machine 42, and an AI voice says: *"Machine 42 broke because the temperature spiked exactly when the speed dropped. Here is the exact part to replace."* It is pure magic, but you pay a massive premium subscription for it.

---

## Layer 1: Core Architecture (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Kiến trúc của Datadog cực kì đơn giản đối với người dùng, vì Datadog đã gánh hết phần khó:
1. **Datadog Agent**: Trái tim của hệ thống. Bạn cài cái Agent này lên máy chủ Ubuntu, hoặc ném nó vào cụm Kubernetes. Thằng Agent này cực kì khôn ngoan (Auto-Discovery). Nó tự rà quét trong máy chủ: *"À, có 1 cái Docker đang chạy Postgres, tao sẽ tự kết nối lấy số liệu. À, có 1 cái Docker chạy Nginx, tao sẽ tự lấy Log"*. Tất cả diễn ra tự động mà bạn không cần cấu hình bằng tay.
2. **Datadog APM (Application Performance Monitoring)**: Tính năng ăn tiền nhất. Bạn chèn 1 thư viện Datadog vào code Node.js của bạn. Ngay lập tức, Datadog vẽ ra một cái Bản đồ Mạng Nhện tuyệt đẹp. Nó cho bạn thấy: Yêu cầu của khách hàng đi từ Web Server $\rightarrow$ tốn 100ms $\rightarrow$ chui vào Database $\rightarrow$ tốn 500ms. Sếp nhìn vào bản đồ là biết ngay thằng Database đang làm chậm hệ thống.
3. **Datadog Cloud (SaaS)**: Toàn bộ dữ liệu khổng lồ đó được đẩy qua Internet về máy chủ của Datadog (Lưu trữ ở Mỹ/Châu Âu). Bạn mở web Datadog để xem. Không bao giờ lo ổ cứng của công ty bị đầy.

</details>

The architecture heavily abstracts the backend data storage away from the customer, focusing entirely on ingestion and visualization:
1. **The Unified Agent**: The singular piece of software running on your infrastructure. In a Kubernetes environment, it is deployed as a DaemonSet. The Agent is incredibly intelligent. Using the `Autodiscovery` feature, it monitors the Docker socket. If a container starts with the image `redis:alpine`, the Agent dynamically loads the Redis integration, auto-configures the metrics collection, and begins shipping telemetry without a human ever touching a YAML file.
2. **APM (Application Performance Monitoring)**: The crown jewel of Datadog. By simply injecting a tracer library into your application code (e.g., `dd-trace-js` for Node, or using Java byte-code instrumentation so you don't even change the code), Datadog generates **Flame Graphs** and **Service Maps**. It traces a single HTTP request across network boundaries, proving exactly which microservice—or which specific SQL query—is causing latency.
3. **The SaaS Backend**: All processing, indexing, and storage of Petabytes of Logs/Metrics/Traces happens in Datadog's proprietary cloud infrastructure. It completely eliminates the Day-2 operational nightmare of scaling Elasticsearch clusters or Prometheus TSDBs.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vì sao các công ty sẵn sàng trả 50.000 USD/tháng cho Datadog thay vì xài hàng Miễn phí?
1. **Sự liên kết dữ liệu (Correlation)**: Với hàng Miễn phí, Log lưu một nơi (Kibana), Metrics lưu một nẻo (Grafana). Khi hệ thống sập, Kỹ sư phải mở 2 tab Web, nhìn đồng hồ CPU bên Grafana, rồi tự động não mò qua Kibana gõ lệnh tìm xem lúc đó có cái Log lỗi nào không. Rất mất thời gian. Ở Datadog, mọi thứ hòa làm 1. Bạn nhìn biểu đồ CPU đang vọt lên màu đỏ, BẠN CLICK CHUỘT VÀO CÁI ĐỈNH MÀU ĐỎ ĐÓ, Datadog lập tức xổ ra chính xác dòng Log lỗi ngay tại giây phút đó. Tốc độ tìm lỗi từ 2 tiếng giảm xuống còn 2 phút.
2. **Chi phí Cơ hội (Opportunity Cost)**: Để nuôi một hệ thống ELK và Prometheus phục vụ cho 10.000 người dùng, công ty phải thuê 3 Kỹ sư DevOps lương rất cao, chuyên ngồi tối ngày lo chuyện: Ổ cứng đầy, máy chủ sập, cấu hình bảo mật. Thay vì trả lương cho 3 người đó, Sếp trả tiền cho Datadog. Datadog làm hộ hết mọi thứ. DevOps rảnh tay đi làm việc khác sinh ra tiền cho công ty.

</details>

Why do massive enterprises willingly pay multi-million dollar annual Datadog invoices when Prometheus and ELK are "free"?
1. **The Power of Correlation (The Single Pane of Glass)**: In the DIY stack, telemetry is siloed. A developer sees a CPU spike in Grafana. To find out *why*, they must mentally copy the exact timestamp, switch browser tabs to Kibana, and manually write a query to search the logs. This Context-Switching severely degrades the MTTR (Mean Time To Recovery) during a critical outage. Datadog natively correlates data. You see a CPU spike on a graph, you literally click the spike, and a contextual menu appears offering: *"View Traces for this exact second"* or *"View Logs for the specific Pod causing this spike"*. The friction of debugging is entirely eliminated.
2. **Total Cost of Ownership (TCO)**: Open-source is free like a puppy, not free like beer. Maintaining a Petabyte-scale Elasticsearch cluster and highly available Prometheus federation requires a dedicated team of elite Platform Engineers. The salary costs of those engineers, combined with the raw AWS EC2/EBS infrastructure costs to run the DIY stack, often exceed the sticker price of the Datadog SaaS subscription. Datadog allows companies to offload "Undifferentiated Heavy Lifting".

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh Quá trình Tích hợp hệ thống Mới.
</details>

Visualizing Time-To-Value (Onboarding a new Database).

| Metric | DIY Open Source (Prometheus) | SaaS (Datadog) |
|---|---|---|
| **Step 1: Ingestion** | DevOps must manually install `postgres_exporter`, configure connection strings, update the Prometheus YAML to scrape the new IP, and restart the server. Takes 2 hours. | Datadog Agent Auto-discovers the Postgres container automatically. Takes 5 seconds. |
| **Step 2: Dashboards** | DevOps opens Grafana, searches the internet for a compatible Dashboard JSON, imports it, realizes it's broken, and spends 3 hours fixing PromQL queries. | Datadog instantly detects Postgres and automatically populates the "Postgres OOTB Dashboard" with 50 perfectly calibrated, beautiful charts. Takes 0 seconds. |

---

## Layer 4: Watchdog (Trí tuệ nhân tạo - AI)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Datadog Watchdog là tính năng mang tính Cách mạng. Bình thường, bạn phải tự đặt Báo động: "Nếu CPU > 90% thì báo tui". Nhưng lỡ ổ cứng đầy mà bạn quên đặt báo động thì sao?
Watchdog là con AI chạy ngầm 24/7. Nó học được Thói quen của hệ thống (Machine Learning). 
Ví dụ: Bình thường mỗi sáng hệ thống có 100 người mua hàng. Sáng nay đột nhiên chỉ có 5 người mua hàng. Không có biểu đồ CPU nào đỏ cả, mọi thứ có vẻ bình thường. Nhưng Watchdog nhận ra "Sự bất thường" (Anomaly) này. Nó tự động hú còi báo động cho bạn, và chỉ thẳng mặt: *"Tôi nghi ngờ thuật toán Thanh Toán bị lỗi"*.

</details>

A major differentiator in the premium Observability market is Machine Learning capabilities, heavily marketed by Datadog as **Watchdog**.
In traditional monitoring, alerting is explicit and static (e.g., `IF latency > 500ms THEN alert`). This requires human engineers to predict every possible failure mode.
Watchdog operates on automated Anomaly Detection. By continuously analyzing the historical baseline of billions of metrics and traces, Watchdog builds a behavioral profile of your application. If a new deployment introduces a subtle memory leak, or if the Database query latency shifts from 10ms to 25ms (which might not trip a static alarm, but severely impacts user experience), Watchdog automatically flags the anomaly. It proactively surfaces insights in the dashboard without any manual rule configuration, often detecting subtle degradation before the Customer Support team even receives a complaint.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Chuẩn hóa nhãn (Tagging Strategy)**: Dữ liệu bay lên Datadog như một bãi rác khổng lồ nếu không có Nhãn (Tag). BẮT BUỘC phải quy định chuẩn chung cho toàn công ty. Mọi máy chủ, mọi dòng code phải được dán tối thiểu 3 nhãn: `env: prod` (Môi trường), `service: payment` (Tên dịch vụ), `version: v1.2.0` (Phiên bản code). Có nhãn đàng hoàng thì bạn mới dùng thanh tìm kiếm của Datadog để lọc được.
2. **Chặn Log rác trước khi gửi lên (Logs without Limits)**: Datadog thu tiền dựa trên MỖI DÒNG LOG bạn gửi lên. Nếu bạn để Code cứ in ra dòng chữ vô dụng: "Trái tim vẫn đang đập", và gửi 1 triệu dòng đó lên Datadog mỗi ngày, cuối tháng công ty bạn sẽ phá sản. Hãy cấu hình Datadog Agent ngay tại máy chủ: "Lọc bỏ toàn bộ những dòng Log có chữ INFO, chỉ gửi những dòng Log có chữ ERROR lên Datadog để tiết kiệm tiền".

</details>

1. **Implement Unified Tagging**: The absolute foundation of Datadog. Telemetry data is useless if it cannot be filtered and aggregated. You MUST enforce a strict infrastructure-as-code tagging policy across AWS/Kubernetes. Every single metric, log, and trace must bear the "Holy Trinity" of reserved tags: `env` (e.g., `prod`, `staging`), `service` (e.g., `auth-api`, `billing-db`), and `version` (e.g., the Git commit SHA). When an alert fires, these tags allow you to instantly pivot from an alert to the specific version of the code that caused the bug.
2. **Aggressive Ingestion Filtering (Cost Control)**: Datadog billing is notoriously predatory if unmanaged. They charge based on the volume of Logs ingested and indexed. If a developer leaves a verbose `console.log("Healthcheck OK")` inside a loop, that useless string is sent to Datadog 10,000 times a second, instantly inflating the monthly bill by thousands of dollars. **Rule**: Implement Ingestion Pipelines and Sampling. Configure the Datadog Agent to drop useless `DEBUG/INFO` logs at the edge (so they never leave the server). For APM Traces, use Sampling Rules to only send 10% of successful traces, but 100% of Error traces.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hóa đơn khổng lồ bất ngờ (Billing Surprises)**: Rất nhiều công ty khởi nghiệp cài Datadog dùng thử, thấy quá ngon nên cứ để đó. Cuối tháng thẻ tín dụng bị trừ 10.000 USD. Lý do: Họ bật tính năng "APM" (Theo dõi vết) cho toàn bộ 100% người dùng. Lưu ý: Datadog tính tiền tính năng APM siêu đắt.
   - *Cách giải*: BẮT BUỘC cài đặt Cảnh báo hóa đơn (Billing Alerts) trong mục Cài đặt.
2. **Khóa chặt vào một nhà cung cấp (Vendor Lock-in)**: Bạn chèn thư viện `dd-trace` của Datadog dính chặt vào trong hàng ngàn dòng code Node.js của bạn. Năm sau, Datadog tăng giá gấp đôi. Bạn tức giận muốn chuyển sang xài hàng miễn phí (Prometheus). Bạn sẽ phải mở hàng ngàn file code ra xóa từng chữ `dd-trace` đi viết lại từ đầu. Sự đau khổ đó khiến bạn đành cắn răng nộp tiền cho Datadog mãi mãi.

</details>

1. **The Datadog Billing Shock**: The most infamous operational hazard. Datadog's pricing matrix is incredibly complex (charging separately for Hosts, Indexed Logs, Ingested Logs, APM Hosts, and Custom Metrics). A massive spike in Custom Metrics (e.g., a developer mistakenly putting a unique User ID into a metric tag) creates Cardinality Explosion. Unlike Prometheus, which simply crashes, Datadog happily ingests the infinite metrics and bills you for them at the end of the month. **Rule**: Always configure strict Datadog Usage Monitors and Billing Alerts the day you open the account.
2. **Severe Vendor Lock-in (Proprietary Tracers)**: If you heavily instrument your application code using Datadog's proprietary libraries (`dd-trace`), your codebase becomes deeply coupled to their commercial platform. If the Datadog subscription becomes too expensive, ripping out their proprietary SDKs across 50 microservices is a monumental refactoring effort. **Rule**: Future-proof your architecture by adopting **OpenTelemetry (OTel)**. Instrument your code using vendor-neutral OpenTelemetry SDKs. You can configure the OTel Collector to ship the data to Datadog today, and seamlessly switch the destination to an Open-Source Jaeger/Prometheus backend tomorrow without modifying a single line of application code.

---

## Related Topics

- For the Open-Source, DIY alternative to Datadog Metrics, see **[Prometheus & Grafana](./prometheus-grafana.md)**.
- For the Open-Source, DIY alternative to Datadog Logs, see the **[ELK Stack](./elk-stack.md)**.
- Datadog's pricing makes sense when you have highly dynamic, scaled architectures like **[Kubernetes](../cloud-infra/kubernetes.md)**.
