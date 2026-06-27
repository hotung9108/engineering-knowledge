# Data Modeling & Dimensional Design

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Tổng quan chuyên sâu về Data Modeling cho môi trường phân tích dữ liệu, bao gồm Star Schema, Snowflake Schema, Xử lý các chiều dữ liệu thay đổi chậm (Slowly Changing Dimensions - SCDs) và giới thiệu về Data Vault cho doanh nghiệp quy mô lớn.

</details>

> **Summary**: An advanced overview of Data Modeling for analytical environments, covering Star Schema, Snowflake Schema, Slowly Changing Dimensions (SCDs), and an introduction to Data Vault for enterprise scale.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tưởng tượng bạn đang quản lý một siêu thị. 
- Mỗi khi có khách mua hàng, máy tính tiền sẽ ghi lại: "Khách A mua sản phẩm B với giá C vào lúc D". Đây là **Fact** (Sự thật/Sự kiện). Sự kiện này không bao giờ thay đổi.
- Nhưng "Khách A" là ai? Họ bao nhiêu tuổi? Sống ở đâu? Đây là **Dimension** (Góc nhìn/Chiều dữ liệu). Nó giúp bạn mô tả chi tiết cho cái Fact kia.
- Thay vì ghi hết thông tin của "Khách A" vào từng hóa đơn mua hàng (rất tốn chỗ), bạn tạo một cuốn sổ riêng tên là "Sổ Khách Hàng". Khi cần phân tích, bạn chỉ việc nối hóa đơn với cuốn sổ này. Đó chính là **Dimensional Modeling**!

</details>

Imagine you manage a supermarket.
- Every time a customer buys something, the cash register records: "Customer A bought Product B for Price C at Time D". This is a **Fact**. This event is immutable; it never changes.
- But who is "Customer A"? How old are they? Where do they live? This is a **Dimension**. It provides context to the Fact.
- Instead of writing all of "Customer A's" details on every single receipt (which wastes space), you create a separate "Customer Book". When you need to analyze sales, you just link the receipt to this book. That is **Dimensional Modeling**!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Dimensional Modeling** (Mô hình hóa Đa chiều) là một kỹ thuật thiết kế cơ sở dữ liệu được tối ưu hóa cho Data Warehouse (Kho dữ liệu). Trái ngược với mô hình chuẩn hóa cấp 3 (3NF) dùng cho các hệ thống giao dịch (OLTP), mô hình đa chiều cố tình "phi chuẩn hóa" (denormalize) dữ liệu để tăng tốc độ truy vấn phân tích (OLAP).
- **Fact Table**: Chứa các dữ liệu định lượng (doanh thu, số lượng) và các khóa ngoại (Foreign Keys) trỏ tới bảng Dimension.
- **Dimension Table**: Chứa các thuộc tính mô tả (tên khách hàng, địa chỉ, danh mục sản phẩm).

**Phân loại:**
- **Loại**: Kiến trúc Dữ liệu / Data Engineering.
- **Mô hình phổ biến**: Star Schema (Mô hình Ngôi sao), Snowflake Schema (Mô hình Bông tuyết), Data Vault.

</details>

**Dimensional Modeling** is a database design technique optimized for Data Warehouses. Unlike 3rd Normal Form (3NF) used in transactional systems (OLTP), dimensional modeling deliberately denormalizes data to speed up analytical queries (OLAP).
- **Fact Table**: Contains quantitative data (revenue, quantity) and Foreign Keys pointing to Dimension tables.
- **Dimension Table**: Contains descriptive attributes (customer name, address, product category).

### Classification
- **Type**: Data Architecture / Data Engineering.
- **Common Models**: Star Schema, Snowflake Schema, Data Vault.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Các cơ sở dữ liệu giao dịch (OLTP) như PostgreSQL/MySQL được thiết kế để `INSERT` và `UPDATE` cực nhanh. Chúng làm điều này bằng cách chia nhỏ dữ liệu thành hàng chục bảng khác nhau (Chuẩn hóa - Normalization). 
Tuy nhiên, nếu Data Analyst muốn thống kê "Doanh thu của khách hàng VIP tại Hà Nội trong năm 2023", họ sẽ phải viết một câu lệnh SQL chứa tới 10 lệnh `JOIN` giữa các bảng. Điều này khiến Database phải quét quá nhiều dữ liệu, dẫn đến treo máy.

Dimensional Modeling ra đời (được phổ biến bởi Ralph Kimball) để giải quyết vấn đề này bằng cách gom nhóm dữ liệu lại thành số lượng bảng ít hơn rất nhiều, giúp các câu lệnh `JOIN` trở nên cực kỳ đơn giản và tốc độ quét dữ liệu nhanh gấp hàng trăm lần.

</details>

Transactional databases (OLTP) like PostgreSQL/MySQL are designed for lightning-fast `INSERT` and `UPDATE` operations. They achieve this by breaking data down into dozens of distinct tables (Normalization).
However, if a Data Analyst wants to aggregate "Revenue of VIP customers in New York during 2023", they would have to write an SQL query with 10 `JOIN` clauses. This forces the Database to scan massive amounts of scattered data, often crashing the system or taking hours.

Dimensional Modeling (popularized by Ralph Kimball) was created to solve this by grouping data into far fewer tables, making `JOIN`s extremely simple and making data scanning hundreds of times faster for analytical engines.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Hệ thống OLTP truyền thống (3NF)**: Thông tin sản phẩm nằm rải rác ở bảng `Product`, `Category`, `SubCategory`. Truy vấn lấy danh mục sản phẩm phải JOIN 3 bảng.
- **Star Schema**: Gom tất cả vào 1 bảng duy nhất `dim_product`. Chỉ cần JOIN 1 lần giữa `fact_sales` và `dim_product`.
- **Snowflake Schema**: Giống Star Schema, nhưng bảng Dimension lại bị chuẩn hóa thêm 1 bậc (Ví dụ `dim_product` lại nối ra `dim_category`). Giúp tiết kiệm ổ cứng nhưng làm chậm tốc độ đọc.

</details>

### Traditional OLTP (3NF)
```sql
-- Analytical query requires multiple complex JOINs
SELECT c.category_name, SUM(o.total_price)
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN subcategories s ON p.subcategory_id = s.id
JOIN categories c ON s.category_id = c.id
GROUP BY c.category_name;
```

### Dimensional Modeling (Star Schema)
```sql
-- Analytical query is drastically simplified and much faster
SELECT dp.category_name, SUM(fs.total_amount)
FROM fact_sales fs
JOIN dim_product dp ON fs.product_key = dp.product_key
GROUP BY dp.category_name;
```

| Aspect | Star Schema | Snowflake Schema | Data Vault |
|---|---|---|---|
| **Structure** | Fact table surrounded by flat Dimensions | Fact table surrounded by normalized Dimensions | Hubs, Links, and Satellites |
| **Query Speed** | Fastest (Fewest JOINs) | Slower (More JOINs) | Slowest (Requires building Marts on top) |
| **Storage Space** | High (Redundant data) | Medium (Normalized) | Very High (Stores all history permanently) |
| **Agility / Scaling** | Hard to change schema later | Moderate | Excellent (Built for enterprise flexibility) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Star Schema**: Lựa chọn tiêu chuẩn (Mặc định) cho hầu hết các Data Warehouse (Snowflake, BigQuery) và Data Marts. Phục vụ trực tiếp cho BI Tools (Tableau, PowerBI).
2. **Slowly Changing Dimensions (SCD)**: Khi khách hàng đổi địa chỉ từ "Hà Nội" sang "TP.HCM". Làm sao để báo cáo lịch sử năm ngoái vẫn tính doanh thu cho "Hà Nội", còn báo cáo năm nay tính cho "TP.HCM"? Cần dùng SCD Type 2.
3. **Data Vault**: Dành riêng cho các tập đoàn khổng lồ (Ngân hàng, Viễn thông) với hàng trăm nguồn dữ liệu khác nhau cần đổ về chung một Data Warehouse mà không làm vỡ cấu trúc.

**Không nên làm (Anti-patterns):**
- **Dùng Snowflake Schema trong Data Warehouse hiện đại**: Các Cloud Data Warehouse như BigQuery tính tiền theo lượng dữ liệu quét (Scan bytes), ổ cứng thì rẻ bèo. Đừng cố chuẩn hóa bảng Dimension để "tiết kiệm ổ cứng", vì việc `JOIN` nhiều bảng sẽ làm tốn CPU và khiến câu query chậm hơn rất nhiều. Hãy giữ nguyên Star Schema.

</details>

1. **Star Schema**: The gold standard for most Data Warehouses (Snowflake, BigQuery) and Data Marts. Feeds directly into BI Tools (Tableau, PowerBI).
2. **Slowly Changing Dimensions (SCD)**: When a customer moves from "New York" to "Texas". How do you ensure last year's reports still attribute revenue to "New York", but this year's to "Texas"? You use SCD Type 2.
3. **Data Vault**: Reserved for massive enterprises (Banking, Telecom) with hundreds of disparate data sources that need to be integrated into a central Enterprise Data Warehouse (EDW) without breaking existing schemas.

### Anti-Patterns
- **Using Snowflake Schema in Modern Cloud DWHs**: Cloud Data Warehouses (like BigQuery or Snowflake) charge by compute/scanned bytes, and storage is dirt cheap. Do not normalize dimensions to "save space", because adding `JOIN`s will spike your CPU usage and slow down queries. Stick to Star Schema (denormalized).

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất:**
1. **Khóa đại diện (Surrogate Keys)**: Đừng bao giờ dùng ID của hệ thống gốc (Business Key) làm Khóa chính trong Data Warehouse. Hãy luôn tạo ra một cột ID mới tự tăng (ví dụ `customer_key = 1, 2, 3...`) trong Data Warehouse. Điều này giúp xử lý SCD Type 2 dễ dàng (1 khách hàng có thể có 2 dòng dữ liệu với 2 địa chỉ khác nhau).
2. **Hiểu rõ SCD Type 1 vs Type 2**:
   - **Type 1 (Ghi đè)**: Khách hàng đổi tên bị sai chính tả. Cập nhật thẳng vào DB, mất dữ liệu cũ. Dễ làm.
   - **Type 2 (Lưu lịch sử)**: Khách hàng đổi cấp bậc từ Silver lên Gold. Tạo một dòng MỚI trong DB. Dòng cũ set `is_active = false` và `end_date = hôm nay`. Dòng mới set `is_active = true`. Rất quan trọng cho báo cáo tài chính!
3. **Mô hình OBt (One Big Table)**: Với các hệ thống cột (Columnar Database) cực mạnh như BigQuery, xu hướng hiện tại đôi khi bỏ qua luôn Star Schema và nhét toàn bộ Fact + Dimension vào 1 bảng khổng lồ chứa 100 cột. Tốc độ đọc sẽ đạt mức tối đa vì không có bất kỳ lệnh JOIN nào.

**Cạm bẫy:**
1. **Fact-to-Fact JOINs**: Tuyệt đối tránh JOIN 2 bảng Fact với nhau (ví dụ: `fact_sales` JOIN `fact_inventory`). Nó sẽ sinh ra thảm họa Cartesian Product (Dữ liệu bị nhân lên vô tận). Hãy dùng kỹ thuật Drill-across (Aggregate cả 2 bảng độc lập rồi mới gộp lại).

</details>

### Best Practices
1. **Always use Surrogate Keys**: Never use the source system's ID (Business Key) as the Primary Key in your Data Warehouse. Always generate a new, autoincrementing ID (e.g., `customer_sk = 1, 2, 3...`). This is mandatory for handling SCD Type 2 (since one customer will have multiple rows for historical states).
2. **Mastering SCD Types**:
   - **Type 1 (Overwrite)**: Fixing a typo in a name. Overwrite the row. Old data is lost forever. Simple.
   - **Type 2 (Add new row)**: Customer upgrades from Silver to Gold tier. Add a NEW row. Set the old row's `is_active = false` and `valid_to = today`. Set new row's `is_active = true`. Critical for accurate historical reporting!
3. **OBT (One Big Table) approach**: In modern Columnar Databases (like BigQuery), there is a trend to bypass Star Schema entirely and denormalize everything (Fact + all Dimensions) into a single 100-column table. Since there are zero `JOIN`s, query performance is unparalleled.

### Common Pitfalls
1. **Fact-to-Fact JOINs**: Never join two fact tables directly (e.g., joining `fact_sales` directly to `fact_inventory`). This creates massive Cartesian Products (data explosion). Instead, use the Drill-Across technique: Aggregate both fact tables independently using a conformed dimension, then join the aggregated results.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là ví dụ dùng Python (PySpark) để xử lý logic Slowly Changing Dimension (SCD) Type 2. Đoạn code này so sánh dữ liệu mới đến (New Data) với dữ liệu cũ đang có (Existing Dimension). Nếu có sự thay đổi, nó sẽ vô hiệu hóa dòng cũ và chèn thêm dòng mới.

</details>

### Implementing SCD Type 2 using PySpark (Python 3.11+)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_date, when

spark = SparkSession.builder.appName("SCD_Type2_Example").getOrCreate()

# 1. Load the existing Dimension Table (from Data Lake / Warehouse)
existing_dim = spark.createDataFrame([
    (101, "CUST-01", "John Doe", "New York", "2023-01-01", "9999-12-31", True)
], ["customer_sk", "customer_id", "name", "city", "valid_from", "valid_to", "is_active"])

# 2. Load the daily incoming updates (CDC or Daily Batch)
incoming_updates = spark.createDataFrame([
    ("CUST-01", "John Doe", "Texas") # John moved to Texas!
], ["customer_id", "name", "city"])

# 3. Identify records that changed
# Join on Business Key (customer_id)
joined_df = existing_dim.filter(col("is_active") == True) \
    .join(incoming_updates, "customer_id", "inner") \
    .filter(existing_dim.city != incoming_updates.city) # City changed!

# 4. Expire the old records
expired_records = joined_df.select(existing_dim["*"]) \
    .withColumn("is_active", lit(False)) \
    .withColumn("valid_to", current_date())

# 5. Insert the new active records
new_records = joined_df.select(
    lit(102).alias("customer_sk"), # In reality, use a surrogate key generator / UUID
    "customer_id",
    incoming_updates["name"],
    incoming_updates["city"],
    current_date().alias("valid_from"),
    lit("9999-12-31").alias("valid_to"),
    lit(True).alias("is_active")
)

# 6. Union and write back to storage (Delta Lake/Iceberg handles this MERGE beautifully)
final_dim = existing_dim.filter(col("customer_id") != "CUST-01") \
    .union(expired_records) \
    .union(new_records)

final_dim.show()
# +-----------+-----------+--------+--------+----------+----------+---------+
# |customer_sk|customer_id|    name|    city|valid_from|  valid_to|is_active|
# +-----------+-----------+--------+--------+----------+----------+---------+
# |        101|    CUST-01|John Doe|New York|2023-01-01|2026-06-27|    false|
# |        102|    CUST-01|John Doe|   Texas|2026-06-27|9999-12-31|     true|
# +-----------+-----------+--------+--------+----------+----------+---------+
```

---

## Related Topics

- [ETL vs ELT](../02-data-ingestion/etl-vs-elt.md) — How data lands into these dimensional models.
- [Data Lakehouse Architecture](../04-data-storage/lakehouse-and-acid-transactions.md) — The modern storage engine where these schemas live (e.g., Delta Lake).
- [Database Fundamentals](../../01-fundamentals/database/README.md) — Basic differences between OLAP and OLTP indexing strategies.
