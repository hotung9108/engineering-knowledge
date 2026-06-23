# Failover

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Chữ "Fail" nghĩa là lỗi, "Over" là chuyển giao. **Failover (Chuyển đổi dự phòng)** là hành động tự động hoặc thủ công chuyển luồng truy cập của khách hàng từ một máy chủ (hoặc hệ thống) ĐANG CHẾT sang một máy chủ DỰ PHÒNG đang sống. Nó giống như việc cầu thủ đá chính bị gãy chân, huấn luyện viên lập tức đưa cầu thủ dự bị vào sân đá thay để trận đấu không bị hủy. Để làm được Failover, bạn bắt buộc phải có máy chủ dự phòng (Redundancy) và phải có cơ chế **Heartbeat (Nhịp tim)** để biết chính xác khi nào máy chủ chính bị chết.

</details>

> **Summary**: Redundancy (having backup hardware) is useless if the system cannot automatically route traffic to it during an outage. **Failover** is the active operational mechanism within High Availability that executes the transition. When a Primary node (Active) suffers a critical fault, the Failover process detects the failure—usually via a missed TCP/UDP Heartbeat—and aggressively re-routes all incoming network traffic and systemic responsibilities to the Secondary node (Passive/Standby). The goal of Failover is to execute this transfer so rapidly that the end-user experiences nothing more than a momentary spike in latency, completely masking the catastrophic hardware failure underneath.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một chiếc máy bay có 2 Phi công: Cơ trưởng (Chính) và Cơ phó (Dự phòng).
1. **Không có Failover**: Cơ trưởng đang lái máy bay thì bị đột quỵ ngất xỉu. Cơ phó ngồi bên cạnh nhưng không biết lái (hoặc không được quyền cầm cần lái). Máy bay rơi tự do. (Hệ thống sập).
2. **Có Failover**: Cơ trưởng ngất xỉu. Bàn tay ông ấy buông khỏi cần gạt (Mất Heartbeat). Ngay lập tức, màn hình máy tính của Cơ phó hiện dòng chữ màu đỏ: "BẠN ĐÃ NẮM QUYỀN ĐIỀU KHIỂN". Cơ phó lập tức cầm cần lái kéo máy bay bay thẳng lên. Hành khách ngồi phía sau chỉ thấy máy bay hơi rung lắc một chút rồi lại êm ru, không ai biết ông Cơ trưởng vừa đột quỵ.

</details>

Imagine a Live TV News Broadcast.
1. **No Failover**: The Main Anchor is reading the news. Her microphone suddenly breaks. The screen goes completely silent. Millions of viewers change the channel. The broadcast is ruined.
2. **With Failover**: The Main Anchor is speaking. Her microphone breaks. The Audio Engineer in the back room instantly detects the silence (Loss of Heartbeat). Within 1 second, he physically flips a switch to turn on the Backup Anchor's microphone. The Backup Anchor smoothly takes over the sentence. The viewers barely noticed the 1-second pause. The switch flipping is the "Failover".

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hệ thống Failover được chia thành 2 mô hình chính:
1. **Active - Passive (Chính - Phụ)**: Máy Chính (Active) gánh 100% người dùng. Máy Phụ (Passive) nổ máy sẵn, đồng bộ dữ liệu liên tục nhưng CHỈ NGỒI CHƠI, không phục vụ ai cả. Khi máy Chính chết, máy Phụ mới nhảy lên làm Máy Chính.
   - *Ưu điểm*: Code rất dễ, không bao giờ lo dữ liệu bị xung đột.
   - *Nhược điểm*: Rất phí tiền. Bạn mua cái Server 10.000$ chỉ để nó ngồi chơi.
2. **Active - Active (Chính - Chính)**: Cả 2 máy đều mở cửa đón khách (Ví dụ 50% - 50%). Khi 1 máy chết, Load Balancer tự động dồn 100% khách sang máy còn sống.
   - *Ưu điểm*: Tận dụng tối đa 100% tiền mua Server.
   - *Nhược điểm*: Code cực khó (Làm sao để 2 máy tính cách nhau 50km cùng sửa 1 dòng Database mà không bị ghi đè lên nhau?). Thường chỉ dùng cho Web Server (Stateless), hiếm khi dùng cho Database.

</details>

Failover topologies are broadly categorized into two architectural paradigms:
1. **Active-Passive (Standby) Failover**: Only the Primary node actively processes incoming traffic. The Secondary node is fully booted and constantly replicates state from the Primary, but it does not serve requests. It strictly monitors the Primary. If the Primary dies, the Secondary assumes the Primary IP/Role.
   - *Pros*: Architecturally simple. Eradicates Database split-brain and concurrent mutation conflicts.
   - *Cons*: Poor resource utilization. You are paying 100% infrastructure cost for a node that sits at 1% CPU utilization indefinitely until a disaster occurs.
2. **Active-Active Failover**: Both nodes aggressively process live traffic simultaneously, typically sitting behind a Load Balancer (Round Robin). If Node A dies, the LB detects the failure and instantly re-routes 100% of traffic to Node B.
   - *Pros*: 100% resource utilization. Can handle twice the traffic volume during normal operations.
   - *Cons*: Extremely difficult to engineer for Stateful layers (Databases). Requires complex Bi-directional replication and Conflict Resolution (CRDTs) to prevent concurrent write anomalies.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Failover tồn tại để giải quyết bài toán "Thời gian Phục hồi" (RTO - Recovery Time Objective).
Nếu một máy chủ Database vật lý bốc cháy. Quy trình phục hồi bằng Sức Người (Manual) sẽ là: 
1. Kỹ sư bị gọi dậy lúc 2h sáng. 
2. Mở máy tính, dò tìm nguyên nhân. 
3. Lên Cloud thuê 1 cái máy chủ mới. 
4. Tải file Backup 500GB từ hôm qua về $\rightarrow$ Tốn 4 tiếng đồng hồ. 
Công ty mất hàng triệu đô la doanh thu.
Failover Tự động (Automated Failover) được sinh ra để biến cái quy trình 4 tiếng đồng hồ đó thành... 10 GIÂY. Không cần kỹ sư phải thức dậy. Phần mềm sẽ tự động phát hiện lỗi, tự động trỏ IP sang máy phụ (đã có sẵn data đồng bộ). Công ty vẫn kiếm tiền trong lúc kỹ sư đang ngủ.

</details>

Failover strictly exists to aggressively minimize the **RTO (Recovery Time Objective)**.
Consider a manual recovery protocol when a primary PostgreSQL instance kernel panics at 3:00 AM:
1. PagerDuty wakes up the DevOps Engineer. (5 mins)
2. Engineer logs into the VPN and identifies the dead node. (10 mins)
3. Engineer provisions a new EC2 instance and initiates a 500GB SQL dump restoration. (4 hours).
This 4-hour RTO is an unacceptable business catastrophe. Automated Failover transforms this human-driven, multi-hour disaster into a 15-second, invisible blip. The Keepalived daemon detects the missed heartbeat and instantly issues an ARP broadcast claiming the Virtual IP. The Passive Replica becomes the Primary. The business continues operating while the Engineer sleeps.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh hiện tượng khi Máy chủ Web (App Server) bị cúp điện.
</details>

Visualizing an App Server failure behind a Load Balancer.

| Phase | No Failover Mechanism | Automated Active-Active Failover |
|---|---|---|
| **Outage Occurs** | Server A loses power. | Server A loses power. |
| **Load Balancer (LB)** | Blindly keeps sending 50% traffic to Server A. | LB Health Check (Ping) fails for Server A. |
| **Action** | None. | LB instantly removes Server A from the Target Group. |
| **User Experience** | 50% of users see White Screen / Timeout. | 100% of users successfully routed to Server B. |
| **Resolution** | Requires human to reboot Server A. | Auto-Scaling Group automatically spins up Server C to replace A. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **DNS Failover (Amazon Route 53)**: Ở cấp độ toàn cầu. Bạn có 2 cụm máy chủ ở VN và Sing. Route 53 sẽ "Ping" cụm VN liên tục. Nếu đứt cáp quang biển làm cụm VN sập, Route 53 sẽ tự động sửa Tên miền `congty.com` trỏ thẳng sang IP của cụm ở Sing. Toàn bộ người dùng tự động được kéo sang Sing.
2. **Database Failover (Redis Sentinel / Patroni)**: Database rất khó để tự động đổi ngôi. Người ta phải tạo ra các phần mềm đứng trung gian "Giám sát" (Ví dụ Redis Sentinel). Khi Sentinel thấy Redis Master bị chết, nó sẽ ra lệnh cho Redis Slave: "Mày lên làm Master đi", sau đó nó báo cho Code Backend biết: "IP mới của Master là xxx nhé, ghi vào đó đi".
3. **Floating IP (IP Ảo nổi)**: Một kỹ thuật cực hay của các Load Balancer (HAProxy). Hai máy chủ A và B có 2 IP thực khác nhau. Nhưng chúng dùng chung 1 cái IP Ảo (Ví dụ `10.0.0.99`). Bằng giao thức VRRP, mạng sẽ trỏ IP 99 vào máy A. Nếu máy A chết, máy B lập tức giật lấy cái IP 99 đó. Khách hàng chỉ cần nhớ IP 99, không cần biết máy A hay B đang chạy.

</details>

1. **Global DNS Failover (Route 53 / Cloudflare)**: The outermost layer of resilience. You host Datacenter A (Primary) in US-East and Datacenter B (Passive) in EU-West. AWS Route 53 continually executes active Health Checks against US-East. If a hurricane destroys US-East, Route 53 dynamically updates the DNS `A` records to point `api.example.com` directly to the EU-West IP addresses. Traffic fails over globally.
2. **Stateful Failover (Redis Sentinel / Patroni for PostgreSQL)**: RDBMS failover cannot rely solely on Load Balancers; it requires electing a new "Master" to accept Writes. Tools like Redis Sentinel act as a cluster of intelligent Watchdogs. If the Master dies, the Sentinels use a Quorum vote to agree it's dead, explicitly promote a specific Slave to Master, and then publish the new Master's IP address to the application code so it can update its connection pool dynamically.
3. **Layer 4 Virtual IPs (Keepalived / VRRP)**: A bare-metal technique. Two physical Nginx Load Balancers (Node 1 and Node 2) share a "Floating" Virtual IP (e.g., `192.168.1.100`). Node 1 actively holds the VIP and broadcasts a heartbeat. If Node 1's power cord is pulled, the heartbeat stops. Node 2 instantly detects the silence, executes a Gratuitous ARP request to the network switch, and physically takes ownership of `192.168.1.100`. The failover is entirely transparent to clients.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Failback (Chuyển ngược lại) phải làm bằng tay**: Khi máy A chết, tự động Failover sang máy B là đúng. NHƯNG, khi máy A sống lại, TUYỆT ĐỐI KHÔNG được tự động Failback (Chuyển từ B về A). Máy A vừa khởi động lại, còn đang rất yếu (chưa nạp cache, phần cứng chưa ổn định), nếu dội 100% traffic về nó, nó sẽ chết tiếp (Flapping). Việc đưa máy A vào lưới điện trở lại phải do Kỹ sư tự tay gõ lệnh sau khi đã kiểm tra kỹ lưỡng.
2. **Luôn chạy thử Failover (Drills)**: Đừng tin vào Code Failover trừ khi bạn đã thấy nó chạy. 90% hệ thống CÓ CAI ĐẶT Failover, nhưng khi sự cố thật xảy ra thì Failover bị lỗi (Do cấu hình sai IP, sai Password, Firewall chặn). Phải định kỳ 6 tháng 1 lần chủ động tắt máy chủ để test Failover.

</details>

1. **Automate Failover, but Manual Failback**: A critical operational rule. If Node A (Primary) panics, automated failover perfectly routes traffic to Node B (Secondary). However, when Node A eventually reboots and comes back online, you MUST NOT automatically Failback (transfer Primary status back to Node A). Node A's cache is completely cold, and the hardware might still be unstable. An automated failback will likely instantly crash Node A again, creating an infinite Ping-Pong loop of downtime. Failback must be a manual, calculated operational procedure executed during off-peak hours.
2. **Continuous Failover Drills (Game Days)**: The absolute worst time to find out your automated Failover script has a typo is at 3:00 AM during a real outage. Configuration drift is real: someone updated a firewall rule 3 months ago that accidentally blocks the VRRP heartbeat protocol. You must actively execute "Game Days" (Chaos Engineering) where you intentionally terminate the Primary Database in Production. If the business survives, you have HA. If it drops, you fix the script.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hội chứng Split-Brain (Đa nhân cách)**: Máy A (Chính) và Máy B (Phụ). Mạng ở giữa bị đứt. Máy B tưởng máy A đã chết, nên B tự xưng làm Máy Chính. Thực ra A chưa chết, A vẫn xưng làm Máy Chính. Giao diện Load Balancer dội 50% khách vào A, 50% khách vào B. Dữ liệu bị ghi đè nát bét (Tài khoản ông A vừa mất tiền ở máy A, vừa có tiền ở máy B).
   - *Cách giải quyết (Quorum)*: Bắt buộc phải có thêm máy C (Người phân xử). Khi đứt mạng, máy nào được máy C bầu chọn (2 phiếu) thì mới được làm Chính. Ai có 1 phiếu thì phải tự nguyện khóa mồm lại.
2. **Failover Cascading (Chết chùm)**: Hệ thống bình thường cần 5 máy chủ để chạy mượt. Bạn có 1 máy dự phòng (Tổng 6 máy). Sự cố xảy ra làm CHÁY 2 máy. 4 máy còn lại phải gồng gánh 100% lượng khách. Vì quá tải, 4 máy kia chạy được 10 phút rồi cũng bốc khói nổ tung nốt.
   - *Cách giải quyết*: Failover phải đi kèm với Auto-Scaling (Tự động thuê thêm Server). Và phải dùng **Rate Limiting** để chặn bớt khách lại, bảo vệ các máy chủ sống sót khỏi bị đè chết.

</details>

1. **The Split-Brain Catastrophe**: The most feared scenario in Database failover. Node A (Active) and Node B (Passive) are communicating via a heartbeat cable. Someone unplugs the heartbeat cable. Node B stops receiving heartbeats, assumes Node A is dead, and promotes itself to Active. However, Node A is perfectly healthy and is still receiving internet traffic. You now have TWO Active Masters independently mutating data without syncing. The database is permanently corrupted.
   - *The Fix (Quorum / STONITH)*: Never use a 2-node cluster for stateful failover. You MUST have a 3rd Node (An Arbiter or Witness). Failover requires a strict Quorum ($N/2 + 1$ votes). If the heartbeat cable breaks, Node A and Node B cannot talk. But Node A can talk to the Arbiter (2 votes). Node A stays Active. Node B only has 1 vote, so it mathematically demotes itself, preventing Split-Brain.
2. **Insufficient Failover Capacity**: You have an Active-Active cluster of 2 servers. Normal traffic utilizes 80% CPU on Server A, and 80% CPU on Server B. Server A dies. Failover perfectly routes 100% of traffic to Server B. Server B instantly spikes to 160% CPU requirement, violently runs out of RAM, and crashes. The Failover mechanism literally caused a total system collapse. **Rule**: In Active-Active HA, nodes must never run above 40% CPU utilization during normal operations, ensuring they can safely absorb the partner's load during an outage.

---

## Related Topics

- For how to prevent the Split-Brain scenario, read about Quorum in **[Consensus Algorithms](../distributed-system/consensus.md)**.
- For managing traffic when the remaining servers are overloaded, use **[Rate Limiting](../scalability/rate-limiting.md)**.
- For moving traffic globally across countries, explore **[Disaster Recovery](./disaster-recovery.md)**.
