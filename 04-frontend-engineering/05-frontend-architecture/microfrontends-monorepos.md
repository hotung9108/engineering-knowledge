# Micro-frontends & Monorepos (Advanced)

Khi quy mô Frontend team lớn (hàng chục dev, nhiều squad khác nhau), kiến trúc truyền thống "1 repo khổng lồ" không còn hoạt động hiệu quả.

## 1. Monorepos

Monorepo là lưu trữ mã nguồn của **Nhiều Project** (Apps) và **Nhiều Packages** (Thư viện chia sẻ) trong cùng một Repository Git duy nhất.

### Lợi ích:
- Chia sẻ mã nguồn cực dễ (UI Components, Utility functions, API types).
- Tái sử dụng cấu hình (ESLint, TSConfig, Jest).
- Atomic commits (Sửa API ở backend và update frontend trong cùng một PR).

### Các công cụ hàng đầu:
1. **Turborepo (Vercel):** Nhẹ, siêu nhanh, tập trung mạnh vào Caching và song song hoá Tasks. Rất hợp cho hệ sinh thái Next.js/React.
2. **Nx (Nrwl):** Cực kỳ đồ sộ, có hệ thống plugins khổng lồ, hỗ trợ tạo code (generators) và build đồ thị dependencies. Thường dùng trong các Enterprise Angular/React thuần cực lớn.

### Kiến trúc tiêu biểu (Turborepo)
```
my-monorepo/
├─ apps/
│  ├─ web/           # Next.js User App
│  ├─ admin/         # Vite Admin Dashboard
│  └─ docs/          # Docusaurus
├─ packages/
│  ├─ ui/            # Shared React UI Components (Button, Input)
│  ├─ config-eslint/ # Shared linting rules
│  └─ utils/         # Math, Date helpers
└─ package.json      # Workspace root
```

---

## 2. Micro-frontends (MFE)

Micro-frontend là việc chia cắt một Frontend App nguyên khối thành nhiều App nhỏ biệt lập, do các team khác nhau tự build và deploy **độc lập**. Sau đó, chúng được ghép lại thành một trang duy nhất ở Browser.

Ví dụ: `Header` do Team Navigation quản lý, `Product Detail` do Team E-commerce quản lý. Cả hai chạy trên 2 URL riêng, nhưng user mở `example.com` thì thấy chúng hợp nhất.

### Module Federation (Webpack 5 / Rspack)
Đỉnh cao của MFE. Nó cho phép một app tải code của một app khác thông qua mạng tại **Runtime**.
Nó tự động giải quyết dependencies chung (Ví dụ cả 2 App đều dùng React 18, trình duyệt chỉ tải React 1 LẦN).

```javascript
// App A (Host - Người nhận)
new ModuleFederationPlugin({
  name: 'hostApp',
  remotes: {
    appB: 'appB@http://localhost:3001/remoteEntry.js',
  },
  shared: ['react', 'react-dom']
})

// Cách gọi:
const RemoteHeader = React.lazy(() => import('appB/Header'));
```

### Các cách thức ghép MFE khác:
- **Build-time integration:** Xuất thư viện qua NPM (Cách cổ điển, cần build lại Host mỗi khi Con update).
- **Iframes:** Cách biệt lập tuyệt đối nhất, nhưng giao tiếp khó (phải dùng `postMessage`) và chậm chạp.
- **Nginx Routing (Trá hình MFE):** Khi user vào `/products`, Nginx trỏ qua App A. Khi vào `/checkout`, Nginx trỏ qua App B. (Không phải MFE thật sự vì reload lại toàn bộ trang, nhưng rất dễ làm).

> [!WARNING]
> Micro-frontends mang lại độ phức tạp cực cao (Version conflict, CSS leak, Global State khó chia sẻ). **Không bao giờ dùng MFE** trừ khi team của bạn có hơn 30+ Frontend Devs và không thể làm việc chung trên cùng một codebase.
