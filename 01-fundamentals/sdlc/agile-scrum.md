# Agile, Scrum, and Kanban

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ngày xưa, người ta làm phần mềm theo kiểu Thác nước (Waterfall) - tốn 2 năm để làm, khi ra mắt thì khách hàng không thèm dùng nữa vì lỗi thời. **Agile** ra đời để giải quyết việc này: Làm ra từng phần nhỏ xíu, giao cho khách dùng thử sau mỗi 2 tuần, nếu sai thì sửa ngay lập tức. **Scrum** và **Kanban** là 2 phương pháp nổi tiếng nhất để thực thi triết lý Agile này vào thực tế.

</details>

> **Summary**: Historically, software was engineered using the Waterfall model—a rigid, multi-year process that often resulted in obsolete products upon delivery. **Agile** is a philosophical framework designed to counter this by prioritizing iterative development, rapid delivery of small functional chunks, and relentless adaptation to customer feedback. **Scrum** and **Kanban** are the two dominant, practical methodologies utilized to execute Agile principles in engineering teams.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn được thuê vẽ một bức tranh phong cảnh siêu to.
- **Waterfall (Thác nước)**: Bạn nhốt mình trong phòng 6 tháng. Vẽ xong đem ra khoe, khách hàng bảo: "Tôi không thích màu xanh này". Bạn vứt bức tranh đi vẽ lại từ đầu. Thảm họa!
- **Agile (Linh hoạt)**: 
  - **Tuần 1**: Bạn vẽ phác thảo bằng bút chì. Khách bảo: "Thêm cái cây đi". Bạn thêm cái cây.
  - **Tuần 2**: Bạn tô màu nửa bức tranh. Khách bảo: "Đổi màu lá sang vàng mùa thu nhé". Bạn đổi ngay tắp lự.
  - **Kết quả**: Cứ mỗi tuần khách lại được xem và chỉnh sửa. Bức tranh cuối cùng hoàn hảo đúng ý khách, không phí phạm thời gian.

</details>

Imagine you are commissioned to paint a massive, complex landscape masterpiece.
- **Waterfall Methodology**: You lock yourself in a studio for 6 months based on initial requirements. You reveal the final painting. The client says, "Actually, I don't like mountains. I wanted an ocean." You have wasted 6 months. It's a disaster.
- **Agile Methodology**: 
  - **Week 1**: You draw a rough pencil sketch. The client reviews it and asks for an extra tree. You easily add it.
  - **Week 2**: You paint the background colors. The client reviews it and asks to change the season to Autumn. You adjust the palette immediately.
  - **Result**: Through rapid, iterative feedback loops, the final painting perfectly matches the client's evolving vision, mitigating catastrophic wasted effort.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Agile**: Không phải là một quy trình làm việc. Nó là một Tuyên ngôn (Manifesto) gồm 4 giá trị cốt lõi: 1) Đề cao con người hơn quy trình. 2) Đề cao phần mềm chạy được hơn tài liệu dày cộp. 3) Hợp tác với khách hàng. 4) Phản hồi với sự thay đổi (thay vì bám cứng lấy plan).
- **Scrum**: Một framework cực kỳ nghiêm ngặt dựa trên Agile. Chia thời gian thành các "Sprint" (2-4 tuần). Đội dev phải cam kết làm xong một lượng công việc trong Sprint đó. Có các buổi họp cố định (Daily, Planning, Retrospective).
- **Kanban**: Một framework cực kỳ lỏng lẻo. Chỉ dùng 1 cái bảng (To Do -> Doing -> Done). Không có Sprint, không có Deadline cứng. Mục tiêu là dòng chảy công việc không bị nghẽn.

</details>

- **Agile**: Agile is *not* a specific process or tool; it is a philosophy governed by the Agile Manifesto. It prioritizes four values: 1) Individuals and interactions over processes and tools. 2) Working software over comprehensive documentation. 3) Customer collaboration over contract negotiation. 4) Responding to change over following a rigid plan.
- **Scrum**: A highly structured, opinionated framework implementing Agile. Work is strictly time-boxed into iterations called **Sprints** (usually 2 weeks). Teams commit to a specific volume of work. It mandates specific Roles (Scrum Master, Product Owner) and Ceremonies (Daily Standup, Sprint Planning, Retrospective).
- **Kanban**: A fluid, continuous-flow framework implementing Agile. It utilizes a visual board (To Do $\rightarrow$ In Progress $\rightarrow$ Review $\rightarrow$ Done) and enforces strict **WIP Limits** (Work-In-Progress) to prevent bottlenecks. It has no time-boxed Sprints.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thế giới công nghệ thay đổi mỗi ngày. Nếu bạn dành 1 năm để viết tài liệu thiết kế (Waterfall) và 1 năm để code cái app gọi xe giống Uber, thì lúc bạn ra mắt, Grab đã chiếm hết thị trường rồi.
Agile sinh ra để rút ngắn **Time-to-Market** (Thời gian đưa sản phẩm ra thị trường). Thay vì làm 1 cái app hoàn hảo mất 2 năm, bạn làm 1 cái app chỉ có tính năng "Đặt xe" trong 2 tháng (gọi là MVP - Minimum Viable Product). Nếu khách chửi, bạn sửa trong 2 tuần tiếp theo.

</details>

The technological landscape evolves exponentially. If an engineering organization spends 12 months writing architectural documentation (Waterfall) and another 12 months programming a ride-hailing app, by the time it launches, competitors will have already captured the entire market. 
Agile exists to violently compress **Time-to-Market**. Instead of building a "perfect" application over 2 years, an Agile team deploys an **MVP (Minimum Viable Product)** containing only the core "Book a Ride" feature in 2 months. As users interact with the app, the team aggressively iterates and pivots based on raw market data, drastically reducing financial risk.

---

## Layer 3: Without vs. With Comparison (Compare)

### Scrum vs. Kanban

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Nhiều team nói "Chúng tôi làm Agile", nhưng họ lại ép Deadline điên cuồng. Hãy phân biệt rõ Scrum và Kanban.
</details>

While both fall under the Agile umbrella, their execution mechanics are radically different.

| Feature | Scrum | Kanban |
|---|---|---|
| **Cadence (Nhịp điệu)** | Fixed Time-boxes (2-week Sprints). | Continuous Flow (No Sprints). |
| **Commitment** | Once a Sprint starts, no new tasks can be added. | Tasks can be pulled in anytime if capacity allows. |
| **Key Metric** | **Velocity** (Story points burned per Sprint). | **Lead/Cycle Time** (Time from To-Do to Done). |
| **Roles** | Product Owner, Scrum Master, Developers. | No defined roles required. |
| **Best For...** | Building new Products with clear feature roadmaps. | Tech Support, DevOps, Bug fixing (Unpredictable work). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Dự án phù hợp với Scrum**: Xây dựng một tính năng mới toanh (Ví dụ: Module Thanh toán). Team cần ngồi lại Planning xem cần làm những API nào, CSDL nào, nhét vừa vặn vào 2 tuần để bàn giao.
- **Dự án phù hợp với Kanban**: Đội Support/Bảo trì Hệ thống (DevOps). Họ không thể lên plan cho 2 tuần vì "Server sập" là sự kiện ngẫu nhiên. Cứ có ticket lỗi ném vào cột `To Do`, ai rảnh sẽ kéo sang `Doing` để sửa ngay lập tức.
- **Scrumban**: 90% công ty hiện nay lai tạp cả 2. Vẫn chạy Sprint 2 tuần, nhưng lâu lâu có Bug đứt ruột rớt từ trên trời xuống, vẫn phá vỡ Sprint để nhét vào làm khẩn cấp.

</details>

- **Scrum Sweet Spot**: New Product Development. Designing and engineering a complex new architectural module (e.g., A Payment Processing Engine). The team utilizes Sprint Planning to decompose Epics into digestible User Stories, estimate effort using Story Points, and commit to delivering a functional iteration by Friday.
- **Kanban Sweet Spot**: Production Maintenance, DevOps, and Support Teams. These teams suffer from massive interrupt-driven workloads (e.g., A critical production database crash). You cannot "Sprint Plan" a random server outage. Kanban's continuous pull system allows critical tickets to immediately enter the workflow without shattering a rigid Sprint commitment.
- **The Reality (Scrumban)**: 90% of the industry operates on a hybrid "Scrumban" model. Teams attempt 2-week Sprints, but continuously violate Scrum rules by pulling in high-priority C-level interrupt tickets mid-sprint.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Daily Standup không phải buổi Báo cáo Tiến độ**: Họp buổi sáng 15 phút không phải để sếp kiểm tra xem bạn làm gì. Nó sinh ra để các dev thông báo cho nhau xem có ai đang BỊ KẸT (Blocker) không để cùng xúm vào gỡ.
2. **Ước lượng bằng Story Points, không phải Giờ (Hours)**: Đừng bao giờ nói "Task này làm mất 8 tiếng". Bởi vì dev xịn làm 2 tiếng, dev cùi làm 3 ngày. Hãy dùng Story Point (Sử dụng dãy Fibonacci 1, 2, 3, 5, 8...) để đánh giá ĐỘ KHÓ và SỰ MƠ HỒ của task.

</details>

1. **Daily Standups are NOT Status Reports**: A 15-minute daily Scrum is not a micromanagement tool for the Product Manager. Its sole architectural purpose is risk mitigation and unblocking. If Developer A is blocked by a missing API, Developer B (who builds APIs) pivots immediately to resolve the dependency.
2. **Estimate Complexity, Not Time (Story Points)**: Never estimate a Jira ticket in "Hours" (e.g., "This will take 8 hours"). A Senior Architect might finish it in 2 hours, while a Junior might take 3 days. Time is relative. Estimate using **Story Points** (Fibonacci sequence: 1, 2, 3, 5, 8). Story points abstractly measure *Complexity*, *Effort*, and *Uncertainty*. A "5-point ticket" is universally understood by the team as moderately complex, regardless of who picks it up.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Water-Scrum-Fall (Agile Giả Cầy)**: Công ty tuyên bố làm Agile. Nhưng BA bắt buộc viết xong tài liệu 100 trang mới cho Dev code. Dev code xong ném qua một bờ tường cho QA test 2 tuần. Đây là Thác nước đội lốt Scrum. (Hậu quả: Vẫn chậm chạp, nhưng lại thêm cả đống họp hành vô bổ).
2. **Sprint Carry-over liên tục**: Task tuần này làm không xong, đẩy sang tuần sau. Tuần sau không xong, đẩy tiếp. Hệ lụy là Velocity (tốc độ code) của team là giả mạo, không ai biết thực sự bao giờ dự án mới xong. Phải chém nhỏ Task ra!

</details>

1. **"Water-Scrum-Fall" (Agile Theater)**: The most catastrophic anti-pattern in the industry. The organization claims to be Agile and forces developers to attend Standups. However, Business Analysts spend 3 months writing monolithic requirements, developers code it in isolated silos, and then throw it over the wall to QA for a 1-month rigid testing phase. This provides zero Agile benefits while maximizing meeting fatigue.
2. **Chronic Sprint Carry-over**: User Stories are so massive (e.g., "Build the entire Authentication System") that they inevitably fail to finish within the 2-week Sprint. They "carry over" to the next Sprint, destroying the team's Velocity metrics and making Release predictability impossible. **Solution**: Violently slice Epics into razor-thin vertical slices (e.g., "Build the Login UI", "Build the JWT Validator").

---

## Related Topics

- Agile requires continuous code merging, which is powered by **[CI/CD Concepts](./ci-cd-concepts.md)**.
- Extreme Agile delivery relies on isolated testing methodologies like **[TDD & BDD](../software-testing/tdd-bdd.md)**.
