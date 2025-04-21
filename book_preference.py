import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.font_manager as fm
import matplotlib as mpl

def run_book_preference_analysis(df: pd.DataFrame, target_groups=None, years=None, genres=None, total_sample=6000):
    
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
    
    if target_groups is None:
        target_groups = ["19~29세", "30~39세"]
    if years is None:
        years = ["2019", "2021", "2023"]
    if genres is None:
        genres = ["소설", "수필", "경제/경영"]

    df = df[df["구분"].isin(target_groups + ["전체"])]
    results = []

    for year in years:
        total_group_sample = df[df["구분"] != "전체"][f"{year}_사례수"].sum()
        for _, row in df.iterrows():
            if row["구분"] == "전체":
                continue
            group = row["구분"]
            group_sample = row[f"{year}_사례수"]
            group_ratio = group_sample / total_group_sample
            adjusted_group_sample = group_ratio * total_sample

            for genre in genres:
                rate = row[f"{year}_{genre}(%)"]
                estimated = adjusted_group_sample * rate / 100
                results.append({
                    "연도": year,
                    "연령대": group,
                    "장르": genre,
                    "선호인원": round(estimated, 2)
                })

    df_weighted = pd.DataFrame(results)

    # 📊 시각화
    st.subheader("📈 장르별 연도별 선호 인원 비교")

    with st.expander("📊 전체 장르별 그래프 자세히 보기", expanded=False):
        for genre in genres:
            genre_df = df_weighted[df_weighted["장르"] == genre]
            
            st.markdown(f"### 📚 {genre}")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(data=genre_df, x="연도", y="선호인원", hue="연령대", ax=ax)

            plt.title(f"{genre} 장르 - 연도별 선택자 수 (6000명 기준)", fontproperties=font_prop)
            plt.ylabel("선호 인원수", fontproperties=font_prop)
            plt.xlabel("", fontproperties=font_prop)
            plt.grid(True, linestyle="--", alpha=0.3)

            # ✅ 범례 위치 조정해서 그래프와 겹치지 않게!
            ax.legend(prop=font_prop, loc="upper left", bbox_to_anchor=(1, 1))

            # 수치 라벨
            for container in ax.containers:
                ax.bar_label(container, fmt="%.1f", label_type="edge", padding=5, fontproperties=font_prop)
                max_height = genre_df["선호인원"].max()
                ax.set_ylim(0, max_height * 1.15)  # ✅ 위쪽 여유 15%
            st.pyplot(fig)
