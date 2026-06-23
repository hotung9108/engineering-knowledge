# NoSQL Fundamentals: Document, Key-Value, and Graph DBs

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: SQL (Relational DB) rất tuyệt vời, nhưng thiết kế bảng cột cứng nhắc của nó khiến nó cực kỳ khó để mở rộng (Scale) ra nhiều máy chủ khi bạn có hàng tỷ dữ liệu. **NoSQL** (Not Only SQL) ra đời bằng cách... vứt bỏ bớt luật lệ (Bỏ Normalization, bỏ Joins, bỏ bớt tính ACID chặt chẽ) để đổi lấy 2 thứ: **Tốc độ cực hạn** và **Khả năng mở rộng ngang (Horizontal Scaling)**. Không có một "chuẩn NoSQL" duy nhất; NoSQL là một cái ô chứa nhiều cấu trúc khác nhau (Key-Value, Document, Graph).

</details>

> **Summary**: While SQL (Relational DBs) excel at strict data integrity, their rigid tabular schema and heavy Join operations make them notoriously difficult and expensive to scale horizontally across hundreds of servers. **NoSQL** (Not Only SQL) emerged as an architectural rebellion. By intentionally sacrificing strict relational rules (abandoning Normalization, complex Joins, and sometimes strict ACID compliance), NoSQL achieves two critical objectives: **Unprecedented throughput velocity** and **effortless Horizontal Scaling**. NoSQL is not a single technology; it is an umbrella term encompassing distinct storage paradigms (Key-Value, Document, Graph, and Wide-Column).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn lưu thông tin lý lịch học sinh:
- **SQL (Hệ thống tủ hồ sơ thép)**: Mọi tờ giấy phải được kẻ sẵn đúng 3 cột (Mã, Tên, Tuổi). Nếu học sinh C có thêm mục "Sở thích", bạn không thể nhét vào được trừ khi gọi thợ sắt đến đục thêm 1 cột mới cho toàn bộ 1000 cái tủ!
- **NoSQL (Hộp các-tông lộn xộn nhưng tiện lợi)**:
  - **Document DB**: Học sinh A bỏ vào hộp một tờ giấy 3 dòng. Học sinh B ném vào đó nguyên một quyển sổ 50 trang dán đầy ảnh. Không sao cả, hộp ai nấy giữ, miễn là đóng gói thành một cục dữ liệu tự do (JSON Document). Cực kỳ linh hoạt.
  - **Key-Value DB**: Bạn có một cuốn sổ tay nhỏ xíu. Ghi `Mã số 1 = Nguyễn Văn A`. Khi hỏi "Số 1 là ai?", nó trả lời trong 0.001 giây. Siêu tốc độ, nhưng chỉ biết tìm đúng theo mã số.

</details>

Imagine you are managing student records:
- **SQL (The Rigid Steel Filing Cabinet)**: Every single folder must contain a strictly formatted form with exactly 3 fields (ID, Name, Age). If Student C wants to add a "Hobbies" section, you cannot allow it unless you halt operations and physically weld a new "Hobbies" field into every single folder in the entire school (Schema Migration).
- **NoSQL (The Flexible Cardboard Boxes)**:
  - **Document DB (MongoDB)**: Student A tosses a 3-line post-it note into their box. Student B tosses a 50-page scrapbook filled with photos into their box. The database doesn't care. Each box is an isolated, self-contained JSON Document. Ultimate flexibility.
  - **Key-Value DB (Redis)**: A massive hyper-optimized coat-check system. You hand the clerk a ticket `123`. They instantly hand you back the coat. It is blazingly fast, but if you ask the clerk, "Give me all red coats," they will refuse. They can only search by the exact Ticket Number.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

NoSQL được chia làm 4 "môn phái" chính:
1. **Document-Oriented (Ví dụ: MongoDB)**: Dữ liệu lưu thành các cục JSON (hoặc BSON). Một cục (Document) chứa tất cả thông tin, kể cả mảng (Array) hay cục JSON con. Không cần định nghĩa Schema (cột) trước.
2. **Key-Value Stores (Ví dụ: Redis, Memcached)**: Dữ liệu lưu dưới dạng Cặp Chìa Khóa - Ổ Khóa. Đơn giản nhất, nhưng chạy nhanh nhất trần đời (toàn bộ lưu trên RAM).
3. **Graph Databases (Ví dụ: Neo4j)**: Lưu dữ liệu dưới dạng "Mạng lưới nhện" (Đỉnh và Cạnh). Dùng để tính toán khoảng cách quan hệ (Ví dụ: "Tìm những người là bạn của bạn của bạn").
4. **Wide-Column Stores (Ví dụ: Cassandra)**: Được thiết kế để lưu hàng tỷ tỷ dòng dữ liệu (Ví dụ: lịch sử nhiệt độ mỗi giây của hàng vạn cảm biến) phân tán trên nhiều máy chủ mà không bao giờ bị nghẽn (tối ưu hóa cho Write).

</details>

NoSQL is categorized into four primary architectural paradigms:
1. **Document-Oriented (e.g., MongoDB, Couchbase)**: Data is stored as semi-structured JSON-like documents (BSON). A single document can contain complex, deeply nested hierarchies and arrays. Schemas are entirely dynamic (Schema-less); Document A and Document B in the same collection can have entirely different fields.
2. **Key-Value Stores (e.g., Redis, Amazon DynamoDB)**: The simplest and most performant architecture. A massive hash table. You assign a primary Key, and bind it to a Value (String, Blob, JSON). Searches execute in `O(1)` time complexity.
3. **Graph Databases (e.g., Neo4j)**: Architected purely for relationships. Data is stored as Nodes (Entities) and Edges (Relationships). Excels at traversing deeply connected networks (e.g., "Find friends of friends who also bought this product").
4. **Wide-Column Stores (e.g., Apache Cassandra, ScyllaDB)**: Engineered for astronomical Write throughput and 100% High Availability across geographically distributed data centers. Heavily utilized for Time-Series data (IoT telemetry) and massive event logging.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề của SQL: Rất khó để Scale ngang (Horizontal Scaling)**
Khi Web của bạn to lên, 1 máy chủ SQL không gánh nổi. Bạn mua thêm máy chủ 2. Nếu áp dụng Normalization, bảng User nằm ở máy 1, bảng Order nằm ở máy 2. Lệnh `JOIN` hai bảng này qua cáp mạng sẽ cực kỳ thảm họa và làm sập hệ thống (Vấn đề Sharding).

**Giải pháp NoSQL: Denormalization (Gộp chung)**
NoSQL không dùng `JOIN`. Nó nhét TOÀN BỘ thông tin (User, Order) vào chung 1 file JSON (Document). Gộp tất cả dữ liệu lại gọi là Denormalization (Phi chuẩn hóa). Dù bị trùng lặp dữ liệu, nhưng giờ đây khi bạn trải dài dữ liệu ra 100 máy chủ, việc lấy thông tin 1 User chỉ mất 1 cú đọc (đọc trọn gói cục JSON đó), tốc độ tăng lên gấp ngàn lần.

</details>

**The SQL Bottleneck: The Horizontal Scaling Nightmare**
As data grows to petabytes, a single monolithic SQL server collapses under the load (Vertical Scaling limits). If you attempt to shard (split) a normalized SQL database across 5 servers, disaster strikes. Table `Users` lives on Server A, and Table `Orders` lives on Server B. Executing a SQL `JOIN` across a physical network partition introduces catastrophic latency and locking complexities.

**The NoSQL Solution: Denormalization and Sharding**
NoSQL inherently rejects the concept of server-side `JOINs`. Instead, it aggressively **Denormalizes** data. A MongoDB Document completely embeds the User's Orders directly inside the User's JSON file. Yes, this introduces Data Redundancy, but it mathematically guarantees that fetching a User requires exactly *One Read Operation* from a single physical server, even if the database is horizontally sharded across 10,000 servers. Storage is cheap; Compute is expensive. NoSQL trades disk space for infinite scalability.

---

## Layer 3: Without vs. With Comparison (Compare)

### Data Modeling: Relational vs Document

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt khi thiết kế CSDL cho một bài viết (Blog Post) có nhiều Bình luận (Comments).
</details>

How to model a Blog Post containing multiple Comments.

#### The SQL Way (Normalized)
Requires 2 rigid tables and an expensive `JOIN` to assemble the final view.
**Table 1: Posts** `[id: 1, title: "Hello"]`
**Table 2: Comments** `[id: 99, post_id: 1, text: "Nice!"], [id: 100, post_id: 1, text: "Cool!"]`
*Query*: `SELECT * FROM Posts p JOIN Comments c ON p.id = c.post_id`

#### The MongoDB Way (Denormalized Document)
Requires exactly 1 table (Collection). The entire data entity is fetched instantly without any relational math.
```json
{
  "_id": 1,
  "title": "Hello",
  "comments": [
    { "id": 99, "text": "Nice!" },
    { "id": 100, "text": "Cool!" }
  ]
}
```

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Redis (Key-Value)**: Thường dùng để làm "Bộ đệm" (Cache). Lưu trữ Session đăng nhập, Bảng xếp hạng Game (Leaderboard), Đếm số lượt xem Video (Vì nó đếm cực kỳ nhanh trên RAM).
- **MongoDB (Document)**: Dùng cho các dự án Startup cần code cực nhanh mà chưa rõ CSDL có các cột gì. Catalog sản phẩm thương mại điện tử (Có sản phẩm thì có cột Size Quần Áo, có sản phẩm thì có cột Dung lượng Ổ cứng $\rightarrow$ Cột lộn xộn, SQL không lưu nổi).
- **Neo4j (Graph)**: Hệ thống gợi ý của Netflix/Tiktok. Phân tích gian lận ngân hàng (Tìm đường dây chuyển tiền vòng vèo rắc rối).

</details>

- **Redis (Key-Value) Domain**: The undisputed king of **Caching**. Used globally to buffer slow SQL queries, store volatile User Login Sessions (JWT blacklists), manage real-time Game Leaderboards, and execute high-frequency rate-limiting architectures. It resides entirely in RAM.
- **MongoDB (Document) Domain**: The default for Rapid Startup Prototyping where the schema is fluid and evolving daily. Essential for **E-commerce Product Catalogs**. (e.g., A T-Shirt has a "Size" field, but a Laptop has a "RAM" field. SQL struggles with polymorphic schemas; MongoDB handles heterogeneous JSON elegantly).
- **Neo4j (Graph) Domain**: Recommendation Engines (TikTok/Netflix algorithms identifying complex user-behavior clusters) and Fraud Detection (Banks analyzing convoluted transaction rings to detect money laundering paths).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiểu rõ CAP Theorem**: Trong hệ thống phân tán, bạn chỉ được chọn 2 trong 3 thứ: C (Tính nhất quán - Dữ liệu luôn đúng), A (Độ sẵn sàng - Gọi là có ngay), P (Chịu lỗi mạng). SQL chọn C (Chấp nhận sập chứ không trả về dữ liệu sai). Hầu hết NoSQL (như Cassandra) chọn A (Luôn sống sót, dù trả về dữ liệu cũ bị sai lệch một chút cũng không sao - Eventual Consistency). Bạn phải biết hệ thống của mình cần gì.
2. **MongoDB: Cẩn thận giới hạn độ lớn của Document**: Việc nhúng dữ liệu (Embedding) cực tốt, nhưng một file JSON trong Mongo chỉ được tối đa 16MB. Nếu bạn nhét một mảng "Comment" vào bài viết, và có 1 triệu người vào comment, cái Document đó sẽ phình to quá 16MB và nổ tung. Với danh sách có thể dài vô tận, bắt buộc phải dùng kỹ thuật tách Bảng (Reference) giống SQL.

</details>

1. **Master the CAP Theorem**: The foundational law of Distributed Systems. You can only mathematically guarantee 2 out of 3 properties: Consistency (C), Availability (A), and Partition Tolerance (P).
   - SQL typically enforces **CP** (If the network splits, the DB rejects writes to maintain perfect data integrity). 
   - NoSQL (like Cassandra/DynamoDB) heavily favors **AP** (If the network splits, the DB continues accepting writes to stay alive, sacrificing perfect consistency and relying on *Eventual Consistency*). You must align your DB choice with your business risk profile.
2. **Beware the MongoDB 16MB Document Limit**: Embedding data is MongoDB's superpower, but it is bounded by physics. The maximum size of a single BSON document is 16MB. If you embed an unbound array (e.g., an Instagram Post document containing an array of 5 million Comments), the document will shatter the 16MB ceiling and the database will catastrophically crash. **Rule**: Embed for *Bounded* 1-to-Few relationships; Use normalized References for *Unbounded* 1-to-Many relationships.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng MongoDB như SQL**: Dev chuyển từ MySQL sang dùng Mongo. Bắt đầu tạo Bảng 1, Bảng 2. Khi cần lấy dữ liệu thì lôi cái đống lệnh `$lookup` ra để viết JOINS. MongoDB chạy JOINS cực kỳ chậm và tốn CPU. Nếu bạn phải viết JOIN quá nhiều ở Mongo, bạn đã chọn sai CSDL. Hãy quay về SQL!
2. **Tin tưởng NoSQL không bao giờ mất dữ liệu**: Một số loại NoSQL cấu hình mặc định là "Ghi xong lên RAM là báo Thành công" (Fire and forget) chứ chưa thực sự ghi xuống ổ cứng. Nếu cúp điện bất thình lình, dữ liệu mất sạch. Luôn phải cấu hình `Write Concern` cẩn thận nếu dữ liệu đó quan trọng (Ví dụ: Thanh toán).

</details>

1. **Using MongoDB as a Relational Database**: A lethal anti-pattern. Developers migrate from PostgreSQL to MongoDB, but continue designing highly normalized schemas across 15 separate Collections. Because MongoDB lacks robust, optimized relational mathematics, developers abuse the `$lookup` aggregation pipeline operator to simulate SQL `JOINs`. This obliterates the CPU. If your data model demands heavy, complex JOINs, **Do Not Use Document NoSQL. Return to PostgreSQL.**
2. **Default Write Concerns (Data Loss)**: Historically, many NoSQL databases prioritized benchmark speed over durability. Their default `Write Concern` configured the database to return an `HTTP 200 OK` success the millisecond the data entered RAM, *before* physically flushing it to the SSD. A sudden power loss resulted in silent data evaporation. Always configure your cluster to require absolute Journal/Disk confirmation for critical payloads (e.g., `w: "majority", j: true`).

---

## Related Topics

- For deep modeling strategies, see **[Database Design & Schema](./database-design.md)**.
- To compare strictly with the relational paradigm, see **[SQL Fundamentals](./sql-fundamentals.md)**.
- See how JSON dictates document formats in **[Data Formats](../web-fundamentals/data-formats.md)**.
