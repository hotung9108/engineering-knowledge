# Python & FastAPI

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Python vốn nổi tiếng với framework Django (một con quái vật nguyên khối khổng lồ) hoặc Flask (nhẹ nhưng cổ hủ). Tuy nhiên, vì Python là một ngôn ngữ "thông dịch" (interpreted), nhược điểm chí mạng của nó luôn là Tốc độ. Cho đến khi **FastAPI** xuất hiện. Nó tận dụng triệt để cơ chế Bất đồng bộ (`async`/`await`) mới của Python và thư viện Pydantic để ép kiểu dữ liệu chặt chẽ. Kết quả? Một framework Python có tốc độ xử lý nhanh ngang ngửa với Node.js và Go, code cực kì ngắn gọn, và đặc biệt TỰ ĐỘNG sinh ra tài liệu API (Swagger UI). Vì Python là ngôn ngữ số 1 của mảng Trí tuệ nhân tạo (AI), FastAPI hiện nay là lựa chọn hoàn hảo nhất để bọc các mô hình AI thành API cho thế giới sử dụng.

</details>

> **Summary**: Python has historically dominated Data Science and Machine Learning, but in Web Backend architectures, it was often bottlenecked by the slow, synchronous execution of heavy monolithic frameworks (Django) or minimalist-but-aging micro-frameworks (Flask). **FastAPI** emerged as a revolutionary paradigm shift. Built natively on Python's modern `asyncio` standard and the ASGI (Asynchronous Server Gateway Interface) specification, it achieves execution speeds rivaling Node.js and Go. Its architectural brilliance lies in its heavy integration with `pydantic`. By aggressively leveraging Python Type Hints (`def get_user(id: int)`), FastAPI executes rigorous request validation, mathematical JSON serialization, and completely automates the generation of OpenAPI (Swagger) documentation, drastically reducing developer boilerplate. It is the undisputed best-in-class framework for serving AI/ML models as microservices.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn mở một Cửa hàng bọc quà (API).
1. **Flask/Django (Cách cũ)**: Khách mang đến một cái hộp bí ẩn. Bạn mở hộp ra, phải lấy thước đo, soi đèn pin xem trong đó là quả táo hay quả bom (Tự viết code kiểm tra dữ liệu bằng tay). Xong xuôi bạn gói quà, nhưng bạn hay quên ghi chú lại món đó là gì (Không có tài liệu).
2. **FastAPI (Cách mới)**: Bạn đặt ra một cái Máy quét cổng từ bằng AI (Pydantic). Bạn cài đặt: "Chỉ nhận Quả táo (String) và Cân nặng (Số)". Khách đưa quả bom vào, Máy quét lập tức giật điện và đuổi khách đi ngay lập tức (Tự động Validate lỗi 422). Không những thế, cái Máy quét còn tự động in ra một cuốn menu cực đẹp (Swagger UI) ghi rõ: "Cửa hàng này nhận bọc Táo và Cân nặng" cho tất cả mọi người cùng đọc. Bạn không cần làm gì ngoài việc gói quà.

</details>

Imagine a Border Customs Checkpoint.
1. **Flask (Legacy)**: The border guard manually opens every suitcase. They have to write custom logic for every traveler: "Is this a shirt? Is this liquid? Is this heavy?". It is slow, highly prone to human error, and the guard forgets to log what they found.
2. **FastAPI**: You install a futuristic X-Ray Portal (Pydantic Type Hints). You tell the portal: `Suitcase(shirts: int, liquids: float)`. When a traveler walks through, if they have a `shoes: string`, the portal automatically rejects them with a perfectly formatted error receipt (HTTP 422). Furthermore, the portal automatically prints a beautiful, live-updating map (OpenAPI Swagger) outside the building telling everyone exactly what is allowed through the border. The guard just stamps the passport.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

FastAPI đứng trên vai 3 gã khổng lồ:
1. **Starlette (Tốc độ)**: Một bộ khung mạng ASGI cực nhanh. Nó cho phép Python chạy code "Bất đồng bộ" (Async) y hệt như Node.js, giúp xử lý hàng ngàn kết nối cùng lúc mà không bị nghẽn luồng.
2. **Pydantic (Bảo vệ)**: Thư viện ép kiểu của Python. Bạn chỉ cần định nghĩa cái Lớp `class User(BaseModel): name: str`, Pydantic sẽ kiểm tra toàn bộ cục JSON khách hàng gửi lên. Thiếu chữ `name`? Nó báo lỗi 422 ngay.
3. **OpenAPI (Tài liệu)**: Dựa vào các định nghĩa Type Hint (`int`, `str`), FastAPI tự động vẽ ra trang web Document (Swagger UI) cho API của bạn. Code bạn đổi, tài liệu tự động đổi theo. Không bao giờ sợ tài liệu lỗi thời.

</details>

FastAPI is not built from scratch; it is a masterclass in composition, orchestrating three highly optimized foundational libraries:
1. **Starlette (The Web Engine)**: A lightweight, ultra-high-performance ASGI (Asynchronous Server Gateway Interface) framework. It empowers Python to escape the legacy WSGI synchronous blocking model. By utilizing `async def` and `await`, FastAPI handles massive concurrent WebSockets and long-polling HTTP requests with Node.js-level efficiency.
2. **Pydantic (The Data Validation Engine)**: The core data parsing library. Instead of writing imperative `if request.json["age"] > 0:` checks, developers define declarative Python Classes inheriting from `BaseModel`. Pydantic aggressively coerces types (turning the string `"1"` into the integer `1`) and mathematically validates complex nested JSON schemas. If validation fails, it instantly returns a meticulously detailed HTTP 422 Unprocessable Entity response.
3. **OpenAPI / Swagger (The Documentation Engine)**: Because FastAPI natively parses Python Type Hints (`id: int`), it inherently understands the exact contractual schema of your entire application. It dynamically translates this AST into a standard OpenAPI JSON schema, serving a beautiful, interactive Swagger UI page at `/docs` with absolutely zero developer boilerplate.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Trước đây, khi các nhà Khoa học dữ liệu (Data Scientist) huấn luyện xong một Mô hình Trí tuệ nhân tạo (AI/ML), họ muốn đưa nó lên Web. Họ thường phải dùng **Flask**. Nhưng Flask chạy tuần tự (Đồng bộ). Quá trình đưa ảnh vào Mô hình AI mất 2 giây. Trong 2 giây đó, toàn bộ Server bị khóa chặt, những người khác không thể vào được.
Hơn nữa, API của Flask cực kì tốn công viết tài liệu (Swagger). Các kĩ sư Frontend liên tục phàn nàn "Ủa cái API dự đoán mặt người này bắt tôi truyền lên cái gì?".
FastAPI ra đời để giải quyết triệt để vấn đề này. Nó sinh ra để các kĩ sư AI có thể xuất xưởng Model của họ thành một API cực nhanh (bằng `async`), cực kì an toàn (chặn dữ liệu rác bằng Pydantic), và Frontend có ngay trang web tài liệu để test trực tiếp mà Backend không cần viết thêm 1 dòng code nào.

</details>

FastAPI was created to bridge the catastrophic gap between Data Science (Machine Learning) and Production-Grade Web Engineering.
Python is the undisputed language of AI (PyTorch, TensorFlow, Scikit-Learn). When an ML Engineer finishes training a model, it must be exposed as a REST API. Historically, they wrapped it in Flask. Because Flask is synchronous (WSGI), an ML inference taking 500ms would physically block the OS thread. 4 concurrent requests would queue up, causing horrific latency spikes. Furthermore, creating strict API documentation for the Frontend team was a manual, unmaintained nightmare.
FastAPI exists to natively support `asyncio`, allowing the server to accept thousands of concurrent requests while the ML Model churns in the background thread. Simultaneously, by treating Python Type Hints as first-class citizens, it completely automates OpenAPI documentation generation, bridging the communication gap between Backend Data Scientists and Frontend UI Engineers flawlessly.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc tạo một API Nhận thông tin Sản phẩm (Có kiểm tra lỗi) bằng Flask cũ và FastAPI.
</details>

Visualizing Boilerplate Reduction (Flask vs FastAPI).

| Metric | Flask (Legacy WSGI) | FastAPI (Modern ASGI) |
|---|---|---|
| **Data Extraction**| `data = request.get_json()`<br>`price = data.get("price")` | Defined strictly in function args via Pydantic `Item` model. |
| **Manual Validation**| `if price is None or type(price) != float:`<br>`return {"error": "Price must be float"}, 400` | **Zero Code**. Pydantic instantly intercepts bad types and throws an HTTP 422 automatically. |
| **The Function** | `def create_item(): ...` | `async def create_item(item: Item): ...` |
| **Documentation** | You must manually maintain a massive `swagger.yaml` file by hand, or write huge Docstrings. | **Zero Code**. You visit `/docs` and the entire interactive UI is generated directly from the Type Hints. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bọc các Mô hình AI/Machine Learning (AI Microservices)**: 99% các dịch vụ AI hiện đại (LLMs, Computer Vision, Text-to-Speech) đều viết bằng Python. FastAPI là lớp vỏ bọc hoàn hảo nhất để đẩy các mô hình này thành API cho bên ngoài gọi vào, tận dụng sức mạnh đa luồng `async` để không làm nghẽn Server.
2. **API Backend siêu tốc cho dự án cỡ vừa**: Nếu bạn làm một ứng dụng không cần kiến trúc nguyên khối khổng lồ như Java Spring, nhưng bạn lại ghét sự lỏng lẻo của JavaScript (Node.js). FastAPI mang lại cảm giác code rất an toàn nhờ Ép kiểu mạnh (Type Hints) mà tốc độ code lại nhanh như gió.
3. **Xử lý luồng dữ liệu thời gian thực (WebSockets)**: Nhờ Starlette, FastAPI hỗ trợ WebSockets cực kì mạnh mẽ và nhẹ nhàng. Phù hợp cho các hệ thống Chat nội bộ của doanh nghiệp hoặc Streaming dữ liệu chứng khoán.

</details>

1. **Machine Learning / AI Microservices (The Standard)**: The absolute dominant use case. If you deploy a PyTorch Neural Network or interact with the OpenAI API, you are using Python. FastAPI provides the fastest, most type-safe, non-blocking HTTP wrapper to serve these models to the public internet via REST endpoints, effectively becoming the industry standard over Flask.
2. **High-Performance CRUD APIs**: For startups who prefer Python's ecosystem (Pandas, Numpy, SQLAlchemy) over Node.js, but require Node.js-level concurrency. FastAPI, when paired with an asynchronous ORM (like `SQLModel` or asynchronous `SQLAlchemy`), provides a lightning-fast data persistence layer with strict schema validation out-of-the-box.
3. **Real-Time Data Streaming (WebSockets)**: Because it is built on ASGI, FastAPI treats WebSockets as first-class citizens. Building a real-time collaborative dashboard or a high-frequency trading ticker is trivial and highly scalable compared to legacy threaded WSGI servers.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiểu rõ `def` và `async def`**: Trong FastAPI, nếu bạn viết `def`, framework sẽ tự động tống cái hàm đó ra một luồng phụ (Threadpool) để tránh làm nghẽn luồng chính. Nếu bạn viết `async def`, nó sẽ chạy thẳng trên luồng chính (Event Loop). 
   - *Luật*: Nếu bạn dùng một thư viện CŨ gọi Database (không hỗ trợ async), hãy dùng `def` bình thường. ĐỪNG dùng `async def` với các hàm đồng bộ, vì nó sẽ KHÓA CHẶT (Block) toàn bộ Server của bạn.
2. **Sử dụng Dependency Injection (DI) của FastAPI**: Khác với Node/Express dùng Middleware rườm rà. FastAPI cho phép bạn nhét một biến `Depends()` thẳng vào tham số của hàm. Rất tuyệt vời để kiểm tra Token Đăng nhập (Authentication) hoặc mở kết nối Database chỉ bằng đúng 1 dòng code rất thanh lịch.

</details>

1. **Master the Concurrency Model (`def` vs `async def`)**: This is the most misunderstood mechanic in FastAPI. 
   - If you define a route with `async def`, FastAPI executes it directly on the main asynchronous Event Loop. If you perform a blocking operation inside this (e.g., a massive `for` loop, or a synchronous `psycopg2` database call), **you instantly kill the entire server**.
   - If you define a route with a standard `def`, FastAPI intelligently offloads it to a background Threadpool. 
   - **Absolute Rule**: If your database driver or HTTP library (like `requests`) is Synchronous, you MUST use `def`. Only use `async def` if every single I/O call inside the function uses `await` (e.g., using `httpx` or `asyncpg`).
2. **Leverage Native Dependency Injection (`Depends`)**: FastAPI handles dependencies brilliantly, avoiding Express.js's confusing Middleware chains. If a route requires an authenticated User, or an active Database Session, you explicitly declare it in the function signature: `async def get_items(user = Depends(get_current_user), db = Depends(get_db)):`. FastAPI resolves the dependency *before* executing the route, creating highly modular, testable code.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nhầm lẫn giữa Dữ liệu Database (SQLAlchemy) và Dữ liệu API (Pydantic)**: Nhiều Dev lười biếng dùng chung 1 Class duy nhất cho cả việc tạo bảng trong Database lẫn làm DTO cho API. Hậu quả là vô tình lộ mật khẩu người dùng hoặc mã số ẩn ra ngoài Swagger UI.
   - *Luật*: Tương tự Spring Boot, Bắt buộc phải tách biệt rạch ròi. `models.py` (SQLAlchemy) dùng cho Database. `schemas.py` (Pydantic) dùng cho việc kiểm tra Dữ liệu vào/ra API. (Hoặc sử dụng công cụ mới `SQLModel` do chính tác giả FastAPI viết để gộp 2 cái này lại an toàn).
2. **Không khóa phiên bản (Dependency Hell)**: Hệ sinh thái Python cực kỳ nổi tiếng với việc cập nhật làm gãy code cũ (Breaking changes). Hôm nay code chạy bình thường, tháng sau Pydantic ra bản 2.0, tự động cập nhật là sập toàn bộ Server. Luôn dùng `requirements.txt` với phiên bản đóng đinh cứng `fastapi==0.103.0`, hoặc dùng công cụ hiện đại như `Poetry` để quản lý.

</details>

1. **The ORM vs Validation Schema Overlap**: Junior developers often attempt to use a single class for both Database ORM mapping (SQLAlchemy) and API Request validation (Pydantic). This creates catastrophic tight coupling. **Rule**: Enforce strict separation. `models.py` contains SQLAlchemy classes interacting with PostgreSQL. `schemas.py` contains Pydantic models (DTOs) dictating the exact JSON structure the API accepts/returns. (Alternatively, utilize the creator's `SQLModel` library, which safely marries the two paradigms).
2. **Dependency Management Chaos (The Python Ecosystem)**: Python environments are notoriously fragile. A random update to a transitive dependency (like `anyio` or `pydantic`) can cause breaking changes that destroy CI/CD pipelines. **The Fix**: Never deploy using a loose `requirements.txt`. Utilize modern dependency resolvers like **Poetry** or **Pipenv** which generate a cryptographic `lockfile`, guaranteeing that Production executes the exact same mathematical binary versions as your Local environment.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cách tạo API, Schema Pydantic và Dependency Injection trong FastAPI.
</details>

### Server Setup & Pydantic Schemas (`main.py`)
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI(title="My Super API")

# 1. Define the Input/Output Schema (Pydantic DTO)
# Pydantic will mathematically validate this. If price is a string, it throws 422.
class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    is_active: bool = True       # Default value
    description: Optional[str] = None # Optional field

# Mock Database
fake_db: List[ProductSchema] = []

# 2. CREATE (POST) Endpoint
# Simply injecting 'ProductSchema' triggers the entire validation engine and Swagger UI update.
@app.post("/products/", response_model=ProductSchema, status_code=201)
async def create_product(product: ProductSchema):
    fake_db.append(product)
    return product

# 3. READ (GET) Endpoint with URL Query Parameters
@app.get("/products/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int): # Automatically converts string URL to int!
    for p in fake_db:
        if p.id == product_id:
            return p
    # Standard way to throw errors
    raise HTTPException(status_code=404, detail="Product not found")
```

### Dependency Injection (Authentication Example)
FastAPI elegantly handles middleware concepts using `Depends()`.

```python
from fastapi import Header

# Dependency Function
async def verify_api_key(x_token: str = Header(...)):
    if x_token != "SECRET_KEY_123":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_token

# The Dependency is injected. The route will NOT run if the Dependency fails.
@app.delete("/products/{product_id}")
async def delete_product(product_id: int, token: str = Depends(verify_api_key)):
    # If we reach here, we are guaranteed the token is valid.
    return {"message": f"Product {product_id} deleted securely."}
```

### Running the Server (Uvicorn)
FastAPI does not have a built-in server. You must use an ASGI server like Uvicorn.
```bash
# In terminal. --reload automatically restarts server on code change.
uvicorn main:app --reload
```

---

## Related Topics

- FastAPI is predominantly used to wrap AI models built in **Python**.
- For managing the Relational data, see **[PostgreSQL](../databases/postgresql.md)**.
- For managing massive, stateful enterprise systems, compare it with **[Spring Boot (Java)](./spring-boot.md)**.
