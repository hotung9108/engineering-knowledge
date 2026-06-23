# Apache Airflow

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trong ngành Kỹ sư Dữ liệu (Data Engineering), bạn phải chạy hàng trăm đoạn script mỗi ngày để gom dữ liệu. Ví dụ: "Lấy dữ liệu từ Shopee, sau đó tính tổng doanh thu, sau đó gửi báo cáo cho Sếp". Nếu bạn dùng chức năng hẹn giờ mặc định của Linux (Cronjob), bạn sẽ khóc ròng: Lỡ đoạn script thứ 1 bị lỗi mạng chạy không được, Linux vẫn nhắm mắt chạy tiếp đoạn script thứ 2, dẫn đến dữ liệu bị sai hoàn toàn. **Apache Airflow** (do Airbnb tạo ra) chính là vị Cứu Tinh. Nó là một Nhạc Trưởng (Orchestrator) siêu thông minh. Bạn dùng Python để vẽ ra một cái Sơ đồ cây (DAG) quy định thứ tự trước sau. Airflow sẽ nhìn vào sơ đồ đó mà điều khiển: Nó đảm bảo script 1 chạy xong màu xanh thì mới cho phép chạy script 2. Nếu script 1 lỗi, nó tự động thử lại 3 lần, nếu vẫn lỗi nó hú còi báo động qua Slack và dừng toàn bộ hệ thống lại.

</details>

> **Summary**: In modern Data Engineering, extracting, transforming, and loading (ETL) data requires executing thousands of interconnected scripts. Relying on traditional temporal schedulers like Linux `cron` is disastrous for complex data pipelines because `cron` has no concept of dependency management (if Step A fails, Step B will execute anyway, polluting the database). Created by Airbnb, **Apache Airflow** is the industry-standard workflow orchestration platform. It allows Data Engineers to programmatically author, schedule, and monitor workflows as **Directed Acyclic Graphs (DAGs)** using pure Python. Airflow is not a data processing engine itself (it doesn't execute heavy SQL); rather, it acts as the master Conductor. It triggers external systems (like Snowflake, Spark, or AWS EMR) in the mathematically correct topological order, handles retries gracefully, and provides a beautiful Web UI to visualize pipeline execution state.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn phải Nấu 1 Bữa Tiệc gồm 3 món.
1. **Dùng Cronjob (Cách cũ)**: Bạn đặt báo thức: 7h00 Vo Gạo, 7h05 Bật Nồi Cơm, 7h30 Chiên Trứng. Giả sử 7h00 nhà cúp nước, bạn không vo gạo được. Nhưng đúng 7h05, cái đồng hồ vẫn bắt bạn phải bật Nồi Cơm. Kết quả: Nồi cơm cháy đen.
2. **Dùng Airflow (Nhạc trưởng AI)**: Bạn viết 1 tờ giấy (DAG): "Bước 1: Vo Gạo $\rightarrow$ Bước 2: Bật Nồi". Bạn đưa tờ giấy cho Quản gia Airflow. Quản gia sẽ đứng canh. Nếu 7h cúp nước, Quản gia sẽ KHÔNG BAO GIỜ bật nồi cơm. Nó sẽ chờ đến khi nào có nước vo gạo xong, hoặc nó gửi tin nhắn SOS cho bạn. Airflow quan tâm đến *Mối quan hệ nhân quả*, chứ không phải *Thời gian mù quáng*.

</details>

Imagine building a Lego House with 5 friends.
1. **Cron (The Blind Clock)**: You give everyone a schedule: "Alice builds the roof at 10:00, Bob builds the walls at 10:05". If Alice drops her Lego pieces and gets delayed, Bob doesn't care. He tries to build the walls on top of thin air at 10:05. The house collapses.
2. **Airflow (The Site Manager)**: You don't give them a strict clock. You draw a Dependency Graph (DAG) and hand it to the Site Manager. The Manager tells Alice: "Build the roof." He tells Bob: "Sit down and do absolutely nothing until Alice says she is 100% finished." If Alice gets sick, the Manager sends you a text message and halts the entire project, preventing Bob from making a catastrophic mistake.

---

## Layer 1: Core Concepts (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Airflow được xây dựng dựa trên 3 trụ cột khái niệm:
1. **DAG (Directed Acyclic Graph)**: Đây là trái tim của Airflow. Nó là một Sơ đồ luồng công việc chảy theo 1 chiều (Không được phép chạy vòng tròn vô tận). Trong DAG quy định rõ: Task A chạy xong mới đến Task B và Task C chạy song song.
2. **Tasks & Operators**: Task là một cục gạch trong DAG. Operator là khuôn đúc ra cục gạch đó. Có hàng trăm Operator: `BashOperator` (Để chạy lệnh Linux), `PythonOperator` (Để chạy hàm Python), `PostgresOperator` (Để chạy câu lệnh SQL).
3. **Scheduler**: Trái tim nhịp đập của hệ thống. Nó thức dậy mỗi giây, nhìn vào tất cả các DAG và kiểm tra xem: "Đã đến giờ chạy chưa? Các bước trước đó đã hoàn thành chưa?". Nếu đủ điều kiện, nó bốc Task đó ném cho Worker chạy.

</details>

Airflow's architecture is defined by its programmatic approach to workflow definition:
1. **DAG (Directed Acyclic Graph)**: A DAG is the core logical entity in Airflow. It represents a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies. "Directed" means the execution flows in a specific direction (A $\rightarrow$ B). "Acyclic" means the flow cannot loop back on itself (A $\rightarrow$ B $\rightarrow$ A is forbidden, as it would create an infinite dependency loop).
2. **Operators (The Templates)**: An Operator is a Python class that acts as a template for a single Task. While Airflow is written in Python, it can orchestrate anything. You use the `BashOperator` to execute shell scripts, the `SnowflakeOperator` to trigger massive SQL aggregations in the cloud, or the `HttpOperator` to call a REST API.
3. **The Scheduler & Executor**: The **Scheduler** is a persistent Python daemon. It continuously parses your DAG files, checks the current time against the DAG's schedule (e.g., `0 2 * * *` for 2 AM daily), and evaluates task dependencies. When a Task is ready, the Scheduler hands it to the **Executor** (often Celery or Kubernetes), which physically runs the Task on a worker node.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vì sao các công ty dữ liệu lớn coi Airflow là Xương sống không thể thay thế?
1. **Everything as Code (Mọi thứ là Code)**: Các phần mềm kéo thả đồ họa cũ rích thường rất khó để quản lý phiên bản. Ở Airflow, Pipeline của bạn là 1 file Code Python. Bạn có thể lưu nó lên Github, nhờ đồng nghiệp Review, và Test tự động.
2. **Backfilling (Chạy bù quá khứ)**: Giả sử hôm nay bạn mới viết xong một thuật toán tính Doanh thu mới. Sếp bảo: "Hãy dùng thuật toán này chạy lại dữ liệu của 3 năm trước cho tôi". Với công cụ khác, bạn phải làm tay rất khổ sở. Với Airflow, bạn chỉ cần gõ 1 lệnh `Backfill từ 2020 đến 2023`. Airflow sẽ tự động cỗ máy thời gian, chạy lùi từng ngày một cách hoàn hảo và điền số liệu vào Database.
3. **Mạng lưới Tích hợp khổng lồ**: Vì là mã nguồn mở lớn nhất thế giới, Airflow có Plugin để nói chuyện với MỌI THỨ: AWS S3, Google BigQuery, Slack, Email, Hadoop, Spark.

</details>

Why has Airflow completely monopolized the modern Data Orchestration market?
1. **Configuration as Code (Pythonic)**: Legacy ETL tools (like Informatica) forced engineers to build pipelines by dragging and dropping boxes in a sluggish Windows GUI. This made version control, code review, and automated testing impossible. Airflow DAGs are written entirely in Python. This allows Data Engineers to utilize loops to dynamically generate thousands of tasks, version control the pipelines in Git, and enforce strict CI/CD practices.
2. **The Power of Backfilling**: A critical data engineering requirement. Suppose you deploy a new DAG today that calculates daily user retention. Management asks: *"Can we apply this logic to the last 2 years of historical data?"* In legacy systems, writing a script to iterate over 730 historical days while managing failures is a nightmare. Airflow natively supports **Backfilling**. You specify a historical start date, and Airflow dynamically spins up execution runs for every single day in the past, executing them in parallel while respecting dependencies.
3. **The Extensible Provider Ecosystem**: Airflow acts as the universal remote control for the modern data stack. It is shipped with hundreds of pre-built "Providers" that abstract away complex API authentications, allowing you to trigger a Spark job on AWS EMR, wait for it to finish, and immediately execute a SQL query on Snowflake with just 10 lines of Python.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh Quá trình Xử lý Sự cố khi Lấy dữ liệu (ETL).
</details>

Visualizing Pipeline Failure Management.

| Metric | Traditional Cron + Bash Scripts | Apache Airflow |
|---|---|---|
| **Failure Detection** | Script fails silently. The Data Analyst opens the dashboard the next morning and presents completely wrong data to the CEO. | Task fails. Airflow instantly catches the exception, halts downstream tasks, and fires a Slack alert: `[FAILED] DAG: daily_sales, Task: fetch_stripe_api`. |
| **Retry Logic** | The API timed out. You have to SSH into the server and manually run the script again. | You define `retries=3, retry_delay=timedelta(minutes=5)`. Airflow automatically waits 5 minutes and tries the API again without human intervention. |

---

## Layer 4: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Airflow không phải là Máy kéo cày (Do not process data in Airflow)**: Đây là sai lầm ngu ngốc và phổ biến nhất của người mới. Họ tải 1 file CSV 10 Gigabyte vào trong bộ nhớ của Airflow và dùng hàm Python để tính toán. Máy chủ Airflow sẽ sập ngay lập tức vì hết RAM. 
   - *Luật tối thượng*: Airflow chỉ là Thằng Chỉ Đường. Việc tính toán nặng phải đẩy ra ngoài (Bảo Database tự chạy lệnh SQL, hoặc bảo máy chủ Spark tự tính). Airflow chỉ đứng ngoài hô: "Chạy đi", và đợi kết quả.
2. **Tính Idempotent (Chạy 100 lần kết quả vẫn như 1)**: Giả sử Task của bạn là "Cộng thêm 100k vào tài khoản". Nếu Airflow chạy lỗi và tự động Retry (Chạy lại) lần 2, tài khoản khách sẽ bị cộng 200k. Rất nguy hiểm. Khi viết code cho Airflow, bạn phải thiết kế sao cho dù cái Task đó có lỡ chạy 10 lần, kết quả cuối cùng trong Database vẫn giống hệt như chạy 1 lần. 

</details>

1. **Airflow is an Orchestrator, NOT an Execution Engine**: The most catastrophic architectural mistake beginners make. They use the `PythonOperator` to load a 50GB Pandas DataFrame into Airflow's worker memory to perform transformations. This immediately triggers an Out-Of-Memory (OOM) kill, crashing the entire scheduler. **Rule**: Push compute down to the target systems. Use Airflow to send a `SnowflakeOperator` command, forcing the massive Snowflake cluster to do the heavy SQL lifting. Airflow should only manage the metadata (Did it start? Did it finish?).
2. **Design for Idempotency**: Airflow guarantees "At-Least-Once" delivery. If a worker node loses network connectivity momentarily, Airflow might retry the Task. If your task executes an `INSERT` statement, a retry will create duplicate data corruption. **Rule**: Every single Task must be absolutely Idempotent. (e.g., Instead of `INSERT`, use `UPSERT` or `MERGE`. Or always `DELETE` the day's data before attempting to write the day's data). Executing a task 1 time or 100 times sequentially must result in the exact same final state in the database.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Kẹt cổ chai do Parsing (DAG Parsing Timeout)**: Vì DAG được viết bằng Python. Cứ mỗi 30 giây, Airflow phải đọc và chạy lại toàn bộ file Code của bạn từ trên xuống dưới để cập nhật sơ đồ. Nếu bạn viết một hàm kết nối vào Database hay API bên ngoài NGAY BÊN NGOÀI cấu trúc Task, Airflow sẽ bị kẹt cứng (Đứng máy). *Luật: Mọi logic kết nối ra bên ngoài bắt buộc phải nhét vào bên trong ruột của cái hàm Task.*
2. **Lạm dụng Airflow cho Real-time (Thời gian thực)**: Airflow được sinh ra để chạy các tác vụ "Theo mẻ" (Batch Processing), ví dụ: Chạy mỗi tiếng 1 lần, mỗi ngày 1 lần. Cấu trúc nội bộ của nó mất khoảng 1-2 giây chỉ để khởi động 1 Task. Nếu bạn ép Airflow chạy một luồng dữ liệu liên tục mỗi giây (Streaming), hệ thống sẽ gãy vụn ngay lập tức. Hãy dùng Kafka hoặc Flink cho dữ liệu Real-time.

</details>

1. **Top-Level Code Execution (The Scheduler Killer)**: Airflow is dynamic; the Scheduler parses every `.py` file in the DAGs folder every 30 seconds to look for structural changes. If you place a heavy operation—like `requests.get()` or a Database connection—at the top level of the file (outside the `execute()` method of an operator), the Scheduler will execute that API call every 30 seconds. This causes the Scheduler's CPU to hit 100% and crashes the cluster. **Rule**: Top-level code must strictly only define the DAG structure. All actual work MUST be encapsulated inside the Operator.
2. **Shoehorning Streaming into a Batch Tool**: Airflow is explicitly designed for Batch processing (e.g., executing a pipeline every hour, or every midnight). It introduces significant scheduling latency (often 1-3 seconds of overhead just to spin up a worker to execute a task). If business requirements demand sub-second Real-Time streaming (e.g., fraud detection the millisecond a credit card is swiped), Airflow is the wrong architectural choice. You must use Apache Kafka or Apache Flink.

---

## Related Topics

- Airflow orchestrates pipelines. The actual code to manipulate the data is almost always written in **[Python](./python-ai.md)**.
- If you need real-time data streaming instead of batch processing, use **[Kafka](../message-brokers/kafka.md)**.
- For deploying scalable Airflow clusters, the modern standard is running it on **[Kubernetes](../cloud-infra/kubernetes.md)**.
