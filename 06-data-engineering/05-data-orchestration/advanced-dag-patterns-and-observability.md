# Advanced DAG Patterns & Observability

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Tổng quan chuyên sâu về thiết kế Data Pipeline bằng Airflow. Tìm hiểu các pattern nâng cao như Dynamic DAGs, Sensors vs Deferrable Operators để tiết kiệm tài nguyên, chiến lược Backfill dữ liệu quá khứ, và Data Observability (Khả năng quan sát dữ liệu).

</details>

> **Summary**: An advanced overview of Data Pipeline design using Airflow. Explore advanced patterns like Dynamic DAGs, Sensors vs Deferrable Operators for resource efficiency, Backfilling strategies, and Data Observability.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **DAG (Đồ thị có hướng không tuần hoàn)**: Tưởng tượng bạn nấu một bữa ăn. Bạn không thể "Chiên trứng" trước khi "Đập trứng". "Đập trứng" phải xong thì mới "Chiên". DAG chính là tờ công thức nấu ăn quy định thứ tự bước nào làm trước, bước nào làm sau, và cấm tuyệt đối việc tạo ra vòng lặp (ví dụ: đang chiên lại quay lại đập chính quả trứng đó).
- **Deferrable Operator**: Trở lại ví dụ nấu ăn, bạn bỏ thịt vào lò nướng mất 1 tiếng. Nếu bạn đứng thộn mặt ra nhìn cái lò nướng suốt 1 tiếng đó thì bạn đang lãng phí thời gian (Giống như Airflow Sensor thông thường tốn RAM). Thay vào đó, bạn hẹn giờ rồi đi làm việc khác. Khi chuông reo, bạn mới quay lại lấy thịt ra. Đó là Deferrable Operator (Tiết kiệm tài nguyên!).

</details>

- **DAG (Directed Acyclic Graph)**: Imagine cooking a meal. You cannot "Fry the egg" before "Cracking the egg". Cracking must finish before Frying starts. A DAG is simply the recipe that dictates the exact execution order, strictly forbidding circular loops (e.g., trying to crack the egg *after* it's already fried).
- **Deferrable Operator**: Back to cooking: you put a roast in the oven for 1 hour. If you just stand there staring at the oven for an hour doing nothing, you are wasting your time (This is how standard Airflow Sensors waste RAM). Instead, you set a timer and go do other chores. When the alarm rings, you come back to the oven. That is a Deferrable Operator (Massive resource savings!).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Data Orchestration** là việc lập lịch, điều phối và giám sát các tác vụ dữ liệu. Công cụ phổ biến nhất là Apache Airflow, nơi các luồng công việc được định nghĩa bằng code Python dưới dạng DAGs.
**Data Observability** là khả năng theo dõi sức khỏe của pipeline: Dữ liệu có đến đúng giờ không? Có bị thiếu dòng nào không? Schema có bị thay đổi lén lút không?

**Phân loại:**
- **Loại**: Điều phối & Giám sát (Orchestration & Observability).
- **Công cụ Orchestration**: Apache Airflow, Dagster, Prefect.
- **Công cụ Observability**: Monte Carlo, Datafold, Datadog.

</details>

**Data Orchestration** is the scheduling, coordination, and monitoring of data tasks. The industry standard is Apache Airflow, where workflows are defined as Python code in the form of DAGs.
**Data Observability** is the ability to monitor the health of pipelines: Did the data arrive on time (SLA)? Is the volume anomalously low? Did the schema change unexpectedly?

### Classification
- **Type**: Orchestration & Observability / Data Engineering.
- **Orchestration Tools**: Apache Airflow, Dagster, Prefect.
- **Observability Tools**: Monte Carlo, Datafold, Datadog.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Ngày xưa, người ta dùng `cron` trên Linux để chạy script ETL lúc 2h sáng, và chạy bảng Dashboard lúc 3h sáng.
Vấn đề là: Nếu dữ liệu hôm đó quá lớn, script ETL chạy đến 3h15 mới xong. Tuy nhiên, `cron` cứ đến đúng 3h là mù quáng kích hoạt bảng Dashboard. Kết quả là sếp nhìn thấy Dashboard rỗng tuếch!

Airflow ra đời để giải quyết bài toán phụ thuộc (Dependency). Dashboard sẽ KHÔNG chạy dựa trên "Thời gian", mà chạy dựa trên "Trạng thái". Nó chỉ chạy khi và chỉ khi script ETL báo cáo là "Tôi đã làm xong". Nếu script ETL lỗi, Airflow sẽ báo động và tự động dừng mọi bước phía sau để tránh tạo ra rác.

</details>

Historically, engineers used Linux `cron` jobs to run the ETL script at 2:00 AM, and the Dashboard update script at 3:00 AM.
The problem: What if the ETL script takes unusually long and finishes at 3:15 AM? The `cron` job blindly triggers the Dashboard script at exactly 3:00 AM anyway. The result? The CEO wakes up to an empty Dashboard!

Airflow was created to manage Dependencies. The Dashboard update does NOT trigger based on "Time"; it triggers based on "State". It will only run if and when the ETL script successfully says "I'm done". If the ETL fails, Airflow fires an alert and halts all downstream tasks to prevent a cascading failure of bad data.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Không có Orchestrator (Dùng Cron)**: Rất khó debug. Không có giao diện (UI) để xem bước nào tạch. Muốn chạy lại dữ liệu của 1 tháng trước (Backfill) phải tự sửa ngày tháng trong code bằng tay.
- **Có Orchestrator (Airflow)**: Giao diện web rõ ràng xanh/đỏ cho từng task. Hỗ trợ tự động chạy lại (Retries). Tích hợp sẵn cơ chế `execution_date` để dễ dàng chạy lại dữ liệu của quá khứ.

</details>

### Without Orchestrator (Linux Cron)
```bash
# Hard to monitor, no dependency management, blind execution
0 2 * * * /usr/bin/python /scripts/extract_sales.py
0 3 * * * /usr/bin/python /scripts/transform_sales.py
```

### With Orchestrator (Airflow DAG)
Tasks are explicitly chained together. If `extract` fails, `transform` waits automatically.
```python
# Clear dependencies and execution order
extract_task >> transform_task >> load_task
```

| Feature | Cron Job | Apache Airflow | Dagster / Prefect |
|---|---|---|---|
| **Dependency Management** | None | Strong (Task-based) | Strong (Data-asset based) |
| **Monitoring UI** | None | Excellent | Excellent |
| **Backfilling** | Manual script editing | Built-in via CLI/UI | Native & Robust |
| **State sharing** | Write to local files | XComs (Limited size) | Native Data passing |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **ETL Pipelines**: Kích hoạt Spark chạy trên cụm EMR lúc 1h sáng, chờ Spark chạy xong thì gửi câu lệnh cho Snowflake tổng hợp dữ liệu, xong xuôi gửi tin nhắn Slack cho team.
2. **Backfilling (Chạy lại dữ liệu quá khứ)**: Một logic tính doanh thu bị sai suốt 3 tháng qua. Bạn sửa code, và yêu cầu Airflow: "Hãy chạy lại DAG này từ ngày 01/01 đến 31/03". Airflow sẽ tự động băm nhỏ ra 90 ngày và chạy lại hoàn hảo (miễn là code của bạn Lũy đẳng - Idempotent).
3. **Dynamic DAGs (DAG Động)**: Bạn có 50 đối tác, mỗi đối tác cần 1 luồng xử lý giống nhau. Thay vì copy-paste 50 file Python, bạn viết 1 vòng lặp đọc tên đối tác từ Database và tự động sinh ra 50 luồng chạy song song trên Airflow.

**Cảnh báo (Anti-patterns):**
- **Dùng Airflow để XỬ LÝ dữ liệu**: Tuyệt đối cấm! Airflow là người chỉ huy (Orchestrator), KHÔNG PHẢI là công nhân (Worker). Đừng tải 1 file CSV 5GB vào RAM của Airflow để xử lý Pandas. Hãy để Airflow gọi Spark/Snowflake làm việc đó. Airflow chỉ đứng nhìn và chờ đợi.

</details>

1. **ETL Pipelines**: Triggering an AWS EMR Spark cluster at 1 AM, waiting for it to finish, then executing a Snowflake aggregation query, and finally sending a Slack notification.
2. **Backfilling Historical Data**: A revenue calculation logic was wrong for the past 3 months. You fix the code and tell Airflow: "Run this DAG for the period between Jan 1 and Mar 31". Airflow automatically spawns 90 daily tasks and executes them seamlessly (provided your code is Idempotent).
3. **Dynamic DAGs**: You have 50 clients that require the exact same pipeline structure. Instead of copy-pasting 50 Python files, you write a script that reads client IDs from a database and dynamically generates 50 parallel task groups in the Airflow UI.

### Anti-Patterns
- **Using Airflow to PROCESS data**: Absolutely forbidden! Airflow is the Orchestrator, NOT the execution engine. Never load a 5GB CSV into Airflow's memory using Pandas. Instead, use Airflow to send a command to Spark or BigQuery to process the data. Airflow should just sit and wait for the "success" signal.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Sensors vs Deferrable Operators (Tối ưu tài nguyên):**
- Giả sử bạn cần đợi 1 file xuất hiện trên S3. Nếu dùng `S3KeySensor` thông thường, Airflow Worker sẽ bị giam lỏng (block) suốt 2 tiếng đồng hồ chỉ để `sleep()` và thỉnh thoảng thức dậy kiểm tra file. Điều này gây tốn CPU/RAM và làm nghẽn cụm Airflow.
- Kể từ Airflow 2.2, hãy dùng **Deferrable Operators** (Async). Khi đang chờ, Task sẽ tự giải phóng Worker, trả lại RAM cho hệ thống. Một tiến trình nhỏ bé tên là `Triggerer` (dùng AsyncIO) có thể giám sát hàng ngàn cảm biến cùng lúc cực kỳ nhẹ nhàng.

**2. Data Observability (Khả năng quan sát):**
- Đừng đợi sếp báo lỗi dữ liệu! Hãy chủ động chặn đứng nó.
- Thêm các bước kiểm tra (Data Quality Checks) vào giữa DAG. Ví dụ: Nếu `COUNT(user_id) == 0` hoặc có giá trị NULL bất thường, đánh fail DAG ngay lập tức và chặn không cho load vào Data Warehouse (được gọi là Circuit Breaker pattern).

**3. Hiểu đúng về `execution_date`:**
- Đây là khái niệm cực kỳ hack não của Airflow. `execution_date` KHÔNG PHẢI là thời gian thực tế lúc DAG bắt đầu chạy. Nó là "Mốc thời gian dữ liệu bắt đầu". Nếu chạy DAG hàng ngày cho dữ liệu của ngày Thứ Hai, thì `execution_date` là Thứ Hai, nhưng thời gian chạy thực tế (start_date) lại là lúc 0h00 rạng sáng Thứ Ba! Đừng dùng `datetime.now()` trong code Airflow, luôn dùng `{{ ds }}` (Jinja template).

</details>

### 1. Sensors vs. Deferrable Operators (Resource Optimization)
- Suppose you need to wait for a file to land in an S3 bucket. If you use a traditional `S3KeySensor`, it occupies an Airflow Worker slot for hours just running `time.sleep()`. This exhausts your worker pool (Worker Starvation) and costs money.
- Since Airflow 2.2, always use **Deferrable Operators** (Async). When waiting, the task completely frees up the Worker slot. A highly efficient async process called the `Triggerer` takes over, capable of monitoring thousands of events simultaneously with minimal RAM.

### 2. Data Observability & Circuit Breakers
- Don't wait for business users to complain about a broken dashboard!
- Inject **Data Quality Checks** directly into your DAG. For example, before pushing data to the production table, assert that `COUNT(*) > 0` and `revenue >= 0`. If the check fails, the DAG fails immediately (Circuit Breaker pattern), preventing corrupted data from polluting the Data Warehouse.

### 3. Mastering `execution_date` (Logical Date)
- This is the most confusing concept in Airflow. `execution_date` (now called `logical_date`) is NOT the actual wall-clock time the task runs. It represents the *start of the data period*. If a daily DAG processes Monday's data, the `logical_date` is Monday `00:00:00`, but the actual run time is Tuesday `00:00:00` (because you can't process Monday until Monday is over). Never use `datetime.now()` inside a DAG to filter data; always use the Jinja template `{{ ds }}`.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một template Airflow DAG chuẩn Production. Nó sử dụng TaskFlow API (Python 3), Jinja templating để lọc dữ liệu theo ngày (`{{ ds }}`), và đặc biệt là cách tách biệt hoàn toàn phần xử lý nặng ra khỏi Airflow (sử dụng Snowake Operator).

</details>

### Production Airflow DAG Template (Python 3.11+ / Airflow 2.5+)

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# Default arguments for resilience
default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False, # Allow parallel execution during backfills
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='daily_revenue_pipeline_v1',
    default_args=default_args,
    description='Extracts, loads, and calculates daily revenue in Snowflake',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False, # Set to True ONLY if you specifically want to backfill past dates on deploy
    tags=['finance', 'core'],
)
def revenue_pipeline():

    @task
    def extract_and_load_api_data(logical_date: str):
        """
        Lightweight Python task.
        Notice how we use `logical_date` (equivalent to {{ ds }}) to ensure Idempotency.
        If we rerun this task for Jan 1st, it will ALWAYS pull Jan 1st data, even if executed in March.
        """
        print(f"Extracting data for target date: {logical_date}")
        # import requests
        # response = requests.get(f"https://api.system.com/sales?date={logical_date}")
        # save_to_s3(response.json(), f"s3://raw-bucket/sales/dt={logical_date}/")
        return f"s3://raw-bucket/sales/dt={logical_date}/"

    # Heavy lifting is pushed to Snowflake. Airflow just orchestrates.
    # Uses Jinja templating {{ ds }} to inject the correct date string dynamically.
    transform_in_snowflake = SnowflakeOperator(
        task_id='transform_and_aggregate',
        snowflake_conn_id='snowflake_default',
        sql="""
            MERGE INTO finance.daily_revenue target
            USING (
                SELECT store_id, SUM(amount) as revenue
                FROM staging.raw_sales
                WHERE sale_date = '{{ ds }}'
                GROUP BY store_id
            ) source
            ON target.store_id = source.store_id AND target.date = '{{ ds }}'
            WHEN MATCHED THEN UPDATE SET target.revenue = source.revenue
            WHEN NOT MATCHED THEN INSERT (store_id, date, revenue) VALUES (source.store_id, '{{ ds }}', source.revenue);
        """
    )
    
    @task
    def data_quality_check():
        """Circuit breaker pattern."""
        print("Running Great Expectations or simple SQL assertions...")
        # If check fails, raise Exception. Airflow stops here.

    # Define dependencies
    s3_path = extract_and_load_api_data("{{ ds }}")
    s3_path >> transform_in_snowflake >> data_quality_check()

# Instantiate the DAG
dag_instance = revenue_pipeline()
```

---

## Related Topics

- [CDC & Idempotent Pipelines](../02-data-ingestion/cdc-and-idempotent-pipelines.md) — The core reason we use `{{ ds }}` and `MERGE` statements in Airflow.
- [Data Contracts & Quality](../06-data-governance/data-contracts-and-quality.md) — Expanding on the Data Quality checks mentioned here.
- [Batch vs Stream Processing](../03-data-processing/streaming-vs-batch-architectures.md) — Airflow manages Batch jobs, but stream processing requires different orchestration (e.g., Flink JobManager).
