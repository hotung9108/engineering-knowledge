# REST APIs (Representational State Transfer)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước những năm 2000, các máy chủ giao tiếp với nhau bằng những phương thức cực kì lằng nhằng và cồng kềnh (như SOAP/XML). Roy Fielding đã viết ra **REST** để thay đổi hoàn toàn Internet. REST không phải là một công nghệ hay một thư viện bạn có thể tải về; nó là một **Phong cách Kiến trúc** (Architectural Style). Cốt lõi của REST nằm ở chữ "Tài nguyên" (Resource). Thay vì tạo ra các đường dẫn hành động (ví dụ: `POST /LayThongTinNguoiDung`), REST ép bạn dùng chung các hành động chuẩn của HTTP (GET, POST, PUT, DELETE) lên một Danh từ duy nhất (ví dụ: `GET /users`). Nhờ sự đơn giản, không lưu trạng thái (Stateless) và chuẩn hóa này, REST đã trở thành ngôn ngữ giao tiếp mặc định của 99% các dịch vụ Web trên toàn thế giới.

</details>

> **Summary**: Prior to the year 2000, network communication was dominated by heavy, complex protocols like SOAP and XML-RPC, which treated the web simply as a transport layer for executing remote code. **REST (Representational State Transfer)**, introduced by Roy Fielding, revolutionized this. REST is not a protocol; it is a strict **Architectural Style**. It mandates that the web should be operated based on *Resources* (Nouns) rather than *Actions* (Verbs). Instead of creating arbitrary endpoints like `/CreateNewUser`, developers map standard HTTP Methods (`GET`, `POST`, `PUT`, `DELETE`) directly to standard Resource URLs (`/users`). Because it is inherently Stateless, highly cacheable, and universally supported by every HTTP client in existence, REST remains the absolute gold standard for building public-facing web APIs.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn điều khiển một con Robot Quản gia.
1. **Cách cũ (Không dùng REST)**: Bạn phải chế ra hàng chục nút bấm với tên gọi lộn xộn: Nút `BatTivi()`, nút `TatTivi()`, nút `SuaKenhTivi()`. Người khác nhìn vào cái điều khiển sẽ không hiểu gì cả.
2. **Cách dùng REST**: Bạn có đúng 4 nút bấm chuẩn hóa (GET, POST, PUT, DELETE) và một cái màn hình để điền tên Đồ vật (Resource). 
   - Bạn muốn lấy Tivi? Chọn nút **GET**, điền **Tivi** $\rightarrow$ Robot mang Tivi ra.
   - Bạn muốn mua Tivi mới? Chọn nút **POST**, điền **Tivi** $\rightarrow$ Robot đi mua cái Tivi mới mang về.
   - Bạn muốn vứt Tivi? Chọn nút **DELETE**, điền **Tivi** $\rightarrow$ Robot ném Tivi đi.
Mọi thứ cực kì rõ ràng, chuẩn mực và dễ hiểu.

</details>

Imagine controlling a Smart Home System.
1. **RPC / Old Way (Verbs)**: You have a control panel with 50 completely random buttons. `TurnOnLight()`, `ExtinguishLight()`, `MakeLightBrighter()`. A new user has to read a manual to memorize what every single button does.
2. **RESTful Way (Nouns + Standard Methods)**: You only have 4 standardized buttons (`GET`, `POST`, `PUT`, `DELETE`) and a target selector (`/lights/bedroom`). 
   - To check the light status: Press **GET** on `/lights/bedroom`.
   - To install a new light: Press **POST** to `/lights`.
   - To smash the lightbulb: Press **DELETE** on `/lights/bedroom`.
Because the rules are universally standardized, any developer in the world instantly knows how to operate your Smart Home without reading a 100-page manual.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Một API được gọi là "Chuẩn REST" (RESTful) nếu nó tuân thủ 5 nguyên tắc:
1. **Client-Server**: Tách biệt hoàn toàn Frontend (Giao diện) và Backend (Dữ liệu).
2. **Stateless (Không lưu trạng thái)**: Đây là nguyên tắc quan trọng nhất. Backend bị "Mất trí nhớ". Lần 1 bạn gọi `GET /profile` kèm thẻ ID của bạn. Lần 2 bạn gọi `PUT /profile`, bạn VẪN PHẢI GỬI LẠI thẻ ID đó. Backend không nhớ bạn là ai từ cuộc gọi trước. (Giúp Backend không bị quá tải bộ nhớ).
3. **Cacheable (Khả năng lưu đệm)**: Backend có thể dán nhãn "Dữ liệu này không đổi trong 1 tiếng". Frontend sẽ tự động không gọi API lại nữa mà lấy dữ liệu từ bộ nhớ tạm.
4. **Uniform Interface (Giao diện chuẩn hóa)**: Dùng đúng các hàm của HTTP. `GET` để Đọc. `POST` để Tạo. `PUT` để Cập nhật toàn bộ. `PATCH` để Cập nhật một phần. `DELETE` để Xóa. Mọi URL phải là Danh từ số nhiều (Ví dụ: `/users`, `/products`).
5. **Layered System**: Frontend không cần biết nó đang kết nối thẳng tới Server hay đang kết nối qua một cái Cổng trung gian (Load Balancer).

</details>

For an API to be considered truly "RESTful", it must strictly adhere to specific architectural constraints:
1. **Client-Server Separation**: The User Interface concerns (Frontend) must be decoupled from the Data Storage concerns (Backend), allowing them to evolve independently.
2. **Statelessness (The Most Critical Rule)**: The Server executes every single HTTP request in total isolation. The Server does NOT store a "Session" in its memory mapping to the client. Therefore, every single request from the Client MUST contain all the authentication tokens and context necessary to execute it. This makes horizontally scaling the Backend trivial.
3. **Cacheability**: Responses must implicitly or explicitly define themselves as cacheable or not (via HTTP Headers like `Cache-Control`).
4. **Uniform Interface (Resource-Based URLs)**: The API utilizes standard HTTP verbs to manipulate Resources. Resources are represented by plural nouns (e.g., `/articles`, `/users`). Verbs are NEVER used in the URL.
5. **Layered System**: The Client cannot tell if it is connected directly to the end server, or to an intermediary load balancer or CDN.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trước REST, người ta dùng SOAP (Gửi thư bằng file XML). SOAP quá rườm rà. Bạn muốn hỏi "User 1 tên gì?", bạn phải gửi 1 file XML dài 50 dòng, gói ghém hàng tá thông tin thừa thãi.
Khi Internet bùng nổ, Mobile App xuất hiện, các lập trình viên cần một thứ Gọn nhẹ, Nhanh và Dễ hiểu.
REST sinh ra vì nó tận dụng LUÔN cái nền tảng HTTP đang có sẵn của Internet. Nó đẩy cục dữ liệu JSON bé xíu đi qua mạng. Quan trọng hơn, REST tạo ra một "Tiếng lóng" chung. Nếu tôi là công ty A, bạn là công ty B, chúng ta chưa từng gặp nhau. Bạn chỉ cần đưa tôi cái link `GET /api/v1/orders`, tôi nhắm mắt cũng biết lệnh đó dùng để Lấy danh sách Đơn hàng. Tính tiêu chuẩn hóa là vũ khí mạnh nhất của REST.

</details>

REST exists to provide **Universality** and **Simplicity** to distributed systems.
In the SOAP/XML era, integrating two enterprise systems required reading massive WSDL (Web Services Description Language) documents and utilizing specialized SOAP clients just to parse the rigid XML envelopes. It was computationally heavy and incredibly frustrating for developers.
REST gained absolute dominance because it leverages the native mechanisms of the Web (HTTP protocol). It utilizes lightweight JSON payloads instead of verbose XML. More importantly, it established a Universal Convention. If a developer joins a new company and sees the endpoint `DELETE /api/users/88`, they instantly know what it does without reading a single line of documentation. This standardization drastically reduced integration times across the global tech industry.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cách thiết kế Đường dẫn (URL) giữa kiểu tùy tiện (RPC) và kiểu chuẩn REST.
</details>

Visualizing Endpoint Design (RPC vs REST).

| Action | Poor API Design (RPC / Verb-Based) | Professional REST API (Noun-Based) |
|---|---|---|
| **Get all users** | `GET /getAllUsers` | `GET /users` |
| **Get user #5** | `POST /getUser?id=5` | `GET /users/5` |
| **Create a user** | `POST /createNewUser` | `POST /users` (Pass JSON body) |
| **Update user #5** | `POST /updateUserXYZ` | `PUT /users/5` (Pass JSON body) |
| **Delete user #5** | `GET /deleteUser?id=5` (Very dangerous!) | `DELETE /users/5` |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Public APIs (OpenAPI / Dịch vụ bên thứ ba)**: Bất kì công ty nào muốn cho người khác xài ké dữ liệu của mình đều dùng REST. Stripe (Cổng thanh toán), Twilio (Gửi SMS), hay GitHub API. Nếu họ dùng gRPC hay công nghệ lạ, không ai biết cách tích hợp.
2. **Web Applications (SPA)**: Các trang web thông thường viết bằng React, Vue, Angular kết nối tới Backend Node.js / Spring Boot. (Ví dụ: Các hệ thống quản trị Admin Dashboard, CMS).
3. **Ứng dụng CRUD đơn giản**: Các ứng dụng thiên về Thêm, Sửa, Xóa, Đọc dữ liệu (Tạo bài viết, Quản lý sinh viên, Phần mềm kế toán) sinh ra là để dành cho REST.

</details>

1. **Public/Partner APIs (B2B Integrations)**: The undisputed realm of REST. If Stripe or GitHub built their public-facing APIs using gRPC, they would severely alienate thousands of developers who don't know how to compile Protocol Buffers. REST over HTTP/JSON guarantees that a developer can test the API using nothing but their terminal (`curl`) or Postman.
2. **Standard Web Applications (SPAs)**: Dashboards, Content Management Systems (CMS), and B2B SaaS platforms. Frontend frameworks (React, Vue) utilize standard `fetch()` or `axios` libraries to effortlessly consume RESTful endpoints from backend services (Node.js/Spring Boot).
3. **CRUD-Heavy Systems**: Applications where the primary operations perfectly map to Create, Read, Update, and Delete paradigms (e.g., Inventory Management, HR Portals, Blogging platforms).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Phiên bản hóa API (Versioning)**: LUÔN LUÔN thêm `v1` vào đường dẫn URL (ví dụ: `api/v1/users`). Sau 1 năm, bạn đập đi xây lại hệ thống, bạn đổi cấu trúc dữ liệu. Nếu bạn đè lên URL cũ, toàn bộ App Mobile của người dùng chưa kịp cập nhật sẽ bị sập (Crash) ngay lập tức. Bạn phải giữ URL cũ và tạo ra `api/v2/users`.
2. **Luôn sử dụng đúng HTTP Status Codes**: Không bao giờ trả về lỗi hệ thống nhưng lại để Mã trạng thái là `200 OK`. 
   - `200`: Thành công. `201`: Tạo thành công.
   - `400`: Khách hàng truyền sai dữ liệu. `401`: Chưa Đăng nhập. `403`: Không có quyền. `404`: Không tìm thấy.
   - `500`: Server bị sập (Lỗi do Coder Backend).
3. **Phân trang (Pagination) và Lọc (Filtering)**: Không bao giờ trả về 1 triệu dòng dữ liệu từ lệnh `GET /users`. Phải bắt buộc khách hàng dùng Query Parameters: `GET /users?limit=20&page=1&role=admin`.

</details>

1. **Mandatory Versioning (URL or Headers)**: The most catastrophic mistake in public API design is breaking backwards compatibility. If your mobile app relies on `GET /api/users`, and you deploy a backend change that renames the `fullName` field to `firstName` and `lastName`, every single mobile app in the world immediately crashes. **Rule**: Always version your APIs from Day 1 (`/api/v1/users`). When a breaking change occurs, release `/api/v2/users` while explicitly maintaining `v1` for legacy clients.
2. **Strict Adherence to HTTP Status Codes**: Do not return an HTTP `200 OK` with a JSON body saying `{"error": "User Not Found"}`. This breaks standard HTTP clients and caching mechanisms.
   - `2xx`: Success (`200 OK`, `201 Created`, `204 No Content`).
   - `4xx`: Client Errors (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`).
   - `5xx`: Server Errors (`500 Internal Server Error` - Your code crashed).
3. **Pagination & Query Parameters**: Never execute an unbounded `SELECT *` via a REST endpoint (`GET /orders`). Always enforce pagination via Query Strings (`GET /orders?page=1&size=50&sort=-createdAt`).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hội chứng Under-fetching (Gọi API quá nhiều lần)**: Ở màn hình Trang chủ, bạn cần hiển thị "Danh sách Bài viết, kèm Tên người đăng, và 3 Comment mới nhất". Nếu bạn cứng nhắc dùng REST chuẩn: Đầu tiên bạn gọi `GET /posts`. Sau đó bạn dùng vòng lặp chạy 10 lần gọi `GET /users/id` để lấy tên tác giả. Rồi gọi 10 lần `GET /posts/id/comments` để lấy bình luận. Màn hình của bạn phải chờ 21 cuộc gọi mạng liên tiếp mới hiển thị xong. Cực kì giật lag! (Đây là lúc nên dùng GraphQL).
2. **Lộ lọt dữ liệu (Over-fetching)**: Khi làm tính năng "Hiển thị tên người dùng", Frontend gọi `GET /users/1`. Backend lười biếng, `SELECT *` và trả về toàn bộ dữ liệu của User đó, bao gồm cả Password Hash, Căn cước công dân. Cực kì nguy hiểm. Backend phải luôn lọc dữ liệu trước khi ném ra ngoài REST.

</details>

1. **The N+1 Problem (Under-fetching)**: The fundamental weakness of REST in relational data UI. A UI component needs a list of 10 Orders, their associated Customer Names, and the Product Details of each item. In pure REST, the client calls `GET /orders` (1 call), then loops through the orders to call `GET /customers/:id` (10 calls), then calls `GET /products/:id` (maybe 30 calls). This waterfall of 41 sequential HTTP network requests causes catastrophic UI latency. (Solution: Backend custom aggregations like `/orders?include=customer,products`, or migrate to GraphQL).
2. **Accidental Data Leakage (Over-fetching)**: A mobile app needs a list of Usernames for a Leaderboard. It calls `GET /users`. The backend developer naively executes `SELECT * FROM users` and serializes the entire Object to JSON. The mobile app only displays the Username, but a malicious actor intercepting the network sees the JSON payload contains `password_hash`, `email`, and `admin_role`. **Rule**: Always utilize Data Transfer Objects (DTOs) in your backend to explicitly whitelist exactly which fields are exposed to the REST response.

---

## Related Topics

- For building REST APIs, you need a Backend framework like **[Node.js / Express](../backend/nodejs-express.md)** or **[Go](../backend/go.md)**.
- If REST's N+1 problem is slowing down your Frontend, explore **[GraphQL](./graphql.md)**.
- If your REST APIs are too slow for internal Microservice-to-Microservice calls, use **[gRPC](./grpc.md)** instead.
