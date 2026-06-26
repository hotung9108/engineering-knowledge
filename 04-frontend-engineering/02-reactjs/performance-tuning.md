# React Performance Tuning

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hướng dẫn toàn diện để hiểu cơ chế re-render của React và áp dụng các kỹ thuật tối ưu hóa bao gồm `React.memo`, `useCallback`, `useMemo`, Component Composition, Code Splitting và React Compiler sắp ra mắt. Tối ưu hóa mà không đo lường là sự vội vàng — hãy profile trước, tối ưu sau.

</details>

> **Summary**: A comprehensive guide to understanding React's re-render mechanics and applying optimization techniques including `React.memo`, `useCallback`, `useMemo`, Component Composition, Code Splitting, and the upcoming React Compiler. Optimization without measurement is premature — profile first, optimize second.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn là một họa sĩ đang vẽ một bức tranh phong cảnh có cái cây và mặt trời. 
- **Không tối ưu**: Khi khách hàng bảo "Đổi mặt trời thành màu đỏ", bạn vứt cả bức tranh đi, lấy giấy mới vẽ lại từ đầu cả cái cây lẫn mặt trời (Re-render toàn bộ). Rất tốn sức!
- **Tối ưu hóa (React Performance Tuning)**: Bạn vẽ mặt trời trên một tờ giấy trong suốt, và vẽ cái cây trên một tờ khác. Khi đổi màu mặt trời, bạn chỉ vẽ lại tờ giấy mặt trời, tờ giấy vẽ cây được giữ nguyên (React.memo). Bạn đỡ mệt hơn rất nhiều.

</details>

Imagine you are a painter drawing a landscape with a tree and a sun.
- **Unoptimized**: When the client says "Make the sun red", you throw the entire painting in the trash, get a new canvas, and redraw both the tree and the sun from scratch (Full Re-render). Exhausting!
- **Optimized (React Performance Tuning)**: You paint the sun on one transparent sheet, and the tree on another. When the sun changes color, you only redraw the sun sheet, keeping the tree sheet exactly as it was (`React.memo`). You save a massive amount of effort.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**React Performance Tuning** là kỷ luật giảm thiểu các công việc thừa thãi trong quá trình render của React. Mặc định, React sẽ tự động vẽ lại (re-render) toàn bộ các component con nếu component cha bị vẽ lại, bất kể props của component con có đổi hay không. Tối ưu hiệu năng là việc can thiệp vào quá trình này để bỏ qua các bước vẽ lại không cần thiết.

**Phân loại:**
- **Loại**: Kỷ luật tối ưu Frontend.
- **Framework**: React 18+ với TypeScript.
- **Các API chính**: `React.memo`, `useMemo`, `useCallback`, `React.lazy`, `Suspense`, `useTransition`, `useDeferredValue`.

</details>

**React Performance Tuning** is the discipline of minimizing unnecessary work in React's rendering pipeline. React's default behavior is to re-render an entire subtree whenever a parent re-renders, regardless of whether child props have changed. Performance tuning intervenes in this process to skip unnecessary re-renders.

### Classification
- **Type**: Frontend optimization discipline.
- **Framework**: React 18+ with TypeScript.
- **Key APIs**: `React.memo`, `useMemo`, `useCallback`, `React.lazy`, `Suspense`, `useTransition`, `useDeferredValue`.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Mặc định React đã rất nhanh. Tuy nhiên, hiệu năng sẽ sụp đổ trong các trường hợp: bảng dữ liệu khổng lồ (1000+ dòng), form phức tạp (gõ một chữ mà cả form giật tung), hoặc khi tính toán quá nặng lúc render làm tụt frame. Hiểu được **khi nào và tại sao** React re-render là điều kiện tiên quyết để tối ưu.

</details>

React is fast by default for most applications. However, performance degrades in these scenarios:

| Scenario | Symptom | Root cause |
|---|---|---|
| Large data tables (1000+ rows) | Janky scrolling, input lag | Every row re-renders on any state change |
| Complex forms | Typing delay | Every keystroke triggers full form tree re-render |
| Dashboard with many widgets | Slow tab switching | All widgets re-render even if only one changed |
| Heavy computation in render | Dropped frames | Expensive calculation runs on every render |

Understanding **when and why** React re-renders is the prerequisite for all optimization work.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu không tối ưu, mỗi lần component Cha re-render, nó sẽ tạo ra một hàm `handleClick` mới tinh, khiến cho component Con (`ExpensiveChild`) tưởng là có dữ liệu mới nên cũng re-render theo, dù ta đã bọc Con bằng `React.memo`.
Để giải quyết, ta dùng `useCallback` và `useMemo` để "cố định" địa chỉ ô nhớ của hàm và object, giúp `React.memo` hoạt động đúng.

</details>

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

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bảng dữ liệu lớn (Data grids)**: Dùng `React.memo` cho các dòng (row); dùng `useMemo` cho dữ liệu đã tính toán.
2. **Dashboard thời gian thực**: Dùng `useTransition` cho các cập nhật dữ liệu không gấp; thiết lập Zustand để chỉ update một phần (selective subscriptions).
3. **Form khổng lồ**: Tách riêng state của từng input để không làm cả form re-render.
4. **Code Splitting theo trang (Route)**: Dùng `React.lazy` + `Suspense`.

**Khi KHÔNG NÊN tối ưu**:
- Nếu chưa thấy lag, đừng tối ưu (Premature optimization).
- Không dùng `React.memo` cho mấy thẻ quá đơn giản như `<span>` hay `<div>` vì nó làm code chậm đi do phải tốn công đi so sánh props.

</details>

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

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Luật Re-render của React**:
1. State của chính nó thay đổi.
2. Cái Context mà nó lắng nghe thay đổi.
3. Component Cha của nó bị re-render. (React KHÔNG tự so sánh props, bạn phải bọc `React.memo` nó mới chịu so sánh).

**Tối ưu bằng Composition (Đỉnh cao không cần Hook)**:
Cách xịn nhất là cấu trúc lại HTML (JSX) để tránh re-render. Nhét các component nặng vào thuộc tính `children`. Khi cha đổi màu (state), component truyền vào `children` trước đó sẽ không bị ảnh hưởng.

</details>

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

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một template danh sách được tối ưu hoàn toàn. Nó tính toán (filter) nhanh hơn nhờ `useMemo`, và mỗi dòng (row) được bọc bởi `React.memo` cộng thêm hàm `onSelect` bọc bằng `useCallback`, đảm bảo chỉ có dòng nào được click mới re-render.

</details>

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
