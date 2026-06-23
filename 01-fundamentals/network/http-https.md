# HTTP & HTTPS: The Language of the Web

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu TCP/IP là con đường nhựa trải dài giữa các quốc gia, thì **HTTP** (Hypertext Transfer Protocol) chính là những chiếc xe tải chở hàng hóa (chữ viết, hình ảnh, video) chạy trên con đường đó. HTTP là một ngôn ngữ dạng văn bản (Text) quy định cách Trình duyệt và Máy chủ nói chuyện với nhau. Ban đầu, HTTP truyền dữ liệu dưới dạng Text trần trụi (rất dễ bị hacker đọc trộm). Sự ra đời của **HTTPS** (S = Secure) trang bị thêm cho xe tải một lớp bọc thép (Mã hóa SSL/TLS), đảm bảo chỉ có người nhận đích thực mới mở được hàng.

</details>

> **Summary**: If TCP/IP represents the physical asphalt highway spanning the globe, **HTTP** (Hypertext Transfer Protocol) dictates the strict logistical format of the cargo trucks driving upon it. HTTP is a stateless, text-based application-layer protocol universally adopted to transmit hypertext documents (HTML), images, and API payloads between Browsers and Web Servers. Historically, HTTP transmitted payloads in plain text, making it catastrophically vulnerable to interception. **HTTPS** (HTTP Secure) wraps the transmission within an impenetrable cryptographic tunnel (SSL/TLS), ensuring data privacy, integrity, and server authentication.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (Browser) gửi một lá thư cho Ngân hàng (Server) để xin rút tiền.
- **HTTP (Gửi bưu thiếp hở)**: Bạn viết mặt sau tấm bưu thiếp: "Tôi tên Tùng, mật khẩu là 123456, hãy rút 10 triệu". Bất kỳ ông bưu tá nào trên đường chuyển phát, người ngồi cạnh bạn ở quán cà phê WiFi, hay tổng đài mạng đều có thể cầm tấm bưu thiếp lên đọc và lấy trộm tiền của bạn.
- **HTTPS (Gửi phong bì niêm phong két sắt)**: Bạn bỏ tờ giấy vào một cái két sắt mini bằng thép, khóa mật mã lại, rồi gửi đi. Ông bưu tá cầm két sắt trên tay nhưng không có mật mã mở khóa (TLS Keys) nên chịu chết không đọc được nội dung bên trong. Chỉ có Giám đốc Ngân hàng (người giữ chìa khóa) mới mở được.

</details>

Imagine you (The Browser) are sending a financial request to your Bank (The Server).
- **HTTP (Mailing a transparent Postcard)**: You write your Account Number and Password on the back of an unsealed postcard and drop it in the mail. Every postal worker, router administrator, and malicious hacker sitting at your local Starbucks public WiFi can simply read the postcard as it passes through their hands (Man-in-the-Middle Attack). Your identity is stolen instantly.
- **HTTPS (Mailing a Titanium Safe)**: You write your request, lock it inside an impenetrable titanium safe, and hand it to the postal worker. The hackers intercept the safe, but without the specific cryptographic decryption keys (TLS Handshake keys), they see nothing but mathematically randomized garbage. Only the verified Bank vault possesses the master key to open it.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Giao thức HTTP**: Là chuỗi văn bản quy chuẩn.
- Bắt đầu luôn là: Động từ (Methods) `GET`, `POST`, `PUT`, `DELETE`.
- Theo sau là Đường dẫn URL: `/users/1`
- Kèm theo các thông tin phụ (Headers): Trình duyệt đang xài (User-Agent), Cấp quyền (Authorization), Loại dữ liệu (Content-Type).
- Cuối cùng là phần thân (Body) chứa dữ liệu gửi đi (JSON, Ảnh).

**2. HTTPS (TLS/SSL)**: Dựa trên hệ thống Khóa Bất đối xứng (Public Key / Private Key) và Chứng chỉ số (SSL Certificate). Máy chủ phải mua một "Căn cước công dân" từ một tổ chức uy tín (CA - Certificate Authority) để chứng minh nó đúng là Ngân hàng thật, không phải Ngân hàng giả mạo.

</details>

**1. The HTTP Protocol Structure**: At its core, it is a beautifully readable, standardized text string architecture.
- **Request Line**: The verb (Method: `GET`, `POST`, `PUT`, `DELETE`), the Target URI (`/api/v1/auth`), and the HTTP Version (`HTTP/1.1`).
- **Headers**: Key-value metadata transmitting critical context (e.g., `User-Agent: Mozilla/5.0`, `Authorization: Bearer xyz123`, `Content-Type: application/json`).
- **Body**: The actual physical payload being transmitted (A JSON document, an MP4 video, or raw HTML).

**2. HTTPS (The TLS/SSL Tunnel)**: Utilizes asymmetric cryptographic algorithms (Public/Private Keys) combined with symmetric session keys to encrypt the HTTP Body and Headers. It fundamentally relies on **SSL Certificates** mathematically cryptosigned by a globally trusted Certificate Authority (CA) to authenticate that the server you are talking to is the legitimate Google.com, and not a DNS-spoofed imposter.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao Google ưu tiên xếp hạng (SEO) cho các trang HTTPS và Trình duyệt Chrome sẽ bôi đỏ cảnh báo "Not Secure" đối với trang HTTP?
Bởi vì cuộc chiến chống lại **Man-In-The-Middle (MITM) Attacks** (Tấn công Xen giữa).
Nếu bạn dùng Wifi ở tiệm Cafe, hacker ngồi đối diện chỉ cần chạy phần mềm Wireshark là có thể "ngửi" (Sniff) thấy toàn bộ gói tin bạn gửi đi. Nếu bạn gửi qua HTTP, hacker thấy ngay mật khẩu Facebook của bạn hiện rõ mồn một. Bắt buộc mọi trang web trên đời đều phải nâng cấp lên HTTPS để mã hóa dữ liệu thành các chuỗi ký tự vô nghĩa.

</details>

Why did Google alter its search engine algorithms to heavily penalize `http://` sites, and why do modern Browsers explicitly label them with a red "Not Secure" warning?
To annihilate the catastrophic vulnerability of **Man-In-The-Middle (MITM) Attacks**.
When you connect to a public Starbucks WiFi router, your network traffic physically broadcasts through the air. A malicious actor sitting 10 feet away can execute a packet sniffer (like Wireshark) and intercept your traffic. If you transmit a login form over plain-text HTTP, your password (`password123`) is visible in pristine text. HTTPS encrypts that payload into mathematically unintelligible hash garbage (`aZ9xqP!L2...`), rendering the intercepted packet utterly useless.

---

## Layer 3: Without vs. With Comparison (Compare)

### Raw Network Request Anatomy

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt giữa Gói tin HTTP trần trụi và luồng Handshake của HTTPS.
</details>

Visualizing exactly what travels across the wire.

#### Raw HTTP Request (Visible to everyone)
*Anyone intercepting the network sees everything.*
```http
POST /login HTTP/1.1
Host: bank.com
Content-Type: application/json

{"username": "admin", "password": "supersecretpassword123"}
```

#### Raw HTTPS Request (Encrypted via TLS 1.3)
*What the hacker intercepts using Wireshark.*
```text
(TLS Handshake - Exchanging Certificates & Keys)
...
(Encrypted Application Data)
0x1A 0xB4 0x9F 0xCC 0x22 0x7E 0xFF 0x01 (Garbage Byte Stream)
```

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Các HTTP Status Codes hay gặp**:
  - `200 OK`: Mọi thứ hoàn hảo.
  - `201 Created`: Thêm mới thành công vào DB.
  - `400 Bad Request`: Mày gửi thiếu tham số, kiểm tra lại code Frontend đi!
  - `401 Unauthorized`: Mày chưa đăng nhập, hoặc sai mật khẩu.
  - `403 Forbidden`: Mày đã đăng nhập, nhưng mày là User thường, không có quyền vào trang của Admin.
  - `404 Not Found`: Đường dẫn URL không tồn tại.
  - `500 Internal Server Error`: Server Backend bị Lỗi Code (Crash/Bug), phải báo ngay cho Dev sửa lỗi.

</details>

- **Mastering HTTP Status Codes**: The universal language of Web Debugging.
  - **`200 OK`**: The golden standard. Request executed flawlessly.
  - **`201 Created`**: A `POST` request successfully inserted a new record into the database.
  - **`400 Bad Request`**: A Client Error. The Frontend Engineer sent a malformed JSON payload (e.g., passing a String where an Integer is required).
  - **`401 Unauthorized`**: Missing or expired Authentication. Provide a valid JWT Token.
  - **`403 Forbidden`**: Valid identity, but insufficient Permissions. (e.g., A standard User attempting to trigger an Admin-only route).
  - **`404 Not Found`**: The requested Endpoint or Database Resource does not physically exist.
  - **`500 Internal Server Error`**: A catastrophic Backend Engineer failure. The Java/Node.js code threw an Unhandled Exception and crashed during execution.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Gia hạn SSL tự động**: Chứng chỉ SSL thường chỉ có hạn 90 ngày (Let's Encrypt). Đừng bao giờ gia hạn bằng tay. Phải dùng các công cụ tự động (Certbot) trên Nginx hoặc dùng Cloudflare để nó tự động đổi khóa, nếu không 1 ngày đẹp trời trang web sẽ chìm trong màu Đỏ.
2. **Đừng bao giờ gửi Mật khẩu qua GET**: Lệnh `GET` truyền thông số lên chính cái đường dẫn URL (`/login?password=123`). Dù có HTTPS, cái URL này vẫn bị lưu lại trong file lịch sử Trình duyệt (Browser History) và file log của Nginx. Ai mở lịch sử lên là thấy mật khẩu. Đăng nhập BẮT BUỘC dùng lệnh `POST` để nhét mật khẩu chìm vào phần Body.

</details>

1. **Automate Certificate Renewal (Let's Encrypt)**: Modern robust SSL Certificates (like those issued by Let's Encrypt) strictly expire after 90 days to minimize the risk of compromised keys. Relying on a human SysAdmin to manually renew certificates via SSH every 3 months is a guaranteed formula for a production outage. You must rigorously automate this pipeline via `Certbot` cron jobs or delegate it entirely to an Edge proxy layer like Cloudflare.
2. **Never send sensitive payloads via `GET`**: The HTTP `GET` method appends parameters directly to the physical URL (`https://bank.com/api?pw=admin123`). Even under perfect HTTPS encryption in transit, the unencrypted URL path is permanently logged in the Server's Nginx `access.log` files, the ISP's DNS logs, and the user's local Browser History. A sysadmin reviewing logs will see raw passwords. Always utilize `POST` or `PUT` methods to bury sensitive payloads deep within the Encrypted Body.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lỗi Mixed Content (Nội dung trộn lẫn)**: Bạn cấu hình xong HTTPS xanh lè cho trang web. Nhưng bên trong trang web, bạn lại chèn một tấm ảnh `<img>` gọi từ nguồn `http://`. Trình duyệt sẽ phát điên, chặn tải tấm ảnh đó, và trang web bị mất khóa bảo mật (văng mất chữ Xanh Lá). Toàn bộ link nhúng (Font, Ảnh, Script) BẮT BUỘC phải là HTTPS.
2. **Quên cấu hình HTTP-to-HTTPS Redirect**: User gõ tên miền của bạn (Ví dụ: `facebook.com`), theo thói quen nó sẽ chạy vào luồng HTTP cũ (Cổng 80) không bảo mật. Bạn phải cấu hình Nginx/Apache lập tức đá (Redirect 301) luồng truy cập đó dội ngược sang cổng HTTPS (Cổng 443).

</details>

1. **Mixed Content Blocking Errors**: A developer flawlessly secures the main domain `https://myapp.com`. However, inside the DOM, they reference a legacy external stylesheet via `<link href="http://old-cdn.com/style.css">`. Modern browsers (Chrome/Firefox) immediately trigger a catastrophic security intervention. They will aggressively block the insecure HTTP asset from downloading, shattering the CSS layout, and instantly downgrade the site's security padlock icon. 100% of embedded network assets MUST utilize the `https://` protocol.
2. **Failing to configure `HTTP -> HTTPS` Redirection (301)**: When a user manually types `example.com` into their address bar, the browser historically defaults to port 80 (`http://`). If the server does not forcefully intervene, the user surfs an insecure session. The Load Balancer or Nginx config must contain an aggressive, unconditional `HTTP 301 Permanent Redirect` rule, physically forcing all incoming Port 80 traffic immediately into the encrypted Port 443 TLS tunnel.

---

## Related Topics

- To understand the physical packets HTTP runs on top of, see **[TCP/IP Model](./tcp-ip.md)**.
- To see how HTTP Status Codes are used to build APIs, explore **[REST API](./rest-api.md)**.
- HTTP requires knowing Domain Names, which relates to **[DNS and Web Works](../web-fundamentals/how-the-web-works.md)**.
