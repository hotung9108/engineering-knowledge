# Query Optimization & Indexes

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi CSDL chỉ có 1,000 dòng, bạn viết câu lệnh SQL tệ đến mấy nó cũng chạy nhanh. Nhưng khi có 10 triệu dòng, một câu lệnh SQL thiếu tối ưu có thể làm sập toàn bộ hệ thống vì nó vét sạch RAM và CPU để tìm kiếm. **Indexing (Đánh chỉ mục)** và **Query Optimization (Tối ưu truy vấn)** là kỹ thuật sống còn để thu hẹp phạm vi tìm kiếm, giúp SQL trả về kết quả trong 0.01 giây thay vì 10 phút.

</details>

> **Summary**: When a database contains only 1,000 rows, even the most egregiously inefficient SQL queries execute instantaneously. However, as the table scales to 10 million rows, a poorly optimized query will trigger a Full Table Scan, devouring all CPU/RAM resources and potentially crashing the database cluster. **Indexing (B-Trees)** and **Query Optimization** are the absolute most critical survival skills for Backend Engineers. They mathematically reduce the search space, accelerating query response times from 10 minutes down to 10 milliseconds.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang tìm từ "Khủng long" trong một cuốn Từ điển dày 10,000 trang.
- **Không có Index (Full Table Scan)**: Bạn lật từng trang từ trang 1 đến trang 10,000 để tìm chữ "Khủng long". Bạn mất 5 ngày để tìm ra. Cực kỳ thảm họa.
- **Có Index (Mục lục B-Tree)**: Bạn lật ra phần Mục lục ở cuối sách. Thấy ghi chữ "K - Trang 500". Bạn lật một phát tới thẳng trang 500. Bạn chỉ mất 5 giây! Indexing trong SQL chính là việc tạo ra cái Mục lục này.

</details>

Imagine you are tasked with finding the word "Dinosaur" in a massive 10,000-page Encyclopedia.
- **Without an Index (A Full Table Scan)**: You must physically read every single word on Page 1, then Page 2, sequentially all the way to Page 10,000 until you find the word. This takes you 5 days. It is catastrophic.
- **With an Index (A B-Tree structure)**: You flip directly to the Alphabetical Index at the back of the book. You look up the letter "D", which points you directly to "Page 500". You instantly jump to Page 500. It took 5 seconds. This is exactly how SQL Indexing bypasses massive datasets.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Index (Chỉ mục)**: Là một cấu trúc dữ liệu bổ sung (thường dùng thuật toán Cây nhị phân B-Tree hoặc Hash Table) được gắn vào một hoặc nhiều Cột trong bảng. Nó được sắp xếp sẵn để CSDL tìm kiếm cực nhanh (Tốc độ $O(\log N)$ thay vì $O(N)$).
**2. Query Optimizer (Bộ tối ưu hóa)**: Một "trí tuệ nhân tạo" nhỏ nằm bên trong SQL Engine. Khi bạn gõ lệnh `SELECT`, nó sẽ tự tính toán xem "Nên dùng Index nào? Nên duyệt bảng nào trước?" để tạo ra một **Execution Plan (Kế hoạch thực thi)** tối ưu nhất.
**3. EXPLAIN**: Một lệnh thần thánh. Đặt chữ `EXPLAIN` trước câu SQL của bạn, hệ thống sẽ in ra bản Kế hoạch thực thi để bạn biết câu SQL của mình chạy nhanh hay chậm.

</details>

**1. Database Index**: A highly optimized, auxiliary data structure (typically a **B-Tree** or Hash Table) attached to one or more columns in a table. It maintains a strictly sorted duplicate of the column data, alongside pointers to the actual row location on the hard drive. It transforms a linear $O(N)$ search time into a logarithmic $O(\log N)$ search time.
**2. The Query Optimizer**: The invisible "brain" within the SQL Engine. When you submit a `SELECT` statement, it parses the query, analyzes statistical data about the tables, and generates multiple theoretical execution paths. It then selects the cheapest, fastest **Execution Plan**.
**3. The `EXPLAIN` Command**: The ultimate diagnostic tool. Prepending `EXPLAIN ANALYZE` to your SQL query forces the Database to explicitly reveal the chosen Execution Plan, highlighting exactly whether it utilized an Index or embarrassingly resorted to a Full Table Scan.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Nút thắt cổ chai I/O (Disk I/O Bottleneck)**
Ổ cứng (HDD/SSD) đọc dữ liệu chậm hơn CPU cả triệu lần. Lệnh `SELECT * FROM users WHERE age = 25` mà không có Index sẽ ép CSDL phải ĐỌC TOÀN BỘ 10 triệu dòng từ ổ cứng lên RAM để kiểm tra xem ai 25 tuổi. Gây nghẽn toàn bộ hệ thống.
Tạo một Index trên cột `age`, dữ liệu đã được CSDL ngầm sắp xếp sẵn thành hình cái cây. CSDL chỉ cần duyệt cây trong 3 bước là tìm thấy đúng cái dòng chứa số 25, không cần phải đọc 9,999,997 dòng rác kia lên RAM nữa.

</details>

**The Disk I/O Bottleneck**
Physical Disk operations (even on NVMe SSDs) are mathematically the slowest operations in computing, magnitudes slower than CPU L1 Cache. 
Executing `SELECT * FROM users WHERE email = 'bob@x.com'` on an un-indexed table containing 10 million rows triggers a **Sequential Scan (Full Table Scan)**. The Database must physically read all 10 million rows from the hard drive into RAM to evaluate the `WHERE` clause. This completely exhausts memory and Disk I/O.
By indexing the `email` column, the database simply traverses a tiny B-Tree residing entirely in RAM, reaching the exact hard drive pointer in 4 jumps, entirely bypassing millions of unnecessary disk reads.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt khi chạy lệnh EXPLAIN cho câu truy vấn trên bảng 1 triệu người dùng.
</details>

Analyzing the output of `EXPLAIN ANALYZE` on a 1-million-row `users` table.

### Query WITHOUT Index
The database has no idea where "John" lives. It must inspect every house on the street.
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'John';
```
**Output:**
```text
-> Seq Scan on users (cost=0.00..150000.00 rows=1 width=104)
-> Filter: (name = 'John')
-> Execution Time: 450.23 ms   -- TERRIBLE (Half a second to find 1 row)
```

### Query WITH Index (B-Tree)
The database looks at the alphabetized index, instantly jumping to the "J" section.
```sql
CREATE INDEX idx_user_name ON users(name);
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'John';
```
**Output:**
```text
-> Index Scan using idx_user_name on users (cost=0.00..4.00 rows=1 width=104)
-> Execution Time: 0.05 ms     -- PERFECT (10,000x Faster!)
```

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Composite Index (Index Gộp)**: Khi bạn hay search kiểu `WHERE first_name = 'A' AND last_name = 'B'`. Phải tạo Index gộp cho cả 2 cột này `CREATE INDEX idx_name ON users(first_name, last_name)`.
- **Unique Index (Index Duy nhất)**: Vừa giúp search nhanh, vừa cấm không cho trùng lặp. Cột `Email` hoặc `CMND` BẮT BUỘC phải dùng Unique Index.
- **B-Tree vs Hash Index**: B-Tree dùng cho phép so sánh Lớn hơn/Nhỏ hơn (Ví dụ `age > 20`). Hash Index chỉ dùng để tìm chính xác dấu Bằng (Ví dụ `email = 'a@a.com'`). Tốc độ Hash Index là tuyệt đối $O(1)$.

</details>

- **Composite Indexes**: When querying multiple columns simultaneously (e.g., `WHERE status = 'ACTIVE' AND created_at > '2023-01-01'`). A single-column index on `status` is insufficient. You must create a multi-column B-Tree index: `CREATE INDEX idx_status_date ON orders(status, created_at)`.
- **Unique Indexes**: Implements an aggressive constraint at the B-Tree level. The database physically prevents duplicate entries. Absolutely mandatory for `email`, `username`, or `SSN` columns to guarantee data integrity alongside lookup performance.
- **B-Tree vs Hash Indexes**: A B-Tree physically sorts data, meaning it dominates Range Queries (`WHERE age BETWEEN 20 AND 30`). A Hash Index uses a mathematical hashing function, meaning it can ONLY process strict Equality Queries (`WHERE id = 5`), but it does so in pure $O(1)$ time.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiệu ứng trái rẽ của Composite Index (Left-most Prefix Rule)**: Nếu bạn tạo Index gộp `(A, B, C)`. Bạn CÓ THỂ dùng nó để search `A`, hoặc `A và B`. Nhưng bạn KHÔNG THỂ search bằng `B và C` (Bỏ qua A). Quy tắc là B-Tree phải đi từ gốc (trái sang phải).
2. **Nghệ thuật chọn Cột để Index (Cardinality)**: Đừng bao giờ Index cột Giới tính (Gender: Nam/Nữ). Cột này chỉ có 2 giá trị. Khi bạn truy vấn `WHERE gender = 'Male'`, nó ra hẳn 50% cái bảng. Index bị vô hiệu hóa vì CSDL thấy "thà đọc nguyên bảng còn nhanh hơn mò mẫm qua Index". Hãy Index những cột có tính "Độc nhất cao" (Email, ID).

</details>

1. **Master the Left-Most Prefix Rule**: The most common misunderstanding of Composite Indexes. If you create an index on `(last_name, first_name)`. A query for `WHERE last_name = 'Smith'` will perfectly utilize the index. A query for `WHERE first_name = 'John'` will **COMPLETELY IGNORE THE INDEX** and trigger a Full Table Scan. A B-Tree must be traversed strictly from the root (left to right). You cannot skip the first node.
2. **Understand Cardinality**: Never place an index on a low-cardinality column (e.g., a `boolean is_active` column or a `gender` column). If a column only has 2 possible values, querying it returns 50% of the entire table. The Query Optimizer will actively reject the Index and execute a Full Table Scan anyway, because jumping back and forth between the Index and the Hard Drive for 5 million rows is slower than just sweeping the entire disk linearly.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **"Đánh Index cho mọi cột cho chắc ăn"**: Index CỰC KỲ TỐN KÉM. Mỗi khi bạn gõ lệnh `INSERT` hoặc `UPDATE` một dòng dữ liệu, CSDL không chỉ ghi dữ liệu đó vào Bảng, mà nó phải đi CẬP NHẬT LẠI cái cây B-Tree của Index. Nếu 1 bảng có 10 Index, tốc độ ghi (Write) của bạn sẽ bị chậm đi 10 lần. Chỉ đánh Index trên cột nào hay xuất hiện trong mệnh đề `WHERE` hoặc `JOIN`.
2. **Bọc hàm vào cột làm mù Index**: Bạn viết lệnh `WHERE YEAR(created_at) = 2023`. Bùm! Full Table Scan. Dù cột `created_at` có Index, nhưng khi bạn bọc một hàm `YEAR()` quanh nó, CSDL bị mù, nó phải đọc toàn bộ dòng lên tính toán rồi mới so sánh. Phải viết lại thành `WHERE created_at >= '2023-01-01' AND created_at < '2024-01-01'`.

</details>

1. **The Over-Indexing Death Spiral**: Junior DBAs often mistakenly place an index on every single column to "make everything fast". **Indexes severely degrade Write Performance**. Every time an `INSERT`, `UPDATE`, or `DELETE` executes, the database must halt and physically re-balance the B-Tree for every single Index attached to the table. 15 indexes on a high-traffic table will throttle Write throughput to near zero.
2. **Sargable Violations (Function Wrapping)**: Writing `WHERE LOWER(email) = 'john@x.com'` or `WHERE YEAR(date) = 2024`. Because you mutated the column using a function *before* evaluation, the database cannot use the sorted B-Tree. It must blindly execute the function on every single row (Full Table Scan). Always mutate the right side of the equation, leaving the indexed column pristine (e.g., `WHERE date >= '2024-01-01'`).

---

## Related Topics

- For designing tables correctly before applying indexes, see **[Database Design & Schema](./database-design.md)**.
- See how Indexing structures differ in distributed environments like **[NoSQL Fundamentals](./nosql-fundamentals.md)**.
