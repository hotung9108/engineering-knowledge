# Hướng dẫn: Điều phối Data Pipeline bằng Apache Airflow

Tuyệt vời! Bạn đã hoàn thành 3 module độc lập: Cào dữ liệu (Ingestion), Làm sạch (Processing), và Nạp DB (Storage). 
Nhưng một Data Engineer không chạy script bằng tay mỗi ngày. Chúng ta dùng **Apache Airflow** để lập lịch tự động chạy 3 script đó theo một chuỗi (DAG).

- **Where**: `d:\Codin\projects\engineering-knowledge\11-projects\owl-movie-website\data_pipeline\dags\topxx_dag.py`

- **What**: 
  1. Tạo thư mục `data_pipeline/dags/`.
  2. Tạo file `topxx_dag.py`.
  3. Khai báo DAG `topxx_movie_pipeline` chạy mỗi ngày một lần.
  4. Tạo các Task liên kết với nhau bằng toán tử `>>`.

- **Full Code**:
```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'topxx_movie_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1), # Chạy mỗi ngày 1 lần
    catchup=False,
    tags=['owl-movie', 'data-engineering'],
) as dag:

    # 0. Do Airflow chạy trong container Docker mặc định chưa có các thư viện Data.
    # Để môi trường local học tập dễ dàng nhất, ta dùng 1 task để cài thư viện vào container trước khi chạy.
    # Trong môi trường thực tế (Production), bạn sẽ build một custom Dockerfile cài sẵn thư viện.
    install_reqs = BashOperator(
        task_id='install_requirements',
        bash_command='pip install beautifulsoup4 pandas pyarrow sqlalchemy psycopg2-binary'
    )

    # 1. Task Crawler
    # Lưu ý: docker-compose đã mount thư mục lên /opt/airflow/
    crawl_task = BashOperator(
        task_id='crawl_movies',
        bash_command='python /opt/airflow/data_pipeline/ingestion/topxx_crawler.py'
    )

    # 2. Task Cleaning (Pandas to Parquet)
    clean_task = BashOperator(
        task_id='clean_data',
        bash_command='python /opt/airflow/data_pipeline/processing/clean_topxx_data.py'
    )

    # 3. Task Loading (Parquet to Postgres Data Warehouse)
    # Lưu ý: Trong docker, host của Postgres warehouse tên là "warehouse", port là 5432 (port nội bộ docker)
    # Tuy nhiên code Storage Layer của bạn đang ghi hardcode là localhost:5433 (để chạy ngoài máy host).
    # Không sao cả, để demo tính năng Airflow, nếu chạy lỗi ta có thể sửa URL kết nối sau.
    load_task = BashOperator(
        task_id='load_to_warehouse',
        bash_command='python /opt/airflow/data_pipeline/storage/load_to_warehouse.py'
    )

    # Thiết lập luồng chạy (Lineage / Dependencies)
    install_reqs >> crawl_task >> clean_task >> load_task
```

- **Why**: 
  - **DAG (Directed Acyclic Graph)**: Biểu diễn quy trình chuẩn, nếu `crawl_task` bị lỗi, `clean_task` sẽ không bao giờ chạy, tránh sinh ra data rác.
  - **BashOperator**: Trong môi trường này, thay vì import code trực tiếp (có thể dính lỗi import scope), ta gọi Bash chạy thẳng các script Python mà bạn đã test ở bước trước. Cách này tuân thủ nguyên tắc "Decoupled".

- **Impact**: 
  Thay vì bạn phải ngồi canh gõ lệnh từng bước, Airflow sẽ tự động điều phối toàn bộ vòng đời của dữ liệu.

---
**Nhiệm vụ của bạn:**
1. Tạo file `topxx_dag.py` và dán **Full Code** vào.
2. Mở trình duyệt, truy cập vào giao diện quản lý Airflow tại: **http://localhost:8080**
3. Đăng nhập bằng `admin` / `admin` (Như đã khai báo ở docker-compose lúc đầu).
4. Tìm DAG `topxx_movie_pipeline`, bấm nút **Play (Trigger DAG)** và xem các hình vuông chuyển sang màu xanh lá cây 🟢 là thành công toàn tập hệ thống Data Engineering!
