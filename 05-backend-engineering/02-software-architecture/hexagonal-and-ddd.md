# Hexagonal Architecture & Domain-Driven Design (DDD)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Kiến trúc Hexagonal (Ports & Adapters) và Domain-Driven Design (DDD) là những mẫu kiến trúc nâng cao giúp tách biệt hoàn toàn core business logic khỏi các yếu tố infrastructure (database, framework, API bên ngoài). Thay vì code phụ thuộc vào Database (như kiến trúc 3-layer truyền thống), Database giờ đây chỉ là một "Adapter" cắm vào "Port" của Core Domain. Điều này giúp hệ thống dễ dàng thay đổi công nghệ (ví dụ chuyển từ MySQL sang MongoDB) mà không phải sửa lại logic nghiệp vụ.

</details>

> **Summary**: Advanced architectural patterns for isolating the core business domain from infrastructure concerns, ensuring long-term maintainability and testability.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tưởng tượng một chiếc Tivi (Core Domain).
- **Kiến trúc cũ**: Dây cáp điện, anten, và đầu đĩa được hàn chết luôn vào bên trong bảng mạch của chiếc Tivi. Nếu hỏng dây điện, bạn phải vứt luôn cả cái Tivi.
- **Hexagonal Architecture**: Chiếc Tivi được thiết kế với các Cổng Cắm (Ports) ở phía sau: Cổng HDMI, cổng nguồn, cổng USB. Bạn mua một cái USB chứa phim (Adapter), cắm vào cổng USB (Port). Tivi không cần biết cái USB đó của hãng nào, chạy chip gì, nó chỉ lấy phim lên chiếu. Nếu muốn đổi sang ổ cứng di động, chỉ việc rút USB ra và cắm ổ cứng vào. Core (chiếc Tivi) được bảo vệ và độc lập hoàn toàn.

</details>

Imagine a Television (Core Domain).
- **Old Architecture**: The power cable, antenna, and DVD player are permanently soldered to the motherboard inside the TV. If the power cable breaks, you have to throw away the whole TV.
- **Hexagonal Architecture**: The TV is designed with Ports on the back: HDMI, power port, USB port. You buy a USB drive with movies (Adapter) and plug it into the USB port (Port). The TV doesn't care what brand the USB is or what chip it uses; it just reads the movie and plays it. If you want to switch to a portable hard drive, you just unplug the USB and plug in the hard drive. The Core (the TV) is completely protected and independent.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Domain-Driven Design (DDD)**: Một triết lý phát triển phần mềm đặt Core Business (Logic nghiệp vụ cốt lõi) lên vị trí ưu tiên hàng đầu. Nó đưa ra các khái niệm như Entities (Thực thể), Value Objects (Đối tượng giá trị), Aggregates (Gộp), và Repositories.
- **Hexagonal Architecture (Ports and Adapters)**: Một mẫu kiến trúc đặt "bộ não" của ứng dụng (Domain) ở trung tâm. Bộ não này định nghĩa các **Ports** (Ổ cắm / Interface). Thế giới bên ngoài (Web, DB, Message Broker) kết nối vào bộ não thông qua các **Adapters** (Đầu cắm / Implementation).

**Phân loại:**
- **Loại**: Kiến trúc Ứng dụng.
- **Nguyên lý cốt lõi**: Đảo ngược Phụ thuộc (Dependency Inversion) — Core Domain không phụ thuộc vào bất cứ thứ gì; mọi thứ khác phải phụ thuộc vào Core.
- **Tên gọi khác**: Onion Architecture, Clean Architecture.

</details>

- **Domain-Driven Design (DDD)**: A software development philosophy that prioritizes the core business domain. It introduces concepts like Entities, Value Objects, Aggregates, Repositories, and Domain Events.
- **Hexagonal Architecture (Ports and Adapters)**: An architectural pattern that puts the application core (Domain) in the center. The core defines **Ports** (interfaces), and the outside world (Web, DB, Message Brokers) connects to the core via **Adapters** (implementations).

### Classification
- **Type**: Application Architecture.
- **Core Principle**: Dependency Inversion (The core domain depends on *nothing*; everything depends on the core).
- **Alternative Names**: Onion Architecture, Clean Architecture.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề với Kiến trúc 3-Tier truyền thống**
Trong kiến trúc truyền thống (`Controller -> Service -> Repository`), các lớp phụ thuộc từ trên xuống dưới. Lớp Service (Nghiệp vụ) phụ thuộc vào Repository (Database), nghĩa là logic kinh doanh bị trói chặt vào công nghệ database (ví dụ: các annotation của JPA, các câu query SQL).

Nếu bạn muốn test logic kinh doanh, bạn bắt buộc phải bật một database ảo hoặc viết các đoạn mock (làm giả) rất phức tạp. Dần dần, các quy tắc kinh doanh bị trộn lẫn vào các câu lệnh SQL, làm hệ thống cứng nhắc không thể thay đổi.

**Giải pháp Hexagonal**
Bằng cách dùng Đảo ngược Phụ thuộc, Domain tự định nghĩa một bản hợp đồng (`UserRepository`). Lớp Hạ tầng (Infrastructure) phải tuân theo hợp đồng đó bằng cách code ra `JpaUserRepositoryAdapter`. Nhờ vậy, Domain giữ được sự thuần khiết (chỉ là code Java nguyên bản), không hề biết Spring, JPA, hay Web là gì.

</details>

### The Problem with 3-Tier Architecture
In traditional layered architecture (`Controller -> Service -> Repository`), dependencies point downwards. The Service depends on the Repository, meaning business logic is tightly coupled to database specifics (e.g., JPA entities, SQL queries). 

If you want to test the business logic, you are forced to spin up an in-memory database or write complex mocks. Over time, business rules leak into SQL queries, making the system rigid.

### The Hexagonal Solution
By using Dependency Inversion, the Domain declares an interface (`UserRepository`). The Infrastructure layer implements it (`JpaUserRepositoryAdapter`). The Domain remains pure Java (POJOs), totally ignorant of Spring, JPA, or the web.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có Hexagonal: File logic của bạn chứa đầy các chữ `@Service`, `@Autowired`, gọi thẳng hàm `save` của JPA. Mới nhìn là biết code bị trói chặt vào Framework Spring.
Có Hexagonal: File logic của bạn tên là `Order.java` không chứa MỘT CHỮ NÀO liên quan tới Spring hay Database. Nó chỉ có các hàm thuần túy như `placeOrder()`. Test cái này cực kỳ dễ vì nó không dính líu tới môi trường chạy.

</details>

### Without Hexagonal (Traditional 3-Tier)
```java
// Business logic is polluted with Framework and Database annotations
@Service
public class OrderService {
    @Autowired
    private JpaOrderRepository repository; // Tightly coupled to JPA

    @Transactional
    public void createOrder(OrderRequest request) {
        OrderEntity entity = new OrderEntity();
        entity.setStatus("CREATED");
        repository.save(entity); // Business logic depends on database
    }
}
```

### With Hexagonal Architecture (Ports & Adapters)
```java
// CORE DOMAIN: Pure Java, NO Spring/JPA annotations
public class Order { // Aggregate Root
    private OrderId id;
    private OrderStatus status;

    public void placeOrder() {
        if (this.status != OrderStatus.DRAFT) throw new DomainException("...");
        this.status = OrderStatus.CREATED;
    }
}

// PORT: Defined in the Core Domain
public interface OrderRepository {
    void save(Order order);
}

// INFRASTRUCTURE ADAPTER: Implements the Port using JPA
@Component
public class JpaOrderAdapter implements OrderRepository {
    private final SpringDataJpaRepository repository;
    
    @Override
    public void save(Order order) {
        OrderEntity entity = OrderMapper.toEntity(order);
        repository.save(entity);
    }
}
```

| Aspect | 3-Tier Architecture | Hexagonal Architecture |
|---|---|---|
| Dependency Direction | Top-down (Web -> Domain -> DB) | Outside-in (Web -> Domain <- DB) |
| Core Domain purity | Low (Polluted with `@Entity`, `@Table`) | High (Pure Java/Kotlin) |
| Unit Testability | Hard (Requires mocking DB layers) | Easy (Core domain has no dependencies) |
| Boilerplate | Low | High (Requires mapping between Domain and Entities) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Khi nào nên dùng Hexagonal & DDD**
1. **Logic nghiệp vụ cực kỳ phức tạp**: Ngân hàng, Bảo hiểm, Phần mềm ERP. Nơi các quy tắc kinh doanh thay đổi liên tục.
2. **Microservices**: DDD là phương pháp hoàn hảo nhất để xác định ranh giới giữa các microservices (Bounded Contexts).
3. **Dự án dài hạn (5+ năm)**: Đảm bảo khi các Framework bị lỗi thời, bạn có thể vứt bỏ Framework cũ thay bằng cái mới mà không ảnh hưởng một dòng code Core Logic nào.

**Không nên dùng khi nào**
- **Dự án CRUD đơn giản**: Nếu web của bạn chỉ để thêm/sửa/xóa bảng dữ liệu, áp dụng DDD là tự bắn vào chân vì quá tốn thời gian.
- **Startup cần ra mắt gấp (MVP)**: Viết code mappers giữa Domain và Database sẽ làm giảm tốc độ code lúc đầu.

</details>

### When to use Hexagonal & DDD
1. **Complex Business Logic**: Financial systems, ERPs, insurance platforms where business rules change frequently.
2. **Microservices**: DDD Bounded Contexts are the ideal way to define microservice boundaries.
3. **Long-lifespan Projects**: Systems expected to live 5+ years where frameworks will inevitably be upgraded or replaced.

### Anti-Patterns (When NOT to use)
- **Simple CRUD Applications**: If your app just reads and writes to a database without complex rules, DDD is a massive over-engineering.
- **Tight Deadlines / Startups**: The initial setup and mapping boilerplate will slow down MVP delivery.
- **Data-Driven Apps**: Apps that just visualize database tables directly (e.g., simple dashboards).

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất**:
1. **Tách biệt Domain và Database Entity**: Phải có 2 class riêng: `Order` (không có `@Entity`) và `OrderJpaEntity` (dùng để lưu database). Phải dùng tool như MapStruct để dịch qua lại ở biên giới.
2. **Dùng Value Objects**: Thay vì dùng kiểu `String email`, hãy tạo một class tên `Email`. Class này sẽ tự kiểm tra tính hợp lệ (`@` và `.com`) ngay lúc khởi tạo. Dữ liệu rác sẽ không bao giờ lọt được vào Domain.
3. **Mô hình Domain Giàu có (Rich Domain)**: Đừng viết các class chỉ có get/set (Anemic Domain). Hãy nhét hàm xử lý vào thẳng bên trong đối tượng. Viết `order.applyDiscount()` thay vì `orderService.applyDiscount(order)`.

**Cạm bẫy (Pitfalls)**:
1. **Thuế Mapping**: Dev sẽ rất ức chế khi phải viết code chuyển đổi (mapper) từ DTO -> Domain -> DB Entity. Nó có vẻ dư thừa, nhưng đó là cái giá phải trả để đổi lấy sự độc lập.
2. **Lọt kẽ hở Infrastructure**: Vô tình trả về đối tượng `Page<T>` của Spring từ một Port. Điều này làm Core Domain bị dính líu trở lại với Spring Data.

</details>

### Best Practices
1. **Separate Domain Models from Data Entities**: `Order` (Domain) and `OrderJpaEntity` (Database) must be different classes. Do not put `@Entity` on your Domain objects. Use mappers (e.g., MapStruct) at the boundaries.
2. **Use Value Objects**: Instead of `String email`, create an `Email` class that validates itself upon instantiation. This prevents invalid data from ever entering the Domain.
3. **Domain Events**: When a state changes (e.g., `OrderPlaced`), the Domain should emit an event. The Infrastructure layer listens to this event and publishes it to Kafka/RabbitMQ.
4. **Rich Domain Models**: Avoid "Anemic Domain Models" (classes with just getters and setters). Put the business logic *inside* the entity. (e.g., `order.applyDiscount()` instead of `orderService.applyDiscount(order)`).

### Common Pitfalls
1. **The Mapping Tax**: Developers get frustrated writing mappers between DTOs -> Domain -> Entities. It feels redundant, but this isolation is the price of maintainability.
2. **Leaking Infrastructure**: Accidentally returning a Spring `Page<T>` object from a Port, which couples the core domain back to Spring Data.
3. **Massive Aggregates**: Designing an Aggregate Root that pulls in 50 related entities. Keep Aggregates small and reference other Aggregates by ID only.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đây là cấu trúc thư mục chuẩn mực. Thư mục `domain` tuyệt đối không được gọi bất cứ thư viện (dependency) nào từ bên ngoài. Thư mục `infrastructure` chứa code giao tiếp web, kết nối DB. Thư mục `application` là nơi gọi và móc nối chúng lại với nhau.

</details>

### Standard Directory Structure for Spring Boot Hexagonal

```
src/main/java/com/example/shop/
├── domain/                    <-- CORE (No Spring/JPA dependencies)
│   ├── model/                 <-- Entities, Value Objects
│   ├── repository/            <-- Outbound Ports (Interfaces)
│   ├── service/               <-- Domain Services
│   └── exception/             <-- Business Exceptions
├── application/               <-- USE CASES (Spring @Service allowed here)
│   ├── port/in/               <-- Inbound Ports (Interfaces for Web)
│   └── service/               <-- Application Services (Orchestration)
└── infrastructure/            <-- ADAPTERS (Spring, JPA, Web, Kafka)
    ├── web/                   <-- REST Controllers (Inbound Adapters)
    ├── persistence/           <-- JPA Entities, Repositories (Outbound Adapters)
    └── messaging/             <-- Kafka Publishers/Listeners
```

### Implementing a Value Object (Java 17 Record)

```java
public record EmailAddress(String value) {
    public EmailAddress {
        if (value == null || !value.contains("@")) {
            throw new IllegalArgumentException("Invalid email format");
        }
    }
}
```

---

## Related Topics

- [JPA Performance Tuning](../03-high-performance-data/jpa-performance-tuning.md) — How to optimize the Infrastructure Persistence adapters.
- [Transactional Outbox Pattern](../04-distributed-async/transactional-outbox-pattern.md) — Publishing Domain Events safely from the infrastructure layer.
