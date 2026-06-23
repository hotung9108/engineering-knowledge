# Disaster Recovery

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: High Availability (HA) giúp web của bạn không chết khi 1 cái máy chủ bị cháy. Nhưng chuyện gì xảy ra nếu một trận Động đất làm sập TOÀN BỘ Trung tâm Dữ liệu (Data Center), giết chết cả máy Chính lẫn máy Phụ? Đó gọi là Thảm họa (Disaster). **Khôi phục sau Thảm họa (Disaster Recovery - DR)** là chiến lược "Sinh tồn ở cấp độ Quốc gia". Nó liên quan đến việc sao chép dữ liệu ra một Data Center khác cách đó hàng ngàn kilomet. DR cực kỳ đắt tiền, và nó không hướng tới việc "Không bao giờ sập", mà hướng tới việc "Khi sập toàn bộ thì mất bao lâu để làm lại từ đầu ở một nơi khác".

</details>

> **Summary**: High Availability (HA) is engineered to mask localized faults (e.g., a dead Server or a severed rack switch) by instantly failing over within the same Data Center. However, HA completely fails when the entire Data Center is physically obliterated by a hurricane, flood, regional power grid collapse, or an act of war. **Disaster Recovery (DR)** is the ultimate macroscopic resilience strategy. It involves geolocating asynchronous backups and standby infrastructure in a completely independent geographic region (e.g., 500 miles away). DR does not promise 100% uptime; it provides a pre-planned, mathematical guarantee of how much data you will lose (RPO) and how many hours it will take to resurrect the business from the ashes (RTO).

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn lưu Toàn bộ Tài liệu Công ty trong két sắt ở Tòa nhà A.
1. **HA (High Availability)**: Để lỡ cái két sắt bị kẹt khóa, bạn mua thêm 1 cái két sắt nữa, để ở phòng bên cạnh, sao chép tài liệu qua đó. Nếu két 1 kẹt, bạn đi bộ sang phòng bên cạnh lấy tài liệu ở két 2. (Rất tiện, mất 1 phút).
2. **Disaster Recovery (DR)**: Đêm đó Tòa nhà A bị cháy rụi thành tro. Dù bạn có 10 cái két sắt trong đó thì cũng mất hết. Nếu bạn có DR, nghĩa là mỗi đêm, bạn đã bí mật thuê xe tải chở 1 bản copy tài liệu cất vào một cái kho ngầm ở Tòa nhà B cách đó 500km. Tòa nhà A cháy, bạn bắt taxi đi 500km sang Tòa nhà B để lấy lại dữ liệu làm lại cuộc đời. (Tốn thời gian đi taxi, và bị mất những tài liệu mới tạo vào buổi sáng chưa kịp copy, nhưng công ty bạn KHÔNG BỊ PHÁ SẢN).

</details>

Imagine backing up your family photos.
1. **High Availability (HA)**: You buy an External Hard Drive and mirror your Laptop's hard drive. If your Laptop dies, you plug the External Drive into a new computer. Immediate recovery.
2. **Disaster Recovery (DR)**: Your house burns down. The Laptop and the External Hard Drive melt. You lose all photos forever. However, if you had a DR plan, you would have been uploading those photos to Google Drive (A data center 1,000 miles away). Your house burns down, you buy a new laptop, log into Google, and download the photos. It takes a few hours to download, but you successfully saved your memories from a total physical disaster.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Toàn bộ lý thuyết về DR xoay quanh 2 con số tối thượng mà Giám đốc (CEO) phải quyết định:
1. **RPO (Recovery Point Objective - Điểm mất dữ liệu)**: Giám đốc chấp nhận mất tối đa dữ liệu của BAO NHIÊU GIỜ?
   - Nếu RPO = 24 giờ: Ta chỉ cần cấu hình Backup mỗi đêm 1 lần. (Rẻ nhất). Nếu cháy Data Center lúc 3h chiều, ta mất trắng mọi Giao dịch từ sáng đến 3h chiều.
   - Nếu RPO = 0: Khách hàng mua món gì, ta phải copy sang Mỹ ngay lập tức (Chạy đồng bộ). (Cực đắt, mạng cực chậm).
2. **RTO (Recovery Time Objective - Thời gian hồi sinh)**: Giám đốc chấp nhận web bị SẬP TRONG BAO LÂU?
   - Nếu RTO = 48 tiếng: Khi sập, Kỹ sư cứ từ từ lấy Backup từ băng từ ra, cài lại Win, copy file. Tốn 2 ngày web sống lại. (Chi phí thấp).
   - Nếu RTO = 5 phút: Bắt buộc phải duy trì 1 trung tâm dữ liệu ở Mỹ đang chạy ngầm sẵn, có đứt cáp thì trỏ DNS sang đó chạy tiếp luôn. (Chi phí x2 vì phải nuôi 2 cụm Server song song).

</details>

Every Disaster Recovery strategy is mathematically defined by two contractual Service Level Objectives negotiated directly with Business Stakeholders:
1. **RPO (Recovery Point Objective - How much Data Loss is acceptable?)**: If the datacenter is vaporized, RPO defines the maximum allowable chronological data loss. 
   - An RPO of 24 Hours means nightly S3 backups are sufficient. You will permanently lose the last 24 hours of user transactions. 
   - An RPO of 0 (Zero Data Loss) mandates synchronous cross-region replication, inducing massive latency penalties on every single Write operation.
2. **RTO (Recovery Time Objective - How much Downtime is acceptable?)**: The maximum allowable time the business can be completely offline while engineers scramble to restore the system.
   - An RTO of 72 Hours means you can rely on "Cold Backups", downloading terabytes of archives from Glacier and manually provisioning raw EC2 servers.
   - An RTO of 10 Seconds mandates an "Active-Active Multi-Region" architecture, requiring massive financial expenditure to run a 100% duplicate, idle infrastructure in another continent.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Năm 2021, tòa nhà Data Center lớn nhất châu Âu (OVHcloud) bốc cháy ngùn ngụt. Hàng triệu trang web bị xóa sổ hoàn toàn khỏi Internet. Rất nhiều công ty phá sản vĩnh viễn ngay trong đêm đó vì họ lưu Code và Database chung 1 chỗ, KHÔNG CÓ BẢN SAO ở vùng khác.
Đám mây (Cloud) thực chất chỉ là "Máy tính của người khác". Việc AWS hay Google Cloud sập cả 1 Region (Cả 1 bang của Mỹ) là chuyện năm nào cũng xảy ra do bão tuyết, ngập lụt hoặc kỹ sư AWS gõ sai lệnh. 
HA bảo vệ bạn khỏi Lỗi Máy Móc. DR bảo vệ bạn khỏi Sự Phẫn nộ của Thiên nhiên và Sai lầm của Con người. DR chính là bản Hợp đồng Bảo hiểm Nhân thọ của Công ty. 

</details>

In March 2021, a catastrophic fire completely destroyed the SBG2 datacenter of OVHcloud in Strasbourg, France. Millions of websites vanished from the internet. Dozens of companies went permanently bankrupt that night because their primary database and their "HA Backups" were physically located in the exact same burning building. They had zero geo-redundancy.
"The Cloud" is ultimately just physical hardware sitting in a warehouse. Entire AWS Regions (e.g., `us-east-1`) suffer catastrophic outages nearly every year due to severe weather events, massive power grid failures, or rogue BGP routing updates pushed by engineers.
High Availability protects the application from inevitable hardware degradation. Disaster Recovery protects the Corporate Entity from extinction-level events. DR is the ultimate corporate insurance policy.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Bảng so sánh 3 Chiến lược DR (Từ Rẻ nhất đến Đắt nhất)
</details>

Visualizing the standard DR Strategies (The Trade-off between Cost and RTO).

| Strategy | Architecture | RTO (Recovery Time) | Cost Level |
|---|---|---|---|
| **Backup & Restore (Cold)** | Only Data is backed up to S3. No servers exist in Region B. | 12 - 48 Hours | Very Low ($) |
| **Pilot Light (Warm)** | Data is replicated. Only the Core DB runs in Region B. App servers are OFF. | 10 - 60 Minutes | Medium ($$) |
| **Warm Standby** | Core DB + Scaled-down App Servers run in Region B constantly. | 1 - 5 Minutes | High ($$$) |
| **Multi-Region Active-Active** | 100% Duplicate infra running in Region A and B concurrently. | **Near Zero** | Astronomical ($$$$$) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Snapshots định kỳ (EBS/S3)**: Đơn giản nhất. Hàng ngày hệ thống tự động gom DB lại thành 1 file ZIP (Snapshot) và ném sang một Server ở nước khác (Cross-Region Backup). Nếu bị Hacker mã hóa tống tiền (Ransomware) toàn bộ hệ thống cũ, kỹ sư chỉ việc bung file ZIP của ngày hôm qua ra 1 máy tính mới toanh.
2. **Infrastructure as Code (Terraform)**: Phép màu của DR hiện đại. Khi sập toàn bộ Cụm Server ở Sing. Kỹ sư không cần click chuột tay cài lại hàng ngàn máy chủ ở Mỹ. Chỉ cần đổi 1 biến môi trường trong code Terraform `region = "us-east-1"`, nhấn Enter. 5 phút sau, AWS tự động đẻ ra 100 cái máy chủ ở Mỹ y chang như ở Sing.
3. **Database Asynchronous Replication (Đồng bộ bất đồng bộ)**: Để DR không làm chậm web. Khách hàng ghi dữ liệu vào DB ở Sing (Master). DB ở Sing báo OK luôn (Khách rất vui vì nhanh). Ngầm bên dưới, DB ở Sing cặm cụi truyền dữ liệu xuyên đại dương qua cái DB ở Mỹ (Slave). Mỹ luôn trễ hơn Sing khoảng 1 giây (Eventual Consistency).

</details>

1. **Cross-Region Snapshots (Immutable Backups)**: The baseline DR requirement. RDBMS automated snapshots or raw Volume Snapshots (AWS EBS) are continuously taken and specifically copied to an entirely different physical Region (e.g., from Tokyo to Sydney). Critically, these backups must be logically isolated. If a rogue employee or Ransomware deletes the Tokyo infrastructure, the Sydney backups remain untouched (Air-gapped) and can be used to rebuild the state.
2. **Infrastructure as Code (IaC) Recovery**: True DR relies heavily on Terraform or AWS CloudFormation. If Tokyo is obliterated, you cannot manually click through the AWS console to recreate 50 VPCs, Security Groups, and Load Balancers. With IaC, recovery is executing `terraform apply -var="region=ap-southeast-2"`. The identical infrastructure topology is algorithmically provisioned in Sydney in under 5 minutes.
3. **Asynchronous Cross-Region Replication**: To maintain a low RPO without crippling application performance, Databases employ Asynchronous Replication. A user in Tokyo writes to the Tokyo Master DB. The DB commits the transaction locally and instantly returns `200 OK`. In the background, the Binlog is streamed across the trans-pacific cable to the Sydney Replica. The Replica is always ~500ms behind (Replication Lag), but performance is pristine.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **RPO và RTO phải được viết vào Hợp Đồng**: Lập trình viên không bao giờ được phép tự quyết định "Nên Backup mấy lần 1 ngày". Đây là quyết định Rủi ro Kinh doanh. Giám đốc phải ký duyệt: "Tao chấp nhận mất 4 tiếng dữ liệu để tiết kiệm 100 triệu/tháng tiền Server". Nếu sau này có sự cố thật và bị mất dữ liệu, tờ giấy đó sẽ cứu Kỹ sư khỏi bị đi tù hoặc đền bù.
2. **Phải Test DR hằng năm (Disaster Recovery Drills)**: Đừng đợi tới lúc cháy nhà mới lôi bình cứu hỏa ra thử. Những ngân hàng lớn BẮT BUỘC phải giả lập sập hệ thống thật vào ngày nghỉ lễ, ép toàn bộ Kỹ sư phải bấm nút Failover dời nhà sang Data Center dự phòng. 90% các bản Backup khi bung ra bị LỖI KHÔNG ĐỌC ĐƯỢC do chưa bao giờ test.

</details>

1. **Business-Driven RPO/RTO SLAs**: Engineers must never arbitrarily define DR limits. Achieving an RPO of 5 minutes instead of 24 hours geometricallty increases AWS egress bandwidth and storage costs. The CTO and CEO must explicitly sign off on a matrix: "We agree to a 24-Hour RPO, accepting the risk of losing 24 hours of transactions, in exchange for saving $500,000 annually." When disaster strikes, this SLA protects the engineering team from termination.
2. **Mandatory DR Drills (Proof of Recovery)**: Schrodinger's Backup: "The condition of any backup is unknown until you try to restore it." 80% of companies that suffer catastrophic data loss actually had automated backup scripts running perfectly. However, when they attempted to restore the SQL Dump, they discovered the decryption keys were lost, or the file was corrupted 3 years ago. You must execute a full, end-to-end bare-metal restoration Drill in an isolated staging environment at least bi-annually.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sao chép Lỗi (Replicating Corruption)**: Đây là tử huyệt của kiến trúc Active-Active đắt tiền. Bạn có DB ở VN đồng bộ theo thời gian thực (Real-time) sang DB ở Mỹ. Một thằng Hacker (Hoặc dev gõ ngu) chạy lệnh `DROP TABLE Users` (Xóa trắng bảng khách hàng). Lệnh xóa này NGAY LẬP TỨC được đồng bộ với tốc độ ánh sáng sang Mỹ, và xóa sạch bảng Users ở Mỹ luôn. 
   - *Luật*: Đồng bộ theo thời gian thực (Replication) KHÔNG THAY THẾ CHO BACKUP (Chụp ảnh lưu trữ). Replication chống lại lỗi phần cứng. Backup chống lại Lỗi con người.
2. **Khóa nhốt Khách hàng (Vendor Lock-in)**: Bạn dùng công nghệ DR độc quyền của Amazon. Nếu Amazon bực mình khóa tài khoản của công ty bạn, bạn mất trắng. DR mức độ cao nhất (Multi-Cloud) là phải dùng Terraform để lỡ Amazon có sập, bạn có thể chạy 1 dòng lệnh bưng nguyên hệ thống đó xây lại ở bên Google Cloud hoặc Microsoft Azure.

</details>

1. **Confusing Replication with Backup (The Corruption Vector)**: The most fatal architectural misunderstanding. A junior architect deploys a brilliant Cross-Region Active-Active Database and proudly declares: "We don't need nightly S3 Backups anymore, the data is safe in two countries!" A developer accidentally deploys a migration that drops the `Orders` table. The `DROP TABLE` command instantly replicates across the ocean. Both databases are cleanly, perfectly destroyed in 50ms. **Rule**: Replication protects against Hardware failure. Immutable Backups (Snapshots with explicit retention policies) protect against Human error and Ransomware. You absolutely need both.
2. **Single-Cloud Blast Radius (Vendor Lock-in)**: You configure perfect DR by utilizing AWS `us-east-1` and AWS `us-west-2`. However, your AWS root account is compromised via phishing, and the attacker deletes the entire AWS Organization. Or, AWS arbitrarily terminates your account due to an automated billing algorithm error. Your business is extinct. The ultimate (and most complex) DR strategy requires Multi-Cloud architecture—storing cold encrypted backups in Google Cloud Storage (GCP) while running compute on AWS, ensuring survival even against the Cloud Provider themselves.

---

## Related Topics

- For how Traffic routes during a DR event, read about **[Failover](./failover.md)**.
- For backing up databases correctly, read **[Database Scaling](../scalability/db-scaling.md)**.
- For ensuring your APIs recover gracefully from small failures, read **[Resilience Overview](../resilience/overview.md)**.
