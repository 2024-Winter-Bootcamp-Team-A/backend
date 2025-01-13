from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShortRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Short


class ShortsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="숏츠 저장 API",
        operation_description="이 API는 숏츠를 저장하는데 사용됩니다.",
        request_body=ShortRequestSerializer,
        responses={201: "숏츠 생성을 완료했습니다.",400:"error"}
    )
    def post(self, request):

        serializer = ShortRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ShortVisitAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="사이트 방문 수 증가 API",
        operation_description="특정 숏츠의 책 구매 사이트 방문 수를 증가시킵니다.",
        responses={
            200: "책 구매 사이트를 방문하였습니다.",
            404: "숏츠를 찾을 수 없습니다."
        }
    )
    def put(self, request, book_id):
        try:
            short = Short.objects.get(book_id=book_id)

            short.book_visit_count += 1
            short.save()

            return Response({"message": "책 구매 사이트를 방문하였습니다."}, status=status.HTTP_200_OK)
        except Short.DoesNotExist:
            return Response({"error": "숏츠를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
