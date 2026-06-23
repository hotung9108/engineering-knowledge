# I/O Models: Blocking vs. Non-blocking vs. Multiplexing

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: I/O (Input/Output) là hoạt động đọc/ghi file từ ổ cứng hoặc gọi mạng qua Internet. Nó cực kỳ chậm so với CPU. Cách server quản lý I/O (Đứng chờ hay Bỏ đi làm việc khác) quyết định kiến trúc cốt lõi của toàn bộ các Framework hiện đại. Hiểu I/O Models là hiểu được vì sao Node.js/Nginx có thể gánh hàng chục nghìn kết nối mà không bị treo.

</details>

> **Summary**: I/O (Input/Output) encompasses reading/writing to physical disks or resolving network requests via the Internet. It is astronomically slower than CPU execution. How an Operating System and Web Server manage this I/O latency (Blocking and waiting vs. Asynchronous multiplexing) dictates the absolute scalability limit of the architecture. Understanding I/O Models is the fundamental key to comprehending why Node.js, Nginx, and Netty exist.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (CPU) là đầu bếp, và bạn gọi shipper (Mạng/Disk) đi mua gia vị (I/O).
1. **Blocking I/O (Đứng đợi)**: Bạn gọi shipper đi mua. Bạn đứng khoanh tay đợi 30 phút ở cửa. Trong lúc đó không làm gì cả. (Phí phạm CPU).
2. **Non-blocking I/O (Hỏi liên tục)**: Bạn gọi shipper đi mua. Bạn quay vào thái thịt. Cứ 1 phút bạn lại chạy ra cửa sổ hét lên: "Shipper về chưa?!". Rất phiền phức và tốn sức.
3. **I/O Multiplexing (Có người báo thức)**: Bạn thuê một bảo vệ (Epoll/Kqueue). Bạn bảo ông ấy: "Khi nào shipper về thì gõ cửa gọi tôi, còn giờ tôi đi nấu món khác". Bạn nấu nướng thỏa thích. 30 phút sau bảo vệ gõ cửa, bạn ra lấy gia vị. Rất hiệu quả!

</details>

Imagine you (the CPU) are a chef, and you order an ingredient delivery (a Network I/O request).
1. **Blocking I/O (Synchronous)**: You place the order. You walk to the front door and stand there perfectly still for 30 minutes until the delivery arrives. You do zero cooking during this time. (Massive CPU waste).
2. **Non-blocking I/O (Polling)**: You place the order. You return to the kitchen and chop onions. Every 60 seconds, you sprint to the window and scream, "Is the delivery here yet?!" It allows you to cook, but constantly checking the window wastes energy.
3. **I/O Multiplexing (Event Loop/Epoll)**: You hire a security guard (Epoll). You tell him, "Watch the door for my delivery. Knock when it arrives." You go back to the kitchen and cook uninterrupted. When the delivery arrives, the guard knocks (an Event Interrupt). You grab it and continue. Maximum efficiency!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

I/O Models là các cơ chế do Hệ điều hành (Linux/Windows) cung cấp để phần mềm giao tiếp với phần cứng.
1. **Blocking I/O**: Luồng (Thread) gọi một hàm I/O (VD: Đọc file). Luồng đó bị Hệ điều hành cho vào trạng thái "Ngủ" (Sleep) cho đến khi file đọc xong.
2. **Non-blocking I/O**: Luồng gọi hàm I/O. Hệ điều hành lập tức trả về lỗi "Chưa xong", luồng không bị ngủ mà có thể chạy lệnh khác. Lát sau nó phải tự chủ động gọi lại hàm I/O để kiểm tra xem xong chưa (Polling).
3. **I/O Multiplexing (epoll trong Linux / kqueue trong macOS)**: Một Luồng duy nhất có thể theo dõi hàng vạn I/O cùng một lúc. Nó nói với OS: "Tôi ngủ đây, nếu bất kỳ I/O nào trong 10,000 cái này xong thì gọi tôi dậy".

</details>

I/O Models are structural mechanisms provided by the Operating System Kernel (Linux/Windows) to mediate hardware interactions.
1. **Blocking I/O**: An execution Thread initiates a read system call. The OS immediately blocks (sleeps) the Thread. The Thread is physically suspended and consumes zero CPU cycles until the hardware interrupt signals the data is ready.
2. **Non-blocking I/O**: A Thread initiates a read system call. If data is not instantly ready, the OS returns an `EWOULDBLOCK` error instead of sleeping the thread. The Thread continues executing, but must actively loop and re-poll the OS later to check if data has arrived.
3. **I/O Multiplexing (`epoll` in Linux, `kqueue` in macOS/FreeBSD)**: The magic behind modern web scale. A single Thread delegates the monitoring of thousands of File Descriptors (Sockets) to the Kernel. The Thread calls `epoll_wait()` and sleeps. The OS wakes the Thread up the millisecond *any* of the thousands of sockets receive data.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Cổ chai C10K (Vấn đề 10,000 kết nối đồng thời)**
Vào những năm 2000, các Web Server (như Apache) dùng **Blocking I/O**. Cứ 1 user truy cập $\rightarrow$ tạo 1 Thread. Thread này lại phải đợi Blocking I/O đọc Database.
Để phục vụ 10,000 user, máy chủ phải sinh ra 10,000 Threads. 10,000 Threads gây ra "Context Switching" làm CPU bốc cháy và RAM cạn kiệt (OOM).

Để giải quyết, **I/O Multiplexing** ra đời. Cho phép Nginx hoặc Node.js chỉ dùng đúng 1 Thread duy nhất, nhưng gánh được 10,000 kết nối song song nhờ cơ chế báo thức (Event-driven).

</details>

**The C10K Problem (Handling 10,000 concurrent connections)**
In the early 2000s, traditional Web Servers (like Apache HTTP Server) relied strictly on the **Blocking I/O** model. 1 incoming user connection $\rightarrow$ Spawns 1 OS Thread. That thread spends 99% of its life blocked, waiting for database queries or slow network clients to send data.
To serve 10,000 concurrent users, the server spawned 10,000 active Threads. The immense memory overhead (Stack memory) and OS Context Switching completely saturated the CPU. The server crashed.

**I/O Multiplexing** was engineered directly into the Linux Kernel (`epoll`) to solve this. It allowed revolutionary technologies like **Nginx** and **Node.js** to serve 10,000 connections simultaneously using only a *Single Thread*, completely eradicating the Thread Context Switching bottleneck.

---

## Layer 3: Without vs. With Comparison (Compare)

### Thread-per-request (Blocking) vs. Event Loop (Multiplexing)

| Metric | Apache (Blocking / Thread-per-request) | Nginx / NodeJS (I/O Multiplexing) |
|---|---|---|
| **Thread Count (for 10K users)** | 10,000 OS Threads | 1 to 4 OS Threads (Event Loops) |
| **RAM Consumption** | ~10 GB (1MB stack per thread) | ~50 MB |
| **Context Switching Overhead** | Extreme (CPU spends time juggling threads) | Near Zero (CPU spends time executing logic) |
| **Scalability Limit** | Low (~10K concurrent before crashing) | Massive (100K+ concurrent easily) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Blocking I/O (Thread-per-request)**: Được dùng trong Java Spring Boot truyền thống (Tomcat), Django, Ruby on Rails. Phù hợp cho các ứng dụng nội bộ doanh nghiệp, CRUD đơn giản, lượng truy cập không quá lớn nhưng logic xử lý phức tạp.
- **I/O Multiplexing (Event-driven)**: Trái tim của Node.js, Nginx, Redis, và WebSockets. Bắt buộc phải dùng cho hệ thống Chat real-time, Live stream, hoặc API Gateway gánh hàng trăm ngàn user.

</details>

- **Blocking I/O (Thread-per-request)**: The traditional architecture of Java Spring Boot (Tomcat Servlet Container), Python Django, and Ruby on Rails. Extremely easy to write and debug code for. Perfect for standard Enterprise CRUD applications where CPU logic is heavy, but concurrent traffic rarely exceeds a few thousand parallel connections.
- **I/O Multiplexing (Event-driven)**: The core engine powering Node.js, Nginx, Redis, Netty (Spring WebFlux), and WebSocket servers. Absolutely mandatory for highly concurrent architectures like Real-time Chat applications, Live Streaming platforms, API Gateways, and high-frequency Microservices.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Không bao giờ "Block" Event Loop**: Trong Node.js hoặc WebFlux, bạn chỉ có 1 luồng chính (Main Thread). Nếu bạn cho luồng đó tính số nguyên tố thứ 1 tỷ (Tốn 5 giây CPU), toàn bộ 10,000 user đang kết nối sẽ bị đơ cứng 5 giây. Các tác vụ nặng về CPU phải được đẩy ra Background Worker (Message Queue).
2. **Hiểu bản chất của Asynchronous**: Khi dùng `async/await` để gọi Database, Thread của bạn không hề đứng đợi. Nhờ I/O Multiplexing, Thread được giải phóng để đi phục vụ request khác.

</details>

1. **Never Block the Event Loop**: The golden rule of I/O Multiplexing systems (Node.js, Vert.x, WebFlux). You only have one executing thread. If you execute a heavy CPU-bound task (e.g., Image processing, hashing a massive password, calculating large primes) that takes 5 seconds, you freeze the *entire server*. All 10,000 concurrent clients will hang for 5 seconds. CPU-bound tasks must be offloaded to separate background Worker Pools or Message Queues.
2. **Understand the Magic of Asynchrony**: When you execute `await database.query()`, your CPU Thread does *not* pause and wait. Under the hood, the framework registers a callback with the OS `epoll` and instantly frees the Thread to serve another incoming HTTP request. This illusion of synchronous code executing asynchronously is the triumph of the modern Web.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng nhầm thư viện Đồng bộ trong hệ thống Bất đồng bộ**: Bạn dùng Node.js nhưng lại gọi hàm `fs.readFileSync()`. Hàm này là Blocking I/O. Nó sẽ giết chết tính năng Multiplexing và phá hủy toàn bộ hiệu năng của Node.js. Luôn dùng `fs.readFile()` (Callback/Promise).
2. **Nghĩ rằng I/O Multiplexing tính toán nhanh hơn**: Sai. Nó không làm toán nhanh hơn Blocking I/O. Nó chỉ quản lý kết nối rảnh rỗi (idle connections) tốt hơn mà không tốn RAM. Nếu hệ thống của bạn cần Render Video (nặng về CPU), Blocking I/O (Multi-thread) mới là chân ái.

</details>

1. **Accidentally Introducing Blocking Calls in an Async Runtime**: Using Node.js but calling `fs.readFileSync()` instead of `fs.readFile()`, or using a legacy JDBC blocking driver in a Spring WebFlux application. A single blocking system call suspends the entire Event Loop Thread, completely destroying the massive scalability benefits of Multiplexing.
2. **Misunderstanding Multiplexing's Purpose**: I/O Multiplexing does *not* execute code faster. A single database query takes the exact same amount of time in Node.js as it does in Java. Multiplexing merely allows the server to survive massively concurrent *idle* network waiting without consuming infinite RAM via OS Threads. For raw, heavy CPU number-crunching, Multi-threading is superior.

---

## Related Topics

- To understand the underlying difference between Threads and Processes, see **[Process vs Thread](./process-thread.md)**.
- See how Concurrency interacts with I/O in **[Concurrency](../computer-science/concurrency.md)**.
