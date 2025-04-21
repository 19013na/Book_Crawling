import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import matplotlib as mpl
from data_chart_3 import run_purchase_trend_analysis
from data_chart_1 import load_reading_rate_data, generate_reading_rate_plot
from book_preference import run_book_preference_analysis

# ---------------------------
# 1️⃣ 인트로 페이지
# ---------------------------


#윈도우
# ✅ 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = fm.FontProperties(fname=font_path).get_name()
font_prop = fm.FontProperties(fname=font_path)

plt.rc('font', family=font_name)
mpl.rcParams['axes.unicode_minus'] = False

#맥북
# font_path = '/System/Library/AssetsV2/com_apple_MobileAsset_Font7/bad9b4bf17cf1669dde54184ba4431c22dcad27b.asset/AssetData/NanumGothic.ttc'
# #font의 파일정보로 font name 을 알아내기
# font_prop = fm.FontProperties(fname=font_path)
# # 2. 폰트를 matplotlib에 반영
# plt.rcParams['font.family'] = font_prop.get_name()


def show_intro():
    st.title("📚 책, 오늘  ")
    st.markdown("### '책 오늘'은")

    with st.container():
        st.markdown("""
            > 오늘의 나에게 꼭 필요한 책을 **추천**해주는 사이트입니다.<br>
            >이곳은 **책과 사람 사이의 거리**를 조금 더 가깝게 만들기 위한 공간입니다.<br>
            >지금 이 순간, 당신의 책장을 채워줄 한 권의 책을 만나보세요. 🌿

            >요즘, 해마다 **독서율이 줄어들고 있다**는 사실 알고 계셨나요?<br>
            >📉 2019년에서 2023년 사이 **전 연령대 독서율이 점차 하락하는 추세**를 보이고 있어요.
        """, unsafe_allow_html=True)
        st.markdown("&nbsp;", unsafe_allow_html=True)

    # chart1 : 기본 독서율 시각화
    df_total = load_reading_rate_data()
    fig1 = generate_reading_rate_plot(df_total, font_prop)
    # 화면에 출력
    st.pyplot(fig1)
    st.markdown("&nbsp;", unsafe_allow_html=True)


    # chart2 : 도서 연령별 선호도 사례수 시각화
    b_df = pd.read_csv("data/도서_연령별_선호도_사례수포함.csv")
    run_book_preference_analysis(b_df)


    # chart3 : 도서 구입량 추세 그래프 시각화
    run_purchase_trend_analysis()
    
    
    st.markdown("&nbsp;", unsafe_allow_html=True)
    # 설명!
    with st.container():
        st.markdown("""
            디지털 콘텐츠의 확산, 과중한 업무와 학업, 빠르게 돌아가는 생활 속에서<br>
            책 읽는 시간이 점점 사라지고 있는 거죠.<br>

            바쁜 일상 속에서 책 한 권을 펼치기란 쉽지 않지만,<br>
            **한 권의 책, 한 줄의 문장**이<br>
            우리 삶에 작은 위로와 큰 영감을 줄 수 있어요.<br>

            이제는 단순히 책을 ‘읽자’는 권유를 넘어서,<br>
            **책을 자연스럽게 마주할 수 있는 환경과 계기**가 필요한 때입니다.<br>

            ### 그래서 저희는,
            **당신에게 꼭 맞는 책을 추천하는 맞춤형 독서 플랫폼**을 만들었습니다.<br>

            - 📚 연령대/장르/성별 인기 도서부터<br>
            - 🎧 오디오북, 유명인의 책까지<br>
            - 📊 데이터 기반 분석으로 더 정확하게<br>

            **지금 이 순간, 당신의 책장을 채워줄 한 권의 책을 만나보세요.** 🌿
        """, unsafe_allow_html=True)
    
    
    if st.button("시작하기"):
        st.session_state.page = 'input'
        
    if st.button("바로 추천받기"):
        st.session_state.page = 'common'

