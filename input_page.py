import streamlit as st

# ---------------------------
# 2️⃣ 사용자 정보 입력 단계별 UI
# ---------------------------

GENRES_BY_BOOK_TYPE = {
    "종이책": ["전체", "경제 경영", "소설/시/희곡", "사회 정치", "에세이", "여행", "역사", "예술", "인문", "자기계발", "자연과학", "IT모바일"],
    "e북": ["전체", "경제 경영", "에세이 시", "인문", "사회 정치", "자기계발", "역사", "예술 대중문화", "자연과학", "IT모바일"],
    "오디오북": ["오디오북"]
}

def show_input():
    st.title("👤 간단한 정보를 입력해주세요")

    # 성별
    if st.session_state.step >= 1:
        gender = st.selectbox("성별", ["선택하세요", "남성", "여성"], key="gender")
        if gender != "선택하세요" and st.session_state.step == 1:
            st.session_state.step = 2
            st.rerun()

    # 연령대
    if st.session_state.step >= 2:
        age_group = st.selectbox("연령대", ["선택하세요", "10대", "20대", "30대", "40대", "50대 이상"], key="age_group")
        if age_group != "선택하세요" and st.session_state.step == 2:
            st.session_state.step = 3
            st.rerun()

# 책 형태 선택
    if st.session_state.step >= 3:
        book_types = st.selectbox(
            "어떤 책 형태를 추천해드릴까요?",
            ["선택하세요", "종이책", "e북", "오디오북"],
            key="book_types"
        )

        if book_types != "선택하세요" and st.session_state.step == 3:
            st.session_state.step = 4
            st.rerun()

    # 선호 장르 선택 (책 형태에 따라 다르게)
    if st.session_state.step >= 4:
        selected_book_type = st.session_state.get("book_types", "종이책")
        available_genres = GENRES_BY_BOOK_TYPE.get(selected_book_type, [])

        if selected_book_type != "오디오북":   
            genre = st.selectbox(
                f"{selected_book_type}에서 선호하는 장르를 선택해주세요",
                options=available_genres,
                key="genre"
            )

            if genre and st.session_state.step == 4:
                st.session_state.step = 5
                st.rerun()
        else:
            if st.session_state.step == 4:
                st.session_state.step = 5
                st.rerun()
                
    if st.session_state.step >= 5:
        st.markdown("---")
        st.success("모든 정보 입력이 완료되었습니다!")
        if st.button("📚 도서 추천 받기"):
            go_to_recommend_page()


# 페이지 전환 함수
def go_to_recommend_page():
    st.session_state.page = 'recommend'