# AWS DynamoDB

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Cơ sở dữ liệu NoSQL Serverless siêu tốc của AWS. Khám phá cách DynamoDB cung cấp độ trễ phản hồi chỉ vài mili-giây (Single-digit millisecond) bất kể bạn có 1 triệu hay 1 tỷ dòng dữ liệu, miễn là bạn thiết kế Partition Key đúng cách.

</details>

> **Summary**: AWS's hyper-scale, Serverless NoSQL database. Explore how DynamoDB guarantees single-digit millisecond latency regardless of whether your table has 1 million or 1 billion rows—provided you design your Partition Keys correctly.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **RDS (SQL)**: Giống như một thư viện truyền thống. Dữ liệu được tổ chức thành các bảng Excel có cột hàng rõ ràng (Relational). Để tìm thông tin 1 học sinh, bạn phải kết nối bảng `Hoc_Sinh` với bảng `Diem_Thi` và bảng `Lop_Hoc` (Phép JOIN). Rất linh hoạt, nhưng dữ liệu càng lớn, phép JOIN càng chậm.
- **DynamoDB (NoSQL)**: Giống như một cuốn từ điển khổng lồ. Bạn chỉ có 2 thứ: "Từ khóa" (Key) và "Định nghĩa" (Value). Để tìm thông tin 1 học sinh, bạn phải biết chính xác Mã Học Sinh (Key). Lật cuốn từ điển ra, tất cả thông tin điểm số, lớp học đã được "gom chung" (Denormalized) vào cùng một trang định nghĩa đó. Bạn tìm thấy nó trong chớp mắt (vài mili-giây). KHÔNG CÓ PHÉP JOIN nào được phép diễn ra!

</details>

- **RDS (SQL)**: Like a highly organized, relational filing cabinet. Data is strictly separated into distinct tables. To get a complete profile of a User, you must computationally stitch together the `Users` table, the `Orders` table, and the `Payments` table using complex `JOIN` operations. Highly flexible for querying, but as tables grow to billions of rows, `JOIN`s become violently slow.
- **DynamoDB (NoSQL)**: Like a gargantuan Dictionary (Key-Value store). You have a "Word" (Partition Key) and the "Definition" (Item data). To get a User's profile, you *must* know their exact User ID. You open the dictionary straight to that ID. All their order and payment data has already been pre-calculated and stuffed into that exact same dictionary entry (Denormalization). You retrieve it in 3 milliseconds. There are NO `JOIN` operations allowed.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Amazon DynamoDB** là một cơ sở dữ liệu NoSQL dạng Key-Value và Document do AWS quản lý hoàn toàn (Serverless). Nó được thiết kế để chạy mọi ứng dụng ở mọi quy mô một cách nhất quán (Độ trễ luôn dưới 10 mili-giây).

**Thành phần cốt lõi:**
- **Table (Bảng)**: Nơi chứa dữ liệu. Không cần phải khai báo trước các cột (Schema-less), ngoại trừ Khóa chính.
- **Item (Dòng/Bản ghi)**: Mỗi Item có thể có cấu trúc dữ liệu JSON khác nhau. Tối đa 400KB mỗi Item.
- **Partition Key (PK)**: Khóa chính bắt buộc. Dùng để băm (Hash) và rải dữ liệu ra nhiều server vật lý khác nhau.
- **Sort Key (SK)**: (Tùy chọn) Khóa sắp xếp. Dùng để gom nhóm các Item có cùng PK và sắp xếp chúng.

</details>

**Amazon DynamoDB** is a fully managed, Serverless, Key-Value and Document NoSQL database. It is explicitly engineered to run high-performance applications at virtually infinite scale, guaranteeing single-digit millisecond latency regardless of data volume.

**Core Components:**
- **Table**: A collection of data. It is Schema-less, meaning you do not define columns (attributes) upfront, except for the Primary Key.
- **Item**: A single record in a table (similar to a row in SQL). Items are typically represented as JSON documents. Hard limit: 400KB max per Item.
- **Partition Key (PK)**: The mandatory primary key. DynamoDB runs it through an internal hash function to determine exactly which physical server (Partition) the Item will be stored on.
- **Sort Key (SK)**: (Optional) A secondary key. Items that share the same Partition Key are stored physically close together, sorted sequentially by this Sort Key.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Năm 2004, Amazon.com gặp khủng hoảng vào dịp mua sắm nghỉ lễ. Cơ sở dữ liệu Oracle khổng lồ của họ bị quá tải vì không thể chịu nổi hàng chục ngàn lượt mua hàng mỗi giây. CSDL SQL truyền thống rất khó mở rộng ngang (Scale Out - thêm máy chủ), nó chỉ có thể mở rộng dọc (Scale Up - mua máy to hơn), và Amazon đã mua cái máy to nhất thế giới rồi!

Họ nhận ra 90% các câu query trên Amazon.com chỉ đơn giản là: "Lấy Giỏ hàng của User X ra đây". Không cần JOIN phức tạp. Do đó, AWS đã phát minh ra DynamoDB: Chấp nhận bỏ đi các tính năng SQL phức tạp để đổi lấy khả năng mở rộng ngang (Scale Out) vô hạn. Nếu bạn cần xử lý 1 triệu giao dịch mỗi giây, DynamoDB tự động rải nó ra 10,000 server vật lý chạy song song trong tíc tắc.

</details>

In 2004, Amazon.com experienced a catastrophic database meltdown during the holiday shopping season. Their monolithic Oracle databases could not handle the sheer volume of transactions. Traditional SQL databases are notoriously difficult to Scale Out (adding more servers horizontally); they mostly Scale Up (buying a bigger server), and Amazon had already bought the biggest servers on Earth!

Amazon engineers analyzed their traffic and realized 90% of their database queries were brutally simple: "Fetch the Shopping Cart for User_ID = 123". They didn't need complex `JOIN`s or relational constraints. 
AWS invented DynamoDB based on this premise: Drop the heavy relational SQL features in exchange for infinite Horizontal Scalability. If your app spikes to 1,000,000 reads per second, DynamoDB automatically shuffles your data across 10,000 hidden physical partitions, maintaining 3ms response times without breaking a sweat.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Mô hình tính phí (Pricing Models)**
- **RDS (Provisioned)**: Bạn thuê một máy tính 4 CPU, 16GB RAM chạy 24/7. Dù không ai xài, bạn vẫn phải trả $100/tháng. Nếu traffic quá lớn, máy bị sập.
- **DynamoDB On-Demand (Serverless)**: Bạn không thuê máy chủ nào cả. Bạn thiết lập bàn giá "On-Demand". Bạn chỉ bị tính tiền dựa trên SỐ LƯỢNG lệnh Đọc/Ghi. 1 triệu lệnh Ghi tốn $1.25. Không có ai dùng = Trả $0. Rất tuyệt vời cho Startup và Lambda.

</details>

### Relational Database (RDS) vs NoSQL (DynamoDB)

| Feature | Amazon RDS (SQL) | Amazon DynamoDB (NoSQL) |
|---|---|---|
| **Data Structure** | Normalized (Spread across tables) | Denormalized (Nested JSON documents) |
| **Flexibility** | Schema is rigid. Easy to write ad-hoc queries. | Schema-less. BUT queries must be known/planned upfront. |
| **Scalability** | Hard to scale writes. (Scale Up) | Infinite scaling. (Scale Out automatically) |
| **Performance** | Slows down as tables get massive (due to JOINs). | Consistent 3ms latency whether 1GB or 500TB. |
| **Billing** | Pay for the server's uptime (Per Hour). | Pay per Read/Write request (On-Demand). |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Giỏ hàng E-commerce & Session State**: Cần tốc độ đọc/ghi cực nhanh (vài mili-giây) và chịu được tải biến động lớn.
2. **Serverless Apps (Kết hợp với Lambda)**: Vì Lambda không giữ kết nối mạng (Connection Pool), nếu 10,000 hàm Lambda gọi RDS cùng lúc, RDS sẽ sập mạng. DynamoDB giao tiếp qua giao thức HTTP API, nên 100,000 Lambda gọi DynamoDB cùng lúc cũng không hề hấn gì.
3. **Bảng xếp hạng Game (Gaming Leaderboards)**: Lưu điểm số của hàng chục triệu người chơi và cập nhật theo thời gian thực (Real-time).

**Không nên làm (Anti-patterns):**
- **Dùng DynamoDB cho Báo cáo (Analytics/OLAP)**: Giám đốc muốn tính tổng doanh thu nhóm theo từng tháng của tất cả khách hàng. DynamoDB KHÔNG CÓ hàm `SUM()`, `GROUP BY` hay `JOIN`. Bạn sẽ phải quét (Scan) toàn bộ bảng, tải hàng GB dữ liệu về code Python để tự cộng lại. Tiền phí (Read Capacity Units) sẽ làm bạn phá sản! Dùng Redshift hoặc Athena cho việc này.

</details>

1. **Shopping Carts & Session Management**: Requires blisteringly fast read/write speeds with massive, unpredictable spikes (e.g., Flash Sales).
2. **Serverless Architectures (The Perfect Pair with Lambda)**: AWS Lambda functions spin up rapidly. A spike of 10,000 concurrent Lambdas will violently crash a traditional RDS database by exhausting its TCP connection pool limit. DynamoDB uses stateless HTTP connections; it swallows 100,000 concurrent Lambda requests effortlessly.
3. **Real-time Bidding & Gaming Leaderboards**: Storing and updating state for millions of simultaneous mobile game players with zero lag.

### Anti-Patterns
- **Analytics & Reporting (OLAP)**: The CEO wants a report: "Sum all revenue grouped by user demographic for the last year". DynamoDB does NOT support `JOIN`, `SUM()`, or `GROUP BY` at the database engine level. To do this, you must run a `Scan` operation, forcing DynamoDB to read every single row in the database. AWS charges you for *Data Read*. Scanning a 1TB table for a simple report will instantly cost you hundreds of dollars in Read Capacity Units (RCUs). Use Amazon Redshift for Analytics.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Nghệ thuật chọn Khóa phân vùng (Partition Key - PK)**
Nếu PK thiết kế sai, DynamoDB sẽ trở thành thảm họa (Hot Partition).
- *Sai lầm*: Chọn PK là `NgàyTháng` (ví dụ: `2024-10-31`). Tất cả 1 triệu giao dịch của ngày hôm nay sẽ dồn vào đúng 1 cái server vật lý của AWS. Server đó bị quá tải (Throttled), trong khi 99 server khác ngồi chơi.
- *Chuẩn*: Chọn PK là `CustomerID` (Mã khách hàng) hoặc một UUID ngẫu nhiên. Dữ liệu sẽ được "băm" và phân tán đều đặn ra hàng ngàn server vật lý.

**2. Global Secondary Index (GSI)**
DynamoDB chỉ cho phép tìm kiếm cực nhanh dựa trên PK (giống như tra từ điển). Nhưng nếu PK của bạn là `CustomerID`, và bạn muốn tìm kiếm theo `Email` thì sao? Bạn phải lập một **GSI** (Một bảng con phụ trợ, nơi AWS tự động chép dữ liệu sang và lấy `Email` làm PK). Bạn sẽ phải trả gấp đôi tiền lưu trữ và tiền ghi, đổi lại tốc độ truy vấn luôn là mili-giây.

**3. Single-Table Design**
Đây là kỹ thuật "hắc ám" (Advanced) nhất của DynamoDB. Thay vì tạo bảng `Users` và bảng `Orders`, chuyên gia AWS khuyên nên nhồi TẤT CẢ mọi thứ vào đúng 1 Table duy nhất! Dùng các khái niệm nạp chồng PK và SK (ví dụ: PK=`USER#123`, SK=`PROFILE` hoặc SK=`ORDER#999`). Cực kỳ khó thiết kế ban đầu, nhưng hiệu năng đạt mức thần thánh.

</details>

### 1. The Art of Partition Key Design (Avoiding Hot Partitions)
If you choose the wrong Partition Key (PK), DynamoDB fails.
- **The Mistake**: Using a `Date` (e.g., `2024-10-31`) as the PK for an orders table. All 1,000,000 orders placed today will mathematically hash to the *exact same underlying physical server*. That single server gets crushed by I/O (a "Hot Partition") and DynamoDB throttles your app, while the other 99 servers sit completely idle.
- **The Solution**: Use a high-cardinality ID (like `CustomerID`, `DeviceID`, or a random `UUID`). The hash function scatters the data evenly across hundreds of physical servers, allowing limitless parallel scaling.

### 2. Global Secondary Indexes (GSI)
You can only execute a lightning-fast `Query` if you know the exact Partition Key. If your PK is `UserID`, but you suddenly need to search for a user by their `EmailAddress`, you are stuck. You cannot search by Email without doing a full table `Scan` (Expensive!).
**The Fix**: Create a GSI. AWS will silently maintain a shadow-copy of your table in the background, but reorganize the data so `EmailAddress` is the new Partition Key. *Trade-off*: You pay double the storage and write costs for the convenience of fast reads.

### 3. Single-Table Design (Advanced)
Traditional developers create a `Users` table and an `Orders` table. In advanced DynamoDB architecture, you put *everything* into exactly ONE single table. By cleverly overloading the PK and SK (e.g., PK=`USER#123`, SK=`PROFILE` vs PK=`USER#123`, SK=`ORDER#999`), you can retrieve a User and all their Orders in a single API call without joining. It is notoriously difficult to model, but yields god-like performance.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là cách sử dụng thư viện `boto3` trong Python để gọi DynamoDB (Thường được đặt trong AWS Lambda). Lưu ý: Chúng ta dùng lệnh `get_item` và `put_item`, không viết lệnh SQL.

</details>

### Interacting with DynamoDB (Python / Boto3)

Because it is a NoSQL database, you do not send SQL query strings (`SELECT * FROM...`). You use the AWS SDK to make REST API calls directly to the DynamoDB service endpoint.

```python
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource (Uses IAM Roles for security, no passwords needed)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ECommerce-SingleTable')

def get_user_profile(user_id):
    """
    O(1) Time Complexity lookup. Lightning fast (3ms latency).
    """
    try:
        response = table.get_item(
            Key={
                'PK': f'USER#{user_id}',
                'SK': 'PROFILE'
            }
        )
        return response.get('Item')
    except ClientError as e:
        print(f"Error fetching user: {e}")
        return None

def create_order(user_id, order_id, total_amount):
    """
    Writes a new JSON document into the table. 
    Notice how it goes into the SAME table, just with a different Sort Key prefix.
    """
    try:
        table.put_item(
            Item={
                'PK': f'USER#{user_id}',
                'SK': f'ORDER#{order_id}',
                'EntityType': 'Order',
                'TotalAmount': total_amount,
                'Status': 'PENDING'
            }
        )
        print("Order saved successfully.")
    except ClientError as e:
        print(f"Error saving order: {e}")
```

---

## Related Topics

- [AWS Lambda](./aws-lambda.md) — The Serverless Compute that perfectly pairs with Serverless DynamoDB.
- [AWS RDS](./aws-rds-and-aurora.md) — The Relational alternative when you desperately need complex SQL `JOIN`s.
- [Data Modeling](../../06-data-engineering/01-data-fundamentals/data-modeling-and-dimensional-design.md) — Traditional relational modeling is the exact opposite of DynamoDB's NoSQL Single-Table Design.
