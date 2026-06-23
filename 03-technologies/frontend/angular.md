# Angular

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu React là một cái mỏ lết linh hoạt, thì **Angular** là một bộ máy khoan công nghiệp nguyên khối được thiết kế bởi Google. Khác với React (chỉ là thư viện), Angular là một Framework Frontend "Pin sạc đầy đủ" (Batteries-Included). Nó ép buộc toàn bộ đội ngũ lập trình viên phải viết code theo một khuôn mẫu chuẩn duy nhất, mặc định sử dụng TypeScript, RxJS, và Dependency Injection. Dù có phần cứng nhắc và đồ sộ lúc ban đầu, sự chặt chẽ này biến Angular trở thành lựa chọn số 1 cho các hệ thống phần mềm Ngân hàng, Bảo hiểm, và các dự án quy mô siêu lớn (Enterprise) nơi cần hàng trăm lập trình viên làm việc chung mà không dẫm đạp lên code của nhau.

</details>

> **Summary**: While React bills itself as a flexible UI library, **Angular** (developed and maintained by Google) is a heavyweight, highly opinionated, "Batteries-Included" Frontend Framework. It is architected specifically for massive Enterprise Single Page Applications (SPAs). Angular enforces a strict, standardized ecosystem: it physically mandates the use of TypeScript, integrates RxJS for complex asynchronous event streams, and fundamentally relies on Dependency Injection (DI) to decouple services from components. By removing the "paradox of choice" that plagues the React ecosystem (where teams must constantly debate which router or state manager to use), Angular provides a robust, predictable, and highly scalable blueprint engineered for large distributed engineering teams.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn chuẩn bị xây một ngôi nhà.
1. **React**: Bạn đi vào siêu thị vật liệu. Bạn tự do lựa chọn mua gạch hãng A, xi măng hãng B, mái tôn hãng C. Bạn có thể xây ra một ngôi nhà cực kì độc đáo, nhưng nếu bạn thiếu kinh nghiệm, ngôi nhà sẽ méo mó và sập. Bạn sẽ cãi nhau với kiến trúc sư cả ngày về việc nên dùng xi măng nào.
2. **Angular**: Bạn thuê một công ty thầu lớn (Google). Họ vứt cho bạn một cuốn sổ tay quy định: "Anh CHỈ ĐƯỢC PHÉP dùng gạch đỏ loại X, xi măng trộn tỉ lệ 3:1, và đường ống nước phải đi góc này". Lúc đầu bạn thấy bực mình vì bị gò bó. Nhưng khi bạn thuê thêm 100 người thợ vào xây chung, ai cũng tuân theo 1 cuốn sổ tay đó, công việc chạy cực kỳ trơn tru, không ai cãi nhau, và ngôi nhà 100 tầng được xây lên vững như bàn thạch.

</details>

Imagine outfitting an Army.
1. **React**: Every soldier is given a budget and told to buy their own gun, their own boots, and their own radio. Some buy snipers, some buy swords. It's highly creative, but communication and standardization across the army are chaotic.
2. **Angular**: The General (Google) issues standard uniforms. Every single soldier receives the exact same M4 Rifle, the exact same radio (RxJS), and the exact same map (Angular Router). No one gets to choose their equipment. The training is much harder, but on the battlefield, the entire army operates as one perfectly synchronized, standardized machine. If a soldier from Platoon A is moved to Platoon B, they instantly know how everything works.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cấu trúc của Angular xoay quanh các khái niệm Cổ điển của Kỹ nghệ phần mềm (Software Engineering):
1. **Component-Driven (Giống React/Vue)**: Mỗi file được chia làm 3 phần rạch ròi: `.html` (Giao diện), `.css` (Định dạng), và `.ts` (Logic TypeScript).
2. **Dependency Injection (DI)**: Thay vì nhét các hàm gọi API vào chung với giao diện, Angular bắt bạn phải tách nó ra một file gọi là `Service`. Khi Component cần gọi API, nó không tự tạo Service, nó chỉ "Hét lên" xin Angular tiêm (Inject) Service đó vào cho nó dùng. Việc này giúp code cực kỳ dễ test.
3. **RxJS (Reactive Extensions)**: Thay vì dùng Promise `async/await` thông thường, Angular ép dùng `Observables`. Nó coi mọi thứ (chuột click, gọi API) là một Dòng chảy dữ liệu (Stream) liên tục. Bạn có thể Bơm, Lọc, Gộp các dòng chảy này lại với nhau cực kỳ mạnh mẽ.

</details>

Angular's architecture is deeply rooted in traditional Object-Oriented Software Engineering paradigms (heavily inspired by Backend architectures like Spring Boot/Java):
1. **Separation of Concerns**: Unlike React's JSX which merges template and logic, an Angular component strictly segregates files: `component.ts` (Class logic), `component.html` (Template View), and `component.scss` (Scoped Styling).
2. **Dependency Injection (DI)**: The backbone of Angular. Components are strictly presentation layers. Complex business logic and HTTP calls are abstracted into injectable singleton classes (`@Injectable()` Services). When a Component requires data, it declares the Service in its constructor, and Angular's DI framework automatically instantiates and wires the dependency. This guarantees loose coupling and makes Unit Testing incredibly simple via mock injections.
3. **Reactive Programming (RxJS)**: Angular bypasses standard `Promises` in favor of `Observables` provided by the RxJS library. Network requests (`HttpClient`) and DOM events are treated as continuous, cancellable data streams. Developers use functional operators (`map`, `filter`, `switchMap`) to compose highly complex asynchronous race conditions effortlessly.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thế giới React rất tuyệt vì sự tự do. Nhưng "Tự do" trong các tập đoàn lớn là một Thảm họa.
Trong công ty 500 Dev, Team A dùng React Router, Team B dùng Wouter. Team A quản lý State bằng Redux, Team B dùng Zustand, Team C dùng Context API. Khi ghép code lại với nhau, hệ thống vỡ nát. Mỗi khi có dự án mới, các Senior lại mất 2 tuần chỉ để cãi nhau xem nên dùng thư viện nào.
Angular tồn tại để **Xóa bỏ Sự lựa chọn (Opinionated)**. Angular đã tự chọn sẵn cho bạn: Router xịn nhất, State xịn nhất, Form xịn nhất, HTTP Client xịn nhất. Lập trình viên không cần bàn cãi về "Kiến trúc", họ chỉ cần bắt tay vào viết Business Logic (nghiệp vụ). Khi một lập trình viên Angular chuyển từ công ty Mỹ sang công ty Nhật, họ mở source code lên và thấy cấu trúc thư mục y chang nhau.

</details>

Angular exists to solve the "Paradox of Choice" and "Architecture Fragmentation" in massive enterprise organizations.
In the React ecosystem, assembling a framework is a localized, bespoke effort. Team Alpha might use `react-query` + `react-router` + `tailwind`. Team Beta might use `redux-saga` + `wouter` + `styled-components`. When developers transfer between teams, they face a massive relearning curve. Upgrading foundational libraries often causes cascading breaking changes.
Angular is highly **Opinionated**. It mandates a singular, monolithic standard. It ships natively with an enterprise-grade Router, a robust HTTP Client, a complex Form validation engine (Reactive Forms), and internationalization (i18n). Developers do not waste sprints debating tech stacks; they exclusively focus on implementing business logic. This homogenization drastically reduces onboarding time and ensures long-term architectural stability across 10-year project lifespans.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cách xử lý một bài toán cực khó: Khách hàng gõ chữ vào ô Tìm kiếm. Mỗi lần gõ 1 chữ, gọi API 1 lần. Nếu khách gõ quá nhanh, phải Hủy (Cancel) các lệnh gọi API cũ, chỉ lấy kết quả của chữ cuối cùng để tránh lỗi.
</details>

Visualizing Asynchronous Race Conditions (Typeahead Search).

| Metric | React (Promises/useEffect) | Angular (RxJS Observables) |
|---|---|---|
| **The Challenge**| User types "A", then "B". Two API calls fire. The "A" call is slow and returns *after* the "B" call, overwriting the UI with outdated data (Race Condition). | Exactly the same. |
| **The Solution** | Complex boilerplate. You must create an `AbortController`, attach it to the `fetch`, and manually trigger `abort()` inside the `useEffect` cleanup function. Extremely error-prone. | `searchControl.valueChanges.pipe(` <br> `debounceTime(300),` <br> `switchMap(term => api.search(term))` <br> `)` |
| **Developer Effort**| High cognitive load. Easy to create memory leaks. | **Elegant**. RxJS's `switchMap` operator natively and automatically cancels any pending previous HTTP requests the microsecond a new keystroke occurs. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Enterprise Applications (Hệ thống Ngân hàng, Bảo hiểm)**: Nơi bảo mật, tính ổn định và bảo trì lâu dài (10-20 năm) quan trọng hơn sự màu mè. Code Angular chạy 10 năm sau vẫn có thể nâng cấp dễ dàng nhờ công cụ CLI quá tốt.
2. **Dashboard quản trị dữ liệu siêu phức tạp**: Angular tích hợp sẵn công cụ `Reactive Forms` cực kỳ khủng khiếp. Bạn có thể kiểm tra một cái Form dài 200 trường dữ liệu, liên kết logic chéo với nhau (Ví dụ: Nếu chọn Giới tính Nam thì tự động khóa ô Sinh Đẻ) một cách vô cùng sạch sẽ.
3. **Các nhóm dev có xuất thân từ Java/C#**: Bởi vì Angular dùng TypeScript với Class, Interface, Decorator (`@Component`), và Dependency Injection. Các lập trình viên Backend (Java Spring Boot, C# .NET) khi chuyển sang học Frontend sẽ cảm thấy cấu trúc của Angular cực kỳ quen thuộc và gần gũi.

</details>

1. **Massive Enterprise SPAs (FinTech/GovTech)**: Banking portals, Insurance claim systems, and Healthcare ERPs. These platforms prioritize strict typing, testability, and 10-year maintainability over rapid UI prototyping. Angular's CLI allows for seamless framework upgrades (`ng update`) even across millions of lines of code.
2. **Heavy Data-Entry / Complex Form Systems**: Angular's **Reactive Forms** module is arguably the most powerful form-handling engine in the Frontend ecosystem. Building a dynamic, 150-field tax declaration form with deeply nested validation rules, cross-field dependency checks, and asynchronous server-side validation is natively supported and architecturally clean.
3. **Backend-Heavy Engineering Teams**: Because Angular architecture (Classes, `@Decorators`, Dependency Injection, Interfaces) perfectly mirrors Backend Object-Oriented frameworks like **Spring Boot (Java)** and **.NET (C#)**, organizations transitioning backend developers to Full-Stack roles typically choose Angular to drastically reduce the architectural learning curve.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khai thác tối đa Reactive Forms**: Tuyệt đối tránh dùng `Template-driven Forms` (Dùng `ngModel`) cho các form lớn. Hãy dùng `Reactive Forms` (`FormGroup`, `FormControl`). Nó giúp tách biệt hoàn toàn Logic kiểm tra lỗi ra khỏi giao diện HTML, làm code dễ Test hơn hàng trăm lần.
2. **Sử dụng `async` pipe (Bí kíp chống rò rỉ bộ nhớ)**: Khi dùng RxJS để gọi API, bạn thường phải viết lệnh `.subscribe()`. Rất nhiều Dev quên gọi lệnh `.unsubscribe()` khi tắt màn hình, dẫn đến tràn RAM trình duyệt. Hãy dùng `<div *ngIf="data$ | async">` ở ngoài HTML. Angular sẽ tự động đăng ký và tự động Hủy đăng ký khi tắt màn hình, an toàn tuyệt đối 100%.

</details>

1. **Exclusively utilize Reactive Forms for Scale**: Angular offers two form paradigms: Template-Driven (simple, `ngModel`-based) and Reactive (complex, model-driven in TS). For enterprise applications, strictly enforce Reactive Forms. By declaring the `FormGroup` programmatically in the TypeScript class, you achieve perfect separation of concerns, synchronous testing capabilities, and the ability to dynamically push/pop FormControls at runtime without touching the DOM.
2. **Master the `async` Pipe (Prevent Memory Leaks)**: When a Component subscribes to an RxJS `Observable` (e.g., an interval or WebSocket), the subscription stays alive in browser memory even if the user navigates away, causing catastrophic memory leaks. Instead of manually storing subscriptions and calling `.unsubscribe()` in `ngOnDestroy`, natively bind the Observable in the HTML template using the `async` pipe: `*ngFor="let item of users$ | async"`. Angular automatically handles the subscription lifecycle and tears it down flawlessly upon component destruction.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hell of Observables (Địa ngục RxJS)**: RxJS quá mạnh nên nó cũng là con dao giết chết người mới. Thay vì gộp chuỗi đàng hoàng bằng `pipe()`, các Dev mới thường viết `.subscribe()` lồng vào bên trong một `.subscribe()` khác (Y hệt như Callback Hell của JS thời tiền sử). Điều này tạo ra một đống code rác rối rắm và giật lag mạng.
2. **Tẩy chay Standalone Components (Angular 14+)**: Ngày xưa, Angular bắt buộc mọi file phải được khai báo trong một cái "Hộ khẩu" khổng lồ gọi là `NgModule`. Nó làm code bị rối và khó chia sẻ. Từ Angular 14, khái niệm `Standalone Components` ra đời (giống hệt React/Vue, Component tự do cất cánh). Rất nhiều Dev cũ lười không chịu cập nhật kiến thức này, tiếp tục viết `NgModule` khiến dự án mới cũng bị phình to vô ích.

</details>

1. **Nested Subscriptions (RxJS Anti-Pattern)**: The most prevalent junior Angular mistake. Developers attempting to execute sequential API calls will subscribe to `Call A`, and inside that block, subscribe to `Call B`. This recreates "Callback Hell" and defeats the entire mathematical purpose of streams. **The Fix**: Strictly enforce the use of Higher-Order Mapping Operators (`switchMap`, `mergeMap`, `concatMap`) inside a `.pipe()` chain. You should only ever have exactly ONE `.subscribe()` at the very end of the chain.
2. **Clinging to `NgModules` (Ignoring Modern Angular)**: Historically, Angular required all components to be registered in a monolithic `app.module.ts`. This created massive dependency trees and hampered lazy-loading. Angular 14+ introduced **Standalone Components** (`@Component({ standalone: true })`). This paradigm shift eliminates `NgModules` entirely, allowing components to directly import their own dependencies (identical to React's mental model). Architecting new applications using legacy `NgModules` is now considered a deprecated architectural anti-pattern.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cấu trúc cơ bản của Angular 17+ (Sử dụng Standalone Components và Control Flow mới).
</details>

### The Angular Component (Modern Standalone format)
```typescript
// user-profile.component.ts
import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from './user.service'; // Dependency

@Component({
  selector: 'app-user-profile',
  standalone: true, // Modern Angular (No NgModules needed)
  imports: [CommonModule], // Import dependencies directly
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss']
})
export class UserProfileComponent implements OnInit {
  // Dependency Injection (Modern approach via inject())
  private userService = inject(UserService);

  // Class Properties (State)
  userTitle = 'Angular Expert';
  users$ = this.userService.getUsers(); // Observable stream (Best practice to append $)

  ngOnInit(): void {
    console.log('Component initialized');
  }

  updateTitle() {
    this.userTitle = 'RxJS Master';
  }
}
```

### The HTML Template (Modern Angular 17+ Control Flow)
Notice the new `@if` and `@for` syntax, replacing the clunky legacy `*ngIf` and `*ngFor` directives.

```html
<!-- user-profile.component.html -->
<div class="profile-container">
  <!-- Interpolation (Binding state) -->
  <h1>{{ userTitle }}</h1>

  <!-- Event Binding (Parentheses) -->
  <button (click)="updateTitle()">Upgrade Title</button>

  <!-- Modern Control Flow: @if -->
  @if (userTitle === 'RxJS Master') {
    <p class="badge">🔥 Master Level Unlocked!</p>
  } @else {
    <p>Keep studying...</p>
  }

  <!-- Modern Control Flow: @for with the async pipe -->
  <!-- The 'async' pipe automatically subscribes and unsubscribes to users$ -->
  <ul>
    @for (user of users$ | async; track user.id) {
      <li>{{ user.name }} - {{ user.email }}</li>
    } @empty {
      <li>No users found in database.</li>
    }
  </ul>
</div>
```

### The Service (Dependency Injection & RxJS)
```typescript
// user.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// ProvidedIn: 'root' makes this a Singleton available globally
@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);

  // Returns a stream of data, not a Promise
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('https://api.example.com/users');
  }
}
```

---

## Related Topics

- Angular is built strictly on top of **[TypeScript](./typescript.md)**.
- For a lightweight, progressive alternative without the enterprise boilerplate, see **[Vue.js](./vuejs.md)**.
- To compare Angular's OOP approach with a Functional UI library, read **[React](./react.md)**.
