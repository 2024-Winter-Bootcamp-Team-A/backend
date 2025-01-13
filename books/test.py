#BeautifulSoup로 크롤링 테스트

import requests
from bs4 import BeautifulSoup

def get_book_details(book_url):
    """
    책 상세 정보를 BeautifulSoup으로 크롤링
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Referer': 'https://www.kyobobook.co.kr/'
    }

    response = requests.get(book_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        title = soup.select_one("#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span").get_text(strip=True)
    except AttributeError:
        title = "데이터 없음"

    try:
        author = soup.select_one("#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_author_box.auto_overflow_wrap > div.auto_overflow_contents > div > div").get_text(strip=True)
    except AttributeError:
        author = "데이터 없음"

    try:
        publisher = soup.select_one("#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_info_text.publish_date > a").get_text(strip=True)
    except AttributeError:
        publisher = "데이터 없음"

    try:
        story = soup.select_one("div.product_detail_area.book_publish_review p.info_text").get_text(strip=True)
    except AttributeError:
        story = "데이터 없음"

    try:
        # 이미지 크롤링
        image_tag = soup.select_one("#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div.col_prod_info.thumb img")
        if image_tag and 'src' in image_tag.attrs:
            image = image_tag["src"]
        else:
            image = "데이터 없음"
    except (AttributeError, TypeError):
        image = "데이터 없음"

    return {
        "title": title,
        "author": author,
        "publisher": publisher,
        "story": story,
        "image": image,
        "book_url": book_url,
    }

# 테스트
book_url = "https://product.kyobobook.co.kr/detail/S000000610612"
details = get_book_details(book_url)
print(details)

