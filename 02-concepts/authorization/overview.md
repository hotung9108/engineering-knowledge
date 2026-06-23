# Authorization Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Authentication (Xác thực) trả lời câu hỏi "Bạn là ai?", thì **Authorization (Phân quyền)** trả lời câu hỏi: **"Bạn được phép làm gì?"**. Sau khi bác bảo vệ cho bạn vào tòa nhà (Xác thực xong), hệ thống phân quyền sẽ quyết định xem thẻ của bạn có được quẹt để mở cửa thang máy lên tầng Giám đốc hay không. Trong kiến trúc phần mềm, Authorization phức tạp hơn Authentication rất nhiều vì nó gắn liền với nghiệp vụ logic của từng công ty.

</details>

> **Summary**: While Authentication (AuthN) resolves identity ("Who are you?"), **Authorization (AuthZ)** determines privileges: **"What are you allowed to do?"** Once a system establishes trust in an identity, it must evaluate rules, roles, and context to grant or deny access to protected resources. In software architecture, Authorization is significantly more complex than Authentication because it is tightly coupled to highly specific, constantly changing business logic and domain rules.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đi xem phim ở rạp.
1. **Authentication (Xác thực)**: Bạn mua vé và đưa cho nhân viên xé vé. Nhân viên nhìn bạn, xé vé và cho bạn vào trong sảnh. Bạn đã được "Xác thực" là khách hàng hợp lệ.
2. **Authorization (Phân quyền)**:
   - Bạn định đi vào Phòng Chiếu VIP $\rightarrow$ Nhân viên chặn lại: "Vé của bạn là vé thường, không được vào phòng VIP". (Bị từ chối phân quyền).
   - Bạn định mở cửa Phòng Máy Chiếu phim $\rightarrow$ Quản lý chặn lại: "Chỉ có nhân viên kỹ thuật mới được vào đây!". (Bị từ chối phân quyền).
   - Bạn đi đúng vào Phòng Chiếu số 3 (như ghi trên vé) $\rightarrow$ Bạn được vào xem phim bình thường. (Phân quyền thành công).

</details>

Imagine attending a theater.
1. **Authentication (AuthN)**: You purchase a ticket and present it to the usher. The usher verifies the ticket is real and allows you into the main lobby. You are now an authenticated guest.
2. **Authorization (AuthZ)**:
   - You attempt to enter the VIP Lounge $\rightarrow$ The usher stops you: "Your ticket does not include VIP privileges." (Access Denied based on Role).
   - You attempt to enter the Projectionist Room $\rightarrow$ Security stops you: "Only employed staff are permitted here." (Access Denied based on Attribute/Identity).
   - You walk into Theater Room 3, matching your ticket $\rightarrow$ You sit down and enjoy the movie. (Access Granted).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Authorization là quá trình kiểm tra (Policy Enforcement) xem một **Subject** (Người dùng/Hệ thống) có được phép thực hiện một **Action** (Hành động: Đọc, Ghi, Xóa) lên một **Resource** (Tài nguyên: Dữ liệu, Nút bấm, File) cụ thể hay không.

Nó hoạt động dựa trên ma trận phân quyền. Tùy vào độ phức tạp, có nhiều mô hình khác nhau:
1. Bạn có là Admin không? (Role-Based).
2. Bạn có thuộc phòng Kế toán và truy cập trong giờ hành chính không? (Attribute-Based).
3. Bài viết này do CHÍNH BẠN viết ra đúng không? (Resource-Based / Ownership).

</details>

Authorization is the architectural process of Policy Enforcement. It strictly evaluates whether a specific **Subject** (User, System, or Service) is permitted to execute a specific **Action** (Read, Write, Delete, Execute) on a specific **Resource** (Database Row, API Endpoint, File).

It operates by evaluating access control matrices or dynamic policies. Depending on complexity, access is granted based on:
1. What label you have (Role-Based).
2. What specific characteristics you and the environment possess (Attribute-Based).
3. Whether you explicitly own the targeted data (Resource/Ownership-Based).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu không có Authorization, hệ thống sẽ rơi vào tình trạng "Vào được nhà là lấy được hết đồ".
Ví dụ: Bạn là người dùng bình thường đăng nhập vào ứng dụng Ngân hàng.
- Không có AuthZ: Bạn có thể gọi API `GET /users/admin/balance` và xem được tài khoản của sếp, hoặc gọi `DELETE /users/1` để xóa luôn tài khoản người khác.
- Có AuthZ: Hệ thống sẽ chặn lại bằng mã lỗi `HTTP 403 Forbidden` (Tôi biết bạn là ai, nhưng bạn không có cửa làm việc này).

</details>

Without Authorization, systems suffer from a fatal flaw known as **Broken Access Control** (Consistently ranked as the #1 vulnerability on the OWASP Top 10).
For example, a standard user successfully logs into a Banking API.
- Without AuthZ: The user can maliciously modify the URL to `GET /accounts/999` and view another customer's balance, or execute `POST /transfer` to drain someone else's funds. This is an Insecure Direct Object Reference (IDOR).
- With AuthZ: The backend evaluates the request, detects that the user ID does not match the account ID being requested, and violently terminates the request with an `HTTP 403 Forbidden` response.

---

## Layer 3: Without vs. With Comparison (Compare)

### API Security Implementation

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt trong tư duy lập trình Backend khi áp dụng Phân quyền.
</details>

Visualizing the code-level difference when securing an endpoint.

| Concept | Authentication Only (Vulnerable) | Full Authorization (Secure) |
|---|---|---|
| **API Endpoint** | `DELETE /articles/50` | `DELETE /articles/50` |
| **Step 1: AuthN**| Check JWT $\rightarrow$ Valid User (ID: 10) | Check JWT $\rightarrow$ Valid User (ID: 10) |
| **Step 2: Logic**| Execute `DB.delete(article_50)` | Fetch Article 50 from DB. |
| **Step 3: AuthZ**| (None) | Check: Is User 10 an `Admin`? OR Is User 10 the `author_id` of Article 50? |
| **Result** | **Breached**. Any user can delete any article. | **Safe**. Returns `403 Forbidden` if User 10 is not the owner. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Phân quyền tĩnh (Static/Role-Based)**: Ứng dụng CMS (Quản lý nội dung) có các vai trò rõ ràng: `Admin` (Được làm mọi thứ), `Editor` (Được sửa bài viết), `Viewer` (Chỉ được xem). Cấu hình này hiếm khi thay đổi.
- **Phân quyền theo ngữ cảnh (Dynamic/Attribute-Based)**: Hệ thống bệnh viện. Bác sĩ chỉ được xem hồ sơ bệnh án của Bệnh nhân đang điều trị, và chỉ được xem trong giờ trực của mình. Đòi hỏi logic if/else rất phức tạp dựa trên thời gian, địa điểm, phòng ban.
- **Phân quyền Microservices**: Ở hệ thống lớn, thay vì mỗi con Service tự viết code if/else phân quyền, người ta tách hẳn phần kiểm tra quyền ra một hệ thống riêng gọi là Policy Engine (Ví dụ: OPA - Open Policy Agent).

</details>

- **Static Access Control (B2B SaaS / CMS)**: Utilizing static roles. An application dictates that an `Admin` can access the billing dashboard, a `Manager` can invite users, and a `User` can only read documents. The logic is strictly tied to a `role` string embedded in the JWT.
- **Dynamic / Contextual Access Control (Healthcare/Finance)**: Utilizing attributes. A doctor is authorized to view a patient's medical records *only if* the patient is actively assigned to them, *and* the request is made from the hospital's internal IP address, *and* the doctor is currently on shift. This requires dynamic evaluation of attributes.
- **Decentralized Policy Enforcement (Microservices)**: In massive distributed systems, hardcoding authorization `if/else` statements across 50 microservices creates unmaintainable technical debt. Architects decouple Authorization into a centralized, dedicated engine (like OPA - Open Policy Agent) that evaluates requests across the entire cluster using a unified policy language.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Deny by Default (Từ chối mặc định)**: Nguyên tắc vàng. Mọi API, mọi nút bấm, mọi thư mục phải bị khóa kín theo mặc định. Chỉ mở cửa khi có luật (Rule) cho phép rõ ràng. Nếu bạn quên viết code Phân quyền cho một API mới tạo, nó phải tự động khóa, thay vì tự động mở.
2. **Kiểm tra quyền ở mọi lớp (Defense in Depth)**: Đừng chỉ ẩn nút "Xóa" trên giao diện Frontend (React/Vue). Hacker có thể mở Postman và gọi thẳng API `DELETE` của Backend. BẮT BUỘC phải kiểm tra quyền ở Backend trước khi đụng vào Database.

</details>

1. **Deny by Default (Implicit Deny)**: The absolute golden rule of Authorization architecture. Unless an explicit rule grants access, access MUST be denied. If a developer creates a new API endpoint and glazes over the authorization middleware, the system must aggressively block all traffic to it (`403 Forbidden`). Permissive-by-default systems inevitably leak data.
2. **Defense in Depth (Never Trust the Client)**: Hiding the "Delete" button in the React UI based on user roles is an essential UX practice, but it is *Zero-Trust Security*. Attackers routinely bypass the UI and execute raw API requests via `curl` or Postman. Authorization MUST be enforced immutably at the Backend API layer, precisely at the moment the Database mutation is requested.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lỗi IDOR (Insecure Direct Object Reference)**: Lỗi sơ đẳng nhưng cực kỳ phổ biến. Backend chỉ kiểm tra xem người dùng đã đăng nhập chưa, sau đó lấy bừa cái ID trên thanh URL (`/invoices/12345`) để truy vấn DB và trả về kết quả. Không hề kiểm tra xem hóa đơn `12345` có phải của người đó không.
2. **Gắn cứng quyền vào Code (Hardcoding)**: Viết code kiểu `if (user_id == 5) { do_something() }`. Khi nhân viên số 5 nghỉ việc, bạn phải tìm sửa lại toàn bộ Source code và deploy lại hệ thống. Phải luôn quản lý quyền thông qua Database.

</details>

1. **IDOR (Insecure Direct Object Reference)**: A catastrophic failure of resource-level authorization. A user is authenticated, they request `GET /invoices/99`, and the backend naively executes `SELECT * FROM invoices WHERE id = 99` without verifying ownership. **Fix**: The SQL query MUST mandate ownership: `SELECT * FROM invoices WHERE id = 99 AND owner_id = <ID_From_JWT>`.
2. **Hardcoding Authorization Logic**: Writing hardcoded conditional statements like `if (user.email == 'ceo@company.com') allow_access()`. When the CEO resigns, the entire application must be halted, rewritten, recompiled, and redeployed. **Fix**: Abstract privileges into a database or a Policy Engine, allowing dynamic updates without touching the monolithic codebase.

---

## Related Topics

- For the identity verification step that precedes Authorization, see **[Authentication Overview](../authentication/overview.md)**.
- To explore specific coding implementations like RBAC and ABAC, read **[Implementation Patterns](./implementation-patterns.md)**.
- For API-level security enforcement, review **[API Security](../../01-fundamentals/security/api-security.md)**.
