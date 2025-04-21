import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2019, 2021, 2023 독서율

def load_reading_rate_data(filepath="data/독서율_비교_2019vs2021vs2023.csv"):
    df = pd.read_csv(filepath)
    df_melted = df.melt(id_vars='구분(독서율 %)', var_name='년도', value_name='독서율(%)')
    df_total = df_melted[df_melted['구분(독서율 %)'] == '전체'].copy()
    return df_total

def generate_reading_rate_plot(df_total, font_prop=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.set_style("whitegrid")

    sns.barplot(
        data=df_total,
        x='년도',
        y='독서율(%)',
        color='skyblue',
        ax=ax
    )

    # 수치 표시
    for index, row in df_total.iterrows():
        ax.text(row['년도'], row['독서율(%)'] + 1,
                f"{row['독서율(%)']:.1f}%",
                ha='center',
                fontsize=12, fontproperties=font_prop, color='#333333')

    ax.set_title('전체 독서율 변화', fontsize=17, weight='bold', fontproperties=font_prop)
    ax.set_ylabel('독서율 (%)', fontsize=13, fontproperties=font_prop)
    ax.set_xlabel('', fontsize=13)
    ax.set_ylim(35, 55)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax.set_xticklabels(df_total['년도'].unique(), fontproperties=font_prop)

    return fig