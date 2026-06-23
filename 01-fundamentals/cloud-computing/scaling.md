# Scaling: Vertical, Horizontal, and Load Balancing

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi trang web của bạn chỉ có 10 người truy cập, một máy chủ bèo nhèo cũng gánh được. Nhưng khi ứng dụng lên sóng truyền hình và đón 1 triệu người truy cập cùng lúc, máy chủ sẽ bốc khói và sập. **Scaling (Mở rộng quy mô)** là nghệ thuật bơm thêm sức mạnh cho hệ thống để chống đỡ bão traffic. Có hai triết lý chính: Bơm steroid cho con server hiện tại cho nó to ra (**Vertical Scaling**), hoặc nhân bản nó lên thành đội quân hàng trăm con server nhỏ bầy đàn (**Horizontal Scaling**).

</details>

> **Summary**: A single entry-level server flawlessly handles a prototype application with 10 concurrent users. However, when an application hits exponential virality (e.g., a Super Bowl commercial), a massive traffic spike will catastrophically overwhelm the server's CPU and Memory, resulting in a system crash. **Scaling** is the architectural science of dynamically provisioning additional computational capacity to survive immense loads. The industry operates on two distinct paradigms: upgrading the physical hardware of a single machine (**Vertical Scaling / Scaling Up**), or cloning the application across a vast distributed fleet of smaller machines (**Horizontal Scaling / Scaling Out**).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn mở một tiệm phở (Server).
1. **Vertical Scaling (Mở rộng Dọc - Scale Up)**: Quán đông khách quá. Thay vì thuê thêm người, bạn cho ông đầu bếp duy nhất uống nước tăng lực, mua cho ổng cái nồi to gấp 10 lần, bắt ổng mọc thêm 4 cái tay để nấu nhanh hơn. Nhưng sức người có hạn, ổng có thể nấu 100 tô/phút, chứ 1000 tô thì ổng gục ngã (Sập server).
2. **Horizontal Scaling (Mở rộng Ngang - Scale Out)**: Bạn giữ nguyên ông đầu bếp cũ. Nhưng bạn mở thêm 10 chi nhánh phở khác y hệt. 
3. **Load Balancer (Bộ Cân Bằng Tải)**: Khách kéo đến quá đông, bạn thuê một ông bảo vệ đứng ở cửa (Load Balancer). Ông bảo vệ chỉ làm đúng 1 việc: Phân lô. Khách 1 vào quán A, khách 2 sang quán B, khách 3 sang quán C. Nhờ thế, không quán nào bị quá tải, khách ăn rất vui vẻ.

</details>

Imagine you own a tiny Bakery (A Single Server).
1. **Vertical Scaling (Scaling Up)**: You become extremely popular. Instead of hiring help, you inject your only Baker with adrenaline, buy them a massive industrial oven, and force them to work 24/7. This works temporarily, but eventually, the Baker hits biological limits. They cannot bake 10,000 cakes an hour. The Baker collapses (Hardware Limits reached).
2. **Horizontal Scaling (Scaling Out)**: You keep your normal Baker. Instead, you instantly clone your Bakery and build 10 identical Bakeries next door, hiring 10 normal Bakers. You have infinite potential.
3. **The Load Balancer (The Traffic Cop)**: 1,000 customers show up. If they all rush into Bakery #1, it will crash. So, you hire a Traffic Cop (Load Balancer) to stand at the entrance of the street. The cop points: "You go to Bakery 1, you go to Bakery 2, you go to Bakery 3." Traffic is perfectly distributed, and no single Bakery melts down.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Vertical Scaling (Scale Up)**: Tắt máy chủ đi. Tháo thanh RAM 8GB ra, lắp thanh 64GB vào. Tháo con CPU i3 ra, thay bằng i9. Khởi động lại.
**2. Horizontal Scaling (Scale Out)**: Lấy Code bọc vào Container (Docker). Rồi triển khai cái Container đó lên 100 máy chủ khác nhau. Các máy chủ chạy song song không phụ thuộc nhau.
**3. Load Balancing**: Một phần mềm (như Nginx/HAProxy) đứng chặn ở cửa ngõ. Nó hứng toàn bộ luồng mạng của người dùng, dùng thuật toán (Ví dụ: Round Robin - Chia bài xoay vòng) để đẩy Request vào con Server nào đang rảnh nhất.

</details>

**1. Vertical Scaling (Scale Up)**: Upgrading the raw hardware specifications of a single monolithic node. In the Cloud, this means clicking a button to upgrade an AWS EC2 instance from a `t2.micro` (1 CPU, 1GB RAM) to an `m5.24xlarge` (96 CPUs, 384GB RAM). It usually requires temporary downtime to reboot.
**2. Horizontal Scaling (Scale Out)**: Distributing the computational load across a vast fleet of independent nodes. This demands stateless architectures. You provision 100 identical micro-servers instead of 1 mega-server.
**3. Load Balancing**: A reverse proxy routing mechanism (Hardware or Software like Nginx/AWS ALB) positioned identically in front of the server fleet. It intercepts all incoming Client HTTP requests and distributes them evenly across the healthy Backend nodes using specific algorithms (e.g., Round Robin, Least Connections).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Nút thắt của Vertical Scaling (Giới hạn vật lý)**:
Vertical Scaling rất dễ làm (Chỉ tốn tiền mua máy xịn). Nhưng nó có giới hạn. Trên thế giới không có cái bo mạch chủ nào cắm được 1 triệu GB RAM. Hơn nữa, nó gây ra điểm chết chí mạng (Single Point of Failure - SPoF). Nếu máy chủ siêu khủng đó bị cháy ổ cứng, TOÀN BỘ hệ thống của bạn chết đứng.

**Sức mạnh của Horizontal Scaling**:
Bởi vì bạn có 100 máy chủ nhỏ rải rác khắp các Data Center, nếu có 5 cái máy bị chập điện nổ tung, 95 cái máy còn lại vẫn âm thầm gánh vác hệ thống. Người dùng không hề nhận ra hệ thống vừa bị lỗi phần cứng. Đó gọi là Tính Sẵn Sàng Cao (High Availability). Ngành IT hiện đại 100% hướng tới Horizontal Scaling.

</details>

**The Physical Ceiling of Vertical Scaling**:
Vertical Scaling is operationally trivial (no code changes required). However, it hits a hard physical ceiling; Motherboards cannot mathematically support infinite CPUs. Crucially, a Mega-Server is a **Single Point of Failure (SPoF)**. If the motherboard fries, or the datacenter loses power, your entire global application instantly goes offline. 

**The Invincibility of Horizontal Scaling**:
Horizontal architectures natively provide **High Availability (HA)** and Fault Tolerance. If a meteor strikes a datacenter and instantly vaporizes 5 backend servers, the Load Balancer detects the dead nodes via Health Checks within milliseconds. It seamlessly reroutes all incoming traffic to the surviving 95 nodes located in a different geographical zone. The end-users experience absolutely zero downtime.

---

## Layer 3: Without vs. With Comparison (Compare)

### Vertical vs Horizontal Architecture

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Bảng so sánh để biết khi nào chọn chiến lược nào.
</details>

Architectural tradeoffs between the two paradigms.

| Feature | Vertical Scaling (Scale Up) | Horizontal Scaling (Scale Out) |
|---|---|---|
| **Limit** | Hard Physical Limit (Max RAM/CPU). | Theoretically Infinite Limit. |
| **Downtime** | Usually requires Reboot downtime. | Zero Downtime (Nodes are added live). |
| **Complexity** | Zero Code changes. Super simple. | Very Complex. Requires Load Balancers, Distributed Caching, and Stateless Code. |
| **Fault Tolerance**| Catastrophic (Single Point of Failure).| Perfect (Redundant architecture). |
| **Primary Target**| Monolithic Relational Databases (SQL). | Web Servers, Microservices, NoSQL DBs. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Dùng Vertical Scaling cho SQL Database**: Các CSDL như MySQL hay Postgres được thiết kế từ hàng chục năm trước, chúng cực kỳ ghét việc bị cắt nhỏ ra nhiều máy chủ (Lỗi toàn vẹn dữ liệu). Do đó, cách duy nhất để Database chạy nhanh là nạp tiền mua con Server to nhất, RAM khủng nhất cho nó.
- **Dùng Horizontal Scaling cho Web Server (Backend)**: Code API (Node.js/Java) nếu thiết kế chuẩn Stateless (Không giữ trạng thái) thì cực kỳ dễ nhân bản. Shopee có thể mở rộng từ 10 con API Server lên 1000 con trong 5 giây mà không gặp bất kỳ lỗi gì.
- **Auto-Scaling (Tự động co giãn)**: Kết hợp Load Balancer với Cloud. Nửa đêm ít khách, Cloud tự động tắt bớt 80 Server đi cho đỡ tốn tiền. Sáng ra đông khách, Cloud tự động bật 80 con Server lên lại.

</details>

- **Vertical Sweet Spot (Relational Databases)**: Traditional ACID-compliant SQL Databases (PostgreSQL, MySQL, Oracle) are notoriously hostile to Horizontal Scaling. Synchronizing strict transactional locks across a network partition destroys performance. Therefore, the industry standard is to vertically scale the Master Database node to the absolute maximum hardware limits possible before attempting complex sharding.
- **Horizontal Sweet Spot (Stateless Microservices)**: REST API Backend Servers (Node.js, Go, Java) are the perfect candidates for Horizontal Scaling. Because they are stateless (meaning they do not store user session data in their local RAM), you can seamlessly clone 1,000 identical Docker containers across a Kubernetes cluster. 
- **Auto-Scaling Groups (ASG)**: The ultimate Cloud paradigm. A Load Balancer constantly monitors CPU utilization. If average CPU hits 80%, the ASG automatically provisions and injects 5 new VMs into the cluster. At 3:00 AM when traffic dies, it automatically terminates them to save OpEx costs.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Stateless là luật thép**: Nếu bạn lưu biến `userLoggedIn = true` vào RAM của Server 1. Khi Load Balancer đẩy Request tiếp theo của User đó sang Server 2, Server 2 sẽ báo "Bạn chưa đăng nhập" (Vì nó đâu có RAM của Server 1). Code của bạn BẮT BUỘC phải dùng JWT Token (Gửi qua mạng) hoặc dùng Redis tập trung để lưu trạng thái đăng nhập. Không có Stateless thì không thể Scale Ngang.
2. **Health Checks cho Load Balancer**: Ông bảo vệ (Load Balancer) không có mắt. Phải viết một đường dẫn API (Ví dụ: `/ping`) trả về HTTP 200. Cứ 5 giây ông bảo vệ lại gõ cửa `/ping` một lần. Nếu Server bị treo không đáp lại, bảo vệ tự động gạch tên Server đó ra khỏi danh sách chia khách.

</details>

1. **The Iron Law of Statelessness (12-Factor App)**: Horizontal scaling instantly fails if your application stores state (e.g., User Sessions, uploaded images) on the local filesystem or RAM. If User A authenticates on Node 1, and the Load Balancer routes their subsequent request to Node 2, Node 2 will reject them because it lacks the session memory. **Mandatory Rule**: All persistent state must be strictly outsourced to a centralized backing service (e.g., JWT for stateless auth, Redis for Session caching, AWS S3 for Image storage). The Web Servers must be treated as disposable, identical, stateless calculators.
2. **Rigorous L7 Health Checks**: A Load Balancer is blind. If Node 3 suffers a Deadlock in its Java code, the physical VM is technically still "Alive" (Network port is open), but the application is frozen. If the Load Balancer continues routing traffic to Node 3, users get Blackholed. You must implement deep Application-Layer (L7) Health Check endpoints (e.g., `GET /health/ready`). The Load Balancer pings this every 5 seconds. If the endpoint fails to return `HTTP 200 OK`, the Load Balancer instantly evicts the Node from the routing pool.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lạm dụng "Sticky Sessions" (Cố chấp lưu Session)**: Dev lỡ code tệ (Lưu biến vào RAM). Không scale ngang được. Thay vì đập đi viết lại cho chuẩn Stateless, dev cầu cứu SysAdmin bật tính năng "Sticky Session" trên Load Balancer (Ép khách A lần sau bắt buộc phải vào lại Server 1). Tính năng này phá nát mọi thuật toán cân bằng tải, làm Server 1 thì quá tải chết ngất, Server 2 thì ngồi đuổi ruồi.
2. **Quên cấu hình Throttling (Rate Limiting) ở Load Balancer**: Bão traffic kéo đến, Load Balancer nai lưng ra chia khách cho 100 Server. Nhưng 100 Server đó lại lao vào truy vấn đúng 1 con Database duy nhất ở dưới đáy. Database chết tươi. Load Balancer không bảo vệ được Database. Phải cài đặt giới hạn tốc độ (Rate Limit) ở cửa ngõ để chặn bớt nếu traffic có dấu hiệu quá hung hãn.

</details>

1. **The "Sticky Sessions" Anti-Pattern**: A developer engineers a stateful application. To "fix" the horizontal scaling bug, they configure the Load Balancer to utilize "Sticky Sessions" (injecting a cookie that strictly pins User A to Node 1 forever). This is architectural poison. It entirely defeats the purpose of Load Balancing. If Node 1 randomly receives 5 "Heavy" users, Node 1 melts down, while Node 2 and Node 3 sit entirely idle because the Load Balancer is forbidden from redistributing the pinned traffic. **Fix the code; do not use Sticky Sessions.**
2. **The Database Bottleneck Illusion**: A team flawlessly configures a Kubernetes Auto-Scaler. Traffic hits, and the Web Tier scales from 10 to 200 nodes. However, those 200 Web Nodes suddenly open 10,000 simultaneous TCP connections to the single, vertically-scaled PostgreSQL Master Database. The Database immediately runs out of connection sockets and crashes. The Auto-Scaler "succeeded" in scaling the compute layer, but ultimately acted as a distributed Denial of Service attack against its own database. Caching layers (Redis) must be implemented to shield the Database from horizontal web scaling.

---

## Related Topics

- For packaging code into lightweight units for Horizontal Scaling, see **[Virtualization & Containers](./virtualization-containers.md)**.
- For databases that scale horizontally natively, explore **[NoSQL Fundamentals](../database/nosql-fundamentals.md)**.
- See how Load Balancers manage networks in **[TCP/IP Model](../network/tcp-ip.md)**.
