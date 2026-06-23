# GraphQL

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Năm 2012, Facebook phải đối mặt với một vấn đề lớn: Ứng dụng Mobile của họ chạy trên mạng 3G rất giật lag. Khi dùng REST API, để hiển thị một trang cá nhân (News Feed), app phải gọi lên Server hàng chục lần để lấy thông tin Người dùng, lấy Bài viết, lấy Bình luận. Hơn nữa, Server REST trả về một đống dữ liệu thừa thãi không xài tới làm tốn băng thông. Facebook đã tự chế ra **GraphQL**. Khác với REST có 100 đường dẫn (Endpoints) khác nhau, GraphQL CHỈ CÓ ĐÚNG 1 ĐƯỜNG DẪN DUY NHẤT. Quyền lực được trao vào tay Frontend: Frontend chỉ cần gửi một câu lệnh (Query) cực kì chi tiết lên Server: "Cho tôi đúng Tên của user này, và đúng 2 bình luận đầu tiên". Server sẽ ngoan ngoãn gom mọi dữ liệu lại và trả về vừa khít như một miếng ghép Lego.

</details>

> **Summary**: In 2012, Facebook's transition from HTML5 to native Mobile apps exposed the severe limitations of REST architecture on high-latency, low-bandwidth 3G networks. Rendering a complex News Feed required dozens of sequential REST calls (the N+1 under-fetching problem), while simultaneously downloading massive JSON payloads full of irrelevant fields (the over-fetching problem). To solve this, Facebook engineered **GraphQL**. It is a strongly-typed Query Language for your API. It fundamentally shifts the power dynamic from the Backend to the Frontend. Instead of exposing multiple fixed Resource URLs (`/users`, `/posts`), GraphQL exposes exactly ONE endpoint (`/graphql`). The Client constructs a precise JSON-like query detailing the exact shape of the data it requires. The GraphQL server aggregates the data from underlying databases or Microservices and returns a response that perfectly mirrors the Client's query, guaranteeing absolute network efficiency.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đi ăn ở nhà hàng bằng 2 cách:
1. **REST API (Ăn theo Set/Thực đơn cố định)**: Bạn gọi "Combo Số 1". Bạn được bưng ra đúng 1 Đĩa cơm, 1 chén canh, 1 ly nước. Dù bạn không biết uống canh, bạn vẫn phải nhận nó (Over-fetching). Và nếu bạn muốn ăn thêm cục Thịt, bạn không được xin thêm, bạn bắt buộc phải gọi thêm một "Combo Số 2" (Under-fetching). Rất cứng nhắc.
2. **GraphQL (Ăn Buffet tự chọn)**: Bạn cầm một cái mâm (Câu lệnh Query) và đi đến quầy. Bạn tự do chỉ tay: "Cho tôi đúng 2 muỗng cơm, 1 cục thịt, không lấy canh". Nhà bếp sẽ soạn đúng y chang cái mâm đó đưa cho bạn. Bạn chỉ cần đi lấy ĐÚNG 1 LẦN, và mâm cơm của bạn không có bất kì đồ ăn thừa nào.

</details>

Imagine ordering food via a Delivery App.
1. **REST (The Set Menu)**: You order the "Burger Combo". The restaurant rigidly sends you a Burger, Fries, and a Coke. What if you are allergic to Fries? Too bad, they sent them anyway, wasting packaging and weight (Over-fetching). What if you also want Ice Cream? You have to make a completely separate phone call, pay a second delivery fee, and wait for a second driver (Under-fetching / N+1 Problem).
2. **GraphQL (The Custom Order)**: You send a highly specific text message: `Order: { Burger { no_onions, extra_cheese }, Ice_Cream { flavor: vanilla } }`. The kitchen receives this exact graph of your desires, packages it all into one single bag, and a single delivery driver brings it to you. You get exactly what you asked for in a single trip.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

GraphQL xoay quanh 3 khái niệm cốt lõi:
1. **Schema & Type System (Bản vẽ cấu trúc)**: Backend phải khai báo một bản vẽ (Schema) cực kì chặt chẽ. Ví dụ: Khai báo `User` thì có `id` là số (Int), `name` là chữ (String). Nếu Frontend xin một trường không có trong bản vẽ, GraphQL sẽ lập tức báo lỗi ngay từ cửa.
2. **Query & Mutation (Đọc và Ghi)**: 
   - `Query` dùng để Lấy dữ liệu (Giống lệnh GET của REST).
   - `Mutation` dùng để Sửa/Xóa/Thêm dữ liệu (Giống POST, PUT, DELETE).
3. **Resolvers (Người đi nhặt dữ liệu)**: Khi Frontend xin `User` và `Posts` của User đó trong cùng 1 câu Query. Backend sẽ có các hàm nhỏ gọi là Resolvers. Hàm Resolver A chạy đi hỏi Postgres lấy User, hàm Resolver B chạy đi hỏi MongoDB lấy Posts. Cuối cùng GraphQL tự gom 2 cái đó lại thành 1 cục JSON ném về cho Frontend.

</details>

GraphQL replaces HTTP Verbs with a structured Query Language underpinned by a strict Type System.
1. **The Schema (Strong Typing)**: The foundation of GraphQL. The Backend explicitly defines a Schema using Schema Definition Language (SDL). It maps out every accessible Object (e.g., `User`, `Post`), their fields, and strictly defines their data types (`String`, `Int`, `Boolean`). This acts as an iron-clad contract between Frontend and Backend.
2. **Queries & Mutations**: REST uses GET/POST/PUT/DELETE. GraphQL uses exactly ONE HTTP Method (usually `POST`). The intention is defined inside the payload.
   - `Query`: Fetches data without side-effects (Idempotent).
   - `Mutation`: Modifies data on the server (Creates, Updates, Deletes).
3. **Resolvers**: The actual backend code. When a Client queries `{ user { name, posts { title } } }`, the GraphQL engine parses the AST (Abstract Syntax Tree) and invokes specific Functions called `Resolvers`. One resolver fetches the User from PostgreSQL. Another resolver fetches the Posts from a Microservice. GraphQL automatically aggregates the results into a single cohesive JSON response.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

GraphQL sinh ra để giải phóng Frontend khỏi sự lệ thuộc vào Backend.
Khi dùng REST: Màn hình điện thoại có thiết kế mới, cần thêm hiển thị "Số lượt Thích". Lập trình viên Frontend phải chạy sang xin Backend: "Anh ơi thêm hộ em trường Số lượt Thích vào API `/posts` nhé". Backend bận rộn, bắt chờ 1 tuần. Mâu thuẫn nội bộ xảy ra.
Khi dùng GraphQL: Backend chỉ cần phơi bày (Expose) toàn bộ cấu trúc Database ra bằng Schema một lần duy nhất. Từ đó về sau, Frontend muốn hiển thị gì thì TỰ VIẾT câu Query ghép lại. Không cần phải xin phép Backend làm thêm API mới nữa. Tốc độ phát triển sản phẩm của Frontend tăng lên gấp 10 lần.

</details>

GraphQL exists to solve the **Frontend-Backend Coupling** and maximize iteration velocity.
In REST architectures, the Backend dictates the shape of the data. If the UI/UX design changes, and the Mobile app now needs to display the User's "Total Followers" on the homepage, the Frontend team is blocked. They must submit a ticket to the Backend team to update the `/api/users` endpoint or create a new one. This cross-team dependency drastically slows down feature delivery.
GraphQL implements **Declarative Data Fetching**. The Backend builds a comprehensive Graph of all possible data relationships once. The Frontend is then fully empowered. If the UI changes tomorrow, the Frontend developer simply adds the `totalFollowers` field to their GraphQL query. The UI is updated instantly. The Backend team doesn't have to write a single line of new code. It completely decouples Frontend evolution from Backend API maintenance.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình lấy dữ liệu: "Lấy User số 1, và tên của 2 người bạn của User đó".
</details>

Visualizing Data Fetching (REST vs GraphQL).

| Metric | REST API (Under-fetching / Waterfall) | GraphQL API (Single Round-Trip) |
|---|---|---|
| **The Network Calls** | Call 1: `GET /users/1` (Wait 200ms)<br>Call 2: `GET /users/1/friends` (Wait 200ms) | Call 1: `POST /graphql` (Wait 200ms) |
| **Payload Output**| Receives 50 useless fields (Address, DoB) that the UI doesn't need (Over-fetching). | Receives EXACTLY what was requested: <br>`{ "user": { "name": "A", "friends": [{"name": "B"}] } }` |
| **Total Latency** | 400ms (Waterfall latency) | **200ms** (Parallelized backend fetching) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Ứng dụng Mobile và Mạng chậm**: Đây là "Thánh địa" của GraphQL. Các app di động (như Facebook, Twitter) cần tiết kiệm từng KB băng thông và pin. Việc tự định nghĩa dữ liệu để tải về 1 lần duy nhất giúp App mượt mà hơn rất nhiều.
2. **API Gateway (Gom dữ liệu từ Microservices)**: Cực kì phổ biến trong nội bộ công ty. Bạn có Dịch vụ Khách hàng (Java), Dịch vụ Đặt hàng (Go), Dịch vụ Kế toán (Node). Thay vì Frontend phải gọi 3 nơi, người ta xây một cổng GraphQL (Apollo Federation) ở giữa. Frontend hỏi GraphQL, GraphQL sẽ tự động xé câu hỏi ra, đi thu gom ở 3 Microservice kia rồi trả về cho Frontend.
3. **Các Hệ thống có UI thay đổi liên tục**: Các nền tảng E-commerce với giao diện thay đổi theo từng đợt Sale, hoặc các Dashboard cần tùy biến hiển thị cao.

</details>

1. **Mobile Applications & Low-Bandwidth IoT**: The original motivation for GraphQL. Mobile devices operating on spotty 3G/LTE connections suffer exponentially from network round-trips. GraphQL ensures that the Mobile app makes exactly one HTTP request and downloads the absolute minimum byte-size required to paint the screen, saving user data plans and battery life.
2. **Microservice Aggregation (BFF - Backend For Frontend)**: In massive Microservice architectures, exposing 50 different backend services to the Frontend is messy. The industry standard is deploying a GraphQL API Gateway (like Apollo Federation). The Gateway acts as an aggregator. The Frontend sends one massive query. The Gateway breaks it apart, concurrently fetches data from the Java Billing Service and the Go Inventory Service, merges the JSON, and sends it back.
3. **Rapid UI Iteration (High-Velocity Startups)**: Startups that constantly A/B test UI designs. Because the Frontend controls the data fetching, UX engineers can completely redesign the page, adding or removing data fields at will, without ever requesting an API change from the Backend team.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Vấn đề N+1 ở Backend (DataLoader)**: GraphQL giải quyết N+1 cho Frontend, nhưng nó lại tạo ra N+1 ở Backend. Nếu Frontend xin 10 User và Bài viết của 10 User đó. GraphQL ở Backend sẽ ngốc nghếch chạy 1 lệnh SQL lấy 10 User, rồi tiếp tục chạy 10 lệnh SQL khác nhau để lấy Bài viết của từng người. Database sẽ sập. *Bắt buộc phải dùng thư viện `DataLoader` để gom 10 câu lệnh SQL đó lại thành 1 câu duy nhất (Dùng `IN (1,2..10)`)*.
2. **Giới hạn Độ sâu (Query Depth Limit)**: Hacker có thể phá sập Server GraphQL của bạn bằng cách gửi câu Query đệ quy lồng nhau: "Lấy User, lấy Bạn của User, lấy Bạn của Bạn của User..." (Lồng 100 lần). Server sẽ tính toán tới cháy máy và sập. *Phải luôn cấu hình chặn độ sâu của Query (Max Depth = 5).*

</details>

1. **Solving the Backend N+1 Problem (DataLoader)**: The most critical architectural flaw of naive GraphQL implementations. While GraphQL fixes N+1 network calls for the Client, it shifts the problem to the Backend Database. If a Client queries 10 Users and their Friends, the GraphQL execution engine will trigger the User Resolver once, and then trigger the Friend Resolver 10 separate times sequentially, hammering the Database with 11 SQL queries. **Absolute Rule**: You MUST utilize the **DataLoader** utility pattern. DataLoader acts as a batching mechanism. It waits 2 milliseconds, collects all 10 individual SQL queries, and batches them into a single efficient query (`SELECT * FROM friends WHERE user_id IN (1,2,3...10)`).
2. **Defending Against Query Complexity (Max Depth & Cost Analysis)**: Because the Client dictates the Query, a malicious actor can craft a deeply nested recursive query to execute a Denial of Service (DoS) attack. Example: `query { author { posts { comments { author { posts ... } } } } }`. The Backend will exhaust CPU trying to resolve this infinite loop. **Rule**: Always configure a GraphQL Firewall. Enforce a Strict **Max Depth Limit** (e.g., maximum 5 levels deep) and implement **Query Cost Analysis** (assigning a "point value" to each field and rejecting queries that exceed 1000 points).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khó dùng Cache mạng (CDN)**: Ở REST, đường dẫn là `GET /users/1`, bạn có thể dùng Cloudflare (CDN) để lưu tạm dữ liệu này tại Việt Nam, máy chủ gốc ở Mỹ không cần chạy. Nhưng ở GraphQL, mọi thứ đều chui qua 1 cửa là `POST /graphql` với câu lệnh giấu kín bên trong. Cấu hình Cache của trình duyệt và CDN gần như bị vô hiệu hóa, làm Server luôn phải tự tính toán lại.
2. **Lỗi 200 OK giả mạo**: Ở REST, lỗi xảy ra thì báo mã 404 hoặc 500. Ở GraphQL, dù hệ thống nổ tung, gãy làm đôi, nó VẪN TRẢ VỀ mã `200 OK` ở tầng HTTP. Lỗi được giấu trong cục JSON `{"errors": [...]}`. Việc này làm các công cụ Monitor (Đo lường sức khỏe hệ thống) hoàn toàn bị mù, tưởng hệ thống vẫn bình thường.

</details>

1. **The HTTP Caching Nightmare**: REST is intrinsically designed to leverage the HTTP protocol. A `GET /posts/5` is universally recognized by Browser Caches and CDN Edge nodes (Cloudflare) as highly cacheable. GraphQL exclusively utilizes `POST /graphql`. According to HTTP standards, `POST` requests are non-idempotent and strictly non-cacheable. Therefore, traditional network-level caching is entirely broken. **Fix**: You must implement complex Application-level caching (like Apollo Client Cache) or utilize Automated Persisted Queries (APQ) to convert safe queries into cacheable GET requests.
2. **False `200 OK` Errors & Monitoring Blindness**: Standard REST utilizes HTTP Status codes semantically (404, 500). In standard GraphQL over HTTP, virtually every single request returns an HTTP `200 OK`, even if the entire database resolution failed violently. The actual errors are nested inside the JSON payload: `{ "data": null, "errors": [{ "message": "DB Crash" }] }`. This breaks standard DevOps infrastructure (Datadog, Prometheus, Nginx logs), which rely on HTTP status codes to trigger alerts. You must configure custom GraphQL-aware monitoring middleware to detect these "soft" failures.

---

## Related Topics

- For internal Microservice-to-Microservice communication where JSON parsing is too slow, do not use GraphQL; use **[gRPC](./grpc.md)**.
- For public APIs intended for third-party developers, standard **[REST APIs](./rest.md)** remain heavily preferred.
- GraphQL backend servers are incredibly popular in the Node.js ecosystem. See **[Node.js / Express](../backend/nodejs-express.md)** (Apollo Server).
