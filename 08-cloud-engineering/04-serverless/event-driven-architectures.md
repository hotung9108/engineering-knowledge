# Event-Driven Architectures (EDA)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trái tim của Serverless. Kiến trúc Hướng sự kiện (EDA) loại bỏ việc các hệ thống phải liên tục "hỏi thăm" nhau. Thay vào đó, khi có điều gì đó xảy ra (Sự kiện), một thông báo sẽ được phát ra để tự động "đánh thức" các hệ thống khác làm việc.

</details>

> **Summary**: The beating heart of Serverless. Event-Driven Architecture (EDA) eliminates the need for systems to constantly "poll" each other. Instead, when something happens (an Event), a signal is emitted that automatically "wakes up" other systems to react.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Kiến trúc cũ (Polling)**: Bạn đặt mua một món hàng trên Shopee. Cứ mỗi 5 phút, bạn lại mở app Shopee ra kiểm tra xem hàng đã giao chưa (Tốn sức, lãng phí thời gian).
- **Kiến trúc Hướng sự kiện (EDA)**: Bạn đặt mua hàng xong thì đi ngủ. Shopee (Người phát sự kiện) cam kết: "Khi nào hàng đến trước cửa nhà bạn (Sự kiện), tôi sẽ nhắn tin (Event) vào điện thoại làm bạn tỉnh giấc (Phản ứng)". Bạn không hề lãng phí sức lực chờ đợi!

</details>

- **Legacy Architecture (Polling)**: You order a package online. Every 5 minutes, you walk to the front door, open it, and check if the package is there. (Wastes massive amounts of energy and time).
- **Event-Driven Architecture (EDA)**: You order a package and go to sleep. The Delivery Driver (Event Producer) promises: "When I drop the package at your door (The Event), I will ring your doorbell (The Signal) which will wake you up (The Reaction)." You consume zero energy while waiting!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Event-Driven Architecture (EDA)** là một mô hình thiết kế phần mềm trong đó các dịch vụ giao tiếp với nhau bằng cách phát ra (Emit) và phản hồi lại (Respond) các Sự kiện. 

**3 Thành phần chính:**
1. **Event Producers (Người tạo sự kiện)**: Bất kỳ thứ gì tạo ra sự kiện. (Ví dụ: Khách hàng click nút "Thanh toán", hoặc một file ảnh vừa được tải lên S3).
2. **Event Router (Người định tuyến)**: Trạm trung chuyển. Nó nhận sự kiện và biết chính xác phải phân phát sự kiện đó cho ai. (Ví dụ: Amazon EventBridge, SNS).
3. **Event Consumers (Người tiêu thụ)**: Các hàm hoặc dịch vụ nhận sự kiện và xử lý. (Ví dụ: Hàm AWS Lambda thức dậy để gửi email biên lai).

</details>

**Event-Driven Architecture (EDA)** is a software design pattern in which decoupled microservices asynchronously communicate by emitting and responding to Events. 
*(An Event is simply a JSON record stating that a significant change in state has occurred).*

**The 3 Core Components:**
1. **Event Producers**: The source. Anything that generates an event. (e.g., A user clicks "Checkout", an IoT sensor detects heat, or a file is uploaded to Amazon S3).
2. **Event Routers (Brokers)**: The middleman. It ingests events from Producers and filters/routes them to the correct destinations. (e.g., Amazon EventBridge, Amazon SNS).
3. **Event Consumers**: The executioners. Services that wait silently until an event arrives, wake up, process the data, and go back to sleep. (e.g., AWS Lambda).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Để tận dụng tối đa sức mạnh của Serverless (Tính tiền theo mili-giây).
Nếu bạn dùng EC2, máy chủ bật 24/7, bạn dùng kiến trúc cũ (gọi API liên tục) cũng không sao vì đằng nào bạn cũng đã trả tiền thuê nguyên tháng.

Nhưng với AWS Lambda, nếu bạn viết code bắt Lambda "ngồi chờ" 5 phút để hệ thống khác phản hồi, bạn sẽ bị AWS tính tiền cho toàn bộ 5 phút ngồi chơi đó! Rất đắt! 
EDA ra đời để đảm bảo các hệ thống Serverless chỉ chạy khi CẦN THIẾT. Cắt giảm 100% chi phí chờ đợi.

</details>

To unlock the true financial power of Serverless computing (Millisecond billing).
If you use legacy EC2 servers, they are powered on 24/7. Having Service A synchronously call Service B and wait 5 seconds for a response isn't a huge deal, because you've already paid a flat monthly fee for the EC2 server anyway.

But with AWS Lambda, you pay for *Compute Duration*. If Lambda A calls Lambda B synchronously, and Lambda B takes 5 seconds to run, Lambda A sits idle for 5 seconds waiting. **AWS will bill you for Lambda A's idle waiting time!** 
EDA exists to enforce fully Asynchronous communication. Lambda A emits an event to EventBridge and terminates immediately (0.01 seconds billed). EventBridge triggers Lambda B. You completely eliminate the cost of "waiting".

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Hai triết lý: Orchestration (Nhạc trưởng) vs Choreography (Vũ đạo)**
Trong kiến trúc sự kiện, khi bạn có 1 quy trình dài (Thanh toán -> Trừ Kho -> Giao hàng), bạn quản lý nó bằng cách nào?
- **Orchestration (AWS Step Functions)**: Có 1 "Nhạc trưởng" đứng giữa. Nhạc trưởng chỉ đạo: "Thanh toán xong rồi, Kho làm việc đi. Kho xong rồi, Giao hàng chạy đi". Dễ theo dõi quy trình, nếu lỗi thì dễ báo cáo. Nhưng Nhạc trưởng trở thành điểm nghẽn (Single point of failure).
- **Choreography (Amazon EventBridge)**: Không ai chỉ đạo ai cả (Vũ đạo tự do). Thanh toán làm xong thì hét lên "TÔI XONG". Kho nghe thấy tiếng hét, tự động chạy. Kho chạy xong hét "TÔI XONG". Giao hàng nghe thấy lại tự chạy. Các dịch vụ hoàn toàn độc lập, rất dễ mở rộng. Nhưng nếu lỗi ở giữa, cực kỳ khó tìm ra lỗi nằm ở đâu (Thiếu bức tranh tổng thể).

</details>

### Coordinating Events: Orchestration vs. Choreography
When you have a complex saga (e.g., 1. Payment -> 2. Inventory -> 3. Shipping), how do the microservices know when to execute?

- **Orchestration (AWS Step Functions)**: The "Conductor" model. A central coordinator explicitly commands each service. (e.g., "Step 1 complete. Now, Inventory Service, reduce stock!"). *Pros*: Easy to monitor, simple error handling and rollbacks. *Cons*: The coordinator is a tight coupling point.
- **Choreography (Amazon EventBridge)**: The "Dancers" model. There is no central brain. The Payment service finishes and blindly shouts to the Event Bus: "Payment Received!". The Inventory service is listening to the bus, hears the shout, and acts autonomously. *Pros*: Absolute decoupling, infinitely scalable. *Cons*: Very difficult to track the overall flow of a single transaction if a bug occurs (requires complex distributed tracing like AWS X-Ray).

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Xử lý file tự động (S3 Event Notifications)**: Khách hàng tải CMND (ảnh) lên S3. Sự kiện `s3:ObjectCreated` lập tức đánh thức Lambda. Lambda gọi AI (Amazon Textract) để đọc chữ trên CMND, sau đó lưu vào DynamoDB. Không có sự can thiệp của con người.
2. **Internet of Things (IoT)**: 1 triệu cái máy lạnh trong thành phố liên tục gửi sự kiện "Nhiệt độ hiện tại" lên AWS IoT Core. Nếu máy nào báo nhiệt độ > 40 độ C, Rule Engine kích hoạt Lambda gửi tin nhắn SMS cho thợ sửa chữa.
3. **Phân tích Real-time**: Ai đó vừa thêm hàng vào giỏ nhưng không mua. Sự kiện được ném vào EventBridge, kích hoạt luồng Marketing tự động gửi email giảm giá sau 30 phút.

**Không nên làm (Anti-patterns):**
- **Quá lạm dụng EDA cho hệ thống đơn giản**: Nếu bạn chỉ làm 1 cái blog cá nhân hoặc app CRUD cơ bản, việc áp dụng EventBridge và băm nhỏ thành 20 hàm Lambda sẽ biến hệ thống thành 1 mớ hỗn độn không thể bảo trì. Hãy dùng Monolith truyền thống.

</details>

1. **Automated Media Processing (S3 Events)**: A user uploads an HD Video to an S3 bucket. S3 natively emits an `ObjectCreated` event. This event triggers an AWS Lambda function, which triggers AWS MediaConvert to transcode the video into 480p, 720p, and 1080p formats.
2. **Internet of Things (IoT) Telemetry**: A million smart thermostats stream temperature events. If a sensor reports `Temp > 100C`, the Event Router catches it and triggers a Lambda function to page a technician via PagerDuty.
3. **Marketing Automation**: A user abandons their shopping cart. An event is fired into EventBridge. A rule routes this to a Step Functions state machine that `Waits 1 Hour`, then triggers an email via Amazon SES offering a 10% discount.

### Anti-Patterns
- **Over-engineering simple CRUD apps**: If you are building a simple internal HR tool to manage employee records, adopting a full Event-Driven Microservices architecture with EventBridge and 50 Lambdas is architectural suicide. You will suffer from "Serverless Spaghetti". Use a simple Monolith (EC2 or ECS) and a single RDS database. EDA is for complex, high-scale, decoupled business domains.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Idempotency (Tính Lũy Đẳng) - Định luật sống còn của Serverless**
Trong thế giới Đám mây, vì mạng Internet không hoàn hảo, một sự kiện CÓ THỂ bị gửi 2 lần (Retry).
Ví dụ: Sự kiện "Chuyển $100". Lambda nhận được sự kiện, chạy code trừ tiền. Nhưng lúc Lambda báo cáo "Tôi xong rồi" thì rớt mạng. AWS tưởng Lambda chưa làm, bèn gửi lại sự kiện "Chuyển $100" lần nữa. Khách bị trừ $200!
*Giải pháp*: Bạn BẮT BUỘC phải viết code Lambda có tính **Lũy Đẳng (Idempotent)**. Tức là hàm chạy 1 lần hay 100 lần với cùng 1 sự kiện thì kết quả vẫn chỉ như chạy 1 lần. 
Cách làm: Lưu `Event_ID` vào DynamoDB. Trước khi trừ tiền, kiểm tra xem `Event_ID` này đã từng xử lý chưa. Nếu có rồi thì bỏ qua!

</details>

### The Golden Rule of Serverless: Idempotency
In the Cloud, networks are inherently unreliable. Distributed systems guarantee *At-Least-Once Delivery*. This means AWS Lambda WILL occasionally receive the exact same event duplicate times.
**The Nightmare Scenario**: An event says "Charge User $100". Lambda executes it successfully, but the network drops before Lambda can send the "Success" acknowledgment back to the trigger source. The source assumes Lambda failed, so it Retries, sending the event again. The user gets charged $200!
**The Solution (Idempotency)**: You MUST write your Lambda code to be Idempotent (meaning executing it 1 time has the exact same state effect as executing it 1,000 times). 
*Implementation*: Extract the unique `event_id`. Before processing the payment, attempt to write the `event_id` into a DynamoDB table using a conditional constraint (`attribute_not_exists`). If the write fails, it means you already processed this event. Skip the payment logic and return a 200 OK.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là một "Luật" (Rule) trong EventBridge viết bằng Terraform. Nó theo dõi mọi sự kiện trên tài khoản AWS. NẾU phát hiện ra một sự kiện tên là "OrderCreated", nó sẽ bắn sự kiện đó vào một hàm Lambda.

</details>

### Creating an EventBridge Rule (Terraform)

This provisions the Event Router. It listens to the central Event Bus and filters out only the specific events our microservice cares about.

```hcl
# 1. Define the Rule (The Filter)
resource "aws_cloudwatch_event_rule" "catch_order_events" {
  name        = "capture-order-created"
  description = "Fires when the Payment Service emits an OrderCreated event"
  
  # The JSON pattern that EventBridge looks for in the massive stream of events
  event_pattern = jsonencode({
    "source": ["com.mycompany.payment"],
    "detail-type": ["OrderCreated"]
  })
}

# 2. Define the Target (Where to send the matching events)
resource "aws_cloudwatch_event_target" "send_to_lambda" {
  rule      = aws_cloudwatch_event_rule.catch_order_events.name
  target_id = "TriggerShippingLambda"
  arn       = aws_lambda_function.shipping_service.arn
}

# 3. Security: Give EventBridge permission to execute the Lambda function
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.shipping_service.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.catch_order_events.arn
}
```

---

## Related Topics

- [AWS Lambda](../02-aws-deep-dive/aws-lambda.md) — The primary consumer of events in AWS.
- [AWS SQS, SNS, EventBridge](../02-aws-deep-dive/aws-sqs-sns-eventbridge.md) — The routing services that make EDA possible.
- [Microservices Architecture](../03-cloud-architecture/microservices-architecture.md) — Why decoupling is architecturally necessary for large organizations.
