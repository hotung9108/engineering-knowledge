# HAProxy

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Nginx là một cô Lễ tân đa năng (Vừa biết phát tờ rơi, vừa biết kiểm tra thẻ, vừa biết dẫn khách), thì **HAProxy** (High Availability Proxy) là một Anh bảo vệ Cửa cuốn cơ bắp, cục súc và cực kì nhanh nhẹn. Nhiệm vụ duy nhất của HAProxy trên cõi đời này là **Cân bằng tải (Load Balancing)**. Nó có thể hoạt động ở Tầng 4 (TCP - Chỉ nhìn địa chỉ IP rồi ném gói tin đi) thay vì Tầng 7 (Đọc hiểu nội dung HTTP). Việc không thèm đọc nội dung chữ bên trong giúp tốc độ của HAProxy thuộc hàng nhanh nhất thế giới. Đó là lý do tại sao HAProxy hiếm khi dùng để đứng trước Web Frontend, mà thường được dùng để giấu sâu bên trong hệ thống, chuyên làm Cân bằng tải cho các Cụm Database khổng lồ (Ví dụ chia tải cho 10 máy chủ PostgreSQL).

</details>

> **Summary**: While Nginx is a versatile "jack-of-all-trades" (Static Web Server, HTTP Reverse Proxy, Caching layer), **HAProxy** (High Availability Proxy) is a highly specialized, hyper-optimized Load Balancer. Its defining architectural advantage is its brutal efficiency in executing **Layer 4 (TCP/UDP) Load Balancing**. At Layer 4, the proxy does not inspect or parse the Layer 7 HTTP headers or the JSON payload. It simply looks at the raw Source and Destination IP addresses and blindly forwards the encrypted binary TCP packets to the backend servers. By skipping the computationally expensive HTTP parsing phase, HAProxy consumes virtually zero CPU and adds negligible microsecond latency. Consequently, while Nginx is often the public-facing edge proxy, HAProxy is the industry standard for internal, high-throughput routing—specifically utilized as a load balancer sitting directly in front of massive Database Clusters (e.g., PostgreSQL, Redis) or RabbitMQ fleets.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một Bưu điện phân loại Bưu kiện.
1. **Nginx (Tầng 7 - Ứng dụng)**: Nginx là một nhân viên cẩn thận. Khi bạn gửi 1 hộp quà, Nginx sẽ **Bóc hộp quà ra**, xem bên trong là Quần áo hay Thức ăn. Nếu là Thức ăn, Nginx mang hộp đó qua Kho Lạnh. Nếu là Quần áo, mang qua Kho Thường. Làm vậy rất thông minh, nhưng bóc hộp quà ra mất rất nhiều thời gian.
2. **HAProxy (Tầng 4 - Mạng)**: HAProxy là một cỗ máy phân loại tự động. Nó **KHÔNG BAO GIỜ bóc hộp quà**. Nó chỉ nhìn cái Nhãn dán bên ngoài (Địa chỉ IP). Cứ thấy nhãn dán báo gửi tới Kho số 1, nó đá cái hộp sang Kho số 1 ngay lập tức trong nháy mắt. Tốc độ nhanh hơn gấp 10 lần.

</details>

Imagine a Postal Sorting Facility.
1. **Layer 7 Routing (Nginx)**: The sorting worker literally opens every single envelope, reads the letter inside to see if it mentions "Billing" or "Support", reseals the envelope, and places it in the correct pile. This intelligent inspection is useful but computationally exhausted.
2. **Layer 4 Routing (HAProxy)**: The worker is blindfolded. They only feel the braille Zip Code on the outside of the sealed envelope (The TCP IP/Port). They instantly toss the envelope into a truck without ever caring what is written inside the letter. Because they skip the "opening and reading" phase, they can sort 10,000 envelopes per second.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

HAProxy là một phần mềm Cân bằng tải có những đặc điểm sau:
1. **Chuyên gia Cân bằng tải**: Nó sinh ra chỉ để lấy Traffic từ 1 nguồn và chia đều ra N nguồn. Thuật toán của nó cực kì đa dạng (Round Robin, Leastconn, Source IP Hash...).
2. **Hoạt động ở Tầng 4 (TCP/UDP)**: Nó có thể cân bằng tải mọi thứ, không chỉ là trang Web. Bạn chạy Game Server, chạy Database, chạy Server Chat... miễn là dùng giao thức mạng, HAProxy đều cân bằng tải được hết.
3. **Giám sát Sức khỏe (Health Checks)**: Sức mạnh tuyệt đối của HAProxy. Cứ mỗi 2 giây, nó gõ cửa Máy chủ A hỏi "Còn sống không?". Nếu Máy chủ A chết, nó lập tức gạch tên A ra khỏi danh sách trong 0.001 giây, và dồn toàn bộ khách cho Máy chủ B. Khách hàng hoàn toàn không biết Máy chủ A vừa chết.

</details>

HAProxy is an open-source software load balancer and proxy server strictly optimized for TCP and HTTP-based applications:
1. **Pure Load Balancing Focus**: Unlike Nginx, HAProxy does not serve static files (no HTML/CSS hosting). It is entirely dedicated to routing traffic.
2. **Layer 4 (TCP) Mastery**: It intercepts raw TCP connections. This means it can load balance *anything* that communicates over a network socket, not just HTTP web traffic. It is widely used to load balance incoming connections to PostgreSQL databases, SMTP Mail servers, MQTT IoT brokers, or custom multiplayer game servers.
3. **Advanced Health Checking**: The "High Availability" in its name comes from its paranoid health-checking algorithms. It continuously probes backend nodes (via TCP pings or custom SQL queries). If a backend database node crashes, HAProxy detects it in milliseconds, cleanly excises the dead node from the routing pool, and seamlessly redirects all new connections to healthy nodes.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Giả sử App của bạn có 5 triệu người dùng. Hệ thống của bạn có 3 Máy chủ API (Backend) và 1 Máy chủ Database (Postgres). 
Máy chủ API chịu tải tốt nhờ Nginx, nhưng Máy chủ Postgres bắt đầu bốc khói vì phải xử lý quá nhiều lệnh đọc. 
Bạn mua thêm 2 Máy chủ Postgres nữa (Tổng cộng là 3 máy). Nhưng làm sao để 3 cái Máy chủ API biết cách "chia đều" câu hỏi cho 3 máy Postgres kia? Chẳng lẽ code cứng IP trong Node.js? Nếu 1 máy Postgres chết thì Node.js báo lỗi à?
Đó là lúc HAProxy xuất hiện. Bạn cài HAProxy đứng giữa API và Postgres. 3 Máy chủ API chỉ cần gọi đến ĐÚNG 1 ĐỊA CHỈ IP duy nhất (Của HAProxy). HAProxy sẽ tự động chia luồng TCP đó ra cho 3 máy Postgres, và tự động bỏ qua nếu có máy Postgres nào bị chết.

</details>

Why deploy HAProxy when you already have Nginx at the edge? Because of **Internal Infrastructure Scaling**.
Nginx perfectly balances HTTP traffic from the public Internet to your internal Node.js servers. But what balances the traffic *from* your Node.js servers *to* your databases?
If you have a primary PostgreSQL database and 3 Read-Replicas, your Node.js application must somehow know the IPs of all 3 replicas and manually distribute its `SELECT` queries among them. If Replica 2 crashes, Node.js throws database connection errors until you manually update the code.
HAProxy solves internal routing. You deploy HAProxy directly in front of the PostgreSQL cluster. Node.js connects to a single, static IP (HAProxy). HAProxy intercepts the raw TCP database connection and intelligently routes it to the least-busy PostgreSQL Read-Replica. If a replica crashes, HAProxy silently removes it. The backend code remains blissfully ignorant of the underlying database topology.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình xử lý Cân bằng tải cho Database (Postgres).
</details>

Visualizing Database Load Balancing (Layer 4).

| Metric | Application direct to Databases | Application via HAProxy |
|---|---|---|
| **Connection Configuration** | The App needs an array of 5 Database IPs hardcoded in `.env`. `DB_HOSTS=[1.1, 1.2...]` | The App needs exactly 1 IP. `DB_HOST=haproxy.local` |
| **Failover (A DB Dies)** | App tries to connect to IP 1.2. It times out (30 seconds). App throws an error. User sees "500 Server Error". | HAProxy already knew IP 1.2 died 1 second ago. It instantly routes the App to IP 1.3. **Zero errors for the user**. |
| **Performance Overhead**| None. | ~1-2 milliseconds of latency added. Highly negligible for the immense High-Availability benefits. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cân bằng tải Database (Layer 4)**: Ứng dụng số 1 của HAProxy. Cân bằng tải cho cụm PostgreSQL, MySQL, Redis Cluster, hoặc RabbitMQ. Hoàn toàn trong suốt với ứng dụng gốc.
2. **Kubernetes Ingress Controller**: Mặc dù Nginx rất phổ biến trong Kubernetes, nhưng rất nhiều hệ thống lõi chọn HAProxy làm Ingress vì nó ăn siêu ít CPU và thuật toán chia tải của nó hoạt động mượt mà hơn khi có hàng ngàn Pod biến mất/hiện ra liên tục.
3. **Cổng bảo vệ Anti-DDoS cấp mạng**: Các nhà cung cấp Hosting lớn thường đặt các cụm HAProxy khổng lồ ở vòng ngoài cùng để chặn các cuộc tấn công xả rác TCP/UDP (Syn Flood) trước khi chúng kịp bay đến hạ tầng ứng dụng.

</details>

1. **Database Load Balancing (TCP Routing)**: The canonical use case. Placing HAProxy in front of a Galera MySQL Cluster, PostgreSQL Read Replicas, or a distributed Redis cluster. It operates purely at the TCP level, ensuring the DB connections are distributed using algorithms like `leastconn` (sending new connections to the database with the fewest active queries).
2. **Kubernetes Ingress (High-Throughput)**: While Nginx is the default Kubernetes Ingress Controller, large-scale deployments often swap it for the HAProxy Ingress Controller. HAProxy's dynamic reconfiguration engine handles the constant spinning up and tearing down of K8s Pods with less CPU thrashing than traditional Nginx reloads.
3. **API Gateway Edge Tier (Layer 4 Defense)**: Large enterprises utilize a two-tier proxy architecture. Tier 1 is a massive cluster of HAProxy nodes terminating raw TCP connections and absorbing SYN-Flood DDoS attacks. Tier 2 consists of Nginx nodes that parse the cleaned HTTP traffic, execute SSL termination, and apply complex Layer 7 routing logic.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sử dụng thuật toán `leastconn` cho kết nối dài**: Ở Nginx (Web), thuật toán `roundrobin` (chia đều 1-1) rất tốt vì tải trang web chỉ mất 0.1 giây. Nhưng nếu dùng HAProxy cho Database (Kết nối TCP mở liên tục hàng giờ), máy A có thể đang xử lý 10 kết nối rất nhẹ, nhưng máy B đang dính 10 kết nối cực nặng. Nếu HAProxy tiếp tục ném cho máy B (theo kiểu roundrobin), máy B sẽ chết. Hãy dùng `leastconn` (Chỉ ném cho máy nào đang có ít kết nối nhất).
2. **Trang bị HAProxy Stats Page**: HAProxy có sẵn một trang Dashboard UI rất đẹp, hiển thị chính xác trạng thái Sống/Chết của hàng trăm máy chủ, số lượng kết nối đang xử lý. BẮT BUỘC phải bật tính năng này lên, cấu hình mật khẩu an toàn, để team DevOps có thể nhìn vào và biết máy chủ nào đang quá tải.

</details>

1. **Utilize `leastconn` for Long-Lived TCP Connections**: Round-Robin is effective for short-lived HTTP requests. However, database connections (TCP) or WebSockets are persistent. If you use Round-Robin, Server A might end up holding 50 idle connections, while Server B ends up holding 50 extremely heavy analytical queries. Server B crashes. **Rule**: For Layer 4 Load Balancing, always set the algorithm to `leastconn` (Least Connections). HAProxy will dynamically route new traffic to whichever backend server currently has the fewest active network sockets, guaranteeing perfectly balanced CPU utilization.
2. **Enable and Secure the Stats Dashboard**: HAProxy ships with an incredibly powerful, built-in HTML dashboard detailing real-time metrics: bytes in/out, active sessions, queue lengths, and health-check statuses of every backend node. **Rule**: Always enable the `stats` module, bind it to an internal management port, and protect it with Basic Authentication. It is the first place DevOps engineers look during an outage.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Quên mất IP gốc của Khách (Layer 4 Blindness)**: Khi chạy ở Tầng 7 (HTTP), Proxy có thể nhét IP của khách vào Header `X-Forwarded-For`. Nhưng HAProxy chạy ở Tầng 4 (TCP), không có khái niệm Header! Nên Database/Server đằng sau sẽ luôn thấy IP truy cập là của HAProxy (127.0.0.1). Điều này làm hỏng việc kiểm tra bảo mật IP trên Database.
   - *Cách giải*: Bắt buộc phải bật giao thức **PROXY Protocol** ở cả HAProxy và máy chủ đích. Giao thức này sẽ nhét lén IP thực của khách vào gói tin TCP ở Tầng 4.
2. **Gặp lỗi Split-Brain (Lỗ hổng Độc thân)**: Bạn dùng HAProxy để cụm Database không bị chết mạng (High Availability). Nhưng bản thân cái máy chủ chạy HAProxy lại chỉ có 1 cái! Nếu máy chủ HAProxy đó cháy, toàn bộ Database sống nhăn răng nhưng App vẫn không gọi được.
   - *Cách giải*: Không bao giờ chạy 1 máy HAProxy. Luôn chạy 2 máy HAProxy song song, và dùng công nghệ `Keepalived` (Virtual IP) để liên kết chúng. Máy HAProxy 1 chết, máy 2 tự động tiếp quản cái IP đó trong 1 giây.

</details>

1. **Layer 4 IP Masking (The PROXY Protocol Solution)**: At Layer 7 (Nginx), you inject `X-Forwarded-For` into the HTTP header to pass the client's IP. At Layer 4 (TCP routing), there are no HTTP Headers. The Backend Database will log every single incoming connection as originating from HAProxy's internal IP. If the Database relies on IP-whitelisting for security, it is completely broken. **Rule**: You must enable the **PROXY Protocol** (invented by the creator of HAProxy). It prepends a tiny binary header containing the true Client IP to the TCP stream *before* forwarding it. The backend database (e.g., Postgres) must also be explicitly configured to understand the PROXY protocol.
2. **Creating a Single Point of Failure (SPOF)**: The ultimate irony is deploying HAProxy to ensure High Availability for 5 backend servers, but running HAProxy on a single Linux Virtual Machine. If the VM hosting HAProxy reboots, the entire system goes entirely offline, even though the 5 backends are perfectly healthy. **Rule**: HAProxy must be deployed in an Active/Passive pair using **Keepalived** and a Floating Virtual IP (VIP). If the Primary HAProxy node dies, Keepalived instantly transfers the public IP address to the Backup HAProxy node, ensuring true High Availability.

---

## Related Topics

- For serving web applications and Layer 7 (HTTP) proxies, use **[Nginx](./nginx.md)**.
- For modern Service Mesh routing in Kubernetes environments, use **[Envoy](./envoy.md)**.
- HAProxy is the standard Load Balancer sitting in front of Data systems like **[PostgreSQL](../databases/postgresql.md)** and **[Redis](../databases/redis.md)**.
