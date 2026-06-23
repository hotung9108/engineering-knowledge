# Java & Spring Boot

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu bạn muốn làm một cái web bán áo thun cuối tuần, hãy dùng Node.js. Nhưng nếu bạn được giao nhiệm vụ viết một hệ thống Ngân hàng lõi (Core Banking) xử lý 100.000 giao dịch chuyển tiền mỗi giây, nơi mà một dấu phẩy đặt sai chỗ sẽ làm bốc hơi hàng tỷ đô la, bạn BẮT BUỘC phải dùng **Java** và **Spring Boot**. Java là một ngôn ngữ "Thiết giáp": Nó gò bó, dài dòng, và bắt buộc mọi thứ phải được khai báo bằng Lớp (Class) và Kiểu dữ liệu (Type) rõ ràng. **Spring Boot** là một Framework khổng lồ được xây trên Java. Nó tự động hóa hàng ngàn công việc lặt vặt (Auto-Configuration) và quản lý các Lớp (Class) bằng một khái niệm ma thuật gọi là Inversion of Control (IoC), giúp hàng ngàn lập trình viên có thể code chung một dự án siêu lớn mà không giẫm chân lên nhau.

</details>

> **Summary**: While Node.js and Python excel at rapid prototyping and I/O agility, they often crumble under the structural weight of massively complex, transaction-heavy enterprise monoliths. **Java** is the undisputed heavyweight champion of Enterprise Backend Engineering. It provides uncompromising Static Typing, robust Object-Oriented paradigms, and the battle-tested Java Virtual Machine (JVM). **Spring Boot** is the preeminent framework within the Java ecosystem. It revolutionized Java development by eliminating the notorious XML configuration boilerplate of the legacy Spring Framework. It introduces "Opinionated Auto-Configuration" and manages the application lifecycle through its powerful **Inversion of Control (IoC) Container** and **Dependency Injection (DI)** architecture. It is the de facto standard for Tier-1 Financial, Healthcare, and Government systems globally.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang điều hành một Xưởng lắp ráp Ô tô khổng lồ.
1. **Cách làm cũ (Không có Spring)**: Bạn phải tự tay đi mua thép, tự thiết kế bản vẽ động cơ, tự nối từng sợi dây điện. Nếu động cơ hỏng, bạn phải tháo tung cả cái xe ra để sửa.
2. **Spring Boot (IoC & DI)**: Bạn chỉ việc ngồi ở phòng Giám đốc và nói: *"Tôi cần một cái Động cơ V8"*. Lập tức, Nhà máy (Spring Container) tự động đúc ra cái động cơ đó, và TỰ ĐỘNG lắp nó vào chiếc xe cho bạn (Dependency Injection). Bạn không cần biết nó được đúc thế nào. Nếu ngày mai bạn muốn đổi sang Động cơ Điện, bạn chỉ cần báo Nhà máy một câu, mọi chiếc xe sẽ tự động được lắp Động cơ Điện mà không cần bạn phải tự tay vặn một con ốc nào.

</details>

Imagine building a massive Skyscraper.
1. **Vanilla Java (No Framework)**: You must personally dig the foundation, mix the cement perfectly, forge your own steel beams, and wire every single electrical outlet by hand. It requires an insane amount of boilerplate effort before you can even build the first room.
2. **Spring Boot (IoC & Dependency Injection)**: You act as the Lead Architect. You draw a blueprint and declare: *"I need a Plumbing System here, and an Electrical Grid there"*. Spring Boot is the massive General Contractor. It reads your blueprint, instantly summons the Plumbers and Electricians (Dependency Injection), and connects everything perfectly in the background (Auto-Configuration). You just focus on designing the rooms.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Spring Boot được xây dựng dựa trên các trụ cột cực kỳ vững chắc:
1. **JVM (Java Virtual Machine)**: Code Java không chạy trực tiếp trên Windows hay Mac. Nó chạy trên JVM. Code 1 lần, mang cục code đó vứt lên bất kỳ hệ điều hành nào (Linux, Windows) nó đều chạy y hệt nhau.
2. **Inversion of Control (Đảo ngược quyền điều khiển)**: Bình thường, bạn viết code: `DB db = new DB()`. Bạn là người kiểm soát việc tạo ra DB. Trong Spring, bạn KHÔNG ĐƯỢC PHÉP dùng chữ `new`. Bạn chỉ việc đánh dấu `@Autowired DB db;`. Spring Boot sẽ tự động TẠO RA (new) và quản lý cái DB đó cho bạn.
3. **AOP (Aspect-Oriented Programming)**: Lập trình Hướng khía cạnh. Bạn có 100 hàm gọi API. Bạn muốn kiểm tra Quyền bảo mật trước khi cho chạy 100 hàm đó. Thay vì copy-paste đoạn code kiểm tra vào 100 hàm, AOP cho phép bạn viết code kiểm tra 1 lần, rồi "Gắn" (Aspect) nó vào đầu 100 hàm kia một cách hoàn toàn vô hình (Thông qua các Annotation như `@PreAuthorize`).

</details>

The architectural superiority of Spring Boot rests on core Java and Enterprise design patterns:
1. **The JVM (Write Once, Run Anywhere)**: Java compiles down to Bytecode, which is executed by the Java Virtual Machine. The JVM is an engineering marvel, featuring extremely advanced Just-In-Time (JIT) compilation and highly tuned Garbage Collection (G1GC, ZGC), making it capable of sustaining millions of high-throughput operations per second seamlessly.
2. **The IoC Container & Dependency Injection**: In standard programming, classes instantiate their own dependencies (`new Service()`), creating tight coupling. Spring utilizes **Inversion of Control**. The Spring ApplicationContext (Container) creates all objects (Beans) at startup. When a Controller requires a Service, it declares it in its constructor, and Spring dynamically injects the Singleton instance at runtime. This guarantees extreme decoupling and perfect Unit Testability (Mocking).
3. **AOP (Aspect-Oriented Programming)**: Cross-cutting concerns (e.g., Security, Logging, Database Transactions) clutter business logic. Spring AOP allows developers to extract this boilerplate into distinct "Aspects". By simply adding an annotation like `@Transactional` above a method, Spring dynamically wraps the method in an invisible try/catch block that automatically handles SQL commits or rollbacks if an exception is thrown.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao các Ngân hàng không dùng Node.js mà lại tôn thờ Java Spring Boot?
1. **Sự An toàn của Hệ thống Kiểu tĩnh (Static Typing)**: Java bắt buộc bạn phải khai báo mọi thứ. Một hàm tính tiền phải nhận vào kiểu `BigDecimal` (Số cực kỳ chính xác), và ói ra `BigDecimal`. Bạn không thể vô tình truyền chữ "Mười" vào đó được. Lỗi bị phát hiện ngay lúc gõ code, chứ không phải lúc tiền đã bay mất.
2. **Đa luồng thực sự (Multi-threading)**: Node.js chỉ có 1 luồng. Nếu bạn có 1 bài toán phức tạp (như tính lãi suất cho 1 triệu khách hàng cùng lúc), Node.js sẽ đơ. Java có hàng nghìn luồng (Threads) chạy song song thực sự trên các nhân CPU.
3. **Kiến trúc rõ ràng (Convention over Configuration)**: Mở 100 dự án Spring Boot ra, bạn sẽ thấy 100 dự án có chung một cấu trúc: `Controller` $\rightarrow$ `Service` $\rightarrow$ `Repository`. Bất kỳ Dev Java nào nhảy vào công ty mới cũng có thể code được ngay trong ngày đầu tiên.

</details>

Why is Spring Boot the undisputed standard for Tier-1 Enterprise, FinTech, and GovTech architectures?
1. **Uncompromising Type Safety & OOP**: Financial systems cannot tolerate the dynamic type coercion bugs prevalent in Python or JavaScript. Java's strict Object-Oriented constraints enforce rigid data contracts. Using `BigDecimal` ensures absolute precision for currency math. Errors are caught by the IDE Compiler immediately, preventing catastrophic runtime production failures.
2. **True Multi-Threading (Concurrency)**: While Node.js fakes concurrency via the Event Loop, Java utilizes true OS-level Multi-Threading. If a system must execute heavily CPU-bound tasks (e.g., massive batch processing of millions of transactions, complex cryptographic hashing, deep algorithmic calculations), Java can spawn thousands of concurrent threads across multiple CPU cores, obliterating Node.js in raw computational throughput. (And with modern Java 21's **Virtual Threads**, it now matches Node/Go in I/O efficiency as well).
3. **Ecosystem & Predictability**: Spring Boot enforces an incredibly rigid standard. It ships with battle-tested libraries for Security (Spring Security), Data access (Spring Data JPA / Hibernate), and messaging (Spring Kafka). An engineer transferring from IBM to a local Bank will find the exact same architectural directory structures and the exact same `@Annotations`, enabling massive organizational scalability.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc quản lý Giao dịch (Transaction) trong Database. Ví dụ: Chuyển tiền từ A sang B. Bị lỗi ở B thì phải hoàn lại tiền cho A (Rollback).
</details>

Visualizing Database Transactions (Vanilla vs Spring AOP).

| Metric | Vanilla Code (No Framework) | Spring Boot (`@Transactional`) |
|---|---|---|
| **The Boilerplate**| `Connection conn = db.getConnection();`<br>`try {`<br>`  conn.setAutoCommit(false);`<br>`  updateA();`<br>`  updateB();`<br>`  conn.commit();`<br>`} catch(Exception e) {`<br>`  conn.rollback();`<br>`} finally {`<br>`  conn.close();`<br>`}` | `@Transactional`<br>`public void transfer() {`<br>`  updateA();`<br>`  updateB();`<br>`}` |
| **Developer Effort**| High. You must manually write the exact same 10 lines of connection-handling boilerplate for every single database operation. Forgetting `finally` causes connection leaks. | **Zero**. You write pure business logic. Spring's AOP Proxy invisibly wraps your method in the exact boilerplate shown on the left. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hệ thống nguyên khối khổng lồ (Enterprise Monoliths)**: Hệ thống quản trị ERP của bệnh viện, phần mềm quản lý Kho vận (Logistics). Đây là những hệ thống có hàng ngàn bảng (Tables) trong Database, logic móc nối chằng chịt. Spring Data JPA (Hibernate) giúp việc quản lý hàng ngàn bảng này cực kỳ dễ dàng thông qua các Class Java (Entity).
2. **Kiến trúc Microservices**: Mặc dù Java khá nặng, nhưng hệ sinh thái Spring Cloud cung cấp TẬN RĂNG các công cụ để xây dựng Microservices: Service Discovery (Eureka), API Gateway, Distributed Tracing. Nó là bộ công cụ chuẩn mực nhất để chia nhỏ hệ thống.
3. **Bảo mật cấp độ cao (Spring Security)**: Bạn cần một hệ thống có phân quyền siêu phức tạp: "Trưởng phòng chỉ được xem dữ liệu của nhân viên phòng đó, Giám đốc được xem hết, Nhân viên quèn chỉ được xem của mình". Spring Security cung cấp một bộ khung bảo mật (Security Filter Chain) mạnh mẽ nhất thế giới để xử lý việc này chỉ bằng vài dòng Cấu hình.

</details>

1. **Massive Domain-Driven Monoliths**: ERPs, Hospital Management Systems, and Supply Chain Logistics. These applications possess hyper-complex business rules and database schemas containing thousands of tables. Spring Boot, paired with **Hibernate / Spring Data JPA**, abstracts the SQL drudgery. Developers map Java Objects (`@Entity`) directly to Database Tables, enabling extremely rapid querying of deeply nested relational data using pure Java methods (`findByEmailAndStatus()`).
2. **Enterprise Microservices (Spring Cloud)**: While Go and Node are lighter, Spring Boot remains dominant in Microservices due to **Spring Cloud**. It provides out-of-the-box infrastructure for Service Discovery (Eureka), Client-side Load Balancing, Distributed Configuration (Config Server), and Circuit Breakers (Resilience4j). It is a complete, turnkey solution for building distributed architectures.
3. **Complex Authorization Pipelines (Spring Security)**: Handling granular, row-level Access Control Lists (ACLs), OAuth2/OIDC flows, and LDAP Active Directory integrations. Building this from scratch in Node/Express is a massive security risk. Spring Security provides an impenetrable, heavily audited Filter Chain architecture. Developers can secure individual methods easily using `@PreAuthorize("hasRole('ADMIN')")`.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Chỉ tiêm qua Constructor (Constructor Injection)**: Ngày xưa, người ta lạm dụng `@Autowired` gắn thẳng lên trên cái biến (Field Injection). Việc này làm cho code không thể Unit Test được nếu không có Spring. Hiện tại, LỜI KHUYÊN BẮT BUỘC là phải tiêm qua Hàm khởi tạo (Constructor). Hoặc dùng thư viện Lombok (`@RequiredArgsConstructor`) để code ngắn gọn.
2. **Sử dụng DTO (Data Transfer Object)**: Tuyệt đối không bao giờ trả nguyên cái Class Database (Entity) về cho Frontend. Lỡ trong Entity có trường `password` hoặc `salary`, Frontend sẽ thấy hết. Bắt buộc phải tạo một Class DTO riêng (chỉ chứa tên và email), map dữ liệu từ Entity sang DTO rồi mới trả về.

</details>

1. **Mandate Constructor Injection (Ban Field Injection)**: Historically, developers lazily applied `@Autowired` directly to class fields. This is now considered a severe Anti-Pattern because it tightly couples the class to the Spring Framework, rendering pure Java Unit Testing impossible. **Rule**: Always utilize Constructor Injection. It enforces immutability (`final` fields) and explicitly declares dependencies. Use **Lombok's** `@RequiredArgsConstructor` to auto-generate the constructor boilerplate invisibly.
2. **Strict Entity-DTO Segregation**: The most dangerous security flaw in Spring applications is returning an `@Entity` (Database mapped object) directly in a `@RestController`. This explicitly leaks the database schema to the public internet, often accidentally exposing sensitive fields (e.g., `hashedPassword`, `internalAuditId`). **Rule**: You MUST create separate **Data Transfer Objects (DTOs)**. Map the `UserEntity` to a `UserResponseDTO` (using mapping libraries like *MapStruct*) before returning JSON to the client.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khởi động quá chậm và Tốn RAM (Cold Start / Memory Bloat)**: Đây là điểm yếu chí mạng của Java Spring. Một app Node.js khởi động mất 1 giây, tốn 50MB RAM. Một app Spring Boot khởi động mất 10 giây, chưa làm gì đã ngốn 500MB RAM. Do đó, KHÔNG NÊN dùng Spring Boot cho kiến trúc "Serverless Lambda" (nơi mà máy chủ bị tắt bật liên tục). Spring Boot chỉ hợp cắm rễ chạy 24/24 trên Máy chủ ảo (EC2 / Kubernetes).
2. **Cơn ác mộng N+1 Hibernate**: JPA / Hibernate quá thông minh nên đôi khi thành thảm họa. Bạn lệnh cho nó lấy ra 100 Sinh viên. Do cấu hình sai, Hibernate tự động bắn thêm 100 câu lệnh SQL nữa để lấy danh sách Môn học của từng sinh viên. DB bị quá tải. 
   - *Luật*: Luôn bật `spring.jpa.show-sql=true` ở môi trường Dev để nhìn xem Hibernate đang chạy lệnh SQL gì ngầm ở dưới. Luôn dùng `JOIN FETCH` để dập tắt N+1.

</details>

1. **The Serverless / Memory Bloat Incompatibility**: The JVM is heavily optimized for long-running throughput, NOT fast startup. A standard Spring Boot application loads thousands of classes into memory and utilizes Reflection to scan for annotations during startup. This results in a massive memory footprint (often > 500MB idle) and slow startup times (5-15 seconds). **Rule**: Spring Boot is a catastrophic choice for ephemeral Serverless architectures (e.g., AWS Lambda) where "Cold Starts" will destroy user latency. It must be deployed as persistent, long-running containers (Kubernetes/ECS). *(Note: Spring Native / GraalVM is actively trying to solve this by compiling Java to machine code).*
2. **Hibernate N+1 and LazyInitializationExceptions**: The double-edged sword of Object-Relational Mappers (ORM). Hibernate masks raw SQL behind Java method calls. If a `UserEntity` has a `@OneToMany` relationship with `Roles`, iterating through 50 Users and calling `user.getRoles()` will trigger 50 distinct SQL `SELECT` queries (The N+1 Problem). Conversely, if you close the database session before calling `getRoles()`, Hibernate throws a fatal `LazyInitializationException`. **Fix**: Developers must fundamentally understand the underlying SQL. Utilize `@EntityGraph` or custom JPQL `JOIN FETCH` queries to aggressively load required relations in a single optimized SQL statement.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cấu trúc chuẩn xác nhất của một ứng dụng Spring Boot 3 REST API.
</details>

### The Standard Layered Architecture (Lombok Enabled)

**1. The Entity (Database Table Mapping)**
```java
package com.example.demo.model;

import jakarta.persistence.*;
import lombok.Data; // Lombok auto-generates Getters/Setters

@Entity
@Table(name = "users")
@Data
public class UserEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String passwordHash; // We NEVER want to send this to the frontend
}
```

**2. The DTO (Data Transfer Object)**
```java
package com.example.demo.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class UserResponseDTO {
    private Long id;
    private String email;
    // Notice: passwordHash is deliberately omitted!
}
```

**3. The Repository (Data Access / DAO)**
```java
package com.example.demo.repository;

import com.example.demo.model.UserEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

// Spring Data JPA magically writes the SQL queries for you
public interface UserRepository extends JpaRepository<UserEntity, Long> {
    
    // Just by naming the method correctly, Spring writes the 'SELECT * WHERE email = ?'
    Optional<UserEntity> findByEmail(String email); 
}
```

**4. The Service (Business Logic)**
```java
package com.example.demo.service;

import com.example.demo.model.UserEntity;
import com.example.demo.dto.UserResponseDTO;
import com.example.demo.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor // Lombok auto-creates Constructor for Dependency Injection!
public class UserService {

    private final UserRepository userRepository; // Injected Dependency

    @Transactional(readOnly = true)
    public UserResponseDTO getUserById(Long id) {
        UserEntity user = userRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("User not found"));
            
        // Map Entity to DTO before returning
        return UserResponseDTO.builder()
                .id(user.getId())
                .email(user.getEmail())
                .build();
    }
}
```

**5. The Controller (REST API Endpoint)**
```java
package com.example.demo.controller;

import com.example.demo.dto.UserResponseDTO;
import com.example.demo.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService; // Injected Dependency

    @GetMapping("/{id}")
    public ResponseEntity<UserResponseDTO> getUser(@PathVariable Long id) {
        UserResponseDTO response = userService.getUserById(id);
        return ResponseEntity.ok(response); // Returns HTTP 200 JSON
    }
}
```

---

## Related Topics

- For managing the Database that Spring communicates with, see **[PostgreSQL](../databases/postgresql.md)**.
- If Spring Boot's memory usage is too heavy for your Microservice, consider exploring **[Go](./go.md)**.
- For scaling and deploying Spring Boot containers, see **[Docker & Kubernetes](../cloud-infra/docker.md)**.
