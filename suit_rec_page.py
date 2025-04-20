import streamlit as st
from input_page import GENRES_BY_BOOK_TYPE
from suit_crawling_page import get_bestsellers  # 크롤링 함수 임포트
from suit_category_map import PAPERBOOK_CATEGORY_MAP, EBOOK_CATEGORY_MAP, GENDER_MAP, AGE_MAP
from suit_rec_sidebar import show_sidebar

# ---------------------------
# 3️⃣ 추천 결과 페이지
# ---------------------------

def show_recommend():
    st.title("✨ 추천 도서 리스트")
    st.markdown("당신이 입력한 정보를 기반으로 다음과 같은 도서를 추천드립니다.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🔧 사이드바에서 조건값 불러오기
    book_type, gender, age_group, genre_name, num_items_best = show_sidebar()

    # 세션 값 불러오기
    book_type = st.session_state.get("book_types", None)
    gender = st.session_state.get("gender", None)
    age_group = st.session_state.get("age_group", None)
    genre_name = st.session_state.get("genre", None)

    # 성별/연령대 변환
    sex = GENDER_MAP.get(gender, "")
    age = AGE_MAP.get(age_group, "")

    # 책 형식 및 장르 변환
    if book_type == "오디오북":
        st.sidebar.info("오디오북은 장르 선택 없이 추천됩니다.")
        genre_number = "017001008"
    else:
        genre_number = PAPERBOOK_CATEGORY_MAP.get(genre_name, "해당 장르는 존재하지 않습니다.") if book_type == "종이책" else EBOOK_CATEGORY_MAP.get(genre_name, "해당 장르는 존재하지 않습니다.")


    # 데이터 가져오기
    df = get_bestsellers(category_number=genre_number, sex=sex, age=age)

    if book_type == "오디오북":
        st.subheader(f"🎧 {age_group} {gender}를 위한 {book_type} 추천 도서")
    else:
        st.subheader(f"📖 {age_group} {gender}를 위한 {book_type} '{genre_name}' 장르 추천 도서")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 추천 도서 출력
    if df.empty:
        st.info("추천 도서를 불러올 수 없습니다 😥")
    else:
        for _, row in df.head(num_items_best).iterrows():  # 슬라이더 값 사용
            # 책 표지 이미지 추가 (여기서는 URL 가정)
            book_image_url = row['이미지']
            
            # 카드 형식으로 도서 정보 표시 (간격을 넓힘)
            st.markdown(f"""
            <div style="background-color: #fff; border-radius: 10px; padding: 20px; margin-bottom: 30px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); width: 100%; max-width: 800px; margin-left: auto; margin-right: auto;">
                <div style="display: flex; align-items: center;">
                    <img src="{book_image_url}" alt="Book Image" width="120" height="180" style="border-radius: 10px; margin-right: 20px;">
                    <div>
                        <h4 style="color: #2a4d74; font-size: 18px;">{row['순위']}. {row['제목']}</h4>
                        <p style="font-size: 14px; color: #5a5a5a;">저자: {row['저자']} / 출판사: {row['출판사']} / 출간일: {row['출간일']}</p>
                        <p style="font-size: 16px; color: #0073e6;"><a href="{row['링크']}" style="text-decoration: none; color: #0073e6;">📖 상세보기</a></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
