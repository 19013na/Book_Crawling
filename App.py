import streamlit as st

from intro_page import show_intro
from input_page import show_input
from recommend_page import show_recommend
from person_book_rec import fetch_celebrity_books

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
elif st.session_state.page == 'recommend':
    show_recommend()


# streamlit run App.py