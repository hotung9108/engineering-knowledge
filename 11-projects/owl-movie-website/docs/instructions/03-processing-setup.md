# Hướng dẫn: Xây dựng Processing Layer (Làm sạch dữ liệu)

Chúc mừng bạn đã crawl thành công! Data thô (JSONL) hiện đã nằm an toàn trong Data Lake (thư mục `data/raw/`). Bước tiếp theo là **Processing Layer**, nơi chúng ta dùng **Pandas** để đọc raw data, chuẩn hóa và xuất ra định dạng **Parquet**.

- **Where**: `d:\Codin\projects\engineering-knowledge\11-projects\owl-movie-website\data_pipeline\processing\clean_topxx_data.py`

- **What**: 
  1. Tạo thư mục `data_pipeline/processing/` (nếu chưa có).
  2. Tạo file `clean_topxx_data.py` để tìm file JSONL mới nhất trong `data/raw/`, đọc bằng Pandas.
  3. Làm sạch dữ liệu (ví dụ: chuyển title thành viết hoa chữ cái đầu, thay thế giá trị Unknown).
  4. Lưu output ra file `.parquet` trong `data/processed/topxx/`.

- **Full Code**:
```python
import os
import glob
import pandas as pd
import datetime

def get_latest_raw_file(raw_dir: str) -> str:
    """Tìm file jsonl mới nhất trong thư mục raw."""
    list_of_files = glob.glob(os.path.join(raw_dir, '*.jsonl'))
    if not list_of_files:
        raise FileNotFoundError("Không tìm thấy file raw data nào!")
    # Lấy file được tạo gần nhất
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def process_data():
    base_dir = os.path.dirname(__file__)
    raw_dir = os.path.join(base_dir, '..', '..', 'data', 'raw', 'topxx')
    processed_dir = os.path.join(base_dir, '..', '..', 'data', 'processed', 'topxx')
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Đọc dữ liệu thô mới nhất
    latest_file = get_latest_raw_file(raw_dir)
    print(f"Đang đọc dữ liệu từ: {latest_file}")
    df = pd.read_json(latest_file, lines=True)

    # 2. Cleaning & Transformation
    # Chuẩn hóa title: Trim khoảng trắng
    df['title'] = df['title'].str.strip()
    
    # Chuẩn hóa country: Nếu rỗng thì đổi thành 'Unknown'
    df['country'] = df['country'].fillna('Unknown')
    
    # Đối với actors và genres, dữ liệu đang là list, ta sẽ chuyển thành string cách nhau bởi dấu phẩy
    # Điều này giúp dễ dàng load vào Database ở bước sau nếu không dùng kiểu Array của Postgres.
    df['actors_str'] = df['actors'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
    df['genres_str'] = df['genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
    
    # Thêm cột processed_at để tracking
    df['processed_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Xóa 2 cột list cũ để bản ghi phẳng (flat)
    df = df.drop(columns=['actors', 'genres'])

    # 3. Xuất ra định dạng Parquet
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(processed_dir, f"movies_clean_{timestamp}.parquet")
    
    df.to_parquet(output_file, engine='pyarrow', index=False)
    print(f"✅ Đã làm sạch và lưu {len(df)} bản ghi thành file Parquet tại: {output_file}")

if __name__ == "__main__":
    process_data()
```

- **Why**: 
  - **Pandas**: Nhanh, nhẹ, xử lý Dataframe cực kỳ linh hoạt (phù hợp với data vừa và nhỏ).
  - **Parquet Format**: Đây là chuẩn định dạng lưu trữ cột (Columnar Storage) của Data Engineering. Nó nén dữ liệu nhỏ hơn JSON nhiều lần, giữ nguyên kiểu dữ liệu (Data types), và tối ưu cực tốt cho việc truy vấn (OLAP).
  - **Biến đổi List thành String**: Giúp việc đẩy vào bảng Fact/Dimension của Data Warehouse SQL ở bước sau đơn giản hơn trong ví dụ thực hành này.

- **Impact**: 
  Dữ liệu từ Raw Data Lake đã được tinh chỉnh thành dạng bảng (Tabular) tiêu chuẩn, sẵn sàng để nạp (Load) vào PostgreSQL Data Warehouse.

---
**Nhiệm vụ của bạn:**
1. Cài đặt các thư viện cần thiết bằng lệnh: `pip install pandas pyarrow` (nếu chưa cài).
2. Tạo file `clean_topxx_data.py`, dán **Full Code** vào và chạy thử bằng `python data_pipeline/processing/clean_topxx_data.py`.
3. Kiểm tra xem thư mục `data/processed/topxx/` đã xuất hiện file `.parquet` hay chưa, rồi báo lại cho tôi nhé!
