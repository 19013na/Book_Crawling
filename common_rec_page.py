import streamlit as st
from person_book_rec import fetch_celebrity_books
from input_page import GENRES_BY_BOOK_TYPE
from bestseller_rec import fetch_kyobo_bestseller

def show_common_rec():
    st.title("✨ 추천 도서 리스트")
    st.markdown("다음과 같은 도서를 추천드립니다. 📖")
    
    # 데이터 가져오기
    df_cel = fetch_celebrity_books()
    df_com = fetch_kyobo_bestseller()
    st.dataframe(df_cel)
    # 사이드바 슬라이더
    st.sidebar.header("🎯 추천 조건 변경")
    num_items_best = st.sidebar.slider("베스트셀러 개수", min_value=5, max_value=20, value=10)
    num_items_author = st.sidebar.slider("추천 작가 수", min_value=5, max_value=20, value=10)

    # 베스트셀러 추천
    st.subheader("📚 실시간 베스트셀러 추천")
    if df_com.empty:
        st.info("베스트셀러 데이터를 불러올 수 없습니다.")
    else:
        for _, row in df_com.head(num_items_best).iterrows():
            with st.container():
                st.markdown(f"📘 **{row['title']}**")
                st.markdown(f"✍️ {row['author']} | {row['publisher']} | {row['pub_date']}")
                st.markdown(f"💬 {row['description'] or '설명 없음'}")
                st.markdown(f"💰 정가: {row['price']} / 평점: {row['review_score']} ({row['review_count']})")
                st.markdown("---")

    # 유명인물 추천
    st.subheader("🧑‍🎤 유명인물 추천 도서")
    if df_cel.empty:
        st.info("추천 작가 데이터를 불러올 수 없습니다.")
    else:
        for _, row in df_cel.head(num_items_author).iterrows():
            with st.container():
                try:
                    st.image(row["image"], width=100)
                except Exception as e:
                    st.warning("이미지를 불러올 수 없습니다.")
                    st.image("https://via.placeholder.com/100", width=100)
                st.markdown(f"🎤 **{row['name']}**")
                st.markdown(f"📘 대표 도서: {row['books'] or '정보 없음'}")
                st.markdown("---")
