# Frontend CI/CD and Deployment Strategies

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hướng dẫn toàn diện về tự động hóa các khâu kiểm soát chất lượng frontend (CI) và triển khai ứng dụng frontend lên production (CD). Bao gồm các giai đoạn của pipeline CI, so sánh hosting qua CDN với container hóa (Docker), và các mô hình triển khai an toàn (Blue/Green, Canary, Feature Flags).

</details>

> **Summary**: A comprehensive guide to automating frontend quality gates (CI) and deploying frontend applications to production (CD), covering CI pipeline stages, CDN hosting vs. Docker containerization, and safe deployment patterns (Blue/Green, Canary, Feature Flags).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng việc xuất bản một cuốn sách:
- **Không có CI/CD**: Nhà văn viết xong bản thảo, tự mang ra nhà in, tự bê ra hiệu sách bán. Nếu có lỗi chính tả hoặc thiếu trang, khách hàng mua về mới phát hiện ra. Nhà văn phải lật đật chạy ra thu hồi lại từng cuốn sách. Rất thảm họa!
- **Có CI/CD**:
  - **CI (Kiểm duyệt - Continuous Integration)**: Trước khi in, có một cỗ máy tự động dò lỗi chính tả (Linting), tự động đọc thử xem cốt truyện có hợp lý không (Testing). Nếu máy báo lỗi, nhà văn bắt buộc phải sửa thì máy mới cho qua.
  - **CD (Phân phối - Continuous Deployment)**: Khi máy đã đóng dấu "Bản thảo hoàn hảo", một hệ thống tự động in sách và chở sách bày lên kệ của tất cả các hiệu sách trên toàn quốc trong vòng 5 phút. Nếu phát hiện lỗi ngoài ý muốn, hệ thống chỉ mất 1 click để thu hồi toàn bộ sách lỗi và bày sách cũ ra lại (Rollback).

</details>

Imagine publishing a book:
- **Without CI/CD**: The author finishes the manuscript, prints it themselves, and drives it to the bookstore to sell. If there are spelling mistakes or missing pages, customers only find out after they buy it. The author has to frantically recall all the books. Disastrous!
- **With CI/CD**:
  - **CI (Continuous Integration)**: Before printing, an automated machine checks for spelling errors (Linting) and test-reads to ensure the plot makes sense (Testing). If it finds an error, it rejects the manuscript until the author fixes it.
  - **CD (Continuous Deployment)**: Once the machine stamps "Perfect Manuscript", an automated system prints the books and places them on the shelves of every bookstore nationwide within 5 minutes. If an unexpected error occurs, the system takes 1 click to instantly recall the bad books and put the old ones back (Rollback).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Frontend CI/CD** là đường ống tự động hóa (pipeline) dùng để kiểm tra chất lượng code, đóng gói ứng dụng, và đẩy nó lên server mỗi khi lập trình viên gộp (merge) code mới.
- **CI (Continuous Integration)**: Các bước kiểm tra tự động chạy mỗi khi bạn tạo Pull Request — kiểm tra lỗi cú pháp (linting), lỗi kiểu dữ liệu (TypeScript), chạy test tự động.
- **CD (Continuous Deployment)**: Quá trình tự động ném các file đã build lên hạ tầng mạng (Vercel, AWS S3, Docker) để người dùng cuối có thể truy cập được.

**Phân loại:**
- **Loại**: Kỹ năng DevOps / Hạ tầng Frontend.
- **Công cụ CI**: GitHub Actions, GitLab CI, CircleCI.
- **Nền tảng CD**: Vercel, Cloudflare Pages, AWS S3 + CloudFront, Docker + Kubernetes.

</details>

**Frontend CI/CD** is the automated pipeline that validates code quality, builds production assets, and deploys them to infrastructure whenever code is merged.

- **CI (Continuous Integration)**: Automated checks that run on every Pull Request — linting, type checking, testing, and bundle analysis.
- **CD (Continuous Deployment)**: Automated delivery of built assets to production infrastructure — CDN, container registry, or edge network.

### Classification
- **Type**: DevOps / frontend infrastructure.
- **CI tools**: GitHub Actions, GitLab CI, CircleCI.
- **CD targets**: Vercel, Cloudflare Pages, AWS S3 + CloudFront, Docker + Kubernetes.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có CI/CD, việc đưa code lên mạng phụ thuộc vào con người: Lập trình viên chạy test trên máy cá nhân (hoặc quên không chạy), tự gõ lệnh build, rồi lấy file tải lên server bằng FTP. Cách làm này gây ra vô số vấn đề:

| Vấn đề | Giải pháp của CI/CD |
|---|---|
| Đẩy code lỗi lên mạng | **CI Blocks** — Chặn không cho gộp code nếu test báo đỏ |
| Tốc độ web bị chậm đột ngột do file quá nặng | **Bundle Size Budget** — Máy tự động đo dung lượng file, nếu vượt quá định mức sẽ báo lỗi |
| Gặp lỗi khi người dùng đang xài | **Deploy an toàn** — Dùng Canary Deploy (chỉ cho 5% user dùng thử) |
| Server sập do copy nhầm file | **Automated CD** — Máy tự động đẩy file lên server chính xác 100% |
| Muốn lùi lại phiên bản cũ mất cả buổi | **Rollback tự động** — Khôi phục bản cũ chỉ tốn 10 giây |

</details>

Without CI/CD, frontend deployments rely on manual processes: developers run tests locally (or skip them), build manually, and upload files via FTP or ad-hoc scripts. This leads to:

| Problem | CI/CD Solution |
|---|---|
| Untested code reaching production | **CI gates** block merging until all checks pass |
| Inconsistent builds | **Reproducible build environments** (Node version pinning, lock files) |
| Risky deployments | **Safe deployment patterns** (Canary, Blue/Green, rollback) |
| Performance regressions unnoticed | **Bundle size budgets** enforced automatically |
| Manual, error-prone deployment | **Automated CD** triggered on merge to main |

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có CI/CD: "Code chạy ngon trên máy em" -> Đẩy thẳng lên nhánh chính -> Không ai check lỗi -> Vỡ giao diện trên Production -> Sếp chửi.
Có CI/CD: Bạn tạo Pull Request -> GitHub Actions tự động chạy 500 bài test -> Test báo sai 1 chỗ -> Bạn bị khóa nút Merge -> Bạn phải sửa cho tới khi xanh hết mới được Merge. Yên tâm ngủ ngon!

</details>

### Without CI/CD

```
Developer: "Works on my machine" → pushes directly to main
→ No lint check → broken TypeScript types in production
→ No tests run → regression goes live
→ Manual FTP upload → partial upload fails → broken site for 5 minutes
→ No rollback plan → scramble to fix forward
```

### With CI/CD

```
Developer: Creates PR → CI pipeline runs automatically
→ ESLint + Prettier: catches formatting and logic issues
→ tsc --noEmit: catches type errors
→ Vitest: runs unit and integration tests
→ Playwright: runs E2E tests in headless browser
→ size-limit: verifies bundle size within budget
→ All pass → PR is mergeable
→ Merge to main → CD builds and deploys to Vercel/CDN
→ Canary deployment: 5% of users receive new version
→ Monitoring: if error rate spikes, automatic rollback
```

| Aspect | Without CI/CD | With CI/CD |
|---|---|---|
| Lint/Type errors | Caught in production (or never) | Caught before merge |
| Test coverage | Inconsistent, depends on developer | Enforced automatically |
| Bundle size | Unknown until user complains | Monitored with enforced budgets |
| Deployment | Manual, risky | Automated, safe, reversible |
| Rollback | Ad-hoc, stressful | One-click or automatic |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sản phẩm SaaS, Startup**: Pipeline chuẩn có test tự động (E2E), tự động ném code lên Vercel để chạy.
2. **Ứng dụng Doanh nghiệp / Ngân hàng**: Đóng gói Frontend thành các thùng container (Docker) và đẩy vào hệ thống máy chủ nội bộ (Kubernetes) để bảo mật tuyệt đối.
3. **Thư viện dùng chung (Design System)**: Code xong tự động đẩy lên trang npm nội bộ để các team khác tải về xài.

</details>

1. **SaaS products** — Full CI pipeline with E2E tests; CD to Vercel or Cloudflare Pages.
2. **Enterprise applications** — Docker containerization; deployment to internal Kubernetes clusters.
3. **Design system libraries** — CI validates component rendering; CD publishes to private npm registry.
4. **Marketing sites** — Static generation; CD to CDN with immutable asset caching.
5. **Mobile web apps** — Performance budgets enforced in CI; Lighthouse CI for automated audits.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Các bước tiêu chuẩn của một CI Pipeline**:
- **Lint và Format**: Chạy ESLint, Prettier xem có code sai chuẩn công ty không.
- **Type Checking**: Chạy TypeScript (`tsc`) để tìm lỗi khai báo biến.
- **Test tự động (Unit Test / E2E)**: Chạy Vitest hoặc Playwright (Mở trình duyệt ảo tự động click thử 100 lần).
- **Đo kích thước (Bundle Size)**: Chạy `size-limit`. Nếu file JS vượt qua 200KB thì đánh trượt!

**2. Các chiêu thức Deploy An Toàn (CD)**:
- **Canary Release (Chim Yến)**: Thợ mỏ xưa mang chim Yến xuống hầm, chim chết nghĩa là có khí độc. Trong IT, Canary deploy là bạn chỉ cho **5%** người dùng trải nghiệm bản web mới. 95% vẫn dùng bản cũ. Nếu 5% kia than lỗi hoặc hệ thống báo lỗi, tự động thu hồi ngay lập tức. Nếu ổn, tăng dần lên 20%, 50%, 100%.
- **Feature Flags**: Tính năng giỏ hàng mới đã đẩy lên code thực tế rồi, nhưng ẩn đằng sau một cái công tắc (Cờ). Sếp bảo bật công tắc thì tính năng mới hiện ra cho người dùng. Có lỗi, chỉ cần gạt công tắc TẮT là xong, không cần code lại hay đẩy code lại.

</details>

### Standard CI Pipeline Stages

1. **Lint and Format**: `eslint .` and `prettier --check .` — enforces code standards.
2. **Type Checking**: `tsc --noEmit` — catches type errors that IDE might miss.
3. **Unit and Integration Tests**: `vitest run` or `jest --ci` — tests utilities, hooks, and component rendering.
4. **End-to-End Tests**: `playwright test` — drives a headless browser through critical user flows.
5. **Bundle Size Check**: `size-limit` — fails the pipeline if bundle exceeds the configured budget.

### Deployment Strategy: CDN Hosting (Vercel, Cloudflare Pages)

Best for: SPAs, SSR/SSG applications (Next.js), and static sites.

- Built assets (HTML, CSS, JS) are deployed to globally distributed CDN edge nodes.
- Users download from the nearest edge location, minimizing latency.
- Edge Functions/Middleware run on edge servers for routing, redirects, and authentication checks.
- Rollback is instantaneous — revert to a previous deployment.

### Deployment Strategy: Docker Containerization

Best for: Enterprise environments, self-hosted infrastructure, Kubernetes deployments.

```dockerfile
# Multi-stage Dockerfile for React/Vite application
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Resulting image: ~15MB (static files + Nginx). Easily scalable via Kubernetes.

### Safe Deployment Patterns

1. **Blue/Green Deployment**: Two identical production environments. Green (new) is deployed and tested; the load balancer switches traffic from Blue (old) to Green. Rollback: switch back to Blue instantly.

2. **Canary Release**: Deploy the new version to 5% of users. Monitor error rates (Sentry), performance metrics, and user feedback. Gradually increase to 10%, 50%, 100%. Automatic rollback if error rate exceeds threshold.

3. **Feature Flags**: Code is deployed to production but hidden behind a flag (`ENABLE_NEW_DASHBOARD=false`). Enables "dark launching" — the code is live but inactive until the flag is toggled.

### Best Practices

1. **Pin Node.js version** — Use `.nvmrc` or `engines` in `package.json` to ensure reproducible builds.
2. **Use `npm ci` instead of `npm install` in CI** — Installs exact versions from lock file; faster and deterministic.
3. **Parallelize CI steps** — Run lint, type check, and unit tests concurrently.
4. **Cache `node_modules` and build output** — Dramatically reduces CI execution time.
5. **Run E2E tests against preview deployments** — Vercel and Cloudflare provide preview URLs for every PR.

### Common Pitfalls

1. **No lock file committed** — Causes non-deterministic installs across environments.
2. **E2E tests against localhost only** — Tests pass in CI but fail in production due to environment differences.
3. **No bundle size budget** — A single accidental large dependency import goes unnoticed.
4. **Manual deployment steps** — "Just upload to S3" invites human error and inconsistency.
5. **No rollback plan** — Every deployment must have a documented, tested rollback procedure.

### Production Checklist

- [ ] CI pipeline blocks merge on any failure (lint, types, tests, bundle size).
- [ ] Node.js version pinned via `.nvmrc`.
- [ ] `npm ci` used in CI (not `npm install`).
- [ ] Bundle size budget configured with `size-limit`.
- [ ] E2E tests run against preview deployment URLs.
- [ ] Deployment strategy documented (Canary, Blue/Green, or Feature Flags).
- [ ] Rollback procedure documented and tested.

---

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đoạn mã cấu hình tự động (CI) dùng GitHub Actions. Bạn thả đoạn code này vào thư mục dự án, GitHub sẽ tự động đọc và thực thi mọi công việc kiểm tra (Quality & E2E) mỗi khi có người đẩy code mới lên.

</details>

### GitHub Actions CI Pipeline

```yaml
# .github/workflows/ci.yml
name: Frontend CI

on:
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: ".nvmrc"
          cache: "npm"
      - run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type Check
        run: npx tsc --noEmit

      - name: Unit Tests
        run: npm run test -- --ci --coverage

      - name: Bundle Size
        run: npx size-limit

  e2e:
    runs-on: ubuntu-latest
    needs: quality
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: ".nvmrc"
          cache: "npm"
      - run: npm ci
      - run: npx playwright install --with-deps

      - name: E2E Tests
        run: npx playwright test
```

---

## Related Topics

- [Vite vs Webpack Internals](./vite-vs-webpack-internals.md) — Build tool configuration that feeds the CI/CD pipeline.
- [Micro-frontends & Monorepos](../05-frontend-architecture/microfrontends-monorepos.md) — CI/CD strategies for monorepos and multi-app deployments.
- [Web Performance & Core Web Vitals](../01-web-fundamentals/web-performance-vitals.md) — Performance budgets enforced through CI.
