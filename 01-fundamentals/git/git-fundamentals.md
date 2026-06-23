# Git Fundamentals: Version Control

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ngày xưa, khi làm việc nhóm, người ta phải lưu file Word thành `BaoCao-Final.doc`, `BaoCao-Final-sua-lan-2.doc`, `BaoCao-Final-Cua-Thang-A.doc`. Nếu 2 người cùng sửa 1 dòng code, code sẽ bị ghi đè và mất vĩnh viễn. **Git** là phần mềm Quản lý Phiên bản (Version Control) đỉnh cao nhất thế giới do chính cha đẻ hệ điều hành Linux (Linus Torvalds) tạo ra. Nó giống như cỗ máy thời gian, chụp lại toàn bộ lịch sử thay đổi của từng dòng code, cho phép bạn hợp nhất code của hàng ngàn người lại với nhau mà không bao giờ bị mất mát dữ liệu.

</details>

> **Summary**: Before Version Control, collaborative software engineering was an unmitigated disaster characterized by frantic zip file emailing (`project_final_v2_real.zip`) and catastrophic code overwrites. **Git** is a Distributed Version Control System (DVCS) engineered by Linus Torvalds. It operates as a cryptographic time machine for code. It meticulously tracks every single character change across a massive codebase, isolates experimental feature development into distinct Branches, and seamlessly merges the contributions of thousands of global engineers while preventing destructive collisions.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang viết một cuốn sách cùng với 3 người bạn.
1. **Repository (Thư viện chung)**: Cuốn sách gốc được để ở Thư viện (Ví dụ: kho GitHub).
2. **Clone (Tạo bản sao)**: Bạn mượn cuốn sách đó, mang về nhà, dùng máy photocopy copy ra một bản y hệt để trên bàn học của bạn.
3. **Commit (Chụp ảnh lưu lại)**: Bạn ngồi viết thêm Chương 1. Viết xong, bạn lấy máy ảnh chụp "Tách" một cái (Lệnh Commit). Bức ảnh này lưu lại chính xác trạng thái của cuốn sách lúc đó. Nếu ngày mai bạn viết sai, bạn có thể vứt sách đi và lấy bức ảnh hôm qua ra chép lại y xì đúc.
4. **Push (Gửi lên thư viện)**: Bạn đem những phần viết mới của mình lên Thư viện, kẹp vào cuốn sách gốc để 3 người bạn kia cùng đọc được.

</details>

Imagine you and three friends are collaboratively writing a massive encyclopedia.
1. **Repository**: The master encyclopedia is securely stored in a Central Library (e.g., GitHub or GitLab).
2. **Clone**: You do not write directly on the master copy. You physically photocopy the entire encyclopedia and bring the replica back to your personal desk.
3. **Commit**: You draft a new Chapter. When you finish a logical section, you take a high-resolution Polaroid photo of the exact pages (A `Commit`). This photo acts as a permanent save point. If you accidentally spill coffee on your draft tomorrow, you simply look at the photo and restore the text perfectly.
4. **Push / Merge**: You travel back to the Library and seamlessly integrate your new Chapter into the master encyclopedia so your friends can see your progress.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Git quản lý code dựa trên 3 trạng thái (State) và 3 khu vực (Area) cốt lõi:
**3 Khu Vực**:
1. **Working Directory (Khu làm việc)**: Các file bạn đang gõ code trực tiếp trên VSCode.
2. **Staging Area (Phòng chờ)**: Lệnh `git add` sẽ đưa các file bạn muốn lưu vào phòng chờ. (Ví dụ bạn sửa 5 file, nhưng chỉ muốn lưu 2 file, thì bạn chỉ add 2 file đó vào phòng chờ).
3. **Local Repository (Kho chứa cá nhân)**: Lệnh `git commit` sẽ đóng gói các file trong phòng chờ thành 1 phiên bản chính thức (Snapshot), gắn thẻ thời gian và tên tác giả, lưu vĩnh viễn vào ổ cứng máy bạn.
*(Khu vực số 4 là Remote Repository - GitHub: Nơi bạn `git push` dữ liệu từ kho cá nhân lên mạng).*

</details>

Git's internal architecture is governed by a strict tripartite state mechanism. A file must transition through three distinct logical areas:
1. **The Working Directory**: Your local file system. This is where you physically edit code in your IDE (VSCode/IntelliJ). Changes here are untracked and volatile.
2. **The Staging Area (Index)**: A conceptual waiting room. When you execute `git add <file>`, you meticulously curate exactly which specific file modifications you intend to include in the upcoming snapshot. You can modify 10 files but only Stage 2 of them.
3. **The Local Repository (HEAD)**: The permanent cryptographic ledger. Executing `git commit` permanently permanently seals everything currently in the Staging Area into an immutable SHA-1 hashed snapshot.
*(The 4th area is the **Remote Repository** (e.g., GitHub). Executing `git push` synchronizes your Local Repository ledger to the cloud).*

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao Git lại áp đảo SVN (Subversion cũ)?**
Ngày xưa, hệ thống SVN là dạng Tập trung (Centralized). Máy chủ chứa toàn bộ lịch sử code. Nếu bạn đem Laptop lên máy bay (không có Wifi), bạn sẽ KHÔNG THỂ lưu code (Commit) được vì không nối được với máy chủ. Nếu máy chủ cháy ổ cứng, toàn bộ lịch sử công ty bay màu.
Git là hệ thống **Phân tán (Distributed)**. Khi bạn gõ `git clone`, Git tải TOÀN BỘ lịch sử 10 năm của công ty về ổ cứng máy bạn. Bạn lên máy bay vẫn Commit ầm ầm. Nếu máy chủ GitHub bị sập, chỉ cần lấy Laptop của bất kỳ một dev nào trong công ty đẩy ngược lên là khôi phục 100% kho lưu trữ.

</details>

**Why did Git mercilessly annihilate older systems like SVN (Subversion)?**
Legacy systems like SVN were strictly **Centralized**. The Master Server held the only complete copy of the version history. If an engineer boarded an airplane without Wi-Fi, they were physically barred from committing code. If the Master Server's hard drive suffered catastrophic failure, the company's entire intellectual property history was permanently erased.
Git is fundamentally a **Distributed** System. When you execute `git clone`, Git doesn't just download the latest files; it literally clones the entire 10-year version history database to your local hard drive. You can commit locally on an airplane. Crucially, if the centralized GitHub server is destroyed in a fire, the repository can be 100% perfectly restored from any single developer's local laptop.

---

## Layer 3: Without vs. With Comparison (Compare)

### Feature Branches: The Isolation Power

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sức mạnh của Nhánh (Branch) trong Git. Tính năng đỉnh cao giúp các Dev không cắn xé lẫn nhau.
</details>

The architectural supremacy of Git Branches (which are practically free and instant compared to SVN's heavy branching).

| Scenario | Without Branches (Directly editing `main`) | With Git Branches |
|---|---|---|
| **Development** | Dev A and Dev B both edit `login.js`. They constantly break each other's code. | Dev A creates `branch-login`. Dev B creates `branch-payment`. Complete isolation. |
| **Emergency Bug**| Production has a critical bug. But `main` contains Dev A's half-finished, broken login code. You cannot deploy! | You switch back to `main` (ignoring the branches), fix the bug, and deploy instantly. |
| **Code Review** | Code is merged instantly. No one checks it. Bugs go to production. | Dev A submits a **Pull Request (PR)**. Seniors review the code before merging it into `main`. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Quản lý Mã nguồn (Source Code Management)**: Dĩ nhiên, dùng để lưu trữ toàn bộ lịch sử code của Frontend, Backend, Mobile.
- **GitOps (Quản lý hạ tầng)**: Ngày nay, ngay cả việc "Thuê bao nhiêu máy chủ AWS" cũng được viết thành Code (Terraform) và đưa lên Git. Nếu ai đó lỡ tay tắt máy chủ, chỉ cần lật lại lịch sử Git (git revert) để tìm lại file cấu hình và bật máy chủ lên lại.
- **Tự động hóa (CI/CD Webhooks)**: Git không chỉ để lưu trữ. Khi bạn gõ `git push`, GitHub có thể tự động nhận biết có code mới, nó gửi một tín hiệu (Webhook) sang máy chủ Server bảo: "Ê, tải code mới về và chạy lại Web đi!".

</details>

- **Application Versioning**: The absolute baseline requirement for any software engineering team. Tracking feature additions, bug fixes, and identifying exactly *who* introduced a breaking change via `git blame`.
- **Infrastructure as Code (GitOps)**: Modern DevOps teams store their infrastructure blueprints (Terraform, Kubernetes YAMLs) strictly inside Git. The Git repository becomes the Single Source of Truth for the physical state of the datacenter. Modifying server configurations requires a Pull Request.
- **CI/CD Triggers**: Pushing a commit to the `main` branch acts as an automated tripwire. GitHub Webhooks detect the push and signal a CI/CD pipeline (e.g., GitHub Actions) to instantly compile the code, run 500 unit tests, and deploy the artifact to production.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Commit Message có ý nghĩa**: Đừng bao giờ viết commit là `git commit -m "sua code"`, `git commit -m "fix bug"`, hay `git commit -m "asdfasdf"`. Sáu tháng sau bạn đọc lại sẽ không hiểu mình đã sửa cái gì. Phải dùng quy tắc Conventional Commits: `fix(auth): sửa lỗi không lưu được token khi login` hoặc `feat(ui): thêm nút bấm thanh toán màu xanh`.
2. **File `.gitignore`**: Tuyệt đối không được gõ `git add .` khi chưa có file `.gitignore`. File này dùng để chặn Git không lưu các file rác (Ví dụ: Thư mục `node_modules` nặng 1GB, file cấu hình `.env` chứa mật khẩu Database). Mật khẩu lọt lên GitHub là coi như cúng tiền cho hacker.

</details>

1. **Semantic Commit Messages (Conventional Commits)**: A commit message reading `git commit -m "fixed stuff"` or `"wip"` is an act of engineering sabotage. Six months later, when `git bisect` identifies that specific commit as the source of a catastrophic bug, the cryptic message provides zero forensic context. Adopt rigid Conventional Commits: `feat(payment): implement Stripe integration` or `fix(auth): resolve JWT expiration bug`.
2. **Mandatory `.gitignore` Auditing**: Executing `git add .` without a robust `.gitignore` file is lethal. It guarantees you will accidentally commit the `node_modules/` black hole (bloating the repository by gigabytes) and, catastrophically, your `.env` files. Committing AWS Access Keys or Database Passwords to a public GitHub repository will result in automated bots stealing your keys and racking up a $50,000 Bitcoin-mining bill in 30 minutes.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nỗi sợ Merge Conflict (Đụng độ code)**: Khi 2 người cùng sửa chung dòng số 5 của 1 file. Git không biết lấy của ai, nó sẽ báo lỗi `Merge Conflict`. Dev mới thường hoảng loạn, sợ hãi xóa bừa và làm mất code của đồng nghiệp. (Cách xử lý: Bình tĩnh mở file lên, VSCode sẽ hiện rõ 2 màu Xanh/Đỏ để bạn tự chọn giữ dòng nào, xóa dòng nào).
2. **Sử dụng lệnh `git push --force` bừa bãi**: Lệnh này nghĩa là "Ép máy chủ phải nhận cục code của tao, xóa bỏ lịch sử của người khác đi". Nếu bạn dùng lệnh này trên nhánh `main`, bạn sẽ vĩnh viễn xóa sổ toàn bộ công sức code mấy ngày qua của cả team. TUYỆT ĐỐI không dùng lệnh này trên nhánh làm việc chung.

</details>

1. **Merge Conflict Paralysis**: When two developers simultaneously edit the exact same line of code, Git throws a `Merge Conflict` and halts the merge. Junior developers panic, assuming they broke the repository, and often clumsily overwrite their colleague's code to resolve it. **Resolution**: Remain calm. Conflicts are routine. Utilize a GUI tool (VSCode Merge Editor) to clearly visualize the Incoming vs. Current changes, manually negotiate the collision, and safely conclude the merge.
2. **The Lethal `git push --force`**: This command instructs the Remote Repository to aggressively overwrite its entire history with your Local history. If your local history is outdated, executing `git push -f origin main` will permanently incinerate days of committed work pushed by your colleagues. It is an extremely destructive command. **Rule**: Never force push to a shared branch. It is only permissible when violently rewriting history on your own, isolated personal Feature Branch.

---

## Layer 7: Cheatsheet

### Repository Initialization & Cloning
```bash
git init                    # Create a new, empty Git repository in the current folder
git clone <url>             # Download an entire repository from GitHub
git remote add origin <url> # Link your local repo to an empty GitHub repository
```

### The Core Workflow
```bash
git status                  # Check the state of your Working Directory (What changed?)
git add .                   # Stage ALL modified/new files (Move to Waiting Room)
git add file.js             # Stage only a specific file
git commit -m "feat: login" # Take the snapshot of staged files with a message
git push origin main        # Upload your snapshots to the GitHub 'main' branch
git pull origin main        # Download the latest changes from GitHub to your laptop
```

### Branching & Merging
```bash
git branch                  # List all local branches (highlighting the current one)
git checkout -b feature-a   # Create a NEW branch named 'feature-a' and switch to it
git checkout main           # Switch back to the 'main' branch
git merge feature-a         # Absorb the code from 'feature-a' into your current branch
git branch -d feature-a     # Delete the branch (after merging is done)
```

### History & Forensics
```bash
git log                     # View the detailed commit history
git log --oneline           # View a compact, 1-line-per-commit history
git diff                    # See exactly which lines of code you modified (before adding)
git blame file.js           # See exactly WHO wrote every single line in a file
```

### Undo & Recovery (Danger Zone)
```bash
git restore file.js         # Discard unsaved changes in a file (Reset to last commit)
git reset HEAD~1            # Undo your last commit (keeps the code, just un-commits it)
git reset --hard HEAD~1     # DANGEROUS: Undo last commit AND permanently delete the code changes
git stash                   # Temporarily hide your messy code so you can switch branches
git stash pop               # Bring the messy code back out of hiding
```

---

## Related Topics

- For advanced collaborative workflows, read **[Git Branching Strategies](./git-branching.md)**.
- For moving code automatically after a push, see **[CI/CD Concepts](../sdlc/ci-cd-concepts.md)**.
- See how software versions map to Git tags in **[Versioning](../sdlc/versioning.md)**.
