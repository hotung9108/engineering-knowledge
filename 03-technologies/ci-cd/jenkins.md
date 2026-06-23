# Jenkins

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước khi có Cloud và Github Actions, **Jenkins** chính là Vua của thế giới CI/CD. Khác với Github Actions (vốn là dịch vụ Cloud người ta chạy sẵn cho bạn), Jenkins là một phần mềm bạn tự mang về cài lên máy chủ của công ty (Self-hosted). Vì bạn có toàn quyền sở hữu máy chủ đó, bạn có thể biến hóa Jenkins làm mọi thứ trên đời thông qua hàng ngàn Plugin do cộng đồng viết. Bạn muốn nó gọi điện thoại báo thức khi Code lỗi? Cài Plugin. Bạn muốn nó tự bật đèn LED đỏ trong công ty? Cài Plugin. Tuy nhiên, quyền lực đi kèm với đau khổ. Việc tự bảo trì một cái máy chủ Jenkins là ác mộng của dân DevOps. Ổ cứng sẽ thường xuyên bị đầy vì rác từ các lần Test cũ, máy chủ hay bị sập ngang, và những cái Plugin hay "chọi" nhau gây lỗi. Dù cũ kĩ và nặng nề, Jenkins vẫn là tượng đài vững chắc ở các Ngân hàng và Tập đoàn lớn – những nơi có quy định bảo mật khắt khe không cho phép đẩy Code ra ngoài Internet (Lên Cloud).

</details>

> **Summary**: Before the rise of Cloud-Native CI/CD platforms (like GitHub Actions or GitLab CI), **Jenkins** was the undisputed king of software automation. Written in Java, Jenkins is a self-hosted, open-source automation server. Its architecture is fundamentally different from modern SaaS CI/CD; you must provision your own infrastructure, install the Jenkins Master node, and manually configure Worker nodes. Its defining strength—and its greatest weakness—is its massive ecosystem of over 1,800 Plugins. Because you own the underlying compute, Jenkins is infinitely customizable and can orchestrate incredibly complex, legacy build environments that modern SaaS tools cannot handle. However, this immense flexibility incurs a massive Day-2 operational penalty. Jenkins is notorious for configuration drift, dependency hell (Plugin conflicts), fragile Groovy scripting (`Jenkinsfile`), and persistent disk exhaustion. Despite this, it remains deeply entrenched in large enterprises, highly regulated industries (FinTech, Defense), and On-Premise environments that mandate absolute air-gapped security.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn muốn có một cỗ máy tự động giặt quần áo.
1. **GitHub Actions (Tiệm giặt ủi)**: Bạn đem quần áo bẩn ra Tiệm giặt ủi. Tiệm tự có máy móc, xà phòng xịn. Bạn ném quần áo vào, 1 tiếng sau quay lại lấy quần áo sạch. Bạn không cần dọn dẹp máy giặt. Rất rảnh rỗi.
2. **Jenkins (Mua máy giặt về nhà tự sửa)**: Bạn mua một cái Máy giặt khổng lồ về nhà. Bạn phải tự mua xà phòng, tự nối ống nước, tự lau chùi cặn bẩn mỗi ngày. Lâu lâu máy giặt hư, bạn phải tự lấy cờ-lê ra sửa. Bù lại, vì là máy của bạn, bạn có thể độ chế nó thành cái máy vừa giặt đồ, vừa nướng bánh mì, vừa nấu cơm. Rất đa năng nhưng cực kì mệt mỏi.

</details>

Imagine you need an Automated Car Wash.
1. **GitHub Actions (The Commercial Car Wash)**: You drive your car to an automated facility. You put in a token, the machine washes your car perfectly, and you drive away. You don't own the facility. You don't pay the water bill. If a brush breaks, the facility owner fixes it.
2. **Jenkins (Building Your Own Car Wash)**: You buy the pumps, the hoses, and the brushes. You build the car wash in your own backyard. You have to buy the soap, monitor the water pressure, and constantly fix the brushes when they break. However, because you built it yourself, you can install a custom robotic arm that also paints your car and changes the tires while it's being washed. Total freedom, but immense maintenance.

---

## Layer 1: Core Architecture (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Kiến trúc của Jenkins xoay quanh một mô hình Cổ điển: **Master-Slave (Chủ - Tớ)**.
1. **Jenkins Master (Bộ não)**: Đây là cái máy chủ chính chứa giao diện Web. Khi bạn truy cập trang web của Jenkins, bạn đang nói chuyện với Master. Nó làm nhiệm vụ quản lý, lập lịch, ghi log. TUYỆT ĐỐI không bao giờ dùng máy Master để chạy lệnh Build Code (Vì nó sẽ làm máy quá tải và sập toàn bộ hệ thống).
2. **Jenkins Nodes/Agents (Thợ xây)**: Bạn phải thuê 10 cái máy chủ khác (Chạy Linux, Mac, Win), và gắn chúng vào máy Master làm "Thợ". Khi Master nhận lệnh "Cần Build App iOS", nó sẽ ném việc đó sang cho thằng Thợ Mac. Khi nhận lệnh "Build Docker", nó ném sang cho thằng Thợ Linux. Thợ làm xong báo kết quả về cho Master.
3. **Jenkinsfile (Bản vẽ Groovy)**: File chứa code khai báo quy trình CI/CD. Nó dùng ngôn ngữ Groovy (Giống Java). Rất mạnh, có thể viết Vòng lặp, Câu điều kiện (If/Else), nhưng cú pháp lại cực kì rối rắm so với file YAML hiện đại.

</details>

Jenkins operates on a classic, persistent **Master-Agent Distributed Architecture**:
1. **The Jenkins Master (Controller)**: The central brain. It serves the Web UI, stores configuration, manages user authentication, schedules Jobs, and holds the plugin registry. **Crucial Rule**: You should never execute heavy compilation workloads directly on the Master node; doing so starves the JVM of memory and crashes the entire CI/CD infrastructure.
2. **The Agents (Worker Nodes)**: Dedicated machines (EC2 instances, physical servers, or K8s Pods) connected to the Master. The Master dispatches Jobs to these agents. This architecture allows for cross-platform builds: The Master can dispatch a C# compilation to a Windows Agent, an iOS build to a macOS Agent, and a Docker build to a Linux Agent simultaneously.
3. **The `Jenkinsfile` (Pipeline as Code)**: Historically, Jenkins Jobs were created by clicking through the Web GUI (ClickOps). This was disastrous for version control. Modern Jenkins uses a `Jenkinsfile` stored in the Git repository. Unlike GitHub Actions (which uses declarative YAML), a Jenkinsfile uses Groovy-based Domain Specific Language (DSL). It can be written in *Declarative* format (structured) or *Scripted* format (imperative programming with `if/else`, loops, and custom try-catch blocks), offering unparalleled but complex logic.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Nếu Github Actions xịn thế, sao người ta không bỏ hẳn Jenkins đi?
1. **Air-Gapped Security (Mạng Cách Ly Hoàn Toàn)**: Ở các hệ thống Quân đội, Ngân hàng lõi, máy chủ KHÔNG CÓ KẾT NỐI INTERNET. Bạn không thể xài Github Actions (Vì máy chủ của Microsoft không chui vào mạng nội bộ của bạn được). Bạn bắt buộc phải tự cài Jenkins vào mạng nội bộ (On-Premise) để quản lý code.
2. **Plugin Ecosystem (Mọi thứ đều có thể)**: Jenkins có hơn 1800 Plugin. Máy móc phần cứng cũ kĩ từ năm 2005? Jenkins có Plugin hỗ trợ. Muốn kết nối với một phần mềm nội bộ không ai biết tên? Dùng Jenkins gọi Script Bash. Sự tùy biến của Jenkins là vô cực.
3. **Di sản (Legacy)**: Hàng ngàn công ty lớn đã viết hàng triệu dòng code cấu hình chạy mượt mà trên Jenkins từ 10 năm trước. Đập bỏ toàn bộ để chuyển sang công nghệ mới là một rủi ro quá lớn.

</details>

If modern SaaS CI/CD platforms are superior in ease-of-use, why does Jenkins fiercely maintain its market share in enterprise environments?
1. **Absolute Infrastructure Sovereignty (Air-Gapped Environments)**: Defense contractors, Intelligence agencies, and Core Banking systems operate in "Air-Gapped" networks—environments physically and logically severed from the public Internet. GitHub Actions or GitLab SaaS physically cannot reach their source code or target servers. Jenkins is downloaded as a raw `.war` file and runs entirely On-Premise, providing 100% control over data sovereignty and network perimeters.
2. **Unmatched Ecosystem & Edge-Case Flexibility**: Jenkins has been the standard for 15 years. It possesses over 1,800 plugins. If you need to integrate a legacy IBM Mainframe test suite, flash firmware onto custom IoT hardware via serial ports, or execute an obscure 20-year-old C++ compiler, Jenkins can do it. Hosted runners on modern SaaS platforms are heavily locked down and generic. Jenkins agents are your own machines; you can connect custom hardware or specialized GPUs directly to them.
3. **The Sunk Cost of Legacy Pipelines**: Massive enterprises have millions of lines of custom Groovy scripts encoding decades of complex business logic, compliance checks, and deployment rituals. Migrating this Byzantine logic to a rigid YAML structure is often a multi-year, multi-million-dollar refactoring effort that brings zero immediate business value.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh Nỗi đau Bảo trì (Day-2 Operations).
</details>

Visualizing Operational Overhead (SaaS vs Jenkins).

| Metric | SaaS CI/CD (GitHub Actions) | Self-Hosted Jenkins |
|---|---|---|
| **Server Maintenance** | None. Microsoft patches the OS, handles security, and replaces broken hard drives. | DevOps team must monitor Jenkins Server CPU, RAM, and Disk Space 24/7. Must manually upgrade Linux OS and Java JVM. |
| **Workspace Cleanliness**| Every build gets a brand-new VM. Artifacts from old builds are guaranteed deleted. 100% reproducible. | Jenkins reuses the same Agent machine for thousands of builds. If a developer forgets to `clean` the directory, old build files corrupt the new build. "Works sometimes" syndrome. |
| **Plugin Upgrades** | Features are updated transparently by GitHub. | Upgrading the "Git Plugin" accidentally breaks the "Docker Plugin". The entire company is blocked from deploying until DevOps fixes the dependency conflict. (Plugin Hell). |

---

## Layer 4: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sử dụng Jenkins Configuration as Code (JCasC)**: Sai lầm kinh điển là dùng chuột cấu hình Jenkins (Tạo User, cài Plugin). Lúc máy chủ sập cài lại từ đầu sẽ khóc ròng. Hãy dùng JCasC: Định nghĩa toàn bộ cấu hình máy chủ Jenkins vào 1 file YAML. Nếu máy chủ cháy, tạo máy mới, nạp file YAML đó vào, máy chủ tự hồi sinh 100% như cũ.
2. **Dùng Container cho các Agent (Jenkins trên Kubernetes)**: Đừng cài Agent lên các máy chủ Linux tĩnh, vì ổ cứng sẽ rất nhanh đầy rác. Hãy nối Jenkins với Kubernetes. Khi có người Push Code, Jenkins sẽ đẻ ra một cái Pod (Docker) nhỏ trên K8s. Pod đó chạy Test xong, tự động tự sát và xóa sạch toàn bộ rác (Ephemeral Agents). Giải quyết triệt để bệnh "Đầy ổ cứng" của Jenkins.

</details>

1. **Adopt Jenkins Configuration as Code (JCasC)**: Historically, configuring Jenkins required clicking through hundreds of UI pages to set up credentials, plugins, and global variables. This made Jenkins servers un-auditable "snowflakes". If the server died, the configuration was lost. **Rule**: You MUST use the JCasC plugin. It allows you to define the entire Jenkins Master configuration (Authentication, Plugins, Slave Nodes, Credentials) in a single declarative YAML file stored in Git. You treat the Jenkins Master itself as an immutable, reproducible artifact.
2. **Use Ephemeral Agents (Kubernetes Plugin)**: The traditional Jenkins setup uses static Virtual Machines as worker nodes. These VMs accumulate garbage files, old Docker images, and zombie processes, leading to intermittent build failures and "Disk Space Full" alerts. **Rule**: Never use static workers. Integrate Jenkins with a Kubernetes cluster. When a Pipeline triggers, Jenkins dynamically spins up a Pod containing the exact required build tools. The Pipeline executes inside the Pod. When it finishes, the Pod is violently destroyed, ensuring absolute environment cleanliness.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hội chứng "Bị kẹt Plugin" (Plugin Dependency Hell)**: Bạn cài quá nhiều Plugin. Một ngày nọ có lỗ hổng bảo mật, bạn nhấn nút Cập nhật Plugin A. Plugin A yêu cầu nâng cấp Plugin B. B lại xung đột với Plugin C. Kết quả là toàn bộ màn hình Jenkins trắng xóa, công ty tê liệt không thể Deploy code.
   - *Cách giải*: Cài càng ít Plugin càng tốt. Những lệnh cơ bản hãy viết bằng Shell Script (`sh 'docker build'`) thay vì cài Plugin Docker. Script thì vĩnh viễn không bao giờ lỗi tương thích.
2. **Để Code chạy trên Node Master**: Mặc định, nếu bạn không quy định rõ, Jenkins sẽ lấy cái máy chủ Gốc (Master) ra để tự chạy Test và Build. Việc này ngốn sạch RAM và CPU, khiến giao diện Web của Jenkins bị đơ cứng, không ai truy cập được. *Luật: Số `executors` trên Node Master LUÔN LUÔN phải đặt bằng 0.*

</details>

1. **Plugin Dependency Hell & The "Frankenstein" Server**: Jenkins administrators often install a new GUI plugin for every minor task (e.g., a "Slack Notification Plugin", an "AWS CLI Plugin"). Plugins depend on specific versions of Jenkins Core and other plugins. Upgrading one plugin often triggers a cascading dependency conflict that completely breaks the server. **Rule**: Treat Plugins as a liability. Minimize plugin usage drastically. Instead of using an "AWS Plugin", use the generic `sh` (Shell) command inside your Jenkinsfile to execute raw `aws cli` bash commands. Bash scripts are immune to Jenkins plugin upgrade conflicts.
2. **Executing Builds on the Built-In Node (Master)**: By default, Jenkins allows workloads to run on the Master node (the "Built-In Node"). When a developer triggers a heavy Java Maven build, it consumes 100% of the Master's CPU and Memory. The Jenkins Web UI instantly freezes, and all other jobs in the queue timeout. **Rule**: The Number of Executors on the Master Node must strictly be set to `0`. The Master must only be used for orchestration and UI serving. All actual workloads must be exclusively delegated to remote Agents.

---

## Related Topics

- For a modern, cloud-native, maintenance-free alternative, migrate to **[GitHub Actions](./github-actions.md)**.
- For deploying infrastructure generated by Jenkins, see **[Terraform](../cloud-infra/terraform.md)**.
- Jenkins Agents are best provisioned dynamically using **[Kubernetes](../cloud-infra/kubernetes.md)**.
