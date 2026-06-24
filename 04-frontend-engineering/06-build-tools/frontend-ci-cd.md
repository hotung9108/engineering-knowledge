# Frontend CI/CD & Deployment Strategies (Advanced)

Dev Frontend không chỉ viết UI mà còn phải biết tự động hoá quá trình kiểm thử, build và đưa sản phẩm tới tay người dùng một cách an toàn nhất.

## 1. CI (Continuous Integration) cho Frontend

Khi một Dev tạo Pull Request (PR), hệ thống CI (GitHub Actions, GitLab CI) sẽ tự động chạy các bước kiểm tra mã nguồn.

### Các Job tiêu chuẩn trong Frontend CI Pipeline:
1. **Lint & Format:** Chạy `ESLint` và `Prettier`. Đảm bảo code sạch, đúng chuẩn team. Bất kỳ lỗi Syntax hay logic cơ bản nào đều làm rớt pipeline.
2. **Type Checking:** Chạy `tsc --noEmit`. TypeScript chỉ bắt lỗi ở Dev, nếu bạn vô tình push mã lỗi type lên, lệnh này sẽ chặn việc merge.
3. **Unit & Integration Testing:** Chạy `Vitest` hoặc `Jest`. Kiểm tra các hàm utils, custom hooks, và render thử components xem có crash không.
4. **E2E Testing (End-to-End):** Chạy `Playwright` hoặc `Cypress`. CI sẽ bật một con browser vô hình (headless) lướt qua trang web y như người dùng thật (Ví dụ: tự điền form Login -> Bấm nút -> Chờ toast "Success" hiện lên).
5. **Bundle Size Check:** Báo cáo xem PR này có lỡ tay thêm một thư viện nặng 5MB làm sập tốc độ tải trang hay không (Dùng `size-limit` hoặc `bundlesize`).

---

## 2. CD (Continuous Deployment)

Sau khi code được Merge vào nhánh chính (`main`), hệ thống CD sẽ đưa code lên Server (Production).

### Chiến lược 1: CDN Hosting (Vercel, Netlify, Cloudflare Pages)
- **Đặc điểm:** Tốt nhất cho SPA (React/Vite) hoặc SSG/SSR (Next.js).
- **Cách hoạt động:** Code được build thành HTML, CSS, JS tĩnh. Sau đó file tĩnh được đẩy lên các CDN Edge Node rải rác toàn cầu. User truy cập sẽ tải file từ node gần họ nhất (siêu nhanh).
- **Edge Computing:** Các API nhỏ hoặc Middleware (Redirect, Rewrite) chạy trên các server Edge cực nhẹ (Vercel Edge Functions, Cloudflare Workers), tăng tốc đáng kể.

### Chiến lược 2: Docker Container (Enterprise / Tự Host)
- **Đặc điểm:** Dùng khi công ty có hạ tầng riêng (AWS, K8s) hoặc vì lý do bảo mật dữ liệu.
- **Cách hoạt động:** 
  1. Viết `Dockerfile` thực hiện Multi-stage build.
  2. Giai đoạn 1 (Builder): Dùng image Node.js nặng để chạy `npm install` và `npm run build`.
  3. Giai đoạn 2 (Runner): Dùng một image siêu nhẹ (ví dụ `nginx:alpine`). Chỉ copy thư mục `/dist` từ giai đoạn 1 sang thư mục html của Nginx.
  4. Docker Image thu được chỉ khoảng ~15MB (chỉ chứa file HTML/JS tĩnh và Nginx). Cực kỳ an toàn và dễ dàng Scale bằng Kubernetes.

### Ví dụ Multi-stage Dockerfile cho Vite/React:
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy built static files
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 3. Deployment Patterns an toàn

- **Blue/Green Deployment:** Chạy 2 môi trường Production giống hệt nhau (Blue là bản cũ đang chạy, Green là bản mới vừa build). Sau khi Green test OK 100%, Load Balancer lập tức chuyển toàn bộ user từ Blue sang Green. Nếu có lỗi, switch ngược về Blue trong 1 giây.
- **Canary Release:** Triển khai bản mới cho 5% user bất kỳ dùng thử trước. Nâng dần lên 10%, 50%, 100% nếu không có lỗi crash (dựa trên Sentry bug report).
- **Feature Flags:** Code tính năng mới đã được Deploy lên Production, nhưng được ẩn bằng một cờ (ví dụ `ENABLE_NEW_DASHBOARD=false`). Chỉ có Dev team hoặc một nhóm user nhất định mới được trải nghiệm. Rất an toàn để "thử nghiệm trong bóng tối".
