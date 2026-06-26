# Consumer-Driven Contract Testing

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Một chiến lược kiểm thử (testing) nâng cao dành cho kiến trúc Microservices, đảm bảo rằng các API và các sự kiện truyền tin không bao giờ bị hỏng khi bên Cung cấp (Producer) và bên Tiêu thụ (Consumer) cập nhật code độc lập với nhau.

</details>

> **Summary**: An advanced testing strategy for microservices that guarantees APIs and messaging events do not break when producers and consumers evolve independently.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tưởng tượng Team A là quán Phở (Provider). Team B là khách hàng (Consumer).
- **Cách cũ (Test tích hợp)**: Khách hàng mua phở về ăn, thấy quán bỏ hành lá vào (trong khi khách không ăn hành). Khách giận dỗi không thèm ăn (Hệ thống sập).
- **Contract Testing (Test theo Hợp đồng)**: Trước khi mua, khách hàng (Team B) viết ra một bản hợp đồng: "Tôi mua 1 tô phở, yêu cầu BẮT BUỘC KHÔNG CÓ HÀNH". Quán Phở (Team A) nhận bản hợp đồng đó và treo trong bếp. Mỗi khi Quán nấu xong 1 tô mới, họ phải tự đối chiếu với bản Hợp đồng của khách. Nếu lỡ tay bỏ hành vào, bát phở bị hắt đi làm lại từ trong bếp (Code build thất bại), không bao giờ đến tay khách hàng. Nhờ vậy, khách hàng luôn nhận được đúng thứ họ cần!

</details>

Imagine Team A is a Noodle Shop (Provider). Team B is a customer (Consumer).
- **The Old Way (Integration Test)**: The customer buys noodles, takes them home, and sees green onions inside (which they hate). The customer refuses to eat (System crash).
- **Contract Testing**: Before buying, the customer (Team B) writes a contract: "I want 1 bowl of noodles, STRICTLY NO GREEN ONIONS". The Noodle Shop (Team A) takes this contract and hangs it in their kitchen. Every time they cook a new bowl, they automatically check it against the customer's contract. If they accidentally put green onions in, the bowl is thrown away in the kitchen (Code build fails) and never reaches the customer. This way, the customer always gets exactly what they need!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Kiểm thử Hợp đồng do Người Tiêu Dùng Thúc Đẩy (CDC Testing)** là một phương pháp luận nơi người dùng của một API (hoặc message broker) sẽ là người định nghĩa chính xác cấu trúc dữ liệu mà họ mong đợi. Những kỳ vọng này được ghi lại thành các "Hợp đồng". Bên cung cấp (Provider/Producer) sau đó sẽ phải chạy các kịch bản test tự động đối chiếu với các hợp đồng này để đảm bảo họ không phá vỡ mong đợi của bất kỳ consumer nào.

**Phân loại:**
- **Loại**: Chiến lược Test Microservices.
- **Frameworks**: Spring Cloud Contract, Pact.
- **Mục đích thay thế**: Thay thế cho các bài Test E2E (End-to-End) thông qua UI thường rất chậm và thiếu ổn định.

</details>

**Consumer-Driven Contract (CDC) Testing** is a methodology where consumers of an API (or message broker) define the exact shape of the data they expect. These expectations are recorded as "Contracts." The provider (producer) then runs automated tests against these contracts to ensure they do not violate any consumer's expectations.

### Classification
- **Type**: Microservices Testing Strategy.
- **Frameworks**: Spring Cloud Contract, Pact.
- **Replaces**: Flaky and slow End-to-End (E2E) UI testing.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi số lượng microservices tăng lên, việc đảm bảo chúng có thể giao tiếp an toàn với nhau trở nên phức tạp theo cấp số nhân.
- **Unit Tests** (Test Đơn vị) chỉ chứng minh được code chạy đúng trong phạm vi nội bộ.
- **Integration Tests** (Test Tích hợp) chứng minh code kết nối được với DB, nhưng lại thường dùng dữ liệu "giả" (mock) khi gọi API sang service khác. Dữ liệu giả thì luôn đúng, nhưng thực tế bên kia đã đổi API rồi!
- **E2E Tests** (Test Đầu cuối) phải bật toàn bộ cụm 50 service lên để test. Nó chạy cực kỳ chậm, hay hên xui (flaky), và tốn tiền duy trì một môi trường Staging khổng lồ.

Contract Testing mang lại **sự tự tin của E2E testing** nhưng với **tốc độ và sự cô lập của Unit Testing**.

</details>

As the number of microservices grows, ensuring they can safely communicate becomes exponential in complexity.
- **Unit Tests** only prove that a service works in isolation.
- **Integration Tests** prove that a service talks to a database, but often mock HTTP calls to other services.
- **E2E Tests** spin up the entire cluster and test user flows. They are slow, fragile (flaky), and require maintaining a massive shared staging environment.

Contract Testing provides the **confidence of E2E testing** with the **speed and isolation of Unit Testing**.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có Contract Test: Team A (Quản lý User) âm thầm đổi tên biến `firstName` thành `first_name`. Team A chạy Unit Test thấy vẫn Pass nên deploy lên Production. Team B (Thanh toán) gọi qua Team A, tìm không thấy biến `firstName` đâu, lỗi `NullPointerException`. Sập server!
Có Contract Test: Team B quăng 1 bản hợp đồng cho Team A ghi rõ: "Tôi cần biến `firstName`". Khi Team A đổi thành `first_name` và nhấn nút Build, hệ thống tự động đối chiếu với hợp đồng của Team B và báo FAILED ngay lập tức. Code không được phép deploy. Không có server nào bị sập!

</details>

### Without Contract Testing (The Integration Nightmare)
```text
[Team A - User Service] changes `firstName` to `first_name` in the JSON response.
Unit tests pass.
Deployed to Production.

[Team B - Billing Service] calls User Service expecting `firstName`.
Receives `first_name`, parses it as `null`.
Production Outage. 
Team B blames Team A for breaking the API.
```

### With Contract Testing (Safe Deployments)
```text
[Team B - Billing Service] writes a Contract: "When I call GET /users/1, I expect a field called 'firstName'".
This contract is published to a shared Broker (e.g., Pact Broker).

[Team A - User Service] changes `firstName` to `first_name`.
Team A runs their CI pipeline.
The pipeline pulls the Contract from the Broker.
The pipeline automatically generates a test hitting Team A's local API.
The test FAILS: "Expected 'firstName', got 'first_name'".
Team A's deployment is blocked. Outage prevented.
```

| Aspect | E2E Testing | Contract Testing |
|---|---|---|
| Speed | Very Slow (Minutes/Hours) | Very Fast (Milliseconds/Seconds) |
| Flakiness | High (Network timeouts, DB state) | Zero (Runs in isolation) |
| Feedback Loop | Late (After deployment to Staging) | Early (During local build / CI) |
| Debuggability | Hard (Which service failed?) | Easy (Points to the exact JSON field) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **REST APIs**: Xác thực cấu trúc JSON, mã HTTP status, và headers không bị thay đổi phá vỡ (breaking changes).
2. **Message Brokers (Kafka/RabbitMQ)**: Đảm bảo cấu trúc gói tin sự kiện (ví dụ `OrderCreatedEvent`) luôn chứa trường `totalAmount`.
3. **GraphQL**: Đảm bảo việc thêm sửa schema không làm chết các app Mobile cũ (khách hàng chưa update app).

**Không nên làm**:
- **Dùng Contract Test để check logic kinh doanh**: Contract chỉ quan tâm đến HÌNH DÁNG dữ liệu (kiểu String, tên field). Nó không quan tâm đến việc `amount = 100` tính thuế đúng hay sai. Việc đó là của Unit Test.
- **Provider-Driven Contracts (Bên cung cấp tự viết hợp đồng)**: Nếu Team A tự viết hợp đồng, họ sẽ tự test chính họ, điều này vô nghĩa. Giá trị thật sự nằm ở việc **Team B (Người dùng)** áp đặt những gì họ cần lên Team A.

</details>

1. **REST APIs**: Validating that JSON schemas, HTTP status codes, and headers remain compatible.
2. **Message Brokers (Kafka/RabbitMQ)**: Validating the payload structure of events (e.g., ensuring `OrderCreatedEvent` always contains `totalAmount`).
3. **GraphQL**: Ensuring schema evolution does not break existing mobile app clients.

### Anti-Patterns
- **Using Contract Tests for Business Logic**: Contract tests ONLY check the shape of the data (types, field names). They do not check if `amount = 100` calculates taxes correctly. That is what Unit Tests are for.
- **Provider-Driven Contracts**: If the Provider writes the contracts, they are just testing themselves. The value comes from the *Consumer* dictating what they actually use (Consumer-Driven).

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn tốt nhất**:
1. **Dùng Pact cho hệ thống Đa ngôn ngữ (Polyglot)**: Nếu công ty bạn dùng cả Node.js, Python, và Java, hãy dùng thư viện Pact (pact.io) vì nó hỗ trợ mọi ngôn ngữ.
2. **Dùng Spring Cloud Contract cho hệ thống thuần Java**: Nếu 100% backend là Spring Boot, Spring Cloud Contract tích hợp cực sâu, nó tự động sinh ra các file `.java` (JUnit Test) từ file hợp đồng `.yml`.
3. **Định lý Postel (Bao dung khi làm Consumer)**: Team B chỉ nên viết hợp đồng cho những field MÀ HỌ THỰC SỰ DÙNG. Nếu API trả về 50 trường dữ liệu, nhưng Team B chỉ xài 2 trường, hợp đồng chỉ được phép test 2 trường đó. Việc này giúp Team A thoải mái sửa đổi 48 trường kia mà không làm fail test của Team B.

**Cạm bẫy**:
1. **Viết quá nhiều test**: Đừng viết Contract để ép Team A trả về lỗi 400, 401, 403, 404 cho mọi ngóc ngách. Chỉ test những mã lỗi mà code của Team B thực sự có dòng `if/else` để xử lý.
2. **Bỏ quên Trạng thái dữ liệu (Provider State)**: Hợp đồng ghi "Khi tôi xin User ID 1, hãy trả về tên John". Team A chạy test bị fail vì trong Database ảo của họ lúc chạy test KHÔNG CÓ user nào ID 1. Team A bắt buộc phải thiết lập Mock Data (Provider State) trước khi chạy contract test.

</details>

### Best Practices
1. **Use Pact for Polyglot Environments**: If you have Node.js, Python, and Java services, use Pact (pact.io) because it is language-agnostic.
2. **Use Spring Cloud Contract for Java-only**: If your entire backend is Spring Boot, Spring Cloud Contract is deeply integrated and generates actual JUnit tests automatically from Groovy/YAML contracts.
3. **Integrate with CI/CD (Pact Broker/Can I Deploy)**: Use a contract broker. Before a service deploys, it must run `pact-broker can-i-deploy --name UserService --version 1.0.0 --to prod`. The broker checks if all contracts are satisfied. If yes, it deploys.
4. **Be tolerant in Consumers (Postel's Law)**: Consumers should only write contracts for the fields they *actually use*. If an API returns 50 fields, but the consumer only uses 2, the contract should only assert those 2 fields. This allows the provider to change the other 48 fields freely without breaking the contract.

### Common Pitfalls
1. **Writing too many contract tests**: Testing every single HTTP error code (400, 401, 403, 404) for every endpoint creates massive overhead. Only test what the consumer actually has conditional logic to handle.
2. **Ignoring Provider State**: If a contract says "When I request User ID 1, return Name: John", the provider test must inject "User ID 1" into the mock database before running the test. Managing these "Provider States" can become tedious if the data is complex.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là file Hợp đồng `.yml` do Team B viết. Nó không yêu cầu giá trị chính xác là "1" (vì data ảo thường thay đổi), nó dùng Regular Expression (`[0-9]+`) để chỉ yêu cầu "miễn là 1 con số là được".
Bên dưới là file JUnit Test được tự động sinh ra bên phía code của Team A dựa trên bản hợp đồng đó. Team A chỉ việc cung cấp hàm `setup()` để giả lập (Mock) dữ liệu cho bài test.

</details>

### Spring Cloud Contract (YAML Definition)

This contract is written by the **Consumer** (Billing Service) but runs in the **Provider's** (User Service) codebase.

```yaml
# src/test/resources/contracts/shouldReturnUserById.yml
request:
  method: GET
  url: /api/users/1
response:
  status: 200
  headers:
    Content-Type: application/json
  body:
    id: 1
    firstName: "John"  # The consumer specifically needs this field
    isActive: true
  matchers:
    body:
      - path: $.id
        type: by_regex
        value: "[0-9]+" # Assert it's a number, not the exact value '1'
      - path: $.firstName
        type: by_type   # Assert it's a String
      - path: $.isActive
        type: by_type   # Assert it's a Boolean
```

### Auto-generated Provider Test (Spring Cloud Contract)

When the Provider (User Service) runs `mvn clean test`, the plugin automatically generates a JUnit test from the YAML above:

```java
import io.restassured.module.mockmvc.RestAssuredMockMvc;
import org.junit.jupiter.api.BeforeEach;

// The Base class sets up the Provider State (Mocking the DB or Service layer)
public class ContractTestBase {

    @Autowired
    UserController userController;

    @MockBean
    UserService userService;

    @BeforeEach
    public void setup() {
        // Setup Provider State
        User mockUser = new User(1L, "John", "Doe", true);
        Mockito.when(userService.findById(1L)).thenReturn(mockUser);
        
        RestAssuredMockMvc.standaloneSetup(userController);
    }
}
```

---

## Related Topics

- [API Layer Design](../01-advanced-api-design/idempotency-and-rate-limiting.md) — The APIs that these contracts protect.
- [Transactional Outbox Pattern](../04-distributed-async/transactional-outbox-pattern.md) — Contract testing applies to async messaging just as much as synchronous REST APIs.
- [CI/CD & Deployment](../../06-build-tools/frontend-ci-cd.md) — Where the "Can I Deploy" contract checks are executed.
