# MongoDB

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trong kỉ nguyên SQL, lập trình viên bị trói buộc bởi những "Bảng" (Tables) cứng nhắc. Muốn thêm một Cột mới? Bạn phải chạy lệnh `ALTER TABLE` rủi ro, làm khóa toàn bộ Database. **MongoDB** xuất hiện như một cuộc cách mạng giải phóng. Nó là cơ sở dữ liệu **NoSQL Document** phổ biến nhất thế giới. Thay vì lưu dữ liệu dạng Bảng-Cột như Excel, MongoDB lưu mọi thứ dưới dạng JSON (chính xác là BSON). Nó cho phép bạn lưu một cấu trúc lộn xộn, lồng nhau chằng chịt mà không cần khai báo trước (Schema-less). Đặc biệt, vì sinh ra cùng thời điểm với Node.js, cú pháp truy vấn của MongoDB sử dụng 100% JavaScript, khiến nó trở thành sự lựa chọn "Mặc định" của các Lập trình viên Frontend/Node.js khi mới học làm Backend (MERN Stack).

</details>

> **Summary**: For decades, Relational Databases forced developers to strictly map Object-Oriented code into rigid, tabular schemas—a painful friction point known as the Object-Relational Impedance Mismatch. **MongoDB** was engineered to eliminate this friction. As the world's most dominant **Document-Oriented NoSQL Database**, it stores data as rich, nested BSON (Binary JSON) documents. It explicitly abandons `JOINs` and strict Schema Enforcement in favor of extreme flexibility and Schema-on-Read dynamics. Because its native query language is JavaScript, it achieved meteoric adoption alongside Node.js, forming the backbone of the ubiquitous **MEAN/MERN Stack**. While it is entirely inappropriate for highly relational financial ledgers, it is unparalleled for managing highly polymorphic data, product catalogs, and rapidly evolving MVPs.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn lưu trữ Hồ sơ Bệnh án.
1. **SQL (Cách cũ)**: Bệnh viện bắt bạn chia nhỏ thông tin: Giấy tờ tùy thân để tủ A, Lịch sử uống thuốc để tủ B, Ảnh chụp X-Quang để tủ C. Mỗi lần bác sĩ muốn xem hồ sơ của bạn, y tá phải chạy đi 3 tủ khác nhau, lấy giấy ra và "Khâu" chúng lại với nhau (Phép `JOIN` trong SQL) rồi mới đưa cho bác sĩ. Rất an toàn, nhưng cực kì mất thời gian.
2. **MongoDB (Cách mới)**: Bạn có một cái Kẹp hồ sơ duy nhất (Document). Mọi thứ: CMND, Lịch sử bệnh, Ảnh X-Quang đều được nhét chung vào cái kẹp đó. Y tá chỉ cần vọc tay vào tủ đúng 1 lần, rút cái kẹp ra là có 100% thông tin. Rất nhanh! Nhưng bù lại, nếu lỡ bạn đổi Địa chỉ nhà, Y tá phải mò đi tìm từng cái kẹp liên quan để sửa lại (thay vì chỉ sửa 1 lần ở Tủ A như cách cũ).

</details>

Imagine packing a Backpack for a trip.
1. **SQL (Relational)**: You have a perfectly compartmentalized tactical bag. There is a specific slot tailored exactly to the millimeter for your Laptop, a specific pouch for 3 pens, and nothing else. If you buy a new Camera, you cannot put it in the bag until you go back to the factory and pay them to sew a brand-new custom pocket onto the bag (Schema Migration).
2. **MongoDB (Document-Oriented)**: You have a massive, unstructured Duffle Bag. You can throw your Laptop, your Camera, 50 pens, and a loose sandwich into it without asking anyone for permission. It effortlessly accepts whatever you toss in (Schema-less). Pulling the whole bag out is incredibly fast. However, if you need to find *exactly* the green pen at the bottom, it might be chaotic if you didn't organize it well yourself.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cấu trúc của MongoDB thay đổi hoàn toàn từ vựng của thế giới SQL:
1. Không có Bảng (Table), mà gọi là **Collection** (Tập hợp).
2. Không có Dòng (Row), mà gọi là **Document** (Tài liệu).
3. **BSON (Binary JSON)**: MongoDB không lưu dữ liệu dưới dạng Text thuần. Nó biên dịch cục JSON của bạn thành mã Nhị phân (Binary). Việc này giúp tăng tốc độ đọc máy tính, đồng thời cho phép lưu thêm các kiểu dữ liệu mà JSON gốc không có (như `Date` nguyên bản, `ObjectId`, hoặc `Double`).
4. **Sharding (Cắt lớp Dữ liệu)**: Sức mạnh bá đạo nhất của Mongo. Khi dữ liệu của bạn phình lên 10 Terabytes, một máy tính không chứa nổi. Mongo tự động băm 10TB đó ra làm 10 phần, ném sang 10 máy chủ khác nhau một cách hoàn toàn tự động.

</details>

MongoDB fundamentally replaces standard RDBMS concepts with the Document Paradigm:
1. **Collections & Documents**: Instead of rigid Tables, MongoDB groups data into `Collections`. Instead of strictly-typed Rows, data is stored as `Documents` (JSON objects).
2. **BSON (Binary JSON)**: Under the hood, MongoDB does not parse raw JSON strings. It serializes the data into BSON. BSON extends the standard JSON spec by adding crucial programmatic data types (e.g., Native `Dates`, 64-bit integers, byte arrays, and its signature 12-byte `ObjectId`). BSON allows MongoDB to traverse nested arrays extremely fast without parsing the entire text file.
3. **Horizontal Scalability (Sharding)**: This is why massive enterprises use MongoDB. Relational databases hit a vertical ceiling. MongoDB natively supports Auto-Sharding. You define a Shard Key (e.g., `Country`), and MongoDB invisibly partitions your Petabyte-scale database across 50 cheap commodity servers. The application still queries it as if it were a single machine.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thế giới Cầu thay đổi. Trong kỉ nguyên Big Data, dữ liệu thường có hình thù cực kì phức tạp (Polymorphic). 
Ví dụ: Làm một trang thương mại điện tử như Shopee.
Nếu dùng SQL: Cái Áo thun thì có `Size`, `Màu`. Cái Laptop thì có `RAM`, `CPU`. Cái Tủ lạnh thì có `Công suất`. Nếu bạn cố gắng nhét tất cả vào 1 Bảng `Product` trong SQL, bạn sẽ tạo ra một cái bảng khổng lồ có 500 cột, trong đó 498 cột bị bỏ trống (NULL), cực kì lãng phí và không thể bảo trì.
MongoDB sinh ra để xử lý các dạng dữ liệu "Đa hình" này. Mỗi Sản phẩm (Document) tự quyết định cấu trúc của chính nó. Document số 1 có trường `RAM`, Document số 2 hoàn toàn không cần có trường `RAM`. Bỏ qua hoàn toàn giới hạn của `ALTER TABLE`.

</details>

MongoDB was engineered to resolve the **Object-Relational Impedance Mismatch** and scale massively across distributed cloud environments.
In Object-Oriented Programming (Java/Node), data is intrinsically hierarchical and nested (An `Order` object contains an array of `Items`, which contains an array of `Tags`). Saving this deeply nested object into a Relational SQL database requires disassembling it, executing 3 distinct `INSERT` statements across 3 tables, and setting up Foreign Keys. Reconstructing it requires expensive `JOIN` operations.
MongoDB exists to mirror Application code directly to the Database. You pass the entire JSON Object from your React Frontend directly into the MongoDB Driver, and it saves exactly as is. This 1:1 mapping accelerates development velocity drastically. Furthermore, its schema-less nature makes it the undisputed king of Polymorphic Data (e.g., Product Catalogs, where every item has wildly different attributes).

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc Nâng cấp ứng dụng (Thêm 1 Cột dữ liệu mới vào Database đang có 1 tỷ dòng).
</details>

Visualizing Schema Migrations (SQL vs MongoDB).

| Metric | Relational SQL (e.g., MySQL) | MongoDB (NoSQL) |
|---|---|---|
| **Adding a new field** | Executing `ALTER TABLE users ADD COLUMN phone VARCHAR(20)`. | **Zero Setup**. You simply send a JSON object with the `phone` key to the DB. |
| **Downtime / Locking**| Altering a 1-billion-row table in older SQL databases can lock the table for hours, effectively bringing down the entire application (Downtime). | **Instant**. Because there is no table schema, the database doesn't care. Old documents just lack the `phone` field. |
| **Data Enforcement** | The Database strictly rejects any insert that breaks the rules. | **Application Responsibility**. The Database accepts anything. Your Node.js code (Mongoose/Zod) MUST validate the data before saving. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khởi nghiệp và Prototype (MERN Stack)**: Vì cú pháp gọi DB bằng JavaScript thuần, các đội Node.js dùng Mongo có tốc độ viết code nháp nhanh gấp 3 lần SQL. Không cần lo nghĩ thiết kế Cột, Bảng. Cứ nhét JSON vào là chạy.
2. **Catalog Sản phẩm Đa hình (E-Commerce)**: Lưu trữ dữ liệu Tivi, Tủ lạnh, Quần áo chung một chỗ. Mỗi loại hàng hóa có các thuộc tính lồng nhau cực kì khác biệt. MongoDB cực kì mạnh mẽ ở khoản này.
3. **Phân tích Log / Dữ liệu IoT (Internet of Things)**: Máy đo nhiệt độ cứ mỗi 1 giây gửi một cục JSON báo cáo trạng thái. Mongo ghi dữ liệu siêu nhanh và cấu trúc JSON lồng nhau giúp lưu cả Mảng Lịch sử đo nhiệt độ vào chung 1 Document cực kỳ tiện lợi.

</details>

1. **Rapid Prototyping & Startups (MEAN/MERN Stack)**: The canonical use case. Startups pivot constantly; their data schemas change weekly. Running SQL migrations every 3 days is agonizing. MongoDB allows developers to ship MVPs rapidly. Because the entire stack (React $\rightarrow$ Node $\rightarrow$ Mongo) uses JavaScript/JSON end-to-end, the mental friction is zero.
2. **Polymorphic Product Catalogs**: E-Commerce platforms. A shoe has `size` and `color`. A laptop has `cpu_cores`, `ram`, and `gpu_teraflops`. Modeling this in SQL requires complex Anti-Patterns (EAV Pattern) or massive Sparse Tables filled with NULLs. MongoDB handles polymorphic structures natively.
3. **Telemetry, IoT, and Content Management Systems (CMS)**: Storing unstructured user-generated content, blog posts with variable metadata, or massive streams of JSON telemetry payloads from IoT devices where the schema isn't fully known in advance.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khử chuẩn hóa (Denormalization)**: Đừng mang tư duy SQL sang MongoDB. Trong SQL, bạn tạo bảng `User` và bảng `Address` rồi nối lại bằng `User_ID`. Trong Mongo, hãy NHÉT LUÔN mảng `Address` vào làm 1 trường bên trong `User`. Mongo khuyến khích gom mọi thứ cần thiết vào chung 1 cục JSON để khi đọc chỉ tốn ĐÚNG 1 LẦN đọc ổ cứng.
2. **Bảo vệ bằng Mongoose (Node.js)**: Vì Mongo cho phép lưu "Rác" (bạn có thể lưu tuổi là chữ "Mười"), nó cực kỳ nguy hiểm. Ở tầng Node.js, BẮT BUỘC phải dùng thư viện như `Mongoose` hoặc `Zod` để ép kiểu dữ liệu chặt chẽ TRƯỚC KHI đẩy vào MongoDB.

</details>

1. **Embrace Denormalization (Embed over Reference)**: The most fatal mistake developers make is treating MongoDB like a Relational DB. If an `Order` has 5 `Items`, do NOT create an `Orders` collection and an `Items` collection and reference them via ObjectIds. MongoDB lacks robust `JOIN` optimization. **Rule**: Embed the `Items` as an Array directly *inside* the `Order` document. If data is read together, it must be stored together on disk.
2. **Enforce Schema at the Application Layer (Mongoose)**: MongoDB's greatest strength (Schema-less flexibility) is also its greatest danger. Without constraints, a typo in your API can accidentally save `{ gae: 25 }` instead of `{ age: 25 }`, corrupting the database silently. **Rule**: Always enforce a rigid Schema at the Application Level. In Node.js ecosystems, this is non-negotiable. Utilize **Mongoose** (an ODM - Object Data Modeling library) to mathematically validate types, `required` fields, and `unique` constraints before the JSON payload ever touches the raw Database Driver.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giới hạn 16MB (Sát thủ ngầm)**: Một Document của Mongo có giới hạn cứng là 16 Megabytes. Nếu bạn thiết kế App Nhắn tin, và bạn nhét TẤT CẢ tin nhắn của phòng Chat vào 1 cái mảng `messages: []` bên trong Document `Room`. Sau vài tháng trò chuyện, mảng đó phình to vượt quá 16MB. Toàn bộ tính năng Chat sẽ sập ngay lập tức và không thể lưu thêm tin nhắn.
   - *Luật*: Không bao giờ Embed (Nhét) mảng dữ liệu có khả năng phình to vô hạn vào bên trong 1 Document. Với mảng vô hạn (như Comment, Tin nhắn), bắt buộc phải tách ra thành Collection mới.
2. **Không hỗ trợ Giao dịch chặt chẽ (ACID)**: Dù MongoDB bản mới đã hỗ trợ ACID Transactions, nhưng nó chạy khá chậm và phức tạp. Tuyệt đối KHÔNG DÙNG MongoDB làm cơ sở dữ liệu lõi cho Ngân hàng, Kế toán - nơi liên quan đến tiền bạc.

</details>

1. **The 16MB Document Limit & Unbounded Arrays**: The most notorious architectural failure in MongoDB. A single BSON Document cannot exceed 16MB. If you design a Blog system and embed all Comments inside the `Post` document (`comments: [{...}, {...}]`), a viral post with 50,000 comments will hit the 16MB limit, causing the Database to fatally reject all further inserts. **Rule**: Understand the Bounded vs. Unbounded Relationship. Embed *Bounded* data (e.g., a User has max 5 Addresses). Reference *Unbounded* data (e.g., a Post has infinite Comments; Comments MUST go into a separate collection).
2. **Ignoring Data Duplication Anomalies**: When you denormalize (embed) a User's `fullName` directly into 10,000 of their `Order` documents for faster read speed, what happens when the User legally changes their name? You are forced to execute a massive write operation to locate and update those 10,000 disparate documents. If the server crashes halfway through, you have massive data inconsistency. **Rule**: Do not use MongoDB for Financial Ledgers or systems where strict, single-source-of-truth normalization is legally required.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cách sử dụng MongoDB thông qua thư viện Mongoose (Node.js).
</details>

### Mongoose Schema Definition (Node.js)
MongoDB is schema-less, so we enforce the rules in code.

```javascript
import mongoose from 'mongoose';

// 1. Enforcing Schema in the Application
const userSchema = new mongoose.Schema({
  username: { 
    type: String, 
    required: true, 
    unique: true 
  },
  email: { 
    type: String, 
    required: true 
  },
  age: { 
    type: Number, 
    min: 18 // Validation logic!
  },
  
  // DENORMALIZATION: Embedding the array directly!
  // A user usually has < 5 addresses. Perfect for embedding.
  addresses: [{
    street: String,
    city: String
  }],
  
  createdAt: { 
    type: Date, 
    default: Date.now 
  }
});

// Create the Model
export const User = mongoose.model('User', userSchema);
```

### Basic CRUD Operations (Mongoose)

```javascript
// CREATE
const createUser = async () => {
  const newUser = await User.create({
    username: "john_doe",
    email: "john@example.com",
    age: 25,
    addresses: [{ street: "123 Main St", city: "NY" }] // Embedded document
  });
  console.log(newUser._id); // Prints the auto-generated ObjectId
};

// READ (Querying)
const findUsers = async () => {
  // Find users older than 20, select only the username field
  const users = await User.find({ age: { $gt: 20 } })
                          .select('username')
                          .limit(10);
                          
  // Searching INSIDE the embedded array! Extremely powerful.
  const nyUsers = await User.find({ "addresses.city": "NY" });
};

// UPDATE
const updateUser = async () => {
  // Find John and push a new address into his embedded array
  await User.updateOne(
    { username: "john_doe" }, 
    { $push: { addresses: { street: "456 Wall St", city: "NY" } } }
  );
};
```

### MongoDB Native Queries (Aggregation Pipeline)
When you need to do complex Math (like `GROUP BY` in SQL), MongoDB uses the Pipeline. Data flows from top to bottom.

```javascript
const analyzeUsers = async () => {
  const result = await User.aggregate([
    // Stage 1: Filter (WHERE age >= 18)
    { $match: { age: { $gte: 18 } } },
    
    // Stage 2: Group by City (Must Unwind the addresses array first!)
    { $unwind: "$addresses" },
    
    // Stage 3: Group by and Count
    { $group: { 
        _id: "$addresses.city", 
        totalUsers: { $sum: 1 } 
      } 
    },
    
    // Stage 4: Sort Descending
    { $sort: { totalUsers: -1 } }
  ]);
};
```

---

## Related Topics

- MongoDB is the "M" in the widely used MERN stack, alongside **[Node.js / Express](../backend/nodejs-express.md)** and **[React](../frontend/react.md)**.
- If your data has strict relationships and you need ACID guarantees, use **[PostgreSQL](./postgresql.md)** instead.
