import streamlit as st
import time
from Person_book_rec import fetch_celebrity_books

GENRES_BY_BOOK_TYPE = {
    "종이책": ["경제 경영", "소설/시/희곡", "사회정치", "에세이", "여행", "역사", "예술", "인문", "자기계발", "자연과학", "IT모바일"],
    "e북": ["경제 경영", "에세이 시", "인문", "사회 정치", "자기계발", "역사", "예술 대중문화", "자연과학", "IT모바일"],
    "오디오북": ["오디오북"]
}

# 초기 세션 상태
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'step' not in st.session_state:
    st.session_state.step = 1

# 페이지 전환 함수
def go_to_recommend_page():
    st.session_state.page = 'recommend'

# ---------------------------
# 1️⃣ 인트로 페이지
# ---------------------------
if st.session_state.page == 'intro':
    st.title("📚 독서 추천 웹앱")
    st.markdown("### 책을 읽으러 오셨군요~ 환영합니다!")

    with st.container():
        st.markdown("""
이 웹앱은 간단한 인적 사항(**성별, 연령대, 선호 장르 등**)을 입력하면  
당신에게 딱 맞는 **개인 맞춤형 도서**를 추천해줍니다.

- 📚 해당 연령대에서 인기가 많은 **베스트셀러**
- 🧑‍🎤 **유명 셀럽 추천 도서**
- 🎧 **오디오북**까지 함께 추천해드려요!

> 오디오북의 경우, 최근 **사용률과 구입량이 증가**하고 있어  
> 접근성 측면에서도 매우 유용한 독서 수단입니다.

---

저희는 **데이터 기반의 분석을 바탕으로**,  
관심이 줄어드는 독서 문화를 다시 살리고,  
각자의 취향에 맞는 책을 손쉽게 찾을 수 있도록 돕고자 합니다. 📖✨
        """)

    if st.button("시작하기"):
        st.session_state.page = 'input'

# ---------------------------
# 2️⃣ 사용자 정보 입력 단계별 UI
# ---------------------------

# ---------------------------
# 2️⃣ 사용자 정보 입력 단계별 UI
# ---------------------------
elif st.session_state.page == 'input':
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

        genre = st.multiselect(
            f"{selected_book_type}에서 선호하는 장르를 선택해주세요",
            options=available_genres,
            key="genre"
        )

        if genre and st.session_state.step == 4:
            st.session_state.step = 5
            st.rerun()



    
    if st.session_state.step >= 5:
        st.markdown("---")
        st.success("모든 정보 입력이 완료되었습니다!")
        if st.button("📚 도서 추천 받기"):
            go_to_recommend_page()

# ---------------------------
# 3️⃣ 추천 결과 페이지
# ---------------------------
elif st.session_state.page == 'recommend':
    st.title("✨ 추천 도서 리스트")

    st.markdown("""
당신이 입력한 정보를 기반으로  
다음과 같은 도서를 추천드립니다. 📖
""")
    df = fetch_celebrity_books()
    if "genre" in st.session_state:
        st.write("✅ 장르 값:", st.session_state.genre)
    else:
        st.write("❌ 장르 값 없음")
    # 🧭 사이드바에서 장르 재선택
    st.sidebar.header("🎯 추천 조건 변경")
    num_items = st.sidebar.slider("추천 작가 수", min_value=5, max_value=20, value=10)
    selected_genres = st.sidebar.multiselect(
    "선호 장르를 다시 선택해보세요",
    GENRES_BY_BOOK_TYPE.get(st.session_state.get("book_types", "종이책"), []),
    default=st.session_state.genre if "genre" in st.session_state else [],
    key="sidebar_genre"
)

    st.sidebar.info("선호 장르를 변경하면 결과가 즉시 반영됩니다.")

    # 📌 도서 추천 필터링 (데이터 연동 시 여기에 적용)
    st.subheader("📚 베스트셀러 추천")
    for genre in selected_genres:
        st.markdown(f"- **책 제목 예시** ({genre}) - 설명 <!-- 여기에 데이터 삽입 -->")

    st.subheader("🧑‍🎤 유명인물 추천 도서")
    if df.empty:
         st.info("추천 작가 데이터를 불러올 수 없습니다.")
    
    else:
        for _, row in df.head(num_items).iterrows():  # 유저가 선택한 수 만큼만 보여줌
            with st.container():
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown("🎤")
                with col2:
                    st.markdown(f"**{row['name']}**")
                    st.markdown(f"📘 대표 도서: {row['books'] or '정보 없음'}")
                    
        st.markdown("---")
    st.subheader("🎧 오디오북 추천")
    for genre in selected_genres:
        st.markdown(f"- **오디오북 예시** ({genre}) - 스트리밍 링크 <!-- 여기에 데이터 삽입 -->")

# streamlit run webapptest1.py