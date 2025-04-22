import streamlit as st

from intro_page import show_intro
from input_page import show_input
from common_rec_page import show_common_rec
from person_book_rec import fetch_celebrity_books
from suit_rec_page import show_recommend

# 탭 제목
st.set_page_config(
    page_title="책, 오늘",
    page_icon="📚",                   
    layout="centered",          
    initial_sidebar_state="auto"
)

# 초기 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'step' not in st.session_state:
    st.session_state.step = 1


# 페이지 라우팅
if st.session_state.page == 'intro':
    show_intro()
elif st.session_state.page == 'input':
    show_input()
elif st.session_state.page == 'common':
    show_common_rec()
elif st.session_state.page == 'recommend':
    show_recommend()

# streamlit run App.py