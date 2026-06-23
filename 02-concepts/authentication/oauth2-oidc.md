# OAuth2 & OIDC (OpenID Connect)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ngày xưa, nếu một game online muốn tìm bạn bè của bạn trên Facebook, bạn phải cung cấp Cả Tên Đăng Nhập và Mật Khẩu Facebook cho cái game đó (Cực kỳ nguy hiểm!). **OAuth2** sinh ra để cấm việc đó. Nó là cơ chế "Cấp quyền không cần nhả mật khẩu". Bạn bảo Facebook: "Hãy mở cửa phần Bạn bè cho game này xem đi". Facebook cấp cho game một Tấm Vé (Token) chỉ có quyền xem bạn bè, tuyệt đối không được đọc tin nhắn.
> Tuy nhiên, OAuth2 chỉ dùng để *Ủy Quyền (Authorization)*. Nó không biết bạn là ai. Vì vậy, thế giới gắn thêm **OIDC (OpenID Connect)** lên trên lưng OAuth2 để lo việc *Xác Thực (Authentication)*. Sự kết hợp này tạo ra nút bấm thần thánh: **"Đăng nhập bằng Google / Apple"**.

</details>

> **Summary**: Historically, delegating third-party access required users to surrender their absolute credentials (Username/Password) to untrusted applications—an architectural security nightmare. **OAuth2** (Open Authorization) was engineered to eradicate this anti-pattern. It is a Delegated Authorization framework that issues explicitly scoped, limited-access Tokens to third-party applications without ever exposing the user's root credentials.
> Crucially, OAuth2 is strictly an *Authorization* protocol (granting access to resources). It was never designed for *Authentication* (verifying identity). To bridge this gap, the industry layered **OIDC (OpenID Connect)** precisely on top of OAuth2. OIDC standardizes identity verification, issuing a JWT `id_token` that powers universally ubiquitous "Sign in with Google / Microsoft" federated identity workflows.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đi thuê Khách sạn.
- **Mật khẩu (Giao chìa khóa gốc)**: Bạn đưa cho người Dọn Phòng cái Chìa Khóa Nhà Gốc của bạn. Họ có thể mở cửa nhà, mở luôn cái két sắt chứa vàng của bạn. (Rất nguy hiểm).
- **OAuth2 (Cấp Thẻ từ phân quyền)**: Bạn dùng Chìa Khóa Gốc để ra quầy Tiếp Tân. Quầy cấp cho người Dọn Phòng một cái Thẻ Từ. Thẻ này chỉ mở được cửa phòng ngủ của bạn từ 8h sáng đến 10h sáng, và KHÔNG THỂ mở được cửa Két sắt. (Bảo mật tuyệt đối).
- **OIDC (Kẹp Hộ chiếu vào Thẻ từ)**: Lúc cấp Thẻ từ, Tiếp Tân dán thêm một cái Hộ Chiếu có ảnh của bạn lên Thẻ. Nhờ đó, người Dọn Phòng không những được vào phòng dọn dẹp, mà còn biết luôn: "À, chủ phòng này tên là Tùng, 30 tuổi".

</details>

Imagine staying at a high-end Hotel.
- **Sharing Passwords (Legacy Pattern)**: You hand the Housekeeper your physical Master Key. They can unlock your hotel room, but they can also unlock your personal safe and steal your valuables.
- **OAuth2 (Delegated Authorization)**: You use your Master Key to authenticate at the Front Desk. You instruct the Front Desk to issue a restricted Valet Keycard to the Housekeeper. This Keycard *only* unlocks your room door, *only* between 8 AM and 10 AM, and physically cannot open the safe. Your Master Key remains safely in your pocket.
- **OIDC (Identity Layer)**: The Front Desk attaches a certified ID Card to the Valet Keycard. Now, the Housekeeper doesn't just have permission to enter the room; they also mathematically know exactly *who* the occupant of the room is (Name, Email, Profile Picture).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**OAuth2** là một Giao thức Ủy quyền. Nó định nghĩa 4 vai trò (Roles) rõ ràng:
1. **Resource Owner**: Người dùng (Là bạn).
2. **Client**: Ứng dụng muốn xin quyền (Ví dụ: Game Spotify, ứng dụng Tinder).
3. **Authorization Server**: Máy chủ giữ chìa khóa, chuyên cấp phép (Ví dụ: Server của Google/Facebook).
4. **Resource Server**: Nơi chứa dữ liệu thực sự (Ví dụ: Server chứa Danh bạ Facebook).

**OIDC (OpenID Connect)**: Là một lớp áo mặc thêm cho OAuth2. Khi kết thúc quy trình OAuth2, Server thay vì chỉ trả về `Access Token` (để lấy dữ liệu), nó trả về thêm một cái `ID Token` (là một chuỗi JWT) chứa đầy đủ thông tin cá nhân của người dùng (Tên, Email, Avatar) để Client đăng nhập luôn.

</details>

**OAuth2** is an open standard for Access Delegation. It fundamentally orchestrates interaction between four distinct Roles:
1. **Resource Owner**: The User (You).
2. **Client**: The Third-Party Application requesting access (e.g., Spotify requesting access to your Facebook friends).
3. **Authorization Server**: The centralized identity provider that authenticates the user and issues tokens (e.g., Google's Auth Servers).
4. **Resource Server**: The API holding the actual protected data (e.g., Google Contacts API).

**OIDC (OpenID Connect)**: A simple identity layer seated precisely on top of the OAuth 2.0 protocol. While vanilla OAuth2 only issues an opaque `Access Token` (designed only for the Resource Server to read), OIDC introduces the `ID Token`. The `ID Token` is a readable JSON Web Token (JWT) explicitly containing the authenticated user's profile information (Claims), allowing the Client application to log the user in locally.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao OAuth2 ra đời?** (Chống lại thảm họa mật khẩu)
Năm 2007, Yelp ra mắt tính năng "Tìm bạn bè". Yelp yêu cầu người dùng GÕ MẬT KHẨU GMAIL vào ô đăng nhập của Yelp. Yelp lấy mật khẩu đó, lén đăng nhập vào Gmail của người dùng để quét danh bạ. Việc này cực kỳ kinh khủng, vì Yelp sẽ giữ mật khẩu gốc của hàng triệu người. OAuth2 ra đời để dập tắt kiểu thiết kế ngu ngốc này.

**Tại sao OIDC ra đời?** (Sự lạm dụng của Lập trình viên)
Lập trình viên muốn dùng Facebook để "Đăng nhập". Nhưng OAuth2 không có khái niệm Đăng nhập, nó chỉ cho cái Token để lấy dữ liệu. Nên các Dev lách luật bằng cách: Lấy Token $\rightarrow$ Gọi API `GET /me` của Facebook $\rightarrow$ Lấy Email $\rightarrow$ Coi như đăng nhập thành công.
Cách lách luật này tạo ra hàng tá lỗ hổng bảo mật. Vì vậy, Google và Microsoft hợp lực đẻ ra OIDC để chuẩn hóa luôn việc Đăng nhập. Cấp luôn `ID Token` để khỏi phải lách luật.

</details>

**The Inception of OAuth2 (The Password Anti-Pattern)**:
In 2007, early Web 2.0 startups (like Yelp) launched "Find Friends" features. They required users to literally type their raw Yahoo/Gmail Passwords directly into Yelp's UI. Yelp would programmatically impersonate the user, log into Yahoo, and scrape the address book. This was an unmitigated security disaster. Yelp possessed the root keys to millions of inboxes. OAuth2 was architected to make this credential-sharing pattern obsolete.

**The Inception of OIDC (Pseudo-Authentication)**:
Developers desperately wanted "Federated Login" (SSO). Because OAuth2 is strictly an Authorization protocol, developers abused it: They would obtain an OAuth2 `Access Token`, immediately fire a request to the Facebook `GET /me` endpoint, and use the returned Email Address to hack together a local login session. This "pseudo-authentication" was mathematically flawed and riddled with vulnerabilities. Tech giants united to create OIDC, officially standardizing Identity Verification by introducing the cryptographically signed `ID Token` specifically meant for the Client.

---

## Layer 3: Without vs. With Comparison (Compare)

### The Authorization Code Flow

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Quy trình "Ủy quyền Code" (Authorization Code Flow) là quy trình an toàn và phổ biến nhất của OAuth2.
</details>

Visualizing the standard **Authorization Code Flow** (The most secure and heavily utilized OAuth2 workflow for web applications).

| Step | Action | Description |
|---|---|---|
| **1. Redirect** | Client $\rightarrow$ Auth Server | The App redirects the User's browser to `google.com/auth`. The App asks for `scope=email,contacts`. |
| **2. Consent** | User $\rightarrow$ Auth Server | Google asks the User: "Do you want to give this App access to your Contacts?" The User clicks "Yes". |
| **3. The Code** | Auth Server $\rightarrow$ Client | Google redirects the browser back to the App, passing a temporary, single-use `Auth_Code` in the URL. |
| **4. Exchange** | Client $\rightarrow$ Auth Server | The App's Backend securely contacts Google's Backend (server-to-server). It trades the `Auth_Code` + its own `Client_Secret` for the final `Access_Token`. |
| **5. Access** | Client $\rightarrow$ Resource Server | The App uses the `Access_Token` to fetch the Contacts via API. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Đăng nhập bằng Mạng Xã Hội (Social Login - OIDC)**: Sử dụng nút "Sign in with Google / Apple / Facebook". Web của bạn không cần tự thiết kế màn hình Quên Mật Khẩu hay Gửi Email xác nhận nữa. Bạn "khoán trắng" việc bảo mật cho Google.
- **Ủy quyền Hệ thống (Machine to Machine - Client Credentials Flow)**: Khi 2 con Server của 2 công ty khác nhau cần nói chuyện tự động với nhau (Không có mặt con người). Ví dụ: Server Shopee gọi Server Giao Hàng Tiết Kiệm để tạo đơn. Shopee tự dùng `Client ID` và `Client Secret` của mình để đổi lấy Token, không có giao diện đăng nhập (Không có buớc Redirect).
- **Ứng dụng di động (PKCE Flow)**: Ứng dụng điện thoại (iOS/Android) rất dễ bị hacker dịch ngược code để ăn cắp mật khẩu `Client Secret`. Vì vậy, không bao giờ được nhét `Client Secret` vào App Mobile. Thay vào đó, chúng phải sử dụng một biến thể OAuth2 bảo mật hơn gọi là **PKCE** (Sinh ra một mật khẩu ngẫu nhiên dùng 1 lần cho mỗi lần đăng nhập).

</details>

- **Federated Identity & SSO (OIDC)**: Implementing "Sign in with Google/Apple". This radically decreases user friction (no new passwords to create) and completely offloads the extreme liability of credential storage, password resets, and MFA enforcement to multi-billion-dollar security teams at Google.
- **Machine-to-Machine Communication (Client Credentials Grant)**: Automated server-to-server interaction with zero human involvement. Example: A cron job on your AWS backend needs to automatically pull metrics from the Datadog API nightly. There is no Browser Redirect. Your backend securely stores a `Client_ID` and `Client_Secret`, presents them directly to Datadog's Auth Server, receives an `Access Token`, and executes the API call.
- **Mobile & SPA Security (Authorization Code with PKCE)**: Native Mobile Apps (iOS/Android) and Single Page Apps (React) cannot securely store a `Client_Secret` (attackers can easily decompile the APK to steal it). Therefore, the standard Auth Code Flow is vulnerable. They MUST utilize the **PKCE (Proof Key for Code Exchange)** extension, which dynamically generates a cryptographic challenge/verifier pair on the fly for every single login, rendering intercepted Auth Codes useless.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sử dụng Scope (Phạm vi) nhỏ nhất có thể**: Nếu App của bạn chỉ cần lấy Email để đăng nhập, chỉ yêu cầu Google cấp Scope `email profile`. Đừng bao giờ yêu cầu Scope `youtube.write` hay `drive.readonly` nếu không cần thiết. Trình duyệt sẽ hiện cảnh báo đỏ lòm khiến User sợ hãi bỏ chạy.
2. **Kiểm chứng thuộc tính `state`**: Khi chuyển hướng User sang Google, hãy đính kèm một chuỗi ngẫu nhiên gọi là `state`. Khi Google trả User về, hãy kiểm tra xem `state` có khớp với lúc đầu không. Đây là tấm khiên thép chặn đứng kiểu tấn công CSRF (Hacker lén ép User đăng nhập vào tài khoản của Hacker).

</details>

1. **Principle of Least Privilege (Micro-Scopes)**: When configuring your OAuth2 request, request the absolute minimum `scope` necessary for the application to function. If you only need Federated Login, request exactly `scope=openid email profile`. Requesting invasive scopes like `https://www.googleapis.com/auth/drive` will trigger terrifying, red-bannered consent screens from Google, causing massive user abandonment (conversion drop-off).
2. **Mandatory `state` Parameter Validation**: When initiating the Redirect flow, always generate a cryptographically random `state` token and store it in the user's local session cookie. When the Auth Server redirects back to your callback URL, it mirrors the `state`. You MUST verify they match perfectly. This is the primary defense against **CSRF Login Forgery** (where an attacker forcefully injects their own valid Authorization Code into a victim's session, tricking the victim into saving sensitive data into the attacker's account).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Rò rỉ Access Token trên URL (Implicit Flow)**: Ngày xưa có kiểu làm lười biếng (Implicit Flow) là bắt Google trả thẳng Token lên thanh địa chỉ trình duyệt (`?token=123`). Việc này làm Token bị lưu lại trong lịch sử duyệt web (Browser History) và rò rỉ ra ngoài. Quy tắc hiện đại: **Tuyệt đối cấm dùng Implicit Flow**. Luôn dùng Auth Code Flow, giấu việc trao đổi Token xuống dưới Backend.
2. **Tin tưởng mù quáng vào ID Token**: Khi một ứng dụng Mobile gửi cái `ID Token` lên Backend của bạn và bảo: "Tôi là Tùng đây, cho tôi vào". Đừng có tin! Hacker có thể lấy trộm một `ID Token` hợp lệ của một trang web khác để lừa bạn. Backend BẮT BUỘC phải giải mã Token, kiểm tra xem trường `aud` (Audience) có đúng là cấp cho Website của mình hay không, và chữ ký có hợp lệ không.

</details>

1. **Utilizing the Deprecated Implicit Flow**: Historically, Single Page Apps utilized the "Implicit Flow" which forced the Auth Server to return the raw `Access Token` directly in the URL fragment (`#access_token=xyz`). This is a catastrophic vulnerability. The token is logged in Browser History, Proxy Logs, and `Referer` headers. **Absolute Rule**: The OAuth 2.1 specification explicitly deprecates the Implicit Flow. All architectures (even frontends) MUST utilize the Authorization Code Flow with PKCE.
2. **Blind Trust in Delegated Identity (Token Substitution)**: A malicious Mobile App client sends an OIDC `id_token` to your Backend API. The Backend decodes it, sees `"email": "admin@company.com"`, and grants access. **Fatal Flaw**: The attacker authenticated perfectly with Google, but for a completely *different* application. They intercepted that valid token and replayed it against *your* API. **Fix**: The Backend MUST cryptographically verify the signature against Google's public JWKS, and strictly verify that the `"aud"` (Audience) claim perfectly matches your specific application's `Client_ID`.

---

## Related Topics

- For how Authentication works theoretically, see **[Authentication Overview](./overview.md)**.
- To understand the exact JSON structure of the ID Token, read **[JWT (JSON Web Tokens)](./jwt.md)**.
- For how API Gateways use these tokens, review **[API Security](../../01-fundamentals/security/api-security.md)**.
