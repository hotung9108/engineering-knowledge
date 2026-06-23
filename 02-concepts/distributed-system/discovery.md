# Service Discovery

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Bạn có 2 cái máy tính. Muốn Máy A gọi API sang Máy B, bạn chỉ cần gõ thẳng `http://192.168.1.5` vào code của Máy A. Xong! Rất dễ. Nhưng với Microservices (như Docker/Kubernetes), Máy B hôm nay có IP này, ngày mai bị khởi động lại nó nhảy sang IP khác. Nếu cứng nhắc ghi IP vào code, Máy A sẽ gọi hụt và chết ngắc. **Service Discovery (Khám phá dịch vụ)** ra đời như một "Cuốn danh bạ điện thoại tự động". Máy A chỉ việc hỏi: "Danh bạ ơi, Service B đang ở địa chỉ IP nào?". Danh bạ sẽ trả về IP mới nhất của B, và A sẽ gọi mượt mà.

</details>

> **Summary**: In static legacy architectures, inter-service communication relied on hardcoded IP addresses or DNS A-records bound to permanent physical servers. In modern Cloud-Native architectures (Kubernetes, AWS Auto Scaling), infrastructure is entirely ephemeral. A `BillingService` pod might be destroyed and instantly recreated with a completely different IP address 50 times a day. If the `OrderService` hardcodes the IP, the request drops into a black hole. **Service Discovery** is the dynamic registry architecture—a highly available, realtime "Phonebook"—that allows ephemeral microservices to dynamically register their current network locations and seamlessly discover the dynamic IPs of their upstream dependencies.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn cần đi ăn Phở ở quán ông Tuấn.
1. **Kiểu Cổ điển (Hardcode IP)**: Bạn chốt chết trong đầu: "Quán phở ông Tuấn ở số 54 Nguyễn Trãi". Thế là bạn chạy xe đến đó. Nhưng hôm qua ông Tuấn mới chuyển mặt bằng sang số 99 Lê Lợi. Bạn đến số 54 thấy nhà trống $\rightarrow$ Bạn nhịn đói (Hệ thống sập).
2. **Service Discovery (Danh bạ động)**: Bạn KHÔNG NHỚ địa chỉ cụ thể nữa. Thay vào đó, bạn gọi điện cho bà Tổng Đài (Service Registry): "Chị ơi, quán phở ông Tuấn giờ ở đâu?". Bà Tổng đài kiểm tra sổ: "Sáng nay ổng mới báo dời sang 99 Lê Lợi em nhé". Bạn chạy tới 99 Lê Lợi và ăn phở ngon lành. Ông Tuấn có dọn nhà 100 lần 1 ngày thì bạn vẫn tìm được ổng, miễn là ổng báo cho Tổng đài biết.

</details>

Imagine trying to find your friend Bob's house.
1. **Hardcoded IP (Static Routing)**: You memorize Bob's address: "123 Main Street". You drive there. However, Bob is an ephemeral cloud nomad. He moved to "456 Elm Street" yesterday. You show up at Main Street, knock on the door, and a stranger answers. You fail to deliver your message.
2. **Service Discovery (Dynamic Registry)**: You stop memorizing addresses. Instead, you call your mutual friend Alice (The Service Registry). Every time Bob moves, he immediately texts Alice his new address. You ask Alice: "Where is Bob right now?". Alice replies: "456 Elm Street." You drive there and find Bob. Bob can move 100 times a day, and you will never lose him.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Kiến trúc Service Discovery có 2 mảng chính:
1. **Service Registry (Cuốn danh bạ)**: Một cái Database chuyên biệt nằm giữa mạng LAN (Ví dụ: Eureka, Consul, ZooKeeper). Nhiệm vụ duy nhất của nó là lưu một cái bảng Map: `Tên Service -> Danh sách [IP1, IP2, IP3]`.
2. **Quá trình Đăng ký (Registration)**: Khi một Container của Service B vừa khởi động xong, việc ĐẦU TIÊN nó làm là gọi điện lên Registry: "Báo cáo, tôi là Service B, tôi đang sống ở IP `10.0.0.5`, nhớ lưu tôi vào sổ!". Khi nó sắp chết, nó cũng phải gọi điện: "Xóa tên tôi đi, tôi sập đây!".

</details>

The architecture strictly comprises two core operations revolving around a central database:
1. **The Service Registry (The Database)**: A highly-available, CP/AP key-value store (e.g., HashiCorp Consul, Netflix Eureka, Apache ZooKeeper). It maintains the global routing table mapping logical service names to physical network locations: `["PaymentService" -> ["10.0.0.5:8080", "10.0.0.6:8080"]]`.
2. **Service Registration (The Handshake)**: The microservice lifecycle hook. The absolute moment a new `PaymentService` Docker container finishes booting up and becomes healthy, it executes a `POST` request to the Registry: "I am PaymentService, my dynamic IP is `10.0.0.5`." The Registry appends it. When the container gracefully shuts down, it sends a `DELETE` request to de-register itself.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Môi trường Ephemeral (Phù du)**: Máy ảo (EC2) hoặc Container (Docker/K8s) ngày nay sinh ra và chết đi liên tục do Auto-Scaling (Tự động tăng giảm tải). Buổi tối ít khách, hệ thống tự tắt bớt 5 cái Server B để tiết kiệm tiền điện. IP của 5 cái Server đó biến mất. Sáng hôm sau đông khách, nó bật lại 5 cái Server B mới tinh với 5 cái IP hoàn toàn khác. Mọi thứ thay đổi điên cuồng, không thể dùng con người để cấu hình file DNS bằng tay được.
**2. Cân bằng tải phía Client (Client-side Load Balancing)**: Nếu Máy A hỏi Danh bạ và biết Máy B đang chạy ở 3 IP là `[IP1, IP2, IP3]`. Máy A sẽ TỰ CHỌN 1 trong 3 IP đó để gọi (Hôm nay gọi IP1, mai gọi IP2). Việc này giúp Máy A tự cân bằng tải mà không cần phải tốn tiền mua thêm 1 cục Hardware Load Balancer (như F5 hay Nginx) đặt ở giữa.

</details>

**1. Ephemeral Infrastructure (Auto-Scaling)**: Modern cloud economics dictate horizontal Auto-Scaling. At 2:00 AM, AWS kills 10 `InventoryService` EC2 instances to save costs. At 8:00 AM, traffic spikes, and AWS spins up 20 brand new instances. These instances are dynamically assigned random private IPs from the VPC CIDR block. Traditional DNS (which heavily relies on TTL caching and manual propagation) is entirely too slow and brittle to map this violently shifting topography. You need a registry that updates in milliseconds.
**2. Enabling Client-Side Load Balancing**: The traditional approach relies on an explicit Server-Side Load Balancer (AWS ALB / Nginx). Service A calls `http://nginx-internal`, and Nginx routes to Service B. Nginx becomes a Single Point of Failure and a network hop bottleneck. With Service Discovery, Service A queries the Registry, receives an array of 5 IPs for Service B, and Service A uses an internal library (like Netflix Ribbon or Spring Cloud LoadBalancer) to execute Round-Robin routing *directly* from A to B. It cuts out the middleman entirely.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh luồng chạy khi một Server vô tình bị cháy.
</details>

Visualizing the routing behavior when a downstream dependency experiences a hardware failure.

| Step | Hardcoded DNS / Static IPs | Service Discovery (Consul / Eureka) |
|---|---|---|
| **1. Normal State** | Service A calls `10.0.0.5`. Works fine. | Service A queries Registry, gets `10.0.0.5`. Works fine. |
| **2. Node Crash** | Server `10.0.0.5` loses power abruptly. | Server `10.0.0.5` loses power abruptly. |
| **3. Reaction** | Service A knows nothing. | Registry's 5-second Health Check to `10.0.0.5` fails. |
| **4. Routing Update**| System admins must manually update DNS (Takes 10 mins). | Registry instantly deletes `10.0.0.5` from its table. |
| **5. User Impact** | All requests from A to B fail for 10 minutes. | Service A queries Registry again, gets the backup IP `10.0.0.6`. Zero downtime. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Kubernetes (K8s Service)**: Kubernetes có tích hợp sẵn hệ thống Service Discovery đỉnh cao nhất thế giới (CoreDNS + kube-proxy). Khi bạn viết code trên K8s, Máy A chỉ cần gọi đúng cái tên miền nội bộ `http://service-b.default.svc`. Kubernetes sẽ tự động bắt lấy yêu cầu đó, tra cuốn danh bạ ngầm của nó, và đẩy gói tin đến đúng IP của Máy B. Lập trình viên không cần phải cài đặt thêm Eureka hay Consul làm gì cho mệt mỏi.
2. **Spring Cloud Netflix (Hệ sinh thái Java)**: Trong thế giới Java đời cũ chưa có Kubernetes, các công ty dùng Netflix Eureka. Máy A phải cài thư viện Eureka Client vào code. Tự tra danh bạ, tự gọi. 
3. **Consul (HashiCorp)**: Thường dùng ở các công ty lớn xài máy chủ vật lý (Bare Metal) hoặc mix giữa Cloud và máy tự ráp. Consul tra danh bạ siêu nhanh và có tính năng kiểm tra sức khỏe (Health Check) cực kỳ tàn bạo.

</details>

1. **Kubernetes Native (CoreDNS / kube-proxy)**: The ultimate abstraction. If you deploy into a Kubernetes cluster, you practically never explicitly implement Service Discovery. K8s does it natively. You deploy an `Order` Pod and expose it via a K8s `Service`. Your `Payment` Pod simply executes `GET http://order-service:8080`. CoreDNS resolves the name, and `kube-proxy` transparently intercepts the TCP packet and load-balances it to the physical IP of an active Pod. It is entirely invisible to the application code.
2. **Spring Cloud Netflix (Application-Level)**: Popularized by Netflix before the era of Kubernetes. It utilizes Netflix Eureka as the Registry. The actual Java Spring Boot application embeds an `EurekaClient`. The Java code explicitly queries Eureka to fetch the IP array, and then uses Netflix Ribbon to execute client-side Load Balancing. This heavily couples the application code to the infrastructure.
3. **HashiCorp Consul (Infrastructure-Level)**: A highly robust, Raft-consensus-backed registry. Unlike Eureka which relies on the App registering itself, Consul often uses sidecar agents running on the VM. It provides incredibly rigorous Health Checks. If a node CPU spikes to 100%, Consul instantly marks it "Unhealthy" and drops it from the DNS resolution pool, preventing cascading failures.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Health Check (Khám sức khỏe) nghiêm ngặt**: Danh bạ chỉ hữu ích nếu thông tin trong đó là Chính Xác. Máy B bị treo CPU không phản hồi, nhưng chưa chết hẳn nên không thể gọi điện báo hủy đăng ký. Bà Tổng đài (Registry) bắt buộc phải "Nháy máy" (Ping) Máy B mỗi 5 giây. Nếu 3 lần Ping không thấy Máy B trả lời, Tổng đài phải TỰ ĐỘNG GẠCH TÊN Máy B ra khỏi danh bạ ngay lập tức. Nếu không, Máy A sẽ gọi trúng cái IP treo đó và sập theo.
2. **Cache Danh bạ tại Client**: Nếu Máy A gọi Máy B 10.000 lần/giây. Chẳng lẽ Máy A phải hỏi Tổng đài 10.000 lần? Tổng đài sẽ cháy máy! Máy A bắt buộc phải hỏi Tổng đài 1 lần thôi, lấy cái IP đó LƯU VÀO RAM (Cache) của Máy A. Cứ gọi vô cái IP đó liên tục. Chừng nào gọi bị lỗi (Máy B đổi IP), thì Máy A mới chạy lên hỏi Tổng đài lại.

</details>

1. **Rigorous Active Health Checking**: A Registry is worse than useless if it serves stale, dead IP addresses. If Service B enters a JVM Deadlock, it is technically "alive" on the network but completely unresponsive. It won't cleanly de-register itself. The Registry (e.g., Consul) MUST actively execute Health Checks (HTTP `GET /health` or TCP Pings) every ~5 seconds. If Service B fails 2 consecutive checks, the Registry must ruthlessly evict its IP from the routing table. Otherwise, clients will be routed to a dead node, causing brutal timeouts.
2. **Client-Side Caching of the Registry Table**: If `Service A` queries `Service B` 5,000 times per second, executing a synchronous HTTP call to the Eureka Registry before *every single* request will instantly DDoS the Registry. **The Fix**: The `Service A` client MUST fetch the routing table and aggressively cache it in local RAM. It uses the cached IPs to execute 5,000 requests instantly. The Client runs a background daemon thread that polls the Registry every 30 seconds to refresh the cached table.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Rò rỉ IP rác (Stale IPs)**: Khi bạn code lỗi phần Đăng xuất (Deregistration) lúc tắt máy. Máy B bị tắt đi nhưng cuốn danh bạ Eureka không hề bị xóa dòng đó. Khi Máy B bật lại, nó lấy IP mới và đăng ký thêm 1 dòng nữa. Cuốn danh bạ phình to ra chứa hàng đống IP ma. Máy A bốc ngẫu nhiên trúng cái IP ma đó và lỗi tưng bừng. Đây là thảm họa thường gặp nhất.
2. **Tự thiết kế lại Bánh xe**: Đừng cố gắng tự viết một hệ thống "Đăng ký IP" bằng MySQL kết hợp với Cronjob để làm Service Discovery. Nó rất chắp vá và sẽ bị nghẽn mạng khi hệ thống có hàng ngàn Microservices. Hãy dùng các đồ chơi xịn của giới nhà giàu (Consul, K8s, Zookeeper), chúng đã được tối ưu đến mức độ tối đa.

</details>

1. **The "Ghost IP" Leak (Deregistration Failure)**: A container crashes ungracefully (e.g., `OOMKilled` by the Linux kernel). It never gets the chance to execute its shutdown hook to explicitly `DELETE` its IP from the Registry. If the Registry lacks aggressive Health Checks, that dead IP permanently remains in the routing table (A Ghost IP). Load balancers will continuously route 33% of your customer traffic into a black hole. **Rule**: Always enforce short TTLs (Time-To-Live) on registrations. The Service must continuously send "Heartbeats" to renew its TTL. If the container dies, the heartbeats stop, the TTL expires, and the IP is automatically purged.
2. **Reinventing the Wheel via RDBMS**: Junior architects attempt to build custom Service Discovery using a MySQL table (`service_name`, `ip_address`) and an arbitrary API. RDBMS architecture is heavily optimized for persistent relational disk storage, not for high-frequency, ephemeral, RAM-heavy pub/sub network volatility. A MySQL table will suffer massive locking contention under heavy auto-scaling events. Do not reinvent this. Deploy HashiCorp Consul or fully embrace Kubernetes DNS.

---

## Related Topics

- For how Kubernetes abstracts all of this completely, see **[Kubernetes](../../03-technologies/cloud-infrastructure/kubernetes.md)**.
- For the architectural style that forces us into this mess, see **[Microservices vs Monolith](../../10-system-design/architecture-patterns/microservices.md)** (System Design).
- For how the registries stay consistent, see **[Consensus Algorithms](./consensus.md)**.
