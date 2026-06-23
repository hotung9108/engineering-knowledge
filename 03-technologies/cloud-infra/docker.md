# Docker

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước năm 2013, việc triển khai phần mềm là một cơn ác mộng. Lập trình viên viết code chạy hoàn hảo trên máy tính của họ (Dùng Windows, Node.js v14). Khi gửi file code đó cho team Vận hành (DevOps) để chạy trên Máy chủ Cloud (Dùng Linux, Node.js v16), code bị sập tung tóe. Câu nói cửa miệng kinh điển là: *"Ủa, nó chạy bình thường trên máy tui mà!"*. **Docker** ra đời và tạo ra một cuộc cách mạng vĩ đại tương đương với việc phát minh ra Container trong ngành vận tải biển. Docker không chỉ gói mỗi File Code. Nó gói toàn bộ "Hệ điều hành, phiên bản Node.js, thư viện, và File Code" vào trong một cái Thùng ảo (Container) đóng kín. Lập trình viên ném cái Thùng đó lên máy chủ. Máy chủ không cần cài Node.js, chỉ việc chạy cái Thùng đó. Nhờ vậy, môi trường chạy code được bảo đảm giống hệt nhau 100% dù ở bất kì đâu.

</details>

> **Summary**: Prior to 2013, software deployment was plagued by the "It works on my machine" syndrome. A developer would build an application on a macOS laptop with specific library versions, hand the source code over to the Operations team, and the application would catastrophically fail on the CentOS production server due to environmental drift and dependency conflicts. **Docker** revolutionized the industry by mainstreaming **Containerization**. Inspired by the standardization of physical shipping containers, Docker does not just package the Application Code; it packages the Code, the Runtime (e.g., Node.js, Python), the system tools, and the exact OS libraries into a standardized, immutable artifact called a **Docker Image**. When this Image is executed as a **Container**, it runs in complete isolation. Because the Container explicitly dictates its entire environment, it is mathematically guaranteed to execute exactly the same way on a developer's laptop, a testing server, or a massive AWS EC2 cluster.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn chuyển nhà từ Việt Nam sang Mỹ. Bạn có một chậu cây hoa hồng rất quý, chỉ sống được ở nhiệt độ 25 độ C và đất phèn.
1. **Cách cũ (Mang mỗi cái cây)**: Bạn nhổ cái cây đem qua Mỹ trồng xuống đất Mỹ (Môi trường máy chủ). Đất lạ, khí hậu lạ, cái cây chết khô. Bạn cãi nhau với người Mỹ: *"Ủa lúc ở Việt Nam nó sống tốt lắm mà!"*.
2. **Cách dùng Docker (Mang nguyên cái nhà kính)**: Bạn xây một cái Hộp Kính đóng kín (Container). Bạn bỏ cái cây vào đó, bỏ sẵn 10kg đất phèn, gắn máy lạnh duy trì đúng 25 độ C. Bạn niêm phong cái hộp lại và gửi qua Mỹ. Tới Mỹ, người ta không cần biết bên ngoài trời đang tuyết hay bão, người ta cứ cắm điện cho cái Hộp Kính đó. Cây hoa hồng bên trong sống khỏe re y hệt như lúc ở Việt Nam. Môi trường bên trong hộp đã bị cô lập hoàn toàn với bên ngoài.

</details>

Imagine moving a rare Tropical Fish from Brazil to Norway.
1. **The Old Way (Bare Metal / Just Code)**: You take the fish (The Code) out of its warm, salty Brazilian river (The Developer's Laptop) and dump it into a freezing Norwegian lake (The Production Server). The fish instantly dies. You argue: *"But it swam perfectly in Brazil!"*
2. **Docker (Containerization)**: You don't just move the fish. You build an indestructible, sealed Glass Aquarium (The Docker Container). You fill it with the exact Brazilian water, set the heater to the exact temperature, and put the fish inside. You ship the entire Aquarium to Norway and plug it in. The fish survives perfectly because it has no idea it's in Norway. Its immediate environment is still exactly Brazil. The container isolates the application from the underlying host infrastructure.

---

## Layer 1: Virtual Machines vs Containers (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nhiều người nghĩ Docker là Máy ảo (VMware, VirtualBox). Không phải.
1. **Máy ảo (Virtual Machine)**: Để tạo 3 máy ảo trên 1 máy tính thật. Bạn phải Cài nguyên 3 cái Hệ điều hành đầy đủ (Windows nặng 20GB, Ubuntu nặng 5GB). Việc khởi động 3 cái máy ảo này mất 5 phút, và ngốn sạch 10GB RAM dù chưa chạy app gì cả. Rất cồng kềnh.
2. **Docker Container**: Docker dùng chung "Nhân hệ điều hành" (Kernel) của máy tính thật. Nó cắt bỏ toàn bộ những thứ thừa thãi (Giao diện màn hình, Driver âm thanh). Một cái Container Ubuntu (Alpine) của Docker chỉ nặng đúng 5 Megabyte! Và vì nó không phải "khởi động Win", nó bật lên trong 0.1 giây. Bạn có thể chạy 100 cái Container Docker trên cùng 1 cái Laptop mà máy vẫn chạy mượt mà.

</details>

A critical distinction: Docker is NOT hardware virtualization.
1. **Virtual Machines (VMware, Hyper-V, AWS EC2)**: Hardware-level virtualization. A Hypervisor carves up the physical server. If you want 3 isolated apps, you must install 3 entire, heavy Guest Operating Systems (e.g., 3x 10GB Windows Server installations). Each VM consumes gigabytes of RAM just for OS background processes, and booting them takes minutes.
2. **Docker Containers**: OS-level virtualization. Containers share the *Host Operating System's Kernel*. They only package the necessary binaries and libraries. A minimal Linux container (Alpine) is 5 Megabytes, not Gigabytes. Because they don't boot an entire OS, containers start in milliseconds and consume virtually zero CPU/RAM overhead. You can comfortably run 10 VMs on a server, but you can run 1,000 Containers on that same server.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Docker sinh ra để giải quyết 2 bài toán lớn nhất của Kỷ nguyên Microservices:
1. **Sự đa dạng ngôn ngữ (Polyglot)**: App của bạn có 1 cục viết bằng Java (cần JDK 8), 1 cục viết bằng Node.js (cần v14), 1 cục viết bằng Python (cần bản 3.9). Chẳng lẽ bắt Team IT phải hì hục cài cả chục phần mềm đó lên máy chủ? Rất dễ đụng độ nhau. Dùng Docker, tất cả được bọc thành Thùng. Máy chủ chỉ cần cài đúng 1 thứ duy nhất: Cài phần mềm Docker. Docker sẽ tự động chạy tất cả các Thùng đó cách ly với nhau.
2. **Tốc độ mở rộng (Auto-Scaling)**: Ngày Black Friday, khách đổ vào mua hàng. Hệ thống cần bật thêm 50 máy chủ ngay lập tức. Nếu dùng Máy ảo (VM), chờ máy ảo khởi động hệ điều hành xong là khách đi hết. Nếu dùng Docker, việc "Nhân bản" một cái Thùng diễn ra trong 0.5 giây. Hệ thống đáp ứng ngay lập tức.

</details>

Docker became the industry standard because it solved the friction of **Polyglot Architectures** and enabled **Microsecond Scalability**.
1. **The Dependency Matrix from Hell**: A modern application consists of a Java API (Requires JDK 11), a React frontend (Requires Node 16), an AI worker (Requires Python 3.9 + specific C-compilers), and a Redis cache. Forcing a SysAdmin to install all these conflicting dependencies natively on a single Linux host is an operational nightmare (Dependency Hell). Docker normalizes the deployment artifact. The Host OS only needs exactly one software installed: The Docker Daemon. It treats the Java App and the Python App exactly the same—as generic black boxes that just execute.
2. **Instantaneous Scalability**: In a Microservices architecture, traffic is highly volatile. If the "Checkout Service" experiences a spike, AWS Auto-Scaling triggers. Booting a new EC2 Virtual Machine takes 2-3 minutes. Booting a new Docker Container on an existing machine takes 200 milliseconds. This unparalleled speed allows systems to dynamically absorb traffic spikes without degrading user experience.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc có Lập trình viên mới vào Công ty (Onboarding).
</details>

Visualizing Developer Velocity (Onboarding).

| Metric | Traditional Development (No Docker) | Dockerized Development |
|---|---|---|
| **Day 1 Setup** | The new dev spends 3 days reading a 50-page Wiki. They must manually install Postgres, install Redis, install Node v14 (but they accidentally installed v16 and broke it). Extremely frustrating. | The new dev installs Docker. They type exactly one command: `docker-compose up`. Docker automatically downloads Postgres, Redis, and runs the Node App perfectly in 5 minutes. |
| **Database Collisions**| The developer is working on Project A (Needs Postgres 10) and Project B (Needs Postgres 14). They cannot install both on their Macbook easily. | The developer runs Project A's container and Project B's container. They are completely isolated. No conflicts ever. |

---

## Layer 4: The Core Components

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hệ sinh thái Docker xoay quanh 3 chữ chính:
1. **Dockerfile (Bản vẽ thiết kế)**: Một file Text chứa các dòng lệnh hướng dẫn cách tạo ra cái Thùng. Ví dụ: "Lấy cái khung Linux, cài Node.js, copy code của tôi vào, chạy lệnh NPM START".
2. **Docker Image (Cái Thùng đông lạnh)**: Sau khi chạy file Dockerfile, bạn sẽ thu được 1 file nén khoảng 100MB. File này chứa toàn bộ chương trình của bạn. Nó là dạng "Chỉ Đọc" (Read-only). Bạn đem file này gửi lên kho Docker Hub hoặc đưa cho sếp.
3. **Docker Container (Cái Thùng đang chạy)**: Khi bạn lấy cái Image ở trên, và bấm nút "Run". Cái thùng được rã đông, chạy thành một chương trình thật sự trên RAM, có ổ cứng, có địa chỉ IP riêng. Một Image có thể đẻ ra hàng trăm Container chạy song song.

</details>

To master Docker, you must understand its holy trinity of abstractions:
1. **Dockerfile (The Blueprint)**: A declarative text document detailing the exact sequential steps to assemble your application. It acts as the ultimate documentation. Example: *1. Start with a baseline Alpine Linux OS. 2. Install Python. 3. Copy `app.py`. 4. Expose Port 8000.*
2. **Docker Image (The Immutable Artifact)**: When you `build` the Dockerfile, the Docker Engine executes the steps and snapshots the result into an Image. An Image is an immutable, read-only template containing the OS filesystem, dependencies, and code. It is essentially a frozen ZIP file of your app. You push this Image to a Registry (like Docker Hub or AWS ECR).
3. **Docker Container (The Runtime Instance)**: When you `run` an Image, the Docker Engine allocates a read-write filesystem layer on top of the Image, assigns it an isolated network interface, and executes it as a running Process on the Host OS. **Analogy**: The Dockerfile is the Source Code (Class), the Image is the compiled `.exe` file (Class definition), and the Container is the running program in RAM (The Object instance).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng Image gốc siêu nhẹ (Alpine)**: Nếu file `Dockerfile` của bạn bắt đầu bằng `FROM ubuntu`, cái thùng của bạn sinh ra sẽ nặng tới 1GB. Việc tải lên tải xuống rất lâu và tốn tiền mạng. Hãy luôn ưu tiên dùng bản `alpine` (Ví dụ: `FROM node:18-alpine`). Hệ điều hành Alpine chỉ nặng vỏn vẹn 5MB, giúp Image thu nhỏ xuống còn 50MB, chạy cực nhanh và an toàn (Ít bị dính Virus hơn).
2. **Viết Dockerfile nhiều tầng (Multi-Stage Builds)**: Khi build code React, bạn phải tải 1GB thư viện `node_modules` về. Nhưng lúc chạy Web, bạn chỉ cần ném duy nhất thư mục `build` (nặng 2MB) cho Nginx. Nếu bứng cả 1GB `node_modules` đó nhét vào Container đem lên Cloud thì quá ngu ngốc. Multi-stage build cho phép Docker: "Build ở tầng 1, xong vứt sạch rác đi, chỉ bốc đúng file thành phẩm ném sang tầng 2 rồi xuất chuồng".

</details>

1. **Utilize Minimal Base Images (Alpine Linux)**: The most common beginner mistake is starting a Dockerfile with `FROM ubuntu` or `FROM node:18`. These images include massive, bloated OS utilities (compilers, package managers) resulting in a 1GB+ Image size. This dramatically increases pull times during Auto-Scaling and increases the attack surface for hackers. **Rule**: Always default to Alpine-based images (e.g., `FROM node:18-alpine`). Alpine is a security-oriented, lightweight Linux distribution that is only 5MB in size.
2. **Implement Multi-Stage Builds**: When compiling a Go application or a React frontend, you need heavy compilers and massive dependency folders (`node_modules`). However, the final production server ONLY needs the compiled binary or the static HTML files. Including the compilers in the final production Image is a catastrophic security and size violation. **Rule**: Use Multi-Stage builds. Stage 1 (`AS builder`) contains the heavy SDKs to compile the code. Stage 2 (`FROM nginx:alpine`) copies ONLY the final compiled artifact from Stage 1, completely discarding all the heavy build-time junk.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sử dụng Container như Database tĩnh (Lưu file vào Container)**: Container được thiết kế để "Chết bất đắc kỳ tử". Nếu bạn cho phép user upload Hình đại diện và bạn lưu hình đó vào trong thư mục của Container. Ngày mai, Container bị lỗi mạng khởi động lại, TẤT CẢ HÌNH ĐẠI DIỆN ĐÓ SẼ BỊ XÓA SẠCH SẼ.
   - *Cách giải*: Trạng thái (State) không bao giờ được giữ trong Container. Nếu có file hình, phải up lên AWS S3. Nếu là Database (MySQL chạy bằng Docker), BẮT BUỘC phải dùng tính năng `Docker Volumes` để đục 1 cái lỗ, nối dữ liệu của Container chảy ra ngoài Ổ cứng thật của máy chủ.
2. **Chạy Container bằng quyền Root**: Mặc định, mọi code trong Docker chạy bằng quyền Cao nhất (Root). Nếu Hacker tìm ra lỗ hổng trong Web của bạn, hắn có thể lợi dụng quyền Root đó để "vượt ngục" (Container Breakout) ra ngoài và chiếm quyền điều khiển luôn cả cái Máy chủ thật. Luôn thêm lệnh `USER node` vào cuối Dockerfile để ép code chạy bằng quyền User quèn.

</details>

1. **Treating Containers as Persistent Storage (Ephemeral Death)**: Containers are inherently ephemeral. If you write an Application Log or save an uploaded User Avatar directly into the Container's filesystem, that data is permanently vaporized the exact millisecond the Container crashes or restarts. **Rule**: Application Containers MUST be Stateless. User uploads belong in Object Storage (AWS S3). If you run stateful databases inside Docker, you must utilize **Docker Volumes** to explicitly mount a path from the Host OS hard drive directly into the Container, ensuring data persists even when the Container dies.
2. **Running as Root (Security Vulnerability)**: By default, processes inside a Docker container run as the `root` user. While isolated, if a hacker exploits a Remote Code Execution (RCE) vulnerability in your Node.js app, they gain root access *inside* the container, which dramatically increases the risk of a "Container Escape" attack to compromise the Host OS. **Rule**: Always adhere to the Principle of Least Privilege. Add a directive like `USER appuser` at the end of your Dockerfile to strictly downgrade the application's runtime permissions.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp các lệnh Docker và Docker Compose quan trọng nhất dành cho Dev.
</details>

### The Perfect Dockerfile (Node.js API)
```dockerfile
# Stage 1: Build the app
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci # Install strictly from lockfile
COPY . .
RUN npm run build

# Stage 2: Production (Tiny Image)
FROM node:18-alpine
WORKDIR /app
# Downgrade privileges for security
USER node 
# Copy only the compiled code from Stage 1
COPY --from=builder /app/dist ./dist
COPY package.json package-lock.json ./
RUN npm ci --only=production

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Essential CLI Commands
```bash
# === BUILDING & RUNNING ===
# Build an image from a Dockerfile in the current directory
docker build -t my-api:v1 .

# Run the container (in background -d), mapping Port 80 on host to 3000 in container
docker run -d -p 80:3000 --name api_server my-api:v1

# === DEBUGGING ===
# See all running containers
docker ps

# See the console logs of a container in real-time
docker logs -f api_server

# "SSH" (Jump) inside a running container to debug
docker exec -it api_server /bin/sh

# === CLEANUP (Fix "Disk is Full") ===
# Forcibly stop and delete a container
docker rm -f api_server

# Nukes all stopped containers, unused networks, and dangling images (DANGEROUS but saves space)
docker system prune -a --volumes
```

### Docker Compose (Running Multiple Containers)
Used for local development (e.g., spinning up Node + Postgres + Redis together). Saved as `docker-compose.yml`.
```yaml
version: '3.8'
services:
  web:
    build: . # Build the Dockerfile in this directory
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db # The network automatically resolves the service name 'db' to an IP
    depends_on:
      - db
  
  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - pgdata:/var/lib/postgresql/data # Persist data on host disk

volumes:
  pgdata: # Declare the volume
```
Commands:
- `docker-compose up -d`: Start everything in the background.
- `docker-compose down`: Stop and destroy everything.

---

## Related Topics

- Managing 1 Docker container is easy. Managing 5000 containers requires an Orchestrator. See **[Kubernetes](./kubernetes.md)**.
- For deploying infrastructure to AWS to host your containers, see **[Terraform](./terraform.md)**.
- Docker fundamentally changed backend deployment. Review how Backend APIs work in **[Backend Overview](../backend/overview.md)**.
