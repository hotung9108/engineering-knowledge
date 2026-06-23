# MySQL

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu PostgreSQL là một nhà bác học uyên bác và tuân thủ nguyên tắc, thì **MySQL** là một anh công nhân cần mẫn, thân thiện và cực kì phổ biến. Ra đời từ giữa những năm 90, MySQL đã trở thành cột sống của hệ sinh thái Web đời đầu (nhờ sự trỗi dậy của LAMP stack: Linux, Apache, MySQL, PHP). Khắp nơi trên thế giới, từ những trang blog WordPress nhỏ bé cho đến những gã khổng lồ như Facebook hay Uber thời kỳ đầu, đều dùng MySQL. Dù hiện tại PostgreSQL đang dần chiếm ưu thế ở các dự án mới vì nhiều tính năng phức tạp, MySQL vẫn giữ vững ngôi vương là Hệ quản trị Cơ sở dữ liệu Quan hệ (RDBMS) mã nguồn mở được sử dụng rộng rãi nhất thế giới nhờ tính ổn định, dễ học và cộng đồng hỗ trợ khổng lồ.

</details>

> **Summary**: While PostgreSQL is renowned for its strict standard compliance and advanced feature set, **MySQL** is the undisputed king of web ubiquity. Born in 1995, it became the default database for the early internet, riding the massive wave of the LAMP stack (Linux, Apache, MySQL, PHP). It powered the rise of WordPress, Joomla, and nearly every major web startup of the 2000s, including Facebook and Twitter. 
> MySQL prioritizes speed, reliability, and ease of use over strict SQL compliance. Its defining architectural feature is its Pluggable Storage Engine architecture (specifically `InnoDB`), which handles ACID compliance, row-level locking, and foreign keys. Although PostgreSQL is increasingly favored for complex, greenfield enterprise applications, MySQL remains the most widely deployed open-source Relational Database Management System (RDBMS) globally, sustained by an unparalleled ecosystem of tools, drivers, and operational knowledge.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn cần thuê một Người Kế Toán.
1. **PostgreSQL**: Một ông Kế toán già, siêu giỏi toán cao cấp. Mọi giấy tờ bạn đưa ông ấy đều bắt bạn phải điền chính xác từng dấu phẩy, sai 1 ly ông ấy trả lại hồ sơ không thèm làm. Rất an toàn, nhưng làm việc cùng hơi áp lực.
2. **MySQL**: Một anh Kế toán trẻ, vui vẻ và linh hoạt. Nếu bạn lỡ viết sai ngày tháng một chút xíu, anh ấy sẽ tự động đoán ý và sửa lại giúp bạn cho xong việc (mặc dù đôi khi sự "nhanh nhảu" này gây ra lỗi ngầm). Anh ấy tính toán cực nhanh, dễ nói chuyện, và đi đâu bạn cũng tìm được người biết làm việc với anh ấy.

</details>

Imagine hiring an Accountant for your store.
1. **PostgreSQL**: A brilliant, highly strict senior accountant. If you submit an expense report missing a single receipt, they instantly reject it. It guarantees 100% perfect financial records, but the bureaucracy slows you down.
2. **MySQL**: A fast, pragmatic accountant. If you hand them a receipt where the date is slightly smudged, they might just guess the date to get the paperwork filed quickly. This makes them incredibly fast and easy to work with for everyday tasks, even though their "silent conversions" can sometimes lead to subtle errors if you aren't careful.

---

## Layer 1: Core Architecture (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Kiến trúc của MySQL rất đặc biệt, nó chia làm 2 tầng rõ rệt:
1. **Tầng Máy chủ (Server Layer)**: Chịu trách nhiệm nhận kết nối mạng, kiểm tra mật khẩu, và Phân tích câu lệnh SQL của bạn (Xem có tối ưu không).
2. **Tầng Lưu trữ (Pluggable Storage Engines)**: Đây là phần "ăn tiền" của MySQL. Nó cho phép bạn thay phần "lõi" ghi đĩa. 
   - `InnoDB`: Lõi mặc định hiện nay. Hỗ trợ Transaction (Giao dịch ACID), khóa từng dòng (Row-level locking). 99% mọi người dùng cái này.
   - `MyISAM`: Lõi cũ. Chạy đọc siêu nhanh, nhưng không có Transaction, và khi ghi dữ liệu nó sẽ "Khóa toàn bộ bảng" (Table-level locking) làm nghẽn hệ thống.

</details>

MySQL's architecture is uniquely modular, conceptually divided into two distinct layers:
1. **The Server Layer (SQL Layer)**: This layer handles connection pooling, authentication, security, and query parsing/optimization. It is independent of how data is actually stored on disk.
2. **The Pluggable Storage Engine Layer**: This is MySQL's defining characteristic. You can choose different underlying algorithms for storing data on a per-table basis.
   - **`InnoDB`**: The modern default. It is a fully ACID-compliant transactional engine. It supports row-level locking, foreign key constraints, and crash recovery. You should almost exclusively use this.
   - **`MyISAM`**: The legacy engine. It does not support transactions or foreign keys. It uses table-level locking (meaning an `INSERT` blocks all other reads/writes to the entire table). It is only useful for highly specific, read-only analytical workloads.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao MySQL lại phủ sóng toàn cầu mạnh mẽ đến vậy?
1. **Dễ cài đặt và Quản lý**: Trong những năm 2000, việc cài Oracle DB tốn hàng tháng trời và hàng triệu đô la. Cài PostgreSQL thì phức tạp. MySQL chỉ mất 5 phút `apt-get install` là có ngay một cái Database nhẹ hều, cắm điện là chạy.
2. **Hiệu năng Đọc (Read Performance)**: Các trang web như Blog, Tin tức, Diễn đàn có đặc điểm là 90% là Đọc (Read), chỉ 10% là Ghi (Write). Kiến trúc của MySQL sinh ra để tối ưu hóa tốc độ đọc. Nó chạy cực kì nhanh và nhẹ nhàng trên các máy chủ cấu hình yếu.
3. **Mô hình Nhân bản (Replication) dễ dàng**: MySQL đi tiên phong trong việc cung cấp tính năng Master-Slave Replication rất dễ thiết lập. Giúp các công ty dễ dàng chia tải: 1 máy Master chuyên Ghi, 3 máy Slave chuyên Đọc.

</details>

Why did MySQL achieve global ubiquity, defeating older and arguably more mathematically pure databases?
1. **Developer Friction (Ease of Use)**: In the early web era, commercial databases (Oracle, DB2) cost millions and required PhDs to operate. PostgreSQL was highly academic and difficult to configure. MySQL was the "Database for the Rest of Us." It installed in seconds, consumed minimal RAM, and just worked out of the box with zero tuning.
2. **Optimized for Web Workloads (Read-Heavy)**: The internet is fundamentally read-heavy (90% reads, 10% writes). Think of reading blogs, browsing products, or loading profiles. MySQL's architecture was heavily optimized for lightning-fast reads, making it the perfect engine for Content Management Systems (WordPress) and early social networks.
3. **Pioneering Easy Replication**: Before advanced clustering existed, scaling a database was incredibly hard. MySQL made Asynchronous Master-Slave Replication extremely simple to set up. A startup could easily spin up one Master node for writes and five Read-Replica nodes to serve web traffic, achieving massive horizontal scale cheaply.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh triết lý xử lý dữ liệu (MySQL vs PostgreSQL).
</details>

Visualizing the "Strictness" philosophy (MySQL vs PostgreSQL).

| Metric | MySQL (Default behavior) | PostgreSQL |
|---|---|---|
| **Invalid Data Insertion** | You try to insert the string `'100abc'` into an `INTEGER` column. MySQL might silently truncate the string, insert `100`, and throw a minor warning. (Fast, but dangerous). | Postgres immediately throws an aggressive `ERROR: invalid input syntax` and aborts the entire transaction. (Strict and safe). |
| **Feature Set** | Focuses on raw speed for standard relational data. JSON support was added later as an afterthought. | Extremely feature-rich. Native, deeply optimized support for JSONB, Arrays, Geographic Data (PostGIS), and Custom Types. |

---

## Layer 4: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bật chế độ Strict Mode**: Điểm yếu lớn nhất của MySQL là sự "Dễ dãi" (Cho phép chèn dữ liệu sai lồng ghép). Điều này gây ra những lỗi ngầm khủng khiếp khi dữ liệu công ty phình to. BẮT BUỘC phải mở file cấu hình `my.cnf` và bật `sql_mode=STRICT_ALL_TABLES`. Lúc này, MySQL sẽ trở nên nghiêm khắc giống hệt PostgreSQL, sai dữ liệu là báo lỗi ngay lập tức.
2. **Tuyệt đối không dùng MyISAM**: Nếu bạn tiếp quản một hệ thống cũ, hãy kiểm tra xem các bảng đang dùng Storage Engine nào. Nếu thấy chữ `MyISAM`, hãy lên kế hoạch chuyển đổi (ALTER TABLE) sang `InnoDB` ngay lập tức. MyISAM có thể gây mất sạch dữ liệu nếu máy chủ đột ngột cúp điện.

</details>

1. **Enforce Strict SQL Mode**: Historically, MySQL's biggest criticism was "Silent Truncation". If you inserted a 20-character string into a `VARCHAR(10)` column, MySQL would silently chop off the last 10 characters and insert the data without crashing. This destroys data integrity. **Rule**: You MUST ensure your database is running with Strict Mode enabled (`sql_mode=STRICT_ALL_TABLES` or `STRICT_TRANS_TABLES`). This forces MySQL to act like a real database and violently reject invalid data. (Note: Modern versions of MySQL 8.0 have this enabled by default).
2. **Migrate away from MyISAM**: If you inherit a legacy MySQL 5.x database, the first audit you perform must be checking the Storage Engine of the tables. If any tables use `MyISAM`, they are ticking time bombs. `MyISAM` does not support crash recovery. A sudden power loss can permanently corrupt the table. You must migrate them to `InnoDB` (`ALTER TABLE name ENGINE=InnoDB;`).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lỗi Character Set (Ký tự rác Unicode)**: Đây là nỗi đau kinh điển nhất của người dùng MySQL. Mặc định ngày xưa, MySQL dùng bảng mã `utf8`. Nhưng chữ `utf8` của MySQL bị lỗi, nó chỉ hỗ trợ 3 bytes (Không lưu được các ký tự Emoji như 😭). Kết quả là khi khách hàng gõ Emoji vào, Database báo lỗi sập.
   - *Cách giải*: BẮT BUỘC khi tạo Database, phải khai báo bảng mã là `utf8mb4` (UTF-8 Max Bytes 4). Đây mới là chuẩn Unicode xịn lưu được mọi loại ngôn ngữ và Emoji trên thế giới.
2. **Khóa bảng ngầm định (Implicit Table Locks)**: Khi bạn dùng lệnh `ALTER TABLE` để thêm một cột mới vào bảng có 10 triệu dòng. MySQL có thể sẽ khóa cứng (Lock) toàn bộ cái bảng đó trong vòng 30 phút để cập nhật. Trong 30 phút đó, toàn bộ website của bạn sẽ bị sập vì không ai truy cập được Database. Hãy dùng các công cụ như `pt-online-schema-change` để đổi cấu trúc bảng mà không gây sập web.

</details>

1. **The `utf8` Emoji Catastrophe**: The most infamous historical quirk of MySQL. If you create a database using `CHARACTER SET utf8`, you naturally assume it supports standard Unicode. It does not. MySQL's `utf8` is fundamentally flawed; it only supports 3-byte characters. When a user tries to save an Emoji (which requires 4 bytes), the query crashes. **Rule**: You MUST explicitly configure your database, tables, and connection drivers to use `utf8mb4` (UTF-8 Max Bytes 4) to ensure absolute Unicode compliance.
2. **Blocking Schema Changes (ALTER TABLE)**: Modifying the schema of a massive table (e.g., adding a new column) in legacy MySQL versions requires locking the entire table and completely rebuilding it on disk. If the table is 50GB, this `ALTER TABLE` lock might last 2 hours, causing a complete Production outage. **Rule**: For large databases, never run direct `ALTER TABLE` statements during peak hours. Utilize Percona Toolkit's `pt-online-schema-change` or Ghost, which create a shadow copy of the table, sync it, and swap it with zero downtime.

---

## Related Topics

- For complex, enterprise-grade analytical queries, the modern trend is to migrate from MySQL to **[PostgreSQL](./postgresql.md)**.
- If you need to cache MySQL queries to handle massive web traffic, put **[Redis](./redis.md)** in front of it.
- To manage the deployment of your MySQL containers, use **[Kubernetes](../cloud-infra/kubernetes.md)**.
