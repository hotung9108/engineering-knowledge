# CSS Architecture and Performance

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Phân tích kỹ thuật về sự đánh đổi của các chiến lược CSS cho ứng dụng frontend hiện đại, so sánh Runtime CSS-in-JS, Zero-Runtime CSS-in-JS, CSS Modules, và cách tiếp cận Utility-first. Việc lựa chọn kiến trúc CSS có tác động trực tiếp đến dung lượng bundle, hiệu năng render và khả năng tương thích với Server Component.

</details>

> **Summary**: A technical analysis of CSS strategy trade-offs for modern frontend applications, comparing Runtime CSS-in-JS, Zero-Runtime CSS-in-JS, CSS Modules, and Utility-first approaches. The choice of CSS architecture has direct impact on bundle size, rendering performance, and Server Component compatibility.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đi mua quần áo:
- **CSS Truyền thống**: Bạn vào kho lấy áo, nhưng tất cả quần áo vứt lộn xộn trong một đống. Bạn dễ lấy nhầm áo của người khác (Lỗi trùng tên class CSS).
- **CSS-in-JS (Styled Components)**: Bạn mua một cái máy may mang về nhà. Mỗi lần bạn cần mặc áo, bạn bật máy may lên và may ngay tại nhà. Áo cực kỳ vừa vặn, nhưng tốn tiền điện và mất thời gian may mỗi lần mặc (Chậm do tốn Javascript lúc chạy).
- **CSS Modules / Tailwind / Zero-Runtime**: Bạn nhờ xưởng may đo sẵn tất cả áo (Build time) rồi cất vào tủ. Khi cần mặc, bạn chỉ lấy ra mặc luôn. Nhanh gọn, không tốn điện, nhưng bạn phải tuân theo kích thước đã đo sẵn. Trình duyệt hiện đại thích cách này nhất.

</details>

Imagine you're buying clothes:
- **Traditional CSS**: You walk into a giant warehouse, but all the clothes are thrown into one massive pile. It's very easy to accidentally grab someone else's shirt (CSS global class name collisions).
- **Runtime CSS-in-JS (Styled Components)**: You buy a sewing machine and keep it at home. Every time you want to wear a shirt, you turn on the machine and sew it on the spot. It fits perfectly, but it wastes electricity and takes time every time you want to wear it (Performance cost of computing CSS in the browser via JavaScript).
- **CSS Modules / Tailwind / Zero-Runtime**: You ask a factory to tailor all your clothes in advance (at Build Time) and put them in your closet. When you need a shirt, you just put it on instantly. It's fast, uses no electricity, but you have to stick to the pre-made sizes. Modern browsers vastly prefer this.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Kiến trúc CSS** là cách tiếp cận có hệ thống để viết, tổ chức và phân phối các file CSS trong một ứng dụng web. Trong hệ sinh thái React, cuộc tranh luận lớn nhất hiện nay xoay quanh việc CSS được xử lý ở đâu — ngay trên trình duyệt lúc đang chạy (Runtime), hay được biên dịch sẵn lúc code (Build time).

**Phân loại:**
- **Loại**: Quyết định kiến trúc Frontend.
- **Các nhóm chính**: Runtime CSS-in-JS, Zero-Runtime CSS-in-JS, CSS Modules, Utility-first CSS (Tailwind).
- **Tác động**: Hiệu năng (dung lượng JS, tốc độ vẽ), Trải nghiệm lập trình viên, Sự tương thích với Server Component (RSC).

</details>

**CSS Architecture** refers to the systematic approach used to author, organize, and deliver stylesheets in a web application. In the React ecosystem, the primary debate centers on where CSS is processed — at runtime in the browser or at build time by the compiler.

### Classification
- **Type**: Frontend styling architecture decision.
- **Categories**: Runtime CSS-in-JS, Zero-Runtime CSS-in-JS, CSS Modules, Utility-first CSS.
- **Impact areas**: Performance (CRP, JS bundle), Developer Experience, RSC compatibility.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

CSS nguyên thủy có nhiều lỗi trầm trọng khi dự án phình to:
- **Không gian chung (Global namespace)**: Trùng tên class.
- **Code thừa (Dead code)**: Xóa code CSS sợ làm hỏng trang khác.
- **Thiếu logic**: CSS không tự đổi màu theo logic của JavaScript được.

CSS-in-JS (như Styled Components) sinh ra để giải quyết vấn đề trên bằng cách dùng JavaScript để quản lý CSS. Nhưng nó lại sinh ra bệnh mới: **chạy chậm** và **không tương thích với Server Components**. Từ đó dẫn tới xu hướng Zero-Runtime và Utility-first.

</details>

Traditional CSS has fundamental scaling problems in large applications:

| Problem | Description |
|---|---|
| Global namespace | All class names share a single scope — collisions are inevitable |
| Dead code | Unused styles accumulate because deletion risks breaking other pages |
| No co-location | Styles live in separate files, disconnected from the components they serve |
| Dynamic styling | CSS alone cannot respond to JavaScript state without class toggling |

CSS-in-JS solved these problems by scoping styles to components and enabling dynamic styling through JavaScript. However, runtime CSS-in-JS introduced new performance costs that prompted the evolution toward zero-runtime and utility-first alternatives.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Runtime CSS-in-JS bắt trình duyệt tải thư viện (JS), dịch chuỗi, tạo class ngẫu nhiên, rồi nhét thẻ `<style>` vào HTML mỗi khi render. Rất tốn kém.
Ngược lại, Zero-Runtime (như Vanilla Extract hay CSS Modules) sẽ xuất ra một file `.css` tiêu chuẩn duy nhất lúc Build. Khi chạy, nó không tốn một giọt JavaScript nào để render CSS.

</details>

### Runtime CSS-in-JS (Styled Components, Emotion)

```typescript
// Styles are JavaScript template literals
// Processed at RUNTIME in the browser
import styled from "styled-components";

const Button = styled.button<{ $primary: boolean }>`
  background: ${(props) => (props.$primary ? "blue" : "gray")};
  color: white;
  padding: 8px 16px;
`;

// Performance cost:
// 1. Browser loads styled-components library JS (~12KB gzipped)
// 2. JS executes to parse template literal strings
// 3. Generates unique class hash (e.g., "sc-1x2y3z")
// 4. Injects <style> tag into <head>
// 5. On re-render with changed props: recalculates, injects new <style>
```

### Zero-Runtime CSS-in-JS (Vanilla Extract)

```typescript
// button.css.ts — Processed at BUILD TIME
import { style } from "@vanilla-extract/css";

export const button = style({
  backgroundColor: "blue",
  color: "white",
  padding: "8px 16px",
  ":hover": { backgroundColor: "darkblue" },
});

// button.tsx — At runtime, it is just a string class name
import { button } from "./button.css";
export function Button() {
  return <button className={button}>Click</button>;
}

// Performance: Zero JS runtime cost. Output is a standard .css file.
```

| Aspect | Runtime CSS-in-JS | Zero-Runtime CSS-in-JS | CSS Modules | Tailwind CSS |
|---|---|---|---|---|
| JS bundle impact | +12-15KB library | None | None | None |
| Runtime cost | Style generation on render | None | None | None |
| Dynamic props | Native | Limited (recipes/variants) | CSS Variables | Class toggling |
| RSC compatible | No (requires Context) | Yes | Yes | Yes |
| Type safety | Template literals | Full TypeScript | None | None (IntelliSense via plugin) |
| DX (Developer Experience) | Excellent | Good | Moderate | Excellent |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

| Kịch bản | Khuyên dùng | Lý do |
|---|---|---|
| Next.js App Router | Tailwind hoặc CSS Modules | Không chi phí runtime; Tương thích RSC |
| Xây dựng Design System | Vanilla Extract / CSS Modules | An toàn kiểu dữ liệu; Không làm phình bundle của người xài |
| Cập nhật dự án cũ | Giữ nguyên CSS-in-JS | Đập đi xây lại tốn thời gian hơn hiệu năng thu được |
| Code nhanh, Prototyping | Tailwind CSS | Tốc độ code cực kỳ nhanh |

**Khi nào nên dùng Runtime CSS-in-JS**:
- Web SPA cũ không có Server Component.
- Yêu cầu logic thay đổi màu sắc/vị trí liên tục dựa vào tọa độ con chuột (Drag-and-drop).

</details>

| Scenario | Recommended Approach | Reasoning |
|---|---|---|
| Next.js App Router (RSC) | Tailwind CSS or CSS Modules | Zero runtime; full RSC compatibility |
| Design System library | Vanilla Extract or CSS Modules | Type-safe tokens; no consumer runtime cost |
| Legacy SPA migration | Keep existing CSS-in-JS | Migration cost outweighs performance gain |
| Rapid prototyping | Tailwind CSS | Fastest development velocity |
| Performance-critical landing pages | CSS Modules or Tailwind | Absolute minimum runtime overhead |
| Existing Styled Components codebase | Evaluate migration when upgrading to RSC | Runtime CSS-in-JS conflicts with Server Components |

### When Runtime CSS-in-JS is still acceptable

- SPAs without Server Components where DX is prioritized over performance.
- Libraries that require highly dynamic style computation (e.g., drag-and-drop positioning).

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**CSS Modules**: Giải pháp đơn giản và tốt nhất không cần JS. Hỗ trợ mặc định trong Next.js.
**Thực tiễn tốt nhất**:
1. Dùng CSS Variables (Biến) để lưu màu sắc thay vì code cứng (Design Tokens).
2. Chọn MỘT kiến trúc duy nhất, đừng mix Tailwind với CSS Modules và CSS-in-JS cùng lúc, file CSS sẽ phình rất to.
3. Luôn dùng kiến trúc Zero-runtime cho dự án mới.
4. Quản lý độ ưu tiên CSS bằng `@layer` thay vì nhồi thẻ `!important`.

**Lỗi thường gặp**:
- Dùng Styled Components trong Next.js App Router: Phải ép `"use client"` lên mọi chỗ, phá hỏng toàn bộ sức mạnh của Server Component.
- Bơm giá trị Javascript liên tục vào Styled Components khiến trình duyệt phải tính toán vẽ lại CSS (Style Recalculation) gây giật lag.

</details>

### CSS Modules

The simplest zero-runtime approach, natively supported by Next.js and Vite.

```css
/* Button.module.css */
.button {
  background-color: var(--color-primary);
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
}

.button:hover {
  background-color: var(--color-primary-dark);
}
```

```typescript
import styles from "./Button.module.css";

export function Button({ children }: { children: React.ReactNode }) {
  return <button className={styles.button}>{children}</button>;
}
```

### Best Practices

1. **Use CSS Variables for Design Tokens** — Share theme values between CSS and JavaScript without runtime computation.
2. **Choose one approach per project** — Mixing CSS Modules, Tailwind, and Styled Components creates inconsistency and increases bundle size.
3. **Prefer zero-runtime solutions for new projects** — The industry is moving away from runtime CSS-in-JS.
4. **Use `@layer` for CSS specificity management** — Modern CSS layers prevent specificity wars between components, utilities, and resets.
5. **Co-locate styles with components** — Whether using CSS Modules (`Component.module.css`) or Vanilla Extract (`component.css.ts`), keep styles next to their component.

### Common Pitfalls

1. **Using Styled Components with Next.js App Router** — Requires `"use client"` on every styled component, negating RSC benefits.
2. **Dynamic props causing style recalculation** — Runtime CSS-in-JS generates new `<style>` tags on every prop change, triggering browser Style Recalculation.
3. **Overusing `@apply` in Tailwind** — The Tailwind creator discourages it; use component extraction with `cn()` and CVA instead.
4. **Not purging unused CSS** — Tailwind's JIT mode handles this automatically, but custom CSS must be audited.
5. **Global styles leaking** — Forgetting to use CSS Modules or scoped approaches leads to unexpected style collisions.

### Production Checklist

- [ ] Single CSS strategy chosen and documented for the project.
- [ ] No runtime CSS-in-JS in Server Components.
- [ ] Design Tokens defined as CSS Custom Properties (variables).
- [ ] CSS bundle size monitored in CI pipeline.
- [ ] `@layer` used for specificity management in complex style systems.

---

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một template tạo hệ thống Màu sắc chuẩn (Design Tokens) bằng CSS Variables và chia layer để đảm bảo CSS của bạn luôn được áp dụng đúng, không bị đè bởi các thư viện khác.

</details>

### CSS Variables Design Tokens

```css
/* globals.css — Design Token layer */
@layer base {
  :root {
    --color-primary: #0ea5e9;
    --color-primary-dark: #0284c7;
    --color-surface: #ffffff;
    --color-text: #0f172a;
    --radius-md: 8px;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  }

  [data-theme="dark"] {
    --color-surface: #0f172a;
    --color-text: #f8fafc;
  }
}
```

---

## Related Topics

- [Tailwind Mastery](./tailwind-mastery.md) — Deep dive into Tailwind CSS configuration, `tailwind-merge`, and CVA.
- [Browser Rendering Pipeline](../01-web-fundamentals/browser-rendering-pipeline.md) — How CSS affects the Critical Rendering Path.
- [App Router & React Server Components](../03-nextjs/app-router-rsc.md) — RSC compatibility constraints on CSS approaches.
