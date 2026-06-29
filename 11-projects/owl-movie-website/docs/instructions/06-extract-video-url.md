# Hướng dẫn Cập nhật: Trích xuất Video URL (Deep Crawl)

Nhận xét của bạn rất sắc sảo! Một hệ thống chiếu phim mà không lấy được link nguồn video thì... đâu còn là web phim. 

Để giải quyết vấn đề này, Crawler của chúng ta phải làm thêm một bước gọi là **Deep Crawl** (cào sâu): Từ trang chủ, lấy link của trang chi tiết phim, sau đó truy cập vào trang chi tiết phim để bóc tách link Embed Video (ví dụ: `https://embed.streamxx.net/...`).

Bạn cần cập nhật lại 2 file sau đây:

---

## 1. Cập nhật Crawler (`topxx_crawler.py`)

- **Where**: `d:\Codin\projects\engineering-knowledge\11-projects\owl-movie-website\data_pipeline\ingestion\topxx_crawler.py`
- **What**: Thêm trường `video_url` vào DTO và thêm logic truy cập trang chi tiết để lấy link Embed.
- **Full Code**:
```python
import json
import os
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import datetime
import time

@dataclass
class MovieDTO:
    id: str
    title: str
    original_title: str
    actors: List[str]
    genres: List[str]
    country: str
    video_url: str  # BỔ SUNG TRƯỜNG NÀY
    crawled_at: str

class TopxxSourceAdapter:
    def __init__(self, base_url: str = "https://topxx.vip"):
        self.base_url = base_url

    def fetch_movies(self, limit: int = 2) -> List[MovieDTO]:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(self.base_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        movies = []
        rows = soup.select("table#list-movies tbody tr.tpx-row")

        for row in rows[:limit]:
            title_elem = row.select_one(".tpx-title")
            title = title_elem.text.strip() if title_elem else "Unknown"
            
            sub_elems = row.select(".tpx-sub")
            original_title = sub_elems[0].text.strip().strip("()") if len(sub_elems) > 0 else ""
            movie_id = sub_elems[1].text.replace("ID:", "").strip() if len(sub_elems) > 1 else ""
            
            actor_elems = row.select(".tpx-col-actors .tpx-avatar")
            actors = [a.get("title", "").strip() for a in actor_elems if a.get("title")]

            genre_elems = row.select(".tpx-tag")
            genres = [g.text.strip() for g in genre_elems]

            country_elem = row.select_one(".tpx-col-country img")
            country = country_elem.get("alt", "").strip() if country_elem else "Unknown"

            # BƯỚC MỚI: DEEP CRAWL LẤY VIDEO URL
            video_url = ""
            detail_link_elem = row.select_one(".tpx-titleLink")
            if detail_link_elem and detail_link_elem.get("href"):
                detail_url = detail_link_elem.get("href")
                try:
                    # Truy cập vào trang chi tiết phim
                    detail_res = requests.get(detail_url, headers=headers)
                    detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
                    # Tìm nút "Xem phim" chứa link embed
                    btn_play = detail_soup.select_one("a.btn-primary")
                    if btn_play and btn_play.get("href"):
                        video_url = btn_play.get("href")
                    # Nghỉ 1 chút để tránh bị server block vì request quá nhanh
                    time.sleep(1)
                except Exception as e:
                    print(f"Lỗi khi crawl detail {detail_url}: {e}")

            dto = MovieDTO(
                id=movie_id, title=title, original_title=original_title,
                actors=actors, genres=genres, country=country,
                video_url=video_url, # BỔ SUNG VÀO DTO
                crawled_at=datetime.datetime.utcnow().isoformat()
            )
            movies.append(dto)
        return movies

def run_crawler():
    adapter = TopxxSourceAdapter()
    movies = adapter.fetch_movies(limit=2)
    
    raw_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'topxx')
    os.makedirs(raw_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(raw_dir, f"movies_raw_{timestamp}.jsonl")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for movie in movies:
            f.write(json.dumps(asdict(movie), ensure_ascii=False) + '\n')
            
    print(f"✅ Đã cào {len(movies)} phim (kèm Video URL) và lưu tại {output_path}")

if __name__ == "__main__":
    run_crawler()
```

- **Why**: Trang chủ chỉ chứa meta-data. Cần truy cập sâu (Deep Crawl) vào `detail_url` để DOM tree hiển thị nút `a.btn-primary` (nơi chứa iframe/embed video).
- **Impact**: Tăng thời gian chạy của Crawler (vì có thêm network requests và `time.sleep()`), nhưng đổi lại Data Lake của chúng ta đã nắm giữ giá trị cốt lõi nhất của bộ phim: Video Link.

---

## 2. Cập nhật Storage (`load_to_warehouse.py`)

- **Where**: `d:\Codin\projects\engineering-knowledge\11-projects\owl-movie-website\data_pipeline\storage\load_to_warehouse.py`
- **What**: Cập nhật lại Schema trong ORM để nhận thêm trường `video_url`.
- **Full Code**: (Bạn chỉ cần chép đè đoạn định nghĩa Class FactMovie, các phần khác giữ nguyên)

```python
# 1. ORM Model: Định nghĩa schema của Data Warehouse
class FactMovie(Base):
    __tablename__ = 'fact_movies'
    
    id = Column(String, primary_key=True)
    title = Column(String)
    original_title = Column(String)
    country = Column(String)
    video_url = Column(String) # BỔ SUNG TRƯỜNG NÀY
    crawled_at = Column(DateTime)
    processed_at = Column(DateTime)
    actors_str = Column(String)
    genres_str = Column(String)
```
- **Why**: Data Warehouse cần được update cấu trúc cột để lưu trữ thuộc tính mới truyền sang từ Processing layer (Lưu ý file `clean_topxx_data.py` tự động đọc mọi trường JSON sang Parquet nên không cần sửa code).
- **Impact**: Do script chúng ta dùng `if_exists='replace'` nên khi chạy lại, Pandas sẽ xóa bảng cũ và tạo bảng mới chứa đầy đủ cột `video_url`.

---
## Test sự thay đổi
Sau khi thay đổi 2 file trên, bạn hãy mở Terminal và chạy lại Pipeline bằng tay (hoặc vào Airflow Trigger chạy lại DAG).

```bash
.\.venv\Scripts\python.exe data_pipeline/ingestion/topxx_crawler.py
.\.venv\Scripts\python.exe data_pipeline/processing/clean_topxx_data.py
.\.venv\Scripts\python.exe data_pipeline/storage/load_to_warehouse.py
```
Mở Database lên kiểm tra, bạn sẽ thấy cột `video_url` xuất hiện!
