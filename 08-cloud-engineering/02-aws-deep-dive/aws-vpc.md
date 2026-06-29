# AWS Virtual Private Cloud (VPC)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nắm vững nền tảng Mạng (Networking) trên AWS. Tìm hiểu cách thiết lập VPC, sự khác biệt sống còn giữa Public và Private Subnets, Internet Gateway, NAT Gateway và Security Groups để bảo vệ hệ thống khỏi các cuộc tấn công.

</details>

> **Summary**: Master the foundation of AWS Networking. Learn how to design a VPC, understand the critical difference between Public and Private Subnets, Internet Gateways, NAT Gateways, and Security Groups to shield your infrastructure.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng AWS là một thành phố khổng lồ đông đúc.
- **VPC (Khu đô thị của bạn)**: Bạn mua một khu đất rộng lớn và xây tường bao quanh. Khu này là của riêng bạn, người lạ không thể tùy tiện vào được.
- **Public Subnet (Sân trước/Phòng khách)**: Là khu vực mở cửa tiếp khách. Bạn để các "Cửa hàng" (Web Servers) ở đây. Bất cứ ai trên đường phố (Internet) cũng có thể bước vào mua hàng.
- **Private Subnet (Két sắt/Phòng ngủ)**: Là căn phòng bí mật tận cùng nhà bạn, không có cửa sổ hướng ra ngoài đường. Bạn cất "Tiền bạc" (Databases) ở đây. Khách mua hàng tuyệt đối không thể vào, chỉ có nhân viên của bạn từ Sân trước mới được phép bước vào lấy đồ.
- **Security Group (Bảo vệ cầm dùi cui)**: Một ông bảo vệ đứng ngay trước cửa phòng. Bạn dặn ổng: "Chỉ cho phép khách đi cửa chính, ai trèo qua cửa sổ thì đánh!".

</details>

Imagine AWS as a massive, bustling city.
- **VPC (Your Private Estate)**: You buy a large plot of land and build a high wall around it. This is your private network; strangers cannot enter it by default.
- **Public Subnet (The Storefront/Living Room)**: This is the public-facing area of your estate. You place your Web Servers here. Anyone walking down the street (the Internet) can walk through the front door and interact with your store.
- **Private Subnet (The Vault/Bedroom)**: The most secure, hidden room in your estate with no windows facing the street. You store your money (Databases) here. The public can never access this room directly; only your Web Servers from the Storefront are allowed to enter.
- **Security Group (The Bouncer)**: A bodyguard standing in front of every single room. You give them a list: "Only allow people coming through port 443 (HTTPS). Reject everyone else."

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon VPC (Virtual Private Cloud)** là dịch vụ cho phép bạn cung cấp một phần bị cô lập logic của đám mây AWS. Tại đây, bạn có toàn quyền kiểm soát môi trường mạng ảo của mình, bao gồm chọn dải IP, tạo các mạng con (Subnets), cấu hình bảng định tuyến (Route Tables) và cổng mạng.

**Thành phần cốt lõi:**
- **Subnet**: Một dải IP bị chia nhỏ từ VPC. Nằm gọn trong 1 Availability Zone (AZ).
- **Internet Gateway (IGW)**: Cánh cửa nối VPC của bạn với Internet. Subnet nào có đường nối (Route) ra IGW thì gọi là Public Subnet.
- **NAT Gateway**: Đặt ở Public Subnet, cho phép các máy chủ trong Private Subnet "đi ké" ra Internet để tải bản cập nhật, nhưng chặn không cho Internet đi ngược vào trong.
- **Security Group (SG)**: Tường lửa ảo hoạt động ở cấp độ Instance (Máy chủ).
- **Network ACL (NACL)**: Tường lửa ảo hoạt động ở cấp độ Subnet.

</details>

**Amazon VPC (Virtual Private Cloud)** is a service that lets you provision a logically isolated section of the AWS Cloud. You have complete control over your virtual networking environment, including the selection of your own IP address range, creation of subnets, and configuration of route tables and network gateways.

**Core Components:**
- **Subnet**: A segmented range of IP addresses in your VPC. Tied to a specific Availability Zone (AZ).
- **Internet Gateway (IGW)**: The doorway that connects your VPC to the public Internet. A subnet with a route to an IGW is called a *Public Subnet*.
- **NAT Gateway**: Placed in the Public Subnet, it allows servers in the *Private Subnet* to initiate outbound connections (e.g., to download OS updates) without allowing incoming connections from the Internet.
- **Security Group (SG)**: A stateful virtual firewall operating at the Instance (Server) level.
- **Network ACL (NACL)**: A stateless virtual firewall operating at the Subnet level.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trước đây (thời kỳ EC2 Classic), khi bạn khởi tạo một máy chủ trên AWS, nó nằm chung trên một mặt phẳng mạng khổng lồ với tất cả các khách hàng AWS khác, và mặc định mở tuếch ra Internet. Bạn chỉ có SG để bảo vệ. Nếu SG bị config sai, máy chủ của bạn sẽ bị hack ngay lập tức.

AWS giới thiệu VPC để mang khái niệm mạng nội bộ (LAN) của các công ty truyền thống lên đám mây. Nó cô lập hoàn toàn hệ thống của bạn ở cấp độ phần cứng mạng (Software Defined Networking). Giờ đây, để hack được Database của bạn, hacker không chỉ cần vượt qua mật khẩu, mà còn phải biết đường định tuyến IP mạng riêng của bạn, vượt qua IGW, và vượt qua NACL.

</details>

Historically (in the era of "EC2 Classic"), when you spun up a server on AWS, it sat on a massive, shared, flat network with all other AWS customers and was directly exposed to the public Internet. You only had Security Groups to protect it. If a developer misconfigured a Security Group, the server was hacked instantly.

AWS introduced VPCs to bring traditional, on-premise Enterprise networking (LAN) to the cloud. It isolates your infrastructure at the network routing layer via Software Defined Networking (SDN). Today, to hack your Database, an attacker doesn't just need the password; they literally cannot mathematically route packets to your Database because it possesses no public IP and sits behind multiple layers of network isolation.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Kiến trúc thảm họa (Chỉ có Public Subnet):**
- Đặt EC2 Web Server và RDS Database chung một chỗ. Cả hai đều có Public IP.
- Ai cũng có thể quét cổng 3306 (MySQL) của Database từ Internet.
- Bị DDOS chết Database trong 5 phút.

**Kiến trúc chuẩn Production (Public + Private):**
- Web Server nằm ở Public Subnet. Chỉ mở port 80 và 443 ra thế giới.
- Database nằm ở Private Subnet. KHÔNG CÓ Public IP. Chỉ cho phép các gói tin đi từ IP nội bộ của Web Server đi vào. An toàn tuyệt đối!

</details>

### The Disaster Architecture (All Public Subnets)
- Placing your Web Servers and your RDS Database in the same Public Subnet. Both have Public IPs.
- Hackers from Russia run automated scripts to port-scan port 3306 (MySQL) continuously over the internet.
- A brute-force attack or zero-day vulnerability takes down your Database in 5 minutes.

### The Production Standard (Public + Private Tiering)
- **Web Servers / Load Balancers** sit in the Public Subnet. They accept traffic from `0.0.0.0/0` (The Internet) on ports 80 (HTTP) and 443 (HTTPS).
- **Databases** sit deeply in the Private Subnet. They possess NO Public IPs. Their Security Group explicitly states: "Only accept traffic from the Security Group ID of the Web Servers". The database is invisible to the outside world.

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Host ứng dụng Web nhiều tầng (3-Tier Web App)**: 
   - Tầng 1 (Public): Application Load Balancer.
   - Tầng 2 (Private): EC2 Web Servers / ECS Fargate.
   - Tầng 3 (Private): RDS Database.
2. **Bảo mật giao tiếp bằng VPC Endpoint**: Khi EC2 trong Private Subnet muốn đẩy file lên S3, gói tin mặc định sẽ chạy ra Internet rồi vòng về S3 (rất chậm và tốn tiền). Dùng VPC Endpoint tạo một "đường hầm nội bộ" nối thẳng từ VPC sang S3 mà không cần ra Internet.
3. **Kết nối Hybrid Cloud bằng VPC Peering / VPN**: Nối mạng công ty vật lý của bạn ở Hà Nội với VPC trên AWS Singapore qua một đường ống VPN mã hóa.

**Không nên làm (Anti-patterns):**
- **Sử dụng CIDR block trùng nhau**: Đừng khởi tạo mọi VPC với dải IP mặc định `10.0.0.0/16`. Sau này khi bạn cần nối (Peering) 2 VPC của 2 dự án lại với nhau, chúng sẽ bị xung đột dải IP và không thể nối được. Hãy quy hoạch IP cẩn thận ngay từ ngày đầu.

</details>

1. **Hosting a 3-Tier Web Application**: 
   - Tier 1 (Public Subnet): Application Load Balancer (ALB).
   - Tier 2 (Private Subnet 1): EC2 Web Servers / ECS Fargate Containers.
   - Tier 3 (Private Subnet 2): RDS Database.
2. **Secure internal communication via VPC Endpoints**: Normally, if an EC2 instance in a Private Subnet wants to upload a file to S3, the packet travels out the NAT Gateway, to the public Internet, and back to AWS S3 (which is slow and incurs bandwidth costs). A VPC Endpoint creates an internal "secret tunnel" directly to S3 without ever leaving the AWS backbone network.
3. **Hybrid Cloud (Site-to-Site VPN)**: Securely connecting your physical corporate office building in London directly to your AWS VPC in Ireland using encrypted IPSec tunnels.

### Anti-Patterns
- **Overlapping CIDR Blocks**: Never launch every VPC in your organization with the default `10.0.0.0/16` IP block. One day, you will acquire another company or need to connect two projects together using VPC Peering. If they share the exact same IP range, routing mathematically fails. Always plan your IP addressing spaces carefully on Day 1.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Tiết kiệm tiền phí NAT Gateway (Kẻ hút máu của AWS)**
NAT Gateway tính tiền theo giờ, CỘNG THÊM phí truyền tải trên MỖI GB dữ liệu đi qua nó. Nếu hệ thống Data Engineering của bạn ở Private Subnet tải hàng Terabyte dữ liệu từ S3 qua NAT Gateway mỗi ngày, hóa đơn cuối tháng sẽ lên tới hàng ngàn đô la!
**Giải pháp**: BẮT BUỘC phải cài đặt *S3 VPC Gateway Endpoint*. Nó hoàn toàn miễn phí và giữ traffic ở lại nội bộ.

**2. Security Group vs NACL (Stateful vs Stateless)**
- **Security Group (Stateful)**: Khá thông minh. Nếu bạn cho phép một gói tin Gửi đi (Outbound), nó sẽ tự động nhớ và cho phép câu trả lời Nhận về (Inbound) lọt qua cửa.
- **NACL (Stateless)**: Rất máy móc. Nếu bạn cấu hình chặn IP của hacker ở Inbound, bạn PHẢI cấu hình cả Outbound. Ít khi dùng NACL trừ phi bạn muốn chặn một dải IP độc hại cụ thể ở cấp độ mạng rập khuôn. Dùng SG cho 99% trường hợp.

</details>

### 1. Defeating the NAT Gateway Data Transfer Trap
NAT Gateways charge an hourly rate PLUS a heavy data processing fee for every GB that passes through them. If your Data Engineering pipelines sit in a Private Subnet and download Terabytes of data from S3 or DynamoDB daily *through* the NAT Gateway, your AWS bill will explode to thousands of dollars.
**The Fix**: You MUST provision *VPC Gateway Endpoints* for S3 and DynamoDB. They are 100% free and route traffic internally, completely bypassing the expensive NAT Gateway.

### 2. Security Groups vs NACLs (Stateful vs Stateless)
- **Security Group (Stateful)**: Intelligent. If you allow an outgoing request to a website (Outbound port 80), the SG automatically remembers the connection and permits the incoming response (Inbound) to pass through, regardless of inbound rules.
- **NACL (Stateless)**: Rigid. It evaluates every single packet independently. If you open port 80 Inbound, you must also manually calculate and open ephemeral ports Outbound for the response to leave. In practice, leave NACLs at their default (allow all) and rely heavily on Security Groups for 99% of your firewall rules, unless explicitly blacklisting a malicious IP subnet.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bên dưới là cấu hình Terraform chuẩn mực để tạo ra một mạng lưới VPC Production-ready (Có đầy đủ Public, Private, Internet Gateway, NAT Gateway).

</details>

### Production-Ready VPC via Terraform

Writing standard AWS networking from scratch involves manually wiring Route Tables, Subnets, and IGWs. The official AWS VPC Terraform module simplifies this massively.

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  # Spread across 3 Availability Zones for High Availability
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  # Private subnets for Compute (EC2) and Databases
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  
  # Public subnets for Load Balancers and NAT Gateways
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  # Enable NAT Gateways so private servers can download patches
  enable_nat_gateway = true
  
  # Best Practice: Use a single NAT Gateway to save costs (unless ultra high-availability is required)
  single_nat_gateway = true

  # Enable DNS hostnames (Required for Private RDS databases to resolve properly)
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
```

---

## Related Topics

- [AWS IAM](./aws-iam.md) — Networking shields you from the outside; IAM shields you from the inside.
- [AWS EC2](./aws-ec2.md) — The compute instances that actually live inside the VPC subnets.
- [AWS RDS](./aws-rds-and-aurora.md) — Databases that should *always* be placed deeply within the Private Subnets.
