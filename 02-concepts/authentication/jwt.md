# JWT (JSON Web Tokens)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ngày xưa, khi bạn đăng nhập, Server phát cho bạn một cái thẻ nhựa ghi số `ID = 123` (Session ID). Khi bạn muốn mua hàng, bạn đưa thẻ nhựa ra. Server phải cử nhân viên chạy xuống tầng hầm, mở két sắt (Database) xem `ID = 123` là tên gì, có bao nhiêu tiền, rồi mới cho bạn mua. Làm vậy quá chậm và tốn sức cho Server. 
> **JWT (JSON Web Token)** giải quyết vấn đề này. Nó là một tấm "Hộ chiếu điện tử" được đóng dấu mộc đỏ. Trên JWT ghi sẵn tên, tuổi, quyền hạn của bạn. Server KHÔNG CẦN nhớ bạn là ai. Nó chỉ cần kiểm tra xem Dấu Mộc Đỏ (Signature) trên Hộ chiếu có phải do chính nó đóng ngày xưa hay không. Khớp dấu $\rightarrow$ Đi qua.

</details>

> **Summary**: In legacy Stateful architectures, authentication relied on opaque Session IDs. The Server stored the user's state in memory or a database. Upon every request, the Server incurred the I/O penalty of querying the database to resolve the Session ID.
> **JWT (JSON Web Token)** introduces Stateless Authentication. A JWT is a mathematically signed, self-contained JSON payload. It explicitly embeds the user's ID, roles, and expiration time directly within the token. The Server stores *absolutely nothing*. When a client presents a JWT, the Server uses a secret cryptographic key to verify the signature. If the signature is mathematically valid, the Server trusts the payload and authorizes the request instantly without a single database lookup.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Session (Kiểu cũ)**: Gửi xe ngoài chợ. Bác bảo vệ ghi biển số xe của bạn vào cuốn sổ (Lưu vào Database), rồi đưa bạn cái vé ghi số `05`. Lúc ra, bạn đưa vé số `05`, bác lật sổ ra dò tìm dòng số `05` để lấy xe cho bạn. (Chậm, bác bảo vệ phải mang vác cuốn sổ nặng nề).
- **JWT (Kiểu mới)**: Bác bảo vệ có một con dấu Độc Quyền. Khi bạn vào, bác in luôn một tờ giấy ghi rõ: "Xe SH, biển số 29A-123.45, người gửi: Tùng". Xong bác đóng cái "Cốp!" con dấu mộc đỏ lên đó. Lúc ra, bác chẳng cần lật sổ sách gì cả. Chỉ cần nhìn thấy đúng con dấu độc quyền của mình trên tờ giấy là bác cho bạn dắt xe về.

</details>

- **Session Authentication**: Like a Coat Check at a club. You give them your coat, and they write your name in a massive ledger book (The Database). They hand you a meaningless plastic tag with the number `#42` (Session ID). To get your coat back, you hand them `#42`, and they must physically search through their giant ledger to find your name.
- **JWT Authentication**: Like a VIP wristband. The bouncer checks your ID once, then clasps a secure, tamper-proof wristband on your arm that explicitly says `VIP - John Doe`. When you walk to the bar, the bartender doesn't need to check any ledger or ask the bouncer. They just look at the secure wristband, see the VIP text, and instantly serve you.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cấu trúc của một JWT bao gồm 3 phần, cách nhau bởi dấu chấm (`.`): `Header.Payload.Signature`
1. **Header (Đầu)**: Khai báo loại token là JWT và thuật toán dùng để ký (thường là `HS256` hoặc `RS256`).
2. **Payload (Thân)**: Chứa dữ liệu thực tế (Claims) như `userId = 1`, `role = admin`, và thời gian hết hạn (`exp`). Lưu ý: Phần này chỉ được mã hóa định dạng (Base64) chứ KHÔNG bị khóa (Encrypt). Bất kỳ ai cũng có thể đọc được chữ bên trong.
3. **Signature (Chữ ký)**: Đây là trái tim của JWT. Server lấy `Header + Payload + MẬT KHẨU BÍ MẬT CỦA SERVER` để băm ra cái chữ ký này. Nếu Hacker lén đổi `role = user` thành `role = admin` ở phần Payload, chữ ký sẽ sai lệch hoàn toàn và Server sẽ chửi thẳng mặt hacker.

</details>

A JWT is a base64url-encoded string consisting of three distinct segments separated by a period (`.`): `Header.Payload.Signature` (e.g., `xxxx.yyyy.zzzz`)

1. **Header**: Metadata. It declares the token type (`JWT`) and the cryptographic signing algorithm utilized (e.g., `HS256` for Symmetric HMAC, or `RS256` for Asymmetric RSA).
2. **Payload (Claims)**: The actual data. It contains verifiable statements about the user (e.g., `"sub": "user_123"`, `"role": "admin"`). It also contains standard operational claims like `"exp"` (Expiration Time). **CRITICAL NOTE**: The Payload is merely Base64-encoded, *not* encrypted. Anyone can decode and read it. Never put secrets here.
3. **Signature**: The cryptographic anchor. The Server concatenates the Header and Payload, mathematically hashes them using the declared algorithm, and signs them using the Server's absolute Secret Key. If a malicious user alters their Payload (e.g., changing `"role": "user"` to `"admin"`), the cryptographic Signature will wildly misalign. The server will detect the tampering and aggressively reject the token.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề của Session trong thế giới Microservices**:
Nếu bạn có 10 con Server chạy song song (Load Balancing). Bạn đăng nhập vào Server 1 (Server 1 lưu Session của bạn vào RAM). 5 giây sau, bạn bấm Mua Hàng, mạng đẩy request của bạn sang Server 2. Server 2 không hề có Session của bạn trong RAM $\rightarrow$ Bắt bạn đăng nhập lại!
Để giải quyết, người ta phải dùng Redis làm trung tâm lưu Session cho cả 10 con Server dùng chung. Nhưng nếu Redis chết $\rightarrow$ Cả 10 con Server đều mất trí nhớ.

**Sự giải phóng của JWT**:
JWT là "Không trạng thái" (Stateless). Không cần Redis, không cần RAM. User tự giữ lấy JWT của mình trên điện thoại. Request bay vào Server 1 hay Server 100 cũng không quan trọng. Cả 100 con Server đều có chung cái `BÍ MẬT ĐÓNG DẤU`. Chỉ cần giải mã chữ ký thành công là xong. Hiệu năng được mở rộng vô hạn.

</details>

**The Scaling Bottleneck of Stateful Sessions**:
In modern cloud architectures, a backend is horizontally scaled across 50 containerized instances. If User A authenticates with Server #1, Server #1 stores the Session ID in its local RAM. When User A executes their next request, the Load Balancer might route them to Server #2. Server #2 has no record of the Session ID. It throws a `401 Unauthorized`.
To solve this, architects introduce a centralized Redis cluster to store Sessions. However, this creates a Single Point of Failure (SPOF) and a massive I/O bottleneck. Every single API request across all 50 servers requires a synchronous network call to Redis.

**The Stateless Liberation (JWT)**:
JWT decentralizes state. The user stores the state (the token) on their own device. The Server stores nothing. Whether the Load Balancer routes the request to Server #1 or Server #500 is irrelevant. Because every server securely shares the cryptographic Secret Key, they can all independently execute CPU-bound math to verify the Signature. Horizontal scalability becomes practically infinite.

---

## Layer 3: Without vs. With Comparison (Compare)

### Verifying an API Request

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt về thời gian khi Server xử lý một API (Ví dụ: Lấy hồ sơ người dùng).
</details>

Visualizing the operational flow of verifying an authenticated request.

| Step | Session ID Architecture (Stateful) | JWT Architecture (Stateless) |
|---|---|---|
| **1. Request** | Client sends `Cookie: session_id=abc` | Client sends `Authorization: Bearer x.y.z` |
| **2. Validation**| Server stops. Pauses code. Makes an asynchronous network call to the Database/Redis to ask: "Does `abc` exist? Who does it belong to?" | Server executes a fast, synchronous CPU math operation to verify the HMAC Signature of `x.y.z`. |
| **3. I/O Latency**| + 5ms to 10ms penalty per request. | **0ms**. No network/database I/O required. |
| **4. Drawback** | Hard to scale. Database can be overwhelmed. | **Revocation is impossible**. If the token is stolen, the Server cannot easily invalidate it before it expires. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Kiến trúc Microservices**: Bắt buộc. API Gateway đứng ở cửa, nhận JWT từ Mobile App. API Gateway kiểm tra chữ ký. Đúng chữ ký, nó nhét thông tin (User 1) vào request rồi đẩy vào trong cho hàng tá các Service con (Payment, Cart) xử lý mà không cần chọc vào DB.
- **Ủy quyền (Authorization - OAuth2)**: Bạn bấm "Đăng nhập bằng Google". Google sẽ trả về cho Website của bạn một cái JWT (được ký bằng Private Key của Google). Website của bạn dùng Public Key của Google để xác nhận đúng là Google gửi $\rightarrow$ Lấy Avatar và Email.
- **Giao tiếp tạm thời (One-time links)**: Khi bạn quên mật khẩu, Server gửi một link vào Email. Link đó thực chất chứa một cái JWT nhỏ bé chỉ có tuổi thọ 15 phút.

</details>

- **Microservice API Gateways**: The quintessential use case. The perimeter API Gateway intercepts the request, verifies the JWT signature, unpacks the Base64 payload, and forwards the raw User ID downstream to internal microservices via HTTP Headers. The internal microservices explicitly trust the Gateway and do not require their own authentication middleware.
- **OIDC (OpenID Connect) & Federated Identity**: The structural foundation of "Login with Apple/Google". When a user authenticates via Google, Google mints an Asymmetrically Signed JWT (`RS256`) and returns it. Your server fetches Google's public keys from the internet to verify the signature. You securely authenticate the user without ever seeing their password.
- **Ephemeral Access Links (Magic Links/Password Resets)**: Generating secure, stateless, self-expiring URLs. A password reset link embeds a JWT with an expiration (`exp`) of 15 minutes and the specific `user_id`. When clicked, the server verifies the JWT; if 16 minutes have passed, the cryptographic validation automatically fails.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cơ chế Refresh Token**: Điểm yếu chết người của JWT là không thể "Đuổi user ra" (Thu hồi/Revoke). Vì vậy, bạn phải đặt tuổi thọ của JWT (Access Token) cực ngắn (ví dụ: 15 phút). Bù lại, bạn cấp thêm một cái `Refresh Token` (Sống 30 ngày) lưu trong Database. Khi Access Token chết sau 15p, Client lén gửi Refresh Token lên để xin Access Token mới. Nếu tài khoản bị hack, Admin chỉ cần xóa Refresh Token trong DB, 15 phút sau Hacker tự động văng ra ngoài.
2. **Tuyệt đối không lưu Mật khẩu trong Payload**: Payload của JWT chỉ được Base64. Ai copy JWT của bạn bỏ lên trang `jwt.io` cũng đọc được sạch sành sanh chữ bên trong. Chỉ nên lưu `User_ID` và `Role`.

</details>

1. **The Access / Refresh Token Duality**: The fundamental flaw of Stateless JWTs is the **Inability to Revoke**. Because the Server queries no database, it cannot "cancel" a stolen JWT. The architectural mandate is to make the `Access Token` (JWT) extremely short-lived (e.g., 15 minutes). Simultaneously, issue an opaque, stateful `Refresh Token` (stored securely in the Database) valid for 30 days. When the Access Token expires, the Client presents the Refresh Token to get a new one. If an Admin bans a user, they delete the Refresh Token in the DB. The attacker's Access Token dies within 15 minutes, permanently severing access.
2. **Payload Hygiene (No Secrets)**: Developers routinely forget that JWT Payloads are structurally unencrypted. Storing PII (Personally Identifiable Information) like Social Security Numbers, Bank Balances, or Passwords inside the JWT payload is a catastrophic data breach waiting to happen. The Payload should strictly contain non-sensitive identifiers (`sub: user_123`, `role: admin`).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lỗ hổng thuật toán 'None'**: Ngày xưa, thư viện JWT bị lỗi ngớ ngẩn. Hacker sửa chữ `HS256` trên Header thành chữ `None` (Không dùng thuật toán). Server lười biếng đọc thấy `None` bèn tin luôn và không thèm kiểm tra chữ ký. Hacker tự phong mình làm Admin dễ dàng. LUÔN LUÔN phải ép cứng (hardcode) thuật toán kiểm tra trên Server.
2. **Lưu JWT vào LocalStorage**: Nếu bạn làm ReactJS/Vue và lưu JWT vào `localStorage.setItem('token', jwt)`. Bạn đang mở toang cánh cửa cho Hacker lấy trộm bằng mã độc Javascript (Lỗi XSS). Phải lưu JWT vào Cookie và bật cờ `HttpOnly`. Khi đó, Javascript sẽ bị mù, không thể đọc được nội dung Cookie, an toàn tuyệt đối.

</details>

1. **The 'None' Algorithm Vulnerability**: A historic and highly destructive flaw in early JWT implementations. Attackers manipulated the Base64 Header, changing the algorithm from `"alg": "HS256"` to `"alg": "none"`. Poorly written backend libraries respected the Header, bypassed cryptographic signature verification entirely, and blindly trusted the modified Payload. **Fix**: Never trust the Header for algorithm selection. Explicitly hardcode the allowed algorithm within your Backend verification function (e.g., `jwt.verify(token, secret, { algorithms: ['HS256'] })`).
2. **XSS Vulnerability via LocalStorage Storage**: A prevalent anti-pattern in SPA (React/Vue/Angular) development is storing the JWT in the browser's `LocalStorage`. `LocalStorage` is natively accessible via JavaScript. If your site suffers a Cross-Site Scripting (XSS) vulnerability, the attacker's script will effortlessly execute `localStorage.getItem('token')` and steal the user's session. **Fix**: Store JWTs exclusively in strictly configured Cookies with the `HttpOnly` and `Secure` flags set to `true`. `HttpOnly` completely severs JavaScript's ability to interact with the cookie, neutralizing XSS theft vectors.

---

## Related Topics

- For how Authentication works theoretically, see **[Authentication Overview](./overview.md)**.
- To understand XSS (the reason you don't use LocalStorage), read **[Web Security](../../01-fundamentals/security/web-security.md)**.
- For how OAuth2 leverages JWTs for federated login, see **[OAuth2 & OIDC](./oauth2-oidc.md)**.
