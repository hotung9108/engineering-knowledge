# SQL Fundamentals: ACID, Normalization, and Joins

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Cơ sở dữ liệu quan hệ (RDBMS) và ngôn ngữ truy vấn cấu trúc (SQL) là xương sống của 90% hệ thống phần mềm doanh nghiệp trong suốt 40 năm qua. Tại sao nó lại vô đối đến vậy? Vì nó sở hữu các tiêu chuẩn cực kỳ khắt khe về tính toàn vẹn dữ liệu (Định lý ACID), cách tổ chức dữ liệu chuẩn hóa (Normalization) để không bị dư thừa, và sức mạnh liên kết các bảng cực mượt (Joins).

</details>

> **Summary**: Relational Database Management Systems (RDBMS) and the Structured Query Language (SQL) have been the undisputed architectural backbone of Enterprise software for 40 years. Their enduring supremacy stems from mathematically rigorous paradigms: ensuring absolute transaction integrity via **ACID** properties, eradicating data redundancy via **Normalization**, and effortlessly fusing relational datasets using declarative **Joins**.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang điều hành một Ngân hàng và phải ghi chép sổ sách:
- **ACID (Giao dịch hoàn hảo)**: Bạn chuyển 100k cho bạn của bạn. Ngân hàng trừ 100k của bạn, nhưng lúc chuẩn bị cộng tiền cho bạn kia thì... cúp điện! Chuyện gì xảy ra? SQL đảm bảo: Hoặc là giao dịch thành công trọn vẹn, hoặc là HỦY TOÀN BỘ (trả lại 100k cho bạn). Tuyệt đối không có chuyện trừ tiền người này mà không cộng tiền người kia.
- **Normalization (Dọn dẹp sổ sách)**: Thay vì mỗi lần khách hàng giao dịch bạn phải ghi lại cả Tên, Địa chỉ, Số điện thoại dài ngoằng (Dư thừa), bạn chỉ cần gán cho khách hàng một cái "Mã Số Căn Cước" (Primary Key). Khi giao dịch, chỉ ghi Mã Số đó thôi.
- **Joins (Gộp sổ)**: Khi sếp yêu cầu xem báo cáo, bạn lấy cuốn "Sổ giao dịch" (chỉ có mã số), đem so sánh với cuốn "Sổ thông tin khách hàng" để ghép tên của họ vào báo cáo cuối cùng.

</details>

Imagine you are managing the central ledger for a highly regulated Bank.
- **ACID (Transaction Integrity)**: You initiate a wire transfer of $100 to a friend. The bank deducts $100 from your account, but milliseconds before crediting your friend's account, a power outage crashes the server! What happens? SQL guarantees an all-or-nothing outcome: Either the entire transaction succeeds, or it fully Rolls Back, refunding your $100. Money is never magically lost in transit.
- **Normalization (Deduplication)**: Instead of writing the Customer's Full Name, Address, and Phone Number onto every single transaction receipt (wasting massive amounts of ink and paper), you assign the Customer a unique "ID Number" (Primary Key). Transactions only record this tiny ID.
- **Joins (Reconstruction)**: When the CEO demands a readable report, you physically place the "Transaction Ledger" next to the "Customer ID Ledger", linking the IDs to retrieve their Full Names for the final presentation.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Định lý ACID**: 4 chữ cái vàng định nghĩa sự an toàn của Transaction (Giao dịch).
- **A**tomicity (Tính nguyên tử): All or Nothing. Hoặc thành công cả cụm, hoặc thất bại hết.
- **C**onsistency (Tính nhất quán): Dữ liệu luôn tuân thủ các Ràng buộc (Ví dụ: Số dư không được âm).
- **I**solation (Tính cô lập): 2 giao dịch diễn ra cùng lúc không được dẫm chân lên nhau.
- **D**urability (Tính bền vững): Khi giao dịch đã được xác nhận (Committed), rút phích cắm điện server cũng không làm mất dữ liệu.

**2. Normalization (Chuẩn hóa)**: Quy trình tách một bảng khổng lồ thành nhiều bảng nhỏ, nối với nhau bằng Khóa chính (Primary Key) và Khóa ngoại (Foreign Key) để đảm bảo không bị lặp lại dữ liệu (Data Anomaly).

**3. Joins (Kết nối bảng)**: Cú pháp SQL để gộp 2 bảng lại với nhau. Gồm `INNER JOIN` (Chỉ lấy phần chung), `LEFT JOIN` (Lấy hết bảng trái, bảng phải thiếu thì điền NULL), v.v.

</details>

**1. The ACID Properties**: The unshakeable pillars of Relational Transactions.
- **A**tomicity: *All or Nothing*. A transaction consisting of 5 SQL statements must succeed entirely, or fail completely (Rollback). No partial execution.
- **C**onsistency: The database must strictly transition from one valid state to another, enforcing all Schema constraints (e.g., Foreign Keys, UNIQUE constraints, NOT NULL).
- **I**solation: Concurrent transactions executing simultaneously must behave as if they were executing sequentially. One transaction cannot read the "half-finished" dirty data of another.
- **D**urability: Once a `COMMIT` is successful, the data is permanently physically written to non-volatile storage (SSD/HDD). Pulling the power plug on the server will not erase it.

**2. Normalization**: A structural design process aiming to reduce data redundancy and eliminate Modification Anomalies. It involves dividing large, flat tables into multiple tightly-focused tables, deeply interlinked via **Primary Keys (PK)** and **Foreign Keys (FK)**.

**3. SQL Joins**: Declarative syntax used to fuse tables back together during read operations based on relational keys. The primary variants are `INNER JOIN` (Intersection), `LEFT JOIN` (Preserves all rows from the Left table), and `FULL OUTER JOIN` (Union).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

SQL sinh ra để giải quyết thảm họa **Cập nhật sai lệch (Update Anomaly)** của việc lưu file tĩnh (như Excel).
Giả sử bạn bán hàng. Trong file Excel, có 50 dòng ghi khách hàng mua đồ, cột Tên đều ghi là "Nguyễn Văn A", cột Địa chỉ ghi "Hà Nội".
Hôm sau, khách đổi địa chỉ sang "TP.HCM". Bạn phải đi tìm và sửa bằng tay 50 dòng đó! Nếu sửa sót 1 dòng, dữ liệu của bạn bị mâu thuẫn (Inconsistent).
Với Normalization của SQL, bảng Giao dịch chỉ lưu Khóa ngoại `user_id = 1`. Bạn chỉ cần Update địa chỉ của `user_id = 1` ở bảng User ĐÚNG 1 LẦN DUY NHẤT.

</details>

SQL Relational schemas were mathematically engineered (based on Edgar Codd's Relational Algebra) to eradicate the **Update Anomaly** inherent in flat-file storage (like Excel spreadsheets).
Consider an E-commerce spreadsheet. 50 orders are logged. Every single row duplicates the Customer's Name ("John Doe") and Address ("New York").
Tomorrow, the customer moves to "California". You must manually find and update all 50 rows. If you miss exactly 1 row, your database is mathematically corrupted (Inconsistent State).
With SQL Normalization (3rd Normal Form), the Orders table only stores a tiny integer Foreign Key (`customer_id = 42`). When the customer moves, you execute an `UPDATE` on the `Customers` table *exactly once*. Data integrity is bulletproof.

---

## Layer 3: Without vs. With Comparison (Compare)

### Data Anomalies vs 3rd Normal Form (3NF)

| Issue | Un-normalized Flat Table (Excel style) | 3rd Normal Form (SQL Database) |
|---|---|---|
| **Update Anomaly** | Changing a Department Name requires updating 1,000 employee rows. Risk of typos. | Update the name in the `Departments` table exactly once. |
| **Insert Anomaly** | Cannot add a new Department to the table until at least one employee is hired into it. | `Departments` table is totally independent. Insert freely. |
| **Delete Anomaly** | Firing the last employee in the "Physics" department accidentally deletes the fact that the "Physics" department ever existed! | Deleting an Employee only removes the FK. The `Department` row remains perfectly intact. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **PostgreSQL / MySQL / Oracle**: Các hệ quản trị CSDL quan hệ khổng lồ.
- **Bắt buộc dùng SQL RDBMS**: Hệ thống Ngân hàng, Sàn thương mại điện tử (Shopee, Tiki), Hệ thống quản lý kho (ERP), Hệ thống tính lương nhân sự. Bất cứ nơi nào mà dữ liệu bị sai lệch có thể dẫn đến việc bạn phải đi tù hoặc mất tiền tỷ.
- **Khi nào KHÔNG dùng SQL**: Lưu trữ log file (hàng tỷ dòng mỗi ngày không cần quan hệ với nhau), Phân tích Big Data phi cấu trúc. (Trường hợp này dùng NoSQL).

</details>

- **The Big Three RDBMS Titans**: **PostgreSQL** (The modern open-source King), **MySQL** (The legacy web King), and **Oracle** (The ultra-expensive Enterprise King).
- **Mandatory SQL Domains**: Financial Ledgers, Banking Systems, E-commerce Checkout pipelines (Inventory decrementing must be strongly ACID-compliant), Healthcare Records, and HR Payroll systems. You deploy SQL anywhere that a data inconsistency anomaly would result in catastrophic financial loss or massive legal liability.
- **When NOT to use SQL**: Rapid ingestion of billions of unstructured IoT sensor logs, caching session tokens, or massive graph traversal (Social Network friend-of-a-friend queries). These demand specialized NoSQL paradigms.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Transaction Phải Ngắn**: Đừng bao giờ mở Transaction, làm vài câu Query, gọi API sang một Server khác (mất 5 giây), rồi mới Commit. Lúc bạn đang giữ Transaction, database sẽ khóa (Lock) các hàng dữ liệu lại. Các user khác muốn mua hàng sẽ bị treo máy (Deadlock). Khóa càng ngắn càng tốt!
2. **Luôn dùng Parameterized Queries (Chống Hack SQLi)**: Nếu bạn cộng chuỗi để làm câu SQL: `SELECT * FROM users WHERE name = '` + name + `'`. Hacker nhập vào tên là `' OR 1=1; DROP TABLE users;--`. Lập tức database của bạn bị xóa sạch (Lỗi SQL Injection). Hãy luôn để Framework ORM tự động map parameter cho bạn.

</details>

1. **Keep Transactions Razor Thin**: Never execute a `BEGIN TRANSACTION`, perform a SQL `UPDATE`, and then execute a slow network HTTP call to a 3rd party API (taking 5 seconds) before issuing the `COMMIT`. During those 5 seconds, the database holds a Row-Level Lock. All other concurrent users attempting to buy that item will freeze indefinitely, destroying your application's throughput. Transactions must be purely algorithmic and execute in milliseconds.
2. **Mandatory Parameterized Queries (Anti-SQLi)**: Never physically concatenate user input into a raw SQL String. 
   `"SELECT * FROM users WHERE email = '" + userInput + "';"`
   A malicious user submits `admin@x.com'; DROP TABLE users;--`. The database dutifully executes the deletion, evaporating your company (SQL Injection). Always utilize Parameterized Queries (`?` placeholders) or robust ORMs (Hibernate/Prisma) which automatically sanitize inputs.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **N+1 Query Problem**: Lỗi kinh điển nhất khi code Web. Bạn viết code in ra danh sách 10 bài viết (1 Câu SQL). Sau đó, mỗi bài viết bạn lại gọi thêm 1 câu SQL để lấy tên Tác giả. Tổng cộng mất 1 + 10 = 11 câu SQL. Nếu in 100 bài, mất 101 câu SQL. Database sẽ nổ tung! (Cách giải quyết: Dùng `JOIN` để gom 2 bảng lại chỉ bằng ĐÚNG 1 CÂU SQL duy nhất).
2. **Lạm dụng LEFT JOIN vô tội vạ**: Khi báo cáo cần dữ liệu từ 10 bảng, dev Junior thường lười và cứ nã `LEFT JOIN` nguyên cả 10 bảng. Việc gộp quá nhiều bảng làm thuật toán (Cartesian product) phình to khủng khiếp, một câu query tốn mất 30 phút mới chạy xong.

</details>

1. **The N+1 Query Problem**: The most catastrophic and widespread performance bug in backend engineering (caused heavily by ORMs like Hibernate or Eloquent). 
   - *The Error*: You execute 1 query to fetch a list of 100 `Orders`. Then, in a `for-loop`, your code automatically executes a separate query to fetch the `Customer` for each order. You have executed 101 separate network roundtrips to the database. The latency multiplier crushes the server.
   - *The Fix*: Explicitly instruct the ORM to "Eager Load" using a single SQL `JOIN`. Execute exactly 1 query to fetch everything simultaneously.
2. **Cartesian Product via Blind Joins**: Junior engineers tasked with building an analytical report will naively chain 15 `LEFT JOINS` across massive tables without understanding the underlying matrix multiplication logic. The database optimizer collapses, attempting to construct a temporary result set in memory containing trillions of theoretical combinations, eventually crashing the server with a Memory/Temp Space Exhaustion error.

---

## Related Topics

- For designing massive data models efficiently, read **[Database Design & Schema](./database-design.md)**.
- To make these joins run lightning fast, see **[Query Optimization & Indexes](./query-optimization.md)**.
- For datasets where ACID compliance is overkill, explore **[NoSQL Fundamentals](./nosql-fundamentals.md)**.
