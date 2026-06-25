# 05 — Frontend Architecture

> Architectural patterns for production frontend applications. Covers API layer design with automatic token refresh, frontend security (XSS, CSRF, CSP), and scaling strategies with monorepos and micro-frontends.

---

## Prerequisites

- [02 — ReactJS](../02-reactjs/) — State Management Patterns (React Query integration).
- [03 — Next.js](../03-nextjs/) — Server Components and Server Actions.

---

## Content

| # | File | Description |
|---|---|---|
| 1 | [API Layer Design](./api-layer-design.md) | Axios Interceptors, Token Refresh Queue, OpenAPI codegen (Orval), React Query. |
| 2 | [Frontend Security](./frontend-security.md) | XSS, CSRF, Token Storage (HttpOnly Cookies), Content Security Policy (CSP). |
| 3 | [Micro-frontends & Monorepos](./microfrontends-monorepos.md) | Turborepo, Nx, Module Federation, MFE integration patterns. |

---

## Learning Objectives

After completing this section, you should be able to:

- Build a production API layer with centralized authentication and error handling.
- Implement secure token storage and defend against XSS, CSRF, and clickjacking.
- Set up a Turborepo monorepo with shared packages.
- Evaluate whether micro-frontends are appropriate for a given team size and architecture.

---

## Related Sections

- [06 — Build Tools](../06-build-tools/) — CI/CD and deployment for the architectures defined here.
- [05 — Backend Engineering](../../05-backend-engineering/) — Backend APIs that the frontend API layer consumes.
