# Next.js Caching & Data Fetching (Advanced)

Caching là "trái tim" và cũng là điểm gây bối rối nhất của Next.js App Router. Hiểu hệ thống Cache 4 tầng là điều bắt buộc.

## 1. Hệ thống 4 Tầng Cache (The 4 Caches)

Next.js tự động cache hầu như mọi thứ theo mặc định để đạt hiệu năng tối đa.

```mermaid
graph TD
    Client[Browser] -->|Request| RouterCache[1. Router Cache (Client-side)]
    RouterCache -- Không có --> FullRoute[2. Full Route Cache (Server-side HTML/RSC)]
    FullRoute -- Miss --> Memo[3. Request Memoization (Server-side API calls)]
    Memo -- Miss --> DataCache[4. Data Cache (Persistent Fetch Cache)]
    DataCache -- Miss --> DB[(Database / External API)]
```

### 1. Request Memoization (Tự động Deduping)
- **Hoạt động:** Nằm ở tầng React (Server). Nếu bạn gọi `fetch('https://api.com/data')` ở 5 component khác nhau trong CÙNG MỘT request render, Next.js thực chất chỉ gọi ra ngoài mạng ĐÚNG 1 LẦN.
- **Thời gian sống:** Bị hủy ngay khi Render xong request đó.
- **Tác dụng:** Cho phép fetch data ngay tại component cần dùng thay vì phải fetch ở layout rồi truyền props cồng kềnh.

### 2. Data Cache (Persistent Fetch Cache)
- **Hoạt động:** Nằm trên Server. Lưu trữ vĩnh viễn kết quả của các hàm `fetch()` (trừ khi bạn cấu hình khác). Đây chính là tính năng ISR (Incremental Static Regeneration) nổi tiếng.
- **Cấu hình Cache:**
  - `fetch(url, { cache: 'force-cache' })` (Mặc định).
  - `fetch(url, { cache: 'no-store' })` (Bỏ cache, tương đương SSR - Server Side Rendering).
  - `fetch(url, { next: { revalidate: 60 } })` (Cache 60 giây).

### 3. Full Route Cache (SSG - Static Site Generation)
- **Hoạt động:** Next.js render sẵn toàn bộ route thành HTML tĩnh lúc build time. Mỗi khi user request, server trả luôn HTML/RSC Payload tĩnh mà không cần chạy lại component.
- **Làm sao để tắt (Chuyển thành Dynamic Route):** Sử dụng các Dynamic Functions như `cookies()`, `headers()`, `searchParams` hoặc fetch không cache (`no-store`) sẽ ép route trở thành Dynamic (Render mỗi khi có request tới).

### 4. Router Cache (Client-side)
- **Hoạt động:** Khi user điều hướng bằng thẻ `<Link>`, Next.js cache lại payload của trang vừa vào ngay trên bộ nhớ trình duyệt (khoảng 30 giây đến 5 phút).
- **Lợi ích:** Bấm Back/Forward ngay lập tức mà không cần gọi network.

---

## 2. Revalidation (Xóa/Cập nhật Cache)

Khi dữ liệu trong DB thay đổi (Ví dụ: Thêm bài viết mới), bạn cần chủ động nói với Next.js xoá cache cũ đi. Việc này được gọi là **On-demand Revalidation**, thường được gọi bên trong Server Actions hoặc Route Handlers (Webhooks).

### Revalidate theo đường dẫn (Path)
Xóa tất cả bộ nhớ cache của một trang cụ thể.

```typescript
import { revalidatePath } from 'next/cache';

export async function createPost() {
  await db.insert(...);
  revalidatePath('/blog'); // Lần tới ai vào /blog cũng sẽ thấy bài mới
}
```

### Revalidate theo thẻ (Tag)
Mạnh mẽ hơn nhiều. Bạn có thể gắn tag cho từng lời gọi `fetch`, sau đó xóa hàng loạt fetch có cùng tag bất kể chúng nằm ở trang nào.

```typescript
// Gắn thẻ khi fetch
const res = await fetch('https://api.com/posts', { 
  next: { tags: ['posts'] } 
});

// Xoá thẻ khi cần (vd trong Server Action)
import { revalidateTag } from 'next/cache';

export async function updatePost() {
  await db.update(...);
  revalidateTag('posts'); // Mọi cache có tag 'posts' bị hủy
}
```

---

## 3. Streaming & Suspense

Thay vì bắt user phải chờ toàn bộ trang tải xong mới thấy giao diện (Waterfall rendering), Next.js sử dụng Streaming để trả dần HTML xuống trình duyệt.

Bọc component chậm (ví dụ gọi DB) vào `<Suspense>`.

```tsx
import { Suspense } from 'react';
import { Skeleton } from '@/components/ui/skeleton';

export default function Dashboard() {
  return (
    <section>
      <h1>Bảng điều khiển</h1>
      {/* UI chính hiện ngay lập tức, RevenueChart sẽ hiển thị Skeleton, 
          HTML của RevenueChart sẽ được stream thêm vào sau khi nó lấy data xong. */}
      <Suspense fallback={<Skeleton className="w-full h-40" />}>
        <RevenueChart />
      </Suspense>
    </section>
  )
}
```
