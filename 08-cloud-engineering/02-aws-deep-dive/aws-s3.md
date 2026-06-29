# AWS S3 (Simple Storage Service)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Dịch vụ lưu trữ lâu đời và vĩ đại nhất của AWS. Khám phá cách S3 lưu trữ Object (không phải ổ cứng vật lý), các hạng lưu trữ (Storage Classes) giúp tiết kiệm chi phí, và tại sao S3 lại là nền tảng của Data Lake.

</details>

> **Summary**: The oldest and most fundamental storage service in AWS. Explore how S3 stores Objects (not physical blocks), cost-saving Storage Classes, and why S3 forms the indestructible bedrock of modern Data Lakes.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **EBS (Ổ cứng của máy tính)**: Giống như một quyển vở nháp. Bạn có thể lật giở từng trang, tẩy xóa từng chữ một cách cực kỳ nhanh chóng. Rất tốt để cài hệ điều hành. Nhưng quyển vở này gắn liền với cái bàn (Máy chủ EC2).
- **S3 (Kho lưu trữ)**: Giống như một cái tủ cất tài liệu khổng lồ vô tận. Bạn bọc tài liệu vào một cái phong bì niêm phong (Object) rồi ném vào tủ. Bạn không thể "chỉnh sửa" một chữ trong phong bì. Muốn sửa, bạn phải kéo cái phong bì đó ra, xé đi, viết phong bì mới rồi nhét lại vào tủ. Đổi lại, cái tủ này chứa được tỷ tỷ phong bì, rẻ bèo, và không bao giờ mất đồ.

</details>

- **EBS (Block Storage)**: Like a spiral notebook. You can quickly flip to any page and erase or overwrite a single letter with a pencil. It's fast and perfect for running an Operating System. But the notebook is physically tied to a specific desk (EC2 instance).
- **S3 (Object Storage)**: Like an infinitely massive, indestructible filing cabinet. You place a document into a sealed envelope (an Object) and drop it in. You cannot "edit" a single word inside the envelope. To change it, you must pull the envelope out, destroy it, write a brand new envelope, and put it back. In exchange for this limitation, the cabinet has infinite space, costs pennies, and essentially never loses your files.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon S3 (Simple Storage Service)** là một dịch vụ lưu trữ đối tượng (Object Storage) cung cấp khả năng mở rộng hàng đầu trong ngành, tính khả dụng của dữ liệu, tính bảo mật và hiệu suất. 

**Thành phần cốt lõi:**
- **Bucket**: Giống như một thư mục gốc lớn. Tên Bucket phải là duy nhất trên TOÀN THẾ GIỚI (không ai khác được trùng tên với bạn).
- **Object**: Bất kỳ file nào (ảnh, video, file CSV). Kích thước từ 0 bytes đến 5 TB một file.
- **Key**: Là đường dẫn tuyệt đối của Object (ví dụ: `images/2024/photo.jpg`).
- **Metadata**: Thông tin đính kèm vào Object (ví dụ: `Content-Type: image/jpeg`).

</details>

**Amazon S3 (Simple Storage Service)** is an object storage service offering industry-leading scalability, data availability, security, and performance. 

**Core Components:**
- **Bucket**: The root container for objects. Bucket names must be GLOBALLY unique across all AWS accounts worldwide (like a domain name).
- **Object**: The fundamental entity (a file: an image, video, CSV, etc.). Ranging from 0 bytes to 5 Terabytes per object.
- **Key**: The absolute path/name of the object (e.g., `uploads/2024/jan/photo.jpg`). S3 is actually a flat structure; it does not have real "folders". The slashes in the Key just make it *look* like folders.
- **Metadata**: Name-value pairs attached to the object describing it (e.g., `Content-Type: image/jpeg`).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu bạn lưu ảnh người dùng tải lên vào ngay ổ cứng EBS của máy chủ EC2, bạn sẽ gặp 2 thảm họa:
1. **Hết dung lượng**: Một ngày nào đó ổ cứng 500GB sẽ đầy, server sẽ sập (Disk Full). Bạn phải lụi cụi gắn thêm ổ cứng mới.
2. **Khó chia sẻ**: Nếu bạn có 5 server chạy song song (Load Balancer), khách hàng upload ảnh vào Server 1. Lần sau khách truy cập lại bị Load Balancer đẩy vào Server 2. Máy 2 không có ảnh, khách sẽ thấy ảnh bị lỗi (404 Not Found).

S3 ra đời để tách phần "Lưu trữ" (Storage) ra khỏi phần "Xử lý" (Compute). S3 có dung lượng vô hạn (Infinite Storage) và tất cả các máy chủ EC2 đều có thể lấy ảnh từ S3 qua mạng.

</details>

If you store user uploads directly on the local EBS hard drive of your EC2 web server, you invite two architectural disasters:
1. **Running out of space**: Eventually, that 500GB drive will hit 100% capacity, crashing the server. You have to manually intervene, provision a larger drive, and copy the data.
2. **The Distributed State Problem**: If you autoscale to 5 Web Servers behind a Load Balancer, a user uploads an avatar to Server #1. On their next refresh, the Load Balancer routes them to Server #2. Server #2 doesn't have the file on its local disk! The image breaks (404 Not Found).

S3 was created to cleanly decouple Storage from Compute. S3 provides mathematically infinite storage capacity. All 5 Web Servers simply upload and download from the centralized S3 bucket via API calls, achieving stateless compute architectures.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Độ bền dữ liệu (Durability)**
- **Ổ cứng tại nhà**: Độ bền có thể là 99%. Một ngày đẹp trời bị chập điện, ổ cứng cháy, mất hết dữ liệu kỷ niệm gia đình.
- **AWS S3**: AWS thiết kế S3 để cung cấp độ bền 99.999999999% (11 số 9). Nếu bạn lưu 10,000,000 file trên S3, theo tính toán thống kê, phải mất 10,000 năm bạn mới bị mất một file. S3 tự động nhân bản file của bạn ra ít nhất 3 Data Center (AZ) khác nhau ngầm bên dưới.

</details>

### Durability vs. Availability
Understanding S3 requires understanding the difference between Durability (will my file be destroyed?) and Availability (can I download my file right now?).

- **Local Hard Drive**: Might have 99% Durability. A mechanical failure or a fire destroys the drive and the data is lost forever.
- **AWS S3 (Standard)**: Engineered for **99.999999999% (11 9's) of Durability**. If you store 10 million objects, you can expect to mathematically lose exactly ONE object every 10,000 years. Behind the scenes, S3 transparently replicates every file you upload across at least 3 geographically separated Availability Zones (Data Centers) before it returns a "Success" message to your API call.

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Static Website Hosting**: Bạn có thể host một website tĩnh (React/Vue/Angular build ra HTML/CSS/JS) trực tiếp trên S3 với chi phí chưa tới $1/tháng, không cần bất kỳ máy chủ EC2 nào!
2. **Data Lake (Hồ dữ liệu)**: Lưu trữ hàng Petabyte file CSV, Parquet, JSON thô. S3 là trái tim của hệ sinh thái Data Engineering. AWS Athena có thể dùng SQL để query trực tiếp dữ liệu nằm trong file S3.
3. **Backup & Archive (Sao lưu)**: Lưu trữ bản backup của Database mỗi đêm. Gửi các log cũ vào **S3 Glacier** để lưu trữ siêu rẻ dài hạn (nhưng mất vài tiếng mới lấy lại được).

**Không nên làm (Anti-patterns):**
- **Dùng S3 để lưu dữ liệu thay đổi liên tục**: S3 không phải là Database. Đừng dùng nó để lưu số dư tài khoản ngân hàng liên tục cộng trừ, vì S3 không sinh ra để "Sửa file" nhanh (nó là Object Storage, không phải Block Storage).

</details>

1. **Static Website Hosting**: You can host an entire React/Vue SPA (compiled to raw HTML/CSS/JS files) directly out of an S3 bucket for pennies a month. Pair it with AWS CloudFront (CDN) and you have a globally distributed, infinitely scalable frontend with exactly zero EC2 servers.
2. **The Modern Data Lake**: Storing Petabytes of raw structured and unstructured data (CSV, Parquet, JSON). S3 is the foundational bedrock of Data Engineering. Tools like AWS Athena or Databricks can run massive distributed SQL queries directly against files resting in S3 without loading them into a Database first.
3. **Archiving & Compliance**: Storing audit logs or database backups. Moving 5-year-old financial records into **S3 Glacier Deep Archive** (where storage costs fractions of a cent per GB, but data retrieval takes 12 hours).

### Anti-Patterns
- **Using S3 as an Active Database**: S3 is Object Storage, not Block Storage. If you need to continuously update a single cell (e.g., updating a user's wallet balance 10 times a second), S3 is a catastrophic choice. To change one byte in a 1GB file on S3, you must download the entire 1GB file, change the byte, and re-upload the entire 1GB file. Use Amazon RDS or DynamoDB for transactional updates.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Tối ưu chi phí bằng Storage Classes**
Đừng bao giờ để mọi thứ ở S3 Standard! Hãy dùng tính năng **S3 Lifecycle Rules** để tiết kiệm tiền:
- **S3 Standard**: Đắt nhất, dùng cho file hay truy cập (VD: Ảnh đại diện).
- **S3 Standard-IA (Infrequent Access)**: Rẻ hơn một nửa. Dùng cho file ít khi mở (VD: Hóa đơn tháng trước). Truy cập vẫn nhanh nhưng sẽ bị tính thêm "phí mở file".
- **S3 Glacier**: Rẻ như cho. Dùng cho dữ liệu lưu trữ bắt buộc theo luật (ví dụ log 5 năm). Muốn tải về phải chờ 3-12 tiếng.

**2. Pre-signed URLs (Đường dẫn tải file an toàn)**
Nếu bucket của bạn là Private, người ngoài không thể tải ảnh. Nhưng nếu bạn muốn bán một cuốn Ebook, người dùng mua xong bạn phải cho họ tải sách.
Bạn dùng code Backend (tài khoản có quyền) để tạo ra một **Pre-signed URL** (Đường dẫn ký tên sẵn). Đường link này cho phép ai có nó được quyền tải file đó, và đường link SẼ TỰ HỦY sau 5 phút!

</details>

### 1. Cost Optimization via Storage Classes & Lifecycle Rules
Never leave all your data sitting blindly in S3 Standard forever; it will drain your budget. Configure **S3 Lifecycle Rules** to automatically transition objects:
- **S3 Standard**: Default, expensive. Millisecond access. For active assets.
- **S3 Standard-IA (Infrequent Access)**: 50% cheaper storage, but charges a retrieval fee per GB. For data accessed less than once a month (e.g., 3-month-old reports).
- **S3 Glacier Flexible Retrieval / Deep Archive**: Extremely cheap (fractions of a penny per GB). For compliance and audit logs. *Trade-off*: Data retrieval is asynchronous and can take between 3 to 12 hours!

### 2. S3 Pre-signed URLs (Secure Sharing)
By default, your S3 bucket should be strictly Private. But what if a user purchases a digital MP3, and you need to let them download it directly from S3 without passing the heavy file through your backend EC2 server?
Use **Pre-signed URLs**. Your backend (which has IAM permissions) cryptographically signs a URL granting access to a specific object. You set an expiration (e.g., 15 minutes). You give this URL to the client's browser. The client downloads directly from S3 safely. After 15 minutes, the URL self-destructs.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là đoạn code Python (dùng thư viện Boto3) để tạo một Pre-signed URL an toàn. Đây là một pattern kinh điển trong phát triển Backend.

</details>

### Generating a Pre-Signed URL (Python / Boto3)

This is the standard architectural pattern for allowing users to download or upload files securely without making the bucket public.

```python
import boto3
from botocore.exceptions import ClientError

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL to share an S3 object securely.
    :param bucket_name: string
    :param object_name: string (The key of the file)
    :param expiration: Time in seconds for the presigned URL to remain valid (Default 1 hour)
    :return: Presigned URL as string. If error, returns None.
    """
    # Create an S3 client. (It automatically uses the IAM Role attached to the EC2/Lambda)
    s3_client = boto3.client('s3')
    
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None

    # Return the secure URL to the frontend React/Mobile App
    return response

# Example output:
# https://my-bucket.s3.amazonaws.com/report.pdf?AWSAccessKeyId=AKIA...&Expires=1630000&Signature=abcd...
```

---

## Related Topics

- [AWS IAM](./aws-iam.md) — How to write Bucket Policies to restrict who can read/write to S3.
- [AWS CloudFront](./aws-cloudfront-and-route53.md) — Using a CDN to cache S3 assets globally to reduce latency.
- [Data Lakehouse Architectures](../../06-data-engineering/04-data-storage/lakehouse-and-acid-transactions.md) — How Data Engineers use S3 to build massive Data Lakes.
