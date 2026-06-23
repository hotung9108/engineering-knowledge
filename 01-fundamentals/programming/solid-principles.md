# SOLID Principles

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: SOLID là 5 nguyên tắc thiết kế hướng đối tượng giúp code dễ bảo trì, dễ mở rộng và ít lỗi. Nó là kim chỉ nam cho mọi Software Engineer khi thiết kế Class và hệ thống.

</details>

> **Summary**: SOLID represents five object-oriented design principles intended to make software designs more understandable, flexible, and maintainable. These principles serve as foundational guidelines for software engineers when designing classes and architectural systems.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Để hiểu SOLID, hãy tưởng tượng bạn đang chế tạo các công cụ trong xưởng cơ khí:

1. **S - Single Responsibility (Đơn nhiệm)**: Cái thìa dùng để múc canh, cái dĩa dùng để xiên thịt. Đừng chế tạo một "Cái thìa có răng cưa ở viền" để làm cả hai. Rất khó dùng và dễ đứt miệng! Trong code: *Mỗi class chỉ làm ĐÚNG MỘT VIỆC.*
2. **O - Open/Closed (Mở/Đóng)**: Khi điện thoại hết dung lượng, bạn cắm thêm thẻ nhớ (Mở rộng). Bạn không cần phải tháo tung máy ra, cắt vi mạch để hàn thêm chip nhớ (Sửa đổi). Trong code: *Dễ dàng thêm tính năng mới mà KHÔNG cần sửa code cũ.*
3. **L - Liskov Substitution (Thay thế Liskov)**: Con vịt đồ chơi không thể thay thế con vịt thật. Mặc dù cả 2 đều là vịt, nhưng vịt đồ chơi không biết đẻ trứng. Nếu bạn cố ép vịt đồ chơi đẻ trứng, hệ thống sẽ sập. Trong code: *Class con phải thay thế được Class cha mà không làm hỏng chương trình.*
4. **I - Interface Segregation (Phân tách Giao diện)**: Đừng bán cho khách hàng chiếc xe đạp có gắn thêm... đồng hồ báo xăng. Họ đâu có cần! Trong code: *Đừng bắt một Class phải chứa những hàm mà nó không bao giờ xài tới. Hãy chia nhỏ ra.*
5. **D - Dependency Inversion (Đảo ngược Phụ thuộc)**: Khi mua quạt máy, bạn cắm nó vào **Ổ cắm điện trên tường**. Bạn không hàn trực tiếp dây quạt vào **đường dây điện ngầm**. Trong code: *Các hệ thống nên kết nối với nhau qua ổ cắm (Interface/Abstraction), thay vì hàn chết vào nhau.*

</details>

To comprehend SOLID, imagine you are building tools in a mechanical workshop:

1. **S - Single Responsibility**: A spoon is designed for scooping soup; a fork is designed for spearing meat. Do not manufacture a "spoon with serrated edges" to accomplish both tasks. It will be difficult to use and may cause injury. In code: *Each class should do exactly one thing.*
2. **O - Open/Closed**: When a smartphone runs out of storage, you insert an external memory card (Extension). You do not dismantle the device and solder a new memory chip onto the motherboard (Modification). In code: *Systems should be easy to extend with new features without altering existing, working code.*
3. **L - Liskov Substitution**: A plastic toy duck cannot replace a real duck. Even though both are classified as "ducks", a toy duck cannot lay eggs. If a system expects an egg and receives a toy duck, the system will crash. In code: *Child classes must be perfectly substitutable for their parent classes without breaking the application logic.*
4. **I - Interface Segregation**: Do not sell a bicycle equipped with a fuel gauge to a customer. They do not need it. In code: *Do not force a class to implement functions it will never use. Break large interfaces into smaller, specific ones.*
5. **D - Dependency Inversion**: When you purchase a fan, you plug it into a standard **wall outlet**. You do not solder the fan's wires directly into the **hidden electrical grid** inside the wall. In code: *High-level systems should connect to low-level systems via standard interfaces (outlets), rather than being tightly coupled.*

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**SOLID** là viết tắt của 5 nguyên tắc thiết kế trong Object-Oriented Programming (OOP) do Robert C. Martin (Uncle Bob) giới thiệu.

| Chữ cái | Tên nguyên tắc | Dịch nghĩa |
|---|---|---|
| **S** | Single Responsibility Principle | Nguyên tắc Đơn trách nhiệm |
| **O** | Open/Closed Principle | Nguyên tắc Đóng / Mở |
| **L** | Liskov Substitution Principle | Nguyên tắc Thay thế Liskov |
| **I** | Interface Segregation Principle | Nguyên tắc Phân tách Giao diện |
| **D** | Dependency Inversion Principle | Nguyên tắc Đảo ngược Phụ thuộc |

</details>

**SOLID** is an acronym for five design principles in Object-Oriented Programming (OOP) introduced by Robert C. Martin (Uncle Bob).

| Letter | Principle Name | Definition |
|---|---|---|
| **S** | Single Responsibility Principle | A class should have one, and only one, reason to change. |
| **O** | Open/Closed Principle | Software entities should be open for extension, but closed for modification. |
| **L** | Liskov Substitution Principle | Objects in a program should be replaceable with instances of their subtypes without altering the correctness of the program. |
| **I** | Interface Segregation Principle | Many client-specific interfaces are better than one general-purpose interface. |
| **D** | Dependency Inversion Principle | Depend upon abstractions, not concretions. |

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu bạn bỏ qua SOLID, code của bạn khi dự án lớn lên sẽ gặp "Bộ ba thảm họa":
- **Rigid (Cứng nhắc)**: Sửa tính năng A, tự nhiên tính năng B lăn ra chết.
- **Fragile (Dễ vỡ)**: Đụng đâu lỗi đó.
- **Immobile (Chết dính)**: Viết được một tính năng hay ở dự án này, nhưng không thể copy sang dự án khác xài lại vì nó dính líu đến quá nhiều thứ.

SOLID sinh ra để giúp code **mềm dẻo, dễ tháo lắp như Lego.**

</details>

Ignoring SOLID principles typically leads to three major architectural flaws as a project scales:
- **Rigidity**: Modifying feature A unexpectedly breaks feature B.
- **Fragility**: The system breaks in multiple places every time a change is made.
- **Immobility**: A useful component in one project cannot be reused in another because it is hopelessly entangled with its current environment.

SOLID exists to ensure code remains **flexible, robust, and highly modular.**

---

## Layer 3: Without vs. With Comparison (Compare)

### 1. S - Single Responsibility Principle (SRP)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Mỗi class chỉ nên có MỘT lý do để thay đổi.**

**❌ Vi phạm SRP: 1 Class ôm đồm mọi việc**
*Lỗi:* Nếu đổi từ SQL sang MongoDB → Phải sửa file này. Nếu đổi Email sang Slack → Cũng sửa file này. 1 file có quá nhiều lý do để bị sửa.

</details>

> **A class should have one, and only one, reason to change.**

### Without Implementation: The God Class
```python
class ReportManager:
    def __init__(self, data):
        self.data = data
        
    def generate_report(self):
        print("Generating report...")
        
    def save_to_database(self):
        print("Saving to SQL database...")
        
    def send_email(self):
        print("Sending email to manager...")
```
*Issue:* If the storage mechanism changes from SQL to MongoDB, this file must be modified. If the notification system changes from Email to Slack, this file must be modified. This single class has too many reasons to change.

### With Implementation: Divide and Conquer
**Python:**
```python
class ReportGenerator:
    def generate(self, data): print("Generating report...")

class ReportRepository:
    def save(self, report): print("Saving to database...")

class ReportNotifier:
    def send(self, report): print("Sending notification...")
```

**Java:**
```java
// Separated into three distinct classes, each with a single responsibility.
public class ReportGenerator {
    public Report generate(Data data) { return new Report(); }
}
public class ReportRepository {
    public void save(Report report) { /* Database persistence logic */ }
}
public class EmailNotifier {
    public void send(Report report) { /* Email transmission logic */ }
}
```

---

### 2. O - Open/Closed Principle (OCP)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Phần mềm phải MỞ để mở rộng (thêm tính năng), nhưng ĐÓNG đối với việc sửa đổi (không sửa code cũ).**

**❌ Vi phạm OCP: Dùng IF-ELSE bừa bãi**
*Lỗi:* Nếu có thêm khách hàng VVIP, ta lại phải chui vào sửa đống `if-else` cũ. Dễ sinh lỗi!

**✅ Tuân thủ OCP: Dùng Đa hình (Polymorphism) / Strategy Pattern**
Thêm khách hàng VVIP siêu dễ, chỉ cần TẠO CLASS MỚI, KHÔNG SỬA CODE CŨ!

</details>

> **Software entities should be open for extension, but closed for modification.**

### Without Implementation: Rampant IF-ELSE statements
```python
class DiscountCalculator:
    def calculate(self, customer_type, price):
        if customer_type == "NORMAL": return price
        elif customer_type == "VIP": return price * 0.8
        # Adding a new customer type (e.g., VVIP) requires modifying this existing logic. This is error-prone.
```

### With Implementation: Polymorphism / Strategy Pattern
**Python:**
```python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, price): pass

class NormalDiscount(DiscountStrategy):
    def calculate(self, price): return price

class VipDiscount(DiscountStrategy):
    def calculate(self, price): return price * 0.8

# Adding a VVIP tier is trivial: simply create a NEW CLASS without modifying existing code.
class VvipDiscount(DiscountStrategy):
    def calculate(self, price): return price * 0.5

class Calculator:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy
        
    def get_price(self, price):
        return self.strategy.calculate(price)
```

**Java:**
```java
interface Discount { double calculate(double price); }

class VipDiscount implements Discount {
    public double calculate(double price) { return price * 0.8; }
}

class Calculator {
    public double getPrice(double price, Discount discount) {
        return discount.calculate(price);
    }
}
```

---

### 3. L - Liskov Substitution Principle (LSP)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Class con phải thay thế được Class cha mà không làm hỏng logic của chương trình.**

**❌ Vi phạm LSP: Ép buộc vô lý**
Hình vuông có phải là Hình chữ nhật không? Trong toán học thì CÓ. Nhưng trong lập trình thì KHÔNG! Nếu cho Hình vuông kế thừa Hình chữ nhật, hàm đổi chiều rộng `width` sẽ vô tình làm đổi luôn cả chiều cao `height` của Hình vuông, gây sai kết quả diện tích.

**✅ Tuân thủ LSP: Thiết kế lại Abstraction**
Hãy dùng chung một Interface `Shape`, và đừng cho Hình vuông kế thừa Hình chữ nhật nữa.

</details>

> **Child classes must be able to replace their parent classes without breaking the program.**

### Without Implementation: Forced Relationships
Is a Square a Rectangle? In mathematics, YES. In object-oriented programming, often NO.
```python
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def get_area(self): return self.width * self.height

class Square(Rectangle):
    # A square must have equal sides
    def set_width(self, w):
        self.width = w
        self.height = w  # Unexpectedly modifies height!
    def set_height(self, h):
        self.width = h
        self.height = h

# Execution
rect = Square()
rect.set_width(5)
rect.set_height(4)
print(rect.get_area()) # Outputs 16 (4x4), but the user expects 20 (5x4). This violates LSP.
```

### With Implementation: Redesign the Abstraction
Utilize a common `Shape` interface, and remove the flawed inheritance relationship between Square and Rectangle.

**Python:**
```python
class Shape(ABC):
    @abstractmethod
    def get_area(self): pass

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def get_area(self): return self.w * self.h

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def get_area(self): return self.side * self.side
```

---

### 4. I - Interface Segregation Principle (ISP)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Đừng bắt các Class phải implement (kế thừa) những hàm mà chúng không bao giờ dùng đến.**

**❌ Vi phạm ISP: Interface quá mập (Fat Interface)**
Ép một chiếc máy in rẻ tiền phải implement cả chức năng `scan()` và `fax()`, dẫn đến việc nó phải quăng lỗi `UnsupportedOperationException`.

**✅ Tuân thủ ISP: Chia nhỏ Interface**
Chia thành các interface `Printer`, `Scanner`, `Fax` riêng biệt.

</details>

> **Do not force classes to implement methods they do not use.**

### Without Implementation: The Fat Interface
```java
// A comprehensive multi-function machine interface
interface MultiFunctionMachine {
    void print();
    void scan();
    void fax();
}

// A budget printer lacks scanning and faxing capabilities
class CheapPrinter implements MultiFunctionMachine {
    public void print() { System.out.println("Printing..."); }
    public void scan() { throw new UnsupportedOperationException("Not supported!"); } // Violation
    public void fax() { throw new UnsupportedOperationException("Not supported!"); }  // Violation
}
```

### With Implementation: Interface Segregation
**Java:**
```java
interface Printer { void print(); }
interface Scanner { void scan(); }
interface Fax { void fax(); }

// Premium Machine implements all necessary interfaces
class SuperMachine implements Printer, Scanner, Fax {
    public void print() { /* implementation */ }
    public void scan() { /* implementation */ }
    public void fax() { /* implementation */ }
}

// Budget Machine implements ONLY what it supports
class CheapPrinter implements Printer {
    public void print() { System.out.println("Printing..."); }
}
```

---

### 5. D - Dependency Inversion Principle (DIP)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Module cấp cao không được phụ thuộc vào Module cấp thấp. Cả hai phải phụ thuộc vào Trừu tượng (Abstraction/Interface).**

**❌ Vi phạm DIP: Hàn chết dây điện vào tường**
Nếu Class Service phụ thuộc trực tiếp vào `MySQLDatabase`, sau này đổi sang dùng MongoDB thì phải mở lại Service để sửa.

**✅ Tuân thủ DIP: Cắm qua ổ cắm (Interface)**
Tạo một Interface `Database`. Service chỉ cần nói chuyện với Interface này. Ai thích MySQL hay MongoDB thì cứ cắm vào.

</details>

> **High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.**

### Without Implementation: Tightly Coupled Dependencies
```python
class MySQLDatabase:
    def save(self, data): print("Saving to MySQL")

class ShopService:
    def __init__(self):
        # The Service depends DIRECTLY on the concrete MySQLDatabase
        self.db = MySQLDatabase()
        
    def checkout(self):
        self.db.save("Order #1")
# If the infrastructure migrates to MongoDB, the ShopService class must be rewritten.
```

### With Implementation: Relying on Abstractions
**Python:**
```python
class Database(ABC): # The Abstraction (Interface)
    @abstractmethod
    def save(self, data): pass

class MySQLDatabase(Database): # Concrete Implementation 1
    def save(self, data): print("Saving to MySQL")

class MongoDBDatabase(Database): # Concrete Implementation 2
    def save(self, data): print("Saving to MongoDB")

class ShopService:
    # ShopService depends on the Abstraction, remaining agnostic to the specific database
    def __init__(self, db: Database):
        self.db = db
        
    def checkout(self):
        self.db.save("Order #1")

# Execution
mysql = MySQLDatabase()
shop1 = ShopService(mysql) # Operates with MySQL

mongo = MongoDBDatabase()
shop2 = ShopService(mongo) # Switches to MongoDB without altering ShopService logic!
```

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Khi làm dự án lớn, làm việc nhóm**: SOLID giúp nhiều người code cùng lúc mà không dẫm chân lên nhau (Conflict code).
- **Khi bảo trì hệ thống dài hạn**: Thêm tính năng dễ như cắm thêm USB (OCP).
- **Cảnh báo**: Nếu làm hackathon 2 ngày hoặc script nhỏ, không cần áp dụng. Áp dụng quá mức sẽ dẫn đến **Over-engineering**.

</details>

- **Large-scale Enterprise Projects**: SOLID enables multiple developers to work concurrently without creating merge conflicts or breaking external modules.
- **Long-term System Maintenance**: Adding features becomes as seamless as plugging in a USB device (OCP compliance).

> [!WARNING]
> Do not apply SOLID principles blindly to small, throwaway scripts or rapid prototypes. Over-applying these principles to trivial problems leads to **Over-engineering** and unnecessary complexity.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Để thành thạo SOLID, hãy luôn đặt câu hỏi cho code của mình:
1. **S**: Class này đang làm MẤY việc? (>1 việc -> Tách!).
2. **O**: Sếp yêu cầu thêm loại User mới, mình có phải sửa `if-else` cũ không? (Có -> Thay bằng Strategy).
3. **L**: Hàm này nhận Class Cha, nếu mình ném Class Con vào nó có chạy đúng không? (Lỗi -> Sai quan hệ kế thừa).
4. **I**: Class này có chứa hàm nào mà nó để trống hoặc quăng lỗi không? (Có -> Tách Interface).
5. **D**: Hàm khởi tạo (`__init__` / `constructor`) có đang trực tiếp `new` một class database/network không? (Có -> Nhét nó qua Tham số).

</details>

To master SOLID, continuously evaluate your code against these questions:
1. **S**: How many distinct responsibilities does this class have? (If > 1, separate it).
2. **O**: If a new business requirement is introduced, do I have to modify existing `if-else` blocks? (If yes, implement a Strategy pattern).
3. **L**: If I pass a Child class into a function expecting the Parent class, does the system still behave correctly? (If no, the inheritance hierarchy is flawed).
4. **I**: Does this class contain empty methods or methods that throw `UnsupportedOperationException`? (If yes, segregate the interface).
5. **D**: Does the constructor directly instantiate concrete database or network classes? (If yes, inject them as dependencies via abstractions).

---

## Related Topics

- **[OOP Principles](./oop-principles.md)** — The 4 foundational pillars required before mastering SOLID.
- **[Design Patterns](./design-patterns.md)** — Practical, proven architectural solutions that heavily leverage SOLID principles.
