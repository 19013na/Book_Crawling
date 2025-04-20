import streamlit as st
from person_book_rec import fetch_celebrity_books
from input_page import GENRES_BY_BOOK_TYPE
from bestseller_rec import fetch_kyobo_bestseller
from person_book_image import fetch_author_images_with_selenium

def show_common_rec():
    st.title(" 추천 도서 리스트")
    st.markdown("당신에게 맞는 도서를 추천드립니다. 📖")

    # 데이터 가져오기
    df_cel = fetch_celebrity_books()
    df_com = fetch_kyobo_bestseller()
    df_img = fetch_author_images_with_selenium(pages=1)  # 작가 이미지
    # 사이드바 필터
    st.sidebar.header("🎯 추천 조건 변경")
    num_items_best = st.sidebar.slider("베스트셀러 개수", min_value=5, max_value=20, value=10)
    num_items_author = st.sidebar.slider("추천 작가 수", min_value=5, max_value=20, value=10)

    # 📌 탭 구성
    tab1, tab2 = st.tabs(["📚 베스트셀러", "🧑‍🎤 유명인 추천"])

    # ---------------------
    # 📚 탭 1: 베스트셀러
    # ---------------------
    with tab1:
        st.subheader("📚 실시간 베스트셀러 추천")
        if df_com.empty:
            st.info("베스트셀러 데이터를 불러올 수 없습니다.")
        else:
            for _, row in df_com.head(num_items_best).iterrows():
                   with st.container():
                        col1, col2 = st.columns([1, 5])  # 이미지 + 정보 2단 구성

                        with col1:
                            st.image(row.get("이미지", "https://via.placeholder.com/100"), width=100)

                        with col2:
                            st.markdown(f"""
                                <div style='
                                    font-size: 22px;
                                    font-weight: bold;
                                    margin-bottom: 4px;
                                    color: #333;
                                '>
                                     {row['title']}
                                </div>
                            """, unsafe_allow_html=True)

                            st.markdown(f"✍️ {row['author']} | {row['publisher']} | {row['pub_date']}")
                            st.markdown(f"💰 정가: {row['price']} ")
                            st.markdown(f"⭐ 평점: {row['review_score']}점 ({row['review_count']})")

                            with st.expander("📖 책 소개 펼쳐보기"):
                                st.markdown(f"{row['description'] or '설명 없음'}")

                        st.markdown("---")


    # ---------------------
    # 🧑‍🎤 탭 2: 셀럽 추천
    # ---------------------
        with tab2:
            st.subheader("🧑‍🎤 유명인물 추천 도서")
            if df_cel.empty or df_img.empty:
                st.warning("작가 정보 또는 이미지 데이터를 불러올 수 없습니다.")
            else:
                for i in range(min(num_items_author, len(df_cel), len(df_img))):
                    name = df_cel.iloc[i]["name"]
                    books = df_cel.iloc[i].get("books", "")
                    image = df_img.iloc[i].get("image", "")

                    with st.container():
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            st.image(image or "https://via.placeholder.com/100", width=80)
                        with col2:
                            st.markdown(f"""
                                <div style='
                                    background-color: #f9f9f9;
                                    padding: 10px 15px;
                                    border-radius: 12px;
                                    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                                    margin-bottom: 10px;
                                    min-height: 120px;  
                                '>
                                    <strong style='font-size: 18px;'>🎤 {name}</strong><br>
                                    <span style='font-size: 15px;'>📘 대표 도서: {books or '정보 없음'}</span>
                                </div>
                            """, unsafe_allow_html=True)