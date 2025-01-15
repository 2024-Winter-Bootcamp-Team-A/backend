from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from shorts.models import Short  # books 앱에서 Book 모델 가져오기
from users.models import User
from books.models import Book
from .models import TodaysShorts  # 동일 앱에서 TodaysShorts 가져오기
from datetime import timedelta  # 날짜 계산
from django.utils.timezone import now  # 현재 시간

class TodaysShortsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="오늘의 숏츠 조회 API",
        operation_description=(
            "오늘 생성된 숏츠 데이터를 조회합니다."
            "오늘 데이터가 없는 경우, 랜덤으로 2개의 문장을 반환합니다."
        ),
        responses={
            200: "성공적으로 숏츠 데이터를 반환했습니다.",
            500: "서버 에러",
        },
    )
    def get(self, request):
        try:
            # 1. 오늘 날짜 계산
            today_start = now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)

            # 2. 오늘의 숏츠 조회
            todays_shorts = TodaysShorts.objects.filter(
                created_at__range=(today_start, today_end),  # 오늘 날짜 범위
                is_deleted=False,  # 삭제되지 않은 데이터
            ).first()

            # 3. 오늘의 데이터가 있는 경우
            if todays_shorts:
                short = Short.objects.get(book=todays_shorts.book_id)
                data = {
                    "id": todays_shorts.id,
                    "sentence": short.point, # 선택한 문장 반환
                    "image": short.image, # 표지 반환
                }
                return Response({"status": "success", "shorts": [data]}, status=status.HTTP_200_OK)

            # 4. 오늘 데이터가 없는 경우
            random_books = Short.objects.order_by("?")[:2]  # 랜덤으로 2개의 책 선택
            random_data = [
                {
                    "id": book.id,
                    "sentence": book.point, # 랜덤 문장 반환
                } for book in random_books
            ]
            return Response({"status": "success", "shorts": random_data}, status=status.HTTP_200_OK)

        except Exception as e:
            # 에러 발생 시 처리
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateTodaysShortSAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="오늘의 숏츠 저장 API",
        operation_description="책 ID를 받아 오늘의 숏츠 테이블에 저장하고, 저장된 핵심문장과 표지를 반환합니다.",
        responses={
            200: "성공적으로 저장되었습니다.",
            400: "요청이 잘못되었습니다.",
            404: "책을 찾을 수 없습니다."
        }
    )
    def post(self, request, book_id):
        try:
            # user_id 가져오기
            user_id = request.session.get('user_id')
            if not user_id:
                return Response({"status": "error", "message": "로그인되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # 1. book_id에 해당하는 책 조회
            short = Short.objects.get(book=book_id)
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)

            # 2. 이미 오늘의 숏츠가 존재하는지 확인
            existing_entry = TodaysShorts.objects.filter(book_id=book_id).first()
            if not existing_entry:
                # 3. 없으면 새로운 데이터를 생성
                TodaysShorts.objects.create(book_id=short,user_id=user)
    

            # 4. 반환할 데이터 구성
            response_data = {
                "image": book.image,
                "point": book.point,  # 핵심문장
            }

            return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)

        except Short.DoesNotExist:
            return Response({"status": "error", "message": "해당 ID의 숏츠를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        