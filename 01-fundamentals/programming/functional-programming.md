# Functional Programming

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Functional Programming (FP) là một phong cách lập trình coi mọi thứ như các hàm toán học. Nó tránh việc thay đổi dữ liệu (Immutability) và các hiệu ứng phụ (Side effects). Kết hợp OOP và FP sẽ tạo ra thứ code bất khả chiến bại.

</details>

> **Summary**: Functional Programming (FP) is a programming paradigm that treats computation as the evaluation of mathematical functions. It strictly avoids mutating state (Immutability) and side effects. Combining Object-Oriented Programming (OOP) architectures with FP logic yields exceptionally robust systems.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang làm món sinh tố dưa hấu.
- **Phong cách thường (Imperative / OOP)**: Lấy dưa hấu, dùng dao gọt vỏ, lấy ruột dưa cho vào máy xay. Bấm nút. Sau đó bạn có một ly sinh tố. Vấn đề là: Quả dưa hấu ban đầu **đã bị phá nát và biến mất**.
- **Phong cách Lập trình hàm (Functional Programming)**: Bạn bỏ quả dưa hấu vào cỗ máy ma thuật. Cỗ máy nhả ra một ly sinh tố dưa hấu, **nhưng quả dưa hấu ban đầu vẫn còn nguyên vẹn!** 

Trong FP, bạn không bao giờ phá hủy hay sửa đổi dữ liệu gốc (gọi là *Immutability* - tính bất biến). Và các Cỗ máy ma thuật (Functions) cứ ném cái gì vào thì chắc chắn trả ra cái đó, không bao giờ tự ý làm cháy cầu chì nhà bạn (gọi là *Pure Function* - Hàm thuần khiết).

</details>

Imagine you are making a watermelon smoothie.
- **Imperative / OOP Style**: You take a watermelon, use a knife to peel it, extract the fruit, and place it into a blender. You press the button, and you receive a smoothie. The caveat: the original watermelon has been **destroyed and no longer exists**.
- **Functional Programming Style**: You place the watermelon into a magical machine. The machine produces a watermelon smoothie, **but the original watermelon remains completely intact and unchanged!**

In FP, you never destroy or modify the original data (this is called *Immutability*). Furthermore, the magical machines (Functions) guarantee that if you input the exact same item, they will return the exact same result without unexpectedly short-circuiting your house's electrical grid (this is called a *Pure Function*).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Functional Programming (FP)** là một hệ tư tưởng lập trình được xây dựng trên 3 khái niệm cốt lõi:
1. **Pure Functions (Hàm thuần khiết)**: Giống như phép toán `1 + 1 = 2`. Dù bạn tính 1 triệu lần thì nó vẫn ra 2, và nó không làm ảnh hưởng đến bất cứ thứ gì khác trên thế giới.
2. **Immutability (Bất biến)**: Dữ liệu một khi đã sinh ra thì không bao giờ bị thay đổi. Nếu muốn thay đổi, hãy tạo ra một bản sao mới.
3. **Declarative (Khai báo)**: Quan tâm đến việc "Tôi muốn cái gì?" (What) thay vì "Làm việc đó từng bước như thế nào?" (How).

</details>

**Functional Programming (FP)** is a declarative programming paradigm constructed upon three core concepts:
1. **Pure Functions**: Similar to the mathematical equation `1 + 1 = 2`. Calculating it a million times will always yield `2`, and the calculation process does not alter anything else in the universe.
2. **Immutability**: Once data is instantiated, its state cannot be modified after it is created. If a modification is required, a completely new copy must be generated.
3. **Declarative Style**: Focuses on "What do I want to achieve?" rather than dictating the control flow step-by-step ("How to achieve it?").

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao lại phải đẻ ra cái phong cách rắc rối không cho sửa dữ liệu này?

| Vấn đề khi cho phép sửa dữ liệu | FP giải quyết |
|---|---|
| **Lỗi do dùng chung**: Biến `A` dùng chung cho 10 class. Class 1 sửa biến `A`, 9 class kia sập. | **Immutability**: Dữ liệu không bao giờ bị sửa. Ai muốn sửa thì tự tạo bản copy mà chơi. |
| **Hàm chạy loạn xạ**: Hàm tính tiền nhưng lại ngầm kết nối database, chạy lúc được lúc không. | **Pure Functions**: Hàm tính tiền CHỈ TÍNH TIỀN. Chạy 1 tỷ lần cũng ra kết quả y hệt. |
| **Xử lý đa luồng (Multi-threading)**: 10 luồng cùng tranh nhau sửa 1 biến gây ra lỗi Race Condition. | Vì không ai sửa được dữ liệu, 10 hay 100 luồng chạy cùng lúc cũng không bao giờ lỗi! |

</details>

Why enforce a paradigm that prohibits modifying variables?

| Problem with Mutable State | FP Solution |
|---|---|
| **Shared State Mutations**: Variable `A` is shared among 10 classes. Class 1 modifies variable `A`, causing the other 9 classes to crash unpredictably. | **Immutability**: Data is never modified in-place. If a component requires altered data, it creates an independent copy. |
| **Unpredictable Side Effects**: A function named `calculateTotal()` secretly establishes a database connection, causing intermittent timeouts. | **Pure Functions**: A calculation function ONLY calculates. It is deterministic and possesses zero side effects. |
| **Concurrency Hazards**: 10 threads attempt to modify a single variable simultaneously, resulting in race conditions and deadlocks. | Because data is immutable, 10 or 10,000 threads can read it concurrently without requiring complex locking mechanisms. |

---

## Layer 3: Without vs. With Comparison (Compare)

### 1. Pure Functions

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**❌ Impure Function (Hàm không thuần khiết - Gây bất ngờ)**
Hàm này mỗi lần gọi ra một kết quả khác nhau, hoặc lén lút sửa đổi dữ liệu bên ngoài.

**✅ Pure Function (Thuần khiết - Luôn đoán trước được)**
Tất cả những gì hàm cần đều được truyền vào qua tham số. Dù tính 1000 năm nữa kết quả vẫn vậy.

</details>

### Without Implementation: Impure Function
This function yields different results based on external state and is unpredictable.
```python
tax_rate = 0.1

# Call 1: calculate_price(100) -> 110
# Call 2: An external process alters tax_rate to 0.2 -> calculate_price(100) -> 120 (Unpredictable behavior!)
def calculate_price(price):
    return price * (1 + tax_rate) 
```

### With Implementation: Pure Function
All required dependencies are explicitly passed as parameters.
**Python:**
```python
def calculate_price(price, tax):
    return price * (1 + tax)
# Deterministic guarantee: calculate_price(100, 0.1) will ALWAYS yield 110.
```

**Java:**
```java
public class Calculator {
    // Static methods acting purely on parameters are excellent candidates for Pure Functions
    public static double calculatePrice(double price, double tax) {
        return price * (1 + tax);
    }
}
```

---

### 2. Immutability

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**❌ Mutable (Dữ liệu bị phá hỏng)**
Nếu dùng `.add()`, danh sách gốc đã bị thay đổi!

**✅ Immutable (Tạo bản sao mới)**
Tạo một tuple (Python) hoặc List.of() (Java). Bất cứ hành động sửa đổi nào cũng tạo ra một List mới, thay vì làm hỏng List cũ.

</details>

### Without Implementation: Mutable State
```java
List<String> names = new ArrayList<>(List.of("Alice", "Bob"));
names.add("Charlie"); // The original list has been permanently mutated!
```

### With Implementation: Immutable State
**Python:**
```python
names = ("Alice", "Bob") # Tuples enforce immutability in Python
# names[0] = "John" -> Immediately throws a TypeError!

# A completely new tuple must be generated
new_names = names + ("Charlie",) 
```

**Java:**
```java
// List.of() generates an Immutable Collection
List<String> names = List.of("Alice", "Bob");

// Generate a new list by concatenating the old list with new elements
List<String> newNames = Stream.concat(names.stream(), Stream.of("Charlie")).toList();
```

---

### 3. Declarative Processing: Map, Filter, Reduce

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thay vì dùng vòng lặp `for` (mệnh lệnh - nói máy tính làm từng bước), FP sử dụng các hàm bậc cao (Higher-Order Functions) như Map, Filter, Reduce để khai báo cái mình muốn.

**Bài toán:** Bạn có danh sách User. Hãy tìm *Email* của những user *trên 18 tuổi*, và viết *in hoa*.

</details>

Instead of utilizing imperative `for` loops that dictate step-by-step execution, FP utilizes Higher-Order Functions (Map, Filter, Reduce) to declare intent.

**Scenario:** Given a list of Users, extract the *emails* of users *over 18 years old*, and convert them to *uppercase*.

### Without Implementation: Imperative Loops
```java
List<String> result = new ArrayList<>();
for (User u : users) {
    if (u.getAge() > 18) {
        result.add(u.getEmail().toUpperCase());
    }
}
```

### With Implementation: Declarative Functional Pipeline

**Python:**
```python
# Utilizing map and filter
adult_emails = list(
    map(lambda u: u.email.upper(), 
        filter(lambda u: u.age > 18, users))
)

# Alternatively, utilizing Pythonic List Comprehensions (A highly declarative approach)
adult_emails = [u.email.upper() for u in users if u.age > 18]
```

**Java:**
```java
List<String> adultEmails = users.stream()
    .filter(u -> u.getAge() > 18)        // FILTER: Age > 18
    .map(User::getEmail)                 // MAP: Extract email attribute
    .map(String::toUpperCase)            // MAP: Transform to uppercase
    .toList();                           // TERMINAL: Collect into a new list
```

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Data Engineering**: Xử lý hàng triệu dòng dữ liệu (Hadoop, Spark hoàn toàn dựa trên khái niệm Map-Reduce của FP).
- **ReactJS**: React Hooks và Redux sử dụng Immutability để biết chính xác khi nào cần cập nhật giao diện (Mọi State đều là bất biến).
- **Multi-threading (Đa luồng)**: Vì biến không thể sửa được, bạn có thể chạy 100 luồng cùng lúc mà không sợ chúng dẫm đạp lên nhau gây chết chương trình.

</details>

- **Data Engineering & Big Data**: Processing millions of data rows. Distributed processing frameworks like Hadoop and Apache Spark are fundamentally built upon the FP Map-Reduce paradigm.
- **Frontend State Management**: ReactJS Hooks and Redux enforce immutability to accurately track state changes and trigger efficient UI re-renders.
- **Highly Concurrent Systems**: Because immutable variables cannot be altered, developers can execute thousands of concurrent threads without the risk of race conditions or the performance overhead of mutex locks.

---

## Layer 5: Deep Practice

### The Optimal Hybrid: OOP + FP

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn không cần phải vứt bỏ OOP để dùng FP. Các ngôn ngữ hiện đại (Java, Python, TS, Kotlin) khuyến khích dùng cả hai:
- Dùng **OOP** để thiết kế Cấu trúc hệ thống (Classes, Interfaces, Dependency Injection).
- Dùng **FP** bên trong ruột các Hàm để xử lý logic, tính toán dữ liệu (Streams, Lambdas).

</details>

You do not need to abandon OOP to leverage FP. Modern programming languages (Java, Python, TypeScript, Kotlin, C#) actively encourage a hybrid approach:
- Utilize **OOP** to architect system structures (Classes, Interfaces, Dependency Injection, and Boundaries).
- Utilize **FP** within the internal logic of methods to process data securely and deterministically (Streams, Lambdas, and Immutability).

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **FP quá đà**: Bắt ép mọi thứ phải Functional dẫn đến code dài ngoằng và khó đọc. Nếu một vòng lặp `for` 3 dòng dễ hiểu hơn một chuỗi `map.reduce.filter` rối rắm, hãy dùng `for`.
2. **Hiệu năng (Performance)**: Tạo ra quá nhiều Object mới (do Immutability) có thể làm đầy bộ nhớ (RAM) và bắt Garbage Collector chạy liên tục. Ở các phần mềm yêu cầu hiệu năng siêu cao (như lập trình Game), người ta vẫn chuộng Mutable data.

</details>

1. **Dogmatic Functional Extremism**: Forcing functional paradigms where they do not fit can lead to cryptic, unreadable code. If a three-line `for` loop is significantly easier to comprehend than a deeply nested `map.reduce.filter` chain, prioritize readability and use the loop.
2. **Performance Degradation (Garbage Collection Overhead)**: Strictly adhering to immutability requires instantiating new objects for every state change. In highly constrained environments or ultra-high-performance applications (e.g., AAA Game Engines or High-Frequency Trading systems), this constant allocation overburdens the Garbage Collector. In such niche scenarios, mutable data structures remain necessary.

---

## Related Topics

- **[OOP Principles](./oop-principles.md)** — The architectural counterpart to FP.
- **[Clean Code](./clean-code.md)** — FP naturally enforces the creation of smaller, highly testable, and cleanly isolated functions.
