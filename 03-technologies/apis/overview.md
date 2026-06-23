# APIs Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: API (Application Programming Interface) là Ngôn ngữ giao tiếp của Internet. Nếu Database là não bộ, Message Broker là hệ thần kinh, thì API chính là "Cái miệng" và "Đôi tai" của hệ thống. Nó cho phép hai phần mềm hoàn toàn xa lạ (ví dụ: Điện thoại iOS của khách hàng và Máy chủ Backend viết bằng Java) nói chuyện và hiểu được nhau thông qua một bộ quy tắc chung. Lịch sử của API là một cuộc tiến hóa liên tục nhằm giải quyết bài toán: Làm sao để truyền dữ liệu qua mạng nhanh hơn, chính xác hơn và linh hoạt hơn. Hành trình này bắt đầu từ SOAP già cỗi, tiến đến kỷ nguyên vàng của **REST**, và hiện tại đang rẽ nhánh thành hai thế lực chuyên biệt: **GraphQL** (cho sự linh hoạt tuyệt đối của Frontend) và **gRPC** (cho tốc độ sấm sét giữa các Microservices).

</details>

> **Summary**: An API (Application Programming Interface) defines the strict contracts and protocols through which disparate software systems communicate over a network. Without APIs, the modern web—where an iOS app written in Swift requests data from a Python backend to display on a React dashboard—would be impossible. APIs abstract away internal database complexity, exposing only secure, defined endpoints to external clients. The architectural evolution of APIs reflects the industry's shifting priorities: moving from the rigid XML-heavy SOAP protocols of the 2000s, to the ubiquitous, resource-oriented **REST** (Representational State Transfer) architecture, and recently branching into highly specialized paradigms like **GraphQL** (solving Over-fetching for mobile clients) and **gRPC** (solving latency and payload size for backend-to-backend Microservice communication).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (Frontend) đi ăn tại một nhà hàng (Backend/Database).
Bạn không thể tự đi vào Bếp (Database), tự mở tủ lạnh, xào nấu rồi lấy thức ăn ra. Bạn có thể làm cháy quán hoặc ăn cắp đồ.
Thay vào đó, quán có một người Bồi bàn (API). 
1. Người bồi bàn đưa cho bạn cái Menu (API Documentation). Menu nói rõ: "Bạn chỉ được gọi 3 món: Phở, Cơm, Bún. Nếu bạn gọi Pizza, tôi sẽ báo lỗi".
2. Bạn đọc Menu và gọi món: "Cho tôi 1 tô Phở" (HTTP Request).
3. Bồi bàn mang yêu cầu vào Bếp, Bếp nấu xong đưa Bồi bàn. Bồi bàn bưng tô Phở ra cho bạn (HTTP Response).
Người Bồi bàn (API) là người trung gian, bảo vệ an toàn cho Nhà bếp, và giúp bạn có đồ ăn mà không cần biết cách nấu.

</details>

Imagine dining at a Restaurant.
1. **The Client (Frontend App)**: You, sitting at the table, hungry for data.
2. **The Kitchen (Backend Database)**: The highly secured, complex environment where the actual food (Data) is stored and cooked. You are strictly forbidden from entering the kitchen directly.
3. **The API (The Waiter)**: The API is the Waiter. The Waiter hands you a Menu (API Documentation) that strictly defines exactly what you are allowed to ask for. You give your order (The HTTP Request) to the Waiter. The Waiter takes it to the kitchen, ensures it's safe to cook, waits for the food, and brings the exact plate (The HTTP Response / JSON) back to your table. You don't need to know *how* the chef cooked the food; you only need to know how to talk to the Waiter.

---

## Layer 1: The Evolution of APIs (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thế giới API được chia làm 3 kiến trúc chính, mỗi cái giải quyết một bài toán riêng:
1. **REST (Kẻ Thống Trị)**: Là tiêu chuẩn vàng hiện tại. Nó dựa trên chuẩn HTTP (GET, POST, PUT, DELETE). Mọi thứ xoay quanh "Tài nguyên" (Resource) và các đường dẫn URL (ví dụ: `GET /users/1`). Dễ học, dễ dùng, nhưng cứng nhắc.
2. **GraphQL (Sự Linh Hoạt)**: Sinh ra bởi Facebook để cứu cánh cho App Mobile mạng yếu. Thay vì phải gọi 3 API REST để lấy thông tin Người dùng, Bài viết, và Bình luận. GraphQL cho phép Frontend gửi 1 câu hỏi cực kì chi tiết: "Cho tôi đúng Tên người dùng và 2 bình luận đầu tiên". Backend sẽ trả về ĐÚNG hình thù dữ liệu đó. Không thừa 1 chữ, không thiếu 1 chữ.
3. **gRPC (Tốc độ Ánh Sáng)**: Sinh ra bởi Google. Thay vì gửi dữ liệu dạng chữ (JSON) rất bự và cồng kềnh. gRPC nén dữ liệu thành mã nhị phân (Binary - Protobuf) và gửi qua kết nối HTTP/2 siêu tốc. Thường không dùng cho Frontend, mà dùng để các Máy chủ Backend nói chuyện nội bộ với nhau nhanh gấp 10 lần REST.

</details>

The API landscape is dominated by three primary architectural paradigms:
1. **REST (Representational State Transfer)**: The undisputed standard of the modern web. It maps standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) to CRUD operations on URLs representing specific Resources (`/api/users/123`). It is stateless, cacheable, and universally understood. However, it suffers from rigid endpoints leading to Over-fetching (returning more data than needed) or Under-fetching (requiring multiple round-trips).
2. **GraphQL**: Invented by Facebook to solve REST's inefficiencies on slow mobile networks. It exposes a *single* endpoint (`/graphql`). The Client dynamically dictates exactly what data shapes it needs via a Query Language. It guarantees the Frontend receives exactly what it asked for—nothing more, nothing less—drastically reducing network payload size and eliminating multiple round-trips.
3. **gRPC (gRPC Remote Procedure Calls)**: Engineered by Google. It Abandons human-readable JSON payloads entirely. It uses Protocol Buffers (Protobuf) to serialize data into highly compressed Binary formats, transmitted over multiplexed HTTP/2 streams. Because Browsers struggle with raw HTTP/2 binary frames, gRPC is strictly utilized for ultra-low latency, internal Server-to-Server (Microservice) communication, offering 10x the performance of REST.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vì sao chúng ta không dùng chung 1 loại API cho khỏe?
Bởi vì "Không có viên đạn bạc" trong lập trình.
- Nếu bạn làm một cái Web bán hàng bình thường, **REST** là quá đủ. Mọi lập trình viên đều hiểu nó ngay lập tức.
- Nhưng khi App Shopee trên điện thoại của bạn chạy bằng mạng 3G chậm chạp, việc tải dư thừa cục JSON 5MB (chứa toàn những trường dữ liệu mà màn hình không hiển thị) là một thảm họa. **GraphQL** sinh ra để Frontend tự gọt tỉa dữ liệu còn đúng 50KB, giúp App chạy mượt mà.
- Lại nói về nội bộ Máy chủ. Dịch vụ Đặt hàng phải hỏi Dịch vụ Tồn kho hàng trăm ngàn lần mỗi giây. Việc cứ phải Dịch chữ JSON sang Object mất rất nhiều thời gian CPU. **gRPC** nhét thẳng mã Nhị phân vào, hai máy chủ không cần dịch chữ nữa, đọc phát hiểu ngay, giảm độ trễ xuống mức mili-giây.
Mỗi công cụ sinh ra để lấp đầy điểm yếu của công cụ kia.

</details>

Why do we need multiple API paradigms? Because the networking constraints of different environments vary wildly.
1. **The Public Integration Constraint (REST)**: If you are building a public API for third-party developers (like Stripe or GitHub APIs), you must use the most universally understood standard. REST is ubiquitous. Every language has an HTTP client. It is the language of the Internet.
2. **The Mobile Bandwidth Constraint (GraphQL)**: On a 3G mobile connection, network latency (Round-Trip Time) is the enemy. Making 4 sequential REST calls to render a User Profile takes 4 seconds. Furthermore, the REST endpoints might return massive 500KB JSON payloads containing timestamps and metadata the UI doesn't render. GraphQL exists so the Mobile client can say: "Send me exactly `Name` and `Avatar_URL` in exactly 1 request."
3. **The Microservice CPU Constraint (gRPC)**: Inside an AWS Datacenter, network bandwidth is unlimited, but CPU cycles are expensive. Parsing and serializing massive JSON strings thousands of times per second wastes CPU. gRPC exists to compile data structures into static, strictly typed Binary contracts. It entirely bypasses JSON string-parsing, allowing internal Microservices to communicate with zero serialization overhead.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cách lấy thông tin: "Tên một Bài viết + Tên Tác giả của bài viết đó".
</details>

Visualizing Data Retrieval Architectures.

| Metric | REST | GraphQL | gRPC |
|---|---|---|---|
| **The Request** | Call 1: `GET /posts/1`<br>*(Returns Post, but only Author_ID)*<br>Call 2: `GET /users/<Author_ID>` | Send exactly 1 Query: <br>`{ post(id: 1) { title, author { name } } }` | Execute compiled binary function:<br>`client.GetPostAndAuthor(req)` |
| **Payload Format**| Human-readable JSON | Human-readable JSON | Machine-only Binary (Protobuf) |
| **Best Used For** | Public APIs, Standard Web Apps | Complex Mobile Apps, Aggregation | Internal Microservices, IoT |

---

## Layer 4: Common Architectures & Roles

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **API Gateway (Cổng Chào)**: Khi bạn có 100 API cho 100 dịch vụ nhỏ khác nhau, thay vì bắt App Mobile nhớ 100 cái địa chỉ URL, người ta xây một Cổng chào duy nhất (API Gateway). App Mobile chỉ gọi duy nhất Cổng chào. Cổng chào sẽ tự biết cách phân đường dẫn đi sâu vào trong. Nó cũng làm nhiệm vụ Chắn Hacker (Rate Limiting) và Kiểm tra thẻ Đăng nhập (Authentication).
2. **Webhooks (API Gọi ngược)**: Thay vì bạn cứ 5 phút gọi API để hỏi "Anh đã xử lý xong chưa?". Hệ thống bên kia sẽ nói: "Cứ đưa đường dẫn URL của anh đây, bao giờ tôi làm xong, tôi sẽ tự lấy URL đó bắn lại (POST) cho anh". Đây gọi là Webhook (Ví dụ: Stripe báo Thanh toán thành công).

</details>

1. **The API Gateway Pattern**: In a Microservices architecture, exposing 50 disparate internal service IPs to the public internet is a massive security risk. An API Gateway (like Kong or AWS API Gateway) sits at the edge of the network. It provides a Single Point of Entry. It absorbs all incoming REST/GraphQL traffic, handles SSL termination, validates JWT Auth Tokens, enforces Rate Limiting, and acts as a reverse proxy, routing the request to the correct internal microservice.
2. **Webhooks (Reverse APIs)**: Traditional APIs require Polling (The client constantly asking the server "Is the task done yet?"). This wastes immense bandwidth. Webhooks implement the "Don't call us, we'll call you" pattern. The Client provides a URL to the Server. When the Server completes the long-running task (e.g., A GitHub Code Push or a Stripe Payment Success), the Server executes an HTTP POST *outward* to the Client's URL, pushing the event payload instantly.

---

## Related Topics

- For building robust REST APIs, explore frameworks like **[Node.js / Express](../backend/nodejs-express.md)** or **[Go](../backend/go.md)**.
- For securing APIs using industry-standard tokens, see **[Cybersecurity / JWT](../cybersecurity/jwt.md)** *(coming soon)*.
- For exploring the specifics of Resource-Oriented architecture, proceed to **[REST APIs](./rest.md)**.
- For solving Frontend over-fetching, proceed to **[GraphQL](./graphql.md)**.
