# GitHub Actions

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước năm 2019, nếu công ty bạn lưu Code ở Github, bạn phải thuê một máy chủ Jenkins bên ngoài để làm CI/CD. Việc nối Github với máy chủ đó rất lằng nhằng (phải cài Webhooks, mở Tường lửa). **GitHub Actions** ra đời và thay đổi hoàn toàn cuộc chơi. Vì Github hiểu rằng "Kho Code chính là nơi kích hoạt mọi thứ", họ nhúng luôn máy chủ CI/CD trực tiếp vào kho Code của bạn. Bạn không cần thuê máy chủ nào cả. Microsoft (chủ của Github) sẽ cho bạn mượn máy tính của họ (Runner) miễn phí. Bạn chỉ việc ném 1 file cấu hình `.yaml` cực kì dễ hiểu vào thư mục `.github/workflows`. Cứ mỗi lần bạn đẩy (Push) code lên mạng, máy chủ của Microsoft lập tức bừng tỉnh, nhận code của bạn, chạy Test, xây dựng Docker và ném thẳng lên AWS giúp bạn. Khi làm xong, máy chủ đó tự hủy. Gọn nhẹ, miễn phí và vô cùng mạnh mẽ.

</details>

> **Summary**: Prior to GitHub Actions (released in 2019), the CI/CD ecosystem was heavily disjointed. You hosted your code on GitHub, but your pipelines ran on a third-party service (CircleCI, TravisCI) or a self-hosted Jenkins server. This required complex webhook integrations and external secret management. **GitHub Actions** consolidated the ecosystem by bringing the CI/CD compute directly into the Source Control repository. It is a fully managed, Cloud-Native CI/CD platform. You define your pipelines declaratively in YAML files stored in the `.github/workflows` directory. Upon triggering an event (like a `push` or a `pull_request`), GitHub automatically provisions an ephemeral Virtual Machine (a "Runner" hosted by Microsoft on Azure), executes your steps, and instantly destroys the VM. It abstracts away all infrastructure management, making it the undisputed standard for modern software delivery.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (Lập trình viên) là một Đầu bếp nướng bánh.
1. **Cách cũ (Dùng Jenkins)**: Bạn nhào bột (viết code) xong, bạn phải tự mang cục bột đó chạy sang một cái Lò nướng ở tòa nhà bên cạnh (Máy chủ Jenkins) để nướng. Lò nướng đó bạn phải tự mua, tự cắm điện, tự lau chùi mỗi ngày.
2. **GitHub Actions**: Bạn đang đứng trong căn Bếp của mình (Kho Github). Bạn nhào bột xong. Bạn chỉ cần viết một tờ giấy chú thích: *"Nướng ở 200 độ C trong 10 phút"*. Lập tức từ trên trần nhà rớt xuống một cái Lò nướng tự động siêu xịn (Máy chủ của Microsoft). Nó tự chộp lấy cục bột của bạn, nướng chín, mang giao cho khách, rồi... cái lò nướng tự bốc hơi biến mất. Bạn không tốn tiền mua lò, không cần chùi rửa, chỉ cần viết giấy chú thích (File YAML).

</details>

Imagine being a Chef.
1. **Traditional CI/CD (Jenkins)**: You prep your ingredients (write code). To cook them, you must purchase a massive Oven (Jenkins Server), place it in a separate room, pay the electricity bill, and scrub it clean every single night to make sure old food doesn't contaminate the new food.
2. **GitHub Actions**: You prep your ingredients in the kitchen (GitHub Repo). You stick a post-it note on the bowl saying: *"Bake at 400 degrees for 10 minutes"*. Instantly, a magical oven materializes out of thin air (The Ephemeral Runner). It reads the note, bakes the cake perfectly, and then the oven immediately disintegrates into dust. You never maintain the oven, and every single cake gets its own brand-new, sterile oven.

---

## Layer 1: Core Concepts (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cấu trúc của GitHub Actions được thiết kế theo dạng Búp bê Nga (Cái này bọc cái kia), gồm 4 tầng:
1. **Workflow (Bản kế hoạch)**: Là file YAML của bạn. Nó định nghĩa "Khi nào thì chạy?" (Ví dụ: Chạy khi có ai đó đẩy code lên nhánh `main`).
2. **Job (Nhiệm vụ lớn)**: Trong 1 Workflow có thể có nhiều Job. Ví dụ: Job 1 là "Test Code", Job 2 là "Đóng gói Docker". Các Job này mặc định chạy Cùng Một Lúc (Song song) trên nhiều máy chủ khác nhau để tiết kiệm thời gian.
3. **Step (Bước nhỏ)**: Mỗi Job chứa nhiều Step chạy tuần tự từ trên xuống dưới. (Ví dụ: Bước 1 tải code về, Bước 2 chạy lệnh `npm install`, Bước 3 chạy lệnh `npm test`).
4. **Action (Hành động đóng gói)**: Thường các Step là lệnh gõ bàn phím bình thường. Nhưng có những hành động quá phức tạp (Ví dụ: Cài đặt AWS CLI để kết nối Cloud). Bạn không cần tự gõ. Bạn chỉ cần gọi một **Action** (Do người khác viết sẵn trên Chợ ứng dụng). Giống như tải thư viện về xài.

</details>

GitHub Actions operates on a strict, hierarchical ontology:
1. **Workflow**: The highest-level concept. It is an automated process defined by a YAML file. It strictly defines the `on:` block (the Event Trigger, e.g., `push` to `main`, a schedule, or a manual button press).
2. **Job**: A workflow contains one or more Jobs. **Crucially, Jobs run in parallel by default.** Each Job is allocated its own entirely separate Virtual Machine (Runner). If you have a `test-ui` Job and a `test-backend` Job, GitHub spins up two servers concurrently. You can force sequential execution using `needs: [job_name]`.
3. **Step**: A Job contains a sequence of Steps. Steps run sequentially on the *same* Runner, meaning they share the same hard drive and environment variables. A Step can either be a raw shell command (e.g., `run: npm run build`) or it can execute an *Action*.
4. **Action**: The killer feature of the platform. Actions are reusable, open-source modular components hosted on the GitHub Marketplace. Instead of writing a 50-line bash script to authenticate with AWS, you simply invoke the official `aws-actions/configure-aws-credentials` Action. It heavily accelerates pipeline development.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Sự tồn tại của Github Actions đã gần như giết chết các công ty làm CI/CD khác (như TravisCI, CircleCI). Lý do:
1. **Bảo mật tuyệt đối**: Trước đây, bạn phải đưa cái Mật khẩu Database (Secret) của bạn cho một bên thứ 3 là TravisCI. Cảm giác rất bất an. Giờ đây, Code của bạn nằm ở Github, bạn lưu Mật khẩu thẳng vào Github Secrets. Quá trình Test và Deploy diễn ra khép kín hoàn toàn bên trong nội bộ nhà Github. Mật khẩu không bao giờ bay ra ngoài Internet.
2. **Chợ ứng dụng (Marketplace) khổng lồ**: Bạn muốn gửi tin nhắn lên Slack khi deploy thành công? Có sẵn Action. Bạn muốn đẩy code lên Máy chủ Google? Có sẵn Action. Việc viết CI/CD giờ đây giống như trò chơi ghép hình Lego, 90% công việc phức tạp đã có người viết sẵn cho bạn xài miễn phí.
3. **Bảo trì = 0**: Máy chủ do Microsoft quản lý. Nó dùng xong là vứt (Ephemeral). Bạn không bao giờ sợ lỗi "Hôm qua rác từ lần chạy trước làm đầy ổ cứng khiến hôm nay chạy lỗi" (Lỗi cực kì kinh điển của Jenkins).

</details>

GitHub Actions aggressively captured the market due to its architectural proximity to Source Control and its Extensibility.
1. **Security and Secret Proximity**: In third-party CI systems, you had to duplicate your sensitive API Keys and Cloud Credentials across multiple platforms. With Actions, your secrets reside directly in GitHub Secrets. The ephemeral runner fetches the source code and the secrets inside the same secure perimeter. It drastically reduces the attack surface.
2. **The Open-Source Marketplace**: Jenkins relied on cumbersome Java plugins that often broke. GitHub Actions leverages the Open-Source community. The GitHub Marketplace contains over 15,000 modular Actions written in JavaScript or Docker. If a new technology is released, an Action for it appears on the Marketplace the next day. It transforms pipeline engineering from "writing bash scripts" to "composing declarative blocks".
3. **Zero-Maintenance Ephemeral Runners**: Maintaining persistent Jenkins workers means dealing with "Configuration Drift" (e.g., leftover files from a previous build causing the next build to succeed falsely). GitHub's Hosted Runners are Ephemeral. Every single Job starts with a brand-new, surgically clean Virtual Machine. When the Job finishes, the VM is violently destroyed. This guarantees absolute reproducibility.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình Review Code (Duyệt code) của Lập trình viên mới.
</details>

Visualizing Code Review & Safety (Quality Assurance).

| Metric | Traditional Workflow | GitHub Actions Workflow |
|---|---|---|
| **Pull Request (PR)** | Junior Dev opens a PR. The Senior Dev must manually pull the code to their own laptop, install libraries, and run tests to see if it's broken. Takes 30 minutes. | Junior Dev opens a PR. GitHub Actions instantly intercepts it. The Senior Dev sees a "Green Checkmark" on the PR proving 1,000 tests passed. Senior Dev approves immediately. |
| **Enforcing Rules** | "Please remember to run the Code Formatter before pushing." (Humans forget). | Branch Protection Rules enabled: The "Merge" button is permanently locked and disabled until GitHub Actions reports that the Linter and Formatter steps passed. Impossible to forget. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Continuous Integration (CI thuần túy)**: Ứng dụng phổ biến nhất. Khóa nút Merge (Gộp code) lại. Bắt buộc MỌI CÚ PUSH phải chạy qua Github Actions. Nếu Test xanh mới được gộp. Đảm bảo nhánh `main` không bao giờ chứa code rác.
2. **Build Docker Image & Push**: Khi có một bản phát hành mới (Tạo Tag `v1.0.0`). Trigger Github Actions tự động chạy lệnh `docker build`, dán nhãn `v1.0.0` và đẩy cái Thùng Docker đó lên AWS ECR hoặc Docker Hub.
3. **Triển khai Web Frontend (Vercel/S3)**: Mỗi khi code được gộp vào nhánh `main`. Github Actions tự động chạy `npm run build` để lấy thư mục HTML/CSS. Sau đó nó gọi API để nén và quăng thư mục đó lên máy chủ Amazon S3 hoặc tự đồng bộ với Vercel.
4. **Tự động hóa Công việc (Cron Jobs)**: Github Actions không chỉ làm CI/CD. Bạn có thể cài nó chạy mỗi 12h đêm: "Tự động gọi API lấy thời tiết ngày mai và đăng lên Kênh chat Slack của công ty". Không cần phải mua máy chủ để treo tool.

</details>

1. **Strict Quality Gates (CI)**: Integrating Actions with GitHub Branch Protection rules. You enforce that no human can bypass the CI pipeline. The pipeline must successfully execute unit tests, SonarQube static code analysis, and dependency vulnerability scans before the "Merge Pull Request" button turns green.
2. **Automated Docker Image Pipelines (CD Prep)**: The transition between CI and CD. Triggered by a Git Tag (e.g., `v1.2.0`). The workflow checks out the code, authenticates securely with a Container Registry (AWS ECR / GitHub GHCR), builds the Docker Image, tags it with the Git SHA, and pushes it.
3. **Serverless & Static Deployments**: Perfect for SPAs (React/Vue) or Serverless frameworks. The workflow runs `npm run build`, then utilizes an Action (like `aws-actions/configure-aws-credentials`) to sync the compiled `/dist` directory directly to an AWS S3 Bucket and invalidate the CloudFront CDN cache.
4. **Scheduled Automations (Cron Jobs)**: GitHub Actions acts as a free, highly reliable Cron Server. You can define `on: schedule: - cron: '0 0 * * *'`. The runner spins up at midnight, executes a Python script to scrape a website or clean up a database, and shuts down.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sử dụng Caching (Lưu đệm) để tăng tốc**: Mặc định, mỗi lần chạy CI, máy chủ của Github phải tải lại 1GB thư viện `node_modules` từ đầu. Việc này làm CI chạy mất 10 phút, lập trình viên chửi thề vì phải chờ đợi. BẮT BUỘC phải dùng Action `actions/setup-node` với cấu hình `cache: 'npm'`. Nó sẽ lưu đệm thư mục tải về. Lần sau chạy CI chỉ mất 1 phút.
2. **Sử dụng OIDC (OpenID Connect) thay cho Mật khẩu AWS**: Cách cũ là lưu `AWS_ACCESS_KEY` vào Github Secrets. Cách này nguy hiểm vì lỡ nhân viên nghỉ việc mang Key đi, hoặc quên đổi Key. Hiện nay, AWS và Github hỗ trợ OIDC. Github sẽ tự động nói chuyện với AWS, "Mày thấy em đang chạy trên Github không? Cấp cho em cái quyền tạm thời 5 phút để up file nhé". AWS cấp quyền tạm, chạy xong vứt bỏ. KHÔNG CÓ MẬT KHẨU NÀO ĐƯỢC LƯU TRỮ CỐ ĐỊNH NỮA. Tuyệt đối an toàn.

</details>

1. **Mandatory Dependency Caching**: Because Hosted Runners are ephemeral and start with a blank hard drive, running `npm ci` or `mvn install` downloads gigabytes of dependencies from the internet on every single commit. This spikes CI times to 15+ minutes. **Rule**: You MUST utilize caching Actions. For Node.js, use `actions/setup-node` with `cache: 'npm'`. GitHub will seamlessly zip the `.npm` folder, store it on their internal network, and inject it into the next runner instantly, dropping build times from 10 minutes to 30 seconds.
2. **OIDC (OpenID Connect) Cloud Authentication**: The modern, cryptographically secure way to deploy to AWS/GCP. Historically, you generated long-lived IAM Access Keys and pasted them into GitHub Secrets. This introduces massive credential rotation and exfiltration risks. **Rule**: Implement OIDC. You configure AWS to intrinsically trust your specific GitHub Repository. The GitHub Runner requests a short-lived JSON Web Token (JWT) from GitHub, presents it to AWS, and AWS issues temporary (1-hour) STS credentials. There are ZERO hardcoded secrets stored anywhere.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lạm dụng máy chủ miễn phí của Github**: Microsoft cho bạn xài khoảng 2000 phút/tháng miễn phí. Nếu công ty bạn làm dự án bự (Build 1 app iOS mất 1 tiếng, hoặc chạy Test Database mất 30 phút), bạn sẽ "đốt" sạch phút miễn phí trong 3 ngày và hệ thống CI bị khóa cứng (Phải trả tiền rất đắt). 
   - *Cách giải*: Nếu công việc quá nặng, hãy thuê 1 cái máy EC2 rẻ bèo trên AWS, và cài phần mềm `Self-hosted Runner` của Github lên đó. Cấu hình để Github đẩy việc về cái máy ảo của bạn chạy. Vẫn dùng chung file YAML, nhưng không tốn phút miễn phí của Github nữa.
2. **Không cố định Phiên bản của Action**: Khi bạn gọi thư viện `uses: actions/checkout@v3`, bạn hi vọng nó chạy ổn định. Nhưng nếu bạn gọi `uses: actions/checkout@master`, ngày mai tác giả cập nhật code rác vào thư viện đó, TOÀN BỘ hệ thống Deploy của công ty bạn sẽ sụp đổ dây chuyền mà bạn không hiểu tại sao. Hãy luôn khóa cứng phiên bản Action.

</details>

1. **Exhausting Free Tier Minutes (Heavy Workloads)**: GitHub provides a generous free tier of compute minutes. However, macOS runners consume minutes at a 10x multiplier. If your team is compiling a massive C++ monolith or a heavy iOS App 50 times a day, you will exhaust your billing quota immediately. **Fix**: For heavy computational workloads (or workloads requiring direct access to your private internal VPN), deploy **Self-Hosted Runners**. You provision an EC2 instance in your own AWS VPC, install the GitHub Runner agent, and configure your YAML to run on `runs-on: self-hosted`. You only pay AWS for the EC2 cost.
2. **Action Version Pinning (Supply Chain Attacks)**: You invoke a third-party action in your YAML using `uses: some-guy/deploy-to-aws@main`. You are trusting that the `main` branch of that repository is secure. Tomorrow, a hacker compromises `some-guy`'s account, injects crypto-mining malware into the `main` branch, and your CI pipeline automatically executes the malware with full production AWS credentials. **Rule**: NEVER bind an Action to a mutable branch (`@main` or `@v2`). Always explicitly pin the Action to an immutable Git SHA Hash (e.g., `uses: actions/checkout@a1b2c3d4e5f6...`).

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Bản mẫu một File CI/CD kinh điển cho Node.js (Lưu tại `.github/workflows/main.yml`)
</details>

### The Golden CI/CD Pipeline (Node.js API)
Place this file exactly at `.github/workflows/ci.yml`.

```yaml
name: Node.js CI/CD Pipeline

# 1. THE TRIGGER: When does this run?
on:
  push:
    branches: [ "main" ] # Run when merging to main
  pull_request:
    branches: [ "main" ] # Run when PR is opened against main

# 2. THE JOBS
jobs:
  # --- JOB 1: TEST THE CODE ---
  test:
    runs-on: ubuntu-latest # Request a free Linux VM
    steps:
    - name: Get the code
      uses: actions/checkout@v4

    - name: Setup Node.js + Caching
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm' # MAGIC: Drastically speeds up npm install

    - name: Install Dependencies
      run: npm ci # Strict install from package-lock.json

    - name: Run Linter
      run: npm run lint

    - name: Run Unit Tests
      run: npm test

  # --- JOB 2: DEPLOY (Only runs if 'test' succeeds) ---
  deploy:
    needs: test # CRITICAL: Wait for tests to pass!
    if: github.ref == 'refs/heads/main' # Only deploy if pushed to main, not on PRs
    runs-on: ubuntu-latest
    
    # Required permissions for secure OIDC authentication (No passwords)
    permissions:
      id-token: write 
      contents: read 

    steps:
    - name: Get the code
      uses: actions/checkout@v4

    - name: Configure AWS Credentials securely
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789012:role/my-github-actions-role
        aws-region: us-east-1

    - name: Deploy to AWS S3 / EC2
      run: |
        echo "Deploying the artifact using AWS CLI..."
        # aws s3 sync ./build s3://my-bucket/
```

---

## Related Topics

- GitHub Actions builds **[Docker](../cloud-infra/docker.md)** images to deploy.
- If you have an advanced, massive Kubernetes setup, GitHub Actions is often paired with **[ArgoCD](./argo-cd.md)** (GitOps) for deployment instead of pushing directly.
- The older, self-hosted alternative to GitHub Actions is **[Jenkins](./jenkins.md)**.
