# Advanced Component Patterns

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hướng dẫn toàn diện về cách xây dựng các React component có khả năng tái sử dụng cao, linh hoạt và dễ mở rộng bằng cách sử dụng các design pattern nâng cao như Compound Components, Render Props, Headless Components (thông qua Hooks) và Polymorphic Components.

</details>

> **Summary**: A comprehensive guide to building highly reusable, flexible, and scalable React components using advanced design patterns like Compound Components, Render Props, Headless Components (Hooks), and Polymorphic Components.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi bạn mua một chiếc bánh sinh nhật:
- **Component bình thường (Nhận quá nhiều Props)**: Giống như bạn gọi điện báo tiệm bánh: "Làm bánh socola, đường kính 20cm, vẽ hoa cúc, nến số 5, giao lúc 8h". Bạn phải truyền 100 thông tin (props). Nếu bạn muốn đổi hoa cúc thành hoa hồng, tiệm bánh báo: "Không được, code chúng tôi cứng nhắc rồi".
- **Advanced Patterns**: Giống như bạn mua một cái "Bánh sinh nhật tự ghép". Tiệm bán riêng cốt bánh, kem, hoa, nến. (Headless / Compound). Tiệm lo phần chất lượng (Logic bánh), còn BẠN là người tự sắp xếp kem và nến theo đúng ý mình (Render UI). Bánh không bao giờ bị hỏng dù bạn cắm nến ở đâu.

</details>

When buying a birthday cake:
- **Normal Components (Prop Drilling)**: It's like calling a bakery: "Bake a chocolate cake, 20cm, draw daisies, put a number 5 candle, deliver at 8 PM". You pass 100 instructions (props). If you want roses instead of daisies, the bakery says, "Sorry, our code is hardcoded".
- **Advanced Patterns**: It's like buying a "DIY Cake Kit". The bakery sells the sponge, cream, flowers, and candles separately (Headless/Compound). The bakery handles the quality and physics (Logic), but YOU assemble the cream and candles exactly how you want (Rendering UI). The cake works perfectly no matter where you put the candles.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Advanced Component Patterns** là các kỹ thuật kiến trúc để thiết kế các React Component tối đa hóa khả năng tái sử dụng, tính linh hoạt và sự tách biệt mối quan tâm (separation of concerns). Chúng giải quyết sự mâu thuẫn cốt lõi giữa việc cung cấp một Component dùng được ngay (sensible defaults) và cho phép người dùng tùy biến sâu (customization).

**Phân loại:**
- **Loại**: Kiến trúc UI.
- **Framework**: React 18+ với TypeScript.
- **Các pattern chính**: Compound Components, Render Props, Headless UI (Custom Hooks), Polymorphic Components.

</details>

**Advanced Component Patterns** are architectural techniques for designing React components that maximize reusability, flexibility, and separation of concerns. They solve the fundamental tension between providing sensible defaults and allowing consumer customization.

### Classification
- **Type**: UI architecture patterns.
- **Framework**: React 18+ with TypeScript.
- **Key patterns**: Compound Components, Render Props, Headless UI (Custom Hooks), Polymorphic Components.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi các thư viện Component phình to, các thiết kế ngây ngô ban đầu sẽ gặp rào cản:
- **Bùng nổ Props**: Truyền 20+ props chỉ để đổi màu chữ. Giải quyết bằng: **Compound Components**.
- **Giao diện cứng nhắc**: Component tự ôm đồm việc render thẻ HTML. Giải quyết bằng: **Headless / Render Props** (Nhường quyền render cho người dùng).
- **Thiếu an toàn kiểu dữ liệu**: Dùng prop `as` nhưng TS không gợi ý được thuộc tính. Giải quyết bằng: **Polymorphic Components**.
- **Lặp code**: Logic giống hệt nhau ở nhiều Component. Giải quyết bằng: **Custom Hooks**.

</details>

As component libraries grow, naive designs hit scaling problems:

| Problem | Root Cause | Pattern Solution |
|---|---|---|
| Props explosion (20+ props) | All configuration via props | **Compound Components** — declarative child composition |
| Rigid UI that cannot be customized | Component owns the markup | **Render Props / Headless** — consumer controls rendering |
| `as` prop without type safety | Casting element types manually | **Polymorphic Components** — generic element type |
| Logic duplication across components | Business logic mixed with UI | **Custom Hooks** — extract logic entirely |

These patterns were formalized by library authors (Radix UI, Headless UI, Downshift, React Table) to create components that are simultaneously powerful, flexible, and accessible.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có pattern: Phải truyền hàng đống cấu hình vào component con thông qua props. Rất khó đọc.
Sử dụng Compound Component: Người dùng tự ghép thẻ `<Dropdown.Item>` vào `<Dropdown.Content>`, rõ ràng, linh hoạt, và thư viện không cần quan tâm người dùng đặt bao nhiêu mục.

</details>

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

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Design systems**: Dùng Compound Component cho `<Select>`, `<Accordion>`, `<Tabs>`, `<Dialog>`.
2. **Data tables**: Dùng Headless hooks (`useTable`) cung cấp logic sắp xếp, phân trang mà không ép buộc phải dùng thẻ `<table>`.
3. **Thư viện Form**: Dùng Render Props (Formik) hoặc Headless (React Hook Form) để quản lý state của Form.
4. **Tooltip / Popover**: Compound Component quản lý vị trí mở, tách biệt với việc vẽ giao diện.

**Khi nào KHÔNG nên dùng**: Các component quá nhỏ như `<Badge>`, `<Avatar>`. Code nguyên khối sẽ tốt hơn là over-engineer.

</details>

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

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Compound Components**: Sử dụng Context để truyền state ngầm xuống các component con. Nhờ đó người dùng có thể tự do thay đổi cấu trúc thẻ HTML.
**Headless Components (Custom Hooks)**: Đây là tiêu chuẩn hiện đại nhất. Hook nắm giữ 100% logic, state, và các thuộc tính Accessibility (ARIA). Nó trả về các hàm (prop getters) để người dùng tự gán vào thẻ HTML của họ.
**Polymorphic Components**: Giúp component có thể render dưới dạng các thẻ HTML khác nhau (ví dụ thẻ `<Button as="a">`) nhưng TypeScript vẫn biết cách báo lỗi nếu truyền sai thuộc tính.

</details>

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

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một hàm tiện ích (Factory function) giúp tạo nhanh cặp Context + Hook dùng chung cho mô hình Compound Component. Nó loại bỏ hoàn toàn các code thừa lặp đi lặp lại.

</details>

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
