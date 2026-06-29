# Hướng dẫn: Cài đặt Docker Compose cho Data Pipeline

Chào bạn! Dựa trên bản thiết kế đã duyệt, đây là hướng dẫn chi tiết để bạn tự tay viết file `docker-compose.yml`. Bạn hãy tạo file và làm theo cấu trúc sau nhé:

- **Where**: `d:\Codin\projects\engineering-knowledge\11-projects\owl-movie-website\docker-compose.yml`

- **What**: Khởi tạo file `docker-compose.yml` (version '3.8') bao gồm 3 services chính: Postgres (Warehouse), MinIO (Data Lake) và Airflow.

- **Full Code**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 10s
      retries: 5
      start_period: 5s

  # Data Warehouse DB (Tách biệt khỏi Airflow DB)
  warehouse:
    image: postgres:15
    environment:
      - POSTGRES_USER=owldb
      - POSTGRES_PASSWORD=owldb
      - POSTGRES_DB=owldb
    volumes:
      - warehouse_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  # Data Lake
  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=admin
      - MINIO_ROOT_PASSWORD=password
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

  airflow-init:
    image: apache/airflow:2.7.1
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
    command: version
    entrypoint:
      - bash
      - -c
      - |
        airflow db init
        airflow users create \
          --username admin \
          --password admin \
          --firstname Admin \
          --lastname User \
          --role Admin \
          --email admin@example.com

  airflow-webserver:
    image: apache/airflow:2.7.1
    depends_on:
      airflow-init:
        condition: service_completed_successfully
    environment:
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
    ports:
      - "8080:8080"
    volumes:
      - ./data_pipeline/dags:/opt/airflow/dags
      - ./data_pipeline:/opt/airflow/data_pipeline
      - ./data:/opt/airflow/data
    command: webserver

  airflow-scheduler:
    image: apache/airflow:2.7.1
    depends_on:
      airflow-init:
        condition: service_completed_successfully
    environment:
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
    volumes:
      - ./data_pipeline/dags:/opt/airflow/dags
      - ./data_pipeline:/opt/airflow/data_pipeline
      - ./data:/opt/airflow/data
    command: scheduler

volumes:
  postgres_data:
  warehouse_data:
  minio_data:
```

- **Why**: 
  - **Docker Compose** giúp chuẩn hóa môi trường local.
  - Việc tách riêng DB của Airflow (Metadata DB) và `warehouse` (DB chứa dữ liệu phim thực tế) giúp hệ thống tuân thủ nguyên tắc **Decoupling** trong Data Engineering.
  - MinIO đóng vai trò là **Data Lake** lưu trữ raw JSON/video, cung cấp S3-compatible API.

- **Impact**: 
  Chỉ với 1 lệnh `docker-compose up -d`, toàn bộ hệ sinh thái lưu trữ (Lake + Warehouse) sẽ được khởi động. Hệ thống Crawler và Backend sau này sẽ phụ thuộc vào các thông số Port/User/Pass mà bạn định nghĩa tại đây.

---

**Nhiệm vụ của bạn:**
Hãy tạo/mở file `docker-compose.yml`, copy đoạn **Full Code** trên dán vào, sau đó chạy lệnh `docker-compose up -d`. 
Nếu gặp khó khăn về cú pháp YAML hay lỗi lúc chạy lệnh, hãy báo cho tôi để tôi hướng dẫn bạn debug nhé!
