# Vite vs Webpack Internals (Advanced)

Cả hai đều là Build Tools, nhưng triết lý hoạt động hoàn toàn trái ngược. Sự thống trị của Webpack đang dần bị Vite thay thế (nhất là với các project CSR/SPA).

## 1. Webpack (Bundle-based Development)

Webpack là một Bundler truyền thống.

### Cách hoạt động ở môi trường Dev
1. Quét từ `entry` (thường là `index.js`).
2. Giải quyết đồ thị phụ thuộc (Dependency Graph) qua hàng nghìn module.
3. Chạy qua các **Loaders** (Babel dịch JSX, Sass dịch ra CSS).
4. **Đóng gói toàn bộ (Bundle)** lại thành 1 file khổng lồ `main.js` và ném vào bộ nhớ (RAM).
5. Cuối cùng mới bật Local Server ở port 3000.

### Vấn đề:
Khi dự án phình to (hàng vạn file), Webpack Dev Server mất 20 giây - 2 phút mới khởi động xong. HMR (Hot Module Replacement) sửa 1 file mất 5 giây mới update. Càng to càng chậm.

---

## 2. Vite (Native ESM-based Development)

Tác giả Evan You (tạo ra VueJS) đẻ ra Vite để giải quyết tốc độ Dev. Triết lý: **Không đóng gói (No Bundling) ở Dev Environment**.

### Cách hoạt động ở Dev
1. Khởi động Web Server lập tức (trong 100ms).
2. Dùng tính năng **Native ESM** (`<script type="module">`) của trình duyệt hiện đại.
3. Khi trình duyệt load trang, nó thấy lệnh `import App from './App.tsx'`, nó tự request thẳng file đó qua mạng nội bộ.
4. Vite server nhận được request, "dịch nóng" file `App.tsx` bằng `esbuild` (được viết bằng Go, nhanh hơn Babel 10-100 lần) và trả về.

=> **Chỉ dịch những file trình duyệt đang thật sự yêu cầu.** Tốc độ Dev siêu tốc bất chấp dự án có lớn bao nhiêu.

### Pre-bundling Dependencies
Các thư viện trong `node_modules` thường xài CommonJS (`require()`), mà trình duyệt thì không hiểu CommonJS, chỉ hiểu ESM (`import`).
Nên trong lần khởi động Vite đầu tiên, nó dùng `esbuild` gom tất cả `node_modules` (như `react`, `lodash`) thành dạng ESM và lưu vào cache (`.vite/deps`). Quá trình này siêu nhanh và giải quyết được vấn đề CommonJS.

---

## 3. Quá trình Build (Production)

Đừng nhầm lẫn! Vite KHÔNG dùng `esbuild` để build ra Production (chỉ dùng ở Dev).

- Ở Production, Vite sử dụng **Rollup**.
- Tại sao? Vì `esbuild` cực kỳ nhanh nhưng tính năng tối ưu hoá (Tree-shaking, Code-splitting) của nó chưa linh hoạt và mạnh mẽ bằng Rollup (hoặc Webpack).
- Webpack ở Production vẫn là ông vua tuỳ chỉnh. Nếu bạn làm các dự án yêu cầu Loader cực kỳ dị, hoặc làm Micro-frontends (Module Federation thuần thục), Webpack vẫn mạnh mẽ hơn Vite. Tuy nhiên, Vite (hiện có plugin vite-plugin-federation) đang bám đuổi rất sát.

---

## 4. Tối ưu hoá Bundle Size

Cho dù dùng Vite hay Webpack, kĩ năng tối ưu Bundle Size là bắt buộc.

1. **Tree Shaking:** Công cụ build tự động xoá những đoạn code (functions, variables) bạn viết nhưng không bao giờ xài tới. (Lưu ý: Bạn phải viết code kiểu ESM `import { x }` để Tree Shaking hoạt động tối đa).
2. **Code Splitting (Dynamic Imports):** Cắt bundle lớn thành các file `chunk` nhỏ hơn bằng `import('...')` hoặc React `lazy`. Trình duyệt sẽ chỉ tải chunk cần thiết.
3. **Analyze Bundle:** Dùng công cụ `webpack-bundle-analyzer` hoặc `rollup-plugin-visualizer` để thấy "Biểu đồ bong bóng", tìm ra thư viện nào (như `moment.js`) đang làm phình to ứng dụng và thay thế (bằng `date-fns` hay `dayjs`).
