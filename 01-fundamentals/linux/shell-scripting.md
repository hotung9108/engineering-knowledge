# Shell Scripting (Bash)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Thay vì gõ tay từng lệnh Linux rời rạc (Ví dụ: 1 lệnh tạo thư mục, 1 lệnh tải file, 1 lệnh giải nén), **Shell Scripting** cho phép bạn gom hàng tá lệnh vào một file kịch bản (Script file đuôi `.sh`). Sau đó, bạn chỉ cần bấm chạy 1 lần, máy tính sẽ tự động làm hết mọi việc từ A đến Z. Đây là vũ khí tối thượng của DevOps dùng để cài đặt hàng ngàn máy chủ, tự động sao lưu dữ liệu mỗi đêm, và xây dựng các đường ống CI/CD.

</details>

> **Summary**: Interacting with the Linux CLI via single manual commands is highly inefficient for repetitive tasks. **Shell Scripting** (specifically **Bash**) is a powerful programming paradigm that allows engineers to string together hundreds of Linux system commands, control flows (if/else), and loops into an executable text file (`.sh`). It is the supreme automation weapon utilized by SysAdmins and DevOps Engineers to rapidly provision servers, orchestrate midnight database backups, and build CI/CD pipelines without manual human intervention.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn phải làm bánh Pizza mỗi ngày.
- **Không có Script (Làm bằng tay)**: Mỗi sáng thức dậy, bạn phải lấy giấy bút ra nhớ lại: Bước 1: Lấy bột. Bước 2: Nhào bột. Bước 3: Cho phô mai. Bước 4: Bật lò. Bạn phải tự làm từng bước, rất tốn thời gian và dễ quên bước 3.
- **Có Script (Dùng Robot)**: Bạn viết tất cả các bước đó vào một tờ giấy (Script file). Bạn đưa tờ giấy cho một con Robot (Bash). Từ giờ trở đi, mỗi sáng bạn chỉ cần gõ đúng 1 lệnh: `./lam-pizza.sh`. Con Robot sẽ đọc tờ giấy và tự động làm bánh giống hệt nhau 1000 lần không bao giờ sai sót.

</details>

Imagine you are tasked with baking a complex Cake every single morning.
- **Manual Execution (No Scripts)**: Every morning, you must actively remember the recipe. You manually grab the flour (Command 1), you manually crack the eggs (Command 2), you manually stir (Command 3). It requires immense mental energy, and on day 15, you forget to add sugar (Human Error).
- **Shell Scripting (The Automation Robot)**: You write the entire recipe down on a piece of paper (The `.sh` Script file). You hand the paper to a robotic chef (The Bash Interpreter). From that day forward, you simply press a single green button: `./bake-cake.sh`. The robot reads the paper and perfectly executes the recipe at superhuman speed. It will bake 10,000 cakes flawlessly without ever forgetting the sugar.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Bash (Bourne Again Shell)**: Là ngôn ngữ kịch bản mặc định trên 99% các máy chủ Linux (Ubuntu, CentOS). File script thường có đuôi `.sh`.
**2. Shebang (`#!/bin/bash`)**: Là dòng chữ phép thuật luôn NẰM Ở DÒNG ĐẦU TIÊN của file script. Nó báo cho hệ điều hành biết: "Ê, hãy dùng phần mềm Bash để đọc và chạy cái file này nhé".
**3. Programming Constructs**: Dù là ngôn ngữ viết script, Bash vẫn có đầy đủ Biến (Variables), Vòng lặp (`for`, `while`), Câu lệnh rẽ nhánh (`if`, `case`), và Hàm (Functions) như các ngôn ngữ lập trình Python/Java.

</details>

**1. Bash (Bourne Again Shell)**: The overwhelmingly dominant, default command-line interpreter and scripting language across almost all UNIX/Linux distributions (Ubuntu, Debian, RHEL). Script files conventionally utilize the `.sh` extension.
**2. The Shebang (`#!/bin/bash`)**: The absolute first line of any shell script. It is an executive directive to the Operating System kernel. It explicitly states: "When executing this text file, pass it through the `/bin/bash` interpreter."
**3. Programming Constructs**: Despite being a "Scripting" language designed to manipulate files, Bash possesses Turing-complete programming features: Variable assignments, robust Conditional logic (`if/elif/else`), Iterators (`for/while` loops), and modular Functions.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Vấn đề Tự động hóa**: Bạn vừa thuê một máy chủ Linux trống trơn. Để chạy được Web, bạn phải cài Node.js, cài Nginx, cấu hình Firewall, tạo User mới. Phải gõ 50 câu lệnh. Bạn làm thành công. Nhưng ngày mai công ty mở rộng, sếp yêu cầu bạn mua thêm 20 máy chủ nữa và cài y hệt. Bạn sẽ gõ 1,000 câu lệnh bằng tay? Chắc chắn bạn sẽ gõ sai và làm sập Server.

**Sức mạnh của Shell Script**: Bạn lưu 50 câu lệnh đó vào file `setup.sh`. Bắn file đó qua 20 con máy chủ và gõ lệnh chạy. Xong! 20 máy chủ được cài đặt hoàn hảo, y hệt nhau tới từng byte, hoàn thành trong 3 phút. Kỹ sư DevOps giỏi là người có thể ngủ ngon vì mọi việc đã có Script tự chạy.

</details>

**The Scalability of Infrastructure Automation**: You just provisioned a naked Ubuntu Server. To prepare it for production, you must update packages, install Docker, configure `ufw` firewall rules, and mount external SSD volumes. This takes 50 manual terminal commands. You succeed. Tomorrow, the CEO demands you provision 100 more identical servers. Typing 5,000 commands manually guarantees catastrophic human error and architectural configuration drift (Server 42 misses a firewall rule and gets hacked).

**The Shell Script Paradigm**: You encode those 50 commands into a single `provision.sh` artifact. You distribute it via SSH to all 100 servers and execute it simultaneously. The entire 100-node cluster configures itself identically, flawlessly, in under 60 seconds. Shell scripting is the absolute genesis of "Infrastructure as Code."

---

## Layer 3: Without vs. With Comparison (Compare)

### Repetitive Task Execution

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc sao lưu (Backup) Database mỗi đêm.
</details>

Comparing the operational overhead of a nightly Database Backup task.

| Phase | Without Shell Script (Manual SysAdmin) | With Shell Script (Cronjob) |
|---|---|---|
| **Execution** | SysAdmin sets an alarm for 2:00 AM. Wakes up, SSH into server. | A `cron` daemon triggers the script automatically at 2:00 AM. |
| **Commands** | Types `pg_dump ...`, waits 5 mins. Types `tar -czvf ...`, waits. | Script executes commands instantly in sequence via `&&`. |
| **Transfer** | Manually runs `scp` to copy the backup file to an S3 bucket. | Script runs `aws s3 cp` automatically. |
| **Notification** | Goes back to sleep. Forgets to tell the team. | Script evaluates `$?`. If successful, triggers a Slack API Webhook (`curl`) saying "Backup Complete." |
| **Error Rate** | High. Typo in the date format overwrites yesterday's backup. | Zero. Variables dynamically generate `backup_2023-10-24.tar.gz`. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Bootstrapping (Khởi tạo Server)**: Viết script để tự động tải các phần mềm cần thiết khi Server vừa mới mọc lên (User-data trong AWS EC2).
- **Cron Jobs (Tác vụ định kỳ)**: Hệ thống Linux có một phần mềm tên là `cron`. Bạn bảo nó: "Cứ 12h đêm hàng ngày, hãy chạy file `backup.sh` cho tao". Thế là bạn đi ngủ, dữ liệu vẫn được sao lưu an toàn.
- **CI/CD Pipelines (Github Actions / Jenkins)**: Bản chất của hệ thống đẩy code tự động chính là chạy các Script. Lệnh "Build Code", "Chạy Test", "Deploy lên Server" thực chất đều là các file Bash script chạy ngầm dưới lưới.

</details>

- **Server Bootstrapping (Init Scripts)**: Cloud Providers (AWS/GCP) allow you to inject `user-data` scripts. When an EC2 instance dynamically scales up, it executes a Bash script on boot to install dependencies and pull the latest application code, joining the cluster automatically without human interaction.
- **Cron Jobs (Scheduled Automation)**: The Linux `cron` daemon is scheduled to execute `.sh` files at specific intervals. Used relentlessly for Log Rotation (compressing and deleting old logs to prevent disk full errors), Database Dumps, and generating nightly financial reports.
- **CI/CD Pipeline Glue (GitHub Actions / GitLab CI)**: The entire CI/CD industry is essentially a fancy GUI wrapped around remote Bash execution. A YAML pipeline file explicitly executes sequential Bash commands (`npm run build`, `docker build`, `kubectl apply`) to orchestrate the entire deployment lifecycle.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Luôn bắt đầu Script với `set -e` (Fail Fast)**: Mặc định của Bash rất ngu ngốc: Lệnh 1 bị lỗi, nó vẫn cắm đầu chạy tiếp Lệnh 2. Nếu Lệnh 1 là "Tạo thư mục", Lệnh 2 là "Copy file vào thư mục", việc chạy Lệnh 2 sẽ gây ra thảm họa. Gõ `set -e` ở đầu script sẽ bắt Bash DỪNG NGAY LẬP TỨC nếu có bất kỳ lệnh nào bị lỗi (Lỗi Khác 0).
2. **Dùng ngoặc kép cho Biến (Double Quotes)**: Khai báo biến `FILE="a b.txt"`. Khi gõ lệnh xóa `rm $FILE`. Bash sẽ hiểu lầm là xóa 2 file tên `a` và `b.txt` (Do dấu cách). BẮT BUỘC phải bọc biến trong ngoặc kép: `rm "$FILE"` để an toàn.

</details>

1. **Mandatory Fail-Fast (`set -e`)**: Bash's default behavior is highly dangerous: if a command fails, it ignores the error and blindly executes the next line. If Line 1 is `cd /backup_dir` (which fails because the directory doesn't exist), and Line 2 is `rm -rf *`, the script will execute the deletion in your *current* directory, destroying your server. **Rule**: Always start scripts with `set -euo pipefail`. `set -e` forces the script to abort instantly if any command returns a non-zero exit code.
2. **Aggressive Variable Quoting**: Spaces in filenames are the nemesis of Bash. If `FILENAME="my document.txt"`, executing `cat $FILENAME` expands into `cat my document.txt`, attempting to open two nonexistent files. You must rigorously wrap variable expansions in double quotes: `cat "$FILENAME"`.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sửa Script bằng Windows (Lỗi Ký tự Xuống dòng `\r`)**: Bạn hì hục code Bash trên máy Windows bằng Notepad. Xong ném lên Server Linux chạy. Linux báo "Command not found". Nguyên nhân: Windows dùng ký tự `\r\n` để xuống dòng, còn Linux dùng `\n`. Linux không hiểu ký tự `\r` rác rưởi của Windows. Giải pháp: Dùng công cụ `dos2unix` để gọt giũa lại file trước khi chạy.
2. **Lạm dụng Bash cho Logic phức tạp**: Bash rất giỏi trong việc điều khiển File và Server. Nhưng nó CỰC KỲ DỞ trong việc xử lý JSON, tính toán mảng phức tạp, hay gọi API mạng. Cú pháp `if else` của Bash là một thảm họa khó đọc. Nếu Script của bạn dài quá 200 dòng và xử lý logic nghiệp vụ, HÃY DỪNG LẠI và chuyển sang viết bằng Python!

</details>

1. **The Windows Line-Ending Nightmare (`\r\n` vs `\n`)**: A developer writes a `.sh` script on a Windows machine using Notepad, commits it to Git, and pulls it onto an Ubuntu server. When executed, it fails with bizarre `bash: \r: command not found` errors. Windows terminates lines with Carriage Return + Line Feed (CRLF), while UNIX exclusively expects Line Feed (LF). The Linux interpreter chokes on the invisible `\r` character. **Fix**: Use VSCode to explicitly save the file with LF line endings, or run `dos2unix script.sh` on the server.
2. **Bash Masquerading as a General Purpose Language**: Bash excels at executing binaries and piping file streams. It is architecturally terrible at parsing complex JSON payloads, manipulating multidimensional arrays, or executing complex string regex. Its syntax is incredibly brittle. **Rule of Thumb**: If your Bash script exceeds 150 lines, or you find yourself fighting its syntax to parse JSON (`jq` helps, but is clunky), rewrite the entire script in **Python**. Python scripts natively support `os.system()` and possess vastly superior standard libraries.

---

## Layer 7: Cheatsheet

### The Foundation
```bash
#!/bin/bash
# This is a comment. The line above is the mandatory shebang.

# Fail Fast Rules (Highly Recommended at the top of every script)
set -euo pipefail
```

### Variables
```bash
# NO spaces around the equals sign!
NAME="Alice"
AGE=25

# Reading a variable requires the $ and Quotes
echo "Hello, my name is $NAME"

# Capturing the output of a command into a variable
CURRENT_DIR=$(pwd)
TODAY=$(date +%F)
```

### If / Else Conditions
```bash
# Notice the strict spaces inside the brackets [ ]
FILE="config.json"

if [ -f "$FILE" ]; then
    echo "$FILE exists. Proceeding..."
else
    echo "Error: $FILE is missing!"
    exit 1  # Exit the script with an error code
fi

# Checking numbers
if [ "$AGE" -gt 18 ]; then
    echo "Adult"
fi
```

### Loops
```bash
# For Loop (Iterating over a list)
for color in Red Green Blue; do
    echo "I like $color"
done

# Iterating over files in a directory
for file in *.txt; do
    echo "Processing $file..."
done

# While Loop (Running until a condition changes)
COUNTER=1
while [ $COUNTER -le 5 ]; do
    echo "Count: $COUNTER"
    ((COUNTER++)) # Increment math
done
```

### Command Line Arguments
```bash
# When running: ./script.sh apple banana
echo "Script Name: $0"       # Outputs: ./script.sh
echo "First Argument: $1"    # Outputs: apple
echo "Second Argument: $2"   # Outputs: banana
echo "Total Arguments: $#"   # Outputs: 2
```

### Useful Tricks
```bash
# Read User Input interactively
read -p "Enter your name: " USER_NAME
echo "Welcome, $USER_NAME"

# Suppress output (throw command junk into the void)
grep "ERROR" log.txt > /dev/null 2>&1

# Check the Exit Status of the last command
ls /fake/directory
if [ $? -ne 0 ]; then
    echo "The previous command failed!"
fi
```

---

## Related Topics

- For the fundamental commands executed within scripts, see **[Essential Commands](./essential-commands.md)**.
- For managing execution rights of scripts, review **[Permissions](./permissions.md)**.
- Bash scripts are the backbone of **[CI/CD Concepts](../sdlc/ci-cd-concepts.md)**.
