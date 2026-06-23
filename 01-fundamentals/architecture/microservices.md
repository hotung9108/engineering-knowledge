# Microservices Architecture

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ngày xưa, người ta thường nhét toàn bộ code của công ty (Đăng nhập, Thanh toán, Giao hàng) vào chung một cục Code khổng lồ (Monolith). Cục code này càng ngày càng phình to, mỗi lần sửa một dòng code nhỏ cũng phải tắt toàn bộ hệ thống đi khởi động lại mất 30 phút. **Microservices (Kiến trúc vi dịch vụ)** đập nát cục code khổng lồ đó ra thành 100 phần mềm nhỏ xíu. Mỗi phần mềm (Service) tự chạy độc lập, tự có Database riêng, và nói chuyện với nhau qua mạng (REST API / gRPC).

</details>

> **Summary**: Historically, enterprise applications were engineered as Monoliths: a single, colossal, indivisible codebase containing every feature (Auth, Billing, Inventory) connected to a single unified Database. As organizations scaled, Monoliths became architectural bottlenecks—deployments took hours, and a single bug in the Billing module would crash the entire application. **Microservices Architecture** shatters the Monolith. It decomposes the application into dozens of small, strictly bounded, independently deployable services. Each service owns its own database, operates in complete isolation, and communicates asynchronously via network protocols (REST/gRPC/Kafka).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn mở một Nhà Hàng.
1. **Monolith (Nhà hàng truyền thống)**: Bạn thuê 1 ông Đầu Bếp vạn năng. Ổng vừa phải nướng thịt, vừa xắt rau, vừa pha nước chấm, vừa rửa bát. Lúc ít khách thì không sao. Khi có 1000 khách, ông Đầu Bếp phát điên, làm đổ nồi canh, và toàn bộ nhà hàng sập tiệm.
2. **Microservices (Chuỗi thức ăn nhanh)**: Bạn đuổi việc ông Đầu Bếp đó. Bạn lập ra 4 quầy riêng biệt: Quầy Thịt (Chỉ nướng thịt), Quầy Rau, Quầy Nước, và Quầy Rửa Bát. Mỗi quầy có nhân viên riêng, dụng cụ riêng (Database riêng). Khách gọi món, Quầy Thịt nướng xong thì ném qua Quầy Rau (Gọi API). Nếu Quầy Nước bị cúp điện đóng cửa, 3 quầy kia vẫn hoạt động bình thường!

</details>

Imagine operating a Restaurant.
1. **The Monolith (The Master Chef)**: You hire one omnipotent Chef. They must simultaneously chop vegetables, grill steaks, boil pasta, and wash the dishes using a single stove. At low volume, it works. At peak hours (1,000 customers), the Chef reaches absolute cognitive overload. They accidentally burn the steak, the kitchen catches fire, and the entire restaurant shuts down.
2. **Microservices (The Assembly Line)**: You fire the Master Chef. You divide the kitchen into isolated stations: The Grill Station, the Salad Station, and the Drink Station. Each station has its own dedicated workers and its own independent tools (its own Database). They communicate by passing tickets (API calls). If the Drink Station's refrigerator breaks down, the Grill and Salad stations continue operating perfectly.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Microservices không phải là Code, nó là Cách chia Cấu trúc**.
1. **Độc lập tuyệt đối (Independently Deployable)**: Team A làm Service Thanh toán có thể đẩy code (Deploy) lên Server lúc 2h chiều mà không cần xin phép Team B (Đang làm Service Giao hàng).
2. **Công nghệ đa dạng (Polyglot)**: Vì các Service tách biệt nhau, Service Thanh toán có thể viết bằng Java (cho an toàn), Service Nhắn tin có thể viết bằng Node.js (cho nhanh), và Data Science viết bằng Python. Chúng chỉ cần hiểu chung tiếng Anh (JSON/REST API) là được.
3. **Database độc quyền**: ĐÂY LÀ ĐIỀU BẮT BUỘC. Service A tuyệt đối không được phép chọc thẳng vào Database của Service B để đọc trộm dữ liệu. Nếu A cần dữ liệu của B, A phải gọi điện (gọi API) xin B, và B sẽ trả về cho A.

</details>

Microservices is fundamentally an architectural design pattern, not a specific technology. It mandates strict structural constraints:
1. **Independent Deployability**: The defining characteristic. The Payment Team can deploy a patch to the Payment Service 50 times a day without coordinating with, compiling, or impacting the Inventory Service.
2. **Polyglot Programming**: Because services are physically decoupled and communicate over agnostic protocols (HTTP/JSON), engineering teams can choose the optimal tool for the job. The Machine Learning service uses Python. The high-concurrency Chat service uses Go. The legacy enterprise logic uses Java.
3. **Database per Service (Decentralized Data)**: The golden, unbreakable rule of Microservices. The User Service connects *only* to the User Database. The Order Service connects *only* to the Order Database. If the Order Service needs a User's email, it is physically barred from executing an SQL `JOIN`. It must execute a network API call to the User Service.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề Tắc nghẽn Nhân sự ở cục Monolith**:
Khi công ty khởi nghiệp có 3 lập trình viên, Monolith rất tuyệt vời. Nhưng khi Netflix hay Uber phình to ra 5,000 lập trình viên, việc 5,000 người cùng code chung vào 1 kho Git là thảm họa. Mỗi lần gộp code (Merge) sinh ra hàng ngàn lỗi đụng độ (Conflict). Sửa 1 lỗi ở phần Đổi Mật Khẩu lỡ tay làm sập luôn phần Thanh Toán. Không ai dám nhấn nút Deploy.

**Sức mạnh của Microservices (Mở rộng theo chiều ngang - Horizontal Scaling)**:
Nó giải quyết bài toán Con Người và Quản lý máy chủ. 
- Về con người: Chia 5,000 người ra thành 500 team nhỏ (Mỗi team 10 người), tự quản lý 1 Service riêng. Không ai giẫm chân ai.
- Về máy chủ: Đêm giao thừa, ai cũng vào nhắn tin chúc tết, nhưng không ai mua hàng. Hệ thống tự động nhân bản (Scale-out) Service Nhắn Tin lên 1000 con Server, trong khi Service Mua Hàng vẫn giữ nguyên 2 con Server. Cực kỳ tiết kiệm tiền (Đám mây).

</details>

**The Monolithic Scaling Bottleneck (Conway's Law)**:
A Monolith is hyper-efficient for a 3-person Startup. However, when an engineering department scales to 5,000 developers operating within a single GitHub repository, velocity violently drops to zero. 5,000 developers attempting to merge code daily triggers perpetual "Integration Hell." A junior developer pushing a Null-Pointer Exception in the Avatar-Upload module violently crashes the entire monolithic process, taking the core Payment Gateway offline with it.

**The Microservice Solution (Granular Scaling & Fault Isolation)**:
It resolves both organizational and computational scaling limits.
- **Organizational**: It strictly enforces Conway's Law. You divide 5,000 engineers into 500 autonomous "Two-Pizza Teams". Each team physically owns, deploys, and monitors their specific Service in complete isolation.
- **Computational (Elasticity)**: On Black Friday, the "Checkout" Service is hammered by traffic, but the "Profile Editing" Service is ignored. In a Monolith, you must horizontally scale the *entire* massive application, wasting terabytes of RAM. In Microservices, the orchestrator (Kubernetes) scales *only* the Checkout Service from 10 pods to 1,000 pods, achieving extreme OpEx efficiency.

---

## Layer 3: Without vs. With Comparison (Compare)

### Monolith vs. Microservices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Bảng so sánh. Microservices không phải là thuốc tiên, nó mang lại một rổ rắc rối mới.
</details>

Microservices are not a silver bullet; they trade monolithic complexity for distributed complexity.

| Feature | Monolith | Microservices |
|---|---|---|
| **Codebase** | Single massive repository. Easy to search. | 100+ separate repositories. Hard to track. |
| **Database** | Single giant SQL DB. ACID transactions are easy (`JOIN`). | Distributed DBs. Transactions spanning multiple services are a nightmare (Requires Sagas). |
| **Communication**| In-memory function calls (0 ms latency). | Network API calls (High latency, network failures). |
| **Deployment** | "Big Bang" release. Extremely risky and slow. | Continuous, isolated deployments. Low risk. |
| **Fault Tolerance**| A memory leak in one module crashes everything. | A memory leak crashes one service; the rest survive. |
| **Debugging** | Easy. A single Stack Trace. | Brutal. Requires Distributed Tracing (Jaeger) to track a request hopping across 15 servers. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Hệ thống lớn, phức tạp (Uber, Netflix, Shopee)**: Bắt buộc dùng Microservices. Shopee có Service cho Giỏ hàng, Service tính Khuyến mãi, Service tính phí Giao hàng. Khi người dùng bấm "Mua", Service Giỏ hàng phải gọi điện qua 3 Service kia để chốt đơn.
- **Kiến trúc Sự kiện (Event-Driven)**: Nếu gọi API bằng HTTP (REST) chờ nhau trả lời thì quá chậm. Shopee dùng hệ thống "Cái loa" (Ví dụ: Kafka/RabbitMQ). Service Thanh toán quẹt thẻ xong, nó chỉ hét lên cái loa: "Thằng Tùng vừa trả tiền xong rồi nhé!". Service Giao Hàng nghe thấy tiếng loa, tự động đi đóng gói hàng. Không ai phải đứng chờ ai.
- **Khi nào KHÔNG NÊN dùng**: Khi bạn làm dự án Startup nhỏ (Website bán áo thun 500 khách/ngày). Hãy dùng Monolith! Chia nhỏ thành 10 Microservices lúc này sẽ khiến bạn tốn cả tỷ đồng tiền nuôi máy chủ AWS (Kubernetes, Load Balancer) và tiền thuê DevOps, trong khi không thu lại được lợi ích gì.

</details>

- **Hyperscale Enterprises (Netflix, Uber, Amazon)**: The mandatory architecture for global scale. When a user requests a ride on Uber, the API Gateway fans out the request. The Geospatial Service calculates the route, the Pricing Service executes machine learning to determine surge pricing, and the Dispatch Service locates the nearest driver. These are all separate, horizontally scaled clusters.
- **Event-Driven Architecture (Asynchronous decoupled)**: Synchronous REST API calls between microservices (Service A waits for Service B to reply) create cascading latency and fragility. Elite microservices communicate asynchronously via an Event Bus (e.g., Apache Kafka or RabbitMQ). The Payment Service successfully charges a credit card, drops a `{ "event": "Payment_Success", "orderId": 42 }` message into Kafka, and immediately returns a response to the user. The Shipping Service passively listens to Kafka, detects the event, and independently initiates the shipping process.
- **The Microservice Premium (When NOT to use them)**: "Monolith First" is a golden rule. If you are a startup building an MVP for a blog or a small E-Commerce store, deploying Microservices is architectural suicide. You will drown in the operational overhead of managing Kubernetes, distributed logging, network latency, and CI/CD pipelines before you ever find Product-Market Fit. Build a clean, modular Monolith first.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **API Gateway (Cổng bảo vệ)**: Đừng bao giờ bắt cái App điện thoại của khách hàng phải tự nhớ địa chỉ IP của 50 cái Service khác nhau. Hãy dựng một cái cổng chào duy nhất (API Gateway). App điện thoại chỉ cần gọi thẳng cổng chào. Cổng chào sẽ kiểm tra Token đăng nhập, sau đó tự động điều hướng (Route) khách vào đúng phòng (Service) khách cần.
2. **Thiết kế theo Domain-Driven Design (DDD)**: Đừng cắt bừa hệ thống ra thành các mảnh nhỏ xíu. Việc cắt Microservices phải dựa trên ranh giới Nghiệp Vụ (Business Domain). Ví dụ: Gom hết mọi thứ liên quan đến Tiền bạc vào 1 Service (Billing). Nếu bạn cắt quá nhỏ, một thao tác đơn giản sẽ phải bay qua mạng 20 lần, hệ thống sẽ chết đứng vì độ trễ mạng (Latency).

</details>

1. **Mandatory API Gateway Pattern**: Do not expose 50 disparate Microservice IP addresses to the public Internet, forcing the iOS Client to orchestrate the network calls. Expose a single, unified entry point (An API Gateway like Kong, Nginx, or AWS API Gateway). The Client sends a single request (`GET /dashboard`) to the Gateway. The Gateway securely validates the JWT token, aggressively enforces Rate Limiting, and autonomously fans out the request to the underlying internal User, Order, and Notification services, aggregating the responses back to the Client.
2. **Domain-Driven Design (DDD) Boundaries**: The most complex aspect of Microservices is determining exactly *where* to cut the monolith. Do not cut randomly. You must map boundaries to strict business domains (Bounded Contexts). E.g., The "Billing Domain" vs the "Inventory Domain". If you decompose services too aggressively (Nano-services), completing a simple transaction will require 15 synchronous network hops, resulting in catastrophic latency and a "Distributed Monolith."

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cơ sở dữ liệu xài chung (Shared Database)**: Dev chia code ra làm 5 Service rất xịn. Nhưng cả 5 Service đó đều chọc chung vào 1 con Database MySQL khổng lồ ở dưới đáy. Đây là lỗi phổ biến nhất thế giới! Nếu Database đó sập, cả 5 Service sập theo $\rightarrow$ Khác gì Monolith đâu? Bắt buộc mỗi Service phải sở hữu 1 Database vật lý riêng biệt.
2. **Lỗi phân tán (Distributed Transactions)**: Ở Monolith, khi bạn chuyển 100k từ User A sang User B, nếu giữa chừng bị lỗi, Database sẽ Tự Động hoàn lại tiền (Rollback) nhờ tính năng ACID. Ở Microservices, User A nằm ở DB 1, User B nằm ở DB 2. Không có SQL nào Rollback hộ bạn cả. Tiền sẽ bị trừ ở A nhưng không cộng vào B. Bạn phải tự viết code rất phức tạp (Mẫu thiết kế Saga) để xử lý hoàn tiền bằng tay.

</details>

1. **The Shared Database Anti-Pattern**: An engineering team physically splits their codebase into 5 slick Node.js deployments, but connects all 5 of them directly to the exact same legacy PostgreSQL Database. This is a "Distributed Monolith" and the absolute worst of both worlds. The database schema becomes tightly coupled across 5 repositories. If the database locks up, the entire fleet crashes. **Rule**: Database per Service. Service A physically cannot read Service B's tables.
2. **Ignoring the Fallacies of Distributed Computing (Distributed Transactions)**: In a Monolith, transferring money utilizes a rigid SQL Transaction: `BEGIN; UPDATE A -100; UPDATE B +100; COMMIT;`. If anything fails, the DB natively executes a `ROLLBACK`. In Microservices, Account A is in `DB_1` (Java Service) and Account B is in `DB_2` (Go Service). Distributed ACID transactions are impossible without crippling locking mechanisms. Engineers naive to this will experience catastrophic data inconsistency (Account A is debited, the network crashes, Account B is never credited). You must master complex distributed compensation patterns like **The Saga Pattern**.

---

## Related Topics

- Microservices strictly rely on the network. See **[REST API](../network/rest-api.md)** and **[gRPC](../network/grpc.md)**.
- Deploying hundreds of services requires **[Virtualization & Containers (Docker)](../cloud-computing/virtualization-containers.md)**.
- Scaling these independent services dynamically requires understanding **[Scaling & Load Balancing](../cloud-computing/scaling.md)**.
