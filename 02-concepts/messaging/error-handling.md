# Messaging Error Handling

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Chuyện gì xảy ra khi bạn nhận được một bức thư nhưng bạn không biết đọc chữ? Bạn vứt nó đi hay bạn gõ cửa hỏi bưu tá? Trong Messaging, lỗi là điều chắc chắn xảy ra. Có thể do Database sập tạm thời (Lỗi mạng), hoặc do tin nhắn bị sai cấu trúc JSON (Lỗi logic). Nếu không xử lý đúng cách, một tin nhắn lỗi có thể làm kẹt toàn bộ hệ thống. **Dead Letter Queue (DLQ)** và **Retry Backoff** là các chiến thuật cứu cánh bắt buộc phải có để hệ thống Message Queue không bị sụp đổ.

</details>

> **Summary**: In asynchronous message-driven architectures, processing failures are an inevitability, not a possibility. Failures broadly categorize into Transient Errors (temporary network glitches, database timeouts) and Persistent Errors (malformed JSON payloads, unhandled Null Pointer Exceptions). If an application naively crashes upon reading a bad message, the Broker will aggressively redeliver it, creating an infinite loop of death (a "Poison Pill"). **Messaging Error Handling** relies on robust defensive patterns—specifically **Exponential Backoff Retries** and **Dead Letter Queues (DLQ)**—to preserve pipeline throughput and isolate toxic data for manual engineering intervention.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn làm việc ở dây chuyền phân loại táo.
1. **Lỗi Tạm thời (Transient Error)**: Băng chuyền chạy bình thường, nhưng bạn lỡ tay làm rơi quả táo xuống đất. Bạn không vứt quả táo đó đi, bạn nhặt lên và làm lại (Retry). Nhưng bạn không nhặt liên tục, bạn đợi 5 giây cho bớt mỏi tay rồi mới nhặt (Backoff).
2. **Lỗi Vĩnh viễn (Poison Pill)**: Quả táo bị thối hoắc, dòi bọ bò lúc nhúc. Bạn có nhặt lên đặt xuống 100 lần thì nó vẫn thối, không thể đóng gói được. Hơn nữa, nó làm kẹt cả dây chuyền, hàng ngàn quả táo ngon phía sau không trôi qua được. Bạn BẮT BUỘC phải nhặt quả táo thối đó, quăng vào một cái "Sọt rác đặc biệt" (DLQ). Dây chuyền tiếp tục chạy bình thường. Cuối ngày, quản lý sẽ ra Sọt rác kiểm tra tại sao táo lại thối.

</details>

Imagine working on a factory conveyor belt sorting apples.
1. **Transient Error (Network Timeout)**: An apple comes down the belt, but your machine temporarily loses power for 2 seconds. The apple isn't bad; your machine just failed. You push the apple slightly back up the belt to try again in a few seconds (Retry).
2. **Persistent Error (The Poison Pill)**: A completely rotten, radioactive apple comes down the belt. Your sorting machine crashes trying to scan it. If the machine simply resets and tries to scan the *same* rotten apple again, it will crash again. It loops infinitely. The thousands of perfect apples behind it are entirely blocked. You MUST mechanically eject this rotten apple into a separate "Hazmat Bin" (The Dead Letter Queue). The belt resumes moving. At the end of the shift, an engineer opens the Hazmat Bin to investigate what went wrong.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Cơ chế Retry (Thử lại)**: Khi Consumer đọc tin nhắn bị lỗi, nó gửi tín hiệu `NACK` (Negative Acknowledge) cho Broker. Broker sẽ đưa tin nhắn đó trở lại hàng đợi để Consumer thử đọc lại lần nữa.
**2. Backoff (Dãn cách thời gian)**: Nếu DB đang bị quá tải, việc Retry liên tục 100 lần/giây chỉ làm DB chết nhanh hơn. Phải dùng Exponential Backoff (Thử lại sau 1s, rồi 2s, 4s, 8s...) để hệ thống có thời gian thở.
**3. DLQ (Dead Letter Queue - Hàng đợi thư chết)**: Là một Queue dự phòng. Khi một tin nhắn bị Retry quá số lần cho phép (Ví dụ: 5 lần) mà vẫn thất bại, Broker sẽ tự động ném nó từ Queue chính sang DLQ.

</details>

**1. The Retry Mechanism (NACK)**: When a Consumer pulls a message and the processing fails (e.g., an exception is thrown), the Consumer must explicitly send a `NACK` (Negative Acknowledgment) to the Broker. The Broker re-queues the message, making it visible for consumption again.
**2. Exponential Backoff**: Immediate, rapid-fire retries are destructive. If a downstream Database is overwhelmed, hammering it with 1,000 retries per second will cause a complete outage. Backoff algorithms mandate that the system waits exponentially longer between each retry (e.g., wait 2s, then 4s, then 8s, up to a maximum cap).
**3. DLQ (Dead Letter Queue)**: A secondary, isolated Message Queue natively supported by Brokers (AWS SQS, RabbitMQ). A routing policy is configured: "If a message receives 5 `NACK`s, stop retrying. Automatically route it to the `DLQ`."

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có DLQ, hệ thống Message Queue của bạn sớm muộn gì cũng sập.
Giả sử có 1 triệu tin nhắn đang xếp hàng. Tin nhắn số 1 bị thiếu field `email`, khiến code báo lỗi Null.
Consumer đọc tin nhắn 1 $\rightarrow$ Lỗi $\rightarrow$ Trả về Broker $\rightarrow$ Broker gửi lại $\rightarrow$ Lỗi tiếp.
Vòng lặp vô hạn này diễn ra với tốc độ hàng nghìn lần/giây, đốt cháy toàn bộ CPU của Server. 999.999 tin nhắn hoàn toàn hợp lệ xếp phía sau không bao giờ được xử lý. Kẻ thù này có tên là **Poison Pill (Viên thuốc độc)**.
DLQ sinh ra để cách ly "Viên thuốc độc" này ra khỏi hệ thống khỏe mạnh.

</details>

Without a Dead Letter Queue, an asynchronous architecture is a ticking time bomb.
Consider a queue holding 1,000,000 pending Orders. Order #1 contains a malformed JSON payload (`"price": "NaN"`).
The Consumer pulls Order #1. The JSON parser throws a Fatal Exception. The Consumer `NACK`s the message. The Broker instantly re-delivers it. The Consumer crashes again.
This infinite loop executes thousands of times per second. CPU utilization pegs at 100%. The remaining 999,999 perfectly valid Orders sitting behind Order #1 are permanently blocked. The system suffers total paralysis. This is the **Poison Pill Anti-Pattern**.
DLQs exist solely to quarantine these toxic payloads, preserving the throughput of the primary pipeline.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh hệ thống Xử lý Thanh toán khi có và không có DLQ.
</details>

Visualizing the structural defense mechanisms of a DLQ.

| Component | Without DLQ (Vulnerable) | With Exponential Backoff + DLQ (Robust) |
|---|---|---|
| **Error Type** | API is down (Transient) | API is down (Transient) |
| **Retry Rate** | Retries 10,000 times in 1 second. | Retries at 2s, 4s, 8s, 16s, 32s. |
| **Result** | Triggers DDoS protection, API bans you. | Gracefully waits for API to recover. |
| **Error Type** | Corrupted JSON (Persistent) | Corrupted JSON (Persistent) |
| **Queue State**| Poison Pill loop. Queue blocked forever. | After 5 retries, message routed to DLQ. |
| **Result** | **System Outage**. Operations Halt. | **System Stable**. Engineers fix JSON in DLQ manually. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Cảnh báo (Alerting)**: Bất cứ khi nào có 1 tin nhắn rơi vào DLQ, hệ thống phải tự động bắn tin nhắn báo động qua Slack hoặc PagerDuty cho đội Dev. DLQ không phải là bãi rác để bỏ quên, nó là phòng cấp cứu.
- **Phân tích lỗi (Root Cause Analysis)**: Đội Dev mở DLQ ra, xem nội dung tin nhắn bị lỗi là gì. Nhờ có cục Data bị lỗi đó, họ dễ dàng tìm ra Bug trong code, sửa Bug, deploy code mới, rồi bấm nút **"Re-drive" (Gửi lại)** toàn bộ thư trong DLQ về Queue chính để hệ thống chạy tiếp.
- **Jitter (Nhiễu)**: Khi thiết lập Backoff, đừng set thời gian tĩnh (Ví dụ: Tất cả cùng chờ đúng 5 giây). Nếu 1000 tin nhắn cùng chờ 5 giây rồi cùng Retry 1 lúc $\rightarrow$ Server sập. Hãy cộng thêm 1 khoảng thời gian ngẫu nhiên (Ví dụ: `5s + Random(1,2)s`) để giải tán đám đông. Đây gọi là Jitter.

</details>

- **Active Alerting (Slack/PagerDuty)**: A Dead Letter Queue is not a graveyard; it is an ICU. If a message hits the DLQ, it signifies a critical, unhandled edge-case in production code. The architecture MUST include a CloudWatch (or equivalent) alarm monitoring the DLQ depth. If `DLQ_Length > 0`, fire a high-priority alert to the Engineering Slack channel immediately.
- **The Redrive Workflow (Bug Fixing)**: The immense power of the DLQ is that no data is lost. A developer investigates the DLQ, identifies the poison JSON, realizes a `null` check is missing in the code, and pushes a hotfix to production. Once the new code is deployed, the developer executes a **Redrive**—moving all messages from the DLQ back into the Main Queue. The fixed code processes them perfectly.
- **Implementing "Jitter"**: When using Exponential Backoff during a massive outage, thousands of messages might fail simultaneously. If they all back off by exactly 5.0 seconds, they will all retry at exactly the same millisecond, triggering a massive DDoSing "Thundering Herd" on your Database. **Fix**: Add **Jitter** (cryptographic randomness) to the retry calculation (e.g., `WaitTime = 5s + Random(0.0, 1.5s)`). This elegantly diffuses the traffic spike.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Phân biệt rạch ròi 2 loại Lỗi**: 
   - Lỗi do Mạng/DB (Lỗi 5xx): Hãy đưa vào chế độ Retry (Vì chờ một tí mạng sẽ có lại). 
   - Lỗi do JSON sai cấu trúc, Validate thất bại (Lỗi 4xx): **CẤM RETRY**. Trăm năm sau nó vẫn lỗi. Hãy bắt `Exception` và đá nó thẳng vào DLQ ngay lập tức, không tốn thời gian chạy Retry 5 lần.
2. **Luôn lưu lại Lịch sử Lỗi (Stack Trace)**: Khi ném tin nhắn vào DLQ, đừng chỉ vứt mỗi cái thân tin nhắn. Hãy gắn thêm siêu dữ liệu (Metadata) vào Header của tin nhắn: Lỗi xảy ra lúc mấy giờ? Dòng code nào gây lỗi? (In ra nguyên cái Stack Trace). Việc này giúp Dev debug nhanh gấp 10 lần.

</details>

1. **Differentiate Transient vs. Persistent Errors**: Blindly retrying every error is an anti-pattern. If the database returns a `503 Service Unavailable`, you should absolutely execute an Exponential Backoff retry. However, if the JSON parser throws a `ValidationException` because a required `user_id` is missing (a `400 Bad Request` equivalent), retrying is mathematically futile. The payload will never magically fix itself. **Fix**: Catch the specific Validation Exceptions in your code and manually force an immediate rejection/route to the DLQ, bypassing the 5-retry loop to save compute resources.
2. **Inject Diagnostic Metadata into DLQ Headers**: When a message is banished to the DLQ, the raw payload alone is often insufficient for debugging. "Why did this fail?" Developers waste hours guessing. **Fix**: Before explicitly sending a message to the DLQ, the Consumer should mutate the message's standard Headers, injecting critical telemetry: `X-Failure-Reason: NullPointerException`, `X-Failed-At: 2024-01-01T12:00Z`, and the truncated Stack Trace.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **DLQ bị lãng quên (The Silent Graveyard)**: Team setup DLQ xong nhưng KHÔNG CÀI ĐẶT CẢNH BÁO. 6 tháng sau, hệ thống mất hàng ngàn đơn hàng. Sếp hỏi "Đơn hàng đâu?". Mở DLQ ra thấy 50.000 tin nhắn nằm chết vùi trong đó từ nửa năm nay không ai hay biết. 
   - *Luật*: Có DLQ thì bắt buộc phải có hệ thống Monitor/Alerting đi kèm.
2. **Lỗi Re-drive mù quáng**: Đội Dev thấy DLQ có 100 tin nhắn, lười không thèm đọc log xem lỗi gì, cứ thế bấm nút đẩy lại vào Main Queue hi vọng "lần này nó sẽ chạy được". Kết quả: 100 tin nhắn lại đập vào Queue chính, lại làm hệ thống nghẽn, tốn CPU Retry 5 lần, rồi lại rớt xuống DLQ. 

</details>

1. **The Silent Graveyard (Unmonitored DLQs)**: Architects proudly design a DLQ but completely fail to connect it to Datadog/PagerDuty. The pipeline fails silently. 6 months later, Customer Support is overwhelmed with "Missing Order" tickets. The engineering team checks the DLQ and discovers 50,000 orphaned, financially critical messages quietly decaying. **Rule**: An unmonitored DLQ is arguably worse than no DLQ, because it creates a false sense of security.
2. **Blind Redriving**: Treating the DLQ like a slot machine. A Junior Developer sees 500 messages in the DLQ, assumes it was a temporary network glitch, and clicks the "Redrive to Main Queue" button without inspecting the logs. Because the error was actually a persistent Null Pointer Exception, all 500 messages flood the main queue, consume massive CPU cycles executing 5 futile retries each, trigger false alerts, and eventually cascade right back into the DLQ. **Rule**: Never redrive a DLQ until the exact Root Cause has been identified and mitigated.

---

## Related Topics

- For a high-level theoretical overview, see **[Messaging Overview](./overview.md)**.
- To understand why a message goes missing, study **[Delivery Guarantees](./delivery-guarantees.md)**.
- For managing retries properly, see **[Resilience / Retry](../resilience/retry.md)**.
