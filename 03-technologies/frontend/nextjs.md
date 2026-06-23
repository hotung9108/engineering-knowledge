# Next.js

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Mặc dù React rất tuyệt vời, nhưng nó có một tử huyệt chí mạng: **Trắng trang lúc mới tải**. Trình duyệt phải tải 1 file JavaScript khổng lồ, chạy xong file đó thì chữ nghĩa mới hiện lên. Nếu Google Bot (con bọ tìm kiếm của Google) vào web của bạn, nó chỉ thấy 1 trang trắng bóc $\rightarrow$ Web của bạn sẽ không bao giờ xuất hiện trên trang 1 Google (Lỗi SEO). **Next.js** sinh ra để cứu React khỏi thảm họa này. Nó đứng trên Server, chạy React trước (Server-Side Rendering), tạo ra một file HTML CÓ SẴN CHỮ, và gửi về cho trình duyệt. Mở web ra là thấy ngay lập tức. Sau đó, file JS mới chạy ngầm để gắn các nút bấm vào (Hydration). 

</details>

> **Summary**: React is fundamentally a Client-Side Rendering (CSR) library. Its architectural flaw is that the initial HTML document is entirely blank (`<div id="root"></div>`). The browser must download, parse, and execute a massive JavaScript bundle before rendering the First Contentful Paint (FCP). This inherently destroys Search Engine Optimization (SEO) and massively degrades performance on slow mobile connections. **Next.js** is a Meta-Framework built *on top* of React. It introduces **Server-Side Rendering (SSR)** and **Static Site Generation (SSG)**. It executes the React components on a Node.js server, pre-renders a fully populated HTML string, and streams it to the client. The browser instantly displays the UI, followed by a background process ("Hydration") that attaches React's event listeners, perfectly marrying SEO-friendly static HTML with highly interactive Single Page Application (SPA) functionality.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đặt mua một bức tranh lắp ráp Lego.
1. **React thuần (CSR)**: Cửa hàng gửi cho bạn 1 cái thùng rỗng và 10.000 mảnh Lego (JS File). Bạn phải tự ngồi lắp ráp trong 5 phút. Trong 5 phút đó, ai bước vào phòng cũng chỉ thấy bạn đang bới đống gạch rác, không thấy bức tranh nào cả (Google Bot không thấy gì).
2. **Next.js (SSR)**: Cửa hàng (Máy chủ) thuê nhân viên lắp ráp sẵn 100% bức tranh tuyệt đẹp. Sau đó đóng thùng bức tranh đã hoàn thiện gửi cho bạn. Bạn mở hộp ra là CÓ THỂ NGẮM NGAY LẬP TỨC. Sau đó, Cửa hàng gửi thêm cho bạn 1 cái điều khiển từ xa (JS Hydration) để bạn làm cho các bánh xe trên bức tranh Lego tự động quay.

</details>

Imagine ordering a prefabricated House.
1. **Pure React (Client-Side Rendering)**: The construction company delivers 50,000 bricks, a cement mixer, and an instruction manual to your empty lot. You (the Browser) must physically build the house yourself. Until you finish 6 months later, you cannot live in it. (Slow initial load, terrible SEO).
2. **Next.js (Server-Side Rendering)**: The construction company builds the *entire* house in their factory (The Node.js Server). They load the finished house onto a massive truck, drive it to your lot, and drop it. You can walk inside immediately (Instant HTML/SEO). A few minutes later, the electrician hooks up the power grid (Hydration), and the light switches start working (Interactivity).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Next.js không thay thế React, nó BỌC lấy React và bổ sung thêm các "Siêu năng lực" mà React thuần không có:
1. **Rendering Strategies (Chiến lược Render)**: Hỗ trợ linh hoạt SSR (Render mỗi khi có người request), SSG (Render 1 lần duy nhất lúc Build, sau đó gửi file tĩnh), và ISR (Render tĩnh nhưng thỉnh thoảng tự động cập nhật ngầm).
2. **App Router (Định tuyến thông minh)**: Thay vì cài thư viện rườm rà như `react-router-dom`, trong Next.js, bạn chỉ cần tạo thư mục `app/dashboard/page.tsx` $\rightarrow$ Tự động có ngay đường link `congty.com/dashboard`.
3. **React Server Components (RSC)**: Khái niệm mới nhất. Cho phép bạn viết một Component React chạy ĐỘC QUYỀN trên Server. Nó có thể gọi thẳng vào Database bằng câu lệnh SQL mà không bao giờ lộ code xuống trình duyệt, giúp Web nhẹ đi cực kỳ nhiều.

</details>

Next.js is an opinionated, full-stack React framework (maintained by Vercel) that standardizes enterprise React architecture by providing out-of-the-box solutions for rendering, routing, and optimization:
1. **Hybrid Rendering Paradigm**: Unlike pure SPAs, Next.js allows developers to configure rendering behavior per-route. You can utilize SSG (Static Site Generation) for a marketing page, SSR (Server-Side Rendering) for a highly dynamic user dashboard, and ISR (Incremental Static Regeneration) for an E-commerce product catalog.
2. **File-System Based Routing (App Router)**: Eliminates the need for monolithic router configurations. The directory structure explicitly dictates the URL topology. Creating a file at `app/products/[id]/page.tsx` automatically provisions a dynamic route supporting `/products/123`.
3. **React Server Components (RSC)**: The paradigm shift of Next.js 13+. Components execute *exclusively* on the server and are never included in the Client JS bundle. This enables direct, secure backend access (e.g., executing raw SQL queries or reading file systems directly inside a React component) while radically reducing the downloaded JavaScript payload.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

React rất mạnh trong việc tạo Giao diện (UI). Nhưng để đem một trang React lên Production (Chạy thực tế cho hàng triệu khách hàng), bạn phải tự mình chắp vá hàng chục thư viện khác nhau:
- Webpack để nén code (Rất khó cấu hình).
- React-Router để chuyển trang.
- Đau đầu tìm cách làm SEO.
- Tự viết thêm 1 cục Backend NodeJS (Express) để lấy dữ liệu.
Next.js gom tất cả những thứ đau đầu đó vào 1 cục duy nhất. Nó là một Framework "Full-Stack". Bạn có thể viết Giao diện (Frontend) và viết cả API gọi Database (Backend) chung trong 1 dự án Next.js duy nhất. Bạn đẩy code lên Vercel, bấm 1 nút, thế là xong.

</details>

Configuring a raw React application (`create-react-app`) for enterprise-grade Production is an operational nightmare.
A production architecture demands Code Splitting, Route Prefetching, Image Optimization, Webpack/Babel tuning, a Routing engine, and crucially, an SEO-compliant Server-Side rendering pipeline. Engineering this manually requires months of infrastructure overhead.
Next.js exists to provide a "Batteries-Included", Zero-Configuration architecture. It abstracts the entire build pipeline (using Turbopack/Rust). Furthermore, it bridges the Frontend/Backend chasm. By providing API Routes (`app/api/route.ts`), Next.js acts as a true Full-Stack framework. A developer can build the UI and the Backend REST APIs within the exact same monorepo, sharing TypeScript interfaces seamlessly between Client and Server.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh luồng chạy khi Người dùng (hoặc Google Bot) vào trang Web.
</details>

Visualizing Initial Page Load (CSR vs SSR).

| Phase | React (Client-Side Rendering) | Next.js (Server-Side Rendering) |
|---|---|---|
| **1. Initial Request** | Browser requests `index.html`. | Browser requests `index.html`. |
| **2. Initial Response** | Server returns `<div id="root"></div>` (A completely blank page). | Server returns `<div id="root"><h1>Hello</h1></div>` (Fully visible content). |
| **3. Google Bot Result**| Bot sees a blank page. Ranks site as **#0 / Poor SEO**. | Bot reads the content perfectly. Ranks site as **#1 / Excellent SEO**. |
| **4. JS Download** | Browser downloads 2MB of JS. | Browser downloads 2MB of JS. |
| **5. Interactivity** | JS executes, fetches API, renders UI. (Total Time: 3s). | JS executes, attaches `onClick` events ("Hydration"). (Total Time: 0.5s visible, 3s interactive). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Trang Thương Mại Điện Tử (E-commerce - SSG/ISR)**: Website bán giày. Có 10.000 đôi giày. Không thể dùng React thuần vì mất SEO. Không thể dùng SSR (Render bằng Server mỗi khi có người vào) vì sẽ làm chết Server vào ngày Sale. Next.js dùng ISR: Máy chủ tự động tạo sẵn 10.000 file HTML tĩnh. Hàng triệu người vào mua đều load cực nhanh vì chỉ đang đọc HTML tĩnh. Cứ 60 giây nó tự cập nhật giá tiền 1 lần ngầm ở phía sau.
2. **Blog & Trang Tin tức (SEO-focused)**: Giống như trang E-commerce, các bài viết cần được Google index lập tức. Next.js là lựa chọn số 1.
3. **Ứng dụng Full-Stack siêu nhỏ**: Bạn muốn làm một cái Web tính lương nội bộ. Thay vì phải setup 1 source code Backend (Spring Boot) và 1 source code Frontend (React). Bạn dùng Next.js, viết cả API tính toán kết nối Database và Giao diện trong chung 1 nơi. Rất nhanh và rẻ.

</details>

1. **E-Commerce Platforms (ISR Paradigm)**: The ultimate battlefield for Next.js. An E-commerce site with 100,000 products demands flawless SEO and hyper-fast TTFB (Time to First Byte). Server-Side Rendering (SSR) every request during Black Friday will melt the database. Next.js solves this with **Incremental Static Regeneration (ISR)**. At build time, it generates 100,000 static HTML files. When a user visits, they receive the static HTML instantly (cached on a CDN). In the background, Next.js occasionally regenerates the page (e.g., every 60 seconds) to update prices and inventory, offering the performance of static sites with the freshness of dynamic servers.
2. **Content-Heavy Portals (News, Blogs)**: Any platform where inbound Organic Search Traffic (Google) is the primary revenue driver. The combination of pre-rendered HTML and Next.js's built-in `<Image />` optimization (which automatically resizes and converts images to WebP formats) guarantees elite Lighthouse performance scores.
3. **BFF (Backend-For-Frontend) Architectures**: Startups building MVPs bypass traditional Backend frameworks (Django/Spring). They utilize Next.js API Routes (Serverless Functions) to securely query the Database (Prisma/PostgreSQL) directly from the Next.js repository, rapidly accelerating Full-Stack delivery.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Phân biệt rạch ròi Server Component và Client Component**: Trong Next.js 13+, MỌI THỨ mặc định là Server Component (chạy trên máy chủ, không có `useState`, không bấm `onClick` được). Chỉ khi nào cục Component đó CÓ TƯƠNG TÁC (như Nút bấm, Ô nhập liệu), bạn mới được phép đặt chữ `"use client"` lên đầu file. Việc lạm dụng `"use client"` sẽ làm mất hoàn toàn sức mạnh của Next.js và biến nó thành React thuần.
2. **Sử dụng `<Image>` và `<Link>` của Next.js**: Tuyệt đối không dùng thẻ `<img>` và `<a>` của HTML thường. Next.js `<Image>` sẽ tự động bóp dung lượng ảnh từ 5MB xuống còn 50KB và tự động thêm Lazy Loading. Thẻ `<Link>` sẽ tự động tải trước (Prefetch) trang đích ngay khi bạn vừa rê chuột qua link, giúp bấm qua trang mới nhanh như chớp.

</details>

1. **Strictly Segregate Server & Client Components**: In the Next.js App Router paradigm, components are **React Server Components (RSC)** by default. They execute exclusively on Node.js, cannot use `useState` or `useEffect`, and cannot bind event listeners (`onClick`). They are perfect for reading databases securely. You MUST explicitly declare `"use client"` at the top of a file to opt-in to Client-Side interactivity. **Best Practice**: Push `"use client"` as far down the component tree as possible. Render the massive static Layout on the Server, and only make the interactive `<LikeButton />` a Client component.
2. **Leverage Framework Core Primitives (`<Image>` / `<Link>`)**: Never utilize standard HTML `<img>` tags. The `next/image` component executes automatic layout shift prevention, lazy loading, and on-the-fly WebP compression via an Edge CDN. Never utilize standard `<a href>` tags for internal routing. The `next/link` component executes background Prefetching; when a user hovers over the link, Next.js silently downloads the destination route's JSON in the background, making the subsequent click instantaneously resolve.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lộ API Keys (Bảo mật)**: Vì Next.js cho phép viết cả Frontend và Backend chung 1 dự án. Nhiều Junior Dev vô tình ném cái chìa khóa `STRIPE_API_KEY` (Thẻ tín dụng) vào trong một file `"use client"`. Hậu quả là toàn bộ chìa khóa bí mật bị phơi bày trên trình duyệt của người dùng. Hacker lấy được và công ty mất hàng triệu đô la.
   - *Luật*: Chìa khóa bảo mật phải nằm trong biến môi trường `.env`. Và chỉ những biến nào CỐ TÌNH có tiền tố `NEXT_PUBLIC_` mới được mang xuống Browser.
2. **Hiểu sai về Hydration Mismatch**: Next.js Render HTML ở Server, sau đó gửi xuống Trình duyệt, Trình duyệt chạy JS để Render lại 1 lần nữa (Hydration). Nếu HTML ở Server ghi là "10:00 AM", nhưng lúc JS chạy ở Trình duyệt nó tính giờ lệch thành "10:01 AM". Trình duyệt sẽ báo lỗi đỏ chót: `Text content did not match`. 
   - *Luật*: Đừng bao giờ render những dữ liệu ngẫu nhiên (như `Math.random()`, Thời gian hiện tại, hoặc dữ liệu lưu trong `localStorage`) ở lần render đầu tiên. Hãy bọc nó trong `useEffect` để ép nó chỉ chạy ở phía Client.

</details>

1. **Accidental Secrets Exposure (The Full-Stack Danger)**: Because Next.js blurs the line between Node.js execution and Browser execution, a junior developer might import a Database Connection String or a Stripe Secret Key directly into a UI Component. If that component accidentally resolves as a Client component, Webpack explicitly bundles the Secret Key into the public JavaScript file, resulting in a catastrophic security breach. **Rule**: Environment variables in `.env` are secure by default. Only variables explicitly prefixed with `NEXT_PUBLIC_` (e.g., `NEXT_PUBLIC_GA_ID`) are embedded into the client bundle.
2. **Hydration Mismatch Errors**: The most notoriously frustrating Next.js error. During SSR, the server generates an HTML string. Upon reaching the browser, React executes the component again to attach event listeners (Hydration). React expects the exact same HTML tree. If your component renders `window.innerWidth` or a localized `Date.now()`, the Server output will mathematically differ from the Browser output. React aggressively throws a `Hydration Mismatch` exception. **Fix**: Any logic relying on Browser-exclusive APIs (`window`, `localStorage`, `navigator`) must be deferred until *after* hydration by encapsulating it within a `useEffect` hook.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp các cơ chế cấu trúc và Fetch dữ liệu cực dị của Next.js (App Router).
</details>

### App Router Directory Structure
Next.js explicitly uses the file system to define Routes. Folders define the path, `page.tsx` defines the UI.

```text
app/
 ├── layout.tsx         # Global layout (HTML, Body tags, Navbar)
 ├── page.tsx           # Route: "/" (Homepage)
 ├── dashboard/
 │    └── page.tsx      # Route: "/dashboard"
 ├── blog/
 │    └── [slug]/
 │         └── page.tsx # Dynamic Route: "/blog/hello-world"
 └── api/
      └── users/
           └── route.ts # Backend API Endpoint: "/api/users"
```

### React Server Components (Data Fetching - SSR)
In Next.js 13+, components are Server Components by default. You can safely make direct DB calls or use `fetch` without `useEffect` or `useState`.

```tsx
// app/users/page.tsx
// Notice this is an async function! (Only works on Server Components)
export default async function UsersPage() {
  
  // This fetch executes securely on the Node.js Server.
  // Next.js automatically caches this fetch by default.
  const res = await fetch('https://api.example.com/users', { 
    cache: 'no-store' // Use 'no-store' to force SSR (Dynamic) instead of SSG (Static)
  });
  const users = await res.json();

  return (
    <ul>
      {users.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}
```

### Client Components (Interactivity)
When you need `onClick`, `useState`, or Browser APIs, you MUST explicitly opt-in.

```tsx
// app/components/LikeButton.tsx
"use client"; // CRITICAL: This directive tells Next.js to ship this JS to the browser

import { useState } from 'react';

export default function LikeButton() {
  const [likes, setLikes] = useState(0);

  // onClick requires Browser JavaScript. It will crash a Server Component.
  return <button onClick={() => setLikes(l => l + 1)}>Like {likes}</button>;
}
```

### Backend API Routes
Building a full REST API directly inside the Next.js project.

```typescript
// app/api/hello/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  return NextResponse.json({ message: 'Hello from Next.js Backend!' });
}

export async function POST(request: Request) {
  const body = await request.json();
  // ... save to database ...
  return NextResponse.json({ success: true, data: body }, { status: 201 });
}
```

---

## Related Topics

- Next.js is heavily reliant on **[React](./react.md)** fundamentals.
- Next.js supports writing Backend logic, replacing traditional **[Node.js / Express](../backend/nodejs-express.md)** for smaller apps.
- For deploying and scaling Next.js SSR functions, see **[AWS Serverless / Lambda](../cloud-infra/aws.md)**.
