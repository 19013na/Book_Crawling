import streamlit as st
from input_page import GENRES_BY_BOOK_TYPE
from suit_crawling_page import get_bestsellers  # 크롤링 함수 임포트
from suit_category_map import PAPERBOOK_CATEGORY_MAP, EBOOK_CATEGORY_MAP, GENDER_MAP, AGE_MAP

# ---------------------------
# 3️⃣ 추천 결과 페이지
# ---------------------------

def show_recommend():
    st.title("✨ 추천 도서 리스트")
    st.markdown("당신이 입력한 정보를 기반으로 다음과 같은 도서를 추천드립니다. 📖")

    # 사이드바 슬라이더
    st.sidebar.header("🎯 추천 조건 변경")
    num_items_best = st.sidebar.slider("작품 개수", min_value=5, max_value=10, value=10)

    # 세션 값 불러오기
    book_type = st.session_state.get("book_types", None)
    gender = st.session_state.get("gender", None)
    age_group = st.session_state.get("age_group", None)
    genre_name = st.session_state.get("genre", None)
    
    # 세션 값 초기화되지 않게 다시 저장
    st.session_state["book_types"] = st.session_state.get("book_types")
    st.session_state["gender"] = st.session_state.get("gender")
    st.session_state["age_group"] = st.session_state.get("age_group")
    st.session_state["genre"] = st.session_state.get("genre", "전체")

    # 성별/연령대 변환
    sex = GENDER_MAP.get(gender, "")
    age = AGE_MAP.get(age_group, "")

    # 책 형식 및 장르 변환
    if book_type == "오디오북":
        st.sidebar.info("오디오북은 장르 선택 없이 추천됩니다.")
        return "전체", "017001008"
    genre_number = PAPERBOOK_CATEGORY_MAP.get(genre_name, "해당 장르는 존재하지 않습니다.") if book_type == "종이책" else EBOOK_CATEGORY_MAP.get(genre_name, "해당 장르는 존재하지 않습니다.")


    # 데이터 가져오기
    df = get_bestsellers(category_number=genre_number, sex=sex, age=age)

    st.markdown(f"{age_group} {gender}를 위한 {book_type} '{genre_name}' 장르 추천 도서")

    # 추천 도서 출력
    st.subheader("📚 베스트셀러 추천")
    if df.empty:
        st.info("추천 도서를 불러올 수 없습니다 😥")
    else:
        for _, row in df.head(num_items_best).iterrows():  # 슬라이더 값 사용
            st.markdown(f"**{row['순위']}. {row['제목']}**")
            st.markdown(f"- 저자: {row['저자']} / 출판사: {row['출판사']} / 출간일: {row['출간일']}")
            st.markdown(f"[📖 상세보기]({row['링크']})")
            st.markdown("---")

    # 첫 페이지로 돌아가기 버튼
    if st.button("첫 페이지로 돌아가기"):
        st.session_state.clear()
        st.rerun()
