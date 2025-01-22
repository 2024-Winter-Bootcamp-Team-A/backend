from rest_framework import serializers
from .models import Short
from books.models import Book
from wishes.models import Wish

class ShortRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Short
        fields = ['book', 'title', 'storage_url']

class DalleShortRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Short
        fields = ['book']

class ShortIndividualSerializer(serializers.ModelSerializer):
    book_url = serializers.CharField(source='book.book_url', read_only=True)  # 직접 참조
    is_wish = serializers.SerializerMethodField()
    wish_count = serializers.SerializerMethodField()

    class Meta:
        model = Short
        fields = [
            'book_id', 'storage_url', 'book_url', 'title',
            'is_deleted', 'created_at', 'updated_at',
            'is_wish', 'wish_count'
        ]

    def get_is_wish(self, obj):
        """사용자가 해당 책을 위시리스트에 추가했는지 여부 반환"""
        request = self.context.get('request', None)
        user_id = request.session.get('user_id') if request else None

        if user_id:
            return Wish.objects.filter(book=obj.book, user_id=user_id).exists()
        
        return False

    def get_wish_count(self, obj):
        """해당 책의 위시리스트 추가 횟수 반환"""
        return Wish.objects.filter(book=obj.book).count()


class BestShortsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='book.title', read_only=True)
    author = serializers.CharField(source='book.author', read_only=True)
    point = serializers.CharField(source='book.point', read_only=True)
    image = serializers.CharField(source='book.image', read_only=True)
    storage_url = serializers.CharField(read_only=True)

    class Meta:
        model = Short
        fields = ['title', 'author', 'point', 'image', 'storage_url']