# Browser Rendering Pipeline (Advanced)

Hiểu rõ cách trình duyệt render trang web từ HTML/CSS/JS thành các pixel trên màn hình là kỹ năng bắt buộc để tối ưu hoá hiệu năng (Web Performance Optimization).

## Critical Rendering Path (CRP)

Quá trình trình duyệt chuyển đổi mã nguồn thành màn hình hiển thị trải qua các bước sau:

1. **Parsing HTML & Xây dựng DOM Tree**
   - Trình duyệt nhận raw bytes, convert thành ký tự, token hóa (tag), và xây dựng DOM (Document Object Model) tree.
   - Khi gặp thẻ `<script>` đồng bộ (không có `async` hoặc `defer`), quá trình parse HTML bị block (Render-blocking).

2. **Parsing CSS & Xây dựng CSSOM Tree**
   - Giống như HTML, CSS được parse thành CSSOM (CSS Object Model).
   - CSS là **Render-blocking resource**. Trình duyệt sẽ không render bất kỳ nội dung nào cho đến khi CSSOM hoàn thiện để tránh hiện tượng FOUC (Flash of Unstyled Content).

3. **Render Tree Construction**
   - DOM và CSSOM được combine lại thành Render Tree.
   - Render Tree chỉ chứa các node **hiển thị được**. Ví dụ: Các node có `display: none` sẽ bị loại khỏi Render Tree (nhưng `visibility: hidden` vẫn tồn tại vì nó chiếm không gian).

4. **Layout (Reflow)**
   - Trình duyệt tính toán kích thước (width, height) và vị trí chính xác (x, y) của từng node trong Render Tree dựa trên viewport.
   - Quá trình này tốn rất nhiều tài nguyên (đặc biệt khi dùng percentage, flexbox, grid).

5. **Paint (Repaint)**
   - Chuyển các node trong Render Tree thành các pixel thực tế trên màn hình (vẽ text, màu sắc, border, shadow, image).
   - Thường được vẽ trên nhiều layer khác nhau.

6. **Compositing**
   - Trình duyệt gộp các layer đã paint lại theo đúng thứ tự z-index để tạo thành hình ảnh cuối cùng hiển thị trên màn hình.

> [!WARNING]
> **JavaScript Execution** có thể block DOM construction, thay đổi DOM/CSSOM và ép trình duyệt phải thực hiện lại toàn bộ quá trình Layout và Paint.

---

## Reflow và Repaint (Tránh "Layout Thrashing")

### Reflow (Layout thrashing)
Xảy ra khi bạn thay đổi các thuộc tính ảnh hưởng đến **geometry** của phần tử (width, height, margin, padding, top, left, font-size).
- Khi một element bị reflow, tất cả các con của nó, các phần tử xung quanh, và thậm chí toàn bộ document có thể phải tính toán lại Layout.
- **Bad Practice:** Đọc (`offsetWidth`, `clientHeight`) và Ghi (`style.width`) liên tục trong một vòng lặp sẽ ép trình duyệt phải reflow liên tục đồng bộ (Synchronous Layout).

### Repaint
Xảy ra khi thay đổi các thuộc tính về **visual** không ảnh hưởng geometry (color, background, box-shadow, visibility).
- Repaint nhẹ hơn Reflow nhưng vẫn tốn GPU/CPU.

---

## GPU Hardware Acceleration & Composite Layers

Để tối ưu animation mượt mà (đạt 60fps), nguyên tắc vàng là **chỉ animate trên thuộc tính kích hoạt Compositing** (bỏ qua Layout và Paint).

Chỉ có 2 thuộc tính thỏa mãn điều kiện này:
1. `transform` (translate, scale, rotate)
2. `opacity`

Khi bạn dùng `transform` hoặc `opacity`, trình duyệt có thể đẩy element đó lên một **Layer riêng biệt (Composite Layer)** và giao cho **GPU** xử lý thay vì CPU, giúp animation cực kỳ mượt.

### Tạo Composite Layer bằng `will-change`
```css
/* Báo trước cho trình duyệt để nó tạo sẵn GPU Layer */
.animated-element {
  will-change: transform, opacity;
}
```

> [!CAUTION]
> Lạm dụng `will-change` hoặc `translateZ(0)` (hack GPU) sẽ tiêu tốn cực kỳ nhiều RAM/VRAM của user. Chỉ dùng cho những element thực sự cần animate liên tục.

## Tóm tắt nguyên tắc tối ưu Render
- Dùng `<script defer>` hoặc `<script async>`.
- Minify và nén CSS/JS, tải critical CSS inline.
- Hạn chế đọc/ghi DOM đan xen (dùng `requestAnimationFrame` để batch DOM updates).
- Chỉ animate `transform` và `opacity`.
