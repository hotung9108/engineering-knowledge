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