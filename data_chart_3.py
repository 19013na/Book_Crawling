import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib import font_manager

def run_purchase_trend_analysis(filepath='data/도서_구입량_result.csv'):
    df = pd.read_csv(filepath, index_col='구분')
    df_melted = df.reset_index().melt(id_vars='구분', var_name='연도_형태', value_name='구입량')

    df_melted['연도'] = df_melted['연도_형태'].str.extract(r'(\d{4})')
    df_melted['형태'] = df_melted['연도_형태'].str.extract(r'_(오디오북|전자책|종이책)')
    df_melted = df_melted.dropna(subset=['연도', '형태'])
    df_melted['연도'] = df_melted['연도'].astype(int)

    df_cleaned = df_melted[df_melted['구분'] == '구입량(구입자 기준)'].drop(columns=['구분', '연도_형태'])
    data = df_cleaned.sort_values(by=['형태', '연도'], ascending=True).reset_index(drop=True)

    font_path = "C:/Windows/Fonts/malgun.ttf"
    font_prop = font_manager.FontProperties(fname=font_path)
    font_size = font_manager.FontProperties(fname=font_path, size=20)

    st.subheader("📈 도서 형태별 연도별 구입량 추세")
    with st.expander("📊 구입량 추이 자세히 보기", expanded=False):
        st.markdown("""
            전자책, 종이책, 오디오북 형태의 구입량 변화 추이를 살펴보세요.  
            > - 최근 2019년에서 2023년 사이 **오디오북 구매량은 6.2에서 7.7로 증가**하며<br>
                가장 큰 상승폭을 보였습니다.  
            > - **전자책은 8.3 → 7.2 → 7.7로 약간의 감소 후 회복**, 전반적으로 안정적인<br> 
                구매 추이를 보이고 있습니다.  
            > - 반면, **종이책은 6.7 → 5.6 → 3.7로 꾸준히 감소**하며 큰 하락세를 보이고 있어요.  
            > ***6000명 기준**
                    
            >👉 이 그래프는 디지털 콘텐츠 소비에 익숙해진 현대인의 **독서 환경 변화**를 보여줍니다.  
            >특히, 모바일 기기로 간편하게 접근 가능한 **전자책과 오디오북**의 인기가 높아지며,  
            >물리적 제약이 있는 **종이책 독서 비율은 점차 줄어드는 경향**을 보이고 있어요.
            """, unsafe_allow_html=True)
        st.markdown("&nbsp;", unsafe_allow_html=True)

        sns.set(style='whitegrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=data, x='연도', y='구입량', hue='형태', marker='o', linewidth=4.0, ax=ax)

        for i in range(len(data)):
            row = data.iloc[i]
            ax.text(row['연도'], row['구입량'] + 0.1, str(row['구입량']),
                    ha='center', fontsize=13, fontproperties=font_prop)

        ax.set_title('도서 형태별 연도별 구입량 변화', fontproperties=font_size)
        ax.set_xlabel('연도', fontproperties=font_prop, fontsize=15)
        ax.set_ylabel('구입량', fontproperties=font_prop, fontsize=15)
        ax.set_xticks([2019, 2021, 2023])
        ax.legend(title='도서 형태', prop=font_prop, title_fontproperties=font_prop)
        ax.set_ylim(3, 10)
        ax.grid(True, linestyle='--', alpha=0.2)

        st.pyplot(fig)