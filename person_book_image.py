import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def fetch_author_images_with_selenium(pages: int = 1) -> pd.DataFrame:
    """
    교보문고 베스트셀러 인물 페이지에서 작가 이름과 이미지 URL을 Selenium으로 크롤링합니다.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    author_list = []

    for page in range(1, pages + 1):
        url = f"https://store.kyobobook.co.kr/bestseller/person/daily/domestic?page={page}"
        driver.get(url)
        time.sleep(2)  # JS 렌더링 대기

        soup = BeautifulSoup(driver.page_source, "html.parser")
        blocks = soup.select("div.relative.flex.rounded-2xl")

        for block in blocks:
            name_tag = block.select_one("a.fz-16 span")
            name = name_tag.get_text(strip=True) if name_tag else "이름없음"

            img_tag = block.select_one("img.h-full.object-cover")
            image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ""

            if name and image_url:
                author_list.append({
                    "name": name,
                    "image": image_url
                })

    driver.quit()
    return pd.DataFrame(author_list)


# 실행 예시
if __name__ == "__main__":
    pd.set_option("display.max_colwidth", None)
    df = fetch_author_images_with_selenium(pages=1)
    print("===> 작가 이미지 리스트:")
    print(df.head(10))
