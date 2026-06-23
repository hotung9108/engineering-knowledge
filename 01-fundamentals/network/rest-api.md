# REST API: REpresentational State Transfer

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hai cái máy tính (Frontend và Backend) muốn nói chuyện với nhau, chúng không thể gọi miệng được. Chúng cần một tập hợp các quy tắc chuẩn mực. **REST API** là tập hợp các quy tắc thiết kế nổi tiếng nhất thế giới để máy tính giao tiếp qua mạng Internet bằng giao thức HTTP. Nó quy định cách đặt tên đường dẫn (URL) sao cho có ý nghĩa, và cách sử dụng các Động từ HTTP (GET, POST) thay vì tự chế ra các lệnh hỗn loạn.

</details>

> **Summary**: When disparate software systems (e.g., a React Frontend and a Java Backend) communicate over a network, they cannot merely scream random text streams at each other. They demand a rigid, architectural contract. **REST (REpresentational State Transfer)** is the globally dominant architectural paradigm governing web APIs. Built entirely upon the HTTP protocol, REST enforces standardized conventions: semantic URL endpoint naming, strict utilization of HTTP Verbs (GET, POST, PUT, DELETE), and stateless architectural design, eradicating chaotic custom RPC protocols.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn gọi điện đến một Thư viện để mượn sách.
- **Không có REST (Thiết kế hỗn loạn)**: Bạn muốn mượn sách, bạn gọi đường dây số 1 (Đường dẫn `/lay-sach`). Lát sau bạn muốn trả sách, bạn phải tìm gọi đường dây số 2 (Đường dẫn `/tra-sach-nhe`). Hệ thống có hàng ngàn đường dây lộn xộn.
- **Có REST (Thiết kế chuẩn mực)**: Chỉ có ĐÚNG 1 đường dây duy nhất gọi là `/books`.
  - Bạn muốn xem danh sách sách? Bạn hét lên: **GET** `/books`!
  - Bạn muốn thêm cuốn sách mới? Bạn hét lên: **POST** `/books`!
  - Bạn muốn xóa cuốn sách số 5? Bạn hét lên: **DELETE** `/books/5`!
Cách thiết kế này làm cho lập trình viên trên toàn thế giới đều dễ dàng hiểu nhau mà không cần đọc hướng dẫn sử dụng dài dòng.

</details>

Imagine phoning a colossal Public Library.
- **Anti-REST (Chaotic RPC Architecture)**: You want to borrow a book, so you must call a specific phone extension (Endpoint `/borrow-book-now`). Later, to return it, you must memorize a completely different extension (`/execute-book-return-procedure`). A system scaling to thousands of operations yields thousands of chaotic, unmemorable extensions.
- **REST Architecture (Standardized Verbs)**: There is exactly *one* universal phone extension for all book-related operations: `/books`.
  - To view the catalog, you shout the HTTP Verb: **`GET /books`**!
  - To donate a new book, you shout: **`POST /books`**!
  - To permanently incinerate book #42, you shout: **`DELETE /books/42`**!
This semantic structure allows software engineers globally to intuitively guess the API design without reading massive, convoluted manuals.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

REST không phải là Code, nó là **Cách đặt tên**. Một API được gọi là "Chuẩn RESTful" khi nó tuân thủ các quy tắc sau:
1. **Dùng Động từ HTTP (HTTP Methods)**: 
   - `GET`: Chỉ để ĐỌC dữ liệu (Lấy về).
   - `POST`: Để TẠO MỚI một dữ liệu.
   - `PUT / PATCH`: Để CẬP NHẬT/SỬA dữ liệu cũ.
   - `DELETE`: Để XÓA dữ liệu.
2. **URL đại diện cho Danh từ (Resource)**: Đường dẫn KHÔNG ĐƯỢC chứa động từ. Ví dụ sai: `/create-user`. Ví dụ chuẩn REST: `POST /users`.
3. **Stateless (Phi trạng thái)**: Mỗi gói tin gửi lên Backend phải mang theo đủ thẻ căn cước (Token Đăng nhập). Backend không bao giờ nhớ bạn là ai từ gói tin trước. (Không dùng Session).
4. **Trả về dữ liệu thô**: Thường là định dạng JSON (Hoặc XML). Backend không được trả về cục HTML chứa nút bấm giao diện.

</details>

REST is fundamentally an architectural style, not a library or framework. An API is deemed "RESTful" when it adheres to strict architectural constraints:
1. **Semantic HTTP Verbs**: 
   - `GET`: Exclusively for Reading/Fetching (Idempotent).
   - `POST`: Exclusively for Creating new resources.
   - `PUT / PATCH`: Exclusively for Updating/Mutating existing resources.
   - `DELETE`: Exclusively for Destroying resources.
2. **Resource-Based URLs (Nouns, Not Verbs)**: Endpoints must identify *Resources* (Nouns), not actions. Anti-pattern: `POST /create_user`. RESTful standard: `POST /users`.
3. **Stateless Execution**: The server maintains absolutely no client session state between requests. Every single incoming HTTP request must contain all contextual authentication (e.g., a JWT Bearer Token) required to authorize it independently.
4. **Data Representation**: Endpoints do not return rendered HTML User Interfaces. They return pure, raw data representations, overwhelmingly standardized as `application/json`.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Ngày xưa, khi code Web, người ta hay nhét chung UI (Giao diện HTML) và Database Logic vào chung 1 cục code (Monolithic). Khi Mobile App (iOS/Android) bùng nổ, App Mobile không thèm đọc cục HTML đó, nó chỉ cần dữ liệu thô.
REST API sinh ra để tách biệt hoàn toàn Frontend (Trình duyệt, App Mobile) khỏi Backend (Máy chủ).
Backend giờ đây chỉ xây một cái kho chứa dữ liệu chuẩn REST (Chỉ ói ra JSON). Khi đó, cả Web ReactJS, App iOS, App Android đều có thể gõ cửa cái kho đó để xin dữ liệu. Code Backend 1 lần, xài được cho mọi nền tảng!

</details>

Historically, web engineering utilized monolithic frameworks (like PHP or JSP) that forcefully coupled Server-Side Business Logic tightly with UI presentation layers (HTML/CSS). When the Mobile App revolution detonated (iOS/Android), this architecture catastrophically failed; a native iPhone app cannot parse and render raw HTML.
REST API was widely adopted to enforce rigid **Frontend/Backend Decoupling**. 
The Backend is now reduced to a pure Data Vault. It exposes a standardized REST/JSON interface. Consequently, a ReactJS Single Page Application, a Swift iOS App, and a Kotlin Android App can all consume the exact same `/api/v1/users` endpoint simultaneously. Code the Backend once; scale across infinite Client platforms.

---

## Layer 3: Without vs. With Comparison (Compare)

### RPC (Remote Procedure Call) vs. REST API

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt giữa việc tự chế API lộn xộn (RPC) và việc tuân thủ quy chuẩn quốc tế REST.
</details>

Comparing the legacy, chaotic RPC naming convention against modern semantic REST.

| Action Intent | The RPC Anti-Pattern (Chaotic Verbs) | The RESTful Standard (Clean Nouns) |
|---|---|---|
| Read all users | `GET /getAllUsers` | `GET /users` |
| Get one user | `POST /getUserById?id=5` | `GET /users/5` |
| Create a user | `POST /createNewUser` | `POST /users` |
| Update a user | `POST /updateUserNow?id=5` | `PUT /users/5` |
| Delete a user | `GET /deleteUser?id=5` (Very Dangerous) | `DELETE /users/5` |
| Get user's items| `GET /getItemsForUser?userId=5` | `GET /users/5/items` |

*Note: Executing a dangerous mutation (Delete) via a `GET` request in RPC is a massive security/caching vulnerability.*

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Ứng dụng Web / App di động**: REST API (trả về JSON) là lựa chọn số 1 (mặc định) cho 90% dự án làm App gọi xe, Đặt đồ ăn, Mạng xã hội ngày nay.
- **Giao tiếp với Bên thứ 3 (Third-Party Integrations)**: Bạn tích hợp cổng thanh toán Momo/Stripe, gửi tin nhắn SMS qua Twilio, Đăng nhập bằng Google. Bọn họ đều bắt bạn phải gọi vào hệ thống REST API của họ để ra lệnh.
- **Khi nào KHÔNG dùng REST**: Nếu hai Microservices (Backend và Backend) nói chuyện với nhau, REST (bằng Text) bị chê là hơi chậm. Họ sẽ dùng **gRPC** (bằng Nhị phân) để đẩy tốc độ lên tối đa.

</details>

- **Public-Facing Clients (Web/Mobile)**: REST over HTTP is the undisputed global standard for 95% of consumer-facing applications (Ride-hailing, E-Commerce, Social Media). React/Flutter apps natively consume JSON from REST endpoints.
- **Third-Party SaaS Integrations**: Payment Gateways (Stripe, PayPal), Communications (Twilio SMS), and Identity Providers (Google OAuth) exclusively expose Public REST APIs. Integrating with external Enterprise systems practically mandates consuming REST architecture.
- **The Anti-Pattern (When NOT to use REST)**: Internal Microservice Meshes. If Backend Auth Service `A` needs to call Backend Payment Service `B` 10,000 times a second inside a private AWS Subnet, the heavy text-parsing overhead of JSON/REST is inefficient. Elite engineering teams utilize binary protocols like **gRPC** for internal server-to-server communication.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Luôn đánh phiên bản (Versioning) cho API**: Đừng bao giờ tạo đường dẫn kiểu `api.domain.com/users`. Ngày mai bạn đổi logic, cái App cũ của khách hàng (không cập nhật) sẽ nổ tung. BẮT BUỘC chèn phiên bản vào URL: `api.domain.com/v1/users`. Sang năm đổi tính năng mới thì thiết kế `/v2/users`, khách cũ xài bản `v1` vẫn bình yên vô sự.
2. **Dùng đúng Status Code của HTTP**: Trả về Lỗi không được trả về `200 OK` (rồi chèn dòng chữ "Lỗi rồi" trong body JSON). Nếu bị lỗi mã thông báo (Token sai), BẮT BUỘC dùng lệnh trả về mã `401 Unauthorized` của hệ thống mạng.

</details>

1. **Mandatory API Versioning**: Never expose a bare endpoint like `api.bank.com/users`. The moment you introduce a breaking schema change to the JSON response (e.g., renaming `fullName` to `first_name`), you will instantly crash thousands of legacy iOS applications still installed on users' phones. **Always explicitly version endpoints in the URI**: `api.bank.com/v1/users`. When initiating a breaking change, deploy `/v2/`, maintaining `/v1/` indefinitely for backward compatibility.
2. **Strict HTTP Status Code Adherence**: A horrific anti-pattern is returning a successful `HTTP 200 OK` network code, but embedding an error payload inside the JSON (`{ "status": "ERROR", "message": "Invalid password" }`). This destroys caching mechanisms and fundamentally breaks API Gateway observability. If a payload is malformed, aggressively return `HTTP 400 Bad Request`. If unauthorized, strictly return `HTTP 401 Unauthorized`.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **N-1 Query qua mạng (Chatty APIs)**: Để hiển thị 1 trang Profile, App Mobile gọi `/users/1` để lấy tên. Xong nó phải gọi tiếp 10 lần API `/users/1/comments` để lấy comment. Frontend bị treo vì tải quá nhiều lần. Đây là điểm yếu của REST (Over-fetching / Under-fetching). (Giải pháp: Backend phải tạo riêng một Endpoint chuyên biệt trộn sẵn dữ liệu, hoặc chuyển sang xài GraphQL).
2. **Nhầm lẫn PUT và PATCH**: 
   - `PUT`: Cập nhật ĐÈ toàn bộ cục dữ liệu mới lên cục cũ. (Lười biếng, rủi ro).
   - `PATCH`: Chỉ gửi lên vài trường bị thay đổi (Ví dụ: Chỉ đổi Số điện thoại). Gọn gàng và tối ưu hơn.

</details>

1. **The Over-Fetching/Under-Fetching Dilemma (Chatty APIs)**: REST is intrinsically rigid. To render a complex UI Dashboard, a React Frontend might need User Info, Recent Orders, and Unread Notifications. Because REST strictly enforces isolated Resource endpoints, the Frontend is forced to execute 3 separate, heavy HTTP network requests (`/users/1`, `/orders?user=1`, `/notifications`). This severe latency bottleneck is the exact reason Facebook invented **GraphQL** (allowing clients to query massive nested datasets in exactly one single network roundtrip).
2. **Conflating `PUT` and `PATCH`**: 
   - **`PUT`**: Represents full-entity Replacement. You must transmit the *entire* 50-field JSON payload just to change one field. It aggressively overwrites the Database record.
   - **`PATCH`**: Represents partial modification. You only transmit the explicit Delta (e.g., `{"phone": "12345"}`). Using `PUT` when you intended `PATCH` often results in accidentally Nullifying missing fields in the Database.

---

## Related Topics

- REST APIs heavily utilize JSON format. See **[Data Formats](../web-fundamentals/data-formats.md)**.
- For internal microservice communication, REST is often replaced by **[gRPC](./grpc.md)**.
- See how API schemas handle backward compatibility in **[Versioning](../sdlc/versioning.md)**.
