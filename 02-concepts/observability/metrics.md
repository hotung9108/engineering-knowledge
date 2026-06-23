# Metrics

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Log (Nhật ký) là một cuốn sách kể chuyện chi tiết, thì **Metrics (Chỉ số)** là cái Bảng Điều Khiển (Dashboard) trong buồng lái máy bay. Metrics là những con số đo lường được đo đạc liên tục theo thời gian (Time-Series Data). Ví dụ: `CPU đang 90%`, `RAM còn 1GB`, `Có 50 người đang thanh toán/giây`. Khác với Log (cực kỳ tốn chỗ vì chứa chữ), Metrics cực kỳ nhẹ vì nó chỉ chứa Toán học (Chữ số). Metrics không nói cho bạn biết LỖI Ở ĐÂU, nó chỉ nói cho bạn biết CÓ LỖI HAY KHÔNG. Nhờ dung lượng nhẹ và tốc độ phản hồi tính bằng mili-giây, Metrics là trái tim của hệ thống Báo động (Alerting) và Tự động mở rộng (Auto-Scaling).

</details>

> **Summary**: While Logs provide granular, event-level forensic context, they are structurally too heavy, verbose, and slow for real-time macroscopic health assessment. **Metrics** are the macro-observability pillar. They are numerical measurements aggregated over strictly defined time intervals (Time-Series Data). Metrics compress millions of discrete application events into a single, mathematically queryable integer or float (e.g., `CPU Utilization = 85%`, `HTTP 500 Error Rate = 12/sec`, `99th Percentile Latency = 450ms`). Because they are mathematically dense and practically weightless in storage, Metrics power the critical reactive layers of infrastructure: Real-time Dashboards (Grafana), Automated Anomaly Alerting (PagerDuty), and Horizontal Pod Autoscaling (HPA) in Kubernetes.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang lái một chiếc xe hơi trên đường cao tốc.
1. **Logs (Cuốn sổ bảo hành)**: Ghi lại cực kỳ chi tiết: "Ngày 15/10: Thay nhớt hãng Castrol. Ngày 20/10: Lốp bên trái dính đinh 5cm". Khi xe hư nằm đường, bạn mới lôi sổ này ra đọc để tìm nguyên nhân. Bạn KHÔNG THỂ vừa lái xe vừa đọc sổ được.
2. **Metrics (Đồng hồ công-tơ-mét)**: Là màn hình nhấp nháy liên tục trước mặt bạn. Nó chỉ hiện số: `Tốc độ: 100km/h`, `Xăng: 10%`, `Nhiệt độ nước: ĐỎ`. Bạn liếc mắt 0.1 giây là biết chiếc xe đang KHỎE hay ĐANG HẤP HỐI. Nếu kim nhiệt độ chỉ mức ĐỎ (Alert), não bạn ngay lập tức phát tín hiệu báo động tấp vào lề, sau đó bạn mới lôi cuốn Sổ (Log) ra đọc.

</details>

Imagine running a marathon while wearing a Smartwatch.
1. **Logs (The Doctor's File)**: A massive, detailed medical report sitting in your doctor's office explaining exactly why you tore your ligament last year. You cannot read this while running.
2. **Metrics (The Smartwatch)**: You glance at your wrist. It shows exactly 3 numbers: `Heart Rate: 185 BPM`, `Pace: 5:00/km`, `Distance: 10km`. These are your Metrics. If your Heart Rate hits `200 BPM`, your watch vibrates aggressively (The Alert). It doesn't tell you *why* your heart is racing (maybe you drank too much coffee, maybe you're sprinting), it just instantly warns you that your systemic health is in critical danger.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 4 loại Metrics cơ bản mà mọi hệ thống giám sát (như Prometheus) đều sử dụng:
1. **Gauges (Đồng hồ đo)**: Một con số có thể TĂNG HOẶC GIẢM bất kỳ lúc nào. Ví dụ: `RAM đang xài là 2GB` (Lát nữa có thể tụt xuống 1GB).
2. **Counters (Bộ đếm)**: Một con số CHỈ CÓ THỂ TĂNG LÊN, không bao giờ giảm (Cho đến khi Restart server). Ví dụ: `Tổng số đơn hàng đã bán là 10.000`. Dùng để tính Vận tốc (1 giây bán được mấy đơn).
3. **Histograms (Phân phối)**: Dùng để đo kích thước hoặc thời gian. Nó chia dữ liệu vào các "Cái Xô". Ví dụ: API chạy mất bao lâu? Có 50 request chui vào xô "Dưới 100ms", 2 request chui vào xô "Trên 1 giây". Giúp nhìn thấy bức tranh tổng thể.
4. **Summaries (Tổng hợp)**: Giống Histogram nhưng nó tự động tính ra số trung bình hoặc số phần trăm (Percentiles). Ví dụ: `99% người dùng web này tải trang dưới 500 mili-giây`.

</details>

Prometheus (the CNCF industry standard) strictly categorizes Metrics into four fundamental mathematical types:
1. **Gauges**: A snapshot metric that can arbitrarily oscillate up or down. Example: `Current Active WebSockets`, `Current CPU Utilization`, `Heap Memory Used`.
2. **Counters**: A cumulative, monotonically increasing integer. It can *never* decrease (unless the process restarts). Example: `Total HTTP Requests Processed`, `Total HTTP 500 Errors`. By differentiating a Counter over time (e.g., `rate()`), you calculate Velocity (Requests Per Second).
3. **Histograms**: Samples observations (usually request durations or response sizes) and counts them in configurable "Buckets". Example: 10 requests took `<100ms`, 5 took `<500ms`, 1 took `<1000ms`. Excellent for calculating Apdex scores.
4. **Summaries**: Similar to Histograms, but calculates exact, sliding-window quantiles/percentiles (e.g., `p50`, `p90`, `p99`) directly on the client side. Example: "99% of requests complete in under 120ms".

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao không dùng Log để đếm số lượng Lỗi? (Tức là thay vì in 100 dòng chữ Error, ta gom lại thành 1 cái Metric `Lỗi = 100`).
Vì **Chi phí (Cost) và Băng thông (Bandwidth)**.
Hãy tưởng tượng hệ thống của bạn nhận 10.000 requests / 1 giây.
Nếu in Log: Bạn sẽ tạo ra 10.000 dòng chữ siêu dài mỗi giây. Bạn tốn 1TB ổ cứng mỗi ngày. Elasticsearch sẽ bị quá tải, sập luôn cả hệ thống Monitor.
Nếu in Metric: Cái Server nó chỉ đơn giản là cộng vào biến RAM `counter_request = counter_request + 1`. Cứ 15 giây, thằng Prometheus chạy tới hỏi: "Biến đó bằng mấy rồi?". Server đáp: "Bằng 150.000". Dữ liệu truyền đi qua mạng chỉ là ĐÚNG 1 CON SỐ Toán học. Cực kỳ nhanh, cực kỳ rẻ, lưu trữ 10 năm cũng chỉ tốn vài chục MB.

</details>

Why not simply derive metrics dynamically by counting Log lines in Elasticsearch?
Because of **Data Volume and Computational Physics**.
At massive scale (e.g., 50,000 Requests Per Second), emitting a JSON Log object for every single request generates Gigabytes of text per minute. If you trigger an Alert based on Log aggregation (e.g., "Alert me if `level:error` > 100"), Elasticsearch must actively scan, parse, and aggregate millions of heavy text documents in real-time. It is brutally expensive and extremely slow.
Metrics bypass text parsing entirely. The application simply increments an integer in local RAM (`request_counter++`). Every 15 seconds, Prometheus hits a `/metrics` endpoint and scrapes that single integer. The network payload is bytes, not Gigabytes. Time-Series Databases (TSDBs) are mathematically optimized to store and query these arrays of integers over years with near-zero latency, enabling real-time alerting with negligible infrastructure cost.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cách đánh giá "Độ trễ của API" giữa cách tính Trung bình (Ngu ngốc) và Percentiles (Chuyên nghiệp).
</details>

Visualizing the danger of using "Averages" (Means) instead of Percentiles (p99) in Metrics.

| Request Times (ms) | Average (Mean) | p99 (99th Percentile) | Interpretation |
|---|---|---|---|
| `[10, 10, 10, 10, 9000]` | ~`1800ms` (Looks terrible) | `9000ms` (Captures the spike) | Average is completely distorted by 1 outlier. |
| `[100, 100, 100, 100, 100]`| `100ms` (Looks great) | `100ms` (Accurate) | Smooth, predictable performance. |
| `[10, 10, 10... (98 times)... 1000]` | **`20ms` (Looks absolutely perfect!)** | **`1000ms` (Reveals the hidden disaster!)** | **The Danger:** The CEO looks at the `20ms` Average and thinks the system is perfect. Meanwhile, 1% of your richest VIP customers are experiencing 1-second hangs and complaining. Only the `p99` metric exposes the truth. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Auto-Scaling (Tự động đẻ thêm máy chủ)**: Kubernetes không biết đọc Log. Kubernetes chỉ biết đọc Metric. Bạn cấu hình: "Nếu Metric `CPU_Gauge` > 80% trong 2 phút, hãy ra lệnh mướn thêm 3 cái Pod mới". Toàn bộ sức mạnh đàn hồi của Cloud dựa hoàn toàn vào Metrics.
2. **Service Level Indicators (SLIs) & Báo động**: Nhờ Metrics, bạn vẽ được 1 biểu đồ: "Tỷ lệ API báo lỗi 500 trên tổng số API". Bạn đặt mức báo động là 1%. Đêm khuya, nếu tỷ lệ này vượt 1%, PagerDuty sẽ tự động gọi điện thoại dựng đầu Kỹ sư dậy (Alerting).
3. **Capacity Planning (Hoạch định tương lai)**: Nhìn vào biểu đồ Metric của 6 tháng qua, Giám đốc thấy Metric `Database_Disk_Usage` cứ mỗi tháng lại tăng 10%. Dựa vào toán học nội suy, Giám đốc tính ra được: "Tháng 12 năm nay ổ cứng sẽ đầy 100%, phải mua thêm ổ cứng ngay từ tháng 11".

</details>

1. **Horizontal Pod Autoscaling (HPA)**: Kubernetes natively consumes Metrics to execute elastic scaling. The HPA controller continuously queries the Metrics API. Rule: `IF avg(cpu_utilization) > 75% THEN scale_replicas(++1)`. Without real-time, lightweight metrics, automated elastic computing is impossible.
2. **SLI / SLO Monitoring & Alerting**: Site Reliability Engineering (SRE) relies entirely on Metrics to enforce Service Level Objectives (SLOs). A team defines a Service Level Indicator (SLI): `Successful_Requests / Total_Requests`. If Grafana detects this metric drops below `99.9%` for 5 consecutive minutes, it triggers an automated Webhook to PagerDuty, physically phoning the on-call engineer to mitigate the outage.
3. **Long-Term Capacity Planning**: TSDBs (Time-Series Databases) efficiently store highly downsampled metric data over years. Architects analyze the mathematical slope of the `Storage_Bytes_Used` metric over the last 12 months. By applying linear regression, they can accurately predict the exact month the SAN hardware will hit 100% capacity, allowing them to proactively order physical hardware 3 months in advance.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Gắn Tags/Labels chuẩn xác**: Một cái Metric `HTTP_Requests_Total = 5000` là vô dụng vì bạn không biết API nào đang được gọi nhiều. Bạn phải gắn Nhãn (Labels) cho nó: `HTTP_Requests_Total{method="GET", path="/users", status="200"}`. Lúc này Prometheus có thể bóc tách dữ liệu ra: Cho tao xem biểu đồ riêng của thằng GET /users.
2. **Luôn đo lường bằng The Golden Signals (4 Tín hiệu Vàng)**: Google SRE quy định mọi hệ thống đều bắt buộc phải đo 4 thứ này:
   - **Latency (Độ trễ)**: Chạy nhanh hay chậm (p99).
   - **Traffic (Lưu lượng)**: Có bao nhiêu người đang vào (Requests per second).
   - **Errors (Lỗi)**: Tỷ lệ lỗi 500 là bao nhiêu %.
   - **Saturation (Độ no/Quá tải)**: CPU/RAM/Ổ cứng sắp đầy chưa?

</details>

1. **High-Cardinality Labeling**: Emitting a flat metric named `http_requests_total` is practically useless for debugging. Metrics MUST be dimensionally labeled: `http_requests_total{method="POST", route="/api/checkout", status="500", region="us-east-1"}`. This multidimensional array allows SREs to execute complex PromQL queries to instantly isolate the fault: e.g., "Graph the error rate specifically for POST requests to the checkout endpoint in the US region."
2. **The Four Golden Signals (Google SRE Standard)**: You do not need to monitor 500 random metrics. Google rigorously defines the 4 critical signals that completely describe system health:
   - **Latency**: The time taken to serve a request (strictly using Histograms/p99, *never* averages).
   - **Traffic**: A measure of demand on the system (e.g., HTTP Requests per second, Network I/O bits/sec).
   - **Errors**: The rate of requests that fail (e.g., HTTP 5xx, or dropped packets).
   - **Saturation**: How "full" the system is. This emphasizes the most constrained resource (e.g., CPU, Memory, or Thread Pool exhaustion).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cái Bẫy Số Khổng Lồ (High Cardinality Trap)**: Việc gắn Nhãn (Label) rất tuyệt, NHƯNG tuyệt đối KHÔNG ĐƯỢC gắn những thứ có quá nhiều giá trị (Vô cực). Ví dụ: `HTTP_Requests{user_id="123"}`. Lập trình viên ngu ngốc cho `user_id` vào Label. Hệ thống có 10 triệu người dùng $\rightarrow$ Prometheus phải tạo ra 10 triệu cái biến lưu trong RAM. RAM nổ tung, Server sụp đổ ngay lập tức.
   - *Luật*: Nhãn (Label) chỉ được phép chứa dữ liệu Có giới hạn (Enum): `Status = 200, 400, 500`, `Method = GET, POST`. Những thứ như ID, Email tuyệt đối phải quăng vào LOG, không được quăng vào METRIC.
2. **Tôn thờ Con số Trung Bình (Average)**: Giám đốc nhìn biểu đồ: "Thời gian xử lý Trung bình của hệ thống là 50 mili-giây. Quá xịn!". Giám đốc không biết rằng, 99 người dùng load mất 10ms, nhưng có 1 người dùng VIP load mất 5000ms (5 giây). Trung bình cộng lại vẫn ra 50ms, che lấp đi việc khách hàng VIP đang cực kỳ tức giận.
   - *Luật*: Trong Metrics, cấm dùng chữ "Trung bình". Bắt buộc phải dùng Percentiles (p90, p95, p99). Hãy nhìn vào con số p99 để biết người xui xẻo nhất đang phải chịu đựng độ trễ là bao nhiêu.

</details>

1. **The High-Cardinality Explosion (TSDB Murder)**: The most fatal mistake in Observability engineering. A developer injects a dynamically unbounded variable into a Metric Label: `database_query_time{query="SELECT * FROM users WHERE id=9872"}`. Prometheus creates a unique, dedicated Time-Series in RAM for *every single unique Label combination*. If your database runs 5 million different queries, Prometheus allocates 5 million Time-Series in memory. The Prometheus server will instantly Out-Of-Memory (OOM) crash, blinding your entire cluster. **Absolute Rule**: Labels must possess strictly bounded, low-cardinality values (e.g., `status_code`, `http_method`). Unbounded data (`user_id`, `exact_sql_query`) strictly belongs in **Logs** or **Traces**.
2. **The Fallacy of the Mean (Averages hide Disasters)**: Evaluating API performance using a pure Mathematical Mean (Average) is architecturally fraudulent. If 99 requests take `1ms`, and 1 request takes `5000ms` (Timeout), the Mean is `50ms`. The graph looks perfectly healthy. However, 1% of your customers are experiencing a hard outage. **The Fix**: SREs explicitly discard Averages. Dashboards and Alerts must be exclusively configured against `p95` and `p99` Percentiles. If the `p99` Latency spikes to `5000ms`, the alert fires, correctly identifying that the tail-end of your traffic is suffering a catastrophic degradation.

---

## Related Topics

- For how to track a specific User ID without blowing up Metrics, read **[Tracing](./tracing.md)**.
- For what you look at when the Metrics turn RED, read **[Logging](./logging.md)**.
- For automated actions triggered by CPU metrics, review **[Kubernetes HPA](../../03-technologies/cloud-infrastructure/kubernetes.md)**.
