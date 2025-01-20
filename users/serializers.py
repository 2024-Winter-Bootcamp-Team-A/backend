from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    sex = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'sex', 'age',]
        read_only_fields = ['id']

    def validate_sex(self, value):
        """API에서 'male', 'female'을 받으면 DB에 0, 1로 변환"""
        gender_mapping = {"male": 0, "female": 1}
        if value not in gender_mapping:
            raise serializers.ValidationError("성별은 'male' 또는 'female'로 입력해야 합니다.")
        return gender_mapping[value]

    def to_representation(self, instance):
        """DB에 저장된 0, 1 값을 API 응답에서 'male', 'female'로 변환"""
        representation = super().to_representation(instance)
        gender_mapping = {0: "male", 1: "female"}
        representation["sex"] = gender_mapping.get(instance.sex, None)
        return representation

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)