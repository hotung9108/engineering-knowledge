# React Fiber and Reconciliation

> A deep dive into React's internal rendering architecture, covering the Fiber data structure, the two-phase render model (Render Phase and Commit Phase), Time Slicing, and Concurrent Rendering. Understanding these internals is essential for diagnosing performance issues and leveraging React 18+ concurrent features.

---

## 1. What is it? (What)

**React Fiber** is the internal reconciliation engine introduced in React 16 that replaced the original Stack Reconciler. A Fiber is a plain JavaScript object representing a **unit of work** — each React element in the tree corresponds to a Fiber node.

### Classification
- **Type**: Virtual DOM reconciliation algorithm / rendering engine.
- **Introduced in**: React 16 (2017), with Concurrent Mode features fully shipped in React 18 (2022).
- **Replaces**: Stack Reconciler (React 15 and earlier).

### Architecture Overview

```mermaid
graph TD
    Update["State Update"] --> RenderPhase["Render Phase<br/>(Async, Interruptible)"]
    RenderPhase --> FiberTree["Walk Fiber Tree<br/>(Depth-First)"]
    FiberTree --> Diff["Diff VDOM<br/>(Old vs New)"]
    Diff --> EffectList["Build Effect List<br/>(Placement, Update, Deletion)"]
    EffectList --> CommitPhase["Commit Phase<br/>(Sync, Uninterruptible)"]
    CommitPhase --> DOMUpdate["Apply to Real DOM"]
    DOMUpdate --> LayoutEffects["Run useLayoutEffect"]
    LayoutEffects --> Paint["Browser Paint"]
    Paint --> Effects["Run useEffect"]
```

---

## 2. Why does it exist? (Why)

### The Problem with Stack Reconciler (React 15)

Before React 16, the reconciliation process was **synchronous and recursive**. When a large update occurred, React locked the main thread until the entire tree was diffed and committed. During this time:

- The browser could not process user input (typing, clicking).
- Animations dropped frames.
- The UI appeared frozen and unresponsive.

### What Fiber Solves

| Problem | Fiber Solution |
|---|---|
| Synchronous, uninterruptible rendering | **Pause and resume** rendering to yield to the browser |
| All updates treated equally | **Priority-based scheduling** (user input > data fetching) |
| Single render pass | **Concurrent rendering** — prepare multiple UI states in background |
| UI freezes during large updates | **Time Slicing** — break work into 5ms chunks |

---

## 3. Without vs. With Comparison (Compare)

### Without Fiber (Stack Reconciler)

```
User types in search box
  → React starts rendering 10,000 search results
  → Main thread BLOCKED for 200ms
  → User's keystrokes are queued, not visible
  → Animation freezes
  → After 200ms: all results appear at once, keystrokes replay
```

### With Fiber (Concurrent Rendering)

```
User types in search box
  → React starts rendering search results at LOW priority
  → After 5ms: React YIELDS to browser
  → Browser processes keystroke, updates input field
  → React resumes rendering results
  → After another 5ms: React yields again
  → Result: Input is responsive, results stream in progressively
```

| Aspect | Stack Reconciler | Fiber Reconciler |
|---|---|---|
| Rendering model | Synchronous, recursive | Asynchronous, iterative |
| Interruptibility | Cannot pause | Can pause, resume, abort |
| Priority handling | None (FIFO) | Lane-based priority system |
| Main thread blocking | Entire tree at once | 5ms time slices |
| React version | ≤ 15 | ≥ 16 (Concurrent in 18+) |

---

## 4. Common Use Cases

1. **Large list rendering** — `useTransition` marks list updates as low priority, keeping the search input responsive.
2. **Tab switching** — `useDeferredValue` defers expensive tab content rendering while showing the tab header immediately.
3. **Real-time dashboards** — Concurrent rendering ensures high-frequency data updates do not block user interactions.
4. **Form-heavy applications** — Fiber's priority system ensures typing responsiveness even during complex validation rendering.
5. **Suspense boundaries** — Fiber's architecture enables streaming server-rendered content and progressive hydration.

### When Fiber internals matter less

- Simple CRUD applications with minimal component depth.
- Static content pages with little interactivity.

---

## 5. Deep Practice

### The Two-Phase Render Model

#### Phase 1: Render Phase (Asynchronous, Interruptible)

1. Starting from the root, React walks the Fiber Tree using a depth-first traversal.
2. Calls the function body of each component (or `render()` for class components).
3. Diffs the new VDOM against the old VDOM.
4. Tags changed Fiber nodes with effects (Placement, Update, Deletion) into an **Effect List**.

> [!IMPORTANT]
> The Render Phase can be **paused, aborted, or restarted**. Therefore, side effects (API calls, DOM mutations, subscriptions) must never be placed in the function body of a component. This is the fundamental reason `useEffect` exists.

#### Phase 2: Commit Phase (Synchronous, Uninterruptible)

1. Traverses the Effect List built in Phase 1.
2. Applies all DOM mutations to the Real DOM.
3. Runs `useLayoutEffect` callbacks (before browser paint).
4. Browser paints the updated screen.
5. Runs `useEffect` callbacks (after browser paint).

> [!IMPORTANT]
> The Commit Phase cannot be interrupted. Once React begins mutating the DOM, it must complete to avoid displaying an inconsistent UI state.

### Time Slicing and the Scheduler

React implements its own scheduler (similar to `requestIdleCallback`) to perform Time Slicing:

- Instead of processing 10,000 components in one pass, React processes a batch of components for approximately 5ms.
- After 5ms, React yields control to the browser for rendering, event handling, and other high-priority tasks.
- When the browser is idle, React resumes processing the next batch.

This is the mechanism behind `useTransition` and `useDeferredValue` in React 18.

### Best Practices

1. **Use `useTransition` for non-urgent state updates** — Wrap slow state updates to prevent them from blocking user input.
2. **Use `useDeferredValue` for derived expensive computations** — Defers re-rendering of expensive components while the source value updates immediately.
3. **Never perform side effects in the component body** — They will execute unpredictably due to Render Phase restarts.
4. **Understand `useLayoutEffect` vs `useEffect`** — Use `useLayoutEffect` only when you need to read layout and synchronously re-render before the browser paints.
5. **Leverage `<Suspense>` boundaries strategically** — Each boundary creates an independent loading state, enabling progressive rendering.

### Common Pitfalls

1. **Placing API calls directly in component body** — These re-execute on every Render Phase restart.
2. **Assuming render count equals commit count** — In Concurrent Mode, a component may render multiple times but commit only once.
3. **Using `useLayoutEffect` for non-layout work** — It blocks the browser paint, causing jank.
4. **Not wrapping expensive state transitions with `useTransition`** — Leaves the UI unresponsive during heavy computation.
5. **Relying on render execution order** — Fiber's interruptible rendering makes execution order non-deterministic.

### Production Checklist

- [ ] No side effects in component function bodies (only in `useEffect` or event handlers).
- [ ] `useTransition` applied to all non-urgent state updates in interactive views.
- [ ] `<Suspense>` boundaries wrapping all async data-fetching components.
- [ ] `useLayoutEffect` used only when pre-paint DOM measurement is required.
- [ ] React Profiler (DevTools) used to verify no unnecessary re-renders.

---

## 6. Code Templates and Integration

### useTransition for Responsive Search

```typescript
import { useState, useTransition } from "react";

interface SearchableListProps {
  items: string[];
}

export function SearchableList({ items }: SearchableListProps) {
  const [query, setQuery] = useState("");
  const [filteredItems, setFilteredItems] = useState(items);
  const [isPending, startTransition] = useTransition();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const value = e.target.value;
    setQuery(value); // HIGH priority — updates input immediately

    startTransition(() => {
      // LOW priority — deferred, interruptible
      const filtered = items.filter((item) =>
        item.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredItems(filtered);
    });
  }

  return (
    <div>
      <input value={query} onChange={handleChange} placeholder="Search..." />
      {isPending && <span>Updating results...</span>}
      <ul>
        {filteredItems.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Related Topics

- [Performance Tuning](./performance-tuning.md) — Practical memoization and composition strategies built on Fiber's re-render mechanics.
- [JS Engine Internals](../01-web-fundamentals/js-engine-internals.md) — How the Event Loop interacts with React's scheduler.
- [App Router & React Server Components](../03-nextjs/app-router-rsc.md) — How Fiber enables server-side streaming with Suspense.
