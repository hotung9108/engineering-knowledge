# Git Advanced: Rebase, Cherry-Pick, Bisect

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu `add`, `commit`, `pull`, `push` là kỹ năng sinh tồn cơ bản, thì **Rebase, Cherry-Pick, Bisect** là những kỹ thuật "ma thuật" dùng để viết lại hoặc điều tra lịch sử. Trong các hệ thống cũ, lịch sử là bất biến. Nhưng trong Git, bạn có quyền làm phép bóp méo thời gian: Tua ngược quá khứ, cắt dán một tính năng từ tương lai về hiện tại, hay dùng thuật toán chia để trị (Bisect) để tìm ra chính xác ông lập trình viên nào đã đẻ ra lỗi (Bug) ở dòng code nào trong kho tàng hàng triệu dòng code.

</details>

> **Summary**: Mastering the foundational Git commands (`add`, `commit`, `push`) allows an engineer to survive. Mastering advanced Git commands allows an engineer to manipulate the space-time continuum of a repository. **Rebase** rewrites architectural history to maintain pristine linear graphs. **Cherry-Pick** executes surgical extraction of isolated commits across branches. **Bisect** deploys a binary search algorithm to forensically pinpoint the exact historical commit that injected a critical production regression. These tools distinguish Junior developers from Senior orchestrators.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng Git là một cuốn Nhật ký Cỗ máy thời gian.
1. **Rebase (Chép lại nhật ký)**: Bạn và Nam cùng viết chung 1 cuốn nhật ký, mỗi người viết 1 trang lộn xộn. Trông rất gớm. Rebase giống như xé quyển nhật ký ra, xếp tất cả các trang của Nam lên đầu, xếp tất cả các trang của bạn xuống dưới. Cuốn nhật ký trở nên thẳng tắp, dễ đọc.
2. **Cherry-Pick (Cắt dán)**: Cả team đang làm tính năng lớn (Nhánh A), nhưng trong đó có 1 dòng code sửa lỗi cực hay. Bạn không thể gộp nguyên Nhánh A vào (vì nó chưa xong). Bạn dùng kéo cắt đúng cái trang sửa lỗi đó (Cherry-pick) dán sang nhánh của bạn.
3. **Bisect (Tìm thủ phạm)**: Hôm nay phần mềm bị lỗi. Bạn biết cách đây 100 ngày nó chạy rất tốt. Thay vì test bằng tay 100 ngày, Bisect cắt đôi thời gian ra, nhảy về ngày 50. Nếu lỗi, nó nhảy về ngày 25. Chỉ mất 7 lần nhảy là tóm được ông nào viết đoạn code gây lỗi đó.

</details>

Imagine Git as a literal Time Machine Journal.
1. **Rebase (Rewriting History)**: You and Bob are writing chapters in a book simultaneously. If you `merge`, the table of contents becomes a tangled web of overlapping timelines. `Rebase` pauses time, takes all of your new chapters, and secretly tapes them exactly *after* Bob's chapters. The resulting book looks like it was written strictly sequentially by one person.
2. **Cherry-Pick (Surgical Extraction)**: A massive unreleased branch contains 50 commits. You realize Commit #42 happens to fix a critical emergency bug currently crashing Production. You cannot merge the entire branch. You use `cherry-pick` to surgically clone only Commit #42 and teleport it into the Production branch.
3. **Bisect (The Detective Search)**: The application is crashing today. You know it worked perfectly 1,000 commits ago. Instead of manually testing 1,000 versions, `Bisect` uses a Binary Search. It tests commit #500. Then #250. Then #125. In exactly 10 automated steps, it definitively identifies the exact commit (and the engineer) that injected the bug.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. `git rebase`**: Thay đổi điểm bắt đầu (Base) của nhánh. Nó bốc toàn bộ các Commit của nhánh bạn, di chuyển điểm gốc lên đỉnh mới nhất của nhánh `main`, sau đó dán từng Commit của bạn đè lên trên. Kết quả: Lịch sử Git thẳng tắp thành 1 đường (Linear History), không bị rẽ nhánh chằng chịt.
**2. `git cherry-pick <commit-hash>`**: Sao chép một Commit bất kỳ (dựa vào mã Hash) từ nhánh khác và dán nó vào nhánh hiện tại.
**3. `git bisect`**: Công cụ tìm lỗi đệ quy. Bạn khai báo Điểm Đầu (Good) và Điểm Cuối (Bad). Git tự động Checkout (nhảy) vào các Commit nằm giữa theo thuật toán Tìm kiếm Nhị phân (Binary Search). Bạn chỉ việc gõ `git bisect good` hoặc `bad` để phản hồi, nó sẽ tìm ra thủ phạm cực nhanh.

</details>

**1. `git rebase`**: A destructive rewriting of commit history. It structurally unplugs your entire Feature Branch from its original branching point, fast-forwards the origin point to the absolute bleeding-edge tip of the `main` branch, and mathematically recalculates and replays your commits linearly on top. The result is a perfect Linear History Graph, entirely devoid of chaotic `Merge Commits`.
**2. `git cherry-pick <commit_sha>`**: A utility for arbitrary commit transplantation. It inspects a specific commit on an isolated branch, calculates the explicit diff (Delta), and applies that exact Delta as a brand-new commit on your current HEAD.
**3. `git bisect`**: An automated forensic debugging utility. By feeding it a known "Good" commit and a known "Bad" commit, it executes an automated Binary Search through the Git history tree, automatically checking out the midpoint commit for you to test until the exact regression introduction point is isolated.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao Rebase thay vì Merge?**
Nếu công ty có 100 Dev. Mỗi người tạo 1 nhánh, rồi dùng `git merge` để gộp vào `main`. Mỗi lần gộp, Git lại đẻ ra 1 cục "Merge Commit" vô nghĩa. Nhìn vào biểu đồ Lịch sử (Git Graph), nó trông giống như một mớ rễ cây rối nùi đen ngòm, không ai hiểu được luồng đi của Code.
Các công ty siêu lớn bắt buộc mọi người dùng `Rebase`. Biểu đồ Git sẽ luôn là một đường thẳng duy nhất, đẹp đẽ và cực kỳ dễ điều tra lỗi.

**Tại sao cần Bisect?**
Trang Web đang bị Lỗi Màn Hình Trắng. Tuần trước thì không bị. Tuần qua cả team push lên 500 Commits. Thay vì phải đi đọc tay lại 500 đoạn code (mất 3 ngày), thuật toán tìm kiếm nhị phân của `bisect` chia 500 ra làm 2 (còn 250), rồi 125, rồi 62... Trong vòng chưa tới 10 phút, bạn túm cổ được ông Dev vừa code ẩu.

</details>

**Why mandate Rebase over Merge (The Linear History Doctrine)?**
In a repository with 500 active contributors, utilizing standard `git merge` for every feature branch results in a catastrophic Git Graph visualization. It physically resembles a tangled bowl of spaghetti, riddled with thousands of redundant "Merge branch 'X' into 'Y'" commits. 
Elite engineering organizations (e.g., Linux Kernel maintainers) strictly mandate `git rebase`. Rebasing forces developers to resolve conflicts locally and ensures the ultimate `main` branch history reads as a flawless, straight, chronological timeline, exponentially simplifying `git blame` forensics.

**The Power of Bisect**
A severe memory leak is detected in Production on Friday. It did not exist last Friday. Between the two dates, the team merged 800 commits. Manually executing `git checkout` to hunt down the bug linearly would take an engineer 2 days of testing. `git bisect` utilizes $O(\log n)$ Binary Search. It reduces 800 commits to exactly 10 checkout steps. What took 2 days now takes 15 minutes.

---

## Layer 3: Without vs. With Comparison (Compare)

### Rebase vs Merge Visualized

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sự khác biệt về cách ghi lại lịch sử giữa Rebase và Merge.
</details>

Visualizing the structural destruction and recreation that occurs during a Rebase.

| Concept | `git merge main` | `git rebase main` |
|---|---|---|
| **Action** | Creates a brand new, explicit "Merge Commit". | Rewrites time. Obliterates your old commits and creates new ones with new Hashes. |
| **Git Graph Visualization**| Tangled. Shows exactly when branches diverged and reconnected (Train tracks). | Purely Linear. Looks as if the branches never existed. A perfectly straight line. |
| **History Integrity** | Preserves absolute historical accuracy (Non-destructive). | Distorts historical accuracy for the sake of cleanliness (Destructive). |
| **Golden Rule** | Safe to use anywhere. | **NEVER** rebase a branch that other developers are actively using. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Interactive Rebase (`rebase -i`)**: Bạn code cả ngày, lỡ tay tạo ra 10 Commits rác rưởi (`fix 1`, `fix 2`, `fix nua`). Trước khi đem nộp bài cho Senior review, bạn dùng lệnh Rebase tương tác để "Nghiền nát" (Squash) 10 commits rác đó thành 1 Commit duy nhất thật xịn xò.
- **Sửa sai với Cherry-Pick**: Lính mới lỡ tay Commit nhầm tính năng A vào nhánh `main` (Thay vì nhánh `feature`). Dev Senior sẽ khôi phục nhánh `main` lại, nhảy sang nhánh `feature` và dùng lệnh `cherry-pick` để "gắp" chính xác đoạn code đó bỏ vào đúng chỗ.
- **Dùng lệnh Rebase thay cho Pull**: Thay vì gõ `git pull` (nó tự sinh ra cục Merge), các Dev có kinh nghiệm luôn gõ `git pull --rebase`. Nó giữ lịch sử cục bộ của họ cực kỳ sạch sẽ.

</details>

- **Interactive Rebasing (`git rebase -i HEAD~5`)**: The ultimate cleanup tool. A developer works for 3 days and creates 15 chaotic, typo-fixing commits (`wip`, `fix typo`, `oops`). Before submitting a Pull Request, they execute an Interactive Rebase to heavily scrub their local history. They **Squash** (crush) the 15 garbage commits into 1 single, beautifully articulated commit.
- **Cherry-Picking Hotfixes**: A team is developing a massive v2.0 release on a long-lived branch. During development, they patch a critical security flaw. That exact patch is urgently needed right now on the v1.0 Production branch. They cannot merge v2.0 into v1.0. They execute `git cherry-pick <hash>` to surgically copy only the security patch across the isolated branches.
- **The Pull Rebase (`git pull --rebase`)**: The standard `git pull` operation physically executes a `git fetch` followed by a `git merge`. If you and a coworker committed simultaneously, it generates a noisy "Merge branch" commit on your local machine. Executing `git pull --rebase` prevents this by fetching their code and gracefully layering your local commits on top.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Luật vàng của Rebase (Tuyệt đối tuân thủ)**: **ĐỪNG BAO GIỜ REBASE MỘT NHÁNH MÀ NGƯỜI KHÁC ĐANG DÙNG CHUNG**. Rebase thay đổi mã băm (Hash) của Commit. Nếu bạn Rebase nhánh `develop` xong rồi ép gởi lên, toàn bộ máy tính của 50 người đồng nghiệp sẽ bị lệch lịch sử. Họ không thể push hay pull được nữa và sẽ chửi bạn rất thảm. Chỉ được Rebase trên nhánh CÁ NHÂN của riêng bạn.
2. **Tự động hóa Bisect**: Git Bisect quá thông minh, nó cho phép chạy kịch bản tự động. Nếu bạn có một đoạn Script Test (`test.sh`). Bạn chỉ cần gõ `git bisect run ./test.sh`. Git sẽ tự động nhảy code, tự động chạy test, tự động báo lỗi. Sau 2 phút, nó nhổ toẹt ra thủ phạm cho bạn mà bạn không cần đụng tay vào bàn phím.

</details>

1. **The Golden Rule of Rebasing**: **DO NOT REBASE PUBLIC/SHARED BRANCHES.** Rebasing destroys existing commits and generates entirely new cryptographic SHA-1 hashes. If you rebase the shared `develop` branch and force-push it to GitHub, you will catastrophically shatter the repository synchronization for every other engineer on your team. Their local Git trees will aggressively diverge from the Server. You may *only* rebase isolated, private feature branches that exist solely on your local machine.
2. **Automated Bisecting (`git bisect run`)**: Manual bisecting is powerful, but automated bisecting is elite. If you have a Unit Test script that verifies if the application is broken (`npm run test:bug`), you can fully automate the forensic investigation. Execute `git bisect run npm run test:bug`. Git will automatically checkout commits, execute the script, read the exit code ($0 = Good, $1 = Bad), and autonomously isolate the exact offending commit in seconds while you drink coffee.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Mất hút trong Interactive Rebase (Bị kẹt ở Vim)**: Dev gõ `git rebase -i` và màn hình Vim đen xì hiện lên. Không biết cách sửa chữ `pick` thành `squash`, lỡ tay xóa vài dòng rồi lưu lại. Kết quả là mất luôn một đống code quan trọng. (Phải học cách dùng lệnh `git reflog` - Cuốn sổ Nam Tào - để cứu mạng trong trường hợp này. Reflog lưu lại mọi hành động lầm lỗi của bạn).
2. **Lạm dụng Cherry-Pick thay vì Merge**: Cherry-pick nhân bản code ra thành một mã Hash mới hoàn toàn. Nếu bạn Cherry-pick quá nhiều lần cùng một đoạn code đi khắp nơi, khi hai nhánh đó gộp (Merge) lại với nhau ở tương lai, Git sẽ bối rối vì thấy code giống nhau nhưng mã Hash khác nhau, gây ra rủi ro Conflict diện rộng. Hãy dùng nó như dao mổ, đừng dùng như dao chặt thịt.

</details>

1. **Interactive Rebase Mutilation (The Vim Trap)**: Executing `git rebase -i` launches a CLI text editor (usually Vim). A junior developer panics, accidentally deletes critical commit lines instead of changing `pick` to `squash`, saves, and effectively annihilates a week of work. **The Lifeline**: If you destroy your history via a botched Rebase, standard `git log` cannot save you. You must execute **`git reflog`**. The Reflog is a God-mode chronological diary of every HEAD movement. You can find the hash *before* your disastrous rebase and execute `git reset --hard <hash>` to resurrect your code.
2. **Cherry-Pick Sprawl**: Cherry-picking fundamentally violates the DRY (Don't Repeat Yourself) principle of version control by cloning identical diffs under new cryptographic Hashes. If you heavily cherry-pick features between Branch A and Branch B, and then attempt to officially `merge` Branch A into Branch B months later, Git's topological algorithms will become violently confused, resulting in incomprehensible Merge Conflicts.

---

## Related Topics

- For the foundational context, review **[Git Fundamentals](./git-fundamentals.md)**.
- See how Rebasing is utilized to keep branches clean in **[Git Workflows](./git-workflows.md)**.
- For a deeper understanding of how Git hashes work conceptually, see **[Encryption vs Hashing](../security/encryption-hashing.md)**.
