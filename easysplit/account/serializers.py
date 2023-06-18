from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from account.models import Group, Member
from record.serializers import BalanceSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer.
    """

    def validate(self, attrs):
        """
        Validate the token obtain request and return the serialized data.

        Args:
            attrs (dict): The request data.

        Returns:
            dict: The serialized data containing the access token, refresh token, and username.
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh_token"] = str(refresh)
        data["access_token"] = str(refresh.access_token)
        del data["access"]
        del data["refresh"]
        data["username"] = self.user.username
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom token refresh serializer.
    """

    def validate(self, attrs):
        """
        Validate the token refresh request and return the serialized data.

        Args:
            attrs (dict): The request data.

        Returns:
            dict: The serialized data containing the access token.
        """
        data = super().validate(attrs)
        data["access_token"] = data.get("access")
        del data["access"]
        return data


class GroupSerializer(ModelSerializer):
    """
    Serializer for the Group model.
    """

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
    """
    Serializer for the Member model.
    """

    balances = BalanceSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = "__all__"
