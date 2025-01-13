from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Book
from .serializers import BookURLSerializer
from .utils import fetch_today_book_urls, fetch_and_save_book_details


class BooksAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="책 정보 개별별 저장 API",
        operation_description=(
            "이 API는 책 상세페이지 URL로 상세 정보를 크롤링하여 데이터베이스에 저장합니다."
        ),
        request_body=BookURLSerializer,
        responses={
            201: "책 정보 저장 성공",
            400: "URL 크롤링 실패 또는 기타 에러",
        }
    )

    def post(self, request):
        serializer = BookURLSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        book_url = serializer.validated_data['book_url']
        result = fetch_and_save_book_details(book_url)
        return Response(result)




class BooksBulkAPIView(APIView):
    """
    책 상세 정보 전체 저장 API (POST)
    - POST /api/v1/books/bulk
    """

    @swagger_auto_schema(
        operation_summary="책 상세 정보 전체 저장 API",
        operation_description=(
            "이 API는 '오늘의 선택' 섹션에서 책 URL을 크롤링하고, "
            "해당 URL로 상세 정보를 크롤링하여 데이터베이스에 저장합니다."
        ),
        responses={
            201: "책 목록 저장 성공",
            400: "URL 크롤링 실패 또는 기타 에러",
        }
    )
    def post(self, request):
        # 1. '오늘의 선택' 책 URL 크롤링
        book_urls = fetch_today_book_urls()
        print(f"[DEBUG] URLs from '오늘의 선택': {book_urls}")  # 디버깅 출력

        if not book_urls:
            return Response(
                {"error": "책 URL 크롤링 실패", "details": "URL 크롤링 중 문제가 발생했습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 각 URL에 대해 상세 정보 크롤링 및 저장
        results = []
        saved_count = 0
        for url in book_urls:
            if not Book.objects.filter(book_url=url).exists():  # 중복 확인
                result = fetch_and_save_book_details(url)
                if result["success"]:
                    results.append(result["data"])
                    saved_count += 1
                else:
                    results.append({"error": result["error"], "url": url})
            else:
                print(f"[INFO] URL already exists in DB: {url}")  # 중복 로그

        # 3. 저장 결과 반환
        return Response(
            {"success": True, "saved_count": saved_count, "details": results},
            status=status.HTTP_201_CREATED
        )
