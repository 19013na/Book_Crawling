import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 3. 도서 구입량
# 2019, 2021, 2023년도 문화체육관광부 국민독서 실태조사
# 도서_구입량_result.csv파일 참고

def plot_book_purchase_trend():
    df = pd.read_csv('data/도서_구입량_result.csv', index_col='구분')
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

    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x='연도', y='구입량', hue='형태', marker='o', linewidth=2.5)

    for i in range(len(data)):
        row = data.iloc[i]
        plt.text(row['연도'], row['구입량'] + 0.1, str(row['구입량']),
                 ha='center', fontsize=9, fontproperties=font_prop)

    plt.title('도서 형태별 연도별 구입량 변화 (구입자 기준)', fontproperties=font_size)
    plt.xlabel('연도', fontproperties=font_prop)
    plt.ylabel('구입량', fontproperties=font_prop)
    plt.xticks([2019, 2021, 2023])
    plt.legend(title='도서 형태', prop=font_prop, title_fontproperties=font_prop)
    plt.ylim(3, 10) 
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    
    fig = plt.gcf()  # 현재 figure 객체 저장
    return fig
    #return plt
