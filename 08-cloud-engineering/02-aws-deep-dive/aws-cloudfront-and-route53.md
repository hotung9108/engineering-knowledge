# AWS CloudFront & Route 53

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Bộ đôi quyền lực kiểm soát lưu lượng truy cập toàn cầu. Tìm hiểu cách Route 53 điều hướng tên miền (DNS) và cách CloudFront (Mạng phân phối nội dung - CDN) mang trang web của bạn đến gần người dùng ở mọi quốc gia để tải trang trong chớp mắt.

</details>

> **Summary**: The global traffic control powerhouse duo. Discover how Route 53 translates Domain Names (DNS) into IP addresses, and how CloudFront (Content Delivery Network - CDN) brings your website physically closer to users in every country for lightning-fast loading.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn mở một tiệm Bánh Pizza cực ngon ở New York (Máy chủ AWS đặt ở Mỹ).
- **Route 53 (Danh bạ điện thoại)**: Một khách hàng muốn mua bánh, họ chỉ nhớ tên tiệm "PizzaNgon.com" (Tên miền), họ không thể nhớ số điện thoại (Địa chỉ IP: `192.168.1.5`). Route 53 chính là cuốn danh bạ, nó tự động dịch tên tiệm thành số điện thoại để khách có thể gọi đến tiệm.
- **Vấn đề địa lý**: Tiệm bánh (Máy chủ) ở Mỹ. Nếu một khách ở Việt Nam gọi đặt bánh, phải mất 30 tiếng bánh mới ship tới nơi (Độ trễ - Latency). Khách ăn bánh bị nguội, họ rất bực.
- **CloudFront (Mạng lưới nhượng quyền - CDN)**: Bạn không xây 1 tiệm to, bạn thuê AWS mở 400 tiệm bánh nhỏ xíu (Edge Locations) ở khắp các nước trên thế giới. Mỗi ngày bạn gửi công thức và làm sẵn bánh (Cache file tĩnh) để tủ lạnh ở 400 tiệm đó. Bây giờ, khách ở Việt Nam đặt bánh, tiệm bánh ở Việt Nam sẽ giao luôn cho khách trong 5 phút. Nhanh, nóng giòn, và tiệm chính ở Mỹ không bị quá tải!

</details>

You open an incredibly delicious Pizza Shop in New York (Your AWS Web Server hosted in US-East).
- **Route 53 (The Phonebook/DNS)**: A customer wants pizza. They only remember the name "DeliciousPizza.com" (Domain Name); they cannot memorize the phone number (IP Address: `192.168.1.5`). Route 53 is the phonebook that translates the human-readable name into the computer-readable IP address so the browser can connect.
- **The Geography Problem**: The kitchen (Server) is in America. If a customer in Vietnam orders a pizza, it takes 30 hours to ship it across the ocean (High Network Latency). The pizza is cold, and the customer is angry (Slow website).
- **CloudFront (The Franchise Network/CDN)**: Instead of one massive kitchen, you hire AWS to open 400 tiny franchise kiosks (Edge Locations) in cities all over the world. You send your pizza recipe and pre-baked pizzas (Cached static files) to these kiosks. Now, when a user in Vietnam orders, the kiosk in Vietnam delivers it instantly in 5 minutes. The customer gets lightning-fast service, and your main kitchen in New York isn't overwhelmed!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Amazon Route 53**: Là dịch vụ Hệ thống tên miền (DNS) đám mây có tính khả dụng và khả năng mở rộng cao (Được cam kết sống 100% SLA). Nó dịch các tên miền (`www.amazon.com`) thành địa chỉ IP (`192.0.2.1`). Điểm đặc biệt: Nó có thể kiểm tra xem máy chủ của bạn có bị sập không để định tuyến sang máy dự phòng.
- **Amazon CloudFront**: Là Mạng phân phối nội dung (CDN). Nó lưu trữ tạm thời (Cache) các file tĩnh của bạn (HTML, CSS, JS, Ảnh, Video) tại hàng trăm Điểm biên (Edge Locations) trên toàn cầu. Khi người dùng tải trang, họ sẽ tải từ máy chủ gần họ nhất.

</details>

- **Amazon Route 53**: A highly available and scalable Cloud Domain Name System (DNS) web service. It translates domain names (`www.example.com`) into the numeric IP addresses (`192.0.2.1`) that computers use to connect to each other. Uniquely, it offers **100% SLA uptime** and intelligent Health Checks for disaster recovery routing.
- **Amazon CloudFront**: A global Content Delivery Network (CDN) service. It securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds. It does this by caching your static files (HTML, CSS, Images, Videos) at hundreds of physical "Edge Locations" located in major cities worldwide.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vật lý là rào cản lớn nhất của mạng Internet. Ánh sáng mất thời gian để di chuyển qua các tuyến cáp quang dưới đáy biển.
Nếu máy chủ của bạn đặt tại Mỹ (us-east-1), một người dùng ở Singapore muốn tải bức ảnh 5MB sẽ mất khoảng 2-3 giây do độ trễ (Latency) đường truyền. Trong thời đại E-commerce, chậm 3 giây đồng nghĩa với việc mất 40% doanh thu.

**CloudFront** ra đời để đánh bại vật lý. Nó sao chép bức ảnh 5MB đó về một trạm AWS đặt ngay tại Singapore. Người dùng Singapore sẽ tải ảnh đó từ trạm Singapore trong vòng 50 mili-giây.

**Route 53** không chỉ là sổ danh bạ. Nếu máy chủ ở Mỹ của bạn bị cháy, DNS thông thường sẽ tiếp tục dẫn khách vào cái máy cháy đó (khách thấy trang báo lỗi). Route 53 thì thông minh hơn, nó phát hiện máy cháy (Health Check), và tự động sửa danh bạ, dẫn khách sang máy chủ dự phòng ở Châu Âu trong vài phút.

</details>

Physics is the ultimate bottleneck of the Internet. Light takes time to travel through transatlantic fiber-optic cables.
If your Web Server is in Virginia, USA (us-east-1), a user in Singapore downloading a 5MB hero image will experience 2-3 seconds of latency. In the E-commerce world, a 3-second delay means a 40% drop in conversion rates.

**CloudFront** exists to defeat physical distance. It proactively copies that 5MB image to an AWS data center sitting in Singapore. The Singaporean user downloads the image locally in 50 milliseconds.

**Route 53** exists because traditional DNS is dumb. If your US data center catches fire, traditional DNS will keep sending users to the burning building (resulting in website downtime). Route 53 actively monitors your servers (Health Checks). If it detects a fire, it automatically updates the phonebook and reroutes all global traffic to your backup data center in Europe within minutes.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Bảo mật: AWS Shield & WAF**
- **Không có CloudFront**: Hacker muốn tấn công từ chối dịch vụ (DDoS) trang web của bạn. Chúng dùng 100,000 con bot gửi request thẳng vào máy chủ EC2 (IP công khai). Máy chủ của bạn nghẽn mạng và bốc cháy.
- **Có CloudFront**: Bạn giấu IP của máy chủ EC2 đi. Hacker chỉ thấy IP của CloudFront. Khi 100,000 con bot tấn công CloudFront, AWS có một lớp giáp tên là **AWS Shield Standard** (Miễn phí) tự động hấp thụ hàng ngàn Gigabit rác và chặn đứng cuộc tấn công trước khi nó kịp chạm vào máy chủ EC2 của bạn. Bạn cũng có thể gắn **WAF (Web Application Firewall)** lên CloudFront để chặn các IP đến từ các quốc gia bị cấm.

</details>

### Security Architecture: Surviving a DDoS Attack

- **Without CloudFront**: Your Application Load Balancer or EC2 instances have public IP addresses exposed directly to the raw Internet. A malicious actor executes a massive Layer 3/4 DDoS attack, flooding your server with 50 Gigabits of junk traffic. Your VPC pipe is clogged, your servers crash, and your AWS bill skyrockets.
- **With CloudFront**: You completely hide your EC2/ALB inside a Private Subnet and only allow traffic from CloudFront. The hackers attack CloudFront. CloudFront is protected by **AWS Shield Standard** (Free, active by default), which absorbs and mitigates network-level DDoS attacks using AWS's massive global bandwidth capacity. You can also attach **AWS WAF** to block specific malicious SQL injection attempts or block IPs from entire countries. The attack never reaches your origin servers!

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Host Website Tĩnh (Static SPA)**: Lưu code React/Vue/Angular trên S3 (Siêu rẻ). Bọc S3 bằng CloudFront. Trỏ tên miền Route53 vào CloudFront. Bạn có một Website với tốc độ tải siêu phàm, miễn nhiễm với DDoS, mà không cần thuê bất kỳ máy chủ EC2 nào!
2. **Video Streaming (Netflix-style)**: Phân phối video khóa học, phim ảnh. CloudFront sẽ cache các đoạn video nhỏ (chunks) trên toàn thế giới, giúp người dùng không bị giật lag khi xem (Buffering).
3. **Route 53 Geo-Routing (Định tuyến theo địa lý)**: Bạn có 2 server (1 ở Mỹ, 1 ở Nhật). Nếu khách truy cập từ Mỹ, Route 53 trả về IP Mỹ. Nếu khách từ Châu Á, Route 53 tự động trả về IP Nhật để có tốc độ tốt nhất.

**Không nên làm (Anti-patterns):**
- **Không Cache API động**: Đừng thiết lập CloudFront cache lại các kết quả API như "Giỏ hàng của khách" (Dynamic Data). Nếu bạn làm sai, khách hàng A có thể nhìn thấy giỏ hàng và thẻ tín dụng của khách hàng B vì CloudFront đã lấy kết quả của người này trả cho người kia!

</details>

1. **Serverless Static Website Hosting**: The Holy Grail of Frontend Deployment. Store your compiled React/Vue/Angular application (HTML/CSS/JS) in an S3 Bucket. Put CloudFront in front of the bucket. Point Route 53 to CloudFront. You now have a globally distributed, DDoS-resistant website that costs pennies per month with exactly zero servers to manage.
2. **Video Streaming & Large File Distribution**: Distributing large video files or software patches. CloudFront caches the massive files at Edge locations, saving you immense bandwidth costs (Data Transfer OUT from S3 to the Internet is expensive, but Data Transfer from S3 to CloudFront is FREE).
3. **Route 53 Geolocation/Latency Routing**: You deploy backend APIs in `us-east-1` and `ap-northeast-1` (Tokyo). You configure Route 53 Latency Routing. When a user types `api.yourcompany.com`, Route 53 dynamically calculates which data center is physically closest to them and routes them there for optimal performance.

### Anti-Patterns
- **Aggressively Caching Dynamic API Responses**: Never misconfigure CloudFront to cache dynamic, user-specific data (e.g., the `GET /cart` API response). If you do, User A will fetch their cart, CloudFront will cache it, and when User B fetches their cart, CloudFront will return User A's private data! Ensure your `Cache-Control` headers for dynamic APIs are strictly set to `no-cache` or bypass CloudFront entirely for APIs.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. OAI / OAC (Khóa chặn S3)**
Khi bạn dùng S3 làm máy chủ web đằng sau CloudFront, có một lỗ hổng: Người dùng có thể Lách qua CloudFront, truy cập thẳng vào đường link gốc của S3. (Làm bạn tốn tiền băng thông S3 đắt đỏ và lách qua bảo mật).
*Giải pháp*: Dùng tính năng **OAC (Origin Access Control)**. OAC bắt S3 phải khóa chặt cửa lại, và chỉ cấp đúng 1 cái chìa khóa cho phép duy nhất CloudFront được vào lấy file.

**2. Invalidating Cache (Xóa Cache thủ công)**
Bạn vừa cập nhật logo mới cho website, nhưng khách hàng vào vẫn thấy logo cũ (do CloudFront vẫn giữ bản copy cũ trong 24 tiếng).
Bạn không thể chờ 24 tiếng. Bạn phải vào bảng điều khiển CloudFront, chạy lệnh **Create Invalidation** với đường dẫn `/*`. Lệnh này báo cho 400 trạm Edge trên toàn thế giới phải LẬP TỨC vứt bỏ bản copy cũ, và chạy về máy chủ Mỹ để lấy logo mới.

</details>

### 1. Securing S3 Origins with OAC (Origin Access Control)
When using S3 behind CloudFront, a massive mistake is leaving the S3 bucket publicly readable. If you do, users can bypass your CloudFront CDN (and your WAF security) and download files directly via the ugly S3 URL, costing you exorbitant AWS Data Transfer fees.
*The Best Practice*: Make the S3 Bucket strictly **Private**. Configure CloudFront with an **OAC (Origin Access Control)**. CloudFront generates a cryptographic identity. You attach a Bucket Policy to S3 saying: "Allow Read Access ONLY if the request comes from this specific CloudFront OAC." Now, direct S3 access is blocked, forcing all traffic through your secure CDN.

### 2. Cache Invalidation Strategies
You deploy a new version of `index.html` with a critical bug fix, but users are still experiencing the bug. Why? Because CloudFront is serving the cached copy of the old `index.html` from the Edge locations!
*The Fix*: You must explicitly trigger a **Cache Invalidation** in CloudFront (e.g., invalidating `/*`). This forces all 400 Edge Locations worldwide to instantly delete the cached file and fetch the fresh copy from S3. 
*Note*: AWS charges money for Invalidations if you do it too frequently. The modern DevOps approach is **Cache Busting**: Append a hash to your filenames during build (e.g., `main.a7f82.js`). When the file changes, the URL changes, completely bypassing the old cache organically!

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đoạn Terraform dưới đây là tiêu chuẩn vàng (Golden Standard) để xuất bản một Website Frontend (S3) ra Internet một cách an toàn thông qua CloudFront, sử dụng OAC để chặn ai đó truy cập trực tiếp S3.

</details>

### The Golden Standard: Secure Static Website (Terraform)

This provisions a CloudFront distribution pointing to a private S3 bucket securely using OAC.

```hcl
# 1. The Origin Access Control (The cryptographic identity for CloudFront)
resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "frontend-oac"
  description                       = "OAC for Frontend Bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# 2. The CloudFront Distribution
resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "S3-frontend-origin"
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html" # Crucial for React/Vue routing

  # Map this CloudFront to your Route53 custom domain (e.g. app.mycompany.com)
  aliases = ["app.mycompany.com"]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-frontend-origin"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https" # Force HTTPS Security
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  # Requires an ACM Certificate for SSL/HTTPS
  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.my_cert.arn
    ssl_support_method       = "sni-only"
  }
}

# 3. The S3 Bucket Policy allowing ONLY CloudFront OAC to read the files
resource "aws_s3_bucket_policy" "frontend_policy" {
  bucket = aws_s3_bucket.frontend.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "s3:GetObject"
        Effect    = "Allow"
        Principal = { Service = "cloudfront.amazonaws.com" }
        Resource  = "${aws_s3_bucket.frontend.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.s3_distribution.arn
          }
        }
      }
    ]
  })
}
```

---

## Related Topics

- [AWS S3](./aws-s3.md) — The storage layer that perfectly compliments CloudFront for web hosting.
- [AWS WAF (Web Application Firewall)](../03-cloud-architecture/well-architected-framework.md#security-pillar) — The security layer you attach to CloudFront.
- [DevOps CI/CD Pipelines](../../06-devops-engineering/README.md) — How to automate uploading files to S3 and triggering the CloudFront Cache Invalidation.
