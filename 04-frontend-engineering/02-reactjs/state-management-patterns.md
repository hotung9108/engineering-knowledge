# State Management Patterns

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Đi sâu vào các mô hình quản lý state hiện đại trong React. Bao gồm sự khác biệt quan trọng giữa Server State và Client State, đồng thời so sánh các kiến trúc: unidirectional (Redux/Zustand), atomic (Jotai/Recoil) và reactive signals.

</details>

> **Summary**: A deep dive into modern state management paradigms in React. Covers the critical distinction between Server State and Client State, and contrasts unidirectional architectures (Redux/Zustand), atomic models (Jotai/Recoil), and reactive signals.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang điều hành một nhà hàng:
- **Client State (Trạng thái nội bộ)**: Bàn số 5 thích ngồi ghế gỗ hay ghế đệm, quạt đang bật hay tắt. Đây là chuyện riêng của quán bạn (Zustand, Jotai). Thay đổi lập tức, ai cũng thấy ngay.
- **Server State (Trạng thái bên ngoài)**: Thực đơn mua nguyên liệu từ chợ. Chợ (API) có thể hết hàng, giá có thể đổi. Bạn cần cử người đi chợ (React Query), mua về cất tủ lạnh (Cache), và thỉnh thoảng phải gọi điện ra chợ hỏi xem giá có đổi không (Background Refetch).

Lỗi phổ biến nhất của lập trình viên là lấy thông tin đi chợ (Server State) cất chung vào sổ ghi chép nội bộ của quán (Redux/Zustand).

</details>

Imagine you are running a restaurant:
- **Client State (Internal Status)**: Does table 5 prefer wooden or padded chairs? Is the fan on or off? This is your restaurant's internal business (Zustand, Jotai). It changes instantly and locally.
- **Server State (External Status)**: The ingredients you buy from the market. The market (API) might run out of stock, or prices might change. You need to send someone to the market (React Query), store the food in the fridge (Cache), and occasionally call the market to check if prices have updated (Background Refetch).

The most common mistake developers make is writing down the market information (Server State) into the restaurant's internal notebook (Redux/Zustand).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**State Management** (Quản lý trạng thái) trong React ám chỉ các mẫu thiết kế và công cụ dùng để chia sẻ, đồng bộ và lưu trữ dữ liệu xuyên suốt các component. Quản lý trạng thái hiện đại chia làm 2 loại khác biệt hoàn toàn:
- **Server State**: Dữ liệu tải từ API — luôn luôn bất đồng bộ, có thể bị cũ (stale) và cần được lưu cache.
- **Client State**: Dữ liệu chỉ liên quan đến giao diện (theme, sidebar mở/đóng, form nháp) — đồng bộ, cục bộ và tạm thời.

**Phân loại:**
- **Loại**: Kiến trúc Frontend.
- **Hệ sinh thái**: React 18+ với TypeScript.
- **Công cụ chính**: React Query / TanStack Query (Server State), Zustand, Jotai, Redux Toolkit, MobX (Client State).

</details>

**State Management** in React refers to the patterns and tools used to share, synchronize, and persist application state across components. Modern state management distinguishes between two fundamentally different categories of state:

- **Server State**: Data fetched from external APIs — inherently asynchronous, cacheable, and potentially stale.
- **Client State**: UI-specific data (theme, sidebar open/closed, form drafts) — synchronous, local, and ephemeral.

### Classification
- **Type**: Frontend architecture pattern.
- **Ecosystem**: React 18+ with TypeScript.
- **Key tools**: React Query / TanStack Query (server state), Zustand, Jotai, Redux Toolkit, MobX (client state).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Các công cụ có sẵn của React (`useState`, `useReducer`, `useContext`) chỉ đủ dùng cho các Component nhỏ gọn. Nhưng khi ứng dụng lớn lên:
- **Gọi API**: `useEffect` + `useState` không tự động lưu cache, tự động gọi lại khi lỗi, hay gộp các request giống nhau. React Query làm được.
- **Share State toàn cục**: Nếu dùng `Context`, khi một giá trị đổi, TẤT CẢ các component bọc trong nó đều re-render. Zustand/Jotai cho phép chọn chính xác component nào cần re-render.
- **Code quá dài**: Redux quá cồng kềnh, Jotai/Zustand ra đời để giữ code ngắn gọn mà vẫn mạnh mẽ.

</details>

React's built-in state primitives (`useState`, `useReducer`, `useContext`) are sufficient for component-local and moderately shared state. However, they break down in these scenarios:

| Problem | Built-in limitation | External tool solution |
|---|---|---|
| API data caching, deduplication, refetching | `useEffect` + `useState` requires manual implementation | React Query handles caching, deduplication, and background refetching |
| Global UI state across distant components | Context triggers re-render of ALL consumers on any change | Zustand/Jotai allow selective subscription |
| Optimistic updates | Complex to implement manually | React Query's `onMutate` provides a first-class API |
| Complex state with many transitions | `useReducer` becomes unwieldy without middleware | Redux Toolkit provides middleware, DevTools, and slices |

> [!WARNING]
> The most common architectural mistake is placing Server State (API data) into a global client store (Redux, Zustand). Server data belongs in a dedicated caching layer (React Query, SWR, Apollo). Client stores should only hold UI-specific state.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có State Management: Bạn phải tự viết `useEffect` dài 15 dòng để gọi API, tự quản lý loading, error, biến `cancelled`. Nếu 3 nơi cùng gọi user đó, trình duyệt gửi đi 3 Request y hệt nhau.
Có React Query + Zustand: Chỉ tốn 5 dòng code. React Query tự động gộp 3 request làm 1, tự lưu cache, tự xử lý loading. Zustand quản lý Theme cực kỳ gọn gàng.

</details>

### Without proper state management

```typescript
// Manual fetching with useEffect — reinvents caching, deduplication, error handling
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchUser(userId)
      .then((data) => { if (!cancelled) setUser(data); })
      .catch((err) => { if (!cancelled) setError(err); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [userId]);

  // No caching, no deduplication, no background refetch, no optimistic updates
  // Every component that needs this user must duplicate this logic
}
```

### With React Query + Zustand

```typescript
// Server State — React Query handles everything
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorDisplay error={error} />;
  return <UserCard user={user} />;
}

// Client State — Zustand (minimal, selective re-renders)
const useUIStore = create<UIState>()((set) => ({
  sidebarOpen: false,
  theme: "dark" as const,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme: "light" | "dark") => set({ theme }),
}));

// Component only re-renders when 'theme' changes — not when sidebarOpen changes
function ThemeDisplay() {
  const theme = useUIStore((state) => state.theme);
  return <span>Current theme: {theme}</span>;
}
```

| Aspect | `useEffect` + `useState` | React Query + Zustand |
|---|---|---|
| Caching | None | Automatic with configurable staleness |
| Deduplication | None | Identical queries share a single request |
| Background refetch | None | On window focus, reconnect, interval |
| Re-render scope | Entire component tree via Context | Selective field-level subscriptions |
| DevTools | None | React Query DevTools + Zustand DevTools |
| Code volume | 15+ lines per fetch | 5 lines per query |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

| Tình huống | Công cụ khuyên dùng | Lý do |
|---|---|---|
| Dữ liệu API (CRUD, phân trang) | React Query / SWR | Thiết kế riêng cho Server State |
| Theme, sidebar, modal (Giao diện) | Zustand | Siêu nhẹ, chỉ re-render chỗ cần thiết |
| Trình chỉnh sửa ảnh, đồ thị | Jotai | Mô hình Atomic phù hợp dữ liệu tách rời độc lập |
| Dữ liệu real-time cực cao (Game, Trading) | MobX / Preact Signals | Phản ứng cực nhanh, bỏ qua so sánh Virtual DOM |
| Form phức tạp | React Hook Form | Chuyên quản lý validation form |
| Ứng dụng khổng lồ, logic rắc rối | Redux Toolkit | Rất nhiều Middleware và công cụ debug mạnh |

</details>

### Choosing the right tool

| Scenario | Recommended Tool | Reasoning |
|---|---|---|
| API data (CRUD, pagination, real-time) | React Query / SWR | Purpose-built for server state with caching |
| Theme, sidebar, modals, preferences | Zustand | Lightweight, selective re-renders |
| Canvas editors, interactive builders | Jotai | Atomic model fits graph-like independent state |
| High-frequency real-time data (trading, gaming) | MobX / Preact Signals | Fine-grained reactivity bypasses VDOM diffing |
| Form state | React Hook Form / Formik | Specialized for form validation lifecycle |
| Complex enterprise workflows | Redux Toolkit | Middleware, sagas, structured actions |

### When built-in React state is sufficient

- State used by only one component or its direct children (`useState`).
- Simple shared state that changes infrequently (`useContext` + `useReducer`).
- Fewer than 3 consumers of the shared state.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất**:
1. **Tách bạch Server và Client**: Không dùng Redux/Zustand để lưu dữ liệu API. Dùng React Query.
2. **Subscription chọn lọc**: Luôn dùng selector khi lấy state (ví dụ `useStore(state => state.theme)`). Nếu gọi trơn `useStore()`, component sẽ re-render MỌI LÚC khi bất kỳ giá trị nào trong store thay đổi.
3. **Colocate (Để gần nhau)**: State nào chỉ 1 component dùng thì cứ xài `useState`. Đừng ép mọi thứ lên Global Store.
4. **Dùng Middleware**: Zustand có `persist` để tự động lưu vào localStorage và `devtools` để xem state trên Redux Extension.

**Lỗi hay gặp**:
- Bọc toàn bộ App vào 1 file Context khổng lồ khiến ứng dụng giật lag vì re-render liên tục.
- Tổ chức state quá sâu (nested objects). Hãy làm phẳng dữ liệu.

</details>

### Zustand — Production Patterns

```typescript
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        isAuthenticated: false,
        login: (user) => set({ user, isAuthenticated: true }, false, "auth/login"),
        logout: () => set({ user: null, isAuthenticated: false }, false, "auth/logout"),
      }),
      { name: "auth-storage" } // Persists to localStorage
    ),
    { name: "AuthStore" } // Label in Redux DevTools
  )
);
```

### Jotai — Atomic State

```typescript
import { atom, useAtom } from "jotai";

// Independent atoms
const countAtom = atom(0);
const doubledAtom = atom((get) => get(countAtom) * 2); // Derived atom

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  return <button onClick={() => setCount((c) => c + 1)}>Count: {count}</button>;
}

function DoubledDisplay() {
  const [doubled] = useAtom(doubledAtom);
  // Only re-renders when countAtom changes — no other atoms affect this component
  return <span>Doubled: {doubled}</span>;
}
```

### Best Practices

1. **Separate server state from client state** — Use React Query for API data; use Zustand/Jotai for UI state.
2. **Use selective subscriptions** — `useStore((state) => state.field)` instead of `useStore()` to minimize re-renders.
3. **Colocate state** — Keep state as close to its consumers as possible; only lift to global when necessary.
4. **Use middleware for cross-cutting concerns** — Zustand's `devtools`, `persist`, and `immer` middleware.
5. **Normalize complex state** — Flatten nested objects; use ID-based lookups instead of deeply nested structures.

### Common Pitfalls

1. **Putting API data in Redux/Zustand** — Leads to manual cache invalidation, stale data, and excessive boilerplate.
2. **Context for frequently changing state** — Any Context value change re-renders ALL consumers, including those that only read unchanged fields.
3. **Subscribing to the entire store** — `useStore()` without a selector causes re-renders on every store change.
4. **Over-globalizing state** — State that is only used in one feature should remain local, not global.
5. **Missing DevTools integration** — Without DevTools, debugging global state mutations becomes extremely difficult.

### Production Checklist

- [ ] Server state managed exclusively by React Query / SWR (not in global stores).
- [ ] Client state uses selective subscriptions (no full-store subscriptions).
- [ ] Zustand/Jotai DevTools middleware enabled in development.
- [ ] No `useContext` for frequently changing values (use Zustand or Jotai instead).
- [ ] State normalization applied for entities with relationships (users, posts, comments).

---

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là kiến trúc tiêu chuẩn trong các dự án lớn:
1. `useUser` (React Query): Chỉ chịu trách nhiệm fetch, cache, và cập nhật API.
2. `useNotificationStore` (Zustand): Chỉ chịu trách nhiệm quản lý thông báo (UI State) đẩy lên góc màn hình. Hai thế giới này hoàn toàn tách biệt.

</details>

### React Query + Zustand Integration Template

```typescript
// api/queries/useUser.ts — Server State
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "../client";

export function useUser(userId: string) {
  return useQuery({
    queryKey: ["user", userId],
    queryFn: () => apiClient.get<User>(`/users/${userId}`).then((r) => r.data),
    staleTime: 5 * 60 * 1000,
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateUserInput) =>
      apiClient.patch<User>(`/users/${data.id}`, data).then((r) => r.data),

    onSuccess: (updatedUser) => {
      queryClient.setQueryData(["user", updatedUser.id], updatedUser);
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}

// stores/useNotificationStore.ts — Client State
import { create } from "zustand";

interface Notification {
  id: string;
  message: string;
  type: "success" | "error" | "info";
}

interface NotificationState {
  notifications: Notification[];
  add: (notification: Omit<Notification, "id">) => void;
  dismiss: (id: string) => void;
}

export const useNotificationStore = create<NotificationState>()((set) => ({
  notifications: [],
  add: (notification) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        { ...notification, id: crypto.randomUUID() },
      ],
    })),
  dismiss: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
}));
```

---

## Related Topics

- [Performance Tuning](./performance-tuning.md) — How state management choices affect re-render performance.
- [Advanced Component Patterns](./advanced-component-patterns.md) — Compound and Headless patterns that interact with state management.
- [API Layer Design](../05-frontend-architecture/api-layer-design.md) — Transport layer that feeds React Query.
