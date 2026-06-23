# Envoy Proxy

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Cả Nginx và HAProxy đều là những gã khổng lồ sinh ra từ đầu những năm 2000, thời đại của máy chủ vật lý, nơi một địa chỉ IP (như 1.1.1.1) sống cố định hàng năm trời. Nhưng ở kỷ nguyên Đám mây (Cloud Native / Kubernetes), mọi thứ xoay chuyển chóng mặt: Hàng ngàn thùng chứa (Containers) được sinh ra và chết đi mỗi phút, địa chỉ IP thay đổi liên tục. Nếu dùng Nginx, bạn phải tự mở file `nginx.conf` ra sửa IP bằng tay rồi khởi động lại máy chủ liên tục, hệ thống sẽ sụp đổ. Lyft (đối thủ của Uber) đã tạo ra **Envoy Proxy**. Khác với các bậc tiền bối, Envoy sinh ra để được "điều khiển bằng API". Bạn không cần viết file cấu hình tĩnh, một máy chủ trung tâm sẽ bắn API liên tục vào Envoy để cập nhật danh sách IP mới nhất mà không cần Restart. Sự linh hoạt tuyệt đối này biến Envoy thành trái tim của kiến trúc **Service Mesh** (Lưới dịch vụ) hiện đại.

</details>

> **Summary**: Nginx and HAProxy were architected in the pre-cloud era of static infrastructure, where backend server IPs remained constant for months. They rely on static configuration files (e.g., `nginx.conf`) that require manual updates and process reloads to register new downstream servers. In the modern Kubernetes (Cloud-Native) era, where Ephemeral Pods scale up and die every few seconds, IPs are completely dynamic. Relying on static reloads causes catastrophic configuration drift and dropped connections. To solve this, Lyft engineered **Envoy Proxy**. Built in modern C++11, Envoy was designed from day one to be API-driven. It completely abandons static configuration files in favor of dynamic xDS APIs. A control plane streams topology changes to Envoy in real-time, allowing it to instantly discover new backend services without ever restarting. Because of its dynamic nature and first-class support for HTTP/2 and gRPC, Envoy has become the universal foundation for modern **Service Mesh** architectures (e.g., Istio).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một người Giao hàng (Proxy).
1. **Nginx (Bản đồ giấy)**: Người giao hàng được phát một tấm Bản đồ giấy in sẵn (File Config). Cứ 1 tiếng, nếu thành phố có xây đường mới, sếp phải gọi người giao hàng quay về bưu điện, vứt bản đồ cũ đi, phát bản đồ mới (Restart Nginx). Nếu thành phố đổi đường liên tục mỗi giây (Kubernetes), người giao hàng sẽ cứ chạy về bưu điện mãi mà không giao được hàng.
2. **Envoy Proxy (Google Maps)**: Người giao hàng được phát một cái Điện thoại có GPS, kết nối mạng 24/7 (xDS API). Nếu một con đường vừa bị chặn (Server chết) hoặc một cây cầu mới vừa xây (Server mới), sếp bấm nút gửi dữ liệu cập nhật thẳng vào điện thoại ngay lập tức. Người giao hàng tự động né đường kẹt xe mà không cần ngừng lại một giây nào. Tốc độ và sự liền mạch là tuyệt đối.

</details>

Imagine driving a Taxi.
1. **Nginx (The Printed Map)**: The driver uses a printed paper map (`nginx.conf`). If a new restaurant opens, or a road is closed due to a crash, the driver doesn't know. The Dispatcher must physically force the driver to stop the car, throw away the old map, and memorize a brand new printed map (Reload). In a city where roads change every second (Kubernetes), the driver is constantly stopping.
2. **Envoy (The Live GPS Navigation)**: The driver uses a live GPS screen (The xDS API). The Dispatcher maintains a live data stream to the car. The exact millisecond a road closes, the GPS line instantly turns red, and the route dynamically adjusts without the driver ever touching the brakes. The configuration updates transparently in real-time.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Envoy là một Cỗ máy Proxy Lớp 7 siêu việt với 3 vũ khí chính:
1. **Cấu hình động (Dynamic Configuration)**: Như đã nói, Envoy không chuộng file Text. Nó giao tiếp với một máy chủ điều khiển (Control Plane) qua giao thức gRPC. Bất cứ khi nào cấu trúc mạng thay đổi, nó tự cập nhật ngay lập tức (Zero-downtime).
2. **Hỗ trợ gRPC nguyên bản (First-Class gRPC)**: Trong khi Nginx chật vật để xử lý gRPC (Mã nhị phân), Envoy được sinh ra cùng thời với gRPC. Nó đọc, hiểu và cân bằng tải gRPC, HTTP/2 dễ như ăn kẹo. Nó thậm chí có thể làm "Phiên dịch viên" gRPC-Web (Cho phép Frontend dùng JSON nói chuyện với Backend gRPC).
3. **Khả năng quan sát (Observability)**: Khi có 100 Microservice, tìm ra lỗi ở đâu là ác mộng. Envoy tự động sinh ra các báo cáo chi tiết: Yêu cầu này mất bao nhiêu mili-giây, lỗi ở chặng số mấy, tỉ lệ lỗi là bao nhiêu. Bạn không cần tự viết code đo lường nữa.

</details>

Envoy is a high-performance Layer 7 proxy and communication bus designed for large modern service-oriented architectures:
1. **The xDS APIs (Dynamic Discovery)**: The defining feature of Envoy. Instead of editing static files, a centralized Control Plane (like Istio) pushes state changes to Envoy instances via gRPC streams. These APIs dynamically update Envoy's Endpoint Discovery (EDS), Cluster Discovery (CDS), and Route Discovery (RDS). Envoy updates its internal routing tables instantaneously without dropping a single active connection.
2. **First-Class HTTP/2 & gRPC Support**: Nginx was retrofitted to support HTTP/2. Envoy was built entirely around it. It natively understands gRPC multiplexing. It can load-balance individual gRPC calls across a cluster, whereas legacy Layer 4 proxies can only load-balance the persistent TCP connection (which breaks gRPC scaling). It also natively acts as a gRPC-Web translation proxy.
3. **Deep Observability**: In a distributed system, tracing a slow request across 50 hops is nearly impossible. Envoy intrinsically generates massive amounts of statistics, distributed tracing spans (Zipkin/Jaeger), and logging. It intercepts the traffic and automatically measures latency, success rates, and retries, pushing the telemetry directly to Prometheus without developers writing a single line of instrumentation code.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong thời đại Microservice, 1 Service muốn gọi Service khác, nó phải tự viết code: `Thử gọi máy 1, nếu lỗi thì gọi máy 2 (Retry), nếu máy 2 lỗi quá 3 lần thì ngắt luôn (Circuit Breaker), phải gửi kèm mã theo dõi (Tracing)`.
Nếu công ty có 100 Service (Dùng đủ loại ngôn ngữ Java, Go, Python). Việc bắt TẤT CẢ LẬP TRÌNH VIÊN phải tự viết lại đống code mạng lằng nhằng trên là thảm họa.
Envoy sinh ra để tạo thành **Service Mesh (Lưới dịch vụ)**. Người ta không cài Envoy ở Cổng chính (Gateway) nữa. Người ta nhét 1 con Envoy nhỏ xíu ĐỨNG SÁT BÊN CẠNH từng cái Microservice (gọi là Sidecar). 
Từ nay, code Java chỉ cần gọi mù quáng ra `localhost`. Con Envoy đứng cạnh nó sẽ hứng lấy tín hiệu, tự tìm đường đi nhanh nhất, tự thử lại nếu lỗi, tự mã hóa bảo mật, rồi ném sang con Envoy của máy đích. Các Lập trình viên Backend được giải phóng hoàn toàn khỏi nỗi lo về Mạng lưới.

</details>

Envoy exists to abstract the Network completely away from the Application Code.
In a legacy microservice architecture, every single application (written in Java, Go, or Node) must independently implement complex networking libraries to handle Retries, Circuit Breaking, Timeout Logic, Service Discovery, and Distributed Tracing. Re-implementing and maintaining these complex libraries across 5 different programming languages is an architectural nightmare.
Envoy introduces the **Service Mesh (Sidecar Pattern)**. You deploy a tiny, ultra-fast Envoy Proxy inside the exact same Kubernetes Pod as your Application container. The Application code is now entirely dumb; it simply executes `HTTP GET localhost:8000`. The Envoy Sidecar intercepts the outgoing request. Envoy handles the Service Discovery, negotiates the mTLS encryption, routes to the destination Envoy Sidecar, handles automatic retries on failure, and reports tracing metrics. The Developers focus 100% on Business Logic, and the DevOps team manages the Network logic entirely via the Envoy Fleet.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình gọi nội bộ: "Dịch vụ Giỏ hàng gọi Dịch vụ Thanh toán bị sập".
</details>

Visualizing Network Resilience (Code vs Service Mesh).

| Metric | Legacy Microservices (Code) | Envoy Service Mesh (Sidecar) |
|---|---|---|
| **Retry Logic** | The Java Developer must manually write `try/catch` blocks and use libraries like Resilience4J to implement retries and exponential backoff. | The Java code just calls `HTTP GET`. The Envoy sidecar detects the failure and automatically retries 3 times. The Java dev writes 0 lines of network code. |
| **Circuit Breaking** | If Payment is dead, Cart keeps calling it, exhausting its own CPU until the whole system crashes (Cascading Failure). | Envoy detects Payment is dead. It opens the "Circuit Breaker", instantly returning an error to Cart *without* even trying to call Payment over the network. Protects the system. |
| **mTLS Encryption** | Developers must manually load SSL certificates into their Node.js and Python code. | Envoy automatically encrypts all traffic leaving the pod and decrypts it at the destination. The internal Apps communicate in plain text. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Service Mesh (Istio)**: Đây là vị trí "Đế vương" của Envoy. Khi cài Istio vào Kubernetes, Istio (Bảng điều khiển trung tâm) sẽ tự động rải hàng ngàn con Envoy đứng cạnh hàng ngàn cái App của bạn để quản lý mạng toàn bộ hệ thống.
2. **API Gateway cấp cao**: Khi Nginx không đủ "Thông minh" để phân loại các API phức tạp, hoặc hệ thống Backend của bạn dùng gRPC quá nhiều. Envoy (hoặc các dự án dựa trên nó như Gloo Edge, Ambassador) được dùng làm cổng chính tiếp khách từ Internet.
3. **Cổng dịch thuật gRPC-Web**: Khi Web Frontend (React) không gọi được mã Nhị phân gRPC. Nó gửi JSON cho Envoy. Envoy đọc JSON, biến nó thành gRPC rồi đẩy vào Backend. Lúc trả về, Envoy tự dịch gRPC ngược lại thành JSON cho React. Rất thần thánh.

</details>

1. **The Data Plane of a Service Mesh (Istio, Linkerd)**: The most prevalent use case. Envoy almost never operates alone. It acts as the "Data Plane" (the workers passing the traffic). A Control Plane (like **Istio**) acts as the brain. Istio ingests Kubernetes YAML files and pushes xDS commands to thousands of Envoy sidecars simultaneously, creating a secure, observable, intelligently routed communication mesh across the entire cluster.
2. **Modern API Gateways (Edge Proxy)**: Because of its dynamic routing and deep L7 inspection, Envoy is increasingly replacing Nginx as the primary Ingress Gateway (The Front Door). Projects like Ambassador, Gloo Edge, and Contour are API Gateways built entirely on top of the Envoy engine, designed specifically to route external HTTP traffic into complex Kubernetes microservices.
3. **The gRPC-Web Translation Proxy**: Browsers cannot execute native gRPC over HTTP/2. Envoy natively includes the `grpc-web` filter. The React Frontend sends a specialized Base64/JSON payload. Envoy intercepts it, translates it seamlessly into a native gRPC binary stream, forwards it to the Backend, and translates the binary response back to the browser. It bridges the REST-to-gRPC divide transparently.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Đừng bao giờ tự viết file config Envoy bằng tay**: Cấu trúc file YAML của Envoy phức tạp và rối rắm gấp 10 lần Nginx. Nó được thiết kế để Máy đọc, không phải Người đọc. Nếu bạn muốn dùng Envoy, hãy cài một Control Plane như Istio hoặc Gloo Edge. Bạn giao tiếp với Istio bằng các lệnh đơn giản, Istio sẽ tự động dịch ra cấu trúc phức tạp nạp cho Envoy.
2. **Tận dụng Circuit Breaking (Cầu dao điện)**: Trong hệ thống lớn, lỗi dây chuyền (Cascading Failure) rất đáng sợ. Máy A gọi Máy B. B sập. Nhưng A cứ cố gọi liên tục, làm A treo, rồi C gọi A làm C treo theo. Hãy cấu hình Cầu dao điện trên Envoy: "Nếu Máy B lỗi quá 5 lần, ngắt cầu dao. Bất cứ ai gọi B sẽ bị báo lỗi ngay lập tức, không tốn thời gian cố kết nối nữa". 

</details>

1. **Never Hand-Write Envoy Configurations**: Nginx configurations are designed for human readability. Envoy configurations are massively verbose JSON/YAML AST trees fundamentally designed for Machine-to-Machine API consumption. Writing Envoy config by hand is an anti-pattern. **Rule**: Always deploy Envoy via a Control Plane. If you need an API Gateway, use Gloo Edge. If you need a Mesh, use Istio. You write simple Custom Resource Definitions (CRDs) in Kubernetes, and the Control Plane translates them into the massive Envoy xDS configs automatically.
2. **Implement Aggressive Circuit Breaking**: Network failures in Microservices cause catastrophic Cascading Failures. If the User Service is experiencing a database lock, the Checkout Service waiting on it will exhaust all its worker threads waiting for a timeout. **Rule**: Configure Envoy's Outlier Detection and Circuit Breakers. If Envoy detects that a specific downstream Pod returned 5 consecutive `500 Internal Server Errors`, Envoy "trips the circuit". For the next 30 seconds, any request to that Pod is instantly rejected by Envoy with a `503 Service Unavailable`, protecting the upstream services from thread exhaustion while giving the failing Pod time to recover.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hội chứng "Nghẽn cổ chai Sidecar" (Latency/Memory Overhead)**: Việc nhét 1 cái Envoy đi kèm với MỌI Microservice nghe rất xịn. Nhưng nếu bạn có 1000 App, bạn sẽ phải chạy thêm 1000 con Envoy. Mỗi con Envoy ngốn 50MB RAM $\rightarrow$ Tốn mất 50GB RAM chỉ để chạy hệ thống mạng. Đồng thời, dữ liệu chạy ra chạy vào bị bẻ lái qua Envoy làm tăng độ trễ thêm 2-3 mili-giây. Với những app siêu nhỏ bé, việc này lãng phí tài nguyên khủng khiếp. (Istio đang ra mắt kiến trúc Ambient Mesh mới để bỏ cái Sidecar này đi).
2. **Độ phức tạp DevOps (Over-engineering)**: Cài Nginx mất 5 phút. Cài và vận hành Istio/Envoy tốn của team DevOps 3 tháng ròng rã vì nó quá phức tạp, có cả ngàn thông số phải tinh chỉnh. *Luật*: Nếu công ty của bạn chỉ có 5-10 Microservice, dùng Nginx. Chỉ dùng Envoy khi hệ thống lớn tới mức con người không thể tự vẽ bản đồ mạng được nữa.

</details>

1. **The Sidecar Resource Penalty (Overhead Exhaustion)**: The architectural cost of the Service Mesh. Injecting an Envoy proxy next to every single Application Container doubles the number of running processes in your cluster. While Envoy is efficient, reserving 50MB of RAM and 0.1 CPU cores for 2,000 sidecars consumes 100GB of RAM purely for networking. Furthermore, intercepting `App -> Sidecar -> Network -> Sidecar -> App` introduces multiple user-space context switches, adding 2-5ms of tail latency. **Rule**: Do not blindly adopt a Service Mesh. If you have a latency-sensitive, hyper-scale application, the sidecar overhead might be unacceptable. (Note: The industry is pivoting towards "Sidecarless" architectures like Istio Ambient Mesh/eBPF to solve this).
2. **Catastrophic Day-2 Operational Complexity**: Envoy and Istio introduce a staggering level of operational complexity. Debugging a failed request now requires traversing the Application Logs, the Ingress Envoy logs, the Control Plane state, and the Destination Sidecar logs. **Rule**: Avoid Over-Engineering. If you have 5 Monoliths or simple Microservices, standard Kubernetes Services and an Nginx Ingress are perfectly fine. Only adopt Envoy/Service Mesh when your Microservice count scales beyond human manageability (e.g., 50+ interconnected services) and you have dedicated Platform Engineers.

---

## Related Topics

- Envoy forms the core data plane for deploying Cloud-Native infrastructure on **[Kubernetes](../cloud-infra/kubernetes.md)**.
- Envoy natively load balances and multiplexes **[gRPC](../apis/grpc.md)** streams, unlike legacy proxies.
- If you only need a simple, high-performance static server and public proxy, stick to the simpler **[Nginx](./nginx.md)**.
