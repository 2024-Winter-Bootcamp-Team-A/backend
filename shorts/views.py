from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShortRequestSerializer, ShortIndividualSerializer, BestShortsSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Short
from books.models import Book
from records.models import Record
from wishes.models import Wish
from django.db.models import Count
from comments.models import Comment
from drf_yasg import openapi


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


class ShortDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="숏츠 설명창 API",
        operation_description="숏츠에 대한 통계 데이터와 책의 핵심 문장을 반환합니다.",
        responses={
            200: "성공적으로 데이터를 반환했습니다.",
            404: "해당 book_id로 숏츠를 찾을 수 없습니다."
        }
    )
    def get(self, request, book_id):
        try:
            short = Short.objects.get(book=book_id)
            book = short.book

            views = Record.objects.filter(book=book).count()
            wishes = Wish.objects.filter(book=book).count()
            shares = short.share_count
            book_visits = short.book_visit_count

            response_data = {
                "views": views,
                "wishes": wishes,
                "shares": shares,
                "book_visits": book_visits,
                "key_sentence": book.point
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Short.DoesNotExist:
            return Response(
                {"error": "해당 book_id로 숏츠를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )
        
class ShortIndividualAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="숏츠 개별 조회 API",
        operation_description="특정 book_id에 해당하는 숏츠 정보를 반환합니다.",
        responses={200: ShortIndividualSerializer()}
    )
    def get(self, request, book_id):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"error": "로그인되지 않았습니다."})
        
        try:
            short = Short.objects.get(book_id=book_id)
            serializer = ShortIndividualSerializer(short, context={"request": request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Short.DoesNotExist:
            return Response(
                {"error": "해당 book_id로 숏츠를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )


class BestShortsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="베스트 숏츠 API",
        operation_description="점수를 기반으로 베스트 숏츠를 반환합니다.",
        responses={200: BestShortsSerializer()}
    )
    def get(self, request):
        shorts = Short.objects.all()

        # 최대값 계산 (0일 경우 대비하여 1로 설정)
        max_wishes = Wish.objects.count() or 1
        max_comments = Comment.objects.count() or 1
        max_views = Record.objects.count() or 1

        a, b, c = 0.4, 0.2, 0.4  # 가중치
        
        best_shorts = None
        best_score = 0

        for short in shorts:
            book = short.book
            wishes = Wish.objects.filter(book=book).count()
            comments = Comment.objects.filter(book=book).count()
            views = Record.objects.filter(book=book).count()

            # Score 계산
            score = (
                a * (wishes / max_wishes) +
                b * (comments / max_comments) +
                c * (views / max_views)
            )

            if score > best_score:
                best_score = score
                best_short = short

        if not best_short:
            return Response({"error": "베스트 숏츠를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BestShortsSerializer(best_short)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ShortsFilterAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="숏츠 조건별 조회 API",
        operation_description="각 타이틀(조회수, 위시리스트, 댓글)에 따라 상위 10개의 책 ID, 이미지 URL을 반환합니다.",
        manual_parameters=[
            openapi.Parameter(
                "title", openapi.IN_QUERY, 
                description="조회 기준 (조회수, 위시, 댓글)", 
                type=openapi.TYPE_STRING,
                enum=["조회수", "위시", "댓글"]
            ),
            openapi.Parameter(
                "limit", openapi.IN_QUERY, 
                description="반환할 데이터 개수 (기본값 10)", 
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: "성공적으로 데이터를 반환했습니다.",
            400: "Invalid parameters"
        }
    )
    def get(self, request):
        """
        쿼리 파라미터:
        - title: 조회 기준 (조회수, 위시, 댓글 중 하나)
        - limit: 반환 데이터 개수 (기본값 10)
        """

        # 1. 쿼리 파라미터 가져오기
        title = request.query_params.get("title")  # 요청된 기준 (조회수, 위시, 댓글)
        limit = int(request.query_params.get("limit", 10))  # 기본값 10

        # 2. title 값 검증
        if title not in ["조회수", "위시", "댓글"]:
            return Response({"error": "Invalid title parameter. Use '조회수', '위시', or '댓글'."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 요청된 기준에 따라 데이터 필터링
        if title == "조회수":
            # Record 테이블에서 조회수 집계
            records = (
                Record.objects.values("book_id")  # book_id 기준으로 그룹화
                .annotate(count=Count("id"))  # book_id별로 Record 수를 계산
                .order_by("-count")[:limit]  # 조회수가 많은 순으로 정렬 후 상위 limit개 가져오기
            )
            response_data = [
                {"book_id": record["book_id"], "image": Book.objects.get(id=record["book_id"]).image}
                for record in records
            ]

        elif title == "위시":
            # Wish 테이블에서 위시리스트 집계
            wishes = (
                Wish.objects.values("book_id")
                .annotate(count=Count("id"))
                .order_by("-count")[:limit]  # 위시리스트 추가가 많은 순으로 정렬 후 상위 limit개 가져오기
            )
            response_data = [
                {"book_id": wish["book_id"], "image": Book.objects.get(id=wish["book_id"]).image}
                for wish in wishes
            ]

        elif title == "댓글":
            # Comment 테이블에서 댓글 집계
            comments = (
                Comment.objects.values("book_id")
                .annotate(count=Count("id"))
                .order_by("-count")[:limit]  # 댓글 수가 많은 순으로 정렬 후 상위 limit개 가져오기
            )
            response_data = [
                {"book_id": comment["book_id"], "image": Book.objects.get(id=comment["book_id"]).image}
                for comment in comments
            ]

        # 4. 결과 반환
        return Response(response_data, status=status.HTTP_200_OK)