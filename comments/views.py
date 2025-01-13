from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from books.models import Book
from users.models import User
from .serializers import CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CommentAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="댓글 생성 API",
        operation_description="사용자가 특정 책의 댓글을 생성합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='댓글 내용'),
            },
            required=['content']
        ),
        responses={
            201: openapi.Response("댓글이 생성되었습니다."),
            400: "잘못된 요청입니다.",
            401: "인증 실패",
            404: "책 또는 사용자 없음"
        }
    )
    def post(self, request, book_id):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"error": "로그인된 사용자만 댓글을 생성할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        content = request.data.get('content')
        if not content:
            return Response({"error": "댓글 내용이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)

            Comment.objects.create(user=user, book=book, content=content)
            return Response({"message": "댓글이 생성되었습니다."}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="댓글 전체 조회 API",
        operation_description="특정 책에 달린 모든 댓글을 조회합니다.",
        responses={
            200: openapi.Response("성공", CommentSerializer(many=True)),
            404: "책을 찾을 수 없습니다."
        }
    )
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            comments = Comment.objects.filter(book=book, is_deleted=False)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class CommentDeleteAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="댓글 삭제 API",
        operation_description="특정 댓글을 삭제합니다.",
        responses={
            200: openapi.Response("댓글이 삭제되었습니다."),
            404: "댓글을 찾을 수 없습니다.",
            401: "인증 실패"
        }
    )
    def delete(self, request, book_id, comment_id):
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"error": "로그인된 사용자만 댓글을 삭제할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            comment = Comment.objects.get(id=comment_id, book_id=book_id, user_id=user_id)
            comment.is_deleted = True
            comment.save()
            return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_200_OK)

        except Comment.DoesNotExist:
            return Response({"error": "댓글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)