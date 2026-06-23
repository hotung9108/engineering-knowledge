# Encryption vs. Hashing vs. Encoding

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trong thế giới bảo mật, người ta thường dùng nhầm lẫn 3 từ: Encoding, Encryption, và Hashing. Chúng hoàn toàn khác nhau.
> - **Encoding (Mã hóa định dạng)**: Biến chữ thành số để máy tính dễ đọc (Ai cũng có thể dịch ngược lại được).
> - **Encryption (Mã hóa bảo mật)**: Bỏ chữ vào két sắt và khóa lại (Chỉ người có Chìa Khóa mới mở ra xem lại được chữ ban đầu).
> - **Hashing (Băm)**: Bỏ chữ vào máy xay sinh tố và xay nát bét (Không một ai trên đời có thể ghép lại thành chữ ban đầu).

</details>

> **Summary**: A pervasive anti-pattern in Junior software engineering is conflating the distinct cryptographic concepts of Encoding, Encryption, and Hashing. They serve entirely different architectural purposes.
> - **Encoding (Base64)**: Transforms data formats for system compatibility. It provides absolutely zero security; anyone can instantly reverse it.
> - **Encryption (AES/RSA)**: Cryptographically locks data using Mathematical Keys. It provides extreme security and is fully Two-Way (Reversible) *only* if you possess the specific decryption key.
> - **Hashing (SHA-256/Bcrypt)**: A mathematical meat-grinder. It provides absolute security because it is strictly One-Way (Irreversible). It is physically impossible to mathematically reverse a hash back into its original text.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn có một Củ Khoai Tây (Dữ liệu).
1. **Encoding (Cắt hạt lựu)**: Củ khoai to quá, con nít không ăn được. Bạn lấy dao cắt hạt lựu nhỏ ra cho dễ nuốt. Nếu cần, bạn vẫn có thể dán keo ghép các hạt lựu lại thành củ khoai. (Ai cũng ghép được).
2. **Encryption (Khóa củ khoai trong két sắt)**: Củ khoai này bằng vàng. Bạn bỏ nó vào két sắt thép, khóa lại bằng mật mã `1234`. Kẻ gian ôm cái két sắt đi cũng không nhìn thấy củ khoai bên trong. Phải có chìa khóa mới lấy củ khoai ra được.
3. **Hashing (Bỏ vào máy xay sinh tố)**: Củ khoai này dính thuốc độc. Bạn không muốn ai ăn. Bạn ném nó vào máy xay, bấm nút xay thành một cốc nước màu vàng. Đưa cốc nước này cho 100 ông tiến sĩ giỏi nhất thế giới, không ông nào có thể biến cốc nước đó quay ngược trở lại thành củ khoai tây nguyên vẹn.

</details>

Imagine you possess a raw Potato (Your Data).
1. **Encoding (Dicing the Potato)**: The potato is too large to fit into a small pipe. You chop it into tiny cubes so it flows smoothly. Anyone who receives the cubes can easily glue them back together into the exact shape of the original potato. (No security).
2. **Encryption (Locking it in a Safe)**: This is a solid gold potato. You place it inside a titanium safe and lock it with a Master Key. A thief can steal the heavy safe, but they cannot see or touch the potato. Only the person holding the exact Master Key can unlock the safe and retrieve the pristine gold potato. (Two-way security).
3. **Hashing (The Blender)**: This potato contains a secret. You drop the potato into an industrial blender and liquefy it. You pour the resulting mush into a cup. You can hand this cup to the greatest mathematicians on Earth, and it is physically and biologically impossible for them to reconstruct the original raw potato from the liquid mush. (One-way verification).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Encoding (Ví dụ: Base64)**: Đổi bảng chữ cái. Máy tính đôi khi bị lỗi khi truyền ký tự có dấu qua mạng (Ví dụ chữ `ế`). Encoding sẽ biến chữ `ế` thành một chuỗi toàn tiếng Anh `eE==`. Sang đầu bên kia, máy tính tự dịch ngược `eE==` thành `ế`. Không có mật khẩu, ai cũng dịch được.
**2. Encryption (Ví dụ: AES, RSA)**: Mã hóa. Dùng một Thuật toán Toán học phức tạp kết hợp với 1 cái **Chìa khóa (Key)** để xáo trộn dữ liệu. 
   - *Symmetric (Đối xứng - AES)*: Dùng 1 chìa khóa chung để khóa và mở. (Giống khóa ổ khóa nhà).
   - *Asymmetric (Bất đối xứng - RSA)*: Dùng 2 chìa. Chìa Public để khóa, Chìa Private để mở.
**3. Hashing (Ví dụ: SHA-256, Bcrypt)**: Băm dữ liệu. Đầu vào là 1 đoạn văn bản dài 1000 trang, đầu ra luôn là 1 chuỗi ký tự dài chính xác 64 ký tự (Không hơn không kém). Đổi 1 dấu phẩy trong văn bản, chuỗi Hash thay đổi hoàn toàn 100%.

</details>

**1. Encoding (Base64, URL Encoding)**: Data translation. Protocols like HTTP struggle to reliably transmit binary data (like an Image) or special characters (spaces, unicode) across text-based networks. Encoding translates binary bytes into safe, printable ASCII text characters. It utilizes zero cryptographic keys. It is publicly reversible by design.
**2. Encryption (AES-256, RSA-2048)**: Data confidentiality. It algorithmically scrambles plaintext into unreadable Ciphertext utilizing a specific Cryptographic Key. 
   - *Symmetric (AES)*: Uses the exact same shared key to Lock and Unlock the data (Lightning fast, used for bulk data like Hard Drives).
   - *Asymmetric (RSA)*: Uses a Public Key to Lock, and a mathematically linked Private Key to Unlock (Slow, used for initial TLS Handshakes).
**3. Hashing (SHA-256, Bcrypt)**: Data integrity and fingerprinting. A mathematical algorithm that maps arbitrary input data (a 10GB movie) into a fixed-size deterministic string (a 64-character hash). A single bit change in the 10GB movie totally avalanches the resulting 64-character hash into something completely unrecognizable.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao phải Băm (Hash) Mật khẩu?**
Nếu bạn dùng Encryption (Mã hóa) để lưu mật khẩu khách hàng vào Database (`admin123` $\rightarrow$ `xZ91q`). Rất an toàn, nhưng nó có 2 chiều. Nghĩa là bạn (Lập trình viên) đang nắm trong tay Chìa Khóa để dịch ngược `xZ91q` thành `admin123`. Nếu bạn bị giang hồ kề dao vào cổ ép giao nộp Chìa Khóa, giang hồ sẽ giải mã được toàn bộ 1 triệu mật khẩu của khách.
**Giải pháp Hashing**: Bcrypt băm mật khẩu thành chuỗi rác (`$2a$10$xyz...`). Ngay cả chính bạn (Người viết code) cũng KHÔNG THỂ biết mật khẩu thật của khách là gì. Giang hồ có bắt được bạn cũng vô ích. Lúc khách hàng đăng nhập, ta đem chữ khách vừa gõ băm ra, nếu chuỗi rác khớp nhau $\rightarrow$ Đăng nhập thành công. Không ai biết mật khẩu gốc!

</details>

**The Absolute Necessity of One-Way Password Hashing**:
If you construct a system that uses Two-Way *Encryption* (AES) to store user passwords in the Database, you have engineered a catastrophic liability. You (the developer) must physically store the AES Decryption Key on the server to verify logins. If the server is compromised, the hacker steals both the Encrypted Database *and* the Decryption Key. They instantly decrypt 1 million plain-text passwords.
**The Hashing Solution**: By using Bcrypt, passwords are irreversibly ground into mathematical mush. You throw away the original password. Even if a hacker steals the Database, the hashes are useless. When a user logs in tomorrow, you hash their incoming text and compare the *two hashes*. The Server verifies identity without ever knowing or storing the actual plain-text secret.

---

## Layer 3: Without vs. With Comparison (Compare)

### Feature Matrix

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Bảng so sánh ngắn gọn để biết khi nào dùng công cụ nào.
</details>

Selecting the correct cryptographic tool for the architectural requirement.

| Feature | Encoding (Base64) | Encryption (AES) | Hashing (Bcrypt/SHA-256) |
|---|---|---|---|
| **Primary Goal** | Format compatibility (Data transmission) | Privacy & Secrecy | Integrity & Fingerprinting |
| **Security Level** | NONE (0%) | Extremely High | Absolute (Irreversible) |
| **Requires a Key?** | No | Yes (Symmetric or Asymmetric) | No (Uses automated algorithms) |
| **Output Length**| Proportional to input (Gets bigger) | Proportional to input | **Fixed Length** (Always identical size) |
| **Use Case** | Sending Image attachments in Email. | Protecting Credit Card numbers in DB. | Storing Passwords. Checking File integrity. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Ứng dụng của Hashing**: 
  - Lưu mật khẩu Database (Luôn dùng Bcrypt hoặc Argon2, tuyệt đối KHÔNG dùng MD5 vì nó đã bị hack nát).
  - Kiểm tra tải File: Khi bạn tải 1 cục file Game 100GB. Làm sao biết trong lúc tải mạng không bị rớt làm thiếu mất 1 Byte? Nhà phát hành sẽ cung cấp một chuỗi Hash (MD5/SHA-256). Tải xong, bạn tự băm cái file vừa tải ra, nếu chuỗi Hash khớp y chang $\rightarrow$ File tải hoàn hảo 100%.
- **Ứng dụng của Encryption (AES)**: Lưu thông tin cực kỳ nhạy cảm cần phải đọc lại được. Ví dụ: Số thẻ tín dụng, Tin nhắn Chat Zalo (Bọc bằng mã hóa Đầu-Cuối End-to-End).
- **Ứng dụng của Encoding**: Mã hóa chuỗi JWT Token (Phần Header và Payload của nó chỉ là Base64). Vì thế, ai cũng có thể đọc được nội dung của JWT Token! (Không được nhét mật khẩu vào JWT).

</details>

- **Hashing Use Cases**: 
  - **Password Storage**: Strictly utilize compute-heavy hashing algorithms with automated Salting (`Bcrypt`, `Argon2`). Never use `MD5` or `SHA-1` for passwords; modern GPUs can crack them in nanoseconds via Rainbow Tables.
  - **Checksums (Integrity Verification)**: When downloading an Ubuntu ISO file, the distributor provides an `SHA-256 Checksum`. You hash the downloaded ISO on your laptop. If your hash perfectly matches their hash, the 4GB file transferred over the chaotic internet without a single corrupted byte.
- **Encryption Use Cases (AES)**: Secure persistent storage for data that *must* be retrieved in plain-text later. E.g., Storing user Credit Card Numbers (PCI-DSS compliance requires strict AES-256 encryption at rest), or End-to-End Encrypted (E2EE) Chat messages (WhatsApp/Signal).
- **Encoding Use Cases (Base64)**: Serializing complex data. The entire payload structure of a standard JWT (JSON Web Token) is merely Base64 Encoded. It is entirely transparent. Anyone can decode a JWT payload in 1 second. (This is why you never store secrets inside a JWT).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Salting (Rắc thêm muối vào Hash)**: Hashing có một điểm yếu chết người tên là "Bảng Cầu Vồng" (Rainbow Table). Hacker có 1 bảng Excel liệt kê sẵn Hash của 1 tỷ mật khẩu thông dụng. Mật khẩu `123456` luôn ra chuỗi Hash là `e10adc...`. Thấy chuỗi này trong DB là hacker biết ngay pass là `123456`.
Giải pháp: Trước khi băm mật khẩu `123456`, hệ thống tự động sinh ra một chuỗi ngẫu nhiên (gọi là Salt - Muối), ví dụ `zX9`. Nó ghép lại thành `123456zX9` rồi mới băm. Kết quả ra chuỗi Hash hoàn toàn mới lạ. Kể cả 2 người cùng đặt pass `123456`, chuỗi Hash lưu trong DB sẽ khác nhau hoàn toàn do dính 2 hạt Muối khác nhau. (Thuật toán Bcrypt tự động làm việc này cho bạn).

</details>

1. **The Critical Importance of Cryptographic Salting**: Raw hashing algorithms (SHA-256) are deterministic. The string `password123` will *always* generate the exact same hash. Hackers pre-compute trillions of these hashes into massive lookup databases called "Rainbow Tables." If they steal your Database, they simply look up your hashes in their table and reverse them instantly.
**The Fix (Salting)**: A "Salt" is a cryptographically secure random string (e.g., `s9dfK!`) generated independently for every single user. The backend concatenates the Salt with the Password (`password123s9dfK!`) *before* applying the Hash. This permanently destroys the viability of Rainbow Tables. Modern libraries like `bcrypt` automatically generate and embed Salts internally.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Tự chế thuật toán Mã hóa (Custom Crypto)**: Lỗi kiêu ngạo lớn nhất của Dev. Nghĩ rằng mình giỏi toán nên tự viết hàm cộng trừ nhân chia để xáo trộn mật khẩu (Security by Obscurity). Chắc chắn 100% hacker sẽ phá được thuật toán tự chế đó trong 10 phút bằng toán học đảo ngược. LUÔN LUÔN dùng thư viện quốc tế đã được thế giới kiểm chứng (AES, Bcrypt). Tuyệt đối không tự phát minh bánh xe.
2. **Hardcode Encryption Key vào Github**: Dùng thuật toán AES-256 xịn nhất thế giới để mã hóa thẻ tín dụng. Nhưng lại gõ thẳng cái Chìa Khóa (Secret Key) vào file `config.js` rồi push lên kho Github Public. Thuật toán tỷ đô vô dụng nếu giấu chìa khóa dưới thảm chùi chân. Chìa khóa phải được lưu trong hệ thống chuyên biệt (AWS KMS, HashiCorp Vault) hoặc Biến môi trường (`.env`) không được push lên mạng.

</details>

1. **"Rolling Your Own Crypto" (Security by Obscurity)**: The most arrogant and fatal flaw a developer can make. Believing you can write a clever custom math function (e.g., bit-shifting characters and multiplying by prime numbers) to encrypt data. Professional cryptographers will shatter your custom algorithm in minutes utilizing differential cryptanalysis. **Absolute Rule**: Never invent cryptography. Strictly utilize robust, battle-tested, peer-reviewed industry standard libraries (libsodium, standard Bcrypt, AES-GCM).
2. **Hardcoding Encryption Keys (The Key Management Disaster)**: An engineer flawlessly implements AES-256 encryption, but carelessly commits the symmetric `ENCRYPTION_SECRET_KEY` directly into the `utils.js` source code pushed to GitHub. This is equivalent to installing a bank vault door but taping the combination code to the outside of the vault. **Fix**: Cryptographic keys must be externalized. They must reside exclusively in volatile memory injected via CI/CD Environment Variables, or strictly managed by Hardware Security Modules (AWS KMS, HashiCorp Vault).

---

## Related Topics

- For how encryption secures network traffic, see **[HTTP & HTTPS](../network/http-https.md)**.
- For how Encoding (Base64) is used in modern authentication, see **[Auth: OAuth & JWT](./auth-oauth-jwt.md)**.
- See how hackers bypass these if not implemented correctly in **[Web Security Vulnerabilities](./web-security.md)**.
