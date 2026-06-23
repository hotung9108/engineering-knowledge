# Distributed Systems Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hệ thống phân tán (Distributed System) là việc chia nhỏ một hệ thống máy tính khổng lồ ra thành nhiều máy tính nhỏ (Node) kết nối với nhau qua mạng Internet. Thay vì mua một siêu máy tính giá 1 triệu đô, bạn mua 1000 cái máy tính cùi bắp giá 1000 đô. Nếu 1 cái máy bị cháy, 999 cái kia vẫn chạy bình thường. Đổi lại, bạn phải giải quyết hàng đống vấn đề đau đầu: Mạng bị đứt, máy tính bị sai giờ, và dữ liệu bị bất đồng bộ.

</details>

> **Summary**: A **Distributed System** is a computing paradigm where multiple, independent processing nodes—geographically separated and communicating exclusively over a network—collaborate to appear to the end-user as a single, cohesive system. Instead of scaling vertically (buying one astronomical, million-dollar supercomputer with single points of failure), architects scale horizontally (clustering thousands of cheap, commodity machines). This provides infinite scalability and massive fault tolerance. However, it introduces the most complex problems in Computer Science: Network Partitions, Clock Synchronization, and Data Consistency.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng việc nấu một bữa tiệc khổng lồ cho 10.000 người.
1. **Hệ thống Monolithic (Máy tính đơn lẻ)**: Bạn thuê 1 Siêu Đầu bếp. Ông ấy có 1 cái chảo khổng lồ to bằng cái sân vận động. Ông ấy làm mọi thứ một mình. Rất dễ quản lý. Nhưng nếu ông ấy bị ốm, toàn bộ 10.000 người sẽ chết đói. (Single Point of Failure).
2. **Hệ thống Phân tán (Distributed System)**: Bạn thuê 1000 đầu bếp bình thường. Người thái thịt, người nhặt rau, người nấu súp. Bọn họ làm việc ở 1000 nhà bếp khác nhau và dùng bộ đàm (Mạng) để gọi nhau. Nếu 5 ông đầu bếp bị ốm, 995 ông còn lại vẫn gánh được việc. Nhược điểm? Bạn sẽ phát điên vì tiếng bộ đàm ồn ào và việc phối hợp 1000 người làm sao để súp không bị quá mặn (Dữ liệu bị lỗi).

</details>

Imagine catering a massive wedding for 10,000 guests.
1. **Monolithic Architecture (Single Node)**: You hire exactly 1 Master Chef. He cooks in 1 gigantic kitchen. Coordination is perfect because everything happens in his own brain. However, if he trips and breaks his arm, the entire wedding is ruined. (Single Point of Failure / Vertical Scaling).
2. **Distributed Architecture**: You hire 1,000 amateur cooks scattered across 1,000 small kitchens around the city. They coordinate exclusively by shouting to each other over Walkie-Talkies (The Network). If 10 cooks get sick, the other 990 take over. The wedding survives. The difficulty? Orchestrating 1,000 isolated humans over static-filled Walkie-Talkies to ensure they don't accidentally bake 1,000 identical cakes while forgetting the salad entirely. (Coordination and Consistency).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hệ thống phân tán được định nghĩa bởi 3 tính chất bắt buộc:
1. **Concurrency (Chạy song song)**: Hàng ngàn máy tính cùng xử lý một bài toán cùng một lúc.
2. **No Global Clock (Không có đồng hồ chung)**: Máy tính A chỉ 12:00:00, máy tính B có thể chỉ 12:00:01 do pin CMOS khác nhau. Không bao giờ có sự đồng nhất thời gian tuyệt đối.
3. **Independent Failure (Chết độc lập)**: Máy tính A cháy nổ hoặc đứt cáp mạng không làm ảnh hưởng đến phần cứng của Máy B. Máy B có thể không hề hay biết Máy A đã chết.

</details>

A Distributed System is rigorously defined by three inherent mathematical characteristics:
1. **Concurrency**: Components execute asynchronously and concurrently. Node A processes Task X while Node B processes Task Y. They act entirely independently until forced to synchronize.
2. **Lack of a Global Clock**: A fundamental law of physics. It is impossible to perfectly synchronize the quartz oscillators of two different motherboards separated by 500 miles. Node A might timestamp an event at `00:05`, while Node B timestamps an event at `00:04`, even if A's event happened *after* B's.
3. **Independent Failure Modes**: Nodes fail in isolation. Node A can experience a catastrophic kernel panic while Node B continues processing happily. Crucially, due to network drops, Node B cannot reliably tell if Node A is actually dead, or just extremely slow to respond.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Chúng ta KHÔNG HỀ MUỐN xây dựng hệ thống Phân tán. Nó cực kỳ tốn tiền và mệt mỏi. Chúng ta bị **ÉP BUỘC** phải làm vậy vì 2 giới hạn vật lý:
1. **Đụng trần Phần cứng**: Bạn có thể mua 1 cái máy chủ RAM 1TB. RAM 2TB. Nhưng bạn không thể mua máy chủ RAM 1000TB. Các công ty như Google chứa hàng Tỷ Petabyte dữ liệu, không có 1 cái máy tính nào trên Trái Đất nhét vừa. Giải pháp duy nhất là nối 1 triệu cái ổ cứng nhỏ lại với nhau.
2. **Luật Vật lý (Tốc độ ánh sáng)**: Server của bạn đặt ở Mỹ. Khách hàng ở Việt Nam bấm nút. Dữ liệu chạy qua cáp quang dưới đáy biển (Tốc độ ánh sáng) tốn 200ms. Độ trễ vật lý này không thể nào xóa bỏ được. Bạn buộc phải đặt thêm 1 Server ở Singapore (Hệ thống phân tán) để khách Việt Nam load web trong 10ms.

</details>

Software Engineers fundamentally **do not want** to build distributed systems. They are forced into it by uncompromising constraints of Physics and Economics.
1. **Vertical Scaling Ceilings**: You can upgrade a single monolithic server from 32GB of RAM to 2TB of RAM (Vertical Scaling). But you cannot purchase a server with 500 Exabytes of RAM. When organizations like Google or Amazon ingest petabytes of telemetry per day, no single machine on the planet can process or store it. You are mathematically forced to split the data across thousands of commodity machines (Horizontal Scaling).
2. **The Speed of Light (Latency Limits)**: If your Single Server is in New York, a user in Tokyo will experience at least 150ms of latency (ping) purely due to the physical distance fiber optic light must travel. The only way to provide 10ms latency to the Tokyo user is to deploy a replicated Server physically located in Tokyo. You have just created a Distributed System.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh độ phức tạp khi Giao tiếp.
</details>

Visualizing the transition from Local execution to Network execution.

| Characteristic | Monolithic (Single Server) | Distributed System (Microservices) |
|---|---|---|
| **Communication** | Fast In-Memory Function Call (Nanoseconds) | Slow Network RPC / HTTP Call (Milliseconds) |
| **Failure Rate** | Binary (Either entirely UP or entirely DOWN) | **Partial Failures** (30% degraded, 70% working) |
| **State Consistency**| Trivial (One Database, One Source of Truth) | Brutal (CAP Theorem, Eventual Consistency) |
| **Max Capacity** | Hardware Limits (e.g., 100k requests/sec) | Theoretically Infinite |
| **Debugging** | Easy (Single Stack Trace) | Nightmare (Requires Distributed Tracing) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Mọi công nghệ hiện đại ngày nay đều là Hệ thống Phân tán:
- **World Wide Web (Internet)**: Hệ thống phân tán lớn nhất lịch sử nhân loại. Hàng tỷ máy tính kết nối nhau vô chính phủ.
- **Microservices**: Bạn xé cái App của bạn ra làm 20 Services chạy trên 20 cái Docker Container, gọi nhau bằng API. Chúc mừng, bạn đang vận hành một Hệ thống phân tán.
- **Blockchain & Crypto**: Phân tán thuần túy. 10.000 máy tính đào Bitcoin khắp thế giới cùng nhau duy trì 1 cuốn sổ cái mà không cần ai đứng đầu.
- **Hệ thống Database lớn**: Cassandra, MongoDB Cluster, Redis Cluster, Elasticsearch.

</details>

Distributed Systems form the absolute bedrock of modern civilization.
- **The Internet (WWW)**: The largest, most chaotic distributed system in human history. Billions of autonomous, heterogeneous nodes communicating via standard TCP/IP protocols with zero central authority.
- **Cloud Computing & Microservices**: If you split a monolithic API into a `User Service` and an `Order Service` running in separate Kubernetes pods, you have built a Distributed System. You must now deal with network drops between the pods.
- **Blockchain / DLT**: The ultimate expression of a trustless distributed system. Thousands of geographically isolated nodes achieving consensus on a decentralized ledger (Bitcoin/Ethereum) without a central coordinating server.
- **Distributed Databases**: Apache Cassandra, MongoDB Sharded Clusters, Elasticsearch. They slice monolithic data into Shards and replicate them across multiple hard drives on different continents.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiểu rõ Định lý CAP**: Trong hệ thống phân tán, khi Mạng bị đứt (Partition), bạn chỉ được chọn 1 trong 2: Hoặc là Khóa hệ thống không cho ai truy cập (Consistency - Tính nhất quán), Hoặc là cho phép truy cập nhưng Dữ liệu bị sai lệch (Availability - Tính sẵn sàng). Bạn KHÔNG THỂ có cả 3.
2. **Lập trình phòng thủ (Defensive Programming)**: Bạn viết hàm A gọi API sang máy B. Đừng bao giờ đinh ninh máy B sẽ trả lời. Mạng luôn luôn rớt. Bạn PHẢI viết code: "Nếu máy B báo lỗi (Timeout), tao sẽ chờ 3s rồi gọi lại (Retry). Nếu gọi 3 lần vẫn lỗi, tao sẽ dùng cái cầu dao ngắt điện (Circuit Breaker) để không gọi nữa, báo lỗi thẳng ra cho Khách hàng".

</details>

1. **Internalize the CAP Theorem**: The foundational law of distributed data. Given a network Partition (P) - which is an unavoidable physical reality - you must choose between Consistency (C) and Availability (A). If the network splits your Asian and American database nodes, do you halt all trading to prevent mismatched balances (Choosing C), or do you let people trade but risk data collisions later (Choosing A)? You cannot cheat physics.
2. **Defensive Architecture (Design for Failure)**: In a monolith, `functionA()` calling `functionB()` practically never fails unless the RAM explodes. In a distributed system, `ServiceA` calling `ServiceB` travels through routers, switches, and firewalls. Packets will drop. You MUST engineer **Resilience Patterns**: Timeouts, Exponential Backoff Retries, and Circuit Breakers. Assume the network is actively hostile.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **8 Ngộ nhận của Hệ thống Phân tán (Fallacies of Distributed Computing)**: Lập trình viên mới vào nghề hay ảo tưởng rằng:
   - "Mạng đáng tin cậy 100%" (Sai, đứt cáp mập cắn hoài).
   - "Độ trễ bằng 0" (Sai, ping luôn tốn mili-giây).
   - "Băng thông là vô hạn" (Sai, nhét 1 file 5GB qua mạng LAN là sập ngay).
   Cứ viết code dựa trên những ngộ nhận này, khi đưa lên Production hệ thống sẽ sụp đổ hoàn toàn.
2. **Microservices theo phong trào**: Nghe nói Microservices xịn lắm, bạn xé cái đồ án tốt nghiệp của mình ra thành 50 cái Microservices bé tí. Cuối cùng, thay vì gỡ lỗi (Debug) 1 file code, bạn phải đi lục lọi Log của 50 con Server khác nhau. Đừng xé nhỏ hệ thống cho đến khi nó thực sự quá tải. Bắt đầu bằng Monolithic.

</details>

1. **The 8 Fallacies of Distributed Computing**: Coined by L. Peter Deutsch at Sun Microsystems. Junior developers architect systems based on naive assumptions: "The network is reliable", "Latency is zero", "Bandwidth is infinite", "Topology doesn't change". Code built on these fallacies performs flawlessly on a single localhost laptop, but implodes violently when deployed across a chaotic AWS multi-region VPC.
2. **Microservice Madness (Distributed Monoliths)**: Splitting a perfectly functional, maintainable Monolith into 30 Microservices simply for "resume driven development". You replace fast, reliable in-memory function calls with slow, unreliable network HTTP calls. You create a "Distributed Monolith"—a system so tightly coupled that if Service A goes down, Services B through Z all immediately crash. **Rule**: Always start Monolithic. Extract domains into distributed services only when scaling pain makes it absolutely unavoidable.

---

## Related Topics

- For the absolute most important rule in this field, see **[Consistency / CAP Theorem](../consistency/overview.md)**.
- For how multiple machines agree on 1 sự thật, read **[Consensus Algorithms](./consensus.md)**.
- For how transactions work across multiple DBs, see **[Distributed Transactions](./transactions.md)**.
