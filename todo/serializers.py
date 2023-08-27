from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model



User = get_user_model()


class TodoSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     print(attrs['title'])
    #     return super().validate(attrs)

    def validate_peririty(self, peririty):
        if (peririty<10 or peririty>20):
            raise serializers.ValidationError('peririty must be betweeen 10 and 20')
        return peririty
    class Meta:
        model = Todo
        fields = '__all__'



class TodoUserSerializer(serializers.ModelSerializer):
    todo = TodoSerializer(read_only=True , many=True)
    class Meta:
        model = User
        fields = '__all__'