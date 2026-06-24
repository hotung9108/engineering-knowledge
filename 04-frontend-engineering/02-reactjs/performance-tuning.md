# React Performance Tuning (Advanced)

React khá nhanh, nhưng không có nghĩa là bạn code bừa bãi. Để tránh React bị chậm đi, bạn phải làm chủ vòng đời Render.

## 1. Khi nào React Re-render?
Một component sẽ re-render nếu 1 trong 3 điều kiện sau xảy ra:
1. `State` nội tại thay đổi.
2. `Context` mà nó subscribe thay đổi.
3. **Component cha của nó re-render.**

**Quy tắc:** Default của React là "Cha render -> Toàn bộ Con, Cháu render theo". React **không tự động** so sánh Props có thay đổi hay không!

---

## 2. Giải quyết Re-render thừa (Memoization)

### `React.memo`
Dùng để bọc component con. Component sẽ HỦY re-render nếu tất cả props truyền vào **giống y hệt lần trước (Shallow Equality)**.

```tsx
const Child = React.memo(({ title, onClick }) => {
  console.log("Rendered!");
  return <button onClick={onClick}>{title}</button>;
});
```

### Tại sao `React.memo` hay bị "phá vỡ"?
Do **Shallow Equality** của JavaScript. Khi Component Cha render, nó tạo ra object/function **mới** ở bộ nhớ.
`{ a: 1 } !== { a: 1 }` và `() => {} !== () => {}`.

Nếu bạn pass một Inline Function hoặc Object trực tiếp xuống Child, `React.memo` vô dụng!

### `useCallback` & `useMemo`
Để bảo vệ `React.memo`, ta cần đóng băng reference của function/object.
- `useCallback`: Trả về CÙNG MỘT function reference.
- `useMemo`: Trả về CÙNG MỘT value reference (object, array) hoặc dùng để tính toán nặng.

```tsx
// Sai:
// <Child user={{name: "A"}} onClick={() => doSomething()} />

// Đúng:
const user = useMemo(() => ({ name: "A" }), []);
const handleClick = useCallback(() => doSomething(), []);
// <Child user={user} onClick={handleClick} />
```

> [!CAUTION]
> **Tuyệt đối KHÔNG LẠM DỤNG useMemo/useCallback cho mọi thứ.** Bản thân các Hook này tốn RAM (để nhớ biến cũ) và tốn CPU (để so sánh Dependency Array). Chỉ dùng khi truyền vào component có `React.memo` hoặc làm Dependency cho `useEffect`.

---

## 3. Tối ưu qua Component Composition (Không dùng Memo)

Đây là kỹ thuật ĐỈNH CAO của Senior React: Tránh re-render bằng cách cấu trúc lại JSX.

**Vấn đề:** Component Cha có một state `color`. Mỗi lần đổi color, Cha render lại, kéo theo một component `ExpensiveTree` cực nặng render theo dù nó không liên quan đến color.

**Giải pháp: Đẩy state xuống (Push State Down) hoặc Kéo component lên (Lift Content Up).**

Kéo component lên qua `children` prop:
```tsx
function ColorPickerWrapper({ children }) {
  const [color, setColor] = useState("red");
  return (
    <div style={{ color }}>
      <button onClick={() => setColor("blue")}>Change Color</button>
      {/* children ở đây là JSX Element đã được TẠO RA từ trước bởi component bên ngoài. 
          Nên khi ColorPickerWrapper render lại, nó tái sử dụng children cũ -> Không bị re-render! */}
      {children} 
    </div>
  );
}

// Cách dùng
<ColorPickerWrapper>
  <ExpensiveTree /> 
</ColorPickerWrapper>
```

---

## 4. Code Splitting & Lazy Loading

- Không tải toàn bộ JS trong 1 file `bundle.js` khổng lồ.
- Dùng `React.lazy` và `Suspense` để cắt JS ra thành từng chunk nhỏ, tải khi người dùng chuyển trang hoặc mở modal.

```tsx
import { lazy, Suspense } from 'react';

const HeavyChartModal = lazy(() => import('./HeavyChartModal'));

// Chỉ tải HeavyChartModal.js qua network KHI isModalOpen = true
{isModalOpen && (
  <Suspense fallback={<Spinner />}>
    <HeavyChartModal />
  </Suspense>
)}
```

---

## 5. React Compiler (Tương lai)
Từ React 19, **React Compiler** (Forget) sẽ tự động chèn `useMemo` và `useCallback` ở level trình biên dịch. Bạn sẽ không cần viết memoization thủ công nữa! Cấu trúc Composition vẫn là quan trọng nhất.
