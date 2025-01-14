from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi
from django.db.models import Count, F, Case, When, CharField, Value
from shorts.models import Short
from comments.models import Comment
from wishes.models import Wish
from records.models import Record
from datetime import timedelta, date
from collections import defaultdict
from django.utils.timezone import now
from django.db.models.functions import TruncDate   



class MostViewedAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Most Viewed Shorts API",
        operation_description="조회수가 가장 높은 숏츠의 통계 데이터를 반환합니다.",
        responses={
            200: openapi.Response(
                description="성공적으로 통계 데이터를 반환합니다.",
                examples={
                    "application/json": {
                        "views": 120,
                        "wishes": 50,
                        "shares": 20,
                        "book_visits": 10,
                        "gender_stats": {
                        "male": 700,
                        "female": 300
                        },
                        "age_stats": {
                        "10s": 200,
                        "20s": 500,
                        "30s": 300
                        },
                        "date_stats": [
                        {"date": "2024-01-01", "count": 200},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        ]
                    }
                }
            ),
            404: "조회 데이터 없음",
        }
    )
    def get(self, request):
        # 조회수가 가장 높은 숏츠 가져오기
        most_viewed_short = Short.objects.annotate(
            total_views=F('book__record')
        ).order_by('-total_views').first()

        if not most_viewed_short:
            return Response({"error": "조회수가 높은 숏츠가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 날짜별 조회수 통계
        recent_date_range = now() - timedelta(days=7)
        date_list = [(recent_date_range + timedelta(days=i)).date() for i in range(8)]

        raw_date_stats = Record.objects.filter(
            book=most_viewed_short.book,
            created_at__gte=recent_date_range
        ).annotate(date=TruncDate('created_at')).values(
            'date'
        ).annotate(
            count=Count('id')
        ).order_by('date')

        if raw_date_stats is None:
            raw_date_stats = []

        date_stats = {str(item["date"]): item["count"] for item in raw_date_stats}
        full_date_stats = [{"date": str(day), "count": date_stats.get(str(day), 0)} for day in date_list]

        # 성별 별 통계
        gender_raw_stats = Record.objects.filter(
            book=most_viewed_short.book
        ).values("user__sex").annotate(
            count=Count("id")
        )

        gender_stats = {
            "male": next((item['count'] for item in gender_raw_stats if item["user__sex"] == 0), 0),
            "female": next((item['count'] for item in gender_raw_stats if item["user__sex"] == 1), 0)
        }

        # 연령별 통계
        age_stats_raw = Record.objects.filter(
            book=most_viewed_short.book
        ).annotate(
            age_group=Case(
                When(user__age__lt=20, then=Value("10s")),
                When(user__age__gte=20, user__age__lt=30, then=Value("20s")),
                When(user__age__gte=30, user__age__lt=40, then=Value("30s")),
                When(user__age__gte=40, user__age__lt=50, then=Value("40s")),
                default=Value("50s+"),
                output_field=CharField(),
            )
        ).values("age_group").annotate(
            count=Count("id")
        )

        age_stats = {item["age_group"]: item["count"] for item in age_stats_raw}
        full_age_stats = {group: age_stats.get(group, 0) for group in ["10s", "20s", "30s", "40s", "50s+"]}

        return Response({
            "views": Record.objects.filter(book=most_viewed_short.book).count(),
            "wishes": Wish.objects.filter(book=most_viewed_short.book).count(),
            "shares": most_viewed_short.share_count,
            "book_visits": most_viewed_short.book_visit_count,
            "gender_stats": gender_stats,
            "age_stats": full_age_stats,
            "date_stats": full_date_stats
        }, status=status.HTTP_200_OK)



class MostWishedAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Most Wished Shorts API",
        operation_description="위시리스트에 가장 많이 추가된 숏츠의 통계 데이터를 반환합니다.",
        responses={
            200: openapi.Response(
                description="성공적으로 통계 데이터를 반환합니다.",
                examples={
                    "application/json": {
                        "views": 70,
                        "wishes": 50,
                        "shares": 20,
                        "book visits": 10,
                        "gender_stats": {
                        "male": 700,
                        "female": 300
                        },
                        "age_stats": {
                        "10s": 200,
                        "20s": 500,
                        "30s": 300
                        },
                        "date_stats": [
                        {"date": "2024-01-01", "count": 200},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        {"date": "2024-01-02", "count": 300},
                        ]
                    }
                }
            ),
            404: "위시리스트 데이터 없음",
        }
    )
    def get(self, request):
        # 위시리스트에 가장 많이 추가된 숏츠 가져오기
        most_wished_short = Short.objects.annotate(
            total_wishes=Count('book__wish')
        ).order_by('-total_wishes').first()

        if not most_wished_short:
            return Response({"error": "위시리스트 데이터가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 날짜별 위시리스트 저장 통계
        recent_date_range = now() - timedelta(days=7)
        date_list = [(recent_date_range + timedelta(days=i)).date() for i in range(8)]

        raw_date_stats = Wish.objects.filter(
            book=most_wished_short.book,
            created_at__gte=recent_date_range
        ).annotate(date=TruncDate('created_at')).values(
            'date'
        ).annotate(
            count=Count('id')
        ).order_by('date')

        if raw_date_stats is None:
            raw_date_stats = []

        date_stats = {str(item["date"]): item["count"] for item in raw_date_stats}
        full_date_stats = [{"date": str(day), "count": date_stats.get(str(day), 0)} for day in date_list]

        # 성별 별 통계
        gender_raw_stats = Wish.objects.filter(
            book=most_wished_short.book
        ).values("user__sex").annotate(
            count=Count("id")
        )

        gender_stats = {
            "male": next((item['count'] for item in gender_raw_stats if item["user__sex"] == 0), 0),
            "female": next((item['count'] for item in gender_raw_stats if item["user__sex"] == 1), 0)
        }

        # 연령별 통계
        age_stats_raw = Wish.objects.filter(
            book=most_wished_short.book
        ).annotate(
            age_group=Case(
                When(user__age__lt=20, then=Value("10s")),
                When(user__age__gte=20, user__age__lt=30, then=Value("20s")),
                When(user__age__gte=30, user__age__lt=40, then=Value("30s")),
                When(user__age__gte=40, user__age__lt=50, then=Value("40s")),
                default=Value("50s+"),
                output_field=CharField(),
            )
        ).values("age_group").annotate(
            count=Count("id")
        )

        age_stats = {item["age_group"]: item["count"] for item in age_stats_raw}
        full_age_stats = {group: age_stats.get(group, 0) for group in ["10s", "20s", "30s", "40s", "50s+"]}

        return Response({
            "views": Record.objects.filter(book=most_wished_short.book).count(),
            "wishes": Wish.objects.filter(book=most_wished_short.book).count(),
            "shares": most_wished_short.share_count,
            "book_visits": most_wished_short.book_visit_count,
            "gender_stats": gender_stats,
            "age_stats": full_age_stats,
            "date_stats": full_date_stats
        }, status=status.HTTP_200_OK)
    

class MostCommentedAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Most Commented Shorts API",
        operation_description="댓글이 가장 많이 달린 숏츠의 통계 데이터를 반환합니다.",
        responses={
            200: openapi.Response(
                description="성공적으로 통계 데이터를 반환합니다.",
                examples={
                    "application/json": {
                        "views": 150,
                        "wishes": 60,
                        "shares": 25,
                        "book_visits": 40,
                        "gender_stats": {
                            "male": 20,
                            "female": 40
                        },
                        "age_stats": {
                            "10s": 15,
                            "20s": 30,
                            "30s": 15
                        },
                        "date_stats": [
                            {"date": "2025-01-08", "count": 5},
                            {"date": "2025-01-09", "count": 8},
                            {"date": "2025-01-10", "count": 12},
                            {"date": "2025-01-11", "count": 18},
                            {"date": "2025-01-12", "count": 10},
                            {"date": "2025-01-13", "count": 7},
                            {"date": "2025-01-14", "count": 5}
                        ]
                    }
                }
            ),
            404: "댓글 데이터 없음",
        }
    )
    def get(self, request):
        # 댓글이 가장 많은 숏츠 가져오기
        most_commented_short = Short.objects.annotate(
            total_comments=Count('book__comments')
        ).order_by('-total_comments').first()

        if not most_commented_short:
            return Response({"error": "댓글 데이터가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 날짜별 댓글 통계
        recent_date_range = now() - timedelta(days=7)
        date_list = [(recent_date_range + timedelta(days=i)).date() for i in range(8)]

        raw_date_stats = Comment.objects.filter(
            book=most_commented_short.book,
            created_at__gte=recent_date_range
        ).annotate(date=TruncDate('created_at')).values(
            'date'
        ).annotate(
            count=Count('id')
        ).order_by('date')

        if raw_date_stats is None:
            raw_date_stats = []

        date_stats = {str(item["date"]): item["count"] for item in raw_date_stats}
        full_date_stats = [{"date": str(day), "count": date_stats.get(str(day), 0)} for day in date_list]

        # 성별 별 통계
        gender_raw_stats = Comment.objects.filter(
            book=most_commented_short.book
        ).values("user__sex").annotate(
            count=Count("id")
        )

        gender_stats = {
            "male": next((item['count'] for item in gender_raw_stats if item["user__sex"] == 0), 0),
            "female": next((item['count'] for item in gender_raw_stats if item["user__sex"] == 1), 0)
        }

        # 연령별 통계
        age_stats_raw = Comment.objects.filter(
            book=most_commented_short.book
        ).annotate(
            age_group=Case(
                When(user__age__lt=20, then=Value("10s")),
                When(user__age__gte=20, user__age__lt=30, then=Value("20s")),
                When(user__age__gte=30, user__age__lt=40, then=Value("30s")),
                When(user__age__gte=40, user__age__lt=50, then=Value("40s")),
                default=Value("50s+"),
                output_field=CharField(),
            )
        ).values("age_group").annotate(
            count=Count("id")
        )

        age_stats = {item["age_group"]: item["count"] for item in age_stats_raw}
        full_age_stats = {group: age_stats.get(group, 0) for group in ["10s", "20s", "30s", "40s", "50s+"]}

        return Response({
            "views": Record.objects.filter(book=most_commented_short.book).count(),
            "wishes": Wish.objects.filter(book=most_commented_short.book).count(),
            "shares": most_commented_short.share_count,
            "book_visits": most_commented_short.book_visit_count,
            "gender_stats": gender_stats,
            "age_stats": full_age_stats,
            "date_stats": full_date_stats
        }, status=status.HTTP_200_OK)