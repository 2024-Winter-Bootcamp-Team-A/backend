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
                            {
                                "book_title": "소설 A",
                                "category": "소설",
                                "image": "https://example.com/image1.jpg",
                                "book_url": "https://example.com/book1",
                                "short_url": "https://example.com/short1",
                                "viewed_at": "2025-01-01"
                            },
                            {
                                "book_title": "소설 B",
                                "category": "시/에세이",
                                "image": "https://example.com/image2.jpg",
                                "book_url": "https://example.com/book2",
                                "short_url": "https://example.com/short2",
                                "viewed_at": "2025-01-02"
                            }
                        ]
                    }
                }
            ),
            401: "로그인되지 않은 사용자입니다.",
            500: "서버 에러"
        }
    )
    def get(self, request, book_id=None):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"status": "error", "message": "로그인되지 않았습니다."}, status=401)

        try:
            if book_id:
                records = Record.objects.filter(user_id=user_id, book_id=book_id).select_related('book').order_by('-created_at')
            else:
                records = (
                Record.objects.filter(user_id=user_id)
                .select_related('book') 
                .order_by('-created_at')
            )

            result = [
                {
                    "book_title": record.book.title,
                    "category": record.book.category,
                    "image": record.book.image,
                    "book_url": record.book.book_url,
                    "short_url": Short.objects.filter(book_id=record.book.id).first().storage_url if Short.objects.filter(book_id=record.book.id).exists() else None,
                    "viewed_at": record.created_at.strftime('%Y-%m-%d') 
                }
                for record in records
            ]

            return Response({"status": "success", "records": result}, status=200)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)