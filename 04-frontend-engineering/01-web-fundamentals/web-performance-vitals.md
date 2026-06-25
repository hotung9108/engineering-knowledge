# Web Performance and Core Web Vitals

> A comprehensive guide to modern web performance optimization centered on Google's **Core Web Vitals (CWV)**, covering LCP, INP, and CLS measurement, optimization strategies, Resource Hints, and caching architectures. CWV directly impacts SEO rankings and user conversion rates.

---

## 1. What is it? (What)

**Core Web Vitals** are a set of three user-centric performance metrics defined by Google that measure real-world loading speed, interactivity, and visual stability of web pages.

### Classification
- **Type**: Performance metrics / optimization discipline.
- **Defined by**: Google Chrome team (part of the Web Vitals initiative).
- **Impact**: Directly affects Google Search ranking (since June 2021).

| Metric | Measures | Good Threshold |
|---|---|---|
| **LCP** (Largest Contentful Paint) | Loading speed | < 2.5 seconds |
| **INP** (Interaction to Next Paint) | Responsiveness | < 200 ms |
| **CLS** (Cumulative Layout Shift) | Visual stability | < 0.1 |

---

## 2. Why does it exist? (Why)

Traditional performance metrics like page load time and DOMContentLoaded do not accurately reflect **user-perceived performance**. A page can fire `DOMContentLoaded` in 500ms while the hero image takes 4 seconds to appear.

Core Web Vitals were introduced to:

- **Standardize user-centric measurement** across the industry.
- **Tie performance to SEO** — incentivizing developers to invest in optimization.
- **Replace unreliable proxies** (First Meaningful Paint, First Input Delay) with more representative metrics.

INP replaced FID (First Input Delay) in March 2024 because FID only measured the delay of the *first* interaction, ignoring subsequent poor responsiveness.

---

## 3. Without vs. With Comparison (Compare)

### Without CWV optimization

```html
<!-- Hero image lazy-loaded — delays LCP -->
<img src="hero.webp" loading="lazy" />

<!-- No dimensions — causes layout shift (CLS) -->
<img src="product.jpg" />

<!-- Synchronous 3rd-party script — blocks main thread (INP) -->
<script src="https://heavy-analytics.com/bundle.js"></script>
```

### With CWV optimization

```html
<!-- Hero image preloaded and eagerly loaded — improves LCP -->
<link rel="preload" as="image" href="hero.webp" />
<img src="hero.webp" width="1200" height="600" fetchpriority="high" />

<!-- Explicit dimensions prevent CLS -->
<img src="product.jpg" width="400" height="300" loading="lazy" />

<!-- Async loading prevents main thread blocking -->
<script src="https://heavy-analytics.com/bundle.js" async></script>
```

| Aspect | Without optimization | With optimization |
|---|---|---|
| LCP | > 4s (lazy hero image) | < 2.5s (preloaded, eager) |
| CLS | > 0.25 (images shift layout) | < 0.1 (reserved dimensions) |
| INP | > 500ms (blocked main thread) | < 200ms (async scripts) |
| SEO impact | Ranking penalty | Ranking boost |

---

## 4. Common Use Cases

1. **E-commerce product pages** — LCP optimization for hero images directly correlates with conversion rate.
2. **News and content sites** — CLS prevention for ad-heavy layouts with dynamic content injection.
3. **SaaS dashboards** — INP optimization for complex interactive data grids and filters.
4. **Marketing landing pages** — All three metrics critical for SEO and bounce rate.
5. **Progressive Web Apps** — Service Worker caching strategies for repeat-visit performance.

### When deep CWV optimization is less critical

- Internal enterprise tools not indexed by search engines.
- Prototypes and staging environments.

---

## 5. Deep Practice

### LCP Optimization

1. **Preload the LCP element**: `<link rel="preload" as="image" href="hero.webp">`.
2. **Optimize Time to First Byte (TTFB)**: Use a CDN, enable server-side caching, optimize backend response times.
3. **Never lazy-load above-the-fold images** — Only apply `loading="lazy"` to below-the-fold content.
4. **Use Server-Side Rendering (SSR) or Static Site Generation (SSG)** with frameworks like Next.js to deliver HTML with content immediately.
5. **Use `fetchpriority="high"`** on the LCP image element.

### INP Optimization

1. **Break up Long Tasks (>50ms)** — Use `setTimeout`, `requestIdleCallback`, or Web Workers.
2. **Optimize React rendering** — Avoid unnecessary re-renders; use `useTransition` and `useDeferredValue` in React 18+.
3. **Minimize JavaScript bundle size** — Code-split aggressively with dynamic `import()`.
4. **Debounce expensive event handlers** — Particularly for scroll, resize, and input events.
5. **Use `scheduler.yield()`** (when available) to yield to the main thread during long computations.

### CLS Optimization

1. **Always set explicit `width` and `height`** on `<img>`, `<video>`, and `<iframe>` elements.
2. **Reserve space for dynamic content** — Use skeleton screens and placeholders for asynchronously loaded content.
3. **Never inject content above existing content** — Particularly ads and banners.
4. **Use `font-display: optional` or `swap`** combined with `size-adjust` to minimize font-related layout shifts.
5. **Avoid `document.write()`** and late-injecting stylesheets.

### Resource Hints

```html
<!-- Preload: High-priority fetch for critical resources (fonts, hero images) -->
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>

<!-- Preconnect: Establish early connections to required origins -->
<link rel="preconnect" href="https://api.example.com">

<!-- DNS-Prefetch: Lightweight — resolve DNS only -->
<link rel="dns-prefetch" href="https://cdn.example.com">

<!-- Prefetch: Low-priority fetch for resources needed on the NEXT page -->
<link rel="prefetch" href="/js/next-page-chunk.js">
```

### HTTP Caching Strategies

- **Immutable assets** (hashed filenames like `main.a1b2c3.js`): `Cache-Control: public, max-age=31536000, immutable`.
- **Mutable assets** (HTML, API configs): `Cache-Control: no-cache` — forces revalidation via ETag/Last-Modified.
- **Service Workers**: Use Workbox for client-side caching with strategies like Cache-First, Network-First, and Stale-While-Revalidate.

### Best Practices

1. **Measure with real user data (RUM)** — Lab tools (Lighthouse) are useful but field data from CrUX or web-vitals library is authoritative.
2. **Test on low-end devices** — Performance that is acceptable on a MacBook Pro may be unacceptable on a mid-range Android phone.
3. **Automate bundle size monitoring** — Use `size-limit` or `bundlesize` in CI pipelines.
4. **Serve modern image formats** — WebP and AVIF provide 25-50% smaller file sizes than JPEG/PNG.
5. **Implement `<link rel="modulepreload">`** for critical JavaScript modules.

### Common Pitfalls

1. **Lazy-loading the LCP image** — Counterintuitively delays the most important visual element.
2. **Third-party scripts blocking the main thread** — Always load analytics and ads asynchronously.
3. **Dynamic content without reserved space** — Causes CLS spikes when content loads.
4. **Over-preloading** — Preloading too many resources competes for bandwidth with critical assets.
5. **Ignoring INP in favor of FID** — FID only measured the first interaction; INP captures all interactions.

### Production Checklist

- [ ] LCP < 2.5s verified in both lab and field data.
- [ ] INP < 200ms verified across all primary user interaction paths.
- [ ] CLS < 0.1 with no unexpected layout shifts.
- [ ] Hero image preloaded with `fetchpriority="high"`.
- [ ] All media elements have explicit `width` and `height`.
- [ ] All third-party scripts loaded with `async` or `defer`.
- [ ] Bundle size budget enforced in CI pipeline.
- [ ] `web-vitals` library integrated for Real User Monitoring (RUM).

---

## 6. Code Templates and Integration

### Core Web Vitals Monitoring with `web-vitals`

```typescript
import { onCLS, onINP, onLCP, type Metric } from "web-vitals";

function reportMetric(metric: Metric): void {
  // Send to your analytics endpoint
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating, // "good" | "needs-improvement" | "poor"
    delta: metric.delta,
    id: metric.id,
    navigationType: metric.navigationType,
  });

  // Use sendBeacon for reliability during page unload
  if (navigator.sendBeacon) {
    navigator.sendBeacon("/api/analytics/vitals", body);
  } else {
    fetch("/api/analytics/vitals", { body, method: "POST", keepalive: true });
  }
}

onLCP(reportMetric);
onINP(reportMetric);
onCLS(reportMetric);
```

---

## Related Topics

- [Browser Rendering Pipeline](./browser-rendering-pipeline.md) — The rendering stages that CWV metrics measure.
- [JS Engine Internals](./js-engine-internals.md) — Main thread contention and its impact on INP.
- [Caching & Data Fetching (Next.js)](../03-nextjs/caching-and-data-fetching.md) — Server-side caching strategies that improve TTFB and LCP.
- [Frontend CI/CD & Deployment](../06-build-tools/frontend-ci-cd.md) — Automating performance budgets in CI pipelines.
