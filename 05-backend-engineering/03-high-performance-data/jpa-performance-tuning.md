# JPA Performance Tuning

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Các kỹ thuật nâng cao để giải quyết bài toán N+1 Query, tối ưu hóa bộ nhớ bằng DTO projections, cấu hình batching cho JDBC và xử lý an toàn các tập dữ liệu lớn trong Spring Data JPA.

</details>

> **Summary**: Advanced techniques for solving the N+1 query problem, optimizing memory usage with DTO projections, configuring JDBC batching, and handling large datasets safely in Spring Data JPA.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (JPA) được giao nhiệm vụ đi siêu thị mua 10 lốc sữa.
- **Cách người ngốc làm (N+1 Query)**: Bạn chạy vào siêu thị lấy 1 lốc sữa mang ra tính tiền. Rồi bạn lại chạy vào lấy lốc thứ 2 mang ra tính tiền. Bạn chạy ra chạy vào 10 lần. Bạn sẽ gục ngã vì mệt mỏi!
- **Cách người khôn làm (Fetch JOIN)**: Bạn lấy 1 cái xe đẩy, nhét cả 10 lốc sữa vào rồi mang ra tính tiền 1 lần duy nhất.
Tương tự như vậy, nếu bạn cần lấy danh sách "Bài viết" và "Bình luận" của bài viết đó, đừng bắt Database chạy 1 câu query để lấy Bài viết, rồi chạy thêm N câu query để lấy Bình luận. Hãy gộp nó lại thành 1 chuyến xe đẩy!

</details>

Imagine you (JPA) are tasked with buying 10 packs of milk from the supermarket.
- **The Foolish Way (N+1 Query)**: You run into the store, grab 1 pack, and go to the cashier. Then you run back in, grab the 2nd pack, and go to the cashier. You run back and forth 10 times. You will collapse from exhaustion!
- **The Smart Way (Fetch JOIN)**: You grab a shopping cart, put all 10 packs in it, and go to the cashier exactly once.
Similarly, if you need to fetch a list of "Posts" and their "Comments", don't force the Database to run 1 query to fetch the Posts, and then N additional queries to fetch the Comments. Group them into one shopping cart trip!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tối ưu hiệu năng JPA** bao gồm việc cấu hình Hibernate (trình cung cấp JPA) và cấu trúc lại các mối quan hệ (Entity) cũng như câu lệnh truy vấn để giảm thiểu tối đa số chuyến đi khứ hồi đến database và lượng RAM tiêu thụ.
- **N+1 Problem**: Chạy 1 câu lệnh để lấy danh sách thực thể, sau đó tự động đẻ ra $N$ câu lệnh phụ để lấy các bảng liên kết (lazy-loaded).
- **EntityGraphs / Fetch JOINs**: Giải pháp để lấy thực thể gốc và các bảng liên kết của nó chỉ trong 1 câu SQL `JOIN` duy nhất.
- **JDBC Batching**: Gom nhiều câu lệnh `INSERT` hoặc `UPDATE` thành 1 chuyến hàng duy nhất gửi xuống Database.

**Phân loại:**
- **Loại**: Truy xuất Dữ liệu / Tối ưu Hiệu năng.
- **Framework**: Spring Data JPA / Hibernate.

</details>

**JPA Performance Tuning** involves configuring Hibernate (the JPA provider) and structuring entity relationships and queries to minimize database round-trips and memory consumption.
- **N+1 Problem**: Executing 1 query to fetch a list of entities, and then $N$ additional queries to fetch their lazy-loaded associations.
- **EntityGraphs / Fetch JOINs**: Solutions to fetch the root entity and its associations in a single SQL `JOIN` query.
- **JDBC Batching**: Grouping multiple `INSERT` or `UPDATE` statements into a single network request to the database.

### Classification
- **Type**: Data Access / Performance Optimization.
- **Framework**: Spring Data JPA / Hibernate.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Một ORM (như JPA/Hibernate) cố gắng map các bảng quan hệ vào các object Java. Nếu một bài `Post` có nhiều `Comment`, khi bạn gọi hàm `post.getComments()`, ORM có thể bí mật bắn ra một câu query xuống Database.

Khi dev chạy thử ở máy cá nhân với 10 dòng dữ liệu, lỗi N+1 chỉ tốn 5ms và không ai nhận ra. Nhưng khi lên Production với 10,000 dòng dữ liệu, một lần gọi API sẽ kích hoạt 10,001 câu truy vấn SQL liên tiếp, khiến CPU Database đạt 100% và API bị Timeout sập luôn.

</details>

An ORM (Object-Relational Mapper) attempts to map relational tables to Java object graphs. If you have a `Post` entity that has many `Comment` entities, calling `post.getComments()` might trigger a stealthy database query. 

In a local environment with 10 rows of data, N+1 queries take 5ms and are invisible. In production, with 10,000 rows, a single API call might trigger 10,001 SQL queries, causing the database CPU to max out and the API to timeout.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không tối ưu: `findAll()` gọi 1 lệnh lấy 1000 Tác giả. Vòng lặp for gọi `.getBooks()` đẻ ra thêm 1000 lệnh lấy sách. Tổng cộng 1001 lệnh.
Có tối ưu: Thêm `@EntityGraph` (hoặc viết `JOIN FETCH`). Nó báo Hibernate làm ơn gộp bảng Sách vào luôn. Tổng cộng chỉ chạy 1 câu query.

</details>

### Without Tuning (The N+1 Nightmare)
```java
// Service layer
List<Author> authors = authorRepository.findAll(); // 1 Query: SELECT * FROM author
for (Author author : authors) {
    // Triggers N queries: SELECT * FROM book WHERE author_id = ?
    System.out.println(author.getBooks().size()); 
}
// Total Queries: 1 + N. If findAll() returns 1000 authors, this runs 1001 SQL queries!
```

### With Tuning (EntityGraph / Fetch JOIN)
```java
// Repository layer
@EntityGraph(attributePaths = {"books"})
List<Author> findAll(); // Generates 1 Query: SELECT a.*, b.* FROM author a LEFT JOIN book b ...

// Service layer
List<Author> authors = authorRepository.findAll(); // 1 Query
for (Author author : authors) {
    System.out.println(author.getBooks().size()); // 0 additional queries! Data is already loaded.
}
// Total Queries: 1.
```

| Issue | Default JPA Behavior | Tuned Behavior |
|---|---|---|
| Lazy Loading Collections | Triggers N+1 queries | Resolved via `@EntityGraph` or `JOIN FETCH` |
| Mass Inserts (10,000 rows) | 10,000 separate `INSERT` requests | 1 request containing 10,000 rows (Batching) |
| Read-only transactions | Tracks changes (Dirty Checking overhead) | Bypass dirty checking (`@Transactional(readOnly = true)`) |
| Returning heavy entities | Loads all columns into memory | DTO Projections (SELECT only needed columns) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **API Dashboard**: Cần lấy cục dữ liệu to (Users + Orders + Items). Bắt buộc dùng `@EntityGraph` để chống N+1.
2. **Chuyển đổi dữ liệu (Import CSV)**: Import 50,000 dòng. Bắt buộc dùng JDBC Batching và gọi `entityManager.clear()` để dọn dẹp RAM, nếu không sẽ bị Out Of Memory (OOM).
3. **Xuất báo cáo (Export Excel)**: Xuất 1 triệu dòng ra file. Bắt buộc dùng JPA Streaming (`Stream<Entity>`) thay vì trả về `List` (List sẽ nạp 1 triệu đối tượng vào RAM và gây nổ server).

**Không nên làm**:
- **Dùng `FetchType.EAGER`**: Tuyệt đối không dùng `EAGER` cho `@OneToMany` hoặc `@ManyToOne`. Nó ép JPA luôn luôn JOIN bảng, kể cả khi bạn không hề cần dữ liệu con, dẫn đến việc lấy dư thừa hàng núi dữ liệu. Hãy luôn dùng `LAZY` và tự fetch khi cần.
- **Gọi `.saveAll()` cho 100,000 thực thể mà không có batching**: Nó sẽ nổ RAM JVM vì Persistence Context của Hibernate sẽ theo dõi trạng thái của từng đối tượng một.

</details>

1. **Dashboard APIs**: Fetching complex aggregates (Users + Orders + Items). Must use `@EntityGraph` to prevent N+1.
2. **Data Migration / CSV Import**: Inserting 50,000 rows. Must use JDBC Batching and `entityManager.clear()` to prevent OOM.
3. **Reporting Exports**: Exporting 1 million rows to Excel. Must use JPA Streaming (`Stream<Entity>`) instead of returning a `List`.

### Anti-Patterns
- **Using `FetchType.EAGER`**: Never use `EAGER` on `@OneToMany` or `@ManyToOne`. It forces JPA to always join the tables, even when you don't need the child data, leading to massive Cartesian products. Always use `LAZY` and fetch explicitly when needed.
- **Calling `.saveAll()` on 100,000 entities without batching**: It will crash the JVM memory because the persistence context tracks every single object.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất**:
1. **Luôn dùng `FetchType.LAZY`**: Chuyển toàn bộ `@ManyToOne` và `@OneToOne` sang `LAZY` (mặc định của Spring là `EAGER`).
2. **Bắt lỗi N+1 tự động**: Cài thư viện `datasource-proxy` hoặc `Hypersistence Optimizer` trên môi trường dev. Nếu nó thấy có N+1 query, nó sẽ quăng lỗi đỏ chót bắt dev sửa ngay lập tức.
3. **DTO Projections thay vì Entity**: Nếu bạn chỉ cần ID và Tiêu đề bài viết, đừng lấy cả cục `Post` chứa nội dung. Khai báo một Record `PostSummaryDto` và viết `SELECT new com.example.PostSummaryDto(p.id, p.title) FROM Post p`.
4. **Dùng `@Transactional(readOnly = true)`**: Với các API chỉ đọc (GET), thêm cái này vào để Hibernate không cần lưu Snapshot rác để theo dõi thay đổi (Dirty checking), tiết kiệm cực nhiều RAM.

**Cạm bẫy (Pitfalls)**:
1. **Phân trang (Pagination) cùng lúc với `JOIN FETCH` mảng (Collection)**: Nếu bạn JOIN bảng Con, dữ liệu trả về sẽ bị nhân bản (Cartesian). Hibernate sẽ không thể dùng `LIMIT/OFFSET` dưới SQL được nữa. Thay vào đó, nó lôi TOÀN BỘ dữ liệu lên RAM rồi cắt trang bằng Java. Nổ RAM là cái chắc!
   - *Cách sửa*: Thay vì JOIN FETCH, hãy gắn `@BatchSize(size = 50)` lên trên mảng `@OneToMany`.
2. **Khóa chính `IDENTITY` làm vô hiệu hóa Batching**: Nếu bạn dùng `@GeneratedValue(strategy = GenerationType.IDENTITY)` (thường thấy ở MySQL), Hibernate sẽ phải `INSERT` từng dòng một để lấy được ID do MySQL sinh ra. Batching bị vô hiệu hóa!
   - *Cách sửa*: Dùng `GenerationType.SEQUENCE` (PostgreSQL) hoặc dùng khóa chính UUID.

</details>

### Best Practices
1. **Always use `FetchType.LAZY`**: Change all `@ManyToOne` and `@OneToOne` to `LAZY` (they are `EAGER` by default).
2. **Detect N+1 Automatically**: Use a library like `datasource-proxy` or `Hypersistence Optimizer` in your local/test environments to throw exceptions if an N+1 query is detected.
3. **DTO Projections over Entities**: If you only need the `id` and `title` of a `Post`, do not return the `Post` entity. Define a Record `PostSummaryDto` and use `SELECT new com.example.PostSummaryDto(p.id, p.title) FROM Post p`. This saves memory and CPU.
4. **Use `@Transactional(readOnly = true)`**: For pure `GET` endpoints, this tells Hibernate to skip building the snapshot used for dirty checking, saving memory.

### Common Pitfalls
1. **Pagination with `JOIN FETCH` on Collections**: If you `JOIN FETCH` a `@OneToMany` collection and also use `Pageable`, Hibernate cannot do the pagination in SQL (because the number of rows multiplies). It will fetch *ALL* rows into JVM memory and paginate there, causing OutOfMemoryError. 
   - *Fix*: Use `@BatchSize(size = 50)` on the collection instead of `JOIN FETCH` when paginating.
2. **IDENTITY Id Generation disables Batching**: If your primary key uses `@GeneratedValue(strategy = GenerationType.IDENTITY)` (typical for MySQL), Hibernate *disables* JDBC batch inserts because it needs to execute the insert immediately to get the generated ID.
   - *Fix*: Use `GenerationType.SEQUENCE` (typical for PostgreSQL) or UUIDs to enable true batching.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là 2 đoạn code kinh điển: Cấu hình Batching để Insert hàng ngàn dòng siêu tốc, và Cấu hình Stream để xuất báo cáo Excel hàng triệu dòng mà RAM chỉ tốn một chút do đọc cuốn chiếu.

</details>

### Enabling JDBC Batching (application.yml)

```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 50
          order_inserts: true
          order_updates: true
        generate_statistics: true # Shows batch execution stats in logs
```

### High-Performance Data Streaming (Exporting millions of rows safely)

```java
import org.springframework.transaction.annotation.Transactional;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.QueryHints;
import jakarta.persistence.QueryHint;
import java.util.stream.Stream;
import static org.hibernate.jpa.HibernateHints.HINT_FETCH_SIZE;

// 1. Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Hint tells the JDBC driver to stream rows rather than load all into memory
    @QueryHints(value = {
        @QueryHint(name = HINT_FETCH_SIZE, value = "1000"),
        @QueryHint(name = "org.hibernate.readOnly", value = "true")
    })
    @Query("SELECT u FROM User u")
    Stream<User> streamAllUsers();
}

// 2. Service
@Service
public class ExportService {
    
    private final UserRepository userRepository;

    // MUST be transactional to keep the database cursor open
    @Transactional(readOnly = true)
    public void exportToCsv() {
        try (Stream<User> userStream = userRepository.streamAllUsers()) {
            userStream.forEach(user -> {
                // Process and write to CSV one by one.
                // The JVM only holds 1000 users (fetch size) in memory at a time.
                csvWriter.write(user);
            });
        } // Stream auto-closes here
    }
}
```

---

## Related Topics

- [Hexagonal & DDD](../02-software-architecture/hexagonal-and-ddd.md) — Why JPA entities shouldn't leak into the domain layer.
- [Database Fundamentals](../../01-fundamentals/database/) — Indexing, B-Trees, and Isolation Levels.
