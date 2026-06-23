# Semantic Versioning (SemVer)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Đặt tên phiên bản phần mềm không phải là việc hứng lên là đặt (Ví dụ: `v1.0-final-chac-chan-khong-sua-nua.zip`). Ngành phần mềm thống nhất sử dụng chuẩn **Semantic Versioning (SemVer)** với cấu trúc `MAJOR.MINOR.PATCH` (Ví dụ: `v2.4.1`). Cách đánh số này như một bản hợp đồng ngầm giữa người viết thư viện và người sử dụng thư viện, báo cho họ biết bản cập nhật mới có làm sập code cũ của họ hay không.

</details>

> **Summary**: Software versioning is not a subjective naming exercise (e.g., `v1.0-final-final-really-done.zip`). The engineering industry adheres to a rigid specification called **Semantic Versioning (SemVer)**, structured as `MAJOR.MINOR.PATCH` (e.g., `v2.4.1`). This nomenclature acts as an implicit legal contract between a software publisher and its consumers, explicitly communicating the risk of breaking changes in new releases.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang nâng cấp một chiếc Xe ô tô (Phiên bản `v1.0.0`).
1. **PATCH (`v1.0.1`)**: Bạn thay cái lốp xe bị thủng. Xe vẫn là cái xe cũ, chạy y như cũ. Không ai bị sốc.
2. **MINOR (`v1.1.0`)**: Bạn lắp thêm một cái Radio Bluetooth. Bất cứ ai biết lái bản `1.0` vẫn thừa sức lái bản `1.1` này (Khả năng tương thích ngược - Backward compatible).
3. **MAJOR (`v2.0.0`)**: Bạn đổi từ xe số Tự động sang xe số Sàn, và chuyển vô-lăng từ bên trái sang bên phải. Những người đang quen lái bản `1.0` bước lên bản `2.0` sẽ gây tai nạn ngay lập tức! (Phá vỡ tương thích - Breaking changes).

</details>

Imagine you are releasing updates to a specific Car model (Version `v1.0.0`).
1. **PATCH (`v1.0.1`)**: You replace a defective tire. The fundamental driving experience is identical. It is a bug fix.
2. **MINOR (`v1.1.0`)**: You install a new Bluetooth Radio system. Anyone who knew how to drive `v1.0` can flawlessly drive `v1.1`, they just have new features available if they want to use them (Backward compatible).
3. **MAJOR (`v2.0.0`)**: You convert the transmission from Automatic to Manual, and move the steering wheel from the left side to the right side. Drivers accustomed to `v1.0` will immediately crash if they attempt to drive `v2.0`! (Breaking changes).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Semantic Versioning** quy định mã phiên bản gồm 3 chữ số: `MAJOR.MINOR.PATCH` (X.Y.Z).
- **PATCH (Z)**: Tăng lên (VD: 1.0.0 $\rightarrow$ 1.0.1) khi bạn sửa một Bug mà không làm thay đổi bất kỳ tính năng (API) nào đang có.
- **MINOR (Y)**: Tăng lên (VD: 1.0.1 $\rightarrow$ 1.1.0) khi bạn ra mắt thêm một Tính năng mới (API mới), nhưng tuyệt đối không được làm hỏng các tính năng cũ. Phải reset PATCH về 0.
- **MAJOR (X)**: Tăng lên (VD: 1.1.0 $\rightarrow$ 2.0.0) khi bạn thay đổi thiết kế cốt lõi, xóa bỏ API cũ, hoặc thay đổi cách dùng khiến code của người dùng cũ BỊ LỖI (Breaking changes). Phải reset MINOR và PATCH về 0.

</details>

**Semantic Versioning** dictates a three-part version number: `MAJOR.MINOR.PATCH` (X.Y.Z).
- **PATCH (Z)**: Incremented (e.g., 1.0.0 $\rightarrow$ 1.0.1) when you implement backwards-compatible bug fixes. The API surface remains strictly untouched.
- **MINOR (Y)**: Incremented (e.g., 1.0.1 $\rightarrow$ 1.1.0) when you introduce new, backwards-compatible functionality or APIs. Previous methods still exist and function identically. The PATCH number resets to 0.
- **MAJOR (X)**: Incremented (e.g., 1.1.0 $\rightarrow$ 2.0.0) when you introduce **Breaking Changes**. This means deleting existing APIs, fundamentally altering signatures, or forcing the consumer to rewrite their code to upgrade. MINOR and PATCH reset to 0.

*Note: Pre-release identifiers (e.g., `v1.0.0-alpha.1`) can be appended to indicate unstable builds.*

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề (Dependency Hell)**: Trong thời đại Node.js (`npm`), Java (`Maven`), một dự án của bạn có thể xài tới 1,000 thư viện nguồn mở. Nếu bạn cấu hình "Luôn tải thư viện mới nhất", một ngày đẹp trời thư viện A đổi cách viết code. Tự nhiên dự án của bạn sập toàn bộ mà bạn không hề sửa dòng code nào.

**Giải pháp (SemVer)**:
SemVer tạo ra lòng tin. Khi nhìn thấy React nâng cấp từ `17.0.1` lên `17.0.2` (PATCH), bạn nhắm mắt cập nhật vì biết chắc code không vỡ. Nhưng khi thấy React lên `18.0.0` (MAJOR), bạn phải ĐỨNG LẠI, đọc tài liệu, và chuẩn bị tâm lý sửa code vì chắc chắn có hàm cũ bị xóa bỏ.

</details>

**The Problem (Dependency Hell)**: Modern software is aggressively modular. A standard Node.js (`npm`) or Java (`Maven`) project might import 1,000 transitive external packages. If developers configure their package managers to "always download the newest version," a random library author changing a function signature from `save(id)` to `save(user, id)` will instantly shatter your production server, even though you didn't touch your own code.

**The Solution (Predictability)**:
SemVer establishes mathematical predictability and developer trust. When a developer sees a library update from `17.0.1` to `17.0.2` (PATCH), they allow automated tools (like Dependabot) to merge it blindly, trusting it's just a bug fix. But when they see a bump to `18.0.0` (MAJOR), they HALT. The MAJOR bump explicitly warns: "Read the migration guide. Your code *will* break."

---

## Layer 3: Without vs. With Comparison (Compare)

### Package.json Dependency Operators (npm example)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Trong các file quản lý thư viện (như `package.json`), bạn sẽ thấy các dấu `^` hoặc `~` đứng trước số phiên bản. Chúng chính là các lệnh tự động hóa dựa trên SemVer.
</details>

Package managers utilize SemVer to automatically resolve safe updates. Understanding the modifiers (Caret vs. Tilde) is critical.

| Symbol | Example | Meaning (What will it auto-update to?) | Safety Level |
|---|---|---|---|
| **Exact** | `"react": "18.2.0"` | ONLY installs exact `18.2.0`. No auto-updates. | Safest, but ignores bug fixes. |
| **Tilde (`~`)** | `"react": "~18.2.0"` | Auto-updates **PATCH** versions (`18.2.1`, `18.2.9`). Rejects MINOR (`18.3.0`). | Safe bug fixes only. |
| **Caret (`^`)** | `"react": "^18.2.0"` | Auto-updates **MINOR & PATCH** (`18.3.0`, `18.9.9`). Rejects MAJOR (`19.0.0`). | Safe new features + bug fixes. (Standard Default). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Version 0.y.z (Khởi đầu)**: Khi bắt đầu làm dự án, hãy để version `0.1.0`. Số `0` ở đầu báo hiệu: "Dự án này chưa ổn định, tôi có thể đổi code (Breaking change) bất cứ lúc nào mà không thèm báo MAJOR".
- **Version 1.0.0 (Công bố)**: Đánh dấu API Public của bạn đã chính thức đi vào hoạt động ổn định. Bắt đầu áp dụng luật SemVer khắt khe từ đây.
- **REST API Versioning**: SemVer không chỉ áp dụng cho mã nguồn, mà còn cho cả API. Các công ty thường nhúng MAJOR version vào URL (VD: `api.stripe.com/v1/payments`). Nếu họ đổi thiết kế API, họ sẽ ra URL mới `.../v2/...` để không giết chết các khách hàng đang dùng `v1`.

</details>

- **Version `0.y.z` (Rapid Prototyping Phase)**: When initializing a new library, start at `0.1.0`. A major version of `0` signals to the world: "This software is unstable. The API is volatile. I reserve the right to introduce Breaking Changes in a MINOR release."
- **Version `1.0.0` (Production Hardening)**: The moment you release `1.0.0`, you lock down your Public API. From this moment forward, you are legally bound to strictly follow SemVer. You cannot silently break consumers.
- **REST API Endpoint Versioning**: SemVer principles govern URL routing. Enterprise APIs embed the MAJOR version directly into the path (e.g., `api.stripe.com/v1/charges`). When Stripe redesigns the payload structure (a Breaking Change), they launch `/v2/charges`, keeping `/v1` alive indefinitely to prevent destroying their legacy clients' businesses.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khóa File Dependencies (Lock Files)**: Luôn đưa file `package-lock.json` (Node), `poetry.lock` (Python) hoặc `go.sum` (Go) lên Git. File Lock ghi lại chính xác tuyệt đối phiên bản thư viện con để đảm bảo mọi dev trong team cài đặt ra một hệ thống y hệt nhau tới từng byte.
2. **Conventional Commits**: Dùng SemVer kết hợp với quy tắc Commit. Ví dụ: Nếu bạn commit bắt đầu bằng `fix: ...` $\rightarrow$ Tự động tăng PATCH. Nếu commit là `feat: ...` $\rightarrow$ Tự động tăng MINOR. Nếu `BREAKING CHANGE: ...` $\rightarrow$ Tự động tăng MAJOR.

</details>

1. **Mandatory Lock Files**: SemVer ranges (`^` and `~`) in your `package.json` introduce variability. If two developers run `npm install` on different days, they might get different PATCH versions, violating CI/CD reproducibility. Always commit the **Lock File** (e.g., `package-lock.json`, `poetry.lock`, `Cargo.lock`) to Version Control. Lock files enforce a mathematically identical dependency tree (down to the exact SHA hash) across all environments.
2. **Automated Versioning via Conventional Commits**: Combine SemVer with structured Git commit messages. Tools like `semantic-release` parse your commit history:
   - If it sees `fix: memory leak` $\rightarrow$ Automates a PATCH release.
   - If it sees `feat: add oauth2` $\rightarrow$ Automates a MINOR release.
   - If it sees `BREAKING CHANGE: dropped java 11 support` $\rightarrow$ Automates a MAJOR release.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hội chứng Sợ MAJOR (Major Version Phobia)**: Dev sợ việc tăng lên bản `v2.0` hoặc `v3.0` vì nghĩ số lớn quá trông "kiêu ngạo" hoặc sợ người dùng không dám tải. Kết quả là họ lén lút đưa Breaking Changes vào bản `v1.9.0` (MINOR) và làm sập toàn bộ người dùng đang xài caret `^1.0.0`. Đây là tội ác!
2. **Gắn nhãn sai tính tương thích**: Thêm một trường Bắt buộc (Required Field) vào REST API JSON Payload. Dev nghĩ đây là tính năng mới nên tăng bản MINOR. SAI! Bắt client cũ phải gửi thêm 1 trường mới nếu không sẽ bị lỗi 400 Bad Request chính là một Breaking Change $\rightarrow$ Bắt buộc tăng MAJOR.

</details>

1. **Major Version Phobia**: Maintainers often fear incrementing the MAJOR number, worrying that `v14.0.0` looks "messy" or scares users. Consequently, they illegally sneak Breaking Changes into a MINOR release (e.g., `v1.9.0`). This violates the core contract of SemVer and immediately crashes downstream projects using Caret (`^`) auto-updates. Do not fear the MAJOR bump.
2. **Misclassifying "Required" Additions**: A backend engineer adds a new, strictly *Required* field (e.g., `"taxId"`) to a POST API JSON payload. They label it a "New Feature" and bump the MINOR version. **WRONG**. Because existing clients do not know about `"taxId"`, their requests will suddenly fail with `400 Bad Request`. Adding a *Required* parameter is inherently a Breaking Change, demanding a MAJOR version bump. Only *Optional* parameters are MINOR.

---

## Related Topics

- Managing dependency versions is executed via **[Git Fundamentals](../git/git-fundamentals.md)**.
- Releasing new versions automatically is the job of **[CI/CD Concepts](./ci-cd-concepts.md)**.
- Proper versioning dictates how you structure **[REST APIs](../network/rest-api.md)**.
