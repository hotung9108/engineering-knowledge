# AWS RDS & Amazon Aurora

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Tìm hiểu Amazon RDS - Dịch vụ cơ sở dữ liệu quan hệ quản lý sẵn. Khám phá sự khác biệt giữa kiến trúc Multi-AZ (Đảm bảo tính sẵn sàng) và Read Replicas (Mở rộng hiệu năng), cùng với sức mạnh vô song của Amazon Aurora.

</details>

> **Summary**: Explore Amazon RDS—the fully managed relational database service. Understand the critical architectural differences between Multi-AZ (for High Availability) and Read Replicas (for Performance Scaling), and discover the unmatched power of Amazon Aurora.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn cần một cuốn sổ cái (Database) để ghi chép tiền bạc:
- **Tự cài Database trên EC2**: Giống như bạn mua một cuốn sổ trắng. Bạn tự kể vạch, tự viết, và mỗi đêm bạn phải tự thức dậy để chép cuốn sổ ra một bản nháp khác đề phòng nhà cháy. Rất mệt!
- **Amazon RDS (PaaS)**: Bạn mượn thư ký của AWS. Bạn bảo: "Lập cho tôi sổ MySQL". Thư ký sẽ tự lo việc kẽ vạch, tự động cập nhật hệ điều hành, tự động chép dự phòng mỗi đêm. Bạn chỉ việc tập trung vào ghi chép số liệu (Viết code SQL).
- **Multi-AZ**: AWS bí mật thuê thêm 1 thư ký dự bị ngồi ở tòa nhà khác. Mỗi khi thư ký 1 viết 1 chữ, thư ký 2 lập tức copy y chang (Synchronous). Nếu thư ký 1 bị ốm, thư ký 2 lập tức lên thay trong vài giây.
- **Amazon Aurora**: AWS tạo ra một hệ thống sổ sách Siêu Cấp độc quyền. Nó sao lưu dữ liệu ra 6 bản ở 3 tòa nhà khác nhau. Nó đọc/ghi nhanh gấp 5 lần MySQL bình thường.

</details>

You need a ledger (Database) to record financial transactions:
- **Installing MySQL manually on EC2**: Like buying a blank notebook. You must draw the lines yourself, write the entries, and wake up every night at 3 AM to make a photocopy in case the house burns down. Exhausting!
- **Amazon RDS (PaaS)**: You hire an AWS Secretary. You say, "Give me a MySQL ledger". The secretary handles drawing the lines, patching the OS, and automatically making nightly photocopies (Backups). You just focus on the accounting (Writing SQL).
- **Multi-AZ (High Availability)**: AWS secretly hires a backup secretary in another building. Every time Secretary A writes a word, Secretary B copies it instantly (Synchronous replication). If Secretary A gets sick, Secretary B takes over immediately.
- **Amazon Aurora**: AWS invents a proprietary Super Ledger. It automatically replicates your data 6 times across 3 different buildings. It processes transactions up to 5x faster than standard MySQL.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon RDS (Relational Database Service)** là dịch vụ PaaS quản lý CSDL quan hệ. AWS tự động hóa các tác vụ quản trị tốn thời gian như cài đặt phần cứng, thiết lập cơ sở dữ liệu, vá lỗi và sao lưu. Hỗ trợ: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server.
**Amazon Aurora** là CSDL tương thích với MySQL và PostgreSQL được AWS thiết kế riêng cho nền tảng Đám mây. Kiến trúc lưu trữ của nó tách biệt hoàn toàn khỏi kiến trúc tính toán.

**Tính năng cốt lõi:**
- **Automated Backups**: Tự động sao lưu dữ liệu mỗi đêm. Cho phép khôi phục dữ liệu tại bất kỳ giây nào (Point-In-Time Recovery) trong vòng tối đa 35 ngày.
- **Multi-AZ Deployment**: Chế độ chạy đồng bộ (Synchronous) ở 2 Availability Zones để chống sập Data Center.
- **Read Replicas**: Bản sao bất đồng bộ (Asynchronous) dùng để tăng tốc độ đọc dữ liệu (Scale Out).

</details>

**Amazon RDS (Relational Database Service)** is a managed PaaS for relational databases. It automates time-consuming administrative tasks such as hardware provisioning, database setup, OS patching, and backups. It supports MySQL, PostgreSQL, MariaDB, Oracle, and SQL Server.
**Amazon Aurora** is a MySQL and PostgreSQL-compatible relational database built explicitly for the cloud by AWS. Its fundamental innovation is decoupling the Compute layer from the Storage layer.

**Core Features:**
- **Automated Backups**: Nightly snapshots. Allows for Point-In-Time Recovery (PITR), meaning you can restore your database to the exact second right before a developer accidentally dropped a table, up to 35 days ago.
- **Multi-AZ Deployment**: Synchronous replication across 2 Availability Zones for Disaster Recovery.
- **Read Replicas**: Asynchronous replication used to scale out Read performance.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Nỗi đau truyền thống (Self-managed DBs)**
Quản trị viên CSDL (DBA) là một nghề cực kỳ vất vả. Nếu hệ thống MySQL tự cài (On-Premise) bị sập ổ cứng lúc 2h sáng, DBA phải bật dậy, sửa ổ cứng, chạy lệnh khôi phục dữ liệu. Quá trình này có thể làm công ty gián đoạn (Downtime) nhiều giờ đồng hồ.

AWS RDS ra đời để giải phóng sức lao động. Tính năng **Multi-AZ Failover** của RDS hoạt động hoàn toàn tự động. Nếu ổ cứng của máy Master bị hỏng, AWS tự động đẩy IP sang máy Standby trong vòng ~60 giây. Ứng dụng của bạn chỉ hơi chớp giật một chút rồi chạy tiếp bình thường, DBA có thể ngủ ngon!

</details>

**The Pain of Self-Managed DBs**
Being a Database Administrator (DBA) is notoriously stressful. If a self-managed MySQL server (On-Premise or on EC2) suffers a hard drive failure at 2 AM, the DBA gets paged, wakes up, provisions a new disk, and manually executes failover/restore scripts. This causes hours of Downtime for the business.

AWS RDS exists to eliminate this "undifferentiated heavy lifting". The **Multi-AZ Failover** feature is entirely automated. If the underlying EC2 host of the Master DB crashes, AWS automatically flips the DNS CNAME record to point to the Standby database in a different AZ within ~60 seconds. Your application experiences a brief blip and continues running seamlessly while the DBA sleeps peacefully.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Sự khác biệt sống còn: Multi-AZ vs Read Replicas**
- Rất nhiều người nhầm lẫn hai khái niệm này!
- **Multi-AZ (Để Sinh Tồn)**: Sinh ra một con máy Standby. Ứng dụng của bạn KHÔNG ĐƯỢC PHÉP đọc dữ liệu từ máy Standby này. Nó chỉ ngồi im và copy dữ liệu đồng bộ. Mục đích duy nhất của nó là để thế mạng khi máy Master chết. (Dùng cho High Availability).
- **Read Replicas (Để Chạy Nhanh)**: Sinh ra các bản sao. Ứng dụng của bạn ĐƯỢC PHÉP gửi câu lệnh `SELECT` tới các bản sao này để giảm tải cho máy Master. Máy Master chỉ chuyên xử lý `INSERT/UPDATE`. Tuy nhiên, vì là bất đồng bộ (Asynchronous), dữ liệu ở bản sao có thể bị chậm vài mili-giây so với Master (Eventual Consistency).

</details>

### The Crucial Distinction: Multi-AZ vs. Read Replicas
Junior engineers frequently confuse these two concepts!

| Feature | Multi-AZ (Disaster Recovery) | Read Replicas (Performance Scaling) |
|---|---|---|
| **Primary Goal** | High Availability (Surviving a crash) | Scalability (Handling massive Read traffic) |
| **Replication Type** | **Synchronous** (Guarantees zero data loss) | **Asynchronous** (May lag by a few milliseconds) |
| **Can the App Read from it?**| **NO**. The Standby DB is completely locked. | **YES**. You can route `SELECT` queries to it. |
| **Failover** | **Automatic**. AWS flips the DNS in ~60s. | **Manual**. You must explicitly promote it. |

*Best Practice*: Production Databases should *always* use Multi-AZ. If your app is read-heavy (like a news website), you add Read Replicas *in addition* to Multi-AZ.

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Ứng dụng E-Commerce/Banking**: Cần tính toàn vẹn dữ liệu cực cao (ACID transactions). Sử dụng RDS PostgreSQL với Multi-AZ để không bao giờ mất đơn hàng của khách khi AWS có sự cố trạm điện.
2. **Hệ thống Phân tích (Analytics) Báo cáo**: Bạn có máy RDS Master phục vụ khách hàng mua sắm. Giám đốc yêu cầu xuất báo cáo doanh thu phức tạp (`JOIN` hàng triệu dòng). Đừng bao giờ chạy lệnh xuất báo cáo trên máy Master (sẽ làm lag hệ thống của khách!). Hãy tạo 1 **Read Replica** riêng biệt, và cho Giám đốc xuất báo cáo trên máy đó.
3. **Amazon Aurora Serverless**: Cho ứng dụng có lượng truy cập thất thường. Nếu đêm không có ai xài, Aurora sẽ tự động giảm CPU xuống mức tối thiểu (thậm chí tắt hẳn). Khi có khách truy cập, nó lập tức thức dậy trong vài giây.

**Cảnh báo (Anti-patterns):**
- **Public IP cho RDS**: Đừng bao giờ để tuỳ chọn `Publicly Accessible = True` cho Production DB! Hacker sẽ quét IP 24/7. Database luôn phải nằm sâu trong **Private Subnet**, chỉ cho phép EC2 trong cùng VPC truy cập.

</details>

1. **Transactional Systems (OLTP)**: E-Commerce, Banking, and ERP systems requiring strict ACID properties. Deploy RDS PostgreSQL or Aurora with Multi-AZ to guarantee data integrity and minimize downtime during data center outages.
2. **Offloading Analytics / Reporting**: You have a Master RDS serving live customers. The CEO wants a complex revenue report that executes a massive `JOIN` across millions of rows. **Never run this query on the Master database!** It will spike the CPU to 100% and crash the live app. Instead, provision a **Read Replica**, point your BI tool (Tableau/Metabase) to the replica, and run the heavy analytics there without affecting production traffic.
3. **Aurora Serverless**: For unpredictable workloads. If your development database is rarely used at night, Aurora Serverless can scale compute capacity down to zero, saving immense costs, and instantly spin back up when a query arrives.

### Anti-Patterns
- **Publicly Accessible Databases**: Never set `Publicly Accessible = True` on an RDS instance unless it's a strictly controlled, temporary toy environment. Shodan and hackers constantly scan the internet for open port 3306 or 5432. RDS must always reside deep within a **Private Subnet**, accessible only via strict Security Groups from internal Web Servers or a Bastion Host.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao Amazon Aurora lại vĩ đại? (Log is the Database)**
RDS thông thường vẫn xài chung kiến trúc của các hệ thống cũ: Chép data từ CPU xuống Ổ cứng (EBS) qua mạng. Nếu dùng Multi-AZ, nó phải chép qua mạng 2 lần. Rất chậm!
**Aurora** viết lại hoàn toàn lớp lưu trữ. Nó biến ổ cứng thành một hệ thống phân tán (Distributed Storage) tự động chia dữ liệu thành từng khối 10GB và nhân bản ra **6 bản sao (trên 3 AZ)**. Khi máy Compute ghi dữ liệu, nó chỉ gửi các bản ghi nhật ký (Redo Logs) xuống hệ thống Storage. Storage sẽ tự biết cách áp dụng log vào data. Kết quả: I/O mạng giảm thê thảm, Aurora chạy nhanh hơn MySQL truyền thống gấp 5 lần!

</details>

### The Architecture of Amazon Aurora ("The Log is the Database")
Traditional RDS uses the standard monolithic MySQL/PostgreSQL engine. When a transaction commits, the compute node must flush the data pages to the EBS volume over the network. If using Multi-AZ, it must synchronously flush data over the network to the Standby node's EBS volume. This causes massive network I/O bottlenecks.

**Amazon Aurora** fundamentally redesigns the database for the cloud:
1. **Decoupled Storage**: Compute (CPU/RAM) is completely separated from Storage.
2. **6-Way Replication**: The Storage layer is a proprietary, distributed, multi-tenant fleet of SSDs. Your data is automatically divided into 10GB chunks and replicated **6 times across 3 Availability Zones** automatically, regardless of how many Compute nodes you have.
3. **Log-Structured**: The Compute node *does not write data pages* to the network. It only streams the "Redo Logs" (the delta of changes) to the Storage fleet. The intelligent storage nodes asynchronously apply the logs to the data pages in the background.
Result? Network I/O is drastically reduced. Aurora processes transactions up to 5x faster than standard MySQL and 3x faster than standard PostgreSQL. Furthermore, because storage is decoupled, spinning up a new Read Replica takes milliseconds (because they all share the exact same underlying distributed storage volume).

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là đoạn code Terraform để khởi tạo một Database RDS PostgreSQL chuẩn Production (đóng kín trong Private Subnet, bật Multi-AZ, và tự động Backup).

</details>

### Provisioning a Production RDS (Terraform)

```hcl
# Security Group to strictly limit access to the DB
resource "aws_security_group" "rds_sg" {
  name        = "production-rds-sg"
  description = "Allow inbound PostgreSQL traffic ONLY from the Web Servers"
  vpc_id      = module.vpc.vpc_id # Assuming VPC is already defined

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    # BEST PRACTICE: Do not use an IP range here. Use the Security Group ID of the EC2 Web Servers!
    security_groups = [aws_security_group.web_server_sg.id] 
  }
}

# The RDS Instance
resource "aws_db_instance" "production_postgres" {
  identifier           = "prod-user-db"
  allocated_storage    = 100
  max_allocated_storage = 500 # Automatically scale disk size up to 500GB if getting full
  
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t4g.large"
  
  db_name              = "company_db"
  username             = "db_admin"
  password             = jsondecode(data.aws_secretsmanager_secret_version.db_pass.secret_string)["password"]
  
  # Crucial Production Settings
  multi_az             = true  # Enables High Availability standby
  publicly_accessible  = false # Absolute necessity. Keep it Private.
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name = aws_db_subnet_group.private_subnets.name
  
  backup_retention_period = 30 # Keep nightly backups for 30 days (allows Point in time recovery)
  storage_encrypted       = true # Encrypt data at rest (KMS)
  
  skip_final_snapshot     = false # Force a backup before someone is allowed to delete this DB
}
```

---

## Related Topics

- [AWS VPC](./aws-vpc.md) — RDS must be deployed in Private Subnets. Security Groups protect it.
- [Data Modeling](../../06-data-engineering/01-data-fundamentals/data-modeling-and-dimensional-design.md) — How to design tables inside this database (3NF for OLTP).
- [Lakehouse & Data Warehousing](../../06-data-engineering/04-data-storage/lakehouse-and-acid-transactions.md) — Why RDS is terrible for Big Data Analytics, and why you must export data to S3/Redshift instead.
