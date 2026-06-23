# Nginx

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Đầu những năm 2000, Internet đối mặt với bài toán "C10K problem" (Làm sao để một máy chủ xử lý được 10.000 kết nối cùng một lúc?). Máy chủ thống trị thời đó là Apache bị sập vì nó tạo ra 1 Tiểu trình (Thread) cho mỗi khách hàng, ăn sạch RAM. **Nginx** (đọc là "Engine-X") ra đời bởi một kỹ sư người Nga để giải quyết bài toán này. Nó sử dụng kiến trúc Hướng Sự Kiện (Event-Driven) cực kì tối ưu. Một "Người thợ" (Worker Process) của Nginx có thể tung hứng hàng ngàn kết nối cùng lúc mà chỉ tốn vài Megabyte RAM. Nhờ tốc độ xé gió và sự nhẹ bén đó, Nginx nhanh chóng lật đổ Apache để trở thành Web Server, Reverse Proxy, và Cân bằng tải phổ biến nhất thế giới. Hầu hết các trang web bạn truy cập ngày nay đều có Nginx đứng gác ở cửa.

</details>

> **Summary**: In the early 2000s, the Apache Web Server dominated the Internet using a thread-per-connection architecture. However, as web traffic exploded, Apache hit the infamous **C10K Problem**—the inability to handle 10,000 concurrent connections due to severe RAM exhaustion and thread context-switching overhead. **Nginx** (pronounced "Engine-X") was engineered by Igor Sysoev specifically to solve this. It utilizes a highly optimized, Asynchronous, Event-Driven architecture. A single Nginx worker process can multiplex thousands of concurrent connections using a tiny, predictable memory footprint. This paradigm shift in performance propelled Nginx to become the undisputed industry standard. Today, it functions not just as an HTTP Web Server for serving static assets, but as the quintessential Reverse Proxy, SSL/TLS Terminator, and Layer 7 Load Balancer protecting backend infrastructure.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một nhà hàng có 10.000 khách.
1. **Apache (Cách cũ)**: Nhà hàng thuê 10.000 người Bồi bàn. Mỗi bồi bàn đứng canh đúng 1 người khách. Khách ngồi suy nghĩ món mất 1 tiếng, bồi bàn cũng phải đứng chầu chực 1 tiếng. Tiền trả lương cho 10.000 bồi bàn (RAM) làm sập tiệm nhà hàng.
2. **Nginx (Cách mới)**: Nhà hàng chỉ thuê đúng 4 người Bồi bàn siêu nhanh nhẹn (Worker Processes). Bồi bàn số 1 đưa Menu cho khách A. Thấy khách A đang suy nghĩ, bồi bàn lập tức bỏ đi đưa Menu cho khách B, khách C. Khi nào khách A nghĩ xong, giơ tay gọi (Sự kiện - Event), bồi bàn mới quay lại ghi món. Bằng cách chạy vòng quanh liên tục không ngừng nghỉ, 4 bồi bàn phục vụ được cả 10.000 khách mà nhà hàng tốn rất ít tiền.

</details>

Imagine handling orders at a very busy fast-food counter.
1. **Thread-Per-Connection (Apache)**: You hire 100 Cashiers. A customer walks up, looks at the menu, and takes 5 minutes to decide. The Cashier stands there, completely paralyzed, unable to help anyone else until that specific customer finishes. You quickly run out of Cashiers (Threads/RAM), and the line goes out the door.
2. **Event-Driven Architecture (Nginx)**: You hire exactly 1 Cashier (The Worker Process). The Cashier hands menus to 100 people and says: "Step aside, raise your hand when you are ready." The Cashier immediately turns back to the counter. They only interact with customers at the exact millisecond the customer is ready to speak or pay (An Event). One Cashier effortlessly manages 1,000 people simultaneously.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nginx không phải là Database, cũng không phải là nơi viết code Logic. Nó là một cái "Phễu" đặt trước Máy chủ, làm 3 nhiệm vụ chính:
1. **Web Server tĩnh**: Phục vụ các file không thay đổi (HTML, CSS, MP4, JPG). Vì Nginx viết bằng ngôn ngữ C, tốc độ lấy file từ ổ cứng của nó nhanh đến mức không có một Framework Backend nào (như Node.js hay Django) có thể bắt kịp.
2. **Reverse Proxy (Người đại diện)**: Nginx đứng nghe ở cổng 80 (HTTP) và 443 (HTTPS). Nhận được yêu cầu, nó sẽ chuyển tiếp (Forward) cái yêu cầu đó vào cái cổng 3000 đang ẩn giấu của Node.js. 
3. **SSL Termination (Giải mã bảo mật)**: Bạn mua chứng chỉ bảo mật (Ổ khóa xanh HTTPS). Thay vì cài ổ khóa đó vào từng máy chủ Node.js rất mệt mỏi, bạn cài ổ khóa đó Lên đúng 1 mình Nginx. Nginx sẽ đứng ra giải mã mọi thứ rồi truyền vào trong cho Node.js bằng HTTP thường.

</details>

Nginx is a piece of infrastructural middleware written in highly optimized C. It fulfills three primary architectural roles:
1. **High-Performance Static Web Server**: It reads and serves static files (HTML, CSS, JS, Images, Videos) directly from disk to the network socket, often utilizing `sendfile()` system calls to bypass user-space memory entirely. It is orders of magnitude faster at serving files than application frameworks like Spring Boot or Express.js.
2. **Reverse Proxy (The Public Face)**: It binds to public ports (80/443) and listens to the Internet. When a request arrives, Nginx terminates the connection, reads the HTTP headers, and acts as a middleman, opening a *new* internal connection to forward the request to the hidden backend application (e.g., `localhost:3000`).
3. **SSL/TLS Terminator**: Managing cryptographic certificates across 50 microservices is a nightmare. Nginx acts as the TLS Terminator. It holds the SSL Certificates, handles the computationally expensive cryptographic handshakes with the Client, decrypts the traffic, and forwards plain HTTP internally inside the secure VPC.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn vừa code xong một trang Web bằng Python (Django). Nó chạy tuyệt vời trên máy tính của bạn (`localhost:8000`). Bạn ném nó lên mạng. Vài ngày sau, có 10.000 người vào xem cùng lúc. Trang web sập. Vì sao?
Vì Python, Ruby hay Node.js sinh ra là để xử lý Logic (Tính tiền, Lấy dữ liệu). Chúng KHÔNG ĐƯỢC THIẾT KẾ để ôm đồm hàng ngàn kết nối rác, kết nối yếu, mạng chập chờn từ hàng triệu cái điện thoại ngoài đường.
Nginx tồn tại để làm "Lá Chắn Không Gian". Nó đứng ra hứng chịu toàn bộ sự hỗn loạn của Internet (DDoS, Mạng lag, Tải file chậm). Nó gạn lọc mọi thứ thật sạch sẽ, đóng gói gọn gàng rồi mới ném phần tinh túy nhất cho Python xử lý. Không có Nginx, mọi Server Backend đều mỏng manh như tờ giấy trước Internet.

</details>

Application frameworks (Express, Django, Laravel, Spring) are fundamentally designed to execute complex Business Logic and interact with Databases. They are inherently fragile when exposed directly to the hostile public Internet.
Nginx exists to be the **Hardened Shield**.
If a malicious actor opens a connection and sends data at 1 byte per minute, a Node.js server will hold that connection open, wasting memory until it crashes. Nginx, using `epoll` (Linux) or `kqueue` (FreeBSD), holds that slow connection effortlessly. It buffers the entire HTTP request in its own RAM. **Crucially, Nginx only wakes up the backend Application Server when the entire, complete HTTP payload has been fully received and verified.** This completely isolates the fragile backend from network latency, slow clients, and connection-exhaustion attacks.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình Scale (Nâng cấp) ứng dụng khi có đông khách.
</details>

Visualizing Horizontal Scaling (Load Balancing).

| Metric | Without Nginx (Direct Server) | With Nginx (Load Balancer) |
|---|---|---|
| **Architecture** | DNS points `myapp.com` directly to Server A (IP: 1.1.1.1). | DNS points `myapp.com` to Nginx (IP: 1.1.1.1). Nginx sits in front of Server A, B, and C. |
| **Server Crash** | Server A crashes. The entire website goes completely offline. | Server A crashes. Nginx instantly detects the failure (Health Check) and dynamically reroutes all traffic to Server B and C. **Zero Downtime**. |
| **Adding Capacity** | You must change DNS records (takes 24 hours to update globally). Very difficult. | You boot up Server D. You add 1 line to `nginx.conf`. Nginx instantly starts sending 25% of traffic to Server D. Takes 1 second. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Phục vụ Frontend (React/Vue/Angular)**: Khi bạn `build` xong ứng dụng React, nó sinh ra 1 đống file HTML/JS. Bạn không nên dùng Node.js để chạy đống file này. Bạn chỉ việc vứt đống file đó vào Nginx, chỉ đường dẫn thư mục, và Nginx sẽ phục vụ chúng với tốc độ bàn thờ.
2. **Cân bằng tải (Load Balancing)**: Nginx hỗ trợ chia đều lưu lượng mạng. Có 3 thuật toán chính: Round-Robin (Chia đều xoay vòng), Least Connections (Máy nào đang rảnh thì chia cho máy đó), IP Hash (Khách hàng A luôn được chỉ định vào cố định Máy chủ A để không bị mất Session đăng nhập).
3. **Giới hạn tốc độ (Rate Limiting)**: Chống Spam. Bạn có thể cấu hình Nginx: "Một IP chỉ được phép tải trang 10 lần trong 1 giây". Nginx sẽ thẳng tay chặn (mã lỗi 429) ở ngay vòng gửi xe, không làm phiền đến Backend.
4. **Bộ nhớ đệm (Micro-Caching)**: Nginx có thể nhớ luôn câu trả lời của Backend. Nếu Backend báo "Bài báo này nội dung thế này", Nginx lưu lại 5 giây. 1000 người vào trong 5 giây đó, Nginx trả lời luôn mà không thèm gọi Backend.

</details>

1. **Serving Single Page Applications (SPAs)**: The standard deployment for React, Angular, or Vue. When these apps are built, they output pure static HTML/JS/CSS. Deploying them inside a Node.js wrapper is an anti-pattern. You simply place the static files in `/var/www/html` and configure Nginx to serve them directly, achieving maximum possible I/O performance.
2. **Layer 7 Load Balancing**: Distributing HTTP traffic across a fleet of internal servers. Nginx inspects the HTTP headers and routes traffic based on URL paths (`/api` goes to Node.js, `/blog` goes to WordPress). It supports multiple distribution algorithms: Round-Robin (default), Least-Connected, and IP-Hash (critical for maintaining stateful WebSocket sessions).
3. **Rate Limiting & DDoS Mitigation**: Protecting the API from abuse. Nginx can enforce strict zone limits (e.g., `limit_req`). It can mathematically throttle an IP address to exactly 5 requests per second, instantly returning a `429 Too Many Requests` error for abusers before the traffic ever reaches the vulnerable Application logic.
4. **Reverse Proxy Caching**: Nginx can cache the dynamic HTTP responses of the backend. If a heavy API endpoint `/stats` takes 2 seconds to compute, Nginx can cache the JSON response for 10 seconds. For the next 10 seconds, Nginx serves the response directly from RAM, effectively acting like a Varnish cache and shielding the database from traffic spikes.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Tách file cấu hình (Modular Configs)**: Đừng bao giờ viết tấ cả mọi thứ vào file `nginx.conf` chính. Cực kì dễ lỗi. Nginx có thư mục `sites-available` và `sites-enabled`. Mỗi trang web (Domain) bạn tạo một file riêng biệt. Sau đó tạo một Symlink (Lối tắt) qua `sites-enabled`. Làm vậy giúp bạn quản lý hàng chục trang web trên 1 máy chủ dễ dàng.
2. **Kiểm tra cú pháp trước khi Restart**: Cú pháp của Nginx cực kì khắt khe, thiếu 1 dấu chấm phẩy (`;`) là sập toàn bộ máy chủ Web. TRƯỚC KHI chạy lệnh `systemctl restart nginx`, BẮT BUỘC phải chạy lệnh `nginx -t` để Nginx tự kiểm tra lỗi chính tả. 
3. **Cấu hình `try_files` cho Frontend**: Khi xài ReactJS (React Router), người dùng gõ link `/about` rồi nhấn F5, Nginx sẽ báo lỗi 404 (Vì không có file nào tên là about.html trên ổ cứng). Bắt buộc phải thêm dòng `try_files $uri $uri/ /index.html;` để Nginx chuyển hướng mọi đường dẫn ảo về lại cho React xử lý.

</details>

1. **Modular Configuration (Sites-Available Pattern)**: Never dump all your routing logic into the root `nginx.conf` file. Follow the Debian/Ubuntu convention. Create individual configuration files for each domain in `/etc/nginx/sites-available/`. When you want to take the site live, create a symbolic link to `/etc/nginx/sites-enabled/`. This isolates configurations and prevents a typo in Domain A from crashing Domain B.
2. **Always Validate Syntax (`nginx -t`)**: Nginx configuration files are highly sensitive to missing semicolons (`;`) or unclosed braces. If you execute `systemctl restart nginx` with a typo, the entire proxy crashes, taking down every single website hosted on that server. **Absolute Rule**: ALWAYS run `nginx -t` (Test config) before reloading the service. It validates the syntax safely without interrupting active traffic.
3. **The `try_files` Directive for SPAs**: The most common bug when deploying React/Vue. Because SPAs utilize Client-Side Routing (HTML5 History API), if a user directly navigates to `yoursite.com/dashboard` and hits Refresh, Nginx searches the disk for a literal file named `dashboard` and throws a 404 Not Found error. You MUST include `try_files $uri $uri/ /index.html;`. This tells Nginx: "If the file doesn't exist, don't throw a 404. Just serve `index.html` and let the React Javascript figure out the routing."

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Vấn đề "IP Thực" của người dùng (X-Forwarded-For)**: Khi Nginx đứng chắn giữa. Node.js sẽ luôn tưởng rằng Nginx (IP: 127.0.0.1) chính là người gọi API. Kết quả là hệ thống log của bạn ghi nhận 100% khách hàng đều có IP là 127.0.0.1, khiến bạn không thể truy tìm Hacker hay chặn IP khách hàng được. 
   - *Cách giải*: Bắt buộc phải cấu hình Nginx nhét IP thật của khách vào Header `X-Forwarded-For`, và cấu hình Backend (VD: Express.js `app.set('trust proxy', true)`) để đọc cái Header đó.
2. **Lỗi Upload File lớn (413 Entity Too Large)**: Mặc định, Nginx cực kì cảnh giác. Nó chỉ cho phép người dùng Upload file nặng tối đa 1 MB. Nếu bạn làm chức năng Up Avatar nặng 2MB, Nginx sẽ ném lỗi `413` chặn đứng ngay lập tức, Backend chưa kịp nhìn thấy file đó. Bạn phải mở file config, thêm dòng `client_max_body_size 50M;` để tăng giới hạn.

</details>

1. **Losing the Real Client IP Address**: Because Nginx is a proxy, it terminates the Client's TCP connection and opens a new connection to the Backend. The Backend (e.g., Node.js) looks at the incoming connection and sees the IP `127.0.0.1` (Nginx's internal IP). If you use this IP for Rate Limiting or Security Logging, your backend is completely blind. **Rule**: You must configure Nginx to explicitly pass the real IP inside HTTP Headers using `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`. Furthermore, your backend framework must be explicitly configured to trust this header (e.g., in Express: `app.set('trust proxy', 1)`).
2. **The `413 Request Entity Too Large` Error**: By default, Nginx is extremely conservative. It strictly limits incoming HTTP POST body sizes to exactly 1 Megabyte to prevent buffer overflow attacks. If you build an Image Upload feature, and a user uploads a 2MB JPEG, Nginx instantly intercepts it and throws a 413 Error. The request never reaches your backend code. You must explicitly override this by setting `client_max_body_size 50M;` in your `server` block.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp các cấu hình Nginx kinh điển nhất. (Lưu tại `/etc/nginx/sites-available/domain.com`)
</details>

### 1. Serving a React/Vue Frontend (SPA)
```nginx
server {
    listen 80;
    server_name myapp.com;

    # Where your built React files live
    root /var/www/myapp/build;
    index index.html;

    location / {
        # CRITICAL for SPAs: If file not found, fallback to index.html
        try_files $uri $uri/ /index.html;
    }
}
```

### 2. Standard Reverse Proxy (Routing to Node.js / Spring Boot)
```nginx
server {
    listen 80;
    server_name api.myapp.com;

    location / {
        # Forward traffic to the hidden internal backend
        proxy_pass http://localhost:3000;
        
        # CRITICAL: Pass the Real IP and Headers to the Backend!
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Load Balancing Across Multiple Backends
```nginx
# Define the pool of servers
upstream backend_servers {
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
    server 10.0.0.3:3000;
}

server {
    listen 80;
    server_name api.myapp.com;

    location / {
        # Nginx will automatically Round-Robin traffic across all 3 IPs
        proxy_pass http://backend_servers;
    }
}
```

### 4. Essential Security & Limits
```nginx
server {
    # ... other configs ...

    # Allow users to upload files up to 50 Megabytes (Fixes 413 Error)
    client_max_body_size 50M;

    # Hide Nginx version number from hackers in HTTP Response headers
    server_tokens off;

    # Enable GZIP Compression to shrink JSON/HTML payloads by 70%
    gzip on;
    gzip_types text/plain application/json text/css application/javascript;
    gzip_min_length 1000;
}
```

### Essential CLI Commands
```bash
# Check if your configuration syntax is correct (DO THIS ALWAYS)
sudo nginx -t

# Apply new configuration WITHOUT dropping active client connections (Graceful)
sudo systemctl reload nginx

# Hard restart (Drops connections)
sudo systemctl restart nginx
```

---

## Related Topics

- For ultra-fast Layer 4 TCP load balancing (without HTTP parsing), explore **[HAProxy](./haproxy.md)**.
- For modern Kubernetes environments where IP addresses change dynamically, Nginx is often replaced by **[Envoy](./envoy.md)**.
- Backend frameworks shielded by Nginx include **[Node.js](../backend/nodejs-express.md)** and **[Spring Boot](../backend/spring-boot.md)**.
