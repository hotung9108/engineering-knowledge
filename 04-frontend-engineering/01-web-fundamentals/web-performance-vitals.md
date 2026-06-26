# Web Performance and Core Web Vitals

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hướng dẫn toàn diện về đo lường, chẩn đoán và tối ưu hóa hiệu năng web. Tập trung mạnh vào Core Web Vitals của Google (LCP, CLS, INP), những chỉ số ảnh hưởng trực tiếp đến SEO và trải nghiệm người dùng.

</details>

> **Summary**: A comprehensive guide to measuring, diagnosing, and optimizing web performance. Focuses heavily on Google's Core Web Vitals (LCP, CLS, INP) which directly impact SEO and user experience.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn vào một nhà hàng:
- **LCP (Tốc độ)**: Cần bao lâu để món chính (đĩa bít tết to nhất) được bưng ra bàn? Nếu quá 2.5 giây, bạn sẽ bực mình.
- **CLS (Sự ổn định)**: Bạn định với tay lấy ly nước, đột nhiên bồi bàn đặt đĩa salad vào giữa làm bạn chộp trượt và đánh đổ ly nước. Trang web cũng vậy, nếu chữ và nút bấm cứ nhảy lung tung khi đang tải, người dùng sẽ bấm nhầm.
- **INP (Phản hồi)**: Bạn gọi bồi bàn "Anh ơi!", nếu anh ta quay lại dạ ngay lập tức thì tốt. Nếu anh ta bận làm việc khác, 3 giây sau mới quay lại, bạn sẽ thấy phục vụ quá tệ.

Core Web Vitals chính là "Điểm đánh giá chất lượng phục vụ" của trang web bạn.

</details>

Imagine you go to a restaurant:
- **LCP (Speed)**: How long does it take for the main dish (the biggest steak) to be placed on your table? If it takes too long (>2.5s), you get annoyed.
- **CLS (Stability)**: You reach out to grab your glass of water, but a waiter suddenly slides a salad plate in the middle, causing you to knock the water over. Websites do this too: if text and buttons jump around while loading, users will click the wrong thing.
- **INP (Responsiveness)**: You call out "Excuse me!" to a waiter. If they immediately respond, great. If they are busy and ignore you for 3 seconds before responding, you feel the service is terrible.

Core Web Vitals are essentially the "Customer Service Rating" for your website.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Core Web Vitals** là một bộ 3 chỉ số hiệu năng lấy người dùng làm trung tâm do Google định nghĩa, dùng để đo lường tốc độ tải trang, khả năng tương tác, và sự ổn định thị giác của trang web trong thế giới thực.

**Phân loại:**
- **Loại**: Chỉ số đo lường hiệu năng.
- **Tác giả**: Đội ngũ Google Chrome.
- **Tác động**: Ảnh hưởng trực tiếp đến thứ hạng tìm kiếm trên Google (SEO).

</details>

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

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Các chỉ số cũ như "Thời gian tải trang" (Page Load Time) không phản ánh đúng **cảm nhận của người dùng**. Trang web có thể báo tải xong trong 500ms, nhưng ảnh chính lại mất tới 4 giây mới hiện ra.

Core Web Vitals ra đời nhằm:
- **Chuẩn hóa đo lường** theo cảm nhận thực tế của người dùng.
- **Gắn liền với SEO** — Ép các lập trình viên phải thực sự tối ưu trang web nếu muốn lên top Google.
- **Loại bỏ các chỉ số ảo**: Tháng 3/2024, INP đã thay thế FID vì FID chỉ đo độ trễ của lần bấm *đầu tiên*, bỏ qua các lần bấm bị lag sau đó.

</details>

Traditional performance metrics like page load time and DOMContentLoaded do not accurately reflect **user-perceived performance**. A page can fire `DOMContentLoaded` in 500ms while the hero image takes 4 seconds to appear.

Core Web Vitals were introduced to:

- **Standardize user-centric measurement** across the industry.
- **Tie performance to SEO** — incentivizing developers to invest in optimization.
- **Replace unreliable proxies** (First Meaningful Paint, First Input Delay) with more representative metrics.

INP replaced FID (First Input Delay) in March 2024 because FID only measured the delay of the *first* interaction, ignoring subsequent poor responsiveness.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu không tối ưu: Ảnh chính bị tải chậm (LCP kém), ảnh không có kích thước làm vỡ bố cục (CLS kém), và script nặng chặn luồng xử lý chính làm trang web bị đơ (INP kém).
Khi tối ưu: Báo trình duyệt tải ảnh chính trước (preload), khai báo sẵn kích thước ảnh, và chạy script ngầm.

</details>

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

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Trang sản phẩm E-commerce**: Tối ưu LCP cho ảnh sản phẩm ảnh hưởng trực tiếp tới tỉ lệ mua hàng.
2. **Trang báo chí (News)**: Tối ưu CLS để quảng cáo không đẩy chữ đi nơi khác khi người dùng đang đọc.
3. **Dashboard phần mềm**: Tối ưu INP khi lọc/tìm kiếm dữ liệu để giao diện không bị treo.
4. **Landing Page**: Rất quan trọng cho SEO và giảm tỉ lệ thoát (bounce rate).

**Khi nào ít quan trọng hơn**:
- Các tool nội bộ của công ty (không cần SEO).

</details>

1. **E-commerce product pages** — LCP optimization for hero images directly correlates with conversion rate.
2. **News and content sites** — CLS prevention for ad-heavy layouts with dynamic content injection.
3. **SaaS dashboards** — INP optimization for complex interactive data grids and filters.
4. **Marketing landing pages** — All three metrics critical for SEO and bounce rate.
5. **Progressive Web Apps** — Service Worker caching strategies for repeat-visit performance.

### When deep CWV optimization is less critical

- Internal enterprise tools not indexed by search engines.
- Prototypes and staging environments.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tối ưu LCP**: 
Không bao giờ dùng `loading="lazy"` cho ảnh ở phần đầu màn hình. Dùng `fetchpriority="high"` cho ảnh quan trọng nhất.

**Tối ưu INP**:
Chia nhỏ các tác vụ quá dài (Long Tasks > 50ms) để trình duyệt có thể chen vào xử lý click của người dùng. Tránh re-render không cần thiết trong React.

**Tối ưu CLS**:
Luôn khai báo `width` và `height` cho ảnh. Dùng `font-display: swap` để tránh giật font chữ. KHÔNG chèn nội dung lên trên nội dung đã render.

</details>

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

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đoạn code sử dụng thư viện `web-vitals` để liên tục đo lường và gửi thông số LCP, CLS, INP thực tế của người dùng về server (sử dụng `sendBeacon` để đảm bảo gửi thành công kể cả khi người dùng đang tắt tab).

</details>

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
