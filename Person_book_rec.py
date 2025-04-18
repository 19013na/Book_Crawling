# crawler.py

import requests
import time
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner="셀럽 추천 도서를 불러오는 중입니다...")
def fetch_celebrity_books(pages: int = 2) -> pd.DataFrame:
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://store.kyobobook.co.kr/bestseller/person/daily/domestic",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    session.headers.update(headers)

    # 쿠키 세팅
    session.get("https://store.kyobobook.co.kr/")

    author_list = []

    for page in range(1, pages + 1): 
        url = f"https://store.kyobobook.co.kr/api/gw/best/best-seller/author?page={page}&per=20&period=001&dsplDvsnCode=001&dsplTrgtDvsnCode=002"
        res = session.get(url)

        try:
            data = res.json()
            writers = data.get("data", {}).get("writerList", [])
        except Exception as e:
            st.warning("데이터 파싱 오류 발생")
            continue

        if not writers:
            break

        for item in writers:
            info = item.get("writerInfo", {})
            name = info.get("chrcName", "").strip()
            link = f"https://www.kyobobook.co.kr/search/authorSearch.laf?author={name}"

            # 대표 도서 추출
            book_list = item.get("representativeBook", [])
            book_titles = [book.get("cmdtName", "").strip() for book in book_list if book.get("cmdtName")]
            books = ", ".join(book_titles)

            author_list.append({
                "name": name,
                "link": link,
                "books": books
            })

        time.sleep(1)

    return pd.DataFrame(author_list)
