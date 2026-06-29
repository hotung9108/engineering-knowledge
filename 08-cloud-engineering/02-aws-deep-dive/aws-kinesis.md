# AWS Kinesis (Data Streaming)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Công cụ xử lý luồng dữ liệu thời gian thực (Real-time). Tìm hiểu cách Kinesis hấp thụ hàng triệu sự kiện mỗi giây (như GPS từ xe Uber, log truy cập web), và cách nó giữ dữ liệu an toàn để xử lý thay vì làm ngập lụt Database.

</details>

> **Summary**: The real-time data streaming engine of AWS. Learn how Kinesis ingests millions of events per second (e.g., GPS coordinates from Uber cars, clickstreams), and how it buffers the data to protect your Database from being completely flooded.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn là một thủ kho (Database). Bình thường, mỗi giờ có 1 chiếc xe tải chở hàng đến, bạn kiểm đếm rồi ghi vào sổ. Rất nhàn rỗi.
Đột nhiên, công ty chạy quảng cáo. Có **10,000 chiếc xe tải** lao đến cửa kho CÙNG MỘT LÚC. Bạn không thể ghi chép kịp, kho bị ùn tắc, toàn bộ hệ thống sụp đổ!

**Kinesis** giống như một Bãi Đỗ Xe Chờ khổng lồ (Buffer) có băng chuyền tự động.
Thay vì 10,000 xe tải lao thẳng vào kho, chúng sẽ ném hàng lên băng chuyền Kinesis. Băng chuyền này di chuyển liên tục, chứa được hàng triệu món hàng và giữ chúng ở đó trong 24 giờ. Bạn (Thủ kho) cứ bình tĩnh, lấy từng món hàng từ băng chuyền xuống để ghi chép với tốc độ của riêng mình. Băng chuyền sẽ giữ hàng hóa an toàn, không món nào bị rớt (mất dữ liệu).

</details>

You are a Warehouse Clerk (The Database). Normally, 1 delivery truck arrives every hour. You check the cargo and write it in the ledger. Very relaxing.
Suddenly, your company goes viral on TikTok. **10,000 trucks** rush to the warehouse door AT THE EXACT SAME SECOND. You cannot physically write that fast. The trucks crash into each other, and the entire system collapses!

**AWS Kinesis** is a massive, automated Conveyor Belt (Buffer/Queue) outside the warehouse.
Instead of 10,000 trucks rushing the clerk, they dump all their packages onto the Kinesis conveyor belt. This belt can hold millions of packages simultaneously and will safely store them there for 24 hours. You (the Clerk) can simply pick packages off the end of the conveyor belt at your own natural, steady pace. The conveyor belt absorbs the massive spike, ensuring the Database is never overwhelmed and zero data is lost.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon Kinesis** là một nền tảng thu thập, xử lý và phân tích dữ liệu luồng (streaming data) theo thời gian thực. Đối thủ mã nguồn mở lớn nhất của nó là **Apache Kafka**.

**Kinesis có 4 dịch vụ con:**
1. **Kinesis Data Streams (KDS)**: Băng chuyền chính. Nhận dữ liệu cực nhanh, lưu tạm 1-365 ngày. Đòi hỏi bạn phải tự viết code (Lambda/EC2) để lấy dữ liệu ra xử lý.
2. **Kinesis Data Firehose**: Giống như ống cứu hỏa. Không cần viết code, nó tự động hút dữ liệu từ băng chuyền, đóng gói lại, rồi xả thẳng vào S3, Redshift hoặc Elasticsearch.
3. **Kinesis Data Analytics**: Cho phép bạn viết mã SQL để phân tích dữ liệu NGAY LÚC NÓ ĐANG CHẠY trên băng chuyền (chưa hề chạm ổ cứng).
4. **Kinesis Video Streams**: Truyền phát luồng video an toàn từ camera an ninh.

</details>

**Amazon Kinesis** is a platform to collect, process, and analyze real-time streaming data so you can get timely insights and react quickly to new information. Its primary open-source competitor is **Apache Kafka**.

**The Kinesis Suite:**
1. **Kinesis Data Streams (KDS)**: The highly customizable, core conveyor belt. It ingests data rapidly and retains it (from 1 to 365 days). You must write custom code (Lambda/EC2) to consume and process this data.
2. **Kinesis Data Firehose**: The delivery mechanism. Fully managed. It requires no code. It automatically reads data from the stream, batches it, compresses it, and dumps it directly into S3, Redshift, or Elasticsearch.
3. **Kinesis Data Analytics**: Allows you to run standard SQL queries on the data stream IN-FLIGHT (while the data is still moving on the conveyor belt, before it is even saved to a database).
4. **Kinesis Video Streams**: For securely streaming live video from connected devices (IoT cameras) to AWS for analytics.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trong thế giới Big Data, có những loại dữ liệu được sinh ra liên tục từng giây (Streaming Data). 
Ví dụ: 
- Bạn có ứng dụng gọi xe (như Grab). Hàng triệu tài xế gửi tọa độ GPS lên server mỗi 3 giây.
- Ứng dụng theo dõi nhịp tim của bệnh viện.

Nếu bạn cắm API trực tiếp vào RDS Database, hàng triệu lệnh `INSERT` mỗi giây sẽ nướng chín Database trong nháy mắt. Hơn nữa, việc này quá đắt đỏ.
Kinesis ra đời để hấp thụ cú sốc này (Decoupling/Buffering). Kinesis sinh ra để nhận hàng trăm ngàn tin nhắn/giây với giá cực rẻ. Nó cho phép các hệ thống chạy ở các tốc độ khác nhau có thể giao tiếp với nhau mà không làm sập nhau.

</details>

In the Big Data world, some data is generated continuously, 24/7, at massive volumes (Streaming Data).
Examples:
- A ride-hailing app (Uber). Millions of drivers send their exact GPS coordinates to the server every 3 seconds.
- IoT sensors on a jet engine streaming temperature data.
- Clickstreams (tracking every button click on a massive e-commerce site).

If you wire your API directly to a standard RDS Database, millions of concurrent `INSERT` statements per second will melt the database instantly.
Kinesis exists to absorb the shock (Buffering/Decoupling). It is engineered specifically to ingest hundreds of thousands of small records per second cheaply. It decouples the speed of the Producers (Mobile apps) from the speed of the Consumers (The Database), preventing catastrophic failures.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Kiến trúc Xử lý Hàng loạt (Batch) so với Thời gian thực (Streaming)**
- **Batch Processing (Ngày xưa)**: Dữ liệu click chuột của khách hàng được gom vào 1 file CSV. Cuối ngày lúc 2h sáng, chạy Spark quét file CSV để xem hôm nay ai bỏ giỏ hàng. Sáng hôm sau mới gửi email mời khách mua lại. Quá muộn, khách đã mua ở chỗ khác!
- **Stream Processing (Kinesis)**: Khách vừa tắt trình duyệt (bỏ giỏ hàng), sự kiện lập tức trôi trên băng chuyền Kinesis. Chỉ 50 mili-giây sau, hàm Lambda bắt được sự kiện, lập tức gửi ngay cho khách 1 cái email Voucher giảm giá 10% để chốt đơn ngay lập tức! (Phản ứng Real-time).

</details>

### Batch Processing vs. Stream Processing

- **Traditional Batch Processing**: User clickstream data is saved to a local CSV file. At 2:00 AM, a nightly Cron job (Batch) processes the massive CSV to find users who abandoned their shopping carts. At 9:00 AM the next day, an email is sent to the user. *Result: Too late, the user already bought the item from a competitor.*
- **Stream Processing (Kinesis)**: The exact millisecond the user closes their browser (cart abandoned), the event is fired into Kinesis. Within 50 milliseconds, an AWS Lambda function reads the stream, detects the abandonment, and immediately fires a 10% Discount Voucher email to the user. *Result: Instant engagement and a recovered sale (Real-time reactivity).*

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Phân tích Log/Clickstream**: Thu thập mọi cú click chuột của người dùng trên web, đưa qua Kinesis Firehose xả vào S3 Data Lake để làm báo cáo BI.
2. **Theo dõi gian lận (Fraud Detection)**: Dữ liệu quẹt thẻ tín dụng liên tục chảy qua Kinesis. Dùng Kinesis Data Analytics chạy thuật toán. Nếu phát hiện 1 thẻ vừa quẹt ở Hà Nội, 3 giây sau lại quẹt ở Mỹ -> Cảnh báo gian lận ngay lập tức và khóa thẻ, trước khi tiền bị chuyển đi.
3. **Hấp thụ sốc (Buffer)**: Bất cứ khi nào hệ thống có một lượng dữ liệu ghi khổng lồ và đột ngột mà Database không kịp xử lý, hãy chặn Kinesis ở giữa.

**Nên dùng Kafka hay Kinesis?**
- **Apache Kafka**: Nhanh hơn, cấu hình cực kỳ linh hoạt, hệ sinh thái siêu lớn. Nhưng cài đặt và bảo trì (Vá lỗi OS, sửa máy chết) là ác mộng tột cùng cho team DevOps.
- **Kinesis**: Kém linh hoạt hơn Kafka một chút, nhưng là Serverless hoàn toàn của AWS. Bấm 1 nút là có. Phù hợp cho 90% các công ty muốn tập trung vào viết code thay vì vận hành cụm Kafka.

</details>

1. **Log & Clickstream Ingestion**: Collecting every mouse click, scroll, and page view globally, feeding it into Kinesis Firehose, which automatically batches the data into 100MB Parquet files and drops them into S3 for cost-effective Data Warehousing.
2. **Real-time Fraud Detection**: Credit card transaction events stream continuously. Using Kinesis Data Analytics (or Flink), you analyze the stream in real-time. If a credit card is swiped in London and then swiped in Tokyo 3 seconds later, the stream processor detects the impossible velocity and immediately blocks the transaction before it clears.
3. **Database Shock Absorber (Buffering)**: Any time you have massive, unpredictable `INSERT` spikes (e.g., voting for a reality TV show finale), place Kinesis in front of the database.

### The Big Debate: Apache Kafka vs. Amazon Kinesis
- **Apache Kafka**: The undisputed king of throughput and flexibility. Massive open-source ecosystem. *Drawback*: Managing a Kafka cluster (Zookeeper, patching VMs, rebalancing partitions when nodes die) is an absolute operational nightmare.
- **Amazon Kinesis**: Slightly less flexible, but it is a fully managed AWS service. No servers to patch. It integrates natively with IAM and Lambda out of the box. Highly recommended unless you explicitly need Kafka's raw power.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Khái niệm Shard (Làn đường)**
Kinesis Data Streams không phải 1 ống nước khổng lồ. Nó được tạo thành từ nhiều ống nhỏ gọi là **Shards** (Làn đường). 
- 1 Shard hỗ trợ Ghi 1MB/s (hoặc 1000 tin nhắn/s) và Đọc 2MB/s.
- Nếu ứng dụng của bạn cần ghi 10MB/s, bạn phải cấu hình luồng Kinesis có 10 Shards. Càng nhiều Shards, phí duy trì mỗi giờ càng cao. Bạn phải liên tục theo dõi để tăng/giảm số Shard (Resharding) cho phù hợp với tải để tiết kiệm tiền.

**2. Kinesis Data Firehose vs Data Streams**
- **Data Streams**: Bạn phải TỰ VIẾT CODE (Consumer) để đọc dữ liệu từ băng chuyền. Dữ liệu đọc xong VẪN CÒN trên băng chuyền cho ứng dụng khác đọc tiếp (Multiple Consumers).
- **Firehose**: Nó giống con robot hốt rác tự động. Cứ 1 phút nó lại gom hết dữ liệu trên băng chuyền, nén lại thành file zip rồi ném vào S3. Bạn không phải viết 1 dòng code nào. Rất tuyệt vời để làm Data Lake.

</details>

### 1. Understanding Shards (Provisioned Throughput)
A Kinesis Data Stream is not a single giant pipe. It is comprised of multiple parallel lanes called **Shards**.
- **1 Shard** provides a strict capacity: **1 MB/second (or 1,000 records) of Write throughput**, and **2 MB/second of Read throughput**.
- If your application pushes 10 MB/second during peak hours, you MUST manually provision the stream to have at least 10 Shards. If you only have 5 Shards, AWS will throw `ProvisionedThroughputExceededException` errors and drop your data. 
- *Pro Tip*: AWS now offers **Kinesis On-Demand**, which automatically manages shards for you, but costs slightly more per gigabyte.

### 2. Streams vs. Firehose (Crucial Difference)
- **Kinesis Data Streams (KDS)**: You must write a custom Consumer application (e.g., an AWS Lambda function or EC2 script) to actively pull data off the stream. Once read, the data *stays on the stream* for its retention period, meaning 5 different apps can read the exact same data stream simultaneously.
- **Kinesis Data Firehose**: A fully managed delivery mechanism. It requires ZERO custom code. It automatically reads the stream, buffers the data (e.g., for 60 seconds or 5MB), optionally converts the JSON into Parquet, and dumps the file directly into an S3 bucket or Redshift. The ultimate "No-Code" ingestion tool for Data Lakes.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là cách dùng thư viện `boto3` trong Python để đẩy 1 dữ liệu (Ví dụ: Một đơn hàng vừa được chốt) vào Kinesis Data Streams.

</details>

### Pushing Data to Kinesis (Python Producer)

This is how a backend web server (the Producer) throws a record onto the Kinesis conveyor belt.

```python
import boto3
import json
import time

# Initialize Kinesis client (Make sure IAM Role has kinesis:PutRecord)
kinesis_client = boto3.client('kinesis', region_name='us-east-1')
STREAM_NAME = 'ecommerce-clickstream'

def send_event_to_kinesis(user_id, action, product_id):
    """
    Pushes a real-time event to the Kinesis Stream.
    """
    event_payload = {
        'user_id': user_id,
        'action': action,          # e.g., 'ADD_TO_CART'
        'product_id': product_id,
        'timestamp': int(time.time())
    }
    
    # Kinesis requires the payload to be a string/bytes
    data = json.dumps(event_payload)
    
    # The PartitionKey determines WHICH Shard this data goes to.
    # By using user_id, we guarantee all actions by the same user go to the same Shard in order.
    try:
        response = kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=data,
            PartitionKey=str(user_id) 
        )
        print(f"Record successfully pushed to Shard: {response['ShardId']}")
        
    except Exception as e:
        print(f"Failed to push record: {e}")

# Example Usage
# send_event_to_kinesis(1234, 'ADD_TO_CART', 9988)
```

---

## Related Topics

- [AWS Lambda](./aws-lambda.md) — The most common "Consumer" that reads and processes data off the Kinesis stream.
- [AWS S3](./aws-s3.md) — The final resting place for data flushed out by Kinesis Firehose.
- [SQS, SNS & EventBridge](./aws-sqs-sns-eventbridge.md) — Comparing Streaming (Kinesis) vs Standard Queuing (SQS).
