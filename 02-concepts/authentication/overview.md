# Authentication Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Authentication (Xác thực) là quá trình hệ thống trả lời câu hỏi: **"Bạn là ai?"**. Nó giống như việc bạn trình Căn cước công dân cho bác bảo vệ trước khi vào tòa nhà. Trong thế giới phần mềm, quá trình này đã tiến hóa từ việc chỉ dùng một cặp `Username/Password` đơn giản, đến việc dùng Session (Phiên), sau đó là Token không trạng thái (JWT), và cuối cùng là Đăng nhập một lần (SSO) hoặc dùng tài khoản bên thứ ba (OAuth2).

</details>

> **Summary**: Authentication (AuthN) is the foundational security process of verifying the identity of a user, device, or system. It answers the fundamental question: **"Who are you?"** and proves it mathematically. In modern software architecture, authentication has evolved from traditional, stateful `Username/Password + Session` models into stateless Token-based architectures (JWT), biometric WebAuthn, and delegated federated identities (SSO/OAuth2).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn muốn lên máy bay.
1. **Identification (Nhận dạng)**: Bạn nói với nhân viên: "Tôi là Tùng". (Đây là bước bạn gõ Username).
2. **Authentication (Xác thực)**: Nhân viên nói: "Chứng minh đi!". Bạn phải đưa ra Hộ chiếu có in hình và dấu mộc đỏ. (Đây là bước bạn gõ Password hoặc quét Vân tay). Nhân viên kiểm tra Hộ chiếu là thật, họ tin bạn đúng là Tùng.
3. Nếu bạn chỉ nói bạn là Tùng mà không có Hộ chiếu, hệ thống sẽ đá bạn ra ngoài (Lỗi `401 Unauthorized`).

</details>

Imagine attempting to board an international flight.
1. **Identification**: You walk up to the counter and state, "I am John Doe." (This is providing your Username).
2. **Authentication**: The security officer replies, "Prove it." You must present a valid, government-issued Passport containing cryptographic watermarks and your photograph. (This is providing your Password or Biometric fingerprint). Once the officer verifies the passport is authentic, you are successfully Authenticated.
3. If you claim to be John Doe but cannot produce the passport, you are violently rejected from the airport (`HTTP 401 Unauthorized`).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Xác thực (AuthN) dựa trên 3 yếu tố cốt lõi (Factors):
1. **Something you KNOW (Thứ bạn biết)**: Mật khẩu, mã PIN, câu hỏi bảo mật. (Dễ bị lộ nhất).
2. **Something you HAVE (Thứ bạn sở hữu)**: Điện thoại di động (nhận mã OTP SMS), thiết bị phần cứng (YubiKey), ứng dụng Google Authenticator.
3. **Something you ARE (Thứ thuộc về cơ thể bạn)**: Vân tay, FaceID, mống mắt. (Khó làm giả nhất).

Khi bạn kết hợp từ 2 yếu tố trở lên, ta gọi là **MFA (Multi-Factor Authentication - Xác thực đa yếu tố)**.

</details>

Authentication (AuthN) is architecturally built upon proving ownership of specific cryptographic or physical factors. There are three primary authentication factors:
1. **Knowledge Factor (Something you KNOW)**: Passwords, PINs, or security questions. (Historically the most common, but mathematically the weakest and most easily compromised via phishing).
2. **Possession Factor (Something you HAVE)**: A mobile phone receiving an SMS OTP, an Authenticator App generating a TOTP (Time-based One-Time Password), or a physical hardware security key (YubiKey).
3. **Inherence Factor (Something you ARE)**: Biometric signatures such as Fingerprints, Facial Recognition (FaceID), or Retinal scans.

Combining two or more of these independent categories is defined as **MFA (Multi-Factor Authentication)**, exponentially increasing the cryptographic difficulty for an attacker.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong môi trường Internet sơ khai, giao thức HTTP là giao thức **Phi trạng thái (Stateless)**. Nghĩa là máy chủ (Server) bị bệnh "mất trí nhớ ngắn hạn". Nếu bạn đăng nhập thành công ở giây thứ 1, thì sang giây thứ 2 khi bạn bấm xem Hồ sơ, máy chủ sẽ hoàn toàn quên mất bạn là ai và lại bắt bạn đăng nhập lại.
**Authentication Systems** được sinh ra để:
1. Kiểm chứng danh tính ở lần chạm đầu tiên (Login).
2. Cấp phát một "Tấm vé qua cổng" (Session ID hoặc JWT Token).
3. Người dùng cầm tấm vé này đưa cho máy chủ trong mọi lần bấm nút tiếp theo để máy chủ nhớ ra họ, mà không cần bắt họ phải gõ lại mật khẩu.

</details>

Fundamentally, the HTTP protocol powering the internet is entirely **Stateless**. The server possesses no intrinsic memory. If a user successfully logs in via `POST /login`, and immediately executes `GET /profile` one millisecond later, the server will have completely forgotten who they are and will demand the password again.
**Modern Authentication Systems** exist to bridge this stateless gap by:
1. Cryptographically verifying the user's identity at the initial touchpoint.
2. Generating and issuing a temporary, secure "Proof of Identity" artifact (a Stateful Session Cookie or a Stateless JWT Token).
3. Requiring the Client to attach this artifact to every subsequent HTTP request, allowing the server to seamlessly "remember" the user without constantly querying the credential database.

---

## Layer 3: Without vs. With Comparison (Compare)

### Single-Factor vs. Multi-Factor (MFA)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt sống còn giữa việc chỉ dùng Mật khẩu và việc dùng thêm OTP.
</details>

Visualizing the catastrophic security difference when a database is breached.

| Scenario | Single-Factor (Password Only) | Multi-Factor (Password + Authenticator App) |
|---|---|---|
| **Data Breach** | Hacker steals your email and password from a breached forum. | Hacker steals your email and password. |
| **The Attack** | Hacker logs directly into your Bank Account from Russia. | Hacker attempts to log in from Russia. |
| **System Response** | **Hacked**. The bank trusts the password and grants access. | Bank asks for the 6-digit TOTP code currently displaying on *your* physical phone. |
| **Outcome** | Attacker drains your bank account. | Attacker is violently blocked. You receive an alert and change your password. **Safe**. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Stateful Session (Cookie)**: Cách cổ điển. Bạn đăng nhập thành công, Server tạo ra một Session ID `abc123` và lưu nó vào RAM/Database của Server, sau đó nhét nó vào Cookie của trình duyệt. 
   - *Dùng khi*: Làm Web truyền thống (Monolith). Rất bảo mật vì Server nắm quyền sinh sát, muốn đuổi ai ra chỉ cần xóa Session ID đó khỏi RAM.
2. **Stateless Token (JWT)**: Cách hiện đại. Server không thèm nhớ gì cả. Đăng nhập xong, Server cấp cho bạn một chuỗi JSON (JWT) có chữ ký bí mật. Bạn tự lưu vào máy. Lần sau bạn đem JWT lên, Server lấy chữ ký ra tính toán lại xem có khớp không.
   - *Dùng khi*: Làm Microservices hoặc Mobile App. Server không sợ bị hết RAM do phải nhớ quá nhiều người.
3. **SSO (Single Sign-On)**: Đăng nhập một lần. Giống như bạn dùng tài khoản Google để đăng nhập vào 100 trang web khác nhau (Tinder, Spotify, Netflix).
   - *Dùng khi*: Nâng cao trải nghiệm người dùng, họ không cần phải nhớ 100 cái mật khẩu rác nữa.

</details>

1. **Stateful Session Authentication**: The legacy Monolithic approach. Upon login, the Server generates a random `Session_ID`, stores it explicitly in its memory/database, and sends it to the Client via a `Set-Cookie` header. 
   - *Use Case*: High-security Monolithic web apps (Banking). It allows instant, aggressive Server-side revocation (the admin deletes the ID from the database, and the user is instantly kicked out).
2. **Stateless Token Authentication (JWT)**: The Microservices approach. The Server generates a cryptographically signed JSON Web Token (JWT) and hands it to the Client. The Server does *not* store the token. When the token comes back, the Server simply mathematically verifies the signature.
   - *Use Case*: Horizontally scaled Microservices and Mobile APIs. It prevents the database from becoming a catastrophic bottleneck because validation requires zero database lookups.
3. **SSO (Single Sign-On) & Federation (OAuth2/OIDC)**: Delegating the authentication burden to an external, trusted Identity Provider (IdP) like Google, Auth0, or Microsoft Entra ID. 
   - *Use Case*: B2B SaaS applications or consumer apps wanting to maximize user acquisition by allowing "Login with Google/Apple", eliminating password fatigue.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Tuyệt đối không tự chế thuật toán băm Mật khẩu**: Đừng bao giờ lưu mật khẩu ở dạng chữ rõ ràng (Plain-text) hoặc dùng các thuật toán cổ lỗ sĩ như MD5 hay SHA-1. BẮT BUỘC phải dùng `Bcrypt` hoặc `Argon2` để băm mật khẩu. Chúng tự động sinh ra "Muối" (Salt) để chống lại các cuộc tấn công bằng Bảng Cầu Vồng (Rainbow Tables).
2. **Bảo vệ Brute-Force**: Hacker sẽ viết code thử tự động 1 triệu cái mật khẩu 1 giây vào tài khoản của Admin. Bắt buộc phải cài đặt **Rate Limiting** (Giới hạn số lần gõ sai). Ví dụ: Gõ sai 5 lần, khóa tài khoản 15 phút.

</details>

1. **Mandatory Cryptographic Hashing**: Never store passwords in plain-text. Never encrypt them symmetrically (AES) where they can be decrypted. You must utilize slow, computationally expensive, one-way Hashing algorithms specifically designed for passwords: **Bcrypt**, **Argon2**, or **scrypt**. These algorithms automatically generate and prepend a cryptographic Salt, rendering Rainbow Table pre-computation attacks mathematically impossible.
2. **Mitigate Brute-Force & Credential Stuffing**: Attackers will deploy Botnets to spam your `/login` endpoint with billions of leaked email/password combinations. You must implement aggressive **Rate Limiting** at the API Gateway layer (e.g., maximum 5 failed attempts per IP per minute) and implement **Account Lockout** policies (lock the account for 15 minutes after 10 failed attempts) accompanied by anomaly detection (suspicious logins from new countries trigger an immediate email alert).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Thông báo lỗi quá nhiệt tình**: Khi user gõ sai pass, nếu bạn báo lỗi là "Mật khẩu sai", hacker sẽ biết "À, vậy là cái email này có tồn tại trong hệ thống". Từ đó chúng sẽ tập trung hack cái email đó. 
   - *Khắc phục*: Dù user gõ sai Email hay sai Pass, LUÔN LUÔN trả về một câu thông báo chung chung: `"Email hoặc mật khẩu không đúng"`.
2. **Mật khẩu mặc định**: Mua thiết bị IoT, Router Wifi, hay cài đặt Database (như MongoDB, Redis) mà để nguyên mật khẩu mặc định của nhà sản xuất (như `admin/admin`). Hacker có những con Bot tự động rà quét trên mạng 24/7. Nếu bạn đưa Database lên mạng mà không đổi pass, nó sẽ bị hack, xóa trắng dữ liệu và tống tiền Bitcoin trong vòng 5 phút.

</details>

1. **Verbose Error Messages (User Enumeration)**: If an attacker submits a random email and the server responds with `"Invalid Password"`, the attacker now mathematically knows the email *exists* in your database. They can compile a list of valid targets. 
   - *The Fix*: Regardless of whether the Email is wrong or the Password is wrong, the server must uniformly and coldly respond with exactly the same message: `"Invalid Credentials."` It must also take the exact same amount of compute time to process, preventing Time-Based Enumeration attacks.
2. **Default Credentials in Infrastructure**: Deploying an Elasticsearch cluster, Redis instance, or IoT camera to the public internet using default vendor credentials (`admin/admin` or `root/password`). Automated botnets relentlessly scan the IPv4 space 24/7. A public Redis instance with no password will be hijacked and converted into a Crypto-mining node or Ransomwared within roughly 15 minutes of being exposed.

---

## Related Topics

- For the specific modern token architecture, read **[JWT (JSON Web Tokens)](./jwt.md)**.
- For delegated authentication, see **[OAuth2 & OIDC](./oauth2-oidc.md)**.
- For how to secure the passwords cryptographically, review **[Encryption vs Hashing](../../01-fundamentals/security/encryption.md)**.
- Once the user is Authenticated, what can they do? See **[Authorization Overview](../authorization/overview.md)**.
