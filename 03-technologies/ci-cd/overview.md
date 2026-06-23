# CI/CD (Continuous Integration / Continuous Deployment) Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước đây, chu trình ra mắt phần mềm (Release) là một nghi lễ đẫm máu. Lập trình viên code cả tháng trời, dồn lại thành một cục to đùng. Đến đêm thứ 6, đội Vận hành (Ops) thức trắng đêm để copy đống code đó lên Máy chủ. Thường thì code sẽ sập, và hai bên đổ lỗi cho nhau. **CI/CD** ra đời để tiêu diệt sự đau khổ này bằng **Tự động hóa**. 
> - **CI (Tích hợp liên tục)**: Cứ mỗi khi Lập trình viên gõ xong 1 dòng code và bấm "Lưu", một con Robot sẽ lập tức nhảy ra kiểm tra lỗi chính tả, chạy Test tự động. Nếu sai, nó gạch đỏ bắt sửa ngay lập tức, không cho phép gộp chung với code của người khác.
> - **CD (Triển khai liên tục)**: Nếu code đã xanh (không lỗi), con Robot tiếp tục tự động đóng gói code đó thành Docker, rồi tự động ném thẳng lên Máy chủ cho khách hàng dùng luôn. 
> Nhờ CI/CD, các công ty lớn như Amazon có thể cập nhật phần mềm 10.000 lần một ngày mà không sợ sập hệ thống.

</details>

> **Summary**: In the pre-Agile era, software deployment was a highly stressful, manual, and infrequent event. Developers would accumulate thousands of lines of code over months (the "Integration Hell"), and operations teams would manually FTP these massive monoliths to production servers during late-night maintenance windows, often resulting in catastrophic outages. **CI/CD (Continuous Integration and Continuous Deployment)** eliminated this friction by automating the entire software lifecycle. 
> - **CI (Continuous Integration)** forces developers to merge code changes frequently. A CI server automatically intercepts every commit, compiles the code, and runs a battery of automated tests to catch regressions instantly.
> - **CD (Continuous Deployment/Delivery)** takes the validated artifact from the CI pipeline, automatically containerizes it, and safely deploys it to staging or production environments without human intervention. CI/CD transforms software delivery from a terrifying monthly ritual into a boring, reliable, daily background process.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một xưởng sản xuất Ô tô.
1. **Làm bằng tay (Không có CI/CD)**: 10 người thợ tự nặn ra 10 cái bánh xe, cửa kính, động cơ theo ý mình. Đến cuối tháng, họ gom lại ráp thành 1 cái xe. Lúc ráp mới phát hiện: Cửa quá to không lắp vừa thân xe, động cơ lắp vào bị nổ. Xe hỏng, cãi nhau to.
2. **Dây chuyền Tự động (Có CI/CD)**: Xưởng lắp một Dây chuyền Robot. 
   - **CI (Robot Kiểm tra)**: Anh thợ vừa làm xong cái bánh xe, đặt lên băng chuyền. Robot lập tức đo đạc, bóp nắn xem bánh xe có tròn không. Nếu méo (Lỗi code), Robot hú còi vứt cái bánh xe đó đi, bắt anh thợ làm lại ngay lập tức.
   - **CD (Robot Lắp ráp)**: Khi bánh xe đã tròn trịa, Robot tự động chuyển nó tới xưởng lắp ráp, tự vặn ốc, tự sơn màu, và tự động lái chiếc xe đó ra Showroom bán cho khách luôn. Con người chỉ việc tập trung làm bánh xe, phần còn lại Robot lo hết.

</details>

Imagine a Car Manufacturing Plant.
1. **The Old Way (Manual Integration)**: 50 mechanics build car parts in completely separate rooms for a month. On the 30th day, they bring all the parts into the main hall and try to bolt them together. They discover the steering wheel doesn't fit the dashboard, and the engine explodes when connected to the battery. Chaos ensues.
2. **The CI/CD Way (The Automated Assembly Line)**: 
   - **CI (The Quality Inspector)**: A mechanic finishes a tiny gear and drops it on a conveyor belt. Instantly, an Automated Inspector (CI) picks it up, tests its strength, and checks if it fits the engine. If it fails, the belt stops, a red light flashes, and the gear is rejected immediately.
   - **CD (The Delivery Truck)**: If the gear passes all tests, the belt automatically bolts it into the car, paints the car, loads it onto a delivery truck, and drops it off at the customer's driveway while they are sleeping. The mechanic never leaves their workbench.

---

## Layer 1: The Pipeline Anatomy (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Một "Đường ống" (Pipeline) CI/CD tiêu chuẩn thường có 5 bước (Stages) chạy nối tiếp nhau:
1. **Source (Bắt đầu)**: Lập trình viên đẩy code lên Github (Tạo Pull Request). Lập tức kích hoạt đường ống.
2. **Build (Biên dịch)**: Pipeline tải code về, chạy lệnh biên dịch (Ví dụ: `npm run build` hoặc build Java ra file `.jar`).
3. **Test (Kiểm thử)**: Quan trọng nhất. Chạy Unit Test (Kiểm tra từng hàm nhỏ) và E2E Test (Giả lập người dùng bấm web). Nếu 1 test rớt $\rightarrow$ Ngắt toàn bộ đường ống, báo lỗi cho Lập trình viên.
4. **Package (Đóng gói)**: Nếu Test xanh, Pipeline gói file code vào Docker Image và đẩy lên kho lưu trữ (Docker Hub / AWS ECR).
5. **Deploy (Triển khai)**: Pipeline kết nối vào Máy chủ (Kubernetes hoặc AWS EC2), tải cái Docker Image mới nhất về và chạy nó lên cho khách hàng dùng.

</details>

A standard CI/CD Pipeline is a finite state machine consisting of sequential stages. If any stage fails, the entire pipeline aborts immediately:
1. **Source (Trigger)**: The pipeline monitors a Source Control repository (GitHub, GitLab). An event, such as a developer pushing a commit or opening a Pull Request, triggers the pipeline execution.
2. **Build**: The CI server spins up an ephemeral runner, clones the source code, installs dependencies (e.g., `npm install`, `mvn clean install`), and compiles the source code into executable binaries.
3. **Test (The Gatekeeper)**: The most critical stage. The pipeline executes the automated test suites (Unit Tests, Integration Tests, Linting, Security Scans). If code coverage drops or a single test fails, the pipeline crashes and blocks the code from being merged.
4. **Package / Release**: If tests pass, the pipeline packages the compiled application. In modern stacks, this means executing `docker build`, creating an immutable Docker Image, and pushing it to a Container Registry (e.g., AWS ECR).
5. **Deploy**: The CD mechanism takes over. It connects to the target environment (Staging or Production) and executes the infrastructure commands (e.g., `kubectl apply` or Terraform triggers) to roll out the new Docker container to live users.

---

## Layer 2: Continuous Delivery vs Deployment (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Chữ **D** trong CI/CD có 2 nghĩa khác nhau, tùy vào sự "Liều lĩnh" của công ty:
1. **Continuous Delivery (Giao hàng liên tục - An toàn)**: Code chạy xong khâu Test, đóng gói xong xuôi. Nhưng nó KHÔNG tự cập nhật lên máy chủ. Nó nằm chờ ở đó. Một ông Giám đốc (hoặc QA) phải bấm bằng tay một nút màu xanh chữ "Phê duyệt" (Approve) thì code mới được lên Production. Phù hợp cho Ngân hàng, Y tế (Sợ lỗi).
2. **Continuous Deployment (Triển khai liên tục - Liều lĩnh)**: Tự động hóa 100%. Lập trình viên bấm nút "Lưu code", tự động Test, tự động Build, tự động Ném thẳng lên Production cho khách hàng xài trong vòng 5 phút mà KHÔNG có ai kiểm duyệt. Rất nguy hiểm nếu code Test viết hời hợt, nhưng mang lại tốc độ nâng cấp tính năng cực nhanh (Netflix, Facebook hay dùng).

</details>

A critical semantic distinction exists within the acronym "CD":
1. **Continuous Delivery (Human-in-the-Loop)**: The pipeline automates the Build, Test, and Packaging phases. The final artifact is technically perfectly ready to be deployed to Production. However, the actual deployment requires a manual human action (clicking an "Approve" button by a Release Manager or QA lead). This is standard for highly regulated industries (FinTech, Healthcare) where compliance requires manual sign-offs.
2. **Continuous Deployment (Fully Autonomous)**: The holy grail of DevOps. There is absolutely no human intervention. If a developer's commit passes all automated unit, integration, and security tests, it is automatically pushed to the live Production environment. This requires an incredibly mature, paranoid automated testing culture. If your tests are weak, you will continuously deploy catastrophic bugs to your users.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình "Chữa cháy" khi ứng dụng bị sập do lỗi Code.
</details>

Visualizing Incident Response (Manual vs CI/CD).

| Metric | Manual Deployment (FTP / SSH) | CI/CD Pipeline |
|---|---|---|
| **Deploying the Fix** | Developer writes fix. Asks SysAdmin to deploy. SysAdmin is eating lunch. Takes 2 hours to manually upload files via FTP and restart Apache. | Developer pushes the fix to `main` branch. GitHub Actions automatically builds and deploys it in exactly 3 minutes. |
| **Rolling Back (Undo)**| SysAdmin didn't backup the old code. Must frantically try to remember what lines they changed to undo it. Site is down for hours. | The CD tool (like ArgoCD) keeps a history. Click "Rollback to Previous Version". The system instantly reverts to the stable Docker image in 5 seconds. |

---

## Layer 4: Common Architectures & Roles

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thế giới CI/CD được chia làm 3 thế hệ công cụ:
1. **Thế hệ 1: Jenkins (Con Khủng Long)**: Ra đời từ rất lâu. Bạn phải tự thuê 1 máy chủ, cài Jenkins lên đó. Phải tự bảo trì máy chủ này (rất hay sập). Viết file cấu hình bằng ngôn ngữ Groovy rất xấu và khó hiểu. Nhưng vì nó miễn phí và mạnh mẽ nên các ngân hàng cũ vẫn dùng.
2. **Thế hệ 2: Cloud CI/CD (GitHub Actions, GitLab CI)**: Không cần tự nuôi máy chủ nữa. Microsoft và GitLab cho bạn xài ké máy chủ của họ. Bạn chỉ cần viết 1 file YAML đơn giản bỏ vào kho Code. Mỗi lần Push code, máy chủ của họ tự chạy test cho bạn. Gọn, nhẹ, là tiêu chuẩn của các Startup hiện nay.
3. **Thế hệ 3: GitOps (ArgoCD)**: Cấp độ cao nhất dành riêng cho Kubernetes. Thay vì dùng Github Actions để "Đẩy" (Push) code vào máy chủ. Máy chủ (ArgoCD) sẽ tự động "Kéo" (Pull) code từ Github về. Đảm bảo máy chủ và Github luôn luôn đồng bộ y hệt nhau 100%.

</details>

The CI/CD tooling landscape is highly fragmented, categorized by deployment paradigms and architectural eras:
1. **The Self-Hosted Behemoth (Jenkins)**: The grandfather of CI/CD. It is highly customizable via thousands of plugins, but it requires dedicated DevOps engineers to maintain the Jenkins Master server, patch security vulnerabilities, and manage worker nodes. Pipelines are written in imperative Groovy scripts.
2. **The Cloud-Native SaaS (GitHub Actions / GitLab CI)**: The modern standard. You do not manage the build servers. The CI engine is tightly integrated directly into your Source Code Repository. Pipelines are defined declaratively in simple YAML files. When an event occurs, GitHub spins up an ephemeral runner, executes the pipeline, and kills the runner. Extremely low maintenance.
3. **The GitOps Paradigm (ArgoCD / Flux)**: A specialized CD pattern designed explicitly for Kubernetes. In traditional CD (Push), GitHub Actions connects to the K8s cluster and executes `kubectl apply`. In GitOps (Pull), a software agent (ArgoCD) lives *inside* the K8s cluster. It continuously monitors the GitHub repository. If the Git repo says "I want 5 Pods", but the Cluster currently has 3 Pods, ArgoCD detects the configuration drift and automatically pulls the changes to synchronize the cluster to exactly match the Git repository. Git becomes the absolute single source of truth for infrastructure.

---

## Related Topics

- The modern standard for Cloud CI/CD is **[GitHub Actions](./github-actions.md)**.
- For managing massive, legacy enterprise pipelines, see **[Jenkins](./jenkins.md)**.
- For deploying to Kubernetes using the advanced GitOps pattern, explore **[ArgoCD](./argo-cd.md)**.
- CI/CD pipelines heavily rely on packaging apps into **[Docker](../cloud-infra/docker.md)** images.
