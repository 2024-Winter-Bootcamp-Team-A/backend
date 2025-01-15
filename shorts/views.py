from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShortRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Short
from .models import  # 통계 데이터 모델
from django.db.models import Count

class ShortsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="숏츠 저장 API",
        operation_description="이 API는 숏츠를 저장하는데 사용됩니다.",
        request_body=ShortRequestSerializer,
        responses={201: "숏츠 생성을 완료했습니다.",400:"error"}
    )
    def post(self, request):

        serializer = ShortRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ShortVisitAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="사이트 방문 수 증가 API",
        operation_description="특정 숏츠의 책 구매 사이트 방문 수를 증가시킵니다.",
        responses={
            200: "책 구매 사이트를 방문하였습니다.",
            404: "숏츠를 찾을 수 없습니다."
        }
    )
    def put(self, request, book_id):
        try:
            short = Short.objects.get(book_id=book_id)

            short.book_visit_count += 1
            short.save()

            return Response({"message": "책 구매 사이트를 방문하였습니다."}, status=status.HTTP_200_OK)
        except Short.DoesNotExist:
            return Response({"error": "숏츠를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        
class ShortShareAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="링크 공유 수 증가 API",
        operation_description="특정 숏츠의 링크 공유 수를 증가시킵니다.",
        responses={
            200: "숏츠 링크가 복사되었습니다.",
            404: "숏츠를 찾을 수 없습니다."
        }
    )
    def put(self, request, book_id):
        try:
            short = Short.objects.get(book_id=book_id)

            short.share_count += 1
            short.save()

            return Response({"message": "숏츠 링크가 복사되었습니다."}, status=status.HTTP_200_OK)
        except Short.DoesNotExist:
            return Response({"error": "숏츠를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


class ShortsStatsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="특정 숏츠 통계 및 설명 조회 API",
        operation_description="특정 숏츠 ID로 조회하여 통계(조회수, 위시리스트, 공유 수, 방문 수)와 핵심 문장을 반환합니다.",
        responses={
            200: "조회 성공",
            404: "해당 숏츠를 찾을 수 없습니다."
        }
    )
    def get(self, request, short_id):
        """
        특정 숏츠의 통계 데이터를 반환하는 API
        """
        try:
            # 1. 숏츠 데이터 가져오기기
            short = Short.objects.get(id=short_id)

            # 2. 통계 데이터 계산
            views = records.objects.filter(book=short.book).count() # 조회수
            wishes = wishes.objects.filter(book=short.book).count() # 위시리스트
            shares = short.share_count # 공유 수
            book_visits = short.book_visit_count # 사이트 방문 수수
            point = short.book.point # 핵심 문장

            # 3. 응답 데이터 구성
            response_data = {
                "views": views,
                "wishes": wishes,
                "shares": shares,
                "book_visits": book_visits,
                "point": point
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
        except Short.DoesNotExit:
            return Response(
                {"status": "error", "message": "해당 숏츠를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )
        