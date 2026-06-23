# Kubernetes (K8s)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Docker giúp đóng gói ứng dụng vào những "Thùng Container" rất tiện lợi. Nhưng khi hệ thống của bạn phình to ra: Bạn có 50 máy chủ vật lý, và bạn muốn chạy 5.000 cái Thùng Docker trên đó. Bạn sẽ đối mặt với ác mộng: "Làm sao biết máy chủ nào đang rảnh để ném thùng lên đó? Nếu một máy chủ bị cháy, 100 cái Thùng trên máy đó chết, ai sẽ tự động đẻ ra 100 cái Thùng mới ở các máy chủ khác để đền bù?". Docker không làm được việc đó. Google đã mở mã nguồn **Kubernetes** (hay gọi tắt là K8s) - Hệ thống Chỉ huy Container vĩ đại nhất thế giới. K8s đóng vai trò là một Vị Nhạc Trưởng. Bạn chỉ việc ném 50 máy chủ cho nó và ra lệnh: *"Tôi muốn lúc nào cũng có đúng 10 Thùng Web và 5 Thùng Database chạy"*. K8s sẽ giám sát hệ thống 24/7. Nếu có thùng nào chết, nó tự bắn bỏ và đẻ thùng mới thay thế trong chớp mắt mà con người không cần thức dậy lúc 2h sáng để xử lý.

</details>

> **Summary**: Docker fundamentally solved how to package and run a single container. However, deploying a single container on a laptop is vastly different from operating a distributed Microservice architecture consisting of 10,000 containers spanning 500 Virtual Machines. In such environments, manual management is impossible. You need an automated system to handle scheduling, self-healing, rolling updates, and network routing. This is **Container Orchestration**. Originally developed by Google (based on their internal 'Borg' system), **Kubernetes (K8s)** is the absolute industry standard for orchestration. It acts as the Operating System for the Cloud. Instead of managing individual servers, you interact with the Kubernetes API, declaratively stating your "Desired State" (e.g., *Ensure 5 replicas of the Node.js API are always running*). Kubernetes continuously monitors the cluster, automatically scheduling containers onto healthy nodes, restarting crashed containers, and seamlessly routing network traffic.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một Hãng xe Công nghệ.
1. **Docker (Tài xế)**: Docker là những người Tài xế biết lái xe. Nếu chỉ có 1-2 tài xế, bạn tự gọi điện chỉ đường cho họ được. Nhưng khi bạn có 5.000 tài xế chạy khắp thành phố, mọi thứ sẽ kẹt cứng và hỗn loạn.
2. **Kubernetes (Tổng đài AI)**: Bạn là Giám đốc, bạn không bao giờ gọi trực tiếp cho Tài xế. Bạn chỉ việc viết Lệnh (File YAML) đưa cho Tổng đài (K8s): *"Tôi muốn luôn có 500 xe chạy ở Quận 1"*. 
   - Tổng đài dùng Camera quét (Monitor). Thấy Quận 1 đang thiếu 10 xe, nó tự gọi 10 tài xế đang ngủ thức dậy đi làm (Auto-scaling). 
   - Thấy 1 chiếc xe xịt lốp (Crash), nó tự gọi xe kéo vứt xe đó đi và cử xe khác trám vào (Self-healing). 
   - Khách gọi xe (Traffic), Tổng đài tự động tính toán để điều phối chiếc xe gần nhất (Load Balancing). Mọi thứ hoàn toàn tự động.

</details>

Imagine managing a massive Orchestra.
1. **Docker (The Musicians)**: Docker containers are individual, highly skilled musicians holding their instruments. A single musician plays well, but 100 musicians playing without direction creates catastrophic noise.
2. **Kubernetes (The Conductor)**: K8s is the Conductor. You (The Director) hand the Conductor a piece of sheet music (A declarative YAML file). The Conductor stands at the podium. If the violinist gets sick and faints (Container Crash), the Conductor doesn't stop the show. They instantly motion for a backup violinist to take the seat (Self-Healing). If the audience demands louder music, the Conductor instantly signals 5 more trumpets to join in (Auto-Scaling). The Conductor ensures the actual performance perfectly matches the sheet music at all times.

---

## Layer 1: Core Components (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

K8s có từ vựng riêng cực kì phức tạp. Đây là 5 chữ quan trọng nhất:
1. **Cluster (Cụm)**: Toàn bộ hệ thống, bao gồm Máy Chủ Huy (Master Node) và Các Máy Tớ (Worker Nodes).
2. **Pod**: Khái niệm nhỏ nhất trong K8s. K8s KHÔNG quản lý Docker Container trực tiếp. Nó bọc cái Container vào một lớp vỏ gọi là Pod. (1 Pod thường chứa 1 Container).
3. **Deployment**: Đây là "Bản cam kết số lượng". Bạn viết lệnh: "Tạo 1 Deployment với 5 Pods của con Web". K8s sẽ sống chết bảo vệ con số 5 đó. Đứt 1 con, nó đẻ 1 con.
4. **Service**: Các Pod có IP thay đổi liên tục, lúc sống lúc chết. Service là một cái "Tên miền tĩnh" và "Cân bằng tải". Các Pod chết mặc Pod, App chỉ cần gọi tên Service, Service sẽ tự chia đều việc cho các Pod đang sống.
5. **Ingress**: Cái Cổng chính bảo vệ Cụm. Khi khách hàng từ Internet gõ `facebook.com`, Ingress sẽ kiểm tra IP, rồi đẩy khách vào đúng cái Service chịu trách nhiệm giao diện.

</details>

Kubernetes introduces a complex, highly abstracted vocabulary. Here are the core primitives:
1. **The Cluster**: The entire ecosystem. It consists of the **Control Plane** (The Master Nodes/Brains running the API server and scheduling) and the **Data Plane** (The Worker Nodes/EC2 instances that actually run the apps).
2. **Pod**: The smallest deployable unit in K8s. Kubernetes *does not* run Containers directly. It wraps one (or sometimes closely coupled multiple) Docker Containers inside a "Pod". Pods share the same local network IP and disk storage. Pods are mortal—they die and are never resurrected.
3. **Deployment**: A declarative controller managing Pods. You never create a Pod manually. You create a Deployment. You state: `"replicas: 3"`. The Deployment controller ensures exactly 3 Pods are running. If a Node crashes and takes down 2 Pods, the Deployment instantly schedules 2 new Pods on a healthy Node to maintain the desired state.
4. **Service**: Because Pods are ephemeral, their IP addresses change constantly. A Service provides a stable, permanent IP address and DNS name. It acts as an internal Load Balancer, routing traffic across all healthy Pods managed by a Deployment.
5. **Ingress**: Services manage internal traffic. An Ingress manages external traffic. It is an API object that configures an external HTTP Load Balancer (like Nginx or HAProxy) to route public traffic (`myapp.com/api`) into the correct internal Service.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn vừa code xong bản cập nhật V2 cho trang web. Nếu quản lý máy chủ bằng tay: Bạn phải tắt máy chủ (Khách hàng vào web sẽ thấy báo lỗi), chép code V2 vào, bật lại. Cách này gây gián đoạn (Downtime).
K8s sinh ra để hệ thống **Không bao giờ có khái niệm Downtime**.
Khi bạn ra lệnh "Cập nhật lên bản V2". K8s sẽ chơi trò "Cuốn chiếu" (Rolling Update):
- K8s đẻ ra 1 Pod V2 mới. 
- Đợi con V2 đó chạy ngon lành, nó mới âm thầm chém chết 1 con V1 cũ.
- Rồi nó đẻ tiếp 1 con V2 thứ hai.
- Lặp lại cho đến khi toàn bộ V1 bị thay thế bằng V2. 
Xuyên suốt quá trình đó, khách hàng đang lướt Web không hề bị ngắt kết nối một giây nào. Đây là sức mạnh tột đỉnh của K8s.

</details>

Why do engineering teams endure the immense learning curve of Kubernetes? Because it solves the most difficult operational challenges of distributed systems autonomously:
1. **Zero-Downtime Deployments (Rolling Updates)**: In legacy systems, deploying a new version required taking the app offline, upgrading, and restarting (causing Downtime). K8s manages this seamlessly. When deploying Version 2, K8s spins up a new V2 Pod. It waits for the V2 Pod to pass its "Readiness Probe" (proving it can handle traffic). Only then does it gently terminate one V1 Pod. It repeats this rolling process until all Pods are upgraded. Users experience zero interruption. If V2 crashes immediately, K8s detects the failure and instantly rolls back to V1.
2. **Self-Healing Infrastructure**: At scale, hardware failures are statistical guarantees. A hard drive will fail. A RAM module will corrupt. If an underlying EC2 worker node catches fire, K8s detects the loss of heartbeat within seconds. It immediately reschedules all the "lost" Pods onto the remaining healthy Nodes in the cluster automatically.
3. **Cloud Agnosticism (Avoiding Vendor Lock-in)**: If you build your entire company on AWS proprietary tools (Lambda, ECS), leaving AWS is impossible. Kubernetes is a universal standard. A K8s YAML file runs exactly the same on AWS (EKS), Google Cloud (GKE), Azure (AKS), or a physical server in your basement. It abstracts away the Cloud Provider.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình xử lý tải khi có đợt Khuyến mãi Flash Sale.
</details>

Visualizing Auto-Scaling (Manual vs Kubernetes).

| Metric | Traditional VMs / Docker Compose | Kubernetes (HPA) |
|---|---|---|
| **Traffic Spike Hits** | CPU hits 100%. App crashes. SysAdmin wakes up at 3 AM, manually provisions a new VM, installs Docker, and starts the container. Takes 30 minutes. | K8s detects CPU hit 80%. The **HPA (Horizontal Pod Autoscaler)** instantly commands the Deployment to scale from 3 Pods to 50 Pods. Takes 5 seconds. System survives. |
| **Traffic Drops** | The SysAdmin forgets to delete the extra VMs. The company pays for 50 VMs for a month. | K8s detects CPU dropped to 10%. HPA automatically scales down to 3 Pods. Saves money instantly. |

---

## Layer 4: Common Architectural Flow

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đường đi của một cú click chuột từ Khách hàng vào tới K8s:
1. Người dùng gõ `api.shopee.vn`.
2. Yêu cầu đụng trúng **Ingress** (Người bảo vệ cổng). Ingress đọc đường dẫn, thấy chữ `/api`, nó quyết định mở cửa.
3. Ingress đẩy tín hiệu vào **Service** (Bộ đàm tổng đài). Service có danh sách 10 cái Pod (Thùng chứa Code) đang chạy.
4. Service chọn ngẫu nhiên 1 cái **Pod** đang rảnh việc, và ném yêu cầu vào đó.
5. **Container** Node.js bên trong Pod nhận lệnh, tính toán, và trả kết quả ngược lại.

</details>

The Anatomy of a Kubernetes Request (The Traffic Path):
1. **The Internet to Ingress**: A user accesses `myapp.com/api/users`. The DNS points to a Cloud Load Balancer, which funnels traffic into the Kubernetes **Ingress Controller** (often Nginx or Envoy).
2. **Ingress to Service**: The Ingress parses the HTTP URL (`/api/users`). It looks up its routing rules and forwards the traffic to the internal **Service** named `backend-api-svc`.
3. **Service to Pod**: The `backend-api-svc` acts as a pure Layer 4 load balancer. It looks at its Endpoint list (which contains the dynamic IPs of all currently living Pods matching its label selector). It forwards the TCP packet to a specific, healthy **Pod**.
4. **Inside the Pod**: The **Docker Container** running your Node.js/Python code receives the request on port 3000, executes the database logic, and returns the HTTP JSON response back up the chain.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khai báo Giới hạn Tài nguyên (Requests & Limits)**: Đây là lỗi chết người hay gặp nhất. Mặc định, nếu bạn ném 1 cái Pod lên K8s, cái Pod đó có thể ăn SẠCH SÀNH SANH RAM của máy chủ, làm chết lây tất cả các Pod khác. BẮT BUỘC phải viết trong file YAML: `Requests: RAM 256MB` (Xin cấp 256MB) và `Limits: RAM 512MB` (Giới hạn tối đa, ăn lố 512MB là K8s lấy súng bắn bỏ Pod ngay lập tức). Điều này bảo vệ cụm K8s không bao giờ bị sập.
2. **Khai báo Liveness và Readiness Probes (Bác sĩ khám bệnh)**: K8s dựa vào "Bác sĩ" để biết Pod còn sống không.
   - `Liveness`: K8s cứ 5s gõ cửa 1 lần. Nếu App bị đứng (Deadlock), không mở cửa. K8s sẽ bắn bỏ Pod và đẻ con mới (Tự chữa lành).
   - `Readiness`: Khi Pod mới đẻ, App Node.js mất 10 giây để kết nối Database. Nếu K8s ném khách hàng vào lúc này, khách sẽ bị lỗi. Readiness sẽ bảo K8s: "Khoan, em chưa sẵn sàng, đừng ném khách cho em". Bao giờ kết nối DB xong, mở Readiness ra, K8s mới ném khách vào.

</details>

1. **Mandatory Resource Requests and Limits**: The most critical configuration in Kubernetes. If you deploy a Pod without defining resource boundaries, a memory-leak in your Java App will consume 100% of the Node's RAM. The Linux OOM-Killer will trigger and might kill the core K8s system components, taking down the entire Node. **Absolute Rule**: Every single Container MUST define `requests` (The minimum CPU/RAM guaranteed to it) and `limits` (The absolute maximum CPU/RAM it can consume before K8s brutally kills it). This ensures predictable scheduling and cluster stability.
2. **Implement Liveness and Readiness Probes**: K8s is blind to your application's internal logic. A Java app might be technically "running" (Process ID exists), but stuck in an infinite Deadlock loop, unable to serve HTTP requests.
   - **Liveness Probe**: Configured to hit `/healthz`. If your app returns a `500 Error`, K8s assumes the app is brain-dead, brutally terminates the Pod, and restarts it (Self-Healing).
   - **Readiness Probe**: Configured to hit `/ready`. When a Pod boots up, it might take 15 seconds to establish Database connections. If K8s sends user traffic immediately, the requests fail. The Readiness probe tells K8s: "Do not put me in the Service Load Balancer until I return a 200 OK here".

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Over-engineering (Dùng dao mổ trâu giết gà)**: Kubernetes là cỗ máy khổng lồ của Google. Việc cài đặt và bảo trì nó tốn cực kì nhiều tiền bạc và chất xám của team DevOps. Nếu công ty bạn chỉ có 2-3 cái API Backend nội bộ, việc cố đấm ăn xôi dùng K8s là một sự lãng phí tiền của ngu ngốc. Hãy dùng Docker Compose hoặc Heroku/Vercel. Chỉ dùng K8s khi hệ thống có hàng chục Microservices và bắt buộc phải scale tự động.
2. **Cố gắng chạy Database (Stateful) trên Kubernetes**: K8s được sinh ra để chạy Code (Stateless - Chết là bỏ). Database (Postgres, MongoDB) là thứ giữ dữ liệu (Stateful), nó cần sự ổn định tuyệt đối về Ổ cứng. Dù K8s có hỗ trợ `StatefulSets`, việc vận hành Database trên K8s là một rủi ro cực kì lớn, rất dễ mất sạch dữ liệu khi K8s tự động dọn dẹp cụm. Hãy luôn mua Database bên ngoài (AWS RDS) và dùng K8s để chạy Code (API).

</details>

1. **Resume-Driven Development (Over-Engineering)**: Kubernetes introduces a staggering amount of operational complexity. It requires a dedicated Platform Engineering team to maintain, secure, and upgrade the cluster. If your startup consists of a monolithic Django App and a Postgres database, adopting Kubernetes is an economic and architectural disaster. **Rule**: Stick to PaaS (Vercel/Heroku) or simple VMs until your Microservice footprint or scaling velocity mathematically demands orchestration.
2. **Running Stateful Workloads (Databases) in K8s**: Kubernetes was engineered for Stateless workloads (Web Servers, API Nodes). Pods are meant to be violently destroyed and recreated. Relational Databases (PostgreSQL, MySQL) violently oppose being destroyed; they require strict disk I/O, cache warming, and careful state replication. While K8s supports `StatefulSets`, operating a production Database inside K8s is notoriously dangerous and prone to catastrophic data corruption during network partitions. **Rule**: Always outsource Stateful workloads. Run your APIs in Kubernetes, but connect them to Managed Databases (like AWS RDS or DynamoDB).

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp các lệnh `kubectl` (Kube Control) dùng để điều khiển cụm.
</details>

### The Holy Trinity of K8s YAML (`app.yaml`)
```yaml
# 1. The Deployment (Runs the Code)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-backend
spec:
  replicas: 3 # I want 3 Pods always running
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: nodejs-app
        image: my-registry/my-backend:v1.0.0
        ports:
        - containerPort: 3000
        resources: # CRITICAL: Prevent cluster crashes
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"

---
# 2. The Service (Internal Load Balancer)
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend # Routes traffic to Pods with this label
  ports:
    - protocol: TCP
      port: 80       # Port the Service listens on
      targetPort: 3000 # Port the Pod listens on

---
# 3. The Ingress (Public Internet Entry)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backend-ingress
spec:
  rules:
  - host: api.myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-service # Routes to the Service above
            port:
              number: 80
```

### Essential `kubectl` CLI Commands
```bash
# Apply a YAML file to the cluster (Create/Update)
kubectl apply -f app.yaml

# View all running Pods in the current namespace
kubectl get pods

# View detailed information about a failing Pod (Why did it crash?)
kubectl describe pod <pod-name>

# View the live Console Logs of a specific Pod
kubectl logs -f <pod-name>

# Execute a bash shell inside a running Pod (For debugging)
kubectl exec -it <pod-name> -- /bin/sh

# Instantly scale the deployment to 10 instances (Imperative, not recommended for Prod)
kubectl scale deployment my-backend --replicas=10

# Forcefully delete a stuck Pod (K8s will automatically spawn a new one)
kubectl delete pod <pod-name>
```

---

## Related Topics

- K8s manages **[Docker](./docker.md)** containers.
- Setting up the underlying AWS Servers to run K8s is best done with **[Terraform](./terraform.md)**.
- For managing complex network routing *inside* K8s (Service Mesh), see **[Envoy Proxy](../web-servers/envoy.md)**.
