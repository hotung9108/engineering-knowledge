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