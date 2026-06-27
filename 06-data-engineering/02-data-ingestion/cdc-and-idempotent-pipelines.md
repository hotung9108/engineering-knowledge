# CDC & Idempotent Pipelines

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Tổng quan chuyên sâu về kỹ thuật thu thập dữ liệu bằng Change Data Capture (CDC), đảm bảo tính toàn vẹn dữ liệu qua ngữ nghĩa Exactly-once (Chỉ xử lý một lần) và thiết kế Data Pipelines có tính Lũy đẳng (Idempotent) để không làm nhân bản dữ liệu khi gặp lỗi.

</details>

> **Summary**: An advanced overview of data ingestion using Change Data Capture (CDC), ensuring data integrity via Exactly-once semantics, and designing Idempotent Data Pipelines that prevent data duplication upon failure.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **CDC (Change Data Capture)**: Tưởng tượng bạn muốn chép lại bài tập của bạn bè. Thay vì mỗi ngày mượn trọn bộ vở để chép lại từ trang 1 đến trang cuối (tốn thời gian), bạn chỉ xin bạn mình một tờ giấy nháp ghi lại "Hôm nay tôi đã bôi xóa chữ A thành chữ B ở trang 10". Bạn dựa vào đó sửa đúng trang 10 của mình. Đó là CDC: Chỉ copy phần thay đổi!
- **Idempotency (Tính Lũy đẳng)**: Bạn mua một món đồ trên mạng, trang web bị lag. Bạn bấm nút "Thanh toán" liên tục 5 lần. Nếu tài khoản của bạn bị trừ tiền 5 lần, đó là hệ thống tồi! Nếu hệ thống hiểu rằng 5 lần bấm đó chỉ là cho 1 mã đơn hàng duy nhất và chỉ trừ tiền bạn ĐÚNG 1 LẦN, đó gọi là tính Lũy đẳng. Data Pipeline cũng vậy, chạy lại pipeline bị lỗi 10 lần cũng không được phép sinh ra dữ liệu rác.

</details>

- **CDC (Change Data Capture)**: Imagine copying your friend's homework daily. Instead of borrowing their entire notebook to copy from page 1 to the end every day (which takes hours), you just ask for a sticky note saying: "Today I erased word A and wrote word B on page 10." You only update page 10 in your notebook. That’s CDC: Only syncing the changes!
- **Idempotency**: You buy an item online, but the website lags. You impatiently click "Pay" 5 times. If your bank is charged 5 times, that's a terrible system! If the system realizes all 5 clicks are for the exact same Order ID and charges you EXACTLY ONCE, that’s Idempotency. Data Pipelines must act the same: rerunning a failed pipeline 10 times must never produce duplicate garbage data.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **CDC (Change Data Capture)**: Là quá trình theo dõi trực tiếp các file Nhật ký Giao dịch (Transaction Logs, vd: WAL của PostgreSQL, Binlog của MySQL) để phát hiện và stream theo thời gian thực mọi thao tác `INSERT`, `UPDATE`, `DELETE` đang diễn ra trong Database nguồn.
- **Idempotent Pipeline**: Một đường ống dữ liệu mà nếu bạn chạy nó 1 lần, hay chạy lại nó $N$ lần cho cùng một tập dữ liệu đầu vào, kết quả ở Database đích vẫn hoàn toàn y hệt nhau, không bao giờ bị nhân đôi dữ liệu.

**Phân loại:**
- **Loại**: Thu thập Dữ liệu (Data Ingestion) / Data Engineering.
- **Công cụ CDC phổ biến**: Debezium, AWS DMS, Fivetran.

</details>

- **CDC (Change Data Capture)**: The process of reading the internal Transaction Logs of a database (e.g., PostgreSQL's WAL, MySQL's Binlog) to detect and stream every `INSERT`, `UPDATE`, and `DELETE` operation in real-time.
- **Idempotent Pipeline**: A data pipeline where executing it once, or executing it $N$ times with the same input data, produces the exact same final state in the target database, with zero duplicate rows.

### Classification
- **Type**: Data Ingestion / Data Engineering.
- **Common CDC Tools**: Debezium, AWS DMS, Fivetran.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao cần CDC?**
Trước đây, để hút dữ liệu, người ta dùng `SELECT * FROM users WHERE updated_at > 'hôm qua'`. Cách này cực kỳ chậm (phải quét toàn bộ bảng), làm quá tải Database chính, và QUAN TRỌNG NHẤT: Nó không thể bắt được các lệnh `DELETE` (vì dữ liệu đã bị xóa mất rồi lấy đâu mà SELECT). CDC đọc thẳng từ log ổ cứng, siêu nhẹ, siêu nhanh và bắt được mọi thay đổi, kể cả dữ liệu bị xóa cứng (hard delete).

**Tại sao cần Idempotency?**
Đường ống dữ liệu MẶC ĐỊNH SẼ LỖI. Đứt cáp mạng, hết RAM, thay đổi Schema... Lỗi là chuyện bình thường. Khi lỗi xảy ra, Data Engineer sẽ sửa code và "Chạy lại" (Backfill/Retry) ngày hôm đó. Nếu code dùng lệnh `INSERT INTO` mù quáng, việc chạy lại sẽ bơm thêm 1 triệu dòng dữ liệu trùng lặp vào báo cáo tài chính. Hậu quả là thảm họa! Do đó, mọi pipeline phải được thiết kế dạng Lũy đẳng (Idempotent).

</details>

**Why CDC?**
Historically, data ingestion relied on batch queries like `SELECT * FROM users WHERE updated_at > 'yesterday'`. This is slow, strains the primary Database, and MOST CRITICALLY: It cannot capture `DELETE` operations (because the row is gone, you can't query it). CDC reads directly from the low-level disk logs. It's incredibly lightweight, near real-time, and captures every single event, including hard deletes.

**Why Idempotency?**
Data pipelines WILL FAIL. Network drops, Out-Of-Memory issues, schema evolution... Failure is inevitable. When a pipeline fails, Data Engineers fix the issue and hit "Retry" or "Backfill". If the pipeline blindly uses `INSERT INTO`, retrying will inject 1 million duplicate rows into the financial reports. A complete disaster! Therefore, pipelines must be Idempotent: safe to retry endlessly.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Không có Idempotency**: Dùng `INSERT`. Chạy ngày 01/01 được 100 dòng. Hôm sau báo cáo sai, sếp bắt chạy lại ngày 01/01. Kết quả bảng có 200 dòng (Trùng lặp 100 dòng).
- **Có Idempotency**: Dùng lệnh `MERGE` (Upsert) hoặc kỹ thuật `DELETE rồi mới INSERT`. Sếp bắt chạy lại 100 lần, bảng vẫn chỉ có đúng 100 dòng mới nhất.

</details>

### Without Idempotency (Dangerous)
```sql
-- Pipeline runs for Date = 2023-10-01
-- If this pipeline crashes halfway, or is rerun manually, it duplicates data!
INSERT INTO target_sales (order_id, amount, ds)
SELECT order_id, amount, ds 
FROM source_sales 
WHERE ds = '2023-10-01';
```

### With Idempotency (Safe to retry 1000 times)
```sql
-- Technique 1: Delete/Overwrite the specific partition before inserting
DELETE FROM target_sales WHERE ds = '2023-10-01';

INSERT INTO target_sales (order_id, amount, ds)
SELECT order_id, amount, ds 
FROM source_sales 
WHERE ds = '2023-10-01';

-- Technique 2: Using MERGE (Upsert) based on Primary Key
MERGE INTO target_sales t
USING (SELECT * FROM source_sales WHERE ds = '2023-10-01') s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET t.amount = s.amount
WHEN NOT MATCHED THEN INSERT (order_id, amount, ds) VALUES (s.order_id, s.amount, s.ds);
```

| Aspect | Batch Query Ingestion | Log-based CDC (Debezium) |
|---|---|---|
| **Impact on Source DB** | High (Heavy SELECT queries) | Near Zero (Reads sequential disk logs) |
| **Latency** | Hours / Daily | Milliseconds (Real-time) |
| **Captures Deletes?** | No (Unless soft-deleted) | Yes (Captures hard deletes perfectly) |
| **Idempotency Strategy** | Overwrite Partition (DELETE/INSERT) | MERGE (Upsert) based on Primary Keys |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Đồng bộ Database (Replication)**: Dùng Debezium hút dữ liệu từ PostgreSQL, đẩy vào Kafka, sau đó ghi đồng bộ sang Snowflake / BigQuery chưa tới 2 giây.
2. **Kiến trúc hướng sự kiện (Event-driven Microservices)**: Khi dịch vụ Thanh Toán gạch nợ thành công, thay vì gọi API sang dịch vụ Giao Hàng (dễ lỗi), nó cập nhật Database của chính nó. CDC sẽ đọc log này và tự động phát một sự kiện `PaymentCompleted` lên Kafka cho dịch vụ Giao Hàng. Kỹ thuật này gọi là Outbox Pattern.
3. **Invalidate Cache**: Dùng CDC để theo dõi bảng `Products`. Hễ có giá tiền thay đổi, CDC bắn tin nhắn ra Redis để xóa cache ngay lập tức.

**Không nên làm (Anti-patterns):**
- **Dùng CDC cho bảng Log/Events rác**: CDC tạo ra 1 tin nhắn Kafka cho MỖI dòng thay đổi. Nếu bạn bật CDC cho một bảng lưu lịch sử Click chuột (10,000 requests/giây), Kafka của bạn sẽ quá tải và nổ tung. Bảng dạng Append-only (chỉ ghi thêm) thì nên dùng Batch Ingestion.

</details>

1. **Data Replication to Data Warehouse**: Using Debezium to tail PostgreSQL logs, publish to Kafka, and sink into Snowflake/BigQuery with sub-second latency.
2. **Event-driven Microservices**: When the Payment service succeeds, instead of calling the Shipping API (which might fail), it simply updates its own DB. CDC reads the log and guarantees the emission of a `PaymentCompleted` event to Kafka. This is the foundation of the Transactional Outbox Pattern.
3. **Cache Invalidation**: Using CDC to monitor a `Products` table. If a price updates, CDC instantly triggers an event to flush the Redis cache for that product.

### Anti-Patterns
- **Enabling CDC on High-Volume Append-Only tables**: CDC generates a Kafka message for *every single row mutation*. If you enable CDC on a user clickstream table (e.g., 10,000 inserts/sec), you will choke your Kafka cluster. Append-only tables (where data is never updated/deleted) should be ingested via bulk Batch processes, not CDC.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất:**
1. **Exactly-Once Semantics (Xử lý đúng 1 lần)**: Sự thật phũ phàng là các hệ thống phân tán (Kafka, Spark) thường chỉ đảm bảo *At-least-once* (Ít nhất 1 lần, tức là có thể gửi trùng lặp). Để đạt được Exactly-once, bạn PHẢI kết hợp At-least-once của hệ thống truyền tải + Tính Idempotent ở đầu ra (ví dụ dùng MERGE UPSERT ở DB đích).
2. **Giữ lại Metadata của CDC**: Khi lưu tin nhắn CDC vào Data Lake, luôn lưu kèm cột `__op` (loại thao tác: c=create, u=update, d=delete) và `__ts_ms` (thời gian ghi log). Nó giúp bạn biết chính xác dòng dữ liệu đó bị xóa hay thêm mới.
3. **Tách biệt Ingestion và Transformation (ELT)**: Khi hút CDC, hãy lưu y nguyên cấu trúc JSON (Raw data) vào Data Lake (Extract & Load). Đừng cố biến đổi dữ liệu (Transform) trên đường đi. Nếu logic biến đổi bị sai, bạn có thể chạy lại lệnh Transform từ dữ liệu Raw một cách an toàn.

**Cạm bẫy:**
1. **Lỗi thứ tự sự kiện (Out of order events)**: Nếu bạn dùng Kafka có nhiều Partitions, tin nhắn Update có thể đến ĐÍCH trước tin nhắn Insert! Hậu quả là lệnh Update bị báo lỗi (vì chưa có dữ liệu).
   - *Cách sửa*: Khi cấu hình Debezium/Kafka, bắt buộc phải dùng Khóa Chính (Primary Key) của Database làm Kafka Message Key. Điều này ép Kafka phải nhét tất cả sự kiện của CÙNG 1 dòng dữ liệu vào CÙNG 1 Partition, đảm bảo thứ tự tuyệt đối.

</details>

### Best Practices
1. **Achieving Exactly-Once Semantics**: The harsh truth of distributed systems (Kafka, Flink) is that network layers usually only guarantee *At-least-once* delivery (duplicates can happen). To achieve true Exactly-once, you MUST combine At-least-once delivery with an **Idempotent target sink** (e.g., using primary-key based UPSERTs in the Data Warehouse).
2. **Retain CDC Metadata**: When landing CDC payloads into a Data Lake, always save the operational metadata provided by Debezium: `__op` (operation type: c=create, u=update, d=delete) and `__ts_ms` (transaction timestamp). This allows downstream models to easily recreate the exact state of the database at any point in time.
3. **Embrace ELT**: When ingesting CDC streams, land the raw JSON payload directly into the Bronze layer of your Lakehouse (Extract & Load). Do NOT attempt complex transformations in-flight. If the transformation logic is buggy, having the raw immutable events allows you to simply replay the transformation step safely.

### Common Pitfalls
1. **Out-of-Order Events**: If your CDC stream uses a Kafka topic with multiple partitions, an `UPDATE` event might reach the destination *before* the initial `INSERT` event, causing a crash!
   - *Fix*: Configure Debezium/Kafka to strictly use the database row's Primary Key as the Kafka Message Key. This guarantees that all mutations for a single row are routed to the exact same Kafka partition, ensuring strict chronological ordering.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là ví dụ dùng Python (PySpark) để xử lý một luồng CDC đọc từ Kafka và cập nhật (Idempotent Upsert) vào một bảng Delta Lake. Nếu dữ liệu bị trùng lặp do mạng bị lag, tính năng `merge` của Delta Lake vẫn đảm bảo kết quả cuối cùng không bị nhân đôi.

</details>

### Idempotent CDC Upsert using PySpark & Delta Lake (Python 3.11+)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from delta.tables import DeltaTable

# Initialize Spark with Delta Lake extensions
spark = SparkSession.builder \
    .appName("CDC_Idempotent_Pipeline") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Path to our target table
target_table_path = "s3a://data-lake/silver/users"

def process_cdc_microbatch(microbatch_df, batch_id):
    """
    This function processes a chunk of real-time CDC data.
    It guarantees Idempotency by using Delta Lake's MERGE command.
    """
    
    # 1. Deduplicate within the micro-batch itself (Keep the latest event per user)
    # Essential because a single batch might contain an INSERT followed by an UPDATE for the same ID.
    deduped_df = microbatch_df.sort(col("__ts_ms").desc()).dropDuplicates(["user_id"])
    
    # 2. Separate into "Upserts" (Create/Update) and "Deletes"
    upsert_df = deduped_df.filter(col("__op").isin("c", "u", "r")) # create, update, read(snapshot)
    delete_df = deduped_df.filter(col("__op") == "d") # delete
    
    # 3. Apply Idempotent MERGE to the target Delta Table
    if DeltaTable.isDeltaTable(spark, target_table_path):
        delta_table = DeltaTable.forPath(spark, target_table_path)
        
        # Handle UPSERTS (Updates and Inserts)
        if upsert_df.count() > 0:
            delta_table.alias("target") \
                .merge(
                    upsert_df.alias("updates"),
                    "target.user_id = updates.user_id" # Match on Primary Key
                ) \
                .whenMatchedUpdateAll() \
                .whenNotMatchedInsertAll() \
                .execute()
                
        # Handle DELETES
        if delete_df.count() > 0:
            delta_table.alias("target") \
                .merge(
                    delete_df.alias("deletes"),
                    "target.user_id = deletes.user_id"
                ) \
                .whenMatchedDelete() \
                .execute()
    else:
        # Initial load if table doesn't exist
        upsert_df.write.format("delta").mode("overwrite").save(target_table_path)

# Example: Read from Kafka Stream and process using the function above
# streaming_df.writeStream \
#     .foreachBatch(process_cdc_microbatch) \
#     .start()
#     .awaitTermination()
```

---

## Related Topics

- [Data Lakehouse & ACID Transactions](../04-data-storage/lakehouse-and-acid-transactions.md) — How storage formats like Delta Lake support the `MERGE` commands used in Idempotent pipelines.
- [Transactional Outbox Pattern](../../05-backend-engineering/04-distributed-async/transactional-outbox-pattern.md) — How backend software engineers safely write the data that CDC eventually captures.
- [Batch vs Stream Processing](../03-data-processing/streaming-vs-batch-architectures.md) — Exploring the processing engines that handle the CDC data.
