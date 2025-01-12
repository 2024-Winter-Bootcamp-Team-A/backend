from rest_framework import serializers
from .models import Short

class ShortRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Short
        fields = ['book', 'title', 'storage_url']