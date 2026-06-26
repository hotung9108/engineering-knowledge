# 01 — Web Fundamentals

> Core web platform knowledge that every frontend engineer must master before diving into frameworks. Covers JavaScript engine internals, browser rendering mechanics, advanced TypeScript, and web performance optimization.

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Kiến thức cốt lõi về nền tảng web mà mọi kỹ sư frontend phải nắm vững trước khi đi sâu vào các framework. Bao gồm hoạt động bên trong của JavaScript engine, cơ chế render của trình duyệt, TypeScript nâng cao, và tối ưu hóa hiệu năng web.

</details>

---

## Prerequisites

- [01 — Fundamentals / Programming](../../01-fundamentals/programming/) — OOP, SOLID, Clean Code basics.
- [01 — Fundamentals / Network](../../01-fundamentals/network/) — HTTP/HTTPS, TCP/IP.

---

## Content

| # | File | Description |
|---|---|---|
| 1 | [JS Engine Internals](./js-engine-internals.md) | V8 architecture, JIT compilation (Ignition + TurboFan), Event Loop, Garbage Collection. |
| 2 | [Browser Rendering Pipeline](./browser-rendering-pipeline.md) | Critical Rendering Path, Reflow/Repaint, GPU Compositing, `will-change`. |
| 3 | [Advanced TypeScript](./advanced-typescript.md) | Type Narrowing, Utility Types, Conditional Types, `infer`, Branded Types, Cheatsheet. |
| 4 | [Web Performance & Core Web Vitals](./web-performance-vitals.md) | LCP, INP, CLS optimization, Resource Hints, HTTP Caching, Service Workers. |

---

## Learning Objectives

After completing this section, you should be able to:

- Explain V8's JIT compilation pipeline and the Event Loop execution model.
- Identify and resolve layout thrashing and rendering performance bottlenecks.
- Write advanced TypeScript using Discriminated Unions, Conditional Types, and Branded Types.
- Optimize all three Core Web Vitals (LCP, INP, CLS) to "Good" thresholds.

---

## Related Sections

- [02 — ReactJS](../02-reactjs/) — Framework-level rendering built on these web fundamentals.
- [04 — Styling](../04-styling/) — CSS architecture and its impact on the rendering pipeline.
