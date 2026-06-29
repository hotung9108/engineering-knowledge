# Hướng dẫn: Khởi tạo cấu trúc thư mục & Viết Crawler (Data Ingestion)

Chào bạn, bước tiếp theo trong quy trình Data Pipeline của chúng ta là xây dựng lớp Ingestion. Bạn sẽ dùng mô hình Adapter Pattern để code dễ dàng mở rộng sau này.

- **Where**: `d:\Codin\projects\engineering-knowledge\11-projects\owl-movie-website\data_pipeline\ingestion\topxx_crawler.py`

- **What**: 
  1. Tạo thư mục `data_pipeline/ingestion/` (nhớ tạo thêm file `__init__.py` rỗng bên trong).
  2. Tạo file `topxx_crawler.py` sử dụng thư viện `requests` và `BeautifulSoup` để cào dữ liệu từ bảng `table#list-movies` trên trang chủ `topxx.vip`.
  3. Định nghĩa class `MovieDTO` làm data format chuẩn.

- **Full Code**:
```python
import json
import os
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import datetime

@dataclass
class MovieDTO:
    id: str
    title: str
    original_title: str
    actors: List[str]
    genres: List[str]
    country: str
    crawled_at: str

class TopxxSourceAdapter:
    def __init__(self, base_url: str = "https://topxx.vip"):
        self.base_url = base_url

    def fetch_movies(self, limit: int = 2) -> List[MovieDTO]:
        """Cào HTML và parse data cho 1-2 phim để test."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
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

            dto = MovieDTO(
                id=movie_id, title=title, original_title=original_title,
                actors=actors, genres=genres, country=country,
                crawled_at=datetime.datetime.utcnow().isoformat()
            )
            movies.append(dto)
        return movies

def run_crawler():
    adapter = TopxxSourceAdapter()
    movies = adapter.fetch_movies(limit=2)
    
    # Lưu data raw ra file JSONL
    raw_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'topxx')
    os.makedirs(raw_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(raw_dir, f"movies_raw_{timestamp}.jsonl")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for movie in movies:
            f.write(json.dumps(asdict(movie), ensure_ascii=False) + '\n')
            
    print(f"✅ Đã cào {len(movies)} phim và lưu tại {output_path}")

if __name__ == "__main__":
    run_crawler()
```

- **Why**: 
  - **Adapter Pattern** (`TopxxSourceAdapter`): Giúp tách biệt logic lấy dữ liệu (cào web) khỏi dữ liệu chuẩn (`MovieDTO`). Sau này nếu đổi sang API hoặc đổi trang web khác, bạn chỉ cần tạo một Adapter mới.
  - **Data Lake (Raw Tier)**: Lưu trực tiếp ra file JSON dưới máy (thay vì vứt thẳng vào DB) để làm bằng chứng (lineage). Dữ liệu này sau đó sẽ được làm sạch (Pandas) ở bước tiếp theo.

- **Impact**: 
  Cung cấp luồng dữ liệu (Input) đầu tiên cho toàn bộ Data Pipeline. File sinh ra sẽ được nạp vào Processing Layer.

---
**Nhiệm vụ của bạn:**
1. Sửa lại file `docker-compose.yml` (tôi thấy bạn đang sửa dở và có lỗi).
2. Tạo các folder và copy file script crawler bên trên, chạy thử bằng lệnh `python data_pipeline/ingestion/topxx_crawler.py`. (Bạn có thể cài đặt package `requests`, `beautifulsoup4` trước nếu chưa có).
