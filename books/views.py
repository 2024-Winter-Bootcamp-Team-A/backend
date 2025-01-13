from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from .models import Book
from .serializers import BookSerializer, BookDetailSerializer
from drf_yasg.utils import swagger_auto_schema

class BookDetailCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="책 개별 저장 API ",
        operation_description="이 API는 책을 개별 저장하는데 사용됩니다.",
        request_body=BookDetailSerializer,  # 요청 바디를 정의
        responses={201: BookSerializer, 400: "Bad Request"},  # 가능한 응답 정의
    )
    def post(self, request):
        # 요청 데이터 검증
        serializer = BookDetailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        book_url = serializer.validated_data['book_url']

        # 크롤링 로직
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'ko-KR,ko;q=0.9',
            'Referer': 'https://www.kyobobook.co.kr/'
        }

        try:
            response = requests.get(book_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 카테고리 크롤링
            try:
                category = soup.select_one(
                    "#mainDiv > main > section.breadcrumb_wrap > div > ol > li:nth-child(3) > a"
                ).get_text(strip=True)
            except AttributeError:
                category = "데이터 없음"

            # 제목 크롤링
            try:
                title = soup.select_one(
                    "#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span"
                ).get_text(strip=True)
            except AttributeError:
                title = "데이터 없음"

            # 저자 크롤링
            try:
                author = soup.select_one(
                    "#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_author_box.auto_overflow_wrap > div.auto_overflow_contents > div > div"
                ).get_text(strip=True)
            except AttributeError:
                author = "데이터 없음"

            # 출판사 크롤링
            try:
                publisher = soup.select_one(
                    "#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_info_text.publish_date > a"
                ).get_text(strip=True)
            except AttributeError:
                publisher = "데이터 없음"

            # 줄거리 크롤링
            try:
                story = soup.select_one(
                    "div.product_detail_area.book_publish_review p.info_text"
                ).get_text(strip=True)
            except AttributeError:
                story = "데이터 없음"

            # 이미지 크롤링
            try:
                image_tag = soup.select_one(
                    "#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div.col_prod_info.thumb img"
                )
                if image_tag and 'src' in image_tag.attrs:
                    image = image_tag["src"]
                else:
                    image = "데이터 없음"
            except (AttributeError, TypeError):
                image = "데이터 없음"

            # 데이터 저장
            book_data = {
                "category": category,  # 추가된 카테고리
                "title": title,
                "author": author,
                "publisher": publisher,
                "story": story,
                "image": image,
                "book_url": book_url,
            }

            book_serializer = BookSerializer(data=book_data)
            if book_serializer.is_valid():
                book_serializer.save()  # DB에 저장
                return Response(book_serializer.data, status=status.HTTP_201_CREATED)
            return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"크롤링 실패: {e}"}, status=status.HTTP_400_BAD_REQUEST)
