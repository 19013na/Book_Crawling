import streamlit as st
from input_page import GENRES_BY_BOOK_TYPE
from suit_crawling_page import get_bestsellers  # 크롤링 함수 임포트
from suit_category_map import PAPERBOOK_CATEGORY_MAP, EBOOK_CATEGORY_MAP, GENDER_MAP, AGE_MAP
from suit_rec_sidebar import show_sidebar_genre_selector

# ---------------------------
# 3️⃣ 추천 결과 페이지
# ---------------------------

def show_recommend():
    st.title("✨ 추천 도서 리스트")
    st.markdown("당신이 입력한 정보를 기반으로 다음과 같은 도서를 추천드립니다. 📖")
    
    selected_book_type = st.session_state.get("book_types", "종이책")
    gender = st.session_state.get("gender")
    age_group = st.session_state.get("age_group")
    default_genre = st.session_state.get("genre", "전체")

    # 🎯 genre를 기반으로 사이드바 표시 및 현재 장르, 카테고리 번호 반환
    selected_genre, category_number = show_sidebar_genre_selector(selected_book_type, default_genre)
    
    # 성별/연령대 변환
    sex = GENDER_MAP.get(gender, "")
    age = AGE_MAP.get(age_group, "")

    # 데이터 불러오기
    df = get_bestsellers(category_number=category_number, sex=sex, age=age)

    st.markdown(f"{age_group} {gender}를 위한 {selected_book_type} {selected_genre}")

    # 추천 출력
    st.subheader("📚 베스트셀러 추천")
    if df.empty:
        st.info("추천 도서를 불러올 수 없습니다 😥")
    else:
        st.markdown(f"**'{selected_genre}' 장르 추천 도서 목록**")
        for _, row in df.iterrows():
            st.markdown(f"**{row['순위']}. {row['제목']}**")
            st.markdown(f"- 저자: {row['저자']} / 출판사: {row['출판사']} / 출간일: {row['출간일']}")
            st.markdown(f"[📖 상세보기]({row['링크']})")
            st.markdown("---")
