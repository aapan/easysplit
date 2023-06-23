from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from account.models import Group, Member


def incorrect_format_message(except_error):
    return f"Response data format is incorrect: {str(except_error)}"


class BaseTestCase(APITestCase):
    def setUp(self):
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
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        return user
