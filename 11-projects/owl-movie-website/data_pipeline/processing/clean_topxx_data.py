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