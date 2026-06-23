# CI/CD: Continuous Integration & Continuous Deployment

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ngày xưa, để đưa code lên Server chạy thật (Deploy), dev phải copy file bằng tay qua FTP, tự gõ lệnh khởi động lại server vào lúc 2 giờ sáng, rất dễ gõ sai lệnh làm sập mạng. **CI/CD** là các con Robot (Pipeline) được lập trình sẵn. Cứ mỗi khi bạn push code lên Github, Robot sẽ tự động tải code về, tự động chạy Test kiểm tra lỗi (CI), và tự động ném code đó lên Server chạy luôn mà không cần con người nhúng tay vào (CD).

</details>

> **Summary**: Historically, deploying software to production was a terrifying, manual process involving moving binaries via FTP and executing bash scripts at 2:00 AM, heavily prone to human error. **CI/CD (Continuous Integration / Continuous Deployment)** completely automates this lifecycle. It acts as an automated robotic pipeline: the moment a developer pushes code to version control, the pipeline intercepts it, automatically compiles it, executes automated test suites (CI), and perfectly provisions and deploys it to the production server (CD) with zero human intervention.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang lắp ráp một chiếc điện thoại trong nhà máy.
- **Không có CI/CD (Làm thủ công)**: Bạn hì hục lắp ráp bằng tay. Lắp xong, bạn vứt nó vào một cái hộp, lấy xe máy chở ra cửa hàng. Đi đường bị xóc hỏng mẹ cái màn hình, đến cửa hàng bật không lên.
- **Có CI/CD (Dây chuyền tự động)**:
  - **CI (Băng chuyền kiểm tra)**: Ngay khi bạn vừa lắp xong 1 cái nút bấm, băng chuyền tự động đưa nó qua máy quét tia X để xem có bị nứt không. Nứt là vứt luôn, không cho lắp tiếp.
  - **CD (Băng chuyền giao hàng)**: Lắp xong xuôi, máy móc tự đóng gói hoàn hảo, ném lên máy bay Drone tự động bay thẳng đến cửa hàng trong 5 phút.

</details>

Imagine you are manufacturing smartphones in a factory.
- **Without CI/CD (Manual Artisanal Labor)**: You build the phone completely by hand. You put it in a cardboard box, strap it to a bicycle, and pedal it to the retail store. It hits a pothole, the screen shatters, and it arrives broken.
- **With CI/CD (The Automated Assembly Line)**:
  - **CI (The QA Scanner)**: The millisecond you attach a new button to the motherboard, a robotic arm grabs it and runs it through an X-Ray machine (Automated Tests). If it detects a flaw, it immediately halts the conveyor belt and flashes a red siren.
  - **CD (The Drone Delivery)**: Once the phone passes all X-Rays, automated robotic arms perfectly shrink-wrap it, load it onto an autonomous drone, and fly it directly into the customer's hands within 5 minutes.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. CI (Continuous Integration - Tích hợp liên tục)**: 
Là quá trình tự động hóa việc gộp code của nhiều dev vào chung một nhánh (như nhánh `main` trên Git). Mục tiêu lớn nhất của CI là CHẠY TEST. Cứ push code lên là Robot (như GitHub Actions, Jenkins) tự động build và chạy Unit Test. Nếu Test báo Đỏ, code của bạn bị chặn không cho gộp.
**2. CD (Continuous Delivery / Deployment - Phân phối / Triển khai liên tục)**:
- **Continuous Delivery**: Code vượt qua CI sẽ được tự động đóng gói (VD: tạo ra file `.jar` hoặc Docker Image) và vứt vào một cái kho. Nó chờ một Nút Bấm bằng tay của sếp để đẩy lên Server.
- **Continuous Deployment**: Xịn hơn Delivery. Không cần sếp bấm nút. Qua CI là tự động bắn thẳng lên Server cho khách dùng luôn.

</details>

**1. CI (Continuous Integration)**: 
The practice of aggressively merging all developer working copies to a shared mainline (e.g., the `main` branch on Git) multiple times a day. Its primary architectural objective is **Automated Validation**. When code is pushed, an external server (e.g., GitHub Actions, Jenkins, GitLab CI) intercepts the webhook, compiles the code, and brutally executes the entire Unit/Integration Test suite. If a single test fails, the pipeline aborts, and the merge is blocked.

**2. CD (Continuous Delivery vs. Continuous Deployment)**:
- **Continuous Delivery**: Extends CI. Code that passes tests is automatically packaged (e.g., compiled into a `.jar` or built into a Docker Image) and securely staged in an artifact registry. It is 100% ready to go to production, but mandates a *manual human intervention* (A Manager clicking a "Deploy" button).
- **Continuous Deployment**: The holy grail. Extends Delivery. There is no human intervention. If the code passes the automated CI tests, the pipeline automatically provisions infrastructure and deploys the code directly to live production end-users.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề "Code chạy trên máy tôi, nhưng chết trên Server"**:
Một team có 5 Dev. Cuối tháng, 5 người gộp code lại với nhau (Merge Hell - Địa ngục gộp code). Code đá nhau chan chát. Khi đẩy lên Server, Server lại xài hệ điều hành Linux trong khi Dev xài Windows $\rightarrow$ App sập rớt đài.

**Giải pháp CI/CD**:
CI/CD tạo ra một **Môi trường vô trùng chuẩn mực**. Code vừa viết xong hôm nay, phải được gộp và test ngay hôm nay. Robot CI/CD chạy môi trường y hệt Server. Nếu nó build thành công, bạn có thể tự tin 99.9% là lên Server cũng sẽ chạy mượt mà. Đội Dev thoát khỏi cảnh thức đêm trực Server.

</details>

**The "It works on my machine!" Fallacy**:
Historically, a team of 5 developers would work in isolated Git branches for a month. On "Release Day", they attempted to merge 50,000 lines of code simultaneously (Integration Hell). The resulting merge conflicts took weeks to resolve. Furthermore, developers coded on Windows laptops, but the server ran Ubuntu Linux. Missing environment variables or differing Node.js versions caused the production server to instantly crash upon deployment.

**The CI/CD Antidote**:
CI/CD enforces a **Standardized, Sterile Execution Environment**. Code is integrated daily (reducing merge conflicts to tiny, manageable chunks). The Pipeline compiles the code on an ephemeral, immutable Linux container perfectly mirroring production. If the Pipeline successfully builds and tests the artifact, you have mathematically eliminated the "It works on my machine" discrepancy.

---

## Layer 3: Without vs. With Comparison (Compare)

### The Deployment Lifecycle

| Phase | Manual Deployment (Legacy) | CI/CD Pipeline (Modern) |
|---|---|---|
| **Integration** | Merging 1 month of code. Massive conflicts. | Merging daily. Trivial conflicts. |
| **Testing** | QA Team spends 3 days clicking around manually. | CI Server executes 5,000 tests in 2 minutes. |
| **Packaging** | Developer builds the app locally, zips it, emails it. | CI Server securely builds a Docker image and pushes to ECR. |
| **Deployment** | SSH into server at 3 AM. Run bash scripts manually. | CD Server orchestrates Kubernetes rolling update automatically. |
| **Rollback (If bug)**| Panic. Try to find the old zip file. Server down for hours. | Click one button. Pipeline redeploys previous image in 10 seconds. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **GitHub Actions**: Nhanh, xịn, tích hợp sẵn vào GitHub. Phù hợp cho 90% dự án hiện nay, từ cá nhân đến công ty lớn.
- **GitLab CI/CD**: Rất nổi tiếng ở các công ty enterprise vì khả năng tự host (cài đặt trên server riêng) để bảo mật mã nguồn.
- **Jenkins**: Ông cụ già của làng CI/CD. Giao diện xấu, cấu hình bằng file Groovy phức tạp, nhưng cực kỳ quyền năng và có hàng ngàn Plugin để kết nối với các hệ thống đồ cổ.

</details>

- **GitHub Actions**: The modern default. Extremely deeply integrated into the GitHub ecosystem. Configured purely via YAML. Ideal for 90% of modern cloud-native projects (Node, Go, Python, Docker).
- **GitLab CI/CD**: Highly favored in Enterprise and heavily regulated environments (Finance, Healthcare) because the entire GitLab suite can be air-gapped and self-hosted on private company servers, ensuring absolute source-code privacy.
- **Jenkins**: The Grandfather of CI/CD. Visually archaic and notoriously difficult to maintain (requires managing complex Groovy `Jenkinsfile` scripts and maintaining the master/worker server architecture). However, it possesses infinite extensibility via thousands of plugins, making it the only choice for complex legacy monoliths.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Pipeline phải CHẠY NHANH**: Nếu chạy CI tốn mất 30 phút, dev sẽ chán nản, đi uống cà phê và mất tập trung. CI hoàn hảo phải chạy xong dưới 5 phút. Hãy dùng Cache (Lưu lại thư mục `node_modules` hoặc `.m2`) để không phải tải lại thư viện mạng mỗi lần build.
2. **Build một lần, Deploy mọi nơi (Build Once, Run Anywhere)**: Đừng bao giờ cấu hình CI build ra 3 file riêng cho Dev, Staging, và Production. Hãy build ra đúng 1 cục Docker Image duy nhất. Cục Image đó chạy qua môi trường nào thì chỉ cần tiêm Biến Môi Trường (Environment Variables) của môi trường đó vào.

</details>

1. **Relentlessly Optimize Pipeline Velocity**: A developer's attention span is short. If a CI pipeline takes 45 minutes to execute tests, context switching occurs, and velocity plummets. A healthy CI pipeline executes in under 5-10 minutes. Achieve this by aggressively caching dependency layers (e.g., caching `node_modules` or Maven `~/.m2` directories) and running Unit Tests in massively parallel matrices.
2. **Immutable Artifacts (Build Once, Run Anywhere)**: Never compile the application dynamically on the target server. Never configure the CI pipeline to build three different binaries for `Dev`, `Staging`, and `Production`. Compile the code into an immutable **Docker Image** exactly *once* during the CI phase. Promote that exact same physical image hash through the pipeline, simply injecting different Environment Variables (`.env`) for database connections at runtime via CD.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cố làm Continuous Deployment khi chưa có Unit Test tốt**: Triển khai liên tục (tự động đẩy thẳng lên Server) là một con dao hai lưỡi. Nếu hệ thống Test của bạn lỏng lẻo (chưa làm TDD đàng hoàng), bạn vừa tự động hóa việc "Bắn Bug trực tiếp vào mặt khách hàng" với tốc độ ánh sáng!
2. **Lộ Mật khẩu trong file CI/CD**: Rất nhiều người gõ thẳng mật khẩu Database hoặc AWS Secret Key vào file `pipeline.yaml` rồi push lên Git. Hacker dùng bot quét được sẽ đào Bitcoin cháy túi bạn. Bắt buộc phải dùng hệ thống quản lý Secret (GitHub Secrets, AWS Secrets Manager, HashiCorp Vault).

</details>

1. **Pursuing Continuous Deployment without TDD**: Continuous Deployment (zero human intervention) is architectural suicide if your underlying Test Suite is weak. If you lack comprehensive Unit and E2E tests, you haven't automated software delivery; you have simply automated the process of detonating critical bugs in Production at the speed of light.
2. **Hardcoding Secrets in Pipeline YAML**: A catastrophic security vulnerability. Developers lazily hardcoding AWS IAM Keys or Database Passwords directly into `.github/workflows/deploy.yml` and pushing it to Version Control. Bots constantly scrape GitHub for these exposed keys to spin up illegal crypto-mining instances. Always utilize hardened secret managers (e.g., GitHub Actions Secrets, HashiCorp Vault).

---

## Related Topics

- CI/CD requires mastering version control. See **[Git Fundamentals](../git/git-fundamentals.md)**.
- CI/CD relies on isolated test execution. See **[The Testing Pyramid](../software-testing/testing-pyramid.md)**.
- Packaging apps perfectly for CD usually means using **[Virtualization & Containers](../cloud-computing/virtualization-containers.md)**.
