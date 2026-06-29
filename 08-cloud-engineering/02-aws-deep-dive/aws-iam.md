# AWS Identity and Access Management (IAM)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: IAM là trái tim của bảo mật trên AWS. Tìm hiểu cách quản lý quyền truy cập bằng Users, Groups, Roles và Policies, nguyên tắc Đặc quyền tối thiểu (Least Privilege), và cách các dịch vụ của AWS "nói chuyện" với nhau một cách an toàn.

</details>

> **Summary**: IAM is the heart of AWS security. Learn how to manage access using Users, Groups, Roles, and Policies, the principle of Least Privilege, and how AWS services securely communicate with each other.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng AWS là một tòa nhà văn phòng khổng lồ (Công ty của bạn).
- **User (Người dùng)**: Là nhân viên có thẻ nhân viên in tên họ (Tài khoản để đăng nhập).
- **Group (Nhóm)**: Tưởng tượng thẻ nhân viên được phân loại theo màu. Nhóm Kế toán thẻ vàng, nhóm IT thẻ xanh.
- **Policy (Quy định/Chính sách)**: Là một tờ giấy viết rõ: "Người cầm thẻ xanh được phép mở cửa phòng Máy chủ, không được mở két sắt". Bạn dán tờ giấy này vào thẻ của nhân viên IT, hoặc dán vào cả Nhóm IT.
- **Role (Vai trò / Mặt nạ)**: Khác với User là người thật, Role giống như một cái "Mặt nạ". Một con Robot dọn vệ sinh (ví dụ: máy chủ EC2) không có thẻ nhân viên. Nó cần mượn cái "Mặt nạ lao công" để được phép vào phòng đổ rác (S3 Bucket). Khi xong việc, nó cởi mặt nạ ra.

</details>

Imagine AWS is a massive office building (Your Company).
- **User**: An employee with a named ID badge (Login credentials).
- **Group**: Categorizing ID badges by department. The Accounting team gets yellow badges, the IT team gets blue badges.
- **Policy**: A piece of paper that dictates the rules: "The bearer of this blue badge is ALLOWED to open the Server Room, but DENIED access to the Safe". You attach this paper to a User or a Group.
- **Role**: Unlike a User (a real person), a Role is like a "Temporary Hat or Mask". A cleaning robot (e.g., an EC2 server) doesn't have an ID badge. It needs to put on the "Janitor Hat" to be allowed into the trash room (S3 Bucket). When it's done, it takes the hat off.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**AWS IAM (Identity and Access Management)** là một dịch vụ web giúp bạn kiểm soát truy cập vào các tài nguyên AWS một cách an toàn. Bạn sử dụng IAM để xác thực (Authentication - Người này là ai?) và cấp quyền (Authorization - Người này được làm gì?).

**Thành phần cốt lõi:**
1. **IAM Identity**: Bao gồm Users (Người thật), Groups (Nhóm users), và Roles (Quyền tạm thời cho máy móc hoặc ứng dụng).
2. **IAM Policy**: Một tài liệu JSON định nghĩa rõ ràng các quyền (Allow/Deny) đối với các hành động (Actions) trên các tài nguyên cụ thể (Resources).

**Phân loại:**
- **Loại**: Bảo mật (Security & Identity).
- **Đặc tính**: Dịch vụ Toàn cầu (Global Service) - IAM không gắn với một Region cụ thể nào.

</details>

**AWS IAM (Identity and Access Management)** is a web service that helps you securely control access to AWS resources. You use IAM to handle Authentication (Who is this?) and Authorization (What are they allowed to do?).

**Core Components:**
1. **IAM Identity**: Includes Users (human accounts), Groups (collections of users), and Roles (temporary credentials assumed by AWS services or federated users).
2. **IAM Policy**: A JSON document that explicitly defines the permissions (Allow/Deny) for specific actions across specific resources.

### Classification
- **Type**: Security & Identity.
- **Property**: Global Service (IAM is not tied to a specific AWS Region; it applies globally).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi bạn tạo tài khoản AWS, bạn nhận được một tài khoản gọi là **Root User**. Root User giống như "Chúa tể" - nó có quyền xóa toàn bộ công ty, đổi thẻ tín dụng, hủy tài khoản. 
Nếu bạn đưa mật khẩu Root User cho 10 lập trình viên trong công ty dùng chung, một người lỡ tay (hoặc cố ý) có thể xóa sạch toàn bộ Database và hạ tầng của công ty. Bạn cũng không biết ai là người đã làm việc đó!

IAM ra đời để bạn có thể:
1. Khóa tài khoản Root lại và vứt chìa khóa đi (Bật MFA và cất đi).
2. Tạo cho mỗi nhân viên một IAM User riêng biệt với quyền hạn chỉ vừa đủ để làm việc (Nguyên tắc Đặc quyền tối thiểu - Least Privilege).
3. Cho phép các dịch vụ AWS giao tiếp với nhau mà không cần giấu mật khẩu trong source code (Dùng IAM Roles).

</details>

When you first create an AWS account, you get the **Root User**. The Root User is "God"—it has absolute power to delete everything, change billing details, and close the account.
If you share the Root User password with 10 developers, someone could accidentally (or maliciously) delete your production Database. Furthermore, you would have no idea *who* did it because everyone used the same login!

IAM exists so you can:
1. Lock away the Root User (enable MFA and never use it again).
2. Create individual IAM Users for every employee with permissions strictly limited to what they need for their job (**Principle of Least Privilege**).
3. Allow AWS services to communicate securely without hardcoding passwords in your application source code (by using IAM Roles).

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Bài toán**: Một ứng dụng Python chạy trên máy chủ EC2 cần lấy file ảnh từ S3 Bucket.

- **Không có IAM Roles**: Lập trình viên phải tạo một IAM User, lấy `Access_Key` và `Secret_Key` (Mật khẩu), rồi ghi cứng (hardcode) mật khẩu này vào file `.env` hoặc source code trên máy chủ EC2. Nếu hacker hack được EC2 hoặc xem được Github, họ lấy được mã khóa và trộm toàn bộ dữ liệu S3.
- **Có IAM Roles**: Lập trình viên tạo một IAM Role cấp quyền đọc S3, rồi "gắn" Role đó vào cái máy chủ EC2. Trong code Python, hoàn toàn không có mật khẩu nào cả! Boto3 (AWS SDK) tự động liên hệ hệ thống ẩn của EC2 để lấy "Mặt nạ tạm thời" (Temporary credentials) xoay vòng mỗi vài giờ. Hacker dù có chép được source code cũng không tìm thấy mật khẩu nào để đánh cắp.

</details>

### Without IAM Roles (Dangerous - Hardcoded Credentials)
```python
import boto3

# TERRIBLE IDEA: Hardcoding long-term credentials in your code or config files.
# If this code leaks to GitHub, hackers will compromise your AWS account in seconds.
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAIOSFODNN7EXAMPLE', 
    aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
)

s3_client.download_file('my-bucket', 'image.jpg', 'local.jpg')
```

### With IAM Roles (Secure - Temporary Credentials)
```python
import boto3

# BEST PRACTICE: Zero credentials in the code.
# The EC2 instance assumes an IAM Role attached to it. The AWS SDK automatically 
# retrieves rotating, temporary credentials in the background.
s3_client = boto3.client('s3')

s3_client.download_file('my-bucket', 'image.jpg', 'local.jpg')
```

| Feature | IAM User | IAM Role |
|---|---|---|
| **Identity Type** | Long-term credentials (Password / Access Keys) | Short-term, temporary credentials |
| **Who uses it?** | Human beings (Developers, Admins) | Machines (EC2, Lambda) or Federated external users |
| **Security Risk** | High (Keys can be leaked or stolen) | Extremely Low (Keys expire automatically) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Ủy quyền dịch vụ (Service Roles)**: Bạn viết 1 hàm Lambda. Hàm này cần đọc DynamoDB. Bạn tạo 1 Role cấp quyền `dynamodb:GetItem`, rồi gắn Role đó cho hàm Lambda.
2. **Cross-Account Access (Truy cập chéo tài khoản)**: Công ty có 2 tài khoản AWS (Dev và Prod). Một dev đang dùng tài khoản Dev muốn kiểm tra S3 ở Prod. Thay vì tạo user mới, họ "Assume Role" (Mượn mặt nạ) từ Prod sang Dev.
3. **SSO / Federation (Đăng nhập 1 lần)**: Công ty dùng Microsoft Active Directory. Thay vì tạo hàng ngàn IAM User thủ công, AWS IAM có thể liên kết (Federate) với Microsoft. Nhân viên dùng tài khoản email công ty để đăng nhập thẳng vào AWS (thông qua việc Assume một IAM Role).

**Cảnh báo (Anti-patterns):**
- **Sử dụng quyền `AdministratorAccess` bừa bãi**: Đừng bao giờ cấp quyền Admin cho lập trình viên mới hoặc cho hệ thống EC2 chỉ vì bạn lười cấu hình JSON Policy! Hãy tuân thủ Least Privilege.

</details>

1. **Service Delegation (IAM Roles for Services)**: You deploy an AWS Lambda function that needs to read from DynamoDB. You create a Role with the `dynamodb:GetItem` permission and attach it to the Lambda function.
2. **Cross-Account Access**: Your company has separate AWS accounts for `Dev` and `Prod`. A developer logged into `Dev` temporarily needs to read a bucket in `Prod`. Instead of creating a new IAM User in `Prod`, the developer explicitly "Assumes a Role" (borrows permissions) established between the two accounts.
3. **Identity Federation (SSO)**: The enterprise uses Microsoft Active Directory (or Okta). Instead of creating hundreds of IAM Users, you configure Federation. Employees log in with their corporate email, which maps them to assume a specific IAM Role in AWS automatically.

### Anti-Patterns
- **Using `AdministratorAccess` out of laziness**: Never assign the full `AdministratorAccess` policy to junior developers or to an EC2 instance just because you are too lazy to figure out the exact JSON Policy required. Violating the Principle of Least Privilege is the fastest way to suffer a catastrophic data breach.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Hiểu rõ cấu trúc IAM Policy (Quyết định Sống còn):**
Một Policy bắt buộc phải có `Effect` (Allow/Deny), `Action` (Hành động gì), và `Resource` (Trên cái gì).
**Bí kíp**: Đừng bao giờ dùng dấu `*` ở Resource nếu không thực sự cần thiết. `Resource: "*"` nghĩa là cấp quyền cho TẤT CẢ mọi S3 bucket trên thế giới thuộc tài khoản của bạn. Hãy ghi đích danh ARN của bucket đó: `Resource: "arn:aws:s3:::my-secret-bucket"`.

**2. IAM Policy Evaluation Logic (Thứ tự ưu tiên):**
Khi AWS quyết định cho phép bạn làm gì đó không, nó xét theo quy tắc:
1. Mặc định mọi thứ là **DENY** (Bị cấm).
2. Nếu có một luật nào đó ghi rõ **Explicit DENY** (Cấm tuyệt đối), thì TẤT CẢ các luật Allow đều bị vô hiệu hóa. Deny luôn chiến thắng Allow!
3. Nếu không có Explicit Deny, và có một luật **ALLOW**, thì yêu cầu được chấp nhận.

**3. IAM Policy Simulator:**
Đừng ngồi đoán xem Policy của bạn có chạy đúng không. AWS cung cấp công cụ *IAM Policy Simulator* trên Web Console để bạn test thử xem User X có quyền làm Hành động Y trên Resource Z hay không trước khi áp dụng vào thực tế.

</details>

### 1. Mastering the IAM Policy Structure (PARC)
Every policy evaluates the Principal, Action, Resource, and Condition.
**Golden Rule**: Avoid using the wildcard `*` in the `Resource` block. Writing `"Action": "s3:GetObject", "Resource": "*"` grants access to download files from *every single bucket* in your AWS account. Always strictly define the Amazon Resource Name (ARN): `"Resource": "arn:aws:s3:::my-production-bucket/*"`.

### 2. Policy Evaluation Logic (The Deny override)
When AWS evaluates permissions, it follows a strict logical flow:
1. By default, all requests are implicitly **DENIED**.
2. If there is an **Explicit DENY** anywhere in the attached policies, it overrides EVERYTHING. Deny *always* wins against Allow!
3. If there is no explicit Deny, and there is at least one **Explicit ALLOW**, the request is granted.

### 3. Avoid long-term Access Keys
For automated CI/CD pipelines (like GitHub Actions deploying to AWS), do NOT generate long-lasting IAM User Access Keys. Instead, use **OIDC (OpenID Connect)**. GitHub Actions will dynamically request a short-lived temporary token from AWS IAM, completely eliminating the risk of leaked keys.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một tài liệu JSON IAM Policy chuẩn mực. Thay vì cấp quyền `s3:*` nguy hiểm, Policy này chỉ cấp ĐÚNG quyền cần thiết để tải file lên và xem danh sách file trong một thư mục cụ thể của một bucket cụ thể.

</details>

### A Best-Practice Least Privilege IAM Policy (JSON)

This policy adheres strictly to the Principle of Least Privilege. It grants read/write access ONLY to a specific sub-folder (`/uploads/`) inside a specific bucket (`my-company-assets`), rather than the whole AWS account.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListingSpecificBucketFolder",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-company-assets"
      ],
      "Condition": {
        "StringLike": {
          "s3:prefix": [
            "uploads/*"
          ]
        }
      }
    },
    {
      "Sid": "AllowUploadingToSpecificFolder",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-company-assets/uploads/*"
      ]
    }
  ]
}
```

---

## Related Topics

- [Cloud Computing Models](../01-cloud-fundamentals/cloud-computing-models.md) — How the Shared Responsibility Model necessitates IAM.
- [AWS EC2](./aws-ec2.md) — How Virtual Machines assume IAM Roles to access other services securely.
- [AWS S3](./aws-s3.md) — The target resource most commonly protected by IAM Policies.
