# Hướng dẫn: Xây dựng Storage Layer (Nạp dữ liệu vào Data Warehouse)

Tuyệt vời! Bạn đã có file Parquet sạch sẽ. Bước tiếp theo là **Storage Layer** (hay còn gọi là Load trong quy trình ETL). Chúng ta sẽ nạp file Parquet này vào **PostgreSQL** Data Warehouse mà bạn đã tạo bằng Docker.

- **Where**: `d:\Codin\projects\engineering-knowledge\11-projects\owl-movie-website\data_pipeline\storage\load_to_warehouse.py`

- **What**: 
  1. Tạo thư mục `data_pipeline/storage/`.
  2. Tạo file `load_to_warehouse.py`.
  3. Định nghĩa **SQLAlchemy ORM** cho bảng `fact_movies`.
  4. Đọc file Parquet mới nhất từ thư mục `data/processed/topxx/` và đẩy vào DB.

- **Full Code**:
```python
import os
import glob
import pandas as pd
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# 1. ORM Model: Định nghĩa schema của Data Warehouse
class FactMovie(Base):
    __tablename__ = 'fact_movies'
    
    id = Column(String, primary_key=True)
    title = Column(String)
    original_title = Column(String)
    country = Column(String)
    crawled_at = Column(DateTime)
    processed_at = Column(DateTime)
    actors_str = Column(String)
    genres_str = Column(String)

class WarehouseRepository:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        # Tự động tạo bảng nếu chưa có
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def load_dataframe(self, df: pd.DataFrame):
        """Sử dụng tính năng to_sql của Pandas kết hợp SQLAlchemy để nạp data."""
        # Upsert hoặc Replace tùy theo chiến lược, ở đây dùng 'append' hoặc 'replace'
        # Do là dự án test, ta có thể tạm thời 'replace' toàn bộ bảng hoặc 'append'
        # Tuy nhiên do có Primary Key, dùng 'append' trên pandas thẳng có thể bị lỗi trùng lặp.
        # Nhưng để đơn giản lúc học, cứ nạp vào xem sao:
        with self.engine.begin() as conn:
            df.to_sql('fact_movies', con=conn, if_exists='replace', index=False)
        print(f"✅ Đã nạp thành công {len(df)} dòng vào Data Warehouse!")

def get_latest_parquet_file(processed_dir: str) -> str:
    list_of_files = glob.glob(os.path.join(processed_dir, '*.parquet'))
    if not list_of_files:
        raise FileNotFoundError("Không tìm thấy file Parquet nào!")
    return max(list_of_files, key=os.path.getctime)

def run_loader():
    base_dir = os.path.dirname(__file__)
    processed_dir = os.path.join(base_dir, '..', '..', 'data', 'processed', 'topxx')
    
    # URL kết nối tới Postgres warehouse (port 5433 như bạn thiết lập trong docker-compose)
    DATABASE_URL = "postgresql+psycopg2://owldb:owldb@localhost:5433/owldb"
    
    repo = WarehouseRepository(DATABASE_URL)
    
    latest_file = get_latest_parquet_file(processed_dir)
    print(f"Đang nạp file: {latest_file} vào Data Warehouse...")
    
    df = pd.read_parquet(latest_file)
    repo.load_dataframe(df)

if __name__ == "__main__":
    run_loader()
```

- **Why**: 
  - **SQLAlchemy (ORM) & Repository Pattern**: Tách biệt logic kết nối DB và logic xử lý dữ liệu. Nếu sau này backend của bạn cần kết nối vào DB này, nó có thể dùng chung cấu trúc Model này.
  - **to_sql()**: Pandas hỗ trợ tích hợp sâu với SQLAlchemy, cho phép biến một Dataframe thành các câu lệnh `INSERT` hàng loạt vào SQL rất dễ dàng.

- **Impact**: 
  Dữ liệu giờ đây đã chính thức sẵn sàng trong Data Warehouse (Postgres) dưới dạng bảng `fact_movies` có cấu trúc cứng. Backend hoặc Frontend có thể query từ bảng này ra để phục vụ người dùng web.

---
**Nhiệm vụ của bạn:**
1. Cài driver để Python kết nối PostgreSQL: 
   `.\.venv\Scripts\python.exe -m pip install sqlalchemy psycopg2-binary`
2. Tạo file `load_to_warehouse.py`, copy **Full Code** và chạy:
   `.\.venv\Scripts\python.exe data_pipeline/storage/load_to_warehouse.py`
3. Bạn có thể dùng công cụ như **DBeaver** hoặc **pgAdmin** kết nối vào `localhost:5433` (User: `owldb`, Pass: `owldb`) để tận mắt thấy dữ liệu đã được lưu trong Database nhé!
