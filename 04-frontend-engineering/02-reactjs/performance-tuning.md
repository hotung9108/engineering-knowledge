# React Performance Tuning

> A comprehensive guide to understanding React's re-render mechanics and applying optimization techniques including `React.memo`, `useCallback`, `useMemo`, Component Composition, Code Splitting, and the upcoming React Compiler. Optimization without measurement is premature — profile first, optimize second.

---

## 1. What is it? (What)

**React Performance Tuning** is the discipline of minimizing unnecessary work in React's rendering pipeline. React's default behavior is to re-render an entire subtree whenever a parent re-renders, regardless of whether child props have changed. Performance tuning intervenes in this process to skip unnecessary re-renders.

### Classification
- **Type**: Frontend optimization discipline.
- **Framework**: React 18+ with TypeScript.
- **Key APIs**: `React.memo`, `useMemo`, `useCallback`, `React.lazy`, `Suspense`, `useTransition`, `useDeferredValue`.

---

## 2. Why does it exist? (Why)

React is fast by default for most applications. However, performance degrades in these scenarios:

| Scenario | Symptom | Root cause |
|---|---|---|
| Large data tables (1000+ rows) | Janky scrolling, input lag | Every row re-renders on any state change |
| Complex forms | Typing delay | Every keystroke triggers full form tree re-render |
| Dashboard with many widgets | Slow tab switching | All widgets re-render even if only one changed |
| Heavy computation in render | Dropped frames | Expensive calculation runs on every render |

Understanding **when and why** React re-renders is the prerequisite for all optimization work.

---

## 3. Without vs. With Comparison (Compare)

### Without optimization — Cascading re-renders

```typescript
function Parent() {
  const [count, setCount] = useState(0);

  // New function reference created every render — breaks React.memo
  const handleClick = () => console.log("clicked");

  // New object reference created every render — breaks React.memo
  const config = { theme: "dark" };

  return (
    <div>
      <button onClick={() => setCount((c) => c + 1)}>Count: {count}</button>
      {/* ExpensiveChild re-renders EVERY time Parent re-renders */}
      <ExpensiveChild onClick={handleClick} config={config} />
    </div>
  );
}
```

### With optimization — Stable references

```typescript
function Parent() {
  const [count, setCount] = useState(0);

  // Stable function reference
  const handleClick = useCallback(() => console.log("clicked"), []);

  // Stable object reference
  const config = useMemo(() => ({ theme: "dark" }), []);

  return (
    <div>
      <button onClick={() => setCount((c) => c + 1)}>Count: {count}</button>
      {/* ExpensiveChild skips re-render when props are referentially equal */}
      <ExpensiveChild onClick={handleClick} config={config} />
    </div>
  );
}

const ExpensiveChild = React.memo(function ExpensiveChild({
  onClick,
  config,
}: {
  onClick: () => void;
  config: { theme: string };
}) {
  console.log("ExpensiveChild rendered");
  return <div onClick={onClick}>Theme: {config.theme}</div>;
});
```

| Aspect | Without optimization | With optimization |
|---|---|---|
| ExpensiveChild re-renders | Every time Parent renders | Only when props actually change |
| Function references | New on every render | Stable via `useCallback` |
| Object references | New on every render | Stable via `useMemo` |
| Complexity | Simpler code | Slightly more complex |

---

## 4. Common Use Cases

1. **Data grids and virtualized lists** — `React.memo` on row components; `useMemo` for computed data.
2. **Real-time dashboards** — `useTransition` for non-urgent data updates; selective Zustand subscriptions.
3. **Form-heavy applications** — Isolate changing state to prevent full form tree re-renders.
4. **Route-based code splitting** — `React.lazy` + `Suspense` for each route.
5. **Modal and dialog lazy loading** — Load heavy components only when displayed.

### When NOT to optimize

- **Premature optimization** — If no user-visible performance problem exists, do not add memoization.
- **Simple components** — `React.memo` on a `<span>` or `<div>` adds overhead without benefit.
- **Components that always re-render with new props** — Memoization is wasted if props change every render.

> [!CAUTION]
> **Do not apply `useMemo` and `useCallback` everywhere.** Each hook consumes memory (to store the previous value) and CPU (to compare the dependency array). Only use them when passing values to `React.memo` components or as dependencies in `useEffect`.

---

## 5. Deep Practice

### React Re-render Rules

A component re-renders if **any** of these conditions is true:

1. Its own `state` changes.
2. A `Context` it subscribes to changes.
3. Its **parent re-renders** (regardless of whether props changed).

React does **not** automatically compare props. `React.memo` opts into shallow prop comparison.

### Composition-Based Optimization (No Memoization Required)

The most elegant optimization technique: restructure JSX to avoid re-renders entirely.

**Problem**: Parent has state that causes an `ExpensiveTree` to re-render unnecessarily.

**Solution**: Lift content up via `children` prop.

```typescript
function ColorPickerWrapper({ children }: { children: ReactNode }) {
  const [color, setColor] = useState("red");
  return (
    <div style={{ color }}>
      <button onClick={() => setColor("blue")}>Change Color</button>
      {/* children was created by the parent component BEFORE ColorPickerWrapper rendered.
          React reuses the existing JSX element — no re-render. */}
      {children}
    </div>
  );
}

// Usage:
// <ColorPickerWrapper>
//   <ExpensiveTree /> {/* Does NOT re-render when color changes */}
// </ColorPickerWrapper>
```

### Code Splitting and Lazy Loading

```typescript
import { lazy, Suspense } from "react";

const HeavyChartModal = lazy(() => import("./HeavyChartModal"));

function Dashboard() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsModalOpen(true)}>Show Chart</button>
      {isModalOpen && (
        <Suspense fallback={<Spinner />}>
          {/* HeavyChartModal JS is only fetched when isModalOpen becomes true */}
          <HeavyChartModal onClose={() => setIsModalOpen(false)} />
        </Suspense>
      )}
    </div>
  );
}
```

### Best Practices

1. **Profile before optimizing** — Use React DevTools Profiler to identify which components re-render unnecessarily and how much time each render takes.
2. **Prefer composition over memoization** — Restructuring components with `children` is zero-cost and eliminates re-renders without hooks.
3. **Memoize expensive computations** — Use `useMemo` for computations that are genuinely expensive (sorting, filtering, transforming large datasets).
4. **Use selective store subscriptions** — `useStore((s) => s.field)` instead of `useStore()`.
5. **Virtualize long lists** — Use `@tanstack/react-virtual` or `react-window` instead of rendering thousands of DOM nodes.

### Common Pitfalls

1. **Memoizing everything** — Adds complexity and memory overhead without measurable benefit for simple components.
2. **Unstable dependency arrays** — Objects or functions created inline in the dependency array defeat `useMemo`/`useCallback`.
3. **Context for high-frequency updates** — Context has no selective subscription; every consumer re-renders on any change.
4. **Forgetting `React.memo` on the child** — `useCallback` on the parent is pointless if the child is not wrapped in `React.memo`.
5. **Ignoring the React Compiler** — React 19's compiler will auto-insert memoization; manual memoization will become less necessary.

### Production Checklist

- [ ] React DevTools Profiler used to identify re-render bottlenecks.
- [ ] `React.memo` applied only to components with verified unnecessary re-renders.
- [ ] `useCallback`/`useMemo` paired with `React.memo` on child components.
- [ ] Composition pattern (`children` prop) used where applicable before resorting to memoization.
- [ ] Long lists (>100 items) virtualized with `@tanstack/react-virtual` or `react-window`.
- [ ] Route-level code splitting implemented with `React.lazy` + `Suspense`.

---

## 6. Code Templates and Integration

### Performance-Optimized List Component

```typescript
import { memo, useMemo, useCallback, useState } from "react";

interface Item {
  id: string;
  name: string;
  category: string;
}

interface ItemRowProps {
  item: Item;
  onSelect: (id: string) => void;
}

// Memoized row — only re-renders if item or onSelect reference changes
const ItemRow = memo(function ItemRow({ item, onSelect }: ItemRowProps) {
  return (
    <tr onClick={() => onSelect(item.id)}>
      <td>{item.name}</td>
      <td>{item.category}</td>
    </tr>
  );
});

export function ItemList({ items }: { items: Item[] }) {
  const [filter, setFilter] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // Expensive computation — memoized
  const filteredItems = useMemo(
    () =>
      items.filter((item) =>
        item.name.toLowerCase().includes(filter.toLowerCase())
      ),
    [items, filter]
  );

  // Stable callback — prevents ItemRow re-renders
  const handleSelect = useCallback((id: string) => {
    setSelectedId(id);
  }, []);

  return (
    <div>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filter items..."
      />
      <table>
        <tbody>
          {filteredItems.map((item) => (
            <ItemRow key={item.id} item={item} onSelect={handleSelect} />
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## Related Topics

- [React Fiber & Reconciliation](./react-fiber-reconciliation.md) — The rendering engine that performance tuning optimizes.
- [State Management Patterns](./state-management-patterns.md) — How state management choices impact re-render scope.
- [Web Performance & Core Web Vitals](../01-web-fundamentals/web-performance-vitals.md) — How React performance affects INP.
