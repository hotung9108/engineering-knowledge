# Data Contracts & Quality

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Giải quyết cơn ác mộng lớn nhất của Data Engineer: "Rác vào, Rác ra" (Garbage In, Garbage Out). Tìm hiểu cách áp dụng Hợp đồng Dữ liệu (Data Contracts), kiểm thử chất lượng dữ liệu tự động (Data Quality checks) và giới thiệu mô hình phân tán Data Mesh.

</details>

> **Summary**: Solving the biggest nightmare of a Data Engineer: "Garbage In, Garbage Out". Learn how to enforce Data Contracts, implement automated Data Quality checks, and an introduction to the decentralized Data Mesh paradigm.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Hợp đồng Dữ liệu (Data Contract)**: Tưởng tượng bạn là đầu bếp (Data Engineer) cần thịt gà để nấu phở. Nhà cung cấp (Software Engineer) thường gửi thịt gà cho bạn. Một ngày nọ, họ tự ý đổi sang gửi thịt vịt mà không thèm báo trước. Nồi phở của bạn hỏng bét, khách hàng chửi bạn! 
  **Data Contract** là một bản hợp đồng ký kết có tính pháp lý: "Nhà cung cấp PHẢI gửi đúng thịt gà, nếu gửi sai sẽ bị từ chối ngay tại cửa ngõ". Nhờ vậy, nồi phở của bạn luôn an toàn.
- **Data Quality**: Bạn có một cái máy dò kim loại trước khi cho nguyên liệu vào nồi. Kiểm tra xem thịt có bị hôi không? Rau có bị thối không? (Check Null, Check Duplicates). Nếu có, báo động đỏ ngay!

</details>

- **Data Contracts**: Imagine you are a chef (Data Engineer) who needs chicken to make soup. Your supplier (Software Engineer) usually delivers chicken. One day, they quietly decide to send duck instead without telling you. Your soup is ruined, and the customers yell at *you*! 
  A **Data Contract** is a legally binding agreement: "The supplier MUST send chicken. If they send duck, the delivery truck is automatically rejected at the gate." This keeps your soup safe.
- **Data Quality**: You have a metal detector and a freshness scanner at the kitchen door. You check if the meat is spoiled or if the vegetables are rotten (Checking for Nulls, Duplicates, Out-of-bounds values). If a bad ingredient is detected, a red alarm goes off immediately!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Data Contract**: Là một bản đặc tả kỹ thuật (thường viết bằng YAML hoặc JSON Schema) định nghĩa rõ ràng cấu trúc, kiểu dữ liệu, và ngữ nghĩa của một luồng dữ liệu do Team Backend (Producer) tạo ra. Cấu trúc này bị ép buộc cứng nhắc (enforced) tại tầng phát sự kiện (ví dụ: Kafka Schema Registry).
- **Data Quality (DQ)**: Là quá trình viết các bộ Test tự động cho Dữ liệu (giống như Unit Test cho Code). Ví dụ: `assert column_age > 0 AND column_age < 150`.
- **Data Mesh**: Là mô hình tổ chức phân tán. Thay vì một team Data Engineer trung tâm phải lo dọn rác cho toàn công ty, Data Mesh ép team Backend nào đẻ ra dữ liệu thì team đó phải tự chịu trách nhiệm về chất lượng và cung cấp nó như một "Sản phẩm" (Data as a Product).

**Phân loại:**
- **Loại**: Quản trị Dữ liệu (Data Governance).
- **Công cụ**: Confluent Schema Registry (Contracts), Great Expectations / dbt Tests (Data Quality).

</details>

- **Data Contract**: A technical specification (often written in YAML or JSON Schema) that clearly defines the structure, data types, and semantics of a data stream produced by a Backend Team (Producer). This schema is strictly enforced at the event-emission layer (e.g., using Kafka Schema Registry).
- **Data Quality (DQ)**: The practice of writing automated tests for Data (just like Unit Tests for Code). Example: `assert column_age > 0 AND column_age < 150`.
- **Data Mesh**: A decentralized organizational paradigm. Instead of a single central Data Engineering team cleaning up everyone's mess, Data Mesh forces the Backend team that generates the data to be fully responsible for its quality, treating it as a "Product" (Data as a Product).

### Classification
- **Type**: Data Governance.
- **Tools**: Confluent Schema Registry (Contracts), Great Expectations / dbt Tests (Data Quality).

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Nỗi đau truyền thống:**
Team Backend thường không quan tâm đến dữ liệu phân tích. Một ngày đẹp trời, Backend Dev đổi tên cột `user_id` thành `customer_id` trong Database MySQL để code cho đẹp. Code Backend vẫn chạy tốt. Nhưng khi Pipeline hút dữ liệu này về Data Warehouse, Pipeline bị gãy vỡ (Crash) vì không tìm thấy cột `user_id`. Báo cáo tài chính buổi sáng bị trống trơn. Giám đốc nổi giận gọi cho team Data, trong khi lỗi là do team Backend!

**Giải pháp:**
Data Contracts ra đời để giải quyết tận gốc xung đột này. Khi có Contract, nếu Backend Dev đổi `user_id` thành `customer_id`, ngay lập tức lệnh Push code của Backend (CI/CD) sẽ báo lỗi đỏ chót: "Vi phạm Hợp đồng Dữ liệu". Lỗi được chặn từ trứng nước!

</details>

**The Traditional Pain Point:**
Backend Software Engineers typically don't care about analytics. One sunny day, a Backend Dev renames the `user_id` column to `customer_id` in the MySQL Database to make the code look cleaner. The backend code works perfectly. But when the overnight Pipeline extracts this data to the Data Warehouse, the pipeline crashes because `user_id` is missing. The morning financial dashboard is empty. The CEO yells at the Data Engineering team, even though the Backend team caused the breakage!

**The Solution:**
Data Contracts were invented to solve this exact friction. With a Contract in place, if the Backend Dev renames `user_id` to `customer_id`, their own CI/CD code push will instantly fail with a glaring red error: "Data Contract Violation". The breakage is caught at the source, before it ever reaches production!

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

- **Không có Data Contract**: Dữ liệu gửi qua Kafka dưới dạng chuỗi JSON tự do. Backend gửi cái gì, Data Engineer nhận cái đó. Lúc giải mã (parse) mới phát hiện thiếu trường dữ liệu, Pipeline sập.
- **Có Data Contract (Schema Registry)**: Dữ liệu được mã hóa bằng định dạng có Schema chặt chẽ (như Avro hoặc Protobuf). Kafka Schema Registry đứng ở giữa làm "Cảnh sát". Nếu Backend gửi gói tin thiếu trường bắt buộc, Kafka sẽ reject gói tin đó ngay lập tức!

</details>

### Without Data Contracts (Fragile JSON)
```python
# Backend easily changes the payload. Data Engineers cry.
producer.send('sales_topic', value={
    # "user_id": 123, <-- Backend quietly removed this!
    "customer_id": "CUST_123", # And added this!
    "amount": 99.99
})
# Result: Downstream Spark job crashes with KeyError: 'user_id'
```

### With Data Contracts (Avro & Schema Registry)
```json
// The Contract (Avro Schema) agreed upon by both teams
{
  "type": "record",
  "name": "SaleEvent",
  "fields": [
    {"name": "user_id", "type": "int"}, // Mandatory field!
    {"name": "amount", "type": "double"}
  ]
}
```
If the backend tries to send a payload without `user_id`, the Schema Registry strictly rejects the serialization. The data never pollutes the pipeline.

| Aspect | Without Governance | With Data Contracts & DQ |
|---|---|---|
| **Schema Changes** | Silent, breaks downstream pipelines | Caught at the source (CI/CD or Registry) |
| **Data Quality Issues** | Found by Business Users (Loss of Trust) | Caught by DQ Tests (Circuit Breakers) |
| **Who owns the fix?** | Data Engineering team cleans up the mess | Domain Team (Backend) fixes their output |
| **Data Format** | Weakly typed (JSON, CSV) | Strongly typed (Avro, Protobuf) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Schema Evolution (Tiến hóa Schema)**: Khi cần thêm một cột mới vào sự kiện hiện tại, bạn dùng Schema Registry để đảm bảo thay đổi này là Tương thích ngược (Backward Compatible). Tức là code cũ đọc data mới vẫn không bị chết.
2. **Data Quality Circuit Breakers (Cầu dao chất lượng)**: Dùng `dbt tests` chạy kiểm tra dữ liệu MỚI trong một bảng tạm (Staging). Nếu test pass (ví dụ `revenue > 0`), mới chạy lệnh `MERGE` đẩy vào bảng Production. Nếu fail, dừng lại và gửi cảnh báo Slack.
3. **Data Mesh Implementation**: Chuyển giao quyền sở hữu CSDL (Ownership). Đội "Sales Backend" tự dựng pipeline dbt, tự viết Data Quality test cho dữ liệu Sales, và cung cấp nó cho team Data Analytics sử dụng.

**Không nên làm (Anti-patterns):**
- **Áp dụng Data Mesh cho công ty quy mô nhỏ**: Data Mesh đòi hỏi sự trưởng thành cực lớn về văn hóa và hạ tầng. Bắt các Backend Dev ở một startup 20 người phải học viết Data Pipeline là sự lãng phí tài nguyên khủng khiếp. Hãy giữ mô hình tập trung (Centralized) cho đến khi team Data trở thành nút thắt cổ chai của toàn công ty.

</details>

1. **Safe Schema Evolution**: When you need to add a new column to an event, you use Schema Registry to enforce Backward Compatibility. This ensures that old consumer applications reading the new data format will not crash.
2. **Data Quality Circuit Breakers**: Using `dbt tests` to validate NEW data in a temporary Staging table. If the tests pass (e.g., `revenue > 0` and `user_id is not null`), the data is `MERGE`d into the Production table. If tests fail, the pipeline halts and alerts Slack, protecting the Production dashboard.
3. **Implementing Data Mesh**: Shifting ownership. The "Sales Backend" team builds their own dbt pipelines, writes their own DQ tests, and serves the clean tables as a "Data Product" to the rest of the company.

### Anti-Patterns
- **Implementing Data Mesh in a Small Startup**: Data Mesh requires massive organizational maturity and self-serve infrastructure. Forcing Backend devs in a 20-person startup to learn data engineering is a massive distraction. Stick to a Centralized Data Team until the central team becomes the undeniable bottleneck for the whole company.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Áp dụng Hợp đồng ngay từ lúc sinh ra (Shift-Left):**
Đừng viết Data Quality Test ở cuối Data Warehouse (vì lúc đó rác đã vào nhà rồi). Hãy "Shift-Left" - đưa bài test sang hẳn bên trái. Nghĩa là viết test ngay từ lúc đẩy code Backend. Hợp đồng dữ liệu phải được lưu trong Git repository của team Backend.

**2. Viết Test những gì quan trọng nhất:**
Kiểm tra mọi cột sẽ làm hệ thống chậm đi. Hãy tập trung vào:
- **Tính duy nhất (Uniqueness)**: Khóa chính không được trùng.
- **Tính toàn vẹn (Completeness)**: Cột quan trọng không được NULL.
- **Tính bất thường (Anomaly/Volume)**: Hôm qua có 100k đơn hàng, hôm nay tự nhiên có 5 đơn. Chắc chắn hệ thống tracking có lỗi, dù data không null.

**3. Data Lineage (Truy xuất nguồn gốc):**
Sử dụng công cụ như dbt hoặc DataHub để vẽ sơ đồ: Bảng Dashboard này được sinh ra từ Bảng A, Bảng A sinh ra từ Cột B của Kafka Topic C. Khi Cột B bị đổi tên, bạn nhìn vào bản đồ Lineage là biết ngay lập tức Dashboard nào sẽ bị chết để báo trước cho sếp.

</details>

### 1. Shift-Left Data Quality
Do not write your Data Quality tests purely at the end of the Data Warehouse (by then, the garbage is already in your house). "Shift-Left" means pushing validation as close to the source as possible. Data Contracts should reside in the Backend team's Git repository and be verified during their CI/CD build process.

### 2. Pragmatic Testing (Don't test everything)
Running assertions on every single column is expensive and slows down pipelines. Focus on the critical dimensions:
- **Uniqueness**: Primary keys must not have duplicates.
- **Completeness**: Critical columns (like `amount`, `status`) must not be NULL.
- **Volume/Anomaly**: Yesterday we had 100k orders; today we have 5. Even if the data isn't NULL, a 99% drop in volume indicates a tracking failure upstream. Alert immediately.

### 3. Data Lineage
Use tools like dbt Docs or DataHub to generate a dependency graph: "This Executive Dashboard is fed by Table A, which is built from Column B of Kafka Topic C". When Column B is planned for deprecation, you look at the Lineage graph and immediately know exactly which Executive Dashboard will break, allowing you to proactively notify stakeholders.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Dưới đây là cấu hình dbt (YAML) để thiết lập Hợp đồng Dữ liệu (Contracts) và Kiểm tra Chất lượng (Tests) ngay bên trong Data Warehouse. dbt sẽ biến các cấu hình này thành mã SQL để chạy kiểm tra trước khi tạo bảng.

</details>

### Data Quality & Contracts using dbt (Data Build Tool)

In modern Data Engineering, `dbt` allows you to define constraints and tests in a simple YAML file. When you run `dbt build`, it first executes the models, then runs these tests. If a test fails, the build halts.

`models/schema.yml`
```yaml
version: 2

models:
  - name: fct_orders
    description: "The core fact table for completed orders."
    config:
      contract:
        enforced: true # This explicitly enforces the Data Contract at the DB level!

    columns:
      - name: order_id
        data_type: string
        description: "Primary key of the order"
        tests:
          - unique
          - not_null

      - name: customer_id
        data_type: string
        tests:
          - not_null
          # Referential integrity check (Foreign Key test)
          - relationships:
              to: ref('dim_customers')
              field: customer_id

      - name: order_amount
        data_type: numeric
        description: "Total revenue of the order"
        tests:
          - not_null
          # Custom assertion: Orders cannot be negative
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
```

**Running the checks:**
```bash
# In your terminal or Airflow DAG:
dbt test --select fct_orders
```

If the upstream backend system sends an `order_amount` of `-50` (perhaps a bug in their discount logic), the `dbt_expectations` test will catch it. The pipeline will fail gracefully, fire a Slack alert, and prevent the negative revenue from polluting the CEO's dashboard.

---

## Related Topics

- [Advanced DAG Patterns & Observability](../05-data-orchestration/advanced-dag-patterns-and-observability.md) — How Airflow actually triggers and monitors these `dbt` tests.
- [CDC & Idempotent Pipelines](../02-data-ingestion/cdc-and-idempotent-pipelines.md) — Where Schema Registry is configured to block bad JSON payloads.
- [Frontend Security](../../04-frontend-engineering/05-frontend-architecture/frontend-security.md) — Ensuring the data collected from the UI is clean before it ever reaches the backend.
