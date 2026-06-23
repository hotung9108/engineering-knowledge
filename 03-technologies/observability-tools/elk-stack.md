# ELK Stack

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Prometheus là bậc thầy gom "Con số" (Metrics), thì bộ ba **ELK Stack (Elasticsearch - Logstash - Kibana)** là ông vua gom "Chữ" (Logs). Khi một công ty chạy 50 cái máy chủ, mỗi máy chủ sinh ra hàng triệu dòng báo lỗi văn bản mỗi ngày. Nếu hệ thống sập, lập trình viên không thể nào mở thủ công 50 cái máy chủ đó lên để dò tìm dòng chữ `[ERROR]`. **ELK Stack** giải quyết việc này bằng cách: Cài một cái vòi hút (Logstash) vào tất cả các máy chủ để hút sạch Log mang về. Nó tống toàn bộ số Log khổng lồ đó vào một cái kho Tìm kiếm siêu tốc (Elasticsearch). Cuối cùng, nó cung cấp cho sếp một giao diện Web tuyệt đẹp (Kibana) để gõ chữ tìm kiếm. Bạn gõ `userId: 12345`, ngay lập tức trong 0.1 giây, ELK trả về toàn bộ mọi hành động của User đó trên cả 50 máy chủ.

</details>

> **Summary**: While Prometheus handles quantitative data (Metrics), it cannot handle massive volumes of high-cardinality text data. Enter the **ELK Stack**, the industry-standard open-source solution for Centralized Log Aggregation and Analysis. It is an acronym for three distinct products that integrate seamlessly:
> 1. **Elasticsearch**: The heart of the stack. A highly scalable, distributed, JSON-based search and analytics engine built on Apache Lucene. It indexes petabytes of text data, allowing for near-real-time, full-text search capabilities across billions of log lines.
> 2. **Logstash**: The data ingestion and processing pipeline. It dynamically ingests raw logs from disparate server files, parses the unstructured text (using Grok filters) into structured JSON data, and ships it to Elasticsearch.
> 3. **Kibana**: The visualization and exploration UI. It sits on top of Elasticsearch, allowing DevOps and Security engineers to execute complex queries, build interactive dashboards, and visually trace errors across massive distributed systems without ever SSH-ing into a server.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn làm thủ thư tại 100 cái Thư viện khác nhau trong thành phố.
1. **Không có ELK**: Sếp bảo bạn: *"Tìm cho tôi cuốn sách nào có nhắc đến chữ 'Khủng long'"*. Bạn phải tự xách xe máy, chạy tới từng thư viện, mở từng trang của 1 triệu cuốn sách ra để đọc. Rất đau khổ và mất cả tháng trời.
2. **Có ELK Stack**: 
   - **Logstash (Người dọn dẹp)**: Đứng ở 100 thư viện, cứ có sách mới là lập tức photo lại, cắt gọt gọn gàng rồi gửi bằng bưu điện về Trụ sở chính.
   - **Elasticsearch (Thủ thư siêu đẳng)**: Nhận sách từ bưu điện, ông này lập tức ghi chú lại (Index): Chữ "Khủng long" nằm ở trang mấy cuốn mấy.
   - **Kibana (Máy tính tra cứu)**: Đặt trước mặt Sếp. Sếp chỉ việc gõ `Khủng long`, máy tính chớp mắt 1 cái và in ra ngay lập tức danh sách 10.000 trang sách có chữ đó.

</details>

Imagine investigating a crime across 50 different banks.
1. **The Old Way (grep)**: You must physically drive to each bank, ask the security guard for the written guest book, and read millions of handwritten names trying to find the suspect "John Doe". It takes weeks.
2. **The ELK Way**: 
   - **Logstash (The Courier)**: Stands at the door of all 50 banks. Every time a person signs the guest book, Logstash translates their messy handwriting into a clean, typed ID card and instantly faxes it to the FBI Headquarters.
   - **Elasticsearch (The Filing Cabinet)**: The FBI Headquarters. A massive, perfectly indexed filing system. It takes the faxes and aggressively indexes them so that every single word is searchable in milliseconds.
   - **Kibana (The Detective's Computer)**: The Detective sits at a desk, types `Name: John Doe AND Action: Robbery`, hits Enter, and instantly sees a beautiful map showing exactly which banks John Doe visited at exactly what time.

---

## Layer 1: The Three Components (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

ELK là một dây chuyền sản xuất gồm 3 nhà máy hoạt động nối tiếp nhau:
1. **L (Logstash) - Nhà máy Sơ chế**: Mọi máy chủ đều viết Log rất bừa bãi. Máy A viết `[Lỗi] - 12h - Nạp tiền thất bại`. Máy B viết `12:00:00 ERROR Tiền nạp không vô`. Logstash đứng giữa, hút đống rác đó vào, và dùng Bộ lọc (Grok) để gọt giũa chúng thành 1 chuẩn duy nhất (JSON): `{"time": "12:00", "level": "ERROR", "message": "Nạp tiền thất bại"}`.
2. **E (Elasticsearch) - Kho Lưu trữ Khổng lồ**: Nhận file JSON từ Logstash. Nó không lưu vào Ổ cứng bình thường. Nó dùng thuật toán Chỉ mục ngược (Inverted Index) giống hệt cách Google hoạt động. Nhờ vậy, dù kho có chứa 1 tỷ dòng Log, bạn tìm chữ "Nạp tiền", nó vẫn trả kết quả ra ngay lập tức.
3. **K (Kibana) - Màn hình Hiển thị**: Màn hình Web để Lập trình viên vào xem. Cung cấp thanh tìm kiếm siêu mạnh, và khả năng vẽ biểu đồ (Ví dụ: Vẽ biểu đồ cột đếm xem hôm nay có bao nhiêu chữ ERROR xuất hiện).

*(Lưu ý: Ngày nay người ta thường dùng thêm **Filebeat (Chữ F)**, hoặc đổi tên thành Elastic Stack)*.

</details>

The ELK pipeline operates as a classic ETL (Extract, Transform, Load) data flow:
1. **Logstash (The Data Processor)**: Servers generate highly unstructured log text (`2023-10-14 12:05:01 WARN [Thread-4] UserService - Timeout`). If you store this raw string, you cannot aggregate it. Logstash utilizes **Grok Filters** (a massive library of Regex patterns) to parse the unstructured string and transform it into a strongly-typed JSON document: `{ "timestamp": "2023-10-14T12:05:01Z", "level": "WARN", "service": "UserService", "message": "Timeout" }`.
2. **Elasticsearch (The Storage & Search Engine)**: It receives the structured JSON document. Unlike a traditional SQL database (which scans rows slowly), Elasticsearch utilizes an **Inverted Index**. It breaks down the text field `message` into individual words ("Timeout"). It maps the word "Timeout" directly to the document ID. When an engineer queries "Timeout", Elasticsearch does not scan the database; it instantly performs a hash-lookup, allowing O(1) full-text search speeds across petabytes of data.
3. **Kibana (The UI)**: A Node.js web application that connects via REST API to Elasticsearch. It provides the Discover tab (for writing complex Lucene syntax queries like `level: ERROR AND service: UserService`) and the Dashboards tab (for visualizing log aggregations, like a pie chart of the top 5 most frequent error types).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vì sao không dùng Prometheus lưu Log cho tiện mà phải xây thêm ELK?
1. **Bản chất của Dữ liệu**: Prometheus được thiết kế bằng C++ để tối ưu hóa việc lưu **CON SỐ**. Nếu bạn nhét 1 triệu dòng chữ vào Prometheus, nó sẽ nổ tung bộ nhớ (Cardinality Explosion). Ngược lại, Elasticsearch được sinh ra bằng Java, tối ưu hóa thuật toán cực mạnh để lưu trữ và tìm kiếm **VĂN BẢN**.
2. **Tính tuân thủ pháp luật (Compliance & Auditing)**: Khi bị Hacker tấn công, Cảnh sát yêu cầu công ty cung cấp bằng chứng Hacker đã làm gì trên máy chủ lúc 2h sáng cách đây 6 tháng. Prometheus đã xóa sạch dữ liệu từ đời nào (vì nó chỉ lưu số ngắn hạn). ELK Stack có khả năng kết hợp với AWS S3, giữ lại nguyên văn 100% bằng chứng rành rành bằng chữ lưu trữ vĩnh viễn với chi phí siêu rẻ.

</details>

Why deploy the ELK Stack when you already have Prometheus? Because Metrics and Logs serve fundamentally different operational purposes, requiring completely different database architectures.
1. **The Cardinality Problem**: Prometheus is a Time-Series Database. It is mathematically incapable of storing high-cardinality data (like unique User IDs, raw error stack traces, or session tokens) without suffering an Out-Of-Memory crash. Elasticsearch is an inverted-index search engine. It was explicitly designed to index and search high-cardinality, unstructured text documents at planetary scale.
2. **Deep RCA (Root Cause Analysis)**: Prometheus Alerts tell you *what* broke ("Database CPU is at 100%"). To fix it, you need to know *why* it broke. You open Kibana, filter for logs around the exact timestamp of the CPU spike, and read the raw text logs. You instantly see: `[FATAL] - Deadlock detected on Table 'Users' by Transaction ID 8904`. Prometheus spots the smoke; ELK finds the fire.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh Quá trình "Truy tìm thủ phạm" khi Khách hàng than phiền bị lỗi.
</details>

Visualizing Log Triage (SSH vs Kibana).

| Metric | Traditional Logging (SSH) | ELK Stack |
|---|---|---|
| **Log Accessibility** | The Customer Service team says User #555 got an error. The Developer must ask DevOps for SSH access. DevOps denies it for security reasons. Developer is blocked. | The Developer opens Kibana on their web browser. No SSH keys required. |
| **Search Speed** | Developer finally gets SSH. They run `grep -r "User #555" /var/log/`. The server freezes because the log file is 50GB. Takes 20 minutes to find one line. | Developer types `user_id: 555` into Kibana. Elasticsearch returns the exact log lines spanning across 15 different servers in 50 milliseconds. |

---

## Layer 4: Architectural Evolution (Filebeat to Fluentd)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thực tế, Logstash (Chữ L) được viết bằng Java, nó cực kì nặng và ăn nhiều RAM. Nếu cài Logstash lên mọi máy chủ, nó sẽ bóp chết CPU của máy chủ đó. 
Vì vậy, kiến trúc hiện đại thường có sự biến tấu:
1. **EFK Stack (Dùng Filebeat)**: Công ty khai sinh ra ELK tạo ra một app nhỏ xíu viết bằng Go tên là **Filebeat**. Người ta cài Filebeat lên các máy chủ. Filebeat cực nhẹ, nó chỉ làm đúng 1 việc là "Đọc file log, gửi cho Logstash". Logstash lúc này được dời về đặt chung chỗ với Elasticsearch, làm nhiệm vụ hứng Log từ Filebeat gửi về rồi mới Nhào nặn (Sơ chế).
2. **EFK Stack (Dùng Fluentd)**: Ở môi trường Kubernetes hiện đại. Người ta vứt luôn Logstash đi. Người ta thay thế bằng **Fluentd** (Hoặc Fluent Bit). Fluentd vừa nhẹ, vừa tích hợp hoàn hảo với Docker/Kubernetes. Nó tự gom Log của toàn bộ Container rồi ném thẳng vào Elasticsearch.

</details>

The classic "Logstash on every server" architecture is obsolete. Logstash requires a massive Java Virtual Machine (JVM) memory footprint, making it far too heavy to run as an agent on resource-constrained application servers. The architecture evolved:
1. **The introduction of Beats (EFK)**: Elastic introduced **Filebeat**, a lightweight binary written in Go. Filebeat acts purely as a dumb "shipper". It sits on the application server, tails the log files with virtually zero CPU overhead, and forwards the raw logs over the network to a centralized, heavy Logstash cluster for processing before hitting Elasticsearch.
2. **Fluentd / Fluent Bit (The Cloud-Native Standard)**: In Kubernetes environments, Logstash is often completely replaced by **Fluentd** or its ultra-lightweight C-based cousin, **Fluent Bit**. Deployed as a DaemonSet (one per Node), Fluent Bit automatically captures all `stdout` and `stderr` streams from every Docker Container on the Node, enriches them with Kubernetes metadata (Pod Name, Namespace), and ships them directly to Elasticsearch, completely bypassing the need for Logstash.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lập trình viên: Hãy in Log bằng định dạng JSON**: Đừng bắt thằng Logstash phải khổ sở dùng Regex cắt ghép dòng chữ `[Lỗi] 12h - Nạp tiền thất bại` nữa. Nó tốn CPU cực kì. Hãy cấu hình thư viện Log trong Code Node.js của bạn (như Winston, Pino) in ra thẳng file JSON ngay từ đầu. Logstash chỉ việc cầm nguyên cục JSON đó ném vào Elasticsearch (Tốc độ tăng gấp 10 lần).
2. **Cấu hình Xóa Log tự động (ILM)**: Elasticsearch lưu dữ liệu rất tốn ổ cứng. Nếu bạn để nó chạy 1 năm, ổ cứng 10TB của công ty cũng sẽ đầy và sập toàn bộ hệ thống. BẮT BUỘC phải cài đặt chính sách Index Lifecycle Management (ILM): "Log giữ nguyên trong 7 ngày để tìm kiếm nhanh. Sau 7 ngày, nén lại cất vào kho lạnh (S3). Sau 30 ngày, Xóa Vĩnh Viễn".

</details>

1. **Structured Logging at the Source (JSON over Text)**: The most impactful architectural change a development team can make. Parsing unstructured text using Grok filters inside Logstash consumes immense CPU resources and is extremely fragile (if a developer adds an extra space to the log format, the Grok Regex breaks). **Rule**: Configure your application loggers (e.g., Winston in Node, Logback in Java) to output raw JSON directly to `stdout`. Fluentd/Logstash can ingest JSON with zero parsing overhead, guaranteeing 100% field accuracy and dramatically reducing pipeline latency.
2. **Implement Index Lifecycle Management (ILM)**: Elasticsearch is notoriously storage-hungry. If left unmanaged, the `.indices` will consume all available disk space, causing the cluster to go into `read_only_allow_delete` mode, causing massive production outages. **Rule**: You MUST implement ILM policies. Example strategy:
   - **Hot Phase (0-7 days)**: Logs reside on expensive NVMe SSDs for lightning-fast debugging.
   - **Warm/Cold Phase (7-30 days)**: Logs are moved to cheaper HDD storage; queries are slower.
   - **Delete Phase (> 30 days)**: Logs are automatically purged to prevent disk exhaustion, or archived into AWS S3 Glacier for long-term compliance.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sập hệ thống vì "Áp lực ngược" (Backpressure)**: Ngày Black Friday, hệ thống của bạn sinh ra quá nhiều Log (Vài triệu dòng mỗi giây). Elasticsearch bị quá tải không ghi kịp. Nó báo về cho Logstash: "Chậm lại tao đầy rồi". Logstash báo về cho máy chủ App: "Khoan ghi Log nữa". Máy chủ App bị kẹt, RAM tràn, VÀ SẬP LUÔN APP CỦA KHÁCH HÀNG CHỈ VÌ GHI LOG KHÔNG KỊP.
   - *Cách giải*: BẮT BUỘC phải chèn một "Vùng đệm" (Message Queue) đứng giữa. Mọi máy chủ cứ bắn thẳng Log vào **Kafka** (Hoặc Redis). Kafka sẽ chịu trận hứng hàng triệu Log. Sau đó Logstash từ từ rút từ Kafka ra đẩy vào Elasticsearch. App không bao giờ bị nghẽn.
2. **Vấn đề bảo mật (Lộ Elasticsearch ra Internet)**: Cực kì nhiều công ty cài Elasticsearch xong quên cài Mật khẩu (Mặc định nó mở toang cửa). Hacker dùng Tool rà quét mạng Internet, tìm thấy IP, vào xóa sạch kho Log và để lại chữ: *"Đưa 1 Bitcoin đây tao trả lại dữ liệu"*. LUÔN LUÔN để Elasticsearch giấu kín trong Private VPC, không bao giờ mở ra Internet.

</details>

1. **Ignoring Backpressure (The Cascade Failure)**: During a severe application incident (e.g., a database connection failure), your application enters a rapid retry loop, suddenly vomiting 10,000x the normal volume of Error logs. Logstash attempts to parse this and overwhelms Elasticsearch. Elasticsearch rejects the writes. Logstash buffers fill up, halting the ingestion agents (Filebeat). Eventually, the application itself blocks on `stdout` writing, causing your actual User-Facing Application to crash simply because the logging infrastructure failed. **Rule**: In high-scale environments, decouple ingestion from indexing by placing a massive buffer (usually **Apache Kafka** or Redis) between Filebeat and Logstash.
2. **Naked Elasticsearch Clusters (Security Breaches)**: Historically, Elasticsearch shipped without security features enabled by default. Thousands of developers deployed Elasticsearch clusters on Public IP addresses without authentication. Malicious bots constantly scan the internet for Port 9200. Upon finding an open cluster, they instantly execute a script that deletes all indices (`DELETE /_all`) and leaves a ransom note demanding Bitcoin. **Rule**: Elasticsearch MUST reside deep within a Private Subnet (VPC), shielded by strict Security Groups. X-Pack Security (TLS and Role-Based Access Control) MUST be enabled.

---

## Related Topics

- To prevent ELK from crashing during traffic spikes, place a Message Broker like **[Kafka](../message-brokers/kafka.md)** in front of it as a buffer.
- The ELK Stack handles Logs. For handling Metrics, you use **[Prometheus & Grafana](./prometheus-grafana.md)**.
- For managing ELK deployments inside Kubernetes clusters, refer to **[Kubernetes](../cloud-infra/kubernetes.md)**.
