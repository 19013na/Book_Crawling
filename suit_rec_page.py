import streamlit as st
from input_page import GENRES_BY_BOOK_TYPE
from suit_crawling_page import get_bestsellers  # 크롤링 함수 임포트
from suit_category_map import PAPERBOOK_CATEGORY_MAP, EBOOK_CATEGORY_MAP, GENDER_MAP, AGE_MAP

# ---------------------------
# 3️⃣ 추천 결과 페이지
# ---------------------------

def show_recommend():
    st.title("✨ 추천 도서 리스트")

    st.markdown("""
당신이 입력한 정보를 기반으로  
다음과 같은 도서를 추천드립니다. 📖
""")

    # 세션에서 사용자 정보 추출
    selected_genre = st.session_state.get("genre", None)
    selected_book_type = st.session_state.get("book_types", "종이책")
    gender = st.session_state.get("gender")
    age_group = st.session_state.get("age_group")

    # 장르 재선택 가능하도록 사이드바 제공
    st.sidebar.header("🎯 장르 다시 선택하기")
    genre_options = GENRES_BY_BOOK_TYPE.get(selected_book_type, [])
    st.sidebar.selectbox(
        "선호 장르를 선택해주세요",
        genre_options,
        key="genre"
    )

    # 장르 없으면 안내
    if not selected_genre:
        st.warning("장르가 선택되지 않았습니다.")
        return

    # 장르 → 카테고리 번호 변환
    if selected_book_type == "종이책":
        category_number = PAPERBOOK_CATEGORY_MAP.get(selected_genre, "001")
    elif selected_book_type == "e북":
        category_number = EBOOK_CATEGORY_MAP.get(selected_genre, "017")
    else:
        pass
    
    # 성별, 나이이
    sex = GENDER_MAP.get(gender, "")
    age = AGE_MAP.get(age_group, "")

    # YES24 데이터 가져오기
    df = get_bestsellers(category_number=category_number, sex=sex, age=age)

    # 도서 추천 출력
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
