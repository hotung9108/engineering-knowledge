# Micro-frontends and Monorepos

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hướng dẫn toàn diện về cách mở rộng (scale) codebase frontend vượt ra ngoài một ứng dụng đơn lẻ. Bao gồm các công cụ quản lý Monorepo (Turborepo, Nx), kiến trúc Micro-frontend (Module Federation, tích hợp lúc build-time), và những sự đánh đổi (trade-offs) để xác định khi nào mỗi cách tiếp cận là phù hợp.

</details>

> **Summary**: A comprehensive guide to scaling frontend codebases beyond a single application, covering Monorepo tooling (Turborepo, Nx), Micro-frontend architectures (Module Federation, build-time integration), and the trade-offs that determine when each approach is appropriate.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi công ty bạn làm 3 trang web khác nhau:
- **Nhiều Repos**: Mỗi trang web là một ngôi nhà riêng, xây tường rào kín mít. Bạn muốn mượn cái búa (Component Nút Bấm), bạn phải đóng gói cái búa, gửi bưu điện sang nhà kia (publish lên NPM). Cực kỳ mất thời gian.
- **Monorepo**: Cả 3 trang web được gom chung vào một khu chung cư. Cái búa được để ở sân sinh hoạt chung (thư mục `packages/ui`). Ai cần lấy xài luôn, không cần đóng gói gửi bưu điện.
- **Micro-frontend (MFE)**: Giống như một cái trung tâm thương mại lớn. Gian hàng giày (Team A), gian hàng áo (Team B) hoàn toàn độc lập, thuê nhân viên riêng, tự thay đổi trang trí bất kỳ lúc nào mà không cần hỏi ban quản lý. Người dùng đi dạo thì cứ tưởng đó là một tòa nhà duy nhất.

</details>

When your company is building 3 different websites:
- **Multiple Repos**: Each website is a separate house with a high fence. If you want to borrow a hammer (a Button component) from one house to another, you have to pack it in a box, mail it to the post office (publish to NPM), and have the other house receive it. Very time-consuming.
- **Monorepo**: All 3 websites are built inside a single apartment complex. The hammer is left in the shared courtyard (the `packages/ui` folder). Anyone who needs it just walks out and grabs it. No mailing required.
- **Micro-frontend (MFE)**: Like a large shopping mall. The shoe store (Team A) and the clothing store (Team B) are completely independent. They hire their own staff and can redecorate whenever they want without asking the mall manager. Users walking through just think it's one big seamless building.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Monorepos** và **Micro-frontends (MFE)** là các chiến lược tổ chức mã nguồn dành cho những dự án rất lớn. Chúng giải quyết các vấn đề khác nhau nhưng có liên quan mật thiết:
- **Monorepo**: Lưu toàn bộ mã nguồn của nhiều ứng dụng khác nhau vào chung MỘT kho lưu trữ (Git repository duy nhất). Dùng các công cụ (Turborepo, Nx) để quản lý việc chia sẻ code nội bộ.
- **Micro-frontend**: Một kiến trúc (architecture) mà trong đó, một ứng dụng lớn hiển thị tới người dùng thực chất được "lắp ghép" từ nhiều ứng dụng nhỏ độc lập với nhau (được phát triển và deploy bởi các team khác nhau).

**Phân loại:**
- **Loại**: Mẫu kiến trúc Frontend / Mở rộng nhóm (team scalability).
- **Công cụ Monorepo**: Turborepo (Vercel), Nx (Nrwl), pnpm Workspaces.
- **Công cụ MFE**: Webpack Module Federation, Rspack, Single-SPA.

</details>

**Monorepos** and **Micro-frontends (MFE)** are organizational strategies for managing large-scale frontend codebases. They address different but related scaling problems:

- **Monorepo**: A single Git repository containing multiple applications and shared packages, managed by a build orchestrator (Turborepo, Nx).
- **Micro-frontend**: An architectural pattern where a single user-facing application is composed from independently developed, deployed, and maintained frontend applications.

### Classification
- **Type**: Frontend architecture / team scalability patterns.
- **Monorepo tools**: Turborepo (Vercel), Nx (Nrwl), pnpm Workspaces.
- **MFE tools**: Webpack Module Federation, Rspack, Single-SPA.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi công ty phát triển từ 5 lập trình viên lên 50 lập trình viên:
- Nếu để chung 1 codebase, mọi người sẽ giẫm chân lên nhau. Đợi test và deploy mất cả ngày.
- Nếu tách ra nhiều repo nhỏ, việc dùng chung các nút bấm, màu sắc, hay thư viện nội bộ lại trở thành cơn ác mộng vì lúc nào cũng phải publish/cập nhật phiên bản trên NPM.

| Vấn đề | Giải pháp |
|---|---|
| Lặp code ở nhiều dự án | **Monorepo** — Tạo các package dùng chung (UI, utils, config) |
| Cập nhật phiên bản chéo | **Monorepo** — Dùng chung 1 lock file, cập nhật đồng loạt |
| Đợi team khác deploy | **Micro-frontend** — Mỗi team tự deploy phần của mình |
| 50 người cùng code 1 repo bị kẹt | **MFE** — Chia team quản lý theo từng tính năng dọc |
| Chạy Build quá chậm | **Monorepo + Caching** — Chỉ build những phần có thay đổi |

</details>

| Problem | Solution |
|---|---|
| Code duplication across repos | **Monorepo** — Shared packages (UI components, utilities, configs) |
| Cross-repo dependency management | **Monorepo** — Single lock file, atomic updates |
| Independent team deployment | **Micro-frontend** — Each team deploys their own app |
| Large team coordination bottleneck | **MFE** — Teams own vertical slices end-to-end |
| Build time scaling | **Monorepo + caching** — Only rebuild changed packages |

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu không có Monorepo: Bạn làm xong trang Admin, sếp bảo làm thêm trang User. Bạn phải copy toàn bộ thư mục components từ Admin sang User. Nửa năm sau, bạn sửa nút Bấm bên Admin, nhưng quên sửa bên User, làm 2 trang lệch nhau.
Nếu có Monorepo: Trang Admin, trang User, và thư mục Nút Bấm nằm chung. Bạn sửa Nút Bấm 1 lần, cả Admin và User lập tức tự động cập nhật.

</details>

### Without monorepo — Multiple repositories

```
repo-web-app/          → npm install (own node_modules)
repo-admin-app/        → npm install (duplicate dependencies)
repo-shared-ui/        → Published to npm, versioned separately
repo-shared-utils/     → Published to npm, versioned separately
```

Problem: Updating a shared UI component requires publishing to npm, incrementing versions in each consumer, and coordinating merges across 4 repositories.

### With monorepo (Turborepo)

```
my-monorepo/
├── apps/
│   ├── web/              # Next.js user-facing app
│   ├── admin/            # Vite admin dashboard
│   └── docs/             # Documentation site
├── packages/
│   ├── ui/               # Shared React components (Button, Input, Modal)
│   ├── config-eslint/    # Shared linting configuration
│   ├── config-typescript/ # Shared tsconfig
│   └── utils/            # Shared utility functions
├── package.json          # Workspace root
└── turbo.json            # Build orchestration
```

| Aspect | Multi-repo | Monorepo |
|---|---|---|
| Code sharing | Publish to npm registry | Direct workspace imports |
| Dependency updates | Per-repo, coordinated manually | Single PR, atomic |
| CI/CD | Independent pipelines per repo | Orchestrated with caching (only build changed) |
| Configuration sharing | Duplicated or published as packages | Shared directly |
| Onboarding | Clone multiple repos | Clone one repo |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Dùng Monorepo khi:**
1. Có một Design System nội bộ dùng chung cho nhiều trang web.
2. Viết Full-stack: Frontend và Backend nằm chung, share chung các kiểu dữ liệu (Typescript Interfaces).

**Dùng Micro-frontend khi:**
1. Công ty CỰC LỚN (trên 30 Dev Frontend), chia làm nhiều squad (ví dụ: Team Thanh Toán, Team Xem Phim, Team Cá Nhân).
2. Từng team muốn đẩy code lên server mà không phải chờ các team khác.

**Khi nào KHÔNG NÊN dùng MFE**:
- Nhóm dưới 15 người. MFE cực kỳ phức tạp, giải quyết lỗi xung đột React hay rò rỉ CSS giữa các MFE sẽ bào mòn sức lực của team nhỏ. Monorepo là quá đủ.

</details>

### Monorepo

1. **Design system + multiple apps** — Share UI components between web, admin, and marketing sites.
2. **Full-stack TypeScript** — Frontend and backend in one repo with shared types.
3. **Internal library development** — Iterate on libraries alongside consuming applications without publish cycles.

### Micro-frontends

1. **Large organizations (30+ frontend developers)** — Multiple squads owning vertical features.
2. **Gradual technology migration** — New features in React while legacy features remain in Angular.
3. **Independent deployment cadence** — Team A deploys daily; Team B deploys weekly.

### When NOT to use micro-frontends

- Teams smaller than 15-20 frontend developers.
- Applications with tightly coupled features that share significant state.
- Greenfield projects where a monorepo provides sufficient team autonomy.

> [!WARNING]
> Micro-frontends introduce extreme complexity (version conflicts, CSS leaks, shared state difficulty, testing overhead). Never adopt MFE unless team size and organizational structure genuinely require independent deployment.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Module Federation (Webpack)**:
Đây là phép màu của MFE. Nó cho phép Website A (Host) tải trực tiếp các đoạn code đang nằm trên server của Website B (Remote) NGAY LÚC ĐANG CHẠY (Runtime) trên trình duyệt.
Bạn không cần build lại Website A. Miễn là Website B deploy code mới, người dùng vào Website A sẽ thấy đoạn code mới đó.

**Kinh nghiệm thực tiễn**:
1. LUÔN LUÔN bắt đầu bằng Monorepo. Chỉ chuyển sang MFE khi tổ chức phình quá to và nghẽn cổ chai.
2. Khi cấu hình Module Federation, phải nhớ khóa phiên bản thư viện chung (`singleton: true`). Nếu không, người dùng tải về 2 bản React khác nhau cùng lúc, ứng dụng sẽ sập ngay lập tức.
3. Phân chia ranh giới MFE theo luồng nghiệp vụ (Ví dụ: Trang Checkout là 1 MFE), đừng phân chia theo UI (Thanh điều hướng Navbar là 1 MFE).

</details>

### Turborepo Configuration

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"]
    },
    "lint": {},
    "test": {
      "dependsOn": ["build"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Module Federation (Webpack 5)

Module Federation allows one application to load code from another application at runtime, enabling true independent deployment.

```javascript
// App A (Host) — webpack.config.js
const { ModuleFederationPlugin } = require("webpack").container;

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: "hostApp",
      remotes: {
        checkoutApp: "checkoutApp@https://checkout.example.com/remoteEntry.js",
      },
      shared: {
        react: { singleton: true, requiredVersion: "^18.0.0" },
        "react-dom": { singleton: true, requiredVersion: "^18.0.0" },
      },
    }),
  ],
};

// Loading remote component
const RemoteCheckout = React.lazy(() => import("checkoutApp/Checkout"));
```

```javascript
// App B (Remote: Checkout) — webpack.config.js
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: "checkoutApp",
      filename: "remoteEntry.js",
      exposes: {
        "./Checkout": "./src/Checkout",
      },
      shared: {
        react: { singleton: true, requiredVersion: "^18.0.0" },
        "react-dom": { singleton: true, requiredVersion: "^18.0.0" },
      },
    }),
  ],
};
```

### MFE Integration Approaches

| Approach | Isolation | Deploy independence | Complexity | Performance |
|---|---|---|---|---|
| **Module Federation** | Medium | Full | High | Good (shared deps) |
| **Build-time NPM packages** | High | Requires host rebuild | Medium | Best |
| **Iframes** | Complete | Full | Low | Poor (heavy, slow) |
| **Nginx routing** | Complete | Full | Low | Full page reload |

### Best Practices

1. **Start with a monorepo; evolve to MFE only when needed** — Monorepo solves 90% of code sharing problems without MFE complexity.
2. **Use `pnpm` workspaces for monorepos** — Strict dependency isolation prevents phantom dependencies.
3. **Pin shared dependencies in Module Federation** — Use `singleton: true` and `requiredVersion` to prevent loading duplicate React.
4. **Define clear micro-frontend boundaries** — Each MFE should own a complete vertical feature, not a horizontal UI layer.
5. **Implement a shared design system as a package** — Not as a micro-frontend. UI components should be build-time dependencies.

### Common Pitfalls

1. **MFE for small teams** — The coordination overhead exceeds the benefit.
2. **CSS leaks between micro-frontends** — Styles from one MFE accidentally affect another. Use CSS Modules or Shadow DOM.
3. **Shared state across MFE boundaries** — Global state management across independently deployed apps is extremely fragile.
4. **Version conflicts in Module Federation** — Two MFEs requiring different React versions causes runtime crashes.
5. **No contract testing** — When MFE A depends on MFE B's exported component, breaking changes are only caught in production.

### Production Checklist

- [ ] Monorepo build caching configured (Turborepo Remote Caching or Nx Cloud).
- [ ] Shared packages (`ui`, `utils`, `config`) extracted and consumed via workspace imports.
- [ ] If using MFE: shared dependencies pinned with `singleton: true`.
- [ ] CSS isolation strategy documented and enforced (CSS Modules, Shadow DOM, or naming convention).
- [ ] Contract tests between micro-frontends (if applicable).

---

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là cấu hình cốt lõi nhất để tạo một Monorepo dùng `pnpm` workspace và `Turborepo`. `pnpm` giúp cài đặt thư viện chung cực kỳ nhanh mà không bị phình ổ cứng, còn Turborepo giúp chạy lệnh `build` trên toàn bộ dự án với tốc độ sấm sét bằng cách nhớ (cache) lại những thư mục không có sửa đổi.

</details>

### Monorepo Package.json Workspace Configuration

```json
// Root package.json (pnpm)
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "lint": "turbo lint",
    "test": "turbo test"
  },
  "devDependencies": {
    "turbo": "^2.0.0"
  }
}
```

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

---

## Related Topics

- [Vite vs Webpack Internals](../06-build-tools/vite-vs-webpack-internals.md) — Build tool internals relevant to Module Federation.
- [Frontend CI/CD & Deployment](../06-build-tools/frontend-ci-cd.md) — CI/CD pipelines for monorepos and micro-frontends.
- [CSS Architecture & Performance](../04-styling/css-architecture-performance.md) — CSS isolation strategies for multi-app architectures.
