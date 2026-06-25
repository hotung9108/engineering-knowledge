# Advanced Component Patterns

> A practical guide to advanced React component design patterns — Compound Components, Render Props, Headless Components (Custom Hooks), and Polymorphic Components. These patterns are the foundation of building reusable, flexible, and accessible UI libraries at scale.

---

## 1. What is it? (What)

**Advanced Component Patterns** are architectural techniques for designing React components that maximize reusability, flexibility, and separation of concerns. They solve the fundamental tension between providing sensible defaults and allowing consumer customization.

### Classification
- **Type**: UI architecture patterns.
- **Framework**: React 18+ with TypeScript.
- **Key patterns**: Compound Components, Render Props, Headless UI (Custom Hooks), Polymorphic Components.

---

## 2. Why does it exist? (Why)

As component libraries grow, naive designs hit scaling problems:

| Problem | Root Cause | Pattern Solution |
|---|---|---|
| Props explosion (20+ props) | All configuration via props | **Compound Components** — declarative child composition |
| Rigid UI that cannot be customized | Component owns the markup | **Render Props / Headless** — consumer controls rendering |
| `as` prop without type safety | Casting element types manually | **Polymorphic Components** — generic element type |
| Logic duplication across components | Business logic mixed with UI | **Custom Hooks** — extract logic entirely |

These patterns were formalized by library authors (Radix UI, Headless UI, Downshift, React Table) to create components that are simultaneously powerful, flexible, and accessible.

---

## 3. Without vs. With Comparison (Compare)

### Without patterns — Props explosion

```typescript
// 15+ props — hard to maintain, impossible to extend
interface DropdownProps {
  isOpen: boolean;
  onToggle: () => void;
  buttonLabel: string;
  buttonClassName?: string;
  menuClassName?: string;
  items: { label: string; onClick: () => void }[];
  showIcons?: boolean;
  iconPosition?: "left" | "right";
  closeOnSelect?: boolean;
  disabled?: boolean;
  // ... and growing
}
```

### With Compound Components pattern

```typescript
// Consumer has full control over structure and styling
<Dropdown>
  <Dropdown.Trigger className="custom-button">Menu</Dropdown.Trigger>
  <Dropdown.Content className="custom-menu">
    <Dropdown.Item onClick={handleProfile}>Profile</Dropdown.Item>
    <Dropdown.Separator />
    <Dropdown.Item onClick={handleLogout}>Logout</Dropdown.Item>
  </Dropdown.Content>
</Dropdown>
```

| Aspect | Props-based | Compound Components |
|---|---|---|
| Flexibility | Fixed structure | Consumer controls layout |
| Props count | 15+ and growing | 2-3 per sub-component |
| Reusability | Low — tightly coupled to design | High — structure is decoupled |
| Accessibility | Must handle internally | Can be composed with a11y utilities |

---

## 4. Common Use Cases

1. **Design systems** — Compound Components for `<Select>`, `<Accordion>`, `<Tabs>`, `<Dialog>`.
2. **Data tables** — Headless hooks (`useTable`) that provide sorting, filtering, and pagination logic without dictating markup.
3. **Form libraries** — Render Props (Formik) or Headless hooks (React Hook Form) for form state management.
4. **Navigation components** — Polymorphic components that render as `<a>`, `<button>`, or framework-specific `<Link>`.
5. **Tooltip and Popover** — Compound Components with positioning logic separated from rendering.

### When simpler approaches suffice

- Leaf components with fixed structure (e.g., a `<Badge>` or `<Avatar>`).
- Internal admin tools where component reuse across projects is unlikely.
- Prototypes where speed of development outweighs long-term flexibility.

---

## 5. Deep Practice

### Pattern 1: Compound Components

Uses React Context for implicit parent-child communication.

```typescript
import { createContext, useContext, useState, type ReactNode } from "react";

// Internal shared state
interface ToggleContextType {
  on: boolean;
  toggle: () => void;
}

const ToggleContext = createContext<ToggleContextType | null>(null);

function useToggleContext(): ToggleContextType {
  const context = useContext(ToggleContext);
  if (!context) {
    throw new Error("Toggle compound components must be used within <Toggle>");
  }
  return context;
}

// Parent
export function Toggle({ children }: { children: ReactNode }) {
  const [on, setOn] = useState(false);
  const toggle = () => setOn((prev) => !prev);

  return (
    <ToggleContext.Provider value={{ on, toggle }}>
      {children}
    </ToggleContext.Provider>
  );
}

// Sub-components
Toggle.On = function ToggleOn({ children }: { children: ReactNode }) {
  const { on } = useToggleContext();
  return on ? <>{children}</> : null;
};

Toggle.Off = function ToggleOff({ children }: { children: ReactNode }) {
  const { on } = useToggleContext();
  return on ? null : <>{children}</>;
};

Toggle.Button = function ToggleButton() {
  const { on, toggle } = useToggleContext();
  return (
    <button onClick={toggle} aria-pressed={on}>
      {on ? "ON" : "OFF"}
    </button>
  );
};

// Usage — consumer controls the layout
// <Toggle>
//   <Toggle.On>The switch is on!</Toggle.On>
//   <Toggle.Button />
//   <Toggle.Off>The switch is off.</Toggle.Off>
// </Toggle>
```

### Pattern 2: Headless Components (Custom Hooks)

The modern standard. The hook owns 100% of the logic, state, and accessibility attributes. The consumer owns 100% of the rendering. Libraries like Radix UI, Downshift, and TanStack Table use this approach.

```typescript
import { useState, useCallback } from "react";

interface UseDropdownReturn {
  isOpen: boolean;
  toggle: () => void;
  getButtonProps: () => Record<string, unknown>;
  getMenuProps: () => Record<string, unknown>;
}

export function useDropdown(): UseDropdownReturn {
  const [isOpen, setIsOpen] = useState(false);
  const toggle = useCallback(() => setIsOpen((prev) => !prev), []);

  const getButtonProps = () => ({
    onClick: toggle,
    "aria-expanded": isOpen,
    "aria-haspopup": true as const,
  });

  const getMenuProps = () => ({
    role: "menu" as const,
    hidden: !isOpen,
  });

  return { isOpen, toggle, getButtonProps, getMenuProps };
}

// Usage — bind props to any element
// function MyDropdown() {
//   const { isOpen, getButtonProps, getMenuProps } = useDropdown();
//   return (
//     <div>
//       <button {...getButtonProps()}>Menu</button>
//       <ul {...getMenuProps()}>
//         <li role="menuitem">Profile</li>
//         <li role="menuitem">Logout</li>
//       </ul>
//     </div>
//   );
// }
```

### Pattern 3: Polymorphic Components

Enables a single component to render as different HTML elements or framework components while preserving type safety.

```typescript
import { type ElementType, type ComponentPropsWithoutRef } from "react";

type ButtonProps<E extends ElementType = "button"> = {
  as?: E;
  variant?: "primary" | "secondary" | "destructive";
} & ComponentPropsWithoutRef<E>;

export function Button<E extends ElementType = "button">({
  as,
  variant = "primary",
  className,
  ...rest
}: ButtonProps<E>) {
  const Component = as || "button";
  return <Component className={`btn btn-${variant} ${className ?? ""}`} {...rest} />;
}

// Usage:
// <Button onClick={handleClick}>Click me</Button>
// <Button as="a" href="https://example.com">Link styled as button</Button>
// <Button as={Link} to="/dashboard">React Router Link</Button>
```

### Best Practices

1. **Always validate Context usage** — Throw descriptive errors when compound sub-components are used outside their parent.
2. **Provide prop-getter functions** in headless hooks — `getButtonProps()`, `getInputProps()` encapsulate accessibility and event handling.
3. **Use `forwardRef`** when building library components that consumers may need to attach refs to.
4. **Prefer composition over configuration** — A component with 5 well-designed sub-components is better than one with 20 props.
5. **Document the "composition contract"** — Clearly state which sub-components are required vs. optional.

### Common Pitfalls

1. **Compound Components without Context validation** — Silent failures when sub-components are used outside the parent.
2. **Over-abstracting simple components** — A `<Badge>` does not need compound architecture.
3. **Render Props without memoization** — Inline render functions create new references on every render.
4. **Polymorphic types without constraints** — Missing `extends ElementType` makes the `as` prop accept anything.
5. **Missing accessibility attributes** — Headless components must provide ARIA attributes through prop getters.

### Production Checklist

- [ ] All compound sub-components throw clear errors when used outside their parent.
- [ ] Headless hooks return prop-getter functions with complete ARIA attributes.
- [ ] `forwardRef` applied to all components that may need external refs.
- [ ] Polymorphic components are fully type-safe (passing `href` to a `<button>` causes a compile error).
- [ ] All patterns documented with usage examples in Storybook.

---

## 6. Code Templates and Integration

### Compound Component Factory

```typescript
import { createContext, useContext, type ReactNode } from "react";

/**
 * Generic factory for creating compound component Context + Hook pairs.
 * Eliminates boilerplate for each new compound component.
 */
export function createCompoundContext<T>(componentName: string) {
  const Context = createContext<T | null>(null);

  function useCompoundContext(): T {
    const context = useContext(Context);
    if (!context) {
      throw new Error(
        `${componentName} compound components must be rendered within <${componentName}>.`
      );
    }
    return context;
  }

  return [Context.Provider, useCompoundContext] as const;
}

// Usage:
// const [AccordionProvider, useAccordionContext] = createCompoundContext<AccordionState>("Accordion");
```

---

## Related Topics

- [State Management Patterns](./state-management-patterns.md) — Choosing between Context, Zustand, Jotai, and Signals.
- [Performance Tuning](./performance-tuning.md) — Memoization strategies to prevent unnecessary re-renders in compound components.
- [Tailwind Mastery](../04-styling/tailwind-mastery.md) — CVA (Class Variance Authority) for variant-based component styling.
