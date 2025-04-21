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
    st.title("📚 독서 추천 웹앱")
    st.markdown("### 책을 읽으러 오셨군요~ 환영합니다!")

    with st.container():
        st.markdown("""
            해마다 **독서율**이 점차 **감소하는 추세**를 보이고 있어요.\n
            독서 환경을 개선하고 책과의 거리를 좁히기 위한 노력이 필요한 시점입니다.\n
            추가 내용 필요
        """)
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
        
    if st.button("바로 추천받기"):
        st.session_state.page = 'common'