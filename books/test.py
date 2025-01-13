# 오늘의 선택 책 URL selenium 크롤링 테스트

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 웹 드라이버 설정
driver = webdriver.Chrome()  # ChromeDriver 경로가 환경 변수에 설정되어 있어야 합니다.
driver.get('https://product.kyobobook.co.kr/today-book/')  # 새로운 '오늘의 선택' 페이지

try:
    # "오늘의 선택" 섹션의 책 리스트 URL 가져오기
    # 이전 방식 (메인 페이지 -> 더보기 클릭)은 주석 처리
    # today_section = driver.find_element(By.CSS_SELECTOR, "div#welcome_today_book")
    # more_button = today_section.find_element(By.CSS_SELECTOR, "a.btn_more_plus_text")
    # more_button.click()
    # time.sleep(3)  # 페이지 로드 대기

    # 새로운 '오늘의 선택' 페이지에서 책 리스트 URL 가져오기
    time.sleep(5)  # 페이지가 완전히 로드되기를 기다림
    book_elements = driver.find_elements(By.CSS_SELECTOR, "a.prod_info")  # 책 URL 요소
    book_urls = [element.get_attribute("href") for element in book_elements]

    # URL 개수 확인 및 출력
    print(f"크롤링된 책 URL 개수: {len(book_urls)}")
    print("크롤링된 책 URL 리스트:")
    for url in book_urls:
        print(url)

finally:
    # 브라우저 닫기
    driver.quit()
