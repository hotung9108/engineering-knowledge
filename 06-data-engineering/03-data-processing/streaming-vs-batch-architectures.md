# Streaming vs Batch Architectures

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Phân tích chuyên sâu về Kiến trúc Xử lý dữ liệu (Lambda vs Kappa), cơ chế hoạt động bên dưới của các engine tính toán phân tán (Spark Shuffling, Flink State Management), và cách chọn đúng công cụ cho bài toán.

</details>

> **Summary**: A deep dive into Data Processing Architectures (Lambda vs Kappa), the internal mechanics of distributed compute engines (Spark Shuffling, Flink State Management), and choosing the right tool for the job.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Batch Processing (Xử lý theo mẻ)**: Giống như việc giặt quần áo. Bạn đợi cả tuần cho đồ dơ chất đầy một rổ to (gom dữ liệu), sau đó tống tất cả vào máy giặt và bấm nút giặt 1 lần duy nhất. Tiết kiệm điện, dễ làm, nhưng nếu bạn cần một cái áo sạch ngay lập tức thì không có.
- **Stream Processing (Xử lý dòng chảy)**: Giống như rửa tay dưới vòi nước. Bạn rửa từng ngón tay ngay khi nó bị dơ. Nước chảy liên tục không ngừng. Cực kỳ nhanh, có áo sạch mặc liền, nhưng tốn nước và rất khó để setup hệ thống xả nước liên tục mà không bị nghẹt.

</details>

- **Batch Processing**: It's like doing laundry. You wait all week until you have a huge pile of dirty clothes (accumulated data), then you stuff it all into the washing machine and press start once. It's highly efficient and simple, but if you need a clean shirt immediately, you're out of luck.
- **Stream Processing**: It's like washing your hands under a running faucet. The moment your finger gets dirty, you wash it. The water flows continuously. It's incredibly fast (real-time), but it consumes more resources and it's much harder to build a plumbing system that runs forever without backing up.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Batch Processing**: Xử lý một lượng lớn dữ liệu có điểm bắt đầu và kết thúc rõ ràng (Bounded data). Ví dụ: Tính toán báo cáo tài chính từ 00:00 đến 23:59 mỗi ngày. (Công cụ: Apache Spark, Hadoop MapReduce).
- **Stream Processing**: Xử lý dữ liệu liên tục không có điểm dừng (Unbounded data) ngay khi nó vừa sinh ra. Ví dụ: Phát hiện gian lận thẻ tín dụng trong 50 mili-giây. (Công cụ: Apache Flink, Kafka Streams).
- **Lambda Architecture**: Một kiến trúc ghép cả Batch và Stream chạy song song để bù trừ ưu khuyết điểm cho nhau.
- **Kappa Architecture**: Kiến trúc hiện đại chỉ dùng ĐÚNG 1 ĐƯỜNG STREAM (Stream is all you need), loại bỏ hoàn toàn Batch.

**Phân loại:**
- **Loại**: Kiến trúc Xử lý dữ liệu / Data Engineering.
- **Engines**: Apache Spark, Apache Flink, dbt.

</details>

- **Batch Processing**: Processing a large volume of bounded data (data with a clear start and end). Example: Calculating daily financial reports from 00:00 to 23:59. (Tools: Apache Spark, Hadoop MapReduce).
- **Stream Processing**: Processing unbounded data (data that never stops) piece by piece as it arrives in real-time. Example: Credit card fraud detection in 50 milliseconds. (Tools: Apache Flink, Kafka Streams).
- **Lambda Architecture**: A hybrid architecture that runs both a Batch layer and a Speed (Stream) layer in parallel.
- **Kappa Architecture**: A modern architecture that treats everything as a Stream ("Stream is all you need"), entirely removing the Batch layer.

### Classification
- **Type**: Data Processing Architectures / Data Engineering.
- **Compute Engines**: Apache Spark, Apache Flink, dbt.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Ngày xưa, mọi thứ đều là Batch (Hadoop/Hive) chạy vào ban đêm. Khi sếp thức dậy lúc 8h sáng, báo cáo đã sẵn sàng. Nhưng với sự ra đời của Uber, Netflix, mạng xã hội... dữ liệu cũ đi sau 1 đêm là dữ liệu vô dụng. Nếu xe của Uber chạy sai đường, bạn cần cảnh báo ngay lập tức chứ không phải đợi sáng hôm sau.

Điều này thúc đẩy sự ra đời của Stream Processing. Tuy nhiên, Stream Processing rất khó (Ví dụ: Đang tính tổng tiền trong 5 phút thì server bị rớt mạng, lúc có mạng lại thì tính sao?). Do đó, người ta đẻ ra Lambda Architecture: Cho hệ thống Stream tính nhanh kết quả tạm thời, rồi tối đến cho hệ thống Batch chạy lại 1 lần nữa từ đầu để đè kết quả "Chuẩn 100%" lên trên kết quả tạm.

</details>

Historically, everything was Batch (Hadoop/Hive) running overnight. When the CEO woke up at 8 AM, the dashboard was ready. However, with the rise of ride-sharing (Uber), real-time recommendations (Netflix), and social media, data that is 24 hours old is completely useless. If an Uber is heading the wrong way, you need an alert instantly, not tomorrow morning.

This necessitated Stream Processing. However, stream processing is notoriously difficult (e.g., What happens to your 5-minute rolling average if a server crashes at minute 3?). Because of this complexity, the industry invented the Lambda Architecture: Use the Stream layer for fast, approximate results, and use the Batch layer overnight to recalculate everything with 100% accuracy and overwrite the stream's results.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Lambda Architecture**: Code 1 luồng Spark (Batch) và 1 luồng Flink (Stream). Khi sửa 1 logic (ví dụ đổi cách tính thuế), bạn phải đi sửa code ở 2 nơi khác nhau bằng 2 ngôn ngữ khác nhau. Cực kỳ mệt mỏi!
- **Kappa Architecture**: Mọi thứ lưu trong Kafka. Flink đóng vai trò là não bộ duy nhất. Khi cần tính thời gian thực, Flink đọc dữ liệu mới. Khi sếp bắt chạy lại báo cáo từ đầu năm, Flink đơn giản là "tua" lại Kafka (rewind offset) và xử lý lại y hệt như stream. Chỉ phải viết code 1 lần!

</details>

### Lambda Architecture (The Legacy Hybrid)
Requires maintaining two entirely different codebases for the exact same business logic.
```text
           +---> Batch Layer (Spark) ------+
           |                               |
Data In ---+                               +---> Serving Layer (View)
           |                               |
           +---> Speed Layer (Flink) ------+
```

### Kappa Architecture (The Modern Standard)
"Stream is all you need". You write the code once. If you need to recompute historical data, you just rewind the Kafka offset to the beginning and stream it fast.
```text
Data In ---> Kafka ---> Stream Processing (Flink) ---> Serving Layer (View)
```

| Feature | Lambda Architecture | Kappa Architecture |
|---|---|---|
| **Code Duplication** | High (Write code twice for Batch & Stream) | Zero (Write code once) |
| **Historical Reprocessing** | Easy (Just run the Batch job again) | Relies on long-retention Kafka logs (Rewind) |
| **Infrastructure Cost** | High (Maintain 2 completely different clusters) | Lower (Maintain 1 streaming cluster) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Apache Spark (Batch & Micro-batch)**: Dùng để xử lý hàng Terabyte dữ liệu mỗi đêm, huấn luyện model AI, chuyển đổi dữ liệu khổng lồ (ETL). Bản chất Spark Streaming không phải Stream thật, nó chia nhỏ thời gian ra (ví dụ 1 giây 1 mẻ) gọi là Micro-batch.
2. **Apache Flink (True Streaming)**: Hệ thống gợi ý thời gian thực, cảnh báo gian lận thẻ tín dụng, Leaderboard game online. Flink xử lý TỪNG EVENT MỘT (Event-at-a-time).
3. **dbt (Data Build Tool)**: Nền tảng Batch SQL cực mạnh chạy thẳng trên Data Warehouse (Snowflake, BigQuery). Phù hợp cho Analytics Engineer không rành code Python.

**Cảnh báo (Anti-patterns):**
- **Dùng Stream khi không thực sự cần**: Hệ thống Stream đắt tiền và rất khó debug. Đừng setup 1 cụm Kafka + Flink khổng lồ chỉ để... gửi báo cáo doanh thu mỗi 24 giờ. Hãy dùng Batch (Airflow + dbt) cho khỏe!

</details>

1. **Apache Spark (Batch & Micro-batch)**: Crunching Terabytes of historical data overnight, training ML models, heavy ETL. Note that Spark Structured Streaming is not true streaming; it processes data in tiny discrete chunks (Micro-batches, e.g., every 1 second).
2. **Apache Flink (True Streaming)**: Real-time fraud detection, real-time gaming leaderboards, dynamic pricing models. Flink processes data *event-at-a-time* with sub-millisecond latency.
3. **dbt (Data Build Tool)**: Modern batch processing using pure SQL directly inside cloud data warehouses. Ideal for Analytics Engineers.

### Anti-Patterns
- **Using Streaming when Batch is sufficient**: Streaming clusters are expensive, complex, and a nightmare to debug. Do not set up a massive Kafka + Flink pipeline if the business only looks at the dashboard once a day at 9 AM. Stick to Airflow + dbt!

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Spark Internals (Sát thủ giấu mặt):**
1. **Shuffling**: Khi bạn gộp nhóm (`GROUP BY`) hoặc nối (`JOIN`) dữ liệu trong Spark, dữ liệu bắt buộc phải bay qua mạng từ máy chủ này sang máy chủ khác. Đây gọi là Shuffle. Nó RẤT CHẬM và dễ gây sập cụm (Out Of Memory).
   - *Cách tối ưu*: Dùng **Broadcast Hash Join** nếu có 1 bảng rất nhỏ. Spark sẽ copy bảng nhỏ đó ném thẳng vào RAM của tất cả các máy chứa bảng to, triệt tiêu hoàn toàn quá trình Shuffle.

**Flink Internals (Quản lý trạng thái):**
1. **Stateful Streaming**: Giả sử bạn tính "Tổng số lượng khách truy cập trong 1 tiếng". Nếu 30 phút server Flink bị sập thì sao? Flink có tính năng lưu Trạng Thái (State) vào ổ cứng (RocksDB) theo định kỳ (Checkpointing). Khi Flink khởi động lại, nó đọc ổ cứng, nhớ lại con số của phút 30 và đếm tiếp. Đảm bảo Absolutely Exactly-Once!

</details>

### Spark Internals (The Silent Killers)
1. **The Shuffle Overhead**: Whenever you perform an aggregation (`GROUP BY`) or a `JOIN` in Spark, data belonging to the same key must physically move across the network to reside on the same worker node. This is called a **Shuffle**. It involves disk I/O, network serialization, and is the #1 cause of Spark job failures (OOM) and slowness.
   - *Optimization*: If you are joining a massive 1TB fact table with a tiny 10MB dimension table, force a **Broadcast Hash Join**. Spark will copy the entire 10MB table into the RAM of every single worker node, completely eliminating the network shuffle!

### Flink Internals (State Management)
1. **Stateful Streaming & Checkpoints**: In streaming, you often calculate aggregations over time (e.g., "Total visitors in the last hour"). If the Flink worker crashes at minute 30, does it lose the count? No. Flink continuously writes its internal variables (State) to persistent storage (like RocksDB + S3) using a mechanism called **Checkpointing**. Upon restart, Flink loads the exact state from minute 30 and resumes processing seamlessly, achieving Exactly-Once semantics.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Ví dụ PySpark tối ưu hóa bằng Broadcast Join. Lệnh `broadcast(dim_table)` là "Thần chú" giúp Spark bỏ qua bước Shuffle đắt đỏ và chạy cực kỳ nhanh khi JOIN một bảng tỷ dòng với một bảng ngàn dòng.

</details>

### Advanced PySpark: Eliminating Shuffles with Broadcast Joins (Python 3.11+)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col

# Initialize Spark
spark = SparkSession.builder \
    .appName("Optimized_Batch_Processing") \
    .config("spark.sql.autoBroadcastJoinThreshold", "10485760") # Auto-broadcast tables under 10MB
    .getOrCreate()

# 1. Load a MASSIVE Fact Table (e.g., 500GB, 1 Billion rows)
fact_sales = spark.read.parquet("s3a://data-lake/bronze/sales/")

# 2. Load a TINY Dimension Table (e.g., 5MB, 10,000 rows)
dim_store = spark.read.parquet("s3a://data-lake/bronze/stores/")

# 3. BAD JOIN (Triggers a massive network Shuffle)
# bad_join_df = fact_sales.join(dim_store, "store_id")

# 4. GOOD JOIN (Broadcast Hash Join)
# By explicitly wrapping the small table in broadcast(), we force Spark to copy
# the 'dim_store' table to the memory of EVERY worker node evaluating 'fact_sales'.
# This completely eliminates the need to shuffle the 500GB fact table across the network!

optimized_df = fact_sales.join(broadcast(dim_store), "store_id")

# 5. Perform Aggregation on the node-local data
result_df = optimized_df.groupBy("store_region") \
    .sum("sales_amount")

# Execute and write
result_df.write.mode("overwrite").parquet("s3a://data-lake/silver/regional_sales/")
```

---

## Related Topics

- [CDC & Idempotent Pipelines](../02-data-ingestion/cdc-and-idempotent-pipelines.md) — How the data gets into Kafka for Flink to process.
- [Data Lakehouse Architectures](../04-data-storage/lakehouse-and-acid-transactions.md) — Where Spark writes the processed batch data.
- [Kafka vs RabbitMQ at Scale](../../05-backend-engineering/04-distributed-async/kafka-vs-rabbitmq-at-scale.md) — Understanding the backbone of Stream Processing.
