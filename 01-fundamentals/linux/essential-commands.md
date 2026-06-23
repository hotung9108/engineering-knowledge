# Linux: Essential Commands & File System

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: 90% máy chủ trên thế giới chạy Linux. Trái ngược với Windows dùng chuột (GUI), Linux giao tiếp với kỹ sư chủ yếu thông qua Màn hình đen gõ chữ (CLI - Command Line Interface). Sức mạnh của Linux nằm ở chỗ: Bất cứ thứ gì bạn dùng chuột click được, Linux đều có thể thực hiện bằng một dòng lệnh, và nó nhanh hơn gấp vạn lần. Việc học thuộc các câu lệnh cơ bản để di chuyển, sao chép, và xem file trong Linux là kỹ năng sinh tồn bắt buộc của mọi Kỹ sư Phần mềm.

</details>

> **Summary**: 90% of the world's production servers run on Linux. Unlike consumer Operating Systems (Windows/macOS) that rely heavily on Graphical User Interfaces (GUIs), Linux demands interaction via the Command Line Interface (CLI). The true power of Linux is automation and pipeline chaining; every action achievable via a mouse click can be executed, chained, and automated exponentially faster via text commands. Memorizing the fundamental commands to navigate the hierarchical file system, manipulate files, and inspect processes is a non-negotiable survival skill for all Software Engineers.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang đi trong một Thư viện khổng lồ hoàn toàn bằng văn bản (Không có hình ảnh).
- **Trạng thái hiện tại (`pwd`)**: Bạn không biết mình đang đứng ở phòng nào. Bạn la lên `pwd` (Print Working Directory). Thư viện vọng lại: "Bạn đang ở phòng Khoa Học".
- **Nhìn xung quanh (`ls`)**: Bạn muốn biết trong phòng có sách gì. Bạn gõ `ls` (List). Thư viện liệt kê: Sách Toán, Sách Lý.
- **Đi sang phòng khác (`cd`)**: Bạn muốn sang phòng Văn Học. Bạn gõ `cd Van-Hoc` (Change Directory). Bạn lập tức bị dịch chuyển sang phòng đó.
- **Đọc sách (`cat`)**: Bạn muốn đọc cuốn "Truyện Kiều". Bạn gõ `cat Truyen-Kieu.txt`. Cả cuốn sách hiện ra trên màn hình.

</details>

Imagine navigating a massive, pitch-black Library where you can only interact by speaking commands into the dark.
- **Finding your location (`pwd`)**: You are lost. You shout `pwd` (Print Working Directory). The dark room responds: "You are currently inside the `/home/user/documents` corridor."
- **Looking around (`ls`)**: You want to see what is around you. You say `ls` (List). The room replies: "There are two items here: `fileA.txt` and `folderB`."
- **Walking to a new room (`cd`)**: You want to enter `folderB`. You command `cd folderB` (Change Directory). You are instantly teleported inside.
- **Reading a book (`cat`)**: You want to read the contents of `fileA.txt`. You say `cat fileA.txt` (Concatenate). The entire text of the book materializes floating in front of your eyes.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Mọi thứ đều là File (Everything is a file)**: Triết lý cốt lõi của Linux. Từ văn bản, ổ cứng cắm ngoài, chuột, bàn phím, kết nối mạng... tất cả đều được biểu diễn dưới dạng một "File".
**2. Cây thư mục (FHS - Filesystem Hierarchy Standard)**: Khác với Windows chia ra ổ `C:\` và `D:\`, Linux gộp chung tất cả vào một gốc duy nhất gọi là Rễ (`/` Root).
- `/bin`: Chứa các lệnh cơ bản (ls, cd).
- `/etc`: Chứa các file Cấu hình (Configuration).
- `/home`: Thư mục cá nhân của từng User (Giống `C:\Users\`).
- `/var`: Chứa các file hay thay đổi (Log hệ thống, Database).
**3. Bash / Shell**: Là phần mềm Màn hình đen. Nó hứng lệnh bạn gõ, dịch ra mã máy để Cốt lõi Linux (Kernel) hiểu và chạy.

</details>

**1. "Everything is a File"**: The foundational philosophical architecture of UNIX/Linux. Regular text, directories, external hard drives, keyboards, and even raw TCP network sockets are all uniformly represented and manipulated as file streams.
**2. FHS (Filesystem Hierarchy Standard)**: Unlike Windows which fragments physical drives into letters (`C:\`, `D:\`), Linux unifies all physical drives under a single absolute root directory `/`.
- `/bin` & `/usr/bin`: Contains essential executable command binaries (`ls`, `cat`).
- `/etc`: The nervous system. Contains system-wide configuration files (e.g., `/etc/nginx/nginx.conf`).
- `/home`: Personal isolated sandboxes for user accounts.
- `/var`: Variable data. Logs, databases, and caches that constantly mutate (`/var/log/syslog`).
**3. The Shell (Bash/Zsh)**: The command-line interpreter. The Shell is the program that accepts your human text (`ls -la`), parses it, and translates it into System Calls executed by the underlying Linux Kernel.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Tại sao Server không dùng giao diện chuôt (GUI) như Windows?**
Một hệ điều hành Windows 11 cần ít nhất 4GB RAM chỉ để chạy giao diện màn hình (hiển thị hình nền, icon, bóng mờ). Server thì làm gì có ai cắm màn hình vào mà xem? 
Linux Server cắt bỏ hoàn toàn lớp giao diện đồ họa. Nó biến thành một cỗ máy nhẹ tựa lông hồng, chỉ ăn khoảng 100MB RAM khi khởi động. Toàn bộ lượng RAM khổng lồ còn lại sẽ được dồn 100% sức mạnh cho việc chạy Database và Web API. Hơn nữa, Command Line cho phép Dev viết Script để tự động hóa 1000 con Server cùng lúc (Chuột không thể click tự động trên 1000 máy được).

</details>

**Why eliminate the Graphical User Interface (GUI)?**
A modern Windows OS consumes roughly 4GB of RAM purely to render the Desktop Environment (wallpapers, shadows, window animations). Production Servers sit in dark, freezing data centers with no monitors attached. A GUI is a catastrophic waste of compute.
A headless Linux Server (CLI only) consumes roughly ~100MB of RAM upon boot. 99% of the hardware resources are efficiently reallocated to the actual revenue-generating workloads (Node.js runtimes, Postgres databases). Furthermore, CLI commands are natively scriptable. You cannot program a mouse to physically click "Install" on 10,000 servers. You *can* run a bash script to execute `apt-get install` across 10,000 servers in 3 seconds.

---

## Layer 3: Without vs. With Comparison (Compare)

### GUI ClickOps vs CLI Pipeline

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Sức mạnh của Dấu Gạch Đứng (`|` - Pipe) trong Linux. Chuyền dữ liệu từ lệnh này sang lệnh khác.
</details>

The terrifying power of the UNIX Pipe (`|`), chaining discrete single-purpose tools together.

**The Task:** Find out how many times the IP address "192.168.1.5" failed to login inside a massive 10GB Server Log file.

| Method | Windows GUI Approach | Linux CLI Approach |
|---|---|---|
| **Step 1** | Double-click `server.log`. Notepad crashes immediately because the file is 10GB (Out of Memory). | Run `cat server.log` (Streams the file line by line without loading it all into RAM). |
| **Step 2** | Install a specialized 3rd-party Log Viewer app. Press `Ctrl+F` and type "Failed". | Pipe the stream into `grep`: <br>`cat server.log | grep "Failed"` |
| **Step 3** | Press `Ctrl+F` again to find the specific IP. | Pipe again: <br>`... | grep "192.168.1.5"` |
| **Step 4** | Manually count the highlighted rows by scrolling. | Pipe to word-count (`wc -l`): <br>`... | wc -l` |
| **Result** | Takes 20 minutes + 3rd party software. | `grep "Failed" server.log | grep "192.168.1.5" | wc -l` <br>**Executes in 2 seconds.** |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Đọc file Log khi App sập**: Khi code Backend bị lỗi trên Server, không ai tải nguyên cái file Log 5GB về máy Mac để đọc cả. Họ sẽ dùng lệnh `tail -f server.log`. Lệnh này giúp họ nhìn trực tiếp vào đáy của file Log theo thời gian thực (giống như xem luồng chat).
- **Tìm kiếm file bị thất lạc**: Cấu hình Nginx nằm đâu nhỉ? Thay vì bấm chuột mò mẫm, gõ lệnh `find / -name "nginx.conf"`. Linux sẽ lùng sục toàn bộ hệ thống và chỉ ra đường dẫn cho bạn trong vài giây.
- **Theo dõi RAM/CPU**: Khi trang web bị chậm rề rề, Dev gõ lệnh `top` hoặc `htop`. Màn hình sẽ hiện ra y hệt Task Manager của Windows, chỉ đích danh tiến trình (Ví dụ: MySQL) đang ngốn 99% CPU để dev vào "Kill" (Giết) nó đi.

</details>

- **Real-time Log Tailing (`tail -f`)**: When a production Node.js application crashes, downloading a 5GB text file over SFTP to your local machine is impossibly slow. Engineers SSH into the server and execute `tail -f /var/log/app.log`. This hooks into the physical file stream, instantly printing any new errors to the terminal the millisecond they are written to disk.
- **Deep File System Searching (`find`)**: You need to locate a misplaced SSL certificate. You execute `find /etc -name "*.pem"`. The kernel recursively traverses the `/etc` directory tree instantly, locating the exact filepath.
- **Process Assassination (`top` & `kill`)**: A runaway infinite `while()` loop in your Python code is maxing out the CPU at 100%. Executing `htop` (The CLI Task Manager) reveals the rogue Python Process ID (PID). Executing `kill -9 1234` sends an unblockable Kernel termination signal (SIGKILL), instantly executing the rogue process and saving the server.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng phím TAB để Tự Điền (Auto-complete)**: Đừng bao giờ gõ bằng tay nguyên một đường dẫn dài như `/var/www/html/project`. Hãy gõ `/var/w` rồi BẤM PHÍM TAB, Linux sẽ tự điền chữ `ww/` cho bạn. Bấm TAB liên tục giúp bạn không bao giờ gõ sai chính tả tên File.
2. **Không lạm dụng lệnh Sudo**: `sudo` nghĩa là "Bố là Cảnh Sát Trưởng (Root)". Khi gõ `sudo`, lệnh của bạn có quyền năng tối thượng, kể cả lệnh "Xóa bay toàn bộ hệ điều hành". Chỉ dùng `sudo` khi cài đặt phần mềm. Khi chỉnh sửa file cá nhân, KHÔNG dùng `sudo`.

</details>

1. **Relentless Use of the `TAB` Key**: Never manually type a massive filepath like `/usr/local/bin/docker-compose`. Type `/usr/lo` and smash the `TAB` key. The Shell's auto-completion will instantly fill in `cal/`. Pressing TAB prevents catastrophic typo-induced bugs (e.g., executing a script in the wrong directory) and triples your typing velocity.
2. **The Principle of Least Privilege (`sudo` Discipline)**: `sudo` (SuperUser DO) elevates your prompt to the `root` kernel level. Executing scripts with `sudo` gives them omnipotent power; they can physically erase the hard drive. Junior developers often prepend `sudo` to *every* command to bypass "Permission Denied" errors. This is dangerous. Only utilize `sudo` for global installations (`apt-get`) or modifying `/etc` configurations. Never run application code (like Node.js) as root.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Thảm họa `rm -rf /`**: Lệnh `rm` (Remove) dùng để xóa. Cờ `-r` (Recursive - Xóa đệ quy mọi thứ bên trong) và `-f` (Force - Xóa ép buộc không cần hỏi lại). Gõ `rm -rf /` nghĩa là bạn đang ra lệnh xóa TOÀN BỘ Ổ CỨNG kể từ Rễ. Server bốc hơi hoàn toàn, công ty phá sản, bạn đi tù. (Nên dùng lệnh `mv` - chuyển file vào sọt rác thay vì xóa vĩnh viễn).
2. **Chỉnh sửa file mà quên Thoát (Vi/Vim)**: Mở file bằng lệnh `vi config.txt`. Sửa xong không biết làm sao để đóng màn hình lại. Bấm `Ctrl + C`, `Ctrl + Z`, `ESC` loạn xạ, màn hình vẫn đơ cứng. (Cách thoát đúng: Bấm phím `ESC`, gõ `:wq` rồi `Enter` để lưu và thoát).

</details>

1. **The `rm -rf` Catastrophe**: The `rm` command removes files. The `-r` flag traverses directories recursively. The `-f` flag bypasses all "Are you sure?" safety prompts. Executing `rm -rf /` inside a production server executes a violent wipe of the entire Hard Drive. The OS deletes itself. You must treat `rm -rf` like a loaded weapon. **Safer Alternative**: In critical environments, alias `rm` to a script that moves files to a `/trash` folder instead of permanently deleting inodes.
2. **The Vim Trap**: Junior engineers execute `vim config.conf` and fall into a panic when standard keyboard shortcuts (`Ctrl+C`, `Ctrl+S`) fail to exit the editor. They end up mashing the keyboard and corrupting the config file. **The Escape Sequence**: Press `ESC` (to ensure Command Mode), type `:wq` (Write and Quit), and strike `Enter`.

---

## Layer 7: Cheatsheet

### File System Navigation & Inspection
```bash
pwd                     # Print current directory path
ls -la                  # List ALL files (including hidden .files) in long format
cd /var/log             # Navigate to specific absolute path
cd ..                   # Navigate UP one directory level
cd ~                    # Navigate to your Home directory
```

### File Manipulation
```bash
touch newfile.txt       # Create an empty file
mkdir -p /apps/node/db  # Create a directory path (and all missing parents)
cp -r src/ dest/        # Copy a directory and all its contents recursively
mv old.txt new.txt      # Rename or Move a file
rm -rf node_modules/    # DANGEROUS: Force delete a folder and all contents
```

### Text Inspection & Grepping
```bash
cat config.json         # Print the entire file to the screen
tail -f access.log      # Stream the end of a file in real-time
head -n 20 error.log    # Print the first 20 lines of a file
grep -i "error" app.log # Search for the word "error" (case-insensitive) inside the file
```

### Process Management
```bash
top                     # View live CPU/RAM usage of all processes (press 'q' to quit)
htop                    # A much prettier, interactive version of 'top'
ps aux | grep node      # Find the specific Process ID (PID) of your Node.js app
kill -9 1234            # Forcefully execute/terminate Process ID 1234
```

### Network & Utilities
```bash
curl -I https://api.com # Fetch just the HTTP Headers of an API (great for testing)
ping 8.8.8.8            # Check if you have internet connectivity to Google
chmod +x script.sh      # Grant execution permission to a bash script
history                 # View your previous command history
```

---

## Related Topics

- Managing access to these files is covered in **[Permissions (chmod/chown)](./permissions.md)**.
- For automating commands securely via scripts, see **[Bash Scripting](./bash-scripting.md)**.
- See how Linux runs perfectly inside virtual sandboxes in **[Virtualization & Containers](../cloud-computing/virtualization-containers.md)**.
