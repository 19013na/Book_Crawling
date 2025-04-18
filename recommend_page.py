import streamlit as st
from person_book_rec import fetch_celebrity_books
from input_page import GENRES_BY_BOOK_TYPE

# ---------------------------
# 3️⃣ 추천 결과 페이지
# ---------------------------

def show_recommend():
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

