# Authorization Implementation Patterns

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Phân quyền (Authorization) không có một giải pháp dùng chung cho tất cả. Nếu bạn làm một cái Blog nhỏ, bạn chỉ cần hệ thống phân quyền đơn giản (RBAC). Nhưng nếu bạn làm hệ thống quản lý Bệnh viện, bạn cần hệ thống cực kỳ chi tiết dựa trên thời gian, địa điểm, và loại bệnh nhân (ABAC). Dưới đây là 3 mô hình (Pattern) phổ biến nhất để lập trình tính năng phân quyền: ACL, RBAC, và ABAC.

</details>

> **Summary**: There is no "silver bullet" for Authorization. The complexity of your authorization architecture must scale proportionally with your domain's requirements. A personal blog requires trivial role checks (RBAC), whereas a military-grade intelligence system requires granular, context-aware rule engines (ABAC). This document breaks down the three foundational Authorization patterns utilized in software engineering: ACL (Access Control Lists), RBAC (Role-Based Access Control), and ABAC (Attribute-Based Access Control).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn tổ chức một bữa tiệc:
1. **ACL (Danh sách khách mời)**: Bảo vệ cầm một tờ giấy ghi tên: "Tùng, Nam, Hoa". Cứ ai đúng tên trong tờ giấy thì cho vào. (Dễ làm, nhưng nếu có 10.000 khách thì tờ giấy dài dằng dặc).
2. **RBAC (Vé hạng VIP/Thường)**: Bảo vệ không thèm quan tâm tên bạn. Bạn giơ vé ra. "Vé Vàng" được lên khu vực VIP uống rượu. "Vé Bạc" chỉ được đứng ở tầng trệt. (Quản lý cực nhàn, phân nhóm rõ ràng).
3. **ABAC (Luật lệ phức tạp)**: Bảo vệ kiểm tra 3 thứ: Bạn có "Vé Vàng" không? Bạn trên 18 tuổi chưa? Và bây giờ có phải sau 22h đêm không? Thỏa mãn cả 3 thì mới cho lên khu vực VIP. (Siêu phức tạp, bảo mật tuyệt đối).

</details>

Imagine hosting an exclusive nightclub event.
1. **ACL (Access Control List)**: The Bouncer holds a literal clipboard with names ("John, Alice, Bob"). If your specific name is on the clipboard, you enter. (Easy for 10 people, impossible to manage for 10,000).
2. **RBAC (Role-Based Access Control)**: The Bouncer ignores your name and only looks at your Wristband. `Red Wristband` = VIP Lounge. `Blue Wristband` = General Admission. (Highly scalable, groups people by category).
3. **ABAC (Attribute-Based Access Control)**: The Bouncer runs a complex algorithm. You are granted VIP access *if* [Wristband == Red] AND [Age >= 21] AND [Current_Time < Midnight]. (Infinitely flexible, high computational overhead).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. ACL (Access Control List - Danh sách kiểm soát truy cập)**
Là một bảng map trực tiếp `User <-> Resource`. Bảng này dán thẳng vào đối tượng cần bảo vệ.
Ví dụ: File Word tên `bao-cao.docx` có gắn một danh sách: `Tùng: Đọc/Ghi`, `Nam: Chỉ Đọc`.

**2. RBAC (Role-Based Access Control - Kiểm soát truy cập theo Vai trò)**
Thay vì gán thẳng User vào Resource, ta đẻ ra một khâu trung gian gọi là **Role (Vai trò)**. Ta gán Quyền vào Role, rồi gán Role vào User.
Ví dụ: Tạo Role `Admin` (Được sửa, Xóa). Gán Tùng và Nam vào nhóm `Admin`.

**3. ABAC (Attribute-Based Access Control - Kiểm soát truy cập theo Thuộc tính)**
Không dùng nhóm cố định nữa. Hệ thống đánh giá dựa trên Thuộc tính (Attribute) của `User`, `Resource`, và `Môi trường (Environment)`.
Ví dụ: "Nhân viên" (User) chỉ được "Sửa" (Action) "Tài liệu phòng Nhân sự" (Resource) trong "Giờ hành chính từ máy tính công ty" (Environment).

</details>

**1. ACL (Access Control List)**
A direct, explicitly defined mapping between a `Subject` and a `Resource`. The permissions are attached directly to the data.
*Example*: A Google Drive file `budget.xlsx` has an internal list: `[john@a.com: Editor, bob@a.com: Viewer]`.

**2. RBAC (Role-Based Access Control)**
Introduces a layer of abstraction. Instead of mapping Users to Resources, Permissions are mapped to **Roles**, and Roles are assigned to Users.
*Example*: `Role: Manager` has `[Can_Hire, Can_Fire]`. `User: Alice` is assigned the `Manager` Role.

**3. ABAC (Attribute-Based Access Control)**
The most granular paradigm. It evaluates boolean logic against dynamic attributes of the `Subject` (User), the `Resource`, and the `Environment` (Context).
*Example*: `IF Subject.Department == Resource.Department AND Environment.IP_Address IN Corporate_Subnet THEN Allow`.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Từ ACL lên RBAC**: ACL quá đau khổ khi công ty phình to. Nếu bạn có 100 nhân viên mới vào làm, bạn phải đi mở 1000 file Word ra để thêm tay từng tên người vào ACL của từng file. Với RBAC, bạn chỉ cần ném 100 người đó vào Role `Nhân_viên`, lập tức họ có quyền xem 1000 file Word kia.
**Từ RBAC lên ABAC**: RBAC lại bị lỗi "Bùng nổ Vai trò" (Role Explosion). Khi logic phức tạp, bạn sẽ phải tạo ra những Role nực cười như: `KeToan_LamCaDem_ChiDuocXem`. Cứ mỗi logic mới là đẻ thêm một Role. ABAC ra đời để dập tắt chuyện đó bằng cách dùng các phép toán `IF/ELSE` trên thuộc tính.

</details>

**The Evolution from ACL to RBAC**: ACLs become an administrative nightmare at scale. If a company hires 50 new engineers, IT must manually modify the ACLs of 5,000 distinct GitHub repositories, AWS buckets, and internal docs to explicitly add their names. With RBAC, IT simply assigns the 50 engineers to the `Engineering` Role, instantly granting them inherited access to all 5,000 resources.
**The Evolution from RBAC to ABAC**: RBAC fails miserably when context matters, leading to **Role Explosion**. If rules become complex, administrators are forced to create absurd, hyper-specific Roles (e.g., `Manager_US_East_NightShift_ReadOnly`). ABAC obliterates Role Explosion by evaluating real-time attributes natively, keeping the system clean and infinitely flexible.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh độ phức tạp của 3 mô hình khi áp dụng vào Code.
</details>

Visualizing the implementation complexity across the three patterns.

| Feature | ACL | RBAC | ABAC |
|---|---|---|---|
| **Mapping** | User $\rightarrow$ Resource | User $\rightarrow$ Role $\rightarrow$ Resource | Rule(User, Resource, Environment) |
| **Code Logic** | `if resource.acl.contains(user.id)` | `if user.role == 'admin'` | `if user.dept == res.dept && time < 17:00` |
| **Scalability** | Extremely Low | High (for static structures) | Very High (for dynamic rules) |
| **Role Explosion**| N/A | High Risk | Eradicated |
| **Best For** | File Systems (Windows/Linux/Google Drive) | Internal B2B Dashboards | Healthcare, Banking, Military |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **ACL (Hệ điều hành / File)**: Khi bạn chuột phải vào 1 thư mục trên Windows, chọn Properties $\rightarrow$ Security. Bạn đang chỉnh sửa ACL. Google Drive (Share cho 1 Email cụ thể) cũng là ACL.
2. **RBAC (Hệ thống CMS / SaaS)**: Các ứng dụng B2B như Slack, Jira, WordPress. Người dùng mua gói phần mềm, ông Giám đốc tự phân quyền cho lính của mình thành `Owner`, `Admin`, `Member`.
3. **ABAC (Hệ thống Y tế / Ngân hàng / Chính phủ)**: AWS IAM (Identity and Access Management) là một hệ thống ABAC khổng lồ. Bạn có thể viết luật: "Chỉ cho phép EC2 ghi vào S3 bucket này nếu xuất phát từ IP công ty và request phải có gán mác môi trường là 'Production'".

</details>

1. **ACL (File Systems & Explicit Sharing)**: The foundation of OS Security. `chmod 777` in Linux modifies an ACL. Google Drive's "Share with specific people via Email" relies heavily on underlying ACL mapping tables.
2. **RBAC (B2B SaaS & Internal Dashboards)**: The industry standard for 90% of web applications. Platforms like Jira, Slack, or WordPress rely on static roles (`Admin`, `Editor`, `Viewer`) to gate UI components and backend endpoints. It is easily encapsulated within a JWT payload (`"role": "admin"`).
3. **ABAC (Cloud Infrastructure & High-Security Compliance)**: AWS IAM Policies are the ultimate manifestation of ABAC. You can author JSON policies granting `s3:PutObject` *only if* `aws:SourceIp` matches a CIDR block AND `aws:RequestedRegion` is `us-east-1` AND the resource tag `Environment` equals `Production`.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Đừng đâm đầu vào ABAC quá sớm**: Hệ thống ABAC cực kỳ tốn công sức để thiết kế và chạy rất chậm (vì phải check quá nhiều điều kiện `IF`). Nếu bạn mới khởi nghiệp hoặc làm dự án nhỏ, hãy dùng RBAC.
2. **Tách biệt Data và Logic Phân quyền**: Đừng rải rác các câu lệnh `if (user.role === 'admin')` đi khắp 1000 file code của bạn. Hãy dồn nó vào một file duy nhất (Middleware) hoặc dùng Policy Engine như **OPA (Open Policy Agent)**.

</details>

1. **YAGNI (You Aren't Gonna Need It) on ABAC**: Do not over-engineer your MVP with an ABAC architecture. ABAC requires complex Policy Decision Points (PDP) and incurs massive latency overhead due to heavy database queries (fetching user attributes, resource attributes). Start with a rigid RBAC structure. Only pivot to ABAC when Business Requirements strictly mandate contextual compliance.
2. **Decouple Policy from Business Logic**: Do not litter your core business services with hardcoded `if (user.role == "Admin")`. Abstract authorization out. In monolithic apps, use localized Middleware (e.g., Spring Security annotations, ExpressJS guards). In distributed microservices, offload decision-making entirely to external Policy Engines like **OPA (Open Policy Agent)** using the Rego language.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Role Explosion trong RBAC**: Khách hàng A nói: "Tôi muốn thằng Quản lý chỉ được quyền Xóa bài viết của chính nó chứ không được Xóa bài người khác". Thế là bạn tạo ra cái Role tên là `Manager_DeleteOwnPost`. Khách hàng B lại đòi: "Tôi muốn Quản lý xóa được bài người khác nhưng chỉ trong giờ hành chính". Thế là bạn đẻ ra Role `Manager_DeleteAll_OfficeHours`. Dần dần bạn có 1000 Roles rác rưởi không thể quản lý. 
   - *Cách giải quyết*: Khi RBAC bắt đầu có dấu hiệu phình to vì các yêu cầu "Ngữ cảnh", đó là lúc bắt buộc phải đập đi xây lại bằng ABAC.
2. **Kiểm tra quyền trên Frontend (Ảo tưởng bảo mật)**: Bạn giấu nút "Xóa" trên giao diện React vì User không có quyền. Bạn cho rằng thế là an toàn và KHÔNG viết code chặn trên API Backend. Hacker dùng Postman gửi request thẳng vào API và xóa bay màu dữ liệu của bạn.

</details>

1. **The RBAC "Role Explosion" Trap**: In an attempt to satisfy complex client requirements without migrating to ABAC, architects create hyper-specific, combinatorial roles. (e.g., `HR_Manager_US_Read_Only`, `HR_Manager_EU_Full_Access`). This leads to a database polluted with thousands of overlapping roles, rendering security auditing impossible. **Fix**: Recognize when business logic transitions from Static (RBAC-friendly) to Contextual (ABAC-required), and migrate gracefully.
2. **Client-Side Security Illusion**: Implementing robust UI state management (hiding buttons, disabling routes) in React/Angular based on the User's Role, but failing to mirror those identical checks in the Backend API controllers. The Frontend is untrusted territory. It is merely a UX convenience. **Absolute Rule**: Authorization must always be executed server-side.

---

## Related Topics

- For a high-level theoretical overview, see **[Authorization Overview](./overview.md)**.
- To understand how identity is verified before authorization begins, see **[Authentication Overview](../authentication/overview.md)**.
- To see how microservices enforce ABAC policies, read about **[System Design / Architecture](../../10-system-design/)**.
