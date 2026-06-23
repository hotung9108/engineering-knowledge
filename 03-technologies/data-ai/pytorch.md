# PyTorch

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Cùng với TensorFlow, **PyTorch** (do nhóm Nghiên cứu AI của Facebook/Meta tạo ra) là một trong hai "Lò rèn" khổng lồ để xây dựng Trí Tuệ Nhân Tạo (Deep Learning). Nếu TensorFlow nổi tiếng vì sự cứng nhắc và công nghiệp, thì PyTorch sinh ra để dành cho các nhà Nghiên cứu khoa học. Đặc điểm "Ăn tiền" nhất của PyTorch là **Dynamic Computation Graph (Đồ thị Tính toán Động)**. Nó cho phép bạn chạy thử, sửa code, và xem kết quả của AI ngay lập tức từng dòng một (y hệt như cách bạn code Python bình thường). Sự linh hoạt tuyệt đối này đã giúp PyTorch nghiền nát TensorFlow trong giới Học thuật. Gần như 100% các bài báo khoa học đột phá về AI hiện nay (Bao gồm cả thuật toán đằng sau ChatGPT của OpenAI) đều được viết bằng PyTorch.

</details>

> **Summary**: Developed by Meta's AI Research lab (FAIR), **PyTorch** has become the undisputed champion of Deep Learning frameworks in academia and research, and is rapidly overtaking the enterprise space. At its core, PyTorch provides hardware-accelerated Tensor computing (like NumPy, but natively executing on GPUs) and deep neural network construction built on an automatic differentiation system (Autograd). 
> What catapulted PyTorch past Google's TensorFlow was its architectural paradigm: **Dynamic Computation Graphs (Eager Execution)**. It evaluates mathematical operations immediately as they are called in Python. This makes debugging PyTorch as intuitive as debugging standard Python code, allowing researchers to build highly complex, dynamic architectures (like recurrent networks whose structure changes depending on the input data) with minimal friction. Today, organizations like OpenAI, Tesla, and Microsoft rely heavily on PyTorch as their foundational AI infrastructure.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang dạy một đứa bé (AI) cách ráp Logo.
1. **TensorFlow (Cách cũ - Static Graph)**: Bạn bắt đứa bé nhắm mắt lại. Bạn giải thích toàn bộ bản vẽ từ đầu đến cuối bằng lời nói. Sau đó bạn hô "Chạy!". Đứa bé mở mắt ra và ráp liên tục. Nếu ráp sai ở bước 3, toàn bộ cái nhà sập, và bạn không thể biết nó sai ở đâu vì nó chạy quá nhanh.
2. **PyTorch (Cách mới - Dynamic Graph)**: Bạn cho đứa bé ráp từng viên gạch một. Cứ ráp xong 1 viên, bạn kiểm tra luôn: *"Đúng rồi, viên này đẹp, ráp tiếp đi"*. Nếu viên số 3 bị sai, bạn dừng nó lại ngay lập tức, sửa lại rồi cho đi tiếp. Cách dạy này trực quan, dễ hiểu và dễ sửa lỗi hơn rất nhiều.

</details>

Imagine composing a Symphony.
1. **TensorFlow 1.x (Static Graph)**: You write the entire sheet music from beginning to end in pen. You hand it to the orchestra, leave the room, and they play the whole thing. If a note sounds bad in the middle, you have to rewrite the entire sheet music and make them start over from the beginning.
2. **PyTorch (Dynamic Eager Execution)**: You stand in front of the orchestra. You ask the violins to play a single note. You listen to it *live*. If it sounds slightly off, you adjust it immediately, and then ask the cellos to join in. You compose and debug the symphony step-by-step, interactively, exactly as you hear it.

---

## Layer 1: Core Components (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

PyTorch xoay quanh 3 công cụ cốt lõi:
1. **Tensors (Ma trận đa chiều)**: Giống y hệt mảng của NumPy. Nó chứa con số. Điểm khác biệt duy nhất và vĩ đại nhất: Tensor của PyTorch có thể được ném vào chạy trên Card đồ họa (GPU) để tăng tốc độ tính toán lên 10.000 lần so với CPU.
2. **Autograd (Đạo hàm Tự động)**: Huấn luyện AI thực chất là giải bài toán Đạo Hàm khổng lồ để tìm ra "Trọng số" (Weights) tối ưu. Bạn không cần giỏi toán. Bạn chỉ cần ráp các lớp (Layers) lại với nhau, Autograd của PyTorch sẽ tự động nhẩm tính Đạo hàm ngược (Backpropagation) cho bạn một cách kỳ diệu ở hậu trường.
3. **`torch.nn` (Thư viện Thần kinh)**: Một kho chứa sẵn các "Khối Lego" cấu tạo nên Bộ não. Bạn cần 1 Lớp nơ-ron nhận diện Hình ảnh? Gọi khối `nn.Conv2d`. Bạn cần 1 Lớp xử lý ngôn ngữ? Gọi khối `nn.Transformer`. Bạn không cần tự viết toán học từ số không.

</details>

PyTorch abstracts the immense mathematical complexity of Deep Learning into three foundational pillars:
1. **Tensors**: The fundamental data structure. Conceptually identical to a NumPy `ndarray` (a multi-dimensional matrix of numbers). The critical distinction is that PyTorch Tensors have native hardware acceleration. Calling `tensor.to('cuda')` instantly moves the massive matrix from the system RAM to the Nvidia GPU VRAM, unlocking massively parallel matrix multiplication capabilities.
2. **Autograd (Automatic Differentiation)**: The engine of Deep Learning. Training a Neural Network involves adjusting millions of weights to minimize an error function. Doing this manually requires calculating complex partial derivatives (Backpropagation) using multivariate calculus. PyTorch's `Autograd` tracks every mathematical operation performed on a Tensor. When you call `.backward()`, it automatically computes the exact gradients for the entire computational graph instantly.
3. **The `torch.nn` Module**: The Neural Network API. It provides pre-built, highly optimized layers. Instead of manually writing the matrix math for a Convolutional Filter, you simply instantiate `nn.Conv2d()`. It provides layers for Recurrent networks (`nn.LSTM`), activation functions (`nn.ReLU`), and loss functions (`nn.CrossEntropyLoss`), acting as the Lego bricks of AI.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trước đây, Google đã làm bá chủ với TensorFlow. Vì sao PyTorch lật đổ được?
Đó là nhờ tính chất **Pythonic (Gần gũi với Python)**.
TensorFlow đời đầu sử dụng Đồ thị Tĩnh (Static Graph). Code TensorFlow trông giống như một thứ ngôn ngữ kỳ lạ ngoài hành tinh, bạn không thể dùng lệnh `print()` để in biến ra xem được. 
PyTorch thì khác, nó tích hợp cực kì sâu vào Python. Bạn dùng lệnh `if / else`, bạn dùng vòng lặp `for`, bạn dùng lệnh `print()` để xem dữ liệu y như viết Web bình thường. Điều này làm cho việc "Sửa lỗi" (Debugging) trở nên dễ dàng vô cùng. Giới Khoa học gia (vốn không rành code) yêu thích PyTorch ngay từ cái nhìn đầu tiên và vứt bỏ hoàn toàn TensorFlow.

</details>

PyTorch captured the absolute majority of academic AI research (powering the generative AI boom) because it prioritized **Developer Ergonomics and Debuggability**.
Prior to PyTorch, TensorFlow 1.x dominated. TF used an "Define-and-Run" paradigm (Static Graphs). You had to programmatically build a massive mathematical graph, compile it, and *then* push data through it inside a rigid "Session". If a matrix dimension was mismatched, the error was thrown miles away from the actual code line, making debugging a nightmare. Native Python features like `print()` or `pdb` debuggers simply didn't work inside the graph.
PyTorch introduced the "Define-by-Run" paradigm (Eager Execution). The graph is built dynamically on the fly as operations are executed. It feels exactly like standard Python. You can use standard Python `if/else` logic to change the network architecture based on dynamic inputs. You can drop a `pdb.set_trace()` directly inside the training loop to inspect a tensor's exact state. This flexibility was so overwhelmingly superior that it forced Google to completely rewrite TensorFlow (TF 2.0) to copy PyTorch's eager execution model.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh quá trình Huấn luyện Mô hình.
</details>

Visualizing Hardware Acceleration.

| Metric | NumPy (Pure CPU) | PyTorch (GPU Acceleration) |
|---|---|---|
| **Data Structure** | `x = np.random.rand(10000, 10000)` | `x = torch.rand(10000, 10000).cuda()` |
| **Matrix Multiplication**| `z = np.matmul(x, x)` | `z = torch.matmul(x, x)` |
| **Execution Time** | The CPU struggles to multiply 100 million numbers sequentially. Takes **~5.5 seconds**. | The GPU utilizes 4000 CUDA cores to calculate thousands of multiplications simultaneously. Takes **~0.05 seconds**. (100x Faster) |

---

## Layer 4: The PyTorch Ecosystem

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hệ sinh thái PyTorch mở rộng ra 3 "Vũ khí" chuyên biệt:
1. **TorchVision (Vua Hình ảnh)**: Chuyên dùng để làm AI nhận diện khuôn mặt, xe tự lái. Chứa sẵn mọi thuật toán cắt ghép, biến đổi ảnh, và cung cấp sẵn các bộ não siêu việt (như ResNet, YOLO) đã được huấn luyện trước (Pre-trained) bởi các tập đoàn lớn. Bạn tải về xài luôn khỏi cần train.
2. **TorchText & Hugging Face (Vua Ngôn ngữ)**: Nếu bạn muốn làm ra con ChatGPT của riêng mình. Hugging Face `transformers` (dựa trên PyTorch) là thư viện tiêu chuẩn của thế giới. Nó chứa hàng ngàn Mô hình Ngôn ngữ Lớn (LLM) cho phép bạn tải về hoàn toàn miễn phí.
3. **PyTorch Lightning (Khung sườn Tự động hóa)**: Khi bạn viết code PyTorch thuần, bạn phải tự viết vòng lặp `for` để Train AI, tự viết hàm lưu file, tự viết hàm đẩy lên GPU. Code lặp đi lặp lại rất dài. **PyTorch Lightning** là một thư viện bọc bên ngoài PyTorch. Nó dọn dẹp code của bạn cực kì gọn gàng, tự động hóa mọi bước lặp lại tẻ nhạt, giúp bạn chỉ tập trung vào thiết kế "Cấu trúc bộ não".

</details>

PyTorch acts as the foundation for highly specialized domains:
1. **TorchVision (Computer Vision)**: The standard library for image processing. It provides datasets, data augmentation pipelines (cropping, normalizing), and crucially, Pre-Trained Models (like ResNet, MobileNet). Instead of training an image classifier from scratch on 1 million images, you download a pre-trained ResNet model and use "Transfer Learning" to fine-tune it on your specific 100 images.
2. **Hugging Face `transformers` (NLP)**: While `torchtext` exists, the Natural Language Processing world is completely dominated by the Hugging Face library, which relies heavily on PyTorch under the hood. If you are fine-tuning a Large Language Model (LLM) like LLaMA 3 or BERT, you are using the Hugging Face API executing on PyTorch tensors.
3. **PyTorch Lightning (High-Level Abstraction)**: Pure PyTorch requires writing significant boilerplate code for the training loop, moving data to GPUs, logging, and saving checkpoints. **PyTorch Lightning** is an elegant framework built on top of PyTorch. It abstracts away all the engineering boilerplate, enforcing strict structural organization. It allows researchers to seamlessly scale their model from running on 1 local GPU to running on 100 distributed GPUs in an AWS cluster just by changing a single parameter `trainer(devices=100)`.

---

## Related Topics

- PyTorch is a library written in **[Python](./python-ai.md)**.
- If you are building AI specifically for mobile devices or deeply embedded enterprise legacy systems, its major competitor **[TensorFlow](./tensorflow.md)** might still be used.
- To orchestrate the massive data ingestion pipelines required to train PyTorch models, use **[Apache Airflow](./apache-airflow.md)**.
