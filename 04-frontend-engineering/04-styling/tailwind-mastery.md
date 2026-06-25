# Tailwind CSS Mastery

> An advanced guide to Tailwind CSS covering deep configuration, the class conflict problem and its solution (`tailwind-merge` + `clsx`), variant-based component design with CVA (Class Variance Authority), and custom plugin authoring. Tailwind is the dominant styling approach for modern React applications.

---

## 1. What is it? (What)

**Tailwind CSS** is a utility-first CSS framework that provides low-level utility classes (e.g., `bg-blue-500`, `p-4`, `rounded-lg`) for building designs directly in HTML/JSX. Unlike component-based frameworks (Bootstrap), Tailwind does not impose design opinions — it provides atomic building blocks.

### Classification
- **Type**: Utility-first CSS framework.
- **Processing**: Build time (JIT compiler scans source files and generates only the used classes).
- **Runtime cost**: Zero — output is a standard `.css` file.
- **Bundle size**: Typically 5-15KB gzipped for a full application.

---

## 2. Why does it exist? (Why)

Traditional CSS approaches (BEM, CSS Modules, CSS-in-JS) all require developers to invent class names, manage file organization, and fight specificity conflicts. Tailwind eliminates these problems by:

| Problem | Tailwind Solution |
|---|---|
| Naming classes | No custom names needed — use utilities directly |
| Dead CSS | JIT compiler includes only classes present in source files |
| Context switching | Styles are co-located in JSX — no separate CSS files |
| Design consistency | Constrained value system (spacing, colors, sizes) |
| Responsive design | Built-in breakpoint prefixes (`md:`, `lg:`) |

---

## 3. Without vs. With Comparison (Compare)

### Without Tailwind — Traditional CSS

```css
/* button.module.css — Separate file, custom names */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  transition: background-color 150ms;
}
.button-primary {
  background-color: #3b82f6;
  color: white;
}
.button-primary:hover {
  background-color: #2563eb;
}
```

### With Tailwind — Inline utilities

```typescript
function Button({ children }: { children: React.ReactNode }) {
  return (
    <button className="inline-flex items-center justify-center px-4 py-2 rounded-md font-medium transition-colors bg-blue-500 text-white hover:bg-blue-600">
      {children}
    </button>
  );
}
// No CSS file needed. Classes are atomic, composable, and tree-shaken.
```

| Aspect | Traditional CSS/Modules | Tailwind CSS |
|---|---|---|
| File count | 2 per component (`.tsx` + `.css`) | 1 per component |
| Naming burden | High (BEM, custom names) | None |
| Dead CSS risk | High | Zero (JIT scans source) |
| Design consistency | Manual enforcement | Built-in constraint system |
| Learning curve | Low (standard CSS) | Moderate (utility vocabulary) |
| Long class strings | None | Can become verbose |

---

## 4. Common Use Cases

1. **Rapid UI development** — Build production-quality layouts 2-3x faster than traditional CSS.
2. **Design systems** — Tailwind's theme configuration serves as a single source of truth for design tokens.
3. **Component libraries** — CVA + `tailwind-merge` enable variant-based, conflict-free components.
4. **Responsive and dark mode** — Built-in `md:`, `lg:`, `dark:` prefixes reduce boilerplate significantly.
5. **Next.js / Vite projects** — First-class support with zero configuration.

### When Tailwind may not be ideal

- Projects where designers deliver pixel-perfect CSS that does not align with Tailwind's spacing/sizing scale.
- Teams with strong CSS expertise who prefer CSS Modules or Vanilla Extract.
- Highly dynamic styles computed from JavaScript state at runtime.

---

## 5. Deep Practice

### Deep Configuration (Design Tokens)

```javascript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    // Override: Replaces ALL default fonts
    fontFamily: {
      sans: ["Inter", "system-ui", "sans-serif"],
      mono: ["JetBrains Mono", "monospace"],
    },
    extend: {
      // Extend: Adds to defaults without removing them
      colors: {
        brand: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          500: "#0ea5e9",
          600: "#0284c7",
          900: "#0c4a6e",
        },
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-in-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
```

### Solving Class Conflicts with `tailwind-merge` + `clsx`

When a component has default classes and receives additional classes via props, conflicts are unpredictable because CSS specificity depends on **declaration order in the stylesheet**, not order in the class string.

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merges class names with Tailwind-aware conflict resolution.
 * The last conflicting utility wins (e.g., "bg-red-500" overrides "bg-blue-500").
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

// Usage in a component:
function Button({ className, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn("bg-blue-500 text-white px-4 py-2 rounded-md", className)}
      {...props}
    />
  );
}

// <Button className="bg-red-500" />
// Result: "text-white px-4 py-2 rounded-md bg-red-500"
// twMerge removes "bg-blue-500" because "bg-red-500" is the override.
```

### CVA (Class Variance Authority) for Variant-Based Components

```typescript
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  // Base classes — always applied
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2",
  {
    variants: {
      variant: {
        default: "bg-blue-500 text-white hover:bg-blue-600",
        outline: "border border-gray-300 bg-transparent hover:bg-gray-100",
        destructive: "bg-red-500 text-white hover:bg-red-600",
        ghost: "hover:bg-gray-100",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        default: "h-10 px-4 py-2 text-sm",
        lg: "h-12 px-8 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

// Usage:
// <Button variant="destructive" size="lg">Delete</Button>
// <Button variant="outline" className="w-full">Full Width</Button>
```

### Custom Tailwind Plugin

```javascript
const plugin = require("tailwindcss/plugin");

module.exports = {
  plugins: [
    plugin(function ({ addComponents, theme }) {
      addComponents({
        ".card": {
          backgroundColor: theme("colors.white"),
          borderRadius: theme("borderRadius.lg"),
          padding: theme("spacing.6"),
          boxShadow: theme("boxShadow.md"),
        },
        ".card-dark": {
          backgroundColor: theme("colors.gray.800"),
          color: theme("colors.gray.100"),
        },
      });
    }),
  ],
};
```

### Best Practices

1. **Never use arbitrary values for design tokens** — Define brand colors, spacing, and fonts in `tailwind.config.ts` instead of using `bg-[#ff0000]`.
2. **Always use `cn()` (tailwind-merge + clsx) for component class merging** — Prevents unpredictable class conflicts.
3. **Use CVA for all variant-based components** — Provides type-safe variants and consistent API.
4. **Avoid `@apply` for component extraction** — Use React component abstraction instead; the Tailwind creator explicitly discourages heavy `@apply` usage.
5. **Configure `content` paths precisely** — Overly broad content scanning slows build times.

### Common Pitfalls

1. **Class conflicts without `tailwind-merge`** — `bg-blue-500 bg-red-500` has unpredictable behavior without `twMerge`.
2. **Dynamic class construction** — `bg-${color}-500` breaks JIT scanning. Use a lookup map instead: `const colors = { red: "bg-red-500" }`.
3. **Arbitrary values everywhere** — Defeats Tailwind's constraint system; use config extension instead.
4. **Not using the VS Code extension** — IntelliSense provides autocomplete, previews, and linting for Tailwind classes.
5. **Overly long class strings** — Extract components instead of writing 20+ utilities on a single element.

### Production Checklist

- [ ] `tailwind.config.ts` defines all project design tokens (no arbitrary values in components).
- [ ] `cn()` utility using `tailwind-merge` + `clsx` used in all reusable components.
- [ ] CVA used for all components with more than two visual variants.
- [ ] Tailwind CSS IntelliSense VS Code extension installed and configured.
- [ ] `content` paths in config are precise (no unnecessary file scanning).

---

## 6. Code Templates and Integration

### Complete `cn` Utility Setup

```typescript
// src/lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
```

### Package Dependencies

```json
{
  "dependencies": {
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.0",
    "@tailwindcss/typography": "^0.5.0",
    "@tailwindcss/forms": "^0.5.0"
  }
}
```

---

## 7. Cheatsheet

| Category | Utilities | Example |
|---|---|---|
| Spacing | `p-`, `m-`, `px-`, `py-`, `gap-` | `px-4 py-2 gap-3` |
| Flexbox | `flex`, `items-`, `justify-`, `flex-col` | `flex items-center justify-between` |
| Grid | `grid`, `grid-cols-`, `col-span-` | `grid grid-cols-3 gap-4` |
| Typography | `text-`, `font-`, `leading-`, `tracking-` | `text-lg font-bold leading-tight` |
| Colors | `bg-`, `text-`, `border-` | `bg-blue-500 text-white` |
| Borders | `border`, `rounded-`, `ring-` | `border rounded-lg ring-2` |
| Effects | `shadow-`, `opacity-`, `blur-` | `shadow-md opacity-75` |
| Transitions | `transition-`, `duration-`, `ease-` | `transition-colors duration-200` |
| Responsive | `sm:`, `md:`, `lg:`, `xl:`, `2xl:` | `md:grid-cols-2 lg:grid-cols-3` |
| Dark mode | `dark:` | `dark:bg-gray-900 dark:text-white` |
| Hover/Focus | `hover:`, `focus:`, `active:` | `hover:bg-blue-600 focus:ring-2` |
| Group | `group`, `group-hover:` | `group-hover:text-blue-500` |

---

## Related Topics

- [CSS Architecture & Performance](./css-architecture-performance.md) — Comparison of all CSS approaches.
- [Advanced Component Patterns](../02-reactjs/advanced-component-patterns.md) — Building reusable components that consume Tailwind + CVA.
- [Frontend CI/CD & Deployment](../06-build-tools/frontend-ci-cd.md) — Bundle size monitoring for Tailwind output.
