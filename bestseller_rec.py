import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner="실시간 베스트셀러를 불러오는 중입니다...")
def fetch_kyobo_bestseller(top_n: int = 10) -> pd.DataFrame:
    """
    교보문고 실시간 베스트셀러 top_n권 크롤링
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = "https://store.kyobobook.co.kr/bestseller/realtime"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    book_items = soup.select("li.mt-9.flex")[:top_n]
    books = []

    for item in book_items:
        try:
            title = item.select_one("a.prod_link.line-clamp-2").get_text(strip=True)
            author_info = item.select_one("div.line-clamp-2.flex").get_text(" ", strip=True)
            author, publisher, pub_date = "", "", ""
            parts = author_info.split("·")
            if len(parts) >= 2:
                author = parts[0].strip()
                publisher = parts[1].strip()
            if len(parts) >= 3:
                pub_date = parts[2].strip()

            price_origin = item.select_one("s.text-gray-700")
            price = price_origin.get_text(strip=True) if price_origin else ""

            description = item.select_one("p.prod_introduction")
            desc = description.get_text(" ", strip=True) if description else ""

            review_score = item.select_one("span.font-bold.text-black")
            score = review_score.get_text(strip=True) if review_score else ""

            review_count = item.select_one("span.font-normal.text-gray-700")
            count = review_count.get_text(strip=True) if review_count else ""

                    # 🔥 진짜 책 이미지 URL 추출
            img_tag = item.select_one("div.relative.flex-shrink-0 img[src*='pdt/']")
            image_url = img_tag['src'] if img_tag else ""
            books.append({
                "title": title,
                "author": author,
                "publisher": publisher,
                "pub_date": pub_date,
                "price": price,
                "description": desc,
                "review_score": score,
                "review_count": count,
                 "이미지": image_url
            })

        except Exception:
            continue
        pd.set_option('display.max_colwidth', None)
    return pd.DataFrame(books)
