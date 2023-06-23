from typing import Optional

from django.urls import reverse
from pydantic import BaseModel, ValidationError
from rest_framework import status

from common.tests import BaseTestCase, incorrect_format_message


class UserDataModel(BaseModel):
    """
    Represents the data model for user data.
    """

    id: int
    username: str
    email: str
    first_name: str
    last_name: str


class AccountTests(BaseTestCase):
    """
    Test case class for account-related tests.
    """

    def test_user_login(self):
        """
        Test user login.
        """
        response = self.client.post(reverse("token_get"), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_data(self):
        """
        Test retrieving logged-in user's data.
        """
        response = self.client.get(reverse("user_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            data = response.json()
            user_data = UserDataModel(**data)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))


class GroupDataModel(BaseModel):
    """
    Represents the data model for group data.
    """

    id: str
    name: str
    owner: int
    note: str
    public_permission: str
    primary_currency: str


class GroupTests(BaseTestCase):
    """
    Test case class for group-related tests.
    """

    def test_retrieve_group(self):
        """
        Test retrieving group.
        """
        response = self.client.get(
            reverse("group-detail", kwargs={"pk": self.default_group.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            data = response.json()
            group_data = GroupDataModel(**data)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

    def test_list_group(self):
        """
        Test listing group data.
        """
        response = self.client.get(reverse("group-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            data = response.json()
            self.assertIsInstance(data, list)
            for item in data:
                group_data = GroupDataModel(**item)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

    def test_create_group(self):
        """
        Test creating group.
        """
        group_data = {
            "name": "Test create group",
            "owner": self.user.id,
            "note": "This is a test group.",
            "public_permission": "limited",
            "primary_currency": "TWD",
        }
        response = self.client.post(reverse("group-list"), data=group_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        try:
            data = response.json()
            group_data = GroupDataModel(**data)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

    def test_update_group(self):
        """
        Test updating group.
        """
        group_data = {"name": "Test update group"}
        response = self.client.patch(
            reverse("group-detail", kwargs={"pk": self.default_group.id}),
            data=group_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            data = response.json()
            group_data = GroupDataModel(**data)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

    def test_delete_group(self):
        """
        Test deleting group.
        """
        response = self.client.delete(
            reverse("group-detail", kwargs={"pk": self.default_group.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MemberDataModel(BaseModel):
    """
    Represents the data model for member data.
    """

    id: str
    balances: list
    created_at: str
    updated_at: str
    name: str
    permission: str
    user: Optional[int]
    group: str


class MemberTests(BaseTestCase):
    """
    Test case class for member-related tests.
    """

    def test_list_member(self):
        """
        Test listing members.
        """
        response = self.client.get(
            reverse("members", kwargs={"group_id": self.default_group.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            data = response.json()
            self.assertIsInstance(data, list)
            for item in data:
                member_data = MemberDataModel(**item)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

    def test_create_member(self):
        """
        Test creating member.
        """
        members_data = {
            "create": [{"user_id": None, "name": "New member", "permission": "view"}],
            "update": [],
            "delete": [],
        }
        response = self.client.post(
            reverse("members", kwargs={"group_id": self.default_group.id}),
            data=members_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            data = response.json()
            self.assertIsInstance(data, list)
            member_data = MemberDataModel(**data[0])
            self.assertEqual(data[-1]["name"], "New member")
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

    def test_update_member(self):
        """
        Test updating member.
        """
        members_data = {
            "create": [],
            "update": [
                {
                    "id": self.binded_member.id,
                    "user_id": self.binded_member.user.id,
                    "name": self.binded_member.name,
                    "permission": "view",
                }
            ],
            "delete": [],
        }
        response = self.client.post(
            reverse("members", kwargs={"group_id": self.default_group.id}),
            data=members_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            data = response.json()
            self.assertIsInstance(data, list)
            for item in data:
                if item["name"] == self.binded_member.name:
                    member_data = MemberDataModel(**item)
                    self.assertEqual(item["permission"], "view")
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

        # can't update owner data
        members_data = {
            "create": [],
            "update": [
                {
                    "id": self.owner_member.id,
                    "user_id": None,
                    "name": self.owner_member.name,
                    "permission": "view",
                },
            ],
            "delete": [],
        }
        response = self.client.post(
            reverse("members", kwargs={"group_id": self.default_group.id}),
            data=members_data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_member(self):
        """
        Test deleting member.
        """
        members_data = {
            "create": [],
            "update": [],
            "delete": [{"id": self.binded_member.id}],
        }
        response = self.client.post(
            reverse("members", kwargs={"group_id": self.default_group.id}),
            data=members_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        # can't delete owner member
        members_data = {
            "create": [],
            "update": [],
            "delete": [{"id": self.owner_member.id}],
        }
        response = self.client.post(
            reverse("members", kwargs={"group_id": self.default_group.id}),
            data=members_data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
