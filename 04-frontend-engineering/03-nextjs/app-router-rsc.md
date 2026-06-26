# App Router and React Server Components

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hướng dẫn toàn diện về kiến trúc App Router của Next.js và React Server Components (RSC), bao gồm mô hình Server/Client component, Ranh giới Mạng (Network Boundary), quy tắc tuần tự hóa (serialization), các mẫu composition và Server Actions. Đây là bước chuyển mình về kiến trúc lớn nhất của React kể từ khi ra mắt hooks.

</details>

> **Summary**: A comprehensive guide to Next.js App Router architecture and React Server Components (RSC), covering the Server/Client component model, the Network Boundary, serialization rules, composition patterns, and Server Actions. This represents the most significant architectural shift in React since hooks.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang lắp ráp một chiếc ô tô:
- **Client Components (Mô hình cũ)**: Bạn gửi toàn bộ nhà máy, công nhân, linh kiện đến tận nhà khách hàng và lắp ráp ô tô ngay trong sân nhà họ. Rất nặng nề và mất thời gian (Gửi quá nhiều JavaScript xuống trình duyệt).
- **Server Components (Mô hình mới)**: Bạn lắp ráp xong khung xe, động cơ, bánh xe ngay tại nhà máy (Server), và chỉ gửi chiếc xe đã hoàn thiện đến nhà khách hàng (HTML tinh gọn).
Nhưng chiếc xe cần vô lăng và radio để khách hàng tương tác? Bạn gắn nhãn `"use client"` cho cái vô lăng. Vô lăng là thứ duy nhất được "lắp ráp" và chạy tại nhà khách hàng. Nhờ vậy, khách hàng nhận xe siêu nhanh mà vẫn lái được.

</details>

Imagine you are building a car:
- **Client Components (Old Model)**: You ship the entire factory, workers, and loose parts to the customer's driveway and build the car there. It's incredibly heavy and slow (sending too much JavaScript to the browser).
- **Server Components (New Model)**: You assemble the chassis, engine, and wheels at the factory (the Server). You ship the finished, pre-assembled car to the customer (pure HTML).
But the car needs a steering wheel and a radio for the customer to interact with? You attach a `"use client"` sticker to the steering wheel. The steering wheel is the only thing "assembled" and running at the customer's house. The customer gets the car instantly and can still drive it.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**React Server Components (RSC)** là một loại Component mới chỉ chạy trên Server (Node.js). Kết hợp với **Next.js App Router**, chúng tạo ra một mô hình mặc định: Mọi component đều render ở server để gửi HTML thuần xuống trình duyệt, trừ khi bạn khai báo `"use client"` để biến nó thành component tương tác trên trình duyệt (Client Component).

**Phân loại:**
- **Loại**: Kiến trúc render Full-stack.
- **Framework**: Next.js 13+ (App Router).
- **Thay thế**: Pages Router cũ (`getServerSideProps`, v.v...).

</details>

**React Server Components (RSC)** are a new component type that renders exclusively on the server (Node.js or Edge runtime). Combined with the **Next.js App Router** (introduced in Next.js 13), they establish a default-server rendering model where components are Server Components unless explicitly opted into client-side interactivity with `"use client"`.

### Classification
- **Type**: Full-stack rendering architecture.
- **Framework**: Next.js 13+ (App Router).
- **React version**: React 18+ with RSC support.
- **Replaces**: Pages Router (`getServerSideProps`, `getStaticProps`).

### Key Distinction

| Aspect | Server Components (default) | Client Components (`"use client"`) |
|---|---|---|
| Render location | Server only | Server (SSR/pre-render) + Client (hydration) |
| Can use `useState`/`useEffect` | No | Yes |
| Can access DB / filesystem directly | Yes | No |
| JavaScript sent to browser | None | Yes (included in bundle) |
| Can receive functions as props | N/A (they are the top) | Only from other Client Components |

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Mô hình React truyền thống gửi toàn bộ code JavaScript xuống trình duyệt, kể cả những phần giao diện tĩnh không bao giờ thay đổi. Việc này gây ra:
- File JS quá nặng, tải chậm.
- Hiện tượng "thác nước" (waterfall): Màn hình tải xong -> Chạy JS -> JS gọi API -> Đợi API trả về -> Mới hiện dữ liệu.
- Phải tạo hàng tá API Routes rác chỉ để Frontend có chỗ gọi vào.

App Router và RSC giải quyết triệt để: Server tự gọi Database, tự render ra HTML tĩnh, và không gửi giọt JS nào xuống trình duyệt.

</details>

The traditional React model sends the entire component tree as JavaScript to the browser, even for components that never need interactivity. This creates:

| Problem | RSC Solution |
|---|---|
| Large JavaScript bundles | Server Components send zero JS to the browser |
| Waterfall data fetching | Components fetch data directly on the server, co-located with their rendering |
| API boilerplate (`/api/` routes, `fetch`, loading states) | Server Actions call server functions directly from forms |
| Data prop drilling from page-level fetchers | Each component fetches its own data independently |
| Client-server type mismatch | Shared TypeScript types between Server Actions and components |

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có RSC (Pages Router): File `Dashboard` phải gọi cục dữ liệu khổng lồ ở trên cùng (`getServerSideProps`), sau đó truyền từ từ qua 10 component con (Prop Drilling).
Có RSC (App Router): Mỗi component con TỰ GỌI dữ liệu của riêng nó ngay trên Server. Cực kỳ dễ bảo trì và mở rộng.

</details>

### Without RSC (Pages Router)

```typescript
// pages/dashboard.tsx — All data fetched at page level, drilled down
export async function getServerSideProps() {
  const [user, stats, notifications] = await Promise.all([
    fetchUser(),
    fetchStats(),
    fetchNotifications(),
  ]);
  return { props: { user, stats, notifications } };
}

export default function Dashboard({ user, stats, notifications }) {
  // Must drill props to every child component
  return (
    <Layout user={user}>
      <StatsPanel stats={stats} />
      <NotificationList notifications={notifications} />
    </Layout>
  );
}
// Problem: Adding a new data dependency requires modifying getServerSideProps
// and threading props through potentially many intermediate components.
```

### With RSC (App Router)

```typescript
// app/dashboard/page.tsx — Server Component (default)
export default async function DashboardPage() {
  // No prop drilling — each component fetches its own data
  return (
    <Layout>
      <StatsPanel />
      <NotificationList />
    </Layout>
  );
}

// components/StatsPanel.tsx — Server Component fetching directly
export default async function StatsPanel() {
  const stats = await db.query("SELECT ... FROM stats");
  return <div>{stats.totalRevenue}</div>;
  // Zero JavaScript sent to the browser for this component
}
```

| Aspect | Pages Router | App Router (RSC) |
|---|---|---|
| Data fetching location | Page-level (`getServerSideProps`) | Co-located in each component |
| JS bundle impact | All components sent to client | Only `"use client"` components |
| Prop drilling | Required for child data | Eliminated |
| API route boilerplate | Manual `/api/` routes | Server Actions |
| Streaming | Not supported | Built-in with `<Suspense>` |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Trang Blog, Tài liệu, Landing Page**: 100% Server Components, siêu nhanh, không có JS thừa.
2. **Dashboard**: Khung viền và Data bằng Server Component. Chart/Biểu đồ bằng Client Component.
3. **Form đăng nhập / Gửi dữ liệu**: Dùng Server Actions, bảo mật tuyệt đối, bỏ qua bước tạo API Route.

**Chỉ dùng Client Component (`"use client"`) khi:**
- Cần xài `useState`, `useEffect`.
- Cần thao tác DOM, click, hover (Button, Modal, Tooltip).
- Xài thư viện ngoài chưa hỗ trợ RSC.

</details>

1. **Content-heavy pages** — Blog posts, documentation, marketing pages — 100% Server Components with zero client JS.
2. **Dashboard layouts** — Server Components for data fetching; Client Components only for interactive charts and filters.
3. **E-commerce product pages** — Server-rendered product details; client-side "Add to Cart" interactions.
4. **Form submission** — Server Actions replace custom API routes for mutations.
5. **Authentication flows** — Server-side session/cookie validation without exposing logic to the client.

### When Client Components are appropriate

- Any component using `useState`, `useEffect`, `useRef`, or browser APIs.
- Interactive elements: buttons with click handlers, modals, tooltips, dropdowns.
- Third-party client libraries (chart libraries, animation libraries).

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Ranh giới Mạng (Network Boundary)**: 
Từ Server Component truyền prop xuống Client Component giống như gửi gói hàng qua bưu điện. Bạn KHÔNG THỂ gửi một hàm (Function) qua bưu điện, bạn chỉ có thể gửi chữ, số, Object, Array, hoặc HTML (JSX).

**Thủ thuật nhúng Server vào Client**:
Đừng import trực tiếp Server Component vào bên trong Client Component (nó sẽ biến thành Client). Hãy truyền thông qua prop `children`.

</details>

### The Network Boundary

Understanding serialization rules between Server and Client Components is critical.

**Server → Client (allowed)**: Serializable values only — `string`, `number`, `boolean`, `null`, `Date`, plain objects, arrays, and JSX elements.

**Server → Client (NOT allowed)**: Functions, class instances, Symbols, and any non-serializable value.

```typescript
// ServerComponent.tsx (Server Component)
import ClientChild from "./ClientChild";

export default async function ServerComponent() {
  const data = await db.query("...");

  return (
    <ClientChild
      data={data}         // Serializable — OK
      // onClick={() => {}} // COMPILE ERROR: Functions cannot cross the network boundary
    />
  );
}
```

### Nesting Server Components Inside Client Components

A common misconception is that everything inside a `"use client"` component must be a Client Component. This is incorrect when using the `children` composition pattern.

```typescript
// ClientWrapper.tsx
"use client";
import { useState, type ReactNode } from "react";

export default function ClientWrapper({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return <div onClick={() => setOpen(!open)}>{children}</div>;
}

// Page.tsx (Server Component)
import ClientWrapper from "./ClientWrapper";
import HeavyServerComponent from "./HeavyServerComponent";

export default function Page() {
  return (
    <ClientWrapper>
      {/* HeavyServerComponent remains a Server Component.
          It renders on the server, and its output (JSX) is serialized
          and embedded inside ClientWrapper. Zero JS added to the bundle. */}
      <HeavyServerComponent />
    </ClientWrapper>
  );
}
```

### Server Actions

Server Actions allow calling server-side functions directly from Client Components or HTML forms, eliminating manual API route creation.

```typescript
// actions.ts
"use server";
import { revalidatePath } from "next/cache";

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string;
  await db.post.create({ data: { title } });
  revalidatePath("/posts"); // Invalidate cache — UI updates automatically
}

// PostForm.tsx
"use client";
import { useFormStatus } from "react-dom";
import { createPost } from "./actions";

export default function PostForm() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <SubmitButton />
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Saving..." : "Save"}
    </button>
  );
}
```

### Best Practices

1. **Default to Server Components** — Only add `"use client"` when interactivity is required.
2. **Push `"use client"` boundaries as far down the tree as possible** — Maximize server-rendered content.
3. **Use the `children` pattern** to nest Server Components inside Client Components.
4. **Co-locate data fetching** — Fetch data in the component that needs it, not at the page level.
5. **Use Server Actions for mutations** — Avoid creating custom API routes for form submissions and data mutations.

### Common Pitfalls

1. **Adding `"use client"` at the layout level** — Forces the entire subtree to be a Client Component, negating RSC benefits.
2. **Passing functions from Server to Client Components** — Functions are not serializable across the network boundary.
3. **Importing a Server Component inside a Client Component directly** — This silently converts it to a Client Component. Use the `children` pattern instead.
4. **Forgetting `"use server"` in Server Actions** — The function will execute on the client, potentially exposing sensitive logic.
5. **Over-relying on Client Components** — Many components that seem interactive (e.g., a formatted date) can remain Server Components.

### Production Checklist

- [ ] `"use client"` directives applied only at the lowest necessary component level.
- [ ] No functions passed as props from Server to Client Components.
- [ ] Server Actions used for all data mutations (no custom `/api/` routes for forms).
- [ ] `<Suspense>` boundaries wrapping all async Server Components for streaming.
- [ ] Database queries and sensitive logic confirmed to be in Server Components only.

---

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đoạn code dưới trình bày cách kết hợp Server Component và `<Suspense>`. Profile tải cực nhanh, còn Activity tải chậm hơn nên được gói vào Suspense để hiển thị bộ khung Skeleton tạm thời, giúp người dùng không phải chờ đợi.

</details>

### Server Component Data Fetching Template

```typescript
// app/users/[id]/page.tsx
import { notFound } from "next/navigation";
import { Suspense } from "react";
import { UserProfile } from "@/components/UserProfile";
import { UserActivity } from "@/components/UserActivity";
import { Skeleton } from "@/components/ui/Skeleton";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function UserPage({ params }: PageProps) {
  const { id } = await params;
  const user = await db.user.findUnique({ where: { id } });

  if (!user) notFound();

  return (
    <main>
      {/* Renders immediately with user data */}
      <UserProfile user={user} />

      {/* Streams in after activity data loads */}
      <Suspense fallback={<Skeleton className="h-40 w-full" />}>
        <UserActivity userId={id} />
      </Suspense>
    </main>
  );
}
```

---

## Related Topics

- [Caching & Data Fetching](./caching-and-data-fetching.md) — The 4-layer caching model that powers RSC data fetching.
- [React Fiber & Reconciliation](../02-reactjs/react-fiber-reconciliation.md) — How Fiber's architecture enables Suspense and streaming.
- [API Layer Design](../05-frontend-architecture/api-layer-design.md) — Client-side API patterns that complement Server Actions.
