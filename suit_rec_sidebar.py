import streamlit as st
from input_page import GENRES_BY_BOOK_TYPE
from suit_crawling_page import get_bestsellers  # 크롤링 함수 임포트
from suit_category_map import PAPERBOOK_CATEGORY_MAP, EBOOK_CATEGORY_MAP, GENDER_MAP, AGE_MAP


# ---------------------------
# 🎯 사이드바: 장르 재선택
# ---------------------------
# def show_sidebar_genre_selector(book_type, default_genre=None):
    
    
#     st.sidebar.header("🎯 장르 선택")

#     if book_type == "오디오북":
#         st.sidebar.info("오디오북은 장르 선택 없이 추천됩니다.")
#         return "전체", "017001008"  # 예시 카테고리

#     genre_options = list(PAPERBOOK_CATEGORY_MAP.keys()) if book_type == "종이책" else list(EBOOK_CATEGORY_MAP.keys())

#     selected_genre = st.sidebar.selectbox(
#         f"{book_type} 장르를 선택해주세요",
#         genre_options,
#         index=genre_options.index(default_genre) if default_genre in genre_options else 0,
#         key="genre"
#     )

#     # 선택된 장르에 따른 카테고리 번호 매핑
#     if book_type == "종이책":
#         category_number = PAPERBOOK_CATEGORY_MAP.get(selected_genre, "001")
#     else:
#         category_number = EBOOK_CATEGORY_MAP.get(selected_genre, "017")

#     return selected_genre, category_number
