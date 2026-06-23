# Go (Golang)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: C++, Java thì quá phức tạp và nặng nề. Python, Node.js thì dễ viết nhưng chạy chậm và quản lý đa luồng (Multi-threading) rất tồi tệ. Google đã tạo ra **Go (Golang)** vào năm 2009 để giải quyết bài toán cốt lõi của họ: "Làm sao để có một ngôn ngữ chạy nhanh như C++, nhưng lại dễ học như Python, và đặc biệt là xử lý hàng triệu kết nối mạng song song một cách dễ dàng nhất?". Sự đột phá lớn nhất của Go là **Goroutines** - một cơ chế Đa luồng siêu nhẹ. Nhờ Goroutines, một máy chủ Go có thể mở hàng trăm ngàn luồng chạy song song mà chỉ tốn vài chục Megabytes RAM. Ngày nay, Go là vị vua thống trị mảng Cloud, Microservices, và là ngôn ngữ đứng sau các công nghệ khổng lồ như Docker và Kubernetes.

</details>

> **Summary**: Software engineering historically suffered a severe dichotomy: C++ and Java offered blazing performance and strict memory control at the cost of extreme developmental complexity and slow compilation. Conversely, Python and Node.js offered rapid prototyping but suffered from sluggish runtime speeds and notoriously difficult/inefficient concurrency models. Google engineered **Go (Golang)** in 2009 to resolve this exact bottleneck for their massive cloud infrastructure. Go is a statically typed, compiled language with garbage collection. Its defining architectural masterpiece is its Concurrency Model, powered by **Goroutines** and **Channels**. By introducing ultra-lightweight user-space threads multiplexed onto OS threads, Go achieves the raw execution speed of C++ while making massive concurrency as trivial as adding the `go` keyword before a function. It is the undisputed language of modern Cloud-Native infrastructure (Docker, Kubernetes, Terraform).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn phải vận chuyển 1 triệu viên gạch.
1. **Java/C++ (OS Threads)**: Bạn thuê những chiếc Xe tải hạng nặng. Sức chở rất lớn, nhưng việc nổ máy, sang số, quay đầu xe (Context Switching) mất rất nhiều thời gian. Hơn nữa, những chiếc xe tải này tốn cực kỳ nhiều chỗ đậu (RAM). Cùng lúc bạn chỉ có thể cho chạy 1000 xe tải.
2. **Node.js (Single Thread)**: Bạn chỉ thuê ĐÚNG 1 chiếc Xe máy. Xe máy luồn lách rất nhanh, giao 1 viên gạch cực kỳ lẹ. Nhưng rốt cuộc, nó vẫn chỉ là 1 chiếc xe. Khi nó đang chở gạch cho người này thì 999.999 người kia phải đứng chờ.
3. **Go (Goroutines)**: Bạn tạo ra một đàn Kiến 100.000 con. Kiến cực kỳ nhỏ, tốn cực kỳ ít chỗ đậu (chỉ 2KB RAM mỗi con so với 2MB của xe tải). Đàn kiến tỏa ra làm việc song song cùng một lúc. Khi một con kiến bị kẹt đường, 99.999 con kia vẫn bò đi giao gạch bình thường. Bạn giao xong 1 triệu viên gạch với tốc độ ánh sáng mà tốn rất ít tiền nuôi kiến.

</details>

Imagine a Call Center answering telephones.
1. **Java/C++ (OS Threads)**: Every time the phone rings, you hire a full-time, salary-paid Employee, give them a huge desk, a computer, and health insurance. Hiring them takes time, and you can only fit 1,000 desks in the building before you run out of physical space (RAM exhaustion).
2. **Node.js (Event Loop)**: You hire exactly ONE super-fast Ninja. The Ninja answers Phone 1, tells them to hold, answers Phone 2, tells them to hold, and constantly runs back and forth. It's incredibly efficient for simple questions, but if Phone 1 requires a 10-minute complex math calculation, the Ninja is trapped, and every other caller hears infinite ringing.
3. **Go (Goroutines)**: You invent magical, invisible helper-bots. Every time the phone rings, you snap your fingers and a bot instantly appears. It costs absolutely nothing to summon them (2KB of RAM). You can easily have 100,000 bots talking to 100,000 customers simultaneously in a small room. If one bot gets stuck doing complex math, the other 99,999 bots are completely unaffected.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Compiled Language (Ngôn ngữ biên dịch)**: Khác với JS hay Python cần môi trường trung gian (Node.js/Trình duyệt) để dịch code lúc chạy. Go dịch toàn bộ code của bạn thành một file nhị phân (Binary) `app.exe` (chỉ gồm số 0 và 1) hiểu trực tiếp bởi Hệ điều hành. File này chạy độc lập, cực nhanh và không cần cài đặt thêm bất kỳ thứ gì trên Server.
2. **Goroutines**: Là những luồng (Thread) ảo do Go quản lý. Thay vì xin Hệ điều hành (OS) cấp phát Thread (tốn 2MB RAM), Go tự tạo ra Goroutines (chỉ tốn 2KB RAM). Hệ thống Go Scheduler sẽ tự động nhét hàng ngàn Goroutines này chạy luân phiên trên một vài Thread thật của máy tính.
3. **Channels (Ống nước)**: Khi hàng ngàn Goroutines chạy song song, việc chúng cãi nhau giành quyền ghi đè dữ liệu là thảm họa. Go giới thiệu Channels: Những cái ống nước kết nối các Goroutines lại với nhau. Nếu Goroutine A muốn đưa dữ liệu cho Goroutine B, nó ném dữ liệu vào ống nước. An toàn tuyệt đối, không bao giờ bị đụng độ (Race Condition).

</details>

1. **Statically Typed & Compiled**: Go is a compiled language. Unlike interpreted languages (Python, JS) or bytecode languages requiring massive Virtual Machines (Java JVM, C# CLR), the Go compiler (`go build`) generates a single, self-contained, statically-linked Machine Code binary executable. You can compile a Go app on your Mac, drop the 10MB binary onto a naked Alpine Linux server (which has zero dependencies installed), and it runs instantly with raw native CPU performance.
2. **Goroutines (Green Threads)**: The crown jewel of Go. A Goroutine is an extremely lightweight, user-space thread managed explicitly by the Go Runtime Scheduler, NOT the Operating System. An OS thread consumes ~2MB of stack memory; a Goroutine consumes merely ~2KB. The Go Scheduler multiplexes hundreds of thousands of Goroutines onto a small pool of actual OS threads using an M:N scheduling algorithm. If a Goroutine blocks on Network I/O, the Scheduler instantly pauses it and swaps in a working Goroutine without executing an expensive OS Context Switch.
3. **Channels (CSP Concurrency Model)**: Traditional Java/C++ concurrency relies on Mutexes and Shared Memory, notoriously leading to Deadlocks and Race Conditions. Go utilizes Communicating Sequential Processes (CSP). **"Do not communicate by sharing memory; instead, share memory by communicating."** Channels act as thread-safe, typed, synchronization pipelines where Goroutines can safely pass data to each other.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Google gặp khủng hoảng vào những năm 2000. Máy chủ C++ của họ biên dịch quá lâu (có khi mất cả tiếng đồng hồ). Khi có lỗi xảy ra, việc debug đa luồng trong C++ khó đến mức muốn tự tử. Trong khi đó, các kĩ sư trẻ viết Python rất nhanh, nhưng code Python chạy quá chậm để phục vụ hàng tỷ lượt tìm kiếm.
Go ra đời với triết lý: **Sự đơn giản là tối thượng**. 
Go cố tình LƯỢC BỎ đi những thứ màu mè của ngôn ngữ hiện đại: Không có Class, Không có Inheritance (Kế thừa), Không có Exceptions (try/catch), Không có Generics (đến mãi gần đây mới có). Sự "Cổ hủ" này ép các lập trình viên phải viết code cực kì minh bạch, dễ đọc. Mở source code Go ra, mọi thứ luôn rõ ràng từ trên xuống dưới. Biên dịch 1 dự án khổng lồ bằng Go chỉ mất vài giây.

</details>

Google engineered Go because their massive engineering scale broke existing languages.
C++ provided necessary speed but suffered from catastrophic compile times (often exceeding 45 minutes for massive Google binaries) and impenetrable, spaghetti-like object hierarchies. Python provided development speed but failed drastically under Google's hyperscale I/O load.
Go exists to maximize **Engineering Productivity at Scale**. Its design philosophy is strictly Minimalist and brutally Pragmatic. It aggressively excludes "clever" programming paradigms. It originally excluded Generics, it excludes Class-based Inheritance, and it explicitly excludes `try/catch` Exception handling in favor of explicit error values. This simplicity guarantees that a Go codebase written by a junior engineer looks functionally identical to a Go codebase written by a principal architect. It compiles instantly, deploys as a single binary, and provides the best concurrency model in modern computing.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc gọi 3 API đồng thời (Song song). Hàm nào nhanh thì trả về trước.
</details>

Visualizing Concurrency (Fetching 3 APIs simultaneously).

| Metric | JavaScript / Node.js | Go (Golang) |
|---|---|---|
| **The Concept** | Event Loop (Asynchronous). The single thread promises to check back later. | Goroutines (Parallel). 3 literal worker bots execute simultaneously. |
| **The Code** | `await Promise.all([`<br>`  fetch(api1), `<br>`  fetch(api2), `<br>`  fetch(api3)`<br>`])` | `go fetch(api1, channel)`<br>`go fetch(api2, channel)`<br>`go fetch(api3, channel)`<br>`// Wait for channel data` |
| **CPU Usage** | Excellent for network waiting (I/O). But if `api1` requires parsing a 500MB JSON file, `api2` and `api3` must wait. The single thread is blocked. | **Flawless**. The Go Scheduler puts the 3 Goroutines on 3 separate CPU Cores. The heavy JSON parsing on Core 1 does not delay Core 2 or Core 3. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hạ tầng Đám mây & DevOps (Cloud-Native)**: Hệ sinh thái Cloud hiện đại được xây bằng Go. Docker, Kubernetes, Terraform, Prometheus. Nếu bạn muốn trở thành Kỹ sư DevOps đỉnh cao, Go là ngôn ngữ bắt buộc phải học để có thể can thiệp sâu vào các công cụ này.
2. **Microservices hiệu năng cao**: Bạn có một ứng dụng đặt xe taxi. Dịch vụ "Theo dõi vị trí tài xế GPS" nhận hàng chục ngàn tọa độ mỗi giây. Viết bằng Node.js có thể tràn RAM. Viết bằng Java Spring Boot thì tốn quá nhiều RAM khởi động. Go là sự lựa chọn hoàn hảo: File chạy siêu nhẹ (vài chục MB), khởi động mất 0.1 giây, và tải được hàng chục ngàn kết nối cùng lúc mà không nóng máy.
3. **API Gateway / Load Balancers**: Nơi đứng mũi chịu sào, phải nhận hàng triệu Request từ bên ngoài rồi phân phát vào bên trong. Go xử lý các luồng mạng (Network Sockets) cực kỳ tối ưu.

</details>

1. **Cloud Infrastructure & DevOps Tooling**: The absolute monopoly of Go. The entire modern Cloud-Native landscape—Docker, Kubernetes, Terraform, Prometheus, HashiCorp Vault, Istio—is authored purely in Go. If a developer wishes to extend Kubernetes Operators or contribute to modern DevOps tooling, Go is the mandatory language.
2. **High-Throughput Microservices**: A ride-hailing company (like Uber, which heavily utilizes Go) has a GPS tracking microservice ingesting 50,000 coordinates per second. A Java Spring Boot service might require 1GB of baseline RAM and 10 seconds to start. Node.js might struggle with the CPU parsing of the massive GeoJSON streams. Go deploys a 15MB binary, starts in 50 milliseconds, consumes 30MB of RAM, and handles the 50,000 WebSocket connections flawlessly utilizing Goroutines.
3. **Network Tools & API Gateways**: Building proxies, load balancers, and command-line interfaces (CLIs). Go's standard library (`net/http`) is so robust and performant that it is consistently used to build production-grade web servers without relying on massive external frameworks.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Xử lý lỗi rõ ràng (Explicit Error Handling)**: Điểm đặc trưng nhất của Go là bạn sẽ phải viết `if err != null` hàng trăm lần. Đừng khó chịu. Khác với Java ném Exception (lỗi tàng hình bay lung tung khó kiểm soát), Go coi Lỗi là một Giá trị bình thường. Bắt buộc bạn phải nhìn thẳng vào sự thật: "Hàm này có thể gây lỗi, bạn muốn giải quyết cái lỗi này ngay bây giờ như thế nào?".
2. **Luôn sử dụng `defer` để dọn dẹp**: Khi bạn mở 1 File hay mở 1 kết nối Database, hãy lập tức viết ngay dòng `defer file.Close()` ngay bên dưới dòng mở. Go sẽ tự động ghi nhớ và ĐẢM BẢO hàm Close sẽ luôn được gọi khi thoát ra ngoài, dù cho giữa chừng có xảy ra lỗi đi chăng nữa.

</details>

1. **Embrace Explicit Error Handling (`if err != null`)**: Developers migrating from Java/TS absolutely hate this at first. Go lacks `try/catch`. Functions that can fail return two values: the result, and an Error object. You are forced to explicitly check `if err != null { return err }` immediately. **Do not fight this paradigm.** Exceptions in Java are "invisible control flows" that lead to unpredictable crashes. Go treats errors as explicit, first-class values. It forces the developer to acknowledge and handle the failure exactly where it occurs, resulting in the most robust, crash-proof production applications in the industry.
2. **Master the `defer` Statement for Resource Cleanup**: Memory leaks often occur when a developer opens a Database Connection, executes logic, hits an error, and returns early, forgetting to close the connection at the bottom of the function. **Best Practice**: The exact microsecond you open a resource, write `defer db.Close()` on the very next line. The `defer` keyword pushes the function onto a LIFO stack. Go mathematically guarantees that `db.Close()` will execute right before the function exits, regardless of how many `return` statements or panic crashes occur in the middle of the logic.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bỏ quên Goroutine rò rỉ (Goroutine Leaks)**: Bạn tạo ra 1 Goroutine bằng lệnh `go doSomething()`. Bên trong đó có một vòng lặp vô hạn hoặc chờ một Channel nhưng không bao giờ có dữ liệu tới. Goroutine đó sẽ bị treo mãi mãi trong RAM. Cứ mỗi lần khách hàng vào, bạn lại đẻ thêm 1 con Goroutine bị treo. Chỉ sau 1 ngày, Server của bạn sẽ cạn sạch RAM.
   - *Luật*: Đừng bao giờ khởi chạy một Goroutine nếu bạn không biết chắc chắn khi nào nó kết thúc. Luôn dùng `context.Context` để có thể Cắt đứt (Cancel) các Goroutine chạy quá lâu.
2. **Dùng biến chung không khóa (Race Conditions)**: 2 Goroutines cùng lúc sửa một biến `count = count + 1`. Vì 2 luồng chạy song song, chúng đè lên nhau, kết quả ra sai bét.
   - *Luật*: Khi dùng đa luồng, tuyệt đối dùng `Channels` để truyền dữ liệu cho nhau. Nếu bắt buộc phải sửa chung một biến, hãy dùng Ổ khóa `sync.Mutex` để khóa biến đó lại: "Đứa này sửa xong thì đứa kia mới được vào sửa".

</details>

1. **Goroutine Leaks (Silent OOM Crashes)**: Goroutines are incredibly cheap, but they are not free. If you launch `go processTask(channel)` and the channel never receives data, the Goroutine blocks forever. It is not garbage collected. If this occurs on an HTTP route, 1,000 visitors = 1,000 permanently leaked Goroutines. The server eventually crashes with an Out-of-Memory (OOM) panic. **The Fix**: Never launch a Goroutine without explicitly understanding exactly how and when it will terminate. Always pass a `context.Context` (with a timeout or cancellation function) down into your Goroutines to aggressively kill them if they take too long.
2. **Shared Memory Race Conditions**: You launch 10 Goroutines that all execute `counter++` on a global variable. Because `counter++` requires 3 CPU cycles (Read, Increment, Write), the Goroutines read the same baseline value, increment it, and overwrite each other. The final counter will be random. **The Fix**: Adhere to Go's proverb: Share memory by communicating (using Channels). If you must mutate a shared variable, you MUST wrap the mutation in a `sync.Mutex` (Lock) or utilize atomic operations (`sync/atomic`), completely locking the memory address until the mutation cycle finishes.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cú pháp Go (Golang) cho xây dựng REST API cơ bản.
</details>

### Basic Syntax & Structs
```go
package main

import "fmt"

// Define a Struct (Go's version of a Class)
type User struct {
    ID   int    `json:"id"` // Struct Tags define how JSON is formatted
    Name string `json:"name"`
}

// Attach a Method to the Struct (Receiver function)
func (u *User) Greet() string {
    return fmt.Sprintf("Hello, I am %s", u.Name)
}

func main() {
    // Variable declaration
    age := 25 // Short syntax (Type inferred)
    
    // Pointers (Passing by reference for performance)
    u := &User{ID: 1, Name: "Alice"} 
    fmt.Println(u.Greet())
}
```

### Explicit Error Handling
Go does not have try/catch. Functions return multiple values.

```go
import (
    "errors"
    "fmt"
)

func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("cannot divide by zero")
    }
    return a / b, nil // nil means "No Error"
}

func main() {
    result, err := divide(10, 0)
    
    // IMMEDIATELY CHECK THE ERROR
    if err != nil {
        fmt.Println("CRITICAL FAILURE:", err)
        return
    }
    
    fmt.Println("Success:", result)
}
```

### Concurrency: Goroutines & Channels
The superpower of Go.

```go
package main

import (
    "fmt"
    "time"
)

// Worker function
func fetchAPI(apiName string, ch chan string) {
    time.Sleep(2 * time.Second) // Simulate network delay
    ch <- fmt.Sprintf("%s data loaded", apiName) // Send data INTO the channel
}

func main() {
    // Create a pipeline (Channel) that transfers Strings
    ch := make(chan string)

    // Launch 3 parallel Goroutines instantly
    go fetchAPI("API 1", ch)
    go fetchAPI("API 2", ch)
    go fetchAPI("API 3", ch)

    // Block and wait to receive 3 messages FROM the channel
    msg1 := <-ch
    msg2 := <-ch
    msg3 := <-ch

    fmt.Println(msg1, msg2, msg3) // Takes exactly 2 seconds total, not 6 seconds!
}
```

### Simple HTTP Web Server (Standard Library)
Go's standard library is powerful enough to not need massive frameworks. (Though frameworks like `Gin` or `Fiber` are popular).

```go
package main

import (
    "encoding/json"
    "net/http"
)

func handleUsers(w http.ResponseWriter, r *http.Request) {
    if r.Method == http.MethodGet {
        users := []User{ {ID: 1, Name: "Alice"} }
        
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(users)
    }
}

func main() {
    // Register the route
    http.HandleFunc("/api/users", handleUsers)
    
    // Start the server on port 8080
    fmt.Println("Server running on port 8080")
    http.ListenAndServe(":8080", nil)
}
```

---

## Related Topics

- If Go's lack of OOP features feels too restrictive, explore Enterprise **[Spring Boot (Java)](./spring-boot.md)**.
- If you prefer rapid prototyping over raw multithreading speed, use **[Node.js / Express](./nodejs-express.md)**.
- Go is the core language powering containers. See **[Docker & Kubernetes](../cloud-infra/docker.md)**.
