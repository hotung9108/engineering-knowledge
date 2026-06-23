# High Availability Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu máy chủ của bạn chết và người dùng vào web thấy màn hình lỗi, đó là một thảm họa kinh doanh. **Tính Sẵn Sàng (Availability)** là thước đo cho biết hệ thống của bạn "Sống" được bao nhiêu phần trăm thời gian trong 1 năm. Nó được đo bằng số đếm các "Số 9" (Ví dụ: `99.9%` hay `99.999%`). Để đạt được độ khả dụng cực cao (High Availability - HA), hệ thống của bạn tuyệt đối không được phép có bất kỳ "Điểm chết duy nhất" nào (Single Point of Failure - SPOF). Mọi thứ đều phải có bản sao dự phòng (Redundancy): Có 2 Load Balancer, 3 App Servers, và 2 Database chạy song song.

</details>

> **Summary**: In enterprise software, downtime correlates directly to massive financial loss and brand destruction. **Availability** is the mathematical probability that a system is operational and able to process requests at any given moment. It is strictly quantified using the "Nines" notation (e.g., Five Nines `99.999%` equates to a maximum of 5.26 minutes of downtime per *year*). Achieving **High Availability (HA)** requires aggressive architectural design explicitly targeting the elimination of all **Single Points of Failure (SPOF)**. It relies on the absolute enforcement of Redundancy (Active/Active or Active/Passive clustering) across every single tier of the technology stack—from hardware load balancers down to physical data center geography.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một chiếc Xe cứu thương.
1. **Low Availability (Sẵn sàng Thấp)**: Bệnh viện chỉ có đúng 1 chiếc xe cứu thương và 1 ông tài xế. Nếu hôm đó ông tài xế bị cảm (SPOF - Điểm chết duy nhất), xe không chạy được. Ai gọi cấp cứu thì đành chịu chết chờ ngày mai ổng hết bệnh.
2. **High Availability (Sẵn sàng Cao)**: Bệnh viện có 3 chiếc xe cứu thương. 1 chiếc chạy chính, 2 chiếc đậu sẵn trong sân nổ máy sẵn (Dự phòng - Redundancy). Nếu chiếc chính bị nổ lốp, tài xế lập tức nhảy sang chiếc số 2 chạy đi luôn. Ngoài ra, bệnh viện còn chia 3 chiếc này đậu ở 3 con phố khác nhau, phòng trường hợp 1 con phố bị kẹt xe thì vẫn còn 2 phố kia đi được. (Phân tán rủi ro).

</details>

Imagine an Airplane flying over the ocean.
1. **Single Point of Failure (SPOF)**: A single-engine Cessna airplane. It only has one engine. If a bird flies into that engine and it breaks, the plane immediately crashes into the ocean. Zero Availability.
2. **High Availability (Redundancy)**: A Boeing 747 has four engines. It is designed to fly perfectly fine on just two engines. Even if two engines explode simultaneously, the airplane continues its flight to the destination without the passengers ever knowing. The extra engines are physical Redundancy.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Đo lường bằng "Số 9" (The Nines)**:
- **99% (Hai số 9)**: Chết tối đa 3.6 ngày/năm. Đạt chuẩn cho các hệ thống nội bộ công ty.
- **99.9% (Ba số 9)**: Chết tối đa 8.7 giờ/năm. Đạt chuẩn cho phần lớn các trang web nhỏ và vừa.
- **99.99% (Bốn số 9)**: Chết tối đa 52 phút/năm. Đạt chuẩn E-commerce lớn.
- **99.999% (Năm số 9)**: Chết tối đa 5 phút/năm. Cực khó, tốn hàng chục triệu đô, dành cho Mạng Viễn thông, Cáp quang, Ngân hàng.

**2. Điểm chết duy nhất (Single Point of Failure - SPOF)**:
Nếu trong sơ đồ kiến trúc của bạn có BẤT KỲ 1 cục nào đứng 1 mình (Chỉ có 1 Load Balancer, hoặc chỉ có 1 Database Master, hoặc 1 Switch mạng vật lý). Thì cục đó là SPOF. HA bắt buộc bạn phải nhân đôi cục đó lên.

</details>

**1. The Mathematics of "Nines"**:
Availability is mathematically defined as: `Uptime / (Uptime + Downtime)`.
- **99% (Two Nines)**: ~3.65 days of downtime per year. Typical for non-critical internal enterprise tooling.
- **99.9% (Three Nines)**: ~8.76 hours of downtime per year. The baseline SLA (Service Level Agreement) for most standard B2B SaaS applications.
- **99.99% (Four Nines)**: ~52.6 minutes of downtime per year. The standard for high-revenue E-commerce platforms. Requires automated failover.
- **99.999% (Five Nines - "Carrier Grade")**: ~5.26 minutes of downtime per year. Extraordinarily expensive to maintain. Required for Telco infrastructure, Pacemakers, and Global Payment Gateways. Requires cross-region active-active clusters.

**2. Eliminating SPOF (Single Point of Failure)**:
A SPOF is any singular component in an architecture whose failure brings down the entire system. If you have 100 App Servers but they all connect to a *single* PostgreSQL instance, that PostgreSQL instance is a SPOF. True HA mandates rigorous `N+1` or `2N` physical and logical redundancy at the Networking, Compute, and Storage layers.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Máy móc LUÔN LUÔN HỎNG. Ổ cứng vật lý có tuổi thọ trung bình 3-5 năm. Trong một trung tâm dữ liệu (Data Center) chứa 10.000 cái ổ cứng, VỀ MẶT TOÁN HỌC, ngày nào cũng sẽ có ít nhất 1 cái ổ cứng bị cháy.
Kỹ sư phần mềm giỏi không cố gắng "Ngăn chặn phần cứng bị cháy" (Vì điều đó là bất khả thi). Kỹ sư giỏi thiết kế một hệ thống mà **"Phần cứng cháy cũng không sao"**.
Tính sẵn sàng cao (HA) sinh ra để biến việc "Sập máy chủ" từ một thảm họa phải gọi Giám đốc dậy giữa đêm, trở thành một sự kiện rất đỗi bình thường, hệ thống tự động chạy sang máy tính dự phòng, và Lập trình viên vẫn ngủ ngon.

</details>

Hardware possesses a Mean Time Between Failures (MTBF). A hard drive will fail. A hypervisor motherboard will short-circuit. An excavator will cut an underground fiber-optic cable. In a hyper-scale environment like AWS hosting millions of servers, hardware failures are not rare anomalies; they are continuous, daily, statistical certainties.
Therefore, engineering effort cannot be spent trying to *prevent* failure (an impossible physics problem). Effort is spent engineering systems that transparently **survive** failure.
High Availability exists to abstract hardware fragility away from the business. It transforms a catastrophic hardware fire from a "Wake up the CEO at 3 AM" emergency into an invisible event handled automatically by failover logic, ensuring uninterrupted revenue flow.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh khi 1 máy chủ chứa Database bị cháy đen thui.
</details>

Visualizing a Database Server Hardware Failure.

| Metric | Single Node (No HA) | HA Cluster (Active-Passive) |
|---|---|---|
| **Immediate Effect** | Database goes offline. All APIs throw 500 Errors. | Primary Database goes offline. |
| **System Reaction** | None. Waiting for human intervention. | Keepalived detects missing heartbeat. Secondary takes over the IP automatically. |
| **Downtime** | 4 to 24 hours (Restore from backup, buy new server). | **15 to 30 Seconds** (Failover time). |
| **Data Loss (RPO)** | Lose data since the last 24h backup. | Zero data loss (Synchronous replication). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **HA ở tầng Load Balancer**: Nginx hiếm khi sập vì tải, nhưng lỡ cài nhầm phiên bản làm Nginx sập thì sao? Người ta phải cài 2 máy chủ Nginx song song. Dùng một phần mềm tên là `Keepalived` để tạo ra 1 "IP Ảo" (Virtual IP). Bình thường IP Ảo này trỏ vào Nginx A. Nếu Nginx A chết, IP Ảo lập tức tự động trỏ sang Nginx B trong 1 giây.
2. **Multi-AZ (Nhiều vùng sẵn sàng trên Cloud)**: Amazon Web Services chia 1 thành phố ra làm 3 khu vực cách nhau 50km (Gọi là Availability Zones - AZ). Họ kéo cáp quang ngầm giữa 3 khu này. Khi bạn thuê Server, bạn rải Server ra cả 3 AZ. Nếu bị đánh bom sập 1 khu AZ số 1, hai khu kia vẫn chạy bình thường. Đảm bảo "Sống sót" trước thảm họa vật lý.
3. **Storage Redundancy (RAID)**: Dữ liệu không bao giờ được lưu trên 1 ổ cứng duy nhất. Phải cắm 2 ổ cứng vào chung 1 máy tính và chạy RAID 1 (Mirror). Khi ghi dữ liệu, máy tính tự chép y chang sang ổ số 2. Cháy 1 ổ cứng, rút ra quăng thùng rác, máy tính không hề bị tắt.

</details>

1. **Edge/Load Balancer HA (Keepalived & VRRP)**: A single Nginx Load Balancer is a massive SPOF. Bare-metal HA pairs two Nginx servers (Active/Passive). They run `Keepalived` using the Virtual Router Redundancy Protocol (VRRP). They share a single floating "Virtual IP" (VIP). The Active node broadcasts a heartbeat. If it dies, the Passive node immediately aggressively claims the VIP via an ARP packet. The DNS never changes, and traffic shifts in milliseconds.
2. **Cloud Multi-AZ Deployments**: The cornerstone of Cloud Native HA. AWS constructs Data Centers in distinct clusters called Availability Zones (AZs) separated by dozens of miles, utilizing independent power grids and flood plains. Architecting for HA mandates deploying Auto Scaling Groups across at least 3 AZs. If a hurricane destroys `us-east-1a`, the Load Balancer instantly routes all traffic to `us-east-1b` and `us-east-1c`.
3. **Hardware Storage Redundancy (RAID/SAN)**: Physical disk failure is neutralized at the OS level using RAID 1 (Mirroring) or RAID 5/6 (Parity). Even further, modern Cloud Databases (like Amazon Aurora) implicitly write 6 copies of your data across 3 distinct AZs before acknowledging the Write, guaranteeing storage survival even against massive localized destruction.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Stateless Backend (Không lưu trạng thái)**: Đây là điều kiện tiên quyết ĐỂ CÓ THỂ ĐẠT ĐƯỢC HA. Đừng bao giờ lưu Ảnh của User tải lên vào thư mục ổ cứng của máy chủ Backend, cũng đừng lưu Giỏ hàng vào RAM của máy chủ đó. Nếu làm vậy, khi máy chủ cháy, ảnh và giỏ hàng cũng mất. Phải đẩy File lên S3, đẩy Giỏ hàng lên Redis. Khi Backend "Sạch sẽ" (Stateless), bạn có thể xóa nó đi, hoặc nhân bản nó lên 100 cái trong nháy mắt.
2. **Chaos Engineering (Thử nghiệm đập phá)**: Bạn nói hệ thống của bạn có HA (Sẵn sàng cao). Đừng nói suông. Hãy cài một con Bot tự động vào tối thứ 7: Bot tự động xóa 1 cái Database bất kỳ, tắt 2 cái Server bất kỳ. Nếu hệ thống của bạn tự động Failover cứu được, bạn mới thực sự có HA. Nếu không, bạn chỉ đang ảo tưởng.

</details>

1. **Stateless Compute Nodes (The Prerequisite for HA)**: You absolutely cannot horizontally scale or seamlessly failover an Application Server if it maintains local state. If you store user uploaded avatars on `ServerA/images/` or store JWT session tokens in `ServerA` RAM, and `ServerA` crashes, the state is permanently destroyed. All Compute nodes MUST be rigorously Stateless. Sessions go to Redis. Files go to S3. This allows the Auto Scaling Group to violently terminate `ServerA` and spin up `ServerB` without losing a single byte of business context.
2. **Continuous Chaos Engineering**: Proving HA requires actively breaking your system in Production. Architects construct diagrams proving $N+1$ redundancy, but misconfigured network routes often prevent the failover from executing correctly in reality. Implement Chaos Engineering (e.g., Netflix Chaos Monkey or Gremlin). Actively inject latency, terminate random EC2 instances, and simulate AZ outages during business hours to violently validate that your automated Failover actually functions under fire.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiểu lầm 100% HA (Ảo tưởng sự hoàn hảo)**: Giám đốc bắt ép Kỹ sư phải xây hệ thống có "Năm số 9" (99.999% - Tức là chỉ được chết 5 phút/năm). Nhưng họ không biết chi phí để tăng từ Ba số 9 lên Năm số 9 là gấp hàng trăm lần tiền Server (Vì phải chạy Active-Active ở 2 quốc gia khác nhau). Nếu bạn bán Phở online, chết 1 tiếng đồng hồ để sửa Database chả làm bạn phá sản đâu. Hãy dùng "Ba số 9" (99.9%) cho rẻ và thực tế.
2. **Quên mất DNS SPOF**: Bạn thuê giàn Server cực xịn trên AWS, có Load Balancer HA, có Multi-AZ đắt tiền. Nhưng bạn lại trỏ Tên miền (Domain) bằng cái hệ thống DNS cùi bắp miễn phí tặng kèm lúc mua tên miền. Khi cái hệ thống DNS cùi bắp đó sập, toàn bộ khách hàng không thể phân giải được IP của AWS $\rightarrow$ Web sập toàn tập. Nhớ rằng: HA là phải HA TỪ ĐẦU ĐẾN CUỐI.

</details>

1. **Chasing Utopian Nines (The Cost/Value Fallacy)**: Non-technical executives frequently demand `99.999%` SLA for standard applications. They do not understand the geometric cost curve of Availability. Moving from `99.9%` (Standard Multi-AZ cluster) to `99.999%` (Global Multi-Region Active-Active routing with Conflict-Free Replicated Data Types) increases architectural complexity and AWS billing by literally 50x. Unless you are Visa or a Hospital, `99.9%` (which permits 8 hours of downtime a year) is vastly more cost-effective.
2. **Hidden SPOFs (The DNS Blindspot)**: An engineering team spends 6 months designing a beautiful, highly resilient, multi-region AWS EKS architecture. However, they leave their domain `company.com` managed by a cheap, single-tenant DNS provider. When that cheap DNS provider suffers a DDoS attack, clients cannot resolve the IP address. The beautiful AWS infrastructure is perfectly healthy, but the system is 100% inaccessible. High Availability demands redundancy across the *entire* stack, crucially including Edge routing (e.g., using AWS Route 53 or Cloudflare Anycast DNS).

---

## Related Topics

- For exactly how a system switches to a backup when failure happens, read **[Failover](./failover.md)**.
- For how to recover when the ENTIRE cloud provider burns down, read **[Disaster Recovery](./disaster-recovery.md)**.
- For keeping databases in sync during all this, read **[Database Scaling](../scalability/db-scaling.md)**.
