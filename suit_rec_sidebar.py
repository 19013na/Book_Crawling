import streamlit as st
from input_page import GENRES_BY_BOOK_TYPE
from suit_crawling_page import get_bestsellers  # 크롤링 함수 임포트
from suit_category_map import PAPERBOOK_CATEGORY_MAP, EBOOK_CATEGORY_MAP, GENDER_MAP, AGE_MAP

# ---------------------------
# 🎯 사이드바: 장르 재선택
# ---------------------------

def show_sidebar():
    st.sidebar.header("🎯 추천 조건 변경")

    # 추천 개수 슬라이더 (선택값 저장 X)
    num_items_best = st.sidebar.slider("📚 작품 개수", min_value=1, max_value=20, value=10)

    # 책 형태
    book_type = st.sidebar.selectbox(
        "📘 책 형태",
        ["종이책", "e북", "오디오북"],
        index=["종이책", "e북", "오디오북"].index(st.session_state.get("book_types", "종이책")),
        key="book_types"
    )

    # 성별
    gender = st.sidebar.selectbox(
        "👤 성별",
        ["남성", "여성"],
        index=["남성", "여성"].index(st.session_state.get("gender", "남성")),
        key="gender"
    )

    # 연령대
    age_options = ["전체", "10대", "20대", "30대", "40대", "50대 이상"]
    age_group = st.sidebar.selectbox(
        "🎂 연령대",
        age_options,
        index=age_options.index(st.session_state.get("age_group", "전체")),
        key="age_group"
    )

    # 장르
    if book_type == "오디오북":
        genre_name = "전체"
    else:
        genre_options = list(PAPERBOOK_CATEGORY_MAP.keys()) if book_type == "종이책" else list(EBOOK_CATEGORY_MAP.keys())
        default_genre = st.session_state.get("genre", genre_options[0])
        genre_name = st.sidebar.selectbox("🎯 장르", genre_options, index=genre_options.index(default_genre), key="genre")

    # 첫 페이지로 돌아가기 버튼
    st.sidebar.markdown("---")  # 간격 띄우기용 구분선
    if st.sidebar.button("🔙 첫 페이지 가기"):
        st.session_state.clear()
        st.rerun()

    return book_type, gender, age_group, genre_name, num_items_best
