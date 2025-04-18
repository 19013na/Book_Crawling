import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

def get_bestsellers(category_number=None, sex=None, age=None, max_items=10):
    
    # 카테고리가 없으면 종합 베스트셀러 가져오기 - 전체: 001
    category_number = category_number or "001"
    url = f'https://www.yes24.com/Product/Category/DayBestSeller?categoryNumber={category_number}'
    
    # 오디오북 설정 필요 - 장르 설정 X

    # 성별 및 나이 조건 추가
    if sex: url += f"&sex={sex}"
    if age: url += f"&age={age}"

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    book_items = soup.select("div.itemUnit")[:max_items]
    book_list = []
    
    for item in book_items:
        try:
            rank = item.select_one(".ico.rank").text
            title_tag = item.select_one(".gd_name")
            author = item.select_one("a[href*='author=']").text
            publisher = item.select_one("a[href*='company=']").text
            date = item.select_one(".authPub.info_date").text

            if not all([rank, title_tag, author, publisher, date]):
                continue

            title = title_tag.text.strip()
            link = "https://www.yes24.com" + title_tag["href"]
            
            book_list.append({
                "순위": rank,
                "제목": title,
                "저자": author,
                "출판사": publisher,
                "출간일": date,
                "링크": link
            })
        except Exception:
            continue

    return pd.DataFrame(book_list)