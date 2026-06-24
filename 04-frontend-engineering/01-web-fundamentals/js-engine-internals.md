# JavaScript Engine Internals (Advanced)

Mọi Frontend Developer Senior đều phải hiểu cách JavaScript thực thi bên dưới trình duyệt. Phổ biến nhất là **V8 Engine** (được dùng trong Chrome và Node.js).

## 1. V8 Engine Architecture

JavaScript là ngôn ngữ thông dịch (interpreted), nhưng V8 sử dụng **JIT (Just-In-Time) Compilation** để tăng tốc độ thực thi.

```mermaid
graph LR
    JS[JavaScript Source] --> Parser[Parser]
    Parser --> AST[Abstract Syntax Tree]
    AST --> Ignition[Ignition (Interpreter)]
    Ignition --> Bytecode[Bytecode]
    Bytecode --> Exec1[Execute]
    
    Ignition -- Profiling Data --> TurboFan[TurboFan (Optimizing Compiler)]
    TurboFan --> MachineCode[Optimized Machine Code]
    MachineCode --> Exec2[Execute faster]
    
    MachineCode -- Deoptimization --> Ignition
```

### Ignition (Interpreter)
- Dịch AST thành **Bytecode** chưa tối ưu và chạy ngay lập tức (giúp trang web khởi động nhanh).
- Trong quá trình chạy, nó thu thập **Profiling Data** (loại biến thường dùng, số lần gọi hàm).

### TurboFan (Optimizing Compiler)
- Các hàm chạy nhiều lần (Hot functions) được TurboFan compile trực tiếp thành **Machine Code** siêu tốc dựa trên Profiling Data.
- **Deoptimization:** Nếu JS là dynamic typing, giả sử một hàm luôn nhận `number`, TurboFan tối ưu hóa nó cho `number`. Nhưng đột nhiên bạn truyền `string`, TurboFan phải hủy bỏ (Deoptimize) và đẩy ngược lại cho Ignition chạy Bytecode.
- **Bài học:** Giữ type ổn định trong JS (hoặc dùng TS) giúp V8 tối ưu code hiệu quả nhất.

---

## 2. Event Loop & Async JavaScript

JS là single-threaded, chạy trên **Call Stack**. Event Loop cho phép JS làm việc bất đồng bộ (non-blocking) bằng cách sử dụng Web APIs và Task Queues.

### Call Stack
Lưu trữ execution context (các hàm đang chạy). Chạy tuần tự theo LIFO (Last In, First Out).

### Web APIs
Các tính năng do trình duyệt cung cấp (không thuộc V8), ví dụ: `setTimeout`, `fetch`, `DOM events`. Chúng chạy ở background thread.

### Macrotask Queue (Task Queue)
Chứa các callbacks từ:
- `setTimeout`, `setInterval`
- `UI rendering`
- `I/O`, events

### Microtask Queue
Chứa các callbacks từ:
- `Promise.then()`, `.catch()`, `.finally()`
- `MutationObserver`
- `queueMicrotask()`

### Nguyên tắc của Event Loop
1. Lấy và thực thi hàm trên cùng của Call Stack cho đến khi rỗng.
2. Kiểm tra **Microtask Queue**. Thực thi TOÀN BỘ microtasks cho đến khi rỗng (kể cả microtask sinh ra thêm microtask khác).
3. Khi Microtask Queue rỗng, Event Loop mới lấy **1 Macrotask** từ Macrotask Queue ra chạy.
4. Lặp lại quá trình.

> [!WARNING]
> Microtasks có độ ưu tiên CAO HƠN Macrotasks. Một vòng lặp vô hạn sinh Promise (`Promise.resolve().then(...)`) sẽ làm "treo" trình duyệt hoàn toàn, trong khi `setTimeout` đệ quy thì không bị treo (do browser có chèn UI render giữa các macrotasks).

---

## 3. Memory Management & Garbage Collection (GC)

Bộ nhớ V8 chia làm 2 vùng chính:

### Stack Memory
- Lưu các biến nguyên thuỷ (Primitives: number, string, boolean, null, undefined) và references (pointers).
- Cực nhanh, tự động dọn dẹp khi function kết thúc.

### Heap Memory
- Lưu các Objects, Arrays, Functions. Không tự dọn dẹp.

### Garbage Collector (Orinoco)
V8 dùng thuật toán **Mark-and-Sweep** kết hợp phân chia thế hệ (Generational GC).

1. **Young Generation (Nursery & Intermediate):**
   - Chứa objects mới tạo. Vùng này nhỏ (vài MB).
   - "Scavenger" chạy thường xuyên, cực nhanh để gom rác.
2. **Old Generation:**
   - Chứa objects sống sót qua 2 lần dọn rác ở Young Gen.
   - Vùng này lớn. "Mark-Sweep-Compact" (Major GC) chạy thưa hơn, gây ra "Stop-The-World" (đóng băng Main Thread một chút). Hiện tại V8 đã có Concurrent Marking để giảm thiểu giật lag.

### Memory Leaks thường gặp trong Frontend:
- **Global Variables:** Vô tình tạo biến toàn cục không giải phóng được.
- **Closures:** Closure giữ reference đến object lớn không cần thiết.
- **Event Listeners:** Đăng ký listener nhưng quên `removeEventListener` khi component unmount.
- **Timers:** Quên `clearInterval()`.
- **Detached DOM elements:** Xóa node khỏi DOM nhưng vẫn lưu trong JS variable.
