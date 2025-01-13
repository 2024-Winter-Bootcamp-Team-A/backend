from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Record
from books.models import Book
from users.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RecordAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="시청 기록 생성 API",
        operation_description="사용자가 특정 책의 숏츠를 시청한 기록을 생성합니다.",
        responses={
            201: openapi.Response("시청 기록이 생성되었습니다."),
            400: "잘못된 요청입니다.",
            401: "인증 실패.",
            404: "책 또는 사용자 없음."
        }
    )
    def post(self, request, book_id):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"error": "로그인된 사용자만 시청 기록을 생성할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)

            # 생성
            record = Record.objects.create(user=user, book=book)
            return Response({"message": "시청 기록이 생성되었습니다."}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

