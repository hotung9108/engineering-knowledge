# 02 — ReactJS

> Deep dive into React's internal architecture and advanced patterns. Covers the Fiber reconciliation engine, component design patterns for reusable UI libraries, state management paradigms, and performance tuning techniques.

---

## Prerequisites

- [01 — Web Fundamentals](../01-web-fundamentals/) — JS Engine, Browser Rendering, TypeScript, Performance.

---

## Content

| # | File | Description |
|---|---|---|
| 1 | [React Fiber & Reconciliation](./react-fiber-reconciliation.md) | Fiber architecture, 2-Phase Render, Time Slicing, Concurrent Rendering. |
| 2 | [Advanced Component Patterns](./advanced-component-patterns.md) | Compound Components, Render Props, Headless UI, Polymorphic Components. |
| 3 | [State Management Patterns](./state-management-patterns.md) | Server vs Client State, Zustand, Jotai, Signals, React Query. |
| 4 | [Performance Tuning](./performance-tuning.md) | Re-render mechanics, `React.memo`, Composition, Code Splitting, React Compiler. |

---

## Learning Objectives

After completing this section, you should be able to:

- Explain React's two-phase render model and how Fiber enables concurrent rendering.
- Design reusable component APIs using Compound, Headless, and Polymorphic patterns.
- Select the appropriate state management tool based on state category (server vs. client).
- Profile and optimize React re-render performance using DevTools and composition techniques.

---

## Related Sections

- [01 — Web Fundamentals](../01-web-fundamentals/) — Platform knowledge underpinning React's behavior.
- [03 — Next.js](../03-nextjs/) — Full-stack React framework built on these React fundamentals.
- [04 — Styling](../04-styling/) — Component styling approaches (Tailwind, CVA).
