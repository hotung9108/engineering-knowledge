# System Administration & Permissions

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hệ điều hành Linux được thiết kế từ gốc để phục vụ "Nhiều người dùng" (Multi-user) cùng lúc. Giám đốc có quyền xóa file, Nhân viên chỉ có quyền đọc file. Để làm được điều này, Linux có một hệ thống Phân quyền (Permissions) cực kỳ chặt chẽ dựa trên 3 nhóm: Chủ sở hữu (User), Nhóm (Group), và Người lạ (Others). Cùng với đó là các công cụ Quản trị hệ thống (Systemd) giúp khởi động và giữ cho các ứng dụng Web/Database luôn chạy ngầm 24/7 kể cả khi bạn đã tắt máy tính cá nhân đi ngủ.

</details>

> **Summary**: The UNIX/Linux architecture is fundamentally designed from the kernel up as a secure, Multi-User environment. Absolute chaos would ensue if an intern could blindly delete the production database log files. Linux enforces security via a rigid **Permission Model** dividing access into User, Group, and Others, manipulated via `chmod` and `chown`. Furthermore, modern Linux relies on **Systemd**, a massive initialization and service manager that ensures background daemons (like Nginx, Docker, PostgreSQL) boot automatically on server startup and survive crashes via automatic restarts.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng một Tòa lâu đài có rất nhiều Căn phòng (Thư mục) và Đồ vật (File).
1. **Users & Groups (Người dùng và Nhóm)**: Bạn là Vua (Root) có quyền đi vào mọi phòng. Lính gác (Group A) chỉ được đứng ngoài sân. Người hầu (Group B) chỉ được vào bếp.
2. **Permissions (Quyền hạn `rwx`)**: Tại kho báu, Vua treo một tấm bảng quy định: 
   - Vua: Được Đọc (`r`), Viết/Lấy đồ (`w`), và Chạy máy móc (`x`).
   - Lính gác (Nhóm): Chỉ được Đọc/Nhìn (`r`). Không được lấy.
   - Người đi đường (Người lạ): Không được làm gì cả (`-`).
3. **Systemd (Quản gia)**: Bạn thuê một ông Quản gia (`systemd`). Bạn dặn: "Bảo vệ kho báu phải đứng gác 24/7. Nếu nó buồn ngủ gục ngã (Crash), ông phải tát nó tỉnh dậy bắt gác tiếp ngay lập tức". Systemd chính là phần mềm giữ cho Server không bao giờ sập.

</details>

Imagine a massive Castle containing thousands of Rooms (Directories) and Objects (Files).
1. **Users & Groups**: You are the King (`root`), possessing the skeleton key to every room. The Royal Guard (A Group) is permitted only in the armory. The Peasants (Others) are kept outside.
2. **Permissions (`rwx`)**: On the Armory Door, the King nails a strict Access Rule plaque:
   - The King (User): Can Read (`r`), Write/Modify (`w`), and Execute weapons (`x`).
   - The Guards (Group): Can Read/See (`r`) the weapons, but cannot modify them.
   - The Peasants (Others): Absolute zero access (`---`).
3. **Systemd (The Butler)**: You hire an immortal Butler (`systemd`). You command the Butler: "The Water Pump (Nginx) must run 24/7. If the pump breaks down (Crashes) at 3:00 AM, you must instantly restart it before anyone notices." Systemd ensures background services never truly die.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Quyền hạn (Permissions)**: Trong Linux, mỗi file có 3 loại quyền cơ bản:
- `r` (Read - Đọc): Xem nội dung file, xem danh sách thư mục.
- `w` (Write - Ghi): Sửa file, xóa file, tạo file mới.
- `x` (Execute - Chạy): Khởi chạy file Script hoặc mở thư mục ra.
Các quyền này được áp dụng cho 3 đối tượng: **U**ser (Chủ), **G**roup (Nhóm), **O**thers (Người khác).
**2. Systemd / Systemctl**: Phần mềm (Daemon) đầu tiên khởi động khi bạn bật máy chủ Linux. PID (Process ID) của nó luôn luôn là `1`. Nó chịu trách nhiệm gọi tất cả các phần mềm khác dậy (Web server, CSDL). Lệnh tương tác chính là `systemctl`.

</details>

**1. The Permission Matrix (`rwx`)**: Every file and directory in Linux enforces a strict 9-character permission string representing Read (`r`), Write (`w`), and Execute (`x`). These are applied distinctly to three entities: The Owner (**U**ser), the assigned **G**roup, and Everyone Else (**O**thers).
**2. Systemd (`systemctl`)**: The "Mother of all Processes." When the Linux kernel boots, the very first process it spawns is `systemd` (PID 1). It is an immense suite of software responsible for booting the system, managing background Daemons (Services), tracking logs (`journalctl`), and enforcing auto-restart policies for crashed applications.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao phải chia quyền phức tạp?**
Nếu không có hệ thống phân quyền, hacker lừa được một phần mềm (Ví dụ: WordPress) chạy lệnh xấu. Lệnh đó có thể bay ra ngoài xóa sạch toàn bộ hệ điều hành. Phân quyền là lớp khiêng chặn đứng rủi ro. Ta ép WordPress chạy dưới tài khoản `www-data` (Tài khoản siêu yếu). Nếu WordPress bị hack, hacker cũng chỉ loanh quanh phá được thư mục của Web, không thể đụng tới thư mục Hệ điều hành.

**Tại sao phải dùng Systemd?**
Bạn gõ lệnh `node server.js` để chạy web. Bỗng nhiên code bạn bị Lỗi (Bug), phần mềm báo lỗi và tắt luôn (Crash). Trang web sập. Sáng hôm sau bạn tỉnh dậy thấy công ty mất 1 tỷ đồng.
Systemd sinh ra để bạn không bao giờ phải chạy phần mềm bằng tay. Bạn viết file cấu hình bảo Systemd chạy Node. Nếu Node sập lúc 2h sáng, Systemd tự động gọi lệnh chạy lại Node trong 0.1 giây.

</details>

**Why is strict permissioning mandatory? (The Blast Radius)**
If permissions did not exist, any compromised software could destroy the entire hardware node. A hacker executes an exploit via a vulnerability in your PHP WordPress site. If WordPress runs as the `root` user, the hacker instantly gains God-mode control over the entire server. By enforcing strict permissions, we run WordPress under a crippled `www-data` user account. Even if hacked, the blast radius is physically contained to the `/var/www` folder. The OS survives.

**Why utilize Systemd for execution?**
Junior developers deploy backend code by executing `npm start` in a raw terminal, and then closing their laptop. The application instantly dies because the terminal session was severed. Or, if it stays alive, a random `TypeError` exception crashes the Node.js process at 3:00 AM. 
Systemd daemonizes your application. It detaches it from the terminal, pushes it to the background, and relentlessly monitors its health. If the process crashes, Systemd immediately executes the `Restart=always` directive, reviving the server before pagers even go off.

---

## Layer 3: Without vs. With Comparison (Compare)

### Octal Permission Math (The Numbers)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Các lệnh `chmod` thường dùng số (Ví dụ: `chmod 755`). Dưới đây là cách tính toán.
</details>

SysAdmins rarely type `chmod u=rwx,g=rx,o=rx`. They use Octal notation (numbers).
Each permission has a mathematical weight:
- **Read (`r`) = 4**
- **Write (`w`) = 2**
- **Execute (`x`) = 1**
- **None (`-`) = 0**

You sum the numbers for each entity (User, Group, Others).

| Command | Math (U - G - O) | String | Meaning / Use Case |
|---|---|---|---|
| `chmod 777` | `(4+2+1) (4+2+1) (4+2+1)` | `rwxrwxrwx` | **Absolute Disaster**. Everyone can read, edit, and run this. Never use in Production. |
| `chmod 755` | `(4+2+1) (4+1) (4+1)` | `rwxr-xr-x` | **Standard Folder**. Owner can do anything. Others can only read and enter the folder. |
| `chmod 644` | `(4+2) (4) (4)` | `rw-r--r--` | **Standard File**. Owner can edit. Others can only read. (HTML files, configs). |
| `chmod 400` | `(4) (0) (0)` | `r--------` | **Highly Secure**. Only the Owner can read. (Used for SSH Private Keys `.pem`). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Quản lý Quyền Chủ Sở Hữu (`chown`)**: Trình duyệt truy cập web qua Nginx (Tài khoản mặc định tên là `www-data`). Nhưng code của bạn được copy vào bằng tài khoản `ubuntu`. Khi Nginx cố đọc file của `ubuntu`, nó bị chặn (Lỗi 403 Forbidden). Bạn phải gõ lệnh đổi chủ: `chown -R www-data:www-data /var/www/html`. Lỗi 403 sẽ biến mất.
- **Biến script thành phần mềm gõ được (`chmod +x`)**: Bạn viết file `deploy.sh`. Gõ lệnh `./deploy.sh` bị báo `Permission denied`. Vì file văn bản mặc định không được phép "Chạy". Bắt buộc phải thêm quyền Execute: `chmod +x deploy.sh`.
- **Systemctl cho ứng dụng Web**: Thay vì dùng `pm2` hay `forever` (các phần mềm bên thứ 3) để giữ cho Node.js chạy ngầm, DevOps chuyên nghiệp sẽ tự viết file `.service` nhét vào Systemd để quản lý chuẩn nhất theo hệ điều hành.

</details>

- **Fixing Web Server 403 Errors (`chown`)**: The most common web deployment error. You upload website files as the `root` or `ec2-user` account. Nginx attempts to serve these files to the internet, but Nginx operates under the sandboxed `www-data` user account. The kernel violently blocks Nginx, resulting in an `HTTP 403 Forbidden` error. You must explicitly transfer Ownership of the directory to Nginx: `chown -R www-data:www-data /var/www/`.
- **Executing Shell Scripts (`chmod +x`)**: When you create a `backup.sh` file, it is merely a text file. If you attempt to execute it (`./backup.sh`), Linux denies access. You must physically grant the Execute permission explicitly: `chmod +x backup.sh`.
- **Production Application Daemonization**: While tools like `pm2` (Node.js) or `tmux` exist, absolute enterprise production environments rely strictly on `systemd` to manage background services (Docker, PostgreSQL, Nginx, Custom APIs) because it integrates flawlessly with the OS boot sequence and Centralized Logging (`journald`).

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nguyên tắc Quyền Tối thiểu (Least Privilege)**: Tuyệt đối không bao giờ dùng `chmod 777` chỉ để sửa cái lỗi "Permission Denied" vì lười suy nghĩ. Nó mở toang cửa nhà bạn cho mọi loại mã độc đi vào sửa file. Hãy tìm hiểu chính xác phần mềm nào đang cần đọc file, và cấp quyền đúng cho User/Group đó thôi.
2. **Kiểm tra Log của Systemd (`journalctl`)**: Khi Nginx không chịu khởi động lên (`systemctl start nginx` báo lỗi), đừng hoảng. Tất cả lý do tại sao nó chết đều được ông quản gia ghi chép lại. Gõ lệnh `journalctl -u nginx -e` (Xem log ở đoạn cuối của Nginx). Nó sẽ chỉ rõ cho bạn biết "Mày viết sai dấu chấm phẩy ở dòng số 5 file config".

</details>

1. **The Principle of Least Privilege**: The cardinal sin of Junior SysAdmins is aggressively executing `sudo chmod -R 777 /` to bypass frustrating "Permission Denied" errors. This is architectural suicide. You have explicitly granted world-writable execution rights to every malicious payload on the internet. Take the 5 minutes required to understand *which* specific user requires access, and elegantly utilize `chown` and targeted `644/755` permissions.
2. **Mastering the Journal (`journalctl`)**: When a Systemd service fails to boot (`systemctl start myapp` fails), Systemd swallows the standard output. To debug why the application crashed during initialization, you must query the central binary logging daemon. Executing `journalctl -u myapp.service -e -f` tails the exact standard error output of the crashing process, immediately revealing the syntax error or missing environment variable causing the death.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Quên `systemctl enable`**: Bạn hì hục cấu hình Systemd chạy con App rất mượt. Bạn gõ `systemctl start app`. Mọi thứ hoàn hảo. 3 tháng sau, Amazon bảo trì máy chủ, khởi động lại máy. Server bật lên nhưng Web bạn sập. Tại sao? Vì lệnh `start` chỉ chạy ngay lúc đó. Bạn QUÊN gõ lệnh `systemctl enable app` (Cho phép App tự chạy mỗi khi máy chủ khởi động lại).
2. **Cấu hình SSH bằng mật khẩu**: Đây là điểm chết bảo mật của mọi máy chủ Linux. Hacker dùng bot để gõ dò mật khẩu liên tục hàng triệu lần/phút (Brute-force). Mật khẩu của bạn là `admin123` sẽ bị đoán trúng trong 2 giây. BẮT BUỘC phải tắt tính năng đăng nhập bằng mật khẩu, và chỉ cho phép đăng nhập bằng SSH Key (Khóa mã hóa nhị phân).

</details>

1. **Failing to `enable` Services**: A DevOps engineer flawlessly configures a new database daemon, executes `systemctl start postgresql`, and goes home. 6 months later, the datacenter loses power and the server reboots. The Database does not come back online. The engineer forgot the critical `systemctl enable postgresql` command, which instructs Systemd to weave the service into the automated boot sequence.
2. **Password-Based SSH Authentication**: Exposing Port 22 (SSH) to the public internet while allowing password authentication is a guaranteed compromise. Global botnets ruthlessly execute SSH Brute-Force dictionary attacks 24/7. An easily guessed password will be cracked in minutes. **Mandatory Configuration**: Edit `/etc/ssh/sshd_config`, set `PasswordAuthentication no`, and strictly mandate asymmetric cryptographic authentication using `.pem` or `.pub` SSH Keys.

---

## Related Topics

- For the commands used to navigate the file system before changing permissions, see **[Essential Commands](./essential-commands.md)**.
- To automate permission changes and system administration across thousands of servers, explore **[Shell Scripting](./shell-scripting.md)**.
- For packaging apps so you don't even have to worry about Host OS permissions, see **[Virtualization & Containers](../cloud-computing/virtualization-containers.md)**.
