# Storage Systems: HDD vs SSD vs NVMe

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Dữ liệu trên RAM sẽ bốc hơi khi mất điện, nên ta phải lưu chúng vĩnh viễn xuống Ổ cứng (Storage). Hiểu bản chất vật lý của ổ cứng từ đĩa từ (HDD) cồng kềnh, đến chip nhớ (SSD SATA) và công nghệ siêu tốc (NVMe PCIe) giúp kỹ sư tối ưu hóa được tốc độ đọc/ghi dữ liệu của Database (Disk I/O).

</details>

> **Summary**: RAM is volatile memory; data vanishes upon power loss. Permanent persistence mandates writing to non-volatile Storage drives. Understanding the physical evolution from mechanical magnetic platters (HDD) to flash memory chips (SSD SATA) and direct-to-CPU lanes (NVMe PCIe) is crucial for Database Engineers optimizing Disk I/O performance.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn (CPU) đang ở trong phòng và cần tìm một cuốn sách trong thư viện (Ổ cứng).
1. **HDD (Ổ cứng cơ)**: Giống như bạn thuê một thủ thư đạp xe bò đi tìm sách. Chậm chạp, ồn ào, nếu xe bò xóc nảy có thể làm rơi hỏng sách.
2. **SSD SATA**: Giống như bạn gọi một chiếc xe hơi chạy ra thư viện lấy sách. Nhanh hơn gấp 5 lần xe bò, nhưng xe hơi vẫn phải đi qua đường hẻm chật chội (Cáp SATA) vốn được thiết kế cho xe bò.
3. **NVMe PCIe**: Giống như bạn xây một đường hầm siêu tốc (PCIe) nối thẳng từ phòng bạn đến thư viện, dùng tàu điện ngầm chạy với tốc độ ánh sáng. Nhanh gấp 30 lần xe hơi!

</details>

Imagine the CPU is requesting a specific book from the massive Archives (Storage).
1. **HDD (Hard Disk Drive)**: Like hiring a librarian on a horse-drawn carriage to fetch the book. It's mechanical, slow, noisy, and if the carriage hits a bump, the book might be destroyed.
2. **SSD (Solid State Drive via SATA)**: Upgrading to a sports car. It's 5x faster, but the car is forced to drive on a dirt road (the legacy SATA cable interface) that was originally built for the horse carriage.
3. **NVMe (Non-Volatile Memory Express via PCIe)**: Building a high-speed hyperloop tunnel (PCIe lanes) directly from the CPU to the archives. It's up to 30x faster than the sports car because it bypasses the legacy dirt roads entirely.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. HDD (Hard Disk Drive)**: Lưu trữ bằng các đĩa từ tính xoay vật lý (5400-7200 vòng/phút). Có một cây kim cơ học chạy ra chạy vào để đọc dữ liệu.
**2. SSD (Solid State Drive)**: Không có bộ phận chuyển động. Dùng chip nhớ NAND Flash. Thường kết nối qua cổng SATA 3 (Giới hạn tốc độ ở mức ~550 MB/s).
**3. NVMe (Non-Volatile Memory Express)**: Vẫn là SSD (dùng chip NAND), nhưng cắm thẳng vào cổng PCIe của bo mạch chủ, kết nối trực tiếp với CPU. Tốc độ đạt 7,000 - 14,000 MB/s.

</details>

**1. HDD (Hard Disk Drive)**: Mechanical storage utilizing rotating magnetic platters (typically 5400 or 7200 RPM) and a physical actuator arm that sweeps across the disk to read/write data.
**2. SSD (Solid State Drive - SATA)**: Solid-state storage lacking moving parts, relying on NAND flash memory chips. Traditionally connects via the legacy SATA III interface, bottlenecking speeds at a theoretical maximum of 600 MB/s.
**3. NVMe (Non-Volatile Memory Express)**: Also an SSD (uses NAND flash), but it ditches the SATA interface. It connects directly to the motherboard's PCIe lanes, establishing a direct, multi-lane data highway to the CPU. Modern PCIe Gen 5 NVMe drives achieve blinding speeds of up to 14,000 MB/s.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **HDD tồn tại vì Rẻ**: Công nghệ từ tính rất rẻ để sản xuất với dung lượng khổng lồ (20TB+). Phù hợp để làm kho lưu trữ lạnh (Cold Storage) như lưu camera an ninh, backup dữ liệu rác.
- **SSD ra đời vì IOPS (Input/Output Operations Per Second)**: Cây kim của HDD mất quá nhiều thời gian để di chuyển vật lý đến vị trí ghi dữ liệu (Seek time). SSD đọc bằng điện tử nên thời gian truy xuất gần như bằng 0.
- **NVMe ra đời vì Cổ chai SATA**: Khi chip SSD ngày càng nhanh, cái dây cáp SATA cũ kỹ trở thành nút thắt cổ chai kìm hãm tốc độ. NVMe vứt bỏ cáp SATA, cắm thẳng vào khe PCIe.

</details>

- **HDDs exist for Cost-Effective Capacity**: Magnetic platter tech is cheap to manufacture at massive scales (20TB+). It dominates "Cold Storage" (e.g., CCTV archives, daily database backups, AWS S3 Glacier).
- **SSDs were invented to solve IOPS (Input/Output Operations Per Second)**: The mechanical actuator arm in an HDD introduces horrific latency ("Seek Time") when reading fragmented files. SSDs use electronic signaling, dropping seek times to near-zero, revolutionizing OS boot times.
- **NVMe was invented to bypass the SATA Bottleneck**: As NAND flash chips became exponentially faster, the legacy SATA interface (designed in the 2000s for mechanical HDDs) strangled their performance. NVMe was engineered from scratch for flash memory, utilizing massively parallel PCIe lanes.

---

## Layer 3: Without vs. With Comparison (Compare)

### Performance Comparison Matrix

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Thông số **IOPS** là quan trọng nhất đối với Database. HDD chỉ chịu được 100 giao dịch/giây, trong khi NVMe gánh được hàng triệu giao dịch.

</details>

The **IOPS** metric is the absolute most critical factor for Database Engineering.

| Metric | HDD (7200 RPM) | SSD (SATA III) | NVMe (PCIe Gen 4) |
|---|---|---|---|
| **Seq. Read/Write** | ~150 MB/s | ~550 MB/s | ~7,000 MB/s |
| **Random Read IOPS** | 70 - 100 IOPS | ~100,000 IOPS | ~1,000,000+ IOPS |
| **Latency (Seek Time)** | 5,000 - 10,000 $\mu$s | 100 $\mu$s | 10 - 20 $\mu$s |
| **Moving Parts** | Yes (High failure rate) | No | No |
| **Primary Use Case** | Cold Backups, Archives | General Computing | Database Clusters, AI |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **AWS RDS / Database Servers**: Luôn luôn bắt buộc phải dùng NVMe SSD (ví dụ: Amazon EBS `io2` Block Express) để đạt được IOPS cực cao cho các câu lệnh SQL Random Access.
- **Hệ thống Streaming (Netflix/YouTube)**: Dùng SSD cho các phim đang "hot" (Hot Storage) và dùng HDD dung lượng cực lớn cho các phim cũ thập niên 90 ít ai xem (Cold Storage) để tiết kiệm chi phí.

</details>

- **Relational Database Servers (PostgreSQL, MySQL)**: High-traffic databases mandate NVMe SSDs (e.g., AWS EBS `io2` or `gp3` volumes). Databases perform aggressive, fragmented Random Reads/Writes. Running a production database on an HDD will instantly bottleneck the entire architecture at 100 IOPS.
- **Tiered Storage Architecture (Netflix/YouTube)**: Tech giants employ a multi-tier strategy. "Hot" content (a newly released trending series) is cached on blazing-fast NVMe servers physically close to users. "Cold" content (a documentary from 1995 watched once a month) is relegated to massive, cheap HDD server farms.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Ghi theo tuần tự (Sequential I/O)**: Nếu phải dùng ổ cứng chậm (HDD) hoặc thậm chí SSD, hãy cố gắng thiết kế cấu trúc dữ liệu Ghi Tuần Tự (Append-only) thay vì Ghi Ngẫu Nhiên (Random Write). Đó là lý do Kafka siêu nhanh dù lưu dữ liệu xuống ổ cứng cơ, vì nó chỉ ghi nối đuôi (Append log).
2. **Theo dõi "TBW" (Terabytes Written)**: SSD không bất tử. Các ô nhớ NAND sẽ chết sau một số lượng lần ghi nhất định. Trên server DB ghi xóa liên tục, SSD có thể "đột tử". Phải dùng hệ thống RAID để dự phòng mất mát.

</details>

1. **Architect for Sequential I/O**: Whether targeting HDD or SSD, Sequential disk access is universally faster than Random access. This is the engineering secret behind **Apache Kafka**. Kafka achieves memory-like speed while persisting to cheap HDDs because it strictly utilizes Sequential Append-Only Logs, completely bypassing the catastrophic Random Seek Time penalties.
2. **Monitor TBW (Terabytes Written) Lifespans**: Unlike HDDs which theoretically last until mechanical failure, SSDs have a finite lifespan. Every NAND flash cell degrades slightly upon writing. High-throughput database write-heavy workloads will eventually burn out Enterprise SSDs. Always utilize **RAID configurations** and actively monitor SMART drive health metrics.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Mua RAM xịn nhưng dùng Ổ cứng dỏm cho Database**: Server có 256GB RAM nhưng CSDL lại lưu trên ổ SATA HDD. Ngay khi dữ liệu vượt quá dung lượng RAM Cache, hệ thống sẽ rơi vào trạng thái "Disk Thrashing", CPU treo 100% chỉ để đợi ổ đĩa quay kim.
2. **Không dự phòng mất dữ liệu ổ cứng**: Mọi ổ cứng đều SẼ hỏng, vấn đề chỉ là khi nào. Chạy Database production trên một ổ đĩa duy nhất (Single node) là tự sát.

</details>

1. **Disk Thrashing via Bad Provisioning**: Provisioning a server with 256GB of RAM but storing the PostgreSQL database on standard HDD volumes. Once the database exceeds the RAM cache buffer and is forced to perform disk reads, the IOPS bottleneck crashes the application.
2. **Single Point of Failure (SPOF)**: Assuming SSDs are invincible. SSD controllers can silently fail instantly without the mechanical "clicking" warning signs of an HDD. Running un-replicated stateful services on single drives is architectural negligence.

---

## Related Topics

- How Operating Systems schedule these disk reads is covered in **[I/O Models](../operating-system/io-models.md)**.
- See how disk persistence works in databases in **[SQL Fundamentals](../database/sql-fundamentals.md)**.
