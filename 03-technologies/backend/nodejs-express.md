# Node.js & Express

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trong suốt một thập kỷ, JavaScript bị giam cầm bên trong Trình duyệt web (Frontend). Nếu bạn muốn viết code Máy chủ (Backend), bạn bắt buộc phải học một ngôn ngữ hoàn toàn khác như PHP, Java, hoặc Ruby. Năm 2009, Ryan Dahl tạo ra **Node.js** bằng cách "mổ bụng" trình duyệt Chrome, lôi lõi V8 Engine (bộ máy đọc code JS) ra ngoài, và cài nó thẳng lên Máy chủ máy tính. Lần đầu tiên trong lịch sử, Lập trình viên có thể dùng chung một ngôn ngữ JavaScript duy nhất cho cả Frontend lẫn Backend. Đi kèm với Node.js là **Express.js** - một thư viện siêu nhẹ giúp dựng API (cổng giao tiếp mạng) chỉ trong đúng 5 dòng code.

</details>

> **Summary**: Historically, JavaScript was strictly a client-side execution environment, quarantined within the sandbox of the Web Browser. Backend engineering required context-switching to distinct languages like PHP, Java, or Ruby. In 2009, **Node.js** shattered this barrier. It extracted the ultra-fast V8 JavaScript Engine from Google Chrome, embedded it with C++ system bindings, and deployed it directly onto the OS Server layer. This birthed the paradigm of "JavaScript Everywhere" (Full-Stack JS). Because raw Node.js networking APIs are aggressively low-level, **Express.js** was created as a minimalist, unopinionated web framework on top of Node.js. It provides a robust routing mechanism and middleware architecture, allowing developers to spin up REST APIs in mere seconds.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng JavaScript là một con cá.
1. **Trình duyệt (Chrome)**: Là một cái bể cá. Con cá (JS) bơi rất giỏi, nhưng nó bị kẹt trong bể, không thể chạm vào đồ đạc trong nhà bạn (Không thể đọc/ghi file trên ổ cứng Máy tính).
2. **Node.js**: Là một bộ "Áo giáp Robot" có chân tay. Người ta bắt con cá bỏ vào buồng lái của bộ giáp. Bây giờ, con cá (JS) không những sống được trên cạn, mà còn có thể dùng tay Robot để nhấc đồ đạc, mở cửa, và kết nối với mạng lưới điện của cả thành phố (Đọc ghi File, mở cổng mạng Server).
3. **Express.js**: Là một cuốn sổ tay hướng dẫn giao tiếp gắn sẵn trên bộ giáp Robot. Thay vì bạn phải tự dạy Robot cách nói "Xin chào" bằng mã Morse phức tạp, cuốn sổ tay này giúp Robot hiểu và phản hồi khách hàng tự động cực kỳ nhanh chóng.

</details>

Imagine JavaScript is an Astronaut.
1. **The Web Browser**: This is a spaceship. The Astronaut (JS) is brilliant, but they are physically locked inside the spaceship (Sandboxed). They can look out the window, but they cannot physically touch the rocks on the planet outside (Cannot access the Server's Hard Drive or OS features).
2. **Node.js**: This is a space suit with advanced robotic arms. By putting the Astronaut in this suit, they can finally step *outside* the spaceship onto the actual planet. They can pick up rocks (Read/Write OS Files) and build communication towers (Open Network Ports).
3. **Express.js**: This is an automatic translator built into the space suit's radio. Instead of the Astronaut manually decoding raw radio static (Raw HTTP Buffers), Express intercepts the signal, translates it into English (JSON Requests), and provides a single button to reply instantly.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Node.js không phải là Framework**: Nó là một "Môi trường chạy" (Runtime Environment). Nó cho phép code JS tương tác với Hệ điều hành (Đọc/Ghi file bằng `fs`, Mở cổng mạng bằng `http`). Nó giữ nguyên bản chất cực kỳ xịn xò của JS: **Bất đồng bộ (Asynchronous) và Đơn luồng (Single-Threaded)**.
2. **Express.js là Thư viện định tuyến**: Nó là thư viện phổ biến nhất của Node. Nó quản lý các Routes (Đường dẫn). Ví dụ: Khách gọi `GET /users`, Express bắt lấy request đó, kiểm tra bảo mật bằng các lớp lọc (Middleware), sau đó chui vào Database lấy dữ liệu, rồi ói ra cục JSON trả về cho khách.

</details>

1. **Node.js (The Runtime Environment)**: Node.js is NOT a framework, and it is NOT a language. It is a C++ program that embeds the V8 JavaScript engine. It provides bindings to the operating system's native primitives (via the `libuv` library). It allows JavaScript to execute File System I/O (`fs`), Cryptography (`crypto`), and Network Socket operations (`net`/`http`). Crucially, it inherits JavaScript's **Single-Threaded, Non-Blocking Event Loop** architecture, making it exponentially more efficient at handling thousands of concurrent I/O connections than traditional Thread-Per-Request models (like Apache/PHP).
2. **Express.js (The Micro-Framework)**: Raw Node.js HTTP servers require parsing raw buffer streams and manually constructing stringified HTTP Headers. Express abstracts this tedium. It is a minimalist web framework providing two core features: **Routing** (mapping URLs and HTTP Methods to specific controller functions) and **Middleware** (a pipeline of functions that intercept, mutate, or reject incoming requests before they reach the controller).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trước Node.js, Máy chủ (như Apache + PHP) dùng cơ chế "Mỗi khách hàng 1 nhân viên" (Thread-per-request). Nếu có 10.000 khách truy cập cùng lúc, Máy chủ phải sinh ra 10.000 nhân viên (Thread). Việc này ngốn cạn kiệt RAM và làm máy chủ nổ tung (Crash).
Node.js ra đời để giải quyết bài toán C10K (10.000 kết nối đồng thời). Nhờ cơ chế Event Loop đơn luồng, Node.js chỉ dùng ĐÚNG 1 NHÂN VIÊN. Khi khách số 1 yêu cầu lấy dữ liệu (Mất 2 giây), nhân viên này không đứng chờ. Anh ta ném yêu cầu đó cho Database, rồi quay ngoắt sang nhận order của khách số 2, số 3, số 10.000. Do đó, Node.js tiêu thụ cực kì ít RAM mà vẫn chịu tải cực lớn (High Concurrency).

</details>

Node.js was engineered specifically to solve the "C10K Problem" (handling 10,000 concurrent network connections).
Traditional backend runtimes (e.g., Apache with PHP or early Java Tomcat) utilized a **Thread-Per-Request** blocking model. Every incoming HTTP connection spawned a new OS Thread. OS Threads are expensive; they consume ~2MB of RAM each. 10,000 users = 20GB of RAM just to keep the connections open, leading to catastrophic server crashes during traffic spikes.
Node.js revolutionized this by utilizing a **Single-Threaded, Event-Driven, Non-Blocking I/O** model. When Node.js receives an HTTP request that requires a 3-second database query, it does NOT block the thread. It offloads the query to the OS, registers a callback, and instantly accepts the next incoming network request. A single Node.js thread can juggle 50,000 idle websocket connections simultaneously while consuming negligible RAM.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc tạo Máy chủ Web bằng Node.js thuần (không có Express) và dùng Express.
</details>

Visualizing Raw Node.js vs Express.js Routing.

| Metric | Raw Node.js (`http` module) | Express.js |
|---|---|---|
| **The Code** | `http.createServer((req, res) => {`<br>`  if (req.url === '/users' && req.method === 'GET') {`<br>`    res.writeHead(200, {'Content-Type': 'application/json'});`<br>`    res.end(JSON.stringify([{id: 1}]));`<br>`  }`<br>`})` | `app.get('/users', (req, res) => {`<br>`  res.json([{id: 1}]);`<br>`});` |
| **Parsing JSON Body**| You must manually listen to data streams (`req.on('data', chunk => ...)`), buffer them, and run `JSON.parse()`. Extremely tedious. | `app.use(express.json());` (One line of Middleware handles everything). |
| **Routing** | A massive, nested `if/else` or `switch` statement that grows to thousands of lines. Unmaintainable. | Elegant `express.Router()`. Cleanly separated into modular files (`userRoutes.js`). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khởi nghiệp và Ra mắt sản phẩm nhanh (MVP/Startups)**: Node + Express vô địch về tốc độ viết code. Không có lề thói khuôn mẫu phức tạp như Java Spring Boot. Chỉ cần tạo 1 file `index.js`, gõ 10 dòng code là có ngay 1 API chạy thực tế.
2. **Ứng dụng Real-time (Thời gian thực)**: Ứng dụng Chat (Tinder, Discord thời đầu), Game nhiều người chơi, Bảng chứng khoán nhảy số liên tục. Khả năng giữ hàng chục ngàn kết nối WebSockets mở liên tục mà không tốn RAM khiến Node.js là trùm của mảng Real-time.
3. **BFF (Backend-For-Frontend) và API Gateway**: Các công ty lớn (như Netflix, Uber) dùng Node.js làm lớp trung gian. Đội Frontend viết Node.js để tự động lấy dữ liệu từ hàng chục hệ thống Microservices khổng lồ (viết bằng Java/Go) phía sau, "xào nấu" gom dữ liệu lại thành 1 cục JSON đẹp đẽ rồi mới đẩy xuống trình duyệt.

</details>

1. **Rapid Prototyping & MVPs (Startups)**: Node.js/Express is completely unopinionated. It lacks the massive architectural boilerplate of Enterprise Frameworks (Java Spring, C# .NET). A Full-Stack developer can spin up an entire REST CRUD API connected to MongoDB/PostgreSQL in a single afternoon. Using TypeScript across both React and Express guarantees end-to-end type safety, doubling developer velocity.
2. **High-Concurrency Real-Time Applications**: Chat engines, Live-Bidding Auction platforms, and Collaborative editing tools (WebSockets / Socket.io). Because Node is event-driven and non-blocking, it excels at maintaining thousands of persistent, idle TCP connections simultaneously. Traditional threaded servers would collapse under the RAM pressure of 50,000 open WebSockets; Node handles it effortlessly.
3. **API Gateways & Backend-For-Frontend (BFF)**: Architectures heavily utilized by Netflix and LinkedIn. Node.js sits as a lightweight middleware layer. It receives a request from the Mobile App, fires off 10 simultaneous asynchronous HTTP requests to heavy backend Java Microservices, aggregates the responses into a single optimized JSON payload, and returns it to the client. Node's native async/await makes this aggregation trivial.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Kiến trúc nhiều tầng (Controller - Service - Repository)**: Express không ép buộc bạn cấu trúc thư mục. Lỗi phổ biến nhất là nhét hết code gọi Database vào trong cái ngã ba Routing (Controller). Hãy chia ra: `routes.js` (Khai báo link) $\rightarrow$ `controller.js` (Nhận/Trả JSON) $\rightarrow$ `service.js` (Logic nghiệp vụ) $\rightarrow$ `repository.js` (SQL Queries).
2. **Quản lý Lỗi tập trung (Global Error Handler)**: Đừng viết `try/catch` ở 100 hàm API rải rác khắp nơi rồi `res.status(500).send("Lỗi")`. Hãy dồn tất cả lỗi về một Middleware chuyên xử lý lỗi nằm ở cuối file `app.js`. Nó sẽ tự động ghi Log và trả mã lỗi chuẩn hóa về cho khách.

</details>

1. **Enforce N-Tier Architecture (Controller-Service Pattern)**: Express's greatest flaw is that it is *too* flexible. Junior developers write "Fat Controllers"—putting raw SQL/Mongoose queries directly inside `app.get()`. This is untestable and unmaintainable. You must manually enforce architecture:
   - **Routes Layer**: Simply maps URLs to Controllers.
   - **Controllers Layer**: Extracts `req.body`, calls the Service, and returns `res.status(200)`.
   - **Services Layer**: Pure business logic (Calculations, IF/ELSE rules). Knows nothing about HTTP `req` or `res`.
2. **Global Error Handling Middleware**: Never handle responses inside individual `catch` blocks. If an exception occurs, pass it to Express's `next(error)` function. Define a single, centralized Error Handling Middleware at the very bottom of your application. This middleware will log the stack trace to Datadog/Sentry, format a sanitized error message (hiding internal DB errors from the client), and return a consistent JSON error schema.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Chặn Đứng Event Loop (Sát thủ Node.js)**: Node.js là đơn luồng. Nếu bạn viết một vòng lặp `for` tính toán 1 tỷ lần, hoặc dùng hàm `JSON.parse` với file 50MB. LUỒNG DUY NHẤT ĐÓ SẼ BỊ KHỰNG LẠI (Block). Toàn bộ 10.000 khách hàng khác đang chờ sẽ bị treo cứng trang web. 
   - *Luật*: Node.js RẤT GIỎI trong việc đẩy file, gọi mạng lưới (I/O). Nhưng Node.js CỰC KỲ DỞ trong việc làm toán nặng (CPU-bound). Đừng bao giờ lấy Node.js đi xử lý ảnh hay nén video.
2. **Quên gọi `next()` trong Middleware**: Middleware giống như trạm thu phí. Khi một Yêu cầu đi qua, bạn phải mở Barie bằng cách gọi lệnh `next()`. Nếu bạn quên gọi `next()`, Yêu cầu đó sẽ bị kẹt lại mãi mãi ở trạm thu phí, trình duyệt của khách hàng cứ xoay vòng vòng cho đến khi báo lỗi Timeout.

</details>

1. **Blocking the Event Loop (CPU Starvation)**: The most catastrophic mistake in Node.js. Node is asynchronous for I/O (Database, Network), but it is perfectly Synchronous for CPU execution. If you execute a highly complex cryptographic hashing function (like `bcrypt.hashSync`) or execute a massive Array Sort on a 1GB JSON payload, the Single Thread is physically blocked. During those 3 seconds, the server cannot accept new requests; every single connected user experiences a frozen application. **Rule**: Offload heavy CPU-bound tasks to separate `Worker Threads` or delegate them to a backend language suited for parallel processing (like Go/Rust).
2. **The Hanging Request (Dangling Middleware)**: In Express, a request travels through a pipeline of Middleware. Inside a middleware function `(req, res, next) => { ... }`, you MUST either terminate the request (by calling `res.send()`) or explicitly pass control to the next function by calling `next()`. If you write an `if` statement but forget to put `next()` in the `else` block, the request is orphaned. The server doesn't crash, but the client's browser spins infinitely until the connection times out.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cách tạo một API RESTful siêu tốc bằng Node.js & Express (kết hợp TypeScript).
</details>

### Server Setup & Middleware (app.ts)
```typescript
import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';

const app = express();

// 1. GLOBAL MIDDLEWARE
app.use(cors()); // Allow Frontend (React) to make requests to this API
app.use(express.json()); // Parse incoming JSON payloads attached to req.body

// 2. BASIC ROUTE
app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({ status: 'OK', uptime: process.uptime() });
});

// 3. ATTACH ROUTER MODULES
import userRoutes from './routes/userRoutes';
app.use('/api/users', userRoutes);

// 4. GLOBAL ERROR HANDLER (Must have 4 parameters)
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error("CRITICAL ERROR:", err.message);
  res.status(500).json({ error: "Internal Server Error" });
});

// START SERVER
app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### Routing & Controllers (userRoutes.ts)
```typescript
import { Router, Request, Response } from 'express';
const router = Router();

// Mock Database
let users = [{ id: 1, name: "Alice" }];

// GET ALL (Read)
router.get('/', (req: Request, res: Response) => {
  res.status(200).json({ data: users });
});

// GET ONE (Read via URL Params)
router.get('/:id', (req: Request, res: Response) => {
  const userId = parseInt(req.params.id);
  const user = users.find(u => u.id === userId);
  
  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }
  res.status(200).json({ data: user });
});

// POST (Create via Body Payload)
router.post('/', (req: Request, res: Response) => {
  const { name } = req.body;
  
  if (!name) {
    return res.status(400).json({ error: "Name is required" }); // Input Validation
  }

  const newUser = { id: users.length + 1, name };
  users.push(newUser);
  res.status(201).json({ data: newUser }); // 201 Created
});

export default router;
```

### Custom Middleware (Authentication Guard)
```typescript
const protectRoute = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization;
  
  if (!token || token !== "Bearer SECRET_KEY") {
    // Terminate request early. Do NOT call next()
    return res.status(401).json({ error: "Unauthorized access" });
  }
  
  // Auth passed. Proceed to the actual Controller.
  next(); 
};

// Apply middleware specifically to this protected route
router.delete('/:id', protectRoute, (req: Request, res: Response) => {
  res.status(200).json({ message: "User deleted" });
});
```

---

## Related Topics

- Node.js executes **[JavaScript](../frontend/javascript.md)** and highly recommends **[TypeScript](../frontend/typescript.md)** for architecture.
- For managing data from Express, see **[PostgreSQL](../databases/postgresql.md)** or **[MongoDB](../databases/mongodb.md)**.
- If Node.js becomes a bottleneck for heavy CPU calculations, look towards **[Go](./go.md)**.
