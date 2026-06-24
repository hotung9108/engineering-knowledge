# State Management Patterns (Advanced)

Trong React hiện đại, Redux không còn là lựa chọn mặc định duy nhất. Việc chọn đúng tool quản lý state quyết định kiến trúc và hiệu năng của toàn bộ app.

## Phân loại Global State

1. **Server State:** Dữ liệu từ API (Cache, Pagination, Deduping).
2. **Client State:** Dữ liệu UI (Theme, Sidebar open, Form data, Drafts).

> [!WARNING]
> Sai lầm lớn nhất là nhét Server State vào Redux/Zustand. **Hãy dùng React Query (TanStack Query) hoặc SWR cho Server State.** Chỉ dùng Global Store cho Client State.

---

## 1. Context API + `useReducer`

Dành cho state nhỏ, ít thay đổi (VD: Theme, Auth User).
- **Điểm yếu:** Bất kỳ thay đổi nào trong Context sẽ làm **TOÀN BỘ** components tiêu thụ Context đó bị re-render, kể cả khi component chỉ cần 1 property nhỏ trong obj.
- **Khắc phục:** Phải chẻ nhỏ Context (1 cho state, 1 cho dispatch function) và bọc component bằng `React.memo`.

---

## 2. Các trường phái Global State Management

### A. Flux/Redux Pattern (Redux Toolkit, Zustand)
State là Single Source of Truth (Một object khổng lồ duy nhất). Data flow một chiều.

**Zustand:**
Vua của Client State Management hiện nay.
- Không cần `<Provider>` bọc quanh App.
- API cực kỳ ngắn gọn.
- **Render Optimization:** Cho phép select đúng một mảnh data. Component sẽ KHÔNG re-render nếu mảnh data đó không đổi.

```typescript
// Zustand Store
import { create } from 'zustand'

const useBearStore = create((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
}))

// Trong component
const bears = useBearStore((state) => state.bears) // Chỉ re-render khi `bears` thay đổi
```

### B. Atomic Pattern (Jotai, Recoil)
State được chia thành vô số các hạt cơ bản (Atoms).
- Phù hợp với các app cần state linh hoạt, dạng đồ thị, tạo xóa state động (như Figma, Excalidraw, Excel grid).
- Tối ưu re-render ở mức tuyệt đối (chỉ component dính đến Atom đó mới render).

```typescript
// Jotai
import { atom, useAtom } from 'jotai'

const countAtom = atom(0)

function Counter() {
  const [count, setCount] = useAtom(countAtom)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

### C. Signals Pattern (Preact Signals, MobX)
Mô hình "Reactive" mượn từ Vue/SolidJS.
- **Đặc biệt:** Khi state thay đổi, UI tự update TRỰC TIẾP bỏ qua React Diffing. Không hề xảy ra Component Render Phase (Vượt qua VDOM).
- Hiệu năng cực kỳ khủng khiếp cho các app thay đổi liên tục (như theo dõi chứng khoán, game).

---

## Kết luận chọn Tool
- **Server Cache / API Data:** React Query, SWR, Apollo GraphQL.
- **App phổ thông, E-commerce, Dashboard:** Zustand.
- **Canvas app, Interactive Builder (Figma clone):** Jotai.
- **Cực kỳ nhiều Data Realtime / Web3:** Signals / MobX.
