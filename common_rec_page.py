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
    num_items_best = st.sidebar.slider("베스트셀러 개수", min_value=1, max_value=10, value=5)
    num_items_author = st.sidebar.slider("추천 작가 수", min_value=1, max_value=20, value=10)


    
    # 📌 탭 구성
    tab1, tab2 = st.tabs(["📚 베스트셀러", "🧑 유명인 추천"])

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
                        col1, col2 = st.columns([2, 6])  # 이미지 + 정보 2단 구성

                        with col1:
                            st.markdown(f"""
                                <style>
                                    .hover-img {{
                                        transition: all 0.3s ease;
                                    }}
                                    .hover-img:hover {{
                                        transform: scale(1.05);
                                        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                                    }}
                                </style>

                                <div style="
                                    width: 170px;
                                    height: 210px;
                                    border-radius: 16px;
                                    overflow: hidden;
                                ">
                                    <img src="{row.get('이미지', 'https://via.placeholder.com/100')}"
                                        class="hover-img"
                                        style="
                                            width: 100%;
                                            height: 100%;
                                            object-fit: cover;
                                            border-radius: 16px;
                                            display: block;
                                        "
                                    />
                                </div>
                            """, unsafe_allow_html=True)


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

                            with st.expander("📖 책 소개"):
                                st.markdown(f"{row['description'] or '설명 없음'}")

                        st.markdown("---")


    # ---------------------
    # 🧑‍🎤 탭 2: 셀럽 추천
    # ---------------------
    with tab2:
        st.subheader("🧑 유명인물이 추천해줍니다")

        if df_cel.empty or df_img.empty:
            st.info("작가 정보 또는 이미지 데이터를 불러올 수 없습니다.")
        else:
            for i in range(min(num_items_author, len(df_cel), len(df_img))):
                name = df_cel.iloc[i]["name"]
                books = df_cel.iloc[i].get("books", "")
                description = df_cel.iloc[i].get("description", "")
                image = df_img.iloc[i].get("image", "")
                
                # 📘 책 목록을 칩 스타일로 만들기
                book_list = books.split(", ")
                book_html = ""
                for book in book_list:
                    book_html += f"""
                        <span style='
                            background-color: #e8f0fe;
                            color: #333;
                            font-size: 13px;
                            padding: 4px 10px;
                            border-radius: 12px;
                            margin: 4px 6px 0 0;
                            display: inline-block;
                        '>{book}</span>
                    """

                with st.container():
                    col1, col2 = st.columns([2, 4])

                    # 📷 인물 이미지 카드 (베스트셀러 UI 동일 스타일)
                    with col1:
                        st.markdown(f"""
                            <style>
                                .hover-img {{
                                    transition: all 0.3s ease;
                                }}
                                .hover-img:hover {{
                                    transform: scale(1.05);
                                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                                }}
                            </style>

                            <div style="
                                width: 180px;
                                height: 250px;
                                border-radius: 18px;
                                overflow: hidden;
                            ">
                                <img src="{image or 'https://via.placeholder.com/100'}"
                                    class="hover-img"
                                    style="
                                        width: 100%;
                                        height: 100%;
                                        object-fit: cover;
                                        border-radius: 16px;
                                        display: block;
                                    "
                                />
                            </div>
                        """, unsafe_allow_html=True)

                    # 📄 작가 정보 카드 (베스트셀러 스타일 적용)
                with col2:
                    with st.container():
                        # 🎤 작가 이름
                        st.markdown(f"""
                            <div style='
                                font-size: 22px;
                                font-weight: bold;
                                margin-bottom: 4px;
                                color: #333;
                            '>
                                {name}
                            </div>
                        """, unsafe_allow_html=True)

                        # 📘 대표 도서 리스트 (칩 스타일 유지)
                        st.markdown(f"""
                            <div style='
                                font-size: 14px;
                                font-weight: 500;
                                margin-top: 8px;
                                margin-bottom: 6px;
                            '> 대표 도서:</div>
                            {book_html}
                        """, unsafe_allow_html=True)

                        # 📝 소개 펼쳐보기 (Streamlit 기본 배경)
                        with st.expander("📝 인물 소개"):
                            st.markdown(description or "작가 설명 없음")


                st.markdown("---")
