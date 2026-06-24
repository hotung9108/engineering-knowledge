# Frontend Security (Advanced)

Bảo mật không chỉ là việc của Backend. Lỗ hổng ở Frontend thường nhắm trực tiếp vào End-user.

## 1. XSS (Cross-Site Scripting)

Hacker chèn mã JavaScript độc hại vào trang web của bạn (qua comment, URL), và khi user khác xem trang, đoạn JS đó chạy và đánh cắp Cookie/Token.

### Phân loại
- **Stored XSS:** Hacker lưu JS độc vào Database. Bất kỳ ai mở bài viết đó đều dính.
- **Reflected XSS:** JS độc nằm trên URL `?search=<script>...`. Server phản hồi thẳng đoạn chữ đó ra HTML.
- **DOM-based XSS:** Hoàn toàn do Frontend (nhét parameter từ URL thẳng vào `innerHTML`).

### Cách phòng chống trong Frontend
1. **Tuyệt đối không dùng `innerHTML` (hoặc `dangerouslySetInnerHTML` trong React)** trừ khi cực kỳ cần thiết và data đó đã được **Sanitize** (làm sạch).
2. Dùng thư viện `DOMPurify` để lọc thẻ `<script>` khỏi chuỗi HTML.
```javascript
import DOMPurify from 'dompurify';
const cleanHTML = DOMPurify.sanitize(dirtyUserHTML);
<div dangerouslySetInnerHTML={{ __html: cleanHTML }} />
```
3. React tự động escape biến trong `{variable}` nên khá an toàn với XSS cơ bản.

---

## 2. Token Storage (Vấn đề lưu JWT)

Nên lưu Access Token ở đâu?

### A. LocalStorage / SessionStorage
- **Dễ dùng**, Frontend đọc được ngay lập tức để gửi đi qua Header `Authorization: Bearer`.
- **LỖI BẢO MẬT CHÍNH:** Dễ bị tấn công XSS. Bất kỳ mã JS độc hại nào (từ extention trình duyệt, thẻ script lạ) đều có thể `localStorage.getItem('token')` và gửi về server hacker.

### B. HttpOnly Cookies (Best Practice hiện đại)
- Token được Backend set vào Cookie với cờ `HttpOnly` và `Secure`.
- Trình duyệt sẽ tự động đính kèm Cookie này trong mọi Request gửi đến Backend đó.
- **BẢO MẬT TUYỆT ĐỐI KHỎI XSS:** JavaScript ở Frontend KHÔNG THỂ đọc được HttpOnly Cookie (`document.cookie` không thấy).
- **Rủi ro CSRF:** Dùng cookie sẽ mở ra rủi ro CSRF, nhưng hiện nay cờ `SameSite=Lax` hoặc `Strict` trong Cookie đã giải quyết gần triệt để vấn đề này.

---

## 3. CSRF (Cross-Site Request Forgery)

Hacker lừa user bấm vào một nút trên web của Hacker (`hacker.com`), nhưng đằng sau nút bấm đó là một request ngầm gửi đến `your-bank.com/transfer`. Vì user đang đăng nhập ở ngân hàng, trình duyệt tự động gửi kèm Cookie, thế là tiền bị chuyển đi.

### Cách phòng thủ:
- **SameSite Cookie:** Đặt cờ `SameSite=Lax` hoặc `Strict` khi Backend set cookie. Trình duyệt sẽ không gửi Cookie đi nếu request xuất phát từ domain khác (`hacker.com`).
- **Anti-CSRF Tokens:** Backend sinh 1 token ẩn giấu trong thẻ `<meta>` hoặc form ẩn. Hacker không thể lấy được token đó.

---

## 4. Content Security Policy (CSP)

Một lớp khiên phòng thủ cực mạnh bằng HTTP Header gửi từ Server. Nó quy định trình duyệt CHỈ được tải tài nguyên (Images, Scripts, Styles) từ các domain được chỉ định.

Ví dụ: Nếu trang của bạn dính lỗ hổng XSS (Hacker chèn được script gọi về `hacker.com/steal`), nhưng bạn đã thiết lập CSP:
```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com
```
Trình duyệt sẽ BÁO LỖI VÀ CHẶN đoạn mã XSS đó lại vì `hacker.com` không nằm trong danh sách trắng (`trusted.cdn.com`).

> [!IMPORTANT]
> Frontend Devs thường cấu hình CSP qua thẻ `<meta>` trong Next.js `Document` hoặc bằng Next.js `headers()` config trong `next.config.js`.
