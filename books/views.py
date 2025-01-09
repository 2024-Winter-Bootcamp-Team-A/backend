from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from drf_yasg.utils import swagger_auto_schema  # Swagger 관련 데코레이터 추가
from drf_yasg import openapi  # Swagger를 위한 openapi 모듈

class BookCreateAPIView(APIView):
    """
    이 클래스는 POST 요청을 처리하여
    Book 데이터를 생성하는 API 뷰입니다.
    """

    @swagger_auto_schema(
        operation_summary="책 정보 저장 API",
        operation_description="이 API는 책 정보를 저장하는데 사용됩니다.",
        request_body=BookSerializer,  # 요청 본문에 BookSerializer 사용
        responses={201: BookSerializer,400:"error"}  # 응답도 BookSerializer로 반환
    )
    def post(self, request):
        """
        클라이언트로부터 POST 요청을 받아서 책 정보를 저장하는 메서드입니다.

        Args:
            request: 클라이언트가 보낸 HTTP 요청. JSON 데이터로 책 정보를 포함합니다.

        Returns:
            Response: 책이 성공적으로 저장된 경우 201 상태 코드와 저장된 데이터를 반환합니다.
                      유효성 검증에 실패한 경우 400 상태 코드와 에러 메시지를 반환합니다.
        """
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
