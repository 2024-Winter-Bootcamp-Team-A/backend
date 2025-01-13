from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Wish
from books.models import Book
from users.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class WishAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="위시리스트 추가 API",
        operation_description="사용자가 특정 책을 위시리스트에 추가합니다.",
        responses={
            201: openapi.Response("위시리스트에 추가되었습니다."),
            400: "잘못된 요청입니다.",
            404: "책 또는 사용자 없음."
        }
    )
    def post(self, request, book_id):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"error": "로그인된 사용자만 위시리스트를 사용할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)

            # 중복 추가 방지
            if Wish.objects.filter(user=user, book=book).exists():
                return Response({"error": "이미 위시리스트에 추가된 책입니다."}, status=status.HTTP_400_BAD_REQUEST)

            # 추가
            Wish.objects.create(user=user, book=book)
            return Response({"message": "위시리스트에 추가되었습니다."}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="위시리스트 삭제 API",
        operation_description="사용자가 특정 책을 위시리스트에서 삭제합니다.",
        responses={
            200: openapi.Response("위시리스트에서 삭제되었습니다."),
            400: "잘못된 요청입니다.",
            404: "책 또는 사용자 없음."
        }
    )
    def delete(self, request, book_id):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"error": "로그인된 사용자만 위시리스트를 사용할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)

            # 삭제
            wish = Wish.objects.filter(user=user, book=book).first()

            if not wish:
                return Response({"error": "위시리스트에 해당 책이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            wish.delete()
            return Response({"message": "위시리스트에서 삭제되었습니다."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
