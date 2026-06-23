# Git Workflows: Branching Strategies

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu bạn làm dự án cá nhân, bạn có thể tống toàn bộ code vào nhánh `main` rồi đẩy lên. Nhưng khi một công ty có 50 lập trình viên cùng làm chung một dự án, việc tống hết code vào `main` sẽ tạo ra một nồi cám lợn khổng lồ không thể chạy được. **Git Workflow** (Luồng làm việc Git) là những bộ quy tắc và chiến lược phân nhánh (Branching) chuẩn mực do cộng đồng đúc kết lại (như GitFlow, GitHub Flow). Chúng quy định rõ ràng: Nhánh nào dùng để test, nhánh nào dùng để chạy thật, và làm sao để ghép code vào nhau mà không gây cháy nổ.

</details>

> **Summary**: In solitary development, committing linearly directly to the `main` branch is acceptable. However, in enterprise environments where 50 to 500 engineers concurrently modify the same monolithic repository, uncoordinated commits will inevitably result in catastrophic integration collisions and un-deployable code. **Git Workflows** (e.g., GitFlow, GitHub Flow, Trunk-Based Development) are rigorous, standardized architectural conventions dictating exactly how Branches are created, named, isolated, reviewed, and merged. They enforce a disciplined pipeline ensuring the `main` branch remains flawlessly stable and production-ready at all times.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn điều hành một xưởng lắp ráp Ô tô.
- **Dòng sông rác (Không có quy trình)**: Tất cả 50 công nhân xúm lại lắp chung một chiếc xe duy nhất. Người thì vặn ốc, người thì tháo bánh. Cuối ngày chiếc xe nổ tung vì không ai biết ai vừa lắp sai cái gì. (Giống việc cả team cùng commit thẳng vào nhánh `main`).
- **Dây chuyền chuẩn (Git Workflow)**: 
  - Chiếc xe hoàn chỉnh đang bán cho khách nằm ở Showroom (Nhánh `main`). Tuyệt đối không ai được đụng vào.
  - Khi cần lắp bộ Cửa mới, anh thợ A bê bản thiết kế vào phòng riêng lắp ráp (Nhánh `feature-cua-xe`).
  - Lắp xong, anh A gọi Tổ trưởng vào kiểm tra (Pull Request).
  - Tổ trưởng gật đầu, cánh cửa đó mới được bê ra Xưởng thử nghiệm (Nhánh `develop/staging`) chạy thử 3 ngày. Chạy tốt mới được đem ra Showroom.

</details>

Imagine operating an Automotive Assembly Plant.
- **The Chaotic Workshop (No Strategy)**: 50 mechanics surround a single car frame. Mechanic A attaches a wheel while Mechanic B simultaneously cuts the axle. At the end of the shift, the car catches fire. It is impossible to identify who broke it. (This equates to 50 engineers pushing code directly to the `main` branch).
- **The Assembly Line (Git Workflows)**:
  - The pristine, finished car currently sold to customers sits safely in the Showroom (The `main` branch). It is locked. No tools allowed.
  - Mechanic A needs to design a new Steering Wheel. They take the blueprints into a private, isolated Workshop (A `feature` branch).
  - Once built, Mechanic A summons the Chief Inspector for rigorous review (**Pull Request**).
  - If approved, the steering wheel is moved to the Testing Track (The `develop` or `staging` branch). Only after surviving extreme testing is it finally installed on the Showroom car.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Git Workflows không phải là phần mềm. Nó là **Luật do con người tự đặt ra với nhau**. Có 3 luồng làm việc phổ biến nhất thế giới:
1. **GitHub Flow**: Cực kỳ đơn giản. Chỉ có 1 nhánh gốc là `main`. Khi làm tính năng mới, tạo nhánh `feature`. Code xong, mở Pull Request (PR) xin duyệt. Duyệt xong gộp thẳng vào `main` và Deploy luôn. Thích hợp cho Web cập nhật liên tục mỗi ngày.
2. **GitFlow**: Rất phức tạp. Chia ra 5 loại nhánh: `main` (Chạy thật), `develop` (Gom code), `feature` (Tính năng), `release` (Chuẩn bị xuất xưởng), `hotfix` (Sửa lỗi khẩn cấp). Thích hợp cho làm App điện thoại (Vài tháng mới tung bản cập nhật 1 lần).
3. **Trunk-Based Development**: Luồng làm việc của các "Siêu nhân" (Google, Netflix). Không thèm dùng nhánh `feature` dài hạn. Tất cả Dev gộp code trực tiếp vào `main` nhiều lần TỰA MỖI NGÀY. Cần hệ thống Test Tự động cực kỳ khủng khiếp mới chơi được kiểu này.

</details>

Git Workflows are not enforced by the Git binary itself; they are **Social Contracts** agreed upon by engineering teams. There are 3 globally dominant paradigms:
1. **GitHub Flow (Lightweight)**: Maximizes velocity. There is only one perpetual branch: `main`. Engineers branch off into `feature`, submit a Pull Request, undergo code review, and merge directly back into `main`. It enables Continuous Deployment (pushing to production 10 times a day).
2. **GitFlow (Heavyweight)**: Highly structured and bureaucratic. It utilizes two perpetual branches (`main` and `develop`) and three ephemeral branches (`feature`, `release`, `hotfix`). It is the gold standard for versioned software (like iOS Apps or Enterprise Desktop Software) where releases happen cyclically (e.g., Version 1.2 deployed every 3 months).
3. **Trunk-Based Development (Elite)**: The paradigm utilized by hyperscalers (Google, Facebook). It aggressively discourages long-lived feature branches. Engineers merge code directly into the "Trunk" (`main`) multiple times a day. This absolutely requires elite CI/CD pipelines, massive automated test suites, and Feature Flags to prevent catastrophic deployments.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề Tích hợp (Integration Hell)**:
Nếu bạn tách ra làm nhánh `feature` riêng, nhưng bạn ôm nhánh đó tận 2 tháng mới chịu gộp (Merge) vào nhánh `main`. Trong 2 tháng đó, 10 ông dev khác đã gộp hàng đống code vào `main` rồi. Khi bạn gộp code của bạn vào, nó sẽ gây ra hàng trăm lỗi đụng độ (Merge Conflicts) khủng khiếp. Có khi sửa lỗi còn lâu hơn cả viết code mới.

**Giải pháp Workflow**:
Các chiến lược Git bắt buộc mọi người phải chia nhỏ công việc. Làm cái nào dứt điểm cái đó và gộp vào `main` càng sớm càng tốt. Nó cũng sinh ra khái niệm **Pull Request (PR)**: Trước khi code của bạn được chui vào `main`, nó phải bị chặn ở cửa để một kỹ sư cấp cao (Senior) đọc lại từ đầu đến cuối. Nếu code ngu, viết lộn xộn, Senior sẽ đá nó ra bắt viết lại.

</details>

**The "Integration Hell" Catastrophe**:
A developer isolates themselves on a `feature-payment` branch and writes code in a silo for 2 months. Meanwhile, 10 other developers continuously merge their own features into the `main` branch, fundamentally altering the architecture. After 2 months, the siloed developer attempts to merge. They are hit with 500 lethal Merge Conflicts. Resolving this "Integration Hell" often takes weeks and introduces severe regressions.

**The Workflow Solution (Discipline & Review)**:
Workflows enforce architectural discipline. They mandate short-lived branches and continuous integration. Crucially, workflows institutionalize the **Pull Request (PR)** or Merge Request (MR). Before a branch is physically allowed to merge into the protected `main` branch, the PR acts as a gated checkpoint. A Senior Engineer must manually execute a **Code Review**, auditing the code for security vulnerabilities, architectural flaws, and formatting standards. If it fails, the code is forcefully rejected.

---

## Layer 3: Without vs. With Comparison (Compare)

### GitFlow Architecture Visualization

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Cách luồng GitFlow hoạt động trong thực tế khi làm 1 App điện thoại.
</details>

Visualizing the rigorous structure of the classic GitFlow model.

| Branch Name | Purpose | Lifespan | Who merges into it? |
|---|---|---|---|
| **`main` (or `master`)** | The absolute truth. Contains ONLY code currently live in Production. | Perpetual | Only merged from `release` or `hotfix`. |
| **`develop`** | The integration hub. Contains the bleeding-edge code for the *next* update. | Perpetual | Merged from completed `feature` branches. |
| **`feature/xyz`** | Your private workspace to build a specific thing (e.g., `feature/login`). | Ephemeral (Days) | You write code here. Merges into `develop`. |
| **`release/v1.2`** | A frozen state. No new features allowed, only final bug testing before launch. | Ephemeral (Weeks)| Forked from `develop`. Merges into `main` AND `develop`. |
| **`hotfix/crash-fix`**| Emergency triage. A critical bug is found in Production (`main`). | Ephemeral (Hours) | Forked from `main`. Merges directly back into `main` AND `develop`. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Khởi nghiệp Web (Dùng GitHub Flow)**: Team Start-up web làm cực nhanh. Sáng code nút Đăng Nhập, trưa Review, chiều gộp vào `main` và Web tự động cập nhật lên mạng luôn (CI/CD). Không cần `develop`, không cần `release`. Tốc độ là ưu tiên số 1.
- **Công ty Game hoặc App Ngân hàng (Dùng GitFlow)**: App ngân hàng không thể ngày nào cũng bắt khách tải bản cập nhật mới. Họ sẽ gom 20 tính năng vào nhánh `develop`. Cuối tháng, cắt ra nhánh `release` để đội Tester đánh đập dã man suốt 2 tuần. Đảm bảo an toàn tuyệt đối 100% mới gộp vào `main` để đưa lên App Store.
- **Bảo vệ nhánh (Branch Protection)**: Trong GitHub, các công ty luôn bật tính năng "Khóa nhánh main". Nó CẤM bạn dùng lệnh `git push origin main`. Bất cứ ai muốn đưa code vào `main` đều BẮT BUỘC phải mở Pull Request và phải có ít nhất 1 người khác bấm nút "Approve" (Duyệt) thì mới được gộp.

</details>

- **High-Velocity Web Startups (GitHub Flow)**: Ideal for SaaS web platforms possessing automated CI/CD pipelines. A developer builds a UI widget on a feature branch, passes automated tests, gets PR approval, and merges to `main`. The pipeline instantly deploys it to production. They might deploy 15 times a day. Minimal bureaucracy.
- **Regulated Enterprise / Mobile Apps (GitFlow)**: Mandatory for systems demanding extreme stability (Banking, Aerospace) or client-side binaries (iOS/Android Apps). You cannot force an iPhone user to download a new App Store update 15 times a day. Features accumulate in `develop`. At month's end, a `release` branch is isolated for 2 weeks of brutal QA testing. Velocity is sacrificed for absolute stability.
- **Enforcing Branch Protection Rules**: The physical implementation of workflows. Repository administrators configure GitHub/GitLab settings to explicitly lock the `main` and `develop` branches. Direct `git push` commands are violently rejected by the server. The *only* mechanical way to alter the branch is via an approved Pull Request.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Rebase trước khi tạo Pull Request**: Trước khi xin gộp code, bạn phải tải code mới nhất của `main` về, và gộp (Merge/Rebase) vào nhánh của bạn để tự kiểm tra xem có bị lỗi đụng độ (Conflict) hay không. Đừng bao giờ quăng một cái Pull Request chứa đầy Conflict lên bắt Senior phải sửa dùm. Đó là hành động cực kỳ nghiệp dư.
2. **Review Code có Tâm**: Khi review code cho đồng nghiệp, đừng chỉ lướt lướt rồi bấm "Approve". Nếu hệ thống bị sập do dòng code đó, người duyệt bài cũng phải chịu trách nhiệm. Hãy đọc kỹ, bắt bẻ cách đặt tên biến, tìm rủi ro bảo mật, và yêu cầu họ sửa (Request Changes) nếu cần.

</details>

1. **The Pre-PR Rebase/Merge Obligation**: Before opening a Pull Request, it is your strict professional duty to synchronize your feature branch with the latest `main` branch (via `git fetch origin` followed by `git rebase origin/main` or `git merge origin/main`). You must physically resolve all Merge Conflicts on your own machine. Submitting a Pull Request that says "This branch has conflicts that must be resolved" is highly unprofessional and disrespects the Reviewer's time.
2. **Rigorous Code Review Hygiene**: Code Review is not a bureaucratic rubber stamp. It is the primary defense against production outages. When reviewing, actively hunt for: Security vulnerabilities (SQL Injection vectors), performance bottlenecks (N+1 queries), missing Unit Tests, and violations of the company's architectural style guide. Do not hesitate to hit "Request Changes". You share liability for the code once you approve it.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lạm dụng GitFlow cho Web**: Team Web làm dự án nhỏ xíu nhưng bày đặt học đòi GitFlow phức tạp. Họ tạo đủ loại nhánh `develop`, `release`, `hotfix`. Kết quả: Mất nửa ngày chỉ để ngồi gộp qua gộp lại giữa các nhánh. Hãy giữ mọi thứ đơn giản nhất có thể (KISS - Keep It Simple, Stupid).
2. **Nhánh Feature Khổng lồ (Monster Branches)**: Dev A tạo nhánh tính năng, viết 50 file, thêm 10.000 dòng code rồi mới mở Pull Request. Không một Senior nào trên đời có đủ kiên nhẫn và sức lực để Review một đống code khổng lồ như vậy. Họ sẽ nhắm mắt bấm Approve đại cho xong (LGTM - Looks Good To Me). Lỗi sẽ lọt ra ngoài. LUÔN CHIA NHỎ nhánh ra, mỗi PR chỉ nên sửa tối đa 300-500 dòng code.

</details>

1. **Over-Engineering with GitFlow**: A 3-person web development agency blindly adopts GitFlow because they read it was an "Enterprise Standard." They spend 20% of their working hours manually choreographing complex merges between `develop` and `release` for a simple WordPress site. **Rule**: Always default to the simplest architecture (GitHub Flow). Only adopt GitFlow if you physically experience pain points involving versioned releases.
2. **The "Monster" Pull Request**: A developer isolates for 3 weeks and submits a single PR encompassing 45 changed files and +12,000 lines of code. This fundamentally breaks the Code Review process. A human brain cannot audit 12,000 lines of code for logic bugs. Reviewers experience "Review Fatigue" and will blindly approve it just to clear their queue, virtually guaranteeing bugs will hit production. **Rule**: PRs must be atomic. Keep PRs under 400 lines of changes. Break massive features into sequentially chained smaller PRs.

---

## Related Topics

- For the literal CLI commands used to execute these strategies, review **[Git Fundamentals](./git-fundamentals.md)**.
- For what happens immediately *after* the Pull Request is merged into `main`, see **[CI/CD Concepts](../sdlc/ci-cd-concepts.md)**.
- See how software versions (like `v1.2.0`) relate to Git in **[Versioning](../sdlc/versioning.md)**.
