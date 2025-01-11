from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema  # Swagger 관련 데코레이터 추가
from drf_yasg import openapi  # Swagger를 위한 openapi 모듈

class UserCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="회원가입 API",
        operation_description="이 API는 새로운 사용자를 생성하는 데 사용됩니다.",
        request_body=UserSerializer,  # 요청 본문에 UserSerializer 사용
        responses={201: openapi.Response("회원가입이 완료되었습니다."), 400: "error"}  # 응답에 대한 설명
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)