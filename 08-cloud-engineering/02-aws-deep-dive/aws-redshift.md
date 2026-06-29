# AWS Redshift

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Kho dữ liệu (Data Warehouse) khổng lồ của AWS. Tìm hiểu tại sao các câu truy vấn phân tích dữ liệu (Analytics) lại làm sập RDS, và làm thế nào kiến trúc Columnar (Lưu trữ theo cột) cùng MPP (Xử lý song song) của Redshift có thể quét hàng tỷ dòng dữ liệu trong vài giây.

</details>

> **Summary**: AWS's massive Data Warehouse solution. Learn why running heavy analytics queries crashes RDS, and how Redshift's Columnar storage architecture and Massively Parallel Processing (MPP) can scan billions of rows in seconds.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn là một thủ thư quản lý hàng ngàn cuốn sách danh bạ điện thoại (Database).
- **Lưu trữ theo hàng (RDS/MySQL)**: Trong danh bạ, một trang giấy in Tên, Số điện thoại, Địa chỉ của một người (Row-based). Nếu Sếp hỏi: "Hãy tìm cho tôi một người tên John sống ở phố X", bạn tìm rất nhanh vì thông tin nằm cạnh nhau. Nhưng nếu Sếp hỏi: "Hãy đếm xem có bao nhiêu người ở thành phố này?", bạn phải lật qua HÀNG TRIỆU trang giấy, lướt qua Tên, Số điện thoại (dù bạn không cần chúng) chỉ để nhìn vào cột Địa chỉ. Rất chậm!
- **Lưu trữ theo cột (Redshift)**: Bạn tháo tung cuốn danh bạ ra. Bạn đóng tất cả các trang "Tên" thành một cuốn sổ riêng, tất cả các trang "Địa chỉ" thành một cuốn riêng. Khi Sếp yêu cầu đếm số người ở thành phố này, bạn vứt cuốn "Tên" đi, chỉ cầm đúng cuốn "Địa chỉ" lên đếm. Bạn đọc cực kỳ nhanh vì không bị nhiễu bởi các thông tin dư thừa!

</details>

You are a librarian managing thousands of phone books (The Database).
- **Row-Based Storage (RDS/MySQL)**: In the phonebook, a single page prints a person's Name, Phone, and Address together. If the Boss asks: "Find John's phone number", you find it instantly. But if the Boss asks: "Count how many people live in New York", you must physically flip through MILLIONS of pages, looking past the Names and Phone Numbers (which you don't need) just to read the Address line. Extremely slow!
- **Column-Based Storage (Redshift)**: You rip the phone books apart. You bind all the "Name" columns into one book, and all the "Address" columns into another book. When the Boss asks for the count of people in New York, you completely ignore the "Names" book. You only scan the "Addresses" book. You read exponentially faster because you don't load unnecessary data into memory!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon Redshift** là một dịch vụ Kho dữ liệu (Data Warehouse) đám mây ở quy mô Petabyte (PB) được quản lý hoàn toàn. Nó cho phép bạn phân tích khối lượng dữ liệu khổng lồ bằng cú pháp SQL tiêu chuẩn.

**Công nghệ cốt lõi:**
1. **Columnar Storage (Lưu trữ theo cột)**: Thay vì lưu từng hàng (Row) cạnh nhau trên ổ cứng, Redshift lưu từng cột (Column) cạnh nhau. Rất tối ưu cho lệnh `SELECT SUM(doanh_thu)`.
2. **MPP (Massively Parallel Processing - Xử lý song song)**: Redshift không phải là 1 máy chủ, nó là một cụm (Cluster) gồm 1 máy Leader và hàng chục máy Compute Nodes. Khi nhận câu SQL, máy Leader băm câu SQL đó ra làm 10 mảnh, gửi cho 10 máy Compute chạy song song, rồi gom kết quả lại.
3. **Redshift Spectrum**: Cho phép bạn viết lệnh SQL query TRỰC TIẾP vào các file `.csv` hoặc `.parquet` đang nằm ngoài S3 mà không cần copy dữ liệu vào ổ cứng của Redshift.

</details>

**Amazon Redshift** is a fully managed, petabyte-scale cloud Data Warehouse service. It allows you to analyze massive amounts of data using standard SQL syntax.

**Core Technologies:**
1. **Columnar Storage**: Instead of storing database records row-by-row consecutively on the hard disk, Redshift stores them column-by-column. This heavily optimizes queries like `SELECT SUM(revenue)`.
2. **MPP (Massively Parallel Processing)**: Redshift is not a single server; it is a Cluster. It has a Leader Node and multiple Compute Nodes. When you send an SQL query, the Leader node slices the query into smaller pieces, distributes them to 10 Compute nodes to process simultaneously in parallel, and aggregates the results.
3. **Redshift Spectrum**: A feature that allows you to run SQL queries DIRECTLY against raw `.csv` or `.parquet` files sitting in Amazon S3, without needing to load/copy the data into Redshift's local hard drives.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cơ sở dữ liệu truyền thống (OLTP - RDS) được thiết kế cho thao tác: Đọc/Ghi từng dòng dữ liệu cực nhanh. (Ví dụ: Thêm 1 đơn hàng vào giỏ).
Nhưng Data Analyst và Data Scientist không làm vậy. Họ gọi các lệnh OLAP (Online Analytical Processing) quét hàng tỷ dòng dữ liệu để vẽ biểu đồ doanh thu cuối năm. Nếu họ chạy lệnh SQL đó trên máy chủ RDS Production, máy chủ sẽ bị treo 100% CPU, khách hàng không mua được hàng.

Redshift ra đời làm kho chứa cuối cùng. Mỗi đêm, dữ liệu từ RDS sẽ được copy (ETL) sang Redshift. Đội Data sẽ tha hồ chạy các câu lệnh SQL siêu nặng trên Redshift mà không ảnh hưởng gì đến khách hàng đang mua sắm.

</details>

Traditional databases (OLTP - like Amazon RDS) are optimized for transactional integrity: Reading or Writing single rows extremely fast (e.g., Inserting 1 order into a shopping cart).
Data Analysts and Scientists do not work like that. They execute OLAP (Online Analytical Processing) queries that scan billions of rows to generate end-of-year revenue reports (`SUM`, `GROUP BY`, massive `JOIN`s). If they run that SQL query on the Production RDS server, it exhausts 100% of the CPU and RAM, crashing the website and blocking live customers from checking out.

Redshift exists to be the analytical backend. Every night, data is copied (via ETL) from the live RDS database into Redshift. The Data team can now hammer Redshift with incredibly heavy SQL queries without ever impacting live production traffic.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

| Tính năng | RDS (OLTP - Giao dịch) | Redshift (OLAP - Phân tích) |
|---|---|---|
| **Lưu trữ** | Row-based (Theo hàng) | Column-based (Theo cột) |
| **Kiểu truy vấn** | Lấy 1 vài dòng (Lấy profile 1 User) | Quét hàng tỷ dòng (Tính tổng doanh thu) |
| **Kiến trúc** | 1 Máy tính duy nhất (Scale Up) | Cụm nhiều máy chạy song song (MPP) |
| **Khóa chính** | Bắt buộc (Primary Key, Foreign Key) | Không bắt buộc cưỡng ép (No strict constraints) |
| **Nhiệm vụ** | Phục vụ khách hàng thực (App/Web) | Phục vụ nội bộ (Vẽ Dashboard BI, Phân tích) |

</details>

### OLTP (RDS) vs OLAP (Redshift)

| Feature | Amazon RDS (OLTP) | Amazon Redshift (OLAP) |
|---|---|---|
| **Storage Engine** | Row-based | Column-based |
| **Query Pattern** | Fetching/Updating a few rows (e.g., Get User Profile) | Scanning/Aggregating billions of rows (`SUM`, `AVG`) |
| **Architecture** | Single Monolithic Server (Scale Up) | Distributed Cluster / MPP (Scale Out) |
| **Constraints** | Strict (Primary Keys, Foreign Keys strictly enforced) | Loose (Keys defined for routing, but constraints not strictly enforced during inserts) |
| **Target Audience** | External Customers (Web/Mobile Apps) | Internal Users (Data Analysts, Business Intelligence) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Enterprise Data Warehouse**: Nơi hội tụ dữ liệu từ 10 nguồn khác nhau (Salesforce, Zendesk, RDS, DynamoDB). Dữ liệu được dọn dẹp sạch sẽ và nằm ở đây để Tableau/PowerBI kết nối vào vẽ biểu đồ.
2. **Log Analysis**: Phân tích hàng Terabyte dữ liệu nhật ký hệ thống (Server logs, Clickstreams) để tìm ra hành vi của người dùng trên website.

**Không nên làm (Anti-patterns):**
- **Dùng Redshift làm Database cho Web App**: Khởi tạo Redshift mất thời gian, và nó không thiết kế để xử lý hàng ngàn lệnh `INSERT` nhỏ lẻ mỗi giây. Đừng bao giờ kết nối code Backend NodeJS trực tiếp vào Redshift để lưu đơn hàng.

</details>

1. **Enterprise Data Warehousing (Single Source of Truth)**: Acting as the central repository where data from 10 different silos (Salesforce, Zendesk, RDS, DynamoDB) is extracted, transformed, and loaded (ETL). Business Intelligence tools like Tableau, Looker, or PowerBI connect directly to Redshift to render dashboards.
2. **Log & Clickstream Analysis**: Analyzing Terabytes of user click behavior to train recommendation engines.

### Anti-Patterns
- **Using Redshift as an Application Database (OLTP)**: Redshift is terrible at handling thousands of small, concurrent `INSERT`, `UPDATE`, or `DELETE` statements. It is optimized for massive batch loads (e.g., inserting 1 million rows at once via the `COPY` command). Never connect your Node.js or Spring Boot production API directly to Redshift to save individual customer orders. Use RDS.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Lệnh COPY (Bí quyết nhập dữ liệu)**
Đừng bao giờ dùng lệnh `INSERT INTO` để nhét 10 triệu dòng vào Redshift. Nó sẽ chậm kinh hoàng. Thay vào đó, hãy gom dữ liệu thành các file CSV, tải lên S3, rồi dùng lệnh `COPY` của Redshift. Nó sẽ hút dữ liệu từ S3 vào song song cực kỳ khủng khiếp.

**2. Distribution Styles (Phân bổ dữ liệu)**
Vì Redshift là một hệ thống gồm nhiều máy (Nodes), bạn phải chỉ định cách chia bài (Distribution). Nếu chia sai, một máy sẽ ôm hết việc, các máy khác ngồi chơi.
- **KEY**: Dữ liệu được chia theo một cột (VD: Cột `user_id`). Tất cả dữ liệu của User 1 sẽ nằm ở Node A. Cực kỳ tốt để thực hiện lệnh JOIN.
- **EVEN**: Chia bài theo vòng tròn (Round-robin). Node A 1 dòng, Node B 1 dòng. Dữ liệu dàn đều, không có máy nào bị quá tải.
- **ALL**: Chép Y NGUYÊN toàn bộ bảng đó ra tất cả các Node. Rất tốn ổ cứng, nhưng cực kỳ nhanh cho những bảng nhỏ thường xuyên bị mang ra JOIN (Ví dụ bảng danh mục Quốc gia).

</details>

### 1. The `COPY` Command (Bulk Loading)
Never use standard `INSERT INTO ... VALUES` statements to load millions of rows into Redshift. It will be excruciatingly slow. The architectural best practice is to dump your data into multiple `.csv` or `.parquet` files, upload them to Amazon S3, and execute Redshift's `COPY` command. The Compute Nodes will parallelize the download and load the data exponentially faster.

### 2. Mastering Distribution Styles
Because Redshift is a distributed cluster (MPP), data is spread across multiple Compute Nodes. If you don't dictate *how* to spread it, network shuffling will destroy your query performance.
- **KEY Distribution**: Data is hashed based on a specific column (e.g., `customer_id`). All records for `customer_id = 123` are guaranteed to land on the exact same physical Node. Highly recommended for large tables that frequently `JOIN` on that column.
- **EVEN Distribution**: Data is dealt like cards in a circle (Round-robin) across all nodes. Ensures perfectly balanced storage, but risks heavy network traffic during `JOIN`s. Good for standalone tables.
- **ALL Distribution**: A full, 100% copy of the entire table is placed on *every single Node*. It wastes storage space, but it completely eliminates network shuffling for `JOIN`s. Best practice: Use `ALL` exclusively for small, slowly-changing dimension tables (e.g., a `country_codes` lookup table).

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đây là lệnh SQL chuyên dụng trong Redshift để tải hàng triệu dòng dữ liệu từ S3 vào Database một cách song song.

</details>

### Redshift Bulk Data Loading (SQL)

This is the standard pattern for ingesting data into Redshift. The IAM Role attached to Redshift must have permissions to read from the specified S3 bucket.

```sql
-- Create the table using Columnar best practices
CREATE TABLE fact_sales (
    sales_id INT,
    customer_id INT,
    product_id INT,
    revenue DECIMAL(10,2),
    sale_date DATE
)
DISTSTYLE KEY         -- Distribute data physically across nodes based on customer_id
DISTKEY (customer_id)
SORTKEY (sale_date);  -- Sort data on disk by date (massively speeds up date-range queries)

-- The holy grail of Redshift ingestion: The COPY command
COPY fact_sales
FROM 's3://my-company-data-lake/sales_data_2024/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftS3ReadRole'
FORMAT AS PARQUET;    -- Parquet is columnar, making the load even faster
```

---

## Related Topics

- [AWS S3](./aws-s3.md) — The Data Lake where raw files sit before being `COPY`'d into Redshift.
- [AWS RDS](./aws-rds-and-aurora.md) — The OLTP database that serves live traffic (the source of Redshift's data).
- [Data Modeling & Dimensional Design](../../06-data-engineering/01-data-fundamentals/data-modeling-and-dimensional-design.md) — How to structure the schemas (Star Schema) inside Redshift.
