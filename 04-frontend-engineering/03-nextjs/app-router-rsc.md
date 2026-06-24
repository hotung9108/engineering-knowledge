# App Router & React Server Components (Advanced)

Next.js 13+ (App Router) mang đến một sự thay đổi kiến trúc khổng lồ cho Frontend với **React Server Components (RSC)**.

## 1. Khái niệm React Server Components (RSC)

Từ trước đến nay (Pages Router, Create React App), mọi component đều được render ở Browser (hoặc Hydrate từ HTML tĩnh).
Trong App Router, mặc định tất cả component là **Server Components**.

### Đặc điểm của Server Components (RSC)
- Render 100% trên Server (Node.js/Edge). Không bao giờ chạy trên Browser.
- Có thể kết nối trực tiếp DB (SQL, Prisma) ngay trong thân Component.
- **KHÔNG THỂ:** Dùng state (`useState`, `useReducer`), effects (`useEffect`), hay browser APIs (`window`, `localStorage`).
- **Ưu điểm cực lớn:** Bất kỳ thư viện JS nào import vào RSC đều KHÔNG lọt vào bundle gửi xuống Client -> Bundle size siêu nhẹ.

### Client Components (`"use client"`)
- Đây là các component quen thuộc có thể dùng State, Effect.
- Chữ `"use client"` không có nghĩa là nó *chỉ* render ở client. Nó vẫn được Pre-render (SSR) thành HTML trên Server giống y hệt Next.js cũ, sau đó mới Hydrate ở Client để tương tác.
- Nó ám chỉ ranh giới: "Từ file này trở xuống, mọi thứ gửi xuống Browser kèm JavaScript bundle".

---

## 2. Ranh giới Client - Server (Network Boundary)

Hiểu rõ quy luật truyền Props giữa RSC và Client Component là sống còn.

### ✅ Truyền từ Server xuống Client
Truyền String, Number, Boolean, Object đơn giản là bình thường. Tuy nhiên, bạn KHÔNG THỂ truyền Function (callbacks, event handlers) hay Class Instances từ Server xuống Client, vì hàm không thể serialize (chuyển thành JSON) qua mạng.

```tsx
// ServerComponent.tsx
import ClientChild from './ClientChild';

export default async function ServerComponent() {
  const data = await db.query('...'); // Lấy DB
  
  return (
    <ClientChild 
      data={data} // OK
      // onClick={() => console.log(data)} // LỖI CRITICAL: Cannot pass function
    />
  );
}
```

### ✅ Lồng Server Component BÊN TRONG Client Component
Rất nhiều người nghĩ: Đã `use client` thì con của nó bắt buộc là Client Component. Sẽ là sai lầm nếu import trực tiếp, nhưng **rất đúng** nếu truyền qua `children` (Composition pattern).

```tsx
// ClientWrapper.tsx
"use client";
export default function ClientWrapper({ children }) {
  const [open, setOpen] = useState(false);
  return <div onClick={() => setOpen(true)}>{children}</div>;
}

// Page.tsx (Server)
export default function Page() {
  return (
    <ClientWrapper>
      {/* HeavyServerComponent là Server Component 100%, 
          vẫn chạy trên Server và nhét kết quả vào giữa ClientWrapper! */}
      <HeavyServerComponent /> 
    </ClientWrapper>
  )
}
```

---

## 3. Server Actions (Đột phá Form Handling)

Đã xa rồi thời phải tự viết API route `/api/submit`, gọi `fetch`, quản lý `isLoading`, `isError`.

Server Actions cho phép gọi một hàm chạy trên Server trực tiếp từ Client component (hoặc form submit).

```tsx
// actions.ts (Bắt buộc "use server")
"use server";
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  await db.post.create({ title });
  
  // Tự động xoá cache và re-render lại UI mới nhất!
  revalidatePath('/posts'); 
}

// ClientComponent.tsx
"use client";
import { useFormStatus } from 'react-dom'; // Tích hợp sẵn trong React
import { createPost } from './actions';

export default function PostForm() {
  // useFormStatus tự động bắt trạng thái pending của Server Action bao ngoài nó
  return (
    <form action={createPost}>
      <input name="title" />
      <SubmitButton />
    </form>
  )
}

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>;
}
```
