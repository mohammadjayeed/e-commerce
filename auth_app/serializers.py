from djoser.serializers import UserCreateSerializer as BaseClassSerializer
from djoser.serializers import UserSerializer as BaseClassSerializerInfo
from rest_framework import serializers
class CustomUserCreateSerializer(BaseClassSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    class Meta(BaseClassSerializer.Meta):
        fields = ['id','username','password','email','first_name','last_name']

class CustomUserInfoSerializer(BaseClassSerializerInfo):
    class Meta(BaseClassSerializerInfo.Meta):
        fields = ['username','email','first_name','last_name']
