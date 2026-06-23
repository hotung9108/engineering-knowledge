# Mocking, Stubbing, and Test Doubles

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Để test một hàm (Unit Test) chạy cực nhanh và không bị lỗi vặt do rớt mạng, bạn phải cô lập hoàn toàn hàm đó khỏi thế giới bên ngoài (Database, API, File System). **Test Doubles** (Diễn viên đóng thế) là các kỹ thuật làm giả lập các phụ thuộc bên ngoài này. Hiểu rõ sự khác biệt giữa Dummy, Stub, Spy, và Mock giúp bạn viết ra những Unit Test độc lập và vững chãi.

</details>

> **Summary**: True Unit Testing mandates absolute isolation. A function under test must be severed from external, unpredictable, or slow dependencies like Databases, Network APIs, and the File System. **Test Doubles** (Stunt doubles for code) are objects instantiated to simulate these external dependencies. Mastering the nuances between Dummies, Stubs, Spies, and Mocks empowers engineers to write deterministic, blazing-fast test suites.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang đạo diễn một bộ phim hành động. Nam chính (Hàm của bạn) cần một cảnh đánh nhau trên máy bay (Database).
- Không thể nào thuê hẳn một cái máy bay thật chỉ để tập diễn (quá đắt, quá chậm). 
- Vì vậy, bạn thuê một **Diễn viên đóng thế (Test Double)**. Bạn dựng một cái mô hình máy bay bằng bìa các-tông trong studio.
- **Stub (Kịch bản tĩnh)**: Bạn bảo cái máy bay các-tông: "Cứ mỗi lần nam chính mở cửa, mày phát ra tiếng xì hơi nhé". Không quan trọng nam chính làm gì, nó luôn trả về 1 kết quả cố định.
- **Mock (Kịch bản tương tác)**: Bạn lắp camera quanh máy bay các-tông để theo dõi hành động của nam chính: "Nam chính có đấm vỡ kính đúng 3 lần không?". Nếu đấm thiếu 1 lần, đạo diễn hô CẮT (Test Fails).

</details>

Imagine you are directing an action movie. The Lead Actor (The Function Under Test) needs to film a fight scene inside a flying airplane (The Production Database).
- You cannot rent a real Boeing 747 just for a rehearsal (it is too expensive and slow).
- Therefore, you use a **Test Double (A Stunt Double / Movie Set)**. You build a cardboard airplane inside the studio.
- **Stub (Pre-programmed behavior)**: You rig the cardboard door: "Whenever the actor opens this door, play a generic wind sound effect." It blindly returns a hardcoded response regardless of context.
- **Mock (Interactive surveillance)**: You place hidden cameras inside the cardboard plane to strictly monitor the actor. "Did the actor punch the window *exactly* three times?" If the actor only punches twice, the Director yells CUT (The Test Fails).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Theo định nghĩa của Martin Fowler, có 4 loại "Diễn viên đóng thế" chính (Test Doubles):
1. **Dummy**: Đưa vào hàm cho đủ tham số chứ không bao giờ được dùng đến.
2. **Stub**: Trả về dữ liệu cứng (hardcoded) để phục vụ cho luồng chạy của hàm. (VD: "Nếu gọi hàm get() thì luôn trả về số 5").
3. **Spy**: Giống Stub, nhưng nó bí mật ghi chép lại xem nó đã được gọi mấy lần, gọi với tham số gì.
4. **Mock**: Giống Spy nhưng xịn hơn. Nó mang theo sự Kỳ vọng (Expectations). Nếu hàm của bạn KHÔNG gọi cái Mock này đúng số lần quy định, Test sẽ tự động Fail ngay lập tức.

</details>

According to Martin Fowler, there are distinct classifications of "Test Doubles" (often lazily, and incorrectly, grouped together as "Mocks"):
1. **Dummy**: Objects passed around solely to satisfy compiler/parameter requirements. Their internal methods are never actually invoked.
2. **Stub**: Objects providing canned, hardcoded answers to calls made during the test. They do not respond to anything outside what they are explicitly programmed for (State-based testing).
3. **Spy**: Stubs that secretly record information based on how they were called. (e.g., An email service spy might record how many messages it "sent").
4. **Mock**: Objects pre-programmed with explicit *Expectations*. They form a specification of the calls they are expected to receive. If the function under test fails to call the mock appropriately, the Mock itself fails the test (Behavior-based testing).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề của Unit Test**: 
Bạn muốn test hàm `Checkout`. Hàm này gọi xuống lớp `Database` để trừ tiền, rồi gọi sang lớp `EmailService` qua mạng để gửi hóa đơn. Nếu chạy test này:
1. Nó mất 3 giây (Vì dính mạng). Unit test phải chạy trong 1ms.
2. Nếu mạng rớt, Test báo Fail. Trong khi thực chất logic hàm `Checkout` của bạn không hề sai! Đây gọi là **Flaky Test** (Test chập chờn).

**Giải pháp**: Cắt đứt toàn bộ xúc tu của hàm `Checkout`. Thay cái `Database` thật bằng một cái Mock. Thay `EmailService` bằng một cái Spy. Bây giờ test chạy siêu nhanh, và chỉ Fail khi logic tính tiền của bạn sai.

</details>

**The Unit Testing Dilemma**: 
You need to test a `CheckoutService.processOrder()` method. Internally, this method executes a SQL query via `UserRepository` and sends a network HTTP call via `EmailService`.
If you execute this test directly:
1. **Latency**: It takes 3 seconds (network delay). A healthy CI/CD pipeline requires 5,000 unit tests to execute in 5 seconds.
2. **Non-Determinism (Flaky Tests)**: If the third-party Email API is temporarily down, your test fails. However, your `CheckoutService` business logic is structurally perfect! False negatives destroy developer trust in the test suite.

**The Test Double Solution**: Sever the tentacles. Inject a Mock `UserRepository` and a Stub `EmailService` into the `CheckoutService`. The test now executes entirely in RAM in 0.1 milliseconds, completely immune to internet outages.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt rõ nét nhất giữa Stub (Chỉ test trạng thái/kết quả) và Mock (Test hành vi tương tác).
</details>

The critical architectural difference lies between **Stubbing** (State-verification) and **Mocking** (Behavior-verification).

### State Verification (Using a Stub)
You assert against the final Output/State. You don't care *how* it got there.
**Java / Mockito:**
```java
// We STUB the repository to return a canned answer
when(userRepository.findById(1)).thenReturn(new User("John"));

String name = userService.getUserName(1);

// We verify the STATE (the output)
assertEquals("John", name); 
```

### Behavior Verification (Using a Mock)
You assert against the Interaction. You verify that your code correctly commanded a dependency.
**Java / Mockito:**
```java
userService.deleteUser(1);

// We verify the BEHAVIOR. Did the service actually call delete() on the database?
// If it didn't call it exactly 1 time, the test FAILS.
verify(userRepository, times(1)).deleteById(1);
```

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Dùng Stub**: Khi bạn cần giả lập một truy vấn lấy dữ liệu từ Database. Ví dụ: Cứ gọi hàm `findProduct()` là trả về Object Cái Áo 100k.
- **Dùng Mock/Spy**: Khi hàm của bạn gọi ra một hệ thống khác mà KHÔNG nhận lại kết quả. Ví dụ: Hàm `sendEmail()`. Bạn không thể bắt kết quả trả về, bạn chỉ có thể "theo dõi" (Mock) xem hàm `sendEmail()` có thực sự được gọi (triggered) hay chưa.
- **Dùng Dummy**: Các tham số rác. Hàm tạo User cần `name`, `age`, `address`. Bạn chỉ muốn test logic tuổi `age`, thì `name` và `address` cứ quăng đại chữ "A" vào (Làm Dummy).

</details>

- **Stub Use Cases**: Simulating Data Retrieval. Bypassing slow SQL `SELECT` queries or HTTP `GET` requests. (e.g., Forcing a weather API stub to immediately return `{ "temp": 20 }` so you can test your app's UI rendering logic).
- **Mock/Spy Use Cases**: Simulating Data Mutators (Fire-and-Forget actions). If your code calls an external notification service (SMS/Email) or logs an event, there is no state returned to assert against. You *must* use a Mock to verify that the interaction successfully occurred (e.g., Asserting that `logger.error()` was invoked exactly once with specific parameters).
- **Dummy Use Cases**: Satisfying strict constructors. If a function requires a `PaymentConfig` object, but your current test only analyzes the `UserAccount` object, pass `null` or an empty `new PaymentConfig()` as a Dummy.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dependency Injection (DI)**: Bạn không thể Mock nếu code của bạn tạo Object bằng từ khóa `new` chìm sâu bên trong hàm. Hãy truyền các service vào qua Constructor. Đây là lý do Spring Boot/NestJS sinh ra DI container. Không có DI, code không thể test được.
2. **Chỉ Mock những thứ thuộc về bạn**: Đừng bao giờ Mock các thư viện bên thứ 3 (Ví dụ: Mock thư viện `axios` hay `KafkaProducer`). Nếu thư viện nâng cấp và đổi cách hoạt động, Mock của bạn vẫn Pass nhưng code chạy thật thì nổ tung. Hãy bọc thư viện đó vào một class Wrapper của bạn, rồi Mock cái Wrapper đó.

</details>

1. **Mandatory Dependency Injection (DI)**: You cannot physically inject a Mock object if your function heavily utilizes tight coupling (e.g., instantiating objects explicitly with the `new` keyword inside the method body). Dependencies must be injected via constructors. This is why DI Frameworks (Spring, NestJS, Angular) are deeply intertwined with TDD.
2. **Don't Mock What You Don't Own**: Never directly mock third-party external libraries or complex SDKs (e.g., directly mocking the `AWS DynamoDB Client` or `axios`). If the third party updates their SDK and alters behavior, your mock will still happily pass, resulting in a false positive that crashes in production. Instead, create a thin, custom Wrapper/Adapter class (Facade Pattern) around the library, and mock your *own* wrapper.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Mock quá liều (Over-mocking)**: Bạn mock MỌI hàm bên trong một class. Cuối cùng, cái Unit test của bạn chẳng test logic gì cả, nó chỉ kiểm tra xem bạn cấu hình cái thư viện Mockito có đúng không. Code bị dính chặt với Implementation, refactor một cái là 100 cái Test đỏ lòm.
2. **Quên verify Mock**: Cấu hình Mock cho vui nhưng ở cuối bài test lại không có lệnh `verify(...)`. Dẫn đến việc code chả làm gì nhưng test vẫn Pass.

</details>

1. **Over-mocking (Mockist Anti-pattern)**: Aggressively mocking every single internal method interaction within the same layer. The test stops verifying Business Logic and merely verifies the structural implementation of the Mocking framework itself. When you attempt to refactor the code to be cleaner, 50 tests shatter violently because the internal interaction chain changed.
2. **Ghost Stubs / Unverified Mocks**: Setting up complex `when().thenReturn()` stubs, but the production code never actually calls them due to an `if` statement bug. If the test lacks assertion or `verify()` checks, it will pass silently, hiding massive logic failures.

---

## Related Topics

- Discover how Mocking enables writing tests before code in **[TDD & BDD](./tdd-bdd.md)**.
- See where Mock-heavy tests sit structurally in the **[Testing Pyramid](./testing-pyramid.md)**.
- For managing dependencies to allow mocking, see **[SOLID Principles](../computer-science/solid-principles.md)** (Dependency Inversion).
