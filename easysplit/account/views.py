from typing import List

from django.db import transaction
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.models import Group, Member
from account.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    GroupSerializer,
    MemberSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view.

    This view extends the default TokenObtainPairView provided by the `rest_framework_simplejwt`
    package and uses the custom serializer `CustomTokenObtainPairSerializer` for token retrieval.

    Example usage:
    POST /api/token/obtain/
    {
        "username": "john",
        "password": "password123"
    }
    """

    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom token refresh view.

    This view extends the default TokenRefreshView provided by the `rest_framework_simplejwt`
    package and uses the custom serializer `CustomTokenRefreshSerializer` for token refreshing.

    Example usage:
    POST /api/token/refresh/
    {
        "refresh": "refresh_token_here"
    }
    """

    serializer_class = CustomTokenRefreshSerializer


class GroupViewSet(ModelViewSet):
    """
    API endpoint for managing groups.

    This viewset provides CRUD functionality for the `Group` model. It uses the `GroupSerializer`
    for serialization and supports authenticated requests only (IsAuthenticated permission).

    Example usage:
    GET /api/groups/ - Retrieve all groups
    POST /api/groups/ - Create a new group
    GET /api/groups/{id}/ - Retrieve a specific group
    PUT /api/groups/{id}/ - Update a specific group
    DELETE /api/groups/{id}/ - Delete a specific group
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
        queryset = Group.objects.filter(members__in=[self.request.user.id])
        return queryset


class MembersView(APIView):
    """
    This view handles the retrieval and updating of members for a specific group.
    """

    @staticmethod
    def check_post_data(group: Group, post_data: dict) -> tuple:
        """
        Check if the provided post_data is valid or not for the given Group.

        Args:
            group (Group): The Group instance to check against.
            post_data (dict): The data received in the POST request.

        Returns:
            tuple[bool, str]: A tuple containing a boolean indicating if the post_data is valid
                            and an error message (if any).

        Note:
            This function checks if the provided post_data contains any invalid updates or deletions
            related to the group's owner member.

            - If an update is attempted on the group owner, it is considered invalid.
            - If a deletion is attempted on the group owner, it is considered invalid.
        """
        is_valid = True
        error_msg = ""

        if group.members.filter(user=group.owner).exists():
            owner_member = group.members.get(user=group.owner)
            update_members_id = [item["id"] for item in post_data["update"]]
            delete_members_id = {id for id in post_data["delete"]}
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
        Member.objects.filter(id__in=delete_list).delete()

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

    # key required ["create", "update", "delete"]
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

        is_valid, error_msg = self.check_post_data(group, post_data)
        if not is_valid:
            return Response({"detail": error_msg}, status=status.HTTP_403_FORBIDDEN)
        self.update_data(group.id, post_data)

        member_serializer = MemberSerializer(
            Member.objects.filter(group__id=group.id), many=True
        )
        return Response(member_serializer.data)
