# Elasticsearch

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Bạn có bao giờ tự hỏi làm sao Google có thể tìm ra chính xác bài báo bạn cần trong hàng tỷ kết quả chỉ mất 0.1 giây, ngay cả khi bạn gõ sai chính tả? Cơ sở dữ liệu SQL (như Postgres) hay NoSQL (như Mongo) sinh ra để *Lưu trữ*, chứ không sinh ra để *Tìm kiếm văn bản*. Nếu bạn dùng lệnh `SELECT * FROM articles WHERE content LIKE '%apple%'`, SQL sẽ phải lật tung từng trang ổ cứng để quét chữ "apple", làm Server sập ngay lập tức. **Elasticsearch** ra đời để giải quyết bài toán này. Nó là một **Search Engine (Động cơ tìm kiếm)** khổng lồ. Nó băm nát tất cả các câu văn thành các "Từ khóa" (Tokens) và tạo ra một "Mục lục ngược" (Inverted Index). Nhờ đó, việc tìm kiếm Full-Text Search, tìm kiếm sai chính tả (Fuzzy Search) hay Autocomplete trở nên nhanh như chớp.

</details>

> **Summary**: Traditional Relational Databases (PostgreSQL/MySQL) and Document Stores (MongoDB) are engineered for structured data retrieval and exact-match indexing (B-Trees). They fail catastrophically when executing wildcard textual searches (`LIKE '%keyword%'`) across massive unstructured text blobs, as this forces a full-table scan, annihilating CPU performance. **Elasticsearch** is not a primary database; it is a highly distributed, RESTful **Search and Analytics Engine** built on top of the Apache Lucene library. Its architectural superpower is the **Inverted Index**—a data structure that maps words back to the documents that contain them. It natively supports Full-Text Search, relevance scoring (TF-IDF / BM25), typos/fuzzy matching, and complex geospatial aggregations at Petabyte scales. It forms the core of the ELK Stack (Elasticsearch, Logstash, Kibana), dominating enterprise log analytics and e-commerce search bars.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang tìm một chi tiết trong một Thư viện có 1 triệu cuốn sách.
1. **Tìm bằng SQL (`LIKE`)**: Bạn cầm kính lúp, lật trang 1 cuốn sách số 1, dò từng chữ. Xong lật trang 2. Bạn phải đọc hết 1 triệu cuốn sách mới tìm ra chữ "Harry Potter". Mất 100 năm.
2. **Tìm bằng Elasticsearch (Inverted Index)**: Elasticsearch giống như cái **Mục Lục (Index)** ở cuối cuốn từ điển. Khi bạn mang sách mới vào thư viện, Elasticsearch sẽ xé nát cuốn sách ra, nhặt lấy các từ khóa quan trọng và ghi vào sổ: *"Chữ 'Harry' xuất hiện ở Sách số 1 (trang 5) và Sách số 9 (trang 10)"*. Khi bạn gõ tìm kiếm chữ "Harry", nó không đọc sách, nó mở cuốn Mục lục ra và chỉ ngay cho bạn: *"Đến thẳng Sách số 1 và 9 lấy cho tôi!"*. Quá trình này mất 0.001 giây.

</details>

Imagine searching for a specific keyword across 10,000 thick textbooks.
1. **Traditional SQL (`LIKE '%keyword%'`)**: You hire a reader to start at Page 1 of Book 1 and literally read every single word sequentially until they reach the end of Book 10,000. It is grueling, slow, and computationally disastrous (O(N) Full Table Scan).
2. **Elasticsearch (Inverted Index)**: Elasticsearch acts as the Master Index at the back of an encyclopedia. When you insert a book into the system, it analyzes it immediately. It creates a dictionary mapping: *"The word 'apple' exists in Book 12, Book 54, and Book 900"*. When a user searches for "apple", the engine simply looks up the word in the dictionary and instantly returns the exact book IDs. It takes 5 milliseconds, completely regardless of how massive the books are.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bản chất của Elasticsearch dựa trên 3 khái niệm:
1. **Apache Lucene (Lõi phân tích)**: Đây là trái tim của Elasticsearch. Khi bạn đưa một câu *"Tôi đang CHẠY bộ"*, Lucene sẽ tự động bỏ chữ "Tôi", bỏ chữ "đang", đổi chữ "CHẠY" thành chữ thường "chạy", và cắt nó thành các Tokens để đưa vào Inverted Index.
2. **RESTful API**: Khác với SQL có cổng kết nối riêng, bạn giao tiếp với Elasticsearch 100% bằng HTTP (gửi cục JSON qua phương thức GET, POST). Do đó mọi ngôn ngữ (Python, JS, Java) đều dùng được rất dễ dàng.
3. **Phân tán (Distributed by Nature)**: Elasticsearch sinh ra là để chạy trên nhiều máy chủ cùng lúc (Cluster). Dữ liệu được chia nhỏ thành các "Shards". Nếu máy chủ 1 bị cháy, dữ liệu vẫn còn bản sao ở máy chủ 2.

</details>

Elasticsearch is a distributed NoSQL datastore explicitly optimized for text analysis and complex aggregations.
1. **Apache Lucene Core (Text Analysis)**: The underlying Java library. When a JSON document is indexed, Lucene executes an "Analysis Pipeline". It tokenizes sentences into words, applies Lowercasing, removes Stop-Words ("a", "the", "is"), and applies Stemming (converting "Running" and "Ran" down to their base root "run"). These tokens are then written into the Inverted Index.
2. **The Inverted Index**: A data structure perfectly mirroring a book's index. It maps specific words (terms) directly to the specific Document IDs that contain them, enabling O(1) or O(log N) search complexities regardless of total text volume.
3. **BM25 Relevance Scoring**: It doesn't just return matches; it ranks them. If you search for "Brown Fox", a document containing the exact phrase "Brown Fox" 10 times in its Title will receive a higher mathematical Score than a document containing "Brown" once in its footer. The most relevant results are inherently returned first.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong các dự án thực tế, Khách hàng luôn gõ sai chính tả.
Ví dụ trên Shopee: Khách hàng muốn mua "Điện thoại Samsung", nhưng họ gõ vội thành "Điệ thoại Sam sung". 
Nếu dùng `SELECT * FROM products WHERE name = 'Điệ thoại Sam sung'`, SQL sẽ trả về 0 kết quả. Khách hàng sẽ tưởng cửa hàng hết hàng và bỏ đi. Công ty mất tiền.
Elasticsearch sinh ra để làm cỗ máy **Fuzzy Search (Tìm kiếm mờ)**. Thuật toán của nó (Levenshtein distance) sẽ tự động nhận ra chữ "Điệ" chỉ khác chữ "Điện" đúng 1 kí tự. Nó thông minh tự sửa lỗi và vẫn trả về kết quả Điện thoại Samsung cho khách hàng. Đây là lí do 100% các trang E-Commerce lớn đều phải xài Elasticsearch cho thanh Tìm kiếm.

</details>

Elasticsearch solves the "Human Input Error" problem and the "Fuzzy Search" requirement in modern applications.
In standard Relational Databases, searching for strings requires Exact Match paradigms. If a user types "Iphonee 15" instead of "iPhone 15", the SQL `WHERE` clause fundamentally fails, returning 0 results. This causes catastrophic revenue loss in E-Commerce platforms.
Elasticsearch implements **Fuzzy Matching** utilizing the Levenshtein Distance algorithm. It mathematically calculates that "Iphonee" requires exactly 1 edit (deleting the 'e') to become "iPhone". It automatically forgives the typo and returns the correct product. Furthermore, it handles complex Synonym mapping (understanding that a search for "Sneakers" should also return "Running Shoes"), acting as the intelligent backbone for modern User Experience (UX).

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc xây dựng tính năng Autocomplete (Gõ chữ tới đâu, gợi ý hiện ra tới đó).
</details>

Visualizing Autocomplete / Search-As-You-Type.

| Metric | Primary Database (PostgreSQL) | Elasticsearch |
|---|---|---|
| **The Methodology** | `SELECT * FROM users WHERE name LIKE 'Joh%'`. Runs every single time the user presses a keystroke. | `GET /users/_search` utilizing highly optimized `edge_ngram` tokenizers. |
| **Performance (Scale)**| The database CPU will spike to 100% and crash if 10,000 users are typing simultaneously. | Specifically engineered for this exact workload. Sub-millisecond responses easily support thousands of concurrent typists. |
| **Typo Tolerance** | Impossible to handle "Jho%" natively in standard SQL. | Natively understands "Jho" means "John" via `fuzziness: auto`. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Thanh tìm kiếm (Search Bar) thông minh**: Shopee, Tiki, Wikipedia. Elasticsearch đứng đằng sau mọi thanh tìm kiếm, cung cấp tính năng gợi ý từ khóa (Autocomplete), sửa lỗi chính tả, và lọc giá tiền cực kì mượt mà.
2. **ELK Stack (Phân tích Log Hệ thống)**: Một công ty có 100 máy chủ. Mỗi giây có 500 lỗi xảy ra được in ra file text (Log). Dev không thể mở 100 máy chủ lên đọc file text được. Họ dùng Logstash (L) để thu gom 500 file text đó, ném vào Elasticsearch (E) để đánh Index, và dùng Kibana (K) để vẽ biểu đồ trực quan (Dashboard). Khi App chết, Dev chỉ việc vào Kibana gõ chữ "ERROR" là thấy ngay lỗi ở máy chủ nào.
3. **Phân tích dữ liệu không gian (Geospatial)**: Kết hợp Tìm kiếm văn bản và Bản đồ. Ví dụ ứng dụng Foody/Yelp: "Tìm các Quán Phở (Text) Nằm trong bán kính 2km (Geo) Đang mở cửa (Boolean) và Có Rating > 4 sao (Range)". Elasticsearch giải quyết các truy vấn gộp này cực kỳ xuất sắc.

</details>

1. **E-Commerce & Enterprise Search**: The backbone of the search bar on major platforms (Wikipedia, GitHub, Uber). It powers Search-As-You-Type (Autocomplete), Handles synonyms, corrects typos (Fuzziness), and applies complex algorithmic Highlighting (returning the snippet of text where the word was found, bolded).
2. **Centralized Log Analytics (The ELK Stack)**: In a microservice architecture, logs are scattered across 50 Docker containers. It is impossible to SSH into them to read `.log` files. The industry standard is the ELK Stack. **Logstash** ingests raw logs, **Elasticsearch** indexes them natively, and **Kibana** provides a beautiful Web GUI. When a system crashes at 3 AM, an engineer simply types `status: 500 AND service: payment` into Kibana, instantly isolating the exact failing container.
3. **Complex Geospatial & Textual Filtering**: Platforms like Yelp or Zillow. Combining complex spatial bounds with textual relevance. "Find an Italian Restaurant (Text Match) within 5 kilometers of my GPS coordinates (Geo-Distance) that has a price under $50 (Numeric Range) and is currently open (Boolean Filter)." Elasticsearch natively executes these multi-dimensional boolean queries flawlessly.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Không dùng Elasticsearch làm Database Chính (Primary DB)**: Đừng bao giờ vứt bỏ Postgres/Mongo để lưu 100% dữ liệu quan trọng vào Elasticsearch. Dù Elasticsearch có cơ chế lưu trữ, nhưng bản chất nó không đảm bảo tính toàn vẹn Giao dịch (ACID) tài chính. Hãy luôn lưu dữ liệu gốc ở Postgres, sau đó "Đồng bộ" (Sync) các dữ liệu cần Tìm kiếm (như Tên sản phẩm, Mô tả) sang Elasticsearch.
2. **Định nghĩa Mapping thật chuẩn trước khi ném dữ liệu vào**: Khác với Mongo (JSON thả cửa). Trước khi đưa dữ liệu vào Elasticsearch, hãy định nghĩa rõ: Trường `title` là kiểu Text (để cắt nhỏ ra tìm kiếm từng từ), nhưng trường `status` phải là kiểu Keyword (Tìm chính xác chữ "ACTIVE", không được cắt nhỏ). Nếu bạn để ES tự đoán (Dynamic Mapping), nó sẽ làm phình to ổ cứng và tìm kiếm sai lệch.

</details>

1. **Never use Elasticsearch as the Primary Source of Truth**: A critical architectural rule. Elasticsearch is an eventual-consistency search engine, not an ACID-compliant financial ledger. It lacks strict transactional guarantees, Foreign Keys, and rollback mechanisms. **The Architecture**: Store your golden data in PostgreSQL. Utilize asynchronous background workers (or CDC tools like Debezium) to securely replicate specific search-heavy columns (Title, Description, Category) into the Elasticsearch cluster. If the ES cluster completely dies, you can always rebuild the Index from the Postgres master.
2. **Strict Mapping (Text vs Keyword)**: Elasticsearch attempts to auto-guess schema types (Dynamic Mapping), which often results in disaster. You must explicitly define your mappings. The most important distinction is String data types.
   - `text`: Analyzed and Tokenized. "New York" becomes `[new, york]`. Used for full-text search (`match` queries).
   - `keyword`: NOT analyzed. Kept as the exact literal string "New York". Used for exact filtering (`term` queries), aggregations, and sorting.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hội chứng "Bùng nổ Cluster" (Split-Brain)**: Khi bạn chạy Elasticsearch trên 2 máy chủ (Node). Mạng cáp quang giữa 2 máy bị đứt tạm thời. Máy 1 nghĩ Máy 2 đã chết, nên tự xưng làm Vua (Master Node). Máy 2 cũng nghĩ Máy 1 đã chết, tự xưng làm Vua. Cả 2 máy cùng nhận dữ liệu Ghi từ khách hàng. Khi mạng nối lại, dữ liệu bị xung đột tan nát.
   - *Luật*: LUÔN LUÔN cấu hình cụm Elasticsearch với SỐ LẺ máy chủ (3, 5, 7) để áp dụng thuật toán Bầu cử (Quorum/Voting). Nếu có 3 máy, 2 máy sẽ bầu ra 1 Vua. Không bao giờ xảy ra tình trạng 2 Vua.
2. **Tràn bộ nhớ Java Heap (OOM)**: Vì Elasticsearch viết bằng Java (Lucene), nó cực kì ngốn RAM. Nếu bạn cho phép người dùng chạy một lệnh `Aggregations` (Gom nhóm và Đếm số lượng) trên 1 tỷ dòng dữ liệu, Elasticsearch sẽ kéo toàn bộ dữ liệu vào RAM và làm sập máy chủ ngay lập tức. Luôn phải giới hạn lượng RAM cho Elasticsearch (Heap size = 50% RAM vật lý) và giới hạn quyền truy vấn của User.

</details>

1. **The Split-Brain Catastrophe**: The most infamous distributed systems failure. If you deploy an Elasticsearch cluster with exactly 2 Master-Eligible Nodes, and the network cable between them drops, both nodes assume the other died. They both promote themselves to Primary Master and begin accepting divergent `WRITE` operations independently. When the network heals, the cluster is irrecoverably corrupted. **Rule**: A distributed cluster MUST have an odd number of Master-Eligible Nodes (Minimum 3) to enforce Quorum Voting (`majority = N/2 + 1`).
2. **JVM Heap Exhaustion (OOM Kills)**: Elasticsearch runs on the Java Virtual Machine. Deep Pagination (users clicking "Page 10,000" of search results) or massive FieldData aggregations force Elasticsearch to load millions of records directly into the JVM Heap, instantly triggering an Out-Of-Memory Panic. **Rule**: Never assign more than 50% of the physical OS RAM to the JVM Heap (up to a max of 32GB) because Lucene requires the remaining OS RAM for filesystem caching. Block Deep Pagination via the `max_result_window` setting.

---

## Related Topics

- Elasticsearch acts as a secondary indexing engine. The golden data should always live in a primary DB like **[PostgreSQL](./postgresql.md)** or **[MongoDB](./mongodb.md)**.
- For purely exact-match, high-speed caching of strings (without Full-Text Analysis), use **[Redis](./redis.md)** instead.
- For deploying scalable Elasticsearch Clusters, utilize orchestration tools like **[Kubernetes](../cloud-infra/kubernetes.md)**.
