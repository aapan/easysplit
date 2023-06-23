from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from account.models import Group, Member


def incorrect_format_message(except_error):
    """
    Generate an error message for incorrect response data format.

    This function takes an exception as input and generates an error message
    indicating that the response data format is incorrect.

    Args:
        except_error (Exception): The exception object representing the error.

    Returns:
        str: The error message indicating the incorrect response data format.
    """
    return f"Response data format is incorrect: {str(except_error)}"


class BaseTestCase(APITestCase):
    """
    Base test case for API test cases.

    This test case provides common setup and utility methods for other test cases.
    """

    def setUp(self):
        """
        Set up the test case.

        It creates a default user, logs in with the default user credentials,
        creates a default group, and creates members for the default group.
        """

        # create default user
        self.user_data = {"username": "user", "password": "user"}
        self.user = self.create_user(**self.user_data)
        self.user1 = self.create_user(username="user1", password="user1")
        self.client.login(**self.user_data)

        # create default group
        self.default_group = Group.objects.create(
            owner_id=self.user.id,
            name="Group1",
            note="",
            public_permission="limited",
            primary_currency="TWD",
        )

        # create default group's member
        self.owner_member = Member.objects.create(
            user=self.default_group.owner,
            group=self.default_group,
            name="Aaron",
            permission="edit",
        )
        self.binded_member = Member.objects.create(
            user=self.user1,
            group=self.default_group,
            name="Binded member",
            permission="edit",
        )
        self.non_binded_member = Member.objects.create(
            user=None,
            group=self.default_group,
            name="Non-binded member",
            permission="edit",
        )

    @staticmethod
    def create_user(username, password):
        """
        Create a user with the given username and password.

        Args:
            username (str): The username for the user.
            password (str): The password for the user.

        Returns:
            User: The created user object.
        """

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        return user
