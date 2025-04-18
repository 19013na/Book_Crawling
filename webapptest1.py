import streamlit as st
import time

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

    # 선호 장르
    if st.session_state.step >= 3:
        genre = st.multiselect("선호 장르", ["소설", "에세이", "경제", "역사", "인문"], key="genre")
        if genre and st.session_state.step == 3:
            st.session_state.step = 4
            st.rerun()

    # 버튼
    if st.session_state.step >= 4:
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

    # 🧭 사이드바에서 장르 재선택
    st.sidebar.header("🎯 추천 조건 변경")
    selected_genres = st.sidebar.multiselect(
        "선호 장르를 다시 선택해보세요",
        ["소설", "에세이", "경제", "역사", "인문"],
        default=st.session_state.genre,
        key="sidebar_genre"
    )

    st.sidebar.info("선호 장르를 변경하면 결과가 즉시 반영됩니다.")

    # 📌 도서 추천 필터링 (데이터 연동 시 여기에 적용)
    st.subheader("📚 베스트셀러 추천")
    for genre in selected_genres:
        st.markdown(f"- **책 제목 예시** ({genre}) - 설명 <!-- 여기에 데이터 삽입 -->")

    st.subheader("🧑‍🎤 셀럽 추천 도서")
    for genre in selected_genres:
        st.markdown(f"- **셀럽 추천 예시** ({genre}) - 추천 이유 <!-- 여기에 데이터 삽입 -->")

    st.subheader("🎧 오디오북 추천")
    for genre in selected_genres:
        st.markdown(f"- **오디오북 예시** ({genre}) - 스트리밍 링크 <!-- 여기에 데이터 삽입 -->")
