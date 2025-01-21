from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from records.models import Record
from books.models import Book
from users.models import User
from shorts.models import Short
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


class RecordsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="시청 기록 전체 조회 API",
        operation_description="사용자의 시청 기록을 반환합니다.",
        responses={
            200: openapi.Response(
                description="시청 기록 조회 성공",
                examples={
                    "application/json": {
                        "status": "success",
                        "records": [
                            { "image": "https://example.com/image1.jpg" },
                            { "image": "https://example.com/image2.jpg" }
                        ]
                    }
                }
            ),
            401: "로그인되지 않은 사용자입니다.",
            500: "서버 에러"
        }
    )
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"status": "error", "message": "로그인되지 않았습니다."}, status=401)

        records = Record.objects.filter(user_id=user_id).select_related('book').order_by('-created_at')

        images = [{"image": record.book.image} for record in records]

        return Response({"records": images}, status=200)