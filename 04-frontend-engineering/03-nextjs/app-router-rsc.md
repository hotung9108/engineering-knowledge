# App Router and React Server Components

> A comprehensive guide to Next.js App Router architecture and React Server Components (RSC), covering the Server/Client component model, the Network Boundary, serialization rules, composition patterns, and Server Actions. This represents the most significant architectural shift in React since hooks.

---

## 1. What is it? (What)

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

## 2. Why does it exist? (Why)

The traditional React model sends the entire component tree as JavaScript to the browser, even for components that never need interactivity. This creates:

| Problem | RSC Solution |
|---|---|
| Large JavaScript bundles | Server Components send zero JS to the browser |
| Waterfall data fetching | Components fetch data directly on the server, co-located with their rendering |
| API boilerplate (`/api/` routes, `fetch`, loading states) | Server Actions call server functions directly from forms |
| Data prop drilling from page-level fetchers | Each component fetches its own data independently |
| Client-server type mismatch | Shared TypeScript types between Server Actions and components |

---

## 3. Without vs. With Comparison (Compare)

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

## 4. Common Use Cases

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

## 5. Deep Practice

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

## 6. Code Templates and Integration

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
