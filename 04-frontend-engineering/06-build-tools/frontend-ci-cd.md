# Frontend CI/CD and Deployment Strategies

> A comprehensive guide to automating frontend quality gates (CI) and deploying frontend applications to production (CD), covering CI pipeline stages, CDN hosting vs. Docker containerization, and safe deployment patterns (Blue/Green, Canary, Feature Flags).

---

## 1. What is it? (What)

**Frontend CI/CD** is the automated pipeline that validates code quality, builds production assets, and deploys them to infrastructure whenever code is merged.

- **CI (Continuous Integration)**: Automated checks that run on every Pull Request — linting, type checking, testing, and bundle analysis.
- **CD (Continuous Deployment)**: Automated delivery of built assets to production infrastructure — CDN, container registry, or edge network.

### Classification
- **Type**: DevOps / frontend infrastructure.
- **CI tools**: GitHub Actions, GitLab CI, CircleCI.
- **CD targets**: Vercel, Cloudflare Pages, AWS S3 + CloudFront, Docker + Kubernetes.

---

## 2. Why does it exist? (Why)

Without CI/CD, frontend deployments rely on manual processes: developers run tests locally (or skip them), build manually, and upload files via FTP or ad-hoc scripts. This leads to:

| Problem | CI/CD Solution |
|---|---|
| Untested code reaching production | **CI gates** block merging until all checks pass |
| Inconsistent builds | **Reproducible build environments** (Node version pinning, lock files) |
| Risky deployments | **Safe deployment patterns** (Canary, Blue/Green, rollback) |
| Performance regressions unnoticed | **Bundle size budgets** enforced automatically |
| Manual, error-prone deployment | **Automated CD** triggered on merge to main |

---

## 3. Without vs. With Comparison (Compare)

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

## 4. Common Use Cases

1. **SaaS products** — Full CI pipeline with E2E tests; CD to Vercel or Cloudflare Pages.
2. **Enterprise applications** — Docker containerization; deployment to internal Kubernetes clusters.
3. **Design system libraries** — CI validates component rendering; CD publishes to private npm registry.
4. **Marketing sites** — Static generation; CD to CDN with immutable asset caching.
5. **Mobile web apps** — Performance budgets enforced in CI; Lighthouse CI for automated audits.

---

## 5. Deep Practice

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

## 6. Code Templates and Integration

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
