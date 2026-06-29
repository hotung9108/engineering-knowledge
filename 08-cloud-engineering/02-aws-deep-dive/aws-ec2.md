# AWS EC2 (Elastic Compute Cloud)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trái tim tính toán của AWS. Tìm hiểu về Máy chủ Ảo (Virtual Machines), cách chọn các dòng máy (Instance Types), ổ cứng (EBS), và cách hệ thống tự động co giãn (Auto Scaling Groups) để xử lý lượng truy cập khổng lồ.

</details>

> **Summary**: The computational heart of AWS. Learn about Virtual Machines, how to select Instance Types, attached storage (EBS), and how to use Auto Scaling Groups to handle massive traffic spikes seamlessly.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn cần một cái máy tính để chạy phần mềm (ví dụ: chạy Website), nhưng bạn không muốn ra cửa hàng mua máy tính vật lý.
- **EC2 (Máy chủ ảo)**: AWS cho bạn thuê một cái máy tính qua mạng. Bạn chọn nó có bao nhiêu RAM, mấy cái CPU, dùng Windows hay Linux. Cứ chạy 1 giờ thì trả tiền 1 giờ.
- **AMI (Bản sao đĩa cứng)**: Giống như cái đĩa cài Win hồi xưa. Bạn cài Win, cài phần mềm, rồi "chụp" nó lại thành AMI. Sau này muốn tạo 10 máy y hệt, chỉ cần dùng AMI đó đúc ra 10 bản.
- **Auto Scaling**: Tưởng tượng cửa hàng của bạn bình thường có 1 thu ngân (1 EC2). Ngày lễ đông khách, hệ thống tự động "gọi" thêm 9 thu ngân nữa (scale out). Hết khách, nó tự cho 9 người kia nghỉ việc (scale in) để đỡ tốn tiền lương.

</details>

You need a computer to run your software (e.g., host a website), but you don't want to buy a physical desktop.
- **EC2 (Virtual Server)**: AWS rents you a computer over the internet. You choose how much RAM, how many CPUs, and whether it runs Windows or Linux. You pay by the hour.
- **AMI (Amazon Machine Image)**: Like a mold or a blueprint. You install your OS, install your software, and "take a snapshot". Later, if you want 10 identical servers, you use that AMI blueprint to clone them instantly.
- **Auto Scaling**: Imagine your store usually has 1 cashier (1 EC2). On Black Friday, the system automatically summons 9 more cashiers (scale out). When the rush is over, it fires those 9 cashiers (scale in) so you stop paying their hourly wage.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon EC2 (Elastic Compute Cloud)** là một dịch vụ web cung cấp năng lực máy tính (Compute) có kích thước linh hoạt trên đám mây. Nó là dịch vụ IaaS (Infrastructure as a Service) nền tảng nhất của AWS.

**Thành phần cốt lõi:**
1. **Instance Types**: Phân loại cấu hình phần cứng. VD: `t3.micro` (nhỏ, dùng test), `c6g.4xlarge` (chuyên tính toán), `r5.8xlarge` (chuyên RAM).
2. **AMI (Amazon Machine Image)**: Bản đồ họa chứa hệ điều hành và phần mềm để khởi động EC2.
3. **EBS (Elastic Block Store)**: Ổ cứng mạng gắn vào máy EC2. Nếu tắt EC2, dữ liệu trên EBS vẫn còn.
4. **Auto Scaling Group (ASG)**: Một nhóm các máy chủ EC2 tự động tăng hoặc giảm số lượng dựa trên chỉ số (VD: CPU > 70% thì tạo thêm máy).

</details>

**Amazon EC2 (Elastic Compute Cloud)** is a web service that provides secure, resizable compute capacity in the cloud. It is the most fundamental IaaS (Infrastructure as a Service) offering in AWS.

**Core Components:**
1. **Instance Types**: Categorizations of hardware. E.g., `t3.micro` (small, cheap), `c6g.4xlarge` (Compute-optimized), `r5.8xlarge` (Memory-optimized).
2. **AMI (Amazon Machine Image)**: The template that contains the OS and software needed to launch your instance.
3. **EBS (Elastic Block Store)**: Network-attached hard drives for your EC2 instances. If you terminate the EC2 instance, the EBS volume can persist.
4. **Auto Scaling Group (ASG)**: A logical grouping of EC2 instances that automatically scale horizontally (add/remove instances) based on metrics (e.g., average CPU > 70%).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Mua một máy chủ vật lý thường tốn hàng chục ngàn đô la và mất nhiều tuần để lắp đặt. Nếu bạn mua cấu hình quá yếu, app sẽ sập lúc đông khách. Nếu mua cấu hình quá mạnh, bạn lãng phí tiền khi vắng khách.
EC2 giải quyết bằng chữ **Elastic (Đàn hồi)**. Bạn có thể thuê một siêu máy tính 96 cores trong vòng 1 tiếng đồng hồ, giải mã xong một bộ gen, rồi tắt nó đi với chi phí chỉ $3.

</details>

Procuring physical hardware involves heavy upfront Capital Expenditure (CapEx) and takes weeks to provision. If you guess your capacity wrong and buy a server that is too small, your app crashes during traffic spikes. If you buy a server that is too large, it sits idle wasting money.
EC2 solves this with the word **Elastic**. You can rent a massive 96-core supercomputer for exactly 1 hour, process a genome sequence, and terminate it, paying only $3.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Không có Auto Scaling (Scale Up / Vertical Scaling)**
- Server của bạn bị quá tải. Bạn tắt server đi, gắn thêm RAM và CPU, bật lại. (Phải có thời gian Downtime - mất khách). Máy chủ mạnh nhất cũng có giới hạn trần vật lý.

**Có Auto Scaling (Scale Out / Horizontal Scaling)**
- Server của bạn đang quá tải (CPU 90%). 
- ASG lập tức đẻ thêm 3 Server giống hệt (CPU giảm xuống 30%).
- Khách hàng không bị ngắt kết nối. Không có giới hạn trần (có thể gọi hàng ngàn máy chủ).

</details>

### Without Auto Scaling (Vertical Scaling / Scale Up)
- Your server hits 100% CPU. You have to shut the server down, manually upgrade it to a larger Instance Type (add RAM/CPU), and reboot.
- **Flaws**: Results in application Downtime. Also, there is a hard physical limit to how large a single machine can be.

### With Auto Scaling (Horizontal Scaling / Scale Out)
- Your server hits 90% CPU.
- The ASG immediately spins up 3 more identical EC2 instances in parallel behind a Load Balancer. Traffic distributes across all 4 servers.
- **Benefits**: Zero downtime. Mathematically infinite scalability.

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Web Hosting (Load Balanced)**: Dùng `Application Load Balancer (ALB)` đứng trước một dàn Auto Scaling Group (EC2). Đây là kiến trúc chuẩn cho 90% Web App.
2. **Machine Learning / Render Video**: Thuê các EC2 dòng `P` hoặc `G` (có sẵn GPU Nvidia) để huấn luyện AI, dùng xong tắt đi để đỡ tốn tiền.
3. **Spot Instances cho tác vụ ngầm (Background Jobs)**: Nếu bạn có tác vụ chạy ngầm không quan trọng (ví dụ resize ảnh), bạn có thể dùng Spot Instances - máy ế của AWS bán rẻ giảm giá 90%. Nhưng AWS có thể giật lại máy bất cứ lúc nào!

**Không nên làm (Anti-patterns):**
- **Cất trữ file ảnh vào ổ cứng EBS của EC2**: Nếu EC2 bị lỗi và chết, ảnh của người dùng bị mất! Thay vào đó, EC2 chỉ xử lý, còn file phải lưu vào S3 (bất tử) hoặc EFS (ổ đĩa mạng chung).

</details>

1. **Standard Web Hosting**: Placing an `Application Load Balancer (ALB)` in front of an Auto Scaling Group of EC2 instances. This handles web traffic resiliently across multiple Availability Zones.
2. **Machine Learning / GPU Rendering**: Renting `P` or `G` family instances (which possess powerful Nvidia GPUs) by the hour to train AI models or render 3D scenes, terminating them immediately after to save massive costs.
3. **Cost Optimization with Spot Instances**: For non-critical, interruptible background tasks (like resizing images or batch data processing), you can use Spot Instances—AWS's excess unused capacity sold at up to a 90% discount. Caveat: AWS can reclaim (kill) a Spot Instance with only a 2-minute warning.

### Anti-Patterns
- **Storing User Uploads on the local EBS volume**: If an EC2 instance crashes or is terminated by the Auto Scaling Group (Scale in), the local EBS volume is usually destroyed. If users uploaded profile pictures there, the data is gone forever. **Best Practice**: Treat EC2 instances as *stateless, disposable workers*. Save all persistent files to **Amazon S3** or **EFS**, and save data to an **RDS** database.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Instance Store vs EBS**
- Hầu hết mọi người dùng **EBS (Elastic Block Store)** - ổ cứng gắn mạng. Ưu điểm: Nếu EC2 chết, EBS có thể gỡ ra gắn sang máy khác. Nhược điểm: Bị nghẽn mạng (Network bottleneck).
- **Instance Store**: Ổ cứng cắm vật lý trực tiếp lên bo mạch chủ của máy chủ EC2. Ưu điểm: Tốc độ I/O nhanh vô đối (Tốt cho Caching, Redis, Swap). Nhược điểm: Phù du (Ephemeral). Nếu bạn Stop/Start EC2, TOÀN BỘ dữ liệu trên Instance Store sẽ bị xóa sạch!

**2. Tiền khởi động (Baking AMIs)**
Nếu cài đặt phần mềm trên EC2 mất 5 phút (tải các thư viện Python, cài Nginx), thì khi Auto Scaling gọi máy mới, phải 5 phút sau máy mới phục vụ được khách (Quá chậm!). 
**Best Practice**: Dùng công cụ như **Packer** để nướng (Bake) sẵn mọi phần mềm vào trong AMI. Khi ASG khởi động máy từ AMI này, nó chỉ mất 30 giây là sẵn sàng phục vụ. Immutable Infrastructure!

</details>

### 1. Instance Store vs. EBS
- **EBS (Elastic Block Store)**: Network-attached storage. *Pro*: Persistent. You can detach it from a broken EC2 and attach it to a new one. *Con*: Slower disk I/O because data travels over the network.
- **Instance Store**: Physically attached SSDs bolted directly onto the host hardware running the EC2 instance. *Pro*: Insanely fast I/O speeds (millions of IOPS). Ideal for buffer caches, Redis, or temporary processing. *Con*: **Ephemeral**. If the instance is Stopped, Terminated, or hardware fails, the data on the Instance Store is permanently, irrevocably lost.

### 2. Baking AMIs (Immutable Infrastructure)
If your `User Data` script (the bash script that runs at boot) takes 5 minutes to download Python packages, compile C-libraries, and configure Nginx, then during a massive traffic spike, your Auto Scaling Group will take 5 minutes to bring a new server online. The spike might crush you before the server is ready.
**Best Practice (The Golden AMI)**: Use HashiCorp Packer to "bake" (pre-install) the OS, patches, Nginx, and your Python dependencies into a custom AMI ahead of time. When the ASG scales out using this Golden AMI, boot time drops from 5 minutes to 30 seconds.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đoạn Bash script bên dưới gọi là **User Data**. Khi EC2 khởi động lần đầu tiên, AWS sẽ chạy đoạn script này với quyền Root. Nó cực kỳ hữu ích để cấu hình máy chủ tự động mà không cần SSH vào máy.

</details>

### User Data Script (Bash)

When you launch an EC2 instance, you can pass a shell script called "User Data". AWS runs this script exactly once, at boot, with root privileges. This allows you to bootstrap servers without manual SSH intervention.

```bash
#!/bin/bash
# 1. Update the OS
yum update -y

# 2. Install Apache Web Server
yum install -y httpd

# 3. Start the service and ensure it runs on reboot
systemctl start httpd
systemctl enable httpd

# 4. Write a simple webpage dynamically grabbing the EC2 metadata (Instance ID)
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
echo "<h1>Hello World! I am served from EC2 instance: $INSTANCE_ID </h1>" > /var/www/html/index.html
```

*(Note: The IP `169.254.169.254` is the AWS Instance Metadata Service (IMDS). Any EC2 instance can ping this internal IP to find out its own ID, IP address, and assumed IAM Role).*

---

## Related Topics

- [AWS VPC](./aws-vpc.md) — Where EC2 instances physically reside.
- [AWS IAM](./aws-iam.md) — Attaching Roles to EC2 so it doesn't need hardcoded passwords.
- [AWS ECS & EKS](./aws-ecs-and-eks.md) — The modern alternative to managing raw EC2 instances (Docker Containers).
