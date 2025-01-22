from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShortRequestSerializer, ShortIndividualSerializer, BestShortsSerializer, DalleShortRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Short
from books.models import Book
from records.models import Record
from wishes.models import Wish
from django.db.models import Count, Q
from comments.models import Comment
from .gen_video import generate_dalle_video
from drf_yasg import openapi
import json
import os


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
    

class ShortsDalleAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="숏츠 저장 API, 근데 이제 DALLE를 곁들인",
        operation_description="영상을 생성할 때마다 돈이 사라지는 마술을 경험하세요. 상당히 비쌉니다.",
        request_body=DalleShortRequestSerializer,
        responses={201: "숏츠 생성을 완료했습니다.",400:"error"}
    )
    def post(self, request):
        serializer = DalleShortRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "book_is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        book = serializer.validated_data["book"]
        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        
        story_json = json.loads(book.story)
        storage_url = generate_dalle_video(3, book.prompt, book.story, str(book.id) + ".mp4")
        

        short_data = {
            'book': book.id,
            'title': story_json["title"],
            'storage_url': storage_url,
        }
        short_serializer = ShortRequestSerializer(data=short_data)

        if short_serializer.is_valid():
            short_serializer.save()
            return Response(short_serializer.data, status=status.HTTP_201_CREATED)

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

class ShortIndividualsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="숏츠 개별 조회 API (사이드패널)",
        operation_description="특정 book_url에 해당하는 숏츠 정보를 반환합니다.",
        manual_parameters=[  
            openapi.Parameter(
                'book_url',  
                openapi.IN_QUERY, 
                description="조회할 책의 URL",
                type=openapi.TYPE_STRING, 
                required=True  # 필수 값 지정
            )
        ],
        responses={200: ShortIndividualSerializer()}
    )
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"error": "로그인되지 않았습니다."})
        
        book_url = request.GET.get('book_url')

        if not book_url:
            return Response({"error": "book_url을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(book_url=book_url)
            short = Short.objects.get(book=book)

            serializer = ShortIndividualSerializer(short, context={"request": request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response({"error": "해당 book_url로 책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        except Short.DoesNotExist:
            return Response({"error": "해당 book_url로 숏츠를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

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
                enum=["조회수", "위시", "댓글"],
                required=False
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
        if title is not None and title not in ["조회수", "위시", "댓글"]:
            return Response({"error": "Invalid title parameter. Use '조회수', '위시', or '댓글'."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 요청된 기준에 따라 데이터 필터링
        if not title:
            # 전체 책 조회
            shorts = Short.objects.all()
            response_data = []

            for short in shorts:
                # Short ID와 동일한 ID를 가진 Book 데이터 조회
                book = Book.objects.filter(id=short.id).first()
                if book:
                    response_data.append({
                        "book_id": book.id,
                        "image": book.image
                    })
        
        elif title == "조회수":
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


class ShortsSearchAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="숏츠 검색 API",
        operation_description="책 제목 또는 저자명에 특정 단어나 문장이 포함된 숏츠를 검색합니다.",
        manual_parameters=[ 
            openapi.Parameter(
                'search',  
                openapi.IN_QUERY, 
                description="검색어 (책 제목 또는 저자)",
                type=openapi.TYPE_STRING, 
                required=True  
            )
        ],
        responses={200: "List of book_id and image", 401: "로그인되지 않았습니다."}
    )
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"status": "error", "message": "로그인되지 않았습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 검색어 가져오기
        search_query = request.GET.get('search', '').strip()

        if not search_query:
            return Response({"error": "검색어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 책 제목 또는 저자에서 검색
        matching_books = Book.objects.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )

        # 해당 책에 연결된 숏츠 조회
        matching_shorts = Short.objects.filter(book__in=matching_books).select_related("book")

        if not matching_shorts.exists():
            return Response(
        {"message": "검색 결과가 없습니다.", "results": []}, 
        status=status.HTTP_200_OK
    )

        # 결과 리스트 생성
        result = [{"book_id": short.book.id, "image": short.book.image} for short in matching_shorts]

        return Response(result, status=status.HTTP_200_OK)
    