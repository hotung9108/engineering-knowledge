# TensorFlow

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước khi có PyTorch, **TensorFlow** (do Google tạo ra) là ông Vua tuyệt đối đã khai sinh ra kỷ nguyên bùng nổ của Deep Learning (Học sâu). Thời kỳ đầu (TensorFlow 1.x), nó nổi tiếng là cực kì khó học, cú pháp phức tạp, và khi gặp lỗi thì hiện ra một đống mã bí hiểm không thể hiểu nổi. Khi PyTorch ra đời và đánh cắp trái tim của giới Khoa học gia bằng sự đơn giản, Google đã hoảng sợ và đập đi xây lại toàn bộ với **TensorFlow 2.0** (tích hợp Keras). Dù hiện nay đã thua PyTorch ở mảng Nghiên cứu Học thuật, TensorFlow vẫn nắm giữ một vũ khí bí mật không thể bị đánh bại: **Môi trường Doanh nghiệp (Production)**. Nếu bạn muốn đưa một mô hình AI lên chạy trên Điện thoại di động, Trình duyệt Web, hoặc nhúng vào một con chip IoT nhỏ xíu, hệ sinh thái khổng lồ của TensorFlow (TF Lite, TF.js, TF Extended) là lựa chọn duy nhất và mạnh mẽ nhất.

</details>

> **Summary**: **TensorFlow**, developed by the Google Brain team, was the seminal framework that catapulted Deep Learning into the mainstream. In its early incarnation (TensorFlow 1.x), it utilized a strict "Define-and-Run" Static Computation Graph. This resulted in a steep learning curve, highly verbose code, and notoriously difficult debugging, which eventually led to researchers abandoning it in favor of PyTorch's dynamic eager execution.
> Recognizing this existential threat, Google aggressively overhauled the architecture with **TensorFlow 2.0**, fully integrating the highly intuitive `Keras` API and enabling Eager Execution by default to match PyTorch's developer ergonomics.
> While PyTorch has largely conquered academic research and Generative AI, TensorFlow maintains a massive stronghold in **Enterprise Production Deployment**. Its expansive ecosystem (TensorFlow Extended (TFX) for MLOps, TensorFlow Lite for mobile/edge deployment, and TensorFlow.js for the browser) makes it the premier choice for organizations that need to deploy highly optimized models to billions of edge devices globally.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn Thiết kế một chiếc Ô tô (Mô hình AI).
1. **PyTorch (Xưởng Cơ khí)**: Rất dễ dàng để độ chế, tháo lắp động cơ. Phù hợp cho các nhà Khoa học chế tạo ra những chiếc siêu xe ý tưởng (Concept car) chạy thử trong phòng thí nghiệm. Nhưng khi muốn đem siêu xe đó sản xuất hàng loạt bán cho 1 triệu người, xưởng cơ khí này gặp khó khăn.
2. **TensorFlow (Nhà máy Dây chuyền)**: Quá trình thiết kế xe hơi khó khăn, cứng nhắc hơn. Nhưng một khi chiếc xe đã được chốt bản vẽ, TensorFlow có nguyên một Dây chuyền khổng lồ để sản xuất hàng loạt. Nó tự động nén cái xe lại cho nhỏ để nhét vừa vào Điện thoại (TF Lite), hoặc đẩy nó chạy thẳng trên Trình duyệt Web (TF.js).

</details>

Imagine designing and building a car.
1. **PyTorch (The Prototyping Workshop)**: Incredible for rapid iteration. You can easily swap parts out on the fly. It's the absolute best tool for scientists inventing a radically new combustion engine. However, when it's time to mass-produce 5 million units of this car, the workshop struggles with the logistics.
2. **TensorFlow (The Mass-Production Factory)**: Building the initial prototype feels slightly more rigid. But once the design is finalized, the TensorFlow ecosystem shines. It possesses a global logistics network. It can instantly shrink your car down to fit on a smartphone (TF Lite), compile it to run directly inside a Web Browser (TF.js), or deploy it to a massive global server cluster (TF Serving) seamlessly.

---

## Layer 1: Core Components (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

TensorFlow hiện đại (Phiên bản 2.x) được cấu thành từ 3 lớp:
1. **Lớp Lõi C++ (Tensor/Gradient)**: Tương tự như PyTorch, TF cung cấp cấu trúc `tf.Tensor` để lưu trữ dữ liệu tính toán song song trên GPU, và công cụ `tf.GradientTape` để tự động tính đạo hàm (backpropagation).
2. **Keras API (Lớp giao diện ăn tiền)**: Keras ban đầu là một thư viện độc lập siêu dễ xài, sau đó bị Google mua lại và sáp nhập vào TF. Keras bọc toàn bộ sự phức tạp của AI lại thành những lệnh cực kì đơn giản. Bạn chỉ mất đúng 5 dòng code `model.add(Dense(64))` là tạo xong một Bộ não, và đúng 1 lệnh `model.fit()` là bắt đầu huấn luyện. Nó dễ đến mức học sinh cấp 3 cũng có thể làm AI.
3. **Graph Execution (Sức mạnh ẩn giấu)**: Dù TF 2.0 đã cho phép chạy lệnh từng dòng (Eager Execution) giống PyTorch để dễ debug. Nhưng khi muốn đem mô hình đi triển khai thực tế, bạn có thể gắn thêm chữ `@tf.function`. TF sẽ biên dịch code Python của bạn ngược lại thành một Đồ thị Tĩnh bằng C++. Chạy siêu nhanh và không cần cài Python trên máy chủ đích.

</details>

The modern TensorFlow 2.x architecture is structured across three conceptual layers:
1. **The Low-Level Core (`tf.Tensor` & `tf.GradientTape`)**: The foundational mathematics engine. It provides the `tf.Tensor` object for GPU-accelerated linear algebra operations. For researchers who need to implement custom, non-standard training loops, `tf.GradientTape` records operations for automatic differentiation during backpropagation.
2. **The Keras API (High-Level Ergonomics)**: Keras was originally a standalone, highly intuitive API wrapper that could sit on top of multiple backends. Google acquired it and tightly coupled it as the default high-level API (`tf.keras`) in TF2.0. Keras abstracts the intense mathematical boilerplate into simple, sequential building blocks. Building an intricate Convolutional Neural Network (CNN) takes barely 10 lines of declarative code using the `Sequential` or `Functional` API.
3. **Graph Compilation (`@tf.function`)**: The true performance differentiator. While TF2.0 evaluates code dynamically (eagerly) for easy debugging, native Python execution is slow. By simply decorating a Python function with `@tf.function`, TensorFlow traces the Python code, automatically converts it into a highly optimized, low-level C++ Computation Graph (AutoGraph), and executes it independently of the Python interpreter, yielding massive performance gains.

---

## Layer 2: The Enterprise Deployment Ecosystem (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vì sao các công ty lớn vẫn không thể bỏ TensorFlow? Đó là nhờ Hệ sinh thái Triển khai (Deployment) khổng lồ không đối thủ:
1. **TensorFlow Lite (AI cho Mobile/IoT)**: Một Mô hình ngôn ngữ hoặc Nhận diện ảnh thường nặng tới 500MB, rất nặng. TF Lite dùng thuật toán Ép Kiểu (Quantization) để nén mô hình đó xuống còn 10MB mà không làm giảm độ thông minh. Nhờ đó, điện thoại Android, iOS hoặc các con chip Camera IoT nhỏ xíu có thể chạy AI ngay trên thiết bị mà không cần Internet.
2. **TensorFlow.js (AI trên Trình duyệt Web)**: Cho phép tải trực tiếp mô hình AI xuống trình duyệt Web của khách hàng. Mọi tính toán AI (như lọc khuôn mặt, đổi phông nền camera) được chạy trực tiếp bằng Card đồ họa trên máy tính của khách hàng. Công ty tiết kiệm được hàng triệu đô tiền thuê máy chủ.
3. **TensorFlow Extended (TFX - MLOps chuẩn Công nghiệp)**: Dây chuyền tự động hóa AI của Google. Nó giám sát vòng đời của AI từ lúc lấy dữ liệu, huấn luyện, kiểm tra độ chính xác, đến lúc đẩy lên Cloud một cách chuyên nghiệp nhất.

</details>

Why does TensorFlow fiercely maintain its enterprise market share despite PyTorch's dominance in Generative AI research? Because of its unparalleled, battle-tested Deployment and MLOps ecosystem.
1. **TensorFlow Lite (Edge & Mobile Computing)**: Deploying a 500MB Neural Network to an embedded microcontroller or an iOS app is impossible due to memory and thermal constraints. TFLite is a specialized toolkit that deeply optimizes models via Post-Training Quantization (converting 32-bit floats to 8-bit integers) and pruning. This dramatically shrinks the model footprint and allows low-latency, offline AI inference directly on edge devices.
2. **TensorFlow.js (In-Browser Machine Learning)**: A groundbreaking JavaScript library that runs ML models directly inside a web browser or Node.js environment. By utilizing WebGL (and now WebGPU) for hardware acceleration, the ML inference happens entirely on the client's machine. This architecture ensures absolute data privacy (user data never leaves the browser) and achieves zero-latency interactions (e.g., real-time background blurring in video calls) while offloading compute costs from the company's servers.
3. **TensorFlow Extended (TFX)**: The industry standard for MLOps. TFX is an end-to-end platform for deploying production ML pipelines. It handles data validation (checking for data drift), model training, rigorous model evaluation, and structured deployment via TF Serving.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh độ dễ sử dụng khi tạo một Mô hình AI cơ bản.
</details>

Visualizing API Simplicity.

| Metric | Low-Level Math (e.g., TensorFlow 1.x) | High-Level Keras (TensorFlow 2.x) |
|---|---|---|
| **Code Verbosity** | Defining variables, initializing sessions, writing the manual forward pass and backward pass formulas. Requires 50+ lines of complex code. | `model = Sequential([Dense(64, activation='relu'), Dense(10)])`. Takes exactly 1 line of code. |
| **Training the Model** | Writing custom `for` loops, managing batch sizes manually, updating weights mathematically. | `model.fit(x_train, y_train, epochs=10)`. Keras handles the entire training loop under the hood. |

---

## Layer 4: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Dùng Keras cho mọi thứ (Đừng làm khó mình)**: Trừ khi bạn đang viết một Luận án Tiến sĩ phát minh ra thuật toán AI mới. Còn nếu bạn làm AI cho công ty để giải quyết các bài toán thông thường (Phân loại ảnh chó mèo, Dịch ngôn ngữ, Tiên đoán giá cổ phiếu), HÃY DÙNG `tf.keras`. Đừng tốn thời gian cố viết những đoạn code Cấp thấp (Low-level). Keras đã tối ưu tốc độ hoàn hảo.
2. **Lưu Mô hình bằng định dạng SavedModel**: Khi huấn luyện AI xong, bạn có 2 cách lưu. 1 là lưu Trọng số (`.h5`). 2 là lưu toàn bộ Mô hình (`SavedModel`). Luôn ưu tiên dùng `SavedModel`. Nó sẽ gói toàn bộ Cấu trúc (Não) + Trọng số (Kinh nghiệm) vào một thư mục chung. Khi chuyển qua cho team Backend (Viết bằng Java hay Go) đem lên máy chủ, họ không cần viết lại cấu trúc AI, chỉ cần load file đó lên là chạy được luôn.

</details>

1. **Default to the Keras Functional API**: When building models, developers often start with the `tf.keras.Sequential` API because it is incredibly simple (just stacking layers). However, `Sequential` cannot handle multi-input/multi-output models or complex residual connections. **Rule**: Standardize your team on the **Keras Functional API**. It is slightly more verbose but offers infinite architectural flexibility (like building DAGs of layers) while retaining all the ease-of-use of Keras. Leave the low-level `tf.GradientTape` loops exclusively for highly experimental research.
2. **Export strictly via the `SavedModel` Format**: In TF/Keras, you can save just the model weights (e.g., an HDF5 file). This is dangerous because loading the weights later requires you to perfectly rewrite the Python code that defines the network architecture. **Rule**: Always export to the standard **TensorFlow SavedModel** directory format. This bundles the Model Weights, the Computation Graph architecture, and the execution functions into a language-agnostic format. A Java, Go, or C++ backend service can load a `SavedModel` and execute inferences without a single line of Python code existing on the production server.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Xung đột phiên bản CUDNN (Nỗi ác mộng tồi tệ nhất)**: Nếu bạn cài TensorFlow bằng lệnh `pip install tensorflow` trên máy Windows, và cố chạy nó bằng Card màn hình Nvidia. Bạn sẽ khóc ròng trong nhiều ngày. Vì TensorFlow cực kì khó tính. Phiên bản TF 2.10 bắt buộc phải đi chung chính xác với phần mềm CUDA 11.2 và cuDNN 8.1. Nếu bạn cài lộn phiên bản, TF sẽ báo lỗi không nhận Card màn hình và quay về chạy bằng CPU rùa bò.
   - *Cách giải*: KHÔNG BAO GIỜ tự cài CUDA bằng tay. Hãy dùng **Docker** (Tải cái Thùng chứa sẵn TF và CUDA do Google làm sẵn). Hoặc dùng Conda: `conda install tensorflow-gpu`.
2. **Quên dùng Tensors (Dùng nhầm Numpy Array)**: Keras quá thông minh nên nó cho phép bạn ném mảng `Numpy` vào để huấn luyện luôn. Tuy nhiên, nếu bạn tự viết một hàm Mất mát (Loss function) và dùng Numpy bên trong đó. Code Python sẽ CHẠM MẶT GRAPH của C++, gây tắc nghẽn cổ chai dữ dội, tốc độ tuột thê thảm. Mọi tính toán nằm trong hàm của TensorFlow BẮT BUỘC phải đổi sang dùng các hàm `tf.math` và biến `tf.Tensor`.

</details>

1. **The CUDA/cuDNN Dependency Hell**: The most notoriously painful aspect of the TensorFlow ecosystem. Hardware acceleration relies on proprietary Nvidia libraries (CUDA toolkit and cuDNN). TF versions are rigidly pinned to specific minor versions of CUDA. If you manually install CUDA 11.8 on your Windows host, but `pip install tensorflow==2.10` (which strictly demands CUDA 11.2), TensorFlow will silently fail to bind to the GPU and fallback to excruciatingly slow CPU execution. **Rule**: Never manage GPU drivers manually on the host machine. You MUST execute TensorFlow environments exclusively via **NVIDIA Docker Containers** (`nvidia-docker`), which neatly package the exact TF binary tightly bound to its perfectly matching CUDA/cuDNN libraries.
2. **Breaking the Computation Graph (Python Fallback)**: The `@tf.function` decorator accelerates code by translating it to a C++ graph. However, if you include a raw Python operation (like a Python `list.append()` or a `numpy.mean()` call) inside the decorated function, TensorFlow cannot compile it. It will secretly fallback to executing that single line in native Python, causing massive overhead and destroying performance. **Rule**: Inside a `@tf.function`, you are restricted strictly to TensorFlow primitives. You must use `tf.TensorArray` instead of Python lists, and `tf.reduce_mean()` instead of Numpy.

---

## Related Topics

- TensorFlow is a massive library written for **[Python](./python-ai.md)**.
- If you are focused purely on Academic Research or Generative AI, consider the more flexible **[PyTorch](./pytorch.md)**.
- In production, TensorFlow models are frequently deployed to scale using **[Kubernetes](../cloud-infra/kubernetes.md)**.
