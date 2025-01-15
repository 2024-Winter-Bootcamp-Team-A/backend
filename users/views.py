from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from records.models import Record
from wishes.models import Wish
from shorts.models import Short
from books.models import Book
from .serializers import UserSerializer, UserLoginSerializer
from drf_yasg.utils import swagger_auto_schema  # Swagger 관련 데코레이터 추가
from drf_yasg import openapi  # Swagger를 위한 openapi 모듈
from django.contrib.auth import authenticate, login
from django.db.models import Count, Subquery, OuterRef

class UserCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="회원가입 API",
        operation_description="이 API는 새로운 사용자를 생성하는 데 사용됩니다.",
        request_body=UserSerializer,
        responses={201: openapi.Response("회원가입이 완료되었습니다."), 400: "error"}  # 응답에 대한 설명
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="로그인 API",
        operation_description="이 API는 이메일과 비밀번호를 사용하여 로그인합니다.",
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response("로그인을 성공했습니다."),
            400: "잘못된 요청입니다.",
            401: "인증 실패",
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            try:
                user = User.objects.get(email=email)
                if user.password == password:
                    # 세션에 사용자 정보 저장
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return Response({"message": f"{user.name}님, 로그인을 성공했습니다."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "비밀번호가 올바르지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "해당 이메일을 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="회원정보 조회 API",
        operation_description="로그인한 사용자의 프로필 정보를 보여줍니다.",
        responses={
            200: openapi.Response(
                description="회원정보 조회 성공",
                examples={
                    "application/json": {
                        "name": "양현민",
                        "email": "gusals1234@naver.com",
                        "join_date": "2025-01-01",
                        "watched_count": 50,
                        "preferred_categories": {
                            "인문학": 1,
                            "소설": 3,
                            "사회학": 2,
                        },
                        "recent_images": {
                            "watched": ["image_url_1", "image_url_2"],
                            "wished": ["image_url_3", "image_url_4"],
                            "sentence_card": ["image_url_5", "image_url_6"],
                        },
                    }
                },
            ),
            401: "로그인되지 않은 사용자입니다.",
        }
    )
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"error": "로그인되지 않았습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=user_id)

            # xxx 님은 xxxx.xx.xx일부터 xx개의 작품을 감상~
            join_date = user.created_at.date()
            watched_count = Record.objects.filter(user=user).count()

            # 선호 카테고리
            category_stats = (
                Record.objects.filter(
                    user=user, 
                    id=Subquery(
                        Record.objects.filter(
                            user=user,
                            book=OuterRef("book")
                        ).values("id")[:1] 
                    )
                )
                .values("book__category")
                .annotate(count=Count("book__category"))
                .order_by("-count")
            )
            preferred_categories = {item["book__category"]: item["count"] for item in category_stats}

            # 시청 기록 이미지
            recent_watched = (
                Record.objects.filter(user=user)
                .select_related("book")
                .order_by("-created_at")[:2]
            )
            recent_watched_images = [record.book.image for record in recent_watched]

            # 위시리스트 숏츠 이미지
            recent_wished = (
                Wish.objects.filter(user=user)
                .select_related("book")
                .order_by("-created_at")[:2]
            )
            recent_wished_images = [wish.book.image for wish in recent_wished]

            # 문장 카드 이미지
            recent_sentence_card = (
                Short.objects.filter(book__record__user=user)
                .select_related("book")
                .order_by("-created_at")[:2]
            )
            recent_sentence_card_images = [short.book.image for short in recent_sentence_card]

            response_data = {
                "name": user.name,
                "email": user.email,
                "name": user.name,
                "join_date": join_date,
                "watched_count": watched_count,
                "preferred_categories": preferred_categories,
                "recent_images": {
                    "watched": recent_watched_images,
                    "wished": recent_wished_images,
                    "sentence_card": recent_sentence_card_images,
                },
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)