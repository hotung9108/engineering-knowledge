# CSS Architecture and Performance

> A technical analysis of CSS strategy trade-offs for modern frontend applications, comparing Runtime CSS-in-JS, Zero-Runtime CSS-in-JS, CSS Modules, and Utility-first approaches. The choice of CSS architecture has direct impact on bundle size, rendering performance, and Server Component compatibility.

---

## 1. What is it? (What)

**CSS Architecture** refers to the systematic approach used to author, organize, and deliver stylesheets in a web application. In the React ecosystem, the primary debate centers on where CSS is processed — at runtime in the browser or at build time by the compiler.

### Classification
- **Type**: Frontend styling architecture decision.
- **Categories**: Runtime CSS-in-JS, Zero-Runtime CSS-in-JS, CSS Modules, Utility-first CSS.
- **Impact areas**: Performance (CRP, JS bundle), Developer Experience, RSC compatibility.

---

## 2. Why does it exist? (Why)

Traditional CSS has fundamental scaling problems in large applications:

| Problem | Description |
|---|---|
| Global namespace | All class names share a single scope — collisions are inevitable |
| Dead code | Unused styles accumulate because deletion risks breaking other pages |
| No co-location | Styles live in separate files, disconnected from the components they serve |
| Dynamic styling | CSS alone cannot respond to JavaScript state without class toggling |

CSS-in-JS solved these problems by scoping styles to components and enabling dynamic styling through JavaScript. However, runtime CSS-in-JS introduced new performance costs that prompted the evolution toward zero-runtime and utility-first alternatives.

---

## 3. Without vs. With Comparison (Compare)

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

## 4. Common Use Cases

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

## 5. Deep Practice

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

## 6. Code Templates and Integration

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
