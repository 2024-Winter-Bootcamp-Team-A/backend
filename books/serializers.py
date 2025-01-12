# Serializer는 API로 받은 데이터를 모델과 연결해주는 역할
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'category', 'title', 'author', 'publisher',
            'image', 'point', 'story', 'prompt', 'book_url',
            'is_deleted', 'created_at', 'updated_at'
        ]