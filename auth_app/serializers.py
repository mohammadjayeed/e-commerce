from djoser.serializers import UserCreateSerializer as BaseClassSerializer

class CustomUserCreateSerializer(BaseClassSerializer):
    class Meta(BaseClassSerializer.Meta):
        fields = ['id','username','password','email','first_name','last_name']
