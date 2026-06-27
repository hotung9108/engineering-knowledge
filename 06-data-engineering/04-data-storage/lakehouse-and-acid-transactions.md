# Lakehouse & ACID Transactions

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Sự tiến hóa từ Data Warehouse và Data Lake sang kiến trúc Lakehouse (Delta Lake, Apache Iceberg), mang lại khả năng giao dịch ACID an toàn, định dạng lưu trữ dạng cột (Parquet), và các kỹ thuật tối ưu hóa siêu cấp như Z-Ordering.

</details>

> **Summary**: The evolution from Data Warehouses and Data Lakes to the Lakehouse architecture (Delta Lake, Apache Iceberg), enabling safe ACID transactions, columnar storage formats (Parquet), and advanced optimizations like Z-Ordering.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Data Warehouse (Kho dữ liệu)**: Giống như một cái tủ hồ sơ đắt tiền, chia ngăn nắp (bảng, cột rõ ràng). Rất dễ tìm đồ, nhưng tủ rất đắt và không nhét vừa một bức tranh hay một cuộn băng video (dữ liệu phi cấu trúc).
- **Data Lake (Hồ dữ liệu)**: Giống như một cái kho bãi khổng lồ, giá siêu rẻ. Bạn ném cái gì vào cũng được: từ văn bản, hình ảnh, video đến file rác. Điểm trừ: Rất khó để tìm lại một file cụ thể vì nó quá lộn xộn.
- **Data Lakehouse**: Bạn mua cái kho bãi khổng lồ siêu rẻ đó (Data Lake), nhưng bạn thuê thêm một ông Quản Thủ Thư Viện cực kỳ xịn (Delta Lake / Iceberg) đứng ở cửa. Ông này ghi chép sổ sách rõ ràng mọi thứ bạn ném vào kho. Thế là bạn có cả 2 ưu điểm: Giá rẻ + Chứa được mọi thứ + Tìm kiếm cực nhanh và cực an toàn!

</details>

- **Data Warehouse**: Like an expensive, perfectly organized filing cabinet. It’s easy to find documents, but the cabinet is costly and you can't stuff a painting or a VHS tape (unstructured data) inside it.
- **Data Lake**: Like a massive, ultra-cheap dumping ground. You can throw anything in there: text, images, videos, or junk. The downside: It’s incredibly difficult to find a specific item later because it's a disorganized mess.
- **Data Lakehouse**: You rent the massive, ultra-cheap dumping ground (Data Lake), but you hire a highly skilled Librarian (Delta Lake / Iceberg) to stand at the door. The librarian keeps a meticulous ledger of exactly where everything is placed. Now you have the best of both worlds: Cheap storage + Handles any data + Blazing fast, organized retrieval!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Data Lakehouse** là một kiến trúc quản lý dữ liệu hiện đại, kết hợp tính linh hoạt và chi phí rẻ của lưu trữ đám mây (Cloud Object Storage như Amazon S3) với các tính năng quản lý dữ liệu mạnh mẽ của một Database truyền thống (Giao dịch ACID, quản lý schema, lệnh UPDATE/DELETE).
Nó đạt được điều này thông qua một lớp siêu dữ liệu (Metadata Layer) nằm đè lên trên các file Parquet/ORC tĩnh.

**Phân loại:**
- **Loại**: Kiến trúc Lưu trữ Dữ liệu (Data Storage).
- **Các định dạng Lakehouse phổ biến**: Delta Lake (Databricks), Apache Iceberg (Netflix/Apple), Apache Hudi (Uber).

</details>

A **Data Lakehouse** is a modern data management architecture that combines the flexibility and cost-efficiency of Cloud Object Storage (like Amazon S3 or Google Cloud Storage) with the robust data management features of a traditional Database (ACID transactions, schema enforcement, `UPDATE`/`DELETE` commands).
It achieves this via a Metadata Layer that sits on top of static data files (like Parquet or ORC).

### Classification
- **Type**: Data Storage Architecture.
- **Leading Lakehouse Formats**: Delta Lake (Databricks), Apache Iceberg (Netflix/Apple), Apache Hudi (Uber).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vào những năm 2010, Data Lake (Hồ dữ liệu) lên ngôi nhờ Hadoop và S3. Nó rất rẻ, nhưng mang theo những điểm yếu chết người:
1. **Không có ACID**: Nếu 1 job Spark đang ghi dữ liệu vào Data Lake bị crash giữa chừng, người dùng sẽ đọc phải file dữ liệu rác (nửa có nửa không).
2. **Không thể DELETE/UPDATE**: File trên S3 là file tĩnh (immutable). Nếu luật GDPR bắt bạn phải xóa thông tin của 1 user cụ thể, bạn phải tải TOÀN BỘ file Parquet 10GB về RAM, lọc dòng đó ra, rồi ghi lại thành 1 file 10GB mới. Cực kỳ tốn kém!
3. **Data Swamp (Đầm lầy dữ liệu)**: Thiếu quản lý Schema khiến hồ dữ liệu biến thành đầm lầy, không ai dám dùng.

Các định dạng Lakehouse ra đời để mang sự kiểm soát chặt chẽ của SQL Database xuống tận mức file tĩnh (S3). Bằng cách lưu một quyển sổ Transaction Log nhỏ bé bên cạnh các file data, Lakehouse cho phép làm được những việc tưởng chừng bất khả thi trên Data Lake.

</details>

In the 2010s, Data Lakes rose to prominence with Hadoop and S3. They were cheap, but had fatal flaws:
1. **No ACID Transactions**: If a Spark job crashed halfway while writing to the Data Lake, downstream users would read corrupted, half-written data.
2. **No native DELETE/UPDATE**: Files on S3 are immutable. If GDPR laws forced you to delete a specific user's data, you had to load a 10GB Parquet file into memory, filter out that one row, and overwrite the entire 10GB file. Extremely inefficient!
3. **The Data Swamp**: Lack of schema enforcement turned Lakes into disorganized Swamps that nobody trusted.

Lakehouse formats were created to bring the strict control of an SQL Database down to the raw object storage level. By keeping a small Transaction Log alongside the data files, the Lakehouse enables database-like capabilities on raw S3 files.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Raw Data Lake (S3 + Parquet)**: Dùng Spark để xóa 1 dòng. Rất phức tạp và nguy hiểm. Nếu 2 người cùng xóa 1 lúc, mất dữ liệu chắc chắn xảy ra.
- **Data Lakehouse (S3 + Delta/Iceberg)**: Hỗ trợ lệnh SQL `DELETE FROM table WHERE id=1`. Hệ thống đảm bảo tính ACID, dù 100 người cùng xóa cũng không bị lỗi xung đột dữ liệu.

</details>

### Without Lakehouse (Raw Data Lake)
Deleting a specific record requires manually rewriting the entire partition. Unsafe for concurrent operations.
```python
# The painful process of a GDPR deletion on a raw Data Lake
df = spark.read.parquet("s3://data-lake/users/year=2023/")
# Filter out the user requesting deletion
clean_df = df.filter(df.user_id != 'USER_999')
# Overwrite the ENTIRE partition (Risky if another job is writing at the same time!)
clean_df.write.mode("overwrite").parquet("s3://data-lake/users/year=2023/")
```

### With Lakehouse (Delta Lake / Iceberg)
Provides standard Database SQL syntax with full ACID guarantees (Concurrency control).
```python
from delta.tables import DeltaTable

# Just like a traditional Database! Safe, fast, and concurrent.
deltaTable = DeltaTable.forPath(spark, "s3://data-lake/users/")
deltaTable.delete("user_id = 'USER_999'")
```

| Feature | Data Warehouse | Raw Data Lake | Data Lakehouse |
|---|---|---|---|
| **Storage Cost** | Very High | Very Low | Very Low |
| **Data Types** | Structured (Tables) | Unstructured (Video, JSON) | Both |
| **ACID Transactions** | Yes | No | Yes |
| **Compute/Storage decoupled?** | Mostly No (Tied together) | Yes | Yes (Use Spark, Trino, or Flink) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Xử lý CDC (Change Data Capture)**: Lakehouse sinh ra là để xử lý các luồng Update/Delete liên tục từ Database gốc. Lệnh `MERGE` (Upsert) của Delta/Iceberg là vũ khí tối thượng cho việc này.
2. **Time Travel (Du hành thời gian)**: Vì Lakehouse lưu lại nhật ký thay đổi, bạn có thể truy vấn dữ liệu của ngày hôm qua một cách dễ dàng: `SELECT * FROM users TIMESTAMP AS OF '2023-01-01'`. Rất hữu ích để huấn luyện Machine Learning (cần dữ liệu gốc lúc model được tạo) hoặc khôi phục dữ liệu lỡ tay xóa.
3. **Phân tích siêu dữ liệu cực lớn**: Truy vấn hàng Petabyte dữ liệu Log người dùng mà không cần nạp vào Data Warehouse đắt đỏ.

**Cảnh báo (Anti-patterns):**
- **Sử dụng cho OLTP (Giao dịch trực tuyến)**: Lakehouse hỗ trợ ACID không có nghĩa là nó dùng để làm Backend cho Website bán hàng! Nó có độ trễ khá cao (hàng giây). Hãy dùng PostgreSQL cho Website (OLTP), và dùng Lakehouse cho phân tích báo cáo (OLAP).

</details>

1. **CDC (Change Data Capture) Ingestion**: Lakehouses are perfectly built to handle continuous Streams of Inserts/Updates/Deletes. The `MERGE` (Upsert) command in Delta/Iceberg is the ultimate weapon for this.
2. **Time Travel & Auditing**: Because the Lakehouse keeps a transaction log, you can easily query what the table looked like exactly 3 months ago: `SELECT * FROM users TIMESTAMP AS OF '2023-01-01'`. This is crucial for Machine Learning reproducibility and recovering from accidental drops.
3. **Massive Log Analytics**: Querying Petabytes of clickstream data directly from S3 using engines like Trino or Spark, without paying to load it into an expensive Data Warehouse.

### Anti-Patterns
- **Using it for OLTP (Online Transaction Processing)**: Just because a Lakehouse supports ACID does NOT mean you should use it as the backend for your E-commerce website! It has high latency (seconds to minutes) optimized for massive throughput. Use PostgreSQL for the website (OLTP), and the Lakehouse for Analytics (OLAP).

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. File Sizing & Compaction (Dọn rác)**
Hệ thống Stream thường ghi ra hàng ngàn file Parquet bé xíu (mỗi file vài KB) cứ mỗi giây. Hệ thống HDFS/S3 cực kỳ ghét "Small files" (tốn RAM để duyệt file). Bạn phải lập lịch chạy lệnh `OPTIMIZE` định kỳ để gom các file nhỏ này thành file lớn 1GB. Nếu không, tốc độ đọc sẽ tụt dốc không phanh.

**2. Z-Ordering / Data Skipping**
Cơ sở dữ liệu truyền thống dùng B-Tree Index. Lakehouse không có B-Tree, nó dùng **Data Skipping** (Bỏ qua file). Metadata log lưu Min/Max của từng cột trong từng file. 
- *Z-Ordering* là kỹ thuật gom các dòng dữ liệu có điểm chung nằm cạnh nhau trong cùng 1 file. Nếu bạn query `WHERE city = 'London'`, Lakehouse đọc log, thấy file A có city [Hanoi..HCM], nó sẽ BỎ QUA không thèm quét file A. Tốc độ query sẽ tăng gấp 100 lần!

**3. Vấn đề "Bóng ma" (Vacuuming)**
Khi bạn `DELETE` một dòng trên Lakehouse, file cũ không bị xóa ngay (để hỗ trợ Time Travel). Nếu không cẩn thận, chi phí ổ cứng S3 sẽ tăng chóng mặt. Hãy chạy lệnh `VACUUM` định kỳ (vd: xóa các file lịch sử cũ hơn 7 ngày) để tiết kiệm tiền.

</details>

### 1. File Sizing & Compaction (The Small File Problem)
Streaming systems often write thousands of tiny Parquet files (a few KBs each) every minute. Distributed file systems (S3/HDFS) hate small files; the metadata overhead destroys read performance. You MUST schedule regular `OPTIMIZE` jobs to compact these tiny files into optimal 1GB files.

### 2. Z-Ordering & Data Skipping
Traditional databases use B-Tree indexes. Lakehouses use **Data Skipping**. The transaction log stores the `Min` and `Max` values of every column for every file.
- *Z-Ordering* is an advanced clustering technique that co-locates related data into the same physical files. If you run `WHERE city = 'London'`, the Lakehouse reads the metadata log. If File A has cities `[Austin..Dallas]`, it completely skips File A without reading a single byte. Query speeds can increase by 100x!

### 3. The "Ghost" Problem (Vacuuming)
When you `DELETE` or `UPDATE` a record in a Lakehouse, the old physical files are NOT immediately deleted from S3 (this is what enables Time Travel). If left unchecked, your AWS bill will skyrocket. You must run `VACUUM` commands periodically (e.g., retaining only 7 days of history) to physically delete obsolete files.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là đoạn code thực tế để tạo bảng, áp dụng Upsert (MERGE), Tối ưu hóa (OPTIMIZE) gom file nhỏ bằng thuật toán Z-Order, và Dọn rác (VACUUM) bằng Apache Iceberg (hoặc Delta Lake) qua PySpark.

</details>

### Production Lakehouse Maintenance (PySpark & Delta Lake / Iceberg concepts)

```python
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("Lakehouse_Maintenance") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

table_path = "s3a://data-lake/gold/customer_analytics"

# 1. UPSERT (MERGE) - Handling incoming changes
deltaTable = DeltaTable.forPath(spark, table_path)
updates_df = spark.read.parquet("s3a://data-lake/silver/customer_updates")

deltaTable.alias("target") \
    .merge(
        updates_df.alias("updates"),
        "target.customer_id = updates.customer_id"
    ) \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .execute()

# 2. OPTIMIZE & Z-ORDER (Run nightly via Airflow)
# Compacts small files and clusters data physically by 'country' and 'signup_date'
# Queries filtering by these columns will now be blazing fast due to Data Skipping.
spark.sql(f"""
    OPTIMIZE delta.`{table_path}`
    ZORDER BY (country, signup_date)
""")

# 3. VACUUM (Run weekly via Airflow)
# Physically delete historical files older than 7 days to save AWS S3 costs.
# Warning: You can no longer 'Time Travel' past 7 days after running this.
spark.sql(f"""
    VACUUM delta.`{table_path}` RETAIN 168 HOURS
""")
```

---

## Related Topics

- [Batch vs Stream Processing](../03-data-processing/streaming-vs-batch-architectures.md) — The engines (Spark/Flink) that process and write data to the Lakehouse.
- [CDC & Idempotent Pipelines](../02-data-ingestion/cdc-and-idempotent-pipelines.md) — How the `MERGE` command is used for real-time replication.
- [Data Modeling & Dimensional Design](../01-data-fundamentals/data-modeling-and-dimensional-design.md) — Designing the tables that reside inside the Lakehouse.
