# Load Balancing

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi bạn có 10 cái máy chủ chạy song song (Scale Out), làm sao để chia đều 10.000 khách hàng cho 10 cái máy đó? Nếu không chia đều, 9 máy sẽ ngồi chơi còn 1 máy sẽ chết cháy vì nhận tới 10.000 khách. **Load Balancer (Bộ Cân bằng tải)** là một anh cảnh sát giao thông đứng ở cửa ngõ hệ thống. Khách hàng không gọi trực tiếp vào máy chủ của bạn, mà gọi cho anh Cảnh sát. Anh Cảnh sát sẽ nhìn xem máy chủ nào đang rảnh để vẫy tay chỉ khách đi vào máy đó. Nó giúp phân phối tải trọng (Load) một cách cân bằng (Balancing) và che giấu hoàn toàn sự phức tạp của hệ thống phía sau.

</details>

> **Summary**: When an application scales horizontally across multiple servers, a mechanism is required to mathematically distribute incoming network traffic across that pool of servers. Without it, traffic would disproportionately hammer a single node, causing localized failure. A **Load Balancer (LB)** acts as the definitive reverse proxy and traffic cop. It exposes a single, highly available public IP address to the internet. As requests arrive, it utilizes routing algorithms (like Round Robin or Least Connections) to seamlessly distribute the load across the backend server pool, ensuring optimal resource utilization, maximizing throughput, and natively providing Fault Tolerance by instantly redirecting traffic away from dead nodes.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một Siêu thị có 10 quầy thu ngân.
1. **Không có Load Balancer**: Khách mua xong tự chạy ùa ra các quầy. Chỗ thì khách xếp hàng dài 50m bóp cổ nhau, chỗ thì bà thu ngân ngồi ngáp vì không có ai. (Hệ thống sập cục bộ).
2. **Có Load Balancer**: Siêu thị thuê một ông Quản lý đứng ở đầu lối ra. Khách đi tới gặp ông Quản lý trước. Ông ấy nhìn lướt qua 10 quầy: "À, quầy số 3 đang trống 1 chỗ, mời anh vào quầy 3". "Quầy 5 bà thu ngân vừa ngất xỉu, mời anh qua quầy 6". Mọi thứ hoạt động trơn tru, không có một quầy nào bị quá tải hay rảnh rỗi.

</details>

Imagine a Supermarket with 10 checkout lanes.
1. **Without Load Balancing**: Customers blindly rush to whichever lane they see first. Lane 1 gets 50 angry people fighting. Lane 9 has zero people, and the cashier is playing on their phone. This is localized catastrophic failure.
2. **With Load Balancing**: The Supermarket places a Traffic Manager at the front. ALL customers must approach the Manager first. The Manager constantly scans the 10 lanes. He points: "You, go to Lane 4. You, go to Lane 7." If the cashier at Lane 2 faints (Node Failure), the Manager instantly stops sending customers there and redistributes them. Every lane operates at exactly 100% efficiency.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Load Balancer có 2 loại chính chia theo "Tầng mạng":
1. **Layer 4 (L4 - Tầng Transport)**: Cân bằng tải theo IP và Cổng (Port). Nó chỉ biết chuyển gói tin đi (Ví dụ: Chuyển dữ liệu từ Port 80 sang Server 1). Rất "ngu" nhưng đổi lại tốc độ bàn thờ (Vài triệu Request/giây). Thường dùng cho các hệ thống TCP/UDP thuần túy hoặc làm lá chắn vòng ngoài (Ví dụ: AWS Network Load Balancer).
2. **Layer 7 (L7 - Tầng Application)**: Cân bằng tải ở tầng Ứng dụng. Nó có khả năng "Mở gói tin HTTP ra đọc". Nó biết bên trong gói tin ghi URL là gì, Header là gì. Nhờ vậy nó có thể định tuyến thông minh: Ai vào `/api` thì đẩy cho cụm Server API, ai vào `/images` thì đẩy cho cụm Server Lưu trữ. Chậm hơn L4 một chút nhưng vô cùng quyền năng. (Ví dụ: Nginx, AWS Application Load Balancer).

</details>

Load Balancers strictly operate at two different layers of the OSI Model:
1. **Layer 4 (Transport Layer - L4)**: Routes traffic based purely on network variables (Source/Destination IP and TCP/UDP Ports). It performs NAT (Network Address Translation) blindly without inspecting the packet payload. Because it is fundamentally "dumb," it uses virtually zero CPU and operates at astronomical speeds (Millions of RPS). Used for raw TCP streams (e.g., AWS Network Load Balancer, HAProxy TCP mode).
2. **Layer 7 (Application Layer - L7)**: Terminates the TCP connection, decrypts the TLS/SSL, and deeply inspects the HTTP headers and URL path. It is highly intelligent. It can implement **Path-Based Routing** (e.g., routing `example.com/api/*` to the Backend Pods, and `example.com/images/*` to an S3 Bucket). It is slightly slower due to packet inspection overhead but provides massive architectural flexibility (e.g., Nginx, Traefik, AWS ALB).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

LB sinh ra để giải quyết 3 bài toán sống còn:
1. **Quy mô (Scale)**: Bạn không thể bán 1 cái điện thoại mà cài sẵn trong đó danh sách 10.000 IP của máy chủ công ty bạn được. Bạn chỉ có thể cung cấp 1 cái tên miền duy nhất (`api.facebook.com`). LB chính là cái phễu hứng 1 cái tên miền đó và tỏa ra 10.000 IP bên trong.
2. **Tránh Sập toàn hệ thống (Fault Tolerance)**: Máy chủ thường xuyên bị cháy, bị chuột cắn cáp, hoặc tự khởi động lại do lỗi Windows. Nếu khách hàng gọi thẳng vào máy chủ bị lỗi đó, họ sẽ thấy màn hình trắng xóa. LB có tính năng **Health Check (Khám sức khỏe)**. Cứ 5 giây nó "nháy máy" Server 1 lần. Nếu Server sập, LB tự động gạch tên Server đó ra khỏi danh sách, người dùng không hề biết có chuyện gì xảy ra.
3. **Bảo mật (Security & SSL Termination)**: Giải mã chứng chỉ HTTPS là một công việc cực kỳ tốn CPU. LB sẽ đứng ra hứng chịu việc giải mã này (SSL Termination). Gói tin sau khi giải mã xong sẽ đi trần (HTTP) ở trong mạng nội bộ, giúp các Server bên trong nhẹ gánh CPU đi rất nhiều.

</details>

The Load Balancer is the keystone of modern infrastructure for three vital reasons:
1. **The Funnel (Single Entrypoint)**: DNS Round Robin is notoriously unreliable due to aggressive client-side caching. You cannot rely on DNS to dynamically distribute load across 100 ephemeral IP addresses. An LB provides a singular, highly-available static IP (or DNS name) to the public internet, abstracting away the entire chaotic, auto-scaling backend topology.
2. **Automated Fault Tolerance (Health Checks)**: Servers kernel panic. Hard drives fail. If a client hardcodes an IP, they hit a brick wall. An LB performs continuous Active Health Checks (e.g., Ping `HTTP 200 OK` on `/healthz` every 5 seconds). The millisecond a node fails to respond, the LB instantly evicts it from the routing pool. The client experiences zero downtime.
3. **SSL Termination & Security**: Cryptographic Handshakes (TLS/SSL) consume heavy CPU cycles. If your 10 application servers process HTTPS directly, they waste 30% of their CPU purely on cryptography. The L7 Load Balancer acts as a **TLS Terminator**. It holds the SSL Certificates, decrypts the heavy incoming traffic at the Edge, and forwards unencrypted plaintext HTTP into the private, secure VPC. It frees your Application CPUs to focus purely on business logic.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc nâng cấp hệ thống (Deploy bản code mới) vào lúc 12h trưa đang có 1 triệu người truy cập.
</details>

Visualizing a "Zero-Downtime Deployment" scenario at peak traffic hours.

| Action | Without Load Balancer (Direct IP) | With Load Balancer |
|---|---|---|
| **Deploy Step 1** | Shut down the Server to copy new code. | LB is told to "Drain" Server 1 (Stop sending new traffic). |
| **User Impact 1** | **Site is DOWN. 503 Errors.** | Zero impact. All traffic routed to Server 2. |
| **Deploy Step 2** | Turn Server back on. | Server 1 is updated and rebooted. |
| **Deploy Step 3** | Pray it works. | LB Health Check verifies Server 1 is OK. Resumes traffic. |
| **Total Downtime** | 5 to 10 Minutes. | **Absolutely 0 Seconds**. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **AWS Elastic Load Balancer (ELB/ALB)**: Đây là đồ chơi mặc định khi bạn dùng Cloud. Bạn nhấn vài nút, AWS sẽ tự tạo cho bạn 1 cái LB xịn sò, không bao giờ sập (Bản thân cái LB của AWS là một cụm cả chục máy chủ chạy ngầm). Đa số các công ty đều dùng cái này.
2. **Nginx (Self-hosted)**: Đội ngũ dùng máy chủ vật lý tự ráp hoặc các Startup nghèo thường cài Nginx (Hoặc HAProxy) lên 1 con Server riêng rồi cấu hình nó làm Load Balancer bằng file `nginx.conf`. Siêu mạnh mẽ, dùng RAM siêu ít.
3. **Kubernetes Ingress (Nginx Ingress Controller)**: Trong thế giới K8s, Load Balancer được gọi là Ingress. Nó làm nhiệm vụ hứng truy cập từ ngoài Internet, mở gói tin L7 ra đọc đường dẫn `/api/v1` và đẩy vào đúng cái Pod tương ứng.

</details>

1. **Managed Cloud Balancers (AWS ALB/NLB, Google Cloud Load Balancing)**: The absolute industry standard. Instead of managing the LB software yourself, you rent it. The Cloud Provider completely abstracts the LB. An AWS ALB is actually a dynamically scaling cluster of underlying nodes. It provides mathematically guaranteed uptime.
2. **Nginx / HAProxy (Bare Metal / Self-Hosted)**: For on-premise data centers or highly customized routing needs, engineers manually provision a dedicated Linux Server and run Nginx or HAProxy as a Reverse Proxy. HAProxy is legendary for its raw speed and is widely used for TCP (L4) database load balancing (e.g., balancing read queries across a PostgreSQL cluster).
3. **Kubernetes Ingress Controllers**: In K8s, a standard Cloud LB routes traffic to the K8s Nodes. Once inside the cluster, the **Ingress Controller** (which is usually an Nginx or Traefik Pod operating at L7) acts as the internal cluster router, directing the HTTP packet to the exact internal `Service` based on deeply complex YAML routing rules.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Chọn đúng Thuật toán (Algorithms)**: 
   - *Round Robin (Quay vòng)*: Máy 1 $\rightarrow$ Máy 2 $\rightarrow$ Máy 3. Đơn giản nhất, dùng khi cấu hình các máy chủ bằng nhau.
   - *Least Connections (Ít kết nối nhất)*: Rất quan trọng. Nó đếm xem máy nào đang rảnh nhất thì tọng việc vào máy đó. Nếu bạn code tính năng Tải File (Có khách tải mất 5 giây, có khách mất 1 tiếng), tuyệt đối phải dùng Least Connections, nếu không dùng Round Robin sẽ làm cháy một cái máy bị chia toàn khách tải lâu.
2. **Bật Session Stickiness (Sticky Sessions) cẩn thận**: Nếu ứng dụng của bạn là đồ cổ, lưu giỏ hàng vào RAM của Máy chủ. Bạn phải bật Sticky Session (Cắm cọc). Khi khách hàng A vào Máy 1, LB sẽ lưu 1 cái Cookie vào trình duyệt khách. Lần sau khách quay lại, LB đọc Cookie và "ÉP" khách đó phải quay lại Máy 1, cấm sang máy 2. (Tuyệt đối tránh xài cái này nếu có thể, hãy dùng Redis để làm Stateless).

</details>

1. **Algorithmic Routing Selection**:
   - *Round Robin*: The default. Distributes 1-2-3, 1-2-3. Excellent for identical, stateless microservices handling homogenous workloads (e.g., standard API CRUD operations).
   - *Least Connections*: Absolutely critical for **Long-Lived Connections** (e.g., WebSockets, SSE, or massive File Uploads). If Server 1 has 5 connections that take 30 minutes each, and Server 2 has 5 connections that finish in 1 second, Round Robin will maliciously assign the next request to Server 1. Least Connections intelligently inspects the active socket count and correctly assigns it to the idle Server 2.
2. **Avoid Sticky Sessions (Session Affinity)**: Legacy architectures store User Sessions in local server RAM. They mandate turning on LB "Sticky Sessions". The LB injects an `AWSALB` cookie into the browser. Every subsequent request from that browser is rigorously routed to the exact same physical server. **The Anti-Pattern**: This destroys auto-scaling. If you scale down, or that specific server crashes, the user's session is instantly annihilated and they are logged out. You must engineer Stateless architectures (Redis) and disable Sticky Sessions.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nút thắt cổ chai ở chính Load Balancer**: LB sinh ra để chống quá tải, nhưng bản thân cục LB cũng là 1 cái máy chủ cơ mà? Nếu 1 triệu người cùng dội vào Nginx, Nginx sập! 
   - *Cách giải quyết*: Lại phải đẻ ra nhiều cục Nginx song song, và dùng DNS (Route 53 của AWS) để phân tải bằng IP (DNS Round Robin) ngay từ ngoài cổng. Hệ thống lớn luôn có rất nhiều tầng Load Balancer chồng lên nhau.
2. **Mất IP thật của Khách hàng**: Khi gói tin đi qua L7 Load Balancer, IP nguồn của gói tin sẽ bị thay bằng IP của cái Load Balancer. Khi máy chủ của bạn (Server) đọc log, nó sẽ thấy 100% người dùng đến từ IP `10.0.0.5` (IP của cục LB), bạn không thể Block IP xấu hay chống DDoS được.
   - *Cách giải quyết*: LB khi bóc gói tin ra, phải viết thêm IP thật của khách vào một cái Header tên là `X-Forwarded-For: 203.x.x.x`. Code của bạn phải sửa lại, đừng đọc IP từ TCP Socket nữa, mà hãy đọc từ cái Header kia.

</details>

1. **The Single Point of Failure (SPOF)**: A junior architect puts 20 App Servers behind exactly ONE self-hosted Nginx Load Balancer running on a single VM. If that single Nginx VM runs out of RAM, the entire 20-node cluster becomes completely unreachable. **Fix**: Load Balancers must be deployed in Highly Available (HA) pairs (Active/Passive using Keepalived and Virtual IPs) or you must utilize massive Managed Cloud Balancers (AWS ALB) which implicitly abstract this problem using Anycast and DNS-level scaling.
2. **The Loss of the Client IP (`X-Forwarded-For`)**: A massive L7 proxy pitfall. When an HTTP proxy intercepts a request, it terminates the client's TCP socket and initiates a *brand new* TCP socket to your backend server. Your backend server's logs will show that 100% of your traffic originates from the internal IP of the Load Balancer (e.g., `10.0.1.55`). This destroys rate-limiting, geo-location, and auditing. **Fix**: You must explicitly configure the Load Balancer to append the `X-Forwarded-For` and `X-Real-IP` HTTP headers. Furthermore, your backend application framework (e.g., Express.js `app.set('trust proxy', true)`) must be configured to parse these headers securely, ignoring forged headers from malicious clients.

---

## Related Topics

- For how to store the data once the servers scale, read **[Database Scaling](./db-scaling.md)**.
- For protecting these servers from too much load, see **[Rate Limiting](./rate-limiting.md)**.
- For how K8s handles LB internally, see **[Service Discovery](../distributed-system/discovery.md)**.
