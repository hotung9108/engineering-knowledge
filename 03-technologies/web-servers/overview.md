# Web Servers & Proxies Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Backend (như Node.js hay Java) là những "Người thợ" nấu ăn trong bếp, thì **Web Server (Máy chủ Web)** và **Proxy (Máy chủ Trung gian)** là những "Bảo vệ" và "Lễ tân" đứng ở ngoài cửa nhà hàng. Khi có hàng triệu người dùng truy cập vào trang web của bạn cùng một lúc, những người thợ nấu ăn sẽ bị quá tải và chết ngộp nếu phải trực tiếp ra tiếp khách. Web Server đứng ra chắn toàn bộ lưu lượng đó. Nó kiểm tra thẻ căn cước (Bảo mật), nó lấy sẵn những món ăn làm sẵn trên bàn đưa cho khách (Caching), và nó phân chia khách hàng đều ra cho các thợ nấu khác nhau để không ai bị quá tải (Load Balancing). Không một hệ thống lớn nào dám để Backend của mình phơi mặt trực tiếp ra Internet mà không có Proxy che chắn phía trước.

</details>

> **Summary**: Exposing an application server (like a Node.js, Python, or Java process) directly to the public Internet is a massive architectural anti-pattern. These application runtimes are engineered to execute complex business logic, not to securely and efficiently juggle 100,000 concurrent, slow TCP connections or defend against DDoS attacks. **Web Servers and Reverse Proxies** act as the hardened, high-performance edge of your infrastructure. Written in low-level languages (C, C++, Rust), they sit directly in front of your application. They absorb massive network traffic, terminate SSL/TLS encryption securely, serve static assets (HTML/CSS/Images) directly from RAM, and act as **Load Balancers**—intelligently routing incoming requests across a fleet of backend servers to guarantee high availability and horizontal scalability.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một Tòa cao ốc văn phòng (Hệ thống máy chủ).
1. **Không có Proxy**: Bất kì ai ngoài đường (Người dùng) cũng có thể mở cửa, đi thẳng vào thang máy, và xông vào bàn làm việc của nhân viên (Backend) để đưa giấy tờ. Rất nguy hiểm (Hacker), và nhân viên sẽ liên tục bị làm phiền, không làm việc được.
2. **Có Proxy (Lễ tân & Bảo vệ)**: Tòa nhà thuê một người Lễ tân cực kì chuyên nghiệp đứng ở Cửa chính (Cổng số 80/443).
   - *Bảo mật*: Lễ tân kiểm tra CMND. Nếu khả nghi (DDoS), đuổi ra ngay lập tức.
   - *Static Files*: Khách chỉ xin Tờ rơi quảng cáo (Hình ảnh, CSS)? Lễ tân rút trong ngăn kéo đưa luôn, khỏi cần gọi nhân viên ra.
   - *Load Balancing (Cân bằng tải)*: Khách muốn nộp hồ sơ, Lễ tân nhìn camera thấy Nhân viên A đang bận, bèn chỉ khách sang nộp cho Nhân viên B đang rảnh. 

</details>

Imagine a high-security Corporate Building.
1. **Direct Connection (No Proxy)**: Any random person off the street can walk straight into the building, wander the halls, and walk directly to an accountant's desk to hand them a document. The accountant gets constantly interrupted by lost people, malicious intruders, and spam mail.
2. **Reverse Proxy (The Front Desk Receptionist)**: The building installs an impenetrable Glass Door and hires a hyper-fast Receptionist.
   - *SSL Termination*: The Receptionist checks everyone's ID and decrypts their sealed briefcases at the door.
   - *Static Serving*: If a visitor just wants a generic Brochure (Static HTML/CSS files), the Receptionist hands it to them instantly from a pile on the desk. The accountant is never bothered.
   - *Load Balancing*: If a visitor needs tax help, the Receptionist checks which of the 5 accountants in the back room currently has the shortest line, and explicitly routes the visitor to that specific desk.

---

## Layer 1: Forward Proxy vs Reverse Proxy (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cần phân biệt rõ hai loại Proxy này vì chúng hoàn toàn trái ngược nhau:
1. **Forward Proxy (Bảo vệ Người Dùng)**: Bạn ngồi trong công ty, Sếp cài một cái Forward Proxy. Bạn muốn truy cập Facebook. Máy tính của bạn không ra thẳng Facebook, mà gửi yêu cầu cho Proxy. Proxy nhận thấy "Facebook bị cấm", nó chặn lại. Nếu là Google, nó thay mặt bạn chạy ra Google lấy dữ liệu rồi đem về cho bạn. (VPN cũng là một dạng Forward Proxy).
2. **Reverse Proxy (Bảo vệ Máy Chủ)**: Ngược lại hoàn toàn. Nó đứng quay mặt ra Internet để bảo vệ Máy chủ của bạn. Người dùng bên ngoài tưởng họ đang nói chuyện với Máy chủ xịn, nhưng thực ra họ đang nói chuyện với thằng Lễ tân (Reverse Proxy). Thằng Lễ tân sẽ che giấu hoàn toàn danh tính và địa chỉ IP thực sự của các Máy chủ giấu ở đằng sau. (Nginx, HAProxy là Reverse Proxy).

</details>

The foundational terminology of Proxies depends on *who* they are protecting:
1. **Forward Proxy (Protects the Client)**: A server sitting between a private local network (e.g., a corporate office) and the public Internet. When a corporate employee tries to access `reddit.com`, the request hits the Forward Proxy first. The proxy evaluates corporate firewall rules, masks the employee's internal IP address, and fetches the site on their behalf. VPNs function as Forward Proxies.
2. **Reverse Proxy (Protects the Server)**: A server sitting directly in front of the Application Servers (Backend). When an external user goes to `api.netflix.com`, they are NOT connecting to a Node.js or Java server. They are connecting to a Reverse Proxy. The proxy intercepts the request, hides the internal IP addresses of the actual backend servers, and acts as the public face of the entire infrastructure. (This guide focuses entirely on Reverse Proxies).

---

## Layer 2: Why do they exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vì sao không cho Node.js hay Spring Boot mở cổng 80 chạy thẳng ra Internet?
1. **Quản lý Kết nối Chậm (Slowloris Attack)**: Kẻ tấn công mở 10.000 kết nối tới Node.js, nhưng mỗi giây nó chỉ gửi 1 byte dữ liệu. Nó không vi phạm luật, nhưng nó "ngâm" kết nối đó. Node.js sẽ bị kẹt cứng 10.000 luồng và sập ngay lập tức. Nginx (được viết bằng C) sinh ra để ôm 1 triệu kết nối chậm như vậy mà chỉ tốn vài MB RAM. Nginx ôm kết nối, khi nào Hacker gửi xong CẢ CÂU, Nginx mới đẩy cục dữ liệu đó cho Node.js xử lý trong 1 mili-giây.
2. **Mã hóa SSL/TLS (HTTPS)**: Tính toán mã hóa SSL cực kì tốn CPU. Nếu bắt Backend vừa tính toán Logic kinh doanh, vừa giải mã SSL, CPU sẽ cháy. Người ta giao việc giải mã (SSL Termination) cho Nginx. Nginx giải mã thành văn bản thường (HTTP), rồi mới gửi vào Backend.
3. **Cân bằng tải (Load Balancing)**: Một máy chủ Node.js không thể gánh 1 triệu người dùng. Bạn phải bật 10 máy chủ Node.js lên. Lúc này, bạn BẮT BUỘC phải có một cái Reverse Proxy đứng ở giữa để chia đều khách hàng ra 10 máy đó (Thuật toán Round-Robin).

</details>

Why is it an anti-pattern to expose an Application Server (e.g., Express.js, Tomcat, Kestrel) directly to the Internet?
1. **Asynchronous Connection Handling & Slowloris Protection**: Application runtimes allocate significant memory per active connection. A hacker can execute a "Slowloris" attack by opening 10,000 TCP connections and sending data exactly 1 byte per second. A Node.js server will hold those 10,000 requests in memory, exhaust its RAM, and crash. Nginx operates on an Event-Driven architecture in C. It can hold 1,000,000 concurrent idle connections using mere megabytes of RAM. Nginx fully buffers the slow incoming request, and ONLY when the entire payload is completely received does it forward it to Node.js.
2. **SSL/TLS Termination Overhead**: Encrypting and decrypting HTTPS traffic involves heavy mathematical CPU computations (RSA/ECC handshakes). Forcing your Application Server to handle SSL steals CPU cycles away from your business logic. A Reverse Proxy handles **SSL Termination** at the network edge using highly optimized C libraries (OpenSSL). It decrypts the traffic and forwards plain, unencrypted HTTP to the backend inside the secure internal VPC.
3. **Horizontal Scaling (Load Balancing)**: A single Node.js process utilizes exactly one CPU core. To handle massive scale, you must deploy 50 identical Node.js servers. The Internet cannot point to 50 IPs. The Reverse Proxy acts as the single public IP address, mathematically distributing incoming traffic across the 50 backend servers using algorithms like Round-Robin or Least-Connections.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình một người dùng vào trang web xem một bức ảnh và tải dữ liệu người dùng.
</details>

Visualizing Traffic Flow (Direct Server vs Reverse Proxy).

| Metric | Without Proxy (App Server Only) | With Reverse Proxy (Nginx) |
|---|---|---|
| **Serving an Image (`logo.png`)** | The backend Node.js code must read the file from disk and stream it. Node.js gets blocked doing disk I/O. | Nginx intercepts the `/logo.png` request. It serves it directly from its RAM cache. **Node.js never even knows the user asked for it.** |
| **Handling 5,000 concurrent users** | 1 Node.js server reaches 100% CPU. The 5,001st user gets a "Timeout Error". | Nginx receives 5,000 requests and perfectly distributes 1,000 requests each to 5 different Node.js backend servers. All users are served quickly. |
| **Updating the Server (Deploying Code)**| To update the code, you must turn off the server. The website goes offline for 5 seconds. | **Zero Downtime**. Nginx gracefully routes traffic away from Server 1, you update it, then Nginx routes traffic back. |

---

## Layer 4: Common Architectures & Roles

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thế giới Proxy được phân tầng rất rõ ràng từ thời đại máy chủ vật lý đến kỷ nguyên Đám mây (Cloud Native):
1. **Web Server / Reverse Proxy Truyền thống (Nginx, Apache)**: Cài đặt trực tiếp lên hệ điều hành Linux. Dùng để làm máy chủ phục vụ các trang web tĩnh (HTML, CSS), giải mã SSL, và cân bằng tải đơn giản cho các ứng dụng nhỏ đến vừa.
2. **Layer 4 Load Balancer (HAProxy)**: Một cỗ máy Cân bằng tải thuần túy hoạt động ở Tầng 4 (Tầng Mạng - TCP/UDP). Nó không thèm đọc nội dung bên trong gói tin HTTP là gì, nó chỉ nhìn IP và Cổng, rồi ném gói tin đi nhanh nhất có thể. Dùng làm cân bằng tải siêu tốc cho Database.
3. **Layer 7 Cloud-Native Proxy (Envoy, Traefik)**: Kỷ nguyên Microservices (Kubernetes). Khi bạn có 1000 Microservices thay đổi IP liên tục mỗi giây. Nginx truyền thống bị đuối sức. Khái niệm **Service Mesh** ra đời. Envoy sinh ra để đọc thấu hiểu nội dung API (Tầng 7 - HTTP/gRPC), tự động tìm đường đi ngắn nhất giữa hàng ngàn Microservices nội bộ với nhau.

</details>

The Proxy landscape is categorized by the OSI Model layers they operate on and the architectural eras they dominate:
1. **Traditional Web Servers / Layer 7 Proxies (Nginx, Apache)**: The stalwarts of the Internet. They operate at Layer 7 (Application Layer). They decrypt HTTPS, read the actual URL path (`/api/v1` vs `/images`), and make intelligent routing decisions based on the HTTP Headers. Nginx remains the most widely deployed web server on Earth.
2. **Layer 4 TCP Load Balancers (HAProxy)**: Operating at the Transport Layer. They do not decrypt SSL. They do not read HTTP Headers. They simply look at the source and destination IP/Ports and blindly, furiously shuttle raw TCP packets back and forth. Because they bypass Layer 7 parsing overhead, they are utilized for ultra-high-throughput routing (e.g., Load Balancing raw TCP connections to a PostgreSQL database cluster).
3. **Cloud-Native Proxies & Service Mesh (Envoy, Traefik)**: The modern era of Kubernetes. In a dynamic cluster, hundreds of Pods (Containers) die and respawn every minute, constantly changing their IP addresses. Legacy proxies require manual config reloading. Envoy is an API-driven proxy that dynamically auto-discovers endpoints. It is deployed as a "Sidecar" next to every single Microservice, forming a "Service Mesh" that manages internal gRPC/HTTP routing, automatic retries, and circuit breaking implicitly.

---

## Related Topics

- For the undisputed industry standard in Web Servers and Reverse Proxies, proceed to **[Nginx](./nginx.md)**.
- For raw, high-performance TCP/UDP Layer 4 Load Balancing, explore **[HAProxy](./haproxy.md)**.
- For modern, Cloud-Native API Gateways and Kubernetes Service Mesh routing, see **[Envoy](./envoy.md)**.
- For how Proxies protect backend logic, review **[Backend Overview](../backend/overview.md)**.
