from celery import shared_task
from .utils import fetch_today_book_urls, fetch_and_save_book_details

@shared_task
def crawl_today_books():
    """
    '오늘의 선택' 섹션에서 책 URL을 크롤링하고, 해당 URL로 책 정보를 크롤링하여 데이터베이스에 저장하는 작업.
    """
    print("작업이 실행되었습니다!") # 테스트 확인용용
    book_urls = fetch_today_book_urls()  # '오늘의 선택'에서 책 URL 가져오기
    results = []

    for url in book_urls:
        result = fetch_and_save_book_details(url)  # 책 정보 크롤링 및 저장
        results.append(result)
    
    print("작업 완료!") # 테스트 확인용
    # 작업 완료 후 성공, 실패 건수 출력
    return {
        'success_count': sum(1 for r in results if r.get('success')),
        'failure_count': sum(1 for r in results if not r.get('success')),
    }
