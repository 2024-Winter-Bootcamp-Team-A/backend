from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserLoginSerializer
from drf_yasg.utils import swagger_auto_schema  # Swagger 관련 데코레이터 추가
from drf_yasg import openapi  # Swagger를 위한 openapi 모듈
from django.contrib.auth import authenticate, login

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