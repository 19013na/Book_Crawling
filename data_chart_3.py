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
        전자책, 종이책, 오디오북 형태의 구입량 변화 추이를 살펴보세요.\n
        특히 최근 몇 년간 **전자책이나 오디오북 사용은 늘고 있지만,**  
        **종이책 독서율**은 계속 **줄어드는 경향**을 보이고 있어요.
        """)
        st.markdown("&nbsp;", unsafe_allow_html=True)

        sns.set(style='whitegrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=data, x='연도', y='구입량', hue='형태', marker='o', linewidth=2.5, ax=ax)

        for i in range(len(data)):
            row = data.iloc[i]
            ax.text(row['연도'], row['구입량'] + 0.1, str(row['구입량']),
                    ha='center', fontsize=9, fontproperties=font_prop)

        ax.set_title('도서 형태별 연도별 구입량 변화', fontproperties=font_size)
        ax.set_xlabel('연도', fontproperties=font_prop)
        ax.set_ylabel('구입량', fontproperties=font_prop)
        ax.set_xticks([2019, 2021, 2023])
        ax.legend(title='도서 형태', prop=font_prop, title_fontproperties=font_prop)
        ax.set_ylim(3, 10)
        ax.grid(True, linestyle='--', alpha=0.2)

        st.pyplot(fig)