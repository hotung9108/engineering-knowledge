# Micro-frontends and Monorepos

> A comprehensive guide to scaling frontend codebases beyond a single application, covering Monorepo tooling (Turborepo, Nx), Micro-frontend architectures (Module Federation, build-time integration), and the trade-offs that determine when each approach is appropriate.

---

## 1. What is it? (What)

**Monorepos** and **Micro-frontends (MFE)** are organizational strategies for managing large-scale frontend codebases. They address different but related scaling problems:

- **Monorepo**: A single Git repository containing multiple applications and shared packages, managed by a build orchestrator (Turborepo, Nx).
- **Micro-frontend**: An architectural pattern where a single user-facing application is composed from independently developed, deployed, and maintained frontend applications.

### Classification
- **Type**: Frontend architecture / team scalability patterns.
- **Monorepo tools**: Turborepo (Vercel), Nx (Nrwl), pnpm Workspaces.
- **MFE tools**: Webpack Module Federation, Rspack, Single-SPA.

---

## 2. Why does it exist? (Why)

| Problem | Solution |
|---|---|
| Code duplication across repos | **Monorepo** — Shared packages (UI components, utilities, configs) |
| Cross-repo dependency management | **Monorepo** — Single lock file, atomic updates |
| Independent team deployment | **Micro-frontend** — Each team deploys their own app |
| Large team coordination bottleneck | **MFE** — Teams own vertical slices end-to-end |
| Build time scaling | **Monorepo + caching** — Only rebuild changed packages |

---

## 3. Without vs. With Comparison (Compare)

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

## 4. Common Use Cases

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

## 5. Deep Practice

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

## 6. Code Templates and Integration

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
