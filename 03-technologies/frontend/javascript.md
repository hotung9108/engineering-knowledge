# JavaScript

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ban đầu, JavaScript được tạo ra chỉ trong 10 ngày để làm mấy cái hiệu ứng nhấp nháy cho vui mắt trên trình duyệt (Netscape). Không ai coi nó là một ngôn ngữ "nghiêm túc". Nhưng ngày nay, JS là ngôn ngữ "độc tôn" cai trị toàn bộ mảng Web Frontend. Mọi Framework (React, Vue, Angular) cuối cùng đều phải dịch ra JavaScript để trình duyệt có thể chạy được. JavaScript nổi tiếng với tính "Bất đồng bộ" (Asynchronous) và vòng lặp sự kiện (Event Loop), cho phép nó xử lý hàng ngàn tác vụ song song chỉ bằng một luồng duy nhất (Single-threaded).

</details>

> **Summary**: JavaScript (JS) is the omnipresent, Turing-complete scripting language of the Web. Originally designed in 10 days for trivial DOM manipulations, it has evolved into a massively optimized, JIT-compiled ecosystem (V8 Engine) that monopolizes all client-side browser execution. It is a dynamic, weakly-typed, multi-paradigm language (supporting both Object-Oriented and Functional styles). Its defining architectural characteristic is its **Single-Threaded, Non-Blocking, Asynchronous Event Loop**, allowing it to handle hyper-concurrent I/O operations (like network requests) without freezing the main execution thread.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một tiệm Cà phê có duy nhất 1 Người pha chế (Single Thread).
1. **Lập trình đồng bộ (Synchronous - Các ngôn ngữ khác)**: Khách số 1 gọi ly Cafe phin (mất 5 phút để nhỏ giọt). Người pha chế đứng nhìn giọt cafe rơi suốt 5 phút. Khách số 2, 3, 4 xếp hàng dài ra tận cửa và chửi bới vì phải chờ quá lâu.
2. **Lập trình bất đồng bộ (Asynchronous - JavaScript)**: Khách số 1 gọi Cafe phin. Người pha chế đặt phin cafe lên ly (Gửi I/O Request), Ghi chú cái tên Khách 1 lại (Callback), rồi lập tức xoay qua hỏi Khách số 2: "Anh uống gì?". Anh pha chế liên tục nhận Order của 100 khách. Lát sau, phin cafe của Khách 1 nhỏ xong (Event bíp bíp), anh pha chế quay lại đưa ly cafe cho Khách 1. CHỈ VỚI 1 NGƯỜI, nhưng phục vụ mượt mà 100 khách.

</details>

Imagine a Fast Food Restaurant with exactly One Cashier (Single Thread).
1. **Synchronous Execution (Blocking)**: Customer 1 orders a complex meal that takes 10 minutes to cook. The Cashier stands perfectly still, staring at the kitchen for 10 minutes until the food is ready, completely ignoring the massive line of angry customers behind Customer 1. 
2. **Asynchronous Execution (Non-Blocking JS)**: Customer 1 orders the 10-minute meal. The Cashier shouts the order to the kitchen (Web API / I/O), gives Customer 1 a buzzer (Promise), and immediately shouts: "Next in line please!". The Cashier continuously takes orders. When Customer 1's food is finally ready, the buzzer vibrates (Callback Queue), and the Cashier hands them the food. A single Cashier efficiently handles infinite customers without ever stopping. This is the **Event Loop**.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Cơ chế hoạt động (The Event Loop)**
Trình duyệt chỉ cấp cho JS đúng 1 luồng xử lý chính (Main Thread). Nếu bạn bắt JS làm toán nặng (Tính số Pi 1 tỷ lần), trình duyệt sẽ bị Đơ (Freeze), người dùng không thể bấm cuộn chuột được nữa. Để không bị đơ, JS sử dụng **Event Loop**. Những việc tốn thời gian (như gọi API lấy dữ liệu) sẽ được "Đá" sang cho trình duyệt làm ngầm. JS đi làm việc khác. Khi API trả về, trình duyệt ném kết quả vào "Hàng đợi" (Task Queue). Khi luồng chính rảnh, nó sẽ bốc kết quả ra xử lý (Callback).

**2. ECMA Script (ES6+)**
JS là tên gọi phổ thông. Tên chuẩn khoa học của nó là ECMAScript (ES). Phiên bản ES6 ra đời năm 2015 là một cuộc cách mạng, mang đến hàng loạt cú pháp xịn xò: `let/const`, Arrow Functions `=>`, Classes, Template Literals, và quan trọng nhất là `Promises` để xử lý Asynchronous một cách thanh lịch.

</details>

**1. The Event Loop Architecture**
JavaScript executes strictly on a **Single Thread**. If you execute a computationally heavy synchronous `while(true)` loop, the entire browser tab completely freezes. To prevent UX death, JS aggressively delegates I/O tasks (Timers, HTTP Fetch, DOM Events) to the Browser's internal Web APIs (written in C++). Once the Web API finishes the network call, it pushes the attached `Callback` function into the **Macrotask/Microtask Queue**. The **Event Loop** continuously monitors the Call Stack; the exact microsecond the Call Stack is empty, it dequeues the Callback and pushes it onto the stack for execution.

**2. ECMAScript Standards (ES6+)**
JavaScript is standardized as ECMAScript (ES). The 2015 ES6 release fundamentally modernized the language. It deprecated var-hoisting chaos by introducing block-scoped `let` and `const`. It modernized syntax via Arrow Functions, Destructuring, Spread Operators, and Classes. Most importantly, it introduced `Promises` (and later `async/await`), rescuing developers from "Callback Hell" when managing complex asynchronous flows.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

JS sinh ra vì HTML quá TĨNH. HTML giống như một tờ báo giấy. Bạn chỉ có thể đọc.
Brendan Eich (Cha đẻ JS) muốn tạo ra một ngôn ngữ cực kỳ dễ học, nhúng thẳng vào file HTML, để giúp các thành phần trên web có thể TƯƠNG TÁC được (Ví dụ: Bấm nút thì đổi màu chữ, di chuột thì hình ảnh phóng to). JS sinh ra không phải để xây dựng hệ thống Ngân hàng Core Banking, nó sinh ra để làm Giao diện trở nên sống động. Đó là lý do tại sao JS lại "dễ dãi" (không ép kiểu dữ liệu) và "bất đồng bộ" (để không bao giờ làm đơ giao diện).

</details>

JavaScript was engineered specifically to solve the static nature of HTML. In 1995, websites were static document trees. Netscape required a lightweight, approachable scripting language directly embedded in the HTML markup to enable dynamic DOM manipulation (e.g., form validation before server submission, simple hover animations).
Its design principles deliberately favored leniency over strictness (Dynamic Typing, Type Coercion) to allow amateur web designers to copy-paste code without compiler compilation errors. It adopted the Asynchronous Event Loop strictly because the browser environment demands 60FPS UI responsiveness; blocking the thread to wait for a 56kbps modem API response was mathematically unacceptable.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh sự tiến hóa của việc Xử lý Bất đồng bộ trong JavaScript (Từ Địa ngục đến Thiên đường).
</details>

Visualizing the evolution of Asynchronous JavaScript.

| Era | Paradigm | Syntax Excerpt | Drawbacks |
|---|---|---|---|
| **ES5 (2009)** | **Callbacks** | `api1(data, function(res1) { api2(res1, function(res2) { ... }) })` | **"Callback Hell"** (The Pyramid of Doom). Unreadable, impossible to handle errors cleanly. |
| **ES6 (2015)** | **Promises** | `api1().then(res1 => api2(res1)).catch(err => ...)` | Chaining is cleaner, but still requires nested `.then()` blocks. |
| **ES8 (2017)** | **Async/Await** | `const res1 = await api1(); const res2 = await api2(res1);` | **Perfect.** Reads exactly like synchronous code, while maintaining asynchronous non-blocking performance under the hood. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **DOM Manipulation (Thao tác giao diện)**: Việc cơ bản nhất. Lấy ID của một cái TextBox, đọc chữ khách hàng vừa gõ, sau đó ẩn TextBox đi và hiện chữ "Cảm ơn". (`document.getElementById`, `addEventListener`).
2. **Client-Side Validation (Kiểm tra dữ liệu)**: Khách hàng điền form Đăng ký. Thay vì gửi mật khẩu "123" lên Server rồi chờ Server chửi "Pass quá ngắn". JS sẽ kiểm tra độ dài pass ngay lập tức trên máy tính khách hàng. Nhanh gấp 10 lần và giảm tải cho Server.
3. **Fetching Data (Lấy dữ liệu ngầm - AJAX)**: Bạn cuộn Facebook xuống dưới cùng. JS sẽ tự động gọi lệnh `fetch()` lên Server để xin thêm 10 bài viết nữa, rồi lén lút chèn 10 bài viết đó vào cuối màn hình mà trình duyệt không hề bị tải lại trang.

</details>

1. **Vanilla DOM Manipulation**: Directly interacting with the Browser Object Model (BOM) and Document Object Model (DOM). Attaching Event Listeners to specific HTML nodes, dynamically injecting CSS classes, reading Form input values, and executing structural mutations (e.g., appending a new `<div class="toast">`).
2. **Client-Side Form Validation**: Drastically reducing backend I/O load and improving UX. Intercepting the `onSubmit` event of a `<form>`. Using JavaScript Regex to locally validate email strings, password complexity, and numeric boundaries. If invalid, JS explicitly cancels the HTTP POST request via `e.preventDefault()` and dynamically renders red error text.
3. **AJAX & Data Fetching (XHR/Fetch)**: The foundation of Single Page Applications. Executing asynchronous background HTTP requests (`fetch('/api/users')`) to REST or GraphQL endpoints. Parsing the returned JSON payload and dynamically hydrating the DOM with the new data without executing a hard browser navigational refresh.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Luôn dùng `const` và `let`**: Tuyệt đối xóa bỏ thói quen dùng `var`. `var` có cơ chế Hoisting cực kỳ nguy hiểm, làm biến bị rò rỉ ra khỏi vòng lặp `for`. Dùng `const` cho mọi thứ, chỉ dùng `let` nếu bạn chắc chắn cái biến đó sẽ bị gán lại giá trị khác.
2. **Thấu hiểu Tham chiếu (Reference) vs Giá trị (Value)**: Bạn gán `objA = { name: 'Tun' }; objB = objA;`. Sau đó bạn sửa `objB.name = 'Teo'`. Cả A và B đều biến thành Teo! Trong JS, Object và Array được copy bằng "Địa chỉ ô nhớ" (Reference). Hãy dùng Spread Operator `objB = {...objA}` để copy dữ liệu một cách an toàn (Shallow Copy).

</details>

1. **Strictly Enforce Block Scoping (`const` / `let`)**: Ruthlessly eradicate `var` from your codebase. `var` enforces Function-level scoping and suffers from arbitrary Hoisting, leading to catastrophic runtime state leaks (especially inside `for` loops with async callbacks). Default absolutely every variable to `const`. Only fallback to `let` if the primitive variable inherently requires reassignment (e.g., a loop counter).
2. **Master Primitive vs Reference Value Semantics**: The most common source of JS bugs. Primitives (String, Number, Boolean) are passed by Value. Objects and Arrays are passed by Reference (memory address). Doing `const arrB = arrA; arrB.push(1);` fundamentally mutates `arrA`. To achieve immutability (crucial for React state), you must generate distinct memory instances using the Spread Operator (`const arrB = [...arrA]`) or utilize deep-cloning utilities (`structuredClone()`).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lỗi Ép kiểu ngầm định (Type Coercion)**: Bạn làm toán `1 + "1"`, JS trả về chuỗi `"11"`. Bạn làm `1 - "1"`, JS lại trả về số `0`. Cực kỳ loạn não. Đặc biệt là dùng dấu `==` để so sánh. Trong JS, `0 == false` là Đúng. `"" == false` là Đúng.
   - *Luật*: Luôn luôn dùng 3 dấu bằng `===` để so sánh (Kiểm tra cả Giá trị lẫn Kiểu dữ liệu). Không bao giờ dùng `==`.
2. **Chặn Luồng Chính (Blocking the Event Loop)**: Bạn gọi `JSON.parse(một_chuỗi_json_dài_10MB)`. Hàm parse này là đồng bộ (Synchronous). Trình duyệt sẽ khựng lại 2 giây, không ai bấm được nút gì.
   - *Luật*: Nếu phải làm toán siêu nặng ở Frontend (Xử lý ảnh, Parse dữ liệu khủng), hãy dùng **Web Workers**. Web Worker cho phép JS mở thêm một luồng (Thread) chạy ngầm phía sau mà không làm đơ giao diện chính.

</details>

1. **Implicit Type Coercion Disasters**: Because JS is dynamically weakly typed, the runtime engine attempts to aggressively coerce incompatible types to execute operations. `[] + {}` evaluates to `"[object Object]"`. `0 == false` evaluates to `true`. Relying on coercion leads to silent logical failures. **Absolute Rule**: Never utilize the abstract equality operator (`==`). Strictly enforce the use of the Strict Equality Operator (`===`), which prevents type coercion and evaluates both Value and Type explicitly.
2. **Main Thread Starvation (Synchronous Blocking)**: Believing "JS is Async, so I can't block it" is false. Only I/O is asynchronous. CPU execution is strictly Synchronous. If you execute a massive synchronous array iteration `array.sort()` or a massive `JSON.parse()`, you aggressively starve the Event Loop. The browser cannot paint pixels or process clicks. **The Fix**: Offload heavy CPU-bound algorithms to background OS threads by utilizing the **Web Worker API**, explicitly communicating with the main thread via message passing (`postMessage`).

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp các cú pháp ES6+ thường dùng nhất trong thực tế.
</details>

### Array Methods (Functional Programming)
```javascript
const users = [{id: 1, age: 20}, {id: 2, age: 15}];

// Map (Transform Data)
const ages = users.map(u => u.age); // [20, 15]

// Filter (Remove Data)
const adults = users.filter(u => u.age >= 18); // [{id: 1, age: 20}]

// Reduce (Aggregate Data)
const totalAge = users.reduce((sum, u) => sum + u.age, 0); // 35

// Find (Get First Match)
const user1 = users.find(u => u.id === 1); 
```

### Object Destructuring & Spread
```javascript
const user = { name: 'Alice', role: 'Admin', age: 25 };

// Destructuring (Extract properties into variables)
const { name, role } = user;

// Rest operator (Get everything else)
const { age, ...otherDetails } = user; // otherDetails = {name: 'Alice', role: 'Admin'}

// Spread operator (Merge/Clone Objects)
const updatedUser = { ...user, age: 26, location: 'NY' }; 
// {name: 'Alice', role: 'Admin', age: 26, location: 'NY'}
```

### Promises & Async/Await
```javascript
// The Modern Way to handle fetch
const getUserData = async (userId) => {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) throw new Error('Network error');
    
    const data = await response.json(); // .json() is also a Promise
    return data;
  } catch (error) {
    console.error("Failed to fetch:", error);
  }
};
```

### Optional Chaining & Nullish Coalescing
```javascript
const data = { user: { profile: null } };

// Optional Chaining (?.) - Safe navigation avoiding "Cannot read properties of undefined"
const avatar = data.user?.profile?.avatar; // Returns undefined, no crash.

// Nullish Coalescing (??) - Fallback ONLY if left side is null or undefined
const fallbackAvatar = avatar ?? 'default.png'; // 'default.png'
```

---

## Related Topics

- For adding strict Type Safety to JavaScript, read **[TypeScript](./typescript.md)**.
- For building scalable UI components with JS, read **[React](./react.md)**.
- For executing JavaScript outside the browser (Backend), read **[Node.js / Express](../backend/nodejs-express.md)**.
