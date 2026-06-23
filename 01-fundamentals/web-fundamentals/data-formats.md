# Data Formats: JSON, XML, YAML, and Protobuf

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Khi Frontend (Browser) muốn gửi dữ liệu cho Backend (Server) qua mạng, chúng không thể gửi nguyên một Object trong bộ nhớ RAM qua được. Chúng phải "ngôn ngữ hóa" Object đó thành một chuỗi ký tự (Serialization). Các chuẩn như **JSON, XML, YAML** ra đời để quy định cách viết chuỗi ký tự đó sao cho máy tính hiểu được. Đặc biệt, **Protocol Buffers (Protobuf)** là chuẩn nén dữ liệu siêu tốc của Google dành riêng cho hệ thống lớn.

</details>

> **Summary**: When disparate software systems (e.g., a React Frontend and a Java Backend) communicate over a network, they cannot transmit raw physical memory objects. The objects must be strictly encoded into a standardized byte stream (**Serialization**) and decoded on the other end (**Deserialization**). **JSON, XML, and YAML** are the dominant human-readable text formats, while **Protocol Buffers (Protobuf)** represents the modern standard for ultra-fast, machine-readable binary compression.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang mô tả hình dáng một con Mèo cho một người mù (Serialization).
- **XML**: Giống như nói chuyện kiểu bộ máy hành chính nhà nước, cực kỳ dài dòng, thủ tục lằng nhằng: *"Bắt đầu con mèo. Bắt đầu màu lông. Màu Đen. Kết thúc màu lông. Kết thúc con mèo."*
- **JSON**: Giống như nói chuyện kiểu kỹ sư, gọn gàng và có ngoặc nhọn: `{"Con Mèo": {"Màu Lông": "Đen"}}`.
- **YAML**: Giống như viết thơ. Vứt hết ngoặc nhọn đi, dùng phím Space (khoảng trắng) để lùi đầu dòng. Cực kỳ dễ đọc.
- **Protobuf**: Giống như mật mã quân sự. Bạn nói `010`. Đối phương tự hiểu `0` là Mèo, `1` là Lông, `0` là Đen. Siêu ngắn, siêu bảo mật, nhưng người ngoài nghe không hiểu gì cả.

</details>

Imagine you must accurately describe a specific Cat to a blindfolded person over the radio (Serialization).
- **XML**: Like a bureaucratic government document. Highly verbose and repetitive. *"Start of Cat. Start of Fur Color. Black. End of Fur Color. End of Cat."*
- **JSON**: Like an engineer. Clean, structured, using curly braces. `{"Cat": {"FurColor": "Black"}}`.
- **YAML**: Like writing a poem. You delete all the ugly braces and quotes, relying purely on indentation (Spaces) to organize the structure. Visually beautiful.
- **Protobuf**: Like sending a military encrypted morse code. You just send `010`. The receiving officer has a codebook (Schema) that translates `0` to Cat, `1` to Fur, `0` to Black. Blazingly fast, but unreadable to civilians.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **XML (eXtensible Markup Language)**: Đẻ ra từ những năm 90. Dùng cặp thẻ mở/đóng `<tag></tag>` y hệt HTML.
- **JSON (JavaScript Object Notation)**: Vua của Web API hiện đại. Dùng `{ "key": "value" }`. Được xây dựng dựa trên cú pháp Object của ngôn ngữ JavaScript.
- **YAML (YAML Ain't Markup Language)**: Vua của file cấu hình (Config). Bỏ hết các dấu ngoặc `{}` và `""`. Sử dụng Indentation (lùi dòng bằng dấu cách) để thể hiện cấu trúc phân cấp.
- **Protobuf (Protocol Buffers)**: Do Google đẻ ra. Thay vì truyền bằng Text (chữ), nó biên dịch cấu trúc dữ liệu thành mã Nhị phân (Binary 0 và 1).

</details>

- **XML (eXtensible Markup Language)**: The legacy giant of the 1990s Enterprise. It relies on verbose opening and closing tags `<tag></tag>` structurally identical to HTML.
- **JSON (JavaScript Object Notation)**: The undisputed King of modern REST APIs. It is a lightweight, text-based data interchange format built upon JavaScript Object literal syntax `{"key": "value"}`.
- **YAML (YAML Ain't Markup Language)**: The undisputed King of Configuration Files (DevOps/Docker/Kubernetes). It violently strips away noisy curly braces and quotes, relying entirely on strict whitespace indentation to denote hierarchy.
- **Protobuf (Protocol Buffers)**: Google's open-source, language-neutral data serialization mechanism. Unlike the previous three, Protobuf is NOT text. It violently compiles data into dense, unreadable **Binary** payloads.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao JSON thay thế XML?**
XML quá nặng. Để gửi chữ "John", XML phải viết `<name>John</name>` (17 bytes). JSON chỉ viết `"name":"John"` (13 bytes). Trình duyệt cũng phải rất vất vả (tốn CPU) để dịch cái đống thẻ `<tag>` của XML, trong khi JSON thì trình duyệt Web (chạy Javascript) nhắm mắt cũng đọc được `JSON.parse()` siêu nhanh.

**Tại sao lại sinh thêm Protobuf?**
Khi bạn có 10,000 Microservices gọi nhau bằng JSON, tốc độ nén/giải nén (parse) chữ Text làm CPU máy chủ bị quá tải. Gói tin chữ Text truyền qua cáp quang cũng rất tốn băng thông. Protobuf ép kiểu dữ liệu chặt chẽ và chuyển thành mã nhị phân siêu nhỏ. Tiết kiệm 50% CPU và 60% băng thông mạng.

</details>

**Why did JSON assassinate XML?**
XML suffers from catastrophic verbosity. To transmit the string "John", XML requires `<name>John</name>` (17 bytes payload). JSON requires `"name":"John"` (13 bytes). Furthermore, parsing XML trees in a Web Browser requires heavy DOM-like traversals, whereas JSON is literally native JavaScript. Browsers can execute `JSON.parse()` natively in C++ instantly.

**Why invent Protobuf if JSON is so good?**
JSON is fantastic for Browser-to-Server communication. However, in a colossal backend architecture featuring 1,000 Microservices talking to each other internally (Server-to-Server), the CPU overhead of constantly parsing raw Strings into Objects (`JSON.parse`) becomes an astronomical bottleneck. Protobuf enforces a strict Schema and compiles objects down to pure Binary bytes, slashing network payload size by 60% and deserialization CPU time by magnitudes.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Cùng biểu diễn một cấu trúc dữ liệu người dùng (User) trên 4 định dạng khác nhau.
</details>

Comparing the exact same User Object across four different structural paradigms.

### 1. XML (The Verbose Legacy)
*Painful to read, massive file size.*
```xml
<user>
    <id>101</id>
    <name>John Doe</name>
    <roles>
        <role>Admin</role>
        <role>User</role>
    </roles>
</user>
```

### 2. JSON (The REST Standard)
*Clean, readable, but heavy on braces/quotes.*
```json
{
  "user": {
    "id": 101,
    "name": "John Doe",
    "roles": ["Admin", "User"]
  }
}
```

### 3. YAML (The DevOps Standard)
*Beautifully minimalist. Quotes are optional. Lists use hyphens.*
```yaml
user:
  id: 101
  name: John Doe
  roles:
    - Admin
    - User
```

### 4. Protocol Buffers (The Performance King)
*Requires a pre-defined Schema (`.proto` file). The actual data sent over the wire is unreadable binary `0A 08 4A 6F...`*
```protobuf
// The Schema defining the contract
message User {
  int32 id = 1;
  string name = 2;
  repeated string roles = 3;
}
```

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **JSON**: Dùng cho MỌI REST API trả về dữ liệu cho ứng dụng Web/Mobile Frontend. Lưu trữ dữ liệu lỏng lẻo trong NoSQL Database (MongoDB).
- **YAML**: Dùng để viết file cấu hình hạ tầng. Ví dụ: File chạy Docker (`docker-compose.yml`), file thiết lập Kubernetes (`deployment.yaml`), GitHub Actions Pipeline.
- **XML**: Vẫn còn sống ngắc ngoải ở các hệ thống ngân hàng cổ đại (SOAP APIs), hoặc trong các file cấu hình giao diện Android cũ, cấu hình Maven Java (`pom.xml`).
- **Protobuf**: Dùng riêng cho kiến trúc gRPC. Các Microservice (Backend gọi Backend) bắt buộc phải dùng Protobuf để đạt tốc độ tối đa.

</details>

- **JSON Domain**: The universal lingua franca of Public API endpoints. Any architecture delivering data to a Frontend Web Browser or iOS/Android application defaults to JSON REST APIs. Also serves as the core data structure for Document NoSQL Databases (e.g., MongoDB, ElasticSearch).
- **YAML Domain**: Infrastructure as Code (IaC) and Configuration engineering. Writing nested configurations in JSON is a nightmare because JSON forbids code comments (`//`) and requires strict quoting. YAML supports comments and minimalist syntax, making it the supreme choice for `docker-compose.yml`, Kubernetes manifests, and CI/CD Pipeline definitions.
- **XML Domain**: Legacy Enterprise architectures. Still heavily prevalent in aging Banking/Fintech systems executing SOAP APIs, Java Spring configurations, Maven build scripts (`pom.xml`), and legacy Android UI layouts.
- **Protobuf Domain**: High-performance internal Microservice meshes. If an authentication microservice needs to rapidly communicate with a payment microservice inside a private subnet, they will utilize gRPC over HTTP/2, serializing binary data strictly via Protobuf.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiểu giới hạn số của JSON**: Chuẩn JSON không phân biệt Integer hay Float, nó chỉ có kiểu `Number`. Nguy hiểm nhất: Nếu bạn gửi một ID ID dạng `Long` rất lớn (Ví dụ ID của Twitter/Snowflake: `9007199254740993`), khi Javascript dịch ra, nó sẽ bị sai lệch số vì giới hạn số chuẩn trong JS nhỏ hơn Java. Cách giải quyết: ID lớn phải luôn gửi bằng chuỗi ký tự Text (String `""`) thay vì Number.
2. **Luôn Linter file YAML**: YAML dùng khoảng trắng (Space) để lùi dòng. Dùng phím `Tab` là chết ngắc. Hãy cài Extension Linting trong VSCode để nó báo lỗi nếu bạn lùi dư 1 dấu Space.

</details>

1. **Beware the JSON 64-bit Number Trap**: JSON's specification fundamentally lacks a strict type system for numeric precision; a `Number` is just a double-precision float. If a Java Backend transmits a colossal 64-bit Long ID (e.g., a Twitter Snowflake ID `9007199254740993`), the JavaScript Frontend parser (`JSON.parse`) will physically lose precision and round the number, causing massive data corruption. **Golden Rule**: Always serialize massive identifiers as `"Strings"`.
2. **Strict YAML Linting**: YAML's aesthetic reliance on whitespace is its Achilles' heel. Mixing `Tab` characters with `Space` characters, or misaligning an indentation by a single space, will silently break Kubernetes deployments or crash CI/CD pipelines. Enforce strict YAML Linting extensions (e.g., Prettier) in your IDE.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Thừa thãi dữ liệu (Over-fetching) trong JSON API**: Khi Frontend gọi API `GET /users/1`, Backend ném lại nguyên một cục JSON nặng 2MB chứa cả danh sách 100 bài viết, mật khẩu mã hóa, ngày tháng năm sinh... Dẫn đến sập băng thông mạng. (Giải pháp: Dùng GraphQL hoặc DTO để lọc bớt JSON).
2. **Nhét logic mã hóa vào Protobuf**: Protobuf mã hóa dữ liệu thành nhị phân (Binary), nó rất khó đọc đối với mắt người, nhưng KHÔNG HỀ BẢO MẬT. Bất kỳ ai bắt được gói tin cũng dịch ngược lại được nếu họ có file `.proto`. Muốn bảo mật phải dùng TLS/SSL.

</details>

1. **JSON Payload Bloat (Over-fetching)**: A backend developer aggressively serializes a heavily nested Database Entity (e.g., eager-fetching all user relationships) directly to JSON. The REST API endpoint subsequently vomits a 5MB JSON payload over the wire, destroying mobile client bandwidth. Always map DB Entities to strict Data Transfer Objects (DTOs) before JSON serialization.
2. **Conflating Protobuf Encoding with Encryption**: A devastating security illusion. Because Protobuf payloads look like unintelligible binary garbage (`0A 0B 4C...`), junior developers assume the data is securely encrypted. **It is not**. It is merely encoded. Anyone intercepting the payload can easily reverse-engineer and decode the raw data. Sensitive data over gRPC must still be encrypted in transit via standard TLS.

---

## Related Topics

- To see how XML and JSON are transmitted over the web, review **[HTTP & HTTPS](../network/http-https.md)**.
- To see how Protobuf empowers modern Microservices, explore **[gRPC](../network/grpc.md)**.
- See how JSON structures inspired document databases in **[NoSQL Fundamentals](../database/nosql-fundamentals.md)**.
