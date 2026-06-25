# 06 — Build Tools

> Deep dive into frontend build tooling and deployment infrastructure. Covers Vite vs Webpack internal architectures, bundle optimization, CI pipeline design, containerized deployment, and safe release strategies.

---

## Prerequisites

- [05 — Frontend Architecture](../05-frontend-architecture/) — Monorepo and MFE patterns that influence build configuration.

---

## Content

| # | File | Description |
|---|---|---|
| 1 | [Vite vs Webpack Internals](./vite-vs-webpack-internals.md) | Bundle-based vs Native ESM, esbuild, Rollup, Tree Shaking, Code Splitting. |
| 2 | [Frontend CI/CD & Deployment](./frontend-ci-cd.md) | CI pipeline stages, CDN vs Docker hosting, Blue/Green, Canary, Feature Flags. |

---

## Learning Objectives

After completing this section, you should be able to:

- Explain the architectural difference between Webpack's bundle-first and Vite's on-demand approach.
- Configure production bundle optimization (Tree Shaking, Code Splitting, manual chunks).
- Design a complete CI pipeline with lint, type check, test, E2E, and bundle size gates.
- Implement safe deployment strategies (Blue/Green, Canary, Feature Flags).

---

## Related Sections

- [05 — Frontend Architecture / Micro-frontends](../05-frontend-architecture/microfrontends-monorepos.md) — Module Federation with Webpack.
- [01 — Web Fundamentals / Performance](../01-web-fundamentals/web-performance-vitals.md) — Performance budgets enforced in CI.
