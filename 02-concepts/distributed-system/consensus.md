# Consensus Algorithms

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trong hệ thống phân tán, có 5 máy chủ cùng chạy để gánh tải. Nếu 1 người dùng chuyển 100k, Máy 1 báo "Chuyển thành công", nhưng Máy 2 chưa kịp nhận được tín hiệu nên vẫn báo "Chưa chuyển". Vậy cuối cùng tiền đã chuyển hay chưa? Cả 5 máy tính phải "cãi nhau" và đi đến một Tuyên bố thống nhất. **Thuật toán Đồng thuận (Consensus Algorithms)** là luật bầu cử giúp hàng ngàn máy tính độc lập có thể "Đồng ý" về một sự thật duy nhất, bất chấp mạng đứt, máy chết, hay thậm chí có máy chủ làm phản.

</details>

> **Summary**: In a Distributed System, State (Data) is replicated across multiple independent nodes to ensure fault tolerance. However, if a network partition occurs or a node crashes mid-transaction, Node A might possess a different version of reality than Node B. How does a decentralized cluster agree on a single, indisputable Source of Truth? **Consensus Algorithms** are mathematically rigorous protocols designed to solve this exact problem. They enable a cluster of unreliable machines to robustly agree on a single shared state, even in the presence of node failures and severe network unreliability.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một nhóm bạn 5 người đang bàn xem tối nay ăn gì.
1. **Chế độ Độc tài (Master-Slave)**: Có 1 người là Nhóm trưởng (Master). Nhóm trưởng phán "Ăn Phở!". 4 người kia (Slave) lẳng lặng đi ăn Phở. Rất nhanh, nhưng nếu Nhóm trưởng lăn ra ngủ, cả đám sẽ chết đói vì không ai dám quyết.
2. **Thuật toán Đồng thuận (Bầu cử Dân chủ)**: Không có nhóm trưởng cố định. Một người hô lên: "Ăn Phở nhé?". Các người khác sẽ "Vote" (Bỏ phiếu). Chỉ khi nào có **Quorum** (Đa số quá bán, tức là >= 3 người) giơ tay đồng ý, thì quyết định "Ăn Phở" mới chính thức được ghi vào sổ. Nếu có 1 người bị ốm nằm ở nhà, 4 người còn lại vẫn đủ sức Vote ra quyết định. Bọn họ "Đồng thuận" với nhau.

</details>

Imagine a group of 5 generals trying to coordinate an attack.
1. **The Dictatorship (Master-Replica)**: One General is the Supreme Commander (The Master). He commands: "Attack at dawn!". The 4 lieutenants (Replicas) obey blindly. It is lightning fast. But if the Commander is assassinated (Node Failure), the 4 lieutenants stand frozen, unable to make a decision, and the army collapses.
2. **The Consensus Protocol (Democracy)**: There is no permanent Commander. Any general can propose a plan: "Let's attack!". They then hold a vote. The plan is only approved if a **Quorum** (a strict majority, i.e., 3 out of 5) explicitly votes "Yes". If 2 generals have their radios broken, the remaining 3 can still successfully vote and execute the attack. They have achieved "Consensus".

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Có 3 khái niệm cốt lõi trong mọi thuật toán đồng thuận:
1. **Quorum (Đa số quá bán)**: Công thức là `(N/2) + 1`. Nếu cụm có 5 máy, cần 3 máy đồng ý. Nếu có 3 máy, cần 2 máy đồng ý. Nếu một quyết định được Quorum thông qua, nó được coi là "Chân lý" (Committed).
2. **Paxos**: Thuật toán đồng thuận huyền thoại nhất, được phát minh bởi Leslie Lamport. Rất hoàn hảo về mặt toán học, nhưng cực kỳ khó hiểu và khó code. Chỉ có Google hoặc Amazon mới đủ trình độ dùng.
3. **Raft**: Thuật toán sinh ra để "dễ hiểu" hơn Paxos. Nó chia bài toán làm 3 phần: Bầu Leader (Bầu cử), Sao chép Log (Ghi sổ), và Xử lý an toàn. 90% các hệ thống hiện đại (như Kafka, etcd, MongoDB) đều xài Raft.

</details>

Consensus Algorithms are built upon fundamental mathematical concepts:
1. **The Quorum (Strict Majority)**: The holy formula is `(N/2) + 1`. In a 5-node cluster, a Quorum is 3. In a 3-node cluster, a Quorum is 2. A piece of data is only considered "Safely Committed" if a Quorum of nodes acknowledges receiving it. This mathematically prevents the "Split-Brain" problem.
2. **Paxos**: The primordial, legendary consensus algorithm formulated by Leslie Lamport. It is mathematically flawless but notoriously incomprehensible and extraordinarily difficult to implement in real-world systems.
3. **Raft**: Designed explicitly for "Understandability" as an alternative to Paxos. It decomposes the consensus problem into three distinct, manageable sub-problems: Leader Election, Log Replication, and Safety. It is the architectural engine behind almost all modern Distributed Systems (e.g., etcd, HashiCorp Consul, Apache Kafka's KRaft).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao không dùng 1 con Master cho rồi, rườm rà Quorum làm gì?
Bài toán **Split-Brain (Tâm thần phân liệt)**. Giả sử bạn có 2 máy chủ A và B, hoạt động Master-Master. Đột nhiên đứt cáp mạng ở giữa. A không nhìn thấy B, A tưởng B chết rồi nên A tự xưng làm Vua. B không nhìn thấy A, B tưởng A chết rồi nên B cũng tự xưng làm Vua. Lúc này, khách hàng 1 chọc vào A, khách hàng 2 chọc vào B. Cả A và B đều tự do ghi đè dữ liệu. Khi mạng có lại, dữ liệu của A và B hoàn toàn khác nhau, hệ thống "phân liệt" và phá hủy toàn bộ dữ liệu.
Nhờ có **Quorum**, nếu dùng 3 máy. Mạng đứt chia làm 2 phe: Phe 1 máy và Phe 2 máy. Phe 1 máy sẽ không bao giờ đạt được Quorum (Cần 2 phiếu), nên nó tự khóa lại không cho ghi dữ liệu. Phe 2 máy đạt Quorum nên vẫn hoạt động bình thường. Lỗi Split-Brain bị tiêu diệt hoàn toàn.

</details>

Why endure the heavy network latency of Consensus Algorithms instead of just using a simple Multi-Master setup?
To prevent the catastrophic **Split-Brain Problem**.
Imagine a 2-node cluster (Node A and Node B) in an Active-Active setup. A network switch fails, severing the connection between A and B. Node A can no longer ping Node B. Node A assumes B is dead and declares itself the sole Dictator. Node B assumes A is dead and also declares itself the sole Dictator.
Client 1 writes data to A. Client 2 writes conflicting data to B. When the network is restored, A and B have massively diverging datasets. The system is permanently corrupted.
**Quorum mathematics annihilates Split-Brain**. If you use a 3-node cluster and a network split occurs, you get a 2-Node partition and a 1-Node partition. The 1-Node partition realizes it does not have a Quorum (`1 < 2`), and immediately locks itself into Read-Only mode. The 2-Node partition has a Quorum (`2 >= 2`) and continues accepting Writes. The cluster survives flawlessly.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh độ An toàn Dữ liệu giữa Cụm chẵn (Không an toàn) và Cụm lẻ (Có Consensus).
</details>

Visualizing why Distributed Clusters MUST always have an ODD number of nodes (3, 5, 7).

| Scenario | 2-Node Cluster (No Consensus) | 3-Node Cluster (Raft Consensus) |
|---|---|---|
| **Network Partition** | Network splits exactly down the middle (1 vs 1). | Network splits into (2 vs 1). |
| **Quorum Required**| Needs 2 nodes to agree. Neither side has 2. | Needs 2 nodes to agree. The 2-node side has it. |
| **System State** | Complete Deadlock OR Split-Brain Corruption. | 1 side operates normally. 1 side pauses. |
| **Fault Tolerance** | Can survive **0** failures. | Can survive **1** failure. |
| **Rule of Thumb** | **NEVER deploy a 2-node DB cluster**. | The standard for Production (etcd/Zookeeper). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Kubernetes (etcd)**: Bộ não của toàn bộ hệ thống Kubernetes là một database nhỏ tên là `etcd`. Nó xài thuật toán Raft. Toàn bộ cấu hình mạng, IP, trạng thái Container đều được thống nhất qua Quorum của etcd.
2. **Apache Kafka (Zookeeper / KRaft)**: Để quyết định xem Broker nào trong cụm Kafka được quyền làm Leader của một Partition, nó phải tổ chức "Bầu cử" bằng thuật toán đồng thuận.
3. **Tiền ảo (Blockchain)**: Thuật toán đồng thuận BFT (Byzantine Fault Tolerance) như Proof-of-Work của Bitcoin. Khác với Raft (chỉ chống máy tính chết), BFT sinh ra để chống lại cả máy tính LÀM PHẢN (Cố tình báo kết quả láo để ăn cắp tiền). Cần tới siêu nhiều điện và toán học để đạt đồng thuận BFT.

</details>

1. **Service Discovery & Configuration (etcd / Consul)**: The central nervous system of Kubernetes. `etcd` is a highly-available Key-Value store powered by the Raft consensus algorithm. It holds the absolute, indisputable truth regarding the state of every Pod, IP address, and Secret in the cluster.
2. **Distributed Commit Logs (Apache Kafka)**: Historically, Kafka relied on a separate 3-node Apache ZooKeeper (ZAB protocol) cluster to elect leaders and manage metadata. Modern Kafka (KRaft) has internalized the Raft algorithm directly into its Brokers to achieve self-managed consensus.
3. **Decentralized Finance (Blockchain / BFT)**: Protocols like Raft assume nodes might crash (Fail-Stop), but assume nodes do not explicitly lie. In decentralized networks (Bitcoin), you must assume nodes are actively malicious (The Byzantine Generals Problem). Blockchains utilize **Byzantine Fault Tolerant (BFT)** consensus algorithms (e.g., Proof-of-Work, Proof-of-Stake) to achieve consensus even when 33% of the network is actively trying to hack the system.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Quy tắc Số Lẻ**: LUÔN LUÔN triển khai các hệ thống Database/Cache phân tán với số lượng Node là SỐ LẺ (3, 5, 7). Đừng bao giờ triển khai 2, 4, 6 Node. Nếu có 4 Node, Quorum là 3. Nếu chết 2 Node, Quorum thất bại, hệ thống sập. Nó cồng kềnh bằng hệ thống 5 Node (Cũng chết được 2 Node) nhưng lại tốn tiền vô ích.
2. **Triển khai đa vùng (Multi-AZ)**: Đừng đặt 3 Node của cụm Raft chung vào 1 tòa nhà. Nếu cúp điện tòa nhà đó, cả 3 Node chết $\rightarrow$ Mất Quorum. Hãy đặt Node 1 ở Tòa A, Node 2 ở Tòa B, Node 3 ở Tòa C. Khi một tòa nhà cháy, bạn mất 1 Node, 2 Tòa kia vẫn giữ được Quorum và hoạt động bình thường.

</details>

1. **The Odd-Number Rule**: You must **ALWAYS** provision consensus-based clusters (ZooKeeper, etcd, MongoDB Config Servers) with an ODD number of nodes (3, 5, or 7). Provisioning an even number (like 4 or 6) is a mathematical anti-pattern. In a 4-node cluster, the Quorum is 3. It can only survive 1 failure. A 3-node cluster also survives 1 failure. A 4-node cluster provides zero additional fault tolerance, increases network chatter, and costs more money.
2. **Geographic Fault Domains (Multi-AZ)**: Never place your entire 3-node Raft Quorum inside the same physical server rack. If the Top-Of-Rack (TOR) switch blows a fuse, you lose all 3 nodes simultaneously, causing total cluster paralysis. Deploy nodes across diverse Availability Zones (AZs). E.g., Node 1 in `us-east-1a`, Node 2 in `us-east-1b`, Node 3 in `us-east-1c`. The loss of an entire physical datacenter only destroys 1 node, leaving the Quorum intact.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiệu ứng Bầu cử Lặp vô hạn (Split Vote)**: Trong Raft, khi các Node bầu Leader, đôi khi 2 Node cùng ứng cử một lúc, chia đều số phiếu, không ai đủ Quorum. Chúng lại bầu lại, lại hòa. Cụm Server bị tê liệt vì mải mê đi bầu cử mà không lo phục vụ khách hàng. 
   - *Cách giải quyết*: Phải cài đặt "Đồng hồ đếm ngược ngẫu nhiên" (Randomized Election Timeout). Node A đếm 150ms, Node B đếm 300ms. Node A sẽ luôn hết giờ trước và ứng cử trước, tránh được chuyện 2 thằng cùng hô một lúc.
2. **Nút thắt cổ chai Độ trễ (Latency Bottleneck)**: Bạn đặt Node 1 ở Việt Nam, Node 2 ở Mỹ, Node 3 ở Châu Âu. Khi khách hàng bấm "Lưu", Node 1 phải chờ Node 2 ở tận bên Mỹ gửi tin nhắn "Đồng ý" (Mất 300ms) để đạt Quorum. Khách hàng sẽ chửi vì web quá chậm. Đừng bao giờ đặt cụm Quorum cách nhau quá nửa vòng Trái Đất trừ khi bạn chấp nhận hy sinh tốc độ (Tính nhất quán cao thì Độ trễ phải cao).

</details>

1. **Infinite Election Loops (Split Votes)**: In the Raft protocol, if the Leader dies, the Followers wait for a timeout, then trigger an Election. If Follower A and Follower B trigger an election at the *exact same millisecond*, they split the votes. Neither achieves a Quorum. They restart the election and tie again. The cluster remains paralyzed indefinitely. **Fix**: Raft solves this elegantly using **Randomized Election Timeouts** (e.g., Node A waits between 150ms and 300ms). Node A will invariably timeout earlier, declare candidacy, and win the Quorum before Node B even wakes up.
2. **The Quorum Latency Penalty**: Junior architects globally distribute a 3-node MongoDB cluster (e.g., Tokyo, Virginia, Frankfurt) for "maximum disaster recovery". A user in Tokyo writes data. To achieve Quorum, the Tokyo node must execute a synchronous network round-trip to Virginia (200ms ping). The write operation blocks for 200ms. The application's latency is absolutely destroyed by the speed of light. **Rule**: Consensus Algorithms require aggressive synchronous network chatter. Keep the nodes in close geographic proximity (same Region, different AZs) to maintain single-digit millisecond Quorum latency.

---

## Related Topics

- For the foundational rule of Distributed Data, see **[Consistency / CAP Theorem](../consistency/overview.md)**.
- For how this applies to databases explicitly, study **[Distributed Transactions](./transactions.md)**.
- For how node services find each other when they spin up, see **[Service Discovery](./discovery.md)**.
