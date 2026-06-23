# Cloud Computing Models: IaaS, PaaS, SaaS

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Ngày xưa, để mở một công ty phần mềm, bạn phải mua những cục Server bằng sắt (Máy chủ vật lý), cắm điện, kéo cáp mạng, thuê kỹ sư trực 24/7. Nếu cháy nhà, mất trắng. **Điện toán đám mây (Cloud Computing)** giải quyết vấn đề này bằng cách cho bạn ĐI THUÊ máy chủ của Amazon (AWS), Google (GCP), hoặc Microsoft (Azure). Tùy vào độ "lười" của bạn, Cloud được chia làm 3 loại chính: IaaS, PaaS, và SaaS. Càng lười thì càng nhàn, nhưng càng ít quyền kiểm soát và càng đắt tiền.

</details>

> **Summary**: Historically, deploying software required immense capital expenditure (CapEx) to purchase physical rack servers, rent data center space, install cooling systems, and hire 24/7 on-call hardware technicians. **Cloud Computing** revolutionized the industry by transitioning to an Operational Expenditure (OpEx) model—renting infinite, highly available computational power from hyper-scalers (AWS, Google Cloud, Azure) over the internet. Cloud services are architecturally categorized into three primary models based on the division of responsibility: **IaaS, PaaS, and SaaS**. The more abstraction you rent, the less engineering overhead you incur, but the less architectural control you retain.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn thèm ăn Pizza.
1. **On-Premise (Tự làm từ A-Z)**: Mua phô mai, nhào bột, tự nướng bằng lò ở nhà. Rất cực, nhà cháy tự chịu. (Đây là Cắm máy chủ ở công ty).
2. **IaaS (Thuê Bếp)**: Bạn ra ngoài thuê một cái bếp nướng công nghiệp (Thuê Máy chủ trống). Họ cho bạn lò nướng và điện. Việc nhào bột, chọn loại phô mai, nướng cháy hay khét là DO BẠN. 
3. **PaaS (Gọi giao bánh tận nhà)**: Bạn gọi cửa hàng. Họ làm sẵn cái bánh nướng chín hoàn hảo rồi mang đến nhà bạn. Bạn chỉ việc mở cửa ra, tự cắt bánh và ngồi ăn ở bàn ăn nhà mình (Chỉ lo viết Code, Server tự chạy).
4. **SaaS (Ra thẳng nhà hàng ăn)**: Bạn đi tay không ra nhà hàng. Bạn ngồi vào bàn, há miệng ra, nhân viên đút Pizza tận mồm, ăn xong đứng dậy quẹt thẻ đi về. Không phải rửa bát, không lo gì cả. (Dùng phần mềm như Gmail, Facebook).

</details>

Imagine you are craving a Pizza. This is "Pizza as a Service".
1. **On-Premise (Legacy)**: You grow the tomatoes, milk the cow for cheese, build an oven from bricks, and bake it yourself. Maximum effort, maximum responsibility.
2. **IaaS (Infrastructure as a Service)**: "Take-and-Bake". You go to the store and buy a raw, frozen pizza. You must bring it home, use your own electricity, your own oven, and set the temperature. If you burn it, it's your fault.
3. **PaaS (Platform as a Service)**: "Delivery". You order a hot, perfectly cooked pizza to your house. The restaurant managed the oven and the ingredients. You only provide the dining table and the drinks.
4. **SaaS (Software as a Service)**: "Dining Out". You sit at a restaurant. The waiter brings the pizza, pours your drink, and washes the dishes after you leave. You only consume the final product.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. IaaS (Infrastructure as a Service)**: Thuê Phần cứng. Amazon cung cấp cho bạn CPU, RAM, Ổ cứng, và Địa chỉ IP ảo. Bạn phải TỰ CÀI hệ điều hành (Linux/Windows), tự cài CSDL, tự cài tường lửa.
**2. PaaS (Platform as a Service)**: Thuê Nền tảng. Nền tảng đã cài sẵn Hệ điều hành, Node.js/Java, bảo mật mạng. Bạn chỉ việc mang cục Code (chữ) của bạn quăng lên nền tảng, nền tảng sẽ tự động chạy cục Code đó thành trang web.
**3. SaaS (Software as a Service)**: Thuê Phần mềm. Bạn là người dùng cuối (User). Bạn không nhìn thấy CPU, không nhìn thấy Code. Bạn chỉ thấy giao diện trang web, bấm đăng nhập là xài.

</details>

The Cloud division of responsibility (The Shared Responsibility Model):
1. **IaaS (Infrastructure as a Service)**: You rent virtualized raw hardware primitives over the internet (Compute, Storage, Networking). The Cloud Provider manages the physical data center, the hypervisor, and the physical servers. **YOU** manage the Operating System (OS patching), Firewalls, Runtimes, and the Application Code.
2. **PaaS (Platform as a Service)**: You rent a fully managed runtime environment. The Cloud Provider completely abstracts away the Operating System, Network load balancing, and Server provisioning. **YOU** only provide the physical Application Code and the Database schemas.
3. **SaaS (Software as a Service)**: You rent a fully functional software application. The Cloud Provider manages literally everything from the hardware up to the User Interface. **YOU** only manage your user account settings and input data.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề của Máy chủ vật lý (On-Premise)**:
Lazada muốn chạy khuyến mãi ngày 11/11. Ngày thường họ cần 10 máy chủ. Ngày 11/11 họ cần 100 máy chủ. Nếu mua bằng sắt, họ mất hàng triệu đô la để sắm 90 cái máy chủ, dùng đúng 1 ngày 11/11, rồi vứt xó 364 ngày còn lại. Cực kỳ lãng phí.

**Giải pháp Điện toán Đám mây (Cloud Elasticity)**:
Mô hình "Dùng bao nhiêu, trả bấy nhiêu" (Pay-as-you-go). Sáng ngày 11/11, Lazada bấm nút thuê 90 con Server ảo trên mây của Amazon (AWS). Hệ thống tự động mọc ra (Scale-up) chịu tải cực mượt. Qua ngày 12/11, hết khuyến mãi, Lazada bấm nút Xóa 90 con Server đó đi. Họ chỉ phải trả tiền thuê cho đúng 24 tiếng đồng hồ đó.

</details>

**The CapEx Nightmare (On-Premise Scaling)**:
Consider a Retailer preparing for Black Friday. Normally, their website traffic requires 5 physical servers. On Black Friday, traffic spikes 20x, requiring 100 servers. To survive, the Retailer must purchase 95 brand new, expensive physical servers, install them, and maintain them. On Saturday, traffic drops back to normal. The 95 servers now sit entirely idle for the remaining 364 days of the year, wasting millions of dollars in CapEx and electricity.

**The Cloud Solution (Elasticity and OpEx)**:
Cloud computing introduces the **Pay-as-you-go** utility model. On Black Friday morning, the Retailer's automated infrastructure dynamically spins up 95 Virtual Machines (IaaS) in AWS within 3 seconds. The servers handle the massive traffic spike. At midnight, when the sale ends, the automation terminates the 95 VMs. The Retailer is only billed for the exact hours those VMs were running. Infinite scalability with zero upfront capital investment.

---

## Layer 3: Without vs. With Comparison (Compare)

### The Shared Responsibility Model

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Bảng phân chia trách nhiệm. Ai chịu lỗi nếu hệ thống bị sập do quá tải hoặc do lỗi Code?
</details>

Who is legally and operationally responsible when something catches fire?

| Layer | On-Premise | IaaS (e.g., AWS EC2) | PaaS (e.g., Heroku) | SaaS (e.g., Gmail) |
|---|---|---|---|---|
| **Data / Content** | YOU | YOU | YOU | YOU |
| **Application Code** | YOU | YOU | YOU | <span style="color:blue">Provider</span> |
| **Runtime (Java/Node)**| YOU | YOU | <span style="color:blue">Provider</span> | <span style="color:blue">Provider</span> |
| **Operating System** | YOU | YOU | <span style="color:blue">Provider</span> | <span style="color:blue">Provider</span> |
| **Virtualization** | YOU | <span style="color:blue">Provider</span> | <span style="color:blue">Provider</span> | <span style="color:blue">Provider</span> |
| **Servers / Network** | YOU | <span style="color:blue">Provider</span> | <span style="color:blue">Provider</span> | <span style="color:blue">Provider</span> |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Đại diện IaaS (Amazon EC2, Google Compute Engine, DigitalOcean Droplets)**: Phù hợp cho các công ty lớn, có nguyên một Đội ngũ Quản trị Hệ thống (SysAdmin/DevOps). Họ muốn tự do cài đặt cấu hình phần cứng tối đa để tối ưu chi phí.
- **Đại diện PaaS (Vercel, Heroku, AWS Elastic Beanstalk)**: Phù hợp cho các team Startup nhỏ, hoặc dự án cá nhân (Sinh viên làm đồ án). Không có DevOps, không biết cài Linux. Chỉ việc lệnh `git push`, Vercel tự động lấy code build thành trang Web cho chạy luôn. Cực kỳ tiện lợi, nhưng nếu dùng nhiều sẽ cực kỳ đắt đỏ.
- **Đại diện SaaS (Gmail, Salesforce, Zoom, Slack)**: Phù hợp cho người dùng kinh doanh. Công ty A muốn xài Email, thay vì thuê Dev tự code ra một hệ thống Email (IaaS), họ trả 5 đô/tháng để dùng Gmail.

</details>

- **IaaS Champions (AWS EC2, Google Compute Engine, Azure VMs)**: Mandatory for massive Enterprise architectures with highly specialized requirements (e.g., custom Linux Kernels, hyper-specific firewall routing, or deploying proprietary Database clusters). Requires a dedicated, highly skilled DevOps/SRE engineering team to maintain OS security patches.
- **PaaS Champions (Vercel, Heroku, AWS Elastic Beanstalk, Google App Engine)**: The absolute gold standard for Startups and rapid MVPs. A small team of 3 Frontend developers does not know how to secure a Linux server. With PaaS, they simply execute `git push main`. The Platform detects the Node.js code, compiles it, provisions a hidden server, load balances it, and attaches an SSL certificate automatically. It trades extreme Developer Velocity for a premium price markup.
- **SaaS Champions (Salesforce, Slack, Google Workspace, GitHub)**: Consumed by the Business Layer. A corporation requires an internal chat tool. They do not hire 50 engineers to build an open-source chat clone (IaaS). They simply pay $10/user/month to Slack. Turnkey solutions minimizing operational risk.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiểu rõ Lock-in (Bị trói chân)**: Càng dùng nền tảng nhàn hạ (PaaS), bạn càng bị trói chặt vào nhà cung cấp đó. Ví dụ bạn xài Vercel, xài toàn bộ các hàm độc quyền của Vercel cung cấp. Một ngày Vercel báo tăng giá x10 lần, bạn KHÔNG THỂ BÊ CODE ĐÓ vứt sang máy chủ khác (IaaS) chạy được. Rất đau đớn. Đóng gói Code bằng Docker là giải pháp duy nhất.
2. **Infrastructure as Code (IaC)**: Dù xài IaaS (EC2), đừng bao giờ lên giao diện web bấm bấm chuột để tạo Server. Lỡ lính mới xóa nhầm, bạn không nhớ đã cấu hình gì để tạo lại. BẮT BUỘC dùng Code (Terraform) để viết: "Tạo 5 con EC2 loại t2.micro". Code chạy ra Server. Mất Server thì chạy Code 5 giây là có lại.

</details>

1. **Vendor Lock-In Awareness**: The Paradox of Abstraction. The higher you climb the Cloud stack (into heavily managed PaaS or Serverless architectures like AWS Lambda/DynamoDB), the tighter you bind your Application Code to proprietary vendor APIs. If AWS raises prices 400%, you cannot easily migrate a monolithic DynamoDB architecture to Google Cloud. **Mitigation**: Strictly containerize applications using standard Docker images (IaaS/CaaS layer). A Docker container runs identically on AWS, Google Cloud, or a laptop in your basement.
2. **Infrastructure as Code (IaC)**: Never provision IaaS resources manually by "ClickOps" (clicking through the AWS Web Console GUI). Manual provisioning is inherently un-auditable, un-repeatable, and prone to catastrophic human error. You must utilize IaC tools (e.g., **Terraform**, AWS CloudFormation) to declare your entire architecture strictly in version-controlled text files. If a rogue admin accidentally deletes your entire VPC, Terraform can rebuild the exact complex network matrix from scratch in 30 seconds.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bỏ quên Bảo mật ở IaaS**: Amazon cam kết "Bảo mật CỦA Đám mây" (Bảo vệ trung tâm dữ liệu khỏi cháy nổ, trộm cắp). Nhưng bạn phải chịu trách nhiệm "Bảo mật TRONG Đám mây". Dev thuê 1 con Server EC2 (IaaS), quên thiết lập Tường lửa (Firewall), mở tung port 22 và port CSDL ra thế giới. 5 tiếng sau, Hacker mò vào xóa sạch dữ liệu và tống tiền Bitcoin. Lỗi này là của bạn, không phải của Amazon.
2. **Hóa đơn Đám mây lủng màng nhĩ**: Đám mây dùng bao nhiêu trả bấy nhiêu. Dev test tính năng xong quên không bấm nút Tắt Server. Tháng sau AWS gửi hóa đơn 2,000 USD (khoảng 50 triệu) về thẻ tín dụng. Rất nhiều sinh viên đã phải khóa thẻ ngân hàng vì lỗi ngớ ngẩn này. Luôn cài đặt Cảnh báo Ngân sách (Billing Alarms)!

</details>

1. **Misunderstanding the Shared Responsibility Model (IaaS)**: A lethal organizational oversight. AWS guarantees "Security OF the Cloud" (Physical guards at the datacenter, hypervisor isolation). The Customer is legally responsible for "Security IN the Cloud". A junior dev spins up an EC2 instance, ignores the Security Group (Firewall) rules, and exposes Port 22 (SSH) and Port 3306 (MySQL) to `0.0.0.0/0` (The entire planet). Automated Russian/Chinese bots discover it within 3 minutes, brute-force the password, encrypt the database, and demand a $50,000 Ransomware payment. AWS will not help you.
2. **Cloud Shock (The Infinite Bill)**: IaaS elasticity is a double-edged sword. A developer spins up a massive, $10-per-hour GPU instance to train an AI model on Friday afternoon. They go home for the weekend and forget to click "Terminate". On Monday, the company credit card is billed $720 for a server doing absolutely nothing. **Mandatory Protocol**: Implement aggressive AWS Billing Alarms and automated Lambda scripts to forcefully terminate non-production servers every Friday at 7:00 PM.

---

## Related Topics

- For managing applications easily across any IaaS provider, explore **[Virtualization & Containers](./virtualization-containers.md)**.
- To execute code without managing the underlying IaaS at all, see **[Serverless](./serverless.md)**.
- The automation of deploying code into PaaS/IaaS is covered in **[CI/CD Concepts](../sdlc/ci-cd-concepts.md)**.
