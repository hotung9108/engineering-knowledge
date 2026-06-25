# 04 — Styling

> Technical analysis of CSS strategy trade-offs for modern React applications. Covers the runtime cost of CSS-in-JS, zero-runtime alternatives, CSS Modules, and advanced Tailwind CSS patterns including `tailwind-merge`, CVA, and custom plugins.

---

## Prerequisites

- [01 — Web Fundamentals](../01-web-fundamentals/) — Browser Rendering Pipeline (CSS impact on CRP).
- [02 — ReactJS](../02-reactjs/) — Component architecture that styling approaches must integrate with.

---

## Content

| # | File | Description |
|---|---|---|
| 1 | [CSS Architecture & Performance](./css-architecture-performance.md) | Runtime vs Zero-Runtime CSS-in-JS, CSS Modules, architecture comparison. |
| 2 | [Tailwind Mastery](./tailwind-mastery.md) | Deep config, `tailwind-merge` + `clsx`, CVA variants, custom plugins, Cheatsheet. |

---

## Learning Objectives

After completing this section, you should be able to:

- Evaluate and justify a CSS strategy based on RSC compatibility, performance, and DX.
- Implement the `cn()` utility with `tailwind-merge` for conflict-free class merging.
- Build variant-based components with CVA (Class Variance Authority).
- Author custom Tailwind plugins for project-specific design tokens.

---

## Related Sections

- [01 — Web Fundamentals / Browser Rendering](../01-web-fundamentals/browser-rendering-pipeline.md) — How CSS choices affect rendering performance.
- [03 — Next.js](../03-nextjs/) — RSC compatibility constraints on CSS approaches.
