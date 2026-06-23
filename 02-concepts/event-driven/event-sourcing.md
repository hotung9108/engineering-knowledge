# Event Sourcing

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trong các Database bình thường, bạn chỉ lưu "Trạng thái hiện tại" (Ví dụ: Số dư tài khoản là 100$). Nếu bạn tiêu đi 20$, bạn lấy 100 - 20 = 80$, rồi GHI ĐÈ số 80$ lên số 100$. Database sẽ KHÔNG CÒN nhớ số 100$ từng tồn tại. **Event Sourcing** là một tư duy trái ngược: CẤM GHI ĐÈ. Database sẽ không lưu số dư, mà lưu 1 cuộn băng ghi hình mọi hành động bạn đã làm (1. Nạp 100$, 2. Mua áo 20$). Khi bạn muốn biết số dư, hệ thống sẽ lấy cuộn băng ra "tua lại" (Phát lại) từ đầu để tính toán ra con số 80$.

</details>

> **Summary**: Traditional CRUD (Create, Read, Update, Delete) databases are fundamentally "State-Oriented". They exclusively store the current Snapshot of reality, destructively overwriting historical data during `UPDATE` operations. **Event Sourcing** is a radical paradigm shift that dictates that the absolute Source of Truth is not the current state, but rather an immutable, append-only chronological log of all domain events that *caused* the current state. State is never mutated; it is mathematically derived (projected) by replaying the history of events from the beginning of time.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang chơi Cờ vua.
1. **Database truyền thống (Lưu trạng thái)**: Bạn chụp 1 tấm ảnh bàn cờ ở phút thứ 10. Bức ảnh chỉ cho bạn biết con Vua đang ở ô nào. Nhưng bức ảnh đó KHÔNG THỂ cho bạn biết ván cờ đã diễn ra như thế nào, con Tướng đã ăn con Xe ở nước thứ mấy. (Bạn mất hoàn toàn lịch sử).
2. **Event Sourcing (Lưu sự kiện)**: Bạn không chụp ảnh. Thay vào đó, bạn lấy tờ giấy ghi chép lại từng nước đi (1. Mã lên E4, 2. Tốt lên D5). Tờ giấy ghi chép đó là Event Sourcing. Nếu bạn lỡ tay làm đổ bàn cờ, bạn chỉ cần lấy tờ giấy ra, xếp lại các quân cờ đi theo đúng từng bước đã ghi, bạn sẽ khôi phục lại (Replay) bàn cờ y hệt như phút thứ 10.

</details>

Imagine a Chess match.
1. **Traditional CRUD (State-Oriented)**: You take a photograph of the chessboard at minute 15. You know precisely where the White King is located *right now*. However, you have absolutely zero idea how the pieces got there, what brilliant sacrifices were made, or what mistakes the opponent made. The history is permanently destroyed.
2. **Event Sourcing (Log-Oriented)**: You do not take a photograph. Instead, you write down the algebraic chess notation for every single move (e.g., `1. e4 e5 2. Nf3 Nc6`). This log is the Source of Truth. If your dog knocks over the chessboard, you simply take a fresh board and replay the recorded moves sequentially. You perfectly reconstruct the state of the board.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Event Store (Kho lưu trữ Sự kiện)**: Trái tim của hệ thống. Đây không phải là bảng MySQL thông thường. Nó là một cuốn sổ Cái (Ledger) dạng Append-only (Chỉ được phép viết tiếp vào cuối, tuyệt đối CẤM lệnh `UPDATE` hoặc `DELETE`).
**2. Aggregation (Gộp trạng thái)**: Bảng Event Store chỉ chứa 1 triệu dòng sự kiện (`Nạp tiền`, `Rút tiền`). Nếu khách hàng hỏi "Tôi còn bao nhiêu tiền?", ta không thể ném 1 triệu dòng đó cho khách. Ta phải chạy một vòng lặp cộng trừ 1 triệu dòng đó lại để ra con số 5 triệu VNĐ. Quá trình này gọi là Gộp (Aggregation/Projection).
**3. Snapshot (Chụp ảnh nhanh)**: Tua lại 1 triệu dòng sự kiện mỗi lần khách hỏi số dư sẽ làm máy chủ sụp đổ. Nên cứ mỗi 10.000 sự kiện, hệ thống sẽ lưu lại 1 cái Snapshot (Tạm tính: Đến mốc 10.000, số dư là 4 triệu). Lần sau khách hỏi, hệ thống chỉ cần tua từ mốc 10.001 trở đi và cộng vào 4 triệu.

</details>

**1. The Event Store (The Ledger)**: The definitive, immutable database. Unlike relational tables, it is strictly an **Append-Only** log. Operations like `UPDATE` or `DELETE` are philosophically and mechanically prohibited. You can only insert new facts.
**2. State Projection (Rehydration)**: The Event Store contains raw history (e.g., `Deposited_100`, `Withdrew_20`). To answer the question "What is my balance?", the application must fetch all historical events for that specific Account ID and execute a functional `reduce()` operation (Replaying the events) to calculate the current integer.
**3. Snapshots (Performance Optimization)**: Replaying an account with 50,000 historical transactions per second is computationally unviable. Architects implement **Snapshots**. Every 1,000 events, the system calculates the state and saves it explicitly (e.g., "At Event #1000, Balance = $5000"). The next read operation fetches the Snapshot, and only replays the minimal delta of Events from #1001 onwards.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao phải đẻ ra cách lưu dữ liệu phức tạp thế này?
**1. Khả năng Kiểm toán (Auditability) hoàn hảo**: Trong hệ thống Kế toán, Ngân hàng, Y tế, bạn KHÔNG ĐƯỢC PHÉP ghi đè dữ liệu. Nếu kế toán nhập nhầm số tiền, họ không được bấm nút "Sửa" hay "Xóa" (Vì như thế là phi tang chứng cứ tham ô). Họ bắt buộc phải tạo ra một phiếu "Điều chỉnh giảm" (Bù đắp). Event Sourcing là hiện thân hoàn hảo của nguyên tắc Kế toán này. Bạn có một lịch sử pháp lý không thể chối cãi 100%.
**2. Cỗ máy Thời gian (Time Travel)**: Đột nhiên sếp hỏi: "Hệ thống giỏ hàng của chúng ta hoạt động thế nào vào đúng lúc 12:00 trưa ngày Black Friday năm ngoái?". Với DB truyền thống: Vô phương cứu chữa (Vì data đã bị ghi đè hàng vạn lần). Với Event Sourcing: Dễ ợt! Bạn chỉ cần cho máy tính Tua cuộn băng sự kiện dừng lại đúng mốc 12:00 ngày hôm đó. Hệ thống sẽ phục hồi lại y chang trạng thái của quá khứ.

</details>

Why abandon the simplicity of CRUD for this immense complexity?
**1. Absolute Cryptographic Auditability**: In highly regulated domains (Banking, Healthcare, Ledger Accounting), destructively overwriting a Database record (`UPDATE balance = 0`) is legally equivalent to destroying evidence. If an accountant makes an error, they cannot use an eraser; they must author a Compensating Entry. Event Sourcing natively enforces strict append-only compliance. It provides an unforgeable, 100% accurate historical audit trail out-of-the-box.
**2. Temporal Queries (Time Travel)**: Business Intelligence asks: "What exactly did the user's shopping cart look like at 14:02 PM last Thursday before they abandoned it?". A CRUD database cannot answer this; the intermediate state is permanently lost. Event Sourcing acts as a Time Machine. By replaying the Event Stream and halting the replay algorithm precisely at the timestamp `14:02 PM`, developers can perfectly reconstruct the exact Domain State at any microsecond in history.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cách hai hệ thống lưu dữ liệu thay đổi Tên người dùng.
</details>

Visualizing Data Persistence: Updating a User's Name from "John" $\rightarrow$ "Johnny" $\rightarrow$ "Johnathan".

| Aspect | Traditional CRUD Database | Event Sourcing (Event Store) |
|---|---|---|
| **Database Table** | `Users` Table | `User_Events` Log |
| **Row Content** | `id: 1, name: "Johnathan"` | 1. `{"type": "Created", "name": "John"}`<br>2. `{"type": "Updated", "name": "Johnny"}`<br>3. `{"type": "Updated", "name": "Johnathan"}` |
| **Current State** | Fetched instantly (Fast). | Projected by reading 3 rows (Slower). |
| **Past State** | **Permanently Destroyed**. | Perfectly preserved. |
| **Write Speed** | Slow (B-Tree Indexing overhead). | Extremely Fast (Sequential Append-Only). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hệ thống Kế toán cốt lõi (Ledgers)**: Mọi ngân hàng trên thế giới đều dùng cơ chế giống hệt Event Sourcing. Sổ phụ ngân hàng của bạn thực chất là một Event Store chứa các sự kiện Nạp/Rút.
2. **Hệ thống Giỏ hàng E-commerce (Shopping Cart)**: Giỏ hàng bị bỏ rơi (Abandoned Cart) là kho vàng của E-commerce. Nếu dùng DB thường, khách bấm Xóa món hàng khỏi giỏ $\rightarrow$ Món hàng bay màu. Amazon dùng Event Sourcing. Khách xóa món hàng $\rightarrow$ Lưu sự kiện `Item_Removed`. Phân tích viên sẽ đọc các sự kiện này để biết: Khách hay xóa món gì nhất trước khi thanh toán? Tại sao? Để từ đó tối ưu bán hàng.
3. **Chơi lại Game (Replay System)**: Các tính năng "Xem lại trận đấu" trong LMHT (League of Legends) hay CS:GO không hề quay video lại màn hình của bạn. Nó chỉ lưu các tọa độ click chuột và tung chiêu (Event Sourcing). Khi bạn ấn xem Replay, Game Engine sẽ lấy đống Event đó chạy lại thành một trận đấu hoàn chỉnh dưới dạng 3D. Rất nhẹ và mượt.

</details>

1. **Financial Ledgers & Banking**: The immutable standard. Every bank statement is fundamentally a projected view of an Append-Only Event Store (Credits and Debits).
2. **E-Commerce Shopping Carts (Behavioral Analytics)**: If a user adds an iPhone to their cart, and then removes it 5 minutes later, a CRUD database deletes the row. The Business loses highly valuable intent data. Event Sourcing records `Item_Added` followed by `Item_Removed`. Data Science teams replay these Event Streams to analyze abandonment patterns and trigger targeted retargeting emails ("Did you forget your iPhone?").
3. **Gaming Replay Engines (eSports)**: Features like "Match Replays" in Starcraft or League of Legends do not record 5 Gigabytes of MP4 Video data. They record a 10 Megabyte file of raw Event Sourcing logs (Mouse clicks, spell casts, exact coordinate timestamps). The Game Engine simply "Projects" those events back into the 3D renderer locally, achieving perfect playback with minimal storage.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bắt buộc đi kèm CQRS**: Vì Event Sourcing lưu dữ liệu dưới dạng "Cuộn băng", việc truy vấn (Query) "Tìm cho tôi tất cả người dùng tên John" là BẤT KHẢ THI. Bạn không thể tua lại 1 tỷ sự kiện của 10 triệu người dùng chỉ để tìm chữ John. Event Sourcing luôn luôn phải gắn liền với CQRS: Khi có Event mới, tạo ra một bản copy dữ liệu dạng CRUD bình thường ném sang một DB khác chuyên để Đọc (Read Database). 
2. **Thiết kế Event cẩn thận**: Event là "Đá tảng", lưu xuống là không bao giờ được sửa. Nếu bạn thiết kế thiếu 1 field `email` trong Event `User_Registered`, bạn sẽ phải ôm hận mãi mãi.

</details>

1. **Absolute Mandate: Pair with CQRS**: Event Sourcing is structurally hostile to complex Read queries. If your database contains 50 million discrete state changes, executing `SELECT * FROM users WHERE age > 25` is computationally impossible; you would have to replay the entire history of the universe on the fly to deduce every user's current age. **You MUST implement CQRS (Command Query Responsibility Segregation)**. The Event Store acts strictly as the Write Database. A background worker consumes the Events and synchronously populates a heavily indexed, highly optimized traditional Read Database (e.g., Elasticsearch or PostgreSQL Views) to serve UI queries.
2. **Schema Versioning & Upcasting**: Because Events are strictly immutable, you cannot execute an `ALTER TABLE` to fix a typo in an old event from 5 years ago. If your business rules change and `Event_V1` structurally differs from `Event_V2`, your projection logic will crash trying to read the ancient `V1` event. You must implement robust **Upcasting** logic inside your application code to mathematically translate legacy `V1` payloads into `V2` structures in memory on the fly during the replay process.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Áp dụng Event Sourcing cho ứng dụng quá Đơn giản**: Bạn làm 1 cái App Quản lý Danh bạ (Chỉ có Thêm, Sửa, Xóa tên người). Nhưng bạn đòi dùng Event Sourcing cho ngầu. Chúc mừng, bạn đã biến 1 bài toán giải quyết trong 1 ngày thành 1 cơn ác mộng tốn 2 tháng code, tốn gấp 10 lần dung lượng ổ cứng, và tốc độ siêu chậm. *Luật*: Đừng xài Event Sourcing trừ khi miền nghiệp vụ Bắt Buộc phải có tính Kiểm toán Lịch sử.
2. **GDPR và Quyền được lãng quên**: Luật Châu Âu quy định: Người dùng có quyền yêu cầu XÓA VĨNH VIỄN toàn bộ dữ liệu của họ khỏi hệ thống. Nhưng Event Sourcing là hệ thống BẤT BIẾN (Không được phép Xóa/Sửa). Hai khái niệm này đấm nhau vỡ mặt. 
   - *Cách giải quyết (Crypto Shredding)*: Bạn không lưu Tên thật của họ vào Event Store. Bạn mã hóa cái Tên đó bằng một Chìa khóa (Key). Lưu bản mã hóa vào Event. Chìa khóa giữ ở DB ngoài. Khi họ đòi Xóa, bạn chỉ cần ném cái Chìa khóa đi. Toàn bộ chuỗi Event kia lập tức trở thành rác vô nghĩa không thể giải mã, thỏa mãn luật pháp mà không vi phạm tính "Không được xóa" của Event Sourcing.

</details>

1. **Resume-Driven Over-Engineering**: The most common anti-pattern. An architect forces Event Sourcing onto a trivial CRUD Domain (like a static "Contact Us" form submission or a simple Blog Post). They introduce 10x code complexity, massive mental overhead, eventual consistency debugging nightmares, and explosive storage growth, completely devoid of any tangible business value. **Rule**: Confine Event Sourcing strictly to Core Business Domains where Historical Intent, Auditability, or Complex Compensation logic are critical.
2. **The GDPR "Right to be Forgotten" Contradiction**: European GDPR laws mandate that a user has the explicit legal right to have their PII (Personally Identifiable Information) permanently eradicated from your servers. Event Sourcing rigidly enforces that the Event Store is Immutable and Append-Only. You cannot execute a `DELETE` command. This creates a severe legal paradox.
   - *The Solution (Crypto-Shredding)*: Never store raw PII (Names, Emails) in the Immutable Event payloads. Encrypt the PII fields using a unique, user-specific cryptographic key. Store the encrypted cipher inside the Event Store. Store the decryption key in a mutable, traditional CRUD Key-Value store. When a GDPR Erasure request arrives, simply permanently `DELETE` the user's decryption key from the Key-Value store. The immutable Event Store is now filled with irreversible, mathematically useless noise. The user is cryptographically "forgotten".

---

## Related Topics

- For the absolute mandatory companion to this pattern, read **[CQRS](./cqrs.md)**.
- For how multiple services use these events to run Transactions, read **[Saga Pattern](./saga.md)**.
- For the fundamental theory of events, review **[Event-Driven Overview](./overview.md)**.
