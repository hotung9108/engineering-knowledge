# Web Performance & Core Web Vitals (Advanced)

Tối ưu hóa hiệu năng web hiện đại xoay quanh **Core Web Vitals (CWV)** do Google định nghĩa. Chúng tác động trực tiếp đến SEO (Google Ranking) và UX (Tỷ lệ chuyển đổi).

## 1. Core Web Vitals (CWV)

### LCP (Largest Contentful Paint) - Tốc độ tải
Thời gian để render phần tử khối chứa văn bản hoặc hình ảnh **lớn nhất** trong viewport.
- **Tốt:** < 2.5 giây.
- **Cách tối ưu:**
  - `preload` hero image: `<link rel="preload" as="image" href="hero.webp">`
  - Tối ưu TTFB (Time to First Byte): Server nhanh, dùng CDN.
  - Tránh lazy-load cho hero image (chỉ lazy-load ảnh below-the-fold).
  - Tránh client-side rendering toàn bộ nội dung (dùng SSR/SSG với Next.js).

### INP (Interaction to Next Paint) - Khả năng phản hồi
Thay thế FID từ tháng 3/2024. Đo lường toàn bộ vòng đời tương tác của user (click, tap, key press). Tính độ trễ từ lúc user thao tác đến khi trình duyệt vẽ frame tiếp theo.
- **Tốt:** < 200 ms.
- **Cách tối ưu:**
  - Chia nhỏ Long Tasks (>50ms) trong main thread (dùng `setTimeout`, `requestIdleCallback`, hoặc Web Workers).
  - Tối ưu React render (tránh re-render không cần thiết, dùng `useTransition` / `useDeferredValue` trong React 18).
  - Giảm thiểu kích thước JavaScript bundle.

### CLS (Cumulative Layout Shift) - Tính ổn định giao diện
Tổng điểm số của các đợt dịch chuyển giao diện bất ngờ (không có user interaction).
- **Tốt:** < 0.1
- **Cách tối ưu:**
  - **Luôn set width/height explicitly** cho thẻ `<img>`, `<video>`, và `<iframe>`.
  - Dự trữ không gian (Skeleton/Placeholder) cho Ads và nội dung tải bất đồng bộ (như Client-side fetched list).
  - Không chèn nội dung động lên phía trên nội dung hiện tại.
  - Dùng `font-display: optional` hoặc `swap` kết hợp với `size-adjust` để giảm thiểu FOUT/FOIT.

---

## 2. Resource Hints

Tối ưu hoá đường truyền mạng bằng cách dặn trình duyệt chuẩn bị trước.

```html
<!-- 1. Preload: Tải file có độ ưu tiên rất cao (Font, Hero Image, Critical CSS). Phải dùng kèm 'as' -->
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>

<!-- 2. Preconnect: Khởi tạo kết nối DNS, TCP, TLS đến một domain khác (VD: CDN API) sớm hơn -->
<link rel="preconnect" href="https://api.my-domain.com">

<!-- 3. DNS-Prefetch: Nhẹ hơn preconnect, chỉ resolve DNS -->
<link rel="dns-prefetch" href="https://assets.my-domain.com">

<!-- 4. Prefetch: Tải nền (low priority) một resource có thể cần ở trang TIẾP THEO -->
<link rel="prefetch" href="/js/next-page-chunk.js">
```

---

## 3. Caching Strategies

Kết hợp cache tầng Server và Browser:

### HTTP Caching (Cache-Control)
- **Immutable Assets (JS, CSS, Images đã băm tên file `main.1a2b.js`):**
  `Cache-Control: public, max-age=31536000, immutable` (Cache vĩnh viễn 1 năm).
- **Mutable Assets (HTML, API configs):**
  `Cache-Control: no-cache` (Bắt buộc hỏi lại server ETag/Last-Modified trước khi dùng cache). Hoặc dùng ISR của Next.js.

### Service Workers & PWA
Sử dụng Workbox để cache request API và tài nguyên tĩnh ở Client, cho phép ứng dụng tải offline hoặc siêu nhanh trong những lần truy cập sau (Cache-first, Network-first, Stale-while-revalidate strategies).
