from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FAQ
from .serializers import FAQSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class FAQAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="FAQ 생성 API",
        operation_description="새로운 FAQ를 생성합니다.",
        request_body=FAQSerializer,
        responses={201: "FAQ가 생성되었습니다.", 400: "잘못된 요청입니다.", 401: "인증이 필요합니다."}
    )
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="FAQ 전체 조회 API",
        operation_description="등록된 모든 FAQ를 조회합니다.",
        responses={200: FAQSerializer(many=True)}
    )
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        faqs = FAQ.objects.all().order_by('-created_at')
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FAQSearchAPIView(APIView):
    
    @swagger_auto_schema(
        operation_summary="FAQ 검색 API",
        operation_description="질문 내용을 기반으로 FAQ를 검색합니다.",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="검색어", type=openapi.TYPE_STRING)
        ],
        responses={200: FAQSerializer(many=True), 404: "검색 결과가 없습니다.", 401: "인증이 필요합니다."}
    )
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        query = request.GET.get('query', '')
        if not query:
            return Response({"error": "검색어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        faqs = FAQ.objects.filter(question__icontains=query)
        if faqs.exists():
            serializer = FAQSerializer(faqs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "검색 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
