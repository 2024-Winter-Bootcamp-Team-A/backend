from rest_framework import serializers
from .models import Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'user', 'book', 'created_at']
        read_only_fields = ['id', 'created_at']