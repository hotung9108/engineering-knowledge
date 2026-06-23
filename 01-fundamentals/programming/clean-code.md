# Clean Code

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Clean Code là tập hợp các nguyên tắc viết code sao cho người khác (hoặc chính bạn sau 6 tháng) đọc vào là hiểu ngay. "Máy tính hiểu code là chuyện bình thường. Viết code cho CON NGƯỜI hiểu mới là đỉnh cao."

</details>

> **Summary**: Clean Code is a set of principles for writing code that is immediately comprehensible to other engineers (or to yourself in the future). "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn mua một tủ sách IKEA về tự lắp. 
- **Bad Code (Code bẩn)**: Cuốn sách hướng dẫn toàn chữ tượng hình, các chi tiết được đặt tên là `X1, Y2, Z3`. Cứ đọc 1 trang bạn lại phải lật lại trang đầu để xem `X1` là cái ốc vít hay tấm gỗ. Bạn lắp xong cái tủ nhưng bực mình muốn đập luôn cả tủ.
- **Clean Code (Code sạch)**: Cuốn sách hướng dẫn vẽ hình rõ ràng, các chi tiết được dán nhãn `Tấm gỗ lưng`, `Ốc vít dài`, `Bản lề`. Mỗi bước chỉ hướng dẫn làm 1 việc. Bạn lắp cái tủ trong 10 phút vừa huýt sáo.

**Trong lập trình:** Máy tính không quan tâm bạn đặt tên biến là `A` hay `CustomerName`, nó vẫn chạy đúng. Nhưng con người thì có! Clean Code là nghệ thuật viết code như viết một bài văn mạch lạc cho con người đọc.

</details>

Imagine you purchase a bookshelf from IKEA to assemble yourself.
- **Bad Code**: The instruction manual is filled with hieroglyphics, and the parts are arbitrarily named `X1, Y2, Z3`. For every step, you must turn back to the first page to decipher whether `X1` is a screw or a wooden plank. You might assemble the shelf eventually, but the process is deeply frustrating.
- **Clean Code**: The instruction manual provides clear illustrations, and the parts are explicitly labeled `Back Panel`, `Long Screw`, and `Hinge`. Each step instructs you to perform exactly one action. You assemble the shelf in ten minutes effortlessly.

**In Programming**: A computer compiler does not care whether you name a variable `A` or `CustomerName`; it executes the logic regardless. Humans, however, do care. Clean Code is the engineering discipline of writing code as if it were a coherent, well-structured essay meant for human consumption.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Clean Code** là code mà:
- **Đọc như một bài báo**: Đọc tên biến, tên hàm là đoán ngay được hàm đó làm gì mà không cần đọc ruột bên trong.
- **Dễ thay đổi**: Sửa 1 chỗ không làm sập toàn bộ hệ thống.
- **Ít bất ngờ**: Không có những "side effect" (tác dụng phụ) ngầm bên trong.
- **Đơn giản**: Không cố gắng tỏ ra nguy hiểm bằng các đoạn code lắt léo.

</details>

**Clean Code** is defined by the following characteristics:
- **High Readability**: Variable and function names are so descriptive that you can deduce their purpose without reading the internal implementation logic.
- **Maintainability**: Modifying one section of the code does not cascade into systemic failures elsewhere.
- **Predictability**: Functions perform exactly what their names imply, without hidden "side effects."
- **Simplicity**: The code avoids unnecessary cleverness or convoluted logic in favor of straightforward execution.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn có biết: **Tỷ lệ thời gian Đọc Code so với Viết Code là 10:1.**
Cứ 1 phút bạn gõ phím viết code mới, bạn (hoặc đồng nghiệp) sẽ tốn 10 phút để đọc lại nó trong tương lai.

| Vòng đời của Code bẩn (Spaghetti Code) |
|---|
| **Năm 1**: Code chạy ngon! Sếp thưởng to! |
| **Năm 2**: Thêm tính năng mất gấp đôi thời gian, đụng vào đâu hỏng đó. |
| **Năm 3**: Cả team sợ không dám sửa bất cứ dòng code nào vì sợ sập server. |
| **Năm 4**: Sếp bảo: "Đập đi làm lại từ đầu!" -> Tốn hàng tỷ đồng. |

</details>

Consider this industry fact: **The ratio of time spent reading code versus writing is well over 10:1.**
For every minute spent typing new code, an engineer will spend ten minutes reading that code in the future.

| The Lifecycle of Spaghetti Code |
|---|
| **Year 1**: The code executes perfectly. Feature delivery is rapid. |
| **Year 2**: Adding new features requires double the expected time. Unrelated modules begin breaking. |
| **Year 3**: The engineering team is terrified to modify the codebase due to the risk of critical outages. |
| **Year 4**: Management mandates a complete system rewrite, resulting in massive financial and temporal losses. |

---

## Layer 3: Core Rules (Compare)

### Rule 1: Naming

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> Tên biến/hàm phải trả lời được 3 câu hỏi: Tại sao nó tồn tại? Nó làm gì? Cách dùng nó?

**❌ Bad Naming (Tên tệ hại)**
```python
d = 0 # Elapsed time in days
lst = [] # Danh sách gì?
def get_data(x, y): pass # Data gì? x, y là cái gì?
flag = True # Cờ hiệu gì?
```

</details>

> A variable or function name should answer three questions: Why does it exist? What does it do? How is it used?

### Without Implementation: Bad Naming
```python
d = 0 # Elapsed time in days
lst = [] # What does this list contain?
def get_data(x, y): pass # What data? What are x and y?
flag = True # What does this flag represent?
```

### With Implementation: Clean Naming
**Python:**
```python
elapsed_time_in_days = 0
active_customers = []

# Function names should be Verbs; Variable names should be Nouns
def calculate_total_price(item_price, tax_rate): pass

# Boolean variables should read like a Yes/No question
is_active = True
has_permission = False
```

**Java:**
```java
int elapsedTimeInDays = 0;
List<Customer> activeCustomers = new ArrayList<>();

public double calculateTotalPrice(double itemPrice, double taxRate) { ... }

boolean isActive = true;
boolean hasPermission = false;
```

---

### Rule 2: Functions

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> Hàm phải NGẮN. Và quan trọng hơn: Hàm chỉ làm ĐÚNG MỘT VIỆC (Do One Thing).

**❌ Bad Function (Hàm ôm đồm)**
```java
// Hàm này làm quá nhiều việc: Kiểm tra user, Tính tiền, Lưu DB, Gửi Email!
public void processOrder(User user, Cart cart) {
    if(user == null) throw new Error();
    double total = 0;
    for(Item i : cart.items) total += i.price;
    db.saveOrder(user, cart);
    email.send("Order successful!");
}
```

</details>

> Functions must be short. More importantly, a function must Do One Thing (SRP).

### Without Implementation: The Monolithic Function
```java
// This function handles validation, calculation, persistence, and notification!
public void processOrder(User user, Cart cart) {
    if(user == null) throw new IllegalArgumentException();
    double total = 0;
    for(Item i : cart.items) total += i.price;
    db.saveOrder(user, cart);
    email.send("Order successful!");
}
```

### With Implementation: Extract and Delegate
**Python:**
```python
def process_order(user, cart):
    validate_user(user)
    total = calculate_total(cart)
    save_order_to_db(user, cart, total)
    send_confirmation_email(user)

# The smaller functions are defined below.
# By reading `process_order`, the entire workflow is immediately comprehensible without cognitive overload.
```

---

### Rule 3: Error Handling

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> Báo lỗi rõ ràng. Đừng nuốt lỗi (Swallow exceptions).

**❌ Bad Error Handling**
```python
def get_user(id):
    try:
        return db.query(id)
    except Exception as e:
        print("Lỗi rồi!") # Log ra console rồi ỉm luôn
        return None # Trả về None khiến hàm khác gọi nó bị lỗi dây chuyền
```

</details>

> Errors must be explicit. Never swallow exceptions.

### Without Implementation: Bad Error Handling
```python
def get_user(user_id):
    try:
        return db.query(user_id)
    except Exception as e:
        print("An error occurred!") # Logs to console and suppresses the error
        return None # Returning None forces the caller to handle null checks, often causing chain-reaction failures.
```

### With Implementation: Explicit Error Handling
**Python:**
```python
def get_user(user_id):
    try:
        return db.query(user_id)
    except DatabaseConnectionError:
        # Raise an exception with a highly specific message to facilitate rapid debugging
        raise CustomException(f"Database connection lost while querying user ID: {user_id}")
```

**Java:**
```java
public User getUser(String id) {
    return userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));
}
```

---

### Rule 4: Comments

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> Code tồi thì viết Comment giải thích. Code xịn thì tự nó đã giải thích chính nó. Đừng dùng Comment để bù đắp cho việc đặt tên ngu ngốc.

**❌ Bad Comments**
```java
// Check to see if the employee is eligible for full benefits
if ((employee.flags & HOURLY_FLAG) && (employee.age > 65)) { ... }
```
Dòng code trên quá lắt léo, tác giả phải viết Comment để giải thích. Tại sao không làm cho code dễ đọc hơn?

**Khi nào nên dùng Comment?**
1. Giải thích TẠI SAO (Why) chứ không phải LÀM GÌ (What). Ví dụ: `// Đợi 2 giây ở đây vì API của đối tác bị limit request, nếu gọi nhanh sẽ bị block.`
2. Viết tài liệu (Docstrings) cho thư viện công khai.

</details>

> Bad code requires comments to explain it. Good code explains itself. Do not use comments to compensate for poor naming conventions.

### Without Implementation: Redundant Comments
```java
// Check to see if the employee is eligible for full benefits
if ((employee.flags & HOURLY_FLAG) != 0 && (employee.age > 65)) { ... }
```
The logic above is too complex, forcing the author to write a comment. Instead, refactor the code to be inherently readable.

### With Implementation: Self-Documenting Code
```java
if (employee.isEligibleForFullBenefits()) { ... }
```
The code now explains itself. The comment is obsolete.

**When should you use comments?**
1. To explain the **WHY** behind a decision, not the **WHAT**. Example: `// Implementing a 2-second delay because the external API enforces strict rate limits; aggressive polling results in an IP ban.`
2. To provide official documentation (Docstrings/Javadocs) for public-facing APIs and libraries.

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Clean Code **luôn luôn** phải được áp dụng, bất kể dự án lớn hay nhỏ.
Ngoại lệ duy nhất: 
- Bạn đang tham gia cuộc thi code (Hackathon, Competitive Programming) yêu cầu tốc độ gõ phím nhanh nhất có thể và sau đó vứt code đi.

</details>

Clean Code principles must be applied **universally**, regardless of the project's scale or domain.
The only acceptable exception is competitive programming or short-lived hackathons where raw execution speed and rapid prototyping temporarily supersede long-term maintainability.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

### Nguyên tắc DRY (Don't Repeat Yourself)
Nếu bạn phải copy-paste một đoạn code 3 lần, đã đến lúc đưa nó vào một hàm (Function) dùng chung.

### Nguyên tắc Boy Scout Rule
"Luôn để lại khu cắm trại sạch sẽ hơn lúc bạn mới đến". Khi bạn mở một file code cũ ra để sửa tính năng mới, nếu thấy tên biến hơi tối nghĩa, hãy đổi tên nó lại cho rõ ràng rồi hẵng commit.

### Magic Numbers (Số ma thuật)
Tuyệt đối không dùng các con số vô nghĩa trong code.
- ❌ `if (status == 2):` -> 2 là cái quái gì?
- ✅ `if (status == ORDER_SHIPPED):` -> À, hóa ra 2 là đã giao hàng.

</details>

### The DRY Principle (Don't Repeat Yourself)
If you find yourself copying and pasting a block of code three times, it must be extracted into a reusable function or module.

### The Boy Scout Rule
"Always leave the campground cleaner than you found it." When you open an existing file to add a new feature, if you encounter an obscure variable name or a poorly structured function, refactor it before committing your new code.

### Avoid Magic Numbers
Never use hard-coded, unexplained numbers in your logic.
- Incorrect: `if (status == 2):` -> What does 2 represent?
- Correct: `if (status == ORDER_SHIPPED):` -> The intent is immediately clear.

---

## Related Topics

- **[SOLID Principles](./solid-principles.md)** — Core design principles to ensure your codebase remains highly adaptable and decoupled.
- **[Design Patterns](./design-patterns.md)** — Proven, standardized architectural templates for writing robust, clean code.
