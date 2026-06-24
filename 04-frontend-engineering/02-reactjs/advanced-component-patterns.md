# Advanced Component Patterns

Thiết kế Component tái sử dụng cao, linh hoạt mà không bị "phình to" props (Props Drilling / Props Explosion) là kỹ năng phân biệt Junior và Senior.

## 1. Compound Components Pattern

Pattern này cho phép cha và các con giao tiếp với nhau ngầm (qua Context) mà không cần truyền props rườm rà. Giúp developer có thể đảo thứ tự hiển thị UI linh hoạt.
Ví dụ kinh điển: `<select>` và `<option>`.

```tsx
import React, { createContext, useContext, useState } from 'react';

// 1. Tạo Context
const ToggleContext = createContext();

// 2. Component Cha
export function Toggle({ children }) {
  const [on, setOn] = useState(false);
  const toggle = () => setOn(!on);
  
  return (
    <ToggleContext.Provider value={{ on, toggle }}>
      {children}
    </ToggleContext.Provider>
  );
}

// 3. Các Components Con
Toggle.On = function ToggleOn({ children }) {
  const { on } = useContext(ToggleContext);
  return on ? children : null;
};

Toggle.Off = function ToggleOff({ children }) {
  const { on } = useContext(ToggleContext);
  return on ? null : children;
};

Toggle.Button = function ToggleButton() {
  const { on, toggle } = useContext(ToggleContext);
  return <button onClick={toggle}>{on ? 'Bật' : 'Tắt'}</button>;
};

// CÁCH SỬ DỤNG
// User có toàn quyền thay đổi vị trí Button, On, Off mà component vẫn hoạt động.
<Toggle>
  <Toggle.On>Đang bật nè!</Toggle.On>
  <Toggle.Button />
  <Toggle.Off>Đang tắt đó!</Toggle.Off>
</Toggle>
```

---

## 2. Render Props Pattern

Chia sẻ state/logic giữa các component nhưng nhường toàn bộ quyền Render UI cho component gọi nó.

```tsx
function WindowWidth({ children }) {
  const [width, setWidth] = useState(window.innerWidth);
  
  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Pass state vào hàm con (Render Prop)
  return children(width);
}

// CÁCH SỬ DỤNG
<WindowWidth>
  {(width) => (
    <div>
      {width > 800 ? <DesktopLayout /> : <MobileLayout />}
    </div>
  )}
</WindowWidth>
```

*(Hiện nay Render Props đã bị thay thế một phần lớn bởi Custom Hooks, nhưng vẫn hữu dụng trong một số thư viện như Formik hay React Router).*

---

## 3. Custom Hooks (Headless Component Pattern)

Đây là chuẩn mực hiện đại (Headless UI). Hook nắm giữ 100% logic, state, a11y (accessibility), và DOM event handlers. Việc render UI hoàn toàn nhường cho developer.
Các thư viện như `Radix UI`, `Downshift`, `React Table` dùng mô hình này.

```tsx
function useDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const toggle = () => setIsOpen(p => !p);

  // Getter cho các props chuẩn a11y
  const getButtonProps = () => ({
    onClick: toggle,
    'aria-expanded': isOpen,
    'aria-haspopup': true,
  });

  const getMenuProps = () => ({
    role: 'menu',
    hidden: !isOpen,
  });

  return { isOpen, getButtonProps, getMenuProps };
}

// CÁCH SỬ DỤNG: Gắn props vào thẻ tuỳ ý (button, div, a)
function MyDropdown() {
  const { isOpen, getButtonProps, getMenuProps } = useDropdown();
  
  return (
    <div>
      <button {...getButtonProps()}>Menu</button>
      <ul {...getMenuProps()}>
        <li>Profile</li>
        <li>Logout</li>
      </ul>
    </div>
  )
}
```

---

## 4. Polymorphic Components (As Prop Pattern)

Dùng khi bạn muốn build một UI Kit (Design System) mạnh mẽ, ví dụ một `Button` component nhưng khi render ra DOM có thể là `<button>`, `<a>`, hoặc `Link` của Next.js tuỳ mục đích SEO.

```tsx
import React from 'react';

// Polymorphic Type (Nâng cao)
type ButtonProps<E extends React.ElementType> = {
  as?: E;
  variant?: 'primary' | 'secondary';
} & React.ComponentPropsWithoutRef<E>;

export function Button<E extends React.ElementType = 'button'>({ 
  as, 
  variant = 'primary', 
  ...rest 
}: ButtonProps<E>) {
  const Component = as || 'button';
  
  return <Component className={`btn-${variant}`} {...rest} />;
}

// CÁCH DÙNG:
// Default là button
<Button onClick={...}>Click me</Button> 

// Trở thành thẻ <a> (Typescript sẽ check href)
<Button as="a" href="https://google.com">Link</Button> 
```
