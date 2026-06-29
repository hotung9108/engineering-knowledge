# AWS EMR & Athena (Big Data)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Công cụ chuyên trị dữ liệu siêu khủng (Big Data). Tìm hiểu cách EMR huy động hàng trăm máy chủ để xử lý hàng Petabyte dữ liệu với Apache Spark, và cách Athena cho phép bạn truy vấn thẳng vào file CSV/JSON trên S3 bằng SQL mà không cần bật máy chủ nào.

</details>

> **Summary**: The heavy lifters of Big Data. Discover how EMR orchestrates hundreds of servers to process Petabytes of data using Apache Spark, and how Athena allows you to run SQL queries directly on CSV/JSON files in S3 without provisioning any servers at all.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **AWS EMR (Elastic MapReduce)**: Tưởng tượng bạn có 1 triệu quyển sách cần dịch sang tiếng Việt trong 1 ngày. Một dịch giả (EC2) không thể làm nổi. Bạn thuê một Quản đốc (EMR). Quản đốc này lập tức gọi 1,000 dịch giả đến, chia cho mỗi người 1,000 cuốn sách, tất cả dịch cùng lúc (Song song). Cuối ngày, gom lại thành 1 triệu cuốn hoàn chỉnh rồi sa thải toàn bộ dịch giả để đỡ tốn tiền.
- **AWS Athena**: Bạn có một nhà kho khổng lồ chứa hàng tỷ tờ giấy lộn xộn (S3). Thay vì tốn tiền thuê người sắp xếp giấy tờ lên kệ (nhập vào Database) rồi mới tìm kiếm, Athena là một con robot ma thuật. Bạn cứ quăng giấy lộn xộn vào kho, khi nào cần tìm gì, hỏi con robot, nó bay vào kho lục lọi và trả lời bạn ngay lập tức. Tính tiền dựa trên số lượng giấy nó phải lục.

</details>

- **AWS EMR (Elastic MapReduce)**: Imagine you have 1 million books to translate in one day. A single translator (EC2) cannot do it. You hire a Foreman (EMR). The Foreman instantly hires 1,000 translators, gives each person 1,000 books, and they all translate simultaneously (Distributed Processing). At the end of the day, the Foreman merges the work and fires all the translators so you stop paying their hourly wages.
- **AWS Athena**: You have a massive warehouse filled with billions of loose, messy papers (Amazon S3). Instead of paying to organize those papers into neat filing cabinets (importing them into a Database) before you can search them, Athena is a magic robot. You leave the papers in a messy pile. When you have a question, you ask the robot. It flies into the warehouse, scans the papers, and gives you the answer instantly. You pay *only* for the amount of paper it had to scan.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Amazon EMR (Elastic MapReduce)**: Là nền tảng đám mây quản lý các framework xử lý Big Data mã nguồn mở như **Apache Spark**, Hadoop, Presto. AWS sẽ tự động cài đặt, cấu hình mạng, và quản lý cụm hàng chục/trăm máy chủ EC2 cho bạn.
- **Amazon Athena**: Là dịch vụ truy vấn tương tác Serverless. Bạn chỉ cần mở giao diện Athena, viết lệnh SQL `SELECT * FROM s3_bucket` và Athena sẽ truy vấn thẳng vào các file `.csv`, `.json`, `.parquet` đang nằm trên S3. Không cần cài đặt bất kỳ Database nào.

</details>

- **Amazon EMR (Elastic MapReduce)**: A managed cluster platform that simplifies running massive Big Data open-source frameworks like **Apache Spark**, Hadoop, and Presto. AWS handles the provisioning of the underlying EC2 instances, cluster setup, network configuration, and tuning.
- **Amazon Athena**: An interactive, Serverless query service. You simply open the AWS Console, write standard SQL (`SELECT * FROM s3_bucket`), and Athena queries the raw `.csv`, `.json`, or `.parquet` files resting in your S3 bucket directly. There is zero database infrastructure to manage.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Nỗi đau Big Data truyền thống:**
Cài đặt một cụm Hadoop/Spark bằng tay là cực hình. Cấu hình mạng giữa các máy, xử lý lỗi khi 1 máy bị sập ổ cứng, tối ưu RAM... khiến team Data Engineer mất hàng tháng trời chỉ để "sửa ống nước". EMR giải quyết bằng cách: Bấm 1 nút, 10 phút sau bạn có 1 cụm Spark 100 máy chạy hoàn hảo.

Nhưng đôi khi, bạn chỉ muốn chạy ĐÚNG 1 câu lệnh SQL để kiểm tra file log trên S3 xem hôm nay có bao nhiêu người truy cập. Bật cả cụm EMR lên thì quá tốn tiền và phiền phức. **Athena** ra đời để phục vụ nhu cầu "Truy vấn dạo" (Ad-hoc queries). Không máy chủ, không cài đặt, gõ SQL là ra kết quả.

</details>

**The Big Data Setup Nightmare:**
Manually installing and tuning a Hadoop or Spark cluster on raw EC2 instances is grueling. Configuring network topologies, handling node failures, and tuning JVM memory takes Data Engineers months. EMR solves this: Click a button, and 10 minutes later you possess a perfectly tuned 100-node Apache Spark cluster.

However, sometimes you only want to run EXACTLY ONE SQL query just to inspect a log file on S3 to count today's visitors. Spinning up an entire EMR cluster just for one query is expensive overkill. **Athena** exists for these "Ad-hoc queries". No servers to boot, no infrastructure to manage. Just type SQL and get your answer.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

| Tính năng | Amazon Redshift (Data Warehouse) | Amazon EMR (Big Data Cluster) | Amazon Athena (Serverless Query) |
|---|---|---|---|
| **Mục đích chính** | Lưu trữ dài hạn & Báo cáo BI | Biến đổi dữ liệu nặng (ETL / ML) | Truy vấn nhanh, kiểm tra dữ liệu thô |
| **Lưu trữ dữ liệu ở đâu?** | Ổ cứng riêng của Redshift (Và S3) | Ổ cứng EC2 (HDFS) & S3 | Bắt buộc nằm trên S3 |
| **Giá cả** | Trả tiền theo Giờ (Khá đắt) | Trả tiền theo Giờ (Rất đắt nếu quên tắt) | Trả $5 cho mỗi 1 Terabyte dữ liệu bị quét |
| **Công nghệ** | CSDL Quan hệ MPP | Apache Spark, Hadoop | Presto / Trino |

</details>

### The Data Analytics Trio Comparison

| Feature | Amazon Redshift (Data Warehouse) | Amazon EMR (Big Data Processing) | Amazon Athena (Serverless Query) |
|---|---|---|---|
| **Primary Use Case** | Highly structured Data Warehouse serving daily BI Dashboards (Tableau). | Heavy Data Transformation (ETL), Machine Learning, Batch Processing. | Ad-hoc querying, log analysis, quick data exploration. |
| **Data Storage Location**| Dedicated Redshift SSDs (and S3). | Ephemeral EC2 Disks (HDFS) and S3. | Strictly remains in Amazon S3. |
| **Billing Model** | Pay per hour for the cluster uptime. | Pay per hour for EC2 compute + EMR fee. | Pay **$5 per Terabyte** of data scanned by the query. |
| **Underlying Tech** | Proprietary AWS MPP Database. | Apache Spark, Hadoop, Hive. | Presto / Trino distributed SQL engine. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **EMR (Quy trình ETL hàng ngày)**: Mỗi đêm 2h sáng, EMR tự động bật lên với 50 máy chủ (Dùng Spot Instances giá rẻ). Spark đọc 5TB log từ S3, lọc bỏ dữ liệu rác, tổng hợp doanh thu, ghi file Parquet nén gọn gàng lại vào S3. Xong việc lúc 4h sáng, EMR tự động tắt (Tiết kiệm hàng ngàn đô la).
2. **Athena (Phân tích Log gỡ rối)**: Website bị lỗi lúc 3h chiều. Kỹ sư mở Athena, gõ lệnh `SELECT * FROM server_logs_bucket WHERE error_code = 500`. Athena quét thẳng file log thô trên S3 và trả về kết quả trong 5 giây. Không cần mở Database nào.
3. **Data Lake Foundation**: S3 làm lõi chứa dữ liệu. EMR làm công nhân dọn rác (ETL). Athena làm công cụ để các Data Analyst truy vấn trực tiếp.

**Không nên làm (Anti-patterns):**
- **Quét file CSV khổng lồ bằng Athena**: Athena tính phí $5/TB dữ liệu QUÉT. Nếu bạn dùng Athena quét file CSV dung lượng 10TB chỉ để đếm số dòng, bạn sẽ bay mất $50. Hãy dùng EMR chuyển đổi file CSV đó thành file **Parquet** (Lưu trữ dạng cột). Lần sau Athena chỉ cần quét 10GB thay vì 10TB, hóa đơn của bạn giảm 1000 lần!

</details>

1. **Transient EMR Clusters (ETL pipelines)**: Every night at 2 AM, an EMR cluster boots up with 50 Spot EC2 instances. Apache Spark reads 5TB of raw JSON clickstream data from S3, cleans it, aggregates it, and writes the clean data back to S3 in optimized Parquet format. At 4 AM, the cluster terminates itself, saving immense CapEx.
2. **Ad-hoc Log Debugging with Athena**: The website crashes. An engineer quickly opens Athena, runs `SELECT * FROM s3_logs WHERE status_code = 500`, and finds the culprit in seconds without spinning up a database.
3. **The Modern Data Lake**: S3 is the storage bedrock. EMR is the heavy computational engine (ETL). Athena is the lightweight SQL interface for Business Analysts.

### Anti-Patterns
- **Querying massive CSV files with Athena**: Athena bills you based on the volume of data scanned. If you run a `SELECT SUM()` on a 10TB CSV file, Athena must read the entire 10TB file ($50). **Best Practice**: Use EMR (Spark) to convert that raw CSV into **Parquet** (a highly compressed, columnar format) and partition it by date. The next time you run the same query, Athena only scans 10GB of Parquet data instead of 10TB. Your bill drops from $50 to $0.05!

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Tối ưu chi phí EMR với Spot Instances**
Cụm EMR thường có 1 máy Master và nhiều máy Core/Task.
Bí quyết của dân Pro: Chạy máy Master bằng On-Demand (Bảo đảm không bị sập). Chạy 90% các máy Task bằng **Spot Instances** (Giảm giá 90%). Apache Spark được thiết kế để chịu lỗi cực tốt. Nếu AWS đột ngột lấy lại máy Spot, Spark sẽ tự động giao việc đang dang dở cho máy khác làm tiếp. Bạn vừa làm Big Data, vừa tiết kiệm khủng khiếp.

**2. Phân vùng dữ liệu S3 cho Athena (Partitioning)**
Nếu file trên S3 của bạn nằm chung một thư mục, Athena sẽ phải quét TẤT CẢ khi truy vấn. Hãy lưu S3 theo cấu trúc thư mục: `s3://bucket/year=2024/month=10/day=05/`. 
Khi bạn viết lệnh `SELECT * WHERE day=05`, Athena sẽ thông minh bỏ qua tất cả các thư mục khác, chỉ đọc dữ liệu của ngày mùng 5. Thời gian query giảm từ 10 phút xuống 1 giây, và chi phí cũng giảm đi 1,000 lần!

</details>

### 1. Crushing EMR Costs with Spot Instances
An EMR cluster consists of a Master node, Core nodes (store HDFS data), and Task nodes (only compute, no storage).
**The Pro Architecture**: Provision the Master and Core nodes using On-Demand pricing (guaranteeing cluster stability). Provision 100% of the Task nodes using **AWS Spot Instances** (saving up to 90%). Because Apache Spark is inherently fault-tolerant, if AWS suddenly reclaims a Spot instance mid-calculation, Spark simply reassigns the failed tasks to the surviving nodes. Massive compute at fractional costs.

### 2. S3 Partitioning for Athena
If all your logs are dumped into a single flat S3 directory, an Athena query will be forced to scan every single byte (Full Table Scan), racking up a huge bill.
**The Fix**: You must enforce Hive-style partitioning in S3. Organize your files into physical folder paths like this: `s3://data-lake/logs/year=2024/month=10/day=05/`.
When you run `SELECT * FROM logs WHERE month='10'`, Athena is smart enough to completely ignore the other 11 folders. It only scans October's data. Query times drop from minutes to seconds, and your AWS bill drops drastically.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Để Athena hiểu được mớ file lộn xộn trên S3, bạn phải tạo một "Bảng ảo" (External Table). Bảng này chỉ là cái vỏ khai báo cấu trúc cột, dữ liệu vẫn nằm trên S3.

</details>

### Creating an External Table in Athena (SQL)

Before Athena can query your S3 files, you must define the schema using an External Table. This metadata is saved in the AWS Glue Data Catalog.

```sql
-- Tell Athena how to parse the JSON files sitting in the S3 bucket
CREATE EXTERNAL TABLE IF NOT EXISTS web_logs (
  `ip_address` string,
  `user_id` string,
  `url_path` string,
  `status_code` int,
  `response_time_ms` int
)
-- We specify that the data on S3 is partitioned by date
PARTITIONED BY (
  `year` string,
  `month` string,
  `day` string 
)
-- Tell Athena the files are in JSON format
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
-- The exact location of the raw files
LOCATION 's3://my-company-data-lake/raw-web-logs/'
TBLPROPERTIES ('has_encrypted_data'='false');

-- After creating the table, you MUST run this command so Athena discovers the partition folders
MSCK REPAIR TABLE web_logs;

-- Now you can query it cheaply!
SELECT url_path, COUNT(*) as hit_count
FROM web_logs
WHERE year = '2024' AND month = '10' AND status_code = 500
GROUP BY url_path
ORDER BY hit_count DESC;
```

---

## Related Topics

- [AWS S3](./aws-s3.md) — The fundamental storage layer for both EMR and Athena.
- [AWS Redshift](./aws-redshift.md) — The traditional Data Warehouse that often acts as the final destination for data processed by EMR.
- [Data Lakehouse Architectures](../../06-data-engineering/04-data-storage/lakehouse-and-acid-transactions.md) — Broader theory on how S3, EMR, and Athena fit into the modern Lakehouse.
