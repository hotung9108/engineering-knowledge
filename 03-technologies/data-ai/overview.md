# Data Engineering & AI Overview

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Kỹ sư Phần mềm (Software Engineering) tập trung vào việc tạo ra các Ứng dụng để người dùng nhập dữ liệu vào (Ví dụ: Ứng dụng Shopee để người dùng đặt hàng), thì **Data Engineering (Kỹ sư Dữ liệu)** tập trung vào việc xử lý núi dữ liệu khổng lồ đó ở hậu trường. 
> Mỗi ngày, một công ty lớn có thể sinh ra hàng tỷ giao dịch, click chuột, và log. Dữ liệu này ban đầu là "Rác" (Dữ liệu thô - Raw Data). Kỹ sư Dữ liệu phải xây dựng những "Đường ống" (Data Pipelines) khổng lồ để bơm, lọc, và làm sạch đống rác đó thành "Vàng" (Dữ liệu sạch). 
> Khi đã có "Vàng", các **Kỹ sư AI (Trí tuệ Nhân tạo)** mới có thể dùng nó để huấn luyện các Mô hình Toán học (Machine Learning Models), giúp dự đoán tương lai (Ví dụ: Gợi ý sản phẩm khách hàng sắp mua, hoặc nhận diện khuôn mặt). AI không thể tồn tại nếu thiếu Dữ liệu sạch.

</details>

> **Summary**: Software Engineering is fundamentally concerned with state mutation (creating applications that allow users to generate and modify data). **Data Engineering**, conversely, is concerned with data logistics at an unimaginably massive scale. Modern enterprises generate petabytes of raw, unstructured telemetry, transactional data, and clickstreams daily. A Data Engineer designs and orchestrates distributed, fault-tolerant **Data Pipelines** (ETL/ELT processes) to ingest this data from disparate sources, cleanse it, transform it, and load it into centralized Data Warehouses or Data Lakes.
> This highly structured, pristine data is the mandatory prerequisite for **Artificial Intelligence (AI) and Machine Learning (ML)**. AI Engineers utilize this curated data to train complex neural networks. Without robust Data Engineering pipelines, Data Scientists are effectively paralyzing their AI models with "Garbage In, Garbage Out" (GIGO). AI is the engine; Data Engineering is the refinery that produces the fuel.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng quá trình làm ra Món Bánh Kem Siêu Ngon (AI).
1. **Dữ liệu thô (Raw Data)**: Giống như bột mì dính đất, trứng gà chưa rửa, đường còn lẫn cát nằm rải rác ở 10 nông trại khác nhau.
2. **Data Engineer (Kỹ sư Dữ liệu - Người sơ chế)**: Là người lái xe tải đi gom nguyên liệu từ 10 nông trại đó về. Họ dùng máy móc để lọc cát ra khỏi đường, rửa sạch trứng, và đóng gói nguyên liệu thành từng hộp sạch sẽ đẹp đẽ đặt vào tủ lạnh.
3. **AI Engineer (Kỹ sư AI - Bếp trưởng)**: Bếp trưởng không bao giờ đi nhặt trứng. Họ chỉ mở tủ lạnh, lấy những hộp nguyên liệu hoàn hảo đã được Kỹ sư Dữ liệu chuẩn bị sẵn, áp dụng "Công thức bí truyền" (Thuật toán Machine Learning) để nướng ra cái Bánh Kem (Mô hình AI) dự đoán được ý thích của khách hàng.

</details>

Imagine the process of refining crude oil to launch a Rocket (AI).
1. **Raw Data**: Highly toxic, unrefined crude oil buried deep underground across 50 different geographic locations.
2. **Data Engineering (The Refinery Pipeline)**: The Data Engineer builds massive physical pipelines to extract the crude oil from the ground, transport it to a central refinery, chemically filter out the sulfur and impurities, and convert it into high-grade, pure Rocket Fuel.
3. **AI Engineering (The Rocket Scientist)**: The AI Engineer designs the aerodynamic Rocket (The Neural Network). But the rocket cannot fly on crude oil. It relies entirely on the Data Engineer to pump the highly refined Rocket Fuel into its engines so it can launch into orbit.

---

## Layer 1: The Data Pipeline Anatomy (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Một hệ thống Dữ liệu (Data Pipeline) thường đi qua 3 bước cốt lõi, gọi tắt là **ETL**:
1. **Extract (Trích xuất)**: Đi gom dữ liệu từ mọi ngóc ngách. Rút dữ liệu từ Database SQL của team Backend, lấy file Excel của phòng Kế toán, hút Log từ hệ thống ELK.
2. **Transform (Biến đổi - Quan trọng nhất)**: Dữ liệu gom về cực kì lộn xộn. (File SQL ghi ngày tháng là `14/10`, file Excel ghi là `Oct-14`). Bước này sẽ dùng Code (Thường là Python) để gọt giũa tất cả về chung 1 chuẩn `2023-10-14`. Xóa bỏ các dòng bị lỗi, ẩn đi số thẻ tín dụng của khách hàng để bảo mật.
3. **Load (Tải vào kho)**: Bơm toàn bộ dữ liệu sạch sẽ đó vào một cái Kho khổng lồ (Data Warehouse hoặc Data Lake). Lúc này, Dữ liệu đã sẵn sàng để team Phân tích (Data Analytics) làm báo cáo, hoặc team AI đem đi train model.

</details>

The backbone of Data Engineering is the **ETL (Extract, Transform, Load)** or **ELT** pipeline:
1. **Extract**: Ingesting data from highly disparate upstream sources. This includes reading transactional databases (PostgreSQL, MySQL) via Change Data Capture (CDC), pulling JSON files from third-party APIs, streaming events from Kafka, or parsing flat CSV files.
2. **Transform (The Heavy Lifting)**: Raw data is dirty, inconsistent, and often non-compliant. The Transformation phase cleanses the data (handling null values), standardizes formats (normalizing dates and currencies), joins datasets together, and masks PII (Personally Identifiable Information) to comply with GDPR/HIPAA. This is heavily computationally intensive, often using Apache Spark.
3. **Load**: Pumping the curated, standardized data into the final analytical storage destination. This is typically an OLAP (Online Analytical Processing) Data Warehouse (like Snowflake, Google BigQuery) or a Data Lake (like AWS S3). Here, Data Analysts can run massive SQL queries, and Data Scientists can train ML models.

---

## Layer 2: From Data to Artificial Intelligence (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tại sao AI lại đang bùng nổ dữ dội? Nhờ 3 yếu tố hội tụ:
1. **Sự bùng nổ Dữ liệu (Big Data)**: Các công ty gom được lượng dữ liệu khổng lồ từ Internet.
2. **Sức mạnh Tính toán (GPU)**: Trước đây dùng CPU chạy AI mất 10 năm. Giờ đây Card đồ họa (GPU) của Nvidia cho phép tính toán song song hàng triệu phép tính, rút ngắn thời gian train AI xuống còn vài ngày.
3. **Các Thuật toán Đột phá**: Đặc biệt là kiến trúc **Transformer** (Trái tim của ChatGPT) ra đời năm 2017. Nó cho phép AI "hiểu" được ngữ cảnh của cả một đoạn văn bản dài thay vì chỉ đọc từng chữ.
Khi Dữ liệu sạch (Data Engineering) gặp được GPU mạnh và Thuật toán xịn (AI Engineering), chúng ta tạo ra được những cỗ máy thông minh như con người.

</details>

Why is Artificial Intelligence experiencing a renaissance right now? It is the convergence of three foundational pillars:
1. **The Proliferation of Big Data**: We finally have the global infrastructure (IoT, social media, digitized transactions) to generate the exabytes of training data required for Deep Learning.
2. **Massive Parallel Compute (GPUs)**: Training deep neural networks on traditional CPUs is mathematically too slow. The adaptation of Graphics Processing Units (GPUs, pioneered by Nvidia)—which handle thousands of matrix multiplications simultaneously—reduced model training times from years to days.
3. **Algorithmic Breakthroughs (Deep Learning)**: The shift from classical statistical Machine Learning (like Linear Regression) to Deep Neural Networks. Specifically, the invention of the **Transformer Architecture** by Google in 2017 (the "T" in ChatGPT), which enabled models to process sequential data (like natural language) in parallel and "pay attention" to context over long distances.

---

## Layer 3: Software Engineering vs Data/AI Engineering (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cách suy nghĩ khi viết Code.
</details>

Visualizing the Paradigm Shift in Engineering.

| Metric | Traditional Software Engineering | Data / AI Engineering |
|---|---|---|
| **The Logic** | **Deterministic (Có quy luật rõ ràng)**. Lập trình viên viết `if (a > b) return true`. Kết quả luôn đúng 100%. | **Probabilistic (Dựa trên xác suất)**. Kỹ sư AI không viết luật. Họ ném dữ liệu cho AI tự học. AI trả lời: *"Tấm hình này có 95% xác suất là con chó"*. Thỉnh thoảng AI sẽ đoán sai. |
| **The Artifact** | Sản phẩm cuối cùng là một File Code (`.exe` hoặc `.js`). Bấm nút là chạy. | Sản phẩm cuối cùng là một Ma trận số khổng lồ (Model Weights). File này nặng hàng chục Gigabyte. |
| **Testing** | Viết Unit Test. Chạy thử thấy màn hình Web hiện đúng màu xanh là xong. | Chạy kiểm thử trên hàng vạn dữ liệu. Đo độ chính xác (Accuracy). Nếu Dữ liệu huấn luyện bị thiên kiến (Bias), AI sẽ phân biệt chủng tộc. Rất khó debug. |

---

## Layer 4: Common Architectures & Roles

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Ngành Dữ liệu chia làm 3 Nhóm công cụ/Vai trò chính:
1. **Data Orchestration (Nhạc trưởng Dữ liệu)**: Việc bơm dữ liệu phải chạy đúng giờ. Ví dụ: Đúng 12h đêm đi lấy file, 1h sáng lọc file, 2h sáng đẩy vào Kho. Người ta dùng **Apache Airflow** để lập lịch và giám sát các bước này. Nếu bước 1 lỗi, nó báo động và dừng bước 2 lại.
2. **AI Frameworks (Lò rèn AI)**: Khi Dữ liệu đã sẵn sàng, Kỹ sư AI dùng ngôn ngữ **Python** kết hợp với các thư viện Toán học khổng lồ (như **TensorFlow** của Google hoặc **PyTorch** của Facebook) để xây dựng bộ não nhân tạo (Neural Networks).
3. **MLOps (Đưa AI vào thực tế)**: AI train xong chỉ nằm trên máy tính của Lập trình viên. MLOps là việc Đóng gói cái bộ não AI đó vào Docker, đem lên Cloud (AWS/K8s) làm thành 1 cái API API. Khi Khách hàng gửi ảnh lên, API đó nhận ảnh, đưa cho AI dự đoán, và trả kết quả về trong 0.5s.

</details>

The Data and AI landscape is highly specialized into specific lifecycle phases:
1. **Data Orchestration & Pipelines (The Plumber)**: ETL jobs are complex, multi-stage Directed Acyclic Graphs (DAGs). You cannot run the "Transform" script until the "Extract" script successfully finishes. **Apache Airflow** is the industry standard for scheduling and monitoring these massive dependencies, ensuring data flows correctly at 2 AM every night.
2. **Deep Learning Frameworks (The Brain Builders)**: Python is the undisputed language of AI. To build Neural Networks, engineers do not write matrix multiplication logic from scratch. They use highly optimized, GPU-accelerated frameworks. **TensorFlow** (created by Google) and **PyTorch** (created by Meta/Facebook) provide the high-level APIs to construct layers of neurons and execute backpropagation automatically.
3. **MLOps (Machine Learning Operations)**: A trained model sitting in a Jupyter Notebook is useless to a business. MLOps is the discipline of treating ML models like software engineering artifacts. It involves versioning the datasets, containerizing the Model (wrapping it in a Python FastAPI backend), deploying it to a Kubernetes cluster equipped with GPUs, and monitoring it for "Model Drift" (when a model's accuracy degrades over time because the real world has changed since it was trained).

---

## Related Topics

- For scheduling and managing complex Data Pipelines, see **[Apache Airflow](./apache-airflow.md)**.
- For the undisputed language of Data and AI, explore **[Python AI Ecosystem](./python-ai.md)**.
- To build modern Deep Learning models, compare **[PyTorch](./pytorch.md)** and **[TensorFlow](./tensorflow.md)**.
- Data Pipelines often consume real-time streaming data from Message Brokers like **[Kafka](../message-brokers/kafka.md)**.
