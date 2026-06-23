# API Security: CORS, Rate Limiting, CSRF

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi bạn mở tung cánh cửa Backend ra Internet bằng REST API, nghĩa là bạn đang mời gọi toàn thế giới tấn công hệ thống của bạn. **Bảo mật API** là thiết lập các hàng rào phòng thủ tự động tại cửa ngõ. 
> - **CORS**: Chặn các trang web lạ gọi trộm API của bạn.
> - **Rate Limiting (Giới hạn tốc độ)**: Chặn hacker gọi API 10,000 lần/giây để làm sập Server.
> - **CSRF (Giả mạo yêu cầu chéo trang)**: Lừa người dùng bấm vào link lạ để tự động chuyển tiền mà họ không hề hay biết.

</details>

> **Summary**: Exposing a REST API to the public internet is functionally equivalent to opening the front door of a bank vault and leaving it unattended. **API Security** architectures implement rigid, automated perimeter defenses at the Gateway layer to neutralize hostile traffic before it reaches business logic. This encompasses configuring strict **CORS** policies to prevent cross-origin Browser hijacking, enforcing aggressive **Rate Limiting** to mitigate brute-force and DDoS attacks, and implementing anti-**CSRF** tokens to prevent catastrophic cross-site forged transactions.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng API của bạn là một Quầy Bán Vé tự động.
1. **CORS (Thẻ tên nhân viên)**: Bạn ra lệnh cho quầy vé: "Chỉ bán vé cho những người mặc đồng phục màu Xanh (Trang web nội bộ)". Nếu một thằng lạ mặc áo Đỏ (Trang web hacker) tới mua vé, quầy lập tức từ chối phục vụ.
2. **Rate Limiting (Xếp hàng lấy số)**: Một thằng giang hồ muốn phá rối, nó đứng trước quầy bấm nút "Mua vé" liên tục 1 triệu lần 1 giây khiến máy bán vé bốc khói. Bạn lắp thêm một phần mềm: "Mỗi người chỉ được bấm tối đa 5 lần/phút. Bấm lần thứ 6 sẽ bị đuổi ra ngoài nghỉ 1 tiếng".
3. **CSRF (Chữ ký xác nhận)**: Hacker gửi cho bạn một đường link hình con mèo. Bạn bấm vào xem mèo. Nhưng ngầm bên dưới, trang web đó tự động lấy thẻ tín dụng của bạn gửi yêu cầu Mua Vé. Để chống lại, quầy vé bắt buộc: "Khi mua vé phải nộp kèm một Chữ Ký Độc Quyền (CSRF Token) giấu dưới đáy giỏ hàng". Trang web con mèo không thể có chữ ký này nên giao dịch bị hủy.

</details>

Imagine your API is a high-security automated Bank Teller.
1. **CORS (The VIP Guest List)**: You instruct the Teller: "Only accept requests from individuals wearing the official Corporate ID Badge (Your specific Frontend Domain)." If a malicious stranger from an unknown domain attempts to ask the Teller for account data, the Browser aggressively blocks the transaction.
2. **Rate Limiting (The Speed Limit)**: A malicious actor wants to break the machine. They stand in front of the Teller and scream 10,000 requests per second, causing the machine's CPU to catch fire. You install a speed limiter: "Any single IP address may only speak to the Teller 5 times per minute. Request #6 triggers an instant 1-hour ban (HTTP 429)."
3. **CSRF (The Forgery Prevention)**: A hacker sends you an email with a funny cat video. You click the link. Invisible to you, the cat website instantly fires an API request to your bank: `Transfer $1000 to Hacker`. Because you are currently logged into your bank, the browser automatically attaches your authentication cookies, and the bank executes it. To prevent this, the bank mandates a mathematically random, hidden "Secret Handshake Token" (CSRF Token) with every transaction. The cat website doesn't know the handshake, so the transfer fails.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. CORS (Cross-Origin Resource Sharing)**: Là cơ chế BẢO VỆ CỦA TRÌNH DUYỆT (Chrome, Firefox). Nếu Frontend nằm ở `web.com` muốn gọi API nằm ở `api.com` (Hai nguồn khác nhau - Cross Origin). Trình duyệt sẽ hỏi Backend: "Ê, thằng `web.com` này có nằm trong danh sách cho phép của mày không?". Backend gật đầu (Gửi header Access-Control-Allow-Origin) thì Trình duyệt mới cho phép dữ liệu đi qua.
**2. Rate Limiting**: Một bộ đếm (thường dùng Redis) đếm số lần gọi API của 1 địa chỉ IP. Vượt ngưỡng sẽ văng lỗi `429 Too Many Requests`.
**3. CSRF (Cross-Site Request Forgery)**: Mượn dao giết người. Hacker không tự tay tấn công API của bạn. Nó tạo trang web giả, dụ Người Dùng Thật bấm vào. Trình duyệt của Người Dùng Thật sẽ tự động gửi kèm Cookie Đăng nhập hợp lệ lên API của bạn để thực hiện lệnh xấu.

</details>

**1. CORS (Cross-Origin Resource Sharing)**: A fundamental **Browser-level** security enforcement. By default, the Browser's Same-Origin Policy strictly prohibits a Frontend hosted at `https://frontend.com` from fetching data from an API at `https://api.com`. To bypass this, the API Backend must explicitly return specific HTTP Headers (e.g., `Access-Control-Allow-Origin: https://frontend.com`). If the headers don't match, the Browser intentionally blocks the HTTP response from reaching the Javascript code.
**2. Rate Limiting**: A perimeter defense mechanism (often implemented at the API Gateway or using Redis) that mathematically throttles incoming traffic. It tracks incoming requests per IP address or User ID against a sliding window algorithm. Exceeding the quota triggers an `HTTP 429 Too Many Requests` response.
**3. CSRF (Cross-Site Request Forgery)**: A "Confused Deputy" attack. The attacker does not steal the user's password. Instead, they trick the victim's browser into executing a state-changing API request (like changing an email address). Because the victim is actively authenticated, their browser automatically attaches their valid Session Cookies to the malicious request, deceiving the Backend into accepting the forged command.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Sự hiểu lầm nguy hiểm về CORS**:
Nhiều Lập trình viên mới làm API, thấy Frontend gọi API bị lỗi CORS văng đỏ lòm trên màn hình. Quá bực mình, họ lên mạng copy đoạn code cấu hình Backend mở cửa cho TẤT CẢ mọi trang web (`Access-Control-Allow-Origin: *`).
Đây là hành động Tự Sát. Nếu bạn mở `*`, bất kỳ trang web lừa đảo nào trên thế giới cũng có thể dùng Javascript để âm thầm gọi API của bạn, lấy cắp dữ liệu khách hàng. CORS sinh ra để khóa chặt Backend, chỉ cho phép đúng cái tên miền Frontend thật của công ty bạn được quyền gọi API.

</details>

**The Lethal Misunderstanding of CORS**:
Junior Frontend developers frequently encounter the dreaded red `CORS Error` in the Chrome Console when attempting to hit a new API. Frustrated, they Google a quick fix and blindly configure their Express/Spring Boot backend to respond with `Access-Control-Allow-Origin: *` (Wildcard).
This is architectural suicide. The Wildcard completely dismantles the browser's Same-Origin protection. It explicitly grants permission to *every malicious website on earth* to execute Javascript `fetch()` requests against your API and read the responses. CORS exists to enforce a strict whitelist. You must physically hardcode your production frontend domain (`https://my-app.com`) into the Backend CORS configuration.

---

## Layer 3: Without vs. With Comparison (Compare)

### The Rate Limiting Defense

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt giữa hệ thống không có bảo vệ và hệ thống có Rate Limiting khi bị tấn công dò mật khẩu.
</details>

Visualizing a Brute-Force Password attack against an API endpoint with and without Rate Limiting.

**The Attack:** A Botnet attempts to guess the Admin password by sending 1,000 `POST /login` requests per second.

| Stage | Without Rate Limiting | With Rate Limiting (10 req/min) |
|---|---|---|
| **Second 1** | Bot sends 1,000 requests. | Bot sends 1,000 requests. |
| **Backend Reaction**| Backend queries the Database 1,000 times. DB CPU hits 50%. | Backend accepts first 10. Redis blocks the remaining 990 instantly. |
| **Second 5** | Bot has sent 5,000 requests. | Bot sends 5,000 requests. |
| **Backend Reaction**| Database runs out of RAM and Crashes. System Offline. | Redis instantly drops 5,000 requests with `HTTP 429`. DB CPU is at 0%. |
| **Attacker Status**| Attacker successfully DDOS'd the system. | Attacker's IP is temporarily banned. System perfectly healthy. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Rate Limiting cho SMS/Email API**: Nếu bạn có tính năng "Nhập SĐT để nhận mã OTP". Nếu không có Rate Limit chặn lại (Ví dụ 1 phút chỉ được nhắn 1 lần), hacker sẽ viết code tự động bấm nút Gửi 1 triệu lần. Hóa đơn tiền SMS cuối tháng của công ty bạn sẽ lên tới hàng trăm triệu đồng (Tấn công cạn kiệt tài chính).
- **CORS Preflight (Lệnh OPTIONS)**: Bạn thấy Trình duyệt tự nhiên gửi một request tên là `OPTIONS` lên Server, mặc dù bạn không hề viết code gọi nó. Đừng hoảng! Đó là Trình duyệt đang "bay trinh sát" (Preflight). Nó hỏi trước Server xem có cho phép phương thức `PUT/DELETE` không, trước khi nó thực sự gửi cục dữ liệu thật lên.
- **SameSite Cookie**: Thay vì phải viết code tạo Token chống CSRF phức tạp, ngày nay trình duyệt có một vũ khí tối thượng tên là `SameSite=Strict`. Khi Backend trả Cookie về, gắn cờ này vào. Trình duyệt sẽ chặn tuyệt đối không cho phép trang web khác gửi ké Cookie của bạn. Bệnh CSRF bị tiêu diệt hoàn toàn.

</details>

- **Financial Rate Limiting (OTP/SMS APIs)**: Exposing an unprotected endpoint that integrates with a paid 3rd-party service (e.g., Twilio SMS for OTP generation) is a massive financial vulnerability. Attackers will script infinite loops hitting `POST /api/send-otp`. Without strict Rate Limiting (e.g., 1 request per phone number per minute), the attacker will incur hundreds of thousands of dollars in Twilio billing charges to your company account overnight.
- **The CORS Preflight (`OPTIONS` Method)**: Developers often panic when they see mysterious HTTP `OPTIONS` requests appearing in their network logs. This is normal. For complex requests (like `PUT`, `DELETE`, or requests with custom Headers like `Authorization`), the Browser natively triggers an automated "Preflight" request. It interrogates the server's CORS configuration first. If the server approves, the browser automatically dispatches the actual `PUT` request immediately afterward.
- **The Modern CSRF Killer (`SameSite` Cookies)**: Historically, mitigating CSRF required complex engineering (Synchronizer Token Patterns). Modern Browsers have largely neutralized this vulnerability via the `SameSite` cookie attribute. When the Backend issues an authentication Cookie, aggressively flag it as `SameSite=Strict` or `SameSite=Lax`. This physically commands the Browser Engine to outright refuse to attach the Cookie to any cross-origin requests, instantly severing the attacker's CSRF attack vector.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **API Gateway làm cửa khẩu**: Đừng viết logic Rate Limit hay CORS vào bên trong từng con Microservice (rất rác code và khó bảo trì). Hãy đặt một hệ thống API Gateway (như Nginx, Kong, AWS API Gateway) đứng chặn ở cửa. Cấu hình Rate Limit 100 req/s tại cổng. Code Backend bên trong hoàn toàn không cần quan tâm đến hacker nữa.
2. **Cấu hình CORS phân biệt Môi trường**: Ở môi trường viết code (Local), cho phép `localhost:3000` được gọi API thoải mái. Nhưng khi đẩy lên Server thật (Production), phải viết code tự động đổi CORS thành đúng cái tên miền `congtycuatoi.com`. Đừng bao giờ lười biếng mà dùng `localhost` hoặc `*` trên Production.

</details>

1. **Centralize Defenses at the API Gateway Layer**: A massive microservice architecture shouldn't duplicate CORS logic, JWT validation, and Rate Limiting algorithms inside 50 different Node.js/Java codebases. This violates the DRY principle and ensures configuration drift. Delegate these global perimeter defenses to a dedicated **API Gateway** (e.g., Kong, AWS API Gateway, Nginx, Cloudflare). The Gateway aggressively filters out malformed, unauthorized, and rate-exceeding requests before they ever touch your internal VPC architecture.
2. **Environment-Aware CORS Configuration**: CORS origins must be dynamically injected via Environment Variables. Hardcoding `http://localhost:3000` in the Express.js configuration is a standard practice during local development. However, if this hardcoded configuration accidentally deploys to Production, legitimate traffic from `https://myapp.com` will be permanently blocked by the Browser. Ensure the build pipeline injects the correct Production URI into the CORS Origin whitelist.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nhầm tưởng CORS là Bảo mật Backend**: CORS chỉ là trò chơi của Trình duyệt. Nếu bạn cấu hình CORS chặn `hacker.com`, Trình duyệt của người dùng sẽ không cho code Javascript chạy. NHƯNG, hacker không dùng trình duyệt. Hacker bật màn hình đen Terminal lên gõ lệnh `curl` bắn thẳng vào API của bạn. Lệnh `curl` không có trình duyệt nên KHÔNG BỊ RÀNG BUỘC BỞI CORS. API của bạn vẫn bị xuyên thủng! CORS không thay thế cho hệ thống Xác Thực (Authentication/JWT).
2. **Rate Limit bằng Local RAM**: Dev code tính năng Rate Limit bằng cách lưu số đếm vào biến Array/Object trên RAM của ứng dụng Node.js. Chạy trên máy dev thì ngon. Lên thực tế, công ty chạy 10 con Server song song qua Load Balancer. User đánh sập hệ thống vì bộ đếm trên 10 con server không đồng bộ với nhau. LUÔN LUÔN dùng Redis làm kho lưu trữ bộ đếm tập trung cho Rate Limit.

</details>

1. **The Fundamental Misunderstanding of CORS Security**: CORS is exclusively a Client-Side Browser enforcement. It protects the *User*, not the *Server*. If your backend refuses `hacker.com`, a legitimate Browser will block the response. However, an attacker bypassing the Browser entirely and utilizing `curl`, Postman, or Python `requests` ignores CORS completely. The backend processes the malicious request perfectly. CORS is absolutely not a replacement for cryptographically verifying a user's identity via JWT Authentication Middleware.
2. **In-Memory Rate Limiting in Distributed Systems**: A junior developer implements Rate Limiting using a local JavaScript object (`const limitMap = new Map()`) to track IP request counts. In local development, it works flawlessly. In production, the application is horizontally scaled across 5 Kubernetes pods behind a Load Balancer. The in-memory maps are isolated. An attacker can hit the system 5x harder because each pod tracks its limit independently. **Mandatory Architecture**: Distributed systems demand centralized state. You must utilize an external **Redis** cluster to globally synchronize Rate Limit counters across all backend instances.

---

## Related Topics

- For how Authentication works before hitting APIs, read **[Auth: OAuth & JWT](./auth-oauth-jwt.md)**.
- For other types of vulnerabilities attacking the code, see **[Web Security Vulnerabilities](./web-security.md)**.
- See how API endpoints are structured structurally in **[REST API](../network/rest-api.md)**.
