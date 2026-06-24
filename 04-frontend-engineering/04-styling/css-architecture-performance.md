# CSS Architecture & Performance (Advanced)

Lựa chọn công nghệ Styling ở quy mô Enterprise không chỉ là về sở thích, mà là bài toán đánh đổi giữa Developer Experience (DX) và Web Performance (Runtime cost).

## 1. Sự thật về CSS-in-JS (Runtime)

Các thư viện nổi tiếng như **Styled Components** hay **Emotion** hoạt động bằng cách:
1. Bạn viết CSS bằng Javascript String Template.
2. Tại **Runtime** (lúc user mở trang web ở browser), thư viện đọc chuỗi JS đó.
3. Sinh ra một mã hash ngẫu nhiên (VD: `css-1x2y3z`).
4. Chèn thêm một thẻ `<style>` vào `<head>` của DOM.

### Hậu quả về Performance:
- **Tốn CPU/JS parsing:** Trình duyệt phải tải thư viện JS, chạy JS để sinh ra CSS, sau đó mới tính toán Render. Điều này làm trễ quá trình Critical Rendering Path.
- **Re-render penalty:** Mỗi lần component re-render với dynamic props (`<Button $primary={isPrimary} />`), Emotion/Styled-components có thể phải tính toán lại và chèn CSS mới vào DOM, gây ra **Style Recalculation** toàn trang (rất giật lag).
- **Khó tương thích với Server Components:** Next.js App Router (RSC) không hỗ trợ React Context tĩnh ở Server, làm các công cụ runtime CSS-in-JS gặp cực nhiều rắc rối setup.

---

## 2. Thời đại của Zero-Runtime CSS-in-JS

Để giữ lại lợi ích viết CSS trong JS (type-safe, scoped) nhưng loại bỏ hoàn toàn chi phí runtime, thế hệ công cụ mới ra đời: **Vanilla Extract**, **Panda CSS**, **Linaria**.

### Cách hoạt động
- Bạn viết CSS trong JS/TS.
- Lúc build project (Webpack/Vite), công cụ này sẽ phân tích file TS, **tách toàn bộ CSS ra thành file `.css` tĩnh truyền thống** (Static Extraction).
- Ở Runtime, user chỉ cần tải file `.css` chuẩn (browser xử lý siêu nhanh, không tốn JS).

### Ví dụ: Vanilla Extract
```typescript
// button.css.ts
import { style } from '@vanilla-extract/css';

export const buttonClass = style({
  backgroundColor: 'blue',
  color: 'white',
  ':hover': { backgroundColor: 'darkblue' }
});

// Button.tsx
import { buttonClass } from './button.css.ts';

export function Button() {
  // Lúc chạy, nó chỉ là một string class thông thường
  return <button className={buttonClass}>Click</button>; 
}
```

---

## 3. CSS Modules

Nếu không thích hệ sinh thái phức tạp của Zero-runtime, CSS Modules là lựa chọn mặc định hoàn hảo (được hỗ trợ Native trong Next.js và Vite).

- **Ưu điểm:** Viết thuần CSS/SASS, học một lần dùng mãi mãi. Scope cục bộ (không sợ trùng class). Zero runtime.
- **Nhược điểm:** Phải liên tục context-switch giữa file `.css` và `.tsx`. Không thể chia sẻ Design Tokens từ JS sang CSS một cách dễ dàng (phải dùng CSS Variables).

---

## 4. Tóm lược lựa chọn Kiến trúc CSS hiện đại

1. **Tailwind CSS (Utility-first):** Xu hướng thống trị hiện tại. Cực nhanh để code, không cần đặt tên class, file CSS output rất nhỏ (chỉ vài chục KB).
2. **Vanilla Extract / Panda CSS:** Dành cho team thích cú pháp Styled Components / System UI nhưng yêu cầu hiệu năng khắc nghiệt và hỗ trợ RSC.
3. **CSS Modules (SCSS):** Chắc chắn, an toàn, dễ bảo trì cho các dự án dài hạn hoặc có team Designer vững chuyên môn.

> [!WARNING]
> Nếu bắt đầu một dự án mới bằng Next.js App Router, hãy tuyệt đối tránh dùng Styled Components / Emotion. Chúng mang lại trải nghiệm DX tồi tệ khi cố gắng ép vào Server Components (cần "use client" khắp nơi, gây flash of unstyled content nếu setup sai).
