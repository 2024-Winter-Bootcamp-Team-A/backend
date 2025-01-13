from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from .serializers import BookSerializer
import re


def fetch_today_book_urls():
    """
    '오늘의 선택' 섹션에서 정확한 책 URL만 가져오는 함수.
    """
    driver = webdriver.Chrome()
    driver.get("https://product.kyobobook.co.kr/today-book/")

    book_urls = set()  # 중복 제거를 위한 set 사용
    try:
        # 페이지 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.prod_list.type_today_recommend > li.prod_item"))
        )

        # "오늘의 선택" 섹션의 책 링크 가져오기
        book_elements = driver.find_elements(By.CSS_SELECTOR, "ul.prod_list.type_today_recommend > li.prod_item a.prod_info")
        for element in book_elements:
            url = element.get_attribute("href")
            # URL이 "detail" 패턴을 포함한 경우만 추가
            if "product.kyobobook.co.kr/detail" in url:
                book_urls.add(url)

        # 디버깅용 출력
        print(f"[DEBUG] Filtered URLs: {list(book_urls)}")

    except Exception as e:
        print(f"[ERROR] Error while fetching book URLs: {e}")
    finally:
        driver.quit()

    return list(book_urls)  # set을 list로 변환


def fetch_and_save_book_details(book_url):
    """
    주어진 URL에서 책 정보를 크롤링하고, 데이터베이스에 저장하는 함수.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Referer': 'https://www.kyobobook.co.kr/'
    }

    try:
        response = requests.get(book_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 데이터 크롤링
        category = soup.select_one("#mainDiv > main > section.breadcrumb_wrap > div > ol > li:nth-child(3) > a")
        title = soup.select_one("#contents > div.prod_detail_header h1 span")
        author = soup.select_one("div.prod_author_box div.auto_overflow_contents div div")
        publisher = soup.select_one("div.prod_info_text.publish_date a")
        story = soup.select_one("div.product_detail_area.book_publish_review p.info_text")
        image_tag = soup.select_one("#contents div.col_prod_info.thumb img")

        # 데이터 정리
        book_data = {
            "category": category.get_text(strip=True) if category else "데이터 없음",
            "title": title.get_text(strip=True) if title else "데이터 없음",
            "author": author.get_text(strip=True) if author else "데이터 없음",
            "publisher": publisher.get_text(strip=True) if publisher else "데이터 없음",
            "story": story.get_text(strip=True) if story else "데이터 없음",
            "image": image_tag["src"] if image_tag and 'src' in image_tag.attrs else "데이터 없음",
            "book_url": book_url,
        }

        # 데이터 저장
        book_serializer = BookSerializer(data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return {"success": True, "data": book_serializer.data}
        return {"success": False, "error": book_serializer.errors}

    except Exception as e:
        print(f"[ERROR] Failed to fetch book details for {book_url}: {e}")
        return {"success": False, "error": f"크롤링 실패: {e}"}
