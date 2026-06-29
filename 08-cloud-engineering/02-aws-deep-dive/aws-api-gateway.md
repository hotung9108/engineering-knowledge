# AWS API Gateway

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Cánh cửa chính để vào hệ thống Backend của bạn. Khám phá cách API Gateway đóng vai trò như một bảo vệ khó tính, giúp chặn Spam, xác thực người dùng, và định tuyến hàng triệu Request HTTP mỗi giây thẳng vào các hàm Lambda hoặc EC2.

</details>

> **Summary**: The front door to your Backend systems. Discover how API Gateway acts as a strict security guard—throttling spam, authenticating users, and flawlessly routing millions of HTTP requests directly into AWS Lambda functions or EC2 backends.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn mở một nhà hàng siêu tốc (Backend).
- **Không có API Gateway**: Bất kỳ khách vãng lai nào (User) cũng có thể chạy thẳng vào trong bếp (Lambda/EC2), túm lấy đầu bếp và hét lên "Làm cho tôi món này". Đầu bếp sẽ bị ngộp, kẻ xấu có thể ném rác vào bếp, và bạn không biết ai đã trả tiền ai chưa.
- **Có API Gateway**: Bạn xây một quầy lễ tân. Tất cả khách hàng ĐỀU PHẢI đứng ở quầy lễ tân. Lễ tân (API Gateway) sẽ:
  1. Yêu cầu đưa thẻ thành viên (Xác thực / Authentication).
  2. Bắt khách xếp hàng nếu quá đông (Giới hạn tốc độ / Throttling).
  3. Từ chối phục vụ những khách gọi món tào lao không có trong menu (Validation).
  4. Đưa tờ ghi món ăn (Request) vào bếp cho đầu bếp (Lambda) làm, rồi mang đồ ăn (Response) ra cho khách.

</details>

You open a high-speed restaurant (Your Backend).
- **Without API Gateway**: Any random person off the street (Users) can walk straight into the kitchen (Lambda/EC2), grab the Chef, and yell their order. The Chefs get overwhelmed, malicious actors can throw garbage into the kitchen, and you have no idea who has paid and who hasn't.
- **With API Gateway**: You build a front Reception Desk. ALL customers MUST wait at the desk. The Receptionist (API Gateway) will:
  1. Demand to see an ID or VIP card (Authentication / IAM).
  2. Force customers to wait in a queue if they are shouting orders too fast (Throttling / Rate Limiting).
  3. Immediately kick out customers asking for items not on the menu (Request Validation).
  4. Securely hand the order (HTTP Request) to the Chef (Lambda), wait for the food, and hand the meal (HTTP Response) back to the customer.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon API Gateway** là một dịch vụ được quản lý toàn diện giúp các nhà phát triển dễ dàng tạo, xuất bản, bảo trì, giám sát và bảo mật các API ở mọi quy mô (REST, HTTP và WebSocket).

**Các tính năng cốt lõi:**
- **Routing (Định tuyến)**: Chuyển hướng URL (Ví dụ: `GET /users`) đến đúng hàm xử lý (Lambda, EC2, hoặc bất kỳ máy chủ nào trên Internet).
- **Security (Bảo mật)**: Tích hợp sẵn với Amazon Cognito hoặc custom Lambda Authorizers để xác thực Token JWT trước khi cho phép vào hệ thống.
- **Throttling (Giới hạn tỷ lệ)**: Chống DDoS và Spam. Tự động trả về lỗi `429 Too Many Requests` nếu 1 IP gọi API quá 100 lần/giây.
- **Caching (Bộ nhớ đệm)**: Lưu lại các response thường gặp để không phải gọi xuống Backend, tăng tốc độ phản hồi.

</details>

**Amazon API Gateway** is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale (REST, HTTP, and WebSocket APIs).

**Core Capabilities:**
- **Routing**: Mapping incoming HTTP URLs (e.g., `POST /checkout`) to the correct backend integration (AWS Lambda, an EC2 Auto Scaling Group, or even an external internet server).
- **Security & Authorization**: Native integration with Amazon Cognito or custom Lambda Authorizers to validate JWT (JSON Web Tokens) *before* the request ever touches your backend code.
- **Throttling & Quotas**: DDoS protection and API monetization. Automatically returns `429 Too Many Requests` if a user exceeds their allowed 100 requests/second limit.
- **Caching**: Temporarily storing API responses at the edge to reduce backend load and drastically improve latency.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi AWS phát minh ra **AWS Lambda** (Serverless), có một vấn đề lớn: Lambda bản chất chỉ là những đoạn code chạy ngầm. Làm sao để ứng dụng Mobile App ở ngoài Internet có thể gọi hàm Lambda? Người dùng không thể cắm dây mạng trực tiếp vào Lambda được.
**API Gateway** ra đời để làm cầu nối. Nó tạo ra các đường link HTTPS công khai trên Internet. Khi Mobile App gọi vào link đó, API Gateway sẽ dịch HTTP Request thành JSON Event, "đánh thức" hàm Lambda tương ứng dậy làm việc, và trả kết quả về dưới dạng HTTP Response.

Nó cũng tách phần "Xác thực & Bảo mật" ra khỏi code Backend. Lập trình viên Backend không cần viết code kiểm tra Token nữa, API Gateway sẽ lo phần đó.

</details>

When AWS invented **AWS Lambda** (Serverless compute), a massive architectural problem arose: Lambda functions are just isolated code executing in the background. How does an iOS Mobile App out on the public Internet trigger a Lambda function? You can't just give an iOS app raw IAM permissions to invoke Lambdas directly.
**API Gateway** was created as the crucial HTTP bridge. It exposes public-facing HTTPS endpoints (URLs). When the Mobile App makes a `GET` request, API Gateway translates the HTTP request into a JSON Event, wakes up the correct Lambda function, passes the data, and returns the Lambda's output as an HTTP Response.

Furthermore, it abstracts "Security & Rate Limiting" away from the backend code. Backend developers no longer have to write boilerplate code to validate JWT tokens or block spam IPs; API Gateway handles it natively at the edge.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**REST API vs. HTTP API vs. WebSocket API**
API Gateway có 3 "hương vị" chính:
1. **REST API (Bản Cổ điển/Đắt tiền)**: Rất mạnh mẽ. Hỗ trợ đủ trò (Validation dữ liệu, Transform dữ liệu, WAF, API Keys để bán API). Nhưng chậm hơn và Đắt.
2. **HTTP API (Bản Đời mới/Rẻ)**: Chuyên dùng làm cầu nối siêu tốc cho Lambda. Nhanh hơn REST API 60%, Rẻ hơn 71%. Rất ít tính năng rườm rà. (Đa số dự án Serverless mới nên dùng cái này).
3. **WebSocket API**: Dùng cho các ứng dụng cần kết nối 2 chiều liên tục (Real-time). Ví dụ: Ứng dụng chat, Game nhiều người chơi.

</details>

### API Types: REST vs HTTP vs WebSocket

API Gateway offers three distinct flavors:
1. **REST API (The Heavyweight)**: The original, feature-rich version. Supports complex Request/Response data transformations, API Keys (for monetizing your API as a SaaS), detailed AWS WAF (Web Application Firewall) integration, and payload validation. *Trade-off*: Slower and significantly more expensive.
2. **HTTP API (The Modern Lightweight)**: Built specifically to be a fast, cheap proxy to AWS Lambda. It is up to 60% faster and 71% cheaper than REST APIs. It strips away the heavy transformation features and focuses purely on high-speed routing and JWT authorization. *(Best Practice: Default to this for modern Serverless apps).*
3. **WebSocket API**: Maintains persistent, bi-directional, real-time connections between the client and the server. Perfect for Chat applications, live stock tickers, or multiplayer games.

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Serverless Web Backend**: Ứng dụng React/Vue (chứa trên S3) gọi API Gateway -> Gọi AWS Lambda -> Đọc dữ liệu DynamoDB. Kiến trúc thần thánh "Zero Server" (Không quản lý máy chủ).
2. **Bán API (SaaS)**: Bạn có cục dữ liệu Thời tiết rất xịn. Bạn dùng API Gateway tạo ra các **API Keys** và **Usage Plans** (Gói cước). Khách hàng mua gói "Silver" chỉ được gọi 10 lần/ngày. Khách mua gói "Gold" được gọi 1000 lần/ngày. API Gateway tự động block ai xài lố.
3. **Ứng dụng Chat (WebSocket)**: Tạo phòng chat ẩn danh. Kết hợp API Gateway (WebSocket) với Redis để giữ trạng thái kết nối của hàng ngàn người chơi.

**Không nên làm (Anti-patterns):**
- **Tải file lớn qua API Gateway**: API Gateway có giới hạn thời gian phản hồi (Timeout) tối đa là **29 giây**, và dung lượng tối đa là 10MB. Không bao giờ dùng API Gateway để người dùng tải lên file Video 1GB. (Thay vào đó, dùng S3 Pre-signed URLs).

</details>

1. **Serverless Architectures**: A React Single Page Application (hosted on S3) makes AJAX calls to API Gateway -> triggers AWS Lambda -> queries DynamoDB. The legendary "Zero Server" architecture that costs nothing when idle.
2. **API Monetization (SaaS)**: You built an AI Image Generator. You want to sell access to your API. You use API Gateway's **API Keys** and **Usage Plans**. You create a "Bronze Tier" (10 requests/day) and a "Gold Tier" (10,000 requests/day). You give clients API Keys. API Gateway automatically tracks usage and throttles clients who exceed their paid tier.
3. **Real-Time Chat Apps (WebSockets)**: Building a live chat room. API Gateway maintains the persistent WebSocket connections for 100,000 users, so your backend Lambda functions only spin up when a message is actually sent, rather than burning EC2 compute just holding connections open.

### Anti-Patterns
- **Large File Uploads/Downloads**: API Gateway has hard limits: a maximum payload size of **10 MB**, and a strict maximum timeout of **29 seconds**. Never route a 500MB Video upload through API Gateway; it will instantly crash. **Best Practice**: Use API Gateway to generate an *S3 Pre-signed URL*, return that URL to the client, and have the client upload the massive video directly to S3, bypassing API Gateway entirely.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Bảo mật: Lambda Authorizers**
API của bạn phải bảo vệ thông tin nội bộ. Khi Client gửi một Request kèm thẻ `Authorization: Bearer <token>`, API Gateway có thể tự động gọi một hàm Lambda đặc biệt gọi là **Lambda Authorizer**. Hàm này sẽ giải mã Token, kiểm tra xem người này có quyền truy cập không.
- Trả về `Allow` -> API Gateway cho phép đi tiếp vào Backend.
- Trả về `Deny` -> API Gateway chặn lại ngay lập tức và trả lỗi `403 Forbidden`. Backend của bạn hoàn toàn không bị làm phiền.

**2. Vấn đề CORS (Cross-Origin Resource Sharing)**
Kẻ thù của mọi Web Developer! Nếu Frontend của bạn ở `app.com` và API Gateway ở `api.com`, trình duyệt sẽ chặn kết nối (Lỗi CORS).
Trên API Gateway, bạn bắt buộc phải cấu hình trả về các header `Access-Control-Allow-Origin` cho các HTTP Method `OPTIONS`. Giao diện AWS có sẵn nút "Enable CORS" để tự động làm việc này.

</details>

### 1. Advanced Security: Lambda Authorizers
You don't want unauthorized users triggering your expensive backend Lambdas. When a client sends a request with an `Authorization: Bearer <jwt-token>` header, API Gateway can intercept it and execute a special Lambda function called a **Lambda Authorizer**.
The Authorizer inspects the token, validates the cryptographic signature, and checks the database if necessary. 
- If valid, it returns an IAM Policy (`Effect: Allow`). API Gateway routes the request to the real backend Lambda.
- If invalid, it returns (`Effect: Deny`). API Gateway immediately blocks the request and returns `403 Forbidden`. The backend Lambda is completely protected from execution (and billing!).

### 2. The CORS Nightmare (Cross-Origin Resource Sharing)
The mortal enemy of Frontend Developers. If your React app is hosted on `https://my-app.com` and your API Gateway endpoint is `https://api.execute-api.us-east-1.amazonaws.com`, the user's browser will block the AJAX request for security reasons unless CORS is explicitly enabled.
You must configure API Gateway to intercept `OPTIONS` preflight requests and return specific headers like `Access-Control-Allow-Origin: https://my-app.com`. If using Serverless Framework or Terraform, you must explicitly enable CORS on every single route.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Rất ít ai thiết lập API Gateway bằng giao diện click chuột của AWS. Ngành công nghiệp thường dùng công cụ **Serverless Framework (YAML)** để định nghĩa cả API Gateway và Lambda cùng một lúc. Nó đơn giản hơn Terraform rất nhiều cho việc này.

</details>

### Provisioning API Gateway (Serverless Framework - `serverless.yml`)

The industry standard for deploying API Gateway + Lambda is the Serverless Framework. It abstracts away the horrific complexity of wiring API Gateway to Lambda manually.

```yaml
service: my-ecommerce-api
frameworkVersion: '3'

provider:
  name: aws
  runtime: nodejs18.x
  region: us-east-1
  # The HTTP API flavor is the modern default
  httpApi:
    cors: true # Solves the CORS nightmare instantly!

functions:
  createOrder:
    handler: src/handlers/createOrder.main
    events:
      # This block completely auto-generates the API Gateway Routing!
      - httpApi:
          path: /orders
          method: POST
          
  getUserProfile:
    handler: src/handlers/getUser.main
    events:
      - httpApi:
          path: /users/{userId} # Path parameters are automatically parsed
          method: GET
          
  # Example of an Authorizer protecting a route
  deleteOrder:
    handler: src/handlers/deleteOrder.main
    events:
      - httpApi:
          path: /orders/{orderId}
          method: DELETE
          authorizer:
            name: customAuthorizerFunction
```

---

## Related Topics

- [AWS Lambda](./aws-lambda.md) — The compute engine that API Gateway is explicitly designed to trigger.
- [AWS Cognito](./aws-iam.md) — The Identity service that natively integrates with API Gateway for User Login.
- [Serverless Framework](../04-serverless/event-driven-architectures.md) — How DevOps teams deploy APIs using Infrastructure as Code.
