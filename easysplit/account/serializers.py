from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from account.models import Group, Member


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh_token"] = str(refresh)
        data["access_token"] = str(refresh.access_token)
        del data["access"]
        del data["refresh"]
        data["username"] = self.user.username
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["access_token"] = data.get("access")
        del data["access"]
        return data


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "owner",
            "note",
            "public_permission",
            "primary_currency",
        ]


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
