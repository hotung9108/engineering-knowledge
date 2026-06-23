# Database Design: Schema & ERD

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước khi gõ bất kỳ dòng code nào, bạn phải thiết kế cấu trúc dữ liệu trên giấy. Quy trình này gọi là Data Modeling. Nó bắt đầu bằng việc vẽ Sơ đồ thực thể liên kết (**ERD** - Entity Relationship Diagram) để vạch rõ ai có quan hệ với ai (1-1, 1-Nhiều, Nhiều-Nhiều). Thiết kế sai CSDL từ đầu giống như xây móng nhà bị lệch, càng lên cao (thêm tính năng) thì nhà càng dễ sập.

</details>

> **Summary**: Before a single line of application code is written, the underlying data architecture must be meticulously modeled. This process, **Data Modeling**, culminates in the creation of an **ERD (Entity-Relationship Diagram)**. The ERD is the architectural blueprint defining Entities and their exact mathematical Cardinality (1:1, 1:N, M:N). A flawed initial schema design is analogous to pouring a crooked concrete foundation; as the application scales, the technical debt compounds until the system collapses under its own weight.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang phân công giường ngủ trong một Bệnh viện.
1. **Quan hệ 1-1 (1 Bệnh nhân - 1 Hồ sơ bệnh án)**: Mỗi người chỉ có đúng 1 cuốn sổ khám bệnh. Rất dễ quản lý.
2. **Quan hệ 1-N (1 Khoa - Nhiều Bệnh nhân)**: Khoa Nhi có 50 đứa trẻ. Nhưng 1 đứa trẻ thì không thể nằm ở Khoa Nhi và Khoa Sản cùng một lúc.
3. **Quan hệ N-N (Nhiều Bác sĩ - Nhiều Bệnh nhân)**: Bác sĩ A khám cho 10 bệnh nhân. Nhưng Bệnh nhân số 1 lại được khám bởi cả Bác sĩ A (Tim mạch) và Bác sĩ B (Dạ dày). Mối quan hệ này rối như tơ vò, bạn bắt buộc phải tạo ra một tờ giấy "Lịch khám" ở giữa để ghi chép ai khám ai. Tờ giấy đó gọi là **Bảng trung gian (Junction Table)**.

</details>

Imagine you are managing room assignments in a Hospital.
1. **One-to-One (1:1) [1 Patient : 1 Medical Record]**: Every patient has exactly one overarching medical file. Simple and linear.
2. **One-to-Many (1:N) [1 Department : Many Patients]**: The Pediatrics department houses 50 children. However, a single child cannot physically reside in both Pediatrics and Cardiology simultaneously.
3. **Many-to-Many (M:N) [Many Doctors : Many Patients]**: Dr. Smith treats 10 different patients. However, Patient X is treated by both Dr. Smith (Cardiology) and Dr. Jones (Neurology). This relationship is a tangled web. To manage it, you must create a new "Appointment Schedule" ledger in the middle to link a specific Doctor to a specific Patient at a specific time. This is a **Junction Table**.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Schema (Lược đồ)**: Là bản thiết kế chi tiết quy định CSDL có những Bảng (Tables) nào, các cột (Columns) kiểu gì (INT, VARCHAR), và các Ràng buộc (Constraints) như NOT NULL hay UNIQUE.
**2. ERD (Entity-Relationship Diagram)**: Bản vẽ đồ họa thể hiện Lược đồ trên. Nó dùng hình hộp để chỉ Thực thể (Bảng) và dùng các đường thẳng (Crow's Foot - Chân chim) để nối các bảng lại với nhau.
**3. Khóa (Keys)**:
- **Primary Key (PK - Khóa chính)**: Định danh duy nhất cho một hàng (Ví dụ: Số CCCD).
- **Foreign Key (FK - Khóa ngoại)**: Một cột trong Bảng A nhưng lại trỏ vào Khóa chính của Bảng B. Giúp 2 bảng liên kết với nhau.

</details>

**1. Schema**: The exact blueprint defining the logical structure of the database. It dictates the Tables, the specific Column Data Types (e.g., `INT`, `VARCHAR`, `TIMESTAMP`), and enforces mathematical Constraints (e.g., `UNIQUE`, `NOT NULL`, `CHECK > 0`).
**2. ERD (Entity-Relationship Diagram)**: The visual representation of the Schema. It utilizes boxes to represent Entities (Tables) and specific connector lines (typically Crow's Foot Notation) to explicitly define the cardinality of relationships between entities.
**3. Keys**:
- **Primary Key (PK)**: The absolute unique identifier for a single row within a table (e.g., an Auto-incrementing Integer or a UUID).
- **Foreign Key (FK)**: A column in Table A that explicitly references the Primary Key of Table B. This enforces **Referential Integrity**.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao không code luôn cho lẹ mà phải ngồi vẽ ERD?
Vì code thì sửa dễ, nhưng **Đổi cấu trúc Database lúc đang chạy thật (Production) là một cơn ác mộng**. Nếu bạn lỡ thiết kế Bảng "Khách Hàng" chỉ có 1 cột "SĐT". 3 năm sau công ty yêu cầu "Một khách hàng được phép có 3 SĐT". Bạn sẽ phải đập đi xây lại toàn bộ code, lôi hàng triệu dữ liệu cũ ra cắt gọt nhét vào bảng mới.
ERD sinh ra để toàn bộ Team (Dev, BA, Sếp) ngồi cãi nhau trên giấy cho tới khi chốt hạ được viễn cảnh tương lai 5 năm của hệ thống, rồi mới bắt tay vào làm.

</details>

Why spend weeks drawing diagrams instead of writing code immediately?
Because while Application Code is easy to refactor, **Executing Schema Migrations on a Live Production Database is an engineering nightmare**. 
If you naively design a `Customers` table with a single `phone_number` column, and 3 years later the Business mandates that "A customer can now have multiple phone numbers," you cannot easily change it. You must architect a massive zero-downtime migration to extract millions of phone numbers into a new 1:N table.
The ERD forces the entire cross-functional team (Engineers, Business Analysts, Stakeholders) to aggressively debate business edge cases *on paper*—where mistakes cost $0—before pouring the concrete.

---

## Layer 3: Without vs. With Comparison (Compare)

### Crow's Foot Notation (Cardinality)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Cách đọc sơ đồ Chân chim (Crow's Foot) trên ERD.
</details>

Understanding how to read the ends of the relationship lines in an ERD.

| Notation Name | Visual Symbol | Meaning (Cardinality) | Example |
|---|---|---|---|
| **One and Only One** | Two vertical lines (`||`) | Exactly 1. No more, no less. | 1 User has exactly 1 Identity Card. |
| **Zero or One** | Circle and vertical line (`O|`) | Optional. 0 or 1. | 1 User might have 0 or 1 Premium Subscription. |
| **One or Many** | Vertical line and Crow's Foot (`|<`) | At least 1, up to infinity. | 1 E-commerce Order MUST contain at least 1 Item. |
| **Zero or Many** | Circle and Crow's Foot (`O<`) | Optional infinity. | 1 User can write 0, 1, or 1000 Blog Posts. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cách giải quyết 3 mối quan hệ trong thực tế:
- **1-1 (One-to-One)**: Đặt Khóa ngoại (FK) ở bên nào cũng được. Hoặc gộp chung luôn thành 1 bảng cho nhanh.
- **1-N (One-to-Many)**: Khóa ngoại (FK) LUÔN LUÔN NẰM Ở BẢNG "NHIỀU" (N). Ví dụ: 1 Hóa Đơn có Nhiều Món Hàng $\rightarrow$ Bảng Món Hàng sẽ cầm cột `hoa_don_id`.
- **N-N (Many-to-Many)**: BẮT BUỘC phải tạo ra Bảng trung gian (Junction Table). Ví dụ: `Sinh_Vien` và `Mon_Hoc`. Bảng trung gian tên là `Dang_Ky_Hoc` chứa 2 cột FK: `sinh_vien_id` và `mon_hoc_id`.

</details>

How to physically implement Cardinality in SQL:
- **1:1 (One-to-One)**: The Foreign Key can be placed on either table (enforced with a `UNIQUE` constraint). Alternatively, simply merge them into a single table unless you are explicitly splitting them for performance/lazy-loading reasons.
- **1:N (One-to-Many)**: The Foreign Key MUST strictly reside on the **"Many" (N)** side. (e.g., 1 Publisher has Many Books $\rightarrow$ The `Books` table receives the `publisher_id` Foreign Key).
- **M:N (Many-to-Many)**: It is physically impossible to map M:N directly in a Relational Database. You MUST inject a **Junction Table** (Associative Entity) in the middle. (e.g., `Students` and `Courses`. Create a `Enrollments` table containing `student_id` and `course_id`).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khóa chính là Vô nghĩa (Surrogate Keys)**: Đừng bao giờ dùng Email hay Căn cước công dân làm Khóa chính. Khách hàng có quyền đổi Email, nếu Email là Khóa chính, bạn sẽ phải update hàng trăm bảng khác đang chĩa FK vào nó. Hãy luôn dùng một cột `ID` (Số tự tăng INT, hoặc UUID ngẫu nhiên) hoàn toàn vô nghĩa và ẩn khỏi mắt người dùng.
2. **Soft Delete (Xóa mềm)**: Đừng bao giờ gọi lệnh `DELETE` trong CSDL thật. Lỡ xóa nhầm hóa đơn là đi tù. Hãy thêm một cột `is_deleted = boolean`. Khi User bấm xóa, bạn chỉ việc Update cột đó thành `true` để ẩn đi trên giao diện. Dữ liệu vẫn còn nguyên ở dưới Database.

</details>

1. **Mandatory Surrogate Keys**: Never use Natural Keys (e.g., Email Address, SSN, or Product Serial Number) as a Primary Key. Natural keys represent business data, and business data *changes*. If a user changes their Email, and that Email is the PK, you must cascade that `UPDATE` across 50 child tables referencing it as a Foreign Key. Always utilize an arbitrary, meaningless **Surrogate Key** (an auto-incrementing `BIGINT` or a random `UUID`) that is entirely decoupled from business logic.
2. **Implement Soft Deletes**: Executing a hard `DELETE FROM users` in a production environment is incredibly dangerous. It triggers cascading deletes, permanently destroying historical relational data. Implement Soft Deletes: Add a `deleted_at (TIMESTAMP)` or `is_active (BOOLEAN)` column. When a user clicks "Delete", you merely execute an `UPDATE` to flag the row. The data is preserved indefinitely for auditing and recovery.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **God Table (Bảng Chúa tể)**: Dev lười suy nghĩ, dồn cả Tên, Địa chỉ, Sản phẩm, Giá tiền, Ngày giao hàng vào MỘT BẢNG DUY NHẤT có 50 cột. Bảng này vi phạm nguyên tắc Chuẩn hóa. Khi cần truy vấn, nó chậm như rùa bò và chứa đầy dữ liệu rác (NULL).
2. **Cứng nhắc với Khóa ngoại (FK Constraint)**: Ở các hệ thống siêu lớn (Microservices), các công ty thường KHÔNG thiết lập Khóa ngoại vật lý trong SQL (bỏ qua lệnh `ADD FOREIGN KEY`). Vì Khóa ngoại ép CSDL phải check chéo liên tục làm giảm tốc độ Insert. Họ đẩy việc quản lý quan hệ lên tầng Code (Application Logic). Nhưng với dự án nhỏ/vừa, KHÔNG CÓ FK LÀ TỰ SÁT.

</details>

1. **The "God Table" Anti-pattern**: Attempting to bypass Normalization completely by constructing a massive, 60-column monolithic table containing User Info, Order History, and Payment Details in a single row. This leads to horrific Update Anomalies, massive Storage Bloat (thousands of `NULL` fields), and destroys caching mechanisms.
2. **Blindly Enforcing Physical Foreign Keys at Scale**: For 95% of applications, physical FK Constraints in the Database are mandatory for data safety. However, at extreme Enterprise scales (e.g., Sharded Architectures or Microservice boundaries), enforcing cross-shard physical FKs introduces catastrophic locking latency. Giant tech companies often drop physical FK constraints, enforcing Referential Integrity strictly within the Application Code Layer instead.

---

## Related Topics

- For the mathematical rules that drive ERDs, see **[SQL Fundamentals](./sql-fundamentals.md)**.
- If an ERD becomes too complex to scale horizontally, consider **[NoSQL Fundamentals](./nosql-fundamentals.md)**.
- Making sure queries run fast across joined tables requires **[Query Optimization](./query-optimization.md)**.
