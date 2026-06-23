# PostgreSQL

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: SQL là ngôn ngữ giao tiếp với Cơ sở dữ liệu Quan hệ, và **PostgreSQL** (hay gọi tắt là Postgres) là hệ quản trị cơ sở dữ liệu mã nguồn mở tiên tiến nhất thế giới. Trái ngược với MySQL được thiết kế cho sự tối giản và dễ dùng, Postgres được thiết kế cho Sự chặt chẽ, Tính năng nâng cao và Tuân thủ tuyệt đối chuẩn SQL. Nếu bạn cần tính tiền, quản lý giao dịch ngân hàng, phân tích dữ liệu địa lý (Bản đồ), hoặc thậm chí lưu trữ JSON linh hoạt như NoSQL, Postgres là lựa chọn hoàn hảo nhất. Nó được mệnh danh là "Chiếc dao găm Thụy Sĩ" của ngành dữ liệu vì khả năng mở rộng (Extensions) vô hạn của nó.

</details>

> **Summary**: While MySQL gained early dominance through ease of use and LAMP stack integration, **PostgreSQL** earned its reputation as the world's most advanced open-source Relational Database Management System (RDBMS). It is fundamentally engineered for extreme ACID compliance, rigorous data integrity, and strict adherence to SQL standards. PostgreSQL transcends traditional row-and-column storage; it is an Object-Relational database supporting complex data types (Arrays, UUIDs, Network Addresses) and hybrid NoSQL capabilities via its incredibly powerful `JSONB` column type. With a robust ecosystem of Extensions (like PostGIS for spatial data or pgvector for AI embeddings), PostgreSQL has become the undisputed default database for modern Cloud-Native applications, Fintech, and Enterprise SaaS.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn thuê một Kế toán viên.
1. **MySQL**: Là một anh kế toán nhanh nhẹn, dễ tính. Bạn đưa một tờ hóa đơn chữ xấu, anh ta ráng đoán chữ và nhập vào sổ. Bạn đưa chữ "Mười" vào ô Điểm số, anh ta tự động cắn răng chuyển nó thành số "10". Rất dễ làm việc chung, nhưng lâu lâu đoán sai làm hỏng sổ sách.
2. **PostgreSQL**: Là một Kế toán trưởng cực kì nguyên tắc, khó tính và sở hữu 10 bằng Đại học. Bạn đưa chữ "Mười" vào ô Điểm số, ông ta ném tờ giấy vào mặt bạn và hét lên: "Lỗi! Yêu cầu là Số thực (Float)". Tuy nhiên, ông ta có thể làm được những phép toán ma thuật: Bạn ném một bản đồ vào, ông ta tính được khoảng cách 2 điểm. Bạn ném một cục JSON lộn xộn vào, ông ta xếp gọn gàng vào kho mà vẫn tìm lại cực nhanh.

</details>

Imagine hiring a Bookkeeper for your business.
1. **MySQL**: A friendly, fast, and highly accommodating bookkeeper. If you accidentally write "Ten" in the numerical Salary column, they will try their best to silently cast it to the number `10`, or truncate it to `0`. It's very easy to work with, but this silent coercion can hide catastrophic accounting bugs.
2. **PostgreSQL**: A strict, uncompromising Chief Financial Officer. If you attempt to insert a string into an Integer column, the database violently rejects the transaction and throws a fatal error. However, this CFO is incredibly smart. You can hand them a spatial Map (Geospatial data) or a flexible JSON document, and they have specialized tools to index and query those bizarre formats with mathematical precision.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

PostgreSQL khác biệt ở 3 điểm cốt lõi:
1. **Tuân thủ ACID tuyệt đối**: Nó sinh ra để không bao giờ làm mất hoặc sai lệch dữ liệu. Nếu máy chủ cúp điện giữa chừng khi đang chuyển tiền, toàn bộ quá trình sẽ được hoàn tác (Rollback) sạch sẽ nhờ cơ chế WAL (Write-Ahead Logging).
2. **Kiểu dữ liệu phong phú (Rich Data Types)**: Trong MySQL, bạn chỉ có Số, Chữ, Ngày tháng. Trong Postgres, bạn có mảng (Array `[1, 2, 3]`), IP Mạng (`192.168.1.1`), UUID, và đặc biệt là JSONB. JSONB cho phép bạn lưu JSON và tìm kiếm bên trong cục JSON đó bằng thuật toán Index cực nhanh (Đánh bại cả MongoDB trong nhiều trường hợp).
3. **Kiến trúc Mở rộng (Extensions)**: Bạn có thể cài thêm "Plugin" vào Database. Nổi tiếng nhất là `PostGIS` biến Postgres thành hệ thống quản lý Bản đồ tốt nhất thế giới (Tính khoảng cách giữa 2 tọa độ GPS). Gần đây là `pgvector` giúp lưu trữ Vector AI.

</details>

PostgreSQL differentiates itself through three foundational architectural pillars:
1. **Uncompromising Data Integrity (ACID & MVCC)**: Postgres is paranoid about data loss. It utilizes Multi-Version Concurrency Control (MVCC) to ensure that database `READs` never block `WRITEs`, and `WRITEs` never block `READs`. Its Write-Ahead Log (WAL) guarantees that committed transactions are permanently durable even during catastrophic server power failures.
2. **Advanced Object-Relational Types**: Traditional databases only support primitives (Int, Varchar, Date). Postgres natively supports Arrays (`INT[]`), universally unique identifiers (`UUID`), Network Addresses (`CIDR`), and most importantly, Binary JSON (`JSONB`). `JSONB` allows developers to store unstructured NoSQL documents inside a Relational Database, and create specialized GIN Indexes to query deeply nested JSON keys at lightning speeds.
3. **The Extensibility Ecosystem**: Postgres is not just a database; it is a platform. It supports dynamic extensions. **PostGIS** transforms Postgres into a Geospatial engine capable of complex geographic polygon intersections. **pgvector** transforms it into a Vector Database for Machine Learning embeddings. **TimescaleDB** morphs it into a Time-Series database.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong thế giới hiện đại, các ứng dụng không chỉ lưu "Tên và Tuổi" nữa.
Bạn xây dựng một ứng dụng Giao đồ ăn (Food Delivery). Bạn cần:
1. Lưu thông tin Khách hàng và Đơn hàng chặt chẽ (Tính tiền phải chuẩn) $\rightarrow$ Cần SQL.
2. Lưu tọa độ của Shipper và tìm các Quán ăn trong bán kính 5km $\rightarrow$ Cần Bản đồ (Geospatial).
3. Lưu Lịch sử Cài đặt App (Mỗi người dùng bật/tắt các cấu hình khác nhau, cấu trúc không cố định) $\rightarrow$ Cần NoSQL (JSON).
Thay vì phải thuê 3 máy chủ chạy MySQL, Neo4J, và MongoDB. PostgreSQL tồn tại để **Gom tất cả mọi thứ vào một chỗ**. Nó có đủ chức năng để làm tốt cả 3 việc trên một cách xuất sắc, giúp kiến trúc hệ thống của bạn cực kì đơn giản.

</details>

PostgreSQL exists to prevent **Polyglot Persistence Fatigue**.
Historically, if an engineering team was building a Ride-Hailing application, they faced a nightmare: They needed MySQL for strict financial transactions, MongoDB for unstructured user preferences, and a specialized Geospatial engine to calculate driver distances. Managing data synchronization and distributed transactions across three wildly different databases is an architectural disaster.
PostgreSQL evolved to be the **"One Database to Rule Them All"**. Because of its mathematical rigor and infinite extensibility, a team can run their entire complex architecture on a single PostgreSQL cluster. It handles the ACID financial ledger seamlessly, parses unstructured `JSONB` user profiles faster than MongoDB, and calculates geospatial `PostGIS` radiuses in real-time. It massively simplifies infrastructure complexity.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc xử lý Dữ liệu Mảng (Arrays) và Dữ liệu linh hoạt (JSON). Ví dụ: Lưu danh sách Tag của một bài viết.
</details>

Visualizing Advanced Data Handling (MySQL vs PostgreSQL).

| Metric | Traditional SQL (MySQL 5.x) | PostgreSQL (`JSONB` & `Arrays`) |
|---|---|---|
| **Storing an Array of Tags**| You MUST create a separate `Tags` table and a junction table (`Post_Tags`). Requires heavy `JOIN` queries. | Add a single column: `tags TEXT[]`. Insert directly: `'{ "tech", "news" }'`. No joins needed. |
| **Storing Flexible Metadata** | Serialize to a massive string. You CANNOT query inside the string. | Store as `JSONB`. Query natively using `SELECT metadata->>'theme' FROM users`. |
| **Indexing JSON** | Impossible. Full Table Scan required. | Create a GIN Index. `CREATE INDEX ON users USING GIN (metadata)`. Millisecond searches. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Phần mềm B2B SaaS (Software as a Service)**: Gần như 100% các công ty khởi nghiệp SaaS hiện đại đều chọn Postgres làm cơ sở dữ liệu chính. Tính năng Multi-tenant (Nhiều công ty dùng chung 1 database nhưng chia RLS - Row Level Security) của Postgres quá mạnh mẽ và an toàn.
2. **Hệ thống Thông tin Địa lý (GIS) & Ride-Hailing**: Ứng dụng Grab, Uber, Gojek, hay Tinder (Tìm người quanh đây). Extension `PostGIS` giúp tìm kiếm: "Liệt kê 10 tài xế gần tôi nhất, sắp xếp theo khoảng cách, loại bỏ những người đang bị kẹt xe (Polygon giao cắt)".
3. **Cơ sở dữ liệu cho Trí tuệ nhân tạo (AI Vector DB)**: Với sự bùng nổ của ChatGPT (RAG), bạn cần lưu trữ dữ liệu văn bản dưới dạng Vector và tìm kiếm độ tương đồng (Similarity Search). Thay vì mua các Vector Database đắt đỏ như Pinecone, bạn chỉ cần cài Extension `pgvector` vào Postgres là xong.

</details>

1. **Enterprise SaaS & Multi-Tenant Architectures**: The absolute standard. Building modern SaaS applications (like Slack or Notion) requires robust data isolation between different customer organizations. PostgreSQL natively supports **Row-Level Security (RLS)**, allowing database administrators to write mathematical policies that invisibly block Tenant A from accidentally querying Tenant B's data, regardless of backend API bugs.
2. **Geospatial & Location-Based Services (LBS)**: Any application requiring maps (Uber, Tinder, Zillow). The `PostGIS` extension is the industry standard for GIS operations. It handles complex geometries, calculates distance vectors over the Earth's curvature, and performs lightning-fast spatial bounding-box intersections.
3. **AI / RAG Vector Storage (`pgvector`)**: The modern LLM revolution requires storing high-dimensional vectors (Embeddings) to perform semantic Similarity Searches. Rather than deploying standalone Vector Databases (like Pinecone or Milvus), teams simply install the `pgvector` extension. This allows developers to execute `<->` (Cosine distance) queries directly inside Postgres, keeping their relational data and AI vectors in the exact same transactional system.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sử dụng UUID thay vì ID tăng dần (Auto-Increment INT)**: Rất nhiều dự án dính lỗi bảo mật vì dùng ID tự tăng (`/users/5`). Kẻ gian sẽ đoán được và thử gọi `/users/6` để ăn cắp dữ liệu. Postgres tối ưu hóa UUID (Một chuỗi ngẫu nhiên khổng lồ `123e4567-e89b-12d3...`) cực tốt. Hãy luôn dùng UUID cho ID chính (Primary Key).
2. **Tận dụng JSONB thay vì JSON**: Postgres có 2 kiểu dữ liệu là `JSON` và `JSONB`. TUYỆT ĐỐI không dùng `JSON` (nó chỉ lưu dưới dạng chuỗi Text bình thường, đọc chậm). Luôn dùng `JSONB` (Binary JSON): Nó phân tích cú pháp trước khi lưu, xóa khoảng trắng thừa, và cực kì tối ưu cho tốc độ tìm kiếm.
3. **Dọn dẹp rác với VACUUM**: Khác với các DB khác, khi bạn `UPDATE` 1 dòng trong Postgres, nó không xóa dòng cũ. Nó tạo dòng mới và đánh dấu dòng cũ là "Đã chết" (Dead Tuples). Sau 1 thời gian, DB sẽ phình to ra chứa toàn rác. Hãy đảm bảo tính năng **Auto-Vacuum** luôn được bật trên máy chủ.

</details>

1. **Adopt UUIDv4 or UUIDv7 for Primary Keys**: Using sequential integers (`id: 1, 2, 3`) introduces Insecure Direct Object Reference (IDOR) vulnerabilities and leaks business metrics (competitors know exactly how many users you have). Postgres has native, highly optimized `UUID` data types. Use them for public-facing Primary Keys. (Modern architectures prefer UUIDv7 because it is time-sortable, which drastically reduces B-Tree index fragmentation compared to random UUIDv4).
2. **Always Choose `JSONB` over `JSON`**: PostgreSQL offers two JSON types. The `JSON` type stores the exact string input (including whitespace) and must dynamically parse the string on every single `SELECT` query. The `JSONB` type parses the object during the `INSERT`, storing it in an optimized binary format. `JSONB` is exponentially faster to query and natively supports GIN indexing. Never use the `JSON` type.
3. **Monitor the MVCC and Auto-Vacuum Engine**: Because of Multi-Version Concurrency Control (MVCC), when you `UPDATE` or `DELETE` a row, Postgres does not physically delete the data. It marks the old row as a "Dead Tuple" and writes a new one. If you have a heavily write-intensive application, the table will suffer from "Table Bloat" (massive disk usage). Postgres runs a background daemon called **Autovacuum** to clean dead tuples. Never disable Autovacuum, and tune its workers aggressively for high-traffic tables.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sử dụng Postgres như một Queue (Hàng đợi tin nhắn)**: Rất nhiều lập trình viên tạo một bảng `Jobs`, cho 10 máy chủ liên tục chạy lệnh `SELECT * FROM Jobs WHERE status = 'pending'`. Vì Postgres dùng cơ chế khóa (Locks), 10 máy chủ sẽ cãi nhau giành giật 1 dòng dữ liệu, gây ra Deadlock và làm sập Database. 
   - *Luật*: Đừng dùng Postgres làm Message Queue (Nên dùng RabbitMQ hoặc Redis). Nếu bắt buộc phải dùng, BẮT BUỘC phải xài cú pháp `FOR UPDATE SKIP LOCKED`.
2. **Vấn đề Connection Pooling**: Postgres mỗi lần có 1 kết nối vào, nó phải tạo hẳn một Tiến trình hệ điều hành (OS Process) cực kì nặng nề (tốn 10MB RAM). Nếu App Node.js của bạn mở 500 kết nối đồng thời, Postgres sẽ cạn sạch RAM.
   - *Luật*: Luôn dùng một phần mềm trung gian như **PgBouncer** đứng trước Postgres để gom các kết nối lại (Connection Pooling).

</details>

1. **Antipattern: Using Postgres as a Job Queue**: A massive architectural trap. Developers often create a `Tasks` table and have multiple background workers constantly polling `SELECT * FROM tasks WHERE status = 'pending'`. Because multiple workers attempt to lock and `UPDATE` the same row simultaneously, massive lock contention and Deadlocks crash the database. **Rule**: If you need a Queue, use RabbitMQ or Redis. If you absolutely must use Postgres, you MUST use the `SELECT ... FOR UPDATE SKIP LOCKED` syntax to safely bypass locked rows.
2. **Catastrophic Connection Overhead**: Unlike MySQL (which uses lightweight threads per connection), PostgreSQL spawns a heavy OS Process (~10MB RAM) for every active connection. If a horizontally scaled Serverless fleet (AWS Lambda) opens 2,000 concurrent database connections, PostgreSQL will instantly run out of memory and crash. **Rule**: You must always place a Connection Pooler (specifically **PgBouncer** or Supavisor) in front of PostgreSQL. PgBouncer holds the 2,000 lightweight client connections and multiplexes them onto a small pool of 50 heavy Postgres connections.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp các lệnh SQL nâng cao làm nên sức mạnh của PostgreSQL.
</details>

### UUIDs and Array Data Types
```sql
-- Creating a table with modern Postgres features
CREATE TABLE users (
    -- Automatically generate secure UUIDs
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
    username VARCHAR(50) UNIQUE NOT NULL,
    
    -- Storing an Array of strings (No external table needed)
    favorite_colors TEXT[],
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Inserting an Array
INSERT INTO users (username, favorite_colors) 
VALUES ('alice', ARRAY['red', 'blue']);

-- Querying arrays: Find users who like 'blue'
SELECT * FROM users WHERE 'blue' = ANY(favorite_colors);
```

### The Power of JSONB
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    attributes JSONB -- Flexible NoSQL storage inside SQL!
);

INSERT INTO products (name, attributes) VALUES
('Laptop', '{"brand": "Apple", "ram": "16GB", "colors": ["silver", "gray"]}'),
('T-Shirt', '{"size": "L", "material": "cotton"}');

-- Extracting a JSON value as Text (Using ->> operator)
SELECT name, attributes->>'brand' AS brand FROM products;

-- Filtering inside the JSON (Find laptops with 16GB ram)
SELECT * FROM products WHERE attributes @> '{"ram": "16GB"}';

-- CREATING A GIN INDEX ON JSONB (Crucial for speed)
CREATE INDEX idx_products_attributes ON products USING GIN (attributes);
```

### Row-Level Security (RLS)
The magic behind multi-tenant SaaS applications.

```sql
-- Assume a table for Medical Records
CREATE TABLE medical_records (
    id SERIAL PRIMARY KEY,
    patient_id UUID,
    diagnosis TEXT
);

-- Enable the RLS engine on this table
ALTER TABLE medical_records ENABLE ROW LEVEL SECURITY;

-- Create a strict Policy: A patient can ONLY see their own records.
-- current_setting('app.current_user_id') is passed securely from the Backend API.
CREATE POLICY patient_isolation_policy ON medical_records
    FOR SELECT
    USING (patient_id = current_setting('app.current_user_id')::UUID);

-- Result: Even if the backend sends a naive "SELECT * FROM medical_records",
-- Postgres invisibly appends the WHERE clause, preventing massive data leaks.
```

### Upserts (ON CONFLICT)
Gracefully handling duplicate entries.

```sql
INSERT INTO users (id, username, login_count)
VALUES ('uuid-1', 'alice', 1)
ON CONFLICT (username) -- If 'alice' already exists...
DO UPDATE SET 
    login_count = users.login_count + 1; -- ...just increment her login count.
```

---

## Related Topics

- For managing PostgreSQL schema from the backend, see **[Node.js](./nodejs-express.md)** (Prisma/TypeORM) or **[Spring Boot](./spring-boot.md)** (Hibernate).
- If your data lacks strict relationships entirely, consider **[MongoDB](./mongodb.md)**.
- If Database connections are exhausted, utilize an In-Memory cache like **[Redis](./redis.md)**.
