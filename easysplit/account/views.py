from typing import List

from django.db import transaction
from django.db.models import Q, QuerySet
from django_simple_third_party_jwt.views import GoogleLogin
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from account.models import Group, Member
from account.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    GroupSerializer,
    MemberSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="",
                examples={
                    "application/json": {
                        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NzA4MTYwOCwiaWF0IjoxNjg2OTk1MjA4LCJqdGkiOiJlOGVmNWY3ZWMxNGE0YWY0YmY3ODdiYzc0ZDU3YzMyYSIsInVzZXJfaWQiOjF9.Gn5tQI6OB5QL9J5NrxFGdat35wQROVMBYHjIb7YEKfc",
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2OTk1NTA4LCJpYXQiOjE2ODY5OTUyMDgsImp0aSI6ImE2NDNkNWNkYWU2ZTRmMjNhNmU3Y2ViNDdlZmI5MjQ0IiwidXNlcl9pZCI6MX0.zWoiY4AOQWOdGL3afX82afBkdPhGx4NxPjRyTD9QnkM",
                        "username": "admin",
                    }
                },
            )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Username"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Password"
                ),
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    serializer_class = CustomTokenRefreshSerializer

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="",
                examples={
                    "application/json": {
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2OTk1NTA4LCJpYXQiOjE2ODY5OTUyMDgsImp0aSI6ImE2NDNkNWNkYWU2ZTRmMjNhNmU3Y2ViNDdlZmI5MjQ0IiwidXNlcl9pZCI6MX0.zWoiY4AOQWOdGL3afX82afBkdPhGx4NxPjRyTD9QnkM",
                    }
                },
            )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh token"
                ),
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="",
                examples={"application/json": {}},
            )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "token": openapi.Schema(type=openapi.TYPE_STRING, description=""),
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomGoogleLoginView(GoogleLogin):
    """
    API endpoint for Google 3rd part login.
    """

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="",
                examples={
                    "application/json": {
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2OTk1NTA4LCJpYXQiOjE2ODY5OTUyMDgsImp0aSI6ImE2NDNkNWNkYWU2ZTRmMjNhNmU3Y2ViNDdlZmI5MjQ0IiwidXNlcl9pZCI6MX0.zWoiY4AOQWOdGL3afX82afBkdPhGx4NxPjRyTD9QnkM",
                        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2OTk1NTA4LCJpYXQiOjE2ODY5OTUyMDgsImp0aSI6ImE2NDNkNWNkYWU2ZTRmMjNhNmU3Y2ViNDdlZmI5MjQ0IiwidXNlcl9pZCI6MX0.zWoiY4AOQWOdGL3afX82afBkdPhGx4NxPjRyTD9QnkM",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2OTk1NTA4LCJpYXQiOjE2ODY5OTUyMDgsImp0aSI6ImE2NDNkNWNkYWU2ZTRmMjNhNmU3Y2ViNDdlZmI5MjQ0IiwidXNlcl9pZCI6MX0.zWoiY4AOQWOdGL3afX82afBkdPhGx4NxPjRyTD9QnkM",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2OTk1NTA4LCJpYXQiOjE2ODY5OTUyMDgsImp0aSI6ImE2NDNkNWNkYWU2ZTRmMjNhNmU3Y2ViNDdlZmI5MjQ0IiwidXNlcl9pZCI6MX0.zWoiY4AOQWOdGL3afX82afBkdPhGx4NxPjRyTD9QnkM",
                    }
                },
            )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "credential": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Google login credential"
                ),
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserView(APIView):
    """
    API endpoint for retrieving the logged-in user's data.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="",
                examples={
                    "application/json": {
                        "id": 0,
                        "username": "string",
                        "email": "string",
                        "first_name": "string",
                        "last_name": "string",
                    }
                },
            )
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Get the logged-in user's data.

        Args:
            request (HttpRequest): The HTTP request object containing user authentication.

        Returns:
            Response: A JSON response containing the user's data.
                - id (int): The user's ID.
                - username (str): The user's username.
                - email (str): The user's email address.
                - first_name (str): The user's first name.
                - last_name (str): The user's last name.
        """
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )


class GroupViewSet(ModelViewSet):
    """
    API endpoint for managing groups.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Get the queryset for the GroupViewSet.

        Returns:
            queryset: The filtered queryset containing groups that the authenticated user is a member of.

        Example usage:
            GET /api/groups/
        """
        queryset = self.queryset.filter(
            Q(members__user=self.request.user) | Q(owner=self.request.user)
        ).distinct()
        return queryset

    @swagger_auto_schema(
        operation_description="Return groups that the authenticated user is a member of."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MembersView(APIView):
    """
    This view handles the retrieval and updating of members for a specific group.
    """

    permission_classes = (IsAuthenticated,)

    @staticmethod
    def validate_post_data(group: Group, post_data: dict) -> tuple:
        """
        Validate if the provided post_data is valid or not for the given Group.

        Args:
            group (Group): The Group instance to validate against.
            post_data (dict): The data received in the POST request.

        Returns:
            tuple[bool, str]: A tuple containing a boolean indicating if the post_data is valid
                            and an error message (if any).

        Note:
            This function validates if the provided post_data contains any invalid updates or deletions
            related to the group's owner member.

            - If an update is attempted on the group owner, it is considered invalid.
            - If a deletion is attempted on the group owner, it is considered invalid.
        """
        is_valid = True
        error_msg = ""

        if group.members.filter(user=group.owner).exists():
            owner_member = group.members.get(user=group.owner)
            update_members_id = [item["id"] for item in post_data["update"]]
            delete_members_id = {item["id"] for item in post_data["delete"]}
            if str(owner_member.id) in update_members_id:
                is_valid = False
                error_msg = "Can't update group owner"
            elif str(owner_member.id) in delete_members_id:
                is_valid = False
                error_msg = "Can't delete group owner"

        return is_valid, error_msg

    @staticmethod
    def get_member_objs(group_id: str, items: List[dict]) -> QuerySet(Member):
        """
        Create and return a queryset of Member objects based on the provided items.

        Args:
            group_id (str): The group ID to associate with the Member objects.
            items (List[dict]): A list of dictionaries representing the Member data.

        Returns:
            QuerySet[Member]: A queryset containing the created Member objects.
        """
        objs = []
        for item in items:
            item["group_id"] = group_id
            objs.append(Member(**item))
        return objs

    @transaction.atomic
    def update_data(self, group_id: str, post_data: dict):
        """
        Update the group data based on the provided post_data using atomic transaction.

        Args:
            group_id (str): The ID of the group.
            post_data (dict): The data received in the POST request.

        Returns:
            None

        Note:
            This method uses the `transaction.atomic` decorator to ensure that all data is updated
            successfully or rolled back in case of an error.
        """
        create_objs = self.get_member_objs(group_id, post_data["create"])
        Member.objects.bulk_create(create_objs)

        update_objs = self.get_member_objs(group_id, post_data["update"])
        Member.objects.bulk_update(update_objs, fields=["user", "name", "permission"])

        delete_list = post_data["delete"]
        Member.objects.filter(id__in=[item["id"] for item in delete_list]).delete()

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="",
                examples={
                    "application/json": [
                        {
                            "id": "579ca85c-dab2-44b3-a01b-eb49ef77a463",
                            "balances": [],
                            "created_at": "2023-06-18T09:23:04.668668+08:00",
                            "updated_at": "2023-06-18T09:23:04.668676+08:00",
                            "name": "User1",
                            "permission": "view",
                            "user_id": None,
                            "group_id": "aff6e4b8-ec21-4cc8-b7ed-c5e9ea12c76b",
                        }
                    ]
                },
            )
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve and return the members of a group.

        Args:
            request (HttpRequest): The HTTP request object.
            group_id (str): The ID of the group.

        Returns:
            Response: The HTTP response containing the member data.

        Raises:
            NotFound (HTTP_404_NOT_FOUND): If the group with the specified group_id does not exist.
        """
        group_id = kwargs["group_id"]
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        member_serializer = MemberSerializer(
            Member.objects.filter(group__id=group.id), many=True
        )
        return Response(member_serializer.data)

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="",
                examples={
                    "application/json": [
                        {
                            "id": "579ca85c-dab2-44b3-a01b-eb49ef77a463",
                            "balances": [],
                            "created_at": "2023-06-18T09:23:04.668668+08:00",
                            "updated_at": "2023-06-18T09:23:04.668676+08:00",
                            "name": "User1",
                            "permission": "view",
                            "user_id": None,
                            "group_id": "aff6e4b8-ec21-4cc8-b7ed-c5e9ea12c76b",
                        }
                    ]
                },
            )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "create": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Create user list",
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "user_id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=None
                            ),
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING, example="User1"
                            ),
                            "permission": openapi.Schema(
                                type=openapi.TYPE_STRING, example="view"
                            ),
                        },
                    ),
                ),
                "update": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Update user list",
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="579ca85c-dab2-44b3-a01b-eb49ef77a463",
                            ),
                            "user_id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=None
                            ),
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING, example="User1"
                            ),
                            "permission": openapi.Schema(
                                type=openapi.TYPE_STRING, example="view"
                            ),
                        },
                    ),
                ),
                "delete": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Delete user list",
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="579ca85c-dab2-44b3-a01b-eb49ef77a463",
                            ),
                        },
                    ),
                ),
            },
            required=["create", "update", "delete"],
        ),
    )
    def post(self, requset, *args, **kwargs):
        """
        Update and return the members of a group based on the provided data.

        Args:
            request (HttpRequest): The HTTP request object.
            group_id (str): The ID of the group.

        Returns:
            Response: The HTTP response containing the updated member data.

        Raises:
            NotFound (HTTP_404_NOT_FOUND): If the group with the specified group_id does not exist.
            Forbidden (HTTP_403_FORBIDDEN): If the provided data is invalid.
        """
        group_id = kwargs["group_id"]
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        post_data = requset.data

        is_valid, error_msg = self.validate_post_data(group, post_data)
        if not is_valid:
            return Response({"detail": error_msg}, status=status.HTTP_403_FORBIDDEN)
        self.update_data(group.id, post_data)

        member_serializer = MemberSerializer(
            Member.objects.filter(group__id=group.id), many=True
        )
        return Response(member_serializer.data)
