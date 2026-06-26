# JVM Tuning & Observability

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Kỹ năng bắt buộc để đưa ứng dụng lên Production: Tinh chỉnh JVM cho môi trường Docker/Kubernetes, cấu hình Graceful Shutdown (Tắt ứng dụng an toàn) để không làm rơi rớt request của người dùng khi scale server, và triển khai Distributed Tracing (Truy vết phân tán) thông qua OpenTelemetry.

</details>

> **Summary**: Essential production readiness skills: Tuning the JVM for containerized environments (Kubernetes), implementing Graceful Shutdown to prevent dropped requests during scaling, and Distributed Tracing via OpenTelemetry.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **JVM Container Tuning**: Tưởng tượng bạn có 1 cái hộp giấy nhỏ (Docker Container) đựng 1 cái bong bóng (Java JVM). Máy tính của bạn là cái nhà to đùng. Java rất ngốc, nó tưởng nó đang ở trong cái nhà to đùng nên thổi cái bong bóng to dần lên. Kết quả là vỡ mất cái hộp giấy (Lỗi OOMKilled). Bạn phải cấu hình để báo cho Java biết: "Mày chỉ được thổi bong bóng bằng 75% cái hộp giấy thôi!".
- **Graceful Shutdown**: Giống như việc đóng cửa tiệm cắt tóc. Nếu đóng cửa cái rụp đuổi khách về khi người ta đang cắt dở (Lỗi 5xx). Graceful Shutdown là treo biển "Không nhận khách mới", nhưng vẫn từ từ hớt tóc cho xong những người đang ngồi trong tiệm rồi mới khóa cửa.
- **Distributed Tracing**: Tưởng tượng 1 cái bánh bị làm hỏng đi qua 5 xưởng khác nhau. Ai làm hỏng? Bạn gắn 1 cái chip theo dõi (Trace ID) vào cái bánh từ khâu đầu tiên. Chỉ cần quét chip, bạn sẽ thấy lịch sử: Xưởng 1 tốn 2 giây, Xưởng 2 tốn 1 giây, Xưởng 3 làm rơi bánh! Tracing giúp bạn bắt lỗi chính xác trong rừng Microservices.

</details>

- **JVM Container Tuning**: Imagine you have a small cardboard box (Docker Container) containing a balloon (Java JVM). Your computer is a giant house. Java is silly; it thinks it's in the giant house, so it inflates the balloon bigger and bigger. The result? It bursts the cardboard box (OOMKilled error). You must tune it to say: "Only inflate the balloon to 75% of the box's size!".
- **Graceful Shutdown**: It's like closing a barbershop. If you suddenly lock the door and kick out customers while halfway through a haircut, they get angry (HTTP 5xx error). Graceful Shutdown means hanging a "No new customers" sign, but finishing the haircuts for the people already sitting in the chairs before finally locking up.
- **Distributed Tracing**: Imagine a cake passing through 5 different factories and getting ruined. Who ruined it? You attach a tracking chip (Trace ID) to the cake at step one. By scanning the chip, you see the history: Factory 1 took 2 seconds, Factory 2 took 1 second, Factory 3 dropped the cake! Tracing helps you pinpoint exactly which microservice caused the error.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **JVM Container Tuning**: Cấu hình giới hạn bộ nhớ của Java (Heap và Non-Heap) sao cho phù hợp và không vượt quá giới hạn RAM và CPU mà Docker/Kubernetes cấp phát.
- **Graceful Shutdown (Tắt an toàn)**: Cấu hình web server (Tomcat/Netty) để nó ngừng nhận request *mới*, nhưng vẫn đợi để xử lý cho xong các request *đang chạy dở* trước khi ứng dụng thực sự tắt đi.
- **OpenTelemetry (OTel)**: Một framework mã nguồn mở tiêu chuẩn dùng để tạo ra, thu thập và xuất dữ liệu đo lường từ hệ thống (Bao gồm: Traces - Dấu vết, Metrics - Chỉ số, Logs - Nhật ký).

**Phân loại:**
- **Loại**: Kỹ năng SRE (Site Reliability Engineering) / Đưa hệ thống lên Production.
- **Môi trường**: Docker, Kubernetes, Cloud.

</details>

- **JVM Container Tuning**: Configuring Java memory limits (Heap vs. Non-Heap) to align with Docker/Kubernetes CPU and Memory quotas.
- **Graceful Shutdown**: Instructing the web server (Tomcat/Netty) to stop accepting *new* requests but finish processing *active* requests before the application exits.
- **OpenTelemetry (OTel)**: An open-source observability framework used to instrument, generate, collect, and export telemetry data (Traces, Metrics, Logs).

### Classification
- **Type**: Production Readiness / SRE (Site Reliability Engineering).
- **Target Environment**: Docker, Kubernetes, Cloud.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Cái bẫy RAM của Docker**
Java 8 trở về trước không hiểu cơ chế cgroups của Linux (thứ Docker dùng để giới hạn RAM). Nếu bạn cấp cho container `512MB` RAM, JVM lại nhìn ra bộ nhớ của *máy chủ vật lý* (ví dụ 32GB RAM) và cấp luôn 8GB cho Heap. Kết quả: Linux Kernel ngay lập tức `OOMKill` (giết) container của bạn vì vượt quá 512MB. Dù Java 17+ đã thông minh hơn, bạn vẫn phải tự tay cấu hình vì Heap chỉ là một phần nhỏ của RAM, Java còn dùng RAM cho Metaspace, Threads và Native Memory.

**Cái bẫy rớt request khi Deploy**
Trong Kubernetes, khi bạn deploy phiên bản mới, nó sẽ gửi lệnh tắt (`SIGTERM`) vào máy chủ cũ. Mặc định, Spring Boot sẽ "Rút phích cắm" ngay lập tức, cắt đứt toàn bộ kết nối Database và HTTP đang chạy dở. Hậu quả là người dùng đang thao tác sẽ nhận ngay lỗi 500 (Internal Server Error).

</details>

### The Container Memory Trap
Java 8 and earlier did not understand Linux cgroups (what Docker uses to limit memory). If you gave a container `512MB` of RAM, the JVM would look at the *Host OS* (e.g., 32GB RAM) and allocate a 8GB Heap. The Linux kernel would immediately `OOMKill` the container. While modern Java 17+ is container-aware, tuning is still required because the JVM Heap is only a fraction of total memory usage (Metaspace, Threads, Off-heap buffers).

### The Deployment Outage Trap
In Kubernetes, during a new deployment, a `SIGTERM` signal is sent to the old pod. By default, Spring Boot shuts down instantly, dropping any HTTP connections currently being processed or database queries in flight, causing 5xx errors for users.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có Graceful Shutdown: Đang deploy bản mới. Lệnh `SIGTERM` bắn tới. Spring Boot tắt ngay lập tức. User đang thanh toán dở nhận lỗi `HikariPool - Connection is closed` -> User chửi.
Có Graceful Shutdown: Lệnh `SIGTERM` bắn tới. Tomcat khóa cửa không nhận thêm khách. Nhưng nó kiên nhẫn đợi 30 giây cho User thanh toán xong. Xong xuôi, Tomcat mới tắt. Mọi thứ mượt mà.

</details>

### Without Graceful Shutdown
1. K8s sends `SIGTERM` to Pod A.
2. Spring Boot immediately closes the ApplicationContext. Database connection pool is destroyed.
3. User request #123 (halfway through processing) throws a `HikariPool - Connection is closed` exception.
4. User receives HTTP 500.

### With Graceful Shutdown
1. K8s sends `SIGTERM` to Pod A.
2. Spring Boot Tomcat stops accepting *new* HTTP connections. (New requests go to Pod B).
3. Tomcat waits up to 30 seconds for User request #123 to finish.
4. Request finishes successfully. User receives HTTP 200.
5. Spring Boot gracefully closes the DB pool and exits.

| Aspect | Default Spring Boot / K8s | Tuned & Graceful |
|---|---|---|
| JVM Memory | Ignorant of Container Limits (High OOMRisk) | Aware of Limits (`MaxRAMPercentage`) |
| K8s Deployments | Causes 500 Errors for active users | Zero-Downtime deployments |
| Troubleshooting | Looking blindly at 10 separate log files | Entering 1 `trace_id` to see the whole story |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Deploy Kubernetes Mượt mà**: Nâng cấp phiên bản phần mềm (Rolling updates) giữa trưa mà không làm rớt dù chỉ 1 request của khách hàng.
2. **Bắt rệp (Debug) Microservice**: Khách ấn "Mua" -> Order Service -> Inventory Service -> Payment Service bị lỗi. OpenTelemetry vẽ ra cái sơ đồ rễ cây, chỉ thẳng mặt: Payment Service mất 5 giây để chạy và văng lỗi NullPointer!
3. **Chỉnh siêu xe (High-Load Tuning)**: Đổi thuật toán dọn rác (Garbage Collection) sang ZGC để ứng dụng chứng khoán chạy nhanh không bao giờ bị khựng lại (Sub-millisecond pause).

</details>

1. **Kubernetes Deployments**: Rolling updates without dropping a single user request.
2. **Microservice Debugging**: A user clicks "Checkout" -> Order Service -> Inventory Service -> Payment Service. Payment fails. OpenTelemetry traces the exact path and shows exactly which service took 5 seconds and threw an exception.
3. **High-Load Tuning**: Adjusting Garbage Collection (e.g., ZGC or G1GC) to prevent stop-the-world pauses in low-latency trading applications.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Bí kíp JVM (Java 17+)**
- **Đừng dùng `-Xmx`**: Hãy dùng `-XX:MaxRAMPercentage=75.0`. Nó bảo JVM hãy chiếm 75% RAM của Container để làm Heap. 25% còn lại chừa cho HĐH và các thành phần Non-Heap.
- **Bật Log khi Crash**: Thêm `-XX:+HeapDumpOnOutOfMemoryError` để lỡ server có nổ RAM thì nó nhả ra cái file `.hprof`. Tải file đó về mở bằng Eclipse MAT để coi code nào làm rò rỉ RAM.

**2. Bí kíp Tắt an toàn (Graceful Shutdown)**
- **K8s PreStop Hook**: K8s gửi lệnh tắt (SIGTERM) VÀ lệnh xóa IP trên Load Balancer CÙNG LÚC. Load Balancer cần vài giây để cập nhật, nên request mới VẪN lọt vào máy chủ đang tắt. Để khắc phục, nhét cái lệnh `sleep 10` vào K8s `preStop` hook. Đợi Load Balancer cập nhật xong xuôi rồi mới cho Spring Boot tắt.

**3. Bí kíp Tracing**
- **Duy trì Trace ID**: Trace ID phải truyền liên tục qua HTTP Header (`traceparent`). Cẩn thận khi code Java gọi `@Async` hoặc tạo Thread mới, Thread mới không tự copy Trace ID của Thread cũ. Bắt buộc phải code thêm cơ chế copy MDC (Mapped Diagnostic Context) sang Thread mới.

</details>

### JVM Tuning Best Practices (Java 17+)
1. **Never use `-Xmx` in Containers**: Instead, use `-XX:MaxRAMPercentage=75.0`. This tells the JVM to use 75% of the *Container's* memory limit for the Heap. The remaining 25% is left for Metaspace, Thread stacks, and the OS.
2. **Choose the right GC**: 
   - G1GC (Default): Best overall balance of throughput and latency.
   - ZGC (`-XX:+UseZGC`): Use for massive heaps (>16GB) or when you require sub-millisecond pause times.
3. **Enable Crash Logs**: Add `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp` so if an OOM occurs, you have a file to analyze in Eclipse MAT.

### Graceful Shutdown Best Practices
1. **Enable in Spring Boot**: Set `server.shutdown=graceful`.
2. **K8s PreStop Hook**: Kubernetes sends a `SIGTERM` to the pod at the exact same time it tells the Ingress to stop routing traffic. Because Ingress updates take a few seconds, the pod might receive traffic *after* it started shutting down. Add a `preStop` sleep hook of 10 seconds in your K8s deployment to wait for network rules to propagate before Spring receives the `SIGTERM`.

### Distributed Tracing Best Practices
1. **Trace ID Propagation**: OpenTelemetry injects a `traceparent` header (W3C standard) into outgoing HTTP requests and Kafka messages. Ensure your asynchronous `@Async` methods or custom ThreadPools copy the MDC (Mapped Diagnostic Context) so the Trace ID isn't lost when switching threads.
2. **Log Correlation**: Configure Logback to include `trace_id` and `span_id` in every log line. When viewing a specific error log in Kibana/Datadog, you can instantly query all logs from all services that share that exact `trace_id`.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Để làm được Zero-Downtime Deployment hoàn hảo, phải kết hợp cả cấu hình Spring Boot (chờ request xử lý xong) VÀ cấu hình Kubernetes (`preStop` sleep 10s để chặn request mới dội vào).
Ngoài ra, Dockerfile phải xài biến môi trường `MaxRAMPercentage` để tự scale theo kích thước Container.

</details>

### 1. Spring Boot Graceful Shutdown (application.yml)

```yaml
server:
  shutdown: graceful # Waits for active requests to finish
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s # Maximum time to wait before force-killing
```

### 2. K8s Deployment configured for Zero-Downtime

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: spring-app
        image: my-backend:1.0.0
        lifecycle:
          preStop:
            exec:
              # Give K8s iptables 10 seconds to stop routing traffic here 
              # before letting the SIGTERM hit the Spring Boot process.
              command: ["sh", "-c", "sleep 10"]
```

### 3. Dockerfile with JVM Tuning (Java 17+)

```dockerfile
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app
COPY target/application.jar app.jar

# MaxRAMPercentage dynamically sizes the heap based on K8s limits
# ActiveProcessorCount ensures ThreadPools size themselves correctly
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75.0 \
               -XX:ActiveProcessorCount=2 \
               -XX:+HeapDumpOnOutOfMemoryError \
               -XX:HeapDumpPath=/tmp/heapdump.hprof"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### 4. OpenTelemetry Logback Configuration (Spring Boot 3)

*Note: Spring Boot 3 natively supports Micrometer Tracing which implements the W3C standard.*

```xml
<!-- logback-spring.xml -->
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <!-- [traceId, spanId] automatically injected by Micrometer Tracing -->
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} [traceId=%X{traceId:-}, spanId=%X{spanId:-}] - %msg%n</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="CONSOLE" />
    </root>
</configuration>
```

---

## Related Topics

- [Hexagonal & DDD](../02-software-architecture/hexagonal-and-ddd.md) — How tracing flows through application layers.
- [Microservices Architecture](../../02-concepts/architecture/microservices.md) — Why distributed tracing is a hard requirement for microservices.
